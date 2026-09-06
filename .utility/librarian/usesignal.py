"""What was actually opened, taken or rejected — so ranking can eventually learn.

`consult._proven_use_bonus` already exists and already reads `application_count`.
On 2026-09-04 that count was **zero for all 130 resources**, so the bonus has
never once fired. The cause is not the code: the four application records
describe what they used in prose —

    resources_used: ["agent harness implementations", "training pipelines"]

— rather than linking it, so `applied_resource` edges were never created and
nothing connects a record to a note. A fully built feedback path receiving
nothing is indistinguishable from no feedback path at all.

[[elastic - elastic-labs]] ships a learning-to-rank corpus for exactly this
loop. The workbench half of that repository was adopted here as
`librarian relevance`; this is the half that was not.

## Two grains, and why both

An **application record** is the heavyweight signal: somebody used a source in
real work and wrote up what happened. It is worth a great deal and there are
four of them, which is not enough to rank on and will not be for a long time.

A **use event** is the lightweight one: this query returned this source, and it
was opened, taken, or dismissed. It costs one command, it accumulates during
ordinary use, and after a few hundred it is a genuine relevance signal.

## What this deliberately does not do yet

**It does not affect ranking.** There is no data, and fitting a ranking signal
to an empty table would produce a knob that looks principled and encodes
nothing. The reading side (`weights`) exists and is measured through
`librarian relevance` like everything else; it stays off until the table has
enough in it to move a number. `usesignal.readiness()` says when that is.

That restraint is the same one `LOCATE_DO_NOT_ADJUDICATE` asks for elsewhere:
a signal nobody has evidence for should not quietly decide what a reader sees.
"""
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from .components import connect
from .config import component_db_path

# How many events before the signal is worth reading. Not a guess dressed as a
# constant: below roughly this many, a handful of sessions by one person
# dominates, and ranking would learn that person's week rather than relevance.
READINESS_EVENTS = 200
READINESS_DISTINCT_QUERIES = 40

VERDICTS = ("opened", "taken", "dismissed", "irrelevant")

SCHEMA = """
CREATE TABLE IF NOT EXISTS use_event (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    recorded_at TEXT NOT NULL,
    query      TEXT NOT NULL,
    note       TEXT NOT NULL,
    rank       INTEGER,
    verdict    TEXT NOT NULL,
    comment    TEXT
);
CREATE INDEX IF NOT EXISTS ix_use_note ON use_event(note);
CREATE INDEX IF NOT EXISTS ix_use_verdict ON use_event(verdict);
"""


@dataclass(frozen=True)
class Readiness:
    events: int
    distinct_queries: int
    distinct_notes: int

    @property
    def ready(self) -> bool:
        return (self.events >= READINESS_EVENTS
                and self.distinct_queries >= READINESS_DISTINCT_QUERIES)

    def sentence(self) -> str:
        if self.ready:
            return (f"{self.events} events over {self.distinct_queries} distinct "
                    "queries - enough to measure a ranking signal against; add a "
                    "configuration to rank_configs.json and run `librarian relevance`")
        return (f"{self.events}/{READINESS_EVENTS} events over "
                f"{self.distinct_queries}/{READINESS_DISTINCT_QUERIES} distinct "
                "queries - not enough to rank on, and reading it now would learn "
                "one person's week rather than relevance")


def ensure_schema(conn: sqlite3.Connection) -> None:
    with conn:
        conn.executescript(SCHEMA)


def record(query: str, note: str, verdict: str, *, rank: int | None = None,
           comment: str = "", db_path: Path | None = None) -> None:
    """Log one judgement about one answer. Data, not a conclusion."""
    if verdict not in VERDICTS:
        raise ValueError(f"verdict must be one of {list(VERDICTS)}")
    conn = connect(db_path or component_db_path())
    try:
        ensure_schema(conn)
        with conn:
            conn.execute(
                "INSERT INTO use_event (recorded_at, query, note, rank, verdict, comment)"
                " VALUES (?,?,?,?,?,?)",
                (datetime.now(timezone.utc).isoformat(timespec="seconds"),
                 query.strip(), note.strip(), rank, verdict, comment.strip()))
    finally:
        conn.close()


def readiness(db_path: Path | None = None) -> Readiness:
    target = Path(db_path or component_db_path())
    if not target.exists():
        return Readiness(0, 0, 0)
    conn = connect(target)
    try:
        ensure_schema(conn)
        row = conn.execute(
            "SELECT COUNT(*) e, COUNT(DISTINCT query) q, COUNT(DISTINCT note) n "
            "FROM use_event").fetchone()
        return Readiness(row["e"] or 0, row["q"] or 0, row["n"] or 0)
    finally:
        conn.close()


def weights(db_path: Path | None = None) -> dict[str, float]:
    """Per-note usefulness, from recorded verdicts. Read by nothing yet.

    `taken` counts double: acting on a source is a stronger statement than
    opening it. `dismissed` subtracts, `irrelevant` subtracts more - a result
    the asker judged unrelated is the clearest negative signal there is, and it
    is the one a click-through log cannot capture at all.
    """
    target = Path(db_path or component_db_path())
    if not target.exists():
        return {}
    conn = connect(target)
    try:
        ensure_schema(conn)
        scores: dict[str, float] = {}
        for row in conn.execute(
                "SELECT note, verdict, COUNT(*) n FROM use_event GROUP BY note, verdict"):
            delta = {"taken": 2.0, "opened": 1.0,
                     "dismissed": -0.5, "irrelevant": -1.5}[row["verdict"]]
            scores[row["note"]] = scores.get(row["note"], 0.0) + delta * row["n"]
        return scores
    finally:
        conn.close()


def recent(limit: int = 20, db_path: Path | None = None) -> list[dict[str, Any]]:
    target = Path(db_path or component_db_path())
    if not target.exists():
        return []
    conn = connect(target)
    try:
        ensure_schema(conn)
        return [dict(r) for r in conn.execute(
            "SELECT * FROM use_event ORDER BY id DESC LIMIT ?", (limit,))]
    finally:
        conn.close()


def format_status(state: Readiness, top: Sequence[tuple[str, float]] = ()) -> str:
    lines = ["Use signal", "", f"  {state.sentence()}", ""]
    if top:
        lines.append("  most-used answers so far:")
        for name, score in top[:10]:
            lines.append(f"      {score:+.1f}  {name}")
    else:
        lines.append("  no events recorded yet. Record one with:")
        lines.append("      python -m librarian used \"<query>\" \"<note>\" --verdict taken")
    return "\n".join(lines)
