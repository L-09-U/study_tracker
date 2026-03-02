import sqlite3
import os

DB_PATH = "data/study.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        subject TEXT,
        hours REAL,
        focus INTEGER,
        exercises INTEGER,
        grade REAL
    )
    """)

    conn.commit()
    conn.close()


def add_record(date, subject, hours, focus, exercises, grade):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO study_records (date, subject, hours, focus, exercises, grade)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (date, subject, hours, focus, exercises, grade))

    conn.commit()
    conn.close()


def get_all_records():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM study_records")
    rows = cursor.fetchall()

    conn.close()
    return rows