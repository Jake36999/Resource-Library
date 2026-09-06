"""The data layer: what a source is *made of*, as rows rather than as prose.

A resource note answers *what is this and what is it for*. That is **information**
— it is what the components of a repository mean once you look at how they
relate. It is written for a person, one source at a time, and it cannot answer a
question asked across the collection: *which sources ship a grammar*, *which
carry more than fifty test fixtures*, *what does a repository that publishes an
MCP server usually also contain*.

Those are questions about **data** — the individual components, registered and
logged, before anything was concluded from them. This module holds that layer.

Three properties follow from being the data layer and are worth stating,
because each is a decision that could have gone the other way:

**It is derived and disposable.** `.Data/surveys/*.json` is what was actually
fetched — a complete `git ls-tree` per repository at a known commit — and this
store is rebuilt from it. Deleting `source_components.sqlite` loses nothing,
exactly as with `catalogue_index.sqlite`. The surveys themselves are the
durable artefact and they are never edited.

**It draws no conclusions.** A row says `SigmaHQ/sigma has 459 paths matching
the fixtures signal`. It does not say that makes it a good source, does not
rank it, and does not decide what anyone should do about it. Conclusions are
information, they live in the notes, and a person wrote them.

**It is lighter than the prose it underpins.** An agent orienting in an
unfamiliar collection should be able to filter 128 sources structurally before
reading a single note — which is the cheap step, and the one that makes the
expensive step deliberate rather than exhaustive.

See `internal docs/Data Information Knowledge.md` for where this sits, and
`.Data/README.md` for the field-by-field dictionary.
"""
from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence

from .config import component_db_path, survey_dir

# Functions, not constants: a module constant is computed at import and cannot
# follow `CATALOGUE_VAULT`. See `config.vault_root`.
SURVEY_DIR = survey_dir
COMPONENT_DB = component_db_path
SCHEMA_VERSION = 1

COUNTED = re.compile(r"^(?P<name>.*?)\s*\((?P<count>\d+)\)$")

SCHEMA = """
CREATE TABLE IF NOT EXISTS source (
    repo_key   TEXT PRIMARY KEY,
    note       TEXT,
    cohort     TEXT NOT NULL,
    file_count INTEGER,
    language   TEXT,
    spdx       TEXT,
    stars      INTEGER,
    archived   INTEGER,
    pushed_at  TEXT
);
CREATE TABLE IF NOT EXISTS directory (
    repo_key TEXT NOT NULL,
    parent   TEXT,
    name     TEXT NOT NULL,
    files    INTEGER NOT NULL,
    depth    INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS extension (
    repo_key  TEXT NOT NULL,
    extension TEXT NOT NULL,
    files     INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS signal (
    repo_key TEXT NOT NULL,
    signal   TEXT NOT NULL,
    files    INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS signal_path (
    repo_key TEXT NOT NULL,
    signal   TEXT NOT NULL,
    path     TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS path (
    repo_key TEXT NOT NULL,
    path     TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS root_file (
    repo_key TEXT NOT NULL,
    name     TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
CREATE INDEX IF NOT EXISTS ix_dir_repo ON directory(repo_key);
CREATE INDEX IF NOT EXISTS ix_dir_name ON directory(name);
CREATE INDEX IF NOT EXISTS ix_ext_repo ON extension(repo_key);
CREATE INDEX IF NOT EXISTS ix_ext_name ON extension(extension);
CREATE INDEX IF NOT EXISTS ix_sig_repo ON signal(repo_key);
CREATE INDEX IF NOT EXISTS ix_sig_name ON signal(signal);
CREATE INDEX IF NOT EXISTS ix_sigpath_repo ON signal_path(repo_key);
CREATE INDEX IF NOT EXISTS ix_path_repo ON path(repo_key);
"""


@dataclass(frozen=True)
class BuildReport:
    sources: int
    directories: int
    extensions: int
    signals: int
    paths: int
    surveys: tuple[str, ...]
    skipped: tuple[str, ...] = ()


def _split_count(entry: str) -> tuple[str, int]:
    """`"docs (250)"` -> `("docs", 250)`. Both surveys store counts this way."""
    match = COUNTED.match(entry.strip())
    if not match:
        return entry.strip(), 0
    return match.group("name"), int(match.group("count"))


