import sqlite3
import os

def get_db_path():
    test_mode = os.getenv("TEST_MODE", "0") == "1"
    return "data/test_tasks.db" if test_mode else "data/tasks.db"


def get_connection():
    return sqlite3.connect(get_db_path())


def init_db():
    os.makedirs("data", exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        status TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()