"""Research briefs: what a project asked the library to find, and what came back.

## Why the request is the artefact

A project agent that says *"find me CSI sensing models"* will be handed RuView,
accurately charted and positively described, and will lose the same leg of the
same project a second time. The fact that disqualified RuView was never about
RuView: it was that its sense model assumes ESP32 input shape, and only
something that knows the project has an Intel 5300 knows to ask.

So a brief cannot be a topic list. It carries three things a topic list does
not:

- `constraints` - closed-vocabulary axis values, validated on the way in, that
  *eliminate* rather than re-rank. Same enums the catalogue itself uses.
- `disqualifiers` - free text, required, non-empty. The assumptions a candidate
  must not make. This is the RuView field.
- `coverage` - run at open time against what the catalogue already holds, so
  the requester learns immediately whether this needs research at all.

## Why closing a brief is where the value is

Every research session finds ten things and uses one. The nine are normally
lost, and next quarter somebody pays to rediscover that they do not work. A
brief cannot be closed until every candidate has a disposition, and a rejection
must carry a reason - so the by-product of doing the work is the negative
result nobody otherwise writes down.

`DOCUMENT_BEFORE_DESTROY`, one level up from the workbench: the same rule that
stops a sandbox being discarded before its record exists, applied to a research
session before its candidates are discarded.

Briefs live in `.Data/briefs/`. They are working state, never truth - a brief
records what was *asked*, and asserts nothing about any source.
"""
from __future__ import annotations

import json
import re
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import policy
from .config import brief_dir

OPEN = "open"
CLAIMED = "claimed"
CLOSED = "closed"

PROPOSED = "proposed"
REJECTED = "rejected"
DISCARDED = "discarded"
DISPOSITIONS = (PROPOSED, REJECTED, DISCARDED)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(frozen=True)
class Candidate:
    """One source considered against a brief.

    `disposition` empty means still open. A brief will not close while any
    candidate is in that state, because an undisposed candidate is exactly the
    thing that gets silently dropped.
    """

    repo_key: str
    found_by: str = ""
    note: str = ""
    disposition: str = ""
    reason: str = ""
    proposal_id: str = ""
    decided_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Brief:
    brief_id: str
    project: str
    need: str
    disqualifiers: tuple[str, ...]
    constraints: dict[str, list[str]] = field(default_factory=dict)
    status: str = OPEN
    created_at: str = ""
    created_by: str = ""
    claimed_by: str = ""
    claimed_at: str = ""
    closed_at: str = ""
    summary: str = ""
    coverage: dict[str, Any] = field(default_factory=dict)
    candidates: tuple[Candidate, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["disqualifiers"] = list(self.disqualifiers)
        payload["candidates"] = [c.to_dict() for c in self.candidates]
        return payload

    @property
    def undisposed(self) -> tuple[Candidate, ...]:
        return tuple(c for c in self.candidates if not c.disposition)

    def path(self) -> Path:
        return brief_dir() / f"{self.brief_id}.json"


# ------------------------------------------------------------------ storage

def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40] or "brief"


def _from_dict(payload: dict[str, Any]) -> Brief:
    candidates = tuple(Candidate(**c) for c in payload.get("candidates", ()))
    fields = {k: v for k, v in payload.items() if k != "candidates"}
    fields["disqualifiers"] = tuple(fields.get("disqualifiers") or ())
    return Brief(candidates=candidates, **fields)


def load(brief_id: str) -> Brief:
    path = brief_dir() / f"{brief_id}.json"
    if not path.exists():
        raise policy.PolicyError(
            policy.BRIEF_REQUIRED,
            f"no brief '{brief_id}'. Open one with `librarian brief open` "
            f"before proposing anything against it.")
    return _from_dict(json.loads(path.read_text(encoding="utf-8")))


def save(brief: Brief) -> Path:
    path = brief.path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(brief.to_dict(), indent=2, ensure_ascii=False),
                    encoding="utf-8")
    return path


