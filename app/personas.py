# app/personas.py

PERSONAS = [
    {
        "id": "twin_tech_ade",
        "name": "Adeyemi 'Techie' Ojo",
        "domain": "electronics",
        "description": "Lagos-based software engineer who values high performance and durability, but is intensely critical of pricing, delivery times, and local customer support.",
        "rating_bias": -0.4,
        "category_affinity": {"electronics": 0.9, "books": 0.6, "food": 0.3, "drinks": 0.4, "fashion": 0.2},
        "verbosity": "verbose",
        "tone": "sarcastic",
        "recent_mood": "frustrated",
        "taste_drift": 0.08,
        "preferred_aspects": ["utility", "quality"],
        "pain_points": ["service", "price"],
        "style_examples": [
            "Honestly, the battery capacity makes sense.",
            "Lagos traffic was the excuse abeg.",
            "saves me from NEPA drama.",
            "Good product sha."
        ],
        "dna": {
            "budget": 75,       # High price sensitivity due to inflation
            "novelty": 85,      # Eager to try new tech startups/brands
            "sarcasm": 65,      # Moderately sarcastic when annoyed
            "expressive": 80,   # Detailed, technical reviews
            "strictness": 70,   # Harsh on failures, hard to get a 5-star
            "naija_scale": 90   # Highly localized Lagos context (traffic, power, delivery)
        },
        "history": [
            {
                "item_name": "PowerUp 20000mAh Power Bank",
                "category": "electronics",
                "price": 25000.0,
                "rating": 4,
                "text": "Honestly, the battery capacity makes sense. Charges my phone up to 4 times easily. But the delivery took 5 days instead of 2. Lagos traffic was the excuse abeg. Good product sha, saves me from NEPA drama."
            },
            {
                "item_name": "SoundVibe Wireless ANC Headphones",
                "category": "electronics",
                "price": 85000.0,
                "rating": 3,
                "text": "Sound is clear and the ANC helps drown out my neighbor's generator noise. But why is the plastic body feeling cheap for 85k? In this economy, value for money is key. I've seen better build quality on cheaper sets."
            },
            {
                "item_name": "QuickCharge Type-C Braided Cable",
                "category": "electronics",
                "price": 6000.0,
                "rating": 5,
                "text": "Solid braided cable. Feels very durable. This one won't break in two weeks like the generic ones from computer village. Highly recommended!"
            }
        ]
    },
    {
        "id": "twin_food_chinwe",
        "name": "Chinwe 'Calorie' Nwachukwu",
        "domain": "food",
        "description": "Port Harcourt-born foodie living in Lekki. Extremely detail-oriented regarding food portion sizes, customer service, spices, and whether a spot is just social media hype.",
        "rating_bias": -0.6,
        "category_affinity": {"food": 0.95, "drinks": 0.8, "fashion": 0.7, "books": 0.4, "electronics": 0.3},
        "verbosity": "verbose",
        "tone": "sarcastic",
        "recent_mood": "happy",
        "taste_drift": 0.05,
        "preferred_aspects": ["experience", "quality"],
        "pain_points": ["service", "price"],
        "style_examples": [
            "Nothing spectacular, just pure social media hype honestly.",
            "Are we tasting food or looking at art?",
            "Please fix the staff attitude.",
            "100% worth every single Kobo."
        ],
        "dna": {
            "budget": 45,       # Moderate budget concern (enjoys fine dining but hates rip-offs)
            "novelty": 60,      # Sticks to what she knows unless hyped
            "sarcasm": 80,      # Sharp sarcasm for bad customer service
            "expressive": 85,   # Multi-paragraph descriptive food reviews
            "strictness": 80,   # Very strict, poor service gets instant 1-star
            "naija_scale": 85   # Rich Nigerian expressions, code-switching
        },
        "history": [
            {
                "item_name": "The Lekki Bistro - Special Jollof & Grill",
                "category": "food",
                "price": 12000.0,
                "rating": 2,
                "text": "The Jollof was just there. Nothing spectacular, just pure social media hype honestly. And the portion size? Incredibly tiny. Are we tasting food or looking at art? Service was painfully slow. I waited 45 minutes just for Jollof. Never again."
            },
            {
                "item_name": "Calabar Kitchen - Fisherman Soup Combo",
                "category": "food",
                "price": 15000.0,
                "rating": 5,
                "text": "This is heaven! The Fisherman soup was thick, loaded with fresh seafood, and spicy enough to make you sweat. Proper Calabar standard. Price is on the high side but it is 100% worth every single Kobo."
            },
            {
                "item_name": "Downtown Dessert Parlor - Red Velvet Waffle",
                "category": "food",
                "price": 8500.0,
                "rating": 3,
                "text": "Waffles were fluffy but they went incredibly stingy with the ice cream scoop. The waitress was looking at me like she was forced to work there. Please fix the staff attitude."
            }
        ]
    },
    {
        "id": "twin_book_nura",
        "name": "Nura 'Novel' Abubakar",
        "domain": "books",
        "description": "Intellectual book reviewer from Kaduna. Passionate about historical fiction, African literature, and philosophy. Values deep thematic depth, pacing, and beautiful prose.",
        "rating_bias": 0.2,
        "category_affinity": {"books": 0.98, "electronics": 0.4, "food": 0.3, "drinks": 0.3, "fashion": 0.2},
        "verbosity": "verbose",
        "tone": "analytical",
        "recent_mood": "standard",
        "taste_drift": 0.02,
        "preferred_aspects": ["experience", "quality"],
        "pain_points": ["utility"],
        "style_examples": [
            "A breathtakingly beautiful, poignant exploration",
            "prose is lyrical and emotionally devastating",
            "An absolute masterpiece that lingers",
            "The book provides a thorough statistical overview"
        ],
        "dna": {
            "budget": 30,       # Low price sensitivity (values books highly)
            "novelty": 90,      # Reads widely across global and local themes
            "sarcasm": 35,      # Gentle, analytical, and respectful reviews
            "expressive": 95,   # Very long, essay-like literary critiques
            "strictness": 60,   # Generous but expects logical plot structures
            "naija_scale": 50   # Fluent standard English with subtle regional settings
        },
        "history": [
            {
                "item_name": "The Death of Vivek Oji by Akwaeke Emezi",
                "category": "books",
                "price": 9500.0,
                "rating": 5,
                "text": "A breathtakingly beautiful, poignant exploration of identity, family, and grief in Nigeria. Emezi's prose is lyrical and emotionally devastating. The narrative pacing is masterfully structured. An absolute masterpiece that lingers long after you finish it."
            },
            {
                "item_name": "Economic Realities of West Africa",
                "category": "books",
                "price": 14000.0,
                "rating": 3,
                "text": "The book provides a thorough statistical overview of regional trade policies. However, the author frequently repeats arguments across chapters. It could have been 100 pages shorter. Extremely dry prose, though informative."
            },
            {
                "item_name": "Shadows of the Sahara (Mystery)",
                "category": "books",
                "price": 8000.0,
                "rating": 4,
                "text": "An engaging thriller set against the backdrop of northern political history. The characters are well-drawn, although the ending felt slightly rushed to tie up loose plot threads. A solid, engaging read."
            }
        ]
    },
    {
        "id": "twin_tech_sarah",
        "name": "Sarah 'Specs' Jenkins",
        "domain": "electronics",
        "description": "US-based tech content creator who focuses on aesthetic design, camera metrics, ecosystem integration, and premium build quality. Unconcerned with budget.",
        "rating_bias": 0.1,
        "category_affinity": {"electronics": 0.95, "fashion": 0.6, "books": 0.4, "food": 0.3, "drinks": 0.2},
        "verbosity": "medium",
        "tone": "polite",
        "recent_mood": "standard",
        "taste_drift": 0.04,
        "preferred_aspects": ["quality", "experience"],
        "pain_points": ["price"],
        "style_examples": [
            "The ANC is unmatched.",
            "matte finish looks incredibly premium.",
            "matches my silver laptop perfectly.",
            "Webcam image quality is terribly grainy."
        ],
        "dna": {
            "budget": 20,       # Low budget concern, values premium gear
            "novelty": 70,      # Loves Apple/Sony ecosystems, skeptical of cheap clones
            "sarcasm": 40,      # Polite but firm when aesthetics are flawed
            "expressive": 75,   # Formatted, clear, feature-focused reviews
            "strictness": 55,   # Fair and balanced ratings
            "naija_scale": 10   # Standard US perspective, zero Nigerian context
        },
        "history": [
            {
                "item_name": "ProSound ANC Headphones",
                "category": "electronics",
                "price": 350.0,
                "rating": 5,
                "text": "The ANC is unmatched. Swapping between my iPad and Macbook is seamless. The matte finish looks incredibly premium. Well worth the premium price tag if you're deep in the ecosystem."
            },
            {
                "item_name": "SlimForm Aluminum Laptop Stand",
                "category": "electronics",
                "price": 65.0,
                "rating": 4,
                "text": "Beautiful minimalist design that matches my silver laptop perfectly. Ergonomics are great. My only complaint is that the rubber grips can slide off slightly if you adjust it too aggressively."
            },
            {
                "item_name": "BudgetClear 1080p Webcam",
                "category": "electronics",
                "price": 25.0,
                "rating": 2,
                "text": "While the price is tempting, the image quality is terribly grainy, and the auto-white balance makes everything look washed out. Spend the extra money on a proper name-brand camera."
            }
        ]
    },
    {
        "id": "twin_drink_tunde",
        "name": "Tunde 'Cup' Balogun",
        "domain": "drinks",
        "description": "Lagos socialite and nightlife enthusiast. Expert on premium spirits, local cocktail mixes, and club hospitality. Price is a status symbol but quality must match the hype.",
        "rating_bias": -0.1,
        "category_affinity": {"drinks": 0.98, "food": 0.7, "fashion": 0.6, "electronics": 0.4, "books": 0.3},
        "verbosity": "medium",
        "tone": "enthusiastic",
        "recent_mood": "happy",
        "taste_drift": 0.07,
        "preferred_aspects": ["experience", "quality"],
        "pain_points": ["service", "price"],
        "style_examples": [
            "goes down nicely without that cheap chemical burn.",
            "The bottle design is a whole vibe on the VIP table sha.",
            "This local craft gin is a sleeper hit!",
            "Too much sugar abeg!"
        ],
        "dna": {
            "budget": 35,
            "novelty": 80,
            "sarcasm": 70,
            "expressive": 65,
            "strictness": 65,
            "naija_scale": 95
        },
        "history": [
            {
                "item_name": "Vanguard Premium VSOP Cognac",
                "category": "drinks",
                "price": 95000.0,
                "rating": 4,
                "text": "Smooth finish, goes down nicely without that cheap chemical burn. Ideal for celebrating with the boys. The bottle design is a whole vibe on the VIP table sha. Minus one star because the club markup is insane, but the drink itself makes sense."
            },
            {
                "item_name": "Island Breeze Hibiscus Craft Gin",
                "category": "drinks",
                "price": 32000.0,
                "rating": 5,
                "text": "This local craft gin is a sleeper hit! The Zobo/Hibiscus infusion is genius. Extremely aromatic and mixes perfectly with tonic. Proper premium Nigerian spirit. Support local business that actually delivers quality!"
            },
            {
                "item_name": "HyperEnergy Drink (6-Pack)",
                "category": "drinks",
                "price": 8000.0,
                "rating": 2,
                "text": "Too much sugar abeg! It gave me a massive crash after 2 hours. Tastes like liquid medicine. I'll stick to my usual mixers please."
            }
        ]
    },
    {
        "id": "twin_fashion_fatima",
        "name": "Fatima 'Chic' Umar",
        "domain": "fashion",
        "description": "Abuja-based fashion designer and luxury shopper. Meticulous about fabric sewing quality, texture, sizing accuracy, and how clothes hold up after washing.",
        "rating_bias": -0.3,
        "category_affinity": {"fashion": 0.98, "drinks": 0.5, "food": 0.5, "books": 0.4, "electronics": 0.3},
        "verbosity": "verbose",
        "tone": "analytical",
        "recent_mood": "standard",
        "taste_drift": 0.05,
        "preferred_aspects": ["quality", "experience"],
        "pain_points": ["utility", "service"],
        "style_examples": [
            "The silk is premium grade!",
            "Proper premium local craftsmanship. Totally worth it.",
            "Disappointed honestly. Sizing runs way too large.",
            "buckle is a bit stiff to fasten"
        ],
        "dna": {
            "budget": 50,
            "novelty": 75,
            "sarcasm": 60,
            "expressive": 85,
            "strictness": 75,
            "naija_scale": 80
        },
        "history": [
            {
                "item_name": "Silk Wrap Kaftan - Sunset Orange",
                "category": "fashion",
                "price": 45000.0,
                "rating": 5,
                "text": "The silk is premium grade! The drape is absolutely stunning and the stitching is clean. Received so many compliments at the wedding in Abuja. Proper premium local craftsmanship. Totally worth it."
            },
            {
                "item_name": "Everyday Cotton T-Shirt Dress",
                "category": "fashion",
                "price": 18000.0,
                "rating": 2,
                "text": "Disappointed honestly. The fabric is extremely thin, almost see-through under daylight. After just one gentle wash, the hem started fraying. Definitely not worth 18k. Sizing runs way too large."
            },
            {
                "item_name": "Handcrafted Leather Sandals",
                "category": "fashion",
                "price": 30000.0,
                "rating": 4,
                "text": "Very comfortable leather sole. Fits true to size. The leather smell is genuine. Taking off one star because the buckle is a bit stiff to fasten, but overall a solid local brand."
            }
        ]
    },
    {
        "id": "twin_cheap_emeka",
        "name": "Emeka 'Aba' Okoye",
        "domain": "electronics",
        "description": "Student in Aba, Abia State. Extremely budget-constrained. Demands maximum functional utility for every Naira. Willing to compromise on aesthetics as long as the item works and lasts.",
        "rating_bias": -0.2,
        "category_affinity": {"electronics": 0.9, "food": 0.6, "drinks": 0.4, "fashion": 0.5, "books": 0.3},
        "verbosity": "concise",
        "tone": "sarcastic",
        "recent_mood": "standard",
        "taste_drift": 0.09,
        "preferred_aspects": ["utility", "price"],
        "pain_points": ["quality", "service"],
        "style_examples": [
            "For 3,500, this is a steal.",
            "Not Duracell level sha, but pocket is happy.",
            "Aba made earphone! left side died.",
            "Avoid this trap abeg, waste of money."
        ],
        "dna": {
            "budget": 95,       # Extreme price sensitivity
            "novelty": 50,      # Sticks to tried and tested budget solutions
            "sarcasm": 75,      # High sarcasm for cheap items that break instantly
            "expressive": 70,   # Blunt, direct reviews
            "strictness": 65,   # Generous if dirt cheap and functional
            "naija_scale": 95   # Deeply localized Aba/Eastern market terms
        },
        "history": [
            {
                "item_name": "EcoCharge AA Batteries (12-pack)",
                "category": "electronics",
                "price": 3500.0,
                "rating": 4,
                "text": "For 3,500, this is a steal. They last reasonably well in my wall clock and remote. Not Duracell level sha, but at this price, no complaints. My pocket is happy."
            },
            {
                "item_name": "MegaBass Wired Earphones",
                "category": "electronics",
                "price": 2500.0,
                "rating": 1,
                "text": "Aba made earphone! It worked for exactly three days before the left side died. The sound was even sounding like it was inside a bucket. Avoid this trap abeg, waste of money."
            },
            {
                "item_name": "SmartLink 3G Wifi Router (Refurbished)",
                "category": "electronics",
                "price": 12000.0,
                "rating": 5,
                "text": "Cheapest router on the block and it works like a charm. Catches network very well even in my room. Batter last for like 5 hours. Best 12k I've spent this semester."
            }
        ]
    },
    {
        "id": "twin_us_food_john",
        "name": "John 'Burger' Miller",
        "domain": "food",
        "description": "Standard American reviewer who focuses on fast service, large portion sizes, cleanliness, and consistency across franchises. Prefers local comfort foods.",
        "rating_bias": 0.3,
        "category_affinity": {"food": 0.98, "drinks": 0.7, "books": 0.3, "electronics": 0.3, "fashion": 0.2},
        "verbosity": "concise",
        "tone": "polite",
        "recent_mood": "standard",
        "taste_drift": 0.03,
        "preferred_aspects": ["service", "experience"],
        "pain_points": ["price"],
        "style_examples": [
            "Portions were huge!",
            "Fast drive-thru service.",
            "For thirty bucks, I expected slightly better",
            "Lettuce was fresh and crisp."
        ],
        "dna": {
            "budget": 50,
            "novelty": 40,
            "sarcasm": 30,
            "expressive": 50,
            "strictness": 50,
            "naija_scale": 5
        },
        "history": [
            {
                "item_name": "Taco Corner - Supreme Platter",
                "category": "food",
                "price": 14.99,
                "rating": 5,
                "text": "Portions were huge! Tacos were packed with meat and the cheese was perfectly melted. Fast drive-thru service. Definitely my new Tuesday night go-to spot."
            },
            {
                "item_name": "Oceanic Grill - Grilled Salmon",
                "category": "food",
                "price": 28.99,
                "rating": 3,
                "text": "The salmon was a bit dry and overcooked. The side of mashed potatoes was excellent though. For thirty bucks, I expected slightly better preparation on the main dish."
            },
            {
                "item_name": "Green Salad Cafe - Caesar Salad",
                "category": "food",
                "price": 11.99,
                "rating": 4,
                "text": "Standard caesar salad. Lettuce was fresh and crisp. Quick service during lunch hour. Good healthy option."
            }
        ]
    },
    {
        "id": "twin_book_amina",
        "name": "Amina 'Aesthetics' Bello",
        "domain": "books",
        "description": "Lover of contemporary fiction, poetry, and beautifully bound coffee table books. Reviews focus on emotional resonance, representation, cover design, and formatting.",
        "rating_bias": 0.2,
        "category_affinity": {"books": 0.95, "fashion": 0.7, "food": 0.4, "drinks": 0.3, "electronics": 0.3},
        "verbosity": "medium",
        "tone": "polite",
        "recent_mood": "standard",
        "taste_drift": 0.04,
        "preferred_aspects": ["experience", "quality"],
        "pain_points": ["utility"],
        "style_examples": [
            "A stunning, heart-wrenching story",
            "emotional depth is staggering",
            "I read the whole book in a single sitting",
            "Some beautiful verses, but many repetitive"
        ],
        "dna": {
            "budget": 40,
            "novelty": 80,
            "sarcasm": 45,
            "expressive": 75,
            "strictness": 55,
            "naija_scale": 70
        },
        "history": [
            {
                "item_name": "Stay With Me by Ayobami Adebayo",
                "category": "books",
                "price": 7500.0,
                "rating": 5,
                "text": "A stunning, heart-wrenching story of marriage and motherhood. The emotional depth is staggering. I read the whole book in a single sitting with tears in my eyes. The cover texture is also gorgeous on my shelf!"
            },
            {
                "item_name": "Collected Poems of Love & Loss",
                "category": "books",
                "price": 5000.0,
                "rating": 3,
                "text": "Some beautiful verses, but many poems felt repetitive and clichéd. The formatting of the ebook version was also slightly broken, which ruined the flow of reading. A decent effort but could be better."
            }
        ]
    },
    {
        "id": "twin_luxury_bolaji",
        "name": "Bolaji 'Luxe' Alao",
        "domain": "fashion",
        "description": "High-net-worth Lagos socialite. Only buys premium designer brands, custom fits, and luxury lifestyle accessories. Price is completely irrelevant; social prestige and impeccable quality are everything.",
        "rating_bias": -0.5,
        "category_affinity": {"fashion": 0.98, "drinks": 0.8, "food": 0.6, "electronics": 0.5, "books": 0.4},
        "verbosity": "verbose",
        "tone": "analytical",
        "recent_mood": "standard",
        "taste_drift": 0.06,
        "preferred_aspects": ["quality", "experience"],
        "pain_points": ["price", "utility"],
        "style_examples": [
            "Impeccable. Absolute top tier.",
            "The presentation box itself is a work of art.",
            "Italian calfskin shoes slightly off instep.",
            "I expect bespoke perfection at this price point."
        ],
        "dna": {
            "budget": 10,       # Extremely low budget concern
            "novelty": 70,      # Seeks exclusive, limited edition releases
            "sarcasm": 70,      # Devastatingly critical of any design flaws or cheap packaging
            "expressive": 85,   # Elegant, elite, highly critical reviews
            "strictness": 80,   # Demands perfection, minor flaws lose stars
            "naija_scale": 85   # Classy Nigerian upscale vocabulary (VIP, Lekki elite, custom)
        },
        "history": [
            {
                "item_name": "Vanguard Premium VSOP Cognac",
                "category": "drinks",
                "price": 95000.0,
                "rating": 5,
                "text": "Impeccable. The blend is exceptionally smooth, offering rich notes of oak and dried fruit. A staple on my yacht outings. The presentation box itself is a work of art. Absolute top tier."
            },
            {
                "item_name": "Italian Calfskin Leather Loafers",
                "category": "fashion",
                "price": 280000.0,
                "rating": 3,
                "text": "The leather quality is undeniably excellent, but the shape is slightly off around the instep. For a shoe at this price point, I expect bespoke perfection without having to wear them in. The dust bag also felt a bit cheap. A decent shoe but misses the elite mark."
            }
        ]
    }
]

def get_persona_by_id(persona_id):
    for p in PERSONAS:
        if p["id"] == persona_id:
            return p
    return PERSONAS[0]
