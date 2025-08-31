# app/core/database.py
from __future__ import annotations
import os
import sqlite3
from pathlib import Path
from typing import Iterable, List, Dict, Any

APP_NAME = "CV Manager"

DATABASE_BASE_DIR = Path(
    os.getenv("CVM_DB_DIR", "/Users/umang/Projects/CV-Manager")
).expanduser()
ARCHIVE_ROOT_DIR = Path(
    os.getenv("CVM_ARCHIVE_DIR", "/Users/umang/Documents/Resumes")
).expanduser()

def db_path() -> Path:
    """
    Full path to the SQLite database file, kept alongside the code.
    Ensures the parent directory exists.
    """
    DATABASE_BASE_DIR.mkdir(parents=True, exist_ok=True)
    return DATABASE_BASE_DIR / "app.db"

def archive_root() -> Path:
    """
    Root directory where archived PDFs live.
    """
    base = ARCHIVE_ROOT_DIR / APP_NAME if ARCHIVE_ROOT_DIR.name != APP_NAME else ARCHIVE_ROOT_DIR
    base.mkdir(parents=True, exist_ok=True)
    return base

def _connect() -> sqlite3.Connection:
    """
    Opens a connection with safe defaults.
    """
    conn = sqlite3.connect(db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

SCHEMA_STATEMENTS: Iterable[str] = [
    """
    CREATE TABLE IF NOT EXISTS applications (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        company      TEXT NOT NULL,
        role         TEXT,
        date_applied TEXT NOT NULL,     -- ISO format YYYY-MM-DD
        notes        TEXT,
        file_path    TEXT NOT NULL,     -- absolute path to archived PDF
        created_at   TEXT DEFAULT (datetime('now'))
    );
    """,
    "CREATE INDEX IF NOT EXISTS idx_company_role ON applications(company, role);",
    "CREATE INDEX IF NOT EXISTS idx_date_applied ON applications(date_applied);",
]

def init_db() -> Path:
    """
    Ensures the database file and schema exist. Returns the DB path.
    Call this once on app startup.
    """
    p = db_path()
    with _connect() as conn:
        for stmt in SCHEMA_STATEMENTS:
            conn.execute(stmt)
        conn.commit()
    # Also ensure archive root exists early, so later code can rely on it.
    _ = archive_root()
    return p

def insert_application(
    company: str,
    role: str,
    date_applied: str,   # "YYYY-MM-DD"
    notes: str,
    file_path: str,      # absolute path to the archived PDF
) -> int:
    """
    Inserts a row and returns the new application id.
    """
    with _connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO applications (company, role, date_applied, notes, file_path)
            VALUES (?, ?, ?, ?, ?);
            """,
            (company, role, date_applied, notes, file_path),
        )
        conn.commit()
        return int(cur.lastrowid)

# Whitelist allowed ORDER BYs to avoid SQL injection if this ever becomes user-controlled.
_ALLOWED_ORDER_BYS = {
    "date_applied DESC, id DESC",
    "date_applied ASC, id ASC",
    "company ASC, date_applied DESC",
    "company DESC, date_applied DESC",
    "created_at DESC",
}

def fetch_all_applications(order_by: str = "date_applied DESC, id DESC") -> List[Dict[str, Any]]:
    """
    Returns all applications as a list of dicts.
    """
    if order_by not in _ALLOWED_ORDER_BYS:
        order_by = "date_applied DESC, id DESC"
    with _connect() as conn:
        rows = conn.execute(f"SELECT * FROM applications ORDER BY {order_by};").fetchall()
        return [dict(row) for row in rows]
