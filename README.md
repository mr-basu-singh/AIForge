# ⚡ AIForge — Production AI Evaluation & Agent Testing Platform

**"LangSmith + OpenAI Evals + Promptfoo — built from scratch."**

AIForge automatically benchmarks multiple AI models on your custom datasets and tells you which model is best, cheapest, and most reliable — in minutes.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-green) ![Streamlit](https://img.shields.io/badge/Streamlit-1.35.0-red) ![Docker](https://img.shields.io/badge/Docker-Containerized-blue)

---

## 🎯 The Problem

Every company building AI products asks:

- Which model should we use — Llama, Gemma, GPT, or Claude?
- Did our prompt change actually improve results?
- Is our model hallucinating?
- Which model gives the best quality per dollar?

Most companies solve this **manually**. AIForge **automates it**.

---

## 🚀 What AIForge Does

1. Upload a CSV with questions and expected answers
2. AIForge sends every question to multiple AI models simultaneously
3. Every answer is automatically scored using two methods
4. Hallucinations are detected automatically
5. AIForge picks the best model based on combined scores
6. A professional PDF report is generated with full analysis

---

## ✨ Features

- 🤖 **Multi-Model Benchmarking** — Test Llama 3.3, Llama 3.1, Gemma, Qwen simultaneously
- 📊 **Dual Evaluation Engine** — Sentence Transformer similarity + LLM-as-a-Judge scoring
- 🧠 **Hallucination Detection** — Automatically flags answers below similarity threshold
- 🧪 **Experiment Tracking** — Every run saved with full history and metrics
- 📝 **Prompt Versioning** — Compare outputs across different prompt versions
- 📄 **PDF Report Generator** — Executive-ready reports with model rankings and cost analysis
- 📁 **Dataset Manager** — Upload custom CSV datasets with preview
- 🐳 **Docker Support** — One-command deployment with Docker Compose
- 🔌 **REST API** — 15 endpoints with Swagger documentation
- ✅ **Test Suite** — 12 unit tests across all core components

---

## 🛠️ Tech Stack

- **Backend** — Python, FastAPI, Uvicorn
- **Frontend** — Streamlit
- **LLM Layer** — Groq API
- **AI Models** — Llama 3.3 70b, Llama 3.1 8b, Gemma 2 9b, Qwen QwQ 32b
- **Evaluation** — Sentence Transformers, Scikit-learn
- **Database** — SQLite, SQLAlchemy
- **Reports** — ReportLab
- **Containerization** — Docker, Docker Compose

---

## ⚡ Quick Start

**1. Clone the repository**

```bash
git clone https://github.com/mr-basu-singh/AIForge.git
cd AIForge
```

**2. Create virtual environment**

```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Add your Groq API key to .env**

```bash
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key at https://console.groq.com

**5. Start backend in Terminal 1**

```bash
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
```

**6. Start frontend in Terminal 2**

```bash
streamlit run frontend/app.py
```

**7. Open browser**

- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🐳 Docker

Run everything with one command:

```bash
docker-compose up --build
```

- Frontend: http://localhost:8501
- Backend: http://localhost:8000

---

## 📊 How To Use

**Step 1 — Upload Dataset**

Go to Dataset Manager and upload a CSV file:

```csv
question,expected_answer
What is RAG?,Retrieval Augmented Generation...
What is LangChain?,LangChain is a framework...
```

**Step 2 — Run Experiment**

Go to Run Experiment, select your models, click Run Experiment

**Step 3 — View Results**

Go to Results and Metrics to see comparison table, charts, and best model

**Step 4 — Download Report**

Go to Reports, click Generate PDF, download your executive report

---

## 📈 Real Benchmark Results

From an actual AIForge experiment:

- **llama-3.3-70b** — Similarity: 0.695 | Judge: 7.4/10 | Latency: 0.455s | Cost: $0.000966 | Hallucination: 10%
- **llama-3.1-8b** — Similarity: 0.636 | Judge: 7.0/10 | Latency: 0.474s | Cost: $0.000218 | Hallucination: 20%

**Winner:** Llama 3.3 gives better quality. Llama 3.1 is 4.5x cheaper.

---

## 🔌 API Endpoints

- GET `/api/v1/health` — Health check
- GET `/api/v1/models` — List available models
- GET `/api/v1/prompts` — List prompt versions
- POST `/api/v1/prompts` — Create prompt version
- DELETE `/api/v1/prompts/{version}` — Delete prompt version
- POST `/api/v1/datasets/upload` — Upload CSV dataset
- GET `/api/v1/datasets` — List datasets
- POST `/api/v1/experiments/run` — Run experiment
- GET `/api/v1/experiments` — List all experiments
- GET `/api/v1/experiments/{id}` — Get experiment details
- GET `/api/v1/experiments/{id}/metrics` — Get model metrics
- GET `/api/v1/experiments/{id}/results` — Get detailed results
- GET `/api/v1/experiments/{id}/best-model` — Get best model
- GET `/api/v1/experiments/{id}/report` — Download PDF report

Full interactive docs at http://localhost:8000/docs

---

## 🧪 Running Tests

```bash
python tests/test_database.py
python tests/test_evaluators.py
python tests/test_adapters.py
```

---

## 🗺️ Future Work

- Multi-provider support (OpenAI, Anthropic, Google Gemini)
- User authentication and API key management
- Async experiment execution for faster results
- Agent testing harness for LangGraph agents
- PostgreSQL support for production deployments
- Real-time progress with WebSockets

---

## 👨‍💻 Author

**Basu Singh**

GitHub: https://github.com/mr-basu-singh

---

## ⭐ Support

If this project helped you — give it a ⭐ on GitHub!
