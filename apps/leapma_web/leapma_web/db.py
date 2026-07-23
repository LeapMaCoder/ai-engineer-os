"""Minimal persistence for SPEC-GL-001 entities (MySQL or SQLite via DATABASE_URL)."""

from __future__ import annotations

import sqlite3
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterator, Optional
from urllib.parse import urlparse, unquote

_db_url: str = ""
_backend: str = "sqlite"


def init_db(database_url: str) -> None:
    global _db_url, _backend
    _db_url = database_url
    if database_url.startswith("sqlite"):
        _backend = "sqlite"
        path = _sqlite_path(database_url)
        path.parent.mkdir(parents=True, exist_ok=True)
        with _connect() as conn:
            conn.executescript(_SQLITE_DDL)
            conn.commit()
        _ensure_auth_columns()
    elif database_url.startswith("mysql"):
        _backend = "mysql"
        import pymysql

        cfg = _mysql_cfg(database_url)
        # Ensure database exists
        db_name = cfg.pop("database")
        bootstrap = pymysql.connect(**cfg)
        try:
            with bootstrap.cursor() as cur:
                cur.execute(
                    f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
                    "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                )
            bootstrap.commit()
        finally:
            bootstrap.close()
        cfg["database"] = db_name
        with _connect() as conn:
            with conn.cursor() as cur:
                for stmt in _MYSQL_DDL:
                    cur.execute(stmt)
            conn.commit()
        _ensure_auth_columns()
    else:
        raise ValueError(f"Unsupported DATABASE_URL scheme: {database_url}")


def _ensure_auth_columns() -> None:
    """Add optional auth columns on existing installs (CREATE IF NOT EXISTS misses ALTERs)."""
    with _connect() as conn:
        if _backend == "sqlite":
            existing = {
                r[1] for r in conn.execute("PRAGMA table_info(users)").fetchall()
            }
            for name, sqlite_type, _mysql_type in _AUTH_COLUMNS:
                if name not in existing:
                    # SQLite cannot add UNIQUE via ADD COLUMN; enforce in app.
                    plain = sqlite_type.replace(" UNIQUE", "")
                    conn.execute(f"ALTER TABLE users ADD COLUMN {name} {plain}")
            conn.commit()
        else:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                    "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'users'"
                )
                existing = {r["COLUMN_NAME"] for r in cur.fetchall()}
                for name, _sqlite_type, mysql_type in _AUTH_COLUMNS:
                    if name not in existing:
                        cur.execute(f"ALTER TABLE users ADD COLUMN {name} {mysql_type}")
            conn.commit()


def _sqlite_path(url: str) -> Path:
    # sqlite:///C:/path or sqlite:///./relative
    raw = url.replace("sqlite:///", "", 1)
    return Path(raw)


def _mysql_cfg(url: str) -> dict[str, Any]:
    # mysql://user:pass@host:3306/dbname
    u = urlparse(url)
    return {
        "host": u.hostname or "127.0.0.1",
        "port": u.port or 3306,
        "user": unquote(u.username or "root"),
        "password": unquote(u.password or ""),
        "database": (u.path or "/leapma").lstrip("/") or "leapma",
        "charset": "utf8mb4",
        "autocommit": False,
    }


@contextmanager
def _connect() -> Iterator[Any]:
    if _backend == "sqlite":
        conn = sqlite3.connect(_sqlite_path(_db_url))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    else:
        import pymysql
        from pymysql.cursors import DictCursor

        cfg = _mysql_cfg(_db_url)
        conn = pymysql.connect(cursorclass=DictCursor, **cfg)
        try:
            yield conn
        finally:
            conn.close()


