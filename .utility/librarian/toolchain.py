"""Adapter to the existing ToolSet. This module calls; it does not reimplement.

The catalogue's deep dive delegates to `run_guided_repository_investigation`,
which brings manifest validation, architecture checks, secret scanning and
session archiving for free. Item 5 of the build list is the one that deletes
code rather than adding it, and this is that item: everything below is
location, normalisation and degradation.

The ToolSet is on a different drive and may not be connected. Every entry
point here works with it absent, because a catalogue that cannot be consulted
when an optional subsystem is offline is worse than one that admits the gap.
"""
from __future__ import annotations

import importlib
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from . import policy
from .config import CatalogueConfig

# The event vocabulary the workflow emits (External Dependencies Reference 1.3).
GUIDED_STATUS_EVENTS = (
    "INTAKE_CREATED", "SCAN_COMPLETE",
    "MANIFEST_PASS", "MANIFEST_WARN", "MANIFEST_BLOCK",
    "REVIEW_REQUIRED", "SLICE_COMPLETE", "REPORT_COMPILED",
    "ARCHIVED", "ERROR",
)

MANIFEST_BLOCK = "MANIFEST_BLOCK"
POLICY_BLOCK = "POLICY_BLOCK"


@dataclass(frozen=True)
class InvestigationResult:
    """Contract per spec 9.4.

    `blocked_by` distinguishes a failed manifest from a refused approval
    because they need different responses - one is a bad source, the other is
    a missing decision - and a generic error hides which happened.
    """

    status: str                       # complete | blocked | review_required | error
    session_id: str = ""
    events: tuple[dict, ...] = ()
    slice_path: Path | None = None
    report_path: Path | None = None
    blocked_by: str | None = None     # MANIFEST_BLOCK | POLICY_BLOCK | None
    policy: dict | None = None
    artifacts: dict = field(default_factory=dict)
    detail: str = ""

    def event_names(self) -> list[str]:
        return [str(e.get("event", "")) for e in self.events]


# ---------------------------------------------------------------- locating it

def toolchain_root(cfg: CatalogueConfig | None = None) -> Path | None:
    """First candidate that actually contains the orchestration layer wins.

    The reference note records `F:\\Mark-XLVIII-main\\ToolSet`; the host
    currently has it under `D:\\Aletheia_project`. Probing rather than
    hard-coding means neither move breaks the adapter.
    """
    cfg = cfg or CatalogueConfig.load()
    candidates: list[str] = []
    env = os.environ.get("TOOLSET_ROOT")
    if env:
        candidates.append(env)
    if cfg.toolchain_root:
        candidates.append(cfg.toolchain_root)
    candidates.extend(cfg.toolchain_candidates)
    for candidate in candidates:
        path = Path(candidate)
        if (path / "local_tool_assist_mcp" / "workflow.py").exists():
            return path
    return None


def toolchain_available(cfg: CatalogueConfig | None = None) -> tuple[bool, str]:
    """Reachability plus a reason, so a missing drive is distinguishable from
    a present but broken install."""
    cfg = cfg or CatalogueConfig.load()
    root = toolchain_root(cfg)
    if root is None:
        tried = ", ".join([cfg.toolchain_root] + list(cfg.toolchain_candidates))
        return False, (f"ToolSet not found. Tried: {tried}. Connect the folder, or set "
                       f"TOOLSET_ROOT, before running an investigation.")
    slicer = root / "aletheia_toolchain" / "semantic_slicer_v7.0.py"
    if not slicer.exists():
        return False, (f"ToolSet found at {root} but the slicer is missing "
                       f"({slicer.name}); only scanning would work.")
    try:
        _load_workflow(root)
    except Exception as exc:
        return False, f"ToolSet at {root} failed to import: {exc}"
    return True, f"ToolSet available at {root}"


def _load_workflow(root: Path):
    """Import the workflow module from a path that is not on sys.path."""
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    module = importlib.import_module("local_tool_assist_mcp.workflow")
    return module


# ------------------------------------------------------------------ the call

