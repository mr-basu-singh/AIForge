from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class RunExperimentRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    dataset_path: str = Field(..., min_length=1)
    selected_models: List[str] = Field(..., min_items=1)
    prompt_version: str = Field(default="v1")


class CreatePromptRequest(BaseModel):
    version: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=10, max_length=4000)
    description: Optional[str] = ""


class ExperimentResponse(BaseModel):
    id: int
    name: str
    dataset_name: str
    models_used: List[str]
    prompt_version: str
    status: str
    created_at: str
    completed_at: Optional[str]


class MetricsResponse(BaseModel):
    model_name: str
    avg_similarity_score: float
    avg_llm_judge_score: float
    avg_latency_seconds: float
    total_cost_usd: float
    total_tokens: int
    success_rate: float
    hallucination_rate: float
    total_questions: int


class HealthResponse(BaseModel):
    status: str
    app: str
    version: str