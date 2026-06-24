import logging
from dataclasses import dataclass
from backend.evaluators.similarity_evaluator import SimilarityEvaluator
from backend.evaluators.llm_judge import LLMJudge
from backend.adapters.base_adapter import ModelResponse

logger = logging.getLogger(__name__)


@dataclass
class EvaluationResult:
    model_name: str
    question: str
    expected_answer: str
    generated_answer: str
    similarity_score: float
    llm_judge_score: float
    latency_seconds: float
    tokens_used: int
    cost_usd: float
    is_hallucination: bool
    success: bool
    error: str = ""


class ScoringEngine:

    def __init__(self):
        logger.info("Initializing Scoring Engine...")
        self.similarity_evaluator = SimilarityEvaluator()
        self.llm_judge = LLMJudge()
        logger.info("Scoring Engine ready.")

    def evaluate(
        self,
        model_response: ModelResponse,
        question: str,
        expected_answer: str,
    ) -> EvaluationResult:

        if not model_response.success or not model_response.generated_answer:
            return EvaluationResult(
                model_name=model_response.model_name,
                question=question,
                expected_answer=expected_answer,
                generated_answer="",
                similarity_score=0.0,
                llm_judge_score=0.0,
                latency_seconds=model_response.latency_seconds,
                tokens_used=model_response.tokens_used,
                cost_usd=model_response.cost_usd,
                is_hallucination=True,
                success=False,
                error=model_response.error or "Model failed to generate answer.",
            )

        similarity = self.similarity_evaluator.score(
            expected_answer,
            model_response.generated_answer
        )

        judge_score = self.llm_judge.score(
            question,
            expected_answer,
            model_response.generated_answer
        )

        hallucination = self.similarity_evaluator.is_hallucination(
            expected_answer,
            model_response.generated_answer
        )

        return EvaluationResult(
            model_name=model_response.model_name,
            question=question,
            expected_answer=expected_answer,
            generated_answer=model_response.generated_answer,
            similarity_score=similarity,
            llm_judge_score=judge_score,
            latency_seconds=model_response.latency_seconds,
            tokens_used=model_response.tokens_used,
            cost_usd=model_response.cost_usd,
            is_hallucination=hallucination,
            success=True,
        )

    def evaluate_batch(
        self,
        model_responses: list,
        questions: list,
        expected_answers: list,
    ) -> list:
        results = []
        for response, question, expected in zip(model_responses, questions, expected_answers):
            result = self.evaluate(response, question, expected)
            results.append(result)
        return results


def compute_model_summary(results: list) -> dict:
    """Compute aggregate metrics for a single model across all questions."""
    if not results:
        return {}

    successful = [r for r in results if r.success]
    total = len(results)

    if not successful:
        return {
            "model_name": results[0].model_name,
            "total_questions": total,
            "success_rate": 0.0,
            "avg_similarity_score": 0.0,
            "avg_llm_judge_score": 0.0,
            "avg_latency_seconds": 0.0,
            "total_cost_usd": 0.0,
            "total_tokens": 0,
            "hallucination_rate": 1.0,
        }

    return {
        "model_name": results[0].model_name,
        "total_questions": total,
        "success_rate": round(len(successful) / total, 4),
        "avg_similarity_score": round(sum(r.similarity_score for r in successful) / len(successful), 4),
        "avg_llm_judge_score": round(sum(r.llm_judge_score for r in successful) / len(successful), 4),
        "avg_latency_seconds": round(sum(r.latency_seconds for r in successful) / len(successful), 4),
        "total_cost_usd": round(sum(r.cost_usd for r in results), 8),
        "total_tokens": sum(r.tokens_used for r in results),
        "hallucination_rate": round(sum(1 for r in successful if r.is_hallucination) / len(successful), 4),
    }