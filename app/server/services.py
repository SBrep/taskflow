from typing import Dict
from .models import Task

tasks: Dict[int, Task] = {}
task_id_counter = 1

def add_task(title: str) -> Task:
    global task_id_counter
    task = Task(id=task_id_counter, title=title)
    tasks[task_id_counter] = task
    task_id_counter += 1
    return task

def get_tasks():
    return list(tasks.values())

def get_task(task_id: int) -> Task:
    return tasks.get(task_id)

def update_task(task_id: int, status: str) -> Task:
    task = tasks.get(task_id)
    if task:
        task.status = status
    return task

def delete_task(task_id: int):
    if task_id in tasks:
        del tasks[task_id]
        return True
    return False