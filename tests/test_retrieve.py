"""Unit tests for Capstone source formatting and retrieval helpers."""

from src.chunking import SOURCE_HANDBOOK, SOURCE_WEBSITE
from src.retrieve import best_source, format_context, format_source_label


def test_handbook_source_label():
    label = format_source_label(
        {"source": SOURCE_HANDBOOK, "page": 18, "url": ""}
    )
    assert label == "Student Handbook - Page 18"


def test_website_source_label():
    label = format_source_label(
        {
            "source": SOURCE_WEBSITE,
            "page": None,
            "url": "https://www.zaio.io/bootcamps",
        }
    )
    assert label == "https://www.zaio.io/bootcamps"


def test_format_context_includes_both_labels():
    chunks = [
        {
            "source": SOURCE_HANDBOOK,
            "page": 7,
            "url": "",
            "text": "Orientation Day is 15 January 2026.",
        },
        {
            "source": SOURCE_WEBSITE,
            "page": None,
            "url": "https://www.zaio.io/",
            "text": "ZAIO offers Full Stack AI Engineer.",
        },
    ]
    context = format_context(chunks)
    assert "[Student Handbook - Page 7]" in context
    assert "[https://www.zaio.io/]" in context


def test_best_source_uses_top_chunk():
    chunks = [
        {
            "source": SOURCE_WEBSITE,
            "page": None,
            "url": "https://www.zaio.io/bootcamps",
            "text": "Courses...",
        }
    ]
    assert best_source(chunks) == "https://www.zaio.io/bootcamps"
