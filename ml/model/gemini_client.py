import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def call_gemini_llm(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY in environment")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        MODEL_NAME,
        generation_config={"response_mime_type": "application/json"},
    )
    response = model.generate_content(prompt, request_options={"timeout": 60})
    text = getattr(response, "text", None)
    if not text or not text.strip():
        raise RuntimeError("Gemini returned an empty response")
    return text.strip()
