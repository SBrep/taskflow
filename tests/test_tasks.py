import os
os.environ["TEST_MODE"] = "1"

import asyncio
from fastapi.testclient import TestClient
from app.server.main import app
from app.server.database import init_db
from app.server import state, external_api

init_db()
client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_crud_operations():
    # Create
    resp = client.post("/tasks", json={"title": "Test task"})
    assert resp.status_code == 200
    task_id = resp.json()["id"]

    # Get all
    resp = client.get("/tasks")
    assert resp.status_code == 200
    assert len(resp.json()) > 0

    # Update
    resp = client.patch(f"/tasks/{task_id}", json={"status": "done"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "done"

    # Delete
    resp = client.delete(f"/tasks/{task_id}")
    assert resp.status_code == 200


def test_shutdown_blocks_requests():
    state.is_shutting_down = True
    resp = client.post("/tasks", json={"title": "blocked"})
    assert resp.status_code == 503
    state.is_shutting_down = False


# ЛР4 тесты
def test_external_success(monkeypatch):
    monkeypatch.setattr(external_api, "unstable_service", lambda: "OK")
    resp = client.get("/external")
    assert resp.status_code == 200
    assert resp.json()["status"] == "success"


def test_external_with_retry(monkeypatch):
    calls = []
    def flaky():
        calls.append(1)
        if len(calls) < 2:
            raise Exception("fail")
        return "OK after retry"

    monkeypatch.setattr(external_api, "unstable_service", flaky)
    resp = client.get("/external")
    assert resp.status_code == 200
    assert resp.json()["status"] == "success"