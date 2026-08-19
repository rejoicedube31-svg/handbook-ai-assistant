"""Persist and search knowledge-base embeddings in ChromaDB.

Capstone: one collection holds Handbook + Website chunks, each with metadata.
"""

from __future__ import annotations

from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_DIR = ROOT / "chroma_db"
COLLECTION_NAME = "knowledge_base"


def get_collection(db_dir: Path = DEFAULT_DB_DIR):
    """Open (or create) the persistent Chroma collection."""
    client = chromadb.PersistentClient(path=str(db_dir))
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def reset_collection(db_dir: Path = DEFAULT_DB_DIR):
    """Delete and recreate the collection (used on fresh ingest)."""
    client = chromadb.PersistentClient(path=str(db_dir))
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def chunk_to_metadata(chunk: dict) -> dict:
    """Chroma only accepts str/int/float/bool — never None."""
    page = chunk.get("page")
    return {
        "source": str(chunk.get("source") or ""),
        "page": int(page) if page is not None else 0,
        "url": str(chunk.get("url") or ""),
    }


def store_chunks(
    chunks: list[dict],
    embeddings: list[list[float]],
    db_dir: Path = DEFAULT_DB_DIR,
) -> int:
    """Replace the DB contents with these chunks + embeddings."""
    if len(chunks) != len(embeddings):
        raise ValueError("chunks and embeddings must be the same length")

    collection = reset_collection(db_dir)
    if not chunks:
        return 0

    collection.add(
        ids=[chunk["chunk_id"] for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[chunk_to_metadata(chunk) for chunk in chunks],
        embeddings=embeddings,
    )
    return len(chunks)


def search_chunks(
    query_embedding: list[float],
    n_results: int = 4,
    db_dir: Path = DEFAULT_DB_DIR,
) -> list[dict]:
    """Return the most similar chunks for a query embedding."""
    collection = get_collection(db_dir)
    if collection.count() == 0:
        return []

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n_results, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    matches: list[dict] = []
    ids = result.get("ids", [[]])[0]
    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]

    for chunk_id, document, metadata, distance in zip(
        ids, documents, metadatas, distances
    ):
        metadata = metadata or {}
        page_value = metadata.get("page", 0)
        matches.append(
            {
                "chunk_id": chunk_id,
                "text": document,
                "source": metadata.get("source") or "",
                "page": int(page_value) if page_value else None,
                "url": metadata.get("url") or "",
                "distance": float(distance),
            }
        )
    return matches
