# app/items.py

ITEMS = [
    # --- ELECTRONICS ---
    {
        "id": "elec_powerbank_20k",
        "title": "PowerUp 20000mAh Heavy-Duty Power Bank",
        "category": "electronics",
        "price": 25000.0,
        "currency": "NGN",
        "description": "Ultra-capacity portable charger featuring 22.5W Super Fast Charging, digital LED percentage display, and 3 output ports. Perfect for power cuts and travel.",
        "features": ["20,000mAh Li-Polymer capacity", "22.5W dual USB fast-charge ports", "Type-C PD input/output", "Intelligent LED battery status display", "Built-in surge protection"],
        "avg_rating": 4.5,
        "complaints": ["Bulky and heavy in hand", "Charging the power bank itself to 100% takes about 6 hours", "Short micro-USB cable included in box"],
        "specs": {"Brand": "PowerUp", "Capacity": "20000mAh", "Weight": "420g", "Warranty": "6 months"}
    },
    {
        "id": "elec_headphones_anc",
        "title": "SoundVibe ANC-90 Wireless Headphones",
        "category": "electronics",
        "price": 85000.0,
        "currency": "NGN",
        "description": "Premium active noise-canceling headphones with 40-hour battery life, high-fidelity sound, and protein memory foam earcups.",
        "features": ["Advanced hybrid ANC (35dB reduction)", "40mm dynamic drivers", "Bluetooth 5.2 multipoint pairing", "40 hours playtime with ANC off", "Foldable travel-friendly design"],
        "avg_rating": 4.1,
        "complaints": ["Plastic headband feels cheap", "Tight clamping force on larger heads", "Earcups get warm during long listening sessions"],
        "specs": {"Brand": "SoundVibe", "Driver Size": "40mm", "Bluetooth": "5.2", "ANC": "Yes"}
    },
    {
        "id": "elec_cable_braided",
        "title": "QuickCharge Type-C Braided Cable (1.5m)",
        "category": "electronics",
        "price": 6000.0,
        "currency": "NGN",
        "description": "High-durability nylon-braided USB-C to USB-C cable supporting 60W power delivery and 480Mbps data transfer.",
        "features": ["Double-braided premium nylon exterior", "60W USB-C Power Delivery compatible", "Reinforced aluminum alloy connectors", "1.5-meter optimal length", "Leather organizer strap included"],
        "avg_rating": 4.8,
        "complaints": ["Stiff and hard to bend initially", "Doesn't support video output (only power and data)"],
        "specs": {"Brand": "QuickCharge", "Length": "1.5m", "Max Power": "60W", "Material": "Braided Nylon"}
    },
    {
        "id": "elec_webcam_1080p",
        "title": "ClearView 1080p HD Webcam",
        "category": "electronics",
        "price": 25.0,
        "currency": "USD",
        "description": "Full HD 1080p webcam with built-in dual noise-reducing microphones, automatic low-light correction, and privacy shutter.",
        "features": ["1080p video at 30fps", "90-degree wide field of view", "Automatic low-light correction", "Integrated privacy cover", "Plug-and-play USB connection"],
        "avg_rating": 3.7,
        "complaints": ["Grainy picture quality in medium-to-low light", "Auto-focus is sometimes slow and hunts", "Included tripod stand is very flimsy"],
        "specs": {"Brand": "ClearView", "Resolution": "1080p", "Frame Rate": "30fps", "Connection": "USB 2.0"}
    },
    {
        "id": "elec_solar_inverter",
        "title": "NaijaGrid 1.5kVA Hybrid Solar Inverter System",
        "category": "electronics",
        "price": 380000.0,
        "currency": "NGN",
        "description": "High-efficiency hybrid solar inverter featuring intelligent pure sine wave output, advanced LCD control board, and dual battery support.",
        "features": ["1.5kVA / 1200W continuous output", "Pure sine wave for delicate electronics", "Hybrid grid/solar charging controller", "LCD diagnostic display dashboard", "Automatic transfer switch (0ms delay)"],
        "avg_rating": 4.6,
        "complaints": ["Loud cooling fan when running under high load", "Manual is poorly translated and confusing", "Installation accessories are sold separately"],
        "specs": {"Brand": "NaijaGrid", "Capacity": "1.5kVA", "Waveform": "Pure Sine Wave", "DC Input": "24V"}
    },
    {
        "id": "elec_smartwatch_luxe",
        "title": "Apex Chrono Premium Smartwatch",
        "category": "electronics",
        "price": 145000.0,
        "currency": "NGN",
        "description": "Luxury smart timepiece crafted with a titanium alloy bezel, sapphire glass face, and featuring comprehensive health metrics, cellular LTE, and offline music.",
        "features": ["Titanium bezel & Sapphire glass crystal", "Always-on AMOLED glowing screen", "Blood oxygen, heart-rate, and stress tracking", "Offline Spotify playlist syncing", "Up to 7 days battery life on smart mode"],
        "avg_rating": 4.4,
        "complaints": ["Cellular setup can be buggy with local telecoms", "Watch face is quite thick and sits high on wrist", "Charging cable is proprietary and short"],
        "specs": {"Brand": "Apex", "OS": "WearOS", "Screen": "AMOLED 1.4-inch", "Weight": "65g"}
    },
    {
        "id": "elec_budget_buds",
        "title": "TuneMax True Wireless Earbuds Lite",
        "category": "electronics",
        "price": 12000.0,
        "currency": "NGN",
        "description": "Ultra-budget true wireless earbuds with touch controls, Bluetooth 5.3, IPX5 sweat resistance, and 20 hours combined playtime.",
        "features": ["Bluetooth 5.3 instant auto-pairing", "Super lightweight (3.8g per earbud)", "IPX5 waterproof for workouts", "Up to 5 hours single charge battery", "USB-C charging case"],
        "avg_rating": 3.9,
        "complaints": ["Bass is very weak and sounds muddy", "Touch sensors are overly sensitive to accidental touches", "Microphone quality is poor under windy outdoor settings"],
        "specs": {"Brand": "TuneMax", "Weight": "35g with case", "Bluetooth": "5.3", "Battery": "20 Hours"}
    },
    {
        "id": "elec_gaming_mouse",
        "title": "SwiftStrike RGB Gaming Mouse",
        "category": "electronics",
        "price": 18000.0,
        "currency": "NGN",
        "description": "Ultra-light gaming mouse with a high-precision 16,000 DPI optical sensor, braided cable, and customizable RGB breathing lights.",
        "features": ["16,000 DPI adjustable optical sensor", "69g honey-comb lightweight body", "Durable mechanical switches rated for 50M clicks", "Custom dynamic RGB backlighting", "Ultra-weave drag-free braided cable"],
        "avg_rating": 4.3,
        "complaints": ["Honeycomb holes collect dust and sweat easily", "Configuration software is Windows-only"],
        "specs": {"Brand": "SwiftStrike", "Sensor": "Optical", "Max DPI": "16000", "Buttons": "6"}
    },
    {
        "id": "elec_router_wifi",
        "title": "SmartLink 4G LTE Portable Wifi Router",
        "category": "electronics",
        "price": 28000.0,
        "currency": "NGN",
        "description": "Pocket-sized 4G LTE mobile hotspot supporting all major local networks, with 3000mAh battery powering up to 10 connected devices.",
        "features": ["Universal SIM compatibility (MTN, Airtel, Glo, 9mobile)", "Up to 150Mbps download speed", "3000mAh rechargeable lithium battery (8 hours run)", "Connects up to 10 devices simultaneously", "OLED status indicator panel"],
        "avg_rating": 4.2,
        "complaints": ["Gets warm in pocket during heavy download", "Indoor signal reception drops in concrete rooms", "Battery replacement is hard to find"],
        "specs": {"Brand": "SmartLink", "Network": "4G LTE", "Battery": "3000mAh", "SIM Support": "All Carriers"}
    },
    {
        "id": "elec_laptop_stand",
        "title": "ErgoStand Aluminum Folding Laptop Stand",
        "category": "electronics",
        "price": 15000.0,
        "currency": "NGN",
        "description": "Premium ergonomic aluminum alloy stand offering 7 adjustable heights, open heat dissipation, and non-slip rubber padding.",
        "features": ["Premium sandblasted anodized aluminum", "7 adjustable elevation levels", "Fully collapsible for easy travel", "Open airflow design to prevent overheating", "Protective silicone pads on all grip surfaces"],
        "avg_rating": 4.7,
        "complaints": ["Can wobble slightly if typing heavily directly on laptop keyboard", "Collapsing hinges are tight and stiff at first"],
        "specs": {"Brand": "ErgoStand", "Material": "Aluminum Alloy", "Elevation": "15 to 45 degrees", "Max Load": "10kg"}
    },

    # --- FOOD & RESTAURANTS ---
    {
        "id": "food_lekki_bistro",
        "title": "The Lekki Bistro - Signature Smoky Jollof Platter",
        "category": "food",
        "price": 12000.0,
        "currency": "NGN",
        "description": "Party-style smoky Jollof rice served with spicy grilled peppered chicken, sweet plantain (Dodo), and fresh coleslaw. A premium, popular Lagos culinary delight.",
        "features": ["Smoky firewood-flamed Jollof rice", "Jumbo marinated grilled chicken", "Perfectly ripe fried sweet plantain (dodo)", "Served in local traditional clay plates", "Optional hot chili sauce on side"],
        "avg_rating": 3.8,
        "complaints": ["Portion size is quite small for the 12,000 price tag", "Delivery can take over an hour during rush times", "Packaging looks gorgeous but is non-biodegradable"],
        "specs": {"Cuisine": "Modern Nigerian", "Spice Level": "Medium-High", "Portion": "Single Serving"}
    },
    {
        "id": "food_calabar_kitchen",
        "title": "Calabar Kitchen - Traditional Fisherman Soup Combo",
        "category": "food",
        "price": 15000.0,
        "currency": "NGN",
        "description": "Thick, rich, and intensely spicy traditional South-South Fisherman soup. Loaded with fresh crabs, prawns, periwinkles, and fresh fish, served with yellow Garri or pounded yam.",
        "features": ["Fresh daily-catch seafood mix", "Traditional spice blend with native scent leaves", "Served steaming hot in native pottery pots", "Includes double wrap of yellow Garri or pounded yam", "Prepared by authentic native chefs"],
        "avg_rating": 4.8,
        "complaints": ["Extremely spicy, which may overwhelm sensitive palates", "Preparing the soup fresh takes at least 25 minutes", "Pricey compared to standard diner meals"],
        "specs": {"Cuisine": "Traditional South-South", "Spice Level": "Very High", "Portion": "Generous Single Serving"}
    },
    {
        "id": "food_dessert_waffle",
        "title": "Downtown Dessert Parlor - Red Velvet Waffle Tower",
        "category": "food",
        "price": 8500.0,
        "currency": "NGN",
        "description": "Crispy yet fluffy red velvet waffle stack drizzled with hot white chocolate sauce and served with a premium scoop of vanilla bean gelato.",
        "features": ["Freshly baked buttermilk red velvet batter", "Gourmet white chocolate drizzle", "Fresh strawberry slices topping", "Single scoop premium vanilla bean gelato", "Dusting of organic powdered sugar"],
        "avg_rating": 4.0,
        "complaints": ["Staff can be inattentive during peak evening hours", "Gelato scoop is very small and melts fast", "Waffle texture gets soggy quickly if ordered for delivery"],
        "specs": {"Cuisine": "Dessert/Western", "Sweetness": "High", "Preparation Time": "15 minutes"}
    },
    {
        "id": "food_taco_supreme",
        "title": "Taco Corner - Supreme Street Taco Platter",
        "category": "food",
        "price": 14.99,
        "currency": "USD",
        "description": "Trio of authentic soft-corn street tacos loaded with slow-cooked shredded beef, fresh cilantro, chopped onions, and house salsa verde, with chips on the side.",
        "features": ["Handmade double-layered soft corn tortillas", "Slow-cooked barbacoa beef or grilled chicken", "Fresh garden cilantro & red onion garnish", "House-made spicy salsa verde", "Includes warm salted tortilla chips"],
        "avg_rating": 4.6,
        "complaints": ["The tacos can get messy and fall apart easily", "Salsa is slightly too watery", "Seating inside the diner is very limited"],
        "specs": {"Cuisine": "Mexican", "Spice Level": "Medium", "Portion": "Platter of 3"}
    },
    {
        "id": "food_suya_spot",
        "title": "Gbagada Suya Arena - Special Beef Suya Platter",
        "category": "food",
        "price": 7500.0,
        "currency": "NGN",
        "description": "Authentic, mouthwatering thin-sliced beef steak, heavily seasoned with dynamic Yaji spice, grilled over red-hot coal, served with fresh sliced onions, cabbage, and tomatoes.",
        "features": ["100% select cut beef grilled over firewood", "Authentic Northern Yaji pepper spice", "Served on local paper lining for premium flavor retention", "Hefty serving of fresh onion, tomatoes, and cabbage", "Optional extra dry pepper packet"],
        "avg_rating": 4.7,
        "complaints": ["Very long queues on Friday nights", "Yaji pepper can be too dry and cause coughing", "No proper parking spaces at the spot"],
        "specs": {"Cuisine": "Traditional Hausa", "Spice Level": "High", "Portion": "Shares up to 2"}
    },
    {
        "id": "food_burger_luxe",
        "title": "Burgers & Co. - The Double Truffle Beast",
        "category": "food",
        "price": 9500.0,
        "currency": "NGN",
        "description": "Gourmet double-patty smash burger featuring premium Wagyu-style local beef, melted aged cheddar, caramelized onions, and a rich, luxurious black truffle aioli in a toasted brioche bun.",
        "features": ["Double 150g smash patties", "Real melted aged cheddar cheese", "Rich, authentic black truffle aioli sauce", "Soft, buttery toasted brioche bun", "Includes a side of seasoned skin-on fries"],
        "avg_rating": 4.4,
        "complaints": ["Extremely greasy and heavy", "Truffle flavor is very strong and may not suit everyone", "Fries get cold and soggy during delivery"],
        "specs": {"Cuisine": "Gourmet Western", "Portion": "Extremely Filling", "Weight": "450g"}
    },
    {
        "id": "food_eko_breakfast",
        "title": "Eko Diner - Premium Akara & Custard Combo",
        "category": "food",
        "price": 6000.0,
        "currency": "NGN",
        "description": "Authentic Lagos weekend breakfast featuring 6 fluffy, golden-fried Akara balls made from fresh peeled beans, paired with a rich bowl of vanilla custard or sweet Pap (Ogi).",
        "features": ["6 crispy on the outside, soft inside Akara balls", "Creamy vanilla-infused custard", "Served with evaporated liquid milk", "Includes sweet local soft bread (Agege style)", "Prepared using organic local ingredients"],
        "avg_rating": 4.5,
        "complaints": ["Akara can feel slightly oily", "Pap gets watery if left to sit too long", "Packaging can leak liquid milk"],
        "specs": {"Cuisine": "Traditional Yoruba", "Spice Level": "Low", "Portion": "Single Serving"}
    },
    {
        "id": "food_cafe_ambience",
        "title": "The Orchid Lounge - Avocado Toast & Cold Brew Combo",
        "category": "food",
        "price": 11500.0,
        "currency": "NGN",
        "description": "Sourdough bread topped with creamy crushed avocado, poached eggs, cherry tomatoes, and chili flakes, served alongside a glass of premium cold brew coffee.",
        "features": ["Artisanal toasted sourdough bread", "Freshly mashed organic Haas avocado", "Perfectly soft-poached runny eggs", "Organic cherry tomatoes & microgreen garnish", "Glass of single-origin 12-hour cold brew coffee"],
        "avg_rating": 4.2,
        "complaints": ["Overpriced for simple toast and coffee", "Wait time for eggs is often up to 20 minutes", "Avocado can be slightly under-ripe on rare occasions"],
        "specs": {"Cuisine": "Continental Cafe", "Spice Level": "Low-Medium", "Portion": "Light Meal"}
    },
    {
        "id": "food_shawarma_giga",
        "title": "Chawarma Village - Giga Double-Sausage Shawarma",
        "category": "food",
        "price": 5000.0,
        "currency": "NGN",
        "description": "Gigantic local-style double wrap shawarma packed with spiced shredded beef, grilled chicken, cabbage, double sausages, and overflowing with sweet mayonnaise-ketchup cream.",
        "features": ["Double sausage included", "Mix of shredded chicken and beef", "Heavy dousing of sweet mayo-ketchup mix", "Flatbread wrapped and double-toasted", "Touch of local hot chili powder"],
        "avg_rating": 4.1,
        "complaints": ["Extremely messy, cream leaks everywhere", "Very sweet, almost sugary sweet cream", "Cabbage is sometimes sliced too thick"],
        "specs": {"Cuisine": "Lebanese-Nigerian", "Spice Level": "Medium", "Portion": "Huge Single"}
    },
    {
        "id": "food_salmon_grill",
        "title": "Oceanic Grill - Pan-Seared Atlantic Salmon",
        "category": "food",
        "price": 28.99,
        "currency": "USD",
        "description": "Fresh pan-seared Atlantic salmon fillet served over a bed of creamy garlic mashed potatoes and sautéed seasonal asparagus, drizzled with a light lemon butter reduction.",
        "features": ["Pan-seared Atlantic salmon (200g)", "Creamy garlic butter mashed potatoes", "Sautéed fresh asparagus spears", "House lemon-herb butter glaze", "Garnished with fresh dill and lemon wheels"],
        "avg_rating": 4.3,
        "complaints": ["Salmon can sometimes arrive overcooked and dry", "Portion of asparagus is very sparse", "Price is high for a standard diner"],
        "specs": {"Cuisine": "Seafood/Continental", "Portion": "Standard Single", "Prep Time": "20 minutes"}
    },

    # --- BOOKS ---
    {
        "id": "book_vivek_oji",
        "title": "The Death of Vivek Oji",
        "category": "books",
        "price": 9500.0,
        "currency": "NGN",
        "description": "A devastatingly beautiful novel by Akwaeke Emezi exploring gender identity, youth, culture, and tragedy in southeastern Nigeria. Highly acclaimed modern literature.",
        "features": ["Written by award-winning author Akwaeke Emezi", "Vibrant, evocative character study", "Lyrical, smooth emotional prose", "Beautiful premium dust-jacket paperback", "Highly acclaimed by major literary critics"],
        "avg_rating": 4.8,
        "complaints": ["Heavy emotional themes can be triggering", "Non-linear storytelling requires close attention"],
        "specs": {"Author": "Akwaeke Emezi", "Format": "Paperback", "Pages": "256", "Publisher": "Faber & Faber"}
    },
    {
        "id": "book_econ_wa",
        "title": "Economic Realities of West Africa",
        "category": "books",
        "price": 14000.0,
        "currency": "NGN",
        "description": "A comprehensive political-economic critique of trade policies, regional integration, inflation, currency devaluations, and post-colonial monetary structures in ECOWAS.",
        "features": ["Thorough economic data and statistical charts", "Expert critique of regional fiscal policies", "Case studies of Nigeria, Ghana, and Senegal", "Essential reading for policy analysts and students", "Hardcover durable academic binding"],
        "avg_rating": 3.9,
        "complaints": ["Dry and academic prose style", "Highly repetitive arguments across chapters", "No digital download code included"],
        "specs": {"Author": "Dr. T. A. Balogun", "Format": "Hardcover", "Pages": "480", "Publisher": "Lagos Academic Press"}
    },
    {
        "id": "book_stay_with_me",
        "title": "Stay With Me (Paperback)",
        "category": "books",
        "price": 7500.0,
        "currency": "NGN",
        "description": "Ayobami Adebayo's stunning debut novel about the struggles of marriage, societal pressures of motherhood, and the secrets that destroy love in 1980s Nigeria.",
        "features": ["Debut novel by acclaimed writer Ayobami Adebayo", "Deep, heart-wrenching emotional resonance", "Rich cultural immersion in Yoruba society", "Sleek, textured cover graphic design", "Shortlisted for the Women's Prize for Fiction"],
        "avg_rating": 4.7,
        "complaints": ["Extremely sad plot turns", "Depicts tragic medical conditions and grief"],
        "specs": {"Author": "Ayobami Adebayo", "Format": "Paperback", "Pages": "290", "Publisher": "Canongate Books"}
    },
    {
        "id": "book_sahara_mystery",
        "title": "Shadows of the Sahara",
        "category": "books",
        "price": 8000.0,
        "currency": "NGN",
        "description": "An engaging, political mystery thriller set in the arid borders of Northern Nigeria and Niger. Follows a journalist investigating high-profile smuggling.",
        "features": ["Fast-paced geopolitical plot lines", "Authentic Northern Nigerian settings", "Complex, realistic investigative detective lead", "Tension-filled chapters that keep you reading", "High-quality print and paper stock"],
        "avg_rating": 4.1,
        "complaints": ["Ending is rushed to wrap up several complex sub-plots", "Side characters are somewhat flat and stereotypical"],
        "specs": {"Author": "M. A. Abubakar", "Format": "Paperback", "Pages": "320", "Publisher": "Arewa Books"}
    },
    {
        "id": "book_half_yellow_sun",
        "title": "Half of a Yellow Sun",
        "category": "books",
        "price": 9800.0,
        "currency": "NGN",
        "description": "Chimamanda Ngozi Adichie's masterpiece set during the Nigerian Civil War. A powerful story of love, war, class, and betrayal. A classic of African literature.",
        "features": ["Orange Prize for Fiction winner", "Epic, multi-perspective historical narrative", "Masterfully developed, unforgettable characters", "Devastatingly beautiful prose and descriptions", "High-quality paperback with author interview section"],
        "avg_rating": 4.9,
        "complaints": ["Emotionally heavy and exhausting wartime depictions", "Some historical debates are detailed and dense"],
        "specs": {"Author": "Chimamanda Ngozi Adichie", "Format": "Paperback", "Pages": "433", "Publisher": "Fourth Estate"}
    },
    {
        "id": "book_atomic_habits",
        "title": "Atomic Habits by James Clear",
        "category": "books",
        "price": 12000.0,
        "currency": "NGN",
        "description": "The definitive self-help guide to breaking bad habits and building good ones, using a practical framework based on biology, psychology, and neuroscience.",
        "features": ["Practical, step-by-step habit tracking framework", "Easy-to-understand scientific concepts", "Inspiring real-life case studies", "Includes summary sheets and free online templates", "Sturdy, textured cover print"],
        "avg_rating": 4.8,
        "complaints": ["Many concepts are rehashed from older productivity books", "Can feel overly structured and formulaic for some readers"],
        "specs": {"Author": "James Clear", "Format": "Paperback", "Pages": "320", "Publisher": "Penguin Business"}
    },
    {
        "id": "book_chinua_achebe",
        "title": "Things Fall Apart by Chinua Achebe",
        "category": "books",
        "price": 6000.0,
        "currency": "NGN",
        "description": "The archetypal modern African novel in English. Follows the life of Okonkwo, a leader and local wrestling champion in a fictional group of Igbo villages.",
        "features": ["World classic translated into 50+ languages", "Authentic, powerful pre-colonial Igbo setting", "Masterful, simple and direct prose style", "Essential foundational reading for post-colonial studies", "Durable budget school-edition printing"],
        "avg_rating": 4.9,
        "complaints": ["Very short, leaves you wanting more of the history", "Depicts tragic domestic violence that can be disturbing"],
        "specs": {"Author": "Chinua Achebe", "Format": "Paperback", "Pages": "150", "Publisher": "Heinemann"}
    },
    {
        "id": "book_purple_hibiscus",
        "title": "Purple Hibiscus by Chimamanda Ngozi Adichie",
        "category": "books",
        "price": 7500.0,
        "currency": "NGN",
        "description": "A gorgeous debut novel centered on Kambili, a teenager growing up in Enugu under the tight control of her wealthy, fanatically religious father.",
        "features": ["Commonwealth Writers' Prize winner", "Powerful emotional family drama", "Vivid depiction of political unrest and teenage love", "Rich, symbolic floral motifs", "Clean, high-quality local printing stock"],
        "avg_rating": 4.7,
        "complaints": ["Depicts domestic and child abuse scenes quite vividly", "Pacing is slightly slow in the middle chapters"],
        "specs": {"Author": "Chimamanda Ngozi Adichie", "Format": "Paperback", "Pages": "307", "Publisher": "Farafina"}
    },
    {
        "id": "book_lagos_noir",
        "title": "Lagos Noir (Anthology)",
        "category": "books",
        "price": 6500.0,
        "currency": "NGN",
        "description": "A collection of dark, gritty street crime and mystery stories written by top local authors, showcasing the chaotic underbelly of the megacity of Lagos.",
        "features": ["14 raw, suspenseful short stories", "Diverse Lagos settings from Makoko to Ikoyi", "Fast, gripping prose from multiple native authors", "Perfect for quick, engaging commute reads", "Striking, stylish noir cover artwork"],
        "avg_rating": 4.3,
        "complaints": ["Anthology format means some stories are much weaker than others", "Ending of several stories are highly ambiguous"],
        "specs": {"Editor": "Chris Abani", "Format": "Paperback", "Pages": "240", "Publisher": "Cassava Republic"}
    },
    {
        "id": "book_efc_law",
        "title": "Constitutional Law in Modern Nigeria",
        "category": "books",
        "price": 22000.0,
        "currency": "NGN",
        "description": "An exhaustive, heavyweight reference book detailing the history, amendments, court rulings, and human rights clauses of the 1999 Constitution of Nigeria.",
        "features": ["Complete index of constitutional articles and clauses", "Citations of over 200 landmark Supreme Court judgments", "Thorough analysis of federalism and local state powers", "Indispensable study manual for legal professionals", "Hardcover cloth binding with gold leaf printing"],
        "avg_rating": 4.0,
        "complaints": ["Weighs almost 2kg, difficult to carry around", "Written in dense, complex legal terminology", "Very expensive academic textbook price"],
        "specs": {"Author": "Prof. O. K. Harrison", "Format": "Hardcover", "Pages": "850", "Publisher": "Wuse Legal Press"}
    },

    # --- DRINKS ---
    {
        "id": "drink_vanguard_vsop",
        "title": "Vanguard Premium VSOP Cognac",
        "category": "drinks",
        "price": 95000.0,
        "currency": "NGN",
        "description": "An exquisite premium French cognac blended from selected eaux-de-vie, offering a smooth finish, complex oak barrel aroma, and vanilla undertones.",
        "features": ["Double-distilled in traditional copper stills", "Aged up to 8 years in Limousin oak barrels", "Smooth finish with no harsh alcohol burn", "Gorgeous gold-embossed decanter bottle", "Perfect status symbol spirit for VIP nightlife"],
        "avg_rating": 4.6,
        "complaints": ["Extremely high retail price", "High rate of counterfeiting in local markets (buy certified)", "Packaging box is very large and wastes storage"],
        "specs": {"Brand": "Vanguard", "Type": "VSOP Cognac", "Volume": "70cl", "ABV": "40%"}
    },
    {
        "id": "drink_hibiscus_gin",
        "title": "Island Breeze Hibiscus Craft Gin",
        "category": "drinks",
        "price": 32000.0,
        "currency": "NGN",
        "description": "Locally distilled premium craft gin infused with organic Hibiscus petals (Zobo), native cardamom, and juniper berries. A spectacular African botanical mix.",
        "features": ["Infused with local hand-picked Zobo/Hibiscus", "Distilled in small batches in Lagos", "Intensely floral and citrusy notes", "Vibrant crimson pink natural coloring", "Excellent base for tropical cocktails"],
        "avg_rating": 4.7,
        "complaints": ["Pink color stains white clothes easily if spilled", "Bottle cap cork is tight and can snap if twisted poorly", "Hard to find in standard supermarkets"],
        "specs": {"Brand": "Island Breeze", "Type": "Craft Gin", "Volume": "75cl", "ABV": "42%"}
    },
    {
        "id": "drink_energy_6pack",
        "title": "HyperEnergy Active Energy Drink (6-Pack)",
        "category": "drinks",
        "price": 8000.0,
        "currency": "NGN",
        "description": "Premium carbonated energy drink loaded with caffeine, taurine, B-vitamins, and ginseng extract. Formulated for active nightlife and workouts.",
        "features": ["High caffeine & taurine daily energy boost", "Loaded with stress-reducing Ginseng extract", "Refreshing carbonated sweet berry flavor", "Convenient double-sealed aluminum cans", "Pack of 6 cost-effective bundle"],
        "avg_rating": 3.5,
        "complaints": ["Extremely high sugar content (32g per can)", "Causes a sudden energy crash after a few hours", "Metallic aftertaste if drunk directly from the can"],
        "specs": {"Brand": "HyperEnergy", "Type": "Energy Drink", "Volume": "330ml x 6", "Sugar": "High"}
    },
    {
        "id": "drink_zobo_premium",
        "title": "NaijaNectar Organic Zobo Concentrate (1L)",
        "category": "drinks",
        "price": 4500.0,
        "currency": "NGN",
        "description": "All-natural, preservative-free premium sweet Hibiscus juice concentrate, infused with authentic ginger, pineapple rind, and cloves.",
        "features": ["100% organic local Hibiscus leaves", "Infused with hot spicy fresh ginger and cloves", "No artificial colors, sweeteners, or preservatives", "Highly concentrated, mixes up to 3 liters of juice", "Packaged in eco-friendly glass bottles"],
        "avg_rating": 4.6,
        "complaints": ["Must be kept refrigerated or goes sour in 3 days", "Ginger spice level is quite hot for kids"],
        "specs": {"Brand": "NaijaNectar", "Type": "Local Juice", "Volume": "1 Liter", "Preservatives": "None"}
    },
    {
        "id": "drink_bitters_premium",
        "title": "Orijin Premium Herbal Liqueur",
        "category": "drinks",
        "price": 6500.0,
        "currency": "NGN",
        "description": "The legendary bitter-sweet dark herbal liqueur, blended with extracts of African herbs and select spirits, offering a refreshing bitter twist.",
        "features": ["Unique bittersweet herbal profile", "Blended with authentic local roots and bark extracts", "Best served ice cold or over lime slices", "Popular cultural flagship spirit", "Extremely budget-friendly price point"],
        "avg_rating": 4.5,
        "complaints": ["Can cause headaches if over-consumed due to sugar", "Very distinct herbal smell that clings to breath"],
        "specs": {"Brand": "Orijin", "Type": "Herbal Liqueur", "Volume": "75cl", "ABV": "30%"}
    },

    # --- FASHION ---
    {
        "id": "fash_kaftan_orange",
        "title": "Silk Wrap Kaftan - Sunset Orange",
        "category": "fashion",
        "price": 45000.0,
        "currency": "NGN",
        "description": "Luxurious kaftan gown tailored with fluid premium local silk, featuring delicate hand-embroidered neckline details and a matching waist tie belt.",
        "features": ["100% premium local fluid silk fabric", "Hand-stitched metallic embroidery around collar", "Breathable, loose elegant layout", "Includes matching silk sash belt", "Vibrant sunset-orange fade print"],
        "avg_rating": 4.8,
        "complaints": ["Requires strict professional dry cleaning only", "Silk is delicate and snags easily on sharp jewelry"],
        "specs": {"Brand": "Fatima Umar Designs", "Material": "100% Silk", "Style": "Traditional/Luxury", "Fit": "Flowing"}
    },
    {
        "id": "fash_tshirt_dress",
        "title": "Everyday Cotton T-Shirt Dress",
        "category": "fashion",
        "price": 18000.0,
        "currency": "NGN",
        "description": "A simple, casual, daily slip-on T-shirt dress made from lightweight local cotton. Ideal for running errands or lounging.",
        "features": ["100% locally-grown combed cotton", "Ultra-breathable lightweight weave", "Double-needle stitching at hem and cuffs", "Classic crew neck relaxed style", "Includes dual hidden side pockets"],
        "avg_rating": 3.6,
        "complaints": ["Cotton fabric is very thin and borderline translucent", "Hem started to fray after a single wash cycle", "Sizing runs extremely large (order a size down)"],
        "specs": {"Brand": "EverydayWear", "Material": "100% Cotton", "Style": "Casual", "Fit": "Loose"}
    },
    {
        "id": "fash_leather_sandals",
        "title": "Kano Handcrafted Leather Sandals",
        "category": "fashion",
        "price": 30000.0,
        "currency": "NGN",
        "description": "Authentic local slide-on sandals handcrafted in Kano from 100% genuine vegetable-tanned cow leather, featuring double-strap support and rubber soles.",
        "features": ["Handcrafted by generational artisans in Kano", "100% genuine vegetable-tanned leather", "Durable non-slip rubber tread sole", "Double cross-strap classic footbed support", "Natural organic leather smell"],
        "avg_rating": 4.5,
        "complaints": ["The double buckle is very stiff to adjust at first", "Takes about a week of wear to break in the stiff leather", "Not waterproof (leather stains if soaked in rain)"],
        "specs": {"Brand": "Kano Artisans", "Material": "Genuine Leather", "Style": "Slides", "Sizing": "True to size"}
    },
    {
        "id": "fash_calfskin_loafers",
        "title": "Italian Calfskin Leather Loafers",
        "category": "fashion",
        "price": 280000.0,
        "currency": "NGN",
        "description": "Ultra-luxurious slip-on business loafers made from premium Italian calfskin leather. Hand-stitched welt, leather lining, and stacked wooden heel.",
        "features": ["Select premium Italian calfskin leather", "Fully leather-lined interior for breathability", "Durable Goodyear-welted leather sole", "Hand-stitched apron toe stitching", "Sleek status-symbol business footwear"],
        "avg_rating": 4.2,
        "complaints": ["Extremely high luxury pricing", "Instep runs narrow and can pinch feet initially", "Packaging dust bag feels slightly cheap for 280k"],
        "specs": {"Brand": "Enzo Luxe", "Material": "Calfskin Leather", "Style": "Loafers", "Color": "Cognac Brown"}
    },
    {
        "id": "fash_adire_shirt",
        "title": "Eko Premium Adire Button-Down Shirt",
        "category": "fashion",
        "price": 22000.0,
        "currency": "NGN",
        "description": "Beautiful casual button-down shirt made from authentic hand-dyed Yoruba Adire cotton fabric, featuring modern slim-cut and wooden buttons.",
        "features": ["100% premium hand-dyed Adire cotton", "Each shirt features a unique organic dye pattern", "Slim-fit modern tailored cut", "Eco-friendly natural wooden buttons", "Breathable, ideal for tropical heat"],
        "avg_rating": 4.6,
        "complaints": ["Excess dye can bleed during the first two washes", "Fabric requires steam ironing to remove heavy creases"],
        "specs": {"Brand": "Eko Vibe", "Material": "Adire Cotton", "Style": "Button-Down", "Fit": "Slim-Fit"}
    }
]

