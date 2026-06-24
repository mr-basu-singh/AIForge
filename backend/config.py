import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # App
    APP_NAME: str = os.getenv("APP_NAME", "AIForge")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"

    # Groq
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./aiforge.db")
    DATASETS_DIR: str = os.getenv("DATASETS_DIR", "datasets")

    # Server
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", 8000))

    # Evaluation
    SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", 0.7))
    LLM_JUDGE_MODEL: str = os.getenv("LLM_JUDGE_MODEL", "llama-3.3-70b-versatile")

    # Available Models
    AVAILABLE_MODELS: list = os.getenv(
        "AVAILABLE_MODELS",
        "llama-3.3-70b-versatile,llama-3.1-8b-instant,gemma2-9b-it,qwen-qwq-32b"
    ).split(",")

    # Security
    MAX_DATASET_ROWS: int = 500
    MAX_PROMPT_LENGTH: int = 4000
    REQUEST_TIMEOUT: int = 30

settings = Settings()