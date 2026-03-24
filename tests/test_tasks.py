from fastapi.testclient import TestClient
from app.server.main import app

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