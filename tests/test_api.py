"""Unit tests for the FastAPI /ask endpoint (Part 3 + Part 5)."""

from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ask_success(monkeypatch):
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
