"""The derived store: vault -> SQLite rows + FTS5.

Everything here is disposable. Deleting `catalogue_index.sqlite` loses nothing
because Markdown is truth; the only cost of deleting it is the seconds spent
rebuilding. That property is what makes the rest of the system safe to change
quickly, so it is asserted by a test rather than merely intended.

A separate database from `solutions_library.sqlite` on purpose (spec 10.1): an
index rebuild must not be able to disturb the scouting queue.
"""
from __future__ import annotations

import json
import sqlite3
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from . import notes as notes_mod
from .config import CatalogueConfig, index_db_path, is_hub, vault_root
from .notes import Chunk, Note

SCHEMA_VERSION = 5

SCHEMA = """
CREATE TABLE IF NOT EXISTS note (
  name          TEXT PRIMARY KEY,
  layer         TEXT NOT NULL,
  path          TEXT NOT NULL,
  type          TEXT,
  frontmatter   TEXT NOT NULL,
  body          TEXT NOT NULL,
  mtime         REAL NOT NULL,
  indexed_at    TEXT NOT NULL,
  parse_error   TEXT
);

CREATE TABLE IF NOT EXISTS resource_facet (
  name                TEXT PRIMARY KEY REFERENCES note(name) ON DELETE CASCADE,
  repo_key            TEXT,
  canonical_url       TEXT,
  primary_topic       TEXT,
  domain_primary      TEXT,
  ecosystem           TEXT,
  maturity_stage      TEXT,
  license_class       TEXT,
  deployment_target   TEXT,
  interface_protocol  TEXT,
  data_locality       TEXT,
  hardware_footprint  TEXT,
  security_compliance TEXT,
  agent_surface      TEXT,
  is_container        INTEGER NOT NULL DEFAULT 0,
  pushed_at           TEXT,
  stars               INTEGER,
  application_count   INTEGER NOT NULL DEFAULT 0,
  -- The one-line description a listing needs. Without it, showing a hundred
  -- results with a sentence each meant opening a hundred notes - so every
  -- listing surface either did N reads or showed no description at all.
  -- Denormalised deliberately: `resource_facet` is derived and disposable,
  -- and the note stays the truth.
  bottom_line         TEXT
);
CREATE INDEX IF NOT EXISTS idx_facet_filters
  ON resource_facet(license_class, deployment_target, hardware_footprint);

CREATE TABLE IF NOT EXISTS link (
  src TEXT NOT NULL,
  dst TEXT NOT NULL,
  relation TEXT,
  PRIMARY KEY (src, dst, relation)
);
CREATE INDEX IF NOT EXISTS idx_link_dst ON link(dst);

CREATE TABLE IF NOT EXISTS chunk (
  id INTEGER PRIMARY KEY,
  note TEXT NOT NULL REFERENCES note(name) ON DELETE CASCADE,
  ordinal INTEGER NOT NULL,
  layer TEXT NOT NULL,
  heading TEXT,
  text TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_chunk_note ON chunk(note);

-- `porter` stems, so a query saying "institution" reaches a note saying
-- "institutional". Without it they are different tokens and the note is
-- unreachable: the scenario test found a source describing itself as a corpus
-- of "institutional records" that no query about institutions could return.
CREATE VIRTUAL TABLE IF NOT EXISTS chunk_fts USING fts5(
  text, heading, note UNINDEXED, content='chunk', content_rowid='id',
  tokenize='porter unicode61'
);

CREATE TABLE IF NOT EXISTS embedding (
  chunk_id INTEGER PRIMARY KEY REFERENCES chunk(id) ON DELETE CASCADE,
  model TEXT NOT NULL,
  vector BLOB NOT NULL,
  dims INTEGER NOT NULL,
  text_hash TEXT NOT NULL
);

-- The one persisted extract: addresses, not content (spec 3.4 / 10.2).
CREATE TABLE IF NOT EXISTS access_point (
  id            TEXT PRIMARY KEY,
  source        TEXT NOT NULL,
  kind          TEXT NOT NULL,
  url           TEXT NOT NULL,
  auth          TEXT,
  rate_limit    TEXT,
  formats       TEXT,
  description   TEXT,
  verified_at   TEXT,
  reachable     INTEGER,
  notes         TEXT
);
CREATE INDEX IF NOT EXISTS idx_access_source ON access_point(source);
CREATE INDEX IF NOT EXISTS idx_access_kind   ON access_point(kind);

-- Community assignments live here and never in note frontmatter (spec 4B R2).
CREATE TABLE IF NOT EXISTS note_community (
  note       TEXT PRIMARY KEY REFERENCES note(name) ON DELETE CASCADE,
  community  INTEGER NOT NULL,
  label      TEXT,
  centrality REAL
);

-- A written summary of each community, at the same level as the assignment.
-- Derived, disposable and advisory (spec 4B R2, R3): a community report is an
-- observation written down, and may not create or rename a topic.
CREATE TABLE IF NOT EXISTS community_report (
  community   INTEGER PRIMARY KEY,
  label       TEXT,
  size        INTEGER NOT NULL,
  topics      TEXT,           -- JSON: topic -> member count
  summary     TEXT NOT NULL,  -- the prose a person or agent reads
  members     TEXT,           -- JSON: member names, most central first
  built_at    TEXT
);

CREATE TABLE IF NOT EXISTS meta (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);
"""

