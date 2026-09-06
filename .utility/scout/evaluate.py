"""Stage 3 - the evaluator, and Stage 4 - the cohort gate.

No model runs in this module. Ranking is arithmetic over signals already
collected, so it is reproducible, explainable and free to re-run whenever the
weights change.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import ScoutConfig, vault_root as _vault_root
from . import db
from .domains import resource_counts
from .rank import score_candidate, explain

DOMAIN_TO_TOPIC = {
    "ml_training_mlops": "agentic_ai_models",
    "signal_audio_speech": "agentic_ai_models",
    "vision_imaging": "geospatial_earth_data",
    "knowledge_management": "curated_lists",
    "distributed_systems": "infrastructure_observability",
    "testing_verification": "architecture_playbooks",
    "crypto_identity": "security_siem",
    "manufacturing_fabrication": "cad_saas_design",
}


def existing_catalogue_keys(vault_root: Path | None = None) -> set[str]:
    """repo_keys already catalogued, so rediscovery becomes corroboration
    rather than a duplicate note."""
    root = vault_root or _vault_root()
    keys: set[str] = set()
    import re
    for folder in ("01-Resources", "04-Reviews"):
        directory = root / folder
        if not directory.exists():
            continue
        for path in directory.glob("*.md"):
            head = path.read_text(encoding="utf-8").split("\n---\n", 1)[0]
            match = re.search(r'^repo_key:\s*"([^"]+)"', head, re.M)
            if match:
                keys.add(match.group(1).lower())
    return keys


def run(conn, cfg: ScoutConfig, vault_root: Path | None = None,
        now: datetime | None = None) -> dict[str, int]:
    rows = db.fetch_state(conn, "scouted")
    if not rows:
        return {"ranked": 0, "rejected_duplicate": 0}

    counts = resource_counts(vault_root)
    catalogued = existing_catalogue_keys(vault_root)
    ranked = duplicates = 0
    reference = now or datetime.now(timezone.utc)

    for row in rows:
        key = (row["repo_key"] or "").lower()
        if key and key in catalogued:
            # Already in the catalogue. The sighting is still information:
            # it raises that resource's corroboration, which is why the row
            # is rejected rather than deleted.
            db.update(conn, row["id"], state="rejected",
                      last_error="already catalogued; recorded as corroboration")
            duplicates += 1
            continue

        domain = row["domain_key"] or "unmatched"
        topic_key = DOMAIN_TO_TOPIC.get(domain, domain)
        # An unmatched or brand-new domain has no resources yet, which is
        # exactly the gap the ranker should reward.
        domain_count = counts.get(topic_key, 0)

        record = {
            "domain_key": domain,
            "corroboration": int(row["corroboration"] or 1),
            "github": json.loads(row["github_json"] or "{}") if row["github_json"] else {},
        }
        score, signals = score_candidate(record, cfg.weights, domain_count, reference)
        db.record_signals(conn, row["id"], [
            {"signal": s.signal, "value": s.value, "weight": s.weight, "detail": s.detail}
            for s in signals])
        db.update(conn, row["id"], state="ranked", score=score)
        ranked += 1

    return {"ranked": ranked, "rejected_duplicate": duplicates}


def enrich_depth(conn, cfg: ScoutConfig, limit: int = 50) -> int:
    """Fill the depth signal for scouted rows before ranking.

    One extra GitHub request per candidate, so it is a separate opt-in step -
    without a token the rate limit makes it impractical at volume.
    """
    from .discovery import (probe_depth, resolve_license, resolve_repo_key,
                            RateLimited)
    rows = db.fetch_state(conn, "scouted", limit)
    updated = 0
    for row in rows:
        if not row["repo_key"]:
            continue
        gh = json.loads(row["github_json"] or "{}") if row["github_json"] else {}
        if "readme_bytes" in gh:
            continue
        try:
            gh.update(probe_depth(row["repo_key"], cfg))
            # One more request, and only for the candidates that need it: the
            # API says NOASSERTION for every composite and every
            # source-available licence, so an unresolved spdx is a question
            # rather than an answer. `license_class` eliminates in
            # `find_donor`, which is why it is worth the request.
            resolved = resolve_license(row["repo_key"], gh.get("license_spdx"), cfg)
            if resolved:
                gh.update(resolved)
            # A renamed repository rediscovered at its new path would otherwise
            # become a second candidate, and one held at its old path keeps a
            # canonical URL that will stop resolving. Two of seventeen sources
            # in the 2026-09 cohort had moved.
            moved = resolve_repo_key(row["repo_key"], cfg)
            if moved:
                gh.update(moved)
        except RateLimited:
            break
        db.update(conn, row["id"], github_json=json.dumps(gh))
        updated += 1
    return updated


def freeze(conn, cfg: ScoutConfig, vault_root: Path | None = None,
           force: bool = False) -> dict[str, Any]:
    """Stage 4 - freeze a cohort once enough ranked items exist."""
    ready = len(db.fetch_state(conn, "ranked"))
    if ready < cfg.cohort_size and not force:
        return {"frozen": False, "ready": ready, "needed": cfg.cohort_size}
    cohort_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M")
    rows = db.freeze_cohort(conn, cohort_id, cfg.cohort_size)
    note = write_cohort_note(conn, cohort_id, rows, vault_root)
    conn.execute("UPDATE scout_cohort SET note_path = ? WHERE cohort_id = ?",
                 (str(note), cohort_id))
    return {"frozen": True, "cohort_id": cohort_id, "size": len(rows),
            "note": str(note)}


def write_cohort_note(conn, cohort_id: str, rows: list[Any],
                      vault_root: Path | None = None) -> Path:
    """The cohort note exists so the ordering can be challenged before any
    expensive work begins, not audited after it."""
    root = vault_root or _vault_root()
    directory = root / "07-Scouting"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"Scout Cohort {cohort_id}.md"

    lines = [
        "---",
        'type: "scout_cohort"',
        f'cohort_id: "{cohort_id}"',
        f'frozen_at: "{db.now_iso()}"',
        f"size: {len(rows)}",
        'status: "queued"',
        "---",
        "",
        f"# Scout Cohort {cohort_id}",
        "",
        "## How To Read This",
        "Items are consumed in descending score. An interrupted run resumes at the",
        "highest-ranked incomplete item, so the most valuable sources are always",
        "finished first. Reorder or strike out rows here before running the deep",
        "dive if the ranking has got something wrong.",
        "",
        "## Queue",
        "| # | Score | Domain | Source | What it is |",
        "| --- | --- | --- | --- | --- |",
    ]
    for index, row in enumerate(rows, 1):
        one_line = (row["one_line"] or "").replace("|", "/")[:110]
        lines.append(f"| {index} | {row['score']:.1f} | {row['domain_key'] or '-'} | "
                     f"[{row['title'] or row['url']}]({row['url']}) | {one_line} |")

    lines += ["", "## Score Components", ""]
    for row in rows[:10]:
        lines.append(f"**{row['title'] or row['url']}** - {row['score']:.1f}")
        for signal in db.signals_for(conn, row["id"]):
            lines.append(f"- {signal['signal']}: {signal['value'] * signal['weight']:.1f} "
                         f"({signal['detail']})")
        lines.append("")
    lines += ["## Related", "- [[Schema Extension - Scouting Pipeline]]",
              "- [[Scouting Domains]]", ""]

    path.write_text("\n".join(lines), encoding="utf-8")
    return path
