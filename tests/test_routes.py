import os

from fastapi.testclient import TestClient

import backend.app.routes as routes
from main import app


def test_health_check_does_not_require_external_services():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_hackrx_run_success(monkeypatch):
    monkeypatch.setattr(routes, "BEARER_TOKEN", "test-token")
    monkeypatch.setattr(routes, "ingest_document", lambda document: "source-id")
    monkeypatch.setattr(
        routes,
        "answer_questions",
        lambda document_url, questions, top_k: ["Covered."],
    )
    client = TestClient(app)

    response = client.post(
        "/api/v1/hackrx/run",
        headers={"Authorization": "Bearer test-token"},
        json={
            "documents": "https://example.com/policy.pdf",
            "questions": ["Is it covered?"],
        },
    )

    assert response.status_code == 200
    assert response.json() == {"answers": ["Covered."]}


def test_hackrx_run_rejects_invalid_token(monkeypatch):
    monkeypatch.setattr(routes, "BEARER_TOKEN", "test-token")
    client = TestClient(app)

    response = client.post(
        "/api/v1/hackrx/run",
        headers={"Authorization": "Bearer wrong-token"},
        json={
            "documents": "https://example.com/policy.pdf",
            "questions": ["Is it covered?"],
        },
    )

    assert response.status_code == 403


def test_process_document_rejects_empty_questions():
    client = TestClient(app)

    response = client.post(
        "/api/v1/process-document",
        json={"documents": "https://example.com/policy.pdf", "questions": []},
    )

    assert response.status_code == 422


def test_process_document_returns_controlled_error(monkeypatch):
    monkeypatch.setattr(
        routes,
        "ingest_document",
        lambda document: (_ for _ in ()).throw(RuntimeError("ingestion failed")),
    )
    client = TestClient(app)

    response = client.post(
        "/api/v1/process-document",
        json={
            "documents": "https://example.com/policy.pdf",
            "questions": ["Is it covered?"],
        },
    )

    assert response.status_code == 500
    assert response.json()["detail"] == "ingestion failed"


def test_process_upload_ingests_file_and_cleans_up(monkeypatch):
    observed = {}

    def fake_ingest(path, force=False):
        observed["path"] = path
        observed["force"] = force
        observed["existed_during_ingestion"] = os.path.exists(path)
        return "source-id"

    monkeypatch.setattr(routes, "ingest_document", fake_ingest)
    monkeypatch.setattr(
        routes,
        "answer_questions",
        lambda document_url, questions, top_k: ["Uploaded content found."],
    )
    client = TestClient(app)

    response = client.post(
        "/api/v1/process-upload",
        files={"document": ("policy.pdf", b"sample pdf bytes", "application/pdf")},
        data={"questions": '["What does this document contain?"]'},
    )

    assert response.status_code == 200
    assert response.json() == {"answers": ["Uploaded content found."]}
    assert observed["force"] is True
    assert observed["existed_during_ingestion"] is True
    assert not os.path.exists(observed["path"])


def test_process_upload_rejects_unsupported_file_type():
    client = TestClient(app)

    response = client.post(
        "/api/v1/process-upload",
        files={"document": ("notes.txt", b"plain text", "text/plain")},
        data={"questions": '["What is this?"]'},
    )

    assert response.status_code == 415
