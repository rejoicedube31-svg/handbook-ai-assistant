"""Crawl ZAIO website pages and extract visible text (Capstone Day 2).

Why crawl?
The Capstone adds https://www.zaio.io as a second knowledge source
alongside the Student Handbook PDF.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import httpx
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.web_config import SEED_URLS, SKIP_PREFIXES

DEFAULT_OUTPUT = ROOT / "data" / "website_raw.json"
USER_AGENT = (
    "Mozilla/5.0 (compatible; ZaioHandbookBot/1.0; "
    "+https://github.com/rejoicedube31-svg/handbook-ai-assistant)"
)


def should_skip(url: str) -> bool:
    """Skip login, external apps, and other noisy URLs."""
    return any(url.startswith(prefix) for prefix in SKIP_PREFIXES)


def extract_text_from_html(html: str) -> tuple[str, str]:
    """Return (title, text) from raw HTML.

    Day 2: basic extract (drop script/style).
    Day 3: deeper clean of nav/header/footer.
    """
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()

    text = soup.get_text(separator=" ", strip=True)
    text = " ".join(text.split())
    return title, text


def fetch_page(client: httpx.Client, url: str) -> dict:
    """Fetch one page and extract title + text."""
    response = client.get(url, follow_redirects=True)
    response.raise_for_status()
    title, text = extract_text_from_html(response.text)
    return {
        "url": str(response.url),
        "title": title,
        "text": text,
        "status_code": response.status_code,
        "char_count": len(text),
    }


def crawl_zaio_pages(
    urls: list[str] | None = None,
    delay_seconds: float = 0.4,
) -> list[dict]:
    """Fetch and extract text from ZAIO seed pages.

    Returns a list of:
    {"url": str, "title": str, "text": str, "status_code": int, "char_count": int}
    """
    targets = [url for url in (urls or SEED_URLS) if not should_skip(url)]
    pages: list[dict] = []

    headers = {"User-Agent": USER_AGENT}
    with httpx.Client(headers=headers, timeout=30.0) as client:
        for index, url in enumerate(targets, start=1):
            try:
                page = fetch_page(client, url)
                pages.append(page)
                print(
                    f"[{index}/{len(targets)}] OK  {page['char_count']:5d} chars  {page['url']}"
                )
            except Exception as exc:  # noqa: BLE001 - report and continue crawl
                print(f"[{index}/{len(targets)}] FAIL {url} -> {exc}")
            if delay_seconds > 0 and index < len(targets):
                time.sleep(delay_seconds)

    return pages


def save_pages(pages: list[dict], output_path: Path = DEFAULT_OUTPUT) -> Path:
    """Save crawled pages as JSON for Day 3+ cleaning/ingest."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(pages, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output_path


def main() -> None:
    print(f"Crawling {len(SEED_URLS)} ZAIO seed URLs...")
    pages = crawl_zaio_pages()
    # Keep pages that actually have extractable text.
    usable = [page for page in pages if page.get("char_count", 0) >= 200]
    path = save_pages(usable)
    print("-" * 60)
    print(f"Fetched {len(pages)} pages; saved {len(usable)} with text -> {path}")
    if usable:
        sample = usable[0]
        preview = sample["text"][:160].encode("ascii", errors="replace").decode("ascii")
        print(f"Sample: {sample['title']}")
        print(f"URL: {sample['url']}")
        print(f"Text: {preview}...")
    print("Capstone Day 2 crawl OK.")


if __name__ == "__main__":
    main()
