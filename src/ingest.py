"""Ingest pipeline: PDF → pages → chunks → embeddings → ChromaDB.

Day 1 stopped at chunks. Day 2 stores vectors so we can search later.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.chunking import chunk_pages
from src.embeddings import embed_texts
from src.pdf_loader import load_pages
from src.vectorstore import store_chunks

DEFAULT_PDF = ROOT / "data" / "handbook.pdf"


def build_chunks(pdf_path: Path = DEFAULT_PDF) -> list[dict]:
    pages = load_pages(pdf_path)
    return chunk_pages(pages)


def ingest(pdf_path: Path = DEFAULT_PDF) -> list[dict]:
    """Full Day 2 ingest: chunk, embed, and persist to ChromaDB."""
    pages = load_pages(pdf_path)
    chunks = chunk_pages(pages)
    embeddings = embed_texts([chunk["text"] for chunk in chunks])
    stored = store_chunks(chunks, embeddings)
    return chunks if stored == len(chunks) else chunks


def main() -> None:
    pdf_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PDF
    print(f"Loading: {pdf_path}")

    pages = load_pages(pdf_path)
    non_empty = sum(1 for page in pages if page["text"])
    print(f"Pages loaded: {len(pages)} ({non_empty} with text)")

    chunks = chunk_pages(pages)
    print(f"Chunks created: {len(chunks)}")

    for chunk in chunks[:3]:
        preview = chunk["text"][:120].replace("\n", " ")
        print("-" * 60)
        print(f"id={chunk['chunk_id']}  page={chunk['page']}")
        print(preview + ("..." if len(chunk["text"]) > 120 else ""))

    if not chunks:
        print("No chunks created. Is the PDF empty or image-only (scanned)?")
        return

    print("-" * 60)
    print("Creating embeddings (first run may download the model)...")
    embeddings = embed_texts([chunk["text"] for chunk in chunks])
    print(f"Embeddings created: {len(embeddings)} (dim={len(embeddings[0])})")

    stored = store_chunks(chunks, embeddings)
    print(f"Stored in ChromaDB: {stored} chunks -> chroma_db/")
    print("Day 2 ingest OK — handbook is searchable.")


if __name__ == "__main__":
    main()
