"""The queue: sources someone is already using that the catalogue does not hold.

## Why this exists separately from a brief

A brief is *"find me something that does X"*. This is the other direction, and
it is the more common one: an agent is already using a repository, mid-task, and
the catalogue has never heard of it. The cost of stopping to chart it properly
is exactly high enough that nobody does, which is why a catalogue built beside
real work still ends up recording only the sources somebody set out to find.

So the price of logging one is a single call with a repo key and a sentence.
That is not a note and does not pretend to be — it is a **queue entry**, and the
standard enrichment path (fetch, survey, classify, stage, promote) runs over it
later, unattended, on a local model.

## What a queue entry may claim

Nothing. It records that someone used something and why they said they used it.
The `why` is first-hand and worth keeping — it is the only part of the eventual
note that comes from actual use rather than from a README — but it is stored as
*reported*, attributed to whoever reported it, and it never becomes a factual
field on its own.

`record_application` feeds this automatically: an application record naming a
resource the catalogue does not hold queues that resource rather than leaving a
dangling link. That is the whole point of the connection — the moment a source
proves useful is the moment worth catching it, and it costs the agent nothing.
"""
from __future__ import annotations

import json
import re
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import policy
from .config import data_root

QUEUED = "queued"
CLAIMED = "claimed"
PROPOSED = "proposed"
CATALOGUED = "catalogued"
SKIPPED = "skipped"
STATUSES = (QUEUED, CLAIMED, PROPOSED, CATALOGUED, SKIPPED)

# A claim held longer than this is assumed dead. An unattended run that is
# killed - and one will be - leaves its claim behind, and a queue that can only
# be unstuck by editing JSON is a queue that quietly stops draining.
STALE_CLAIM_SECONDS = 3600

REPO_KEY = re.compile(r"^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$")
URL_KEY = re.compile(r"github\.com/([A-Za-z0-9._-]+/[A-Za-z0-9._-]+)")


def queue_dir() -> Path:
    return data_root() / "queue"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(frozen=True)
class Entry:
    entry_id: str
    repo_key: str
    reported_by: str
    project: str = ""
    why: str = ""
    status: str = QUEUED
    created_at: str = ""
    claimed_by: str = ""
    claimed_at: str = ""
    proposal_id: str = ""
    note: str = ""
    resolution: str = ""
    sightings: int = 1

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def path(self) -> Path:
        return queue_dir() / f"{self.entry_id}.json"


def normalise(repo_key_or_url: str) -> str:
    """Accept what an agent actually has to hand.

    A project agent mid-task has a URL in its context, not a canonical key.
    Refusing the URL would mean it has to stop and transform one, and the
    entire design of this path is that logging costs nothing.
    """
    text = str(repo_key_or_url or "").strip().rstrip("/")
    if not text:
        return ""
    match = URL_KEY.search(text)
    if match:
        text = match.group(1)
    if text.endswith(".git"):
        text = text[:-4]
    return text if REPO_KEY.match(text) else ""


# ------------------------------------------------------------------ storage

def load(entry_id: str) -> Entry:
    path = queue_dir() / f"{entry_id}.json"
    if not path.exists():
        raise ValueError(f"no queue entry '{entry_id}'")
    return Entry(**json.loads(path.read_text(encoding="utf-8")))


def save(entry: Entry) -> Path:
    path = entry.path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(entry.to_dict(), indent=2, ensure_ascii=False),
                    encoding="utf-8")
    return path


def all_entries(status: str = "") -> list[Entry]:
    directory = queue_dir()
    if not directory.exists():
        return []
    out = []
    for path in sorted(directory.glob("*.json")):
        entry = Entry(**json.loads(path.read_text(encoding="utf-8")))
        if not status or entry.status == status:
            out.append(entry)
    return out


def find(repo_key: str) -> Entry | None:
    key = normalise(repo_key)
    for entry in all_entries():
        if entry.repo_key == key:
            return entry
    return None


# -------------------------------------------------------------------- the API

def log_use(repo_key_or_url: str, *, reported_by: str, project: str = "",
            why: str = "", vault: Path | None = None) -> dict[str, Any]:
    """Record that something was used. The cheapest write on the surface.

    Returns one of three answers, and the first is the useful one:

    - `catalogued` — it is already here, with the note. Go and read it.
    - `queued` — new; it is now in line for enrichment.
    - `seen_again` — already queued; the sighting count went up, because a
      source three projects reached for independently should be charted before
      one that nobody has touched twice.
    """
    from . import propose as propose_mod

    key = normalise(repo_key_or_url)
    if not key:
        raise ValueError(
            f"'{repo_key_or_url}' is not a repository. Give 'owner/repo' or a "
            f"github.com URL; anything else cannot be fetched later and would "
            f"queue work nobody can do.")

    existing_note = propose_mod.already_catalogued(key, vault)
    if existing_note:
        return {"status": CATALOGUED, "repo_key": key, "note": existing_note,
                "next": f"read it with `librarian note '{existing_note}'`"}

    seen = find(key)
    if seen:
        updated = Entry(**{**seen.to_dict(),
                           "sightings": seen.sightings + 1,
                           "why": seen.why or str(why).strip()})
        save(updated)
        return {"status": "seen_again", "repo_key": key,
                "entry_id": updated.entry_id, "sightings": updated.sightings}

    entry = Entry(
        entry_id=f"{re.sub(r'[^a-z0-9]+', '-', key.lower())}-{uuid.uuid4().hex[:6]}",
        repo_key=key, reported_by=str(reported_by), project=str(project),
        why=str(why).strip(), created_at=_now())
    save(entry)
    return {"status": QUEUED, "repo_key": key, "entry_id": entry.entry_id,
            "next": "enrichment will fetch, survey and stage it; nothing is "
                    "claimed about it until then"}


