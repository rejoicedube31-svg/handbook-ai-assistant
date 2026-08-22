"""Unit tests for Capstone Chroma metadata helpers."""

from pathlib import Path

from src.chunking import SOURCE_HANDBOOK, SOURCE_WEBSITE
from src.vectorstore import chunk_to_metadata, search_chunks, store_chunks


def test_handbook_metadata_keeps_page():
    meta = chunk_to_metadata(
        {"source": SOURCE_HANDBOOK, "page": 18, "url": ""}
    )
    assert meta["source"] == SOURCE_HANDBOOK
    assert meta["page"] == 18
    assert meta["url"] == ""


def test_website_metadata_uses_url_and_zero_page():
    meta = chunk_to_metadata(
        {
            "source": SOURCE_WEBSITE,
            "page": None,
            "url": "https://www.zaio.io/bootcamps",
        }
    )
    assert meta["source"] == SOURCE_WEBSITE
    assert meta["page"] == 0
    assert meta["url"] == "https://www.zaio.io/bootcamps"


def test_store_and_search_roundtrip_keeps_dual_metadata(tmp_path: Path):
    chunks = [
        {
            "chunk_id": "handbook_p7_c0",
            "text": "Orientation Day is on 15 January 2026 at 10 am.",
            "source": SOURCE_HANDBOOK,
            "page": 7,
            "url": "",
        },
        {
            "chunk_id": "website_bootcamps_c0",
            "text": "ZAIO offers Full Stack AI Engineer and Data Science bootcamps.",
            "source": SOURCE_WEBSITE,
            "page": None,
            "url": "https://www.zaio.io/bootcamps",
        },
    ]
    # Tiny fake embeddings that still allow nearest-neighbour search.
    embeddings = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
    ]
    stored = store_chunks(chunks, embeddings, db_dir=tmp_path)
    assert stored == 2

    handbook_hits = search_chunks([1.0, 0.0, 0.0], n_results=1, db_dir=tmp_path)
    assert handbook_hits[0]["source"] == SOURCE_HANDBOOK
    assert handbook_hits[0]["page"] == 7

    website_hits = search_chunks([0.0, 1.0, 0.0], n_results=1, db_dir=tmp_path)
    assert website_hits[0]["source"] == SOURCE_WEBSITE
    assert website_hits[0]["url"] == "https://www.zaio.io/bootcamps"
    assert website_hits[0]["page"] is None
