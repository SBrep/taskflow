import time
from .database import get_db_connection
from .external_api import unstable_service
from . import state
import logging

logger = logging.getLogger(__name__)


def add_task(title: str) -> dict:
    start_time = time.time()
    
    with state.lock:
        state.total_requests += 1
        state.total_tasks_created += 1
    
    try:
        with get_db_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO tasks (title, status) VALUES (?, ?)",
                (title, "new")
            )
            conn.commit()
            task_id = cursor.lastrowid

        logger.info(f"Task created | id={task_id} | title='{title}'")
        return {"id": task_id, "title": title, "status": "new"}
    
    except Exception as e:
        with state.lock:
            state.total_errors += 1
        logger.error(f"Failed to create task '{title}'", exc_info=True)
        raise


def get_stats() -> dict:
    with state.lock:
        error_rate = (state.total_errors / state.total_requests * 100) if state.total_requests > 0 else 0
        return {
            "total_requests": state.total_requests,
            "total_tasks": state.total_tasks_created,
            "active_requests": state.active_requests,
            "total_errors": state.total_errors,
            "error_rate_percent": round(error_rate, 2),
            "is_shutting_down": state.is_shutting_down
        }


def get_tasks() -> list[dict]:
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT id, title, status FROM tasks")
        return [dict(row) for row in cursor.fetchall()]


def get_task(task_id: int) -> dict | None:
    with get_db_connection() as conn:
        row = conn.execute(
            "SELECT id, title, status FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        return dict(row) if row else None


def update_task(task_id: int, status: str) -> dict | None:
    with get_db_connection() as conn:
        cursor = conn.execute(
            "UPDATE tasks SET status = ? WHERE id = ?", (status, task_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return None
        row = conn.execute(
            "SELECT id, title, status FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        return dict(row) if row else None


def delete_task(task_id: int) -> bool:
    with get_db_connection() as conn:
        cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        return cursor.rowcount > 0


def call_external_with_retry(max_retries: int = 3) -> str:
    attempt = 0
    delay = 0.2
    while attempt < max_retries:
        try:
            return unstable_service()
        except Exception:
            attempt += 1
            if attempt == max_retries:
                with state.lock:
                    state.total_errors += 1
                logger.warning(f"External service failed after {max_retries} attempts")
                raise
            time.sleep(delay)
            delay *= 2