"""Unit tests for answer generation rules."""

from src.generate import NOT_AVAILABLE, generate_answer


def test_empty_context_returns_not_available():
    answer = generate_answer("What is the fee?", context="")
    assert answer == NOT_AVAILABLE


def test_whitespace_context_returns_not_available():
    answer = generate_answer("What is the fee?", context="   \n  ")
    assert answer == NOT_AVAILABLE
