"""The airlock: an outside agent may propose a resource note, never write one.

## What this makes safe

Four agents in four projects, told to research and log what they find, will
otherwise write markdown straight into `01-Resources/` with nothing checking it
until `librarian integrity` runs afterwards - by which point there are N
malformed notes and no record of which agent wrote them or from what evidence.
A thousand notes nobody can trust looks exactly like a thousand notes.

So contribution is two steps, and the split is not bureaucratic. It falls along
the line the vault already draws between layers:

| Step | Who | Produces | Where |
| --- | --- | --- | --- |
| `propose` | any agent, including a local model | **data** - structured fields, from fetched evidence | `.Data/staging/proposals/` |
| `promote` | a person, or a project agent that used it | **information** - the prose a reader consumes | `01-Resources/` |

Filling ten closed enumerations from a survey is constrained choice, and a small
local model does it well enough to be worth running for free. Writing the
Bottom Line is interpretation, and a small model will produce plausible mush
that passes every structural check there is. So `propose` accepts the first and
`promote` requires the second: **nothing reaches a reader without a sentence
somebody stands behind** (`INTERPRETATION_IS_NOT_MACHINE_WORK`).

## One validator, not two

Staged notes are checked by calling the *integrity checks themselves* on an
in-memory note, rather than by a second copy of the rules that will drift from
the first. `EVIDENCE_REQUIRED` is enforced here rather than asserted: a
proposal without a survey or a fetched metadata record is refused, because a
field nobody fetched is a guess.
"""
from __future__ import annotations

import json
import re
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import brief as brief_mod
from . import content_model, integrity, notes, policy
from .config import staging_dir, vault_root

# The prose a machine may not write. Everything else on a resource note is a
# fact from a survey; these are the parts a reader actually consumes, and they
# are the reason to keep a human in the loop at all.
INTERPRETIVE_SECTIONS = ("Bottom Line", "What It Solves")

# Sections a proposal may carry from evidence alone.
EVIDENCE_SECTIONS = ("What Is Inside", "Architecture & Mechanics",
                     "Integration & Use Cases")

STAGED = "staged"
PROMOTED = "promoted"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(frozen=True)
class Proposal:
    proposal_id: str
    repo_key: str
    canonical_url: str
    brief_id: str
    proposed_by: str
    axes: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    sections: dict[str, str] = field(default_factory=dict)
    evidence: dict[str, Any] = field(default_factory=dict)
    status: str = STAGED
    created_at: str = ""
    promoted_at: str = ""
    promoted_to: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def path(self) -> Path:
        return staging_dir() / f"{self.proposal_id}.json"


# ------------------------------------------------------------------ storage

def load(proposal_id: str) -> Proposal:
    path = staging_dir() / f"{proposal_id}.json"
    if not path.exists():
        raise ValueError(f"no staged proposal '{proposal_id}'")
    return Proposal(**json.loads(path.read_text(encoding="utf-8")))


def save(proposal: Proposal) -> Path:
    path = proposal.path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(proposal.to_dict(), indent=2, ensure_ascii=False),
                    encoding="utf-8")
    return path


def all_proposals(status: str = "") -> list[Proposal]:
    directory = staging_dir()
    if not directory.exists():
        return []
    out = []
    for path in sorted(directory.glob("*.json")):
        proposal = Proposal(**json.loads(path.read_text(encoding="utf-8")))
        if not status or proposal.status == status:
            out.append(proposal)
    return out


# ---------------------------------------------------------------- proposing

def note_name(repo_key: str) -> str:
    """`owner/repo` -> `owner - repo`, the convention already in the vault."""
    owner, _, repo = str(repo_key).partition("/")
    safe = re.sub(r"[^A-Za-z0-9 &_.-]", "", f"{owner} - {repo}" if repo else owner)
    return safe.strip()


