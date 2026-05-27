// app/static/app.js

// Global Session Variables
let allPersonas = [];
let allItems = [];
let selectedPersona = null;
let selectedItem = null;
let activeTab = "tab-sandbox";
let currentRecommendations = [];
let activeDebateItem = null;
let activeRecTab = "debate";

// API Provider Configurations
let currentProvider = localStorage.getItem("tastetwin_provider") || "groq";
let currentApiKey = localStorage.getItem("tastetwin_apikey") || "";

// ----------------------------------------------------------------------
// 1. INITIALIZATION & DATA LOADING
// ----------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", async () => {
    // Setup API keys in UI inputs from localStorage
    document.getElementById("engine-provider").value = currentProvider;
    document.getElementById("api-key-input").value = currentApiKey;
    handleProviderChange();
    updateModeBadge();

    // Fetch initial datasets from FastAPI server
    try {
        const resPersonas = await fetch("/api/personas");
        allPersonas = await resPersonas.json();
        
        const resItems = await fetch("/api/items");
        allItems = await resItems.json();
        
        // Populate selectors
        populateSelectors();
        
        // Load default persona and item
        if (allPersonas.length > 0) {
            selectedPersona = JSON.parse(JSON.stringify(allPersonas[0])); // deep copy
            loadPersonaValuesToUI(selectedPersona);
            renderTasteDNA(selectedPersona.dna);
            renderCorpusHistory(selectedPersona.history);
            
            // Sync Taste Map and chatbot DNA
            syncTasteMap();
            initChatbotDNA();
        }
        
        if (allItems.length > 0) {
            selectedItem = allItems[0];
            loadTargetProduct();
        }
        
        // Load Task B recommendations baseline
        triggerRecommendationRetrieval();
        
        // Start Driver.js onboarding tour if not completed
        if (!localStorage.getItem('tasteTwinTourDone')) {
            setTimeout(() => {
                const driver = window.driver.js.driver;
                const tourObj = driver({
                    showProgress: true,
                    steps: [
                        { element: '.config-trigger', popover: { title: 'Welcome to TasteTwin!', description: 'Start by clicking here to select an execution mode. You can use the blazing-fast Local Heuristics, or select an LLM like Groq Llama 3 (requires an API key).', side: "bottom", align: 'start' } },
                        { element: 'button[data-tab="tab-sandbox"]', popover: { title: 'User Sandbox', description: 'This is where you set the active persona and explore the Digital Twin memory. Select different users to load their historical data, preferences, and generated Taste DNA.', side: "right", align: 'start' } },
                        { element: 'button[data-tab="tab-taste-map"]', popover: { title: 'Taste Map', description: 'Visually explore how the algorithm clusters users and items in a mathematical vector space based on behavioral similarity.', side: "right", align: 'start' } },
                        { element: 'button[data-tab="tab-chatbot"]', popover: { title: 'Profiler Chatbot', description: 'Interact with our conversational profiling agent! It will ask you questions to discover your preferences and dynamically build your Taste DNA.', side: "right", align: 'start' } },
                        { element: 'button[data-tab="tab-taska"]', popover: { title: 'Task A: Review Gen', description: 'Generate realistic, culturally-contextualized product reviews based exactly on the user\'s internal Taste DNA and mood.', side: "right", align: 'start' } },
                        { element: 'button[data-tab="tab-taskb"]', popover: { title: 'Task B: Recommendations', description: 'Watch specialized AI agents debate and recommend the perfect item based on Taste, Budget, Novelty, and Nigerian Context.', side: "right", align: 'start' } },
                        { element: 'button[data-tab="tab-evaluation"]', popover: { title: 'Mathematical Evaluation', description: 'View the raw performance metrics of our custom Coordinate Descent ranking engine.', side: "right", align: 'start' } }
                    ],
                    onDestroyStarted: () => {
                        localStorage.setItem('tasteTwinTourDone', 'true');
                        tourObj.destroy();
                    }
                });
                tourObj.drive();
            }, 800); // slight delay so the UI fully renders
        }
        
    } catch (err) {
        console.error("Initialization failed: ", err);
    }
});

function populateSelectors() {
    const pSelect = document.getElementById("persona-select");
    pSelect.innerHTML = "";
    allPersonas.forEach(p => {
        const opt = document.createElement("option");
        opt.value = p.id;
        opt.textContent = `${p.name} (${p.domain.toUpperCase()})`;
        pSelect.appendChild(opt);
    });

    const pSimSelect = document.getElementById("persona-select-simulator");
    if (pSimSelect) {
        pSimSelect.innerHTML = "";
        allPersonas.forEach(p => {
            const opt = document.createElement("option");
            opt.value = p.id;
            opt.textContent = `${p.name} (${p.domain.toUpperCase()})`;
            pSimSelect.appendChild(opt);
        });
    }

    const iSelect = document.getElementById("item-select");
    iSelect.innerHTML = "";
    allItems.forEach(item => {
        const opt = document.createElement("option");
        opt.value = item.id;
        opt.textContent = `${item.title} (${item.category.toUpperCase()})`;
        iSelect.appendChild(opt);
    });

    const tbiSelect = document.getElementById("taskb-item-select");
    if (tbiSelect) {
        tbiSelect.innerHTML = "";
        allItems.forEach(item => {
            const opt = document.createElement("option");
            opt.value = item.id;
            opt.textContent = `${item.title} (${item.category.toUpperCase()})`;
            tbiSelect.appendChild(opt);
        });
    }
}

function syncPersonaSelectionSimulator() {
    const pSimSelect = document.getElementById("persona-select-simulator");
    const pSelect = document.getElementById("persona-select");
    if (pSimSelect && pSelect) {
        pSelect.value = pSimSelect.value;
        loadSelectedPersona();
    }
}

// ----------------------------------------------------------------------
// 2. CONFIGURATION MANAGEMENT
// ----------------------------------------------------------------------
function toggleConfigPanel() {
    const dropdown = document.getElementById("config-dropdown");
    dropdown.classList.toggle("open");
}

// Close config panel if clicked outside
window.addEventListener("click", (e) => {
    const dropdown = document.getElementById("config-dropdown");
    const trigger = document.querySelector(".config-trigger");
    if (!dropdown.contains(e.target) && !trigger.contains(e.target)) {
        dropdown.classList.remove("open");
    }
});

function handleProviderChange() {
    const provider = document.getElementById("engine-provider").value;
    const keyContainer = document.getElementById("api-key-container");
    if (provider === "heuristic") {
        keyContainer.classList.add("hidden");
    } else {
        keyContainer.classList.remove("hidden");
    }
}

function saveConfiguration() {
    const provider = document.getElementById("engine-provider").value;
    const apiKey = document.getElementById("api-key-input").value.trim();
    
    currentProvider = provider;
    currentApiKey = apiKey;
    
    localStorage.setItem("tastetwin_provider", provider);
    localStorage.setItem("tastetwin_apikey", apiKey);
    
    updateModeBadge();
    toggleConfigPanel();
    
    // Update API editor template to match config
    updateApiEditorTemplate();
    
    // Reload recommendations with new settings
    triggerRecommendationRetrieval();
}

function updateModeBadge() {
    const badge = document.getElementById("active-mode-badge");
    const subMode = document.getElementById("simulation-output-mode");
    
    let text = "Mode: Local Heuristic";
    if (currentProvider === "gemini") {
        text = "Mode: Gemini Agent";
    } else if (currentProvider === "openai") {
        text = "Mode: OpenAI Agent";
    } else if (currentProvider === "groq") {
        text = "Mode: Groq Agent (llama-4-scout)";
    }
    
    badge.textContent = text;
    if (subMode) {
        subMode.textContent = `Mode: ${text} Mode`;
    }
}

// ----------------------------------------------------------------------
// 3. TASTE DNA SANDBOX OPERATIONS
// ----------------------------------------------------------------------
function loadSelectedPersona() {
    const select = document.getElementById("persona-select");
    const p = allPersonas.find(x => x.id === select.value);
    if (p) {
        selectedPersona = JSON.parse(JSON.stringify(p)); // deep copy
        loadPersonaValuesToUI(selectedPersona);
        renderTasteDNA(selectedPersona.dna);
        renderCorpusHistory(selectedPersona.history);
        
        // Tweak API editor template
        updateApiEditorTemplate();
        
        // Sync Taste Map and chatbot DNA
        syncTasteMap();
        initChatbotDNA();
        
        // Reset recommendations
        triggerRecommendationRetrieval();
    }
}

