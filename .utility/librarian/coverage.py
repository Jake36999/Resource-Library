"""Say "I do not cover this" instead of returning the best four irrelevant notes.

A ranked list is always non-empty. `find_donor` will happily answer *how do I
make a soufflé rise evenly* with four sources, at scores of 1.00, 0.98, 0.97 and
0.95, because those numbers are normalised **within** a response and say nothing
about whether the response is any good.

That is the failure mode that makes a catalogue unsafe to trust: not being
wrong, but being wrong indistinguishably from being right. A tool that can say
*nothing here answers this* is more useful than one that cannot, because the
reader stops needing to check.

## What the verdict is computed from

Nothing about scores, which are relative. Three things that are absolute:

**Query account** — how much of what was asked did the best answer actually
match? Measured over *selective* terms only, so `the`, `and` and `our` cannot
inflate it.

**Consensus** — did more than one source match substantially? One source
matching two terms may be coincidence; three sources doing so is a subject the
catalogue holds.

**Where it matched** — a term found in `Reading Notes` is evidence *about* a
source, often the opposite of a claim. `consult.CLAIM_SECTIONS` already draws
that line for ranking and it is reused here.

## Calibration, and what it ruled out

The thresholds were fitted against the thirty scenarios in `scenarios.json`,
which carry known answers including two the corpus deliberately does not cover.
`coverage.calibrate()` re-runs that fit and prints the confusion table.

**The fit produced a negative result worth more than the thresholds.** Five
candidate signals were measured against answerable and unanswerable scenarios,
and none separates them:

| Signal | answerable (median) | unanswerable (median) |
| --- | --- | --- |
| selective terms matched by the best answer | 6 | **7** |
| total matched across the top five | 20 | 22 |
| sources matching two or more terms | 5 | 5 |
| score decay across the top eight | 0.11 | 0.12 |
| distinct topics in the top eight | 6 | 6 |

The unanswerable questions match *more* than the median answerable one. That is
not noise, it is the mechanism: `gpu-execution-alternative` is a long, careful
description whose vocabulary — `execution`, `memory`, `constraint`,
`optimisations` — is everywhere in a corpus about software, and it matches
plenty of things that are not the answer.

**So: every signal derivable from word overlap inherits the same blindness,
because the system has no representation of what a question is *about*, only of
which words it contains.** Coverage detection and query understanding are one
problem, not two, and this module cannot be finished before `queryunderstanding`
is.

## Stage 2 closed, 2026-09-05: the gap is corpus-shaped

Eight representations have now been measured against the same thirty scenarios,
and **none separates a question the catalogue answers from one it merely has
material near**:

| Representation | Lift over "always answerable" |
| --- | --- |
| five lexical overlap signals | none; unanswerable matched *more* |
| cosine, whole query | **+0%** |
| cosine, segmented ask only | **+0%** |
| cosine, the hand-written `component` phrase | **+0%** |

The last row is the one that settles it. `component` is a short phrase written
by hand to say exactly what is being asked — the cleanest possible statement of
intent, with no surrounding context to dilute it — and a threshold on it does no
better than assuming every question is answerable.

Cosine at least points the right way: the answerable median is above the
unanswerable one in all three variants, where the lexical signals had it
backwards. But the ranges overlap completely, and a consistent shift you cannot
threshold is not a decision procedure.

**Why this is the expected result rather than a disappointing one.** The
unanswerable scenarios are not nonsense; they are questions the catalogue holds
genuinely adjacent material for. Telling *I have this* from *I have things like
this* cannot be done by looking at the question, however it is represented,
because the difference is in whether the retrieved thing actually answers it -
a judgement about the **result**, not the query. Closing that would need
something reading candidate notes against the question, which is a different
and much more expensive machine.

So Stage 2 closes on its second stated outcome: the gap is **corpus-shaped
rather than ranking-shaped**. Holding more material is Stage 4's job.

**One caveat, stated because it bounds the claim.** There are only five
unanswerable scenarios, so this measures *no usable effect at this size* rather
than *no effect*. `separation_probe()` re-runs the whole comparison; run it when
the scenario set gains negatives, particularly externally-authored ones.

## What this therefore claims, and what it does not

It reliably detects a question from **outside the collection entirely** — the
case where nothing corroborates, `consensus` is zero and the top result matched
one incidental word. That is a real and common failure and it is now caught.

It cannot detect **adjacent but wrong**: a question the catalogue has plenty of
vocabulary for and no answer to. Those come back `thin`, which is the honest
verdict — *cannot tell* — rather than a confident one. `thin` should be read as
"no opinion", never as "probably fine".
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from . import consult
from .config import CatalogueConfig, index_db_path

# Deliberately conservative. The measured separation between answerable and
# unanswerable is nil for long queries (see the docstring), so these are set to
# catch the case that *is* separable - nothing corroborating at all - and to
# return `thin` rather than a confident verdict everywhere else.
STRONG_ACCOUNT = 0.34      # share of selective query terms the best answer matched
THIN_ACCOUNT = 0.10
CONSENSUS_MATCHES = 2      # results matching at least two selective terms

COVERED = "covered"
THIN = "thin"
UNCOVERED = "uncovered"


@dataclass(frozen=True)
class Verdict:
    level: str                 # covered | thin | uncovered
    account: float             # 0..1, how much of the query the best answer matched
    consensus: int             # results matching two or more selective terms
    selective_terms: tuple[str, ...]
    best_matched: tuple[str, ...]
    reason: str

    @property
    def trustworthy(self) -> bool:
        return self.level == COVERED

    def sentence(self) -> str:
        if self.level == UNCOVERED:
            return ("nothing here covers this - the catalogue is answering from "
                    f"{self.consensus} weak match(es); {self.reason}")
        if self.level == THIN:
            return f"thin coverage - {self.reason}; treat these as leads, not answers"
        return f"covered - {self.reason}"


def _selective(query: str, db_path: Path | None = None,
               cfg: CatalogueConfig | None = None) -> tuple[str, ...]:
    """The query terms that discriminate, using the same rule ranking uses."""
    cfg = cfg or CatalogueConfig.load()
    terms = consult.terms_from(query)
    conn = sqlite3.connect(str(db_path or index_db_path()))
    conn.row_factory = sqlite3.Row
    try:
        keep = consult._selective_terms(conn, terms, cfg.selectivity_ceiling,
                                        cfg.selectivity_scope)
    except sqlite3.OperationalError:
        keep = frozenset(t.lower() for t in terms)
    finally:
        conn.close()
    return tuple(sorted(keep))


def assess(query: str, response: Any, *, db_path: Path | None = None,
           cfg: CatalogueConfig | None = None) -> Verdict:
    """Is this response worth trusting, in absolute terms?"""
    selective = _selective(query, db_path, cfg)
    results = list(getattr(response, "results", ()) or ())

    if not results:
        return Verdict(UNCOVERED, 0.0, 0, selective, (),
                       "no source matched at all")

    def counted(result: Any) -> tuple[str, ...]:
        fields = getattr(result, "fields", {}) or {}
        heading = fields.get("matched_in") or ""
        if not consult.is_claim_section(heading):
            return ()
        return tuple(t for t in (fields.get("matched") or ())
                     if t.lower() in selective)

    per_result = [counted(r) for r in results]
    best = max(per_result, key=len) if per_result else ()
    account = (len(set(t.lower() for t in best)) / len(selective)) if selective else 0.0
    consensus = sum(1 for m in per_result if len(m) >= 2)

    if account >= STRONG_ACCOUNT and consensus >= CONSENSUS_MATCHES:
        reason = (f"the best answer accounts for {len(best)} of "
                  f"{len(selective)} distinctive terms, and {consensus} sources agree")
        return Verdict(COVERED, account, consensus, selective, best, reason)
    if account >= STRONG_ACCOUNT or (account >= THIN_ACCOUNT and consensus >= CONSENSUS_MATCHES):
        reason = (f"the best answer accounts for {len(best)} of "
                  f"{len(selective)} distinctive terms, with {consensus} "
                  f"corroborating source(s)")
        return Verdict(THIN, account, consensus, selective, best, reason)
    reason = (f"the best answer accounts for {len(best)} of {len(selective)} "
              f"distinctive terms in a claim section")
    return Verdict(UNCOVERED, account, consensus, selective, best, reason)


# ------------------------------------------------------------------ calibration

def calibrate(*, db_path: Path | None = None,
              cfg: CatalogueConfig | None = None) -> dict[str, Any]:
    """Fit the verdict against known answers, and report the confusion table.

    The scenario set is the ground truth: a scenario whose expected answers came
    back is *covered*, one whose did not is *uncovered*. Two scenarios are
    marked in the corpus as deliberately unanswerable, and those are the cases
    the verdict most needs to get right - being able to say "no" about the two
    things the catalogue genuinely lacks is the entire point.
    """
    from . import scenariotest

    rows: list[dict[str, Any]] = []
    for scenario in scenariotest.load():
        outcome = scenariotest.run_one(scenario, db_path=db_path, limit=5, cfg=cfg)
        response = consult.find_donor(scenario["description"], {}, 5,
                                      db_path=db_path, cfg=cfg)
        verdict = assess(scenario["description"], response, db_path=db_path, cfg=cfg)
        rows.append({
            "scenario": scenario["id"],
            "truth": "answerable" if outcome.useful else "unanswerable",
            "verdict": verdict.level,
            "account": round(verdict.account, 3),
            "consensus": verdict.consensus,
        })

    table: dict[tuple[str, str], int] = {}
    for row in rows:
        key = (row["truth"], row["verdict"])
        table[key] = table.get(key, 0) + 1
    # The costly error is calling an unanswerable question covered: that is the
    # system asserting an answer it does not have, which is what a reader would
    # act on. Calling an answerable one uncovered merely wastes an opportunity.
    false_confidence = table.get(("unanswerable", COVERED), 0)
    missed = table.get(("answerable", UNCOVERED), 0)
    return {"rows": rows, "table": table,
            "false_confidence": false_confidence, "missed": missed,
            "n": len(rows)}


def format_calibration(result: dict[str, Any]) -> str:
    lines = ["Coverage verdict against the scenario set", ""]
    lines.append(f"  {'scenario':<34}{'truth':<14}{'verdict':<11}{'account':>8}{'agree':>7}")
    for row in sorted(result["rows"], key=lambda r: (r["truth"], r["verdict"])):
        flag = ""
        if row["truth"] == "unanswerable" and row["verdict"] == COVERED:
            flag = "  <-- asserts an answer it does not have"
        lines.append(f"  {row['scenario']:<34}{row['truth']:<14}{row['verdict']:<11}"
                     f"{row['account']:>8.2f}{row['consensus']:>7}{flag}")
    lines += ["", "  confusion (truth x verdict):"]
    for truth in ("answerable", "unanswerable"):
        cells = "  ".join(f"{v}={result['table'].get((truth, v), 0)}"
                          for v in (COVERED, THIN, UNCOVERED))
        lines.append(f"      {truth:<14}{cells}")
    lines += ["",
              f"  false confidence (said covered, was not): {result['false_confidence']}",
              f"  missed (said uncovered, was answerable):  {result['missed']}",
              "",
              "  The first number is the one that matters. Calling an unanswerable",
              "  question covered is the system asserting an answer it does not",
              "  have; the reverse merely wastes an opportunity."]
    return "\n".join(lines)


# ------------------------------------------------- can anything separate them?

SEPARATION_VARIANTS = ("whole", "ask_only", "component")


def separation_probe(*, db_path: Path | None = None,
                     cfg: CatalogueConfig | None = None) -> dict[str, Any]:
    """Can any representation of a query tell answerable from unanswerable?

    Re-runnable, because the answer is corpus-dependent and the current one was
    measured against only five unanswerable scenarios. Run it again when the
    scenario set gains negatives or the corpus grows substantially.

    Reports, per representation, the best accuracy any single threshold
    achieves against the do-nothing baseline of always answering *answerable*.
    A lift of zero means the representation carries no usable information for
    this decision, whatever its medians look like.
    """
    import sqlite3
    import statistics

    from . import embed as embed_mod, scenariotest
    from . import queryunderstanding as qu
    from .config import index_db_path

    cfg = cfg or CatalogueConfig.load()
    conn = sqlite3.connect(str(db_path or index_db_path()))
    conn.row_factory = sqlite3.Row
    layers = ("resource", "review", "paper")

    def best_cosine(text: str) -> float:
        hits, _ = embed_mod.search(conn, text, cfg, limit=50, layers=layers)
        per_note: dict[str, float] = {}
        for _, name, score in hits:
            per_note[name] = max(per_note.get(name, -1.0), score)
        return max(per_note.values()) if per_note else 0.0

    try:
        scores: dict[str, list[float]] = {v: [] for v in SEPARATION_VARIANTS}
        truth: list[str] = []
        for scenario in scenariotest.load():
            outcome = scenariotest.run_one(scenario, db_path=db_path, limit=5, cfg=cfg)
            truth.append("Y" if outcome.useful else "N")
            segments = qu.segment(scenario["description"])
            scores["whole"].append(best_cosine(scenario["description"]))
            scores["ask_only"].append(
                best_cosine(" ".join(segments.ask) or scenario["description"]))
            scores["component"].append(
                best_cosine(scenario.get("component") or scenario["description"]))
    finally:
        conn.close()

    total = len(truth) or 1
    answerable = sum(1 for t in truth if t == "Y")
    out: dict[str, Any] = {"scenarios": total, "answerable": answerable,
                           "unanswerable": total - answerable,
                           "baseline": round(answerable / total, 3),
                           "variants": {}}
    for name, values in scores.items():
        pairs = sorted(zip(values, truth))
        best = 0
        for index in range(len(pairs) + 1):
            threshold = pairs[index][0] if index < len(pairs) else 1.0
            correct = sum(1 for v, t in pairs
                          if (v < threshold and t == "N") or (v >= threshold and t == "Y"))
            best = max(best, correct)
        yes = [v for v, t in zip(values, truth) if t == "Y"]
        no = [v for v, t in zip(values, truth) if t == "N"]
        out["variants"][name] = {
            "best_accuracy": round(best / total, 3),
            "lift": round((best - answerable) / total, 3),
            "median_answerable": round(statistics.median(yes), 4) if yes else None,
            "median_unanswerable": round(statistics.median(no), 4) if no else None,
        }
    return out


def format_separation(result: dict[str, Any]) -> str:
    lines = [
        "Can any query representation separate answerable from unanswerable?", "",
        f"  {result['scenarios']} scenarios, {result['answerable']} answerable, "
        f"{result['unanswerable']} not",
        f"  do-nothing baseline (always say 'answerable'): {result['baseline']:.0%}",
        "",
        f"  {'representation':<14}{'best':>7}{'lift':>8}{'med(Y)':>9}{'med(N)':>9}",
    ]
    for name, row in result["variants"].items():
        lines.append(f"  {name:<14}{row['best_accuracy']:>7.0%}{row['lift']:>+8.0%}"
                     f"{row['median_answerable']:>9.4f}{row['median_unanswerable']:>9.4f}")
    lines += ["",
              "  A lift of zero means no threshold on that representation beats",
              "  simply assuming every question is answerable, whatever the",
              "  medians suggest."]
    return "\n".join(lines)
