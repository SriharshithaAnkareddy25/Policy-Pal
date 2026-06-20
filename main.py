import logging

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routes import router as pipeline_router

load_dotenv()
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Policy QA Pipeline",
    description="Extracts document text and answers user questions using a retrieval-augmented QA system.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "policy-qa-pipeline"}


app.include_router(pipeline_router, prefix="/api/v1", tags=["Pipeline"])
