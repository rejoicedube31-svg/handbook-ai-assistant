"""Generate an answer from retrieved handbook context using an LLM.

Rules:
- Only answer from the provided context.
- If the context is missing or insufficient, return the fixed not-available message.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from openai import OpenAI

NOT_AVAILABLE = (
    "I'm sorry, I don't have that information in the student handbook."
)

SYSTEM_PROMPT = """You are a student handbook assistant.
Answer ONLY using the CONTEXT provided by the user.
If the context does not contain enough information to answer, reply exactly with:
I'm sorry, I don't have that information in the student handbook.
Do not invent policies, dates, fees, or rules.
Keep answers clear and concise.
"""


def generate_answer(question: str, context: str) -> str:
    """Ask the LLM to answer from context, or return not-available."""
    if not context.strip():
        return NOT_AVAILABLE

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Copy .env.example to .env and add your key."
        )

    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    user_prompt = (
        f"CONTEXT:\n{context}\n\n"
        f"QUESTION:\n{question}\n\n"
        "Answer using only the context."
    )

    response = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    answer = (response.choices[0].message.content or "").strip()
    return answer or NOT_AVAILABLE