function loadPersonaValuesToUI(p) {
    document.getElementById("slide-budget").value = p.dna.budget;
    document.getElementById("slide-novelty").value = p.dna.novelty;
    document.getElementById("slide-sarcasm").value = p.dna.sarcasm;
    document.getElementById("slide-expressive").value = p.dna.expressive;
    document.getElementById("slide-strictness").value = p.dna.strictness;
    document.getElementById("slide-naija").value = p.dna.naija_scale;

    updateSliderLabelDisplays(p.dna);

    // Populate BCS and Taste Drift metrics gauges
    const bcsEl = document.getElementById("sandbox-bcs");
    const driftEl = document.getElementById("sandbox-drift");
    if (bcsEl) {
        bcsEl.textContent = (p.bcs !== undefined && p.bcs !== null) ? p.bcs.toFixed(1) : "--";
    }
    if (driftEl) {
        driftEl.textContent = (p.taste_drift !== undefined && p.taste_drift !== null) ? p.taste_drift.toFixed(3) : "--";
    }
    
    // Update Task B UI
    const tbName = document.getElementById("taskb-active-persona-name");
    if (tbName) {
        tbName.textContent = p.name;
    }
}

function updateSliderLabelDisplays(dna) {
    document.getElementById("val-budget").textContent = `${dna.budget}%`;
    document.getElementById("val-novelty").textContent = `${dna.novelty}%`;
    document.getElementById("val-sarcasm").textContent = `${dna.sarcasm}%`;
    document.getElementById("val-expressive").textContent = `${dna.expressive}%`;
    document.getElementById("val-strictness").textContent = `${dna.strictness}%`;
    document.getElementById("val-naija").textContent = `${dna.naija_scale}%`;
}

function updateDNAValue(trait) {
    if (!selectedPersona) return;
    
    let sliderId = "";
    switch(trait) {
        case "budget": sliderId = "slide-budget"; break;
        case "novelty": sliderId = "slide-novelty"; break;
        case "sarcasm": sliderId = "slide-sarcasm"; break;
        case "expressive": sliderId = "slide-expressive"; break;
        case "strictness": sliderId = "slide-strictness"; break;
        case "naija": sliderId = "slide-naija"; break;
    }
    
    const value = parseInt(document.getElementById(sliderId).value);
    
    // Update active persona copy
    if (trait === "naija") {
        selectedPersona.dna.naija_scale = value;
    } else {
        selectedPersona.dna[trait] = value;
    }
    
    // Update labels and visual radar bars
    updateSliderLabelDisplays(selectedPersona.dna);
    renderTasteDNA(selectedPersona.dna);
    
    // Reset recommendations on sandbox adjustments
    triggerRecommendationRetrieval();
}

function renderTasteDNA(dna) {
    const barsContainer = document.querySelector(".visual-dna-bars");
    barsContainer.innerHTML = "";

    const traits = [
        { key: "Budget Conscious", val: dna.budget, icon: "fa-wallet", color: "var(--accent-emerald)" },
        { key: "Novelty Seeking", val: dna.novelty, icon: "fa-compass", color: "var(--accent-blue)" },
        { key: "Sarcasm Tendency", val: dna.sarcasm, icon: "fa-face-grimace", color: "var(--accent-rose)" },
        { key: "Verbal Expressive", val: dna.expressive, icon: "fa-paragraph", color: "var(--accent-cyan)" },
        { key: "Rating Strictness", val: dna.strictness, icon: "fa-gauge-high", color: "var(--accent-amber)" },
        { key: "Cultural Scale (Naija)", val: dna.naija_scale, icon: "fa-earth-africa", color: "var(--accent-purple)" }
    ];

    traits.forEach(t => {
        const barItem = document.createElement("div");
        barItem.className = "dna-bar-item";
        
        barItem.innerHTML = `
            <div class="dna-bar-label"><i class="fa-solid ${t.icon}"></i> ${t.key}</div>
            <div class="dna-bar-track">
                <div class="dna-bar-fill" style="width: ${t.val}%; background: ${t.color}; box-shadow: 0 0 8px ${t.color}"></div>
            </div>
            <div class="dna-bar-percent" style="color: ${t.color}">${t.val}%</div>
        `;
        barsContainer.appendChild(barItem);
    });
}

function renderCorpusHistory(history) {
    const list = document.getElementById("corpus-history-list");
    list.innerHTML = "";
    
    history.forEach(rev => {
        const item = document.createElement("div");
        item.className = "corpus-item";
        
        let stars = "";
        for (let i = 1; i <= 5; i++) {
            stars += i <= rev.rating ? '<i class="fas fa-star"></i>' : '<i class="far fa-star"></i>';
        }
        
        // Format prices elegantly
        let priceStr = rev.price ? `N${rev.price.toLocaleString()}` : "N/A";
        
        item.innerHTML = `
            <div class="corpus-meta">
                <span class="corpus-item-name">${rev.item_name} (${rev.category.toUpperCase()})</span>
                <span class="corpus-stars">${stars}</span>
            </div>
            <p class="corpus-text">"${rev.text}"</p>
        `;
        list.appendChild(item);
    });
}

// ----------------------------------------------------------------------
// 4. TASK A: REVIEW SIMULATOR OPERATIONS
// ----------------------------------------------------------------------
function loadTargetProduct() {
    const select = document.getElementById("item-select");
    const item = allItems.find(x => x.id === select.value);
    if (item) {
        selectedItem = item;
        
        const card = document.getElementById("product-spec-card");
        
        let featuresHtml = item.features.map(f => `<li>${f}</li>`).join("");
        let complaintsHtml = item.complaints.map(c => `<li>${c}</li>`).join("");
        
        let currencySymbol = item.currency === "NGN" ? "N" : "$";
        let formattedPrice = item.price != null ? item.price.toLocaleString() : "N/A";
        
        card.innerHTML = `
            <div class="spec-category-badge">${item.category}</div>
            <div class="spec-title">${item.title}</div>
            <div class="spec-price">${currencySymbol}${formattedPrice}</div>
            <hr class="card-divider" style="margin: 0.4rem 0;">
            <p class="description" style="font-size: 0.82rem;">${item.description}</p>
            <ul class="spec-features">
                ${featuresHtml}
            </ul>
            ${item.complaints.length > 0 ? `
                <div class="spec-complaints-title"><i class="fa-solid fa-circle-exclamation"></i> Common Customer Complaints:</div>
                <ul class="spec-complaints">
                    ${complaintsHtml}
                </ul>
            ` : ""}
        `;
        
        // Tweak API editor template
        updateApiEditorTemplate();
    }
}

