"""Capstone API: POST /ask for handbook + ZAIO website questions (n8n-ready JSON).

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
    title="Handbook AI Assistant (Capstone)",
    description=(
        "Ask questions answered from the Student Handbook PDF and the ZAIO website. "
        "Returns answer + source (handbook page or website URL)."
    ),
    version="0.2.0",
)


class AskRequest(BaseModel):
    question: str = Field(
        ...,
        description="The student's question",
        examples=["What courses does ZAIO offer?"],
    )

    @field_validator("question")
    @classmethod
    def question_must_not_be_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("question must not be empty")
        return cleaned


class AskResponse(BaseModel):
    answer: str = Field(
        ...,
        description="Generated answer, or the Capstone not-found message",
    )
    source: str | None = Field(
        default=None,
        description=(
            'Citation: website URL (e.g. "https://www.zaio.io/...") '
            'or "Student Handbook - Page N". Null when not found.'
        ),
    )


@app.exception_handler(RequestValidationError)
async def invalid_request_handler(_request, _exc: RequestValidationError):
    """Handle invalid requests gracefully with JSON (n8n-ready)."""
    return JSONResponse(
        status_code=400,
        content={
            "error": 'Invalid request. Send JSON like {"question": "Your question here"}.'
        },
    )


@app.get("/")
def health():
    """Simple health check so you can confirm the server is up."""
    return {
        "status": "ok",
        "message": "Handbook AI Assistant Capstone API is running",
        "sources": ["Student Handbook", "ZAIO Website"],
    }


@app.post("/ask", response_model=AskResponse)
def ask_endpoint(payload: AskRequest) -> AskResponse:
    """
    Ask a question against the Student Handbook and ZAIO website.

    Example request:
    ```json
    {"question": "What courses does ZAIO offer?"}
    ```

    Example responses:
    ```json
    {
      "answer": "...",
      "source": "https://www.zaio.io/bootcamps"
    }
    ```
    or
    ```json
    {
      "answer": "...",
      "source": "Student Handbook - Page 18"
    }
    ```
    or (not found):
    ```json
    {
      "answer": "I could not find that information in the available knowledge base.",
      "source": null
    }
    ```
    """
    result = ask(payload.question)
    return AskResponse(answer=result["answer"], source=result["source"])
