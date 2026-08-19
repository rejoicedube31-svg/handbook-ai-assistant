"""Unit tests for Chroma metadata mapping."""

from src.chunking import SOURCE_HANDBOOK, SOURCE_WEBSITE
from src.vectorstore import chunk_to_metadata


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
