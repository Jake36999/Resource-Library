"""Re-check what the catalogue claims against what is true now.

Every resource note records a moment: `github_pushed_at`, `github_stars`,
`archived`, a licence, a `maturity_stage`. All of it was captured on three days
in 2026, and until now nothing re-read any of it. A repository archived
tomorrow stays `Active` here indefinitely, and the catalogue has no way to know
it is wrong.

That is the difference between a catalogue and a photograph of one, and it is
the single thing a live GitHub search does better than this system.

## What this does and refuses to do

**It reports; it never edits a note.** A divergence is a *reading*, and a
reading is data — it belongs in `.Data`, alongside the surveys, under the same
rule as everything else in that layer: no conclusions. Whether a note should
change is a judgement, `MARKDOWN_IS_TRUTH` says the note is the authority, and
a background job quietly rewriting prose would break both.

So the output is a `freshness` row per source and a warning from `integrity`
when a note's claim and the world disagree. Someone then decides.

**It is cheap and it is conditional.** One `GET /repos/{owner}/{repo}` per
source, using the shared client so a token raises the ceiling from 60/hour to
5,000. `librarian freshness --stale-days 30` only re-checks what has not been
checked recently, so the routine case costs almost nothing.

## Which divergences matter

Not all of them. `stars` moves constantly and means nothing; `pushed_at` moving
is a repository being maintained, which is the normal case.

The ones that make a recorded claim *wrong* are: a repository that has been
archived while the note calls it active, a repository that has moved or been
deleted, and a licence that has changed. Those warn. Everything else is
recorded and reported without warning, because a catalogue that cries about
star counts trains its reader to ignore it.
"""
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

from . import notes as notes_mod
from .components import connect
from .config import component_db_path
from .config import vault_root

# A note whose `maturity_stage` says the project is alive. If the repository is
# archived and the note says one of these, the note is wrong.
LIVE_STAGES = frozenset({"Active", "Production_Ready"})

# Values GitHub uses to mean "we could not tell". Two of them, and treating
# them as different from each other produced a false divergence on the first
# run - `UNKNOWN -> NOASSERTION` is not a change, it is the same non-answer
# spelled two ways.
UNKNOWN_SPDX = frozenset({"", "UNKNOWN", "NOASSERTION", "NONE", "NULL"})

# `licence_stale_api_field` is recorded and does **not** warn. The first version
# had no such kind: it saw `github_license_spdx: UNKNOWN` against an API now
# reporting MIT and warned that `license_class` may be wrongly Unknown and the
# source silently withheld. For all six real cases that was false - the
# 2026-09-03 backfill had already resolved every one of them from LICENSE text,
# so `license_class` was `Permissive` and nothing was withheld. A check that
# overstates its own severity is how a warning list stops being read.
WARNING_KINDS = ("gone", "moved", "archived", "licence_changed",
                 "licence_undercaptured", "licence_withdrawn",
                 "licence_class_disagrees")

SCHEMA = """
CREATE TABLE IF NOT EXISTS freshness (
    repo_key    TEXT NOT NULL,
    note        TEXT,
    checked_at  TEXT NOT NULL,
    reachable   INTEGER NOT NULL,
    live_pushed TEXT,
    live_stars  INTEGER,
    live_spdx   TEXT,
    live_archived INTEGER,
    live_full_name TEXT,
    divergence  TEXT NOT NULL,
    PRIMARY KEY (repo_key, checked_at)
);
CREATE INDEX IF NOT EXISTS ix_fresh_repo ON freshness(repo_key);
"""


@dataclass(frozen=True)
class Reading:
    repo_key: str
    note: str
    checked_at: str
    reachable: bool
    live: dict[str, Any]
    divergence: tuple[dict[str, str], ...]

    @property
    def warns(self) -> bool:
        return any(d["kind"] in WARNING_KINDS for d in self.divergence)


@dataclass(frozen=True)
class FreshnessReport:
    readings: tuple[Reading, ...]
    skipped: int = 0
    stopped: str = ""

    @property
    def diverged(self) -> tuple[Reading, ...]:
        return tuple(r for r in self.readings if r.divergence)

    @property
    def warning(self) -> tuple[Reading, ...]:
        return tuple(r for r in self.readings if r.warns)


def ensure_schema(conn: sqlite3.Connection) -> None:
    with conn:
        conn.executescript(SCHEMA)