def investigate(repo_path: Path, objective: str, *, allow_slice: bool = False,
                profile: str = "safe", output_root: str = "",
                cfg: CatalogueConfig | None = None,
                runner: Callable[..., dict] | None = None) -> InvestigationResult:
    """Run the guided investigation and normalise its result.

    `runner` is the injection point: tests pass a fake with the same shape, so
    no test needs the ToolSet, a repository or a subprocess. `profile` stays
    "safe" and `LTA_DEV_MODE` is never set - the session invariant
    `allow_command_execution == false` is what makes the intake safe to run
    unattended, and the workbench is where execution lives instead.
    """
    policy.check_action("investigate_repository")
    cfg = cfg or CatalogueConfig.load()
    target = Path(repo_path)

    if runner is None:
        ok, reason = toolchain_available(cfg)
        if not ok:
            return InvestigationResult(status="error", blocked_by=None, detail=reason)
        if not target.exists():
            return InvestigationResult(
                status="error",
                detail=f"target repository {target} does not exist; the toolchain "
                       f"works on a local path, so a source must be cloned first")
        root = toolchain_root(cfg)
        workflow = _load_workflow(root)
        runner = workflow.run_guided_repository_investigation

    root_for_output = output_root or cfg.toolchain_output_root or ""
    try:
        raw = runner(
            objective=objective,
            target_repo=str(target),
            profile=profile,
            allow_slice=allow_slice,
            output_root=root_for_output,
        )
    except Exception as exc:                                # pragma: no cover - defensive
        return InvestigationResult(status="error", detail=f"{type(exc).__name__}: {exc}")

    return normalise(raw, output_root=root_for_output, cfg=cfg)


def normalise(raw: dict[str, Any], *, output_root: str = "",
              cfg: CatalogueConfig | None = None) -> InvestigationResult:
    """Map the workflow's dict onto the contract, including the two blocks.

    The workflow returns `review_required` for both "you did not approve
    slicing" and "policy refused the slice", distinguished only by the
    presence of a `policy` dict. Collapsing them would lose the difference
    between a decision nobody made and a decision that was refused.
    """
    cfg = cfg or CatalogueConfig.load()
    status = str(raw.get("status", "error"))
    events = tuple(raw.get("events") or ())
    session_id = str(raw.get("session_id", ""))
    artifacts = dict(raw.get("artifacts") or {})
    policy_dict = raw.get("policy")

    names = [str(e.get("event", "")) for e in events]
    blocked_by: str | None = None
    if status == "blocked" or MANIFEST_BLOCK in names:
        blocked_by = MANIFEST_BLOCK
    elif status == "review_required" and policy_dict:
        blocked_by = POLICY_BLOCK

    slice_path = _slice_path(session_id, output_root, cfg)
    report = artifacts.get("final_markdown") or ""
    detail = str(raw.get("error") or "")
    if not detail and blocked_by == MANIFEST_BLOCK:
        detail = "manifest validation returned BLOCK; the source was not sliced"
    elif not detail and status == "review_required":
        detail = ("slicing needs approval; in Mode A a frozen cohort supplies it, "
                  "in Mode B a person does")

    return InvestigationResult(
        status=status, session_id=session_id, events=events,
        slice_path=slice_path if slice_path and slice_path.exists() else None,
        report_path=Path(report) if report else None,
        blocked_by=blocked_by, policy=policy_dict, artifacts=artifacts, detail=detail)


def _slice_path(session_id: str, output_root: str, cfg: CatalogueConfig) -> Path | None:
    """`semantic_slice.json` is not in the returned artifacts, so derive it.

    Layout, from `session.py`: `<output_root>/sessions/<id>/intermediate/`.
    """
    if not session_id:
        return None
    roots: list[Path] = []
    if output_root:
        roots.append(Path(output_root))
    env = os.environ.get("LTA_OUTPUT_ROOT")
    if env:
        roots.append(Path(env))
    root = toolchain_root(cfg)
    if root:
        roots.append(root / "local_tool_assist_outputs")
    for candidate in roots:
        path = candidate / "sessions" / session_id / "intermediate" / "semantic_slice.json"
        if path.exists():
            return path
    return roots[0] / "sessions" / session_id / "intermediate" / "semantic_slice.json" \
        if roots else None


# ------------------------------------------------------------------ evidence

def read_slice(slice_path: Path, *, max_symbols: int = 400) -> dict[str, Any]:
    """Summarise a slice for use as deep-dive evidence.

    Bounded on purpose: the slice is evidence for a description, not a payload
    to be stored. Nothing here is persisted - per spec 3.3 a slice is a
    component of a source, not a source, and it dies with the session that
    produced it.
    """
    import json

    try:
        data = json.loads(Path(slice_path).read_text(encoding="utf-8"))
    except Exception as exc:
        return {"available": False, "reason": str(exc)}

    slices = data.get("slices") or data.get("symbols") or []
    if isinstance(slices, dict):
        slices = list(slices.values())
    symbols: list[dict[str, Any]] = []
    for item in slices[:max_symbols]:
        if not isinstance(item, dict):
            continue
        symbols.append({
            "name": item.get("name") or item.get("symbol") or "",
            "kind": item.get("kind") or item.get("type") or "",
            "path": item.get("path") or item.get("file") or item.get("source_file") or "",
            "doc": (item.get("docstring") or item.get("doc") or "")[:300],
        })
    modules = sorted({s["path"] for s in symbols if s["path"]})
    return {"available": True, "symbol_count": len(slices),
            "modules": modules[:120], "symbols": symbols,
            "built_at_commit": data.get("built_at_commit", "")}
