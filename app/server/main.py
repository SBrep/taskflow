from fastapi import FastAPI
from .routes import router
from .database import init_db
from . import state
import time

app = FastAPI()


@app.on_event("startup")
def startup():
    init_db()


@app.on_event("shutdown")
def shutdown():
    state.is_shutting_down = True
    print("Waiting for active requests to finish...")

    while state.active_requests > 0:
        time.sleep(0.1)

    print("Shutdown complete")


app.include_router(router)