def already_catalogued(repo_key: str, vault: Path | None = None) -> str:
    """The note that already covers this source, or "".

    Checked before staging rather than after promotion, because the point of
    the airlock is that the agent hears *this is already charted, here it is*
    while it can still act on that.
    """
    root = Path(vault) if vault else vault_root()
    key = str(repo_key).strip().lower()
    for path in (root / "01-Resources").glob("*.md"):
        try:
            frontmatter, _, _ = notes.parse_frontmatter(
                path.read_text(encoding="utf-8", errors="replace"))
        except OSError:                                     # pragma: no cover
            continue
        if str(frontmatter.get("repo_key", "")).strip().lower() == key:
            return path.stem
    return ""


def propose(repo_key: str, canonical_url: str, axes: dict[str, str],
            evidence: dict[str, Any], *, brief_id: str = "",
            proposed_by: str = "agent",
            metadata: dict[str, Any] | None = None,
            sections: dict[str, str] | None = None,
            vault: Path | None = None) -> Proposal:
    """Stage a candidate. Writes to `.Data/`, never to the vault.

    Refuses on four grounds, each by name: no evidence, an axis value outside
    its enumeration, a source already catalogued, or prose only a person should
    write.
    """
    policy.check_action("propose_resource")
    root = Path(vault) if vault else vault_root()

    key = str(repo_key).strip()
    if not key or "/" not in key:
        raise ValueError("repo_key must look like 'owner/repo'")

    # EVIDENCE_REQUIRED, enforced rather than asserted. A proposal whose fields
    # came from a model's recollection is exactly what this system exists not
    # to contain.
    if not _has_evidence(evidence):
        raise policy.PolicyError(
            policy.EVIDENCE_REQUIRED,
            "a proposal must carry evidence it was fetched: a survey (file "
            "listing), or a metadata record with a fetched_at. 'Unknown' is a "
            "valid field value; an unfetched claim is not.")

    existing = already_catalogued(key, root)
    if existing:
        raise policy.PolicyError(
            policy.STAGING_BEFORE_VAULT,
            f"'{key}' is already catalogued as [[{existing}]]. Read it, and if "
            f"it is wrong or stale, say so against that note rather than "
            f"proposing a second one.")

    given = dict(sections or {})
    intrusive = [s for s in INTERPRETIVE_SECTIONS if str(given.get(s, "")).strip()]
    if intrusive and proposed_by != "user":
        raise policy.PolicyError(
            policy.INTERPRETATION_IS_NOT_MACHINE_WORK,
            f"{intrusive} is the part a reader consumes and is written at "
            f"promotion, by whoever stands behind it. Propose the structured "
            f"fields and the evidence sections; leave the interpretation empty.")

    checked = _check_axes(dict(axes or {}), root)

    proposal = Proposal(
        proposal_id=f"{re.sub(r'[^a-z0-9]+', '-', key.lower())}-{uuid.uuid4().hex[:6]}",
        repo_key=key, canonical_url=str(canonical_url).strip(),
        brief_id=str(brief_id), proposed_by=str(proposed_by),
        axes=checked, metadata=dict(metadata or {}),
        sections={k: str(v).strip() for k, v in given.items()
                  if k in EVIDENCE_SECTIONS and str(v).strip()},
        evidence=dict(evidence), created_at=_now())
    save(proposal)

    if brief_id:
        brief_mod.add_candidate(brief_id, key, found_by=str(proposed_by))
        brief_mod.decide(brief_id, key, brief_mod.PROPOSED,
                         proposal_id=proposal.proposal_id)
    return proposal


def _has_evidence(evidence: dict[str, Any]) -> bool:
    if not isinstance(evidence, dict) or not evidence:
        return False
    if evidence.get("survey") or evidence.get("file_count"):
        return True
    return bool(evidence.get("fetched_at") and evidence.get("source"))


