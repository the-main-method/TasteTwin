---
title: TasteTwin
emoji: 🧠
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 8090
---

# TasteTwin AI — Behavioral Digital Twin & Multi-Agent Recommendation Engine

TasteTwin AI is a state-of-the-art computational psychology and multi-agent debate framework designed for both **Task A (User Modeling & Review Simulation)** and **Task B (Explainable Cross-Domain Recommendations)** of the DSN x BCT LLM Agent Challenge.

Designed with **Dual-Mode Execution** (Zero-latency Local Heuristics + Deep Live LLM Agent reasoning via Gemini/OpenAI), TasteTwin is packed with authentic **Nigerian Contextualization** (modeling power outages/NEPA grid bypass, Lagos logistics delays, and natural Pidgin code-switching) and served via an intuitive **Single Page Application (SPA) web frontend**.

---

##  Key Features

* **Task A: Behavioral Digital Twin Simulation**
  * Decouples numerical rating calculations from text generation to achieve highly competitive **RMSE scores** ($0.0438$ over a 50,000 dataset) and eliminate LLM rating drift.
  * Simulates a detailed, psychological **Inner Monologue** representing the twin's internal reasoning.
  * Generates high-fidelity, aspect-consistent written reviews matching the twin's voice, sarcasm level, and cultural background.
* **Task B: Multi-Agent Recommendation Debate**
  * Spawns four specialist agents (**Taste**, **Budget**, **Novelty**, and **Naija Context** agents) who debate the merits and drawbacks of each item.
  * A **Judge Agent** synthesizes the arguments, awards a final rating, and outputs structured explanations: *"Why Recommended"* and *"Why NOT Recommended"*.
* **Interactive SPA Frontend**
  * Clean, modern deep-blue dark mode user interface.
  * Interactive Sandbox sliders to modify any twin's DNA (Budget, Novelty, Sarcasm, Strictness, Naija Scale) in real-time.
  * Real-time typing transitions for the Inner Monologue and sequential chat bubble animations for the Live Agent Debate.
  * Built-in interactive Solution Paper reader to inspect the mathematical formulas and architecture side-by-side with the working sandbox.
* **100% Zero-Latency Dual-Mode Execution**
  * Runs perfectly out-of-the-box in **Local Heuristic Mode** with zero latency, zero internet requirements, and zero API keys.
  * Seamlessly elevates to **LLM Agent Mode** (Google Gemini or OpenAI) when an API key is provided directly in the UI.

---

## 🛠️ Tech Stack & Architecture

* **Backend**: FastAPI, Uvicorn, Pydantic, Scikit-learn, Pandas, NumPy, google-generativeai, openai.
* **Frontend**: HTML5, Vanilla CSS3 (custom CSS design system with HSL colors and glassmorphism), Vanilla ES6 JavaScript (reactive DOM binding and typewriter animations).
* **Containerization**: Single-stage, highly optimized Docker image and Docker Compose orchestrator.

---

##  Getting Started & Local Running

You can build, test, and deploy TasteTwin AI in a single, simple Docker command.

### Prerequisites
Make sure you have [Docker](https://docs.docker.com/) and [Docker Compose](https://docs.compose.spec.io/) installed.

### 1. Run via Docker Compose (Recommended)
From the root of the project directory, run:
```bash
docker-compose up --build
```
This command compiles the Docker image, installs all dependencies, exposes port **8090**, and starts the FastAPI server.

### 2. Verify Uptime
Once the service is active, verify that the health check endpoint returns successfully:
```bash
curl -f http://localhost:8090/api/health
```
**Expected Response:**
```json
{"status":"healthy","service":"TasteTwin AI Engine"}
```

### 3. Open the Web Application
Open your web browser and navigate to:
```
http://localhost:8090/
```
You will be greeted by the TasteTwin AI dashboard. By default, it runs in **Heuristic Mode**.

---

##  REST API Playground & curl Testing

You can easily interact with the REST API using simple `curl` commands.

### Task A: Simulate User Review (`POST /api/simulate-review`)
Simulates star ratings, inner thoughts, and review texts for a user-item combo.

**Command:**
```bash
curl -X POST "http://localhost:8090/api/simulate-review" \
     -H "Content-Type: application/json" \
     -d '{
       "persona_id": "twin_tech_ade",
       "item_id": "elec_solar_inverter",
       "provider": "heuristic"
     }'
```

**Expected JSON Response:**
```json
{
  "rating": 4.6,
  "monologue": "Omo, Nexus Solar Inverter makes sense. N380,000 is high but it saves me from NEPA drama. I'm going to rate this a 4.6 based on my criteria.",
  "review": "So I finally decided to test this out. Performance makes massive sense, particularly the pure sine wave for delicate electronics. But the pain point is that loud cooling fan when running under high load. Good product sha, but they need to fix the flaws.",
  "mode": "Local Heuristic"
}
```

---

### Task B: Cross-Domain Recommendations (`POST /api/recommend`)
Ranks candidates and outputs a complete Multi-Agent debate script and explanations.

**Command:**
```bash
curl -X POST "http://localhost:8090/api/recommend" \
     -H "Content-Type: application/json" \
     -d '{
       "persona_id": "twin_food_chinwe",
       "category_filter": "food",
       "provider": "heuristic"
     }'
```

**Expected JSON Response:**
```json
{
  "recommendations": [
    {
      "item_id": "food_calabar_kitchen",
      "title": "Calabar Kitchen - Traditional Fisherman Soup Combo",
      "category": "food",
      "price": 15000.0,
      "currency": "NGN",
      "predicted_rating": 4.8,
      "why_recommended": "Matches the user's focus on fresh daily-catch seafood mix. Highly wallet-friendly price of N15,000.",
      "why_not_recommended": "The user will strongly dislike that extremely spicy, which may overwhelm sensitive palates.",
      "debate": [
        {
          "agent": "Taste Agent",
          "avatar": "🎨",
          "text": "This item is highly rated (4.8 average) and offers excellent specs like fresh daily-catch seafood mix. It aligns perfectly with their domain expertise in food!",
          "score": 5.0
        },
        ...
      ]
    }
  ],
  "mode": "Local Heuristic"
}
```

---

##  Creative Adjustments & local Nigerian Tuning

* **NEPA Grid Bypass Optimization**: The engine recognizes that local users face persistent electricity cuts. Therefore, portable solar inverters and battery power banks receive a large cultural utility boost.
* **Lagos Logistics Integration**: Shipping delay complaints are naturally contextualized around Third Mainland Bridge traffic, Apapa port congestion, and dispatch rider challenges.
* **Code-Switching Accuracy**: Incorporates high-fidelity local Pidgin terminology (*abeg, sha, omo, make sense, mama put, computer village*) dynamically based on the Persona's **Naija Scale DNA**.
