"""Clean crawled ZAIO website HTML/text (Capstone Day 3).

Why clean?
Nav menus, headers, and footers repeat on every page and hurt retrieval.
We keep the main page content that actually answers student questions.
"""

from __future__ import annotations

import re

from bs4 import BeautifulSoup

# Repeated chrome that often still leaks into main text.
NOISE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(
        r"Bootcamps All Bootcamps Full Stack AI Engineer Cloud & DevOps Engineer "
        r"Full Stack Web Development Data Science Cybersecurity Digital Marketing "
        r"Compare Courses Qualifications All Qualifications.*?(?=Launch Your Tech Career|"
        r"Courses Designed|Full Stack AI Engineer|Compare|Tuition|About|Frequently Asked|"
        r"Success Stories|Find the right|Our Graduates|Join our community|Are you an enterprise|"
        r"Do I need|Occupational|Beginner|7 Months|6 Months|9 Weeks)",
        re.IGNORECASE,
    ),
    re.compile(
        r"Made with in South Africa.*?Zaio Technology(?:\s+Learn Full Stack.*)?$",
        re.IGNORECASE,
    ),
    re.compile(
        r"The Weekly Commit Newsletter - two useful minutes in your inbox every Thursday\. "
        r"Subscribe free\s*",
        re.IGNORECASE,
    ),
)


def extract_main_html(soup: BeautifulSoup) -> BeautifulSoup:
    """Prefer <main>; otherwise strip header/footer/nav from a copy of the doc."""
    main = soup.find("main")
    if main is not None:
        return main

    for tag in soup(["header", "footer", "nav", "aside"]):
        tag.decompose()
    return soup.body or soup


def clean_html_to_text(html: str) -> tuple[str, str]:
    """Return (title, cleaned_text) from raw HTML."""
    soup = BeautifulSoup(html, "html.parser")

    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()

    for tag in soup(["script", "style", "noscript", "svg", "iframe"]):
        tag.decompose()

    content_root = extract_main_html(soup)
    text = content_root.get_text(separator=" ", strip=True)
    text = clean_visible_text(text)
    return title, text


def clean_visible_text(text: str) -> str:
    """Normalize whitespace and strip leftover chrome phrases."""
    cleaned = " ".join((text or "").split())
    for pattern in NOISE_PATTERNS:
        cleaned = pattern.sub(" ", cleaned)
    return " ".join(cleaned.split()).strip()
