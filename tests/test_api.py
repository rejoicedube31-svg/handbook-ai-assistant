"""Unit tests for the Capstone FastAPI /ask endpoint."""

from fastapi.testclient import TestClient

from src.api import app
from src.generate import NOT_AVAILABLE

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "Student Handbook" in body["sources"]
    assert "ZAIO Website" in body["sources"]


def test_ask_handbook_source(monkeypatch):
    monkeypatch.setattr(
        "src.api.ask",
        lambda _q: {
            "answer": "Orientation Day is on 15 January 2026 at 10 am.",
            "source": "Student Handbook - Page 7",
            "chunks_used": 2,
        },
    )
    response = client.post("/ask", json={"question": "When is orientation day?"})
    assert response.status_code == 200
    body = response.json()
    assert body["answer"].startswith("Orientation Day")
    assert body["source"] == "Student Handbook - Page 7"


def test_ask_website_source(monkeypatch):
    monkeypatch.setattr(
        "src.api.ask",
        lambda _q: {
            "answer": "ZAIO offers Full Stack AI Engineer and other bootcamps.",
            "source": "https://www.zaio.io/bootcamps",
            "chunks_used": 4,
        },
    )
    response = client.post(
        "/ask", json={"question": "What courses does ZAIO offer?"}
    )
    assert response.status_code == 200
    body = response.json()
    assert "bootcamp" in body["answer"].lower() or "Full Stack" in body["answer"]
    assert body["source"] == "https://www.zaio.io/bootcamps"


def test_ask_not_found_returns_null_source(monkeypatch):
    monkeypatch.setattr(
        "src.api.ask",
        lambda _q: {
            "answer": NOT_AVAILABLE,
            "source": None,
            "chunks_used": 0,
        },
    )
    response = client.post(
        "/ask", json={"question": "What is the cafeteria pizza topping?"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == NOT_AVAILABLE
    assert body["source"] is None


def test_ask_rejects_missing_question():
    response = client.post("/ask", json={})
    assert response.status_code == 400
    assert "error" in response.json()


def test_ask_rejects_empty_question():
    response = client.post("/ask", json={"question": "   "})
    assert response.status_code == 400
    assert "error" in response.json()


def test_ask_rejects_non_json():
    response = client.post(
        "/ask",
        content="question=hello",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 400
    assert "error" in response.json()
