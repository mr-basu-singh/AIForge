```markdown
# ⚡ AIForge — Production AI Evaluation & Agent Testing Platform

> **"LangSmith + OpenAI Evals + Promptfoo — built from scratch."**

AIForge is a full-stack platform that automatically benchmarks multiple AI models on your custom datasets and tells you which model is the best, cheapest, and most reliable — in minutes.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35.0-red)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

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

1. You upload a CSV with questions and expected answers
2. AIForge sends every question to multiple AI models simultaneously
3. Every answer is automatically scored using two methods
4. Hallucinations are detected automatically
5. AIForge picks the best model based on combined scores
6. A professional PDF report is generated with full analysis

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 Multi-Model Benchmarking | Test Llama 3.3, Llama 3.1, Gemma, Qwen simultaneously |
| 📊 Dual Evaluation Engine | Sentence Transformer similarity + LLM-as-a-Judge scoring |
| 🧠 Hallucination Detection | Automatically flags answers below similarity threshold |
| 🧪 Experiment Tracking | Every run saved with full history and metrics |
| 📝 Prompt Versioning | Compare outputs across different prompt versions |
| 📄 PDF Report Generator | Executive-ready reports with model rankings and cost analysis |
| 📁 Dataset Manager | Upload custom CSV datasets with preview |
| 🐳 Docker Support | One-command deployment with Docker Compose |
| 🔌 REST API | 15 endpoints with Swagger documentation |
| ✅ Test Suite | 12 unit tests across all core components |

---

## 🏗️ Architecture

```
Engineer
    ↓
Streamlit Frontend (6 pages)
    ↓
FastAPI Backend (15 REST endpoints)
    ↓
Experiment Engine
    ↓
Model Router
    ↓
Multiple AI Models (Groq API)
    ↓
Scoring Engine
    ├── Sentence Transformer Similarity
    ├── LLM Judge (0-10 score)
    └── Hallucination Detector
    ↓
SQLite Database
    ↓
PDF Report Generator
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI, Uvicorn |
| Frontend | Streamlit |
| LLM Layer | Groq API |
| AI Models | Llama 3.3 70b, Llama 3.1 8b, Gemma 2 9b, Qwen QwQ 32b |
| Evaluation | Sentence Transformers, Scikit-learn |
| Database | SQLite, SQLAlchemy |
| Reports | ReportLab |
| Containerization | Docker, Docker Compose |

---

## 📁 Folder Structure

```
AIForge/
├── frontend/
│   ├── app.py                  # Streamlit UI (6 pages)
│   └── requirements.txt
├── backend/
│   ├── api/
│   │   ├── main.py             # FastAPI app entry point
│   │   ├── routes.py           # All 15 API endpoints
│   │   └── schemas.py          # Pydantic request/response models
│   ├── adapters/
│   │   ├── base_adapter.py     # Abstract base class
│   │   └── groq_adapter.py     # Groq API integration + Model Router
│   ├── evaluators/
│   │   ├── similarity_evaluator.py  # Sentence Transformer scoring
│   │   ├── llm_judge.py             # LLM-as-a-Judge scoring
│   │   └── scoring_engine.py        # Combined evaluation pipeline
│   ├── experiments/
│   │   ├── experiment_tracker.py    # Full experiment pipeline
│   │   └── prompt_versioning.py     # Prompt version management
│   ├── reports/
│   │   └── pdf_generator.py    # PDF report generation
│   ├── database/
│   │   ├── db.py               # Database connection + session
│   │   └── models.py           # SQLAlchemy table models
│   └── config.py               # Centralized settings
├── datasets/
│   └── sample.csv              # Sample dataset
├── tests/
│   ├── test_adapters.py        # Groq adapter tests
│   ├── test_evaluators.py      # Evaluation engine tests
│   └── test_database.py        # Database + experiment tests
├── docker/
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚡ Quick Start

### Option 1 — Local Development

**1. Clone the repository**
```bash
git clone https://github.com/mr-basu-singh/AIForge.git
cd AIForge
```

**2. Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Setup environment variables**
```bash
cp .env.example .env
```
Open `.env` and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key at: https://console.groq.com

**5. Start backend (Terminal 1)**
```bash
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
```

**6. Start frontend (Terminal 2)**
```bash
streamlit run frontend/app.py
```

**7. Open browser**
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

### Option 2 — Docker (One Command)

```bash
git clone https://github.com/mr-basu-singh/AIForge.git
cd AIForge

