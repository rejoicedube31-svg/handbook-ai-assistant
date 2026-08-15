"""Website crawler stub (implemented on Capstone Day 2).

Day 1 only defines the crawl scope in web_config.py.
Day 2 will fetch each seed URL and return {url, title, text}.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.web_config import SEED_URLS


def crawl_zaio_pages(urls: list[str] | None = None) -> list[dict]:
    """Fetch and extract text from ZAIO pages.

    Returns a list of:
    {"url": str, "title": str, "text": str}
    """
    targets = urls or SEED_URLS
    raise NotImplementedError(
        f"Capstone Day 2: crawl {len(targets)} ZAIO seed URLs "
        "(see src/web_config.py)."
    )


if __name__ == "__main__":
    print(f"Seed URLs ready: {len(SEED_URLS)}")
    for url in SEED_URLS:
        print(f" - {url}")
    print("Run Capstone Day 2 to implement crawling.")
