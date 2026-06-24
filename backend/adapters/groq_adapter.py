import time
import logging
from groq import Groq
from backend.adapters.base_adapter import BaseAdapter, ModelResponse
from backend.config import settings

logger = logging.getLogger(__name__)

# Cost per 1000 tokens in USD
MODEL_COSTS = {
    "llama-3.3-70b-versatile": {"input": 0.00059, "output": 0.00079},
    "llama-3.1-8b-instant":    {"input": 0.00005, "output": 0.00008},
    "gemma2-9b-it":            {"input": 0.00020, "output": 0.00020},
    "qwen-qwq-32b":            {"input": 0.00029, "output": 0.00039},
}

class GroqAdapter(BaseAdapter):

    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is missing in .env file.")
        self.client = Groq(api_key=settings.GROQ_API_KEY)

    def generate(self, prompt: str, question: str, model_name: str) -> ModelResponse:
        try:
            messages = []

            if prompt and prompt.strip():
                messages.append({"role": "system", "content": prompt.strip()})

            messages.append({"role": "user", "content": question.strip()})

            start_time = time.time()

            response = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                max_tokens=512,
                temperature=0.1,
            )

            latency = round(time.time() - start_time, 3)

            generated_answer = response.choices[0].message.content.strip()
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens

            cost = self._calculate_cost(model_name, input_tokens, output_tokens)

            return ModelResponse(
                model_name=model_name,
                generated_answer=generated_answer,
                latency_seconds=latency,
                tokens_used=total_tokens,
                cost_usd=cost,
                success=True,
            )

        except Exception as e:
            logger.error(f"Groq generation failed for model {model_name}: {e}")
            return ModelResponse(
                model_name=model_name,
                generated_answer="",
                latency_seconds=0.0,
                tokens_used=0,
                cost_usd=0.0,
                success=False,
                error=str(e),
            )

    def _calculate_cost(self, model_name: str, input_tokens: int, output_tokens: int) -> float:
        if model_name not in MODEL_COSTS:
            return 0.0
        rates = MODEL_COSTS[model_name]
        input_cost  = (input_tokens  / 1000) * rates["input"]
        output_cost = (output_tokens / 1000) * rates["output"]
        return round(input_cost + output_cost, 8)

    def get_available_models(self) -> list:
        return settings.AVAILABLE_MODELS


class ModelRouter:
    """Routes requests to the correct adapter."""

    def __init__(self):
        self.adapter = GroqAdapter()

    def run(self, prompt: str, question: str, model_name: str) -> ModelResponse:
        return self.adapter.generate(prompt, question, model_name)

    def run_all_models(self, prompt: str, question: str, models: list) -> list:
        results = []
        for model in models:
            logger.info(f"Running model: {model}")
            result = self.adapter.generate(prompt, question, model)
            results.append(result)
        return results

    def get_available_models(self) -> list:
        return self.adapter.get_available_models()