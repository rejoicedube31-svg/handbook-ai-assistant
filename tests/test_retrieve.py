"""Unit tests for Capstone source formatting and retrieval helpers."""

from src.chunking import SOURCE_HANDBOOK, SOURCE_WEBSITE
from src.retrieve import (
    _merge_by_best_distance,
    best_source,
    format_context,
    format_source_label,
    retrieve,
)


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


def test_best_source_empty():
    assert best_source([]) is None


def test_merge_keeps_best_distance_per_chunk_id():
    matches = [
        {"chunk_id": "a", "distance": 0.5, "text": "first"},
        {"chunk_id": "a", "distance": 0.2, "text": "better"},
        {"chunk_id": "b", "distance": 0.3, "text": "other"},
    ]
    merged = _merge_by_best_distance(matches)
    assert [item["chunk_id"] for item in merged] == ["a", "b"]
    assert merged[0]["text"] == "better"
    assert merged[0]["distance"] == 0.2


def test_retrieve_course_question_runs_boost_search(monkeypatch):
    calls: list[str] = []

    def fake_embed(text: str):
        calls.append(text)
        return [0.1, 0.2, 0.3]

    def fake_search(_embedding, n_results: int = 4):
        return [
            {
                "chunk_id": f"id-{n_results}",
                "text": "Full Stack AI Engineer bootcamp",
                "source": SOURCE_WEBSITE,
                "page": None,
                "url": "https://www.zaio.io/bootcamps",
                "distance": 0.3,
            }
        ]

    monkeypatch.setattr("src.retrieve.embed_query", fake_embed)
    monkeypatch.setattr("src.retrieve.search_chunks", fake_search)

    results = retrieve("What courses does ZAIO offer?", n_results=4)
    assert len(results) >= 1
    assert len(calls) == 2  # main question + course boost query
    assert "bootcamps" in calls[1].lower()
