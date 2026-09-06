"""Separate what is being asked from the context it arrives wrapped in.

`config-validation-surface` fails under every ranking configuration in the grid,
and the reason is visible in one sentence of its description:

    The scrape loop, the storage engine and the query layer all assume the
    configuration parsed cleanly and are out of scope.

`storage`, `engine`, `query` and `layer` are named there **to exclude them**,
and they are the terms driving the result. No corpus-side knob fixes that,
because the corpus is not where the problem is. `coverage.calibrate()` reached
the same conclusion from the other direction: five signals derived from word
overlap, none able to separate a question the catalogue answers from one it
merely has vocabulary for.

Every genuine request contains context that is not the request. Somebody asking
for help with a parser will describe the compiler around it; somebody asking
about retries will describe the queue. Treating all of it as the ask is the
single largest unaddressed defect in retrieval here.

## What this does

It segments a query into three roles and weights the terms accordingly:

- **ask** — the first sentence, and anything in a clause that is not marked
  otherwise. Full weight.
- **context** — surrounding description. Reduced weight, never zero: a mention
  of the surrounding system is weak evidence, not noise.
- **excluded** — inside a clause that marks something as *not* wanted. Zero.

## Why the exclusion markers are what they are

There is a real risk of writing toward the test here, which
[[Source Documentation Standard]] forbids: the scenarios say *out of scope*
because one author wrote all thirty of them, and fitting a parser to that
phrasing would produce a number and no capability.

Two guards. First, the markers are drawn from how engineering requests are
ordinarily written — *X is unchanged*, *we are not touching Y*, *rather than Z*
— and not from reading the scenario file for phrases. Second, and the one that
actually matters, **the change is measured on both instruments**. The twenty
eval questions are short and contain no scope clauses at all, so segmentation
should leave them untouched; if it moves them, it is doing something other than
what it claims. `librarian relevance` runs both in one pass.

## What was measured, and what it settled

Both obvious remedies were implemented and measured on the full grid. **Both
are worse than doing nothing**, and the second is worse than the first:

| configuration | eval MRR | useful@5 | strong@5 | misses |
| --- | --- | --- | --- | --- |
| shipped (no segmentation) | 0.917 | **0.87** | **0.80** | **4** |
| drop excluded terms | 0.917 | 0.83 | 0.80 | 5 |
| weight ask / context / excluded | 0.942 | 0.77 | 0.77 | 7 |
| both together | 0.942 | 0.80 | 0.77 | 6 |

The segmenter itself works: on `config-validation-surface` it correctly puts
`scrape`, `loop`, `storage`, `engine`, `query` and `layer` in `excluded` and
keeps `configuration`, `malformed`, `reject` and `declarative` in the ask. The
terms removed are the right terms. Removing them still makes retrieval worse,
because the coverage ranking rewards breadth of match and both interventions
reduce breadth until single-term matches take the top — with segmentation on,
`qdrant - examples` reached first place on the single word `examples`.

One bug was found and fixed on the way, and it is the reason the first
measurement looked better than it was: this module had its own word regex, so it
excluded `scope` while the search tokenised `scope.`, and the excluded term
never matched the term being excluded. Two tokenisers is one too many;
`_words` now defers to `consult.terms_from`.

**The conclusion is a boundary, and it is worth more than a working knob would
have been.** Together with `coverage.calibrate()` — five overlap-derived signals,
none separating answerable from unanswerable — this says the ask/context
distinction is real, is correctly detectable, and **cannot be exploited by
re-weighting words**. Anything built on term overlap inherits the blindness,
whichever direction the weights point.

What that leaves is a representation of what a question is *about*, which means
a model. [[urchade - GLiNER]] extracts typed entities zero-shot and would give
`configuration`, `validation` and `schema` as *things* rather than as tokens
that happen to be present. That is now the evidenced next step rather than a
guess, and the harness to judge it already exists: add a configuration to
`rank_configs.json` and run `librarian relevance`.

This module and its configurations are kept for that comparison. Nothing here
is enabled: `query_segmentation` defaults to `False` and `coverage_order`
defaults to `bm25`, which is what the grid says is best.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Sequence

# Phrases that mark the rest of their clause as *not* the ask. Written from how
# requests are ordinarily phrased, not from the scenario corpus.
EXCLUSION_MARKERS = (
    "out of scope", "outside the scope", "not in scope",
    "is unchanged", "are unchanged", "stays the same", "stay the same",
    "not changing", "are not changing", "is not changing",
    "not touching", "we are not", "nobody is changing",
    "leave alone", "leaving alone", "already handled", "already solved",
    "do not need", "don't need", "no need to",
)

# Sentence-ish boundaries. Deliberately crude: a segmenter that needs a
# tokeniser to be correct is one more dependency for a lexical heuristic.
SENTENCE = re.compile(r"(?<=[.;:!?])\s+|\n+")
WORD = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_'-]*")

ASK_WEIGHT = 1.0
CONTEXT_WEIGHT = 0.45
EXCLUDED_WEIGHT = 0.0


@dataclass(frozen=True)
class Segments:
    ask: tuple[str, ...]
    context: tuple[str, ...]
    excluded: tuple[str, ...]

    def weight_of(self, term: str) -> float:
        low = term.lower()
        if low in self.excluded:
            return EXCLUDED_WEIGHT
        if low in self.ask:
            return ASK_WEIGHT
        if low in self.context:
            return CONTEXT_WEIGHT
        return CONTEXT_WEIGHT

    @property
    def kept(self) -> tuple[str, ...]:
        """Every term that still counts, ask first."""
        return tuple(list(self.ask) + [t for t in self.context if t not in self.ask])


def _words(text: str) -> list[str]:
    """Tokenise exactly as the search does.

    A private regex here produced `scope` while `consult.terms_from` produced
    `scope.`, so an excluded term did not match the term being excluded and
    survived into the query. Two tokenisers is one too many; this defers.
    """
    from .consult import terms_from

    return [w.lower() for w in terms_from(text) if len(w) > 2]


def segment(query: str) -> Segments:
    """Split a query into ask, context and excluded terms.

    A term appearing in both an ask clause and an excluded one stays in the ask:
    exclusion is about the clause, and a word the asker used positively
    elsewhere was clearly not being ruled out.
    """
    sentences = [s.strip() for s in SENTENCE.split(query or "") if s.strip()]
    if not sentences:
        return Segments((), (), ())

    ask: list[str] = []
    context: list[str] = []
    excluded: list[str] = []
    for position, sentence in enumerate(sentences):
        low = sentence.lower()
        if any(marker in low for marker in EXCLUSION_MARKERS):
            excluded.extend(_words(sentence))
            continue
        (ask if position == 0 else context).extend(_words(sentence))

    ask_set = dict.fromkeys(ask)
    context_set = {w: None for w in context if w not in ask_set}
    # A word used positively somewhere is not excluded, whatever the clause it
    # also appears in. Without this, "the configuration parsed cleanly" in a
    # scope clause would delete `configuration` from a query about configuration.
    excluded_set = {w: None for w in excluded
                    if w not in ask_set and w not in context_set}
    return Segments(tuple(ask_set), tuple(context_set), tuple(excluded_set))


def explain(query: str) -> str:
    seg = segment(query)
    return "\n".join([
        f"  ask      ({len(seg.ask):>2}): {', '.join(seg.ask[:16])}",
        f"  context  ({len(seg.context):>2}): {', '.join(seg.context[:16])}",
        f"  excluded ({len(seg.excluded):>2}): {', '.join(seg.excluded[:16])}",
    ])
