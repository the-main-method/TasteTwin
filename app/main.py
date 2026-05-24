# app/main.py

import os
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

import re
import json
import random

from app.personas import PERSONAS, get_persona_by_id
from app.items import ITEMS, get_item_by_id
from app.engine import (
    TasteTwinEngine,
    run_leave_one_out_evaluation,
    optimize_predictor_weights,
    calculate_similar_user_neighborhood,
    calculate_taste_graph,
    modulate_pidgin,
    predict_rating_heuristically,
    compile_heuristic_review,
    GENAI_AVAILABLE,
    OPENAI_AVAILABLE,
    calculate_behavioral_consistency,
    compute_taste_drift
)

app = FastAPI(
    title="TasteTwin AI — Behavioral Intelligence Engine",
    description="DSN x BCT LLM Agent Challenge Web App and API endpoint",
    version="1.0.0"
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------------------
# PYDANTIC SCHEMAS
# ----------------------------------------------------------------------

class ConfigRequest(BaseModel):
    provider: str
    api_key: Optional[str] = None

class CustomDNAModel(BaseModel):
    budget: float
    novelty: float
    sarcasm: float
    expressive: float
    strictness: float
    naija_scale: float

class CustomPersonaModel(BaseModel):
    name: str
    domain: str
    description: str
    dna: CustomDNAModel
    history: List[Dict[str, Any]]

class CustomItemModel(BaseModel):
    title: str
    category: str
    price: float
    currency: str
    description: str
    features: List[str]
    complaints: Optional[List[str]] = []
    avg_rating: Optional[float] = 4.0

class SimulateReviewRequest(BaseModel):
    persona_id: str
    item_id: str
    provider: Optional[str] = "heuristic"
    api_key: Optional[str] = None
    custom_persona: Optional[CustomPersonaModel] = None
    custom_item: Optional[CustomItemModel] = None

class RecommendRequest(BaseModel):
    persona_id: str
    category_filter: Optional[str] = "all"
    provider: Optional[str] = "heuristic"
    api_key: Optional[str] = None
    custom_persona: Optional[CustomPersonaModel] = None

# Global Engine instance
engine = TasteTwinEngine()

# ----------------------------------------------------------------------
# NEW SCHEMAS & HELPERS
# ----------------------------------------------------------------------

class IngestDatasetRequest(BaseModel):
    content: str

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatbotRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []
    current_dna: CustomDNAModel
    provider: Optional[str] = "heuristic"
    api_key: Optional[str] = None

class CustomDescriptionRequest(BaseModel):
    description: str
    type: str  # "persona" or "item"
    provider: Optional[str] = "heuristic"
    api_key: Optional[str] = None

class LoadAmazonRequest(BaseModel):
    category: Optional[str] = "Appliances"
    limit: Optional[int] = 1000

class ColdStartRequest(BaseModel):
    description: str
    provider: Optional[str] = "heuristic"
    api_key: Optional[str] = None



# ----------------------------------------------------------------------
# NLP REFERENCE DATABASES & VECTOR SPACE PARSER INITS
# ----------------------------------------------------------------------
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

DNA_REFERENCES = {
    "budget": {
        "high": "budget conscious broke saving money expensive inflation student cheap cost price value wallet economy kobo naira computer village tight budget cut cost cheap deals low price pocket friendly extremely budget conscious",
        "low": "luxury wealthy premium expensive rich any price unconcerned with budget luxury opulent affluent high-end balling VIP Lekki expensive fine dining gold signature bespoke custom dollar splurge"
    },
    "novelty": {
        "high": "adventurous variety explore new curious experimental novel different try everything change discover curiosity seeker surprise me unexpected brands new categories wild different choices",
        "low": "routine familiar traditional same standard habit classic stick to what I know safety comfort consistent routine comfort zone established brand classic standard consistent choices"
    },
    "sarcasm": {
        "high": "sarcastic dry humor savage funny ironic cynical joke witty mockery critical banter sass mocking comedy savage review cynical remarks dry wit sarcasm irony",
        "low": "serious polite formal earnest respectful straightforward gentle quiet humble analytical direct polite tone honest feedback serious review gentle critique"
    },
    "expressive": {
        "high": "verbose detailed long reviews paragraphs chatty essay write a lot lengthy feedback talking wordy comprehensive complete breakdown exhaustively multi-paragraph writeups",
        "low": "concise short reviews brief lazy simple direct word or two minimal silent lazy writing straight to the point short feedback direct rating short direct feedback"
    },
    "strictness": {
        "high": "strict demanding perfectionist critical harsh hard to please zero tolerance high standards picky difficult unforgiving strict reviewer perfection expectation minor flaws count",
        "low": "generous easy going lenient soft forgiving gentle positive loose soft-hearted relaxed lenient easy-to-please easygoing tolerant soft review"
    },
    "naija_scale": {
        "high": "nigerian lagos pidgin local naira zobo jollof traffic abeg omo sha kobo computer village nepa Abuja street mainland Lekki Ikeja dispatch kilishi chin chin grill chop local context",
        "low": "american western US-based standard English foreign london states abroad overseas white burger fries steak dollar pound Euro standard accent foreign context standard english"
    }
}

CATEGORY_REFERENCES = {
    "electronics": "electronics tech battery charge device power solar headphones camera screen utility hardware router computer accessory wiring gadget powerup soundvibe cables charging electrical inverters backup generator computer village",
    "food": "food restaurant eat cook spicy jollof soup waffle kitchen dining delicious tasty grill bistro dinner meal calorie plate recipe burger comfort Lekki bistro calorie Calabar kitchen dessert waffle pepper rice",
    "books": "books read novel literature prose author pages cover fiction thriller biography poetry book shelf chapter plot reading history story paperback Akwaeke Emezi Vivek Oji Kaduna Abubakar prose style",
    "drinks": "drinks wine beer soda alcohol bottle gin cognac beverage zobo refreshment sip cocktail spirits bar pub club pub juice cup VSOP champagne cognac hibiscus craft gin stout lager brew zobo mix",
    "fashion": "fashion wear clothing dress shirt shoes fabric silk leather sandals luxury outfit style designer stitch sewing fashion purse kaftan silk wrap orange cotton heel bag premium fabric wear"
}

# We initialize a local parser vectorizer with a larger vocabulary
PARSER_VECTORIZER = TfidfVectorizer(stop_words='english')

def init_parser_vectorizer():
    corpus = []
    # Add descriptions of catalog items
    for item in ITEMS:
        txt = f"{item.get('title', '')} {item.get('category', '')} {item.get('description', '')} " \
              f"{' '.join(item.get('features', []))} {' '.join(item.get('complaints', []))}"
        corpus.append(txt)
    # Add descriptions and reviews from personas
    for persona in PERSONAS:
        hist_txt = " ".join([r.get('text', '') for r in persona.get('history', [])])
        txt = f"{persona.get('name', '')} {persona.get('description', '')} {hist_txt}"
        corpus.append(txt)
    # Add references
    for key, ref in DNA_REFERENCES.items():
        corpus.append(ref["high"])
        corpus.append(ref["low"])
    for key, ref in CATEGORY_REFERENCES.items():
        corpus.append(ref)
        
    try:
        PARSER_VECTORIZER.fit(corpus)
    except Exception as e:
        print(f"Error fitting PARSER_VECTORIZER: {e}")

# Initialize parser vectorizer
init_parser_vectorizer()

def compute_cosine_sim_text(t1: str, t2: str) -> float:
    try:
        vectors = PARSER_VECTORIZER.transform([t1, t2]).toarray()
        v1, v2 = vectors[0], vectors[1]
        dot = np.dot(v1, v2)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(dot / (norm1 * norm2))
    except Exception:
        return 0.0

def matches_any(text: str, patterns: List[str]) -> bool:
    text_l = text.lower()
    for pat in patterns:
        if " " in pat:
            if pat in text_l:
                return True
        else:
            if re.search(r'\b' + re.escape(pat) + r'\b', text_l):
                return True
    return False

def parse_persona_description_heuristically(desc: str) -> Dict[str, float]:
    dna = {
        "budget": 50.0,
        "novelty": 50.0,
        "sarcasm": 50.0,
        "expressive": 50.0,
        "strictness": 50.0,
        "naija_scale": 50.0
    }
    desc_l = desc.lower()
    
    for k, ref in DNA_REFERENCES.items():
        sim_high = compute_cosine_sim_text(desc_l, ref["high"])
        sim_low = compute_cosine_sim_text(desc_l, ref["low"])
        
        if sim_high == 0.0 and sim_low == 0.0:
            dna[k] = 50.0
        else:
            diff = sim_high - sim_low
            # Scale difference dynamically centered at 50, amplified to project extremes nicely
            slider_val = 50.0 + diff * 150.0
            dna[k] = round(max(5.0, min(95.0, slider_val)), 1)
            
    return dna

def parse_item_description_heuristically(desc: str) -> Dict[str, Any]:
    desc_l = desc.lower()
    
    # 1. Classify Category based on Cosine Similarity against reference vectors
    best_cat = "electronics"
    max_sim = -1.0
    for cat, ref in CATEGORY_REFERENCES.items():
        sim = compute_cosine_sim_text(desc_l, ref)
        if sim > max_sim:
            max_sim = sim
            best_cat = cat
            
    # 2. Extract Price & Currency via Regex
    price = 15000.0
    currency = "NGN"
    price_match = re.search(r'(?:ngn|naira|n|₦)\s*([\d,]+(?:\.\d+)?)', desc_l)
    if price_match:
        price = float(price_match.group(1).replace(",", ""))
    else:
        usd_match = re.search(r'(?:usd|\$)\s*([\d,]+(?:\.\d+)?)', desc_l)
        if usd_match:
            price = float(usd_match.group(1).replace(",", ""))
            currency = "USD"
        else:
            # Mathematical priors based on category averages
            avg_prices = {
                "electronics": 95000.0,
                "food": 12000.0,
                "books": 8000.0,
                "drinks": 20000.0,
                "fashion": 35000.0
            }
            price = avg_prices.get(best_cat, 15000.0)
            
    # 3. Split sentences and extract Features & Complaints semantically
    sentences = [s.strip() for s in re.split(r'[.!?]\s+', desc) if s.strip()]
    
    feature_ref = "excellent great durable feature premium support high quality solid works well perfect beautiful love positive nice design specifications capacity robust"
    complaint_ref = "defect complaint issue bad slow delay expensive noise broke failed glitch drawback error flaw disappointed stiff annoying warning fragile lag"
    
    scored_features = []
    scored_complaints = []
    
    for sent in sentences:
        if len(sent.split()) < 3:
            continue
        sim_f = compute_cosine_sim_text(sent.lower(), feature_ref)
        sim_c = compute_cosine_sim_text(sent.lower(), complaint_ref)
        scored_features.append((sent, sim_f))
        scored_complaints.append((sent, sim_c))
        
    scored_features.sort(key=lambda x: x[1], reverse=True)
    scored_complaints.sort(key=lambda x: x[1], reverse=True)
    
    features = []
    for sent, score in scored_features:
        if score > 0.02 and sent not in features:
            features.append(sent[:60])
        if len(features) >= 3:
            break
            
    if not features:
        features = ["Premium quality material", "User-friendly interface", "Long lasting utility"]
        
    complaints = []
    for sent, score in scored_complaints:
        # Avoid duplicating features in complaints
        if score > 0.02 and sent not in features and sent not in complaints:
            complaints.append(sent[:60])
        if len(complaints) >= 2:
            break
            
    if not complaints:
        complaints = ["Slightly expensive in this economy", "Delivery might take small time"]
        
    title = "Custom Product"
    title_match = re.search(r'^([^\n.!?]+)', desc)
    if title_match:
        title = title_match.group(1).strip()[:40]
        
    return {
        "title": title,
        "category": best_cat,
        "price": price,
        "currency": currency,
        "description": desc,
        "features": features,
        "complaints": complaints,
        "avg_rating": 4.0
    }

def parse_custom_description_with_llm(provider: str, api_key: str, desc: str, desc_type: str) -> Dict[str, Any]:
    system_instr = "You are a professional text parser. Extract JSON metadata from the provided description."
    
    if desc_type == "persona":
        prompt = f"""
        Extract a structured personality DNA from the following persona description:
        "{desc}"
        
        Output a valid JSON object matching this structure EXACTLY:
        {{
          "name": "Extract a suitable name based on description",
          "dna": {{
            "budget": 50.0,
            "novelty": 50.0,
            "sarcasm": 50.0,
            "expressive": 50.0,
            "strictness": 50.0,
            "naija_scale": 50.0
          }}
        }}
        Do NOT wrap in markdown code blocks. Only return the raw JSON block.
        """
    else:
        prompt = f"""
        Extract product specifications from the following item description:
        "{desc}"
        
        Output a valid JSON object matching this structure EXACTLY:
        {{
          "title": "Suitable title",
          "category": "electronics", // must be one of: electronics, food, books, drinks, fashion
          "price": 12000.0,
          "currency": "NGN", // NGN or USD
          "description": "...",
          "features": ["feature 1", "feature 2", "feature 3"],
          "complaints": ["complaint 1", "complaint 2"]
        }}
        Do NOT wrap in markdown code blocks. Only return the raw JSON block.
        """
        
    from app.engine import run_groq_agent, run_gemini_agent, run_openai_agent
    if provider == "groq":
        resp = run_groq_agent(api_key, prompt, system_instr)
    elif provider == "gemini" and GENAI_AVAILABLE:
        resp = run_gemini_agent(api_key, prompt, system_instr)
    elif provider == "openai" and OPENAI_AVAILABLE:
        resp = run_openai_agent(api_key, prompt, system_instr)
    else:
        raise Exception("API provider not available.")
        
    json_match = re.search(r'\{.*\}', resp, re.DOTALL)
    if json_match:
        return json.loads(json_match.group(0))
    else:
        raise Exception("Failed to parse JSON response from LLM parser.")

def run_chatbot_heuristically(message: str, current_dna: Dict[str, float]) -> Dict[str, Any]:
    msg_l = message.lower()
    dna = current_dna.copy()
    shifts = []
    
    # 1. Identify which slider has the highest semantic similarity to the user's message
    active_slider = None
    max_affinity = 0.0
    for k, ref in DNA_REFERENCES.items():
        sim_h = compute_cosine_sim_text(msg_l, ref["high"])
        sim_l = compute_cosine_sim_text(msg_l, ref["low"])
        affinity = sim_h + sim_l
        if affinity > max_affinity:
            max_affinity = affinity
            active_slider = k
            
    # 2. Adjust slider value dynamically based on direction
    if active_slider and max_affinity > 0.04:
        sim_h = compute_cosine_sim_text(msg_l, DNA_REFERENCES[active_slider]["high"])
        sim_l = compute_cosine_sim_text(msg_l, DNA_REFERENCES[active_slider]["low"])
        
        # Step size proportional to how strongly they expressed the preference in text
        step = round(min(25.0, max_affinity * 100.0), 1)
        if step < 5.0:
            step = 12.0
            
        if sim_h > sim_l:
            dna[active_slider] = round(min(100.0, dna[active_slider] + step), 1)
            shifts.append(f"{active_slider.capitalize()} increased by {step}%")
        else:
            dna[active_slider] = round(max(0.0, dna[active_slider] - step), 1)
            shifts.append(f"{active_slider.capitalize()} decreased by {step}%")
    else:
        # Subtle default shift
        active_slider = random.choice(list(DNA_REFERENCES.keys()))
        
    # 3. Formulate interview questions dynamically
    # Choose a question from a slider that is NOT the currently modified slider to probe the user next
    candidate_sliders = [k for k in DNA_REFERENCES.keys() if k != active_slider]
    next_slider = random.choice(candidate_sliders)
    
    raw_question = ""
    
    if next_slider == "budget":
        # Sort items by NGN equivalent price to find cheapest and most expensive
        def get_ngn_price(it):
            p = it.get("price", 10000.0)
            if it.get("currency") == "USD":
                return p * 1500.0
            return p
        sorted_items = sorted(ITEMS, key=get_ngn_price)
        cheapest_item = sorted_items[0]
        expensive_item = sorted_items[-1]
        raw_question = (
            f"Looking at our active catalog, would you prefer a budget-friendly option like '{cheapest_item['title']}' for {cheapest_item['currency']}{cheapest_item['price']:,.0f}, "
            f"or is a premium high-end choice like '{expensive_item['title']}' for {expensive_item['currency']}{expensive_item['price']:,.0f} more your speed?"
        )
        
    elif next_slider == "novelty":
        # Randomly select a product and its category
        random_item = random.choice(ITEMS)
        cat = random_item["category"]
        raw_question = (
            f"If we are picking items, would you want to stick to familiar standard domains, or are you down to explore '{random_item['title']}' in the '{cat}' category to try something totally new?"
        )
        
    elif next_slider == "strictness":
        # Find a product with active user complaints
        items_with_complaints = [it for it in ITEMS if it.get("complaints")]
        selected_item = random.choice(items_with_complaints) if items_with_complaints else ITEMS[0]
        complaint = random.choice(selected_item["complaints"]) if selected_item.get("complaints") else "any minor delay or flaw"
        raw_question = (
            f"If you purchased '{selected_item['title']}' and encountered this specific issue: '{complaint.lower()}', "
            f"would that be an immediate dealbreaker for you, or are you generally easygoing and lenient with minor product defects?"
        )
        
    elif next_slider == "sarcasm":
        # Query user feedback style preferences using sarcasm extremes in actual personas
        sarcastic_persona = max(PERSONAS, key=lambda p: p["dna"]["sarcasm"])
        polite_persona = min(PERSONAS, key=lambda p: p["dna"]["sarcasm"])
        raw_question = (
            f"When giving product feedback, do you prefer serious, polite, and detailed reviews like '{polite_persona['name']}', "
            f"or do you lean into dry sarcasm and savage humor like '{sarcastic_persona['name']}' when a brand fails you?"
        )
        
    elif next_slider == "expressive":
        # Query user review length preferences using expressive extremes in actual personas
        expressive_persona = max(PERSONAS, key=lambda p: p["dna"]["expressive"])
        concise_persona = min(PERSONAS, key=lambda p: p["dna"]["expressive"])
        raw_question = (
            f"When reviewing a purchase, do you write comprehensive, long specification essays like '{expressive_persona['name']}', "
            f"or do you keep it extremely direct and short like '{concise_persona['name']}'?"
        )
        
    elif next_slider == "naija_scale":
        # Find a local power utility product or local factors in the catalog
        local_refs = "solar inverter power backup nepa delivery jollof zobo chin chin soup lagos traffic computer village"
        scored_items = []
        for it in ITEMS:
            txt = f"{it.get('title', '')} {it.get('description', '')}".lower()
            sim = compute_cosine_sim_text(txt, local_refs)
            scored_items.append((it, sim))
        scored_items.sort(key=lambda x: x[1], reverse=True)
        local_item = scored_items[0][0] if scored_items else ITEMS[0]
        raw_question = (
            f"How much do practical local realities—like NEPA power issues, generator costs, or Lagos traffic delays—impact your buying decisions, "
            f"as seen in items like '{local_item['title']}'?"
        )
        
    # 4. Modulate tone using Lekki/Lagos organic rhythm if naija_scale is high
    naija_scale = dna.get("naija_scale", 50.0)
    
    if shifts:
        base_replies = [
            f"That makes a lot of sense. I have adjusted your profile settings to reflect this: {shifts[0]}. Out of curiosity: {raw_question}",
            f"Understood! Your Taste DNA parameters have been successfully updated: {shifts[0]}. Let's discuss: {raw_question}",
            f"I see exactly what you mean. Adjusting your profile: {shifts[0]}. Tell me, please: {raw_question}"
        ]
    else:
        base_replies = [
            f"I completely understand your perspective. Your DNA profile looks stable. Out of curiosity: {raw_question}",
            f"Understood! Taste DNA parameters are solid. Let's discuss: {raw_question}"
        ]
        
    base_reply = random.choice(base_replies)
    reply = modulate_pidgin(base_reply, naija_scale)
        
    explanation = " | ".join(shifts) if shifts else "Analyzed message semantics; sliders kept stable."
    
    return {
        "reply": reply,
        "updated_dna": dna,
        "explanation": explanation
    }

def run_chatbot_with_llm(provider: str, api_key: str, message: str, history: List[ChatMessage], current_dna: Dict[str, float]) -> Dict[str, Any]:
    system_instr = (
        "You are an expert agentic psychologist and digital twin profiler. Your job is to interview the user to refine their Taste DNA. "
        "CRITICAL INSTRUCTION: You must evaluate ONLY the USER'S messages to adjust the Taste DNA sliders. Do NOT look at the chatbot's (assistant's) own previous responses or pidgin words to adjust the 'naija_scale'. The 'naija_scale' should represent ONLY the user's own local affinity. If the user's message is formal or lacks pidgin entirely, aggressively DECREASE the naija_scale towards 0. "
        "Your responses must be highly intelligent, engaging, and localized (incorporate organic Nigerian expressions like omo, abeg, makes sense, sha, etc., if appropriate). "
        "You will analyze the user's latest message, adjust their 6 DNA sliders (budget, novelty, sarcasm, expressive, strictness, naija_scale) between 0 and 100, "
        "and return a response in strict JSON format."
    )
    
    hist_formatted = "\n".join([f"{'USER' if h.role == 'user' else 'ASSISTANT'}: {h.content}" for h in history])
    
    prompt = f"""
    CURRENT TASTE DNA:
    {current_dna}
    
    CONVERSATION HISTORY (FOR CONTEXT ONLY):
    {hist_formatted}
    
    [CRITICAL] USER'S LATEST MESSAGE (ANALYZE THIS FOR DNA SHIFTS):
    "{message}"
    
    GUIDELINES:
    1. Respond to the user's message, asking them a follow-up question to probe another aspect of their personality (e.g. price vs premium, new vs familiar, response to bad customer service).
    2. Adjust the sliders based on the context clues (e.g. if they mention being budget-minded, increase budget; if they code-switch into Nigerian expressions, increase naija_scale). Evaluate ONLY the user's messages to adjust sliders, ignoring your own words or local dialect.
    3. Output your response as a strict JSON object matching this structure EXACTLY:
    {{
      "reply": "Conversational response to user...",
      "updated_dna": {{
        "budget": 50.0,
        "novelty": 50.0,
        "sarcasm": 50.0,
        "expressive": 50.0,
        "strictness": 50.0,
        "naija_scale": 50.0
      }},
      "explanation": "Brief explanation of which sliders shifted and why."
    }}
    Do NOT include any markdown code blocks outside of the JSON itself.
    """
    
    from app.engine import run_groq_agent, run_gemini_agent, run_openai_agent
    if provider == "groq":
        resp = run_groq_agent(api_key, prompt, system_instr)
    elif provider == "gemini" and GENAI_AVAILABLE:
        resp = run_gemini_agent(api_key, prompt, system_instr)
    elif provider == "openai" and OPENAI_AVAILABLE:
        resp = run_openai_agent(api_key, prompt, system_instr)
    else:
        raise Exception("API provider not available.")
        
    json_match = re.search(r'\{.*\}', resp, re.DOTALL)
    if json_match:
        return json.loads(json_match.group(0))
    else:
        raise Exception("Failed to parse JSON response from LLM chatbot.")


# ----------------------------------------------------------------------
# REST API ENDPOINTS
# ----------------------------------------------------------------------

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "TasteTwin AI Engine"}

