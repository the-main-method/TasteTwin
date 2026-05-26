# app/stream_and_train_amazon.py

import os
import re
import json
import math
import random
from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Import engine components to enable dynamic swapping
from app.personas import PERSONAS
from app.items import ITEMS
import app.engine as engine
import app.main as main

def stream_and_parse_amazon(category="Appliances", limit=1000):
    """
    Streams actual reviews and metadata for a category from McAuley-Lab/Amazon-Reviews-2023 on Hugging Face.
    Maps them directly into the TasteTwin database schemas.
    """
    config_reviews = f"raw_review_{category}"
    config_meta = f"raw_meta_{category}"
    
    print(f"[TasteTwin Ingestion] Streaming reviews from HF McAuley-Lab/Amazon-Reviews-2023 ({config_reviews})...")
    
    # 1. Stream reviews
    reviews_stream = load_dataset(
        "McAuley-Lab/Amazon-Reviews-2023", 
        config_reviews, 
        split="full", 
        streaming=True, 
        trust_remote_code=True
    )

    raw_reviews = []
    count = 0
    needed_asins = set()
    
    for row in reviews_stream:
        uid = row.get("user_id") or row.get("reviewerID") or f"user_{random.randint(1000, 9999)}"
        asin = row.get("parent_asin") or row.get("asin")
        rating = row.get("rating") or row.get("overall") or 3.0
        text = row.get("text") or row.get("review_text") or row.get("reviewText") or row.get("content") or ""
        title = row.get("title") or row.get("summary") or ""
        
        if not asin or not text.strip():
            continue
            
        full_text = f"{title}. {text}" if title else text
        
        raw_reviews.append({
            "user_id": uid,
            "asin": asin,
            "rating": float(rating),
            "text": full_text,
            "timestamp": row.get("timestamp") or 0
        })
        needed_asins.add(asin)
        count += 1
        if count >= limit:
            break
            
    print(f"[TasteTwin Ingestion] Streamed {len(raw_reviews)} raw reviews. Extracting metadata for {len(needed_asins)} unique products...")
    
    # 2. Stream metadata matching needed ASINs
    meta_stream = load_dataset(
        "McAuley-Lab/Amazon-Reviews-2023", 
        config_meta, 
        split="full", 
        streaming=True, 
        trust_remote_code=True
    )
        
    meta_map = {}
    meta_count = 0
    scanned_count = 0
    
    for row in meta_stream:
        scanned_count += 1
        
        # Avoid hanging if some ASINs are missing from metadata
        if scanned_count > 50000:
            print(f"[TasteTwin Ingestion] Scanned 50,000 metadata rows. Stopping early to prevent hanging.")
            break
            
        asin = row.get("parent_asin") or row.get("asin")
        if not asin:
            continue
            
        # We only ingest metadata for products in our review stream to ensure high overlap
        if asin not in needed_asins:
            continue
            
        if asin in meta_map:
            continue
            
        title = row.get("title") or f"Amazon Product {asin}"
        desc_val = row.get("description") or row.get("description_text") or ""
        if isinstance(desc_val, list):
            desc = " ".join(desc_val)
        else:
            desc = str(desc_val)
            
        price_val = row.get("price") or 15.0
        price = 15.0
        if isinstance(price_val, (int, float)):
            price = float(price_val)
        elif isinstance(price_val, str):
            price_match = re.search(r'([\d.]+)', price_val)
            if price_match:
                price = float(price_match.group(1))
                
        # Category classification
        cats = row.get("categories") or row.get("category") or ["appliances"]
        if isinstance(cats, list):
            cat_str = " ".join([str(c) for c in cats]).lower()
        else:
            cat_str = str(cats).lower()
            
        category = "electronics" # Appliances default
        if any(x in cat_str for x in ["food", "restaurant", "grocery", "snack", "cook"]):
            category = "food"
        elif any(x in cat_str for x in ["book", "kindle", "literature", "novel"]):
            category = "books"
        elif any(x in cat_str for x in ["drink", "wine", "beer", "soda", "beverage"]):
            category = "drinks"
        elif any(x in cat_str for x in ["clothing", "shoes", "fashion", "dress", "jewelry", "beauty"]):
            category = "fashion"
            
        features = row.get("features") or row.get("feature") or []
        if isinstance(features, str):
            features = [features]
        elif not isinstance(features, list):
            features = []
            
        meta_map[asin] = {
            "id": asin,
            "title": title,
            "category": category,
            "price": price,
            "currency": "USD",
            "description": desc or f"Amazon product in the {category} category.",
            "features": features[:4] if features else ["Premium build design", "Advanced performance utility"],
            "complaints": [],
            "avg_rating": 4.0
        }
        meta_count += 1
        # Stop early if we matched all needed ASINs
        if len(meta_map) >= len(needed_asins):
            break
            
    print(f"[TasteTwin Ingestion] Matched metadata for {len(meta_map)} products.")
    
    # 3. Consolidate: Keep reviews with valid metadata
    valid_reviews = [r for r in raw_reviews if r["asin"] in meta_map]
    print(f"[TasteTwin Ingestion] Retained {len(valid_reviews)} fully-grounded reviews.")
    
    if not valid_reviews:
        raise RuntimeError("No overlapping reviews and metadata found in the streamed data split.")
        
    # 4. Extract Complaints and Features dynamically from reviews
    product_reviews = {}
    for r in valid_reviews:
        product_reviews.setdefault(r["asin"], []).append(r)
        
    for asin, item in meta_map.items():
        revs = product_reviews.get(asin, [])
        if not revs:
            continue
        # Regularized Average Rating (Bayesian shrinkage with global prior of 4.1 stars and strength 3)
        total_sum = sum(x["rating"] for x in revs)
        regularized_avg = (total_sum + 3 * 4.1) / (len(revs) + 3)
        item["avg_rating"] = round(regularized_avg, 2)
        
        # Complaints from low reviews
        low_revs = [x for x in revs if x["rating"] <= 3]
        complaints = []
        for r in low_revs:
            first_sent = re.split(r'[.!?]\s+', r["text"])[0].strip()
            if len(first_sent) > 10 and len(first_sent) < 80:
                complaints.append(first_sent)
        item["complaints"] = list(set(complaints))[:2]
        if not item["complaints"]:
            item["complaints"] = ["High price barrier for budget users", "Slight logistics delay under peak seasons"]
            
        # Features from high reviews
        high_revs = [x for x in revs if x["rating"] >= 4]
        features = list(item["features"])
        for r in high_revs:
            first_sent = re.split(r'[.!?]\s+', r["text"])[0].strip()
            if len(first_sent) > 10 and len(first_sent) < 80 and first_sent not in features:
                features.append(first_sent)
        item["features"] = list(set(features))[:4]
        
    # 5. Build Personas by grouping reviews by user
    user_groups = {}
    for r in valid_reviews:
        user_groups.setdefault(r["user_id"], []).append(r)
        
    # Filter to users with at least 2 reviews to allow realistic collaborative mapping
    # If not enough, lower threshold to 1 review
    min_reviews = 2
    active_users = {uid: revs for uid, revs in user_groups.items() if len(revs) >= min_reviews}
    if len(active_users) < 10:
        min_reviews = 1
        active_users = user_groups
        
    new_personas = []
    
    # Names database to synthesize realistic profiles
    nigerian_names = ["Chinedu", "Amina", "Oluwaseun", "Efe", "Emeka", "Tari", "Kelechi", "Tunde", "Fatimah", "Ngozi"]
    western_names = ["Alexander", "Sophie", "Liam", "Emma", "Noah", "Olivia", "James", "Ava", "William", "Isabella"]
    
    for uid, revs in active_users.items():
        hist = []
        categories_visited = set()
        prices_paid = []
        ratings = []
        total_words = 0
        
        for r in revs:
            item = meta_map[r["asin"]]
            hist.append({
                "item_name": item["title"],
                "category": item["category"],
                "price": item["price"],
                "rating": int(r["rating"]),
                "text": r["text"]
            })
            categories_visited.add(item["category"])
            prices_paid.append(item["price"])
            ratings.append(r["rating"])
            total_words += len(r["text"].split())
            
        # Synthesize user DNA
        avg_rating = sum(ratings) / len(ratings) if ratings else 4.0
        avg_price = sum(prices_paid) / len(prices_paid) if prices_paid else 15.0
        avg_words = total_words / len(revs) if revs else 30.0
        
        # 1. Strictness: Inverse of average rating
        strictness_val = round(max(10.0, min(95.0, 100.0 - (avg_rating * 18.0))), 1)
        
        # 2. Budget: Proportional to low prices
        # In Appliances, high price is > $100. If avg_price is high, budget sensitivity is low
        budget_val = round(max(10.0, min(95.0, 100.0 - (avg_price / 2.0))), 1)
        
        # 3. Novelty: Proportional to category exploration
        novelty_val = round(min(95.0, max(15.0, len(categories_visited) * 40.0 + random.randint(-10, 10))), 1)
        
        # 4. Expressiveness: Proportional to word length
        expressive_val = round(max(10.0, min(95.0, avg_words * 0.8)), 1)
        
        # 5. Sarcasm
        sarcasm_val = round(float(random.randint(25, 80)), 1)
        
        # 6. Naija scale (allow some localized testing)
        naija_scale = round(float(random.choice([15.0, 45.0, 80.0])), 1)
        
        # Categories affinities
        affinities = {"electronics": 0.5, "books": 0.5, "food": 0.5, "drinks": 0.5, "fashion": 0.5}
        for cat in categories_visited:
            affinities[cat] = 0.9
            
        # Select realistic name
        name_pool = nigerian_names if naija_scale > 60 else western_names
        name = f"{random.choice(name_pool)} ({uid[:6]})"
        
        # Style examples from history
        style_examples = [re.split(r'[.!?]\s+', r["text"])[0].strip() for r in revs if len(r["text"]) > 10]
        
        new_personas.append({
            "id": uid,
            "name": name,
            "domain": hist[0]["category"] if hist else "electronics",
            "description": f"Verified Amazon reviewer with {len(hist)} catalog interactions, focusing primarily on {hist[0]['category']}.",
            "rating_bias": round(avg_rating - 4.0, 2),
            "category_affinity": affinities,
            "verbosity": "verbose" if avg_words > 60 else "concise",
            "tone": "sarcastic" if sarcasm_val > 60 else "earnest",
            "recent_mood": "frustrated" if avg_rating < 3.0 else "happy",
            "taste_drift": 0.05,
            "preferred_aspects": ["utility", "quality"] if avg_price > 50 else ["price"],
            "pain_points": ["price"] if budget_val > 60 else ["quality"],
            "style_examples": style_examples[:3] if style_examples else ["Good purchase.", "Decent utility abeg."],
            "dna": {
                "budget": budget_val,
                "novelty": novelty_val,
                "sarcasm": sarcasm_val,
                "expressive": expressive_val,
                "strictness": strictness_val,
                "naija_scale": naija_scale
            },
            "history": hist
        })
        
    print(f"[TasteTwin Ingestion] Synthesized {len(new_personas)} rich customer personas from real Amazon history.")
    
    return new_personas, list(meta_map.values())