def queue_unknown(resources: list[str], *, reported_by: str, project: str = "",
                  why: str = "", vault: Path | None = None) -> list[dict[str, Any]]:
    """Queue whichever of these the catalogue does not already hold.

    Called by `record_application`, which is where this pays: the moment a
    source proved useful enough to write a record about is the moment it is
    worth charting, and the agent has already typed the name.
    """
    out = []
    for resource in resources or []:
        key = normalise(resource)
        if not key:
            # A resource named by note title rather than repo key is already
            # catalogued by definition - it had a note to name. Not an error.
            continue
        try:
            out.append(log_use(key, reported_by=reported_by, project=project,
                               why=why, vault=vault))
        except ValueError:                                  # pragma: no cover
            continue
    return out


def claim(entry_id: str, agent: str) -> Entry:
    entry = load(entry_id)
    if entry.status not in (QUEUED, CLAIMED):
        raise policy.PolicyError(
            policy.BRIEF_REQUIRED,
            f"{entry_id} is {entry.status}; only a queued entry can be worked.")
    updated = Entry(**{**entry.to_dict(), "status": CLAIMED,
                       "claimed_by": str(agent), "claimed_at": _now()})
    save(updated)
    return updated


def stale(entry: Entry, *, seconds: int = STALE_CLAIM_SECONDS) -> bool:
    """A claim nobody is working any more.

    An entry claimed before timestamps existed has no `claimed_at` and is
    treated as stale, which is the right default: it was claimed by a run that
    has certainly ended.
    """
    if entry.status != CLAIMED:
        return False
    if not entry.claimed_at:
        return True
    try:
        held = (datetime.now(timezone.utc)
                - datetime.fromisoformat(entry.claimed_at)).total_seconds()
    except ValueError:                                      # pragma: no cover
        return True
    return held > seconds


def workable(*, seconds: int = STALE_CLAIM_SECONDS) -> list[Entry]:
    """What a run may pick up: anything queued, plus abandoned claims.

    This is the resume story. A killed run does not have to be cleaned up
    before the next one starts; the next one simply takes back what nobody is
    holding.
    """
    return [e for e in all_entries()
            if e.status == QUEUED or stale(e, seconds=seconds)]


def release(entry_id: str, *, reason: str = "released by hand") -> Entry:
    """Hand a claim back without resolving the entry."""
    entry = load(entry_id)
    if entry.status != CLAIMED:
        raise ValueError(f"{entry_id} is {entry.status}, not claimed")
    updated = Entry(**{**entry.to_dict(), "status": QUEUED,
                       "claimed_by": "", "claimed_at": "",
                       "resolution": reason})
    save(updated)
    return updated


def resolve(entry_id: str, status: str, *, proposal_id: str = "",
            note: str = "", resolution: str = "") -> Entry:
    """Close an entry out. `skipped` needs a reason, for the same reason a
    rejected candidate does: it is the record that stops the next pass
    repeating this one."""
    if status not in STATUSES:
        raise ValueError(f"status must be one of {list(STATUSES)}")
    if status == SKIPPED and not str(resolution).strip():
        raise policy.PolicyError(
            policy.DISPOSITION_REQUIRED,
            f"skipping '{entry_id}' needs a reason - it is what stops the next "
            f"enrichment pass fetching this again.")
    entry = load(entry_id)
    updated = Entry(**{**entry.to_dict(), "status": status,
                       "proposal_id": str(proposal_id) or entry.proposal_id,
                       "note": str(note) or entry.note,
                       "resolution": str(resolution) or entry.resolution})
    save(updated)
    return updated


def summarise(entry: Entry) -> str:
    lines = [f"{entry.entry_id}  [{entry.status}]",
             f"  {entry.repo_key}"
             + (f"  x{entry.sightings}" if entry.sightings > 1 else "")]
    if entry.project or entry.reported_by:
        lines.append(f"  reported by {entry.reported_by or '?'}"
                     + (f" on {entry.project}" if entry.project else ""))
    if entry.why:
        lines.append(f"  why: {entry.why}")
    if entry.note:
        lines.append(f"  note: {entry.note}")
    if entry.resolution:
        lines.append(f"  resolution: {entry.resolution}")
    return "\n".join(lines)
