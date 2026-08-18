"""Unit tests for Capstone unified chunk metadata."""

from src.chunking import SOURCE_HANDBOOK, SOURCE_WEBSITE, chunk_pages, chunk_website_pages


def test_handbook_chunks_include_source_and_page():
    pages = [{"page": 7, "text": "Orientation Day is on 15 January 2026. " * 15}]
    chunks = chunk_pages(pages, chunk_size=80, chunk_overlap=20)
    assert len(chunks) > 0
    assert chunks[0]["source"] == SOURCE_HANDBOOK
    assert chunks[0]["page"] == 7
    assert chunks[0]["url"] == ""
    assert chunks[0]["chunk_id"].startswith("handbook_p7_c")


def test_website_chunks_include_source_and_url():
    pages = [
        {
            "url": "https://www.zaio.io/bootcamps",
            "text": "Full Stack AI Engineer bootcamp details. " * 20,
            "char_count": 800,
        }
    ]
    chunks = chunk_website_pages(pages, chunk_size=80, chunk_overlap=20, min_chars=200)
    assert len(chunks) > 0
    assert chunks[0]["source"] == SOURCE_WEBSITE
    assert chunks[0]["page"] is None
    assert chunks[0]["url"] == "https://www.zaio.io/bootcamps"
    assert chunks[0]["chunk_id"].startswith("website_bootcamps_c")


def test_website_skips_short_pages():
    pages = [
        {"url": "https://www.zaio.io/events", "text": "tiny", "char_count": 50},
    ]
    chunks = chunk_website_pages(pages, min_chars=200)
    assert chunks == []