def swap_to_amazon_dataset(category="Appliances", limit=1000):
    """
    Ingests Amazon reviews, swaps the active global database registers in-memory,
    precomputes 32D high-fidelity embeddings, and runs coordinate descent optimization.
    """
    try:
        new_personas, new_items = stream_and_parse_amazon(category=category, limit=limit)
        
        # 1. Swapping global tables
        PERSONAS.clear()
        PERSONAS.extend(new_personas)
        
        ITEMS.clear()
        ITEMS.extend(new_items)
        
        print(f"[TasteTwin Core] Dynamic Database Swap Complete. Active PERSONAS={len(PERSONAS)}, ITEMS={len(ITEMS)}.")
        
        # 2. Refitting NLP Vectorizers
        print("[TasteTwin Core] Refitting TF-IDF Vectorizers on Amazon corpus...")
        engine.init_tfidf_vectorizer()
        main.init_parser_vectorizer()
        
        # 3. Coordinate Descent Optimization
        print("[TasteTwin Core] Training RMSE Predictor weights on new Amazon database...")
        rmse, logs = engine.optimize_predictor_weights()
        print(f"[TasteTwin Core] Training Complete. Converged RMSE: {rmse:.4f}")
        for log in logs:
            print(f"  {log}")
            
        # Export trained weights
        weights_path = os.path.join("app", "trained_weights.json")
        with open(weights_path, "w") as f:
            json.dump(engine.TRAINED_WEIGHTS, f, indent=2)
        print(f"[TasteTwin Core] Exported trained weights successfully to {weights_path}")
        
        return {
            "status": "success",
            "category": category,
            "personas_count": len(PERSONAS),
            "items_count": len(ITEMS),
            "optimized_rmse": rmse,
            "weights": engine.TRAINED_WEIGHTS,
            "logs": logs
        }
        
    except Exception as e:
        print(f"[TasteTwin Core ERROR] Ingestion & Optimization pipeline failed: {str(e)}")
        raise e

if __name__ == "__main__":
    # Test script run
    print("[TasteTwin Pipeline] Running pipeline test...")
    swap_to_amazon_dataset(category="Appliances", limit=200)
