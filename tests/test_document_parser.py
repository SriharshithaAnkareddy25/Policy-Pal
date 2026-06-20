import pytest

from backend.app import document_parser


def test_extract_text_routes_pdf(monkeypatch):
    monkeypatch.setattr(document_parser, "extract_text_from_pdf", lambda path: f"pdf:{path}")

    assert document_parser.extract_text("sample.pdf") == "pdf:sample.pdf"


def test_extract_text_rejects_unsupported_extension():
    with pytest.raises(ValueError, match="Unsupported file type"):
        document_parser.extract_text("sample.txt")
