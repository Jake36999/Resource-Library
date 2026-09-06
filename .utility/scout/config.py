"""Configuration for the scouting pipeline.

Every tunable lives in library_config.json under "scout" so ranking behaviour
can be changed without touching code. Secrets are never read from here - API
keys come from the environment only, and are never written to disk.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

UTILITY_ROOT = Path(__file__).resolve().parent.parent
VAULT_ROOT = UTILITY_ROOT.parent
CONFIG_PATH = UTILITY_ROOT / "library_config.json"
# Resolved per call, not frozen at import. The constant pointed at
# `.utility/solutions_library.sqlite` for a day after the databases moved to
# `.Data/Databases/`, and nothing noticed - because nothing runs the scout
# pipeline. A stale path in an unexercised module is invisible twice over.
def db_path() -> Path:
    from librarian.config import database_dir

    return database_dir() / "solutions_library.sqlite"


DB_PATH = db_path()
STAGING_DIR = UTILITY_ROOT / "staging"
DOSSIER_DIR = STAGING_DIR / "dossiers"
LOG_DIR = UTILITY_ROOT / "logs"

DEFAULT_WEIGHTS = {
    "gap_fit": 30.0,
    "corroboration": 20.0,
    "vitality": 15.0,
    "reusability": 15.0,
    "adoption": 10.0,
    "depth": 10.0,
}


@dataclass(frozen=True)
class ScoutConfig:
    enabled: bool = True
    cohort_size: int = 100
    discovery_per_query: int = 15
    scout_batch_size: int = 50
    max_attempts: int = 3
    lease_seconds: int = 2400
    weights: dict[str, float] = field(default_factory=lambda: dict(DEFAULT_WEIGHTS))
    # Stage batching is mandatory: config/runtime.json on this host allows one
    # resident task model, so scouting and deep diving must not interleave.
    scout_model: str = ""
    research_model: str = ""
    escalate_top_fraction: float = 0.10
    escalate_below_confidence: float = 0.45
    # Stage 5 delegates to the ToolSet rather than reading a README alone:
    # shallow clone, run_guided_repository_investigation, read the slice as
    # evidence, delete the clone. Off by default so the pipeline still runs
    # with the ToolSet disconnected and so tests need no network; turned on in
    # library_config.json. The slice is never retained (spec decision 7.2).
    toolchain_evidence: bool = False
    escalation_provider: str = "none"   # none | openai | anthropic
    escalation_model: str = ""
    domains_note: str = "00-Indexes/Scouting Domains.md"
    seed_file: str = "repositories to chart.md"
    github_api_base: str = "https://api.github.com"
    request_timeout: int = 20
    user_agent: str = "Resource-Library-Scout"

    @classmethod
    def load(cls, path: Path | None = None) -> "ScoutConfig":
        raw: dict[str, Any] = {}
        target = path or CONFIG_PATH
        if target.exists():
            try:
                raw = json.loads(target.read_text(encoding="utf-8")).get("scout", {}) or {}
            except Exception:
                raw = {}
        weights = dict(DEFAULT_WEIGHTS)
        for key, value in (raw.get("weights") or {}).items():
            if key in weights:
                try:
                    weights[key] = float(value)
                except (TypeError, ValueError):
                    pass
        known = {f for f in cls.__dataclass_fields__ if f != "weights"}
        kwargs = {k: v for k, v in raw.items() if k in known}
        return cls(weights=weights, **kwargs)


def github_token() -> str | None:
    """Environment only. A token raises the rate limit from 60/hr to 5000/hr."""
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_API_TOKEN")


def escalation_key(provider: str) -> str | None:
    if provider == "openai":
        return os.environ.get("OPENAI_API_KEY")
    if provider == "anthropic":
        return os.environ.get("ANTHROPIC_API_KEY")
    return None


def vault_root() -> Path:
    """The vault this run operates on. Mirrors `librarian.config.vault_root`.

    Duplicated rather than imported so `scout` keeps no import-time dependency
    on `librarian`; the environment variable is the shared contract.
    """
    return Path(os.environ.get("CATALOGUE_VAULT", VAULT_ROOT))