FACET_FIELDS = (
    "repo_key", "canonical_url", "primary_topic", "domain_primary", "ecosystem",
    "maturity_stage", "license_class", "deployment_target", "interface_protocol",
    "data_locality", "hardware_footprint", "security_compliance",
    "agent_surface",
)

# Layers that get a facet row. Reviews are held resources and are filterable
# for the same reasons; papers carry the same taxonomy axes.
FACETED_LAYERS = {"resource", "review", "paper"}


@dataclass(frozen=True)
class IndexStats:
    """Contract per spec 9.1."""

    notes: int
    chunks: int
    links: int
    duration_s: float
    errors: list[str]


# ------------------------------------------------------------------ plumbing

def connect(db_path: Path | None = None) -> sqlite3.Connection:
    path = Path(db_path) if db_path else index_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


def init(conn: sqlite3.Connection) -> None:
    """Create the schema, recreating it outright when the version has moved.

    `CREATE TABLE IF NOT EXISTS` cannot add a column to a table that already
    exists, so a schema change would otherwise fail at the first insert with
    "no such column" - which is a confusing way to learn that the index is out
    of date. Because the index is derived and disposable, the correct response
    is simply to rebuild it: Markdown is truth and nothing is lost.
    """
    stored = None
    try:
        row = conn.execute(
            "SELECT value FROM meta WHERE key = 'schema_version'").fetchone()
        stored = row["value"] if row else None
    except sqlite3.OperationalError:
        stored = None                       # no meta table yet: a fresh database
    if stored is not None and stored != str(SCHEMA_VERSION):
        for (name,) in conn.execute(
                "SELECT name FROM sqlite_master WHERE type IN ('table','view') "
                "AND name NOT LIKE 'sqlite_%'").fetchall():
            conn.execute(f"DROP TABLE IF EXISTS \"{name}\"")
        conn.commit()
    conn.executescript(SCHEMA)
    conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES('schema_version', ?)",
                 (str(SCHEMA_VERSION),))
    conn.commit()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def stamp(conn: sqlite3.Connection, key: str, value: str) -> None:
    conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES(?, ?)", (key, value))


def get_stamp(conn: sqlite3.Connection, key: str, default: str = "") -> str:
    row = conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
    return row["value"] if row else default


# --------------------------------------------------------------------- build

def build(vault: Path | None = None, db_path: Path | None = None, *,
          rebuild: bool = False, cfg: CatalogueConfig | None = None) -> IndexStats:
    """Index the whole vault.

    `rebuild=True` drops every derived row first. Without it the build is
    still a full refresh - it upserts every note and removes rows for notes
    that no longer exist - so the two differ only in whether embeddings
    survive, which is the expensive part to recompute.
    """
    cfg = cfg or CatalogueConfig.load()
    root = Path(vault) if vault else vault_root()
    started = time.perf_counter()
    errors: list[str] = []

    conn = connect(db_path)
    try:
        init(conn)
        if rebuild:
            for table in ("embedding", "chunk", "community_report",
                          "note_community", "link",
                          "resource_facet", "note"):
                conn.execute(f"DELETE FROM {table}")
            conn.execute("INSERT INTO chunk_fts(chunk_fts) VALUES('rebuild')")

        loaded: list[Note] = []
        for path in notes_mod.iter_note_paths(root):
            try:
                loaded.append(notes_mod.load_note(path, root))
            except Exception as exc:                       # pragma: no cover
                errors.append(f"{path.name}: {exc}")

        seen = {note.name for note in loaded}
        duplicates = _duplicate_names(loaded)
        errors.extend(duplicates)

        # Drop notes that have left the vault. Markdown is truth, so its
        # absence is authoritative too.
        for row in conn.execute("SELECT name FROM note").fetchall():
            if row["name"] not in seen:
                conn.execute("DELETE FROM note WHERE name = ?", (row["name"],))

        chunk_total = 0
        for note in loaded:
            chunk_total += _write_note(conn, note, cfg)
            if note.parse_error:
                errors.append(f"{note.name}: {note.parse_error}")

        _recount_applications(conn)
        conn.execute("INSERT INTO chunk_fts(chunk_fts) VALUES('rebuild')")

        link_total = conn.execute("SELECT COUNT(*) AS n FROM link").fetchone()["n"]
        stamp(conn, "indexed_at", now_iso())
        stamp(conn, "vault_root", str(root))
        stamp(conn, "note_count", str(len(loaded)))
        conn.commit()
        return IndexStats(notes=len(loaded), chunks=chunk_total, links=link_total,
                          duration_s=round(time.perf_counter() - started, 3),
                          errors=errors)
    finally:
        conn.close()


