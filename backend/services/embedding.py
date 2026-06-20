import hashlib
import logging
import os
import time
from typing import List

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")
EMBED_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:embedContent"
TASK_TYPE = os.getenv("GEMINI_EMBEDDING_TASK_TYPE", "SEMANTIC_SIMILARITY")
OUTPUT_DIMENSIONALITY = os.getenv("GEMINI_EMBEDDING_DIMENSION")

_embedding_cache: dict[str, List[float]] = {}


def _embedding_config() -> dict:
    config = {"taskType": TASK_TYPE}
    if OUTPUT_DIMENSIONALITY:
        config["outputDimensionality"] = int(OUTPUT_DIMENSIONALITY)
    return config


def _call_gemini_embedding_api(
    text: str,
    max_retries: int = 3,
    delay_base: float = 1.0,
) -> List[float]:
    api_key = os.getenv("GEMINI_EMBD_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GEMINI_EMBD_KEY or GEMINI_API_KEY in environment")

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key,
    }
    payload = {
        "model": f"models/{MODEL}",
        "taskType": TASK_TYPE,
        "content": {
            "parts": [{"text": text}],
        },
    }
    if OUTPUT_DIMENSIONALITY:
        payload["outputDimensionality"] = int(OUTPUT_DIMENSIONALITY)

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(EMBED_URL, headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                data = response.json()
                values = data.get("embedding", {}).get("values")
                if not isinstance(values, list) or not values:
                    raise RuntimeError("Invalid Gemini embedding response format")
                return values

            if response.status_code in (429, 502, 503, 504) and attempt < max_retries:
                backoff = delay_base * (2 ** (attempt - 1))
                logger.warning(
                    "Transient Gemini embedding error %s; retrying in %.1f sec",
                    response.status_code,
                    backoff,
                )
                time.sleep(backoff)
                continue

            raise RuntimeError(
                f"Gemini embedding API returned HTTP {response.status_code}: {response.text}"
            )
        except requests.RequestException as exc:
            if attempt < max_retries:
                backoff = delay_base * (2 ** (attempt - 1))
                logger.warning(
                    "Gemini embedding network error (%s); retrying in %.1f sec",
                    exc,
                    backoff,
                )
                time.sleep(backoff)
                continue
            raise RuntimeError(f"Failed to call Gemini embedding API: {exc}") from exc

    raise RuntimeError("Exceeded retries calling Gemini embedding API")


def get_embedding(text: str) -> List[float]:
    key = hashlib.md5(text.encode("utf-8")).hexdigest()
    if key in _embedding_cache:
        return _embedding_cache[key]

    embedding = _call_gemini_embedding_api(text)
    _embedding_cache[key] = embedding
    return embedding


def get_embeddings(texts: List[str]) -> List[List[float]]:
    return [get_embedding(text) for text in texts]