def _check_axes(axes: dict[str, str], vault: Path) -> dict[str, str]:
    """Closed enumerations, checked against the model the vault declares.

    `NO_SCHEMA_DRIFT`: an axis value nothing recognises does not create a new
    category, it removes the note from every constrained query - silently, and
    for as long as nobody looks.
    """
    model = content_model.load(vault)
    # Absent and broken are different failures, and `content_model` already
    # draws that line: a vault that never adopted the schema is not in
    # violation of it. Degrade there - a new library must be able to take its
    # first proposal - and raise on a model that exists and does not parse,
    # which is somebody's mistake.
    if model.error and not model.missing:
        raise ValueError(f"the note content model does not parse: {model.error}")
    if model.missing or not model.axis_values:
        return {k: str(v).strip() for k, v in axes.items() if str(v).strip()}

    out: dict[str, str] = {}
    for axis, value in axes.items():
        text = str(value).strip()
        if not text:
            continue
        permitted = model.axis_values.get(axis)
        if permitted is not None and text not in permitted:
            raise policy.PolicyError(
                policy.NO_SCHEMA_DRIFT,
                f"{axis}='{text}' is not in the enumeration. Permitted: "
                f"{sorted(permitted)}. Add it to [[Note Content Model]] "
                f"deliberately, or pick one of these.")
        out[axis] = text
    return out


# ----------------------------------------------------------------- promoting

def render(proposal: Proposal, sections: dict[str, str],
           vault: Path | None = None) -> str:
    """The note as it would be written. Rendered before it is validated."""
    model = content_model.load(Path(vault) if vault else vault_root())
    shape = model.shapes.get("resource")
    name = note_name(proposal.repo_key)
    meta = proposal.metadata or {}

    frontmatter: dict[str, Any] = {
        "uuid": str(uuid.uuid4()),
        "canonical_url": proposal.canonical_url,
        "repo_key": proposal.repo_key,
        "type": meta.get("type", "infrastructure_tool"),
        "primary_topic": meta.get("primary_topic", ""),
        "status": "active",
        "license": meta.get("license", "Unknown"),
    }
    frontmatter.update(proposal.axes)
    for key in ("github_stars", "github_pushed_at", "github_description",
                "github_language", "github_license_spdx", "github_topics",
                "github_default_branch", "github_homepage"):
        if key in meta:
            frontmatter[key] = meta[key]
    frontmatter["ingestion_agent"] = proposal.proposed_by
    frontmatter["metadata_captured_at"] = (
        proposal.evidence.get("fetched_at") or proposal.created_at)
    if proposal.brief_id:
        frontmatter["source_file"] = f"brief:{proposal.brief_id}"

    lines = ["---"]
    for key, value in frontmatter.items():
        lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}"
                     if isinstance(value, (list, dict, int, float))
                     else f'{key}: {json.dumps(str(value), ensure_ascii=False)}')
    lines += ["---", "", f"# {name}"]

    body = {**proposal.sections, **{k: v for k, v in sections.items() if v}}
    ordered = shape.ordered_sections if shape else tuple(body)
    for section in ordered:
        text = str(body.get(section, "")).strip()
        if section == "Taxonomy":
            text = text or _taxonomy_table(proposal.axes)
        elif section == "Evidence":
            text = text or _evidence_block(proposal)
        elif section == "GitHub Snapshot":
            text = text or _snapshot(meta)
        elif section == "Semantic Links":
            text = text or _links(frontmatter.get("primary_topic", ""))
        if not text:
            continue
        lines += ["", f"## {section}", text]
    lines.append("")
    return "\n".join(lines)


def _taxonomy_table(axes: dict[str, str]) -> str:
    rows = ["| Axis | Value |", "| --- | --- |"]
    rows += [f"| {axis} | {value} |" for axis, value in sorted(axes.items())]
    return "\n".join(rows)


