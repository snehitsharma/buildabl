from fastapi.testclient import TestClient
from fastapi import Request

import app as app_module


async def allow_request(request: Request):
    return None


def test_health_endpoint():
    client = TestClient(app_module.app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_endpoint_rejects_missing_query():
    app_module.app.dependency_overrides[app_module.rate_limit] = allow_request

    try:
        client = TestClient(app_module.app)
        response = client.post("/chat", json={})
    finally:
        app_module.app.dependency_overrides.clear()

    assert response.status_code == 422


def test_chat_endpoint_returns_generated_response(monkeypatch):
    async def fake_get_cached_response(query):
        return None

    async def fake_set_cached_response(query, response):
        return None

    class FakeGraph:
        def invoke(self, state):
            assert state == {"query": "Hello"}
            return {"response": "Hi there"}

    monkeypatch.setattr(app_module, "get_cached_response", fake_get_cached_response)
    monkeypatch.setattr(app_module, "set_cached_response", fake_set_cached_response)
    monkeypatch.setattr(app_module, "graph", FakeGraph())
    app_module.app.dependency_overrides[app_module.rate_limit] = allow_request

    try:
        client = TestClient(app_module.app)
        response = client.post("/chat", json={"query": "Hello"})
    finally:
        app_module.app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {"response": "Hi there"}
