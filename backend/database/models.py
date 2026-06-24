from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    dataset_name = Column(String(255), nullable=False)
    models_used = Column(JSON, nullable=False)
    prompt_version = Column(String(50), default="v1")
    status = Column(String(50), default="pending")  # pending, running, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


class ExperimentResult(Base):
    __tablename__ = "experiment_results"

    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, nullable=False)
    model_name = Column(String(255), nullable=False)
    question = Column(Text, nullable=False)
    expected_answer = Column(Text, nullable=False)
    generated_answer = Column(Text, nullable=False)
    similarity_score = Column(Float, default=0.0)
    llm_judge_score = Column(Float, default=0.0)
    latency_seconds = Column(Float, default=0.0)
    tokens_used = Column(Integer, default=0)
    cost_usd = Column(Float, default=0.0)
    is_hallucination = Column(Integer, default=0)  # 0 = No, 1 = Yes
    created_at = Column(DateTime, default=datetime.utcnow)


class PromptVersion(Base):
    __tablename__ = "prompt_versions"

    id = Column(Integer, primary_key=True, index=True)
    version = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ModelMetrics(Base):
    __tablename__ = "model_metrics"

    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, nullable=False)
    model_name = Column(String(255), nullable=False)
    avg_similarity_score = Column(Float, default=0.0)
    avg_llm_judge_score = Column(Float, default=0.0)
    avg_latency_seconds = Column(Float, default=0.0)
    total_cost_usd = Column(Float, default=0.0)
    total_tokens = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    hallucination_rate = Column(Float, default=0.0)
    total_questions = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)