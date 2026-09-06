"""Mode D - the workbench.

An ephemeral sandbox holding one source while a person actually engages with
it, destroyed once the value has been written down. A hundred repositories are
read; none are kept.

The workbench is a **separate subsystem with its own policy**, not a loosened
intake. The intake never executes fetched code and its session invariant
`allow_command_execution == false` is untouched. Execution lives here instead,
under different rules: person-initiated only, isolated, ephemeral, and
unreachable from Mode A or Mode C.

Executing code from repositories found by automated scouting is the highest
risk operation in the system. Three controls, and they are why this mode is
separate rather than folded into the intake:

    never during a sweep   - unattended execution of unreviewed code is the
                             failure this design exists to prevent
    no credentials, ever   - the sandbox never sees the token set
    network off by default - exfiltration and dependency confusion both need
                             egress, so egress is a decision, not an assumption

None of this makes running unknown code safe. It makes the blast radius a
container that was going to be destroyed anyway.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from . import clone as clone_mod
from . import policy
from .config import CatalogueConfig, WORKBENCH_ROOT, vault_root

# Set by the sweep entry point. `open()` refuses while it is set, which is the
# runtime half of "open must be unreachable from Mode A"; the other half is
# that the sweep path does not import this module at all.
MODE_ENV = "LIBRARIAN_MODE"
SWEEP_MODES = {"sweep", "mode_a", "unattended"}

STATE_FILE = "workbench.json"


class WorkbenchRefused(RuntimeError):
    """A refusal that names the rule. Never a bare failure."""

    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


@dataclass(frozen=True)
class Workbench:
    """Contract per spec 9.5."""

    id: str
    repo_key: str
    container: str
    path: Path
    opened_at: str
    documented: bool = False
    network: str = "none"
    record_path: str = ""
    notes: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {"id": self.id, "repo_key": self.repo_key, "container": self.container,
                "path": str(self.path), "opened_at": self.opened_at,
                "documented": self.documented, "network": self.network,
                "record_path": self.record_path, "notes": list(self.notes)}


@dataclass(frozen=True)
class CloseResult:
    """Contract per spec 9.5."""

    persisted: tuple[str, ...] = ()
    destroyed: tuple[str, ...] = ()
    refused: str | None = None
    detail: str = ""


# ------------------------------------------------------------------- state

def _root() -> Path:
    root = Path(os.environ.get("LIBRARIAN_WORKBENCH_ROOT", WORKBENCH_ROOT))
    root.mkdir(parents=True, exist_ok=True)
    return root


def _dir(workbench_id: str) -> Path:
    return _root() / workbench_id


def _save(bench: Workbench) -> None:
    path = _dir(bench.id)
    path.mkdir(parents=True, exist_ok=True)
    (path / STATE_FILE).write_text(json.dumps(bench.as_dict(), indent=2),
                                   encoding="utf-8")


def _load(workbench_id: str) -> Workbench:
    state = _dir(workbench_id) / STATE_FILE
    if not state.exists():
        raise WorkbenchRefused("NO_SUCH_WORKBENCH",
                               f"no workbench '{workbench_id}'. `list()` shows open ones.")
    data = json.loads(state.read_text(encoding="utf-8"))
    return Workbench(id=data["id"], repo_key=data["repo_key"],
                     container=data["container"], path=Path(data["path"]),
                     opened_at=data["opened_at"], documented=bool(data["documented"]),
                     network=data.get("network", "none"),
                     record_path=data.get("record_path", ""),
                     notes=tuple(data.get("notes", ())))


def list_open() -> list[Workbench]:
    out = []
    for path in sorted(_root().glob("*/" + STATE_FILE)):
        try:
            out.append(_load(path.parent.name))
        except Exception:                                   # pragma: no cover
            continue
    return out


def status(workbench_id: str) -> Workbench:
    return _load(workbench_id)


# --------------------------------------------------------------- the sandbox

def container_available(cfg: CatalogueConfig | None = None) -> tuple[bool, str]:
    cfg = cfg or CatalogueConfig.load()
    runtime = cfg.container_runtime
    if shutil.which(runtime) is None:
        return False, (f"{runtime} is not on PATH. A container is the isolation "
                       f"boundary; a bare virtualenv is not sufficient, since it "
                       f"isolates packages but not the filesystem.")
    try:
        completed = subprocess.run([runtime, "info", "--format", "{{.ServerVersion}}"],
                                   capture_output=True, text=True, timeout=20)
    except Exception as exc:                                # pragma: no cover
        return False, f"{runtime} did not respond: {exc}"
    if completed.returncode != 0:
        return False, (f"{runtime} is installed but not running "
                       f"({(completed.stderr or '').strip()[:160]}). Start Docker "
                       f"Desktop before opening a workbench.")
    return True, f"{runtime} {completed.stdout.strip()} available"


def _run_command(cfg: CatalogueConfig, workbench_id: str, mount: Path) -> list[str]:
    """The container command, built here in code.

    Every flag is a control, not a preference:
      --network none      egress off by default
      --env-file /dev/null / no -e   the token set never enters
      --memory --cpus     a runaway process cannot take the machine down
      --user              non-root inside
      -v <workbench>:...  the only host path visible
    """
    return [
        cfg.container_runtime, "run", "--detach", "--rm",
        "--name", f"librarian-{workbench_id}",
        "--network", "none",
        "--memory", cfg.workbench_memory,
        "--cpus", cfg.workbench_cpus,
        "--user", "1000:1000",
        "--workdir", "/work",
        "--volume", f"{mount}:/work",
        cfg.workbench_image,
        "sleep", "infinity",
    ]


def _docker(args: list[str], timeout: int = 120) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout)


# --------------------------------------------------------------------- open

def open(repo_key: str, *, depth: int = 1, cfg: CatalogueConfig | None = None,
         cloner: Callable[..., Any] | None = None,
         runner: Callable[[list[str], int], Any] | None = None,
         allow_no_container: bool = False) -> Workbench:
    """Shallow clone into a sandbox and hand back a live environment.

    Refuses outright during a sweep. `allow_no_container=True` exists for a
    host without Docker and is recorded on the workbench, because an
    engagement that ran on the host filesystem is a different fact from one
    that ran in a container and the record must not blur them.
    """
    policy.check_action("workbench_open")
    mode = os.environ.get(MODE_ENV, "").strip().lower()
    if mode in SWEEP_MODES:
        raise WorkbenchRefused(
            policy.EXECUTION_SANDBOX_ONLY,
            "a sweep may not open a workbench. Mode A is unattended, and "
            "unattended execution of unreviewed code is the one thing this "
            "design must never do.")

    cfg = cfg or CatalogueConfig.load()
    runner = runner or _docker
    workbench_id = f"{_slug(repo_key)}-{uuid.uuid4().hex[:8]}"
    path = _dir(workbench_id)
    path.mkdir(parents=True, exist_ok=True)
    checkout = path / "source"
    notes: list[str] = []

    try:
        cloner = cloner or clone_mod.shallow_clone
        cloner(repo_key, checkout, depth=depth)
    except Exception as exc:
        shutil.rmtree(path, ignore_errors=True)
        raise WorkbenchRefused("CLONE_FAILED", str(exc)[:300]) from exc

    container = ""
    ok, reason = (True, "") if runner is not _docker else container_available(cfg)
    if ok:
        completed = runner(_run_command(cfg, workbench_id, path), 180)
        if getattr(completed, "returncode", 1) == 0:
            container = (getattr(completed, "stdout", "") or "").strip()[:64]
        else:
            reason = (getattr(completed, "stderr", "") or "").strip()[:200]
            ok = False
    if not ok:
        if not allow_no_container:
            clone_mod.discard(path)
            raise WorkbenchRefused(
                policy.EXECUTION_SANDBOX_ONLY,
                f"no sandbox available ({reason}). Fetched code runs only inside a "
                f"workbench sandbox; pass allow_no_container=True to read the clone "
                f"without running it.")
        notes.append(f"no container: {reason}. Read-only engagement; do not execute "
                     f"anything from this clone.")

    bench = Workbench(id=workbench_id, repo_key=repo_key, container=container,
                      path=path, opened_at=_now(), documented=False,
                      network="none", notes=tuple(notes))
    _save(bench)
    return bench


def _slug(value: str) -> str:
    return "".join(ch if ch.isalnum() else "-" for ch in value).strip("-").lower()[:40]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ----------------------------------------------------------------- document

def document(workbench_id: str, record: dict[str, Any], *,
             vault: Path | None = None, db_path: Path | None = None,
             attested_by: str = "user") -> Path:
    """Write the application record. Required before `close` will destroy anything.

    This is the mechanism that makes records accumulate: the record is not a
    chore to remember afterwards, it is the price of closing the workbench.
    """
    policy.check_action("workbench_document")
    from . import consult

    bench = _load(workbench_id)
    payload = dict(record)
    payload.setdefault("resources_used", [payload.get("project", bench.repo_key)])
    written = consult.record_application(payload, vault=vault, db_path=db_path,
                                         attested_by=attested_by)
    _save(Workbench(**{**bench.as_dict(), "path": bench.path,
                       "documented": True, "record_path": written["path"],
                       "notes": bench.notes}))
    return Path(written["path"])


# -------------------------------------------------------------------- close

def close(workbench_id: str, *, force: bool = False, reason: str = "",
          cfg: CatalogueConfig | None = None,
          runner: Callable[[list[str], int], Any] | None = None) -> CloseResult:
    """Persist the artefacts, destroy everything else.

    Without a record this refuses and changes nothing. `force=True` exists for
    a genuinely abandoned engagement and is logged with its reason, because a
    forced close is the one path that loses what was learned.
    """
    policy.check_action("workbench_close")
    cfg = cfg or CatalogueConfig.load()
    runner = runner or _docker
    bench = _load(workbench_id)

    if not bench.documented and not force:
        return CloseResult(
            refused=policy.DOCUMENT_BEFORE_DESTROY,
            detail=("this workbench has no application record. The value is "
                    "extracted before the sandbox is discarded, or it is lost. "
                    "Call document() first, or close(force=True, reason=...)."))
    if force and not reason:
        return CloseResult(
            refused="FORCE_REQUIRES_REASON",
            detail="a forced close discards what was learned; say why in `reason`.")

    persisted: list[str] = []
    if bench.record_path:
        persisted.append(bench.record_path)

    destroyed: list[str] = []
    if bench.container:
        completed = runner([cfg.container_runtime, "rm", "--force",
                            f"librarian-{bench.id}"], 120)
        if getattr(completed, "returncode", 1) == 0:
            destroyed.append(f"container librarian-{bench.id}")
        else:                                               # pragma: no cover
            destroyed.append(f"container librarian-{bench.id} (already gone)")

    # The clone, the virtualenv, the caches and any graph built inside go
    # together. Teardown runs even when the engagement errored, because a
    # sandbox left behind is a sandbox that stops being ephemeral.
    if clone_mod.discard(bench.path):
        destroyed.append(f"clone and sandbox state at {bench.path}")
    else:                                                   # pragma: no cover
        return CloseResult(persisted=tuple(persisted), destroyed=tuple(destroyed),
                           refused="TEARDOWN_INCOMPLETE",
                           detail=f"could not remove {bench.path}; it still exists")

    if force:
        _log_force(bench, reason)
    return CloseResult(persisted=tuple(persisted), destroyed=tuple(destroyed),
                       detail="forced" if force else "")


def _log_force(bench: Workbench, reason: str) -> None:
    from .config import LOG_DIR
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with (LOG_DIR / "workbench_force_close.log").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"id": bench.id, "repo_key": bench.repo_key,
                                 "opened_at": bench.opened_at, "closed_at": _now(),
                                 "reason": reason}) + "\n")


# ------------------------------------------------- mapping and closure (4B.2)

@dataclass(frozen=True)
class ClosureSummary:
    """What persists from a mapping run: prose, not a symbol graph.

    "The scheduler isolates to nine files and four packages, entry point X" is
    a descriptor of the source and belongs in its note. A stored dependency
    graph of its symbols would be a component library by another name.
    """

    target: str
    files: tuple[str, ...] = ()
    packages: tuple[str, ...] = ()
    unresolved: tuple[str, ...] = ()
    confidence: float = 0.0
    backend: str = "none"
    reason: str = ""

    def prose(self) -> str:
        if not self.files:
            return (f"Closure for '{self.target}' could not be computed "
                    f"({self.reason or 'no graph'}).")
        packages = (f", and {len(self.packages)} package(s): "
                    f"{', '.join(sorted(self.packages)[:8])}") if self.packages else ""
        caveat = (f" {len(self.unresolved)} edge(s) are unresolved (dynamic imports "
                  f"or plugin lookups), so treat this as a floor, not a total."
                  if self.unresolved else "")
        return (f"'{self.target}' isolates to {len(self.files)} file(s){packages}. "
                f"Confidence {self.confidence:.2f}.{caveat}")


def map_source(workbench_id: str, target: str = "", *,
               cfg: CatalogueConfig | None = None,
               runner: Callable[..., Any] | None = None) -> ClosureSummary:
    """Graph the clone with graphify, inside the workbench only.

    Permitted use 2 (spec 4B.2). The graph is written under the workbench
    directory and dies with it: `NO_PERSISTENT_SOURCE_GRAPH` means no graph of
    a catalogued source outlives the workbench that built it. There is no
    second closure implementation - graphify's `calls`, `imports` and
    `contains` edges are dependency closure already.
    """
    policy.check_action("graphify_query")
    from . import graph as graph_mod

    cfg = cfg or CatalogueConfig.load()
    bench = _load(workbench_id)
    source = bench.path / "source"
    ok, reason = graph_mod.graphify_available(cfg)
    if not ok:
        return ClosureSummary(target=target or bench.repo_key, reason=reason)

    binary = graph_mod._binary(cfg)
    runner = runner or (lambda args, timeout: subprocess.run(
        args, capture_output=True, text=True, timeout=timeout))
    completed = runner([binary, "update", str(source), "--no-cluster"],
                       max(cfg.graphify_timeout_seconds, 300))
    if getattr(completed, "returncode", 1) != 0:
        return ClosureSummary(target=target or bench.repo_key, backend="graphify",
                              reason=(getattr(completed, "stderr", "") or "")[-200:])

    graph_path = source / "graphify-out" / "graph.json"
    if not graph_path.exists():
        return ClosureSummary(target=target or bench.repo_key, backend="graphify",
                              reason="graphify produced no graph.json")
    return closure_from_graph(graph_path, target or bench.repo_key)


def closure_from_graph(graph_path: Path, target: str) -> ClosureSummary:
    """Walk `calls`, `imports` and `contains` transitively from the target.

    Static approximation. Dynamic imports, plugin registries and reflection
    defeat it, so unresolved edges lower the confidence rather than being
    dropped - a closure that silently omits what it could not follow is worse
    than one that admits the gap.
    """
    document = json.loads(Path(graph_path).read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in document.get("nodes", [])}
    follow = {"calls", "imports", "imports_from", "contains", "method", "uses",
              "inherits", "extends", "re_exports"}
    unresolved_relations = {"indirect_call", "references"}

    seeds = [node_id for node_id, node in nodes.items()
             if target.lower() in str(node.get("label", "")).lower()
             or target.lower() in str(node.get("source_file", "")).lower()]
    if not seeds:
        seeds = list(nodes)

    adjacency: dict[str, list[tuple[str, str, str]]] = {}
    for link in document.get("links", []):
        adjacency.setdefault(link["source"], []).append(
            (link["target"], link.get("relation", ""), link.get("confidence", "")))

    reached: set[str] = set()
    unresolved: set[str] = set()
    inferred = 0
    stack = list(seeds)
    while stack:
        current = stack.pop()
        if current in reached:
            continue
        reached.add(current)
        for target_id, relation, confidence in adjacency.get(current, ()):
            if relation in unresolved_relations:
                unresolved.add(nodes.get(target_id, {}).get("label", target_id))
                continue
            if relation in follow:
                if confidence == "INFERRED":
                    inferred += 1
                stack.append(target_id)

    files = sorted({str(nodes[n].get("source_file") or "") for n in reached
                    if nodes.get(n, {}).get("source_file")})
    packages = sorted({str(nodes[n].get("label") or "") for n in reached
                       if nodes.get(n, {}).get("file_type") == "external"})
    # Confidence degrades with unresolved edges and with reliance on inferred
    # ones. R9: anything derived from INFERRED edges must say so.
    penalty = min(0.6, 0.05 * len(unresolved) + 0.02 * inferred)
    return ClosureSummary(target=target, files=tuple(files), packages=tuple(packages),
                          unresolved=tuple(sorted(unresolved)[:20]),
                          confidence=round(max(0.1, 1.0 - penalty), 2),
                          backend="graphify",
                          reason=f"{inferred} inferred edge(s) followed" if inferred else "")