@app.get("/api/personas")
def get_all_personas():
    """Returns the list of available personas in our database with injected dynamic twin parameters."""
    extended_personas = []
    for p in PERSONAS:
        p_copy = p.copy()
        p_copy["bcs"] = calculate_behavioral_consistency(p)
        drift_val, _, _ = compute_taste_drift(p)
        p_copy["taste_drift"] = drift_val
        extended_personas.append(p_copy)
    return extended_personas

@app.get("/api/items")
def get_all_items():
    """Returns the list of products/items in our database."""
    return ITEMS

@app.post("/api/simulate-review")
def api_simulate_review(req: SimulateReviewRequest):
    """
    TASK A: User Modeling
    Simulates a realistic star rating, review text, and inner monologue for a user-item combo.
    """
    try:
        engine.set_credentials(req.provider, req.api_key)
        c_persona = req.custom_persona.dict() if req.custom_persona else None
        c_item = req.custom_item.dict() if req.custom_item else None
        
        result = engine.simulate_user_review(
            persona_id=req.persona_id,
            item_id=req.item_id,
            custom_persona=c_persona,
            custom_item=c_item
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")

@app.post("/api/recommend")
def api_recommend_items(req: RecommendRequest):
    """
    TASK B: Intelligent Recommendation
    Delivers cross-domain, explainable recommendations ranked via a Multi-Agent debate.
    """
    try:
        engine.set_credentials(req.provider, req.api_key)
        c_persona = req.custom_persona.dict() if req.custom_persona else None
        
        result = engine.recommend_items(
            persona_id=req.persona_id,
            category_filter=req.category_filter,
            custom_persona=c_persona
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {str(e)}")

@app.get("/api/evaluate")
def api_evaluate():
    """
    Runs leave-one-out cross-validation across all personas to report
    RMSE, Lexical ROUGE-L, Hit Rate@5, and NDCG@5.
    """
    try:
        return run_leave_one_out_evaluation()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")

@app.post("/api/train-weights")
def api_train_weights():
    """
    Runs coordinate descent training on active dataset to optimize prediction parameters.
    """
    try:
        rmse, logs = optimize_predictor_weights()
        return {"rmse": rmse, "logs": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training weights failed: {str(e)}")

@app.get("/api/taste-map")
def api_taste_map(persona_id: str):
    """
    Generates collaborative K-NN similarity scores and builds the nodes/edges Taste Graph.
    """
    try:
        persona = get_persona_by_id(persona_id)
        if not persona:
            raise HTTPException(status_code=404, detail="Persona not found")
        neighbors = calculate_similar_user_neighborhood(persona)
        graph = calculate_taste_graph(persona)
        return {"neighbors": neighbors, "graph": graph}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Taste Map construction failed: {str(e)}")

@app.post("/api/ingest-dataset")
def api_ingest_dataset(req: IngestDatasetRequest):
    """
    Streaming drag-and-drop JSONL dataset ingestion.
    Appends elements directly into the active in-memory corpus database.
    """
    try:
        lines = req.content.strip().split("\n")
        ingested_personas = 0
        ingested_items = 0
        
        for line in lines:
            if not line.strip():
                continue
            data = json.loads(line)
            
            # Simple heuristic detection of schema
            if "dna" in data and "history" in data:
                # Persona schema
                if not any(p["id"] == data["id"] for p in PERSONAS):
                    PERSONAS.append(data)
                    ingested_personas += 1
            elif "features" in data and "category" in data:
                # Item schema
                if not any(i["id"] == data["id"] for i in ITEMS):
                    ITEMS.append(data)
                    ingested_items += 1
                    
        return {
            "status": "success",
            "ingested_personas": ingested_personas,
            "ingested_items": ingested_items,
            "total_personas": len(PERSONAS),
            "total_items": len(ITEMS)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ingestion failed: {str(e)}")

@app.post("/api/parse-custom-description")
def api_parse_custom_description(req: CustomDescriptionRequest):
    """
    Parses natural language custom profile or item description into Taste DNA/Item schemas.
    """
    try:
        if req.provider in ["groq", "gemini", "openai"] and req.api_key:
            parsed = parse_custom_description_with_llm(req.provider, req.api_key, req.description, req.type)
        else:
            if req.type == "persona":
                dna = parse_persona_description_heuristically(req.description)
                parsed = {
                    "name": "Custom Profile",
                    "dna": dna
                }
            else:
                parsed = parse_item_description_heuristically(req.description)
        return parsed
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Description parsing failed: {str(e)}")

@app.post("/api/load-amazon")
def api_load_amazon(req: LoadAmazonRequest):
    """
    Ingests and Swap database registers with actual Hugging Face Amazon Reviews 2023 dataset,
    re-fits TF-IDF vectorizers, and optimizes predictor weights via Coordinate Descent.
    """
    try:
        from app.stream_and_train_amazon import swap_to_amazon_dataset
        result = swap_to_amazon_dataset(category=req.category, limit=req.limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hugging Face Amazon Ingestion & Optimization failed: {str(e)}")

@app.post("/api/cold-start")
def api_cold_start(req: ColdStartRequest):
    """
    Synthesizes a new persona twin from a single sentence description.
    Uses TF-IDF similarity to estimate DNA values and domain, then generates
    a rich persona with 3 grounded historical reviews using LLM or local heuristic generator.
    """
    try:
        desc = req.description.strip()
        if not desc:
            raise HTTPException(status_code=400, detail="Description cannot be empty")
            
        provider = req.provider
        api_key = req.api_key
        
        # 1. Infer DNA and Domain heuristically first (as basis or fallback)
        dna = parse_persona_description_heuristically(desc)
        
        # Infer domain
        desc_l = desc.lower()
        best_cat = "electronics"
        max_sim = -1.0
        for cat, ref in CATEGORY_REFERENCES.items():
            sim = compute_cosine_sim_text(desc_l, ref)
            if sim > max_sim:
                max_sim = sim
                best_cat = cat
                
        # Generate ID
        import uuid
        twin_id = f"twin_cold_{uuid.uuid4().hex[:8]}"
        
        # Try to use LLM to synthesize a gorgeous, extremely rich persona if credentials are provided
        if provider in ["groq", "gemini", "openai"] and api_key:
            try:
                system_instr = (
                    "You are a computational psychology twin synthesiser. Your job is to convert a short user statement "
                    "into a complete, rich TasteTwin Persona JSON object with 3 pre-grounded historical reviews."
                )
                
                # We'll select 3 sample items from the catalog in the inferred category to present to the LLM
                # so that it can write reviews grounded in actual catalog products!
                grounding_items = [it for it in ITEMS if it["category"] == best_cat][:3]
                if len(grounding_items) < 3:
                    grounding_items = ITEMS[:3]
                    
                items_context = []
                for idx, it in enumerate(grounding_items):
                    items_context.append({
                        "title": it["title"],
                        "category": it["category"],
                        "price": f"{it['price']} {it['currency']}",
                        "description": it["description"],
                        "features": it["features"],
                        "complaints": it.get("complaints", [])
                    })
                    
                prompt = f"""
                We are synthesizing a new behavioral twin based on this user description:
                "{desc}"
                
                The inferred Taste DNA is: {dna}
                The inferred primary domain category is: "{best_cat}"
                
                Your job is to generate a highly detailed, professional TasteTwin Persona.
                Write exactly 3 reviews for the 'history' array. These reviews MUST be grounded in the following real catalog items:
                {items_context}
                
                For each review, simulate a realistic rating (1-5) and write a descriptive, organic review text (50-100 words) that reflects the user's inferred DNA:
                - If budget DNA is high, comment heavily on the price.
                - If naija_scale DNA is high, incorporate realistic, organic Nigerian expressions (e.g. abeg, omo, sha, traffic, etc.) in a natural speaking style (not repetitive or fake!).
                - If sarcasm DNA is high, write with a sarcastic/dry humor tone.
                - If strictness is high, penalize any minor flaws.
                - If expressive is high, write a longer, highly descriptive critique.
                
                Output a valid JSON object matching this structure EXACTLY:
                {{
                  "id": "{twin_id}",
                  "name": "Generates a cool name matching the persona (e.g. 'Adebayo 'Budget' Cole' or similar)",
                  "domain": "{best_cat}",
                  "description": "A rich 1-2 sentence description of their shopping habits, preferences, and local constraints.",
                  "rating_bias": -0.2,
                  "category_affinity": {{
                    "electronics": 0.5,
                    "food": 0.5,
                    "books": 0.5,
                    "drinks": 0.5,
                    "fashion": 0.5
                  }},
                  "verbosity": "medium",
                  "tone": "standard",
                  "recent_mood": "standard",
                  "taste_drift": 0.0,
                  "preferred_aspects": ["quality"],
                  "pain_points": ["price"],
                  "style_examples": [
                    "Example of how they talk...",
                    "Another style example..."
                  ],
                  "dna": {{
                    "budget": {dna['budget']},
                    "novelty": {dna['novelty']},
                    "sarcasm": {dna['sarcasm']},
                    "expressive": {dna['expressive']},
                    "strictness": {dna['strictness']},
                    "naija_scale": {dna['naija_scale']}
                  }},
                  "history": [
                    {{
                      "item_name": "Exact title of catalog item 1",
                      "category": "{best_cat}",
                      "price": 15000.0,
                      "rating": 4,
                      "text": "Review text..."
                    }},
                    ...
                  ]
                }}
                Do NOT wrap in markdown code blocks. Only return the raw JSON block.
                """
                
                from app.engine import run_groq_agent, run_gemini_agent, run_openai_agent
                if provider == "groq":
                    resp = run_groq_agent(api_key, prompt, system_instr)
                elif provider == "gemini" and GENAI_AVAILABLE:
                    resp = run_gemini_agent(api_key, prompt, system_instr)
                elif provider == "openai" and OPENAI_AVAILABLE:
                    resp = run_openai_agent(api_key, prompt, system_instr)
                else:
                    raise Exception("SDK error")
                    
                json_match = re.search(r'\{.*\}', resp, re.DOTALL)
                if json_match:
                    new_persona = json.loads(json_match.group(0))
                    # Validate new persona id
                    new_persona["id"] = new_persona.get("id", twin_id)
                    # Add to in-memory PERSONAS
                    PERSONAS.append(new_persona)
                    
                    new_persona_copy = new_persona.copy()
                    new_persona_copy["bcs"] = calculate_behavioral_consistency(new_persona)
                    drift_val, _, _ = compute_taste_drift(new_persona)
                    new_persona_copy["taste_drift"] = drift_val
                    return new_persona_copy
                else:
                    raise Exception("Failed to parse JSON response from LLM")
                    
            except Exception as e:
                print(f"[TasteTwin] Cold-start LLM synthesis failed, falling back to heuristic: {e}")
                
        # Heuristic path fallback
        name_pool = {
            "electronics": ["Adebayo 'Tech' Cole", "Ibrahim 'Volt' Bello", "Chinedu 'Gig' Okafor"],
            "food": ["Funmi 'Calorie' Olowu", "Ngozi 'Chop' Obi", "Tunde 'Taste' Ajayi"],
            "books": ["Zainab 'Prose' Umar", "Segun 'Read' Thomas", "Chioma 'Novel' Eze"],
            "drinks": ["Femi 'Vibe' Lawson", "Emeka 'Cup' Okoro", "Yetunde 'Sip' Williams"],
            "fashion": ["Abisola 'Chic' Adenuga", "Halima 'Style' Musa", "Kelechi 'Fit' Nze"]
        }
        name = random.choice(name_pool.get(best_cat, ["Adebayo Cole"]))
        
        description = f"Digital twin synthesized from: '{desc}'. Primary interest in {best_cat}."
        
        category_affinity = {"electronics": 0.4, "food": 0.4, "books": 0.4, "drinks": 0.4, "fashion": 0.4}
        category_affinity[best_cat] = 0.9
        
        # Pick 3 target items in that category to review
        grounding_items = [it for it in ITEMS if it["category"] == best_cat][:3]
        if len(grounding_items) < 3:
            grounding_items = ITEMS[:3]
            
        history = []
        
        # Prepare temporary persona for rating predictor
        temp_persona = {
            "id": twin_id,
            "name": name,
            "domain": best_cat,
            "description": description,
            "dna": dna,
            "category_affinity": category_affinity,
            "history": []
        }
        
        for it in grounding_items:
            rating = predict_rating_heuristically(temp_persona, it)
            monologue, review_text = compile_heuristic_review(temp_persona, it, rating)
            
            review_entry = {
                "item_name": it["title"],
                "category": it["category"],
                "price": it["price"],
                "rating": int(round(rating)),
                "text": review_text
            }
            history.append(review_entry)
            temp_persona["history"].append(review_entry)
            
        new_persona = {
            "id": twin_id,
            "name": name,
            "domain": best_cat,
            "description": description,
            "rating_bias": 0.0,
            "category_affinity": category_affinity,
            "verbosity": "verbose" if dna["expressive"] > 70 else "concise" if dna["expressive"] < 40 else "medium",
            "tone": "sarcastic" if dna["sarcasm"] > 60 else "analytical" if dna["strictness"] > 60 else "standard",
            "recent_mood": "standard",
            "taste_drift": 0.0,
            "preferred_aspects": ["quality" if dna["strictness"] > 50 else "utility"],
            "pain_points": ["price" if dna["budget"] > 50 else "service"],
            "style_examples": [
                "Honestly, the product is quite good sha.",
                "Pocket friendly abeg, no complain."
            ],
            "dna": dna,
            "history": history
        }
        
        PERSONAS.append(new_persona)
        
        new_persona_copy = new_persona.copy()
        new_persona_copy["bcs"] = calculate_behavioral_consistency(new_persona)
        drift_val, _, _ = compute_taste_drift(new_persona)
        new_persona_copy["taste_drift"] = drift_val
        return new_persona_copy
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cold start synthesis failed: {str(e)}")

@app.post("/api/chatbot")
def api_chatbot(req: ChatbotRequest):
    """
    Interactive interviewer profiling chatbot that adjusts Taste DNA values dynamically.
    Proactively triggers product recommendations and catalog shortage warnings under appropriate thresholds.
    """
    try:
        current_dna_dict = req.current_dna.dict()
        
        # 1. Measure user pidgin density in current message to mirror speaking style
        msg_lower = req.message.lower()
        local_terms = {"omo", "abeg", "sha", "wahala", "kpa", "correct", "nepa", "traffic", "dispatch", "padi", "guy"}
        msg_words = re.findall(r'\b\w+\b', msg_lower)
        user_pidgin_count = sum(1 for w in msg_words if w in local_terms)
        user_pidgin_density = user_pidgin_count / len(msg_words) if msg_words else 0.0
        
        # 2. Run chatbot profiler
        if req.provider in ["groq", "gemini", "openai"] and req.api_key:
            result = run_chatbot_with_llm(req.provider, req.api_key, req.message, req.history, current_dna_dict)
        else:
            result = run_chatbot_heuristically(req.message, current_dna_dict)
            
        # 3. Check for recommendation trigger:
        # - User explicitly asks for recommendations
        # - OR, conversation history has >= 4 messages (meaning at least 2 full turns) and no recommendation has been served yet
        rec_intent = any(w in msg_lower for w in ["recommend", "suggest", "what do you have", "shop", "buy", "product", "item", "catalog", "choice", "option"])
        turn_trigger = (len(req.history) >= 4)
        
        already_recommended = False
        for msg in req.history:
            msg_content = msg.content.lower()
            if "i recommend" in msg_content or "delight" in msg_content or "delighted" in msg_content or "suitable items" in msg_content or "catalog shortage" in msg_content:
                already_recommended = True
                break
                
        trigger_rec = (rec_intent or (turn_trigger and not already_recommended))
        
        catalog_alert = False
        recommended_item = None
        
        if trigger_rec:
            # Let's run TasteTwin recommendations using the updated DNA!
            temp_persona = {
                "id": "chatbot_user",
                "name": "Interactive User",
                "domain": "all",
                "description": f"User's current interest: {req.message}",
                "dna": result["updated_dna"],
                "category_affinity": {
                    "electronics": 0.6,
                    "food": 0.4,
                    "books": 0.4,
                    "drinks": 0.4,
                    "fashion": 0.4
                },
                "history": []
            }
            
            recs_result = engine.recommend_items(
                persona_id="chatbot_user",
                category_filter="all",
                custom_persona=temp_persona
            )
            recs = recs_result.get("recommendations", [])
            
            if recs:
                top_rec = recs[0]
                predicted_delight = top_rec["predicted_rating"]
                
                if predicted_delight < 4.0:
                    # Warehouse Shortage Alarm!
                    print(f"[TasteTwin Alarm] Catalog Shortage: No suitable items for persona (delight {predicted_delight} < 4.0)!")
                    catalog_alert = True
                    recommended_item = None
                    
                    shortage_reply = "Omo, after checking our current catalog with your profile DNA, I couldn't find any item that would completely satisfy you o. High standard is high standard sha! I have triggered a backend warehouse alert [TasteTwin Alarm] for our manager to source better items for you. Abeg, check back small time!"
                    result["reply"] = modulate_pidgin(shortage_reply, result["updated_dna"]["naija_scale"], user_pidgin_density=user_pidgin_density)
                else:
                    catalog_alert = False
                    
                    # SIMULATE WHAT THE USER WOULD WRITE ABOUT IT
                    monologue, review_text = compile_heuristic_review(temp_persona, top_rec, predicted_delight)
                    
                    # Return cleanly for the UI to render the recommendation card
                    recommended_item = top_rec
                    recommended_item["simulated_review"] = review_text
                    
        result["catalog_alert"] = catalog_alert
        result["recommended_item"] = recommended_item
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot failed to respond: {str(e)}")


# Mount static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def serve_index():
    """Serves the single page application frontend."""
    index_path = os.path.join("app", "static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse(
        status_code=404,
        content={"error": "Frontend files not found. Please verify the app/static path."}
    )

