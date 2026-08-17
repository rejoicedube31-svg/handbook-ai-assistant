"""Unit tests for website HTML cleaning."""

from src.web_cleaner import clean_html_to_text, clean_visible_text


SAMPLE_HTML = """
<html>
  <head><title>Full Stack AI Engineer | Zaio</title></head>
  <body>
    <header><nav>Bootcamps Qualifications Community</nav></header>
    <main>
      <h1>Full Stack AI Engineer</h1>
      <p>Build agentic web applications using LLMs, Langchain, N8N, and more.</p>
      <p>Beginner. 7 Months.</p>
    </main>
    <footer>Made with in South Africa 2026 Zaio Technology Contact us</footer>
  </body>
</html>
"""


def test_clean_html_keeps_main_content():
    title, text = clean_html_to_text(SAMPLE_HTML)
    assert title == "Full Stack AI Engineer | Zaio"
    assert "Build agentic web applications" in text
    assert "Bootcamps Qualifications Community" not in text
    assert "Contact us" not in text


def test_clean_visible_text_strips_newsletter_chrome():
    noisy = (
        "The Weekly Commit Newsletter - two useful minutes in your inbox every Thursday. "
        "Subscribe free Launch Your Tech Career"
    )
    cleaned = clean_visible_text(noisy)
    assert "Weekly Commit" not in cleaned
    assert "Launch Your Tech Career" in cleaned
