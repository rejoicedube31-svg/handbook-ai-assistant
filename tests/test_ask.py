"""Unit tests for the ask() orchestration helper."""

from src.ask import ask
from src.chunking import SOURCE_HANDBOOK, SOURCE_WEBSITE
from src.generate import NOT_AVAILABLE


def test_ask_returns_handbook_source(monkeypatch):
    monkeypatch.setattr(
        "src.ask.retrieve",
        lambda _q: [
            {
                "text": "Live classes are on Tuesday.",
                "source": SOURCE_HANDBOOK,
                "page": 11,
                "url": "",
                "distance": 0.2,
            }
        ],
    )
    monkeypatch.setattr(
        "src.ask.generate_answer",
        lambda _q, _c: "Live classes are on Tuesday.",
    )

    result = ask("When are the live classes?")
    assert result["answer"] == "Live classes are on Tuesday."
    assert result["source"] == "Student Handbook - Page 11"
    assert result["chunks_used"] == 1


def test_ask_returns_website_source(monkeypatch):
    monkeypatch.setattr(
        "src.ask.retrieve",
        lambda _q: [
            {
                "text": "ZAIO offers Full Stack AI Engineer.",
                "source": SOURCE_WEBSITE,
                "page": None,
                "url": "https://www.zaio.io/fullstack-ai-engineer-bootcamp",
                "distance": 0.3,
            }
        ],
    )
    monkeypatch.setattr(
        "src.ask.generate_answer",
        lambda _q, _c: "ZAIO offers a Full Stack AI Engineer bootcamp.",
    )

    result = ask("What courses does ZAIO offer?")
    assert "Full Stack AI" in result["answer"]
    assert result["source"] == "https://www.zaio.io/fullstack-ai-engineer-bootcamp"


def test_ask_clears_source_when_not_available(monkeypatch):
    monkeypatch.setattr(
        "src.ask.retrieve",
        lambda _q: [
            {
                "text": "Unrelated text.",
                "source": SOURCE_HANDBOOK,
                "page": 3,
                "url": "",
                "distance": 0.4,
            }
        ],
    )
    monkeypatch.setattr(
        "src.ask.generate_answer",
        lambda _q, _c: NOT_AVAILABLE,
    )

    result = ask("What is the cafeteria pizza topping?")
    assert result["answer"] == NOT_AVAILABLE
    assert result["source"] is None
    assert result["chunks_used"] == 1
