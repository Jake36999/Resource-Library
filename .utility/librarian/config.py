"""Configuration for the catalogue system.

Tunables live in `library_config.json` under "catalogue", alongside the
scouting pipeline's own block, so one file describes the whole operation.
Secrets are never read from here - the environment is the only source.

Paths are resolved once, at import, from this file's location. The vault is
the parent of `.utility`, which makes every module runnable from anywhere
without a working-directory assumption.
"""
from __future__ import annotations

import json
import os
from functools import lru_cache
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

UTILITY_ROOT = Path(__file__).resolve().parent.parent
VAULT_ROOT = UTILITY_ROOT.parent
CONFIG_PATH = UTILITY_ROOT / "library_config.json"

# Deliberately a separate database from solutions_library.sqlite: an index
# rebuild must not be able to disturb the scouting queue (spec 10.1).
# Defaults only. Resolve through `data_root()`, `database_dir()` and
# `index_db_path()` - a constant here is frozen at import and cannot follow
# `CATALOGUE_VAULT`.
DATA_ROOT = VAULT_ROOT / ".Data"
DATABASE_DIR = DATA_ROOT / "Databases"
INDEX_DB_PATH = DATABASE_DIR / "catalogue_index.sqlite"

LOG_DIR = UTILITY_ROOT / "logs"
WORKBENCH_ROOT = UTILITY_ROOT / "workbenches"
EVAL_PATH = Path(__file__).resolve().parent / "eval_questions.json"

# Folder -> layer. The folder is the primary signal because it is the one
# thing every note in this vault agrees on; frontmatter `type` refines it.
# Where the notes a *person* navigates live, and where the notes about the
# system's own construction live. Kept as constants because three modules look
# notes up by folder and a fourth writes them there.
INDEX_FOLDER = "00-Indexes"
INTERNAL_FOLDER = "internal docs"

LAYER_FOLDERS = {
    "00-Indexes": "index",
    # Development documentation: specifications, standards, working files,
    # operational records. Separated from `00-Indexes` on 2026-09-04 so the
    # navigational surface a reader opens is topics and sources, not the
    # system's own construction notes. Never an answerable layer.
    "internal docs": "internal",
    "01-Resources": "resource",
    "02-Glossary": "glossary",
    "03-Patterns": "pattern",
    "04-Reviews": "review",
    "06-Papers": "paper",
    "07-Scouting": "scouting",
    "08-Workflows": "workflow",
    "09-Applications": "application",
}

# Not indexed: generated visual artefacts and the operational layer.
SKIP_DIRS = {".obsidian", ".utility", ".git", "05-Canvases", "node_modules"}

LICENSE_CLASSES = (
    "Permissive", "Weak_Copyleft", "Copyleft", "Source_Available", "Unknown",
)

# Hubs route; they do not describe a source. They live in the same folders as
# the notes they route to, so the `type` field is what separates them.
#
# `topic_index` is deliberately NOT here. A topic index routes, but it is also
# a legitimate answer to "where does this subject live" - which is exactly
# what `orient` asks - so excluding it would empty the response it exists for.
HUB_TYPES = frozenset({
    "review_queue", "master_index", "domain_register",
})


def is_hub(note_type: str) -> bool:
    return note_type in HUB_TYPES or note_type.endswith("_hub")

# Hubs are excluded from centrality rather than down-weighted (spec 4B.3 R4):
# every resource note carries `taxonomy_hub:: [[Taxonomy Index]]`, so raw
# in-degree would rank the router above everything it routes to.
DEFAULT_CENTRALITY_EXCLUDE = (
    "Taxonomy Index",
    "Master Index",
    "Application Index",
    "Workflow Index",
    "Paper Index",
    "Glossary Index",
    "Pattern Index",
    "Review Queue",
)


