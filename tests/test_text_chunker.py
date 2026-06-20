from backend.services.text_chunker import chunk_text


def test_chunk_text_removes_empty_chunks():
    chunks = chunk_text("First paragraph.\n\nSecond paragraph.", chunk_size=50, chunk_overlap=5)

    assert chunks
    assert all(chunk.strip() for chunk in chunks)
    assert "First paragraph" in chunks[0]
