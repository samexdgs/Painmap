"""Database layer — SQLite for free, persistent local storage on Streamlit Cloud."""

import sqlite3
import os
from datetime import datetime, timedelta
from contextlib import contextmanager
from pathlib import Path

DB_PATH = os.environ.get("PAINMAP_DB", "painmap.db")


@contextmanager
def conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    try:
        yield c
        c.commit()
    finally:
        c.close()


def init_db():
    Path(DB_PATH).touch(exist_ok=True)
    with conn() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            primary_condition TEXT NOT NULL,
            gender TEXT,
            age INTEGER,
            city TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS pain_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            region TEXT NOT NULL,
            pain_type TEXT NOT NULL,
            intensity INTEGER NOT NULL,
            quality TEXT,
            trigger TEXT,
            duration_min INTEGER,
            note TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            label TEXT NOT NULL,
            time_of_day TEXT NOT NULL,
            frequency TEXT NOT NULL,
            email_alert INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_logs_user ON pain_logs(user_id);
        CREATE INDEX IF NOT EXISTS idx_logs_ts ON pain_logs(timestamp);
        """)


def insert_user(username, email, password_hash, salt, primary_condition,
                 gender, age, city):
    with conn() as c:
        try:
            cur = c.execute(
                "INSERT INTO users (username,email,password_hash,salt,"
                "primary_condition,gender,age,city) VALUES (?,?,?,?,?,?,?,?)",
                (username, email, password_hash, salt, primary_condition,
                 gender, age, city),
            )
            return cur.lastrowid
        except sqlite3.IntegrityError as e:
            if "username" in str(e):
                return None, "username_taken"
            if "email" in str(e):
                return None, "email_taken"
            return None, "unknown_error"


def get_user_by_login(username_or_email):
    with conn() as c:
        row = c.execute(
            "SELECT * FROM users WHERE username=? OR email=?",
            (username_or_email, username_or_email)
        ).fetchone()
        return dict(row) if row else None


def get_user_by_id(user_id):
    with conn() as c:
        row = c.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
        return dict(row) if row else None


def update_user(user_id, **fields):
    if not fields:
        return
    cols = ", ".join(f"{k}=?" for k in fields)
    vals = list(fields.values()) + [user_id]
    with conn() as c:
        c.execute(f"UPDATE users SET {cols} WHERE id=?", vals)


def update_password(user_id, password_hash, salt):
    with conn() as c:
        c.execute("UPDATE users SET password_hash=?, salt=? WHERE id=?",
                   (password_hash, salt, user_id))


def delete_user(user_id):
    with conn() as c:
        c.execute("DELETE FROM users WHERE id=?", (user_id,))


def insert_pain_log(user_id, region, pain_type, intensity, quality,
                     trigger, duration_min, note):
    with conn() as c:
        c.execute(
            "INSERT INTO pain_logs (user_id,region,pain_type,intensity,"
            "quality,trigger,duration_min,note) VALUES (?,?,?,?,?,?,?,?)",
            (user_id, region, pain_type, intensity, quality, trigger,
             duration_min, note),
        )


def get_user_logs(user_id, limit=None, days=None):
    with conn() as c:
        q = "SELECT * FROM pain_logs WHERE user_id=?"
        params = [user_id]
        if days:
            cutoff = (datetime.now() - timedelta(days=days)).isoformat()
            q += " AND timestamp >= ?"
            params.append(cutoff)
        q += " ORDER BY timestamp DESC"
        if limit:
            q += f" LIMIT {int(limit)}"
        rows = c.execute(q, params).fetchall()
        return [dict(r) for r in rows]


def insert_reminder(user_id, label, time_of_day, frequency, email_alert):
    with conn() as c:
        c.execute(
            "INSERT INTO reminders (user_id,label,time_of_day,frequency,email_alert)"
            " VALUES (?,?,?,?,?)",
            (user_id, label, time_of_day, frequency, int(bool(email_alert))),
        )


def get_reminders(user_id):
    with conn() as c:
        rows = c.execute(
            "SELECT * FROM reminders WHERE user_id=? ORDER BY time_of_day",
            (user_id,)
        ).fetchall()
        return [dict(r) for r in rows]


def delete_reminder(reminder_id):
    with conn() as c:
        c.execute("DELETE FROM reminders WHERE id=?", (reminder_id,))
