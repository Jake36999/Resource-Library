"""Check the catalogue's own claims against the data they came from.

[[Topic - Data Lineage & Provenance]] holds eight sources about attributing an
artefact to the inputs that produced it. The catalogue did not do it to itself:
a note asserting that `javaparser` carries 1,833 test paths was traceable to
`.Data/surveys/` only by a person reading both, and `**Not read:**` was an
honest convention rather than a checkable one.

[[Data Information Knowledge]] says information must be derivable from data.
This is the derivation, run backwards.

## What is checkable, and what is not

A resource note makes two kinds of statement. *That the symbol solver is the
harder half* is a judgement — it is information, a person made it, and no
amount of tooling can verify it. But *that `javaparser-symbol-solver-testing` is
1,436 files* is arithmetic over a survey, and if the note and the survey
disagree then one of them is wrong.

So this checks the arithmetic and leaves the judgement alone. Concretely: any
number a note states about a repository's structure — file counts, path counts,
directory sizes — is looked up in the component store.

Three outcomes, and the middle one is the interesting one:

- **supported** — the survey has a row with that number.
- **unsupported** — no row matches. Usually the claim counts something the
  signal table does not model, occasionally the number is wrong. Reported, not
  failed, because a false accusation here is worse than a missed one.
- **contradicted** — the survey has the corresponding quantity and it is a
  different number. That is a defect in the note.

## Why this is not stricter

It would be easy to demand that every number in a note carry a citation, and
that would produce notes nobody wants to read and authors who avoid numbers.
The value of a specific claim — *1,399 photographs and two notebooks* — is
exactly that it is concrete, and the way to keep authors writing that way is to
make being concrete cheap and being wrong visible.
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

# Numbers a note states about structure. Deliberately narrow: `1,833 test
# paths`, `(1436 files)`, `578 files`. A bare number in prose is not a claim
# about a tree and is not treated as one.
CLAIM = re.compile(
    r"(?P<number>\d[\d,]{1,9})\s*"
    r"(?P<unit>files?|paths?|entries|directories|notebooks?|scripts?|"
    r"tests?|fixtures?|schemas?|grammars?|documents?)\b",
    re.IGNORECASE)

CHECKED_SECTIONS = ("What Is Inside", "Architecture & Mechanics", "Reading Notes")

# A number an author deliberately approximated is not a number they got wrong.
# `tree-sitter` says "~30 files" against a survey recording 28, and reporting
# that as a contradiction punishes exactly the honest hedging that makes a note
# readable. Detected immediately before the number, so "around 150" is caught
# and "30 files, around which" is not.
HEDGE = re.compile(r"(?:~|≈|about|around|roughly|approximately|some|nearly|over"
                   r"|under|almost|circa|c\.)\s*$", re.IGNORECASE)

SUPPORTED = "supported"
UNSUPPORTED = "unsupported"
CONTRADICTED = "contradicted"


@dataclass(frozen=True)
class Claim:
    note: str
    repo_key: str
    number: int
    unit: str
    context: str
    status: str
    matched_by: str = ""
    nearest: int | None = None


def _quantities(repo_key: str, conn: Any) -> dict[str, set[int]]:
    """Every count the data layer holds for one source, by rough kind."""
    out: dict[str, set[int]] = {"total": set(), "signal": set(),
                                "directory": set(), "extension": set()}
    row = conn.execute("SELECT file_count FROM source WHERE repo_key = ?",
                       (repo_key,)).fetchone()
    if row and row["file_count"]:
        out["total"].add(int(row["file_count"]))
    for table, key in (("signal", "signal"), ("directory", "directory"),
                       ("extension", "extension")):
        for record in conn.execute(f"SELECT files FROM {table} WHERE repo_key = ?",
                                   (repo_key,)):
            if record["files"]:
                out[key].add(int(record["files"]))
    return out


def check(vault: Path | None = None, *,
          db_path: Path | None = None) -> list[Claim]:
    """Every structural number in every resource note, against the surveys."""
    target = Path(db_path or component_db_path())
    if not target.exists():
        return []
    root = vault or vault_root()
    conn = connect(target)
    claims: list[Claim] = []
    try:
        for note in notes_mod.load_vault(root):
            if note.layer not in ("resource", "review"):
                continue
            repo_key = note.string("repo_key")
            if not repo_key:
                continue
            quantities = _quantities(repo_key, conn)
            everything = set().union(*quantities.values()) if quantities else set()
            if not everything:
                continue                      # never surveyed; not a note defect
            for heading in CHECKED_SECTIONS:
                text = note.section(heading) or ""
                for match in CLAIM.finditer(text):
                    number = int(match.group("number").replace(",", ""))
                    if number < 3:            # "two notebooks" is not a survey claim
                        continue
                    unit = match.group("unit").lower()
                    start = max(0, match.start() - 44)
                    context = " ".join(text[start:match.end() + 24].split())
                    if number in everything:
                        where = next(k for k, v in quantities.items() if number in v)
                        claims.append(Claim(note.name, repo_key, number, unit,
                                            context, SUPPORTED, where))
                        continue
                    # Off-by-a-little against a real quantity is a note that
                    # was edited after the survey, or a miscount. Either way a
                    # person should look; a number with no neighbour at all is
                    # far more likely to be counting something else entirely.
                    nearest = min(everything, key=lambda v: abs(v - number))
                    close = abs(nearest - number) <= max(2, number * 0.02)
                    hedged = bool(HEDGE.search(text[:match.start()]))
                    claims.append(Claim(
                        note.name, repo_key, number, unit, context,
                        CONTRADICTED if (close and not hedged) else UNSUPPORTED,
                        nearest=nearest))
    finally:
        conn.close()
    return claims


def summarise(claims: Sequence[Claim]) -> dict[str, int]:
    out = {SUPPORTED: 0, UNSUPPORTED: 0, CONTRADICTED: 0}
    for claim in claims:
        out[claim.status] += 1
    return out


def format_report(claims: Sequence[Claim], *, show: str = CONTRADICTED,
                  limit: int = 25) -> str:
    counts = summarise(claims)
    total = sum(counts.values()) or 1
    lines = [
        "Claim provenance - structural numbers in notes, against the surveys",
        "",
        f"  {counts[SUPPORTED]:>4} supported     ({counts[SUPPORTED] / total:.0%}) "
        "- the survey holds a row with that number",
        f"  {counts[CONTRADICTED]:>4} contradicted  ({counts[CONTRADICTED] / total:.0%}) "
        "- a corresponding quantity exists and differs",
        f"  {counts[UNSUPPORTED]:>4} unsupported   ({counts[UNSUPPORTED] / total:.0%}) "
        "- no row matches; usually counting something the signals do not model",
        "",
    ]
    selected = [c for c in claims if c.status == show][:limit]
    if selected:
        lines.append(f"  showing {show}:")
        for claim in selected:
            near = f" (nearest recorded: {claim.nearest})" if claim.nearest else ""
            lines.append(f"    {claim.note}")
            lines.append(f"       {claim.number} {claim.unit}{near}")
            lines.append(f"       ...{claim.context}...")
    lines += ["",
              "  Judgements are not checked and cannot be. This is arithmetic over",
              "  a survey, which is the half of a note that can be wrong quietly."]
    return "\n".join(lines)
