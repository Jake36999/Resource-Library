"""Intake evidence: clone, investigate, read, discard.

This is what stage 5 of the pipeline calls instead of reading a README and
guessing. The sequence is fixed and short:

    shallow clone -> run_guided_repository_investigation -> read the slice
                  -> summarise -> delete the clone

What survives is a *summary* - module names, symbol counts, entry points -
which is evidence for a better description of the source. The slice itself is
not kept and not indexed: a slice is a component of a source, not a source,
and a permanent index of extracted symbols would be a snippet library ageing
independently of its origins (spec 3.3, decision 7.2).

Every failure degrades to "no slice evidence" and says why. A sweep must
never stop because one source could not be cloned.
"""
from __future__ import annotations

import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from . import clone as clone_mod
from . import toolchain as toolchain_mod
from .config import CatalogueConfig


@dataclass(frozen=True)
class SourceEvidence:
    """What a delegated investigation contributes to a dossier."""

    available: bool
    repo_key: str = ""
    status: str = ""
    reason: str = ""
    symbol_count: int = 0
    modules: tuple[str, ...] = ()
    entry_points: tuple[str, ...] = ()
    events: tuple[str, ...] = ()
    blocked_by: str | None = None
    slice_retained: bool = False        # always False; stated so it is checkable
    extra: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "available": self.available, "repo_key": self.repo_key,
            "status": self.status, "reason": self.reason,
            "symbol_count": self.symbol_count, "modules": list(self.modules),
            "entry_points": list(self.entry_points), "events": list(self.events),
            "blocked_by": self.blocked_by, "slice_retained": self.slice_retained,
        }


def investigate_source(repo_key_or_url: str, objective: str, *,
                       cfg: CatalogueConfig | None = None,
                       allow_slice: bool = True,
                       depth: int = 1,
                       investigator: Callable[..., Any] | None = None,
                       cloner: Callable[..., Any] | None = None) -> SourceEvidence:
    """Catalogue one source by delegating to the ToolSet.

    `investigator` and `cloner` are injection points so the whole path can be
    exercised with no network, no git and no ToolSet - which is what makes
    this testable at all.
    """
    cfg = cfg or CatalogueConfig.load()
    repo_key = repo_key_or_url.strip()

    if investigator is None:
        ok, reason = toolchain_mod.toolchain_available(cfg)
        if not ok:
            return SourceEvidence(False, repo_key, "unavailable", reason)
        investigator = toolchain_mod.investigate
    if cloner is None:
        ok, reason = clone_mod.git_available()
        if not ok:
            return SourceEvidence(False, repo_key, "unavailable", reason)
        cloner = clone_mod.shallow_clone

    workspace = Path(tempfile.mkdtemp(prefix="librarian-intake-"))
    checkout = workspace / "source"
    try:
        try:
            cloned = cloner(repo_key, checkout, depth=depth)
        except Exception as exc:
            return SourceEvidence(False, repo_key, "clone_failed", str(exc)[:300])

        result = investigator(Path(getattr(cloned, "path", checkout)), objective,
                              allow_slice=allow_slice, profile="safe", cfg=cfg)
        events = tuple(result.event_names())

        if result.status != "complete":
            return SourceEvidence(
                False, repo_key, result.status,
                result.detail or "investigation did not complete",
                events=events, blocked_by=result.blocked_by)

        if not result.slice_path:
            return SourceEvidence(
                False, repo_key, "complete",
                "investigation completed but produced no slice to read",
                events=events)

        summary = toolchain_mod.read_slice(result.slice_path)
        if not summary.get("available"):
            return SourceEvidence(False, repo_key, "complete",
                                  f"slice unreadable: {summary.get('reason', '')}",
                                  events=events)

        modules = tuple(summary.get("modules", ()))
        return SourceEvidence(
            True, repo_key, "complete", "",
            symbol_count=int(summary.get("symbol_count", 0)),
            modules=modules,
            entry_points=_entry_points(modules),
            events=events,
            extra={"built_at_commit": summary.get("built_at_commit", ""),
                   "symbols": summary.get("symbols", [])[:80]})
    finally:
        # The clone and everything under it go, whatever happened above.
        clone_mod.discard(workspace)


def _entry_points(modules: tuple[str, ...]) -> tuple[str, ...]:
    """A cheap guess at where a reader should start.

    Named `entry_points` rather than presented as fact: this is a heuristic
    over filenames, and the note should say so if it repeats it.
    """
    interesting = ("__main__", "main.", "cli.", "app.", "server.", "setup.py",
                   "pyproject.toml", "__init__.py")
    found = [m for m in modules if any(token in m.lower() for token in interesting)]
    return tuple(found[:10])


def evidence_block(evidence: SourceEvidence, limit: int = 1800) -> str:
    """Render the evidence for a model prompt, labelled untrusted.

    Bounded and labelled for the same reason the scout's README block is:
    fetched material describes a source, it does not instruct the reader.
    """
    if not evidence.available:
        return (f"STRUCTURE EVIDENCE: unavailable ({evidence.status}: "
                f"{evidence.reason}). Describe the source from documentation "
                f"alone and do not infer structure.")
    lines = [
        "STRUCTURE EVIDENCE (untrusted; derived from a semantic slice of the "
        "source, which has since been discarded):",
        f"- symbols found: {evidence.symbol_count}",
        f"- modules: {', '.join(evidence.modules[:40])}",
    ]
    if evidence.entry_points:
        lines.append(f"- likely entry points: {', '.join(evidence.entry_points)}")
    return "\n".join(lines)[:limit]
