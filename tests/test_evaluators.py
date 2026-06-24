import sys
sys.path.insert(0, '.')

def test_similarity_score_high():
    from backend.evaluators.similarity_evaluator import SimilarityEvaluator
    ev = SimilarityEvaluator()
    score = ev.score("Retrieval Augmented Generation", "Retrieval Augmented Generation combines retrieval with generation.")
    assert score > 0.7
    print(f"✅ test_similarity_score_high passed — score: {score}")

def test_similarity_score_low():
    from backend.evaluators.similarity_evaluator import SimilarityEvaluator
    ev = SimilarityEvaluator()
    score = ev.score("Retrieval Augmented Generation", "I like pizza and pasta.")
    assert score < 0.5
    print(f"✅ test_similarity_score_low passed — score: {score}")

def test_hallucination_detection():
    from backend.evaluators.similarity_evaluator import SimilarityEvaluator
    ev = SimilarityEvaluator()
    assert ev.is_hallucination("Retrieval Augmented Generation", "I like pizza.") == True
    assert ev.is_hallucination("Retrieval Augmented Generation", "RAG combines retrieval with generation.") == False
    print("✅ test_hallucination_detection passed")

def test_llm_judge_score():
    from backend.evaluators.llm_judge import LLMJudge
    judge = LLMJudge()
    score = judge.score("What is RAG?", "Retrieval Augmented Generation", "RAG is Retrieval Augmented Generation.")
    assert 0.0 <= score <= 10.0
    print(f"✅ test_llm_judge_score passed — score: {score}")

def test_scoring_engine():
    from backend.evaluators.scoring_engine import ScoringEngine
    from backend.adapters.base_adapter import ModelResponse
    engine = ScoringEngine()
    response = ModelResponse(
        model_name="llama-3.1-8b-instant",
        generated_answer="Retrieval Augmented Generation combines retrieval with generation.",
        latency_seconds=0.9,
        tokens_used=50,
        cost_usd=0.001,
        success=True
    )
    result = engine.evaluate(response, "What is RAG?", "Retrieval Augmented Generation")
    assert result.similarity_score > 0.0
    assert result.llm_judge_score >= 0.0
    assert result.success == True
    print(f"✅ test_scoring_engine passed — similarity: {result.similarity_score}, judge: {result.llm_judge_score}")

if __name__ == "__main__":
    test_similarity_score_high()
    test_similarity_score_low()
    test_hallucination_detection()
    test_llm_judge_score()
    test_scoring_engine()
    print("\n✅ All evaluator tests passed.")