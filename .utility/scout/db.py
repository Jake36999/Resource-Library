"""Queue storage for the scouting pipeline.

The queue is the resumability guarantee: state lives in SQLite, never in
memory, so an interrupted run resumes at the highest-ranked incomplete item
with no work repeated and nothing lost.
"""
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import time
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterator

from .config import DB_PATH

STATES = (
    "discovered",   # found, no model has looked at it
    "scouted",      # local worker has categorised it
    "ranked",       # deterministic evaluator has scored it
    "queued",       # frozen into a cohort, awaiting deep dive
    "deep_dive",    # leased, being worked on right now
    "catalogued",   # dossier written, ready for note rendering
    "rejected",     # duplicate, dead, or out of scope
    "deferred",     # diverted to human review
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS scout_queue (
  id                INTEGER PRIMARY KEY,
  url               TEXT NOT NULL,
  url_hash          TEXT NOT NULL UNIQUE,
  repo_key          TEXT,
  title             TEXT,
  description       TEXT,
  discovery_query   TEXT,
  discovery_backend TEXT,
  domain_key        TEXT,
  archetype         TEXT,
  tags              TEXT,
  one_line          TEXT,
  sensitivity       TEXT NOT NULL DEFAULT 'normal',
  scout_confidence  REAL,
  corroboration     INTEGER NOT NULL DEFAULT 1,
  github_json       TEXT,
  score             REAL,
  cohort_id         TEXT,
  state             TEXT NOT NULL DEFAULT 'discovered',
  attempts          INTEGER NOT NULL DEFAULT 0,
  last_error        TEXT,
  lease_owner       TEXT,
  lease_expires_at  TEXT,
  note_path         TEXT,
  dossier_path      TEXT,
  discovered_at     TEXT NOT NULL,
  updated_at        TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_scout_state_score ON scout_queue(state, score DESC);
CREATE INDEX IF NOT EXISTS idx_scout_cohort ON scout_queue(cohort_id, score DESC);
CREATE INDEX IF NOT EXISTS idx_scout_repo ON scout_queue(repo_key);

CREATE TABLE IF NOT EXISTS scout_signal (
  queue_id   INTEGER NOT NULL,
  signal     TEXT NOT NULL,
  value      REAL NOT NULL,
  weight     REAL NOT NULL,
  detail     TEXT,
  PRIMARY KEY (queue_id, signal)
);

CREATE TABLE IF NOT EXISTS scout_cohort (
  cohort_id   TEXT PRIMARY KEY,
  frozen_at   TEXT NOT NULL,
  size        INTEGER NOT NULL,
  consumed    INTEGER NOT NULL DEFAULT 0,
  note_path   TEXT
);
"""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def url_hash(url: str) -> str:
    normalised = url.strip().lower().rstrip("/")
    for prefix in ("https://", "http://", "www."):
        if normalised.startswith(prefix):
            normalised = normalised[len(prefix):]
    if normalised.endswith(".git"):
        normalised = normalised[:-4]
    return hashlib.sha256(normalised.encode("utf-8")).hexdigest()[:32]


@contextmanager
def connect(path: Path | None = None) -> Iterator[sqlite3.Connection]:
    target = Path(path or DB_PATH)
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(target, timeout=30)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init(path: Path | None = None) -> None:
    with connect(path) as conn:
        conn.executescript(SCHEMA)


def add_candidate(conn: sqlite3.Connection, *, url: str, title: str = "",
                  description: str = "", repo_key: str | None = None,
                  discovery_query: str = "", discovery_backend: str = "",
                  domain_key: str = "") -> tuple[int | None, bool]:
    """Insert a candidate. Returns (row id, created).

    A URL already present does not create a row - it increments that row's
    corroboration count instead. Independent rediscovery is the single most
    informative signal the pipeline collects, so it must never be discarded
    as a mere duplicate.
    """
    h = url_hash(url)
    existing = conn.execute(
        "SELECT id FROM scout_queue WHERE url_hash = ?", (h,)
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE scout_queue SET corroboration = corroboration + 1, updated_at = ? WHERE id = ?",
            (now_iso(), existing["id"]),
        )
        return existing["id"], False
    stamp = now_iso()
    cur = conn.execute(
        """INSERT INTO scout_queue
           (url, url_hash, repo_key, title, description, discovery_query,
            discovery_backend, domain_key, state, discovered_at, updated_at)
           VALUES (?,?,?,?,?,?,?,?,'discovered',?,?)""",
        (url, h, repo_key, title, description, discovery_query,
         discovery_backend, domain_key, stamp, stamp),
    )
    return cur.lastrowid, True


def update(conn: sqlite3.Connection, row_id: int, **fields: Any) -> None:
    if not fields:
        return
    fields["updated_at"] = now_iso()
    assignments = ", ".join(f"{k} = ?" for k in fields)
    conn.execute(
        f"UPDATE scout_queue SET {assignments} WHERE id = ?",
        (*fields.values(), row_id),
    )


def fetch_state(conn: sqlite3.Connection, state: str, limit: int | None = None,
                order: str = "id") -> list[sqlite3.Row]:
    sql = f"SELECT * FROM scout_queue WHERE state = ? ORDER BY {order}"
    if limit:
        sql += f" LIMIT {int(limit)}"
    return list(conn.execute(sql, (state,)))


def counts(conn: sqlite3.Connection) -> dict[str, int]:
    rows = conn.execute("SELECT state, COUNT(*) n FROM scout_queue GROUP BY state")
    return {r["state"]: r["n"] for r in rows}


def record_signals(conn: sqlite3.Connection, row_id: int,
                   signals: list[dict[str, Any]]) -> None:
    conn.execute("DELETE FROM scout_signal WHERE queue_id = ?", (row_id,))
    conn.executemany(
        "INSERT INTO scout_signal (queue_id, signal, value, weight, detail) VALUES (?,?,?,?,?)",
        [(row_id, s["signal"], float(s["value"]), float(s["weight"]), s.get("detail", ""))
         for s in signals],
    )


def signals_for(conn: sqlite3.Connection, row_id: int) -> list[sqlite3.Row]:
    return list(conn.execute(
        "SELECT * FROM scout_signal WHERE queue_id = ? ORDER BY weight DESC", (row_id,)))


# ---------------------------------------------------------------- leasing

def claim_next(conn: sqlite3.Connection, owner: str, lease_seconds: int,
               cohort_id: str | None = None) -> sqlite3.Row | None:
    """Take the highest-ranked queued item under a lease.

    An expired lease is reclaimable, so a crashed run does not deadlock the
    queue behind an item nobody is working on.
    """
    now = datetime.now(timezone.utc)
    stamp = now.isoformat(timespec="seconds")
    expiry = (now + timedelta(seconds=lease_seconds)).isoformat(timespec="seconds")
    params: list[Any] = [stamp]
    where = "(state = 'queued' OR (state = 'deep_dive' AND lease_expires_at < ?))"
    if cohort_id:
        where += " AND cohort_id = ?"
        params.append(cohort_id)
    row = conn.execute(
        f"SELECT * FROM scout_queue WHERE {where} ORDER BY score DESC, id ASC LIMIT 1",
        params,
    ).fetchone()
    if not row:
        return None
    conn.execute(
        "UPDATE scout_queue SET state='deep_dive', lease_owner=?, lease_expires_at=?, "
        "attempts = attempts + 1, updated_at=? WHERE id=?",
        (owner, expiry, stamp, row["id"]),
    )
    return conn.execute("SELECT * FROM scout_queue WHERE id = ?", (row["id"],)).fetchone()


def release(conn: sqlite3.Connection, row_id: int, state: str,
            error: str | None = None, **fields: Any) -> None:
    update(conn, row_id, state=state, lease_owner=None, lease_expires_at=None,
           last_error=error, **fields)


def owner_token() -> str:
    return f"{os.getpid()}@{int(time.time())}"


# ---------------------------------------------------------------- cohorts

def freeze_cohort(conn: sqlite3.Connection, cohort_id: str, size: int) -> list[sqlite3.Row]:
    rows = list(conn.execute(
        "SELECT * FROM scout_queue WHERE state='ranked' ORDER BY score DESC, id ASC LIMIT ?",
        (size,)))
    if not rows:
        return []
    conn.executemany(
        "UPDATE scout_queue SET state='queued', cohort_id=?, updated_at=? WHERE id=?",
        [(cohort_id, now_iso(), r["id"]) for r in rows])
    conn.execute(
        "INSERT OR REPLACE INTO scout_cohort (cohort_id, frozen_at, size, consumed) "
        "VALUES (?,?,?,COALESCE((SELECT consumed FROM scout_cohort WHERE cohort_id=?),0))",
        (cohort_id, now_iso(), len(rows), cohort_id))
    return list(conn.execute(
        "SELECT * FROM scout_queue WHERE cohort_id=? ORDER BY score DESC, id ASC",
        (cohort_id,)))


def active_cohort(conn: sqlite3.Connection) -> str | None:
    row = conn.execute(
        "SELECT cohort_id FROM scout_queue WHERE state IN ('queued','deep_dive') "
        "AND cohort_id IS NOT NULL ORDER BY cohort_id LIMIT 1").fetchone()
    return row["cohort_id"] if row else None


def existing_repo_keys(conn: sqlite3.Connection) -> set[str]:
    rows = conn.execute(
        "SELECT DISTINCT repo_key FROM scout_queue WHERE repo_key IS NOT NULL")
    return {r["repo_key"] for r in rows}