async function triggerReviewSimulation() {
    // Check if we have either selected models or custom descriptions
    const customPersonaText = document.getElementById("custom-persona-desc-simulator") ? document.getElementById("custom-persona-desc-simulator").value.trim() : "";
    const customItemText = document.getElementById("custom-item-desc") ? document.getElementById("custom-item-desc").value.trim() : "";

    if (!customPersonaText && !selectedPersona) {
        alert("Please select a persona or enter a custom persona description!");
        return;
    }
    if (!customItemText && !selectedItem) {
        alert("Please select a product or enter a custom product description!");
        return;
    }

    // Loading indicators
    const mOut = document.getElementById("inner-monologue-output");
    const rOut = document.getElementById("written-review-output");
    
    mOut.innerHTML = '<span class="loading-prompt"><i class="fa-solid fa-spinner fa-spin"></i> Brain is thinking... (compiling behavioral twin)</span>';
    rOut.innerHTML = `
        <div class="rating-display" id="rating-output">
            <i class="far fa-star"></i><i class="far fa-star"></i><i class="far fa-star"></i><i class="far fa-star"></i><i class="far fa-star"></i>
        </div>
        <span class="loading-prompt"><i class="fa-solid fa-spinner fa-spin"></i> Formulating written review text...</span>
    `;

    try {
        let customPersonaObj = null;
        let customItemObj = null;

        // 1. If custom persona is provided, parse it
        if (customPersonaText) {
            mOut.innerHTML = '<span class="loading-prompt"><i class="fa-solid fa-spinner fa-spin"></i> Parsing custom persona details & behavioral DNA...</span>';
            const parsePersonaPayload = {
                description: customPersonaText,
                type: "persona",
                provider: currentProvider,
                api_key: currentApiKey
            };
            const parseRes = await fetch("/api/parse-custom-description", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(parsePersonaPayload)
            });
            const parseData = await parseRes.json();
            if (parseRes.status !== 200) {
                throw new Error(parseData.detail || "Failed to parse custom persona");
            }
            customPersonaObj = {
                name: parseData.name || "Custom Profile",
                domain: "all",
                description: customPersonaText,
                dna: parseData.dna,
                history: []
            };
        }

        // 2. If custom item is provided, parse it
        if (customItemText) {
            rOut.innerHTML = `
                <div class="rating-display" id="rating-output">
                    <i class="far fa-star"></i><i class="far fa-star"></i><i class="far fa-star"></i><i class="far fa-star"></i><i class="far fa-star"></i>
                </div>
                <span class="loading-prompt"><i class="fa-solid fa-spinner fa-spin"></i> Parsing custom product details & specifications...</span>
            `;
            const parseItemPayload = {
                description: customItemText,
                type: "item",
                provider: currentProvider,
                api_key: currentApiKey
            };
            const parseRes = await fetch("/api/parse-custom-description", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(parseItemPayload)
            });
            const parseData = await parseRes.json();
            if (parseRes.status !== 200) {
                throw new Error(parseData.detail || "Failed to parse custom product");
            }
            customItemObj = parseData;
        }

        // 3. Compile the simulation payload
        mOut.innerHTML = '<span class="loading-prompt"><i class="fa-solid fa-spinner fa-spin"></i> Running behavioral simulation...</span>';
        rOut.innerHTML = `
            <div class="rating-display" id="rating-output">
                <i class="far fa-star"></i><i class="far fa-star"></i><i class="far fa-star"></i><i class="far fa-star"></i><i class="far fa-star"></i>
            </div>
            <span class="loading-prompt"><i class="fa-solid fa-spinner fa-spin"></i> Generating persona-consistent review...</span>
        `;

        const payload = {
            persona_id: customPersonaObj ? "custom_sandboxed_twin" : selectedPersona.id,
            item_id: customItemObj ? "custom_sandboxed_item" : selectedItem.id,
            provider: currentProvider,
            api_key: currentApiKey
        };
        
        if (customPersonaObj) {
            payload.custom_persona = customPersonaObj;
        } else if (selectedPersona) {
            payload.custom_persona = selectedPersona;
        }

        if (customItemObj) {
            payload.custom_item = customItemObj;
        }

        const res = await fetch("/api/simulate-review", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        
        if (res.status !== 200) {
            throw new Error(data.detail || "Simulation API Failure");
        }

        // Render Outputs with typing transitions
        playSimulationResult(data.monologue, data.review, data.rating);

    } catch (err) {
        mOut.innerHTML = `<span class="placeholder-text" style="color: var(--accent-rose)"><i class="fa-solid fa-circle-xmark"></i> Failure: ${err.message}. Please verify backend health.</span>`;
        rOut.innerHTML = `<p class="placeholder-text">Waiting for simulation...</p>`;
    }
}

function playSimulationResult(monologue, review, rating) {
    const mOut = document.getElementById("inner-monologue-output");
    const rOut = document.getElementById("written-review-output");
    
    mOut.innerHTML = "";
    rOut.innerHTML = "";

    // Type Monologue first
    typeWriter(mOut, monologue, 15, () => {
        // Render Stars
        const starDiv = document.createElement("div");
        starDiv.className = "rating-display";
        starDiv.style.marginBottom = "0.8rem";
        
        let starsHtml = "";
        for (let i = 1; i <= 5; i++) {
            if (i <= Math.floor(rating)) {
                starsHtml += '<i class="fas fa-star"></i>';
            } else if (i - 0.5 === rating) {
                starsHtml += '<i class="fas fa-star-half-alt"></i>';
            } else {
                starsHtml += '<i class="far fa-star"></i>';
            }
        }
        starsHtml += ` <span style="font-size:0.85rem; color:var(--text-muted); font-weight:600; margin-left:6px;">(${rating} / 5.0)</span>`;
        starDiv.innerHTML = starsHtml;
        rOut.appendChild(starDiv);

        // Type Review
        const textPara = document.createElement("p");
        textPara.style.fontSize = "0.92rem";
        textPara.style.lineHeight = "1.6";
        rOut.appendChild(textPara);
        
        typeWriter(textPara, review, 20);
    });
}

function typeWriter(element, text, speed = 20, callback = null) {
    let index = 0;
    // Fast typing: do word by word or chunk by chunk if long text to avoid user frustration
    let words = text.split(" ");
    
    function type() {
        if (index < words.length) {
            element.textContent += (index === 0 ? "" : " ") + words[index];
            index++;
            setTimeout(type, speed);
        } else {
            if (callback) callback();
        }
    }
    type();
}

