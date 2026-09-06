"""Two sources that do the same job, before the catalogue answers with both.

`integrity.distinct_resource_prose` catches two notes whose *prose* could be
swapped. Nothing catches two *sources* that do the same thing described in
different words — and that is the failure that scales badly. At 128 it is held
in one person's memory. At 400 it is not, and the symptom is silent: the
catalogue starts answering one question with three entries that are the same
answer, and the reader has no way to tell.

[[asreview]] is the reference. Deduplication is a **named stage** of systematic
review, run before screening rather than during it, precisely because reviewers
cannot be trusted to notice duplicates while doing something else.

## What "duplicate" means here, and why it is not one number

A source can resemble another in three unrelated ways, and collapsing them into
a single similarity score loses the thing a person needs to make the call:

- **Structural** — the component profile is alike: same signals, same extension
  mix, same directory shape. Two SQL parsers look alike whatever they say about
  themselves. Computed from the data layer.
- **Semantic** — the notes claim the same capability. Computed over
  `Transferable Capability`, which is the section deliberately written in
  domain-neutral terms, so two sources doing one job from different fields
  should land near each other there. That is the whole reason that section
  exists.
- **Declared** — the taxonomy already says so: same `primary_topic`, same
  `domain_primary`, overlapping `patterns`.

A pair is reported with all three, and the verdict stays with a person. This
module **never merges, deletes or reranks anything** — the same rule the rest of
the data layer follows.

## Why not embeddings

They would be better at the semantic half and they are optional here by design;
retrieval already degrades to lexical when LM Studio is absent, and a
duplicate check that only works when a model is resident is one nobody runs.
Jaccard over the vocabulary of one section is crude, needs nothing, and is
enough to produce a shortlist for a person — which is all this is for.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

from . import notes as notes_mod
from .components import connect
from .config import component_db_path
from .config import vault_root

WORD = re.compile(r"[a-z][a-z0-9-]{2,}")

# Words carried by almost every `Transferable Capability` section because the
# section's own conventions put them there. `consult.STOPWORDS` handles ordinary
# English - maintaining a second copy of that list here produced `and`, `are`
# and `can` as evidence that two sources do the same job, which is the same
# defect `SELECTIVITY_CEILING` prevents one layer up. This adds only the words
# the *house style* makes ubiquitous.
SECTION_BOILERPLATE = frozenset({
    "alternative", "applies", "wherever", "rather", "instead", "something",
    "anything", "thing", "things", "capability", "source", "sources",
    "catalogue", "system", "systems", "somebody", "nobody", "everything",
})

# Calibrated against the corpus on 2026-09-04, not chosen. Jaccard over a
# 49-134 word vocabulary is a narrow scale: across all 8,385 pairs the maximum
# observed was 0.124 and the median 0.038. The first version of this module set
# `SEMANTIC_FLOOR = 0.18` - **above the maximum**, so the check could never fire
# and reported "no duplicates found", which is worse than no check at all.
#
# 0.098 is the 99.5th percentile of the 8,385 pairs. Re-derive it with
# `duplicates.distribution()` after any large intake; a floor fixed against a
# corpus that has moved is the same defect one layer along.
SEMANTIC_FLOOR = 0.098
CORROBORATION_STRUCTURAL = 0.45
CORROBORATION_DECLARED = 0.30


@dataclass(frozen=True)
class Pair:
    left: str
    right: str
    structural: float
    semantic: float
    declared: float
    shared_signals: tuple[str, ...]
    shared_terms: tuple[str, ...]

    @property
    def corroborated(self) -> bool:
        """Does anything besides the wording agree the two are alike?"""
        return (self.structural >= CORROBORATION_STRUCTURAL
                or self.declared >= CORROBORATION_DECLARED)

    @property
    def score(self) -> float:
        """Semantic similarity, ranked first; the others corroborate.

        A weighted sum was tried first and was wrong on the arithmetic: the
        three components have incomparable ranges. Semantic Jaccard tops out
        near 0.14 on this corpus while structural and declared both run to 1.0,
        so a composite that *said* semantic evidence mattered most gave it the
        smallest contribution and ranked by directory shape instead - which
        pairs every Python project with tests against every other one.

        Ranking on the trusted signal and requiring the others to agree keeps
        the stated reasoning and the arithmetic consistent.
        """
        return round(self.semantic, 3)

    def why(self) -> str:
        bits = []
        if self.shared_terms:
            bits.append("both claim " + ", ".join(self.shared_terms[:6]))
        if self.shared_signals:
            bits.append("both carry " + ", ".join(self.shared_signals[:4]))
        return "; ".join(bits) or "similar taxonomy only"


def _jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def _capability_terms(note: Any) -> set[str]:
    """The vocabulary of what a source claims to do, minus what every note says."""
    from .consult import STOPWORDS

    text = ""
    for heading in ("Transferable Capability", "Bottom Line"):
        text += " " + (note.section(heading) or "")
    words = {w for w in WORD.findall(text.lower())}
    return {w for w in words
            if w not in SECTION_BOILERPLATE and w.lower() not in STOPWORDS}


def _structural_profile(db_path: Path | None = None) -> dict[str, dict[str, Any]]:
    """Signals and dominant extensions per source, from the data layer."""
    target = Path(db_path or component_db_path())
    if not target.exists():
        return {}
    conn = connect(target)
    try:
        out: dict[str, dict[str, Any]] = {}
        for row in conn.execute("SELECT repo_key, signal FROM signal"):
            out.setdefault(row["repo_key"], {"signals": set(), "exts": set()})
            out[row["repo_key"]]["signals"].add(row["signal"])
        for row in conn.execute(
                "SELECT repo_key, extension FROM extension WHERE files >= 5"):
            out.setdefault(row["repo_key"], {"signals": set(), "exts": set()})
            out[row["repo_key"]]["exts"].add(row["extension"])
        return out
    finally:
        conn.close()


def find(vault: Path | None = None, *, db_path: Path | None = None,
         floor: float = SEMANTIC_FLOOR) -> list[Pair]:
    """Candidate duplicate pairs, most alike first. Reports only."""
    root = vault or vault_root()
    resources = [n for n in notes_mod.load_vault(root)
                 if n.layer in ("resource", "review") and n.string("repo_key")]
    structural = _structural_profile(db_path)

    profiles = []
    for note in resources:
        repo_key = note.string("repo_key")
        struct = structural.get(repo_key) or {"signals": set(), "exts": set()}
        profiles.append({
            "name": note.name,
            "terms": _capability_terms(note),
            "signals": struct["signals"],
            "exts": struct["exts"],
            "topic": note.string("primary_topic") or "",
            "domain": note.string("domain_primary") or "",
            "patterns": set(note.frontmatter.get("patterns") or ()),
        })

    pairs: list[Pair] = []
    for i, left in enumerate(profiles):
        for right in profiles[i + 1:]:
            semantic = _jaccard(left["terms"], right["terms"])
            structural_score = (
                0.6 * _jaccard(left["signals"], right["signals"])
                + 0.4 * _jaccard(left["exts"], right["exts"]))
            declared = (
                0.4 * (left["topic"] == right["topic"] and bool(left["topic"]))
                + 0.3 * (left["domain"] == right["domain"] and bool(left["domain"]))
                + 0.3 * _jaccard(left["patterns"], right["patterns"]))
            pair = Pair(left["name"], right["name"],
                        round(structural_score, 3), round(semantic, 3),
                        round(declared, 3),
                        tuple(sorted(left["signals"] & right["signals"]))[:6],
                        tuple(sorted(left["terms"] & right["terms"]))[:8])
            if pair.semantic >= floor and pair.corroborated:
                pairs.append(pair)
    pairs.sort(key=lambda p: -p.score)
    return pairs


def distribution(vault: Path | None = None) -> dict[str, float]:
    """The semantic similarity spread, so a floor is derived rather than guessed.

    Run this after a large intake. The scale is corpus-dependent and a
    threshold fixed against a corpus that has since doubled is not a threshold.
    """
    import statistics

    root = vault or vault_root()
    resources = [n for n in notes_mod.load_vault(root)
                 if n.layer in ("resource", "review") and n.string("repo_key")]
    terms = {n.name: _capability_terms(n) for n in resources}
    names = list(terms)
    values = [_jaccard(terms[a], terms[b])
              for i, a in enumerate(names) for b in names[i + 1:]]
    if not values:
        return {}
    values.sort()
    return {
        "pairs": float(len(values)),
        "max": round(values[-1], 4),
        "median": round(statistics.median(values), 4),
        "p99": round(values[int(len(values) * 0.99)], 4),
        "p995": round(values[int(len(values) * 0.995)], 4),
        "current_floor": SEMANTIC_FLOOR,
    }


def format_report(pairs: Sequence[Pair]) -> str:
    if not pairs:
        return ("no candidate duplicates above the floor\n"
                "  That is a result, not a silence: the check ran and found "
                "nothing worth a person's time.")
    lines = [f"{len(pairs)} candidate duplicate pair(s), most alike first", "",
             "  These are candidates for a person to judge. Nothing was merged,",
             "  deleted or reranked - two sources doing one job is often exactly",
             "  what a catalogue should hold, and saying so is the point.", ""]
    for pair in pairs:
        lines.append(f"  {pair.score:.2f}  {pair.left}")
        lines.append(f"        {pair.right}")
        lines.append(f"        semantic {pair.semantic:.2f} · structural "
                     f"{pair.structural:.2f} · declared {pair.declared:.2f}")
        lines.append(f"        {pair.why()}")
        lines.append("")
    return "\n".join(lines)