def refresh(vault: Path | None = None, db_path: Path | None = None,
            since: datetime | float | None = None,
            cfg: CatalogueConfig | None = None) -> IndexStats:
    """Re-index only what changed since `since`.

    Deletions still need a full pass over the name list, which is cheap; it is
    the parsing and chunking that `since` avoids.
    """
    cfg = cfg or CatalogueConfig.load()
    root = Path(vault) if vault else vault_root()
    cutoff = _as_epoch(since)
    started = time.perf_counter()
    errors: list[str] = []

    conn = connect(db_path)
    try:
        init(conn)
        seen: set[str] = set()
        touched = 0
        chunk_total = 0
        for path in notes_mod.iter_note_paths(root):
            seen.add(path.stem)
            if cutoff is not None and path.stat().st_mtime <= cutoff:
                continue
            try:
                note = notes_mod.load_note(path, root)
            except Exception as exc:                       # pragma: no cover
                errors.append(f"{path.name}: {exc}")
                continue
            chunk_total += _write_note(conn, note, cfg)
            touched += 1
            if note.parse_error:
                errors.append(f"{note.name}: {note.parse_error}")

        for row in conn.execute("SELECT name FROM note").fetchall():
            if row["name"] not in seen:
                conn.execute("DELETE FROM note WHERE name = ?", (row["name"],))

        _recount_applications(conn)
        conn.execute("INSERT INTO chunk_fts(chunk_fts) VALUES('rebuild')")
        link_total = conn.execute("SELECT COUNT(*) AS n FROM link").fetchone()["n"]
        stamp(conn, "indexed_at", now_iso())
        conn.commit()
        return IndexStats(notes=touched, chunks=chunk_total, links=link_total,
                          duration_s=round(time.perf_counter() - started, 3),
                          errors=errors)
    finally:
        conn.close()


def _as_epoch(since: datetime | float | None) -> float | None:
    if since is None:
        return None
    if isinstance(since, datetime):
        return since.timestamp()
    return float(since)


def _duplicate_names(loaded: Iterable[Note]) -> list[str]:
    """Two notes with the same stem would collide on the primary key.

    Reported rather than silently overwritten: a note that vanished from the
    index because another shares its name is exactly the kind of quiet loss
    the index must not cause.
    """
    seen: dict[str, Path] = {}
    out: list[str] = []
    for note in loaded:
        if note.name in seen:
            out.append(f"duplicate note name '{note.name}': {seen[note.name]} and {note.path}")
        else:
            seen[note.name] = note.path
    return out


def _write_note(conn: sqlite3.Connection, note: Note, cfg: CatalogueConfig) -> int:
    conn.execute(
        "INSERT INTO note(name, layer, path, type, frontmatter, body, mtime, "
        "indexed_at, parse_error) VALUES(?,?,?,?,?,?,?,?,?) "
        "ON CONFLICT(name) DO UPDATE SET layer=excluded.layer, path=excluded.path, "
        "type=excluded.type, frontmatter=excluded.frontmatter, body=excluded.body, "
        "mtime=excluded.mtime, indexed_at=excluded.indexed_at, "
        "parse_error=excluded.parse_error",
        (note.name, note.layer, str(note.path), note.type,
         json.dumps(note.frontmatter, ensure_ascii=False, default=str),
         note.body, note.mtime, now_iso(), note.parse_error),
    )

    conn.execute("DELETE FROM link WHERE src = ?", (note.name,))
    for link in note.links():
        conn.execute("INSERT OR IGNORE INTO link(src, dst, relation) VALUES(?,?,?)",
                     (link.src, link.dst, link.relation))

    conn.execute("DELETE FROM resource_facet WHERE name = ?", (note.name,))
    # Hubs sit in the same folders as the notes they route to; a facet row for
    # one would put a router into every filtered candidate set.
    if note.layer in FACETED_LAYERS and not is_hub(note.type):
        _write_facet(conn, note)

    chunks = notes_mod.chunk_note(note, cfg.chunk_target_chars, cfg.chunk_min_chars)

    # Leave unchanged chunks alone. Embeddings cascade from chunk rows, so a
    # blanket delete-and-reinsert threw away every vector on a routine index
    # run - minutes of work lost to re-indexing notes that had not changed.
    existing = conn.execute(
        "SELECT ordinal, heading, text FROM chunk WHERE note = ? ORDER BY ordinal",
        (note.name,)).fetchall()
    unchanged = (len(existing) == len(chunks) and all(
        row["ordinal"] == chunk.ordinal
        and (row["heading"] or "") == chunk.heading
        and row["text"] == chunk.text
        for row, chunk in zip(existing, chunks)))
    if unchanged:
        return len(chunks)

    conn.execute("DELETE FROM chunk WHERE note = ?", (note.name,))
    for chunk in chunks:
        conn.execute(
            "INSERT INTO chunk(note, ordinal, layer, heading, text) VALUES(?,?,?,?,?)",
            (chunk.note, chunk.ordinal, chunk.layer, chunk.heading, chunk.text))
    return len(chunks)