// ----------------------------------------------------------------------
// 5. TASK B: MULTI-AGENT RECOMMENDER & DEBATES
// ----------------------------------------------------------------------
async function triggerRecommendationRetrieval() {
    if (!selectedPersona) return;
    
    const list = document.getElementById("recommendations-list");
    list.innerHTML = `
        <div class="loading-prompt">
            <i class="fa-solid fa-gears fa-spin"></i> Retrieving candidates & launching multi-agent debate...
        </div>
    `;

    try {
        const payload = {
            persona_id: selectedPersona.id,
            category_filter: "all",
            provider: currentProvider,
            api_key: currentApiKey
        };
        
        if (selectedPersona.id) {
            payload.custom_persona = selectedPersona;
        }

        const res = await fetch("/api/recommend", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        
        if (res.status !== 200) {
            throw new Error(data.detail || "API Failure");
        }

        currentRecommendations = data.recommendations;
        
        // Render lists
        renderRecommendations(currentRecommendations);
        
        // Auto-select first recommendation to play debate
        if (currentRecommendations.length > 0) {
            selectDebateItem(currentRecommendations[0].item_id);
        }

    } catch (err) {
        list.innerHTML = `<div class="loading-prompt" style="color:var(--accent-rose)"><i class="fa-solid fa-triangle-exclamation"></i> Error: ${err.message}</div>`;
    }
}

function renderRecommendations(recs) {
    const list = document.getElementById("recommendations-list");
    list.innerHTML = "";
    
    if (recs.length === 0) {
        list.innerHTML = '<div class="loading-prompt">No items matching this domain query.</div>';
        return;
    }

    recs.forEach(rec => {
        const card = document.createElement("div");
        card.className = "rec-item-card" + (activeDebateItem === rec.item_id ? " active" : "");
        card.setAttribute("data-id", rec.item_id);
        card.onclick = () => selectDebateItem(rec.item_id);

        let currencySymbol = rec.currency === "NGN" ? "N" : "$";
        let formattedPrice = rec.price != null ? rec.price.toLocaleString() : "N/A";

        card.innerHTML = `
            <div class="rec-item-details">
                <div class="rec-item-title">${rec.title}</div>
                <div class="rec-item-price">${currencySymbol}${formattedPrice}</div>
                <div class="rec-item-rationales">
                    <span class="rational-pill rec"><i class="fa-solid fa-circle-check"></i> ${rec.why_recommended}</span>
                    ${rec.why_not_recommended !== "None" ? `
                        <span class="rational-pill not-rec"><i class="fa-solid fa-circle-xmark"></i> ${rec.why_not_recommended}</span>
                    ` : ""}
                </div>
            </div>
            <div class="rec-item-score-circle">${rec.predicted_rating}</div>
        `;
        list.appendChild(card);
    });
}

function filterRecommendations(category) {
    // Toggle active chip
    const chips = document.querySelectorAll(".filter-chip");
    chips.forEach(c => c.classList.remove("active"));
    event.target.classList.add("active");

    if (category === "all") {
        renderRecommendations(currentRecommendations);
    } else {
        const filtered = currentRecommendations.filter(x => x.category === category);
        renderRecommendations(filtered);
    }
}

function syncTaskBItemSelection() {
    document.getElementById("taskb-custom-title").value = "";
    document.getElementById("taskb-custom-price").value = "";
    document.getElementById("taskb-custom-desc").value = "";
}

async function triggerTaskBProductAudit() {
    if (!selectedPersona) return;

    const list = document.getElementById("recommendations-list");
    const arena = document.getElementById("debate-arena");
    
    // Clear list selection highlights temporarily
    const cards = document.querySelectorAll(".rec-item-card");
    cards.forEach(c => c.classList.remove("active"));
    
    arena.innerHTML = `
        <div class="loading-prompt">
            <i class="fa-solid fa-comments fa-spin"></i> Ingesting audited product & launching multi-agent debate...
        </div>
    `;

    // 1. Gather custom inputs if filled
    const cTitle = document.getElementById("taskb-custom-title").value.trim();
    const cPrice = document.getElementById("taskb-custom-price").value.trim();
    const cDesc = document.getElementById("taskb-custom-desc").value.trim();
    const cCurrency = document.getElementById("taskb-custom-currency").value;
    const cCategory = document.getElementById("taskb-custom-category").value;

    let payload = {
        persona_id: selectedPersona.id,
        provider: currentProvider,
        api_key: currentApiKey
    };

    if (selectedPersona.id) {
        payload.custom_persona = selectedPersona;
    }

    let customItem = null;
    let selectedPreloadedItem = null;

    if (cTitle && cDesc) {
        // Use custom item
        customItem = {
            title: cTitle,
            price: cPrice ? parseFloat(cPrice) : 15000.0,
            currency: cCurrency,
            category: cCategory,
            description: cDesc,
            features: ["Custom premium features"],
            complaints: ["Custom design complaints"],
            avg_rating: 4.0
        };
        payload.custom_item = customItem;
        payload.item_id = "custom_audit_" + Math.random().toString(36).substr(2, 6);
    } else {
        // Use preloaded item
        const pSelect = document.getElementById("taskb-item-select");
        if (!pSelect || !pSelect.value) {
            arena.innerHTML = `<div class="loading-prompt" style="color:var(--accent-rose)"><i class="fa-solid fa-triangle-exclamation"></i> Error: Select a product or fill custom fields.</div>`;
            return;
        }
        selectedPreloadedItem = allItems.find(x => x.id === pSelect.value);
        if (!selectedPreloadedItem) return;
        payload.item_id = selectedPreloadedItem.id;
    }

    try {
        const res = await fetch("/api/simulate-review", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        
        if (res.status !== 200) {
            throw new Error(data.detail || "API Failure");
        }

        // Build a mock recommendation object for Task B re-ranking
        const mockRec = {
            item_id: payload.item_id,
            title: customItem ? customItem.title : selectedPreloadedItem.title,
            category: customItem ? customItem.category : selectedPreloadedItem.category,
            price: customItem ? customItem.price : selectedPreloadedItem.price,
            currency: customItem ? customItem.currency : selectedPreloadedItem.currency,
            predicted_rating: data.rating,
            why_recommended: data.why_recommended,
            why_not_recommended: data.why_not_recommended,
            what_would_have_made_it_fail: data.what_would_have_made_it_fail,
            simulated_review: data.review,
            simulated_monologue: data.monologue,
            debate: data.debate
        };

        // Add to the top of currentRecommendations if not already present
        let existingIdx = currentRecommendations.findIndex(x => x.item_id === mockRec.item_id);
        if (existingIdx !== -1) {
            currentRecommendations[existingIdx] = mockRec;
        } else {
            currentRecommendations.unshift(mockRec);
        }

        // Render lists & highlight selected debate item
        renderRecommendations(currentRecommendations);
        selectDebateItem(mockRec.item_id);

    } catch (err) {
        arena.innerHTML = `<div class="loading-prompt" style="color:var(--accent-rose)"><i class="fa-solid fa-triangle-exclamation"></i> Error: ${err.message}</div>`;
    }
}

function selectDebateItem(itemId) {
    activeDebateItem = itemId;
    
    // Highlight active card
    const cards = document.querySelectorAll(".rec-item-card");
    cards.forEach(c => {
        if (c.getAttribute("data-id") === itemId) {
            c.classList.add("active");
        } else {
            c.classList.remove("active");
        }
    });

    const rec = currentRecommendations.find(x => x.item_id === itemId);
    if (rec) {
        document.getElementById("debate-panel-subtitle").innerHTML = `Specialist agents debating: <strong>${rec.title}</strong>`;
        
        // Show details tabs panel
        const tabsEl = document.getElementById("rec-details-tabs");
        if (tabsEl) {
            tabsEl.style.display = "flex";
        }
        
        // Restore active details panel display
        switchRecTab(activeRecTab);
        
        // Populate simulated review details
        const starsEl = document.getElementById("rec-rating-stars");
        if (starsEl) {
            let starsHtml = "";
            const r = rec.predicted_rating || 4.0;
            for (let i = 1; i <= 5; i++) {
                if (i <= Math.floor(r)) {
                    starsHtml += '<i class="fas fa-star"></i>';
                } else if (i - 0.5 === r) {
                    starsHtml += '<i class="fas fa-star-half-alt"></i>';
                } else {
                    starsHtml += '<i class="far fa-star"></i>';
                }
            }
            starsHtml += ` <span style="font-size:0.85rem; color:var(--text-muted); font-weight:600; margin-left:6px;">(${r} / 5.0 predicted delight)</span>`;
            starsEl.innerHTML = starsHtml;
        }
        
        const revTextEl = document.getElementById("rec-simulated-review-text");
        if (revTextEl) {
            revTextEl.textContent = rec.simulated_review || rec.review || "No review text simulated.";
        }
        
        const monoTextEl = document.getElementById("rec-monologue-text");
        if (monoTextEl) {
            monoTextEl.textContent = rec.simulated_monologue || rec.monologue || "No monologue simulated.";
        }
        
        const failTextEl = document.getElementById("rec-counterfactual-text");
        if (failTextEl) {
            failTextEl.textContent = rec.what_would_have_made_it_fail || "No counterfactual failure reasons specified.";
        }

        playAgentDebateSequence(rec.debate);
    }
}

function playAgentDebateSequence(debate) {
    const arena = document.getElementById("debate-arena");
    arena.innerHTML = "";
    
    let index = 0;
    
    function playNextBubble() {
        if (index < debate.length) {
            const step = debate[index];
            const bubble = document.createElement("div");
            
            let agentClass = step.agent.toLowerCase().replace(/\s+/g, '-');
            bubble.className = `debate-bubble ${agentClass}`;
            
            bubble.innerHTML = `
                <div class="debate-avatar">${step.avatar}</div>
                <div class="debate-text-card">
                    <div class="debate-sender">${step.agent}</div>
                    <div class="debate-message" id="debate-msg-${index}"></div>
                    <div class="debate-item-score">Score Focus: ${step.score}</div>
                </div>
            `;
            
            arena.appendChild(bubble);
            arena.scrollTop = arena.scrollHeight; // auto scroll
            
            // Type message
            const msgContainer = document.getElementById(`debate-msg-${index}`);
            typeWriter(msgContainer, step.text, 15, () => {
                index++;
                setTimeout(playNextBubble, 600); // delay before next agent enters
            });
        }
    }
    
    playNextBubble();
}

// ----------------------------------------------------------------------
// 6. API PLAYGROUND OPERATIONS
// ----------------------------------------------------------------------
function updateApiEditorTemplate() {
    const editor = document.getElementById("api-request-editor");
    if (!selectedPersona || !selectedItem) return;
    
    const sampleBody = {
        persona_id: selectedPersona.id,
        item_id: selectedItem.id,
        provider: currentProvider
    };
    
    editor.value = JSON.stringify(sampleBody, null, 2);
}

async function sendApiRequest() {
    const editorValue = document.getElementById("api-request-editor").value;
    const viewer = document.getElementById("api-response-viewer");
    
    viewer.textContent = "Sending request to FastAPI backend server...\n(Orchestrating agent pipelines)";
    
    try {
        const payload = JSON.parse(editorValue);
        
        // Auto-inject session API key if LLM provider selected
        if (payload.provider !== "heuristic" && currentApiKey) {
            payload.api_key = currentApiKey;
        }

        // We check if the request matches Task A or Task B to choose the correct endpoint
        let endpoint = "/api/simulate-review";
        if (payload.category_filter !== undefined || payload.item_id === undefined) {
            endpoint = "/api/recommend";
        }

        const res = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        
        viewer.textContent = JSON.stringify(data, null, 2);

    } catch (err) {
        viewer.textContent = `Error: ${err.message}\nEnsure request is valid JSON.`;
    }
}

// ----------------------------------------------------------------------
// 7. NAVIGATION & TAB SWITCHING
// ----------------------------------------------------------------------
function switchTab(tabId) {
    activeTab = tabId;
    
    // Update navigation buttons
    const tabs = document.querySelectorAll(".nav-tab");
    tabs.forEach(t => {
        if (t.getAttribute("data-tab") === tabId) {
            t.classList.add("active");
        } else {
            t.classList.remove("active");
        }
    });

    // Update content blocks
    const contents = document.querySelectorAll(".tab-content");
    contents.forEach(c => {
        if (c.getAttribute("id") === tabId) {
            c.classList.add("active");
        } else {
            c.classList.remove("active");
        }
    });
    
    // Play debate sequence again if switching to Task B
    if (tabId === "tab-taskb" && activeDebateItem) {
        setTimeout(() => {
            selectDebateItem(activeDebateItem);
        }, 100);
    }
    
    // Re-draw Taste Map when its tab becomes active, as canvases drawn while hidden have 0 width/height
    if (tabId === "tab-taste-map" && selectedPersona) {
        setTimeout(() => {
            syncTasteMap();
        }, 50);
    }
}

function switchPaperTab(paperTabId) {
    // Update active tab buttons
    const tabs = document.querySelectorAll(".paper-tab");
    tabs.forEach(t => {
        if (t.getAttribute("onclick").includes(paperTabId)) {
            t.classList.add("active");
        } else {
            t.classList.remove("active");
        }
    });

    // Update active page content
    const contents = document.querySelectorAll(".paper-section-content");
    contents.forEach(c => {
        if (c.getAttribute("id") === paperTabId) {
            c.classList.add("active");
        } else {
            c.classList.remove("active");
        }
    });
}

// ----------------------------------------------------------------------
// 8. INTERACTIVE TASTE MAP CANVAS RENDERER & DATA SYNC
// ----------------------------------------------------------------------
async function syncTasteMap() {
    if (!selectedPersona) return;
    
    try {
        const res = await fetch(`/api/taste-map?persona_id=${selectedPersona.id}`);
        const data = await res.json();
        
        // Populate Neighbors List
        const neighborsList = document.getElementById("taste-map-neighbors");
        neighborsList.innerHTML = "";
        data.neighbors.forEach(neigh => {
            const card = document.createElement("div");
            card.className = "rec-item-card";
            card.style.cursor = "default";
            
            const simPercent = Math.round(neigh[2] * 100);
            
            card.innerHTML = `
                <div class="rec-item-details">
                    <div class="rec-item-title">${neigh[1]}</div>
                    <div style="font-size:0.75rem; color:var(--text-secondary);">ID: ${neigh[0]}</div>
                </div>
                <div class="rec-item-score-circle" style="background:linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-cyan) 100%); font-size:0.85rem;">
                    ${simPercent}%
                </div>
            `;
            neighborsList.appendChild(card);
        });
        
        // Populate Timeline
        const timelineList = document.getElementById("taste-map-timeline");
        timelineList.innerHTML = "";
        selectedPersona.history.forEach((rev, idx) => {
            const timelineItem = document.createElement("div");
            timelineItem.className = "corpus-item";
            timelineItem.style.position = "relative";
            timelineItem.style.paddingLeft = "1.5rem";
            timelineItem.style.borderLeft = "2px solid var(--accent-purple)";
            timelineItem.style.marginLeft = "0.5rem";
            
            let stars = "";
            for (let i = 1; i <= 5; i++) {
                stars += i <= rev.rating ? '<i class="fas fa-star" style="color:var(--accent-amber);"></i>' : '<i class="far fa-star"></i>';
            }
            
            timelineItem.innerHTML = `
                <div style="position:absolute; left:-6px; top:12px; width:10px; height:10px; border-radius:50%; background:var(--accent-purple); box-shadow:0 0 6px var(--accent-purple);"></div>
                <div class="corpus-meta">
                    <span class="corpus-item-name">${rev.item_name}</span>
                    <span class="corpus-stars">${stars}</span>
                </div>
                <div style="font-size:0.7rem; color:var(--text-muted); text-transform:uppercase;">${rev.category} | N${rev.price.toLocaleString()}</div>
                <p class="corpus-text" style="margin-top:0.2rem;">"${rev.text}"</p>
            `;
            timelineList.appendChild(timelineItem);
        });
        
        // Draw Interactive Canvas
        drawTasteMap(data.graph);
        
    } catch (err) {
        console.error("Failed to sync taste map: ", err);
    }
}

function drawTasteMap(graph) {
    const canvas = document.getElementById("taste-map-canvas");
    if (!canvas) return;
    
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * window.devicePixelRatio;
    canvas.height = rect.height * window.devicePixelRatio;
    
    const ctx = canvas.getContext("2d");
    ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
    
    const width = rect.width;
    const height = rect.height;
    
    ctx.clearRect(0, 0, width, height);
    
    const nodes = graph.nodes;
    const edges = graph.edges;
    
    const centerX = width / 2;
    const centerY = height / 2;
    
    // Distribute nodes visually
    nodes.forEach(node => {
        if (node.id === "user_active") {
            node.x = centerX;
            node.y = centerY;
        } else if (node.group === "category") {
            const idx = nodes.filter(n => n.group === "category").indexOf(node);
            const count = nodes.filter(n => n.group === "category").length;
            const angle = (idx / count) * 2 * Math.PI;
            const radius = Math.min(width, height) * 0.38;
            node.x = centerX + Math.cos(angle) * radius;
            node.y = centerY + Math.sin(angle) * radius;
        } else if (node.group === "neighbor") {
            const idx = nodes.filter(n => n.group === "neighbor").indexOf(node);
            const count = nodes.filter(n => n.group === "neighbor").length;
            const angle = (idx / count) * 2 * Math.PI + 0.5;
            const radius = Math.min(width, height) * 0.22;
            node.x = centerX + Math.cos(angle) * radius;
            node.y = centerY + Math.sin(angle) * radius;
        } else {
            const idx = nodes.filter(n => n.group === "item_history").indexOf(node);
            const count = nodes.filter(n => n.group === "item_history").length;
            const angle = (idx / count) * 2 * Math.PI - 0.5;
            const radius = Math.min(width, height) * 0.45;
            node.x = centerX + Math.cos(angle) * radius;
            node.y = centerY + Math.sin(angle) * radius;
        }
    });
    
    // Draw links
    edges.forEach(edge => {
        const fromNode = nodes.find(n => n.id === edge.from);
        const toNode = nodes.find(n => n.id === edge.to);
        
        if (fromNode && toNode) {
            ctx.beginPath();
            ctx.moveTo(fromNode.x, fromNode.y);
            ctx.lineTo(toNode.x, toNode.y);
            
            ctx.lineWidth = edge.weight || 1;
            if (edge.label.includes("rated")) {
                ctx.strokeStyle = "rgba(168, 85, 247, 0.15)";
            } else if (edge.label.includes("similarity")) {
                ctx.strokeStyle = "rgba(59, 130, 246, 0.3)";
            } else {
                ctx.strokeStyle = "rgba(6, 182, 212, 0.25)";
            }
            ctx.stroke();
        }
    });
    
    // Draw nodes
    nodes.forEach(node => {
        ctx.beginPath();
        const size = node.size || 10;
        ctx.arc(node.x, node.y, size, 0, 2 * Math.PI);
        
        let color = "var(--accent-purple)";
        let glowColor = "rgba(168, 85, 247, 0.6)";
        if (node.id === "user_active") {
            color = "#f43f5e";
            glowColor = "rgba(244, 63, 94, 0.8)";
        } else if (node.group === "neighbor") {
            color = "#3b82f6";
            glowColor = "rgba(59, 130, 246, 0.7)";
        } else if (node.group === "category") {
            color = "#10b981";
            glowColor = "rgba(16, 185, 129, 0.6)";
        } else if (node.group === "item_history") {
            color = "#f59e0b";
            glowColor = "rgba(245, 158, 11, 0.4)";
        }
        
        ctx.shadowColor = glowColor;
        ctx.shadowBlur = 10;
        ctx.fillStyle = color;
        ctx.fill();
        
        ctx.shadowBlur = 0;
        
        ctx.beginPath();
        ctx.arc(node.x, node.y, size * 0.4, 0, 2 * Math.PI);
        ctx.fillStyle = "#ffffff";
        ctx.fill();
        
        ctx.fillStyle = "rgba(243, 244, 246, 0.85)";
        ctx.font = "bold 9px 'Inter', sans-serif";
        ctx.textAlign = "center";
        ctx.fillText(node.label, node.x, node.y + size + 11);
    });
}

window.addEventListener("resize", () => {
    if (activeTab === "tab-taste-map" && selectedPersona) {
        syncTasteMap();
    }
});

// ----------------------------------------------------------------------
// 9. PROFILER INTERVIEWER CHATBOT
// ----------------------------------------------------------------------
let chatbotHistory = [];
let chatbotDNA = {
    budget: 50.0,
    novelty: 50.0,
    sarcasm: 50.0,
    expressive: 50.0,
    strictness: 50.0,
    naija_scale: 50.0
};

function initChatbotDNA() {
    if (selectedPersona) {
        chatbotDNA = JSON.parse(JSON.stringify(selectedPersona.dna));
        renderChatbotDNA(chatbotDNA);
    }
}

function renderChatbotDNA(dna) {
    const barsContainer = document.getElementById("chatbot-dna-bars");
    if (!barsContainer) return;
    barsContainer.innerHTML = "";

    const traits = [
        { key: "Budget Conscious", val: dna.budget, icon: "fa-wallet", color: "var(--accent-emerald)" },
        { key: "Novelty Seeking", val: dna.novelty, icon: "fa-compass", color: "var(--accent-blue)" },
        { key: "Sarcasm Tendency", val: dna.sarcasm, icon: "fa-face-grimace", color: "var(--accent-rose)" },
        { key: "Verbal Expressive", val: dna.expressive, icon: "fa-paragraph", color: "var(--accent-cyan)" },
        { key: "Rating Strictness", val: dna.strictness, icon: "fa-gauge-high", color: "var(--accent-amber)" },
        { key: "Cultural Scale (Naija)", val: dna.naija_scale, icon: "fa-earth-africa", color: "var(--accent-purple)" }
    ];

    traits.forEach(t => {
        const barItem = document.createElement("div");
        barItem.className = "dna-bar-item";
        barItem.style.marginBottom = "0.7rem";
        
        barItem.innerHTML = `
            <div class="dna-bar-label" style="font-size:0.78rem;"><i class="fa-solid ${t.icon}"></i> ${t.key}</div>
            <div class="dna-bar-track" style="height:10px;">
                <div class="dna-bar-fill" style="width: ${t.val}%; background: ${t.color}; box-shadow: 0 0 6px ${t.color}"></div>
            </div>
            <div class="dna-bar-percent" style="color: ${t.color}; font-size:0.75rem;">${t.val}%</div>
        `;
        barsContainer.appendChild(barItem);
    });
}

async function sendChatbotMessage() {
    const input = document.getElementById("chatbot-input");
    const msgText = input.value.trim();
    if (!msgText) return;
    
    input.value = "";
    
    const feed = document.getElementById("chatbot-feed");
    
    // Add User Bubble
    const userBubble = document.createElement("div");
    userBubble.className = "chat-bubble user";
    userBubble.innerHTML = `
        <div class="chat-sender">You 👤</div>
        <div class="chat-message-text">${msgText}</div>
    `;
    feed.appendChild(userBubble);
    feed.scrollTop = feed.scrollHeight;
    
    // Add Loading Assistant Bubble
    const loadingBubble = document.createElement("div");
    loadingBubble.className = "chat-bubble assistant";
    loadingBubble.innerHTML = `
        <div class="chat-sender">Psychologist Agent 🧠</div>
        <div class="chat-message-text" id="chatbot-loading-text"><i class="fa-solid fa-spinner fa-spin"></i> Analyzing context clues & thinking...</div>
    `;
    feed.appendChild(loadingBubble);
    feed.scrollTop = feed.scrollHeight;
    
    try {
        const payload = {
            message: msgText,
            history: chatbotHistory,
            current_dna: chatbotDNA,
            provider: currentProvider,
            api_key: currentApiKey
        };
        
        const res = await fetch("/api/chatbot", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        
        const data = await res.json();
        if (res.status !== 200) {
            throw new Error(data.detail || "Chatbot connection error");
        }
        
        feed.removeChild(loadingBubble);
        
        // Add Real Assistant Bubble
        const assistantBubble = document.createElement("div");
        assistantBubble.className = "chat-bubble assistant";
        assistantBubble.innerHTML = `
            <div class="chat-sender">Psychologist Agent 🧠</div>
            <div class="chat-message-text" id="chatbot-msg-${chatbotHistory.length}"></div>
        `;
        feed.appendChild(assistantBubble);
        feed.scrollTop = feed.scrollHeight;
        
        const msgContainer = document.getElementById(`chatbot-msg-${chatbotHistory.length}`);
        typeWriter(msgContainer, data.reply, 15, () => {
            if (data.explanation) {
                const expl = document.createElement("div");
                expl.style.fontSize = "0.75rem";
                expl.style.color = "rgba(255,255,255,0.4)";
                expl.style.marginTop = "0.5rem";
                expl.style.fontStyle = "italic";
                expl.innerHTML = `<i class="fa-solid fa-microchip"></i> Agent Reasoning: ${data.explanation}`;
                assistantBubble.appendChild(expl);
                feed.scrollTop = feed.scrollHeight;
            }
            
            chatbotDNA = data.updated_dna;
            renderChatbotDNA(chatbotDNA);
            
            document.getElementById("chatbot-clues-explanation").textContent = data.explanation || "No clues parsed.";
            if (selectedPersona) {
                selectedPersona.dna = JSON.parse(JSON.stringify(chatbotDNA));
                loadPersonaValuesToUI(selectedPersona);
                renderTasteDNA(selectedPersona.dna);
            }

            // Append recommendation card or alert after chatbot has finished speaking
            if (data.catalog_alert) {
                const alertCard = document.createElement("div");
                alertCard.className = "chatbot-rec-card";
                alertCard.style.borderLeft = "4px solid var(--accent-rose)";
                alertCard.innerHTML = `
                    <div style="font-weight:bold; display:flex; align-items:center; gap:6px; color:#f87171; margin-bottom:0.3rem;">
                        <i class="fa-solid fa-triangle-exclamation"></i> [TasteTwin Alarm] Shortage Triggered
                    </div>
                    <div>No items in our active catalog matched your high standards (predicted delight &lt; 4.0★). A backend shortage notification was logged!</div>
                `;
                feed.appendChild(alertCard);
                feed.scrollTop = feed.scrollHeight;
            } else if (data.recommended_item) {
                const rec = data.recommended_item;
                const recCard = document.createElement("div");
                recCard.className = "chatbot-rec-card";
                
                let stars = "";
                const r = rec.predicted_rating || 4.0;
                for (let i = 1; i <= 5; i++) {
                    stars += i <= Math.floor(r) ? '<i class="fas fa-star"></i>' : '<i class="far fa-star"></i>';
                }
                
                let currencySymbol = rec.currency === "NGN" ? "N" : "$";
                let formattedPrice = rec.price ? rec.price.toLocaleString() : "N/A";
                
                recCard.innerHTML = `
                    <div class="chatbot-rec-header">
                        <span class="chatbot-rec-title"><i class="fa-solid fa-gift"></i> TasteTwin Choice: ${rec.title}</span>
                        <span class="chatbot-rec-price">${currencySymbol}${formattedPrice}</span>
                    </div>
                    <div class="chatbot-rec-rating">
                        ${stars} <span style="margin-left:6px; color:var(--text-muted); font-size:0.75rem;">(${r}★ delight)</span>
                    </div>
                    
                    <div class="chatbot-rec-section-title">Simulated Future Review</div>
                    <div class="chatbot-rec-review">"${rec.simulated_review || rec.review}"</div>
                    
                    ${rec.simulated_monologue || rec.monologue ? `
                        <div class="chatbot-rec-section-title">User Inner Thoughts</div>
                        <div class="chatbot-rec-monologue">"${rec.simulated_monologue || rec.monologue}"</div>
                    ` : ""}
                `;
                
                feed.appendChild(recCard);
                feed.scrollTop = feed.scrollHeight;
            }
        });
        
        chatbotHistory.push({ role: "user", content: msgText });
        chatbotHistory.push({ role: "assistant", content: data.reply });
        
    } catch (err) {
        document.getElementById("chatbot-loading-text").innerHTML = `<span style="color:var(--accent-rose)"><i class="fa-solid fa-triangle-exclamation"></i> Error: ${err.message}</span>`;
    }
}

function handleChatbotKey(event) {
    if (event.key === "Enter") {
        sendChatbotMessage();
    }
}

// ----------------------------------------------------------------------
// 10. CUSTOM CREATOR BINDINGS
// ----------------------------------------------------------------------
async function parseCustomPersonaDNA() {
    const desc = document.getElementById("custom-persona-desc").value.trim();
    if (!desc) {
        alert("Please enter a description for the persona!");
        return;
    }
    
    const textarea = document.getElementById("custom-persona-desc");
    const originalText = textarea.value;
    textarea.value = "Compiling & parsing persona DNA with TasteTwin behavioral parser...";
    textarea.disabled = true;
    
    try {
        const payload = {
            description: desc,
            type: "persona",
            provider: currentProvider,
            api_key: currentApiKey
        };
        
        const res = await fetch("/api/parse-custom-description", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        
        const data = await res.json();
        if (res.status !== 200) {
            throw new Error(data.detail || "API parse error");
        }
        
        selectedPersona = {
            id: "custom_sandboxed_twin",
            name: data.name || "Custom Persona Twin",
            domain: "all",
            description: desc,
            dna: data.dna,
            history: selectedPersona ? selectedPersona.history : []
        };
        
        loadPersonaValuesToUI(selectedPersona);
        renderTasteDNA(selectedPersona.dna);
        
        const pSelect = document.getElementById("persona-select");
        let optionExists = false;
        for (let i = 0; i < pSelect.options.length; i++) {
            if (pSelect.options[i].value === "custom_sandboxed_twin") {
                optionExists = true;
                break;
            }
        }
        if (!optionExists) {
            const opt = document.createElement("option");
            opt.value = "custom_sandboxed_twin";
            opt.textContent = `${selectedPersona.name} (CUSTOM)`;
            pSelect.appendChild(opt);
        }
        pSelect.value = "custom_sandboxed_twin";
        
        triggerRecommendationRetrieval();
        textarea.value = originalText;
    } catch (err) {
        alert("Failed to parse custom persona: " + err.message);
        textarea.value = originalText;
    } finally {
        textarea.disabled = false;
    }
}

async function parseCustomItemDNA() {
    const desc = document.getElementById("custom-item-desc").value.trim();
    if (!desc) {
        alert("Please enter a description for the product!");
        return;
    }
    
    const textarea = document.getElementById("custom-item-desc");
    const originalText = textarea.value;
    textarea.value = "Parsing specifications & customer complaints from description...";
    textarea.disabled = true;
    
    try {
        const payload = {
            description: desc,
            type: "item",
            provider: currentProvider,
            api_key: currentApiKey
        };
        
        const res = await fetch("/api/parse-custom-description", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        
        const data = await res.json();
        if (res.status !== 200) {
            throw new Error(data.detail || "API parse error");
        }
        
        selectedItem = {
            id: "custom_sandboxed_item",
            title: data.title || "Custom Product",
            category: data.category || "electronics",
            price: data.price || 10000.0,
            currency: data.currency || "NGN",
            description: data.description || desc,
            features: data.features || ["Premium build"],
            complaints: data.complaints || []
        };
        
        const iSelect = document.getElementById("item-select");
        let optionExists = false;
        for (let i = 0; i < iSelect.options.length; i++) {
            if (iSelect.options[i].value === "custom_sandboxed_item") {
                optionExists = true;
                break;
            }
        }
        if (!optionExists) {
            const opt = document.createElement("option");
            opt.value = "custom_sandboxed_item";
            opt.textContent = `${selectedItem.title} (CUSTOM)`;
            iSelect.appendChild(opt);
        }
        iSelect.value = "custom_sandboxed_item";
        
        loadTargetProduct();
        textarea.value = originalText;
    } catch (err) {
        alert("Failed to parse custom product: " + err.message);
        textarea.value = originalText;
    } finally {
        textarea.disabled = false;
    }
}

// ----------------------------------------------------------------------
// 11. LEAVE-ONE-OUT CROSS VALIDATION
// ----------------------------------------------------------------------
async function runLOOEvaluation() {
    document.getElementById("loo-rmse").innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
    document.getElementById("loo-rouge").innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
    document.getElementById("loo-hitrate").innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
    document.getElementById("loo-ndcg").innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
    
    try {
        const res = await fetch("/api/evaluate");
        const data = await res.json();
        
        if (res.status !== 200) {
            throw new Error(data.detail || "Evaluation error");
        }
        
        document.getElementById("loo-rmse").textContent = data.rmse.toFixed(3);
        document.getElementById("loo-rouge").textContent = (data.rouge_l * 100).toFixed(1) + "%";
        document.getElementById("loo-hitrate").textContent = (data.hit_rate * 100).toFixed(1) + "%";
        document.getElementById("loo-ndcg").textContent = (data.ndcg * 100).toFixed(1) + "%";
        
    } catch (err) {
        alert("Evaluation failed: " + err.message);
        document.getElementById("loo-rmse").textContent = "ERR";
        document.getElementById("loo-rouge").textContent = "ERR";
        document.getElementById("loo-hitrate").textContent = "ERR";
        document.getElementById("loo-ndcg").textContent = "ERR";
    }
}

// ----------------------------------------------------------------------
// 12. DRAG & DROP FILE INGESTOR
// ----------------------------------------------------------------------
function triggerFileSelect() {
    document.getElementById("jsonl-file-input").click();
}

function handleDragOver(e) {
    e.preventDefault();
    const zone = document.getElementById("drag-drop-zone");
    zone.style.borderColor = "var(--accent-cyan)";
    zone.style.background = "rgba(6, 182, 212, 0.05)";
}

function handleDragLeave(e) {
    e.preventDefault();
    const zone = document.getElementById("drag-drop-zone");
    zone.style.borderColor = "rgba(255, 255, 255, 0.1)";
    zone.style.background = "rgba(255, 255, 255, 0.01)";
}

function handleFileDrop(e) {
    e.preventDefault();
    handleDragLeave(e);
    
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files.length > 0) {
        processUploadedFile(files[0]);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        processUploadedFile(files[0]);
    }
}

function processUploadedFile(file) {
    const reader = new FileReader();
    const statusLog = document.getElementById("ingest-status-log");
    
    statusLog.textContent = "Reading file...";
    
    reader.onload = async (e) => {
        const textContent = e.target.result;
        statusLog.textContent = "Streaming dataset into memory...";
        
        try {
            const res = await fetch("/api/ingest-dataset", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ content: textContent })
            });
            
            const data = await res.json();
            if (res.status !== 200) {
                throw new Error(data.detail || "Ingestion API failure");
            }
            
            statusLog.innerHTML = `<i class="fa-solid fa-circle-check"></i> Ingestion Successful! Ingested ${data.ingested_personas} personas and ${data.ingested_items} items.`;
            
            const resPersonas = await fetch("/api/personas");
            allPersonas = await resPersonas.json();
            
            const resItems = await fetch("/api/items");
            allItems = await resItems.json();
            
            populateSelectors();
            
        } catch (err) {
            statusLog.innerHTML = `<span style="color:var(--accent-rose)"><i class="fa-solid fa-triangle-exclamation"></i> Ingestion failed: ${err.message}</span>`;
        }
    };
    reader.readAsText(file);
}

// ----------------------------------------------------------------------
// 13. COORDINATE DESCENT WEIGHTS TRAINER
// ----------------------------------------------------------------------
async function trainWeights() {
    const consoleBox = document.getElementById("training-console");
    consoleBox.innerHTML = "> Initiating Coordinate Descent weight tuning optimizer...\n";
    
    try {
        const res = await fetch("/api/train-weights", { method: "POST" });
        const data = await res.json();
        
        if (res.status !== 200) {
            throw new Error(data.detail || "Weights training failure");
        }
        
        let index = 0;
        const logs = data.logs;
        
        function printNextLog() {
            if (index < logs.length) {
                consoleBox.innerHTML += `> ${logs[index]}\n`;
                consoleBox.scrollTop = consoleBox.scrollHeight;
                index++;
                setTimeout(printNextLog, 450);
            } else {
                consoleBox.innerHTML += `\n> Optimization complete! Final minimized RMSE: ${data.rmse.toFixed(4)}\n`;
                consoleBox.innerHTML += `> In-memory weights synchronized across all simulator instances successfully. ✓`;
                consoleBox.scrollTop = consoleBox.scrollHeight;
            }
        }
        
        printNextLog();
        
    } catch (err) {
        consoleBox.innerHTML += `\n> [FATAL ERROR] Optimization loop aborted: ${err.message}\n`;
        consoleBox.scrollTop = consoleBox.scrollHeight;
    }
}

async function streamAmazonDataset() {
    const category = document.getElementById("amazon-category-select").value;
    const limit = parseInt(document.getElementById("amazon-limit-select").value);
    
    const streamBtn = document.getElementById("amazon-stream-btn");
    const statusLog = document.getElementById("amazon-status-log");
    const consoleBox = document.getElementById("training-console");
    
    streamBtn.disabled = true;
    streamBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Streaming...';
    statusLog.style.color = "var(--accent-cyan)";
    statusLog.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> Connecting to Hugging Face and streaming <b>${category}</b> dataset...`;
    
    consoleBox.innerHTML = `> [TasteTwin Ingestion] Contacting Hugging Face McAuley-Lab/Amazon-Reviews-2023 for raw_review_${category} and raw_meta_${category}...\n`;
    consoleBox.innerHTML += `> [TasteTwin Ingestion] streaming=True enabled to prevent high disk/RAM footprint.\n`;
    consoleBox.innerHTML += `> [TasteTwin Ingestion] Streaming limit set to ${limit} elements. Please wait, fetching real reviews on the fly...\n`;
    consoleBox.scrollTop = consoleBox.scrollHeight;
    
    try {
        const payload = {
            category: category,
            limit: limit
        };
        
        const res = await fetch("/api/load-amazon", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        
        const data = await res.json();
        if (res.status !== 200) {
            throw new Error(data.detail || "FastAPI Hugging Face API Ingestion Error");
        }
        
        statusLog.style.color = "var(--accent-emerald)";
        statusLog.innerHTML = `<i class="fa-solid fa-circle-check"></i> Ingested <b>${data.personas_count}</b> custom customer twins & <b>${data.items_count}</b> items from real Amazon dataset!`;
        
        consoleBox.innerHTML += `\n> [TasteTwin Core] Database Dynamic Swap successful! Active PERSONAS: ${data.personas_count}, ITEMS: ${data.items_count}\n`;
        consoleBox.innerHTML += `> [TasteTwin Core] Refitting TF-IDF Vectorizers and Taste DNA embedding maps on Amazon corpus...\n`;
        consoleBox.scrollTop = consoleBox.scrollHeight;
        
        // Print coordinate descent training logs
        let index = 0;
        const logs = data.logs || [];
        
        function printNextLog() {
            if (index < logs.length) {
                consoleBox.innerHTML += `> ${logs[index]}\n`;
                consoleBox.scrollTop = consoleBox.scrollHeight;
                index++;
                setTimeout(printNextLog, 400);
            } else {
                consoleBox.innerHTML += `\n> Optimization complete! Final minimized RMSE: ${data.optimized_rmse.toFixed(4)}\n`;
                consoleBox.innerHTML += `> In-memory weights synchronized across all simulator instances successfully. ✓`;
                consoleBox.scrollTop = consoleBox.scrollHeight;
            }
        }
        
        printNextLog();
        
        // Refresh session database in memory
        const resPersonas = await fetch("/api/personas");
        allPersonas = await resPersonas.json();
        
        const resItems = await fetch("/api/items");
        allItems = await resItems.json();
        
        populateSelectors();
        
        // Load default persona and item from new database
        if (allPersonas.length > 0) {
            selectedPersona = JSON.parse(JSON.stringify(allPersonas[0]));
            loadPersonaValuesToUI(selectedPersona);
            renderTasteDNA(selectedPersona.dna);
            renderCorpusHistory(selectedPersona.history);
            syncTasteMap();
            initChatbotDNA();
        }
        if (allItems.length > 0) {
            selectedItem = allItems[0];
            loadTargetProduct();
        }
        
        triggerRecommendationRetrieval();
        
    } catch (err) {
        statusLog.style.color = "var(--accent-rose)";
        statusLog.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> Streaming Failed: ${err.message}`;
        consoleBox.innerHTML += `\n> [FATAL ERROR] Ingestion & Optimization aborted: ${err.message}\n`;
        consoleBox.scrollTop = consoleBox.scrollHeight;
    } finally {
        streamBtn.disabled = false;
        streamBtn.innerHTML = '<i class="fa-solid fa-cloud-arrow-down"></i> Stream & Train';
    }
}

