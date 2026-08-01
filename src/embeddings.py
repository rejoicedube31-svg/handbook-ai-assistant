"""Create text embeddings with Sentence Transformers.

Why embeddings?
They turn text into number vectors so "attendance policy" can match
"minimum class attendance" even when the words are not identical.
"""

from __future__ import annotations

from functools import lru_cache

from sentence_transformers import SentenceTransformer

# Small, fast, runs locally — no API key needed for embeddings.
DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model(model_name: str = DEFAULT_MODEL) -> SentenceTransformer:
    """Load the model once and reuse it (downloads on first use)."""
    return SentenceTransformer(model_name)


def embed_texts(texts: list[str], model_name: str = DEFAULT_MODEL) -> list[list[float]]:
    """Return one embedding vector per input string."""
    if not texts:
        return []
    model = get_embedding_model(model_name)
    vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return [vector.tolist() for vector in vectors]


def embed_query(question: str, model_name: str = DEFAULT_MODEL) -> list[float]:
    """Embed a single user question."""
    return embed_texts([question], model_name=model_name)[0]
