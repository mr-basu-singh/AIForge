AIForge — Production AI Evaluation & Agent Testing Platform

"LangSmith + OpenAI Evals + Promptfoo — built from scratch."

AIForge is a full-stack platform that automatically benchmarks multiple AI models on your custom datasets and tells you which model is the best, cheapest, and most reliable — in minutes.

The Problem
Every company building AI products asks:

Which model should we use — Llama, Gemma, GPT, or Claude?
Did our prompt change actually improve results?
Is our model hallucinating?
Which model gives the best quality per dollar?

Most companies solve this manually. AIForge automates it.

What AIForge Does

You upload a CSV with questions and expected answers
AIForge sends every question to multiple AI models simultaneously
Every answer is automatically scored using two methods
Hallucinations are detected automatically
AIForge picks the best model based on combined scores
A professional PDF report is generated with full analysis


Features
FeatureDescription🤖 Multi-Model BenchmarkingTest Llama 3.3, Llama 3.1, Gemma, Qwen simultaneously📊 Dual Evaluation EngineSentence Transformer similarity + LLM-as-a-Judge scoring🧠 Hallucination DetectionAutomatically flags answers below similarity threshold🧪 Experiment TrackingEvery run saved with full history and metrics📝 Prompt VersioningCompare outputs across different prompt versions📄 PDF Report GeneratorExecutive-ready reports with model rankings and cost analysis📁 Dataset ManagerUpload custom CSV datasets with preview🐳 Docker SupportOne-command deployment with Docker Compose🔌 REST API15 endpoints with Swagger documentation✅ Test Suite12 unit tests across all core components

Architecture
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

🛠️ Tech Stack
LayerTechnologyBackendPython, FastAPI, UvicornFrontendStreamlitLLM LayerGroq APIAI ModelsLlama 3.3 70b, Llama 3.1 8b, Gemma 2 9b, Qwen QwQ 32bEvaluationSentence Transformers, Scikit-learnDatabaseSQLite, SQLAlchemyReportsReportLabContainerizationDocker, Docker Compose

Folder Structure
AIForge/
├── frontend/
│   ├── app.py
│   └── requirements.txt
├── backend/
│   ├── api/
│   │   ├── main.py
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── adapters/
│   │   ├── base_adapter.py
│   │   └── groq_adapter.py
│   ├── evaluators/
│   │   ├── similarity_evaluator.py
│   │   ├── llm_judge.py
│   │   └── scoring_engine.py
│   ├── experiments/
│   │   ├── experiment_tracker.py
│   │   └── prompt_versioning.py
│   ├── reports/
│   │   └── pdf_generator.py
│   ├── database/
│   │   ├── db.py
│   │   └── models.py
│   └── config.py
├── datasets/
│   └── sample.csv
├── tests/
│   ├── test_adapters.py
│   ├── test_evaluators.py
│   └── test_database.py
├── docker/
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
├── docker-compose.yml
├── requirements.txt
└── README.md

Quick Start
Option 1 — Local Development
1. Clone the repository
bashgit clone https://github.com/mr-basu-singh/AIForge.git
cd AIForge
2. Create virtual environment
bashpython -m venv venv
venv\Scripts\activate
3. Install dependencies
bashpip install -r requirements.txt
4. Add your Groq API key to .env
envGROQ_API_KEY=your_groq_api_key_here
Get your free Groq API key at: https://console.groq.com
5. Start backend (Terminal 1)
bashuvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
6. Start frontend (Terminal 2)
bashstreamlit run frontend/app.py
7. Open browser

Frontend: http://localhost:8501
Backend API: http://localhost:8000
API Docs: http://localhost:8000/docs


Option 2 — Docker
bashdocker-compose up --build

How To Use
Step 1 — Upload Dataset
Go to Dataset Manager and upload a CSV:
question,expected_answer
What is RAG?,Retrieval Augmented Generation...
What is LangChain?,LangChain is a framework...
Step 2 — Run Experiment
Go to Run Experiment → select models → click Run Experiment
Step 3 — View Results
Go to Results & Metrics → see comparison table, charts, best model
Step 4 — Download Report
Go to Reports → Generate PDF → download executive report

Real Benchmark Results
ModelSimilarityJudge ScoreLatencyCostHallucinationllama-3.3-70b-versatile0.6957.4/100.455s$0.00096610%llama-3.1-8b-instant0.6367.0/100.474s$0.00021820%

API Endpoints
MethodEndpointDescriptionGET/api/v1/healthHealth checkGET/api/v1/modelsList available modelsGET/api/v1/promptsList prompt versionsPOST/api/v1/promptsCreate prompt versionDELETE/api/v1/prompts/{version}Delete prompt versionPOST/api/v1/datasets/uploadUpload CSV datasetGET/api/v1/datasetsList datasetsPOST/api/v1/experiments/runRun experimentGET/api/v1/experimentsList all experimentsGET/api/v1/experiments/{id}Get experiment detailsGET/api/v1/experiments/{id}/metricsGet model metricsGET/api/v1/experiments/{id}/resultsGet detailed resultsGET/api/v1/experiments/{id}/best-modelGet best modelGET/api/v1/experiments/{id}/reportDownload PDF report

Running Tests
bashpython tests/test_database.py
python tests/test_evaluators.py
python tests/test_adapters.py

Roadmap

 Multi-provider support (OpenAI, Anthropic, Google Gemini)
 User authentication and API key management
 Async experiment execution for faster results
 Agent testing harness for LangGraph agents
 PostgreSQL support for production deployments
 Real-time progress with WebSockets


Author
Basu Singh

GitHub: @mr-basu-singh

Support
If this project helped you — give it a ⭐ on GitHub!
