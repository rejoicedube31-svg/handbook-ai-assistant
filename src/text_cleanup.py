"""Fix common PDF extraction quirks.

This handbook extracts like:
  "W e  w i l l  h a v e"  → should become "We will have"

Rule for this PDF:
- single spaces separate letters inside a word
- double spaces / newlines separate words
"""

from __future__ import annotations

import re

_WORD_BREAK = "<|>"


def normalize_pdf_text(text: str) -> str:
    """Collapse character-spaced PDF text while keeping real word breaks."""
    if not text or not text.strip():
        return ""

    # Treat newlines as word breaks.
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").replace("\n", _WORD_BREAK)

    # Double (or more) spaces are word breaks in this handbook PDF.
    normalized = re.sub(r" {2,}", _WORD_BREAK, normalized)

    # Detect character-spaced pages: most tokens are single characters.
    probe = [token for token in normalized.replace(_WORD_BREAK, " ").split(" ") if token]
    if not probe:
        return ""

    single_ratio = sum(1 for token in probe if len(token) == 1) / len(probe)
    if single_ratio < 0.5:
        return re.sub(r"\s+", " ", text).strip()

    # Remove the remaining single spaces (letter separators), restore words.
    normalized = normalized.replace(" ", "")
    normalized = normalized.replace(_WORD_BREAK, " ")
    return re.sub(r" +", " ", normalized).strip()
