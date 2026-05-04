import sqlite3
import os

DB_PATH = os.path.join("data", "tasks.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

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