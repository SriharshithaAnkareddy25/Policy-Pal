import email
import logging
import os
import tempfile

import fitz
import requests
from docx import Document

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".eml"}


def download_file(url: str) -> str:
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()

        suffix = os.path.splitext(url.split("?", 1)[0])[-1].lower()
        if suffix not in SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {suffix or '<none>'}")

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(response.content)
            temp_path = tmp_file.name

        logger.info("Downloaded remote document to temporary file")
        return temp_path
    except Exception:
        logger.exception("Error downloading remote document")
        raise


def clean_text(text: str) -> str:
    lines = text.splitlines()
    filtered = [
        line.strip()
        for line in lines
        if line.strip() and not line.lower().startswith("page")
    ]
    return "\n".join(filtered)


def extract_text_from_pdf(file_path: str) -> str:
    try:
        texts = []
        with fitz.open(file_path) as doc:
            for page in doc:
                texts.append(page.get_text("text"))
        return clean_text("\n".join(texts)).strip()
    except Exception:
        logger.exception("Error extracting PDF text")
        raise


def extract_text_from_docx(file_path: str) -> str:
    try:
        doc = Document(file_path)
        return clean_text("\n".join(para.text for para in doc.paragraphs)).strip()
    except Exception:
        logger.exception("Error extracting DOCX text")
        raise


def extract_text_from_email(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            message = email.message_from_file(file)

        parts = []
        for part in message.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                if isinstance(payload, bytes):
                    parts.append(payload.decode(errors="ignore"))
                else:
                    parts.append(str(part.get_payload()))

        return clean_text("\n".join(parts)).strip()
    except Exception:
        logger.exception("Error extracting email text")
        raise


def extract_text(file_path_or_url: str) -> str:
    temp_path = None
    if file_path_or_url.startswith(("http://", "https://")):
        file_path = download_file(file_path_or_url)
        temp_path = file_path
    else:
        file_path = file_path_or_url

    try:
        extension = os.path.splitext(file_path)[1].lower()
        logger.info("Extracting document text with extension=%s", extension)

        if extension == ".pdf":
            return extract_text_from_pdf(file_path)
        if extension == ".docx":
            return extract_text_from_docx(file_path)
        if extension == ".eml":
            return extract_text_from_email(file_path)
        raise ValueError(f"Unsupported file type: {extension}")
    finally:
        if temp_path:
            try:
                os.unlink(temp_path)
            except OSError:
                logger.warning("Unable to delete temporary document file")
