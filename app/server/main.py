from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# In-memory storage
tasks: Dict[int, dict] = {}
task_id_counter = 1


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    status: str


@app.get("/health")
def health():
    return "OK"


@app.post("/tasks")
def create_task(task: TaskCreate):
    global task_id_counter

    new_task = {
        "id": task_id_counter,
        "title": task.title,
        "status": "new"
    }

    tasks[task_id_counter] = new_task
    task_id_counter += 1

    return new_task


@app.get("/tasks")
def get_tasks():
    return list(tasks.values())


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]


@app.patch("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    tasks[task_id]["status"] = update.status
    return tasks[task_id]


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    del tasks[task_id]
    return {"message": "deleted"}