def _signal_rows(signals: Any) -> Iterator[tuple[str, int, list[str]]]:
    """Two survey formats, one shape out.

    The 2026-09-04 pass stored `{"n": count, "sample": [...]}`. The 2026-09-03
    pass stored the sample under `docs` and the real count under a companion
    key `docs__count`, as a single-element list of a string - so the sample is
    *truncated* and its length is not the count. Taking `len(sample)` there
    would have recorded ten tests for a repository with 847, silently and for
    64 of the 113 sources.

    Neither file is rewritten. The surveys are the record of what was actually
    fetched, and a record that gets normalised in place stops being one.
    """
    raw = signals or {}
    for name, value in raw.items():
        if name.endswith("__count"):
            continue
        if isinstance(value, dict):
            yield name, int(value.get("n") or 0), list(value.get("sample") or ())
            continue
        if not isinstance(value, list):
            continue
        sample = [str(x) for x in value[:10]]
        companion = raw.get(f"{name}__count")
        count = len(value)
        if isinstance(companion, list) and companion:
            try:
                count = int(str(companion[0]))
            except (TypeError, ValueError):
                pass
        elif isinstance(companion, (int, str)):
            try:
                count = int(companion)
            except (TypeError, ValueError):
                pass
        yield name, count, sample


def connect(db_path: Path | None = None) -> sqlite3.Connection:
    target = Path(db_path or component_db_path())
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(target)
    conn.row_factory = sqlite3.Row
    return conn


def build(survey_dir_override: Path | None = None,
          db_path: Path | None = None) -> BuildReport:
    """Rebuild the store from every survey. Idempotent, and safe to delete."""
    source_dir = Path(survey_dir_override or survey_dir())
    conn = connect(db_path)
    with conn:
        for table in ("source", "directory", "extension", "signal",
                      "signal_path", "path", "root_file", "meta"):
            conn.execute(f"DROP TABLE IF EXISTS {table}")
        conn.executescript(SCHEMA)

    counts = dict(sources=0, directories=0, extensions=0, signals=0, paths=0)
    surveys: list[str] = []
    skipped: list[str] = []

    for path in sorted(source_dir.glob("*-cohort.json")):
        cohort = path.stem.replace("-cohort", "")
        surveys.append(path.name)
        data = json.loads(path.read_text(encoding="utf-8"))
        with conn:
            for key, entry in data.items():
                if not isinstance(entry, dict) or entry.get("tree_error"):
                    skipped.append(f"{path.name}:{key}")
                    continue
                meta = entry.get("meta") or {}
                # The 2026-09-03 survey is keyed by note name and carries the
                # repo under `repo`; the 2026-09-04 one is keyed by repo_key
                # and carries the note name nowhere. Both are handled rather
                # than either file being rewritten.
                repo_key = meta.get("full_name") or entry.get("repo") or key
                note = entry.get("note") or (key if "/" not in key else None)
                conn.execute(
                    "INSERT OR REPLACE INTO source VALUES (?,?,?,?,?,?,?,?,?)",
                    (repo_key, note, cohort, entry.get("files"),
                     meta.get("language"), meta.get("spdx"), meta.get("stars"),
                     1 if meta.get("archived") else 0, meta.get("pushed")))
                counts["sources"] += 1

                for item in entry.get("top") or ():
                    name, files = _split_count(item)
                    conn.execute("INSERT INTO directory VALUES (?,?,?,?,?)",
                                 (repo_key, None, name, files, 1))
                    counts["directories"] += 1
                for parent, children in (entry.get("second") or {}).items():
                    for item in children:
                        name, files = _split_count(item)
                        conn.execute("INSERT INTO directory VALUES (?,?,?,?,?)",
                                     (repo_key, parent, name, files, 2))
                        counts["directories"] += 1
                for item in entry.get("extensions") or ():
                    name, files = _split_count(item)
                    conn.execute("INSERT INTO extension VALUES (?,?,?)",
                                 (repo_key, name, files))
                    counts["extensions"] += 1
                for name, files, sample in _signal_rows(entry.get("signals")):
                    conn.execute("INSERT INTO signal VALUES (?,?,?)",
                                 (repo_key, name, files))
                    counts["signals"] += 1
                    for sample_path in sample:
                        conn.execute("INSERT INTO signal_path VALUES (?,?,?)",
                                     (repo_key, name, sample_path))
                        counts["paths"] += 1
                # Present only in surveys written from 2026-09-05. Older ones
                # carry samples, so component retrieval reaches depth 1-2 for
                # them and the full tree for newer ones - a difference worth
                # knowing rather than papering over.
                for full_path in entry.get("paths") or ():
                    conn.execute("INSERT INTO path VALUES (?,?)",
                                 (repo_key, full_path))
                    counts["paths"] += 1
                for name in entry.get("root_files") or ():
                    conn.execute("INSERT INTO root_file VALUES (?,?)",
                                 (repo_key, name))
    with conn:
        conn.execute("INSERT OR REPLACE INTO meta VALUES ('schema_version', ?)",
                     (str(SCHEMA_VERSION),))
        conn.execute("INSERT OR REPLACE INTO meta VALUES ('surveys', ?)",
                     (json.dumps(surveys),))
    conn.close()
    return BuildReport(surveys=tuple(surveys), skipped=tuple(skipped), **counts)


