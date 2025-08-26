# 🫁 🌿 BreathWell AI - Asthma Assistant 🌷

**BreathWell AI** is an **AI-powered asthma assistant** built with **LangChain, Azure OpenAI, FAISS, and Gradio**.
It provides **real-time, personalized recommendations** for asthma patients by combining:

* ✅ **Current environmental factors** (location, AQI, pollutants)
* ✅ **Patient history & symptoms** (stored in vector embeddings)
* ✅ **Reliable, fact-checked medical insights**

This project secured **🥇 1st Place** at **AI-Gati Hackathon, RSG Pune Conference 2025** 🚀🔥.

---

## 🚀 Features

* 🌍 **Location & AQI Detection** via Google Maps + Air Quality API
* 🩺 **Personalized Health Recommendations** based on AQI category
* 📚 **RAG (Retrieval-Augmented Generation)** using FAISS + Azure embeddings
* 🤖 **Conversational AI Agent** powered by LangChain & GPT-4o
* 🎨 **Interactive UI** with Gradio (custom-styled for a smooth UX)

---

## 🛠️ Tech Stack

* **Python** (dependency management via [Poetry](https://python-poetry.org/))
* **LangChain** (agents, tools, orchestration)
* **Azure OpenAI** (`gpt-4o`, `text-embedding-ada-002`)
* **FAISS** (vector store for patient history)
* **Google Maps API + Air Quality API**
* **Gradio** (demo interface)

---

## 📂 Project Structure

```bash
AI_GATI_Med/
├── app.py               # Core LangChain agent, tools, AQI fetch, recommendations
├── ui.py                # Gradio UI demo
├── create_embeddings.py # Script to generate embeddings
├── load_embeddings.py   # Script to load embeddings
├── pdf_faiss_index/     # FAISS index with stored embeddings
├── pyproject.toml       # Poetry dependencies
├── poetry.lock          # Poetry lock file
├── .env                 # Environment variables
└── README.md            # Project documentation
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Aqsaafk/AI_GATI_Med.git
cd AI_GATI_Med
```

### 2. Install Dependencies

```bash
poetry install
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory with:

```bash
ENDPOINT_URL="https://your-azure-openai-endpoint"
DEPLOYMENT_NAME="gpt-4o"
AZURE_OPENAI_API_KEY="your-azure-openai-key"
GOOGLE_API_KEY="your-google-api-key"
```

---

## ▶️ Running the Project

Run in **two terminals**:

### Terminal 1: Backend Agent

```bash
poetry run python app.py
```

### Terminal 2: Gradio Demo

```bash
poetry run python ui.py
```

Gradio will launch a local web interface (and optionally a shareable public link).

---

## 💡 Example Queries

* “What’s the AQI in Pune today?”
* “Give me asthma recommendations if air quality is poor.”
* “Show me my patient history from the database.”

---

## ✨ Future Scope

* 🩸 Doctor-verified health data → **Trustworthy AI**
* 🔗 **IoT integration** (pulse ox, heart monitors, step trackers)
* 📊 Expand to **other lifestyle diseases** (diabetes, hypertension, obesity)
* 🔐 **HIPAA-compliant security & privacy**

---

## 🏆 Achievements

🥇 **1st Place Winner - AI-Gati Hackathon (RSG Pune 2025)**
Organized by **APGI - Agile Practitioners Group of India** & **Scrum Alliance**.

---

## 📜 License

MIT License

