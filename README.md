# PolicyPal

PolicyPal is a FastAPI service for document-grounded policy question answering. It downloads a supported policy document, extracts text, chunks and embeds it, stores vectors in Pinecone, retrieves relevant excerpts, and asks Gemini to return concise JSON answers.

## Canonical Project Layout

The root application is the source of truth:

- `main.py` - FastAPI entrypoint (`main:app`)
- `backend/` - API routes, document parsing, retrieval, Pinecone, and embeddings
- `ml/` - prompt construction and Gemini answer generation
- `frontend/` - Next.js dashboard and server-side API proxy

The nested `PolicyPal/` folder is legacy duplicate code and is ignored by the root repository.

## Environment Variables

Create a local `.env` file with:

```env
PINECONE_API_KEY=...
GEMINI_EMBD_KEY=...
GEMINI_API_KEY=...
BEARER_TOKEN=...
```

Optional settings:

```env
PINECONE_INDEX_NAME=policy-embeddings
PINECONE_DEPLOY_TYPE=serverless
PINECONE_REGION=us-east-1
GEMINI_MODEL=gemini-2.5-flash
```

## Local Setup

```bash
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

## API

`POST /api/v1/process-document`

```json
{
  "documents": "https://example.com/policy.pdf",
  "questions": ["What is covered?"]
}
```

`POST /api/v1/process-upload`

Accepts multipart form data with a `document` field (`.pdf`, `.docx`, or
`.eml`, up to 20 MB) and `questions` as a JSON array string.

`POST /api/v1/hackrx/run`

Requires:

```http
Authorization: Bearer <BEARER_TOKEN>
```

Response:

```json
{
  "answers": ["..."]
}
```

Supported document types: `.pdf`, `.docx`, `.eml`.

## Deployment

Render uses:

```bash
pip install --upgrade pip && pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port $PORT
```

The `/health` endpoint is safe for platform health checks because it does not initialize Pinecone or call Gemini.

## Tests

Run fast mocked tests:

```bash
pytest
```

Real Pinecone/Gemini smoke testing should be run manually only when credentials and network access are available.