def catalogued(vault: Path | None = None) -> list[dict[str, Any]]:
    """What the notes claim, as the baseline a reading is compared against."""
    root = vault or vault_root()
    out: list[dict[str, Any]] = []
    for note in notes_mod.load_vault(root):
        if note.layer not in ("resource", "review"):
            continue
        repo_key = note.string("repo_key")
        if not repo_key:
            continue
        out.append({
            "repo_key": repo_key,
            "note": note.name,
            "pushed_at": note.string("github_pushed_at"),
            "stars": note.frontmatter.get("github_stars"),
            "spdx": note.string("github_license_spdx"),
            "license_class": note.string("license_class"),
            "maturity_stage": note.string("maturity_stage"),
            "captured": note.string("metadata_captured_at"),
        })
    return out


def compare(claim: dict[str, Any], live: dict[str, Any]) -> list[dict[str, str]]:
    """What changed, and whether it makes the note wrong.

    `kind` is what changed; membership of `WARNING_KINDS` is whether anybody
    needs to act. Separating those two means the set of things watched can grow
    without the set of things shouted about growing with it.
    """
    out: list[dict[str, str]] = []
    if not live:
        return [{"kind": "gone", "was": claim["repo_key"], "now": "unreachable",
                 "detail": "GitHub returned nothing for this repository"}]

    current_name = str(live.get("full_name") or "")
    if current_name and current_name.lower() != claim["repo_key"].lower():
        out.append({"kind": "moved", "was": claim["repo_key"], "now": current_name,
                    "detail": "the repository was renamed or transferred"})

    archived = bool(live.get("archived"))
    stage = claim.get("maturity_stage") or ""
    if archived and stage in LIVE_STAGES:
        out.append({"kind": "archived", "was": stage, "now": "archived",
                    "detail": "the note calls this maintained; upstream is read-only"})

    # Three different things were collapsed into one "licence changed" on the
    # first run, and the distinction decides what anybody should do about it.
    # The first real pass found `UNKNOWN -> MIT` on the 2026-08-31 cohort:
    # nothing upstream had changed, the note simply never captured a licence
    # that was there all along.
    live_spdx = str((live.get("license") or {}).get("spdx_id") or "").upper()
    was_spdx = str(claim.get("spdx") or "").upper()
    live_known = live_spdx not in UNKNOWN_SPDX
    was_known = was_spdx not in UNKNOWN_SPDX
    if live_known and not was_known:
        # Two very different situations, and only one of them costs anything.
        # `license_class` is the field `find_donor` eliminates on, so if it is
        # already resolved the source is answerable and the stale API field is
        # bookkeeping. If it is `Unknown`, the source really is being withheld.
        resolved = str(claim.get("license_class") or "").strip()
        # Does the resolved class actually agree with what the live SPDX means?
        # Assuming it does was the first version's second mistake: a note
        # resolved to `Permissive` against an API now reporting GPL-2.0 is the
        # genuinely dangerous case - a copyleft source offered to a
        # permissive-only query - and it would have been silently recorded as
        # bookkeeping.
        implied = ""
        try:
            from scout.rank import license_class as _classify

            implied = _classify(live_spdx)
        except Exception:
            implied = ""
        if resolved and implied and implied != "Unknown" and resolved != implied:
            out.append({
                "kind": "licence_class_disagrees", "was": resolved, "now": implied,
                "detail": f"the note resolves to {resolved} but the API reports "
                          f"{live_spdx}, which classifies as {implied}; "
                          f"`license_class` is what eliminates, so one of these "
                          f"is offering or withholding this source wrongly"})
        elif resolved and resolved != "Unknown":
            out.append({
                "kind": "licence_stale_api_field", "was": was_spdx or "(none)",
                "now": live_spdx,
                "detail": f"the API now reports a licence the note recorded as "
                          f"unknown, but `license_class` is already {resolved} "
                          f"from the LICENSE text - nothing is withheld; the "
                          f"snapshot field is simply out of date"})
        else:
            out.append({
                "kind": "licence_undercaptured", "was": was_spdx or "(none)",
                "now": live_spdx,
                "detail": "the API reports a licence the note never recorded and "
                          "`license_class` is Unknown, so this source is "
                          "eliminated from every constrained answer"})
    elif was_known and not live_known:
        out.append({"kind": "licence_withdrawn", "was": was_spdx,
                    "now": live_spdx or "(none)",
                    "detail": "the API no longer reports a licence it once did"})
    elif live_known and was_known and live_spdx != was_spdx:
        out.append({"kind": "licence_changed", "was": was_spdx, "now": live_spdx,
                    "detail": "the project relicensed, or the note is wrong"})

    live_pushed = str(live.get("pushed_at") or "")
    was_pushed = str(claim.get("pushed_at") or "")
    if live_pushed and was_pushed and live_pushed != was_pushed:
        out.append({"kind": "pushed", "was": was_pushed[:10], "now": live_pushed[:10],
                    "detail": "activity since the note was written"})

    live_stars = live.get("stargazers_count")
    was_stars = claim.get("stars")
    if isinstance(live_stars, int) and isinstance(was_stars, int):
        if was_stars and abs(live_stars - was_stars) / max(was_stars, 1) > 0.2:
            out.append({"kind": "stars", "was": str(was_stars), "now": str(live_stars),
                        "detail": "star count moved more than 20%"})
    return out


