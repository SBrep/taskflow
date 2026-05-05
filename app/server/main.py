import logging
import time
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from .routes import router
from .database import init_db
from . import state

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%H:%M:%S"
)

logger = logging.getLogger("taskflow")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    logger.info("Taskflow service started")
    yield
    state.is_shutting_down = True
    logger.info("Shutting down... waiting for active requests")
    while state.active_requests > 0:
        await asyncio.sleep(0.1)
    logger.info("Taskflow service stopped gracefully")


app = FastAPI(lifespan=lifespan, title="Taskflow")


# Middleware для логирования запросов и latency (ЛР 6)
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    status_code = 200  # значение по умолчанию
    
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
        
    except Exception as e:
        status_code = 500
        logger.error(f"Request failed: {request.method} {request.url.path}", exc_info=True)
        raise
        
    finally:
        process_time = (time.time() - start_time) * 1000
        
        # Улучшенное логирование и подсчёт ошибок
        if status_code >= 500:
            log_level = logging.ERROR
            with state.lock:
                state.total_errors += 1
        elif status_code >= 400:
            log_level = logging.WARNING # Клиентские ошибки помечаю предупреждением (400, 422...)
        else:
            log_level = logging.INFO

        logger.log(
            log_level,
            f"{request.method} {request.url.path} | "
            f"status={status_code} | "
            f"latency={process_time:.2f}ms"
        )


app.include_router(router)