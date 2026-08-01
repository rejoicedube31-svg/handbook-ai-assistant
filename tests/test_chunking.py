"""Unit tests for page chunking."""

import pytest

from src.chunking import chunk_pages


def test_chunks_keep_page_numbers():
    pages = [
        {"page": 7, "text": "Orientation Day: 15 January 2026 at 10 am. " * 20},
        {"page": 11, "text": "Live classes every Thursday 6pm-8pm. " * 20},
    ]
    chunks = chunk_pages(pages, chunk_size=80, chunk_overlap=20)

    assert len(chunks) > 0
    assert all("text" in chunk and "page" in chunk and "chunk_id" in chunk for chunk in chunks)
    assert {chunk["page"] for chunk in chunks} == {7, 11}
    assert chunks[0]["chunk_id"].startswith("p7_c")


def test_skips_empty_pages():
    pages = [
        {"page": 1, "text": ""},
        {"page": 2, "text": "Hello handbook world"},
    ]
    chunks = chunk_pages(pages, chunk_size=50, chunk_overlap=10)
    assert len(chunks) == 1
    assert chunks[0]["page"] == 2


def test_rejects_invalid_overlap():
    with pytest.raises(ValueError):
        chunk_pages([{"page": 1, "text": "abc"}], chunk_size=10, chunk_overlap=10)
