"""Day 1 ingest: PDF → pages → chunks (print a quick check).

Embeddings + vector DB come on Day 2.
"""

from pathlib import Path
import sys

# Allow `python src/ingest.py` from the project root
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.pdf_loader import load_pages
from src.chunking import chunk_pages


DEFAULT_PDF = ROOT / "data" / "handbook.pdf"


def build_chunks(pdf_path: Path = DEFAULT_PDF) -> list[dict]:
    pages = load_pages(pdf_path)
    return chunk_pages(pages)


def main() -> None:
    pdf_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PDF
    print(f"Loading: {pdf_path}")

    pages = load_pages(pdf_path)
    non_empty = sum(1 for p in pages if p["text"])
    print(f"Pages loaded: {len(pages)} ({non_empty} with text)")

    chunks = chunk_pages(pages)
    print(f"Chunks created: {len(chunks)}")

    # Quick check: show the first 3 chunks
    for chunk in chunks[:3]:
        preview = chunk["text"][:120].replace("\n", " ")
        print("-" * 60)
        print(f"id={chunk['chunk_id']}  page={chunk['page']}")
        print(preview + ("..." if len(chunk["text"]) > 120 else ""))

    if chunks:
        print("-" * 60)
        print("Day 1 quick check OK — PDF extracted and chunked with page numbers.")
    else:
        print("No chunks created. Is the PDF empty or image-only (scanned)?")


if __name__ == "__main__":
    main()