def all_briefs(status: str = "") -> list[Brief]:
    directory = brief_dir()
    if not directory.exists():
        return []
    out = []
    for path in sorted(directory.glob("*.json")):
        try:
            brief = _from_dict(json.loads(path.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, TypeError) as exc:
            # A malformed brief is somebody's mistake and must not be skipped
            # quietly - that is how a request disappears without a trace.
            raise ValueError(f"{path.name} does not parse as a brief: {exc}") from exc
        if not status or brief.status == status:
            out.append(brief)
    return out


# ------------------------------------------------------------- the lifecycle

def open_brief(project: str, need: str, disqualifiers: list[str],
               constraints: dict[str, list[str]] | None = None, *,
               created_by: str = "agent",
               assess_coverage: bool = True) -> Brief:
    """State a need in a form the library can act on without guessing.

    `disqualifiers` is required and must be non-empty. A brief without one is
    a topic list, and a topic list is what produced the RuView outcome.
    """
    project = str(project).strip()
    need = str(need).strip()
    if not project or not need:
        raise ValueError("a brief needs both a project and a need")

    cleaned = [str(d).strip() for d in (disqualifiers or []) if str(d).strip()]
    if not cleaned:
        raise policy.PolicyError(
            policy.BRIEF_REQUIRED,
            "a brief must state at least one disqualifier - what a candidate "
            "must not assume, require or depend on. Without it this is a topic "
            "list, and a topic list cannot rule anything out.")

    checked = _check_constraints(constraints or {})
    brief = Brief(
        brief_id=f"{_slug(project)}-{uuid.uuid4().hex[:8]}",
        project=project, need=need,
        disqualifiers=tuple(cleaned), constraints=checked,
        created_at=_now(), created_by=str(created_by),
        coverage=_coverage(need, checked) if assess_coverage else {})
    save(brief)
    return brief


def _check_constraints(constraints: dict[str, list[str]]) -> dict[str, list[str]]:
    """Axis values are validated here, not at the point of search.

    A constraint that names a value outside its enumeration silently matches
    nothing, and a brief that asks for the impossible reads exactly like a brief
    nobody could satisfy (`NO_SCHEMA_DRIFT`, `FAILURE_MUST_BE_LOUD`).
    """
    from . import consult

    vocabulary = consult.axis_vocabulary()
    if not vocabulary:
        # A vault that has not adopted the content model has no enumeration to
        # check against, and refusing every constraint would make the first
        # brief in a new library impossible. Same degradation `integrity` and
        # `propose` already make: absent is not the same as violated.
        return {axis: [str(v).strip() for v in (values or []) if str(v).strip()]
                for axis, values in (constraints or {}).items()
                if any(str(v).strip() for v in (values or []))}

    out: dict[str, list[str]] = {}
    for axis, values in (constraints or {}).items():
        if axis not in vocabulary:
            raise ValueError(
                f"'{axis}' is not a filterable axis. Available: "
                f"{', '.join(sorted(vocabulary))}")
        wanted = [str(v).strip() for v in (values or []) if str(v).strip()]
        unknown = [v for v in wanted if v not in vocabulary[axis]]
        if unknown:
            raise ValueError(
                f"{axis} does not permit {unknown}; it permits "
                f"{sorted(vocabulary[axis])}")
        if wanted:
            out[axis] = wanted
    return out


def _coverage(need: str, constraints: dict[str, list[str]]) -> dict[str, Any]:
    """What the catalogue already holds for this need.

    Answered at open time so a brief that needs no research says so before
    anyone spends a model on it. Degrades to a note rather than failing: a
    missing index must not stop a request being recorded.
    """
    try:
        from . import consult, coverage as coverage_mod

        response = consult.find_donor(need, constraints, 5)
        verdict = coverage_mod.assess(need, response)
        return {
            "verdict": verdict.level,
            "already_catalogued": [r.name for r in response.results[:5]],
            "note": verdict.sentence(),
        }
    except (OSError, ValueError, RuntimeError, ImportError) as exc:
        # A missing or unbuilt index must not stop a request being recorded.
        # Deliberately not a bare `except`: this swallowed an attribute error
        # for a whole session and reported it as "coverage unknown", which is
        # the shape of silence this project keeps having to design out.
        return {"verdict": "unknown",
                "note": f"coverage not assessed: {exc}"}


def claim(brief_id: str, agent: str) -> Brief:
    """Take responsibility for a brief. One holder at a time."""
    brief = load(brief_id)
    if brief.status == CLOSED:
        raise policy.PolicyError(
            policy.BRIEF_REQUIRED,
            f"{brief_id} is closed; open a new brief rather than reopening one.")
    if brief.status == CLAIMED and brief.claimed_by != agent:
        raise policy.PolicyError(
            policy.BRIEF_REQUIRED,
            f"{brief_id} is already claimed by '{brief.claimed_by}'.")
    updated = _replace(brief, status=CLAIMED, claimed_by=str(agent),
                       claimed_at=_now())
    save(updated)
    return updated


def add_candidate(brief_id: str, repo_key: str, *, found_by: str = "",
                  note: str = "") -> Brief:
    """Register something worth considering. Cheap on purpose.

    Adding is free; *closing* is what costs, because every candidate added here
    must later be disposed of by name.
    """
    brief = load(brief_id)
    _require_open(brief)
    key = str(repo_key).strip()
    if not key:
        raise ValueError("a candidate needs a repo_key")
    if any(c.repo_key == key for c in brief.candidates):
        return brief
    candidate = Candidate(repo_key=key, found_by=str(found_by), note=str(note))
    updated = _replace(brief, candidates=brief.candidates + (candidate,))
    save(updated)
    return updated


def decide(brief_id: str, repo_key: str, disposition: str, *,
           reason: str = "", proposal_id: str = "") -> Brief:
    """Say what happened to one candidate.

    A rejection without a reason is refused. The reason is the entire point:
    *RuView's sense model assumes ESP32 input shape* is worth more to the next
    reader than most positive entries, and it exists only if written here.
    """
    brief = load(brief_id)
    _require_open(brief)
    if disposition not in DISPOSITIONS:
        raise ValueError(f"disposition must be one of {list(DISPOSITIONS)}")
    if disposition in (REJECTED, DISCARDED) and not str(reason).strip():
        raise policy.PolicyError(
            policy.DISPOSITION_REQUIRED,
            f"'{repo_key}' cannot be {disposition} without a reason. The reason "
            f"is the negative result - it is what stops the next search "
            f"repeating this one.")

    found = False
    candidates = []
    for candidate in brief.candidates:
        if candidate.repo_key == repo_key:
            found = True
            candidate = Candidate(
                repo_key=candidate.repo_key, found_by=candidate.found_by,
                note=candidate.note, disposition=disposition,
                reason=str(reason).strip(), proposal_id=str(proposal_id),
                decided_at=_now())
        candidates.append(candidate)
    if not found:
        raise ValueError(f"'{repo_key}' is not a candidate on {brief_id}; "
                         f"add it before deciding on it")
    updated = _replace(brief, candidates=tuple(candidates))
    save(updated)
    return updated


def close(brief_id: str, summary: str, *, discard_undisposed: bool = False,
          discard_reason: str = "not pursued") -> Brief:
    """End the session. Refuses while anything is undecided.

    `discard_undisposed` is the deliberate escape hatch, and it is not silent:
    it records each dropped candidate as `discarded` with a reason, so the
    brief still shows what was seen and let go.
    """
    brief = load(brief_id)
    if brief.status == CLOSED:
        raise policy.PolicyError(policy.BRIEF_REQUIRED,
                                 f"{brief_id} is already closed.")
    if not str(summary).strip():
        raise policy.PolicyError(
            policy.DISPOSITION_REQUIRED,
            "closing a brief requires a summary of what was found and what it "
            "means for the asking project.")

    pending = brief.undisposed
    if pending and not discard_undisposed:
        raise policy.PolicyError(
            policy.DISPOSITION_REQUIRED,
            f"{len(pending)} candidate(s) have no disposition: "
            f"{', '.join(c.repo_key for c in pending)}. Decide each one, or "
            f"close with discard_undisposed=True to drop them on the record.")

    candidates = tuple(
        c if c.disposition else Candidate(
            repo_key=c.repo_key, found_by=c.found_by, note=c.note,
            disposition=DISCARDED, reason=discard_reason, decided_at=_now())
        for c in brief.candidates)

    updated = _replace(brief, candidates=candidates, status=CLOSED,
                       closed_at=_now(), summary=str(summary).strip())
    save(updated)
    return updated


def _require_open(brief: Brief) -> None:
    if brief.status == CLOSED:
        raise policy.PolicyError(
            policy.BRIEF_REQUIRED,
            f"{brief.brief_id} is closed and cannot take further work.")


def _replace(brief: Brief, **changes: Any) -> Brief:
    payload = brief.to_dict()
    payload.update({k: v for k, v in changes.items() if k != "candidates"})
    candidates = changes.get("candidates", brief.candidates)
    payload["candidates"] = [c.to_dict() for c in candidates]
    return _from_dict(payload)


# -------------------------------------------------------------------- report

def summarise(brief: Brief) -> str:
    """What this brief cost and what it bought, in prose."""
    lines = [f"{brief.brief_id}  [{brief.status}]",
             f"  project     {brief.project}",
             f"  need        {brief.need}"]
    if brief.constraints:
        rendered = "; ".join(f"{a}={'|'.join(v)}"
                             for a, v in sorted(brief.constraints.items()))
        lines.append(f"  constraints {rendered}")
    for index, item in enumerate(brief.disqualifiers):
        lines.append(f"  {'rules out' if index == 0 else '         '}   {item}")
    if brief.coverage:
        lines.append(f"  coverage    {brief.coverage.get('verdict', '?')} - "
                     f"{brief.coverage.get('note', '')}")
    for candidate in brief.candidates:
        mark = {PROPOSED: "+", REJECTED: "-", DISCARDED: "~"}.get(
            candidate.disposition, "?")
        detail = candidate.reason or candidate.proposal_id or "undecided"
        lines.append(f"    {mark} {candidate.repo_key}: {detail}")
    if brief.summary:
        lines.append(f"  summary     {brief.summary}")
    return "\n".join(lines)
