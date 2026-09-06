"""The domain search test: can somebody mid-project find what they need?

`evalset.py` asks whether the catalogue can find a note when the question is
already phrased the way the note is written. That measures the index. It cannot
measure the thing the catalogue exists for, which is somebody arriving with a
component of *their* system, described in *their* vocabulary, wanting to know
whether anything relevant exists.

So each scenario here isolates one component of a real system, describes it the
way its own team would, and names the surrounding architecture as context that
is explicitly *not* being worked on. The descriptions deliberately avoid the
phrasing used in any note, because a test that echoes the corpus measures
nothing.

Three things are measured, and the third is the one nothing else measures:

    useful@5        did anything worth opening come back at all
    first_useful    how far down the first one was
    cross_domain    did a useful answer arrive from outside the asker's own field

`cross_domain` is the alternative-discovery rate. A catalogue that only ever
returns sources from the asker's own field cannot answer *what else does this
job*, which is the question a project stalls on. See
[[Use Contexts And Agnostic Description]].

A run samples scenarios at random, so repeated runs explore the corpus rather
than tuning one fixed set. Pass a seed to reproduce a run exactly.
"""
from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence

from . import consult

SCENARIOS = Path(__file__).with_name("scenarios.json")
DEFAULT_SAMPLE = 6
K = 5


@dataclass(frozen=True)
class Outcome:
    scenario: str
    component: str
    returned: tuple[str, ...]
    strong_hits: tuple[str, ...]
    acceptable_hits: tuple[str, ...]
    first_useful: int | None          # 1-indexed rank, None when nothing useful
    cross_domain: tuple[str, ...]     # useful answers from outside `home_topic`
    unanticipated: tuple[str, ...]    # useful answers from a topic the scenario did not list
    why_first: str = ""

    @property
    def useful(self) -> bool:
        return self.first_useful is not None

    @property
    def reciprocal(self) -> float:
        return 1.0 / self.first_useful if self.first_useful else 0.0


@dataclass(frozen=True)
class Report:
    outcomes: tuple[Outcome, ...]
    seed: int
    notes: tuple[str, ...] = ()

    @property
    def useful_at_k(self) -> float:
        return _mean([1.0 if o.useful else 0.0 for o in self.outcomes])

    @property
    def strong_at_k(self) -> float:
        return _mean([1.0 if o.strong_hits else 0.0 for o in self.outcomes])

    @property
    def mrr(self) -> float:
        return _mean([o.reciprocal for o in self.outcomes])

    @property
    def cross_domain_rate(self) -> float:
        """Share of scenarios where a useful answer came from another field."""
        return _mean([1.0 if o.cross_domain else 0.0 for o in self.outcomes])

    @property
    def unanticipated_rate(self) -> float:
        """Share where a useful answer came from a topic the scenario did not
        list. Reported alongside the real measure because it is what the first
        version of this test called cross-domain, and the difference between
        the two numbers is a definition change rather than a result."""
        return _mean([1.0 if o.unanticipated else 0.0 for o in self.outcomes])


def _mean(values: Sequence[float]) -> float:
    return round(sum(values) / len(values), 3) if values else 0.0


def load(path: Path | None = None) -> list[dict[str, Any]]:
    data = json.loads((path or SCENARIOS).read_text(encoding="utf-8"))
    return list(data.get("scenarios") or [])


def run_one(scenario: dict[str, Any], *, db_path: Path | None = None,
            limit: int = K, cfg: Any | None = None) -> Outcome:
    expects = scenario.get("expects") or {}
    strong = set(expects.get("strong") or ())
    acceptable = set(expects.get("acceptable") or ())
    useful = strong | acceptable
    # `home_topic` is the single field the asker is working in. Measuring
    # against it is the whole point: a catalogue that only returns sources from
    # the asker's own field cannot answer "what else does this job".
    #
    # The first version measured against `expected_topics` instead - the two or
    # three topics an answer might legitimately come from - which reported
    # "answers from topics I failed to anticipate" and called it alternative
    # discovery. That was a mis-specified metric, not a low score.
    home = scenario.get("home_topic") or ""
    anticipated = set(scenario.get("expected_topics")
                      or scenario.get("cross_domain") or ())

    response = consult.find_donor(scenario["description"], {}, limit,
                                  db_path=db_path, cfg=cfg)
    returned = tuple(r.name for r in response.results)

    first = None
    for position, result in enumerate(returned, start=1):
        if result in useful:
            first = position
            break

    outside = tuple(
        r.name for r in response.results
        if r.name in useful and (r.fields.get("primary_topic") or "") != home)
    unanticipated = tuple(
        r.name for r in response.results
        if r.name in useful and (r.fields.get("primary_topic") or "") not in anticipated)

    return Outcome(
        scenario=scenario["id"],
        component=scenario.get("component", ""),
        returned=returned,
        strong_hits=tuple(n for n in returned if n in strong),
        acceptable_hits=tuple(n for n in returned if n in acceptable),
        first_useful=first,
        cross_domain=outside,
        unanticipated=unanticipated,
        why_first=response.results[0].why if response.results else "",
    )


def run(sample: int = DEFAULT_SAMPLE, *, seed: int | None = None,
        db_path: Path | None = None, path: Path | None = None,
        cfg: Any | None = None) -> Report:
    """Sample scenarios at random and score them.

    `sample=0` runs every scenario, which is what a release check should do; a
    smaller random sample is for the routine case, where the point is to keep
    exploring the corpus instead of memorising six questions.
    """
    scenarios = load(path)
    if not scenarios:
        return Report((), seed or 0, ("no scenarios defined",))
    seed = random.randrange(1_000_000) if seed is None else seed
    chosen = scenarios if sample <= 0 or sample >= len(scenarios) else \
        random.Random(seed).sample(scenarios, sample)
    return Report(tuple(run_one(s, db_path=db_path, cfg=cfg)
                        for s in chosen), seed)


def format_report(report: Report) -> str:
    lines = [f"Domain search test - {len(report.outcomes)} scenario(s), seed {report.seed}", ""]
    for outcome in report.outcomes:
        mark = "ok  " if outcome.strong_hits else ("weak" if outcome.useful else "MISS")
        rank = f"@{outcome.first_useful}" if outcome.first_useful else "  -"
        lines.append(f"  {mark} {rank}  {outcome.scenario:<32} {outcome.component}")
        if outcome.strong_hits:
            lines.append(f"          strong: {', '.join(outcome.strong_hits)}")
        if outcome.acceptable_hits:
            lines.append(f"          also:   {', '.join(outcome.acceptable_hits)}")
        if outcome.cross_domain:
            lines.append(f"          from another field: {', '.join(outcome.cross_domain)}")
        if not outcome.useful:
            lines.append(f"          returned: {', '.join(outcome.returned[:4]) or '(nothing)'}")
            lines.append(f"          top said: {outcome.why_first}")
    lines += [
        "",
        f"  useful@{K}       {report.useful_at_k:.2f}   something worth opening came back",
        f"  strong@{K}       {report.strong_at_k:.2f}   a clearly-right answer came back",
        f"  MRR            {report.mrr:.2f}   how far down the first useful answer was",
        f"  cross-domain   {report.cross_domain_rate:.2f}   a useful answer came from outside the asker's field",
        f"  unanticipated  {report.unanticipated_rate:.2f}   ...from a topic the scenario did not list",
    ]
    return "\n".join(lines)