def _write_facet(conn: sqlite3.Connection, note: Note) -> None:
    values: dict[str, Any] = {field: (note.string(field) or None) for field in FACET_FIELDS}
    values["name"] = note.name
    values["is_container"] = 1 if note.is_container() else 0
    values["pushed_at"] = note.string("github_pushed_at") or note.string("pushed_at") or None
    stars = note.get("github_stars", note.get("stars"))
    try:
        values["stars"] = int(stars) if stars is not None else None
    except (TypeError, ValueError):
        values["stars"] = None
    values["application_count"] = 0
    # First paragraph of `Bottom Line`, trimmed. A listing shows a sentence,
    # not a section.
    summary = " ".join((note.section("Bottom Line") or "").split())
    values["bottom_line"] = summary[:400] or None
    columns = ", ".join(values)
    marks = ", ".join("?" for _ in values)
    conn.execute(f"INSERT OR REPLACE INTO resource_facet({columns}) VALUES({marks})",
                 tuple(values.values()))


def _recount_applications(conn: sqlite3.Connection) -> None:
    """Proven use, counted from what is actually recorded.

    Only `applied_resource` edges from application records count. A resource
    named in an application's prose but not linked is not evidence of use, and
    inflating this number would corrupt the one signal that distinguishes a
    resource that worked from a plausible stranger.
    """
    conn.execute("UPDATE resource_facet SET application_count = 0")
    conn.execute(
        "UPDATE resource_facet SET application_count = ("
        "  SELECT COUNT(*) FROM link JOIN note ON note.name = link.src"
        "  WHERE link.dst = resource_facet.name"
        "    AND link.relation = 'applied_resource'"
        "    AND note.layer = 'application')"
    )


# ------------------------------------------------------------------ readers

def chunks_for(note_name: str, db_path: Path | None = None) -> list[Chunk]:
    conn = connect(db_path)
    try:
        rows = conn.execute(
            "SELECT note, layer, ordinal, heading, text FROM chunk "
            "WHERE note = ? ORDER BY ordinal", (note_name,)).fetchall()
        return [Chunk(note=r["note"], layer=r["layer"], ordinal=r["ordinal"],
                      heading=r["heading"] or "", text=r["text"]) for r in rows]
    finally:
        conn.close()


def counts(db_path: Path | None = None) -> dict[str, int]:
    conn = connect(db_path)
    try:
        init(conn)
        out = {}
        for table in ("note", "chunk", "link", "embedding", "access_point",
                      "note_community", "resource_facet"):
            out[table] = conn.execute(f"SELECT COUNT(*) AS n FROM {table}").fetchone()["n"]
        out["indexed_at"] = get_stamp(conn, "indexed_at", "never")
        return out
    finally:
        conn.close()


def is_stale(db_path: Path | None = None, vault: Path | None = None) -> bool:
    """True when a note has changed since the last build.

    Consult uses this to say so in `Response.notes` rather than quietly
    answering from a stale index.
    """
    root = Path(vault) if vault else vault_root()
    conn = connect(db_path)
    try:
        init(conn)
        row = conn.execute("SELECT MAX(mtime) AS m FROM note").fetchone()
        indexed_max = row["m"] or 0.0
    finally:
        conn.close()
    try:
        current = max((p.stat().st_mtime for p in notes_mod.iter_note_paths(root)),
                      default=0.0)
    except OSError:                                        # pragma: no cover
        return False
    return current > indexed_max + 1.0