@dataclass(frozen=True)
class CatalogueConfig:
    """Everything the read and index paths can be tuned by."""

    # --- index
    chunk_target_chars: int = 1200
    chunk_min_chars: int = 80

    # --- retrieval
    default_limit: int = 10
    max_limit: int = 50
    rrf_k: int = 60                      # Reciprocal Rank Fusion constant
    lexical_weight: float = 1.0
    vector_weight: float = 1.0

    # --- ranking knobs, exposed so `librarian relevance` can compare
    # configurations as data instead of by editing a constant and re-running.
    # The idea is lifted from `elastic - elastic-labs`, whose
    # `relevance-workbench` is an application whose whole purpose is putting
    # two ranking configurations side by side on the same queries, and from
    # `JayLZhou - GraphRAG`, which makes ten published methods comparable by
    # expressing each as a configuration over shared stages.
    selectivity_ceiling: float = 0.50    # df above which a term discriminates nothing
    coverage_min_terms: int = 2          # terms a note must match to be "covered"
    coverage_order: str = "bm25"         # terms | bm25 | idf
    selectivity_scope: str = "answerable"  # answerable | all
    query_segmentation: bool = False     # drop terms a query marks as out of scope
    # On by default from 2026-09-05. Measured as *non-displacing*: both
    # instruments are byte-identical with it on and off, because components are
    # appended after the notes and capped. That is a proof of no cost, not a
    # proof of benefit - and neither instrument can supply the latter, because
    # both score note names only. Component-granularity scenarios are the
    # missing instrument, and they wait on externally-authored ones (Phase B1).
    include_components: bool = True      # also return addresses inside a source
    name_weight_multiplier: float = 1.2  # name ranking's edge in the fusion
    coverage_weight_multiplier: float = 1.0

    # --- embeddings (step 4). Absent LM Studio, retrieval degrades to
    # filters + FTS5 and says so in Response.notes; it never raises.
    embeddings_enabled: bool = True
    # The id LM Studio actually serves carries the quantisation suffix;
    # `resolve_model` still accepts the bare family name.
    embedding_model: str = "text-embedding-nomic-embed-text-v1.5@q4_k_m"
    embedding_base_url: str = "http://127.0.0.1:1234/v1"
    embedding_timeout_seconds: int = 120
    # Small batches on purpose: a long queue is what gets the model
    # evicted mid-request on a host that keeps one task model resident.
    embedding_batch_size: int = 8

    # --- graph (step 9)
    graph_enabled: bool = True
    # Empty by default: `graph.graphify_available` already probes PATH, so a
    # machine-specific path belongs in `library_config.json` on the machine
    # that has it, never compiled into a package that ships elsewhere.
    graphify_bin: str = ""
    graphify_timeout_seconds: int = 30
    centrality_exclude: tuple[str, ...] = DEFAULT_CENTRALITY_EXCLUDE
    # Swapping gap_fit's basis is a ranking change and must be measured
    # against the eval set before it is trusted (spec 4B.4).
    measured_gap_fit: bool = False

    # --- toolchain (step 6). The reference note says F:; the host currently
    # has it on D:. Candidates are tried in order and the first that has
    # local_tool_assist_mcp wins, so neither location is hard-coded.
    toolchain_root: str = ""
    # Probed in order, first hit wins, absence degrades with a named
    # reason. Machine-specific entries live in `library_config.json`.
    toolchain_candidates: tuple[str, ...] = ()
    toolchain_output_root: str = ""

    # --- workbench (step 10)
    workbench_image: str = "python:3.11-slim"
    workbench_memory: str = "4g"
    workbench_cpus: str = "2"
    workbench_clone_depth: int = 1
    container_runtime: str = "docker"

    extras: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path | None = None) -> "CatalogueConfig":
        raw: dict[str, Any] = {}
        target = path or CONFIG_PATH
        if target.exists():
            try:
                doc = json.loads(target.read_text(encoding="utf-8"))
                raw = doc.get("catalogue", {}) or {}
                sources = doc.get("read_only_sources", {}) or {}
                if not raw.get("toolchain_root") and sources.get("toolset"):
                    raw["toolchain_root"] = sources["toolset"]
            except Exception:
                raw = {}
        known = set(cls.__dataclass_fields__) - {"extras"}
        kwargs: dict[str, Any] = {}
        for key, value in raw.items():
            if key in known:
                if key in {"centrality_exclude", "toolchain_candidates"} and isinstance(value, list):
                    value = tuple(value)
                kwargs[key] = value
        extras = {k: v for k, v in raw.items() if k not in known}
        return cls(extras=extras, **kwargs)

    def limit(self, requested: int | None) -> int:
        if not requested:
            return self.default_limit
        return max(1, min(int(requested), self.max_limit))


def embedding_base_url() -> str | None:
    """Environment overrides config so a different LM Studio host needs no edit."""
    return os.environ.get("LMSTUDIO_BASE_URL")


def vault_root() -> Path:
    """The vault this run operates on.

    `VAULT_ROOT` is the *default* - the directory this package happens to sit
    inside - and never the truth. Everything that resolves a path must go
    through a function like this one rather than through a module constant,
    because a constant is computed at import and `CATALOGUE_VAULT` is usually
    set afterwards.

    That distinction was the whole of Stage 3. Before 2026-09-05, fifteen call
    sites asked and seventeen did not, including the one that decided where the
    databases lived - so pointing the tool at another vault read the index from
    one place and wrote it to another. Half-working was worse than not working.
    """
    return Path(os.environ.get("CATALOGUE_VAULT", VAULT_ROOT))


