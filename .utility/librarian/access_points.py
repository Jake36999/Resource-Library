"""Access points - the one extract the design keeps.

Everything else taken from inside a source is ephemeral. Addresses are the
exception because they are pointers outward rather than copies inward: an API
endpoint, a dataset download root, an auth scheme and a rate limit answer
*what is where* directly, they are small, and they do not decay into
decontextualised fragments the way a code excerpt does.

The need is the one [[Application - Quantum Simulation Project]] recorded: a
project that matures from method-finding into data-gathering stops asking
"how is this done" and starts asking "where is the data and how do I reach
it". Nothing in a catalogue of repositories answers that unless addresses are
held deliberately.

Extraction is conservative. A URL that is a badge, a licence link or a
documentation homepage is not an access point, and recording it as one would
make the table exactly as useless as the noise it is meant to cut through.
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence

from . import index as index_mod
from . import notes as notes_mod
from . import policy
from .config import vault_root

URL = re.compile(r"https?://[^\s)>\]\"'`,]+")
WSS = re.compile(r"wss?://[^\s)>\]\"'`,]+")

# Hosts that are never an access point: badges, images, package pages, and the
# repository host itself. Without this list every README yields a dozen
# addresses that address nothing.
NOISE_HOSTS = (
    "shields.io", "badge", "travis-ci", "circleci", "codecov", "coveralls",
    "img.shields", "githubusercontent.com", "gravatar", "twitter.com",
    "linkedin.com", "youtube.com", "youtu.be", "slack.com", "discord",
    "opensource.org", "creativecommons.org", "gnu.org/licenses",
    "stackoverflow.com", "medium.com", "wikipedia.org",
)
NOISE_SUFFIXES = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".pdf")

KIND_RULES: tuple[tuple[str, re.Pattern], ...] = (
    ("graphql", re.compile(r"/graphql\b", re.I)),
    ("sparql", re.compile(r"/sparql\b", re.I)),
    ("websocket", re.compile(r"^wss?://", re.I)),
    ("feed", re.compile(r"/(rss|atom)(\.xml)?\b|\.rss$|\.atom$", re.I)),
    ("dataset_download", re.compile(
        r"\.(csv|parquet|geojson|ndjson|jsonl|zip|tar\.gz|nc|h5|hdf5)(\?|$)", re.I)),
    ("rest_api", re.compile(r"(^|//|\.)api\.|/api(/|$)|/v\d+(/|$)|/rest(/|$)", re.I)),
)

AUTH_RULES: tuple[tuple[str, re.Pattern], ...] = (
    ("oauth2", re.compile(r"\boauth\s*2?|authorization code flow", re.I)),
    ("api_key", re.compile(r"\bapi[ _-]?key\b|\baccess[ _-]?token\b|\bbearer\b", re.I)),
    ("basic", re.compile(r"\bbasic auth", re.I)),
    ("none", re.compile(r"\bno (?:auth|authentication|api key)\b|\bunauthenticated\b", re.I)),
)

RATE_LIMIT = re.compile(
    r"(\d[\d,]*)\s*(?:requests?|calls?|queries)\s*(?:per|/|a)\s*"
    r"(second|minute|min|hour|hr|day|month)", re.I)

FORMAT_TOKENS = ("json", "csv", "parquet", "geojson", "xml", "ndjson", "netcdf",
                 "hdf5", "arrow", "protobuf")

# How much text around a URL is read for auth and rate-limit hints. Wider and
# the nearest mention of "api key" belongs to a different endpoint.
CONTEXT_CHARS = 400

VERIFY_TIMEOUT = 10
USER_AGENT = "Resource-Library-Librarian/1.0"


@dataclass(frozen=True)
class AccessPoint:
    """Contract per spec 10.2."""

    id: str
    source: str
    kind: str
    url: str
    auth: str = "unknown"
    rate_limit: str = ""
    formats: tuple[str, ...] = ()
    description: str = ""
    verified_at: str = ""
    reachable: int | None = None      # 1 ok | 0 failed | None never checked
    notes: str = ""

    def as_row(self) -> tuple:
        return (self.id, self.source, self.kind, self.url, self.auth,
                self.rate_limit, json.dumps(list(self.formats)), self.description,
                self.verified_at or None, self.reachable, self.notes)


def make_id(source: str, url: str) -> str:
    return hashlib.sha256(f"{source}{url}".encode("utf-8")).hexdigest()[:16]


# ---------------------------------------------------------------- extraction

def _is_noise(url: str) -> bool:
    low = url.lower().rstrip(".,;")
    if any(host in low for host in NOISE_HOSTS):
        return True
    if low.endswith(NOISE_SUFFIXES):
        return True
    return False


def classify(url: str) -> str | None:
    for kind, pattern in KIND_RULES:
        if pattern.search(url):
            return kind
    return None


def _blocks(text: str) -> list[str]:
    """Paragraphs, because a paragraph is the unit an address is described in.

    A fixed character window around the URL was tried first and attributed one
    document's rate limit to four unrelated endpoints - and, cutting mid-token,
    read "100 per hour" as "00 per hour". Attributing a limit to the wrong
    endpoint is worse than recording no limit, so context stops at the
    paragraph boundary.
    """
    return [block for block in re.split(r"\n\s*\n", text or "") if block.strip()]


def _auth_from(context: str) -> str:
    for auth, pattern in AUTH_RULES:
        if pattern.search(context):
            return auth
    return "unknown"


def _rate_limit_from(context: str) -> str:
    match = RATE_LIMIT.search(context)
    return f"{match.group(1)} per {match.group(2).lower()}" if match else ""


def _formats_from(context: str) -> tuple[str, ...]:
    low = context.lower()
    return tuple(token for token in FORMAT_TOKENS if token in low)


def extract(text: str, source: str, *, description: str = "") -> list[AccessPoint]:
    """Pull addresses out of documentation.

    Only URLs that classify into a known kind survive. An unclassified URL is
    a link, not an address, and the difference is the whole value of the
    table.
    """
    found: dict[str, AccessPoint] = {}
    for block in _blocks(text):
        for match in list(URL.finditer(block)) + list(WSS.finditer(block)):
            url = match.group(0).rstrip(".,;:")
            if _is_noise(url):
                continue
            kind = classify(url)
            if kind is None:
                continue
            point = AccessPoint(
                id=make_id(source, url), source=source, kind=kind, url=url,
                auth=_auth_from(block), rate_limit=_rate_limit_from(block),
                formats=_formats_from(block) or _formats_from(url),
                description=description[:300],
                notes="extracted from documentation; not yet verified")
            found.setdefault(url, point)
    return list(found.values())


def from_note(note: notes_mod.Note) -> list[AccessPoint]:
    """Extract from a resource note, keyed by its repo_key where it has one."""
    source = note.string("repo_key") or note.name
    return extract(note.body, source, description=note.section("Bottom Line")[:200])


def scan_vault(vault: Path | None = None) -> list[AccessPoint]:
    root = Path(vault) if vault else vault_root()
    out: list[AccessPoint] = []
    for note in notes_mod.load_vault(root):
        if note.layer in {"resource", "review", "paper"}:
            out.extend(from_note(note))
    return out


# --------------------------------------------------------------------- store

def store(points: Iterable[AccessPoint], db_path: Path | None = None) -> int:
    """Upsert, preserving verification state.

    A re-scan must not blank `verified_at` and `reachable`: re-extracting the
    same address is not evidence that it stopped working.
    """
    conn = index_mod.connect(db_path)
    try:
        index_mod.init(conn)
        written = 0
        for point in points:
            existing = conn.execute(
                "SELECT verified_at, reachable FROM access_point WHERE id = ?",
                (point.id,)).fetchone()
            row = list(point.as_row())
            if existing:
                row[8] = existing["verified_at"]
                row[9] = existing["reachable"]
            conn.execute(
                "INSERT OR REPLACE INTO access_point(id, source, kind, url, auth, "
                "rate_limit, formats, description, verified_at, reachable, notes) "
                "VALUES(?,?,?,?,?,?,?,?,?,?,?)", tuple(row))
            written += 1
        conn.commit()
        return written
    finally:
        conn.close()


def all_points(db_path: Path | None = None, source: str | None = None) -> list[sqlite3.Row]:
    conn = index_mod.connect(db_path)
    try:
        index_mod.init(conn)
        if source:
            return conn.execute(
                "SELECT * FROM access_point WHERE source = ? ORDER BY kind, url",
                (source,)).fetchall()
        return conn.execute(
            "SELECT * FROM access_point ORDER BY source, kind, url").fetchall()
    finally:
        conn.close()


# -------------------------------------------------------------- verification

@dataclass(frozen=True)
class VerifyReport:
    checked: int = 0
    reachable: int = 0
    unreachable: int = 0
    skipped: int = 0
    failures: tuple[tuple[str, str], ...] = ()
    notes: tuple[str, ...] = field(default_factory=tuple)


def probe(url: str, timeout: int = VERIFY_TIMEOUT) -> tuple[bool, str]:
    """HEAD, then GET if the server dislikes HEAD.

    A 401 or 403 counts as reachable: an endpoint that demands a key is
    working, and recording it as dead would delete a usable address.
    """
    for method in ("HEAD", "GET"):
        request = urllib.request.Request(url, method=method)
        request.add_header("User-Agent", USER_AGENT)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return True, f"{method} {response.status}"
        except urllib.error.HTTPError as exc:
            if exc.code in (401, 403, 405, 429):
                return True, f"{method} {exc.code} (reachable, access controlled)"
            if method == "GET":
                return False, f"{method} {exc.code}"
        except Exception as exc:
            if method == "GET":
                return False, str(exc)[:160]
    return False, "no response"


def verify(db_path: Path | None = None, *, source: str | None = None,
           limit: int = 0, timeout: int = VERIFY_TIMEOUT,
           prober=None) -> VerifyReport:
    """Check reachability and record it.

    An unreachable endpoint is *flagged*, never dropped. A dropped address
    loses the knowledge that it once existed, which is exactly what somebody
    debugging a broken integration needs.
    """
    policy.check_action("access_point_verify")
    prober = prober or probe
    conn = index_mod.connect(db_path)
    try:
        index_mod.init(conn)
        sql = "SELECT id, url FROM access_point"
        params: list = []
        if source:
            sql += " WHERE source = ?"
            params.append(source)
        sql += " ORDER BY verified_at IS NOT NULL, verified_at"
        if limit:
            sql += " LIMIT ?"
            params.append(limit)
        rows = conn.execute(sql, params).fetchall()

        checked = ok = bad = 0
        failures: list[tuple[str, str]] = []
        stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        for row in rows:
            reachable, detail = prober(row["url"], timeout)
            conn.execute(
                "UPDATE access_point SET reachable = ?, verified_at = ?, notes = ? "
                "WHERE id = ?",
                (1 if reachable else 0, stamp, detail[:200], row["id"]))
            checked += 1
            if reachable:
                ok += 1
            else:
                bad += 1
                failures.append((row["url"], detail))
        conn.commit()
        return VerifyReport(checked=checked, reachable=ok, unreachable=bad,
                            failures=tuple(failures[:20]))
    finally:
        conn.close()


def refresh(vault: Path | None = None, db_path: Path | None = None,
            *, verify_after: bool = False) -> dict[str, int]:
    """Re-extract from the vault, then optionally re-verify."""
    points = scan_vault(vault)
    written = store(points, db_path)
    out = {"extracted": len(points), "stored": written}
    if verify_after:
        report = verify(db_path)
        out.update({"checked": report.checked, "reachable": report.reachable,
                    "unreachable": report.unreachable})
    return out
