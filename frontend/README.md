# PolicyPal Frontend

Next.js dashboard and document-analysis interface for PolicyPal.

## Development

Start the FastAPI backend from the repository root, then run:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://127.0.0.1:3000`.

The server-side API proxy uses `POLICYPAL_API_URL`, defaulting to
`http://127.0.0.1:8000/api/v1`. Set `BEARER_TOKEN` in `frontend/.env.local`
only when the protected HackRx endpoint is required. Secrets are never sent
to the browser.

## Checks

```powershell
npm run lint
npm run build
```
