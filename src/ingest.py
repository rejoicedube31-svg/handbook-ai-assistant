"""Ingest pipeline: handbook + website → chunks → embeddings → one ChromaDB.

Capstone Day 5: both knowledge sources live in the same vector collection.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.embeddings import embed_texts
from src.knowledge_base import build_all_chunks, save_chunks, summarize_chunks
from src.vectorstore import get_collection, store_chunks

DEFAULT_PDF = ROOT / "data" / "handbook.pdf"


def ingest() -> list[dict]:
    """Build all chunks, embed them, and persist to ChromaDB."""
    chunks = build_all_chunks()
    save_chunks(chunks)
    embeddings = embed_texts([chunk["text"] for chunk in chunks])
    store_chunks(chunks, embeddings)
    return chunks


def main() -> None:
    print("Building unified knowledge chunks (handbook + website)...")
    chunks = build_all_chunks()
    stats = summarize_chunks(chunks)
    save_chunks(chunks)

    print(f"Handbook chunks: {stats['handbook']}")
    print(f"Website chunks:  {stats['website']}")
    print(f"Total chunks:    {stats['total']}")

    if not chunks:
        print("No chunks created. Run website crawl and confirm the PDF exists.")
        return

    print("-" * 60)
    print("Creating embeddings...")
    embeddings = embed_texts([chunk["text"] for chunk in chunks])
    print(f"Embeddings created: {len(embeddings)} (dim={len(embeddings[0])})")

    stored = store_chunks(chunks, embeddings)
    collection = get_collection()
    print(f"Stored in ChromaDB: {stored} chunks -> chroma_db/")
    print(f"Collection count:   {collection.count()}")
    print("Capstone Day 5 ingest OK — both sources are searchable.")


if __name__ == "__main__":
    main()
