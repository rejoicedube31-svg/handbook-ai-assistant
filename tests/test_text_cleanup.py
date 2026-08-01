"""Unit tests for PDF text cleanup."""

from src.text_cleanup import normalize_pdf_text


def test_collapses_character_spaced_words():
    raw = "W e  w i l l  h a v e  l i v e  c l a s s e s"
    assert normalize_pdf_text(raw) == "We will have live classes"


def test_uses_newlines_as_word_breaks():
    raw = "W e l c o m e\n0 3 .\nT a b l e  o f  C o n t e n t s"
    cleaned = normalize_pdf_text(raw)
    assert "Welcome" in cleaned
    assert "Table of Contents" in cleaned


def test_empty_input():
    assert normalize_pdf_text("") == ""
    assert normalize_pdf_text("   ") == ""


def test_normal_text_unchanged_aside_from_whitespace():
    raw = "Live classes are on Tuesday."
    assert normalize_pdf_text(raw) == "Live classes are on Tuesday."
