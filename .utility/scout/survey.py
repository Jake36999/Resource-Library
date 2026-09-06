"""Decompose a repository into components, without reading any of its code.

This is the method that actually built the catalogue, promoted from a scratchpad
to a service on 2026-09-04. Both 2026-09 cohorts — 113 of 128 resources — were
surveyed by throwaway scripts that were then deleted, so the *output* survived
in `.Data/surveys/` and the *surveyor* did not. That is the exact failure
[[Data Information Knowledge]] warns about: the data layer outliving the
conclusions is worth nothing if the thing that produced it has to be rewritten
from prose each time.

Promoting it also removed two defects the scratchpad version had, both of which
came from reinventing what already existed:

- **No token support.** It used a bare `urlopen` against a 60/hour
  unauthenticated limit and slept through resets. `discovery._request` already
  handled `GITHUB_TOKEN` (5,000/hour) and rate-limit errors, and is now reused.
- **A hand-rolled clone.** `clone.shallow_clone` already existed with a
  policy check, `GIT_TERMINAL_PROMPT=0` and forced disposal on Windows; the
  scratchpad had none of those. It gained `blobless=True` instead.

## What a survey is, and is not

A survey records **what a repository is made of** — directory shape, extension
mix, root files, and paths classified into kinds of material. It reads no file
contents: a blobless clone fetches trees and no blobs, so this is structurally
incapable of copying code, which is the same boundary
`NO_PERSISTENT_SOURCE_GRAPH` draws elsewhere.

It draws no conclusions. `SigmaHQ/sigma has 4,521 paths matching the grammar
signal` is data. That this makes it a good source for detection rules is
information, it belongs in a note, and a person writes it.

## The signal table is coarse on purpose

A signal matches a path by substring. `tests` will catch `contest.py`, and
`data` will catch `metadata.json`. That is tolerated because the alternative —
a classifier that is usually right and occasionally confidently wrong — is worse
for a layer whose whole job is being checkable. A count here is a hint to look,
never a fact about quality.
"""
from __future__ import annotations

import json
import subprocess
import time
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence

from librarian import clone as clone_mod

from .config import ScoutConfig, vault_root
from .discovery import RateLimited, fetch_repo

# Resolved per call, so a survey lands in whichever vault is configured.
def survey_dir() -> Path:
    return vault_root() / ".Data" / "surveys"
LS_TREE_TIMEOUT = 180

# Path substrings that mark a kind of material. Deliberately coarse; see the
# module docstring. Order is irrelevant - a path may match several signals and
# is counted under each, because a file under `tests/fixtures/` genuinely is
# both.
SIGNALS: dict[str, tuple[str, ...]] = {
    "docs": ("docs/", "doc/", "documentation/", "website/"),
    "examples": ("example", "examples/", "samples/", "demo", "tutorial",
                 "cookbook", "recipes/"),
    "notebooks": (".ipynb",),
    "benchmarks": ("benchmark", "bench/", "perf/"),
    "tests": ("test", "spec/", "__tests__"),
    "fixtures": ("fixture", "testdata", "test_data", "golden", "snapshot"),
    "schemas": (".schema.json", "schema/", "schemas/", ".proto", "openapi",
                ".graphql", ".owl", ".ttl", ".rdf"),
    "grammars": ("grammar", ".ebnf", ".bnf", ".lark", ".peg", ".g4", ".jj",
                 ".flex"),
    "data": (".csv", ".parquet", ".jsonl", ".sqlite", "dataset", "corpus",
             "lexicon"),
    "diagrams": (".mmd", ".puml", ".drawio", "diagram"),
    "containers": ("dockerfile", "docker-compose", "chart.yaml", "k8s/"),
    "agent_instructions": ("claude.md", "agents.md", ".claude/", "skills/",
                           ".cursor", "mcp"),
    "iac": (".tf", "terraform/", "ansible", ".bicep"),
}

SAMPLE_PATHS = 10
TOP_DIRECTORIES = 14
SECOND_LEVEL = 10


@dataclass
class SurveyReport:
    surveyed: list[str] = field(default_factory=list)
    failed: list[tuple[str, str]] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    path: Path | None = None

    @property
    def ok(self) -> bool:
        return not self.failed


def classify(paths: Sequence[str]) -> dict[str, dict[str, Any]]:
    """Paths -> `{signal: {"n": count, "sample": [...]}}`.

    The stored shape carries the count **and** a truncated sample, because the
    2026-09-03 survey stored only a sample and its length was mistaken for the
    count - ten tests recorded for a repository with 847. Storing both removes
    the ambiguity rather than documenting it.
    """
    lowered = [p.lower() for p in paths]
    out: dict[str, dict[str, Any]] = {}
    for label, needles in SIGNALS.items():
        hits = [p for p, low in zip(paths, lowered)
                if any(n in low for n in needles)]
        if hits:
            out[label] = {"n": len(hits), "sample": hits[:SAMPLE_PATHS]}
    return out


