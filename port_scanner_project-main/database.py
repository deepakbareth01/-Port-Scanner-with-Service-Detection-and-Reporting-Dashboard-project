import sqlite3
import json
from datetime import datetime

DB_NAME = "scans.db"



def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT,
            scan_time TEXT,
            results TEXT
        )
        """
    )
    conn.commit()
    conn.close()



def save_scan(target, results):
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        "INSERT INTO scans (target, scan_time, results) VALUES (?, ?, ?)",
        (
            target,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            json.dumps(results),
        ),
    )
    conn.commit()
    conn.close()



def get_all_scans():
    conn = sqlite3.connect(DB_NAME)
    rows = conn.execute(
        "SELECT id, target, scan_time FROM scans ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return rows