_SQLITE_DDL = """
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  created_at TEXT NOT NULL,
  is_paid INTEGER NOT NULL DEFAULT 0,
  username TEXT UNIQUE,
  email TEXT,
  password_hash TEXT,
  display_name TEXT,
  concept_mode_default TEXT
);
CREATE TABLE IF NOT EXISTS growth_sessions (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  goal_intent TEXT,
  position_hint TEXT,
  probe_question TEXT,
  probe_answer TEXT,
  next_step TEXT,
  exercise_prompt TEXT,
  attempt_text TEXT,
  feedback_body TEXT,
  feedback_uncertain INTEGER NOT NULL DEFAULT 0,
  feedback_rejected_codegen INTEGER NOT NULL DEFAULT 0,
  progress_note TEXT,
  next_intent TEXT,
  stage TEXT NOT NULL DEFAULT 'orient',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS user_track_progress (
  user_id TEXT NOT NULL,
  track_id TEXT NOT NULL,
  chapter_id TEXT NOT NULL,
  lesson_id TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT 'unlocked',
  last_attempt TEXT,
  last_passed INTEGER NOT NULL DEFAULT 0,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (user_id, track_id, chapter_id, lesson_id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
"""

_MYSQL_DDL = [
    """CREATE TABLE IF NOT EXISTS users (
  id VARCHAR(36) PRIMARY KEY,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  is_paid TINYINT(1) NOT NULL DEFAULT 0,
  username VARCHAR(64) NULL UNIQUE,
  email VARCHAR(255) NULL,
  password_hash VARCHAR(255) NULL,
  display_name VARCHAR(64) NULL,
  concept_mode_default VARCHAR(16) NULL
) ENGINE=InnoDB""",
    """CREATE TABLE IF NOT EXISTS growth_sessions (
  id VARCHAR(36) PRIMARY KEY,
  user_id VARCHAR(36) NOT NULL,
  goal_intent TEXT NULL,
  position_hint TEXT NULL,
  probe_question TEXT NULL,
  probe_answer TEXT NULL,
  next_step TEXT NULL,
  exercise_prompt TEXT NULL,
  attempt_text TEXT NULL,
  feedback_body TEXT NULL,
  feedback_uncertain TINYINT(1) NOT NULL DEFAULT 0,
  feedback_rejected_codegen TINYINT(1) NOT NULL DEFAULT 0,
  progress_note TEXT NULL,
  next_intent TEXT NULL,
  stage VARCHAR(32) NOT NULL DEFAULT 'orient',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_gs_user FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB""",
    """CREATE TABLE IF NOT EXISTS user_track_progress (
  user_id VARCHAR(36) NOT NULL,
  track_id VARCHAR(64) NOT NULL,
  chapter_id VARCHAR(64) NOT NULL,
  lesson_id VARCHAR(64) NOT NULL DEFAULT '',
  status VARCHAR(32) NOT NULL DEFAULT 'unlocked',
  last_attempt TEXT NULL,
  last_passed TINYINT(1) NOT NULL DEFAULT 0,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, track_id, chapter_id, lesson_id),
  CONSTRAINT fk_utp_user FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB""",
]

_AUTH_COLUMNS = (
    ("username", "TEXT UNIQUE", "VARCHAR(64) NULL UNIQUE"),
    ("email", "TEXT", "VARCHAR(255) NULL"),
    ("password_hash", "TEXT", "VARCHAR(255) NULL"),
    ("display_name", "TEXT", "VARCHAR(64) NULL"),
    ("concept_mode_default", "TEXT", "VARCHAR(16) NULL"),
)


def _now() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def create_user(*, is_paid: bool = False) -> str:
    uid = str(uuid.uuid4())
    with _connect() as conn:
        if _backend == "sqlite":
            conn.execute(
                "INSERT INTO users (id, created_at, is_paid) VALUES (?, ?, ?)",
                (uid, _now(), 1 if is_paid else 0),
            )
            conn.commit()
        else:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (id, is_paid) VALUES (%s, %s)",
                    (uid, 1 if is_paid else 0),
                )
            conn.commit()
    return uid


def create_session(user_id: str) -> str:
    sid = str(uuid.uuid4())
    now = _now()
    with _connect() as conn:
        if _backend == "sqlite":
            conn.execute(
                "INSERT INTO growth_sessions (id, user_id, stage, created_at, updated_at) "
                "VALUES (?, ?, 'orient', ?, ?)",
                (sid, user_id, now, now),
            )
            conn.commit()
        else:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO growth_sessions (id, user_id, stage) VALUES (%s, %s, 'orient')",
                    (sid, user_id),
                )
            conn.commit()
    return sid


