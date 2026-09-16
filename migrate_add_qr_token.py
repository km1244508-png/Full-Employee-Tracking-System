"""
migrate_add_qr_token.py
-------------------------
Run this ONCE to add the missing `qr_token` column to an existing
attendance.db (SQLite) without deleting any existing data.

Usage (from the project's root folder, same place as app.py):
    python migrate_add_qr_token.py
"""

import sqlite3
import os

DB_PATH = "attendance.db"

if not os.path.exists(DB_PATH):
    print(f"'{DB_PATH}' not found in this folder. Run this script from your project root.")
    raise SystemExit(1)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("PRAGMA table_info(employees)")
columns = [row[1] for row in cur.fetchall()]

if "qr_token" in columns:
    print("qr_token column already exists — nothing to do.")
else:
    cur.execute("ALTER TABLE employees ADD COLUMN qr_token VARCHAR(64)")
    conn.commit()
    print("Done — qr_token column added. Your existing employees and data are untouched.")

conn.close()