"""Retrieve the most relevant knowledge chunks for a question.

Flow: question → embed → search Chroma (handbook + website) → top chunks.
"""

from __future__ import annotations

from src.chunking import SOURCE_HANDBOOK, SOURCE_WEBSITE
from src.embeddings import embed_query
from src.vectorstore import search_chunks

# Cosine distance from Chroma (lower = more similar).
# Loose enough for real topics; the LLM decides when to refuse.
MAX_DISTANCE = 0.85

COURSE_HINTS = (
    "course",
    "courses",
    "bootcamp",
    "bootcamps",
    "programme",
    "program",
    "offer",
)


def _merge_by_best_distance(matches: list[dict]) -> list[dict]:
    """Keep the best (lowest distance) copy of each chunk_id."""
    best: dict[str, dict] = {}
    for match in matches:
        chunk_id = match["chunk_id"]
        current = best.get(chunk_id)
        if current is None or match["distance"] < current["distance"]:
            best[chunk_id] = match
    return sorted(best.values(), key=lambda item: item["distance"])


def retrieve(question: str, n_results: int = 6) -> list[dict]:
    """Return relevant chunks across handbook and website sources."""
    query_embedding = embed_query(question)
    matches = search_chunks(query_embedding, n_results=max(n_results, 8))

    # Course questions often need the /bootcamps listing chunks; help them surface.
    lower = question.lower()
    if any(hint in lower for hint in COURSE_HINTS):
        course_embedding = embed_query(
            "ZAIO bootcamps courses Full Stack AI Engineer "
            "Data Science Cybersecurity Digital Marketing Cloud DevOps"
        )
        matches.extend(search_chunks(course_embedding, n_results=8))

    merged = _merge_by_best_distance(matches)
    filtered = [match for match in merged if match["distance"] <= MAX_DISTANCE]
    return filtered[:n_results]


def format_source_label(chunk: dict) -> str:
    """Format citation for API / context labels."""
    source = chunk.get("source") or ""
    if source == SOURCE_WEBSITE:
        url = (chunk.get("url") or "").strip()
        return url or "Website"
    page = chunk.get("page")
    if page:
        return f"Student Handbook - Page {page}"
    return "Student Handbook"


def format_context(chunks: list[dict]) -> str:
    """Build the context block we will send to the LLM."""
    if not chunks:
        return ""
    parts = []
    for chunk in chunks:
        label = format_source_label(chunk)
        parts.append(f"[{label}]\n{chunk['text']}")
    return "\n\n".join(parts)


def best_source(chunks: list[dict]) -> str | None:
    """Use the top-ranked chunk as the cited source."""
    if not chunks:
        return None
    return format_source_label(chunks[0])


# Kept for older imports / tests that still call this name.
def best_source_page(chunks: list[dict]) -> str | None:
    return best_source(chunks)
