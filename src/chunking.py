"""Split text into overlapping chunks with Capstone metadata.

Why chunk?
Embeddings and search work better on small pieces than on a whole document.
Each chunk carries source metadata for citation (Handbook page or Website URL).
"""

from __future__ import annotations

import re
from urllib.parse import urlparse

SOURCE_HANDBOOK = "Handbook"
SOURCE_WEBSITE = "Website"


def _slug_from_url(url: str) -> str:
    """Turn a URL path into a safe chunk-id prefix."""
    path = urlparse(url).path.strip("/") or "home"
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", path).strip("-").lower()
    return slug or "home"


def chunk_text(
    text: str,
    *,
    chunk_id_prefix: str,
    source: str,
    page: int | None = None,
    url: str | None = None,
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> list[dict]:
    """Split one text block into chunks with unified metadata."""
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    normalized = " ".join((text or "").split())
    if not normalized:
        return []

    chunks: list[dict] = []
    start = 0
    chunk_index = 0

    while start < len(normalized):
        end = start + chunk_size
        piece = normalized[start:end].strip()
        if piece:
            chunks.append(
                {
                    "text": piece,
                    "source": source,
                    "page": page,
                    "url": url or "",
                    "chunk_id": f"{chunk_id_prefix}_c{chunk_index}",
                }
            )
            chunk_index += 1

        if end >= len(normalized):
            break
        start = end - chunk_overlap

    return chunks


def chunk_pages(
    pages: list[dict],
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> list[dict]:
    """Turn handbook page texts into chunks with page numbers.

    Backward compatible with the original assignment, now with Capstone metadata.
    """
    chunks: list[dict] = []
    for page in pages:
        page_number = page["page"]
        page_chunks = chunk_text(
            page.get("text") or "",
            chunk_id_prefix=f"handbook_p{page_number}",
            source=SOURCE_HANDBOOK,
            page=page_number,
            url="",
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        chunks.extend(page_chunks)
    return chunks


def chunk_website_pages(
    pages: list[dict],
    chunk_size: int = 800,
    chunk_overlap: int = 150,
    min_chars: int = 200,
) -> list[dict]:
    """Turn cleaned website pages into chunks with URL metadata."""
    chunks: list[dict] = []
    for page in pages:
        if page.get("char_count", len(page.get("text", ""))) < min_chars:
            continue
        url = page["url"]
        prefix = f"website_{_slug_from_url(url)}"
        page_chunks = chunk_text(
            page.get("text") or "",
            chunk_id_prefix=prefix,
            source=SOURCE_WEBSITE,
            page=None,
            url=url,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        chunks.extend(page_chunks)
    return chunks
