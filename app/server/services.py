import time
from .database import get_connection


def add_task(title: str):
    # имитация долгой операции
    time.sleep(2)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, status) VALUES (?, ?)",
        (title, "new")
    )

    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    return {"id": task_id, "title": title, "status": "new"}


def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, status FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    return [
        {"id": row[0], "title": row[1], "status": row[2]}
        for row in rows
    ]


def get_task(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, status FROM tasks WHERE id = ?",
        (task_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {"id": row[0], "title": row[1], "status": row[2]}


def update_task(task_id: int, status: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status = ? WHERE id = ?",
        (status, task_id)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return None

    cursor.execute(
        "SELECT id, title, status FROM tasks WHERE id = ?",
        (task_id,)
    )

    row = cursor.fetchone()
    conn.close()

    return {"id": row[0], "title": row[1], "status": row[2]}


def delete_task(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()

    return deleted