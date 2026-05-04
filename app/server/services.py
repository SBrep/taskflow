import time
from .database import get_db_connection
from .external_api import unstable_service


def add_task(title: str) -> dict:
    with get_db_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (title, status) VALUES (?, ?)",
            (title, "new")
        )
        conn.commit()
        task_id = cursor.lastrowid

    return {"id": task_id, "title": title, "status": "new"}


def get_tasks() -> list[dict]:
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT id, title, status FROM tasks")
        return [dict(row) for row in cursor.fetchall()]


def get_task(task_id: int) -> dict | None:
    with get_db_connection() as conn:
        row = conn.execute(
            "SELECT id, title, status FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()
        return dict(row) if row else None


def update_task(task_id: int, status: str) -> dict | None:
    with get_db_connection() as conn:
        cursor = conn.execute(
            "UPDATE tasks SET status = ? WHERE id = ?",
            (status, task_id)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return None

        row = conn.execute(
            "SELECT id, title, status FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()
        return dict(row) if row else None


def delete_task(task_id: int) -> bool:
    with get_db_connection() as conn:
        cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        return cursor.rowcount > 0


# ====================== ЛР 4 ======================
def call_external_with_retry(max_retries: int = 3) -> str:
    attempt = 0
    delay = 0.2

    while attempt < max_retries:
        try:
            return unstable_service()
        except Exception as e:
            attempt += 1
            if attempt == max_retries:
                raise
            time.sleep(delay)
            delay *= 2  # exponential backoff