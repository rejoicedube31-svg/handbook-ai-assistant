"""Build unified knowledge chunks from Handbook PDF + ZAIO website (Capstone Day 4)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.chunking import SOURCE_HANDBOOK, SOURCE_WEBSITE, chunk_pages, chunk_website_pages
from src.pdf_loader import load_pages

DEFAULT_PDF = ROOT / "data" / "handbook.pdf"
DEFAULT_WEBSITE = ROOT / "data" / "website_clean.json"
DEFAULT_OUTPUT = ROOT / "data" / "knowledge_chunks.json"


def load_website_pages(path: Path = DEFAULT_WEBSITE) -> list[dict]:
    """Load cleaned website pages from Day 3."""
    if not path.exists():
        raise FileNotFoundError(
            f"Website data not found: {path}\n"
            "Run: python src/web_crawler.py"
        )
    return json.loads(path.read_text(encoding="utf-8"))


def build_handbook_chunks(pdf_path: Path = DEFAULT_PDF) -> list[dict]:
    pages = load_pages(pdf_path)
    return chunk_pages(pages)


def build_website_chunks(website_path: Path = DEFAULT_WEBSITE) -> list[dict]:
    pages = load_website_pages(website_path)
    return chunk_website_pages(pages)


def build_all_chunks(
    pdf_path: Path = DEFAULT_PDF,
    website_path: Path = DEFAULT_WEBSITE,
) -> list[dict]:
    """Combine handbook + website chunks into one knowledge base."""
    handbook_chunks = build_handbook_chunks(pdf_path)
    website_chunks = build_website_chunks(website_path)
    return handbook_chunks + website_chunks


def save_chunks(chunks: list[dict], output_path: Path = DEFAULT_OUTPUT) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(chunks, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output_path


def summarize_chunks(chunks: list[dict]) -> dict:
    handbook = [c for c in chunks if c["source"] == SOURCE_HANDBOOK]
    website = [c for c in chunks if c["source"] == SOURCE_WEBSITE]
    return {
        "total": len(chunks),
        "handbook": len(handbook),
        "website": len(website),
    }


def main() -> None:
    print("Building unified knowledge chunks...")
    chunks = build_all_chunks()
    stats = summarize_chunks(chunks)
    path = save_chunks(chunks)

    print(f"Handbook chunks: {stats['handbook']}")
    print(f"Website chunks:  {stats['website']}")
    print(f"Total chunks:    {stats['total']}")
    print(f"Saved -> {path}")

    handbook_sample = next(c for c in chunks if c["source"] == SOURCE_HANDBOOK)
    website_sample = next(c for c in chunks if c["source"] == SOURCE_WEBSITE)
    print("-" * 60)
    print(
        f"Handbook sample: id={handbook_sample['chunk_id']} "
        f"page={handbook_sample['page']}"
    )
    print(
        f"Website sample:  id={website_sample['chunk_id']} "
        f"url={website_sample['url']}"
    )
    print("Capstone Day 4 chunking OK.")


if __name__ == "__main__":
    main()