def last_checked(conn: sqlite3.Connection) -> dict[str, str]:
    ensure_schema(conn)
    return {r["repo_key"]: r["checked_at"] for r in conn.execute(
        "SELECT repo_key, MAX(checked_at) AS checked_at FROM freshness "
        "GROUP BY repo_key")}


def _age_days(stamp: str) -> float:
    try:
        when = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except ValueError:
        return 1e9
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - when).total_seconds() / 86400


def run(*, vault: Path | None = None, db_path: Path | None = None,
        stale_days: float = 7.0, limit: int | None = None,
        fetch: Any = None) -> FreshnessReport:
    """Re-check sources not seen recently. Writes readings; edits nothing.

    `fetch` is injected so the whole path is testable without a network, which
    is the pattern the rest of this package already uses for LM Studio and the
    toolchain.
    """
    if fetch is None:                              # imported lazily: scout is optional
        from scout.config import ScoutConfig
        from scout.discovery import fetch_repo

        cfg = ScoutConfig.load()

        def fetch(repo_key: str) -> dict[str, Any]:
            return fetch_repo(repo_key, cfg)

    conn = connect(db_path or component_db_path())
    ensure_schema(conn)
    seen = last_checked(conn)
    readings: list[Reading] = []
    skipped = 0
    stopped = ""
    try:
        for claim in catalogued(vault):
            previous = seen.get(claim["repo_key"])
            if previous and _age_days(previous) < stale_days:
                skipped += 1
                continue
            if limit is not None and len(readings) >= limit:
                skipped += 1
                continue
            try:
                live = fetch(claim["repo_key"]) or {}
            except Exception as exc:               # rate limit, network, anything
                stopped = str(exc)[:200]
                break
            now = datetime.now(timezone.utc).isoformat(timespec="seconds")
            divergence = compare(claim, live)
            reading = Reading(claim["repo_key"], claim["note"], now,
                              bool(live), live, tuple(divergence))
            readings.append(reading)
            with conn:
                conn.execute(
                    "INSERT OR REPLACE INTO freshness VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (reading.repo_key, reading.note, now, 1 if live else 0,
                     live.get("pushed_at"), live.get("stargazers_count"),
                     (live.get("license") or {}).get("spdx_id"),
                     1 if live.get("archived") else 0, live.get("full_name"),
                     json.dumps(divergence)))
    finally:
        conn.close()
    return FreshnessReport(tuple(readings), skipped, stopped)


def divergences(db_path: Path | None = None) -> list[dict[str, Any]]:
    """The latest reading per source, for anything that diverged.

    Read by `integrity.check_recorded_claims_are_current`, which is why this
    returns rows rather than printing: a check needs the note name.
    """
    target = Path(db_path or component_db_path())
    if not target.exists():
        return []
    conn = connect(target)
    try:
        ensure_schema(conn)
        rows = conn.execute(
            "SELECT f.* FROM freshness f JOIN (SELECT repo_key, "
            "MAX(checked_at) AS latest FROM freshness GROUP BY repo_key) m "
            "ON m.repo_key = f.repo_key AND m.latest = f.checked_at").fetchall()
    except sqlite3.OperationalError:
        return []
    finally:
        conn.close()
    out: list[dict[str, Any]] = []
    for row in rows:
        try:
            parsed = json.loads(row["divergence"] or "[]")
        except json.JSONDecodeError:
            parsed = []
        if parsed:
            out.append({"repo_key": row["repo_key"], "note": row["note"],
                        "checked_at": row["checked_at"], "divergence": parsed})
    return out


def format_report(report: FreshnessReport) -> str:
    lines = [f"checked {len(report.readings)}, skipped {report.skipped} "
             f"(recent enough), diverged {len(report.diverged)}, "
             f"needing attention {len(report.warning)}", ""]
    for reading in report.diverged:
        marks = [d for d in reading.divergence if d["kind"] in WARNING_KINDS]
        head = "  !!" if marks else "   ~"
        lines.append(f"{head} {reading.note or reading.repo_key}")
        for d in reading.divergence:
            flag = "*" if d["kind"] in WARNING_KINDS else " "
            lines.append(f"      {flag} {d['kind']:<9} {d['was']} -> {d['now']}")
    if report.stopped:
        lines += ["", f"  stopped early: {report.stopped}"]
    lines += ["", "  Nothing here was edited. A reading is data; whether a note "
              "should change is a judgement."]
    return "\n".join(lines)
