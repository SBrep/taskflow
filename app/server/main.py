from fastapi import FastAPI
from contextlib import asynccontextmanager

from .routes import router
from .database import init_db
from . import state


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    print("Taskflow service started")
    yield
    # Shutdown
    state.is_shutting_down = True
    print("Shutting down... waiting for active requests to finish")
    while state.active_requests > 0:
        await asyncio.sleep(0.1)  # небольшой асинхронный sleep
    print("Taskflow service stopped gracefully")


app = FastAPI(lifespan=lifespan, title="Taskflow")

app.include_router(router)