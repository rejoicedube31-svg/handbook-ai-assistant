"""Split handbook pages into overlapping text chunks.

Why chunk?
Embeddings and search work better on small pieces than on a whole PDF.
Overlap keeps sentences that sit on a chunk boundary from being cut in half.
"""

from __future__ import annotations


def chunk_pages(
    pages: list[dict],
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> list[dict]:
    """Turn page texts into chunks, keeping the source page number.

    Each chunk looks like:
    {"text": "...", "page": 12, "chunk_id": "p12_c0"}
    """
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks: list[dict] = []

    for page in pages:
        page_number = page["page"]
        text = " ".join((page.get("text") or "").split())
        if not text:
            continue

        start = 0
        chunk_index = 0
        while start < len(text):
            end = start + chunk_size
            piece = text[start:end].strip()
            if piece:
                chunks.append(
                    {
                        "text": piece,
                        "page": page_number,
                        "chunk_id": f"p{page_number}_c{chunk_index}",
                    }
                )
                chunk_index += 1

            if end >= len(text):
                break
            start = end - chunk_overlap

    return chunks
