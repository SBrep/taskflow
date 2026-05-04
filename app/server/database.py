import sqlite3
import os
from contextlib import contextmanager

def get_db_path() -> str:
    test_mode = os.getenv("TEST_MODE", "0") == "1"
    return "data/test_tasks.db" if test_mode else "data/tasks.db"


@contextmanager
def get_db_connection():
    conn = sqlite3.connect(get_db_path())
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row  # чтобы возвращались dict-like объекты
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    os.makedirs("data", exist_ok=True)
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'new'
            )
        """)
        conn.commit()