def _evidence_block(proposal: Proposal) -> str:
    evidence = proposal.evidence or {}
    bits = [f"- Proposed by `{proposal.proposed_by}` on {proposal.created_at}."]
    if proposal.brief_id:
        bits.append(f"- Against brief `{proposal.brief_id}`.")
    if evidence.get("survey"):
        bits.append(f"- Survey: `{evidence['survey']}`.")
    if evidence.get("file_count"):
        bits.append(f"- {evidence['file_count']} files listed at "
                    f"{evidence.get('fetched_at', 'an unrecorded time')}.")
    if evidence.get("source"):
        bits.append(f"- Metadata from {evidence['source']}.")
    return "\n".join(bits)


def _snapshot(meta: dict[str, Any]) -> str:
    if not meta:
        return "- No GitHub metadata was captured."
    keys = [k for k in meta if k.startswith("github_")]
    return "\n".join(f"- `{k}`: {meta[k]}" for k in sorted(keys)) or \
        "- No GitHub metadata was captured."


def _links(topic: str) -> str:
    lines = ["- [taxonomy_hub:: [[Taxonomy Index]]]"]
    if topic:
        lines.insert(0, f"- [parent_topic:: [[Topic - {topic}]]]")
    return "\n".join(lines)


def validate(text: str, name: str, vault: Path | None = None) -> list[str]:
    """Run the vault's own integrity checks against a note that does not exist.

    Deliberately not a second copy of the rules. These are the same three
    functions `librarian integrity` runs, called on a one-note list, so a rule
    added there is enforced here without anybody remembering to mirror it.
    """
    root = Path(vault) if vault else vault_root()
    frontmatter, body, error = notes.parse_frontmatter(text)
    if error:
        return [f"frontmatter does not parse: {error}"]

    path = root / "01-Resources" / f"{name}.md"
    note = notes.Note(name=name, path=path, layer="resource",
                      type=str(frontmatter.get("type") or ""),
                      frontmatter=frontmatter, body=body, mtime=0.0)

    violations = []
    for check in (integrity.check_frontmatter_complete,
                  integrity.check_sections_complete,
                  integrity.check_axis_values_known):
        for violation in check(root, [note]):
            if violation.severity != integrity.WARNING:
                violations.append(violation.detail)
    return violations


def rederive(proposal: Proposal, vault: Path | None = None, *,
             paths: list[str] | None = None) -> dict[str, Any]:
    """Recompute the derivable axes on a staged proposal, from what it stored.

    A taxonomy change invalidates every proposal made before it. Six languages
    were added to `ecosystem` on 2026-09-09 and forty proposals staged that
    morning had the axis empty - not because the evidence was missing, but
    because the enumeration had nowhere to put it.

    Costs nothing: no model call, no network. It re-reads the metadata already
    on the proposal. A derived value always wins over a stored one, because a
    fact beats a guess and `derive` is the half that reads rather than asks.

    Only axes it can actually compute from stored metadata are touched -
    `hardware_footprint` and `security_compliance` need the full evidence text,
    which a proposal does not keep, so they are left exactly as they are.
    """
    from . import content_model, derive

    root = Path(vault) if vault else vault_root()
    permitted = content_model.load(root).axis_values
    fresh = derive.derive_axes(proposal.metadata or {}, {}, "",
                               paths=paths or (), repo_key=proposal.repo_key,
                               permitted=permitted)
    # Without the evidence text these two are not recomputable, and their
    # derivation would return a default that overwrote a better answer.
    fresh.pop("hardware_footprint", None)
    fresh.pop("security_compliance", None)
    if not paths:
        # Without a listing this would be a claim of absence rather than an
        # absence of evidence, and `None` is a permitted value on that axis.
        fresh.pop("agent_surface", None)

    changed = {axis: value for axis, value in fresh.items()
               if value and proposal.axes.get(axis) != value}
    if not changed:
        return {"proposal_id": proposal.proposal_id, "changed": {}}

    save(Proposal(**{**proposal.to_dict(),
                     "axes": {**proposal.axes, **changed}}))
    return {"proposal_id": proposal.proposal_id, "repo_key": proposal.repo_key,
            "changed": changed}