# Add your Groq API key to .env
echo "GROQ_API_KEY=your_key_here" > .env

# Run everything
docker-compose up --build
```

- Frontend: http://localhost:8501
- Backend: http://localhost:8000

---

## 📊 How To Use

### Step 1 — Upload Dataset
Go to **Dataset Manager** → upload a CSV file with this format:

```csv
question,expected_answer
What is RAG?,Retrieval Augmented Generation is a technique...
What is LangChain?,LangChain is a framework for building LLM applications...
What is a vector database?,A vector database stores high-dimensional embeddings...
```

### Step 2 — Run Experiment
Go to **Run Experiment** → select:
- Experiment name
- Dataset
- Models to compare
- Prompt version

Click **🚀 Run Experiment**

### Step 3 — View Results
Go to **Results & Metrics** → see:
- Model comparison table
- Bar charts by metric
- Detailed per-question results
- Best model recommendation

### Step 4 — Download Report
Go to **Reports** → click **Generate PDF** → download executive report

---

## 📈 Real Benchmark Results

From an actual AIForge experiment comparing Llama 3.3 vs Llama 3.1:

| Model | Similarity | Judge Score | Latency | Cost | Hallucination |
|---|---|---|---|---|---|
| llama-3.3-70b-versatile | 0.695 | 7.4/10 | 0.455s | $0.000966 | 10% |
| llama-3.1-8b-instant | 0.636 | 7.0/10 | 0.474s | $0.000218 | 20% |

**Conclusion:** Llama 3.3 gives better quality with lower hallucination. Llama 3.1 is 4.5x cheaper for budget-sensitive use cases.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/models` | List available models |
| GET | `/api/v1/prompts` | List prompt versions |
| POST | `/api/v1/prompts` | Create prompt version |
| DELETE | `/api/v1/prompts/{version}` | Delete prompt version |
| POST | `/api/v1/datasets/upload` | Upload CSV dataset |
| GET | `/api/v1/datasets` | List datasets |
| POST | `/api/v1/experiments/run` | Run experiment |
| GET | `/api/v1/experiments` | List all experiments |
| GET | `/api/v1/experiments/{id}` | Get experiment details |
| GET | `/api/v1/experiments/{id}/metrics` | Get model metrics |
| GET | `/api/v1/experiments/{id}/results` | Get detailed results |
| GET | `/api/v1/experiments/{id}/best-model` | Get best model |
| GET | `/api/v1/experiments/{id}/report` | Download PDF report |

Full interactive docs at: `http://localhost:8000/docs`

---

## 🧪 Running Tests

```bash
# Database tests
python tests/test_database.py

# Evaluator tests
python tests/test_evaluators.py

# Adapter tests
python tests/test_adapters.py
```

Expected output:
```
✅ test_db_init passed
✅ test_prompt_versioning passed
✅ test_create_delete_prompt passed
✅ test_experiment_tracker_init passed
✅ All database tests passed.

✅ test_similarity_score_high passed — score: 0.9403
✅ test_similarity_score_low passed — score: 0.0936
✅ test_hallucination_detection passed
✅ test_llm_judge_score passed — score: 10.0
✅ test_scoring_engine passed
✅ All evaluator tests passed.

✅ test_groq_adapter_success passed
✅ test_groq_adapter_all_models passed — 4 models found
✅ test_model_response_fields passed
✅ All adapter tests passed.
```

---

## 🗺️ Roadmap

- [ ] Multi-provider support (OpenAI, Anthropic, Google Gemini)
- [ ] User authentication and API key management
- [ ] Async experiment execution for faster results
- [ ] Agent testing harness for LangGraph agents
- [ ] PostgreSQL support for production deployments
- [ ] Rate limiting and request queuing
- [ ] Real-time experiment progress with WebSockets
- [ ] Custom scoring metrics

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/MultiProviderSupport`)
3. Commit your changes (`git commit -m 'Add OpenAI adapter'`)
4. Push to the branch (`git push origin feature/MultiProviderSupport`)
5. Open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Basu Singh**
- GitHub: [@mr-basu-singh](https://github.com/mr-basu-singh)

---

## ⭐ Support

If this project helped you — give it a ⭐ on GitHub!