# ------------------------------------------------------------------ the reads

def sources_with(signal: str, *, minimum: int = 1,
                 db_path: Path | None = None) -> list[dict[str, Any]]:
    """Which sources carry a given kind of material, and how much of it."""
    conn = connect(db_path)
    try:
        rows = conn.execute(
            "SELECT s.repo_key, s.note, g.files, s.file_count, s.language "
            "FROM signal g JOIN source s ON s.repo_key = g.repo_key "
            "WHERE g.signal = ? AND g.files >= ? ORDER BY g.files DESC",
            (signal, minimum)).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def sources_with_extension(extension: str, *, minimum: int = 1,
                           db_path: Path | None = None) -> list[dict[str, Any]]:
    conn = connect(db_path)
    try:
        rows = conn.execute(
            "SELECT s.repo_key, s.note, e.files, s.file_count "
            "FROM extension e JOIN source s ON s.repo_key = e.repo_key "
            "WHERE e.extension = ? AND e.files >= ? ORDER BY e.files DESC",
            (extension, minimum)).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def profile(repo_key: str, db_path: Path | None = None) -> dict[str, Any]:
    """Everything the data layer holds about one source. No conclusions."""
    conn = connect(db_path)
    try:
        row = conn.execute("SELECT * FROM source WHERE repo_key = ?",
                           (repo_key,)).fetchone()
        if row is None:
            return {}
        out: dict[str, Any] = dict(row)
        out["directories"] = [dict(r) for r in conn.execute(
            "SELECT parent, name, files FROM directory WHERE repo_key = ? "
            "ORDER BY depth, files DESC", (repo_key,))]
        out["extensions"] = [dict(r) for r in conn.execute(
            "SELECT extension, files FROM extension WHERE repo_key = ? "
            "ORDER BY files DESC", (repo_key,))]
        out["signals"] = [dict(r) for r in conn.execute(
            "SELECT signal, files FROM signal WHERE repo_key = ? "
            "ORDER BY files DESC", (repo_key,))]
        out["root_files"] = [r["name"] for r in conn.execute(
            "SELECT name FROM root_file WHERE repo_key = ?", (repo_key,))]
        return out
    finally:
        conn.close()


def vocabulary(db_path: Path | None = None) -> dict[str, list[tuple[str, int]]]:
    """What can be filtered on, and how many sources each value reaches.

    The first thing an unfamiliar agent should call: it answers *what are the
    axes here* without needing the schema, the documentation or a guess.
    """
    conn = connect(db_path)
    try:
        def tally(sql: str) -> list[tuple[str, int]]:
            return [(r[0], r[1]) for r in conn.execute(sql)]
        return {
            "signals": tally("SELECT signal, COUNT(DISTINCT repo_key) FROM signal "
                             "GROUP BY signal ORDER BY 2 DESC"),
            "extensions": tally("SELECT extension, COUNT(DISTINCT repo_key) FROM extension "
                                "GROUP BY extension ORDER BY 2 DESC LIMIT 40"),
            "languages": tally("SELECT COALESCE(language,'(none)'), COUNT(*) FROM source "
                               "GROUP BY 1 ORDER BY 2 DESC"),
            "cohorts": tally("SELECT cohort, COUNT(*) FROM source GROUP BY 1 ORDER BY 1"),
        }
    finally:
        conn.close()


def status(db_path: Path | None = None) -> dict[str, Any]:
    target = Path(db_path or component_db_path())
    if not target.exists():
        return {"present": False, "path": str(target)}
    conn = connect(db_path)
    try:
        counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                  for t in ("source", "directory", "extension", "signal",
                            "signal_path", "path", "root_file")}
        meta = {r["key"]: r["value"] for r in conn.execute("SELECT * FROM meta")}
        return {"present": True, "path": str(target), "counts": counts, "meta": meta}
    finally:
        conn.close()


def format_vocabulary(vocab: dict[str, list[tuple[str, int]]]) -> str:
    lines = ["What the data layer can be filtered on", ""]
    for axis, values in vocab.items():
        lines.append(f"  {axis}")
        for name, n in values[:24]:
            lines.append(f"      {name:<24} {n:>4} sources")
        lines.append("")
    return "\n".join(lines)
