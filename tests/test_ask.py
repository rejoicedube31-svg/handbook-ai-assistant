"""Unit tests for the ask() orchestration helper."""

from src.ask import ask
from src.generate import NOT_AVAILABLE


def test_ask_returns_source_for_known_answer(monkeypatch):
    monkeypatch.setattr(
        "src.ask.retrieve",
        lambda _q: [{"text": "Live classes are on Tuesday.", "page": 11, "distance": 0.2}],
    )
    monkeypatch.setattr(
        "src.ask.generate_answer",
        lambda _q, _c: "Live classes are on Tuesday.",
    )

    result = ask("When are the live classes?")
    assert result["answer"] == "Live classes are on Tuesday."
    assert result["source"] == "Page 11"
    assert result["chunks_used"] == 1


def test_ask_clears_source_when_not_available(monkeypatch):
    monkeypatch.setattr(
        "src.ask.retrieve",
        lambda _q: [{"text": "Unrelated handbook text.", "page": 3, "distance": 0.4}],
    )
    monkeypatch.setattr(
        "src.ask.generate_answer",
        lambda _q, _c: NOT_AVAILABLE,
    )

    result = ask("What is the cafeteria pizza topping?")
    assert result["answer"] == NOT_AVAILABLE
    assert result["source"] is None
    assert result["chunks_used"] == 1
