import hashlib
import json
import logging
import re
from typing import Any, List

from backend.services.retrieval import semantic_search
from ml.model.gemini_client import call_gemini_llm
from ml.pipeline.prompt_builder import build_llm_prompt

logger = logging.getLogger(__name__)


def _response_text(raw_response: Any) -> str:
    if isinstance(raw_response, dict):
        return (
            raw_response.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
        )
    return str(raw_response or "")


def extract_json_payload(raw_response: Any) -> dict:
    text = _response_text(raw_response).strip()
    if not text:
        raise ValueError("LLM response was empty")

    fenced_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    if fenced_match:
        text = fenced_match.group(1)
    elif not text.startswith("{"):
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("No JSON object found in LLM response")
        text = text[start : end + 1]

    parsed = json.loads(text)
    if not isinstance(parsed, dict):
        raise ValueError("LLM JSON response must be an object")
    return parsed


def answer_questions(
    document_url: str,
    questions: List[str],
    top_k: int = 8,
) -> List[str]:
    source_id = hashlib.md5(document_url.encode("utf-8")).hexdigest()

    combined_query = " ".join(questions)
    context_chunks = semantic_search(
        combined_query,
        top_k=top_k,
        namespace=source_id,
        fltr={"source": {"$eq": source_id}},
    )

    prompt = build_llm_prompt(context_chunks, questions)

    try:
        raw_response = call_gemini_llm(prompt)
        parsed = extract_json_payload(raw_response)
        answers = parsed.get("answers")
        if not isinstance(answers, list):
            raise ValueError("LLM response is missing an answers list")
        if len(answers) != len(questions):
            raise ValueError(
                f"LLM returned {len(answers)} answer(s) for {len(questions)} question(s)"
            )
        return [str(answer).strip() for answer in answers]
    except Exception as exc:
        logger.exception("Gemini answer generation failed")
        raise RuntimeError(
            "Gemini could not generate an answer. Check GEMINI_API_KEY and "
            "GEMINI_MODEL, then retry."
        ) from exc
