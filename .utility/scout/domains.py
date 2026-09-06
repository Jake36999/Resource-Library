"""Domain register.

Markdown is authoritative, per the platform rule that retrieved and worker
content cannot expand workflow scope. The scout may not invent a domain; it
may only report `unmatched`, which surfaces as a candidate new theme for a
human to accept or reject.

Domains are parsed out of `00-Indexes/Scouting Domains.md` rather than held in
code, so editing the note is how the rotation changes.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .config import ScoutConfig, vault_root as _vault_root

# **Name** (`domain_key`)  ... Seed queries: `a`, `b`, `c`
HEADING = re.compile(r"^\*\*(?P<name>[^*]+)\*\*\s*\(`(?P<key>[a-z0-9_]+)`\)\s*$", re.M)
SEEDS = re.compile(r"^Seed queries:\s*(?P<body>.+)$", re.M)
TIER = re.compile(r"^###\s*Tier\s*(?P<tier>\d)", re.M)


@dataclass(frozen=True)
class Domain:
    key: str
    name: str
    tier: int
    description: str
    seed_queries: tuple[str, ...]


def parse(text: str) -> list[Domain]:
    domains: list[Domain] = []
    # Establish which tier section each heading falls under.
    tier_marks = [(m.start(), int(m.group("tier"))) for m in TIER.finditer(text)]

    def tier_at(pos: int) -> int:
        current = 1
        for start, tier in tier_marks:
            if start < pos:
                current = tier
            else:
                break
        return current

    matches = list(HEADING.finditer(text))
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[start:end]
        seeds: tuple[str, ...] = ()
        seed_match = SEEDS.search(block)
        if seed_match:
            seeds = tuple(q.strip() for q in re.findall(r"`([^`]+)`", seed_match.group("body")))
        description = block
        if seed_match:
            description = block[:seed_match.start()]
        description = " ".join(description.split())
        domains.append(Domain(
            key=match.group("key"),
            name=match.group("name").strip(),
            tier=tier_at(match.start()),
            description=description,
            seed_queries=seeds,
        ))
    return domains


def load(cfg: ScoutConfig | None = None, vault_root: Path | None = None) -> list[Domain]:
    cfg = cfg or ScoutConfig.load()
    root = vault_root or _vault_root()
    note = root / cfg.domains_note
    if not note.exists():
        raise FileNotFoundError(
            f"Domain register not found at {note}. The scout cannot run without an "
            "authoritative domain list."
        )
    return parse(note.read_text(encoding="utf-8"))


def rotation(cfg: ScoutConfig | None = None, vault_root: Path | None = None,
             include_tier2: bool = False) -> list[Domain]:
    """Domains currently eligible for scouting."""
    domains = load(cfg, vault_root)
    return [d for d in domains if d.tier == 1 or include_tier2]


def resource_counts(vault_root: Path | None = None) -> dict[str, int]:
    """Approved resources per topic_key, read from the topic index notes.

    This feeds the gap-fit signal, so it must reflect the vault as it actually
    stands rather than a cached number.
    """
    root = vault_root or _vault_root()
    counts: dict[str, int] = {}
    index_dir = root / "00-Indexes"
    if not index_dir.exists():
        return counts
    for path in index_dir.glob("Topic - *.md"):
        text = path.read_text(encoding="utf-8")
        key_match = re.search(r'^topic_key:\s*"([^"]+)"', text, re.M)
        count_match = re.search(r"^resource_count:\s*(\d+)", text, re.M)
        if key_match:
            counts[key_match.group(1)] = int(count_match.group(1)) if count_match else 0
    return counts