// ----------------------------------------------------------------------
// 14. NEW FEATURES CORE HANDLERS (COLD START & ARENA TABS)
// ----------------------------------------------------------------------
function switchRecTab(tabName) {
    activeRecTab = tabName;
    // 1. Toggle active class on tab buttons
    const btns = document.querySelectorAll(".rec-tab-btn");
    btns.forEach(btn => {
        if (btn.getAttribute("onclick").includes(tabName)) {
            btn.classList.add("active");
            btn.style.color = "#fff";
        } else {
            btn.classList.remove("active");
            btn.style.color = "var(--text-secondary)";
        }
    });

    // 2. Toggle panels visibility
    const debatePanel = document.getElementById("debate-arena");
    const reviewPanel = document.getElementById("rec-future-review-panel");
    const monologuePanel = document.getElementById("rec-monologue-panel");
    const counterfactualsPanel = document.getElementById("rec-counterfactuals-panel");

    if (debatePanel) debatePanel.style.display = tabName === "debate" ? "block" : "none";
    if (reviewPanel) reviewPanel.style.display = tabName === "future-review" ? "block" : "none";
    if (monologuePanel) monologuePanel.style.display = tabName === "monologue" ? "block" : "none";
    if (counterfactualsPanel) counterfactualsPanel.style.display = tabName === "counterfactuals" ? "block" : "none";
}