def data_root() -> Path:
    """`.Data` for the current vault. Derived on call, never at import."""
    return Path(os.environ.get("CATALOGUE_DATA", vault_root() / ".Data"))


def database_dir() -> Path:
    return data_root() / "Databases"


def survey_dir() -> Path:
    return data_root() / "surveys"


def index_db_path() -> Path:
    return Path(os.environ.get("CATALOGUE_INDEX_DB",
                               database_dir() / "catalogue_index.sqlite"))


def component_db_path() -> Path:
    return database_dir() / "source_components.sqlite"


def brief_dir() -> Path:
    """Research briefs: what a project asked the library to find.

    Working state, not truth - a brief records a request and its dispositions,
    it never asserts anything about a source. Durable rather than disposable,
    because the reason a candidate was rejected is the negative result nobody
    otherwise writes down.
    """
    return data_root() / "briefs"


def staging_dir() -> Path:
    """Proposed resource notes, before a person or a project agent promotes one.

    Nothing here is in the vault and nothing here is indexed. This is the airlock
    that makes it safe to let an unattended agent contribute: it may fill in
    structured fields from evidence, and it may not put a word in front of a
    reader.
    """
    return data_root() / "staging" / "proposals"


# ------------------------------------------------------- distribution posture

DEFAULT_POSTURE = "private"
POSTURES = ("private", "distributed")

# What each licence class permits, given what is done with the result.
#
# `distributed` is the classic reading, and it is the one every licence FAQ
# assumes: copyleft obligations bind, source-available terms may forbid the use
# outright, and a repository with no licence grants nothing at all.
#
# `private` is this catalogue's actual posture. It serves one person's R&D on
# tooling that is not published, so no obligation is triggered by any of the
# three uses: reading a repository is unaffected by its licence, running it is
# unaffected, and copying from it distributes nothing. Under that posture the
# licence class stops being a gate and becomes a fact worth recording for the
# day the posture changes.
#
# The facts are recorded identically under both. Only the consequence moves.
PERMITTED_USES = {
    "private": {
        "Permissive": ("donor", "reference", "tool"),
        "Weak_Copyleft": ("donor", "reference", "tool"),
        "Copyleft": ("donor", "reference", "tool"),
        "Source_Available": ("donor", "reference", "tool"),
        "Unknown": ("donor", "reference", "tool"),
    },
    "distributed": {
        "Permissive": ("donor", "reference", "tool"),
        "Weak_Copyleft": ("donor", "reference", "tool"),
        "Copyleft": ("reference", "tool"),
        "Source_Available": ("reference",),
        "Unknown": ("reference",),
    },
}


@lru_cache(maxsize=4)
def distribution_posture(path: Path | None = None) -> str:
    """How this catalogue's output will be used. See `library_config.json`.

    An unreadable or absent config degrades to `private`, matching the rest of
    the system's posture on missing inputs: report the default, never raise.
    """
    target = path or CONFIG_PATH
    if not target.exists():
        return DEFAULT_POSTURE
    try:
        raw = json.loads(target.read_text(encoding="utf-8")).get("usage") or {}
    except Exception:
        return DEFAULT_POSTURE
    value = str(raw.get("distribution_posture") or DEFAULT_POSTURE)
    return value if value in POSTURES else DEFAULT_POSTURE


def permitted_uses(license_class: str | None,
                   posture: str | None = None) -> tuple[str, ...]:
    """Answer the question the catalogue is actually asked of a licence:
    can this be used as **donor** code, as a **reference**, or as a **tool**?

    That is a more useful answer than a class name, because the class alone
    does not say what it stops you doing, and what it stops you doing depends
    entirely on the posture rather than on the licence.
    """
    table = PERMITTED_USES[posture or distribution_posture()]
    return table.get(license_class or "Unknown", table["Unknown"])


DEFAULT_ROLE = "reference"
ROLES = ("reference", "integration")


def catalogue_role(path: Path | None = None) -> str:
    """What the catalogue is *for*, which decides what a property costs.

    `reference` — it locates and describes prior work so a person can find it,
    read it and decide. A source's licence, age and popularity are facts to
    report, not grounds for hiding it.

    `integration` — it selects components to depend on. Then staleness and
    obscurity really do predict risk and should suppress a candidate.

    See `LOCATE_DO_NOT_ADJUDICATE` in the Design Specification. Degrades to
    `reference`, which is the posture that withholds least.
    """
    target = path or CONFIG_PATH
    if not target.exists():
        return DEFAULT_ROLE
    try:
        raw = json.loads(target.read_text(encoding="utf-8")).get("usage") or {}
    except Exception:
        return DEFAULT_ROLE
    value = str(raw.get("catalogue_role") or DEFAULT_ROLE)
    return value if value in ROLES else DEFAULT_ROLE