@dataclass
class GrowthSession:
    id: str
    user_id: str
    goal_intent: Optional[str]
    position_hint: Optional[str]
    probe_question: Optional[str]
    probe_answer: Optional[str]
    next_step: Optional[str]
    exercise_prompt: Optional[str]
    attempt_text: Optional[str]
    feedback_body: Optional[str]
    feedback_uncertain: bool
    feedback_rejected_codegen: bool
    progress_note: Optional[str]
    next_intent: Optional[str]
    stage: str


def _row_to_session(row: Any) -> GrowthSession:
    d = dict(row)
    return GrowthSession(
        id=d["id"],
        user_id=d["user_id"],
        goal_intent=d.get("goal_intent"),
        position_hint=d.get("position_hint"),
        probe_question=d.get("probe_question"),
        probe_answer=d.get("probe_answer"),
        next_step=d.get("next_step"),
        exercise_prompt=d.get("exercise_prompt"),
        attempt_text=d.get("attempt_text"),
        feedback_body=d.get("feedback_body"),
        feedback_uncertain=bool(d.get("feedback_uncertain")),
        feedback_rejected_codegen=bool(d.get("feedback_rejected_codegen")),
        progress_note=d.get("progress_note"),
        next_intent=d.get("next_intent"),
        stage=d["stage"],
    )


def get_session(session_id: str) -> Optional[GrowthSession]:
    with _connect() as conn:
        if _backend == "sqlite":
            cur = conn.execute(
                "SELECT * FROM growth_sessions WHERE id = ?", (session_id,)
            )
            row = cur.fetchone()
        else:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM growth_sessions WHERE id = %s", (session_id,))
                row = cur.fetchone()
    return _row_to_session(row) if row else None


def update_session(session_id: str, **fields: Any) -> None:
    if not fields:
        return
    fields = {**fields, "updated_at": _now()}
    cols = list(fields.keys())
    if _backend == "sqlite":
        sets = ", ".join(f"{c} = ?" for c in cols)
        vals = list(fields.values()) + [session_id]
        sql = f"UPDATE growth_sessions SET {sets} WHERE id = ?"
        with _connect() as conn:
            conn.execute(sql, vals)
            conn.commit()
    else:
        sets = ", ".join(f"{c} = %s" for c in cols)
        vals = list(fields.values()) + [session_id]
        sql = f"UPDATE growth_sessions SET {sets} WHERE id = %s"
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, vals)
            conn.commit()


def user_is_paid(user_id: str) -> bool:
    with _connect() as conn:
        if _backend == "sqlite":
            row = conn.execute(
                "SELECT is_paid FROM users WHERE id = ?", (user_id,)
            ).fetchone()
            return bool(row["is_paid"]) if row else False
        with conn.cursor() as cur:
            cur.execute("SELECT is_paid FROM users WHERE id = %s", (user_id,))
            row = cur.fetchone()
            return bool(row["is_paid"]) if row else False


