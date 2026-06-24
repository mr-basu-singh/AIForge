# ⚡ AIForge — AI Evaluation Platform

> LangSmith + OpenAI Evals + Promptfoo built from scratch.

## Quick Start

### Option 1 — Local Development

```bash
# 1. Clone and setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 2. Add your Groq API key to .env
GROQ_API_KEY=your_key_here

# 3. Start backend (Terminal 1)
uvicorn backend.api.main:app --reload --port 8000

# 4. Start frontend (Terminal 2)
streamlit run frontend/app.py
```

### Option 2 — Docker

```bash
docker-compose up --build
```

## Access

- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Features

- Multi-model benchmarking (Llama, Gemma, Qwen)
- Similarity scoring with sentence transformers
- LLM Judge evaluation (0-10 scoring)
- Hallucination detection
- Experiment tracking with history
- Prompt versioning
- PDF report generation
- Docker containerization

## Tech Stack

- FastAPI + Uvicorn
- Streamlit
- Groq API
- Sentence Transformers
- SQLite + SQLAlchemy
- ReportLab
- Docker