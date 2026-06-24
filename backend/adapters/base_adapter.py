from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class ModelResponse:
    model_name: str
    generated_answer: str
    latency_seconds: float
    tokens_used: int
    cost_usd: float
    success: bool
    error: Optional[str] = None


class BaseAdapter(ABC):

    @abstractmethod
    def generate(self, prompt: str, question: str, model_name: str) -> ModelResponse:
        pass

    @abstractmethod
    def get_available_models(self) -> list:
        pass