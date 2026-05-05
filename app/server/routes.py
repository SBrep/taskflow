from fastapi import APIRouter, HTTPException
from .models import TaskCreate, TaskUpdate
from .services import (
    add_task, get_tasks, get_task,
    update_task, delete_task, call_external_with_retry, get_stats
)
from . import state
from functools import wraps

router = APIRouter()


def track_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if state.is_shutting_down:
            raise HTTPException(status_code=503, detail="Service is shutting down")
        
        state.active_requests += 1
        try:
            return func(*args, **kwargs)
        finally:
            state.active_requests -= 1
    return wrapper


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/stats")
def stats():
    return get_stats()


@router.get("/metrics")
def metrics():
    return get_stats()


@router.get("/tasks")
@track_request
def list_tasks():
    return get_tasks()


@router.post("/tasks")
@track_request
def create_task(task: TaskCreate):
    return add_task(task.title)


@router.get("/tasks/{task_id}")
@track_request
def read_task(task_id: int):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/tasks/{task_id}")
@track_request
def modify_task(task_id: int, update: TaskUpdate):
    task = update_task(task_id, update.status)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/tasks/{task_id}")
@track_request
def remove_task(task_id: int):
    if delete_task(task_id):
        return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")


@router.get("/external")
@track_request
def call_external():
    try:
        result = call_external_with_retry()
        return {"status": "success", "result": result}
    except Exception:
        return {"status": "failed"}