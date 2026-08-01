"""Day 3 API: POST /ask for handbook questions (n8n-ready JSON).

Why FastAPI?
- Accepts/returns JSON easily (Part 5 / n8n prep)
- Validates request bodies and returns clear errors
"""

from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.ask import ask

app = FastAPI(
    title="Handbook AI Assistant",
    description="Ask questions about the student handbook.",
    version="0.1.0",
)


class AskRequest(BaseModel):
    question: str = Field(..., description="The student's question")

    @field_validator("question")
    @classmethod
    def question_must_not_be_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("question must not be empty")
        return cleaned


class AskResponse(BaseModel):
    answer: str
    source: str | None = None


@app.exception_handler(RequestValidationError)
async def invalid_request_handler(_request, _exc: RequestValidationError):
    """Part 5: handle invalid requests gracefully with JSON."""
    return JSONResponse(
        status_code=400,
        content={
            "error": 'Invalid request. Send JSON like {"question": "Your question here"}.'
        },
    )


@app.get("/")
def health():
    """Simple health check so you can confirm the server is up."""
    return {"status": "ok", "message": "Handbook AI Assistant is running"}


@app.post("/ask", response_model=AskResponse)
def ask_endpoint(payload: AskRequest) -> AskResponse:
    """
    Example request:
    {"question": "When are the live classes?"}

    Example response:
    {"answer": "...", "source": "Page 11"}
    """
    result = ask(payload.question)
    return AskResponse(answer=result["answer"], source=result["source"])
