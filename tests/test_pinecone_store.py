from backend.services import pinecone_store


class FakeIndex:
    def __init__(self):
        self.upserts = []

    def upsert(self, vectors, namespace):
        self.upserts.append((vectors, namespace))


def test_ingest_document_skips_existing_namespace(monkeypatch):
    monkeypatch.setattr(pinecone_store, "document_already_ingested", lambda source_id: True)
    monkeypatch.setattr(
        pinecone_store,
        "extract_text",
        lambda document: (_ for _ in ()).throw(AssertionError("should not extract")),
    )

    source_id = pinecone_store.ingest_document("https://example.com/policy.pdf")

    assert source_id == pinecone_store.generate_source_id("https://example.com/policy.pdf")


def test_store_embeddings_upserts_to_source_namespace(monkeypatch):
    fake_index = FakeIndex()
    monkeypatch.setattr(pinecone_store, "chunk_text", lambda text: ["alpha", "beta"])
    monkeypatch.setattr(pinecone_store, "get_embedding", lambda text: [0.1, 0.2])
    monkeypatch.setattr(pinecone_store, "ensure_index", lambda dimension=None: fake_index)
    monkeypatch.setattr(pinecone_store, "get_index", lambda: fake_index)

    count = pinecone_store.store_embeddings_for_text("alpha beta", source_id="source-1")

    assert count == 2
    assert fake_index.upserts[0][1] == "source-1"
    assert fake_index.upserts[0][0][0]["metadata"]["source"] == "source-1"
