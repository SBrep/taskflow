from fastapi import APIRouter, HTTPException
from .models import TaskCreate, TaskUpdate
from .services import add_task, get_tasks, get_task, update_task, delete_task

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/tasks")
def list_tasks():
    return get_tasks()

@router.post("/tasks")
def create_task(task: TaskCreate):
    return add_task(task.title)

@router.get("/tasks/{task_id}")
def read_task(task_id: int):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/tasks/{task_id}")
def modify_task(task_id: int, update: TaskUpdate):
    task = update_task(task_id, update.status)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/tasks/{task_id}")
def remove_task(task_id: int):
    if delete_task(task_id):
        return {"message": "deleted"}
    raise HTTPException(status_code=404, detail="Task not found")