def shape(paths: Sequence[str]) -> dict[str, Any]:
    """Directory and extension structure, with no network access."""
    top = Counter(p.split("/")[0] if "/" in p else "(root)" for p in paths)
    second: dict[str, list[str]] = {}
    for head, _ in top.most_common(TOP_DIRECTORIES):
        if head == "(root)":
            continue
        subs = Counter(p.split("/")[1] for p in paths
                       if p.split("/")[0] == head and p.count("/") >= 2)
        if subs:
            second[head] = [f"{k} ({v})" for k, v in subs.most_common(SECOND_LEVEL)]
    exts = Counter(Path(p).suffix.lower() for p in paths if Path(p).suffix)
    return {
        "files": len(paths),
        # The complete listing, not a sample. Added 2026-09-05 because
        # component retrieval could only reach depth 1-2: `relevance-workbench`
        # and `goldset` resolved, `sqllogictest` and `multitask` did not, and
        # those are exactly the kind of thing a query should surface. A tree is
        # a few hundred kilobytes of text and the surveys are the durable
        # artefact - sampling the thing you cannot re-fetch cheaply is a false
        # economy. Surveys written before this date carry samples only.
        "paths": list(paths),
        "top": [f"{k} ({v})" for k, v in top.most_common(TOP_DIRECTORIES)],
        "second": second,
        "extensions": [f"{k} ({v})" for k, v in exts.most_common(12)],
        "root_files": [p for p in paths if "/" not in p][:18],
        "signals": classify(paths),
    }


def list_tree(repo_key: str, *, timeout: int = LS_TREE_TIMEOUT) -> list[str]:
    """Every path at HEAD, via a blobless clone that is always discarded.

    No file contents are fetched and the clone is removed in a `finally`, so a
    failure part-way through cannot leave a partial checkout behind.
    """
    handle = clone_mod.shallow_clone(repo_key, blobless=True)
    try:
        listed = subprocess.run(
            ["git", "ls-tree", "-r", "HEAD", "--name-only"],
            cwd=handle.path, capture_output=True, text=True,
            errors="replace", timeout=timeout)
        if listed.returncode != 0:
            raise RuntimeError((listed.stderr or "ls-tree failed").strip()[:200])
        return [line for line in listed.stdout.splitlines() if line.strip()]
    finally:
        clone_mod.discard(handle.path)


def metadata(repo_key: str, cfg: ScoutConfig) -> dict[str, Any]:
    """GitHub's own account of a repository, via the shared client.

    `discovery.fetch_repo` carries token handling and rate-limit errors; a
    survey that reinvents them ends up sleeping through resets on a 60/hour
    budget, which is what the scratchpad version did.
    """
    raw = fetch_repo(repo_key, cfg)
    if not raw:
        return {}
    licence = raw.get("license") or {}
    return {
        "full_name": raw.get("full_name"),
        "description": raw.get("description"),
        "language": raw.get("language"),
        "spdx": licence.get("spdx_id"),
        "default_branch": raw.get("default_branch"),
        "stars": raw.get("stargazers_count"),
        "forks": raw.get("forks_count"),
        "open_issues": raw.get("open_issues_count"),
        "size_kb": raw.get("size"),
        "archived": bool(raw.get("archived")),
        "fork": bool(raw.get("fork")),
        "created": raw.get("created_at"),
        "pushed": raw.get("pushed_at"),
        "homepage": raw.get("homepage"),
        "topics": raw.get("topics") or [],
    }


def survey_one(repo_key: str, cfg: ScoutConfig | None = None) -> dict[str, Any]:
    """One repository: metadata, then structure. Never raises for a bad tree."""
    cfg = cfg or ScoutConfig.load()
    entry: dict[str, Any] = {"repo": repo_key,
                             "surveyed_at": time.strftime("%Y-%m-%d")}
    meta = metadata(repo_key, cfg)
    if not meta:
        entry["meta"] = {"error": "not found"}
        return entry
    entry["meta"] = meta
    try:
        entry.update(shape(list_tree(repo_key)))
    except Exception as exc:                       # a clone can fail for many reasons
        entry["tree_error"] = str(exc)[:200]
    return entry


def run(repo_keys: Iterable[str], out_path: Path | None = None,
        cfg: ScoutConfig | None = None, *,
        resume: bool = True) -> SurveyReport:
    """Survey many repositories, writing after each one.

    Resumable by construction: the output file is the state. A run that dies at
    repository forty does not repeat the first thirty-nine, which matters when
    the budget is an hourly API limit rather than time.
    """
    cfg = cfg or ScoutConfig.load()
    target = Path(out_path or (survey_dir() /
                               f"{time.strftime('%Y-%m-%d')}-cohort.json"))
    target.parent.mkdir(parents=True, exist_ok=True)
    done: dict[str, Any] = {}
    if resume and target.exists():
        try:
            done = json.loads(target.read_text(encoding="utf-8"))
        except Exception:
            done = {}

    report = SurveyReport(path=target)
    for repo_key in repo_keys:
        if repo_key in done and "meta" in done[repo_key]:
            report.skipped.append(repo_key)
            continue
        try:
            entry = survey_one(repo_key, cfg)
        except RateLimited as exc:
            report.failed.append((repo_key, str(exc)))
            break                                  # stop; the rest would fail too
        except Exception as exc:
            report.failed.append((repo_key, str(exc)[:200]))
            continue
        done[repo_key] = entry
        target.write_text(json.dumps(done, indent=1, ensure_ascii=False),
                          encoding="utf-8")
        if entry.get("tree_error") or "error" in (entry.get("meta") or {}):
            report.failed.append((repo_key, entry.get("tree_error")
                                  or "metadata not found"))
        else:
            report.surveyed.append(repo_key)
    return report


def format_report(report: SurveyReport) -> str:
    lines = [f"surveyed {len(report.surveyed)}, "
             f"skipped {len(report.skipped)} already present, "
             f"failed {len(report.failed)}"]
    if report.path:
        lines.append(f"  written to {report.path}")
    for repo_key, reason in report.failed[:12]:
        lines.append(f"  FAILED {repo_key}: {reason}")
    if report.surveyed:
        lines.append("  rebuild the data layer with "
                     "`python -m librarian components build`")
    return "\n".join(lines)
