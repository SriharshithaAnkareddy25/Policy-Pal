import hashlib
import logging
import os
import sys
import time
from typing import Any, List, Optional

from dotenv import load_dotenv

from backend.app.document_parser import extract_text
from backend.services.embedding import get_embedding
from backend.services.text_chunker import chunk_text

load_dotenv()

logger = logging.getLogger(__name__)

INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "policy-embeddings")
DEPLOY_TYPE = os.getenv("PINECONE_DEPLOY_TYPE", "serverless").lower()
REGION = os.getenv("PINECONE_REGION", "us-east-1")
BATCH_SIZE = int(os.getenv("PINECONE_BATCH_SIZE", "100"))

_pc: Optional[Any] = None
_index: Optional[Any] = None
_dimension: Optional[int] = None


def _index_names(indexes: Any) -> list[str]:
    if hasattr(indexes, "names"):
        return list(indexes.names())
    names = []
    for item in indexes:
        if isinstance(item, str):
            names.append(item)
        elif isinstance(item, dict):
            names.append(item.get("name", ""))
        else:
            names.append(getattr(item, "name", ""))
    return [name for name in names if name]


def get_pinecone_client() -> Any:
    global _pc
    if _pc is None:
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise RuntimeError("Missing PINECONE_API_KEY in environment")
        try:
            from pinecone import Pinecone
        except ImportError as exc:
            raise RuntimeError(
                "The Pinecone SDK loaded by "
                f"'{sys.executable}' does not expose Pinecone. Remove conflicting "
                "packages and reinstall with this interpreter: "
                f"'{sys.executable}' -m pip uninstall -y pinecone pinecone-client; "
                f"'{sys.executable}' -m pip install -r requirements.txt"
            ) from exc
        _pc = Pinecone(api_key=api_key)
    return _pc


def _make_spec():
    if DEPLOY_TYPE == "pod":
        from pinecone import PodSpec

        return PodSpec(name=os.getenv("PINECONE_POD_TYPE", "starter"), environment=REGION)
    from pinecone import ServerlessSpec

    return ServerlessSpec(cloud=os.getenv("PINECONE_CLOUD", "aws"), region=REGION)


def _describe_dimension(client: Any, index_name: str) -> Optional[int]:
    description = client.describe_index(index_name)
    if isinstance(description, dict):
        return description.get("dimension")
    return getattr(description, "dimension", None)


def get_embedding_dimension(sample_text: str = "dimension check") -> int:
    global _dimension
    if _dimension is None:
        embedding = get_embedding(sample_text)
        if not isinstance(embedding, list) or not embedding:
            raise RuntimeError("Embedding provider returned an invalid vector")
        _dimension = len(embedding)
        logger.info("Detected embedding dimension: %s", _dimension)
    return _dimension


def ensure_index(dimension: Optional[int] = None):
    client = get_pinecone_client()
    expected_dimension = dimension or get_embedding_dimension()
    existing_names = _index_names(client.list_indexes())

    if INDEX_NAME not in existing_names:
        logger.info(
            "Creating Pinecone index %s with dimension=%s deploy_type=%s",
            INDEX_NAME,
            expected_dimension,
            DEPLOY_TYPE,
        )
        try:
            client.create_index(
                name=INDEX_NAME,
                dimension=expected_dimension,
                metric="cosine",
                spec=_make_spec(),
            )
        except Exception as exc:
            if getattr(exc, "status", None) != 409:
                raise
            logger.info("Pinecone index %s already exists after create race", INDEX_NAME)
    else:
        existing_dimension = _describe_dimension(client, INDEX_NAME)
        if existing_dimension and existing_dimension != expected_dimension:
            raise RuntimeError(
                f"Pinecone index '{INDEX_NAME}' has dimension {existing_dimension}, "
                f"but embeddings are dimension {expected_dimension}. Create a compatible "
                "index or update PINECONE_INDEX_NAME."
            )
        logger.info("Using Pinecone index %s", INDEX_NAME)

    return get_index()


def get_index():
    global _index
    if _index is None:
        _index = get_pinecone_client().Index(INDEX_NAME)
    return _index


def generate_source_id(document_url: str) -> str:
    return hashlib.md5(document_url.encode("utf-8")).hexdigest()


def _namespace_vector_count(namespace: str) -> int:
    try:
        stats = get_index().describe_index_stats()
        namespaces = getattr(stats, "namespaces", None)
        if namespaces is None and isinstance(stats, dict):
            namespaces = stats.get("namespaces", {})
        namespace_stats = (namespaces or {}).get(namespace, {})
        if isinstance(namespace_stats, dict):
            return int(namespace_stats.get("vector_count", 0))
        return int(getattr(namespace_stats, "vector_count", 0))
    except Exception as exc:
        logger.warning("Unable to read Pinecone stats for namespace=%s: %s", namespace, exc)
        return 0


def document_already_ingested(source_id: str) -> bool:
    return _namespace_vector_count(source_id) > 0


def store_embeddings_for_text(text: str, source_id: str) -> int:
    chunks = chunk_text(text)
    total = 0

    for i in range(0, len(chunks), BATCH_SIZE):
        batch_chunks = chunks[i : i + BATCH_SIZE]
        vectors = []
        for j, chunk in enumerate(batch_chunks, start=i):
            cleaned = chunk.strip()
            if not cleaned:
                continue

            embedding = get_embedding(cleaned)
            if not isinstance(embedding, list) or not embedding:
                logger.warning("Embedding for chunk %s is invalid; skipping", j)
                continue

            ensure_index(dimension=len(embedding))
            vectors.append(
                {
                    "id": f"{j:06d}",
                    "values": embedding,
                    "metadata": {
                        "text": cleaned if len(cleaned) <= 2000 else cleaned[:2000],
                        "chunk_index": j,
                        "source": source_id,
                    },
                }
            )

        if not vectors:
            continue

        for attempt in range(1, 4):
            try:
                get_index().upsert(vectors=vectors, namespace=source_id)
                break
            except Exception as exc:
                backoff = 2 ** (attempt - 1)
                logger.warning(
                    "Pinecone upsert attempt %s failed for namespace=%s; retrying in %s sec: %s",
                    attempt,
                    source_id,
                    backoff,
                    exc,
                )
                time.sleep(backoff)
        else:
            raise RuntimeError(f"Failed to upsert vectors into namespace={source_id}")

        total += len(vectors)

    logger.info("Stored %d embedding vector(s) under namespace=%s", total, source_id)
    return total


def ingest_document(document_url: str, force: bool = False) -> str:
    source_id = generate_source_id(document_url)

    if not force:
        try:
            if document_already_ingested(source_id):
                logger.info("Document already ingested; skipping re-embedding namespace=%s", source_id)
                return source_id
        except Exception as exc:
            logger.warning("Could not verify ingestion cache for namespace=%s: %s", source_id, exc)

    text = extract_text(document_url)
    if not text or not text.strip():
        raise ValueError("No extractable text found in the document.")

    store_embeddings_for_text(text, source_id=source_id)
    return source_id
