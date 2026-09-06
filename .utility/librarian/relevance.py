"""The relevance workbench: two ranking configurations, same questions.

Lifted from `elastic - elastic-labs`, whose `relevance-workbench` is an
application whose entire purpose is putting ranking configurations side by side
on the same corpus, and from `JayLZhou - GraphRAG`, which makes ten published
methods comparable by expressing each as a configuration over shared stages
rather than as ten programs.

It exists because of how the ceiling at `consult.SELECTIVITY_CEILING` was
settled: by editing a constant, re-running two commands, pasting numbers into a
scratch file and deleting the script. That answered one question and left
nothing behind, so the next question costs the same again — and worse, it left
no way to tell a ranking change from a **corpus** change. Both instruments read
the vault, and the vault contains this system's own index notes, so editing a
design document moves the scenario score. A configuration comparison run in one
pass over one index cannot be confounded that way; a comparison run yesterday
and today can.

    python -m librarian relevance                 # every configuration
    python -m librarian relevance --only current,coverage-bm25
    python -m librarian relevance --scenarios 0   # full set rather than a sample

A configuration is data, in `rank_configs.json`. Adding one is not a code edit,
which is the point: the cost of asking should be low enough that nobody skips
asking.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Sequence

from . import evalset, scenariotest
from .config import CatalogueConfig

CONFIGS = Path(__file__).with_name("rank_configs.json")


@dataclass(frozen=True)
class Measurement:
    name: str
    note: str
    eval_mrr: float
    eval_hit: float
    useful_at_k: float
    strong_at_k: float
    scenario_mrr: float
    cross_domain: float
    misses: tuple[str, ...]

    @property
    def miss_count(self) -> int:
        return len(self.misses)


def load(path: Path | None = None) -> list[dict[str, Any]]:
    doc = json.loads((path or CONFIGS).read_text(encoding="utf-8"))
    return list(doc.get("configurations") or [])


def apply(base: CatalogueConfig, overrides: dict[str, Any]) -> CatalogueConfig:
    """Overlay a configuration's knobs onto the shipped config.

    Unknown keys are an error rather than a silent no-op: a typo that quietly
    measures the default twice is the worst possible outcome for a tool whose
    only job is telling two configurations apart.
    """
    known = set(CatalogueConfig.__dataclass_fields__)
    unknown = sorted(set(overrides) - known)
    if unknown:
        raise KeyError(f"unknown ranking knob(s) {unknown}. Known: {sorted(known)}")
    return replace(base, **overrides)


def measure(name: str, note: str, cfg: CatalogueConfig, *,
            sample: int = 0, db_path: Path | None = None) -> Measurement:
    ev = evalset.run(cfg=cfg, db_path=db_path)
    rep = scenariotest.run(sample, seed=0, db_path=db_path, cfg=cfg)
    return Measurement(
        name=name, note=note,
        eval_mrr=round(ev.mean_reciprocal_rank, 3),
        eval_hit=round(ev.hit_rate, 3),
        useful_at_k=rep.useful_at_k,
        strong_at_k=rep.strong_at_k,
        scenario_mrr=rep.mrr,
        cross_domain=rep.cross_domain_rate,
        misses=tuple(o.scenario for o in rep.outcomes if not o.useful),
    )


def run(only: Sequence[str] | None = None, *, sample: int = 0,
        db_path: Path | None = None,
        path: Path | None = None) -> list[Measurement]:
    """Measure every configuration against one index, in one pass."""
    base = CatalogueConfig.load()
    wanted = set(only or ())
    out: list[Measurement] = []
    for entry in load(path):
        if wanted and entry["name"] not in wanted:
            continue
        cfg = apply(base, entry.get("knobs") or {})
        out.append(measure(entry["name"], entry.get("note", ""), cfg,
                           sample=sample, db_path=db_path))
    return out


def format_report(rows: Sequence[Measurement]) -> str:
    if not rows:
        return "no configurations matched"
    head = (f"{'configuration':<22}{'eval MRR':>9}{'hit@5':>7}"
            f"{'useful@5':>10}{'strong@5':>10}{'scen MRR':>10}{'cross':>7}{'miss':>6}")
    lines = ["Relevance workbench - one index, one pass, so a difference is the "
             "configuration", "", head, "-" * len(head)]
    best = max(r.useful_at_k for r in rows)
    for r in rows:
        mark = " *" if r.useful_at_k == best else "  "
        lines.append(f"{r.name:<22}{r.eval_mrr:>9.3f}{r.eval_hit:>7.2f}"
                     f"{r.useful_at_k:>10.2f}{r.strong_at_k:>10.2f}"
                     f"{r.scenario_mrr:>10.3f}{r.cross_domain:>7.2f}"
                     f"{r.miss_count:>4}{mark}")
    lines.append("")
    baseline = next((r for r in rows if r.name == "current"), rows[0])
    for r in rows:
        if r is baseline:
            continue
        gained = sorted(set(baseline.misses) - set(r.misses))
        lost = sorted(set(r.misses) - set(baseline.misses))
        if gained or lost:
            lines.append(f"  {r.name}:")
            if gained:
                lines.append(f"      recovers: {', '.join(gained)}")
            if lost:
                lines.append(f"      breaks:   {', '.join(lost)}")
    lines += ["", "  Every row ran against the same index in the same process.",
              "  Comparing a number here against one from a previous session is not",
              "  valid: both instruments read the vault, and the vault contains this",
              "  system's own index notes, so editing a design document moves the",
              "  scenario score without any ranking change at all."]
    for r in rows:
        if r.note:
            lines.append(f"  {r.name}: {r.note}")
    return "\n".join(lines)