def upsert_lesson_progress(
    user_id: str,
    track_id: str,
    chapter_id: str,
    lesson_id: str,
    *,
    status: str,
    last_attempt: str | None,
    last_passed: bool,
) -> None:
    now = _now()
    with _connect() as conn:
        if _backend == "sqlite":
            conn.execute(
                """
                INSERT INTO user_track_progress
                  (user_id, track_id, chapter_id, lesson_id, status, last_attempt, last_passed, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id, track_id, chapter_id, lesson_id) DO UPDATE SET
                  status=excluded.status,
                  last_attempt=excluded.last_attempt,
                  last_passed=excluded.last_passed,
                  updated_at=excluded.updated_at
                """,
                (
                    user_id,
                    track_id,
                    chapter_id,
                    lesson_id,
                    status,
                    last_attempt,
                    1 if last_passed else 0,
                    now,
                ),
            )
            conn.commit()
        else:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO user_track_progress
                      (user_id, track_id, chapter_id, lesson_id, status, last_attempt, last_passed)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                      status=VALUES(status),
                      last_attempt=VALUES(last_attempt),
                      last_passed=VALUES(last_passed)
                    """,
                    (
                        user_id,
                        track_id,
                        chapter_id,
                        lesson_id,
                        status,
                        last_attempt,
                        1 if last_passed else 0,
                    ),
                )
            conn.commit()


def list_passed_lessons(user_id: str, track_id: str) -> set[str]:
    with _connect() as conn:
        if _backend == "sqlite":
            rows = conn.execute(
                "SELECT lesson_id FROM user_track_progress "
                "WHERE user_id=? AND track_id=? AND last_passed=1",
                (user_id, track_id),
            ).fetchall()
            return {r["lesson_id"] for r in rows}
        with conn.cursor() as cur:
            cur.execute(
                "SELECT lesson_id FROM user_track_progress "
                "WHERE user_id=%s AND track_id=%s AND last_passed=1",
                (user_id, track_id),
            )
            rows = cur.fetchall()
            return {r["lesson_id"] for r in rows}


def latest_session_for_user(user_id: str) -> Optional[GrowthSession]:
    with _connect() as conn:
        if _backend == "sqlite":
            row = conn.execute(
                "SELECT * FROM growth_sessions WHERE user_id=? "
                "ORDER BY updated_at DESC LIMIT 1",
                (user_id,),
            ).fetchone()
        else:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM growth_sessions WHERE user_id=%s "
                    "ORDER BY updated_at DESC LIMIT 1",
                    (user_id,),
                )
                row = cur.fetchone()
    return _row_to_session(row) if row else None


def latest_attempted_lesson(user_id: str, track_id: str) -> Optional[tuple[str, str]]:
    """Return (chapter_id, lesson_id) of most recently updated progress row."""
    with _connect() as conn:
        if _backend == "sqlite":
            row = conn.execute(
                "SELECT chapter_id, lesson_id FROM user_track_progress "
                "WHERE user_id=? AND track_id=? ORDER BY updated_at DESC LIMIT 1",
                (user_id, track_id),
            ).fetchone()
        else:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT chapter_id, lesson_id FROM user_track_progress "
                    "WHERE user_id=%s AND track_id=%s ORDER BY updated_at DESC LIMIT 1",
                    (user_id, track_id),
                )
                row = cur.fetchone()
    if not row:
        return None
    d = dict(row)
    return d["chapter_id"], d["lesson_id"]


@dataclass
class UserRecord:
    id: str
    is_paid: bool
    username: Optional[str]
    email: Optional[str]
    password_hash: Optional[str]
    display_name: Optional[str]
    concept_mode_default: Optional[str]
    created_at: Optional[str] = None


def _row_to_user(row: Any) -> UserRecord:
    d = dict(row)
    created = d.get("created_at")
    if created is not None and not isinstance(created, str):
        created = str(created)
    return UserRecord(
        id=d["id"],
        is_paid=bool(d.get("is_paid")),
        username=d.get("username"),
        email=d.get("email"),
        password_hash=d.get("password_hash"),
        display_name=d.get("display_name"),
        concept_mode_default=d.get("concept_mode_default"),
        created_at=created,
    )


def get_user(user_id: str) -> Optional[UserRecord]:
    with _connect() as conn:
        if _backend == "sqlite":
            row = conn.execute(
                "SELECT * FROM users WHERE id = ?", (user_id,)
            ).fetchone()
        else:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                row = cur.fetchone()
    return _row_to_user(row) if row else None


def get_user_by_username(username: str) -> Optional[UserRecord]:
    uname = (username or "").strip()
    if not uname:
        return None
    with _connect() as conn:
        if _backend == "sqlite":
            row = conn.execute(
                "SELECT * FROM users WHERE username = ? COLLATE NOCASE", (uname,)
            ).fetchone()
        else:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM users WHERE username = %s",
                    (uname,),
                )
                row = cur.fetchone()
    return _row_to_user(row) if row else None


def register_user(
    *,
    username: str,
    password_hash: str,
    display_name: str | None = None,
    email: str | None = None,
) -> str:
    """Create a registered account user. Raises ValueError if username taken."""
    uname = username.strip()
    if get_user_by_username(uname):
        raise ValueError("用户名已被占用")
    uid = str(uuid.uuid4())
    dname = (display_name or "").strip() or uname
    em = (email or "").strip() or None
    with _connect() as conn:
        if _backend == "sqlite":
            conn.execute(
                "INSERT INTO users (id, created_at, is_paid, username, email, "
                "password_hash, display_name) VALUES (?, ?, 0, ?, ?, ?, ?)",
                (uid, _now(), uname, em, password_hash, dname),
            )
            conn.commit()
        else:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (id, is_paid, username, email, "
                    "password_hash, display_name) VALUES (%s, 0, %s, %s, %s, %s)",
                    (uid, uname, em, password_hash, dname),
                )
            conn.commit()
    return uid


def set_user_display_name(user_id: str, display_name: str | None) -> None:
    name = (display_name or "").strip() or None
    with _connect() as conn:
        if _backend == "sqlite":
            conn.execute(
                "UPDATE users SET display_name = ? WHERE id = ?",
                (name, user_id),
            )
            conn.commit()
        else:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE users SET display_name = %s WHERE id = %s",
                    (name, user_id),
                )
            conn.commit()


def set_user_concept_mode_default(user_id: str, mode: str | None) -> None:
    """Persist account default concept mode: ``normal`` | ``story`` (or NULL)."""
    m = (mode or "").strip().lower() or None
    if m not in (None, "normal", "story"):
        m = "normal"
    with _connect() as conn:
        if _backend == "sqlite":
            conn.execute(
                "UPDATE users SET concept_mode_default = ? WHERE id = ?",
                (m, user_id),
            )
            conn.commit()
        else:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE users SET concept_mode_default = %s WHERE id = %s",
                    (m, user_id),
                )
            conn.commit()


def merge_guest_into_user(guest_id: str, account_id: str) -> None:
    """Move guest progress/sessions onto an account. No-op if same id."""
    if not guest_id or not account_id or guest_id == account_id:
        return
    with _connect() as conn:
        if _backend == "sqlite":
            # Progress: prefer account row on conflict; take guest if account missing.
            rows = conn.execute(
                "SELECT track_id, chapter_id, lesson_id, status, last_attempt, "
                "last_passed, updated_at FROM user_track_progress WHERE user_id=?",
                (guest_id,),
            ).fetchall()
            for r in rows:
                existing = conn.execute(
                    "SELECT 1 FROM user_track_progress WHERE user_id=? AND track_id=? "
                    "AND chapter_id=? AND lesson_id=?",
                    (account_id, r["track_id"], r["chapter_id"], r["lesson_id"]),
                ).fetchone()
                if existing:
                    continue
                conn.execute(
                    "INSERT INTO user_track_progress "
                    "(user_id, track_id, chapter_id, lesson_id, status, "
                    "last_attempt, last_passed, updated_at) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        account_id,
                        r["track_id"],
                        r["chapter_id"],
                        r["lesson_id"],
                        r["status"],
                        r["last_attempt"],
                        r["last_passed"],
                        r["updated_at"],
                    ),
                )
            conn.execute(
                "DELETE FROM user_track_progress WHERE user_id=?", (guest_id,)
            )
            conn.execute(
                "UPDATE growth_sessions SET user_id=? WHERE user_id=?",
                (account_id, guest_id),
            )
            conn.commit()
        else:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT track_id, chapter_id, lesson_id, status, last_attempt, "
                    "last_passed, updated_at FROM user_track_progress WHERE user_id=%s",
                    (guest_id,),
                )
                rows = cur.fetchall()
                for r in rows:
                    cur.execute(
                        "SELECT 1 FROM user_track_progress WHERE user_id=%s AND "
                        "track_id=%s AND chapter_id=%s AND lesson_id=%s",
                        (
                            account_id,
                            r["track_id"],
                            r["chapter_id"],
                            r["lesson_id"],
                        ),
                    )
                    if cur.fetchone():
                        continue
                    cur.execute(
                        "INSERT INTO user_track_progress "
                        "(user_id, track_id, chapter_id, lesson_id, status, "
                        "last_attempt, last_passed, updated_at) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (
                            account_id,
                            r["track_id"],
                            r["chapter_id"],
                            r["lesson_id"],
                            r["status"],
                            r["last_attempt"],
                            r["last_passed"],
                            r["updated_at"],
                        ),
                    )
                cur.execute(
                    "DELETE FROM user_track_progress WHERE user_id=%s", (guest_id,)
                )
                cur.execute(
                    "UPDATE growth_sessions SET user_id=%s WHERE user_id=%s",
                    (account_id, guest_id),
                )
            conn.commit()
