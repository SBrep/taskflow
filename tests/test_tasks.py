import os
os.environ["TEST_MODE"] = "1"

from fastapi.testclient import TestClient
from app.server.main import app
from app.server.database import init_db
from app.server import state

init_db()

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task():
    response = client.post("/tasks", json={"title": "test"})
    assert response.status_code == 200
    assert response.json()["title"] == "test"


def test_get_tasks():
    client.post("/tasks", json={"title": "task1"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_task():
    response = client.post("/tasks", json={"title": "task"})
    task_id = response.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"status": "done"})
    assert response.json()["status"] == "done"


def test_delete_task():
    response = client.post("/tasks", json={"title": "task"})
    task_id = response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200


# -------------------------
# ЛР3 ТЕСТЫ
# -------------------------

def test_shutdown_blocks_requests():
    state.is_shutting_down = True

    response = client.post("/tasks", json={"title": "blocked"})
    assert response.status_code == 503

    state.is_shutting_down = False


def test_active_requests_counter():
    before = state.active_requests

    response = client.get("/tasks")
    assert response.status_code == 200

    after = state.active_requests
    assert after == before