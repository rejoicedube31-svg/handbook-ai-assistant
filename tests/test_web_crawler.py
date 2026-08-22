"""Unit tests for website crawl helpers (no live network)."""

import json
from pathlib import Path

from src.web_crawler import save_pages, should_skip
from src.web_config import SEED_URLS


def test_should_skip_login_and_external_apps():
    assert should_skip("https://www.zaio.io/app/login") is True
    assert should_skip("https://applications.zaio.io/book-consultation") is True
    assert should_skip("mailto:hello@zaio.io") is True
    assert should_skip("https://www.trustpilot.com/review/zaio.io") is True


def test_should_not_skip_public_zaio_pages():
    assert should_skip("https://www.zaio.io/") is False
    assert should_skip("https://www.zaio.io/bootcamps") is False


def test_seed_urls_are_public_zaio_pages():
    assert len(SEED_URLS) >= 10
    assert all(url.startswith("https://www.zaio.io") for url in SEED_URLS)
    assert all(not should_skip(url) for url in SEED_URLS)


def test_save_pages_writes_json(tmp_path: Path):
    output = tmp_path / "pages.json"
    pages = [
        {
            "url": "https://www.zaio.io/",
            "title": "Zaio",
            "text": "Launch your tech career",
            "char_count": 24,
        }
    ]
    path = save_pages(pages, output)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded[0]["url"] == "https://www.zaio.io/"
    assert loaded[0]["text"] == "Launch your tech career"
