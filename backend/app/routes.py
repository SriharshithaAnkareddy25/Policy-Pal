import logging
import os
import re
import json
import tempfile
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field, field_validator

from backend.services.pinecone_store import ingest_document
from ml.pipeline.pipeline_qa import answer_questions

load_dotenv()

router = APIRouter()
security = HTTPBearer()
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
logger = logging.getLogger(__name__)

SUPPORTED_DOCUMENT_EXTENSIONS = (".pdf", ".docx", ".eml")
MAX_UPLOAD_SIZE = 20 * 1024 * 1024


def _public_error_detail(exc: Exception) -> str:
    detail = str(exc) or exc.__class__.__name__
    detail = re.sub(r"key=[^&\s'\"]+", "key=<redacted>", detail)
    detail = re.sub(r"(x-goog-api-key['\"]?\s*:\s*)[^,\s}]+", r"\1<redacted>", detail)
    return detail[:500]


class DocumentRequest(BaseModel):
    documents: str = Field(..., min_length=1)
    questions: List[str] = Field(..., min_length=1)

    @field_validator("documents")
    @classmethod
    def validate_document(cls, value: str) -> str:
        document = value.strip()
        if not document:
            raise ValueError("documents must not be empty")

        path_without_query = document.split("?", 1)[0].lower()
        if not path_without_query.endswith(SUPPORTED_DOCUMENT_EXTENSIONS):
            supported = ", ".join(SUPPORTED_DOCUMENT_EXTENSIONS)
            raise ValueError(f"Unsupported document type. Supported types: {supported}")
        return document

    @field_validator("questions")
    @classmethod
    def validate_questions(cls, value: List[str]) -> List[str]:
        questions = [question.strip() for question in value if question and question.strip()]
        if not questions:
            raise ValueError("questions must contain at least one non-empty question")
        return questions


class DocumentResponse(BaseModel):
    answers: List[str]


def _process_document_request(request: DocumentRequest) -> DocumentResponse:
    logger.info("Processing document request with %d question(s)", len(request.questions))
    ingest_document(request.documents)
    answers = answer_questions(
        document_url=request.documents,
        questions=request.questions,
        top_k=8,
    )
    return DocumentResponse(answers=answers)


def _parse_upload_questions(raw_questions: str) -> List[str]:
    try:
        value = json.loads(raw_questions)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=422, detail="questions must be a JSON array") from exc

    if not isinstance(value, list):
        raise HTTPException(status_code=422, detail="questions must be a JSON array")

    questions = [str(question).strip() for question in value if str(question).strip()]
    if not questions:
        raise HTTPException(status_code=422, detail="At least one question is required")
    return questions


async def _save_upload(upload: UploadFile) -> str:
    extension = Path(upload.filename or "").suffix.lower()
    if extension not in SUPPORTED_DOCUMENT_EXTENSIONS:
        supported = ", ".join(SUPPORTED_DOCUMENT_EXTENSIONS)
        raise HTTPException(status_code=415, detail=f"Unsupported document type. Supported types: {supported}")

    size = 0
    temp_path = ""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as temp_file:
            temp_path = temp_file.name
            while chunk := await upload.read(1024 * 1024):
                size += len(chunk)
                if size > MAX_UPLOAD_SIZE:
                    raise HTTPException(status_code=413, detail="Document exceeds the 20 MB upload limit")
                temp_file.write(chunk)
        if size == 0:
            raise HTTPException(status_code=422, detail="Uploaded document is empty")
        return temp_path
    except Exception:
        if temp_path:
            try:
                os.unlink(temp_path)
            except OSError:
                pass
        raise
    finally:
        await upload.close()


@router.post("/process-document", response_model=DocumentResponse)
async def process_document(request: DocumentRequest):
    try:
        return _process_document_request(request)
    except Exception as exc:
        logger.exception("Document processing failed")
        raise HTTPException(status_code=500, detail=_public_error_detail(exc)) from exc


@router.post("/process-upload", response_model=DocumentResponse)
async def process_upload(
    document: UploadFile = File(...),
    questions: str = Form(...),
):
    parsed_questions = _parse_upload_questions(questions)
    temp_path = await _save_upload(document)
    try:
        logger.info(
            "Processing uploaded document %s with %d question(s)",
            document.filename,
            len(parsed_questions),
        )
        ingest_document(temp_path, force=True)
        answers = answer_questions(
            document_url=temp_path,
            questions=parsed_questions,
            top_k=8,
        )
        return DocumentResponse(answers=answers)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Uploaded document processing failed")
        raise HTTPException(status_code=500, detail=_public_error_detail(exc)) from exc
    finally:
        try:
            os.unlink(temp_path)
        except OSError:
            logger.warning("Unable to delete uploaded temporary document")


@router.post("/hackrx/run", response_model=DocumentResponse)
async def run_hackrx_submission(
    request: DocumentRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    if not BEARER_TOKEN or credentials.credentials != BEARER_TOKEN:
        logger.warning("Rejected /hackrx/run request with invalid bearer token")
        raise HTTPException(status_code=403, detail="Invalid token")

    try:
        return _process_document_request(request)
    except Exception as exc:
        logger.exception("HackRx pipeline request failed")
        raise HTTPException(status_code=500, detail=_public_error_detail(exc)) from exc
