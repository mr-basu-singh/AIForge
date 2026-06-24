import sys
sys.path.insert(0, '.')

def test_groq_adapter_success():
    from backend.adapters.groq_adapter import ModelRouter
    router = ModelRouter()
    result = router.run("You are a helpful assistant.", "What is RAG?", "llama-3.1-8b-instant")
    assert result.success == True
    assert len(result.generated_answer) > 0
    assert result.latency_seconds > 0
    assert result.tokens_used > 0
    print("✅ test_groq_adapter_success passed")

def test_groq_adapter_all_models():
    from backend.adapters.groq_adapter import ModelRouter
    router = ModelRouter()
    models = router.get_available_models()
    assert len(models) == 4
    print(f"✅ test_groq_adapter_all_models passed — {len(models)} models found")

def test_model_response_fields():
    from backend.adapters.groq_adapter import ModelRouter
    router = ModelRouter()
    result = router.run("You are helpful.", "What is AI?", "llama-3.1-8b-instant")
    assert hasattr(result, "model_name")
    assert hasattr(result, "generated_answer")
    assert hasattr(result, "latency_seconds")
    assert hasattr(result, "tokens_used")
    assert hasattr(result, "cost_usd")
    assert hasattr(result, "success")
    print("✅ test_model_response_fields passed")

if __name__ == "__main__":
    test_groq_adapter_success()
    test_groq_adapter_all_models()
    test_model_response_fields()
    print("\n✅ All adapter tests passed.")