"""API-тесты без сети: TestClient."""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())


def test_health(client: TestClient) -> None:
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_videos(client: TestClient) -> None:
    resp = client.get("/api/v1/videos?q=vector")
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    assert client.get("/api/v1/videos/ghost").status_code == 404


def test_ask(client: TestClient) -> None:
    resp = client.post("/api/v1/ask", json={"question": "How to build the index?"})
    assert resp.status_code == 200
    assert len(resp.json()["segments"]) == 1


def test_ask_rejects_empty(client: TestClient) -> None:
    resp = client.post("/api/v1/ask", json={"question": "   "})
    assert resp.status_code == 422


@pytest.mark.integration()
def test_ask_compose_shape(client: TestClient) -> None:
    """Интеграционный по маркеру: docker-видео, без сети."""
    resp = client.post("/api/v1/ask", json={"question": "compose up builds the stack"})
    assert resp.status_code == 200
    assert resp.json()["segments"][0]["stamp"] == "00:45"
