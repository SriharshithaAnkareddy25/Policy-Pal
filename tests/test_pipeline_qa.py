import pytest

from ml.pipeline import pipeline_qa


def test_extract_json_payload_handles_fenced_json():
    parsed = pipeline_qa.extract_json_payload(
        '```json\n{"answers": ["Covered after 24 months."]}\n```'
    )

    assert parsed == {"answers": ["Covered after 24 months."]}


def test_answer_questions_reports_when_gemini_fails(monkeypatch):
    monkeypatch.setattr(
        pipeline_qa,
        "semantic_search",
        lambda *args, **kwargs: [{"text": "Grace period is thirty days."}],
    )
    monkeypatch.setattr(
        pipeline_qa,
        "call_gemini_llm",
        lambda prompt: (_ for _ in ()).throw(RuntimeError("model down")),
    )
    with pytest.raises(RuntimeError, match="Gemini could not generate an answer"):
        pipeline_qa.answer_questions("https://example.com/policy.pdf", ["Grace period?"])


def test_answer_questions_reports_answer_count_mismatch(monkeypatch):
    monkeypatch.setattr(pipeline_qa, "semantic_search", lambda *args, **kwargs: [])
    monkeypatch.setattr(pipeline_qa, "call_gemini_llm", lambda prompt: '{"answers": []}')
    with pytest.raises(RuntimeError, match="Gemini could not generate an answer"):
        pipeline_qa.answer_questions("https://example.com/policy.pdf", ["One?"])
