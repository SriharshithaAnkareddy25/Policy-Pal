from ml.pipeline.prompt_builder import build_llm_prompt


def test_build_llm_prompt_contains_questions_context_and_json_instruction():
    prompt = build_llm_prompt(
        [{"text": "Cataract surgery has a two year waiting period."}],
        ["What is the waiting period for cataract surgery?"],
    )

    assert "1. What is the waiting period for cataract surgery?" in prompt
    assert "Cataract surgery has a two year waiting period." in prompt
    assert '"answers"' in prompt
    assert "Return valid JSON only" in prompt
