"""Retrieve the handbook chunks most relevant to a question.

Flow: question → embed → search Chroma → return top chunks.
"""

from __future__ import annotations

from src.embeddings import embed_query
from src.vectorstore import search_chunks

# Cosine distance from Chroma (lower = more similar).
# Keep a loose cutoff so real handbook topics still reach the LLM;
# the LLM (not this filter) decides when to say "not available".
MAX_DISTANCE = 0.85


def retrieve(question: str, n_results: int = 4) -> list[dict]:
    """Return relevant chunks for a question (may be empty if none are close)."""
    query_embedding = embed_query(question)
    matches = search_chunks(query_embedding, n_results=n_results)
    return [match for match in matches if match["distance"] <= MAX_DISTANCE]


def format_context(chunks: list[dict]) -> str:
    """Build the context block we will send to the LLM."""
    if not chunks:
        return ""
    parts = []
    for chunk in chunks:
        parts.append(f"[Page {chunk['page']}]\n{chunk['text']}")
    return "\n\n".join(parts)


def best_source_page(chunks: list[dict]) -> str | None:
    """Use the top-ranked chunk's page as the cited source."""
    if not chunks:
        return None
    return f"Page {chunks[0]['page']}"
