"""Deterministic ranking.

The ranker is code, not a model. A small local model asked to score
"importance" produces numbers that are neither reproducible across runs nor
comparable between items, and a queue ordered by noise is worse than a queue
ordered by arrival because it looks principled.

Every function here is pure so the ordering can be unit-tested and explained.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

# librarian never imports scout, so this direction is safe; the posture is
# catalogue policy and belongs in one place rather than two.
from librarian.config import catalogue_role, distribution_posture

PERMISSIVE = {"mit", "mit-0", "apache-2.0", "bsd", "bsd-2-clause", "bsd-3-clause",
              "isc", "unlicense", "0bsd", "zlib", "cc0-1.0", "postgresql", "python-2.0",
              # PSF is the Python standard library's licence, met wherever a
              # project vendors stdlib code. CC-BY-4.0 is a content licence and
              # the right answer for a specification repository, which is what
              # `syntax-tree/mdast` turned out to be.
              "psf-2.0", "cc-by-4.0"}
WEAK_COPYLEFT = {"lgpl", "lgpl-2.1", "lgpl-3.0", "mpl-2.0", "epl-2.0", "cddl-1.0"}
COPYLEFT = {"gpl", "gpl-2.0", "gpl-3.0", "gpl-3.0-or-later", "agpl", "agpl-3.0",
            "cc-by-sa-4.0", "osl-3.0"}
# Source-available licences let you read the code but restrict use, and are not
# OSI open source. GitHub reports most of them as NOASSERTION, so they arrive
# looking like "unknown" when they are in fact a known and restrictive answer.
SOURCE_AVAILABLE = {"busl-1.1", "bsl-1.1", "fsl-1.1", "fsl-1.1-apache-2.0",
                    "elastic-2.0", "sspl-1.0", "hippocratic-2.1", "commons-clause"}


UNRESOLVED_SPDX = {"", "unknown", "noassertion", "other", "none", "null"}

# How much each class restricts reuse. Used only to pick the answer for a
# LICENSE that names several licences: the most restrictive one present is the
# one that governs what a reuser may actually do, so it is the safe reading.
# Unknown sits at the top because "we could not tell" must never be quieter
# than "we could tell, and it was fine".
RESTRICTIVENESS = {"Permissive": 0, "Weak_Copyleft": 1, "Copyleft": 2,
                   "Source_Available": 3, "Unknown": 4}


def spdx_is_unresolved(spdx: str | None) -> bool:
    """True when the API has told us nothing usable and the text must be read."""
    return (spdx or "").strip().lower() in UNRESOLVED_SPDX


def license_class(spdx: str | None) -> str:
    low = (spdx or "").strip().lower()
    if spdx_is_unresolved(low):
        return "Unknown"
    if low in PERMISSIVE:
        return "Permissive"
    if low in WEAK_COPYLEFT:
        return "Weak_Copyleft"
    if low in COPYLEFT:
        return "Copyleft"
    if low in SOURCE_AVAILABLE:
        return "Source_Available"
    return "Unknown"


# ------------------------------------------------------- licence from text

# The GPL family is the hard case and the reason this is not simple substring
# matching. Every one of these texts names its siblings: LGPL-2.1 refers to the
# GPL throughout, and GPL-3.0 names both the AGPL and the LGPL in its closing
# sections. A naive match reports three licences for a file that grants one.
#
# The discriminator is position. A licence document opens with its own title,
# and refers to its relatives later, so within this family the marker that
# appears *earliest* is the licence that actually governs.
GPL_FAMILY = (
    ("AGPL", "gnu affero general public license"),
    ("LGPL", "gnu lesser general public license"),
    ("GPL", "gnu general public license"),
)
GPL_SPDX = {("AGPL", "3"): "AGPL-3.0", ("AGPL", ""): "AGPL-3.0",
            ("LGPL", "2.1"): "LGPL-2.1", ("LGPL", "3"): "LGPL-3.0",
            ("LGPL", ""): "LGPL-2.1",
            ("GPL", "2"): "GPL-2.0", ("GPL", "3"): "GPL-3.0", ("GPL", ""): "GPL-3.0"}
VERSION_NEAR = re.compile(r"version\s+(3|2\.1|2)\b")

# Distinctive strings from each licence's own body. Matching the body is strong
# evidence: the licence is here, not merely referred to.
LICENCE_BODY = (
    ("MPL-2.0", "mozilla public license version 2.0"),
    ("Apache-2.0", "apache license, version 2.0"),
    ("Apache-2.0", "licensed under the apache license"),
    ("Apache-2.0", "apache license version 2.0, january 2004"),
    ("MIT", "permission is hereby granted, free of charge"),
    ("ISC", "permission to use, copy, modify, and/or distribute this software"),
    ("BSD-3-Clause", "neither the name of"),
    ("BSD-2-Clause", "redistribution and use in source and binary forms"),
    ("Unlicense", "this is free and unencumbered software released into the public domain"),
    ("CC0-1.0", "creative commons legal code"),
    ("CC-BY-SA-4.0", "attribution-sharealike 4.0"),
    ("CC-BY-4.0", "attribution 4.0 international"),
    ("BUSL-1.1", "business source license 1.1"),
    ("Elastic-2.0", "elastic license 2.0"),
    ("SSPL-1.0", "server side public license"),
    ("PSF-2.0", "python software foundation license"),
)

# Licences named in prose rather than reproduced. Weaker evidence, and the
# reason a composite is flagged rather than resolved: a LICENSE saying "some
# files are PSF licensed" is telling you the file you care about may not be
# under the licence whose text follows it.
LICENCE_MENTION = (
    ("PSF-2.0", "psf licensed"),
    ("PSF-2.0", "python software foundation"),
    ("Apache-2.0", "apache licensed"),
    ("Apache-2.0", "apache 2.0"),
    ("Apache-2.0", "apache-2.0"),
    ("MIT", "mit licensed"),
    ("MIT", "mit license"),
    ("MPL-2.0", "mozilla public license"),
    ("CC-BY-4.0", "creative commons attribution 4.0"),
    ("CC-BY-SA-4.0", "creative commons attribution-sharealike"),
)


@dataclass(frozen=True)
class LicenceReading:
    """What the licence text actually said, and whether we are sure of it."""
    names: tuple[str, ...]        # every SPDX id the text supports
    license_class: str            # the most restrictive class present
    composite: bool               # more than one distinct licence named
    review_required: bool         # a person must confirm before this is trusted
    evidence: str                 # why, in one line

    joiner: str = " AND "

    @property
    def spdx(self) -> str:
        """One identifier when there is one, else all of them joined. Never a
        guess: a composite reports everything it found rather than picking."""
        return self.joiner.join(self.names) if self.names else "Unknown"


def _gpl_member(low: str) -> str | None:
    """Which GPL-family licence a text grants, by earliest title occurrence."""
    seen: list[tuple[int, str]] = []
    for family, marker in GPL_FAMILY:
        at = low.find(marker)
        if at >= 0:
            seen.append((at, family))
    if not seen:
        return None
    at, family = min(seen)
    window = low[at:at + 200]
    match = VERSION_NEAR.search(window)
    return GPL_SPDX.get((family, match.group(1) if match else ""))


def license_from_text(text: str, readme: str = "") -> LicenceReading:
    """Classify a LICENSE file deterministically. No model, no guessing.

    A text naming several licences returns all of them, the most restrictive
    class among them, and `review_required=True` - because the correct answer
    for a composite is a person reading it, and a confident single answer would
    be exactly the plausible guess `EVIDENCE_REQUIRED` forbids.

    `readme` is the fallback for repositories that state their licence in prose
    and ship no LICENSE file. It is always weaker evidence, so a reading that
    rests on it always requires review.
    """
    low = " ".join((text or "").lower().split())
    source = "LICENSE"
    if not low and readme:
        low = " ".join(_license_section(readme).lower().split())
        source = "readme"
    if not low:
        return LicenceReading((), "Unknown", False, True, "no licence text found")

    # The authoritative answer, when the file bothers to state one.
    expression = spdx_expression(low)
    if expression:
        names, choice = expression
        classes = [license_class(n) for n in names]
        picked = (min if choice else max)(classes,
                                          key=lambda c: RESTRICTIVENESS[c])
        joiner = " OR " if choice else " AND "
        return LicenceReading(
            names, picked, len(names) > 1,
            len(names) > 1 or picked == "Unknown" or source == "readme",
            f"{source} declares SPDX-License-Identifier: " + joiner.join(names),
            joiner=joiner)

    found: list[str] = []
    gpl = _gpl_member(low)
    if gpl:
        found.append(gpl)
    for spdx, marker in LICENCE_BODY:
        if marker in low and spdx not in found:
            found.append(spdx)
    if "BSD-3-Clause" in found and "BSD-2-Clause" in found:
        found.remove("BSD-2-Clause")     # 3-clause is 2-clause plus a clause

    body_count = len(found)
    for spdx, marker in LICENCE_MENTION:
        if marker in low and spdx not in found:
            found.append(spdx)
    for spdx, pattern in SPDX_TOKEN:
        if spdx not in found and pattern.search(low):
            found.append(spdx)

    if not found:
        return LicenceReading((), "Unknown", False, True,
                              f"{source} present but matched no known licence")

    names = tuple(sorted(found))
    composite = len(names) > 1
    # A composite read from prose is always a conjunction: this file is MIT,
    # that vendored one is PSF, and the most restrictive licence present
    # governs what a reuser may do.
    #
    # A *choice* between licences is only ever inferred from an explicit SPDX
    # `OR` expression, handled above. It was briefly inferred from wording too,
    # and that was wrong in a way worth recording: "either version 3 of the
    # License, or (at your option) any later version" is GPL and AGPL
    # boilerplate present in every copy of those licences, and it describes a
    # choice between *versions of one licence*, not between licences. Reading
    # it as a choice took the least restrictive name in the list and reported
    # ckan (AGPL-3.0) and wazuh (GPL-2.0) as Permissive - the exact direction
    # of error that puts a copyleft project into a permissive-only answer.
    worst = max((license_class(n) for n in names),
                key=lambda c: RESTRICTIVENESS[c])
    referred = len(names) - body_count
    detail = (f"{body_count} reproduced in full, {referred} referred to"
              if composite else
              "reproduced in full" if body_count else "referred to only")
    return LicenceReading(
        names, worst, composite,
        composite or worst == "Unknown" or source == "readme",
        f"{source} names " + ", ".join(names) + f" ({detail})")


# SPDX identifiers written as bare tokens, which is how a readme states a
# licence rather than reproducing it. `[CC-BY-4.0][license] (c) Titus Wormer`
# is the entire licence declaration in `syntax-tree/mdast`, and no prose
# marker reaches it. Applied last, so a reproduced licence body always wins.
SPDX_TOKEN = tuple((spdx, re.compile(pattern, re.I))
                   for spdx, pattern in (
    ("CC-BY-SA-4.0", r"\bcc[\s-]?by[\s-]?sa[\s-]?4\.0\b"),
    ("CC-BY-4.0", r"\bcc[\s-]?by[\s-]?4\.0\b"),
    ("CC0-1.0", r"\bcc0[\s-]?1\.0\b"),
    ("Apache-2.0", r"\bapache[\s-]?2\.0\b"),
    ("AGPL-3.0", r"\bagpl[\s-]?v?3(?:\.0)?\b"),
    ("LGPL-2.1", r"\blgpl[\s-]?v?2\.1\b"),
    ("LGPL-3.0", r"\blgpl[\s-]?v?3(?:\.0)?\b"),
    ("GPL-3.0", r"\bgpl[\s-]?v?3(?:\.0)?\b"),
    ("GPL-2.0", r"\bgpl[\s-]?v?2(?:\.0)?\b"),
    ("MPL-2.0", r"\bmpl[\s-]?2\.0\b"),
    ("BSD-3-Clause", r"\bbsd[\s-]?3[\s-]?clause\b"),
    ("BSD-2-Clause", r"\bbsd[\s-]?2[\s-]?clause\b"),
    ("MIT", r"\bmit\b"),
    ("ISC", r"\bisc\b"),
    ("Unlicense", r"\bunlicense\b"),
))


# An explicit SPDX expression is the authoritative answer and outranks every
# heuristic below it. `Apache-2.0 OR GPL-2.0-only` is a choice offered to the
# reuser; `MIT AND PSF-2.0` is a combination binding all of it.
SPDX_EXPRESSION = re.compile(
    r"spdx-license-identifier\s*:\s*([a-z0-9.\-+ ()]+?)(?:\s*$|[\n`\"'])", re.I)
SPDX_NORMALISE = {"gpl-2.0-only": "GPL-2.0", "gpl-3.0-only": "GPL-3.0",
                  "gpl-2.0-or-later": "GPL-2.0", "gpl-3.0-or-later": "GPL-3.0",
                  "lgpl-2.1-only": "LGPL-2.1", "lgpl-3.0-only": "LGPL-3.0",
                  "agpl-3.0-only": "AGPL-3.0", "agpl-3.0-or-later": "AGPL-3.0",
                  "bsd-3-clause": "BSD-3-Clause", "bsd-2-clause": "BSD-2-Clause",
                  "apache-2.0": "Apache-2.0", "mit": "MIT", "isc": "ISC",
                  "mpl-2.0": "MPL-2.0", "psf-2.0": "PSF-2.0",
                  "cc-by-4.0": "CC-BY-4.0", "cc-by-sa-4.0": "CC-BY-SA-4.0",
                  "cc0-1.0": "CC0-1.0", "unlicense": "Unlicense",
                  "busl-1.1": "BUSL-1.1", "elastic-2.0": "Elastic-2.0"}


def spdx_expression(text: str) -> tuple[tuple[str, ...], bool] | None:
    """Licences named by an SPDX expression, and whether they are a choice.

    Returns None when the text states no expression, so callers fall through
    to reading the licence body.
    """
    match = SPDX_EXPRESSION.search(text or "")
    if not match:
        return None
    raw = match.group(1).strip().strip("`\"'").replace("(", " ").replace(")", " ")
    parts = [p for p in re.split(r"\s+", raw) if p]
    choice = any(p.upper() == "OR" for p in parts)
    names: list[str] = []
    for part in parts:
        if part.upper() in {"AND", "OR", "WITH"}:
            continue
        spdx = SPDX_NORMALISE.get(part.lower(), part)
        if spdx not in names:
            names.append(spdx)
    return (tuple(sorted(names)), choice) if names else None


LICENSE_HEADING = re.compile(r"^#{1,6}\s*licen[cs]e\b.*$", re.M | re.I)


def _license_section(readme: str) -> str:
    """The `## License` section of a readme, or nothing.

    Deliberately narrow. A repository that states its licence only in prose is
    a repository whose licence needs a person to confirm, and this exists to
    stop that case being silently recorded as Unknown when the answer was
    written down - which is what `syntax-tree/mdast` did.
    """
    match = LICENSE_HEADING.search(readme or "")
    if not match:
        return ""
    rest = readme[match.end():]
    nxt = re.search(r"^#{1,6}\s+", rest, re.M)
    return rest[:nxt.start()] if nxt else rest[:1000]


@dataclass(frozen=True)
class Signal:
    signal: str
    value: float      # normalised 0..1
    weight: float
    detail: str = ""

    @property
    def points(self) -> float:
        return self.value * self.weight


# ------------------------------------------------------------ components

def gap_fit(domain_resource_count: int, target: int = 10) -> float:
    """Highest when the destination topic is thinnest.

    Coverage breadth is the catalogue's actual goal, so this carries the
    largest weight. It also self-limits: once a topic fills, it stops
    attracting new work, which is what stops automated scouting from
    producing a mile-wide, inch-deep catalogue.
    """
    if domain_resource_count < 0:
        domain_resource_count = 0
    if domain_resource_count >= target:
        return 0.0
    return round(1.0 - (domain_resource_count / target), 4)


def corroboration(times_seen: int) -> float:
    """Independent rediscovery. Two sightings is the meaningful threshold;
    beyond four there is no additional information."""
    if times_seen <= 1:
        return 0.0
    if times_seen == 2:
        return 0.6
    if times_seen == 3:
        return 0.85
    return 1.0


# Two scales, chosen by `usage.catalogue_role`. See `LOCATE_DO_NOT_ADJUDICATE`
# in the Design Specification for why there are two.
VITALITY_FLOORS = {
    # Selecting components to depend on: a dead dependency is a liability, and
    # an archived one will never take a security fix.
    "integration": {"archived": 0.0, "unknown": 0.2, "stale": 0.1, "ageing": 0.3},
    # Locating prior work for a person to read: an archived repository is
    # *settled*, which for reading is a virtue rather than a defect - it will
    # not move under you, and its lessons are finished. Maintained still ranks
    # higher, because currency is genuine information; it is no longer the
    # difference between visible and invisible.
    "reference": {"archived": 0.55, "unknown": 0.45, "stale": 0.4, "ageing": 0.55},
}


def vitality(pushed_at: str | None, archived: bool = False,
             now: datetime | None = None, role: str | None = None) -> float:
    """Recency of the last push, scaled by what the catalogue is for.

    Changed 2026-09-04. This function used to open `if archived: return 0.0`,
    with a docstring reading *a dead repository teaches history, not practice*
    - and teaching history is exactly what a reference guide is for. Under a
    15-point weight that zero removed every archived repository from
    contention, including nine of the 2026-09-04 cohort and several of its most
    instructive entries: [[ajaxorg - treehugger]], [[cst - cst]] and
    [[Azure-Samples - graphrag-accelerator]] are all read for their design, and
    none of them is going anywhere.
    """
    floors = VITALITY_FLOORS[role or catalogue_role()]
    if archived:
        return floors["archived"]
    if not pushed_at:
        return floors["unknown"]
    try:
        stamp = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
    except ValueError:
        return floors["unknown"]
    reference = now or datetime.now(timezone.utc)
    days = (reference - stamp).days
    if days <= 30:
        return 1.0
    if days <= 90:
        return 0.85
    if days <= 365:
        return 0.6
    if days <= 730:
        return floors["ageing"]
    return floors["stale"]


# Two scales, chosen by `usage.distribution_posture` in library_config.json.
# The licence *facts* are identical under both; what a licence costs is not.
REUSABILITY_SCALES = {
    # Output may end up in something published, so a licence that forbids
    # integration really does make a resource less useful, and a repository
    # with no licence has granted nothing.
    "distributed": {"Permissive": 1.0, "Weak_Copyleft": 0.67, "Copyleft": 0.33,
                    "Source_Available": 0.1, "Unknown": 0.0},
    # This catalogue's actual posture. Nothing here is published, so reading a
    # repository, running it, and copying from it all trigger no obligation.
    # Licence stops being decisive and becomes a mild preference for keeping
    # future options open - a 15% spread that can break a tie and can never
    # bury a better answer.
    #
    # `Unknown` sits above `Source_Available` deliberately: a source-available
    # licence states restrictions, while an absent one states nothing. Under
    # private use neither binds, but only one of them has told you it intends
    # to.
    "private": {"Permissive": 1.0, "Weak_Copyleft": 0.95, "Copyleft": 0.90,
                "Source_Available": 0.80, "Unknown": 0.85},
}


def reusability(spdx: str | None, posture: str | None = None) -> float:
    """How much a licence should count against a candidate, given what this
    catalogue's output is for.

    Changed 2026-09-04. The single scale this replaced scored `Unknown` at a
    hard 0.0, which under a 15-point weight removed every unlicensed source
    from serious contention - and twelve of the 2026-09-04 cohort are
    unlicensed, most of them small academic or single-author repositories where
    publishing without a licence is normal rather than a refusal. For a private
    R&D catalogue that was the wrong question being asked with great
    confidence: the question is *can I read this, run this, or take from this*,
    and privately the answer to all three is yes.

    Set `usage.distribution_posture` to `distributed` to restore the strict
    scale before any of this is published.
    """
    scale = REUSABILITY_SCALES[posture or distribution_posture()]
    return scale[license_class(spdx)]


# The score an unstarred repository gets. Under `reference` it is deliberately
# well above zero: a discovery tool exists to surface work nobody has found,
# so treating "nobody found it" as evidence of worthlessness inverts the job.
ADOPTION_FLOORS = {"integration": 0.0, "reference": 0.35}


def adoption(stars: int | None, role: str | None = None) -> float:
    """Log-scaled deliberately. Linear stars would let a 200k-star framework
    bury a 500-star geospatial library that is far more relevant to a given
    project. Saturates around 100k.

    Changed 2026-09-04: the floor is no longer zero under the `reference` role.
    Six of the 2026-09-04 cohort have exactly zero stars, among them
    [[hannesfrank - Course-Knowledge-Graphs]], a graded graph fixture set that
    is immediately reusable, and [[corzosoft - azure-edm-reference-data-platform]],
    which is one of the fullest worked examples in the catalogue. Popularity is
    weak evidence of quality in either direction and it is *no* evidence for
    material that has never been indexed by anything.
    """
    floor = ADOPTION_FLOORS[role or catalogue_role()]
    n = max(0, int(stars or 0))
    if n <= 0:
        return floor
    return round(max(floor, min(1.0, math.log10(n + 1) / 5.0)), 4)


def depth(has_docs: bool = False, has_papers: bool = False,
          readme_bytes: int = 0, has_spec: bool = False) -> float:
    """Predicts whether an expensive deep dive will actually yield material.
    A repository with no prose rarely repays a careful read."""
    score = 0.0
    if has_docs:
        score += 0.35
    if has_papers:
        score += 0.30
    if has_spec:
        score += 0.15
    if readme_bytes >= 8000:
        score += 0.20
    elif readme_bytes >= 2000:
        score += 0.10
    return round(min(1.0, score), 4)


# ------------------------------------------------------------ composite

def score_candidate(record: dict[str, Any], weights: dict[str, float],
                    domain_resource_count: int,
                    now: datetime | None = None,
                    posture: str | None = None,
                    role: str | None = None) -> tuple[float, list[Signal]]:
    """Return (0-100 score, component signals).

    Signals are returned alongside the total because a rank you cannot
    explain is a rank you cannot trust or tune.
    """
    gh = record.get("github") or {}
    signals = [
        Signal("gap_fit", gap_fit(domain_resource_count), weights.get("gap_fit", 30.0),
               f"{domain_resource_count} resources already in {record.get('domain_key') or 'unmatched'}"),
        Signal("corroboration", corroboration(int(record.get("corroboration") or 1)),
               weights.get("corroboration", 20.0),
               f"seen {record.get('corroboration') or 1}x"),
        Signal("vitality", vitality(gh.get("pushed_at"), bool(gh.get("archived")), now, role),
               weights.get("vitality", 15.0),
               f"pushed {gh.get('pushed_at') or 'unknown'}"),
        Signal("reusability", reusability(gh.get("license_spdx"), posture),
               weights.get("reusability", 15.0),
               f"licence {gh.get('license_spdx') or 'unknown'}"),
        Signal("adoption", adoption(gh.get("stars"), role), weights.get("adoption", 10.0),
               f"{gh.get('stars') or 0} stars"),
        Signal("depth", depth(bool(gh.get("has_docs")), bool(gh.get("has_papers")),
                              int(gh.get("readme_bytes") or 0), bool(gh.get("has_spec"))),
               weights.get("depth", 10.0),
               f"readme {gh.get('readme_bytes') or 0}B"),
    ]
    total = round(sum(s.points for s in signals), 3)
    return total, signals


def explain(score: float, signals: list[Signal]) -> str:
    lines = [f"score {score:.1f}/100"]
    for s in sorted(signals, key=lambda x: -x.points):
        lines.append(f"  {s.signal:<14} {s.points:5.1f}  ({s.detail})")
    return "\n".join(lines)