def readiness(proposal: Proposal, vault: Path | None = None) -> dict[str, Any]:
    """What this proposal still needs before it could be promoted.

    Computed by rendering the note with placeholder interpretation and running
    the vault's own checks over it. A proposal that can never be promoted is
    worse than a refused one, because it sits in staging looking finished -
    so the answer is produced at propose time, when the agent that fetched the
    evidence is still in a position to go and get the rest of it.
    """
    root = Path(vault) if vault else vault_root()
    text = render(proposal, {section: "placeholder"
                             for section in INTERPRETIVE_SECTIONS}, root)
    problems = validate(text, note_name(proposal.repo_key), root)
    model = content_model.load(root)
    out: dict[str, Any] = {"ready": not problems, "blocked_on": problems}
    if model.error:
        # "ready" with nothing checked is the silent pass this project keeps
        # having to design out. Say that the checks did not run.
        out["unchecked"] = (f"note shape was not validated: {model.error}")
    return out


def promote(proposal_id: str, bottom_line: str, what_it_solves: str, *,
            primary_topic: str = "", sections: dict[str, str] | None = None,
            promoted_by: str = "user", vault: Path | None = None,
            dry_run: bool = False) -> dict[str, Any]:
    """Move a staged proposal into the vault. The only call that writes truth.

    `bottom_line` and `what_it_solves` are required arguments rather than
    optional fields, because they are the whole reason this step exists: a note
    whose interpretation was generated is a note nobody has read.
    """
    policy.check_action("promote_proposal")
    root = Path(vault) if vault else vault_root()
    proposal = load(proposal_id)

    if proposal.status == PROMOTED:
        raise policy.PolicyError(
            policy.STAGING_BEFORE_VAULT,
            f"{proposal_id} was already promoted to {proposal.promoted_to}.")
    if not str(bottom_line).strip() or not str(what_it_solves).strip():
        raise policy.PolicyError(
            policy.INTERPRETATION_IS_NOT_MACHINE_WORK,
            "promotion requires a Bottom Line and What It Solves, written by "
            "whoever is standing behind this note. That sentence is what a "
            "reader acts on.")

    existing = already_catalogued(proposal.repo_key, root)
    if existing:
        raise policy.PolicyError(
            policy.STAGING_BEFORE_VAULT,
            f"'{proposal.repo_key}' was catalogued as [[{existing}]] since this "
            f"was staged. Reconcile the two rather than writing a duplicate.")

    if primary_topic:
        proposal = Proposal(**{**proposal.to_dict(),
                               "metadata": {**proposal.metadata,
                                            "primary_topic": primary_topic}})

    body = {"Bottom Line": str(bottom_line).strip(),
            "What It Solves": str(what_it_solves).strip(),
            **{k: str(v).strip() for k, v in (sections or {}).items()}}
    text = render(proposal, body, root)
    name = note_name(proposal.repo_key)

    problems = validate(text, name, root)
    if problems:
        return {"status": "rejected", "name": name, "violations": problems,
                "hint": "the note the vault would reject is the note this "
                        "would have written; fix the proposal and retry"}
    if dry_run:
        return {"status": "would_write", "name": name, "text": text}

    path = root / "01-Resources" / f"{name}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"{path.name} already exists")
    path.write_text(text, encoding="utf-8")

    save(Proposal(**{**proposal.to_dict(), "status": PROMOTED,
                     "promoted_at": _now(), "promoted_to": name}))

    refreshed = True
    try:
        from . import index as index_mod
        index_mod.refresh(root, None, since=0)
    except Exception:                                       # pragma: no cover
        refreshed = False
    return {"status": "written", "name": name, "path": str(path),
            "promoted_by": promoted_by, "index_refreshed": refreshed}