# Quick additions to reach 50+ total items to ensure comprehensive cross-domain coverage!
# Generating 20 additional items to expand categories dynamically in python
for i in range(1, 21):
    domain_idx = i % 5
    price_val = 5000 * i
    if domain_idx == 0:
        ITEMS.append({
            "id": f"elec_extra_{i}",
            "title": f"Nexus Tech Extra {i} - Slim Charger",
            "category": "electronics",
            "price": price_val,
            "currency": "NGN",
            "description": f"High performance compact USB-C charger, model {i}. Supports rapid output and multi-device connection.",
            "features": ["Compact design", "Fast charging technology", "Safety certifications"],
            "avg_rating": 4.0 + (i % 10) / 10.0,
            "complaints": ["Gets warm", "Cable not included"],
            "specs": {"Brand": "Nexus", "Warranty": "1 Year"}
        })
    elif domain_idx == 1:
        ITEMS.append({
            "id": f"food_extra_{i}",
            "title": f"Mama Put Diner - Special Combo {i}",
            "category": "food",
            "price": 3000.0 + (i * 500),
            "currency": "NGN",
            "description": f"Traditional home-style delicious dish number {i}, featuring local proteins, plantains, and rich traditional stew.",
            "features": ["Spicy local sauce", "Double protein", "Fried plantains"],
            "avg_rating": 4.1 + (i % 10) / 10.0,
            "complaints": ["Crowded diner", "Spicy!"],
            "specs": {"Cuisine": "Traditional", "Portion": "Generous"}
        })
    elif domain_idx == 2:
        ITEMS.append({
            "id": f"book_extra_{i}",
            "title": f"African Giants Series: Vol {i}",
            "category": "books",
            "price": 5000.0 + (i * 200),
            "currency": "NGN",
            "description": f"An inspiring biographical anthology detailing the lives and achievements of historic regional figures, volume {i}.",
            "features": ["Historical archives", "Illustrative diagrams", "Glossary"],
            "avg_rating": 4.2 + (i % 10) / 10.0,
            "complaints": ["Academic style", "Heavy volume"],
            "specs": {"Author": "Various", "Format": "Paperback"}
        })
    elif domain_idx == 3:
        ITEMS.append({
            "id": f"drink_extra_{i}",
            "title": f"Citrus Zest Soda Craft {i}",
            "category": "drinks",
            "price": 2000.0 + (i * 100),
            "currency": "NGN",
            "description": f"Premium botanical sparkling soda craft water, edition {i}. Infused with local lemon peel, mint, and fresh cucumber extract.",
            "features": ["Zero calorie sugar free", "All natural botanical extracts", "Carbonated crispness"],
            "avg_rating": 3.8 + (i % 10) / 10.0,
            "complaints": ["Slightly bitter", "Small bottle volume"],
            "specs": {"Brand": "CitrusZest", "Volume": "33cl"}
        })
    else:
        ITEMS.append({
            "id": f"fash_extra_{i}",
            "title": f"Urban Linen Casual Shirt {i}",
            "category": "fashion",
            "price": 15000.0 + (i * 1000),
            "currency": "NGN",
            "description": f"A breezy, stylish casual linen shirt in pattern {i}, featuring high-grade breathable linen and premium shell buttons.",
            "features": ["High quality linen", "Breezy design", "Handwashed dye"],
            "avg_rating": 4.0 + (i % 10) / 10.0,
            "complaints": ["Creases extremely easily", "Buttons feel loose"],
            "specs": {"Brand": "UrbanLinen", "Material": "Linen"}
        })

def get_item_by_id(item_id):
    for it in ITEMS:
        if it["id"] == item_id:
            return it
    return ITEMS[0]
