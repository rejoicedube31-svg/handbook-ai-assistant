"""Load a PDF and extract text per page.

Why page-level extraction?
The API must return something like "source": "Page 12".
If we throw away page numbers now, we cannot cite sources later.
"""

from pathlib import Path

from pypdf import PdfReader

from src.text_cleanup import normalize_pdf_text


def load_pages(pdf_path: str | Path) -> list[dict]:
    """Return a list of {page, text} for every page in the PDF.

    page is 1-based (matches how humans read handbooks).
    """
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(
            f"PDF not found: {path}\n"
            "Put your handbook in data/handbook.pdf and try again."
        )

    reader = PdfReader(str(path))
    pages: list[dict] = []

    for index, page in enumerate(reader.pages):
        raw = page.extract_text() or ""
        text = normalize_pdf_text(raw)
        pages.append(
            {
                "page": index + 1,
                "text": text.strip(),
            }
        )

    return pages