async function synthesizeColdStartTwin() {
    const descText = document.getElementById("cold-start-desc").value.trim();
    if (!descText) {
        alert("Please enter a description for the cold-start synthesis!");
        return;
    }
    
    const btn = document.getElementById("cold-start-btn");
    const originalHtml = btn.innerHTML;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Synthesizing Twin...';
    btn.disabled = true;
    
    try {
        const payload = {
            description: descText,
            provider: currentProvider,
            api_key: currentApiKey
        };
        
        const res = await fetch("/api/cold-start", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        
        const data = await res.json();
        if (res.status !== 200) {
            throw new Error(data.detail || "Cold-start API failure");
        }
        
        // Append synthesized twin to allPersonas
        allPersonas.push(data);
        
        // Update selectors
        populateSelectors();
        
        // Select it
        const pSelect = document.getElementById("persona-select");
        pSelect.value = data.id;
        loadSelectedPersona();
        
        // Switch tab to DNA sandbox so the user sees the newly compiled twin!
        switchTab("tab-sandbox");
        
        // Alert success
        alert(`Successfully synthesized behavioral digital twin: ${data.name}!`);
        
    } catch (err) {
        alert("Cold-start synthesis failed: " + err.message);
    } finally {
        btn.innerHTML = originalHtml;
        btn.disabled = false;
    }
}
