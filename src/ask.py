"""Day 2 ask CLI: question → retrieve → generate → print answer + source."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.generate import NOT_AVAILABLE, generate_answer
from src.retrieve import best_source_page, format_context, retrieve


def ask(question: str) -> dict:
    """Full RAG path used later by the API as well."""
    chunks = retrieve(question)
    context = format_context(chunks)
    answer = generate_answer(question, context)

    if answer.strip() == NOT_AVAILABLE:
        source = None
    else:
        source = best_source_page(chunks)

    return {
        "answer": answer,
        "source": source,
        "chunks_used": len(chunks),
    }


def main() -> None:
    if len(sys.argv) < 2:
        print('Usage: python src/ask.py "Your question here"')
        sys.exit(1)

    question = " ".join(sys.argv[1:]).strip()
    print(f"Question: {question}")
    result = ask(question)
    print("-" * 60)
    print(f"Answer: {result['answer']}")
    print(f"Source: {result['source'] or 'N/A'}")
    print(f"Chunks used: {result['chunks_used']}")


if __name__ == "__main__":
    main()
