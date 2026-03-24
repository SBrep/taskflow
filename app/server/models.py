from pydantic import BaseModel

class Task(BaseModel):
    id: int
    title: str
    status: str = "new"

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    status: str