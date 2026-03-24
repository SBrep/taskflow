from fastapi import FastAPI
from .routes import router

app = FastAPI(title="Taskflow Service")
app.include_router(router)