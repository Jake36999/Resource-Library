from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import textwrap
import uuid as uuidlib
from collections import Counter, defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from adapters.lmstudio import LMStudioClient, LMStudioSettings


VAULT_ROOT = Path(__file__).resolve().parent.parent
UTILITY_ROOT = VAULT_ROOT / ".utility"
CONFIG_PATH = UTILITY_ROOT / "library_config.json"


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


CONFIG = load_config()
SEED_FILE = VAULT_ROOT / CONFIG["seed_file"]
DB_PATH = UTILITY_ROOT / Path(CONFIG["database_file"]).name

FOLDERS = CONFIG["folders"]
INDEX_DIR = VAULT_ROOT / FOLDERS["indexes"]
RESOURCE_DIR = VAULT_ROOT / FOLDERS["resources"]
GLOSSARY_DIR = VAULT_ROOT / FOLDERS["glossary"]
PATTERN_DIR = VAULT_ROOT / FOLDERS["patterns"]
REVIEW_DIR = VAULT_ROOT / FOLDERS["reviews"]
CANVAS_DIR = VAULT_ROOT / FOLDERS["canvases"]
TOPIC_CANVAS_DIR = CANVAS_DIR / "Topics"
LOG_DIR = UTILITY_ROOT / "logs"
PROMPT_DIR = UTILITY_ROOT / "prompts"
STAGING_DIR = UTILITY_ROOT / "staging"
REVIEW_QUEUE_DIR = UTILITY_ROOT / "review_queue"
GITHUB_CACHE_PATH = STAGING_DIR / "github_repo_metadata.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def entity_uuid(kind: str, key: str) -> str:
    return str(uuidlib.uuid5(uuidlib.NAMESPACE_URL, f"solutions-library::{kind}::{key}"))


def normalize_repo_url(raw: str) -> str | None:
    url = raw.strip()
    url = url.rstrip(").,;]")
    url = url.removesuffix(".git")
    if "github.com" not in url:
        return None
    url = re.sub(r"^https?://github\.com/", "https://github.com/", url)
    url = re.sub(r"^git@github\.com:", "https://github.com/", url)
    url = url.replace("github.com/", "https://github.com/", 1) if url.startswith("github.com/") else url
    match = re.match(r"https://github\.com/([^/\s]+)/([^/\s#?]+)", url)
    if not match:
        return None
    owner, repo = match.group(1), match.group(2)
    return f"https://github.com/{owner}/{repo}"


def repo_key_from_url(url: str) -> str:
    match = re.match(r"https://github\.com/([^/\s]+)/([^/\s#?]+)", url)
    if not match:
        raise ValueError(f"Unsupported repository URL: {url}")
    return f"{match.group(1)}/{match.group(2)}"


def split_repo_key(repo_key: str) -> tuple[str, str]:
    owner, repo = repo_key.split("/", 1)
    return owner, repo


def note_title_for_repo(owner: str, repo: str) -> str:
    return repo if owner.lower() == repo.lower() else f"{owner} - {repo}"


def sanitize_filename(name: str) -> str:
    safe = re.sub(r'[<>:"/\\|?*]', "-", name)
    safe = re.sub(r"\s+", " ", safe).strip()
    return safe


def note_path(*parts: str) -> Path:
    return Path(*parts)


def jsonish(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def bullets(items: Iterable[str]) -> str:
    lines = [f"- {item}" for item in items if item]
    return "\n".join(lines) if lines else "- None yet."


def table_rows(rows: Iterable[str]) -> str:
    content = "\n".join(rows)
    return content if content else "| (none yet) | - | - |"


def yaml_frontmatter(data: dict[str, Any]) -> str:
    lines = ["---"]
    for key, value in data.items():
        if value is None:
            continue
        lines.append(f"{key}: {jsonish(value)}")
    lines.append("---")
    return "\n".join(lines)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        current = path.read_text(encoding="utf-8")
        if current == text:
            return
    path.write_text(text, encoding="utf-8", newline="\n")


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def contains_any(value: str, keywords: Iterable[str]) -> bool:
    lower = value.lower()
    return any(keyword.lower() in lower for keyword in keywords)


def read_seed_urls(seed_path: Path) -> list[str]:
    raw_text = seed_path.read_text(encoding="utf-8")
    urls = []
    seen = set()
    for match in re.finditer(r"https://github\.com/[^\s)\]]+", raw_text):
        url = normalize_repo_url(match.group(0))
        if url and url not in seen:
            seen.add(url)
            urls.append(url)
    return urls


LOCAL_REPO_CONTEXT_MAX_CHARS = 16000
LOCAL_REPO_DOCUMENT_MAX_CHARS = 3000
LOCAL_REPO_DOCUMENT_MAX_COUNT = 6
LOCAL_REPO_FILE_NAMES = {
    "readme.md",
    "readme",
    "license",
    "license.md",
    "copying",
    "copying.md",
    "pyproject.toml",
    "package.json",
    "cargo.toml",
    "go.mod",
    "requirements.txt",
    "setup.py",
    "setup.cfg",
    "makefile",
}
LOCAL_REPO_EXTENSIONS = {
    ".md",
    ".rst",
    ".txt",
    ".toml",
    ".json",
    ".yaml",
    ".yml",
    ".ini",
    ".cfg",
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".rs",
    ".go",
    ".java",
    ".c",
    ".cpp",
    ".h",
}


def seed_excerpt_for_url(seed_path: Path, canonical_url: str) -> str:
    raw_text = seed_path.read_text(encoding="utf-8")
    for line in raw_text.splitlines():
        if canonical_url in line:
            return line.strip()
    return canonical_url


def repository_root_candidates(repo_key: str) -> list[Path]:
    owner, repo = split_repo_key(repo_key)
    display_name = note_title_for_repo(owner, repo)
    candidates = [
        STAGING_DIR / owner / repo,
        STAGING_DIR / owner / repo.lower(),
        STAGING_DIR / f"{owner}__{repo}",
        STAGING_DIR / f"{owner}-{repo}",
        STAGING_DIR / repo,
        STAGING_DIR / display_name,
        STAGING_DIR / repo_key.replace("/", "__"),
    ]
    seen: set[Path] = set()
    ordered: list[Path] = []
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate.exists() and candidate.is_dir():
            ordered.append(candidate)
    return ordered


def read_text_limited(path: Path, limit: int) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if len(text) > limit:
        text = text[:limit].rstrip() + "\n[truncated]"
    return text


def file_priority(path: Path) -> tuple[int, int, str]:
    name = path.name.lower()
    suffix = path.suffix.lower()
    parts = [part.lower() for part in path.parts]
    if name.startswith("readme"):
        priority = 0
    elif name.startswith("license") or name in {"copying", "unlicense"}:
        priority = 1
    elif name in {"pyproject.toml", "package.json", "cargo.toml", "go.mod", "requirements.txt", "setup.py", "setup.cfg", "makefile"}:
        priority = 2
    elif "docs" in parts or "doc" in parts:
        priority = 3
    elif suffix in LOCAL_REPO_EXTENSIONS:
        priority = 4
    else:
        priority = 5
    return priority, len(path.parts), path.as_posix().lower()


def collect_repository_documents(repo_root: Path) -> list[RepositoryDocument]:
    if not repo_root.exists() or not repo_root.is_dir():
        return []
    files: list[Path] = []
    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        if path.name.startswith("."):
            continue
        name = path.name.lower()
        if name in LOCAL_REPO_FILE_NAMES or path.suffix.lower() in LOCAL_REPO_EXTENSIONS or name.startswith("readme") or name.startswith("license"):
            files.append(path)
    files.sort(key=file_priority)
    documents: list[RepositoryDocument] = []
    remaining = LOCAL_REPO_CONTEXT_MAX_CHARS
    for path in files[:LOCAL_REPO_DOCUMENT_MAX_COUNT * 2]:
        if remaining <= 0:
            break
        text = read_text_limited(path, min(LOCAL_REPO_DOCUMENT_MAX_CHARS, remaining))
        if not text:
            continue
        documents.append(RepositoryDocument(path=path.relative_to(repo_root).as_posix(), text=text))
        remaining -= len(text)
        if len(documents) >= LOCAL_REPO_DOCUMENT_MAX_COUNT:
            break
    return documents


def build_repository_context(
    repo_key: str,
    canonical_url: str,
    source_file: str,
    topic: TopicSpec,
    profile: ResourceProfile,
    github_metadata: GitHubRepositoryMetadata | None = None,
) -> RepositoryContext:
    repo_roots = repository_root_candidates(repo_key)
    repo_root = repo_roots[0] if repo_roots else STAGING_DIR / repo_key.replace("/", "__")
    documents = collect_repository_documents(repo_root)
    inventory = [document.path for document in documents]
    seed_excerpt = seed_excerpt_for_url(VAULT_ROOT / source_file, canonical_url)
    heuristic_summary = profile.summary or generic_profile(repo_key, topic).summary
    return RepositoryContext(
        repo_key=repo_key,
        canonical_url=canonical_url,
        source_file=source_file,
        topic_key=topic.key,
        heuristic_topic_title=topic.title,
        heuristic_summary=heuristic_summary,
        inventory=inventory,
        documents=documents,
        seed_excerpt=seed_excerpt,
        github_metadata=github_metadata,
    )


def detect_license_name(text: str) -> str:
    lower = text.lower()
    if "apache license" in lower or "apache-2.0" in lower:
        return "Apache-2.0"
    if "mit license" in lower or re.search(r"\bmit\b", lower):
        return "MIT"
    if "gnu general public license" in lower or "gpl" in lower:
        if "lgpl" in lower:
            return "LGPL"
        if "agpl" in lower:
            return "AGPL"
        return "GPL"
    if "mozilla public license" in lower or "mpl-2.0" in lower:
        return "MPL-2.0"
    if "bsd" in lower and "redistribution and use" in lower:
        return "BSD"
    if "isc license" in lower:
        return "ISC"
    if "unlicense" in lower:
        return "Unlicense"
    if "all rights reserved" in lower or "proprietary" in lower:
        return "Proprietary"
    return "unknown"


def license_override_for(repo_key: str) -> str | None:
    """Manually verified SPDX identifier for a repository, from
    library_config.json -> license_overrides. Keyed on repo_key, matched
    case-insensitively. Returns None when no override is recorded."""
    if not repo_key:
        return None
    overrides = CONFIG.get("license_overrides", {}) if isinstance(CONFIG, dict) else {}
    if not isinstance(overrides, dict):
        return None
    wanted = repo_key.strip().lower()
    for key, value in overrides.items():
        if str(key).strip().lower() == wanted and value:
            entry = value
            if isinstance(entry, dict):
                entry = entry.get("spdx")
            return str(entry) if entry else None
    return None


def license_class_from_name(license_name: str) -> str:
    lower = (license_name or "").strip().lower()
    # "NOASSERTION"/"Other" mean GitHub found a licence file it could not
    # identify, which is not the same as no licence at all - both land in
    # Unknown, but the raw value is preserved in the note for manual reading.
    if not lower or lower in {"unknown", "noassertion", "other"}:
        return "Unknown"
    if lower in {
        "mit", "mit-0", "apache-2.0", "bsd", "bsd-2-clause", "bsd-3-clause",
        "isc", "unlicense", "0bsd", "zlib", "cc0-1.0", "postgresql", "python-2.0",
    }:
        return "Permissive"
    # Weak copyleft is kept distinct from strong copyleft because it governs
    # whether a resource can be linked into a closed project without
    # relicensing - the single most common integration question.
    if lower in {"lgpl", "lgpl-2.1", "lgpl-3.0", "mpl-2.0", "epl-2.0", "cddl-1.0"}:
        return "Weak_Copyleft"
    # Source-available licences permit reading but restrict use, and are not
    # OSI open source. GitHub reports them as NOASSERTION, so without this they
    # arrive looking like "unknown" when they are a known, restrictive answer -
    # the opposite of what an integration decision needs to hear.
    if lower in {
        "busl-1.1", "bsl-1.1", "fsl-1.1", "fsl-1.1-apache-2.0", "fsl-1.1-mit",
        "elastic-2.0", "sspl-1.0", "hippocratic-2.1", "hippocratic-3.0",
        "commons-clause", "polyform-noncommercial-1.0.0",
    }:
        return "Source_Available"
    if lower in {
        "gpl", "gpl-2.0", "gpl-3.0", "gpl-3.0-or-later",
        "agpl", "agpl-3.0", "cc-by-sa-4.0", "osl-3.0",
    }:
        return "Copyleft"
    if lower == "proprietary":
        return "Proprietary"
    return "Unknown"


def detect_maturity_stage(text: str, topic: TopicSpec) -> str:
    lower = text.lower()
    if any(token in lower for token in ["archived", "deprecated", "end of life", "no longer maintained", "abandoned"]):
        return "Abandoned"
    if any(token in lower for token in ["experimental", "prototype", "proof of concept", "wip", "alpha", "beta", "incubating"]):
        return "Incubating"
    if any(token in lower for token in ["production ready", "production-ready", "stable", "battle tested", "enterprise", "used in production"]):
        return "Production_Ready"
    if topic.key in {"curated_lists", "architecture_playbooks"}:
        return "Reference"
    return "Active"


def detect_security_compliance(text: str) -> str:
    lower = text.lower()
    if "hipaa" in lower:
        return "HIPAA"
    if "gdpr" in lower:
        return "GDPR_Compliant"
    if "soc 2" in lower or "soc2" in lower:
        return "SOC2"
    if "fips" in lower:
        return "FIPS"
    if "end-to-end encrypted" in lower or "e2e encrypted" in lower:
        return "E2E_Encrypted"
    return "Uncertified"


def detect_deployment_target(text: str, topic: TopicSpec, repo_key: str) -> str:
    lower = text.lower()
    if topic.key in {"frontend_design_systems", "cad_saas_design"} or any(token in lower for token in ["browser", "frontend", "react", "bootstrap", "css"]):
        return "Browser"
    if any(token in lower for token in ["local only", "offline", "air-gapped", "air gapped", "local-first", "local first", "desktop"]):
        return "Local_Only"
    if topic.key in {"agentic_ai_models", "scientific_simulation_math"} or any(token in lower for token in ["model", "llm", "python sdk", "sdk", "voice", "tts", "stt"]):
        return "Local_Only"
    if topic.key in {"data_api_big_data", "geospatial_earth_data", "infrastructure_observability", "security_siem", "government_civic_tech"}:
        return "Server"
    return "Server"


def detect_interface_protocol(text: str, topic: TopicSpec) -> str:
    lower = text.lower()
    if any(token in lower for token in ["cli", "command line", "shell"]):
        return "CLI"
    if any(token in lower for token in ["rest", "api", "graphql", "endpoint", "openapi"]):
        return "REST"
    if any(token in lower for token in ["web ui", "browser", "ui", "site", "website", "documentation"]):
        return "Web_UI"
    if any(token in lower for token in ["python sdk", "python package", "pip install", "module"]):
        return "Python_SDK"
    if topic.key == "curated_lists":
        return "Markdown"
    return "Unknown"


def detect_data_locality(text: str, topic: TopicSpec) -> str:
    lower = text.lower()
    if any(token in lower for token in ["air-gapped", "air gapped", "offline", "local-first", "local first"]):
        return "Air_Gapped_Capable"
    if any(token in lower for token in ["stateless", "browser", "frontend"]):
        return "Stateless"
    if topic.key in {"frontend_design_systems", "cad_saas_design"}:
        return "Stateless"
    if any(token in lower for token in ["distributed", "cloud", "cluster", "replicated", "server"]):
        return "Distributed"
    return "Local_First" if topic.key in {"agentic_ai_models", "scientific_simulation_math"} else "Distributed"


def detect_hardware_footprint(text: str, topic: TopicSpec) -> str:
    lower = text.lower()
    if any(token in lower for token in ["vram", "gpu", "llm", "model", "tts", "stt", "voice", "video"]):
        return "Low_VRAM" if any(token in lower for token in ["8gb", "low vram", "lightweight"]) else "GPU_Optional"
    if any(token in lower for token in ["browser", "frontend", "css", "html"]):
        return "Browser_Only"
    if topic.key in {"data_api_big_data", "geospatial_earth_data"} or any(token in lower for token in ["memory", "large dataset", "high memory"]):
        return "High_Memory"
    return "CPU_Only"


def infer_ecosystem_from_text(text: str, topic: TopicSpec) -> str:
    lower = text.lower()
    if topic.key == "curated_lists":
        return "Markdown"
    if any(token in lower for token in ["react"]):
        return "React"
    if any(token in lower for token in ["bootstrap", "normalize", "animate", "modernizr", "css"]):
        return "Web_CSS"
    if any(token in lower for token in ["python", "pyproject", "pip"]):
        return "Python"
    if any(token in lower for token in ["terraform", "puppet", "chef", "openstack"]):
        return "Infrastructure_Automation"
    if any(token in lower for token in ["prometheus", "netdata", "statsd", "sentry"]):
        return "Observability"
    if any(token in lower for token in ["api", "endpoint", "dataset", "portal"]):
        return "Data_Platform"
    if any(token in lower for token in ["stac", "geojson", "satellite", "map"]):
        return "Geo_Data"
    if topic.key in {"agentic_ai_models", "architecture_playbooks"}:
        return "Model_Serving" if "llm" in lower or "model" in lower else "Markdown"
    return "Mixed"


def deterministic_metadata_signals(context: RepositoryContext, topic: TopicSpec) -> dict[str, str]:
    text = context.combined_text
    license_name = detect_license_name(text)
    return {
        "ecosystem": infer_ecosystem_from_text(text, topic),
        "domain_primary": DOMAIN_PRIMARY_BY_TOPIC_KEY.get(topic.key, "Mixed"),
        "maturity_stage": detect_maturity_stage(text, topic),
        "license": license_name,
        "license_class": license_class_from_name(license_name),
        "deployment_target": detect_deployment_target(text, topic, context.repo_key),
        "interface_protocol": detect_interface_protocol(text, topic),
        "data_locality": detect_data_locality(text, topic),
        "hardware_footprint": detect_hardware_footprint(text, topic),
        "security_compliance": detect_security_compliance(text),
    }


@dataclass(frozen=True)
class TopicSpec:
    key: str
    title: str
    description: str
    inclusion_criteria: str
    canonical_vocabulary: list[str]
    keywords: list[str]
    patterns: list[str]
    glossary_terms: list[str]
    mechanics: list[str]
    use_cases: list[str]
    overlaps: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class PatternSpec:
    key: str
    title: str
    definition: str
    aliases: list[str]
    examples: list[str]
    glossary_terms: list[str]
    topic_keys: list[str]


@dataclass(frozen=True)
class GlossarySpec:
    key: str
    word: str
    definition: str
    aliases: list[str]
    related_terms: list[str]
    topic_keys: list[str]
    sense_label: str = "canonical"


@dataclass(frozen=True)
class ResourceProfile:
    summary: str
    mechanics: list[str]
    use_cases: list[str]
    patterns: list[str]
    glossary_terms: list[str]
    secondary_topics: list[str]
    sensitivity: str = "normal"
    status: str = "published"
    review_reason: str | None = None
    ecosystem: str | None = None
    domain_primary: str | None = None
    maturity_stage: str | None = None
    license_class: str | None = None
    deployment_target: str | None = None
    interface_protocol: str | None = None
    data_locality: str | None = None
    hardware_footprint: str | None = None
    security_compliance: str | None = None
    maturity: str = "seed"


@dataclass(frozen=True)
class RepositoryDocument:
    path: str
    text: str


@dataclass(frozen=True)
class GitHubRepositoryMetadata:
    full_name: str
    description: str
    language: str
    license_name: str
    license_spdx: str
    default_branch: str
    topics: list[str]
    homepage: str
    archived: bool
    disabled: bool
    stars: int
    watchers: int
    pushed_at: str
    updated_at: str


@dataclass(frozen=True)
class RepositoryContext:
    repo_key: str
    canonical_url: str
    source_file: str
    topic_key: str
    heuristic_topic_title: str
    heuristic_summary: str
    inventory: list[str]
    documents: list[RepositoryDocument]
    seed_excerpt: str
    github_metadata: GitHubRepositoryMetadata | None = None

    @property
    def combined_text(self) -> str:
        pieces = [
            f"Repo Key: {self.repo_key}",
            f"Canonical URL: {self.canonical_url}",
            f"Source File: {self.source_file}",
            f"Heuristic Topic: {self.heuristic_topic_title}",
            f"Heuristic Summary: {self.heuristic_summary}",
            f"Seed Excerpt: {self.seed_excerpt}",
            "Inventory:",
            *[f"- {item}" for item in self.inventory],
        ]
        if self.github_metadata:
            metadata = self.github_metadata
            pieces.extend(
                [
                    "GitHub Snapshot:",
                    f"- Full Name: {metadata.full_name}",
                    f"- Description: {metadata.description}",
                    f"- Language: {metadata.language}",
                    f"- License: {metadata.license_name} ({metadata.license_spdx})",
                    f"- Default Branch: {metadata.default_branch}",
                    f"- Stars: {metadata.stars}",
                    f"- Homepage: {metadata.homepage}",
                    f"- Topics: {', '.join(metadata.topics)}",
                    f"- Pushed At: {metadata.pushed_at}",
                    f"- Updated At: {metadata.updated_at}",
                ]
            )
        for document in self.documents:
            pieces.append(f"## {document.path}\n{document.text}")
        return "\n".join(pieces)


class EvidenceSnippetCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_kind: str = "repository"
    source_ref: str
    snippet: str
    confidence: float = 0.5


class ScoutResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    canonical_url: str
    repo_key: str
    archetype: str
    primary_topic_key: str
    secondary_topic_keys: list[str] = Field(default_factory=list)
    sensitivity: str = "normal"
    maturity: str = "seed"
    token_budget_estimate: int = 0
    confidence: float = 0.0
    reason: str = ""
    candidate_glossary_terms: list[str] = Field(default_factory=list)
    candidate_patterns: list[str] = Field(default_factory=list)
    candidate_taxonomy: dict[str, str] = Field(default_factory=dict)


class ChartResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    canonical_url: str
    repo_key: str
    summary: str
    mechanics: list[str] = Field(default_factory=list)
    use_cases: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    alternatives: list[str] = Field(default_factory=list)
    complements: list[str] = Field(default_factory=list)
    evidence_snippets: list[EvidenceSnippetCandidate] = Field(default_factory=list)
    glossary_terms: list[str] = Field(default_factory=list)
    patterns: list[str] = Field(default_factory=list)
    primary_topic_key: str | None = None
    secondary_topic_keys: list[str] = Field(default_factory=list)
    maturity: str | None = None
    license: str | None = None
    candidate_taxonomy: dict[str, str] = Field(default_factory=dict)
    confidence: float = 0.0


class MetadataResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    canonical_url: str
    repo_key: str
    ecosystem: str = "Mixed"
    domain_primary: str = "Mixed"
    maturity_stage: str = "Active"
    license_class: str = "Unknown"
    license: str = "unknown"
    deployment_target: str = "Server"
    interface_protocol: str = "Unknown"
    data_locality: str = "Distributed"
    hardware_footprint: str = "CPU_Only"
    security_compliance: str = "Uncertified"
    confidence: float = 0.0
    evidence_snippets: list[EvidenceSnippetCandidate] = Field(default_factory=list)


class EntityTermResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    canonical_form: str
    aliases: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    observed_context: str
    sense_label: str = "canonical"
    role: str = "unknown"
    salience_score: float = 0.0


class EntityExtractionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    canonical_url: str
    repo_key: str
    terms: list[EntityTermResult] = Field(default_factory=list)


@dataclass(frozen=True)
class ResourceEnrichment:
    scout: ScoutResult | None = None
    chart: ChartResult | None = None
    metadata: MetadataResult | None = None
    entities: EntityExtractionResult | None = None
    evidence_snippets: list[EvidenceSnippetCandidate] = field(default_factory=list)


@dataclass
class LMStudioRuntime:
    settings: LMStudioSettings
    client: LMStudioClient | None
    available: bool = False
    consecutive_failures: int = 0
    failure_limit: int = 3


@dataclass
class GitHubRuntime:
    enabled: bool = True
    available: bool = True
    api_base: str = "https://api.github.com"
    api_token: str | None = None
    timeout_seconds: int = 12
    cache: dict[str, GitHubRepositoryMetadata] = field(default_factory=dict)
    cache_dirty: bool = False


def github_metadata_from_payload(payload: dict[str, Any]) -> GitHubRepositoryMetadata:
    license_data = payload.get("license") or {}
    topics = payload.get("topics") or []
    if not isinstance(topics, list):
        topics = []
    return GitHubRepositoryMetadata(
        full_name=str(payload.get("full_name") or ""),
        description=str(payload.get("description") or ""),
        language=str(payload.get("language") or ""),
        license_name=str(license_data.get("name") or "Unknown"),
        license_spdx=str(license_data.get("spdx_id") or "UNKNOWN"),
        default_branch=str(payload.get("default_branch") or "main"),
        topics=[str(item) for item in topics if str(item).strip()],
        homepage=str(payload.get("homepage") or ""),
        archived=bool(payload.get("archived") or False),
        disabled=bool(payload.get("disabled") or False),
        stars=int(payload.get("stargazers_count") or 0),
        watchers=int(payload.get("watchers_count") or 0),
        pushed_at=str(payload.get("pushed_at") or ""),
        updated_at=str(payload.get("updated_at") or ""),
    )


GITHUB_CACHE_NEEDS_REWRITE: set[bool] = set()


def load_github_metadata_cache() -> dict[str, GitHubRepositoryMetadata]:
    if not GITHUB_CACHE_PATH.exists():
        return {}
    try:
        raw = json.loads(GITHUB_CACHE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}
    cache: dict[str, GitHubRepositoryMetadata] = {}
    raw_shape_seen = False
    if isinstance(raw, dict):
        for repo_key, payload in raw.items():
            if not isinstance(payload, dict):
                continue
            try:
                topics = payload.get("topics") or []
                if not isinstance(topics, list):
                    topics = []
                # Accept both the canonical dataclass shape and a raw GitHub API
                # payload. Only four field names differ between the two shapes
                # (stars/stargazers_count, watchers/watchers_count and the
                # nested license object), so a shape mismatch silently zeroed
                # exactly those fields while every sibling field survived.
                if "stars" not in payload or "license_name" not in payload:
                    raw_shape_seen = True
                nested_license = payload.get("license")
                if not isinstance(nested_license, dict):
                    nested_license = {}
                license_name = payload.get("license_name")
                if not license_name:
                    license_name = nested_license.get("name")
                license_spdx = payload.get("license_spdx")
                if not license_spdx:
                    license_spdx = nested_license.get("spdx_id")
                stars = payload.get("stars")
                if stars is None:
                    stars = payload.get("stargazers_count")
                watchers = payload.get("watchers")
                if watchers is None:
                    watchers = payload.get("watchers_count")
                cache[repo_key] = GitHubRepositoryMetadata(
                    full_name=str(payload.get("full_name") or repo_key),
                    description=str(payload.get("description") or ""),
                    language=str(payload.get("language") or ""),
                    license_name=str(license_name or "Unknown"),
                    license_spdx=str(license_spdx or "UNKNOWN"),
                    default_branch=str(payload.get("default_branch") or "main"),
                    topics=[str(item) for item in topics if str(item).strip()],
                    homepage=str(payload.get("homepage") or ""),
                    archived=bool(payload.get("archived") or False),
                    disabled=bool(payload.get("disabled") or False),
                    stars=int(stars or 0),
                    watchers=int(watchers or 0),
                    pushed_at=str(payload.get("pushed_at") or ""),
                    updated_at=str(payload.get("updated_at") or ""),
                )
            except Exception:
                continue
    if raw_shape_seen:
        GITHUB_CACHE_NEEDS_REWRITE.add(True)
    return cache


def save_github_metadata_cache(runtime: GitHubRuntime) -> None:
    if not runtime.cache_dirty:
        return
    # cache_dirty is also set by load_github_metadata_cache when it had to
    # normalise a non-canonical stored shape, so the file is rewritten in the
    # canonical shape rather than left to mis-load on the next run.
    GITHUB_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {repo_key: asdict(metadata) for repo_key, metadata in sorted(runtime.cache.items())}
    write_text(GITHUB_CACHE_PATH, json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))


def load_github_runtime() -> GitHubRuntime:
    config = CONFIG.get("github", {}) if isinstance(CONFIG, dict) else {}
    env_enabled = os.environ.get("GITHUB_METADATA_ENABLED")
    enabled = config.get("enabled", True)
    if env_enabled is not None:
        enabled = env_enabled.strip().lower() not in {"0", "false", "no", "off"}
    api_token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_API_TOKEN") or config.get("api_token")
    api_base = os.environ.get("GITHUB_API_BASE", config.get("api_base", "https://api.github.com"))
    timeout_seconds = int(config.get("timeout_seconds", 12))
    return GitHubRuntime(
        enabled=bool(enabled),
        available=bool(enabled),
        api_base=str(api_base),
        api_token=api_token,
        timeout_seconds=timeout_seconds,
        cache=load_github_metadata_cache(),
        cache_dirty=bool(GITHUB_CACHE_NEEDS_REWRITE),
    )


def github_request_json(runtime: GitHubRuntime, path: str) -> dict[str, Any]:
    url = f"{runtime.api_base.rstrip('/')}/{path.lstrip('/')}"
    request = Request(url, method="GET")
    request.add_header("User-Agent", "Codex Solutions Library")
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")
    if runtime.api_token:
        request.add_header("Authorization", f"Bearer {runtime.api_token}")
    with urlopen(request, timeout=runtime.timeout_seconds) as response:
        raw = response.read().decode("utf-8")
    return json.loads(raw) if raw else {}


def fetch_github_metadata(runtime: GitHubRuntime, repo_key: str) -> GitHubRepositoryMetadata | None:
    if repo_key in runtime.cache:
        return runtime.cache[repo_key]
    if not runtime.enabled or not runtime.available:
        return None
    try:
        payload = github_request_json(runtime, f"/repos/{repo_key}")
        metadata = github_metadata_from_payload(payload)
        runtime.cache[repo_key] = metadata
        # GitHub silently follows renames and redirects, so the payload can
        # describe a different repository than the one requested. Cache it
        # under the resolved name as well and record the divergence, otherwise
        # the seed spelling is preserved forever as if it were canonical.
        resolved = (metadata.full_name or "").strip()
        if resolved and resolved.lower() != repo_key.lower():
            runtime.cache[resolved] = metadata
            LOG_DIR.mkdir(parents=True, exist_ok=True)
            with (LOG_DIR / "github_redirects.log").open("a", encoding="utf-8") as handle:
                handle.write(
                    json.dumps(
                        {
                            "requested": repo_key,
                            "resolved": resolved,
                            "created_at": now_iso(),
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )
        runtime.cache_dirty = True
        return metadata
    except HTTPError as exc:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        error_path = LOG_DIR / "github_errors.log"
        with error_path.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    {
                        "repo_key": repo_key,
                        "error": f"HTTP {exc.code}: {exc.reason}",
                        "created_at": now_iso(),
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
        if exc.code != 404:
            runtime.available = False
        return None
    except Exception as exc:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        error_path = LOG_DIR / "github_errors.log"
        with error_path.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    {
                        "repo_key": repo_key,
                        "error": str(exc),
                        "created_at": now_iso(),
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
        runtime.available = False
        return None


def read_prompt_template(name: str) -> str:
    return (PROMPT_DIR / name).read_text(encoding="utf-8")


def strip_json_fence(text: str) -> str:
    candidate = text.strip()
    if candidate.startswith("```"):
        candidate = re.sub(r"^```(?:json)?\s*", "", candidate, flags=re.IGNORECASE)
        candidate = re.sub(r"\s*```$", "", candidate)
    start = candidate.find("{")
    if start > 0:
        candidate = candidate[start:]
    return candidate.strip()


def parse_json_object(text: str) -> dict[str, Any]:
    candidate = strip_json_fence(text)
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        # A model that emits a valid object and then keeps talking produces
        # "Extra data: line N column M". raw_decode stops at the end of the
        # first complete object instead of failing the whole response.
        start = candidate.find("{")
        if start == -1:
            raise
        obj, _ = json.JSONDecoder().raw_decode(candidate[start:])
        if not isinstance(obj, dict):
            raise
        return obj


def load_lmstudio_runtime() -> LMStudioRuntime:
    settings = LMStudioSettings.from_config(CONFIG)
    client = LMStudioClient(settings)
    if not settings.enabled:
        available, reason = False, "LM Studio disabled by configuration."
    else:
        available, reason = client.availability()
    # Record why enrichment did or did not run. Previously a silent
    # `lmstudio_available: false` was the only trace, which gave no way to tell
    # a stopped server apart from a model that failed to load.
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with (LOG_DIR / "lmstudio_status.log").open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                {"available": available, "reason": reason, "base_url": settings.base_url, "created_at": now_iso()},
                ensure_ascii=False,
            )
            + "\n"
        )
    if not available:
        print(f"[lmstudio] {reason}")
    return LMStudioRuntime(settings=settings, client=client if available else None, available=available)


def call_lmstudio_stage(
    runtime: LMStudioRuntime,
    stage: str,
    prompt_name: str,
    payload: dict[str, Any],
    *,
    model: str | None = None,
    max_tokens: int | None = None,
) -> dict[str, Any] | None:
    if not runtime.available or runtime.client is None:
        return None
    try:
        content = runtime.client.chat(
            stage,
            [
                {"role": "system", "content": read_prompt_template(prompt_name)},
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False, indent=2)},
            ],
            model=model,
            max_tokens=max_tokens,
            json_mode=True,
        )
        parsed = parse_json_object(content)
        runtime.consecutive_failures = 0
        return parsed
    except Exception as exc:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        error_path = LOG_DIR / "lmstudio_errors.log"
        with error_path.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    {
                        "stage": stage,
                        "error": str(exc),
                        "payload_keys": sorted(payload.keys()),
                        "created_at": now_iso(),
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
        # A response the model mangled says nothing about whether the server is
        # reachable, so it must not disable the model. Only repeated transport
        # failures do, and only after a few in a row - previously a single
        # timeout on the first repository silently disabled enrichment for the
        # entire remaining run.
        transport_failure = not isinstance(exc, (ValueError, json.JSONDecodeError))
        if transport_failure:
            runtime.consecutive_failures += 1
        if runtime.consecutive_failures >= runtime.failure_limit:
            runtime.available = False
            runtime.client = None
        return None


TAXONOMY_LABEL_ALIASES = {
    "agentic ai": "Agentic_AI",
    "agentic_ai": "Agentic_AI",
    "civic tech": "Civic_Tech",
    "civic_tech": "Civic_Tech",
    "cad saas": "CAD_SaaS",
    "cad_saas": "CAD_SaaS",
    "scientific computation": "Scientific_Computation",
    "scientific_computation": "Scientific_Computation",
    "scientific python": "Scientific_Python",
    "scientific_python": "Scientific_Python",
    "model serving": "Model_Serving",
    "model_serving": "Model_Serving",
    "data platform": "Data_Platform",
    "data_platform": "Data_Platform",
    "infrastructure automation": "Infrastructure_Automation",
    "infrastructure_automation": "Infrastructure_Automation",
    "web css": "Web_CSS",
    "web_css": "Web_CSS",
    "web frontend": "Web_Frontend",
    "web_frontend": "Web_Frontend",
    "public sector": "Public_Sector",
    "public_sector": "Public_Sector",
    "production ready": "Production_Ready",
    "production_ready": "Production_Ready",
    "local only": "Local_Only",
    "local_only": "Local_Only",
    "browser only": "Browser_Only",
    "browser_only": "Browser_Only",
    "python sdk": "Python_SDK",
    "python_sdk": "Python_SDK",
    "web ui": "Web_UI",
    "web_ui": "Web_UI",
    "low vram": "Low_VRAM",
    "low_vram": "Low_VRAM",
    "high memory": "High_Memory",
    "high_memory": "High_Memory",
    "air gapped capable": "Air_Gapped_Capable",
    "air_gapped_capable": "Air_Gapped_Capable",
    "local first": "Local_First",
    "local_first": "Local_First",
    "distributed": "Distributed",
    "stateless": "Stateless",
    "mixed": "Mixed",
    "unknown": "Unknown",
    "uncertified": "Uncertified",
    "permissive": "Permissive",
    "copyleft": "Copyleft",
    "proprietary": "Proprietary",
    "cli": "CLI",
    "rest": "REST",
    "graphql": "GraphQL",
    "grpc": "gRPC",
    "markdown": "Markdown",
    "browser": "Browser",
    "server": "Server",
    "local": "Local_Only",
    "active": "Active",
    "reference": "Reference",
    "incubating": "Incubating",
    "abandoned": "Abandoned",
}


def normalize_taxonomy_label(value: Any, default: str) -> str:
    if value is None:
        return default
    text = str(value).strip()
    if not text:
        return default
    key = re.sub(r"[\s\-]+", " ", text).strip().lower()
    if key in TAXONOMY_LABEL_ALIASES:
        return TAXONOMY_LABEL_ALIASES[key]
    collapsed = re.sub(r"[^a-z0-9]+", "_", key).strip("_")
    if collapsed in TAXONOMY_LABEL_ALIASES:
        return TAXONOMY_LABEL_ALIASES[collapsed]
    return text


def select_enriched_value(candidate: Any, fallback: Any, default: str, placeholders: set[str]) -> str:
    candidate_value = normalize_taxonomy_label(candidate, default)
    if candidate_value in placeholders:
        return normalize_taxonomy_label(fallback, default)
    return candidate_value


def github_metadata_evidence_snippets(metadata: GitHubRepositoryMetadata | None) -> list[EvidenceSnippetCandidate]:
    if metadata is None:
        return []
    snippets: list[EvidenceSnippetCandidate] = []
    if metadata.description.strip():
        snippets.append(
            EvidenceSnippetCandidate(
                source_kind="github_repo",
                source_ref="description",
                snippet=metadata.description.strip(),
                confidence=0.95,
            )
        )
    if metadata.topics:
        snippets.append(
            EvidenceSnippetCandidate(
                source_kind="github_repo",
                source_ref="topics",
                snippet=", ".join(metadata.topics[:12]),
                confidence=0.82,
            )
        )
    if metadata.language.strip():
        snippets.append(
            EvidenceSnippetCandidate(
                source_kind="github_repo",
                source_ref="language",
                snippet=metadata.language.strip(),
                confidence=0.74,
            )
        )
    if metadata.license_name.strip() or metadata.license_spdx.strip():
        snippets.append(
            EvidenceSnippetCandidate(
                source_kind="github_repo",
                source_ref="license",
                snippet=f"{metadata.license_name} ({metadata.license_spdx})".strip(),
                confidence=0.9,
            )
        )
    return snippets


def infer_ecosystem_from_github_metadata(metadata: GitHubRepositoryMetadata | None, topic: TopicSpec, fallback_text: str) -> str:
    if metadata is None:
        return infer_ecosystem_from_text(fallback_text, topic)
    lower_text = f"{metadata.full_name} {metadata.description} {' '.join(metadata.topics)}".lower()
    language = metadata.language.strip().lower()
    if topic.key == "curated_lists":
        return "Markdown"
    if language in {"python"}:
        return "Python"
    if language in {"css", "scss", "sass", "less"} or any(token in lower_text for token in ["css", "css-framework", "bootstrap", "normalize"]):
        return "Web_CSS"
    if language in {"javascript", "typescript", "html", "mdx"} or any(token in lower_text for token in ["react", "frontend", "ui", "browser"]):
        if topic.key == "frontend_design_systems":
            return "Web_Frontend"
    if language in {"go"}:
        return "Go"
    if language in {"rust"}:
        return "Rust"
    if language in {"shell", "bash"}:
        return "Shell"
    return infer_ecosystem_from_text(f"{fallback_text} {metadata.description} {' '.join(metadata.topics)} {metadata.language}", topic)


def merge_unique_strings(*groups: Iterable[str]) -> list[str]:
    items: list[str] = []
    for group in groups:
        for item in group:
            if not item:
                continue
            if item not in items:
                items.append(item)
    return items


def truncate_text(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n[truncated]"


def as_string_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, tuple):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str):
        return [value] if value.strip() else []
    return []


def parse_evidence_snippets(value: Any, default_source_kind: str = "repository") -> list[EvidenceSnippetCandidate]:
    snippets: list[EvidenceSnippetCandidate] = []
    for item in value if isinstance(value, list) else []:
        if not isinstance(item, dict):
            continue
        payload = dict(item)
        payload.setdefault("source_kind", default_source_kind)
        payload.setdefault("confidence", 0.5)
        try:
            snippets.append(EvidenceSnippetCandidate.model_validate(payload))
        except ValidationError:
            continue
    return snippets


def parse_entity_terms(value: Any) -> list[EntityTermResult]:
    terms: list[EntityTermResult] = []
    for item in value if isinstance(value, list) else []:
        if not isinstance(item, dict):
            continue
        try:
            terms.append(EntityTermResult.model_validate(item))
        except ValidationError:
            continue
    return terms


def fallback_evidence_snippets(context: RepositoryContext) -> list[EvidenceSnippetCandidate]:
    snippets: list[EvidenceSnippetCandidate] = []
    for document in context.documents[:3]:
        snippets.append(
            EvidenceSnippetCandidate(
                source_kind="local_snapshot",
                source_ref=document.path,
                snippet=truncate_text(document.text, 240),
                confidence=0.58,
            )
        )
    if not snippets:
        snippets.append(
            EvidenceSnippetCandidate(
                source_kind="seed",
                source_ref=context.source_file,
                snippet=context.seed_excerpt,
                confidence=0.5,
            )
        )
    return snippets


def profile_payload(topic: TopicSpec, profile: ResourceProfile) -> dict[str, Any]:
    return {
        "summary": profile.summary,
        "mechanics": profile.mechanics,
        "use_cases": profile.use_cases,
        "patterns": profile.patterns,
        "glossary_terms": profile.glossary_terms,
        "secondary_topics": profile.secondary_topics,
        "sensitivity": profile.sensitivity,
        "status": profile.status,
        "review_reason": profile.review_reason,
        "taxonomy": {
            "ecosystem": profile.ecosystem,
            "domain_primary": profile.domain_primary,
            "maturity_stage": profile.maturity_stage,
            "license_class": profile.license_class,
            "deployment_target": profile.deployment_target,
            "interface_protocol": profile.interface_protocol,
            "data_locality": profile.data_locality,
            "hardware_footprint": profile.hardware_footprint,
            "security_compliance": profile.security_compliance,
        },
        "topic": {
            "key": topic.key,
            "title": topic.title,
            "description": topic.description,
            "canonical_vocabulary": topic.canonical_vocabulary,
            "inclusion_criteria": topic.inclusion_criteria,
            "keywords": topic.keywords,
        },
    }


def build_scout_payload(context: RepositoryContext, topic: TopicSpec, profile: ResourceProfile, deterministic: dict[str, str]) -> dict[str, Any]:
    return {
        "canonical_url": context.canonical_url,
        "repo_key": context.repo_key,
        "source_file": context.source_file,
        "heuristic_topic_key": context.topic_key,
        "heuristic_topic_title": context.heuristic_topic_title,
        "heuristic_profile": profile_payload(topic, profile),
        "seed_excerpt": context.seed_excerpt,
        "inventory": context.inventory,
        "documents": [{"path": document.path, "text": truncate_text(document.text, 2000)} for document in context.documents],
        "deterministic_metadata": deterministic,
        "combined_context": truncate_text(context.combined_text, 12000),
    }


def build_chart_payload(context: RepositoryContext, topic: TopicSpec, profile: ResourceProfile, scout: ScoutResult | None, deterministic: dict[str, str]) -> dict[str, Any]:
    return {
        "canonical_url": context.canonical_url,
        "repo_key": context.repo_key,
        "source_file": context.source_file,
        "heuristic_topic_key": context.topic_key,
        "heuristic_topic_title": context.heuristic_topic_title,
        "heuristic_profile": profile_payload(topic, profile),
        "scout": scout.model_dump() if scout else {},
        "deterministic_metadata": deterministic,
        "documents": [{"path": document.path, "text": truncate_text(document.text, 2200)} for document in context.documents],
        "combined_context": truncate_text(context.combined_text, 14000),
    }


def build_entity_payload(context: RepositoryContext, chart: ChartResult | None, scout: ScoutResult | None) -> dict[str, Any]:
    return {
        "canonical_url": context.canonical_url,
        "repo_key": context.repo_key,
        "source_file": context.source_file,
        "scout": scout.model_dump() if scout else {},
        "chart": chart.model_dump() if chart else {},
        "combined_context": truncate_text(context.combined_text, 10000),
    }


def build_metadata_payload(
    context: RepositoryContext,
    topic: TopicSpec,
    profile: ResourceProfile,
    scout: ScoutResult | None,
    chart: ChartResult | None,
    entities: EntityExtractionResult | None,
    deterministic: dict[str, str],
) -> dict[str, Any]:
    return {
        "canonical_url": context.canonical_url,
        "repo_key": context.repo_key,
        "source_file": context.source_file,
        "heuristic_topic_key": context.topic_key,
        "heuristic_topic_title": context.heuristic_topic_title,
        "heuristic_profile": profile_payload(topic, profile),
        "scout": scout.model_dump() if scout else {},
        "chart": chart.model_dump() if chart else {},
        "entities": entities.model_dump() if entities else {},
        "deterministic_metadata": deterministic,
        "documents": [{"path": document.path, "text": truncate_text(document.text, 1800)} for document in context.documents],
        "combined_context": truncate_text(context.combined_text, 12000),
    }


def merge_resource_profile(
    topic: TopicSpec,
    profile: ResourceProfile,
    github_metadata: GitHubRepositoryMetadata | None,
    scout: ScoutResult | None,
    chart: ChartResult | None,
    metadata: MetadataResult | None,
    entities: EntityExtractionResult | None,
) -> tuple[ResourceProfile, str]:
    glossary_terms = merge_unique_strings(
        profile.glossary_terms,
        scout.candidate_glossary_terms if scout else [],
        chart.glossary_terms if chart else [],
        [term.canonical_form for term in entities.terms] if entities else [],
        topic.glossary_terms,
    )
    patterns = merge_unique_strings(
        profile.patterns,
        scout.candidate_patterns if scout else [],
        chart.patterns if chart else [],
        [f"Pattern - {PATTERN_TITLE_BY_KEY[key]}" for key in topic.patterns if key in PATTERN_TITLE_BY_KEY],
    )
    secondary_topics = merge_unique_strings(
        profile.secondary_topics,
        scout.secondary_topic_keys if scout else [],
        chart.secondary_topic_keys if chart else [],
        topic.overlaps,
    )
    summary = chart.summary if chart and chart.summary else github_metadata.description if github_metadata and github_metadata.description else profile.summary
    mechanics = chart.mechanics if chart and chart.mechanics else profile.mechanics
    use_cases = chart.use_cases if chart and chart.use_cases else profile.use_cases
    maturity = scout.maturity if scout and scout.maturity and scout.maturity != "seed" else chart.maturity if chart and chart.maturity and chart.maturity != "seed" else profile.maturity
    sensitivity = scout.sensitivity if scout and scout.sensitivity and scout.sensitivity != "normal" else profile.sensitivity
    status = "review_pending" if (scout and scout.sensitivity in {"high", "review_pending"}) else profile.status
    review_reason = profile.review_reason
    if scout and scout.reason and status == "review_pending":
        review_reason = scout.reason
    github_license_value = None
    if github_metadata:
        # A manually verified licence wins over the API. GitHub returns
        # NOASSERTION for anything its detector does not recognise, which
        # includes every source-available licence, so a human reading the
        # LICENSE file is the only reliable source for those.
        override = license_override_for(github_metadata.full_name)
        if override:
            github_license_value = override
        elif github_metadata.license_spdx and github_metadata.license_spdx.upper() != "UNKNOWN":
            github_license_value = github_metadata.license_spdx
        elif github_metadata.license_name and github_metadata.license_name != "Unknown":
            github_license_value = github_metadata.license_name
    if github_metadata and github_metadata.description:
        github_context = f"GitHub description: {github_metadata.description}"
        if github_context not in mechanics:
            mechanics = [github_context, *mechanics]
    if metadata:
        ecosystem = select_enriched_value(metadata.ecosystem, profile.ecosystem, "Mixed", {"Mixed", "Unknown"})
        domain_primary = select_enriched_value(metadata.domain_primary, profile.domain_primary, "Mixed", {"Mixed", "Unknown"})
        maturity_stage = select_enriched_value(metadata.maturity_stage, "Abandoned" if github_metadata and github_metadata.archived else profile.maturity_stage, "Active", {"Active", "Unknown"})
        license_class = select_enriched_value(metadata.license_class, license_class_from_name(github_license_value or "unknown"), "Unknown", {"Unknown"})
        deployment_target = select_enriched_value(metadata.deployment_target, profile.deployment_target, "Server", {"Server", "Unknown"})
        interface_protocol = select_enriched_value(metadata.interface_protocol, profile.interface_protocol, "Unknown", {"Unknown"})
        data_locality = select_enriched_value(metadata.data_locality, profile.data_locality, "Distributed", {"Distributed", "Unknown"})
        hardware_footprint = select_enriched_value(metadata.hardware_footprint, profile.hardware_footprint, "CPU_Only", {"CPU_Only", "Unknown"})
        security_compliance = select_enriched_value(metadata.security_compliance, profile.security_compliance, "Uncertified", {"Uncertified", "Unknown"})
        license = select_enriched_value(metadata.license, github_license_value or "unknown", "unknown", {"unknown", "Unknown"})
    else:
        ecosystem = profile.ecosystem or infer_ecosystem_from_github_metadata(github_metadata, topic, summary + " " + " ".join(mechanics) + " ".join(use_cases))
        domain_primary = profile.domain_primary or DOMAIN_PRIMARY_BY_TOPIC_KEY.get(topic.key, "Mixed")
        maturity_stage = "Abandoned" if github_metadata and github_metadata.archived else profile.maturity_stage or MATURITY_STAGE_BY_TOPIC_KEY.get(topic.key, "Active")
        license_class = profile.license_class or license_class_from_name(github_license_value or "unknown")
        deployment_target = profile.deployment_target or DEPLOYMENT_TARGET_BY_TOPIC_KEY.get(topic.key, "Server")
        interface_protocol = profile.interface_protocol or INTERFACE_PROTOCOL_BY_TOPIC_KEY.get(topic.key, "Unknown")
        data_locality = profile.data_locality or DATA_LOCALITY_BY_TOPIC_KEY.get(topic.key, "Distributed")
        hardware_footprint = profile.hardware_footprint or HARDWARE_FOOTPRINT_BY_TOPIC_KEY.get(topic.key, "CPU_Only")
        security_compliance = profile.security_compliance or SECURITY_COMPLIANCE_BY_TOPIC_KEY.get(topic.key, "Uncertified")
        license = github_license_value or "unknown"

    return ResourceProfile(
        summary=summary,
        mechanics=mechanics,
        use_cases=use_cases,
        patterns=patterns,
        glossary_terms=glossary_terms,
        secondary_topics=secondary_topics,
        sensitivity=sensitivity,
        status=status,
        review_reason=review_reason,
        ecosystem=normalize_taxonomy_label(ecosystem, "Mixed"),
        domain_primary=normalize_taxonomy_label(domain_primary, "Mixed"),
        maturity_stage=normalize_taxonomy_label(maturity_stage, "Active"),
        license_class=normalize_taxonomy_label(license_class, "Unknown"),
        deployment_target=normalize_taxonomy_label(deployment_target, "Server"),
        interface_protocol=normalize_taxonomy_label(interface_protocol, "Unknown"),
        data_locality=normalize_taxonomy_label(data_locality, "Distributed"),
        hardware_footprint=normalize_taxonomy_label(hardware_footprint, "CPU_Only"),
        security_compliance=normalize_taxonomy_label(security_compliance, "Uncertified"),
        maturity=maturity,
    ), license


def run_lmstudio_enrichment(
    runtime: LMStudioRuntime,
    context: RepositoryContext,
    topic: TopicSpec,
    profile: ResourceProfile,
) -> ResourceEnrichment:
    if not runtime.available or runtime.client is None:
        return ResourceEnrichment(evidence_snippets=fallback_evidence_snippets(context))

    deterministic = deterministic_metadata_signals(context, topic)
    scout_payload = build_scout_payload(context, topic, profile, deterministic)
    scout_raw = call_lmstudio_stage(runtime, "scout", "scout.md", scout_payload, max_tokens=512)
    scout: ScoutResult | None = None
    if scout_raw is not None:
        try:
            scout = ScoutResult.model_validate(scout_raw)
        except ValidationError:
            scout = None
    if not runtime.available or scout_raw is None:
        return ResourceEnrichment(scout=scout, evidence_snippets=fallback_evidence_snippets(context))

    chart_payload = build_chart_payload(context, topic, profile, scout, deterministic)
    chart_raw = call_lmstudio_stage(runtime, "chart", "chart.md", chart_payload, max_tokens=1200)
    chart: ChartResult | None = None
    if chart_raw is not None:
        try:
            chart = ChartResult.model_validate(chart_raw)
        except ValidationError:
            chart = None
    if not runtime.available or chart_raw is None:
        return ResourceEnrichment(scout=scout, chart=chart, evidence_snippets=fallback_evidence_snippets(context))

    entity_payload = build_entity_payload(context, chart, scout)
    entity_raw = call_lmstudio_stage(runtime, "entity_extraction", "entity_extraction.md", entity_payload, max_tokens=900)
    entities: EntityExtractionResult | None = None
    if entity_raw is not None:
        try:
            entities = EntityExtractionResult.model_validate(entity_raw)
        except ValidationError:
            entities = None
    if not runtime.available or entity_raw is None:
        return ResourceEnrichment(scout=scout, chart=chart, entities=entities, evidence_snippets=fallback_evidence_snippets(context))

    metadata_payload = build_metadata_payload(context, topic, profile, scout, chart, entities, deterministic)
    metadata_raw = call_lmstudio_stage(runtime, "metadata_enrichment", "metadata_enrichment.md", metadata_payload, max_tokens=800)
    metadata: MetadataResult | None = None
    if metadata_raw is not None:
        try:
            metadata = MetadataResult.model_validate(metadata_raw)
        except ValidationError:
            metadata = None

    evidence_snippets = []
    if chart:
        evidence_snippets.extend(chart.evidence_snippets)
    if metadata:
        evidence_snippets.extend(metadata.evidence_snippets)
    if not evidence_snippets:
        evidence_snippets = fallback_evidence_snippets(context)

    return ResourceEnrichment(
        scout=scout,
        chart=chart,
        metadata=metadata,
        entities=entities,
        evidence_snippets=evidence_snippets,
    )


TOPICS: list[TopicSpec] = [
    TopicSpec(
        key="curated_lists",
        title="Curated Aggregators & Reference Lists",
        description="Repositories that curate, annotate, or index other resources rather than implementing a single tool.",
        inclusion_criteria="Awesome lists, resource directories, annotated collections, or repositories whose value is primarily discovery and comparison.",
        canonical_vocabulary=["curation", "taxonomy", "directory", "reference list", "index", "collection", "annotated examples"],
        keywords=["awesome", "generated-awesomeness", "project-ideas", "annotated", "collection", "checklist", "resources", "tracker"],
        patterns=["curated_curation", "reference_architecture"],
        glossary_terms=["Curation", "Taxonomy", "Reference List", "Discovery", "Annotated Example"],
        mechanics=[
            "Curates links, annotations, and taxonomies rather than a single implementation path.",
            "Optimized for discovery, comparison, and reuse across many downstream projects.",
            "Often requires atomic extraction into individual notes before it becomes graph-friendly.",
        ],
        use_cases=[
            "Scan for candidate tools or approaches.",
            "Compare overlapping ecosystems without manual tab-switching.",
            "Seed a new index before deeper source ingestion is available.",
        ],
    ),
    TopicSpec(
        key="agentic_ai_models",
        title="Agentic AI & Models",
        description="Model-centric and agent-centric repositories that cover orchestration, inference, prompting, multimodal systems, and voice/video tooling.",
        inclusion_criteria="Model repositories, agent frameworks, orchestration examples, multimodal systems, TTS/STT models, or collections focused on AI model discovery.",
        canonical_vocabulary=["LLM", "agent orchestration", "inference", "prompting", "tool use", "multimodal", "TTS", "STT"],
        keywords=["ai", "llm", "model", "semantic-kernel", "chatgpt", "skills", "distributed-ai", "efficient-dlms", "voice", "tts", "stt", "video"],
        patterns=["agent_orchestration", "model_inference_pipeline", "multimodal_processing"],
        glossary_terms=["LLM", "Agent", "Prompt", "Inference", "TTS", "STT", "Multimodal Model"],
        mechanics=[
            "Uses prompts, tools, memory, or pipelines to coordinate model behavior.",
            "May combine text, audio, video, or other modalities into one inference path.",
            "Often surfaces evaluation, routing, or serving layers rather than only model weights.",
        ],
        use_cases=[
            "Prototype assistants and agent workflows.",
            "Compare model families and serving patterns.",
            "Study multimodal or voice-centric open-source systems.",
        ],
        overlaps=["architecture_playbooks"],
    ),
    TopicSpec(
        key="data_api_big_data",
        title="Data APIs & Big Data",
        description="Data portals, API layers, and repository collections useful for ingestion, retrieval, analytics, and source discovery.",
        inclusion_criteria="Open data portals, public APIs, dataset catalogs, API tracking projects, and big-data resource lists.",
        canonical_vocabulary=["API", "dataset", "endpoint", "schema", "open data", "rate limit", "catalog", "ingestion"],
        keywords=["data", "api", "nasa", "open-banking", "dataset", "gov", "portal", "source", "tracker"],
        patterns=["open_data_portal", "etl_api_ingestion", "schema_mapping"],
        glossary_terms=["API", "Dataset", "Open Data", "Endpoint", "Schema", "Rate Limit"],
        mechanics=[
            "Exposes structured data through endpoints, catalogs, or retrieval layers.",
            "Frequently needs schema mapping, auth handling, and rate-limit awareness.",
            "Often feeds ETL, analytics, or scientific workflows.",
        ],
        use_cases=[
            "Build ingestion pipelines for public or partner data.",
            "Compare accessible datasets and API shapes.",
            "Seed analytics or knowledge-graph projects with reliable sources.",
        ],
        overlaps=["government_civic_tech", "geospatial_earth_data"],
    ),
    TopicSpec(
        key="geospatial_earth_data",
        title="Geospatial & Earth Data",
        description="Spatial, satellite, and earth-science resources that handle maps, coordinates, imagery, or geodata pipelines.",
        inclusion_criteria="Geospatial data portals, satellite pipelines, mapping tools, spatial feature management, or Earth-observation datasets.",
        canonical_vocabulary=["geospatial", "satellite imagery", "STAC", "GeoJSON", "raster", "spatial index", "coordinates"],
        keywords=["geo", "geoq", "satellite", "earth", "modis", "landsat", "geojson", "stac", "hdf5", "netcdf"],
        patterns=["spatial_indexing", "stac_ingestion"],
        glossary_terms=["Geospatial Data", "Satellite Imagery", "GeoJSON", "STAC"],
        mechanics=[
            "Coordinates geometry-aware retrieval and spatial analysis.",
            "Often intersects with raster, tile, or satellite-ingestion workflows.",
            "May expose geodata through web apps or structured APIs.",
        ],
        use_cases=[
            "Build earth-observation or mapping pipelines.",
            "Cross-reference spatial datasets with other APIs.",
            "Organize geodata sources for later ML or GIS work.",
        ],
        overlaps=["data_api_big_data", "government_civic_tech"],
    ),
    TopicSpec(
        key="infrastructure_observability",
        title="Infrastructure & Observability",
        description="Infrastructure automation, deployment, telemetry, monitoring, and service reliability tools.",
        inclusion_criteria="Infrastructure-as-code tools, cloud platforms, monitoring systems, metrics collectors, logging or alerting systems, and operational tooling.",
        canonical_vocabulary=["infrastructure as code", "telemetry", "monitoring", "metrics", "alerting", "orchestration", "provisioning", "cloud"],
        keywords=["terraform", "puppet", "chef", "openstack", "prometheus", "statsd", "netdata", "sentry", "cloudflare", "api-umbrella"],
        patterns=["infrastructure_as_code", "observability_pipeline", "service_telemetry"],
        glossary_terms=["Infrastructure as Code", "Monitoring", "Observability", "Telemetry", "Metrics"],
        mechanics=[
            "Coordinates deployment, provisioning, telemetry, and runtime health.",
            "Often splits into declarative config, collector, aggregator, and alert layers.",
            "Acts as the connective tissue for operating larger systems.",
        ],
        use_cases=[
            "Automate deployments and configuration management.",
            "Trace service health and system reliability over time.",
            "Compare telemetry platforms and monitoring primitives.",
        ],
        overlaps=["security_siem", "government_civic_tech"],
    ),
    TopicSpec(
        key="security_siem",
        title="Security & SIEM",
        description="Threat detection, security enrichment, event processing, and dual-use security-adjacent tooling.",
        inclusion_criteria="Security analytics, SIEM pipelines, threat enrichment, adversarial tooling, or other security-adjacent resources that benefit from manual review.",
        canonical_vocabulary=["SIEM", "threat detection", "enrichment", "alerting", "event processing", "security analytics"],
        keywords=["security", "siem", "threat", "cctv", "awesome-ai-security-tools", "siembol"],
        patterns=["threat_detection_pipeline", "event_enrichment", "security_analytics"],
        glossary_terms=["SIEM", "Threat Detection", "Enrichment", "Alerting"],
        mechanics=[
            "Ingests and normalizes events before applying threat logic or enrichment.",
            "Often includes alerts, detections, and contextual joins.",
            "May be dual-use and therefore should be review-gated before publication.",
        ],
        use_cases=[
            "Study security event pipelines.",
            "Compare threat detection or enrichment patterns.",
            "Hold security-adjacent resources in a review queue until approved.",
        ],
        overlaps=["infrastructure_observability", "data_api_big_data"],
    ),
    TopicSpec(
        key="frontend_design_systems",
        title="Frontend & Design Systems",
        description="Front-end frameworks, CSS systems, rendering libraries, and browser-facing implementation references.",
        inclusion_criteria="UI frameworks, component libraries, CSS resets, animation systems, browser feature detection, and frontend implementation notes.",
        canonical_vocabulary=["component library", "responsive design", "CSS reset", "feature detection", "layout", "DOM"],
        keywords=["react", "bootstrap", "animate", "normalize", "modernizr", "grid"],
        patterns=["component_based_ui", "feature_detection", "responsive_layout"],
        glossary_terms=["Component Library", "Responsive Design", "CSS Reset", "Feature Detection", "DOM"],
        mechanics=[
            "Composes interface primitives into reusable components and layout systems.",
            "Often separates feature detection, normalization, animation, and layout concerns.",
            "Useful as a reference for browser compatibility and design-system decisions.",
        ],
        use_cases=[
            "Build or compare UI systems.",
            "Study browser behavior and front-end primitives.",
            "Seed product-design decisions with proven implementation patterns.",
        ],
        overlaps=["architecture_playbooks", "cad_saas_design"],
    ),
    TopicSpec(
        key="scientific_simulation_math",
        title="Scientific Simulation & Math",
        description="Scientific computation, simulation, symbolic mathematics, and domain-specific analysis tools.",
        inclusion_criteria="Simulation libraries, symbolic math packages, astronomy toolkits, active-learning review tools, or similar scientific references.",
        canonical_vocabulary=["simulation", "symbolic mathematics", "astronomy", "active learning", "domain modeling", "multibody dynamics"],
        keywords=["simbody", "astropy", "sympy", "scikit-ued", "gap-system", "asreview"],
        patterns=["scientific_simulation", "symbolic_computation", "active_learning_review"],
        glossary_terms=["Simulation", "Symbolic Mathematics", "Astronomy", "Active Learning"],
        mechanics=[
            "Applies domain-specific numerical or symbolic reasoning.",
            "May model physical systems, algebraic structures, or research workflows.",
            "Usually prioritizes correctness, reproducibility, and inspection of intermediate state.",
        ],
        use_cases=[
            "Simulate bodies or physical systems.",
            "Derive symbolic expressions or solve algebraic problems.",
            "Support research review and scientific analysis workflows.",
        ],
        overlaps=["data_api_big_data", "geospatial_earth_data"],
    ),
    TopicSpec(
        key="government_civic_tech",
        title="Government & Civic Tech",
        description="Public-sector open source, civic platforms, governance tooling, and public-data publishing references.",
        inclusion_criteria="Government open-source projects, civic technology, service playbooks, public data platforms, or policy-adjacent repositories.",
        canonical_vocabulary=["civic tech", "open government", "public service", "publishing platform", "playbook", "open data"],
        keywords=["government", "whitehall", "usds", "cfpb", "data.gov", "government.github.com", "playbook", "open-source-checklist"],
        patterns=["civic_tech_playbook", "public_data_publishing", "service_guidance"],
        glossary_terms=["Civic Tech", "Public Service", "Open Government", "Playbook"],
        mechanics=[
            "Combines public-service content, policy guidance, or platform tooling.",
            "Often supports transparency, publishing, or service standards.",
            "Useful for comparing governance patterns and public-sector design choices.",
        ],
        use_cases=[
            "Study public-sector open-source practices.",
            "Track public-data platforms and policy artifacts.",
            "Reference service design or governance playbooks.",
        ],
        overlaps=["data_api_big_data", "infrastructure_observability"],
    ),
    TopicSpec(
        key="cad_saas_design",
        title="CAD & SaaS Design",
        description="Computer-aided design, SaaS design systems, and product design tooling that should remain available for future expansion.",
        inclusion_criteria="CAD tools, SaaS design resources, product-design systems, export-oriented workspace tools, or related references.",
        canonical_vocabulary=["CAD", "SaaS", "product design", "workspace", "export formats", "design tooling"],
        keywords=["cad", "saas", "design", "product", "studio", "tooling"],
        patterns=["cad_workflow", "saas_product_design"],
        glossary_terms=["CAD", "SaaS", "Product Design"],
        mechanics=[
            "Focuses on artifacts, formats, and workflow integration for design work.",
            "Often emphasizes exportability, workspace state, and human-in-the-loop review.",
            "Can be expanded later as the catalog gains CAD or SaaS resources.",
        ],
        use_cases=[
            "Catalogue design tools for later reference.",
            "Compare product-design workflows.",
            "Prepare the vault for future CAD resources without changing the schema again.",
        ],
        overlaps=["frontend_design_systems", "architecture_playbooks"],
    ),
    TopicSpec(
        key="architecture_playbooks",
        title="Architecture & Developer Playbooks",
        description="Annotated codebases, implementation walkthroughs, and design playbooks that explain how systems are built.",
        inclusion_criteria="Annotated repositories, reference architectures, checklist-style governance notes, or repos whose purpose is to teach design and implementation patterns.",
        canonical_vocabulary=["reference architecture", "playbook", "annotated implementation", "design pattern", "async", "ASGI", "dependency injection"],
        keywords=["annotated", "skills", "playbook", "checklist", "advanced-usage", "skills", "framework"],
        patterns=["reference_architecture", "playbook", "dependency_injection", "async_architecture"],
        glossary_terms=["Architecture", "Playbook", "Dependency Injection", "Async", "ASGI"],
        mechanics=[
            "Explains how a system is built, not just what it does.",
            "Captures design decisions, interface contracts, and reusable mechanics.",
            "Functions as a memory anchor for later project planning.",
        ],
        use_cases=[
            "Study implementation patterns and code organization.",
            "Map a repository to reusable architectural concepts.",
            "Feed a local memory system with reusable technical patterns.",
        ],
        overlaps=["agentic_ai_models", "frontend_design_systems", "government_civic_tech"],
    ),
]


PATTERNS: list[PatternSpec] = [
    PatternSpec(
        key="curated_curation",
        title="Curated Resource Curation",
        definition="A repository pattern that aggregates, annotates, and routes users toward other resources rather than implementing a single end-user tool.",
        aliases=["resource catalog", "awesome-list curation"],
        examples=["orsinium-labs/generated-awesomeness", "pracdata/awesome-open-source-data-engineering", "The-Cool-Coders/Project-Ideas-And-Resources"],
        glossary_terms=["Curation", "Reference List", "Taxonomy"],
        topic_keys=["curated_lists"],
    ),
    PatternSpec(
        key="agent_orchestration",
        title="Agent Orchestration",
        definition="Coordinating prompts, tools, memory, and models so a system can execute multi-step work rather than single-shot inference.",
        aliases=["orchestration layer"],
        examples=["Azure-Samples/semantic-kernel-advanced-usage", "vercel-labs/skills"],
        glossary_terms=["Agent", "LLM", "Prompt", "Tool Use"],
        topic_keys=["agentic_ai_models", "architecture_playbooks"],
    ),
    PatternSpec(
        key="model_inference_pipeline",
        title="Model Inference Pipeline",
        definition="A pipeline that routes model inputs through preprocessing, inference, postprocessing, and optional review or memory layers.",
        aliases=["serving pipeline"],
        examples=["moyu6027/awsome-chatgpt-like", "armanakbari/Awsome-Efficient-DLMs"],
        glossary_terms=["Inference", "Multimodal Model", "Prompt"],
        topic_keys=["agentic_ai_models"],
    ),
    PatternSpec(
        key="open_data_portal",
        title="Open Data Portal",
        definition="A discoverable data-access pattern where public or partner data is published through structured endpoints or catalogs.",
        aliases=["public data portal"],
        examples=["GSA/data.gov", "not-a-bank/open-banking-tracker-data"],
        glossary_terms=["API", "Dataset", "Open Data", "Endpoint"],
        topic_keys=["data_api_big_data", "government_civic_tech"],
    ),
    PatternSpec(
        key="spatial_ingestion",
        title="Spatial Ingestion",
        definition="Handling geospatial or Earth-observation data with spatial formats, coordinates, and map-aware processing.",
        aliases=["geo ingestion"],
        examples=["ngageoint/geoq"],
        glossary_terms=["Geospatial Data", "STAC", "GeoJSON"],
        topic_keys=["geospatial_earth_data", "data_api_big_data"],
    ),
    PatternSpec(
        key="infrastructure_as_code",
        title="Infrastructure as Code",
        definition="Declarative provisioning and configuration of infrastructure using code instead of manual setup.",
        aliases=["IaC"],
        examples=["hashicorp/terraform", "puppetlabs/puppet", "chef/chef", "openstack/openstack"],
        glossary_terms=["Infrastructure as Code", "Provisioning", "Cloud"],
        topic_keys=["infrastructure_observability"],
    ),
    PatternSpec(
        key="observability_pipeline",
        title="Observability Pipeline",
        definition="A telemetry architecture that collects, stores, queries, and alerts on metrics or events.",
        aliases=["telemetry pipeline"],
        examples=["prometheus/prometheus", "netdata/netdata", "statsd/statsd", "getsentry/sentry"],
        glossary_terms=["Monitoring", "Observability", "Telemetry", "Metrics"],
        topic_keys=["infrastructure_observability"],
    ),
    PatternSpec(
        key="threat_detection_pipeline",
        title="Threat Detection Pipeline",
        definition="Security analytics flow that ingests events, enriches them, and raises detections or alerts.",
        aliases=["security analytics pipeline"],
        examples=["G-Research/siembol", "scadastrangelove/awesome-ai-security-tools"],
        glossary_terms=["SIEM", "Threat Detection", "Enrichment"],
        topic_keys=["security_siem"],
    ),
    PatternSpec(
        key="component_based_ui",
        title="Component-Based UI",
        definition="Front-end architecture that composes reusable interface primitives into a larger experience.",
        aliases=["component library"],
        examples=["react/react", "twbs/bootstrap"],
        glossary_terms=["Component Library", "DOM", "Responsive Design"],
        topic_keys=["frontend_design_systems"],
    ),
    PatternSpec(
        key="feature_detection",
        title="Feature Detection",
        definition="A compatibility strategy that checks what the browser or environment can do before deciding which code path to execute.",
        aliases=["progressive enhancement"],
        examples=["Modernizr/Modernizr"],
        glossary_terms=["Feature Detection"],
        topic_keys=["frontend_design_systems"],
    ),
    PatternSpec(
        key="scientific_simulation",
        title="Scientific Simulation",
        definition="A domain model that simulates physical, mathematical, or scientific systems for analysis.",
        aliases=["simulation engine"],
        examples=["simbody/simbody", "astropy/astropy"],
        glossary_terms=["Simulation", "Astronomy", "Symbolic Mathematics"],
        topic_keys=["scientific_simulation_math"],
    ),
    PatternSpec(
        key="symbolic_computation",
        title="Symbolic Computation",
        definition="Mathematical reasoning over symbolic expressions rather than only numeric values.",
        aliases=["computer algebra"],
        examples=["sympy/sympy", "gap-system/gap"],
        glossary_terms=["Symbolic Mathematics"],
        topic_keys=["scientific_simulation_math"],
    ),
    PatternSpec(
        key="civic_tech_playbook",
        title="Civic Tech Playbook",
        definition="Public-service guidance or government-facing architecture that documents standards, publishing, or implementation patterns.",
        aliases=["public playbook"],
        examples=["usds/playbook", "alphagov/whitehall", "cfpb/open-source-checklist"],
        glossary_terms=["Civic Tech", "Playbook", "Open Government"],
        topic_keys=["government_civic_tech"],
    ),
    PatternSpec(
        key="reference_architecture",
        title="Reference Architecture",
        definition="An annotated repository that exposes architectural decisions, code structure, and reusable design contracts.",
        aliases=["architecture walkthrough"],
        examples=["hhstore/annotated-py-projects", "Azure-Samples/semantic-kernel-advanced-usage"],
        glossary_terms=["Architecture", "Design Pattern", "Async"],
        topic_keys=["architecture_playbooks"],
    ),
    PatternSpec(
        key="knowledge_graph_routing",
        title="Knowledge Graph Routing",
        definition="A graph structure that routes from top-level indexes to topics, glossary terms, patterns, and resources using typed links.",
        aliases=["semantic routing"],
        examples=["Master Index", "Glossary Index", "Pattern Index"],
        glossary_terms=["Knowledge Graph", "Topic Index", "Glossary Sense"],
        topic_keys=["architecture_playbooks"],
    ),
]


GLOSSARY: list[GlossarySpec] = [
    GlossarySpec("curation", "Curation", "The act of selecting, organizing, and annotating resources for later discovery or reuse.", ["curated"], ["Taxonomy", "Reference List", "Discovery"], ["curated_lists"]),
    GlossarySpec("taxonomy", "Taxonomy", "A controlled structure for grouping concepts or resources into meaningful categories.", ["taxonomies"], ["Curation", "Topic Index"], ["curated_lists", "architecture_playbooks"]),
    GlossarySpec("reference-list", "Reference List", "A curated list of resources meant for comparison, discovery, or routing into deeper work.", ["reference list"], ["Curation", "Discovery"], ["curated_lists"]),
    GlossarySpec("discovery", "Discovery", "The process of finding or surfacing candidate resources, concepts, or tools.", [], ["Curation", "Reference List"], ["curated_lists"]),
    GlossarySpec("annotated-example", "Annotated Example", "A resource that explains a codebase or workflow through commentary and selective explanation.", ["annotated examples"], ["Architecture", "Playbook"], ["architecture_playbooks"]),
    GlossarySpec("api", "API", "A programmatic interface that exposes structured capabilities or data to another system.", ["APIs"], ["Endpoint", "Schema", "Dataset"], ["data_api_big_data", "government_civic_tech", "geospatial_earth_data"]),
    GlossarySpec("agent", "Agent", "An autonomous or semi-autonomous system that can plan, call tools, or manage multi-step work.", ["agents"], ["LLM", "Tool Use", "Prompt"], ["agentic_ai_models", "architecture_playbooks"]),
    GlossarySpec("llm", "LLM", "A large language model used for text generation, reasoning, or tool-augmented workflows.", ["large language model"], ["Prompt", "Inference", "Agent"], ["agentic_ai_models"]),
    GlossarySpec("prompt", "Prompt", "Instructional input supplied to a model or agent to shape its output or behavior.", ["prompts"], ["LLM", "Agent"], ["agentic_ai_models", "architecture_playbooks"]),
    GlossarySpec("inference", "Inference", "The act of running a trained model to produce predictions or generated output.", [], ["LLM", "Multimodal Model"], ["agentic_ai_models"]),
    GlossarySpec("tts", "TTS", "Text-to-speech synthesis that converts written input into spoken audio.", ["text-to-speech"], ["STT", "Voice"], ["agentic_ai_models"]),
    GlossarySpec("stt", "STT", "Speech-to-text transcription that converts audio into text.", ["speech-to-text"], ["TTS", "Voice"], ["agentic_ai_models"]),
    GlossarySpec("multimodal", "Multimodal Model", "A model that handles more than one kind of input or output modality, such as text, audio, image, or video.", ["multimodal"], ["LLM", "Inference"], ["agentic_ai_models"]),
    GlossarySpec("dataset", "Dataset", "A structured collection of records or files that can be queried, analyzed, or ingested.", ["data set"], ["API", "Open Data"], ["data_api_big_data", "geospatial_earth_data"]),
    GlossarySpec("open-data", "Open Data", "Data made accessible for reuse, analysis, or public distribution through a platform or portal.", ["open data"], ["API", "Dataset"], ["data_api_big_data", "government_civic_tech"]),
    GlossarySpec("endpoint", "Endpoint", "A network-accessible route that accepts requests and returns a response.", ["endpoints"], ["API", "Schema"], ["data_api_big_data"]),
    GlossarySpec("schema", "Schema", "A structured description of the shape, meaning, or validation rules for data.", ["schemas"], ["API", "Dataset"], ["data_api_big_data", "government_civic_tech"]),
    GlossarySpec("rate-limit", "Rate Limit", "A cap on how frequently an API can be called within a time window.", ["rate limits"], ["API"], ["data_api_big_data"]),
    GlossarySpec("geospatial-data", "Geospatial Data", "Data with location-aware coordinates, geometry, or map context.", ["geospatial"], ["GeoJSON", "STAC", "Satellite Imagery"], ["geospatial_earth_data"]),
    GlossarySpec("satellite-imagery", "Satellite Imagery", "Earth-observation imagery captured from satellites or orbital platforms.", ["satellite"], ["Geospatial Data", "STAC"], ["geospatial_earth_data"]),
    GlossarySpec("geojson", "GeoJSON", "A common JSON-based format for geographic features and geometry.", ["geo json"], ["Geospatial Data"], ["geospatial_earth_data"]),
    GlossarySpec("stac", "STAC", "SpatioTemporal Asset Catalog, a standard for cataloging geospatial assets.", ["spatiotemporal asset catalog"], ["Geospatial Data", "Satellite Imagery"], ["geospatial_earth_data"]),
    GlossarySpec("observability", "Observability", "The ability to understand system behavior through metrics, logs, traces, and alerts.", [], ["Monitoring", "Telemetry", "Metrics"], ["infrastructure_observability"]),
    GlossarySpec("monitoring", "Monitoring", "The collection and inspection of runtime signals to detect health or performance issues.", [], ["Observability", "Metrics"], ["infrastructure_observability"]),
    GlossarySpec("telemetry", "Telemetry", "Signals emitted by a system for measurement, debugging, or alerting.", [], ["Observability", "Monitoring"], ["infrastructure_observability"]),
    GlossarySpec("metrics", "Metrics", "Quantitative signals collected from systems to measure state or behavior.", [], ["Monitoring", "Telemetry"], ["infrastructure_observability"]),
    GlossarySpec("iac", "Infrastructure as Code", "Managing infrastructure through declarative or programmatic code rather than manual configuration.", ["infrastructure as code", "IaC"], ["Provisioning", "Cloud"], ["infrastructure_observability"]),
    GlossarySpec("cloud", "Cloud", "An infrastructure model that provides compute, storage, or platform capabilities as managed services.", [], ["Infrastructure as Code"], ["infrastructure_observability", "government_civic_tech"]),
    GlossarySpec("siem", "SIEM", "Security information and event management systems that centralize, normalize, and analyze security events.", [], ["Threat Detection", "Enrichment"], ["security_siem"]),
    GlossarySpec("threat-detection", "Threat Detection", "The process of identifying malicious, suspicious, or policy-violating activity.", [], ["SIEM", "Enrichment"], ["security_siem"]),
    GlossarySpec("enrichment", "Enrichment", "Adding external context or derived attributes to raw events before analysis or alerting.", [], ["SIEM", "Threat Detection"], ["security_siem"]),
    GlossarySpec("alerting", "Alerting", "Routing detected conditions to humans or systems that need to act on them.", [], ["Observability", "SIEM"], ["security_siem", "infrastructure_observability"]),
    GlossarySpec("public-service", "Public Service", "Government work or service delivery intended for public benefit.", ["public service"], ["Civic Tech", "Open Government"], ["government_civic_tech"]),
    GlossarySpec("component-library", "Component Library", "A reusable set of UI primitives or patterns used to compose interfaces.", ["design system"], ["Responsive Design", "DOM"], ["frontend_design_systems"]),
    GlossarySpec("responsive-design", "Responsive Design", "A layout approach that adapts to different screen sizes or device capabilities.", [], ["Component Library", "CSS Reset"], ["frontend_design_systems"]),
    GlossarySpec("css-reset", "CSS Reset", "A stylesheet or strategy that normalizes browser defaults.", ["normalize stylesheet"], ["Feature Detection", "Responsive Design"], ["frontend_design_systems"]),
    GlossarySpec("feature-detection", "Feature Detection", "Checking whether an environment supports a capability before using it.", ["progressive enhancement"], ["CSS Reset"], ["frontend_design_systems"]),
    GlossarySpec("dom", "DOM", "The browser document model that front-end code manipulates.", ["document object model"], ["Component Library"], ["frontend_design_systems"]),
    GlossarySpec("simulation", "Simulation", "The imitation of a system or process for analysis, prediction, or exploration.", [], ["Scientific Simulation"], ["scientific_simulation_math"]),
    GlossarySpec("symbolic-mathematics", "Symbolic Mathematics", "Mathematical manipulation of symbolic expressions rather than numeric approximations alone.", ["computer algebra"], ["Simulation"], ["scientific_simulation_math"]),
    GlossarySpec("astronomy", "Astronomy", "The scientific study of celestial objects, space, and the physics of the universe.", [], ["Geospatial Data"], ["scientific_simulation_math"]),
    GlossarySpec("multibody-dynamics", "Multibody Dynamics", "The simulation of connected bodies and joints under physics constraints.", ["rigid body dynamics"], ["Simulation"], ["scientific_simulation_math"]),
    GlossarySpec("active-learning", "Active Learning", "A machine-learning workflow that chooses informative samples for labeling or review.", [], ["Review Workflow"], ["scientific_simulation_math"]),
    GlossarySpec("data-engineering", "Data Engineering", "The practice of building systems that ingest, transform, and deliver data.", [], ["API", "Dataset", "Schema"], ["data_api_big_data"]),
    GlossarySpec("product-design", "Product Design", "The design of user-facing software experiences and workflows.", [], ["SaaS", "CAD"], ["cad_saas_design"]),
    GlossarySpec("civic-tech", "Civic Tech", "Open-source software and practices focused on public-service or civic outcomes.", [], ["Open Government", "Playbook"], ["government_civic_tech"]),
    GlossarySpec("playbook", "Playbook", "A guidance document or implementation handbook that codifies best practices.", [], ["Architecture", "Civic Tech"], ["government_civic_tech", "architecture_playbooks"]),
    GlossarySpec("open-government", "Open Government", "Government processes or data intentionally made accessible and reusable.", [], ["Open Data", "Civic Tech"], ["government_civic_tech"]),
    GlossarySpec("cad", "CAD", "Computer-aided design tooling and workflows.", [], ["SaaS", "Product Design"], ["cad_saas_design"]),
    GlossarySpec("saas", "SaaS", "Software delivered as a hosted service and often paired with product-design workflows.", [], ["CAD", "Product Design"], ["cad_saas_design"]),
    GlossarySpec("knowledge-graph", "Knowledge Graph", "A graph-based model of entities and typed relationships used for retrieval and reasoning.", [], ["Topic Index", "Glossary Sense"], ["architecture_playbooks"]),
    GlossarySpec("topic-index", "Topic Index", "A sub-index that routes a domain or problem space to the resources that belong there.", [], ["Master Index", "Glossary Index"], ["architecture_playbooks"]),
    GlossarySpec("glossary-sense", "Glossary Sense", "A single meaning for a term when a spelling could map to more than one concept.", [], ["Glossary", "Ontology"], ["architecture_playbooks"]),
    GlossarySpec("evidence-snippet", "Evidence Snippet", "A short excerpt or summary fragment that justifies a classification or link.", [], ["Catalog", "Review"], ["architecture_playbooks"]),
    GlossarySpec("architecture", "Architecture", "The structure, decisions, and organizing ideas that shape how a system is built.", [], ["Playbook", "Dependency Injection"], ["architecture_playbooks"]),
    GlossarySpec("dependency-injection", "Dependency Injection", "A pattern where dependencies are supplied to a component instead of created internally.", ["DI"], ["Architecture"], ["architecture_playbooks"]),
    GlossarySpec("async", "Async", "A programming style that allows work to progress without blocking on each step.", ["asynchronous"], ["ASGI", "Architecture"], ["architecture_playbooks"]),
    GlossarySpec("asgi", "ASGI", "Asynchronous Server Gateway Interface, a Python protocol for async web applications.", ["asynchronous server gateway interface"], ["Async"], ["architecture_playbooks"]),
]


RESOURCE_HINTS: dict[str, ResourceProfile] = {
    "orsinium-labs/generated-awesomeness": ResourceProfile(
        summary="Generated or curated awesome-style resource index for discovering open-source tools and projects.",
        mechanics=[
            "Functions as a discovery layer instead of a single implementation.",
            "Encodes resource taxonomies rather than execution code.",
            "Useful as a high-level seed for further topic extraction.",
        ],
        use_cases=["Discover candidate tools quickly.", "Bootstrap a taxonomy of resources.", "Compare large curated lists."],
        patterns=["Pattern - Curated Resource Curation"],
        glossary_terms=["Curation", "Reference List", "Discovery", "Taxonomy"],
        secondary_topics=["architecture_playbooks"],
    ),
    "pracdata/awesome-open-source-data-engineering": ResourceProfile(
        summary="Curated index of open-source data engineering resources and tools.",
        mechanics=["Centers on discovery and comparison.", "Clusters tooling by task or layer.", "Useful for assembling data-platform stacks."],
        use_cases=["Find data engineering references.", "Build a stack from existing tools.", "Map data workflows.",],
        patterns=["Pattern - Curated Resource Curation"],
        glossary_terms=["Curation", "Data Engineering", "Reference List"],
        secondary_topics=["data_api_big_data"],
    ),
    "The-Cool-Coders/Project-Ideas-And-Resources": ResourceProfile(
        summary="Curated repository of project ideas and supporting resources.",
        mechanics=["Aggregates prompts, ideas, and references.", "Useful for inspiration and scoping.", "Acts as a discovery layer rather than implementation code."],
        use_cases=["Find project ideas.", "Seed prototypes.", "Collect adjacent resources."],
        patterns=["Pattern - Curated Resource Curation"],
        glossary_terms=["Curation", "Discovery", "Reference List"],
        secondary_topics=["architecture_playbooks"],
    ),
    "hhstore/annotated-py-projects": ResourceProfile(
        summary="Annotated Python project collection focused on implementation structure and design choices.",
        mechanics=["Explains codebases through commentary and comparison.", "Useful for studying architecture, async patterns, and framework mechanics.", "Acts as a reference architecture library."],
        use_cases=["Study Python web/app implementations.", "Compare async frameworks and project structures.", "Feed architectural memory systems."],
        patterns=["Pattern - Reference Architecture"],
        glossary_terms=["Architecture", "Async", "ASGI", "Dependency Injection"],
        secondary_topics=["architecture_playbooks", "frontend_design_systems"],
    ),
    "Azure-Samples/semantic-kernel-advanced-usage": ResourceProfile(
        summary="Advanced usage examples for Semantic Kernel patterns and integrations.",
        mechanics=["Demonstrates orchestration, skills, and model integration.", "Useful for agent design and tool chaining.", "Contains patterns rather than a single product."],
        use_cases=["Study Semantic Kernel workflows.", "Prototype model-augmented applications.", "Compare advanced agent patterns."],
        patterns=["Pattern - Agent Orchestration"],
        glossary_terms=["Agent", "LLM", "Prompt", "Tool Use"],
        secondary_topics=["architecture_playbooks"],
    ),
    "vercel-labs/skills": ResourceProfile(
        summary="Repository of skills or capability modules for agent-style workflows.",
        mechanics=["Encodes reusable action units for assistants.", "Useful as an integration surface for agent routing.", "Supports capability-based composition."],
        use_cases=["Build skill-driven agent flows.", "Study tool boundaries.", "Prototype reusable capabilities."],
        patterns=["Pattern - Agent Orchestration"],
        glossary_terms=["Agent", "Tool Use", "Prompt"],
        secondary_topics=["agentic_ai_models", "architecture_playbooks"],
    ),
    "scadastrangelove/awesome-ai-security-tools": ResourceProfile(
        summary="Curated list of AI security tools and related resources.",
        mechanics=["Aggregates security-adjacent material.", "Should be reviewed before general publication.", "Useful for model, prompt, and tool security discovery."],
        use_cases=["Find AI security references.", "Build a security research index.", "Audit tool landscapes."],
        patterns=["Pattern - Threat Detection Pipeline"],
        glossary_terms=["SIEM", "Threat Detection", "Enrichment"],
        secondary_topics=["security_siem"],
        sensitivity="security_adjacent",
        status="review_pending",
        review_reason="Security-adjacent and dual-use resource list; publish only after manual review.",
    ),
    "G-Research/siembol": ResourceProfile(
        summary="Streaming event-processing platform for security analytics and threat detection.",
        mechanics=["Processes events and applies enrichment/detection logic.", "Fits a SIEM-style security pipeline.", "Contains dual-use security-adjacent capabilities."],
        use_cases=["Threat detection and enrichment.", "Security event analytics.", "Reference security pipeline design."],
        patterns=["Pattern - Threat Detection Pipeline"],
        glossary_terms=["SIEM", "Threat Detection", "Enrichment", "Alerting"],
        secondary_topics=["security_siem", "infrastructure_observability"],
        sensitivity="security_adjacent",
        status="review_pending",
        review_reason="Security-adjacent event processing platform; route through review before publication.",
    ),
    "not-a-bank/open-banking-tracker-data": ResourceProfile(
        summary="Data project tracking open-banking providers, endpoints, or related source information.",
        mechanics=["Tracks structured finance/data sources.", "Useful for comparisons across APIs or providers.", "Bridges discovery and ingestion for external datasets."],
        use_cases=["Track open-banking sources.", "Compare API surfaces or provider metadata.", "Seed financial data catalogs."],
        patterns=["Pattern - Open Data Portal"],
        glossary_terms=["API", "Dataset", "Open Data", "Endpoint"],
        secondary_topics=["data_api_big_data", "government_civic_tech"],
    ),
    "awslabs/awsome-distributed-ai": ResourceProfile(
        summary="Curated resources focused on distributed AI systems and workflows.",
        mechanics=["Collects references around scaling or distributing AI workloads.", "Useful for architecture comparison.", "Supports search for infra-model coupling."],
        use_cases=["Study distributed AI stacks.", "Find scaling references.", "Compare orchestration layers."],
        patterns=["Pattern - Agent Orchestration"],
        glossary_terms=["Agent", "Inference", "Cloud"],
        secondary_topics=["agentic_ai_models", "infrastructure_observability"],
    ),
    "armanakbari/Awsome-Efficient-DLMs": ResourceProfile(
        summary="Curated references for efficient deep learning models and methods.",
        mechanics=["Centers on model efficiency and deployment tradeoffs.", "Useful for resource-constrained inference decisions.", "Acts as a comparative index."],
        use_cases=["Find efficient model ideas.", "Compare deployment costs.", "Study model compression or efficiency topics."],
        patterns=["Pattern - Model Inference Pipeline"],
        glossary_terms=["Inference", "LLM", "Cloud"],
        secondary_topics=["agentic_ai_models"],
    ),
    "moyu6027/awsome-chatgpt-like": ResourceProfile(
        summary="Curated references for ChatGPT-like models, clones, and adjacent systems.",
        mechanics=["Collects model and product references rather than one implementation.", "Useful for comparing chatbot architectures.", "Supports model discovery and selection."],
        use_cases=["Find chat-style model references.", "Compare conversational systems.", "Seed agent research."],
        patterns=["Pattern - Model Inference Pipeline"],
        glossary_terms=["LLM", "Prompt", "Agent"],
        secondary_topics=["agentic_ai_models"],
    ),
    "cfpb/open-source-checklist": ResourceProfile(
        summary="Checklist-oriented repository for evaluating open-source project readiness or governance.",
        mechanics=["Encodes process guidance rather than runtime code.", "Useful for project planning and review.", "Pairs well with playbook-style notes."],
        use_cases=["Audit open-source readiness.", "Guide project governance.", "Provide a policy checklist for maintainers."],
        patterns=["Pattern - Civic Tech Playbook"],
        glossary_terms=["Playbook", "Open Government", "Architecture"],
        secondary_topics=["government_civic_tech", "architecture_playbooks"],
    ),
    "alphagov/whitehall": ResourceProfile(
        summary="UK government publishing platform for structured public content and service information.",
        mechanics=["Combines publishing workflows with public-service structure.", "Useful for civic-tech and gov platform study.", "Emphasizes content, governance, and publishing models."],
        use_cases=["Study government publishing systems.", "Compare content governance workflows.", "Reference civic platform architecture."],
        patterns=["Pattern - Civic Tech Playbook"],
        glossary_terms=["Civic Tech", "Open Government", "Playbook"],
        secondary_topics=["government_civic_tech"],
    ),
    "GSA/data.gov": ResourceProfile(
        summary="Open data portal and catalog for public datasets and metadata.",
        mechanics=["Exposes public data discovery and catalog layers.", "Useful for dataset routing and metadata study.", "Anchors open-data and civic-tech workflows."],
        use_cases=["Find public datasets.", "Study data catalog design.", "Map metadata and portal flows."],
        patterns=["Pattern - Open Data Portal"],
        glossary_terms=["API", "Dataset", "Open Data", "Schema"],
        secondary_topics=["data_api_big_data", "government_civic_tech"],
    ),
    "ngageoint/geoq": ResourceProfile(
        summary="Geospatial web application for collecting and managing map-based features and data.",
        mechanics=["Combines spatial data collection with group workflows.", "Useful for geodata management and mapping tasks.", "Lives at the intersection of geospatial and civic systems."],
        use_cases=["Collect geospatial features.", "Manage map-based collaboration.", "Seed earth-data workflows."],
        patterns=["Pattern - Spatial Ingestion"],
        glossary_terms=["Geospatial Data", "GeoJSON", "STAC"],
        secondary_topics=["geospatial_earth_data", "government_civic_tech"],
    ),
    "usds/playbook": ResourceProfile(
        summary="US Digital Service playbook for digital service design and delivery guidance.",
        mechanics=["Documents service standards and delivery guidance.", "Useful for governance and architecture references.", "Acts as a process memory anchor."],
        use_cases=["Reference digital-service guidance.", "Compare policy and delivery patterns.", "Seed civic-tech notes."],
        patterns=["Pattern - Civic Tech Playbook"],
        glossary_terms=["Playbook", "Civic Tech", "Open Government"],
        secondary_topics=["government_civic_tech", "architecture_playbooks"],
    ),
    "NatLabRockies/api-umbrella": ResourceProfile(
        summary="API management and proxy layer for organizing and protecting multiple APIs.",
        mechanics=["Sits between consumers and backend APIs.", "Useful for routing, governance, and request mediation.", "Supports API portfolio management."],
        use_cases=["Centralize API access.", "Add proxy or governance layers.", "Compare API management patterns."],
        patterns=["Pattern - Open Data Portal", "Pattern - Infrastructure as Code"],
        glossary_terms=["API", "Endpoint", "Schema", "Rate Limit"],
        secondary_topics=["data_api_big_data", "infrastructure_observability"],
    ),
    "github/government.github.com": ResourceProfile(
        summary="GitHub-facing government community or directory site for public-sector open-source work.",
        mechanics=["Acts as a public navigation surface rather than a code library.", "Useful for civic-tech discovery.", "Connects government and GitHub ecosystems."],
        use_cases=["Discover public-sector GitHub activity.", "Map civic-tech communities.", "Find government repositories."],
        patterns=["Pattern - Civic Tech Playbook"],
        glossary_terms=["Civic Tech", "Open Government", "Discovery"],
        secondary_topics=["government_civic_tech"],
    ),
    "square/square.github.io": ResourceProfile(
        summary="Square's GitHub-facing site or documentation surface for open-source and engineering references.",
        mechanics=["Functions as a website or documentation presence rather than a standalone library.", "Useful for studying an organizational open-source surface.", "Acts as a routing node for company resources."],
        use_cases=["Inspect company engineering references.", "Map public open-source presence.", "Compare documentation surfaces."],
        patterns=["Pattern - Reference Architecture"],
        glossary_terms=["Reference List", "Discovery", "Architecture"],
        secondary_topics=["architecture_playbooks"],
    ),
    "twbs/bootstrap": ResourceProfile(
        summary="Responsive front-end component framework for building mobile-first interfaces.",
        mechanics=["Provides reusable layout and component primitives.", "Includes CSS, utility classes, and front-end conventions.", "Designed for broad browser compatibility and quick assembly."],
        use_cases=["Build interface shells quickly.", "Study design-system structure.", "Compare responsive layout strategies."],
        patterns=["Pattern - Component-Based UI"],
        glossary_terms=["Component Library", "Responsive Design", "CSS Reset", "DOM"],
        secondary_topics=["frontend_design_systems"],
    ),
    "animate-css/animate.css": ResourceProfile(
        summary="Cross-browser CSS animation library with reusable animation classes.",
        mechanics=["Encapsulates motion primitives as CSS classes.", "Useful for simple animation without bespoke keyframes everywhere.", "Pairs naturally with component libraries."],
        use_cases=["Add motion to UI elements.", "Study animation utility patterns.", "Pair with design-system work."],
        patterns=["Pattern - Component-Based UI"],
        glossary_terms=["Component Library", "Responsive Design"],
        secondary_topics=["frontend_design_systems"],
    ),
    "nathansmith/960-Grid-System": ResourceProfile(
        summary="Grid-system reference for layout planning and proportional front-end composition.",
        mechanics=["Encodes a layout grid rather than an application.", "Useful for studying layout proportion and structure.", "Acts as a reference for responsive systems."],
        use_cases=["Study grid systems.", "Compare layout strategies.", "Seed front-end design vocabulary."],
        patterns=["Pattern - Component-Based UI"],
        glossary_terms=["Responsive Design", "Component Library"],
        secondary_topics=["frontend_design_systems"],
    ),
    "necolas/normalize.css": ResourceProfile(
        summary="Browser-normalization stylesheet that reduces cross-browser rendering inconsistencies.",
        mechanics=["Resets or normalizes browser defaults.", "Useful as a CSS baseline before additional styling.", "Often paired with other front-end foundations."],
        use_cases=["Start a consistent style baseline.", "Compare reset strategies.", "Reduce browser-specific surprises."],
        patterns=["Pattern - Feature Detection"],
        glossary_terms=["CSS Reset", "Responsive Design"],
        secondary_topics=["frontend_design_systems"],
    ),
    "Modernizr/Modernizr": ResourceProfile(
        summary="Feature-detection library for progressive enhancement in web front ends.",
        mechanics=["Checks environment capabilities before executing a code path.", "Supports compatibility-aware front-end behavior.", "Helpful when browsers differ significantly."],
        use_cases=["Detect browser capabilities.", "Implement progressive enhancement.", "Compare compatibility strategies."],
        patterns=["Pattern - Feature Detection"],
        glossary_terms=["Feature Detection", "DOM"],
        secondary_topics=["frontend_design_systems"],
    ),
    "react/react": ResourceProfile(
        summary="Component-based UI library for building interactive interfaces.",
        mechanics=["Splits interface state into reusable components.", "Centers on declarative rendering and composition.", "Acts as a base for many front-end ecosystems."],
        use_cases=["Build interactive UI layers.", "Study component composition.", "Compare modern front-end architecture."],
        patterns=["Pattern - Component-Based UI"],
        glossary_terms=["Component Library", "DOM", "Responsive Design"],
        secondary_topics=["frontend_design_systems"],
    ),
    "simbody/simbody": ResourceProfile(
        summary="Open-source multibody dynamics simulation library for physical systems.",
        mechanics=["Models rigid or articulated bodies with numerical simulation.", "Useful for robotics, biomechanics, and vehicle dynamics.", "Emphasizes simulation correctness and physical constraints."],
        use_cases=["Simulate body dynamics.", "Study biomechanics or robotics models.", "Reference physical simulation design."],
        patterns=["Pattern - Scientific Simulation"],
        glossary_terms=["Simulation", "Scientific Simulation"],
        secondary_topics=["scientific_simulation_math"],
    ),
    "astropy/astropy": ResourceProfile(
        summary="Python astronomy toolkit for science workflows and celestial data analysis.",
        mechanics=["Provides astronomy-focused data structures and utilities.", "Useful for coordinate systems, units, and data analysis.", "Sits naturally in scientific computation workflows."],
        use_cases=["Analyze astronomical data.", "Manage units and coordinates.", "Seed scientific calculation notes."],
        patterns=["Pattern - Scientific Simulation"],
        glossary_terms=["Astronomy", "Simulation"],
        secondary_topics=["scientific_simulation_math"],
    ),
    "sympy/sympy": ResourceProfile(
        summary="Symbolic mathematics library for algebra, calculus, and expression manipulation.",
        mechanics=["Operates on symbolic expressions rather than only numbers.", "Useful for derivation, simplification, and equation solving.", "Acts as a core symbolic-computation reference."],
        use_cases=["Manipulate algebraic expressions.", "Solve symbolic problems.", "Reference computer algebra workflows."],
        patterns=["Pattern - Symbolic Computation"],
        glossary_terms=["Symbolic Mathematics"],
        secondary_topics=["scientific_simulation_math"],
    ),
    "LaurentRDC/scikit-ued": ResourceProfile(
        summary="Toolkit for ultrafast electron diffraction analysis and related scientific workflows.",
        mechanics=["Supports domain-specific scientific analysis.", "Useful for data processing and interpretation in UED.", "Sits at the edge of physics and computational analysis."],
        use_cases=["Analyze diffraction data.", "Study scientific processing pipelines.", "Expand the science catalog."],
        patterns=["Pattern - Scientific Simulation"],
        glossary_terms=["Simulation", "Scientific Computation"],
        secondary_topics=["scientific_simulation_math"],
    ),
    "gap-system/gap": ResourceProfile(
        summary="Computational discrete algebra system for group-theory and algebraic reasoning.",
        mechanics=["Supports symbolic and discrete algebra calculations.", "Useful for mathematically structured workflows.", "Acts as a reference for formal computational systems."],
        use_cases=["Study algebraic systems.", "Reference formal math tooling.", "Map symbolic computation resources."],
        patterns=["Pattern - Symbolic Computation"],
        glossary_terms=["Symbolic Mathematics"],
        secondary_topics=["scientific_simulation_math"],
    ),
    "markusschanta/awesome-jupyter": ResourceProfile(
        summary="Curated Jupyter ecosystem index for notebooks, extensions, and related tooling.",
        mechanics=["Curates notebook-oriented resources.", "Useful for exploring interactive scientific workflows.", "Acts as a discovery index rather than implementation code."],
        use_cases=["Discover Jupyter tools.", "Compare notebook extensions.", "Seed scientific workflow references."],
        patterns=["Pattern - Curated Resource Curation"],
        glossary_terms=["Curation", "Discovery"],
        secondary_topics=["scientific_simulation_math", "curated_lists"],
    ),
    "asreview/asreview": ResourceProfile(
        summary="Active-learning toolkit for systematic reviews and screening workflows.",
        mechanics=["Uses human-in-the-loop review to prioritize samples.", "Useful for research review and triage.", "Connects scientific methods with machine-assisted screening."],
        use_cases=["Manage systematic reviews.", "Study active-learning workflows.", "Build review queues for research tasks."],
        patterns=["Pattern - Scientific Simulation"],
        glossary_terms=["Active Learning", "Review Workflow"],
        secondary_topics=["scientific_simulation_math"],
    ),
}


def generic_profile(repo_key: str, topic: TopicSpec) -> ResourceProfile:
    owner, repo = split_repo_key(repo_key)
    title_hint = repo.replace("-", " ").replace("_", " ")
    summary = f"{note_title_for_repo(owner, repo)} is a {topic.title.lower()} resource that can support {topic.canonical_vocabulary[0].lower()} work."
    return ResourceProfile(
        summary=summary,
        mechanics=list(topic.mechanics),
        use_cases=list(topic.use_cases),
        patterns=[f"Pattern - {PATTERN_TITLE_BY_KEY[key]}" for key in topic.patterns if key in PATTERN_TITLE_BY_KEY],
        glossary_terms=list(topic.glossary_terms),
        secondary_topics=list(topic.overlaps),
    )


PATTERN_TITLE_BY_KEY = {pattern.key: pattern.title for pattern in PATTERNS}
GLOSSARY_BY_KEY = {term.key: term for term in GLOSSARY}
GLOSSARY_BY_WORD = {term.word.lower(): term for term in GLOSSARY}
TOPIC_BY_KEY = {topic.key: topic for topic in TOPICS}

DOMAIN_PRIMARY_BY_TOPIC_KEY = {
    "curated_lists": "Discovery",
    "agentic_ai_models": "Agentic_AI",
    "data_api_big_data": "Data",
    "geospatial_earth_data": "Geospatial",
    "infrastructure_observability": "Infrastructure",
    "security_siem": "Security",
    "frontend_design_systems": "Frontend",
    "scientific_simulation_math": "Scientific_Computation",
    "government_civic_tech": "Civic_Tech",
    "cad_saas_design": "CAD_SaaS",
    "architecture_playbooks": "Architecture",
}

MATURITY_STAGE_BY_TOPIC_KEY = {
    "curated_lists": "Reference",
    "agentic_ai_models": "Active",
    "data_api_big_data": "Active",
    "geospatial_earth_data": "Active",
    "infrastructure_observability": "Production_Ready",
    "security_siem": "Incubating",
    "frontend_design_systems": "Production_Ready",
    "scientific_simulation_math": "Production_Ready",
    "government_civic_tech": "Active",
    "cad_saas_design": "Exploratory",
    "architecture_playbooks": "Reference",
}

DEPLOYMENT_TARGET_BY_TOPIC_KEY = {
    "curated_lists": "Local_Only",
    "agentic_ai_models": "Local_Only",
    "data_api_big_data": "Server",
    "geospatial_earth_data": "Server",
    "infrastructure_observability": "Server",
    "security_siem": "Server",
    "frontend_design_systems": "Browser",
    "scientific_simulation_math": "Local_Only",
    "government_civic_tech": "Server",
    "cad_saas_design": "Browser",
    "architecture_playbooks": "Local_Only",
}

INTERFACE_PROTOCOL_BY_TOPIC_KEY = {
    "curated_lists": "Markdown",
    "agentic_ai_models": "Python_SDK",
    "data_api_big_data": "REST",
    "geospatial_earth_data": "REST",
    "infrastructure_observability": "CLI",
    "security_siem": "CLI",
    "frontend_design_systems": "Web_UI",
    "scientific_simulation_math": "Python_SDK",
    "government_civic_tech": "Web_UI",
    "cad_saas_design": "Web_UI",
    "architecture_playbooks": "Markdown",
}

DATA_LOCALITY_BY_TOPIC_KEY = {
    "curated_lists": "Stateless",
    "agentic_ai_models": "Local_First",
    "data_api_big_data": "Distributed",
    "geospatial_earth_data": "Distributed",
    "infrastructure_observability": "Distributed",
    "security_siem": "Distributed",
    "frontend_design_systems": "Stateless",
    "scientific_simulation_math": "Local_First",
    "government_civic_tech": "Distributed",
    "cad_saas_design": "Stateless",
    "architecture_playbooks": "Stateless",
}

HARDWARE_FOOTPRINT_BY_TOPIC_KEY = {
    "curated_lists": "CPU_Only",
    "agentic_ai_models": "Low_VRAM",
    "data_api_big_data": "High_Memory",
    "geospatial_earth_data": "High_Memory",
    "infrastructure_observability": "CPU_Only",
    "security_siem": "CPU_Only",
    "frontend_design_systems": "Browser_Only",
    "scientific_simulation_math": "CPU_Only",
    "government_civic_tech": "CPU_Only",
    "cad_saas_design": "Browser_Only",
    "architecture_playbooks": "CPU_Only",
}

SECURITY_COMPLIANCE_BY_TOPIC_KEY = {
    "curated_lists": "Uncertified",
    "agentic_ai_models": "Uncertified",
    "data_api_big_data": "Uncertified",
    "geospatial_earth_data": "Uncertified",
    "infrastructure_observability": "Uncertified",
    "security_siem": "Security_Adjacent",
    "frontend_design_systems": "Uncertified",
    "scientific_simulation_math": "Uncertified",
    "government_civic_tech": "Uncertified",
    "cad_saas_design": "Uncertified",
    "architecture_playbooks": "Uncertified",
}

TAXONOMY_DIMENSIONS = [
    "ecosystem",
    "domain_primary",
    "maturity_stage",
    "license_class",
    "deployment_target",
    "interface_protocol",
    "data_locality",
    "hardware_footprint",
    "security_compliance",
]


def infer_ecosystem(repo_key: str, topic: TopicSpec, profile: ResourceProfile) -> str:
    lower = " ".join([repo_key, profile.summary, *profile.mechanics, *profile.use_cases]).lower()
    if topic.key == "curated_lists":
        return "Markdown"
    if topic.key == "agentic_ai_models":
        if any(token in lower for token in ["voice", "tts", "stt", "audio"]):
            return "Audio_AI"
        if any(token in lower for token in ["video", "multimodal"]):
            return "Multimodal_AI"
        if any(token in lower for token in ["semantic-kernel", "skill", "agent"]):
            return "Agent_Framework"
        return "Model_Serving"
    if topic.key == "data_api_big_data":
        if any(token in lower for token in ["portal", "dataset", "api", "tracker"]):
            return "Data_Platform"
        return "Data_Engineering"
    if topic.key == "geospatial_earth_data":
        if any(token in lower for token in ["stac", "geojson", "satellite", "landsat", "modis"]):
            return "Geo_Data"
        return "Geospatial"
    if topic.key == "infrastructure_observability":
        if any(token in lower for token in ["terraform", "puppet", "chef"]):
            return "Infrastructure_Automation"
        if any(token in lower for token in ["prometheus", "netdata", "sentry", "statsd"]):
            return "Observability"
        return "Cloud_Native"
    if topic.key == "security_siem":
        return "Security_Tools"
    if topic.key == "frontend_design_systems":
        if "react" in lower:
            return "React"
        if any(token in lower for token in ["bootstrap", "normalize", "animate", "modernizr"]):
            return "Web_CSS"
        return "Web_Frontend"
    if topic.key == "scientific_simulation_math":
        if any(token in lower for token in ["sympy", "gap"]):
            return "Symbolic_Computation"
        if any(token in lower for token in ["simbody", "astropy"]):
            return "Scientific_Python"
        return "Scientific_Computation"
    if topic.key == "government_civic_tech":
        return "Public_Sector"
    if topic.key == "cad_saas_design":
        return "Product_Design"
    if topic.key == "architecture_playbooks":
        return "Documentation"
    return "Mixed"


def infer_taxonomy_fields(repo_key: str, topic: TopicSpec, profile: ResourceProfile) -> dict[str, str]:
    return {
        "ecosystem": profile.ecosystem or infer_ecosystem(repo_key, topic, profile),
        "domain_primary": profile.domain_primary or DOMAIN_PRIMARY_BY_TOPIC_KEY.get(topic.key, "Mixed"),
        "maturity_stage": profile.maturity_stage or MATURITY_STAGE_BY_TOPIC_KEY.get(topic.key, "Active"),
        "license_class": profile.license_class or "Unknown",
        "deployment_target": profile.deployment_target or DEPLOYMENT_TARGET_BY_TOPIC_KEY.get(topic.key, "Server"),
        "interface_protocol": profile.interface_protocol or INTERFACE_PROTOCOL_BY_TOPIC_KEY.get(topic.key, "Unknown"),
        "data_locality": profile.data_locality or DATA_LOCALITY_BY_TOPIC_KEY.get(topic.key, "Distributed"),
        "hardware_footprint": profile.hardware_footprint or HARDWARE_FOOTPRINT_BY_TOPIC_KEY.get(topic.key, "CPU_Only"),
        "security_compliance": profile.security_compliance or SECURITY_COMPLIANCE_BY_TOPIC_KEY.get(topic.key, "Uncertified"),
    }


def resolve_glossary_spec(identifier: str) -> GlossarySpec:
    lowered = identifier.lower().strip()
    if lowered in GLOSSARY_BY_KEY:
        return GLOSSARY_BY_KEY[lowered]
    if lowered in GLOSSARY_BY_WORD:
        return GLOSSARY_BY_WORD[lowered]
    for term in GLOSSARY:
        aliases = [term.key.lower(), term.word.lower(), *(alias.lower() for alias in term.aliases)]
        if lowered in aliases:
            return term
    raise KeyError(identifier)


def resolve_glossary_record(identifier: str, glossary_lookup: dict[str, GlossaryRecord]) -> GlossaryRecord:
    lowered = identifier.lower().strip()
    if lowered in glossary_lookup:
        return glossary_lookup[lowered]
    spec = resolve_glossary_spec(identifier)
    if spec.key in glossary_lookup:
        return glossary_lookup[spec.key]
    if spec.word.lower() in glossary_lookup:
        return glossary_lookup[spec.word.lower()]
    raise KeyError(identifier)


def maybe_resolve_glossary_record(identifier: str, glossary_lookup: dict[str, GlossaryRecord]) -> GlossaryRecord | None:
    try:
        return resolve_glossary_record(identifier, glossary_lookup)
    except KeyError:
        return None


def glossary_words_from_identifiers(identifiers: Iterable[str], exclude_key: str | None = None) -> list[str]:
    words: list[str] = []
    for identifier in identifiers:
        if not identifier:
            continue
        if exclude_key and identifier.lower() == exclude_key.lower():
            continue
        try:
            spec = resolve_glossary_spec(identifier)
        except KeyError:
            continue
        if spec.word not in words:
            words.append(spec.word)
    return words


def classify_resource(repo_key: str) -> tuple[TopicSpec, ResourceProfile]:
    lower = repo_key.lower()
    if repo_key in RESOURCE_HINTS:
        profile = RESOURCE_HINTS[repo_key]
        topic = infer_topic_for_repo(repo_key, profile.secondary_topics or [])
        return topic, profile
    topic = infer_topic_for_repo(repo_key, [])
    return topic, generic_profile(repo_key, topic)


def infer_topic_for_repo(repo_key: str, secondary_topics: list[str]) -> TopicSpec:
    lower = repo_key.lower()
    # strongest signals first
    if any(token in lower for token in ["semantic-kernel", "chatgpt-like", "efficient-dlms", "distributed-ai", "tts", "stt", "voice", "model", "llm", "skills"]):
        return TOPIC_BY_KEY["agentic_ai_models"]
    if any(token in lower for token in ["awesome", "generated-awesomeness", "project-ideas", "annotated", "checklist"]):
        return TOPIC_BY_KEY["curated_lists"]
    if any(token in lower for token in ["terraform", "puppet", "chef", "openstack", "prometheus", "statsd", "netdata", "sentry", "api-umbrella"]):
        return TOPIC_BY_KEY["infrastructure_observability"]
    if any(token in lower for token in ["siembol", "security", "threat", "ai-security"]):
        return TOPIC_BY_KEY["security_siem"]
    if any(token in lower for token in ["bootstrap", "animate", "normalize", "modernizr", "react", "grid"]):
        return TOPIC_BY_KEY["frontend_design_systems"]
    if any(token in lower for token in ["simbody", "astropy", "sympy", "scikit-ued", "gap-system", "asreview"]):
        return TOPIC_BY_KEY["scientific_simulation_math"]
    if any(token in lower for token in ["whitehall", "usds", "cfpb", "government", "data.gov", "open-source-checklist", "playbook"]):
        return TOPIC_BY_KEY["government_civic_tech"]
    if any(token in lower for token in ["geoq", "geo", "satellite", "landsat", "modis", "netcdf", "hdf5", "stac", "geojson"]):
        return TOPIC_BY_KEY["geospatial_earth_data"]
    if any(token in lower for token in ["cad", "saas", "design"]):
        return TOPIC_BY_KEY["cad_saas_design"]
    if any(token in lower for token in ["api", "data", "dataset", "portal", "tracker"]):
        return TOPIC_BY_KEY["data_api_big_data"]
    return TOPIC_BY_KEY["architecture_playbooks"]


class ResourceRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    uuid: str
    canonical_url: str
    repo_key: str
    owner: str
    repo_name: str
    display_name: str
    note_path: str
    review_path: str | None = None
    archetype: str
    primary_topic_key: str
    secondary_topic_keys: list[str] = Field(default_factory=list)
    patterns: list[str] = Field(default_factory=list)
    glossary_terms: list[str] = Field(default_factory=list)
    aliases: list[str] = Field(default_factory=list)
    summary: str
    mechanics: list[str] = Field(default_factory=list)
    use_cases: list[str] = Field(default_factory=list)
    maturity: str = "seed"
    sensitivity: str = "normal"
    status: str = "published"
    license: str = "unknown"
    ecosystem: str = "Mixed"
    domain_primary: str = "Mixed"
    maturity_stage: str = "Active"
    license_class: str = "Unknown"
    deployment_target: str = "Server"
    interface_protocol: str = "Unknown"
    data_locality: str = "Distributed"
    hardware_footprint: str = "CPU_Only"
    security_compliance: str = "Uncertified"
    source_file: str = ""
    created_at: str = ""
    updated_at: str = ""
    review_reason: str | None = None


class IndexRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    uuid: str
    index_key: str
    kind: str
    title: str
    description: str
    parent_uuid: str | None
    note_path: str
    canvas_path: str | None
    canonical_vocabulary: list[str] = Field(default_factory=list)
    inclusion_criteria: str
    summary: str
    sort_order: int = 0
    created_at: str = ""
    updated_at: str = ""


class PatternRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    uuid: str
    pattern_key: str
    title: str
    definition: str
    aliases: list[str] = Field(default_factory=list)
    examples: list[str] = Field(default_factory=list)
    glossary_terms: list[str] = Field(default_factory=list)
    topic_keys: list[str] = Field(default_factory=list)
    note_path: str
    summary: str
    status: str = "active"
    created_at: str = ""
    updated_at: str = ""


class GlossaryRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    uuid: str
    term_key: str
    canonical_word: str
    sense_label: str
    definition: str
    aliases: list[str] = Field(default_factory=list)
    related_terms: list[str] = Field(default_factory=list)
    topic_keys: list[str] = Field(default_factory=list)
    note_path: str
    summary: str
    status: str = "active"
    created_at: str = ""
    updated_at: str = ""


class EdgeRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    source_uuid: str
    target_uuid: str
    source_kind: str
    target_kind: str
    relationship_type: str
    confidence: float
    provenance: str
    note: str


class OccurrenceRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    term_uuid: str
    resource_uuid: str
    note_path: str
    observed_context: str
    source_location: str
    term_role: str
    sense_label: str
    confidence: float
    provenance: str


class TaxonomyRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    uuid: str
    resource_uuid: str
    note_path: str
    ecosystem: str
    domain_primary: str
    maturity_stage: str
    license_class: str
    deployment_target: str
    interface_protocol: str
    data_locality: str
    hardware_footprint: str
    security_compliance: str
    summary: str
    source_file: str = ""
    created_at: str = ""
    updated_at: str = ""


def init_dirs() -> None:
    for path in [
        INDEX_DIR,
        RESOURCE_DIR,
        GLOSSARY_DIR,
        PATTERN_DIR,
        REVIEW_DIR,
        CANVAS_DIR,
        TOPIC_CANVAS_DIR,
        LOG_DIR,
        STAGING_DIR,
        REVIEW_QUEUE_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        PRAGMA journal_mode=WAL;

        CREATE TABLE IF NOT EXISTS indexes (
            uuid TEXT PRIMARY KEY,
            index_key TEXT UNIQUE NOT NULL,
            kind TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            parent_uuid TEXT,
            note_path TEXT NOT NULL,
            canvas_path TEXT,
            canonical_vocabulary TEXT NOT NULL,
            inclusion_criteria TEXT NOT NULL,
            summary TEXT NOT NULL,
            sort_order INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS resources (
            uuid TEXT PRIMARY KEY,
            canonical_url TEXT UNIQUE NOT NULL,
            repo_key TEXT UNIQUE NOT NULL,
            owner TEXT NOT NULL,
            repo_name TEXT NOT NULL,
            display_name TEXT NOT NULL,
            note_path TEXT NOT NULL,
            review_path TEXT,
            archetype TEXT NOT NULL,
            primary_topic_key TEXT NOT NULL,
            secondary_topic_keys TEXT NOT NULL,
            patterns TEXT NOT NULL,
            glossary_terms TEXT NOT NULL,
            aliases TEXT NOT NULL,
            summary TEXT NOT NULL,
            mechanics TEXT NOT NULL,
            use_cases TEXT NOT NULL,
            maturity TEXT NOT NULL,
            sensitivity TEXT NOT NULL,
            status TEXT NOT NULL,
            license TEXT NOT NULL,
            source_file TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            review_reason TEXT
        );

        CREATE TABLE IF NOT EXISTS taxonomy (
            uuid TEXT PRIMARY KEY,
            resource_uuid TEXT UNIQUE NOT NULL,
            note_path TEXT NOT NULL,
            ecosystem TEXT NOT NULL,
            domain_primary TEXT NOT NULL,
            maturity_stage TEXT NOT NULL,
            license_class TEXT NOT NULL,
            deployment_target TEXT NOT NULL,
            interface_protocol TEXT NOT NULL,
            data_locality TEXT NOT NULL,
            hardware_footprint TEXT NOT NULL,
            security_compliance TEXT NOT NULL,
            summary TEXT NOT NULL,
            source_file TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS aliases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_uuid TEXT NOT NULL,
            alias TEXT NOT NULL,
            alias_type TEXT NOT NULL,
            UNIQUE(resource_uuid, alias, alias_type)
        );

        CREATE TABLE IF NOT EXISTS index_memberships (
            index_uuid TEXT NOT NULL,
            resource_uuid TEXT NOT NULL,
            membership_role TEXT NOT NULL,
            confidence REAL NOT NULL,
            provenance TEXT NOT NULL,
            UNIQUE(index_uuid, resource_uuid, membership_role)
        );

        CREATE TABLE IF NOT EXISTS patterns (
            uuid TEXT PRIMARY KEY,
            pattern_key TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            definition TEXT NOT NULL,
            aliases TEXT NOT NULL,
            examples TEXT NOT NULL,
            glossary_terms TEXT NOT NULL,
            topic_keys TEXT NOT NULL,
            note_path TEXT NOT NULL,
            summary TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS glossary_terms (
            uuid TEXT PRIMARY KEY,
            term_key TEXT UNIQUE NOT NULL,
            canonical_word TEXT NOT NULL,
            sense_label TEXT NOT NULL,
            definition TEXT NOT NULL,
            aliases TEXT NOT NULL,
            related_terms TEXT NOT NULL,
            topic_keys TEXT NOT NULL,
            note_path TEXT NOT NULL,
            summary TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS term_occurrences (
            id TEXT PRIMARY KEY,
            term_uuid TEXT NOT NULL,
            resource_uuid TEXT NOT NULL,
            note_path TEXT NOT NULL,
            observed_context TEXT NOT NULL,
            source_location TEXT NOT NULL,
            term_role TEXT NOT NULL,
            sense_label TEXT NOT NULL,
            confidence REAL NOT NULL,
            provenance TEXT NOT NULL,
            UNIQUE(term_uuid, resource_uuid, source_location, term_role)
        );

        CREATE TABLE IF NOT EXISTS term_relations (
            id TEXT PRIMARY KEY,
            source_term_uuid TEXT NOT NULL,
            target_term_uuid TEXT NOT NULL,
            relationship_type TEXT NOT NULL,
            confidence REAL NOT NULL,
            provenance TEXT NOT NULL,
            UNIQUE(source_term_uuid, target_term_uuid, relationship_type)
        );

        CREATE TABLE IF NOT EXISTS evidence_snippets (
            id TEXT PRIMARY KEY,
            resource_uuid TEXT NOT NULL,
            source_kind TEXT NOT NULL,
            source_ref TEXT NOT NULL,
            snippet TEXT NOT NULL,
            confidence REAL NOT NULL,
            provenance TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS edges (
            id TEXT PRIMARY KEY,
            source_uuid TEXT NOT NULL,
            target_uuid TEXT NOT NULL,
            source_kind TEXT NOT NULL,
            target_kind TEXT NOT NULL,
            relationship_type TEXT NOT NULL,
            confidence REAL NOT NULL,
            provenance TEXT NOT NULL,
            note TEXT NOT NULL,
            UNIQUE(source_uuid, target_uuid, relationship_type, provenance)
        );

        CREATE TABLE IF NOT EXISTS review_queue (
            id TEXT PRIMARY KEY,
            resource_uuid TEXT NOT NULL,
            reason TEXT NOT NULL,
            note_path TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS ingestion_runs (
            id TEXT PRIMARY KEY,
            run_key TEXT UNIQUE NOT NULL,
            source_file TEXT NOT NULL,
            created_at TEXT NOT NULL,
            resource_count INTEGER NOT NULL,
            taxonomy_count INTEGER NOT NULL,
            glossary_count INTEGER NOT NULL,
            pattern_count INTEGER NOT NULL,
            edge_count INTEGER NOT NULL,
            note_count INTEGER NOT NULL,
            canvas_count INTEGER NOT NULL,
            summary TEXT NOT NULL
        );
        """
    )
    conn.commit()


def upsert_index(conn: sqlite3.Connection, record: IndexRecord) -> None:
    conn.execute(
        """
        INSERT INTO indexes (
            uuid, index_key, kind, title, description, parent_uuid,
            note_path, canvas_path, canonical_vocabulary, inclusion_criteria,
            summary, sort_order, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(index_key) DO UPDATE SET
            uuid=excluded.uuid,
            kind=excluded.kind,
            title=excluded.title,
            description=excluded.description,
            parent_uuid=excluded.parent_uuid,
            note_path=excluded.note_path,
            canvas_path=excluded.canvas_path,
            canonical_vocabulary=excluded.canonical_vocabulary,
            inclusion_criteria=excluded.inclusion_criteria,
            summary=excluded.summary,
            sort_order=excluded.sort_order,
            created_at=excluded.created_at,
            updated_at=excluded.updated_at
        """,
        (
            record.uuid,
            record.index_key,
            record.kind,
            record.title,
            record.description,
            record.parent_uuid,
            record.note_path,
            record.canvas_path,
            jsonish(record.canonical_vocabulary),
            record.inclusion_criteria,
            record.summary,
            record.sort_order,
            record.created_at,
            record.updated_at,
        ),
    )


def upsert_resource(conn: sqlite3.Connection, record: ResourceRecord) -> None:
    conn.execute(
        """
        INSERT INTO resources (
            uuid, canonical_url, repo_key, owner, repo_name, display_name,
            note_path, review_path, archetype, primary_topic_key,
            secondary_topic_keys, patterns, glossary_terms, aliases, summary,
            mechanics, use_cases, maturity, sensitivity, status, license,
            source_file, created_at, updated_at, review_reason
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(repo_key) DO UPDATE SET
            uuid=excluded.uuid,
            canonical_url=excluded.canonical_url,
            owner=excluded.owner,
            repo_name=excluded.repo_name,
            display_name=excluded.display_name,
            note_path=excluded.note_path,
            review_path=excluded.review_path,
            archetype=excluded.archetype,
            primary_topic_key=excluded.primary_topic_key,
            secondary_topic_keys=excluded.secondary_topic_keys,
            patterns=excluded.patterns,
            glossary_terms=excluded.glossary_terms,
            aliases=excluded.aliases,
            summary=excluded.summary,
            mechanics=excluded.mechanics,
            use_cases=excluded.use_cases,
            maturity=excluded.maturity,
            sensitivity=excluded.sensitivity,
            status=excluded.status,
            license=excluded.license,
            source_file=excluded.source_file,
            created_at=excluded.created_at,
            updated_at=excluded.updated_at,
            review_reason=excluded.review_reason
        """,
        (
            record.uuid,
            record.canonical_url,
            record.repo_key,
            record.owner,
            record.repo_name,
            record.display_name,
            record.note_path,
            record.review_path,
            record.archetype,
            record.primary_topic_key,
            jsonish(record.secondary_topic_keys),
            jsonish(record.patterns),
            jsonish(record.glossary_terms),
            jsonish(record.aliases),
            record.summary,
            jsonish(record.mechanics),
            jsonish(record.use_cases),
            record.maturity,
            record.sensitivity,
            record.status,
            record.license,
            record.source_file,
            record.created_at,
            record.updated_at,
            record.review_reason,
        ),
    )


def upsert_pattern(conn: sqlite3.Connection, record: PatternRecord) -> None:
    conn.execute(
        """
        INSERT INTO patterns (
            uuid, pattern_key, title, definition, aliases, examples,
            glossary_terms, topic_keys, note_path, summary, status,
            created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(pattern_key) DO UPDATE SET
            uuid=excluded.uuid,
            title=excluded.title,
            definition=excluded.definition,
            aliases=excluded.aliases,
            examples=excluded.examples,
            glossary_terms=excluded.glossary_terms,
            topic_keys=excluded.topic_keys,
            note_path=excluded.note_path,
            summary=excluded.summary,
            status=excluded.status,
            created_at=excluded.created_at,
            updated_at=excluded.updated_at
        """,
        (
            record.uuid,
            record.pattern_key,
            record.title,
            record.definition,
            jsonish(record.aliases),
            jsonish(record.examples),
            jsonish(record.glossary_terms),
            jsonish(record.topic_keys),
            record.note_path,
            record.summary,
            record.status,
            record.created_at,
            record.updated_at,
        ),
    )


def upsert_glossary(conn: sqlite3.Connection, record: GlossaryRecord) -> None:
    conn.execute(
        """
        INSERT INTO glossary_terms (
            uuid, term_key, canonical_word, sense_label, definition, aliases,
            related_terms, topic_keys, note_path, summary, status,
            created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(term_key) DO UPDATE SET
            uuid=excluded.uuid,
            canonical_word=excluded.canonical_word,
            sense_label=excluded.sense_label,
            definition=excluded.definition,
            aliases=excluded.aliases,
            related_terms=excluded.related_terms,
            topic_keys=excluded.topic_keys,
            note_path=excluded.note_path,
            summary=excluded.summary,
            status=excluded.status,
            created_at=excluded.created_at,
            updated_at=excluded.updated_at
        """,
        (
            record.uuid,
            record.term_key,
            record.canonical_word,
            record.sense_label,
            record.definition,
            jsonish(record.aliases),
            jsonish(record.related_terms),
            jsonish(record.topic_keys),
            record.note_path,
            record.summary,
            record.status,
            record.created_at,
            record.updated_at,
        ),
    )


def upsert_taxonomy(conn: sqlite3.Connection, record: TaxonomyRecord) -> None:
    conn.execute(
        """
        INSERT INTO taxonomy (
            uuid, resource_uuid, note_path, ecosystem, domain_primary,
            maturity_stage, license_class, deployment_target, interface_protocol,
            data_locality, hardware_footprint, security_compliance, summary,
            source_file, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(resource_uuid) DO UPDATE SET
            uuid=excluded.uuid,
            note_path=excluded.note_path,
            ecosystem=excluded.ecosystem,
            domain_primary=excluded.domain_primary,
            maturity_stage=excluded.maturity_stage,
            license_class=excluded.license_class,
            deployment_target=excluded.deployment_target,
            interface_protocol=excluded.interface_protocol,
            data_locality=excluded.data_locality,
            hardware_footprint=excluded.hardware_footprint,
            security_compliance=excluded.security_compliance,
            summary=excluded.summary,
            source_file=excluded.source_file,
            created_at=excluded.created_at,
            updated_at=excluded.updated_at
        """,
        (
            record.uuid,
            record.resource_uuid,
            record.note_path,
            record.ecosystem,
            record.domain_primary,
            record.maturity_stage,
            record.license_class,
            record.deployment_target,
            record.interface_protocol,
            record.data_locality,
            record.hardware_footprint,
            record.security_compliance,
            record.summary,
            record.source_file,
            record.created_at,
            record.updated_at,
        ),
    )


def insert_aliases(conn: sqlite3.Connection, resource_uuid: str, aliases: list[str]) -> None:
    for alias in aliases:
        conn.execute(
            """
            INSERT OR IGNORE INTO aliases (resource_uuid, alias, alias_type)
            VALUES (?, ?, ?)
            """,
            (resource_uuid, alias, "canonical_alias"),
        )


def insert_membership(conn: sqlite3.Connection, index_uuid: str, resource_uuid: str, role: str, confidence: float, provenance: str) -> None:
    conn.execute(
        """
        INSERT OR IGNORE INTO index_memberships (index_uuid, resource_uuid, membership_role, confidence, provenance)
        VALUES (?, ?, ?, ?, ?)
        """,
        (index_uuid, resource_uuid, role, confidence, provenance),
    )


def insert_edge(conn: sqlite3.Connection, record: EdgeRecord) -> None:
    conn.execute(
        """
        INSERT OR IGNORE INTO edges (
            id, source_uuid, target_uuid, source_kind, target_kind,
            relationship_type, confidence, provenance, note
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            record.id,
            record.source_uuid,
            record.target_uuid,
            record.source_kind,
            record.target_kind,
            record.relationship_type,
            record.confidence,
            record.provenance,
            record.note,
        ),
    )


def insert_occurrence(conn: sqlite3.Connection, record: OccurrenceRecord) -> None:
    conn.execute(
        """
        INSERT OR IGNORE INTO term_occurrences (
            id, term_uuid, resource_uuid, note_path, observed_context,
            source_location, term_role, sense_label, confidence, provenance
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            record.id,
            record.term_uuid,
            record.resource_uuid,
            record.note_path,
            record.observed_context,
            record.source_location,
            record.term_role,
            record.sense_label,
            record.confidence,
            record.provenance,
        ),
    )


def insert_evidence_snippet(conn: sqlite3.Connection, resource_uuid: str, snippet: EvidenceSnippetCandidate, source_ref: str | None = None) -> None:
    source_ref = source_ref or snippet.source_ref
    conn.execute(
        """
        INSERT OR IGNORE INTO evidence_snippets (
            id, resource_uuid, source_kind, source_ref, snippet, confidence, provenance
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            entity_uuid("evidence", f"{resource_uuid}::{snippet.source_kind}::{source_ref}::{snippet.snippet[:80]}"),
            resource_uuid,
            snippet.source_kind,
            source_ref,
            snippet.snippet,
            snippet.confidence,
            "lmstudio_enrichment",
        ),
    )


def insert_review(conn: sqlite3.Connection, resource_uuid: str, reason: str, note_path: str) -> None:
    conn.execute(
        """
        INSERT OR IGNORE INTO review_queue (id, resource_uuid, reason, note_path, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (entity_uuid("review", resource_uuid), resource_uuid, reason, note_path, "pending", now_iso()),
    )


def build_master_index_record() -> IndexRecord:
    now = now_iso()
    return IndexRecord(
        uuid=entity_uuid("index", "master"),
        index_key="master",
        kind="master",
        title="Master Index",
        description="Root router for the solutions library vault.",
        parent_uuid=None,
        note_path=(INDEX_DIR / "Master Index.md").relative_to(VAULT_ROOT).as_posix(),
        canvas_path=(CANVAS_DIR / "Library Map.canvas").relative_to(VAULT_ROOT).as_posix(),
        canonical_vocabulary=["taxonomy", "topic index", "glossary", "patterns", "review queue"],
        inclusion_criteria="Routes only to topic sub-indexes and other hub notes.",
        summary="Root router for the solutions library vault.",
        sort_order=0,
        created_at=now,
        updated_at=now,
    )


def build_topic_index_records(master_uuid: str) -> list[IndexRecord]:
    records = []
    now = now_iso()
    for idx, topic in enumerate(TOPICS, start=1):
        records.append(
            IndexRecord(
                uuid=entity_uuid("index", topic.key),
                index_key=topic.key,
                kind="topic",
                title=f"Topic - {topic.title}",
                description=topic.description,
                parent_uuid=master_uuid,
                note_path=(INDEX_DIR / f"Topic - {topic.title}.md").relative_to(VAULT_ROOT).as_posix(),
                canvas_path=(TOPIC_CANVAS_DIR / f"Topic - {topic.title}.canvas").relative_to(VAULT_ROOT).as_posix(),
                canonical_vocabulary=topic.canonical_vocabulary,
                inclusion_criteria=topic.inclusion_criteria,
                summary=topic.description,
                sort_order=idx,
                created_at=now,
                updated_at=now,
            )
        )
    return records


def build_hub_index_records(master_uuid: str) -> list[IndexRecord]:
    now = now_iso()
    hubs = [
        ("taxonomy_hub", "Taxonomy Index", "Cross-cutting layer for controlled resource facets and cross-analysis."),
        ("glossary_hub", "Glossary Index", "Parallel glossary layer for canonical definitions and observed contexts."),
        ("pattern_hub", "Pattern Index", "Cross-cutting layer for reusable architectural patterns."),
        ("review_hub", "Review Queue", "Quarantine layer for resources that require manual review before publication."),
    ]
    records = []
    for order, (key, title, description) in enumerate(hubs, start=100):
        note_lookup = {
            "taxonomy_hub": INDEX_DIR / "Taxonomy Index.md",
            "glossary_hub": GLOSSARY_DIR / "Glossary Index.md",
            "pattern_hub": PATTERN_DIR / "Pattern Index.md",
            "review_hub": REVIEW_DIR / "Review Queue.md",
        }
        records.append(
            IndexRecord(
                uuid=entity_uuid("index", key),
                index_key=key,
                kind=key,
                title=title,
                description=description,
                parent_uuid=master_uuid,
                note_path=note_lookup[key].relative_to(VAULT_ROOT).as_posix(),
                canvas_path=None,
                canonical_vocabulary=[title.lower()],
                inclusion_criteria=description,
                summary=description,
                sort_order=order,
                created_at=now,
                updated_at=now,
            )
        )
    return records


def resource_title_and_path(repo_key: str, status: str) -> tuple[str, Path]:
    owner, repo = split_repo_key(repo_key)
    title = note_title_for_repo(owner, repo)
    filename = sanitize_filename(f"{title}.md")
    folder = REVIEW_DIR if status == "review_pending" else RESOURCE_DIR
    return title, folder / filename


def build_resource_record(
    repo_url: str,
    source_file: str,
    runtime: LMStudioRuntime | None = None,
    github_runtime: GitHubRuntime | None = None,
) -> tuple[ResourceRecord, TopicSpec, ResourceProfile, list[EvidenceSnippetCandidate], GitHubRepositoryMetadata | None]:
    canonical_url = normalize_repo_url(repo_url)
    if not canonical_url:
        raise ValueError(f"Unsupported repository URL: {repo_url}")
    repo_key = repo_key_from_url(canonical_url)
    owner, repo = split_repo_key(repo_key)
    topic, heuristic_profile = classify_resource(repo_key)
    runtime = runtime or load_lmstudio_runtime()
    github_runtime = github_runtime or load_github_runtime()
    github_metadata = fetch_github_metadata(github_runtime, repo_key)
    context = build_repository_context(repo_key, canonical_url, source_file, topic, heuristic_profile, github_metadata)
    enrichment = run_lmstudio_enrichment(runtime, context, topic, heuristic_profile)
    profile, license_name = merge_resource_profile(topic, heuristic_profile, github_metadata, enrichment.scout, enrichment.chart, enrichment.metadata, enrichment.entities)
    if enrichment.scout and enrichment.scout.primary_topic_key in TOPIC_BY_KEY and enrichment.scout.confidence >= 0.5:
        topic = TOPIC_BY_KEY[enrichment.scout.primary_topic_key]
    display_name, note_file = resource_title_and_path(repo_key, profile.status)
    secondary_topics = list(dict.fromkeys(profile.secondary_topics))
    primary_topic_key = topic.key
    if primary_topic_key in secondary_topics:
        secondary_topics.remove(primary_topic_key)
    patterns = [pattern if pattern.startswith("Pattern -") else f"Pattern - {pattern}" for pattern in profile.patterns]
    glossary_terms = list(dict.fromkeys(profile.glossary_terms + topic.glossary_terms))
    aliases = [repo_key, canonical_url]
    now = now_iso()
    review_path = None
    if profile.status == "review_pending":
        review_path = note_file.relative_to(VAULT_ROOT).as_posix()
    record = ResourceRecord.model_validate(
        {
            "uuid": entity_uuid("resource", canonical_url),
            "canonical_url": canonical_url,
            "repo_key": repo_key,
            "owner": owner,
            "repo_name": repo,
            "display_name": display_name,
            "note_path": note_file.relative_to(VAULT_ROOT).as_posix(),
            "review_path": review_path,
            "archetype": {
                "curated_lists": "curated_aggregator",
                "agentic_ai_models": "ai_resource",
                "data_api_big_data": "data_api_resource",
                "geospatial_earth_data": "geospatial_resource",
                "infrastructure_observability": "infrastructure_tool",
                "security_siem": "security_resource",
                "frontend_design_systems": "frontend_library",
                "scientific_simulation_math": "scientific_library",
                "government_civic_tech": "civic_tech_resource",
                "cad_saas_design": "cad_saas_resource",
                "architecture_playbooks": "reference_architecture",
            }.get(primary_topic_key, "resource"),
            "primary_topic_key": primary_topic_key,
            "secondary_topic_keys": secondary_topics,
            "patterns": patterns,
            "glossary_terms": glossary_terms,
            "aliases": aliases,
            "summary": profile.summary,
            "mechanics": profile.mechanics or topic.mechanics,
            "use_cases": profile.use_cases or topic.use_cases,
            "maturity": profile.maturity,
            "sensitivity": profile.sensitivity,
            "status": profile.status,
            "license": normalize_taxonomy_label(license_name, "unknown"),
            "ecosystem": profile.ecosystem or infer_ecosystem_from_text(profile.summary + " " + " ".join(profile.mechanics) + " ".join(profile.use_cases), topic),
            "domain_primary": profile.domain_primary or DOMAIN_PRIMARY_BY_TOPIC_KEY.get(topic.key, "Mixed"),
            "maturity_stage": profile.maturity_stage or MATURITY_STAGE_BY_TOPIC_KEY.get(topic.key, "Active"),
            "license_class": profile.license_class or license_class_from_name(normalize_taxonomy_label(license_name, "unknown")),
            "deployment_target": profile.deployment_target or DEPLOYMENT_TARGET_BY_TOPIC_KEY.get(topic.key, "Server"),
            "interface_protocol": profile.interface_protocol or INTERFACE_PROTOCOL_BY_TOPIC_KEY.get(topic.key, "Unknown"),
            "data_locality": profile.data_locality or DATA_LOCALITY_BY_TOPIC_KEY.get(topic.key, "Distributed"),
            "hardware_footprint": profile.hardware_footprint or HARDWARE_FOOTPRINT_BY_TOPIC_KEY.get(topic.key, "CPU_Only"),
            "security_compliance": profile.security_compliance or SECURITY_COMPLIANCE_BY_TOPIC_KEY.get(topic.key, "Uncertified"),
            "source_file": source_file,
            "created_at": now,
            "updated_at": now,
            "review_reason": profile.review_reason,
        }
    )
    evidence_snippets = github_metadata_evidence_snippets(github_metadata)
    evidence_snippets.extend(enrichment.evidence_snippets)
    if not evidence_snippets:
        evidence_snippets = fallback_evidence_snippets(context)
    return record, topic, profile, evidence_snippets, github_metadata


def topic_from_key(key: str) -> TopicSpec:
    return TOPIC_BY_KEY[key]


def summary_for_topic(topic: TopicSpec) -> str:
    return f"{topic.title} is the routing layer for resources that belong to the {topic.title.lower()} domain."


def format_evidence_snippets(snippets: list[EvidenceSnippetCandidate]) -> str:
    if not snippets:
        return "- No structured evidence snippets were captured; only bootstrap context was available."
    rows = []
    for snippet in snippets[:4]:
        source_ref = snippet.source_ref or snippet.source_kind
        safe_snippet = truncate_text(snippet.snippet, 220).replace("\n", " ")
        rows.append(f"- [{snippet.source_kind}] {source_ref} :: {safe_snippet} (confidence {snippet.confidence:.2f})")
    return "\n".join(rows)


def note_header(title: str, body: str, frontmatter: dict[str, Any]) -> str:
    return f"{yaml_frontmatter(frontmatter)}\n\n# {title}\n\n{body.strip()}\n"


def build_resource_note(
    record: ResourceRecord,
    topic: TopicSpec,
    siblings: list[ResourceRecord],
    patterns: list[PatternRecord],
    glossary_lookup: dict[str, GlossaryRecord],
    evidence_snippets: list[EvidenceSnippetCandidate] | None = None,
    github_metadata: GitHubRepositoryMetadata | None = None,
) -> str:
    evidence_snippets = evidence_snippets or []
    topic_link = f"[[Topic - {topic.title}]]"
    sibling_links = [f"[[{sib.display_name}]]" for sib in siblings[:3]]
    pattern_links = [
        f"[[Pattern - {pattern.title}]]"
        for pattern in patterns
        if f"Pattern - {pattern.title}" in record.patterns or pattern.title in record.patterns
    ]
    glossary_links: list[str] = []
    for identifier in record.glossary_terms:
        try:
            glossary = resolve_glossary_record(identifier, glossary_lookup)
        except KeyError:
            continue
        link = f"[[Glossary - {glossary.canonical_word}]]"
        if link not in glossary_links:
            glossary_links.append(link)
        if len(glossary_links) >= 8:
            break
    github_section = ""
    if github_metadata:
        github_section = "\n\n".join(
            [
                "## GitHub Snapshot",
                bullets(
                    [
                        f"Description: {github_metadata.description or 'None provided'}",
                        f"Language: {github_metadata.language or 'Unknown'}",
                        f"License: {github_metadata.license_name or 'Unknown'} ({github_metadata.license_spdx or 'UNKNOWN'})",
                        f"Default Branch: {github_metadata.default_branch or 'main'}",
                        f"Stars: {github_metadata.stars}",
                        f"Watchers: {github_metadata.watchers}",
                        f"Homepage: {github_metadata.homepage or 'None provided'}",
                        f"Archived: {'yes' if github_metadata.archived else 'no'}",
                        f"Disabled: {'yes' if github_metadata.disabled else 'no'}",
                        f"Pushed At: {github_metadata.pushed_at or 'Unknown'}",
                        f"Updated At: {github_metadata.updated_at or 'Unknown'}",
                        "Topics: " + (", ".join(github_metadata.topics) if github_metadata.topics else "None provided"),
                    ]
                ),
            ]
        )
    body = "\n\n".join(
        [
            "## Bottom Line\n" + record.summary,
            "## What It Solves\n" + bullets(topic.use_cases),
            "## Architecture & Mechanics\n" + bullets(record.mechanics or topic.mechanics),
            "## Taxonomy\n"
            + bullets(
                [
                    f"Ecosystem: {record.ecosystem}",
                    f"Domain Primary: {record.domain_primary}",
                    f"Maturity Stage: {record.maturity_stage}",
                    f"License Class: {record.license_class}",
                    f"Deployment Target: {record.deployment_target}",
                    f"Interface Protocol: {record.interface_protocol}",
                    f"Data Locality: {record.data_locality}",
                    f"Hardware Footprint: {record.hardware_footprint}",
                    f"Security Compliance: {record.security_compliance}",
                ]
            ),
            "## Integration & Use Cases\n" + bullets(record.use_cases or topic.use_cases),
            "## Semantic Links\n"
            + "\n".join(
                [
                    f"- [parent_topic:: {topic_link}]",
                    "- [taxonomy_hub:: [[Taxonomy Index]]]",
                    *[f"- [related_to:: {link}]" for link in sibling_links],
                    *[f"- [implements_pattern:: {link}]" for link in pattern_links],
                    *[f"- [mentions_term:: {link}]" for link in glossary_links],
                ]
            ),
            "## Evidence\n"
            + "\n".join(
                [
                    f"- Source URL: {record.canonical_url}",
                    "- Source kind: repository seed list",
                    "- Ingestion mode: heuristic bootstrap with later README/source-tree enrichment",
                ]
            ),
            github_section,
            "## Evidence Anchors\n" + format_evidence_snippets(evidence_snippets),
        ]
    )
    frontmatter = {
        "uuid": record.uuid,
        "canonical_url": record.canonical_url,
        "repo_key": record.repo_key,
        "owner": record.owner,
        "repo_name": record.repo_name,
        "aliases": record.aliases,
        "type": record.archetype,
        "primary_topic": topic.title,
        "secondary_topics": [TOPIC_BY_KEY[key].title for key in record.secondary_topic_keys if key in TOPIC_BY_KEY],
        "ecosystem": record.ecosystem,
        "domain_primary": record.domain_primary,
        "maturity_stage": record.maturity_stage,
        "license_class": record.license_class,
        "deployment_target": record.deployment_target,
        "interface_protocol": record.interface_protocol,
        "data_locality": record.data_locality,
        "hardware_footprint": record.hardware_footprint,
        "security_compliance": record.security_compliance,
        "patterns": [
            pattern.title
            for pattern in patterns
            if f"Pattern - {pattern.title}" in record.patterns or pattern.title in record.patterns
        ],
        "glossary_terms": glossary_words_from_identifiers(record.glossary_terms),
        "status": record.status,
        "maturity": record.maturity,
        "sensitivity": record.sensitivity,
        "license": record.license,
        "source_file": record.source_file,
        "evidence_count": len(evidence_snippets),
    }
    if github_metadata:
        frontmatter.update(
            {
                "github_description": github_metadata.description,
                "github_language": github_metadata.language,
                "github_license": github_metadata.license_name,
                "github_license_spdx": github_metadata.license_spdx,
                "github_default_branch": github_metadata.default_branch,
                "github_stars": github_metadata.stars,
                "github_topics": github_metadata.topics,
                "github_homepage": github_metadata.homepage,
                "github_pushed_at": github_metadata.pushed_at,
                "github_updated_at": github_metadata.updated_at,
            }
        )
    return note_header(record.display_name, body, frontmatter)


def build_taxonomy_record(record: ResourceRecord) -> TaxonomyRecord:
    now = record.updated_at or now_iso()
    return TaxonomyRecord.model_validate(
        {
            "uuid": entity_uuid("taxonomy", record.uuid),
            "resource_uuid": record.uuid,
            "note_path": record.note_path,
            "ecosystem": record.ecosystem,
            "domain_primary": record.domain_primary,
            "maturity_stage": record.maturity_stage,
            "license_class": record.license_class,
            "deployment_target": record.deployment_target,
            "interface_protocol": record.interface_protocol,
            "data_locality": record.data_locality,
            "hardware_footprint": record.hardware_footprint,
            "security_compliance": record.security_compliance,
            "summary": f"{record.display_name} classified as {record.domain_primary} with a {record.ecosystem} ecosystem and {record.deployment_target} deployment target.",
            "source_file": record.source_file,
            "created_at": record.created_at or now,
            "updated_at": now,
        }
    )


def build_topic_note(topic: TopicSpec, resources: list[ResourceRecord], topic_indexes: dict[str, IndexRecord], glossary_lookup: dict[str, GlossaryRecord], patterns: list[PatternRecord], review_records: list[ResourceRecord]) -> str:
    resource_links = [f"[[{resource.display_name}]]" for resource in resources]
    review_links = [f"[[{resource.display_name}]]" for resource in review_records]
    pattern_links = [f"[[Pattern - {pattern.title}]]" for pattern in patterns if pattern.topic_keys and topic.key in pattern.topic_keys]
    glossary_links = []
    for identifier in topic.glossary_terms:
        try:
            glossary = resolve_glossary_record(identifier, glossary_lookup)
        except KeyError:
            continue
        link = f"[[Glossary - {glossary.canonical_word}]]"
        if link not in glossary_links:
            glossary_links.append(link)
    overlap_links = [f"[[Topic - {TOPIC_BY_KEY[key].title}]]" for key in topic.overlaps if key in TOPIC_BY_KEY]
    body = "\n\n".join(
        [
            "## Inclusion Criteria\n" + topic.inclusion_criteria,
            "## Canonical Vocabulary\n" + bullets(topic.canonical_vocabulary),
            "## Why This Topic Exists\n" + topic.description,
            "## Mechanics\n" + bullets(topic.mechanics),
            "## Typical Use Cases\n" + bullets(topic.use_cases),
            "## Approved Resources\n" + bullets(resource_links),
            "## Review Queue\n" + bullets(review_links),
            "## Related Patterns\n" + bullets(pattern_links),
            "## Related Glossary\n" + bullets(glossary_links),
            "## Related Topics\n" + bullets(overlap_links),
        ]
    )
    frontmatter = {
        "topic_key": topic.key,
        "type": "topic_index",
        "status": "active",
        "canonical_vocabulary": topic.canonical_vocabulary,
        "inclusion_criteria": topic.inclusion_criteria,
        "patterns": topic.patterns,
        "glossary_terms": topic.glossary_terms,
        "resource_count": len(resources),
        "review_count": len(review_records),
    }
    return note_header(f"Topic - {topic.title}", body, frontmatter)


def build_master_note(topic_counts: dict[str, int], hub_records: list[IndexRecord]) -> str:
    topic_links = [f"[[Topic - {topic.title}]]" for topic in TOPICS]
    hub_links = [f"[[{hub.title}]]" for hub in sorted(hub_records, key=lambda item: item.sort_order)]
    body = "\n\n".join(
        [
            "## Route Map\n" + bullets(f"{link} ({topic_counts.get(topic.key, 0)} approved)" for link, topic in zip(topic_links, TOPICS)),
            "## Hubs\n" + bullets(hub_links),
            "## Operating Rules\n" + bullets(
                [
                    "The master index routes only to topic indexes and hub notes.",
                    "Resource notes live in the resource layer or review layer.",
                    "Glossary notes centralize meaning and observed contexts.",
                    "Pattern notes hold reusable structures across domains.",
                ]
            ),
        ]
    )
    frontmatter = {
        "type": "master_index",
        "status": "active",
        "purpose": "root router",
        "topic_count": len(TOPICS),
    }
    return note_header("Master Index", body, frontmatter)


def build_pattern_note(pattern: PatternSpec, examples: list[str], glossary_lookup: dict[str, GlossaryRecord], topic_lookup: dict[str, TopicSpec]) -> str:
    example_links = [f"[[{example}]]" for example in examples]
    glossary_links = []
    for identifier in pattern.glossary_terms:
        try:
            glossary = resolve_glossary_record(identifier, glossary_lookup)
        except KeyError:
            continue
        link = f"[[Glossary - {glossary.canonical_word}]]"
        if link not in glossary_links:
            glossary_links.append(link)
    topic_links = [f"[[Topic - {topic_lookup[key].title}]]" for key in pattern.topic_keys if key in topic_lookup]
    body = "\n\n".join(
        [
            "## Definition\n" + pattern.definition,
            "## Why It Matters\n" + bullets(
                [
                    "Gives the vault a reusable architectural concept for graph traversal.",
                    "Helps compare repositories that solve the same problem in different ways.",
                ]
            ),
            "## Example Repositories\n" + bullets(example_links),
            "## Related Glossary\n" + bullets(glossary_links),
            "## Related Topics\n" + bullets(topic_links),
        ]
    )
    frontmatter = {
        "pattern_key": pattern.key,
        "aliases": pattern.aliases,
        "type": "pattern",
        "status": "active",
        "examples": pattern.examples,
        "glossary_terms": pattern.glossary_terms,
        "topic_keys": pattern.topic_keys,
    }
    return note_header(f"Pattern - {pattern.title}", body, frontmatter)


def build_glossary_note(term: GlossarySpec, occurrences: list[OccurrenceRecord], related_terms: list[str], resources_by_uuid: dict[str, ResourceRecord]) -> str:
    rows = []
    ordered_occurrences = sorted(occurrences, key=lambda item: (resources_by_uuid.get(item.resource_uuid).display_name.lower() if resources_by_uuid.get(item.resource_uuid) else item.resource_uuid.lower(), item.source_location))
    for occurrence in ordered_occurrences[:10]:
        resource = resources_by_uuid.get(occurrence.resource_uuid)
        resource_link = f"[[{resource.display_name}]]" if resource else occurrence.resource_uuid
        safe_context = occurrence.observed_context.replace("|", "\\|").replace("\n", " ")
        rows.append(
            f"| {resource_link} | {occurrence.term_role} | {occurrence.sense_label} | {safe_context} | {occurrence.source_location} |"
        )
    table = table_rows(rows)
    related_links = []
    for identifier in related_terms:
        try:
            related = resolve_glossary_spec(identifier)
        except KeyError:
            continue
        if related.key == term.key:
            continue
        link = f"[[Glossary - {related.word}]]"
        if link not in related_links:
            related_links.append(link)
    body = "\n\n".join(
        [
            "## Definition\n" + term.definition,
            "## Aliases\n" + (", ".join(term.aliases) if term.aliases else "None"),
            "## Related Terms\n" + bullets(related_links),
            "## Observed Contexts\n| Resource | Role | Sense | Context | Source |\n| --- | --- | --- | --- | --- |\n" + table,
            "## Sense Notes\n" + bullets(
                [
                    f"Sense label: {term.sense_label}",
                    "This note is the canonical meaning for this sense, not merely a spelling variant.",
                ]
            ),
        ]
    )
    frontmatter = {
        "term_key": term.key,
        "canonical_word": term.word,
        "sense_label": term.sense_label,
        "aliases": term.aliases,
        "related_terms": glossary_words_from_identifiers(related_terms, exclude_key=term.key),
        "type": "glossary_term",
        "status": "active",
        "topic_keys": term.topic_keys,
    }
    return note_header(f"Glossary - {term.word}", body, frontmatter)


def build_taxonomy_note(resources: list[ResourceRecord]) -> str:
    ordered_resources = sorted(resources, key=lambda item: item.display_name.lower())
    rows = []
    for resource in ordered_resources:
        rows.append(
            f"| [[{resource.display_name}]] | {resource.ecosystem} | {resource.domain_primary} | {resource.maturity_stage} | {resource.license_class} | {resource.deployment_target} | {resource.interface_protocol} | {resource.data_locality} | {resource.hardware_footprint} | {resource.security_compliance} |"
        )
    matrix = table_rows(rows)
    body = "\n\n".join(
        [
            "## Purpose\nThe taxonomy turns each repository into a multi-axis record so the vault can filter by ecosystem, domain, maturity, deployment, protocol, locality, and footprint without re-reading source notes.",
            "## Dimensions\n" + bullets(
                [
                    "Ecosystem: the primary technical family or stack the repository sits in.",
                    "Domain Primary: the broad problem domain used for top-level routing.",
                    "Maturity Stage: a coarse life-cycle label for how established the repository appears.",
                    "License Class: a legal-usage bucket that can be refined later from repository metadata.",
                    "Deployment Target: the most likely runtime surface for the resource.",
                    "Interface Protocol: how users or systems tend to interact with the resource.",
                    "Data Locality: how the resource handles state or data movement.",
                    "Hardware Footprint: the rough compute profile required to use the resource.",
                    "Security Compliance: whether the resource claims or implies a formal compliance posture.",
                ]
            ),
            "## Resource Matrix\n| Resource | Ecosystem | Domain | Maturity | License | Target | Protocol | Locality | Footprint | Security |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n" + matrix,
            "## Cross-Analysis\n" + bullets(
                [
                    "Use this hub to compare repositories before deciding what to build, merge, or study next.",
                    "Filter by combinations such as `domain_primary + deployment_target + hardware_footprint` to find fit-for-purpose tools.",
                    "Treat `Unknown` and `Uncertified` values as prompts for later enrichment rather than final truth.",
                ]
            ),
        ]
    )
    frontmatter = {
        "type": "taxonomy_hub",
        "status": "active",
        "resource_count": len(resources),
        "dimensions": TAXONOMY_DIMENSIONS,
    }
    return note_header("Taxonomy Index", body, frontmatter)


def build_review_queue_note(review_records: list[ResourceRecord]) -> str:
    rows = []
    for record in review_records:
        rows.append(f"| [[{record.display_name}]] | {record.review_reason or 'Needs review'} | {record.primary_topic_key} |")
    table = table_rows(rows)
    body = "\n\n".join(
        [
            "## Queue\n| Resource | Reason | Topic |\n| --- | --- | --- |\n" + table,
            "## Gate\n" + bullets(
                [
                    "Resources in this queue are held back from the approved resource layer.",
                    "Review items can be promoted into the main resource layer after inspection.",
                ]
            ),
        ]
    )
    frontmatter = {
        "type": "review_queue",
        "status": "active",
        "review_count": len(review_records),
    }
    return note_header("Review Queue", body, frontmatter)


def extract_term_candidates(text: str) -> list[str]:
    candidates: list[str] = []
    for term in GLOSSARY:
        patterns = [term.word.lower(), term.key.lower()] + [alias.lower() for alias in term.aliases]
        if any(pattern in text.lower() for pattern in patterns):
            candidates.append(term.key)
    return list(dict.fromkeys(candidates))


def collect_occurrences(resources: list[ResourceRecord], glossary_lookup: dict[str, GlossaryRecord]) -> dict[str, list[tuple[str, str, str]]]:
    occurrences: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for resource in resources:
        resource_text = " ".join([resource.display_name, resource.summary, " ".join(resource.mechanics), " ".join(resource.use_cases)])
        for term_key, glossary in glossary_lookup.items():
            if any(alias.lower() in resource_text.lower() for alias in [glossary.canonical_word, term_key, *glossary.aliases]):
                snippet = resource.summary[:120]
                occurrences[term_key].append((resource.display_name, resource.note_path, snippet))
    return occurrences


def build_glossary_records(resources: list[ResourceRecord]) -> list[GlossaryRecord]:
    ordered_keys: list[str] = []
    for term in GLOSSARY:
        ordered_keys.append(term.key)
    for topic in TOPICS:
        for identifier in topic.glossary_terms:
            try:
                spec = resolve_glossary_spec(identifier)
            except KeyError:
                continue
            ordered_keys.append(spec.key)
    ordered_keys = list(dict.fromkeys(ordered_keys))
    now = now_iso()
    records: list[GlossaryRecord] = []
    for term_key in ordered_keys:
        term = GLOSSARY_BY_KEY[term_key]
        record = GlossaryRecord.model_validate(
            {
                "uuid": entity_uuid("glossary", term.key),
                "term_key": term.key,
                "canonical_word": term.word,
                "sense_label": term.sense_label,
                "definition": term.definition,
                "aliases": term.aliases,
                "related_terms": term.related_terms,
                "topic_keys": term.topic_keys,
                "note_path": (GLOSSARY_DIR / f"Glossary - {term.word}.md").relative_to(VAULT_ROOT).as_posix(),
                "summary": term.definition,
                "status": "active",
                "created_at": now,
                "updated_at": now,
            }
        )
        records.append(record)
    return records


def build_pattern_records() -> list[PatternRecord]:
    now = now_iso()
    records: list[PatternRecord] = []
    for pattern in PATTERNS:
        records.append(
            PatternRecord.model_validate(
                {
                    "uuid": entity_uuid("pattern", pattern.key),
                    "pattern_key": pattern.key,
                    "title": pattern.title,
                    "definition": pattern.definition,
                    "aliases": pattern.aliases,
                    "examples": pattern.examples,
                    "glossary_terms": pattern.glossary_terms,
                    "topic_keys": pattern.topic_keys,
                    "note_path": (PATTERN_DIR / f"Pattern - {pattern.title}.md").relative_to(VAULT_ROOT).as_posix(),
                    "summary": pattern.definition,
                    "status": "active",
                    "created_at": now,
                    "updated_at": now,
                }
            )
        )
    return records


def write_resource_note(
    record: ResourceRecord,
    topic: TopicSpec,
    patterns: list[PatternRecord],
    glossary_lookup: dict[str, GlossaryRecord],
    siblings: list[ResourceRecord],
    evidence_snippets: list[EvidenceSnippetCandidate] | None = None,
    github_metadata: GitHubRepositoryMetadata | None = None,
) -> None:
    text = build_resource_note(record, topic, siblings, patterns, glossary_lookup, evidence_snippets, github_metadata)
    write_text(VAULT_ROOT / record.note_path, text)


def write_topic_note(topic: TopicSpec, approved: list[ResourceRecord], review_records: list[ResourceRecord], patterns: list[PatternRecord], glossary_lookup: dict[str, GlossaryRecord], topic_indexes: dict[str, IndexRecord]) -> None:
    text = build_topic_note(topic, approved, topic_indexes, glossary_lookup, patterns, review_records)
    write_text(VAULT_ROOT / topic_indexes[topic.key].note_path, text)


def write_pattern_note(pattern_record: PatternRecord, pattern_spec: PatternSpec, glossary_lookup: dict[str, GlossaryRecord], resources_by_key: dict[str, ResourceRecord]) -> None:
    examples = []
    for repo_key in pattern_spec.examples:
        resource = resources_by_key.get(repo_key)
        if resource:
            examples.append(resource.display_name)
    text = build_pattern_note(pattern_spec, examples, glossary_lookup, TOPIC_BY_KEY)
    write_text(VAULT_ROOT / pattern_record.note_path, text)


def write_glossary_note(term_record: GlossaryRecord, term_spec: GlossarySpec, occurrences: list[OccurrenceRecord], resources_by_uuid: dict[str, ResourceRecord]) -> None:
    text = build_glossary_note(term_spec, occurrences, term_spec.related_terms, resources_by_uuid)
    write_text(VAULT_ROOT / term_record.note_path, text)


def write_taxonomy_note(resources: list[ResourceRecord]) -> None:
    text = build_taxonomy_note(resources)
    write_text(INDEX_DIR / "Taxonomy Index.md", text)


def write_review_note(review_records: list[ResourceRecord]) -> None:
    text = build_review_queue_note(review_records)
    write_text(REVIEW_DIR / "Review Queue.md", text)


def build_topic_canvas(topic: TopicSpec, topic_record: IndexRecord, resources: list[ResourceRecord], review_records: list[ResourceRecord], glossary_lookup: dict[str, GlossaryRecord]) -> dict[str, Any]:
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    center_id = entity_uuid("canvas-node", f"{topic.key}-center")
    nodes.append(
        {
            "id": center_id,
            "type": "file",
            "file": topic_record.note_path,
            "x": 0,
            "y": 0,
            "width": 400,
            "height": 240,
        }
    )
    # resource nodes
    ordered = resources[:]
    ordered.sort(key=lambda item: item.display_name.lower())
    for idx, resource in enumerate(ordered):
        node_id = entity_uuid("canvas-node", resource.note_path)
        nodes.append(
            {
                "id": node_id,
                "type": "file",
                "file": resource.note_path,
                "x": (idx % 4) * 430 - 650,
                "y": (idx // 4) * 260 + 260,
                "width": 320,
                "height": 190,
            }
        )
        edges.append(
            {
                "id": entity_uuid("canvas-edge", f"{center_id}->{node_id}"),
                "fromNode": center_id,
                "fromSide": "bottom",
                "toNode": node_id,
                "toSide": "top",
            }
        )
    # glossary anchor nodes
    glossary_keys = [key for key in topic.glossary_terms if key in glossary_lookup][:4]
    for idx, key in enumerate(glossary_keys):
        glossary = glossary_lookup[key]
        node_id = entity_uuid("canvas-node", glossary.note_path)
        nodes.append(
            {
                "id": node_id,
                "type": "file",
                "file": glossary.note_path,
                "x": 560,
                "y": idx * 200 - 120,
                "width": 280,
                "height": 160,
            }
        )
        edges.append(
            {
                "id": entity_uuid("canvas-edge", f"{center_id}->{node_id}"),
                "fromNode": center_id,
                "fromSide": "right",
                "toNode": node_id,
                "toSide": "left",
            }
        )
    review_links = review_records[:3]
    for idx, resource in enumerate(review_links):
        node_id = entity_uuid("canvas-node", f"review::{resource.note_path}")
        nodes.append(
            {
                "id": node_id,
                "type": "file",
                "file": resource.note_path,
                "x": -980,
                "y": idx * 220 - 120,
                "width": 320,
                "height": 180,
            }
        )
        edges.append(
            {
                "id": entity_uuid("canvas-edge", f"{center_id}->{node_id}"),
                "fromNode": center_id,
                "fromSide": "left",
                "toNode": node_id,
                "toSide": "right",
            }
        )
    return {"nodes": nodes, "edges": edges}


def build_root_canvas(master_record: IndexRecord, topic_records: list[IndexRecord], hub_records: list[IndexRecord]) -> dict[str, Any]:
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    master_id = entity_uuid("canvas-node", master_record.index_key)
    nodes.append(
        {
            "id": master_id,
            "type": "file",
            "file": master_record.note_path,
            "x": 0,
            "y": 0,
            "width": 420,
            "height": 260,
        }
    )
    hub_order = [hub for hub in sorted(hub_records, key=lambda item: item.sort_order) if hub.kind != "master"]
    for idx, hub in enumerate(hub_order):
        node_id = entity_uuid("canvas-node", hub.index_key)
        nodes.append(
            {
                "id": node_id,
                "type": "file",
                "file": hub.note_path,
                "x": 520,
                "y": idx * 220 - 200,
                "width": 320,
                "height": 180,
            }
        )
        edges.append(
            {
                "id": entity_uuid("canvas-edge", f"{master_id}->{node_id}"),
                "fromNode": master_id,
                "fromSide": "right",
                "toNode": node_id,
                "toSide": "left",
            }
        )
    for idx, topic in enumerate(topic_records):
        node_id = entity_uuid("canvas-node", topic.index_key)
        nodes.append(
            {
                "id": node_id,
                "type": "file",
                "file": topic.note_path,
                "x": (idx % 3) * 400 - 620,
                "y": (idx // 3) * 260 + 320,
                "width": 320,
                "height": 180,
            }
        )
        edges.append(
            {
                "id": entity_uuid("canvas-edge", f"{master_id}->{node_id}"),
                "fromNode": master_id,
                "fromSide": "bottom",
                "toNode": node_id,
                "toSide": "top",
            }
        )
    return {"nodes": nodes, "edges": edges}


def canvas_json(nodes_edges: dict[str, Any]) -> str:
    return json.dumps(nodes_edges, indent=2, ensure_ascii=False)


def insert_ingestion_run(conn: sqlite3.Connection, source_file: str, resource_count: int, taxonomy_count: int, glossary_count: int, pattern_count: int, edge_count: int, note_count: int, canvas_count: int) -> None:
    conn.execute(
        """
        INSERT OR REPLACE INTO ingestion_runs (
            id, run_key, source_file, created_at, resource_count, taxonomy_count,
            glossary_count, pattern_count, edge_count, note_count, canvas_count, summary
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            entity_uuid("run", f"{source_file}::{now_iso()}"),
            f"seed::{source_file}",
            source_file,
            now_iso(),
            resource_count,
            taxonomy_count,
            glossary_count,
            pattern_count,
            edge_count,
            note_count,
            canvas_count,
            f"Generated the vault scaffold from {source_file}.",
        ),
    )


def build_edges(
    master_record: IndexRecord,
    topic_records: list[IndexRecord],
    hub_records: list[IndexRecord],
    resources: list[ResourceRecord],
    patterns: list[PatternRecord],
    glossary_records: list[GlossaryRecord],
) -> tuple[list[EdgeRecord], dict[str, list[EdgeRecord]]]:
    edges: list[EdgeRecord] = []
    node_edges: dict[str, list[EdgeRecord]] = defaultdict(list)
    resource_lookup = {resource.repo_key: resource for resource in resources}
    topic_lookup = {record.index_key: record for record in topic_records}
    pattern_lookup = {record.pattern_key: record for record in patterns}
    glossary_lookup = {record.term_key: record for record in glossary_records}

    # hierarchy edges
    for topic in topic_records:
        edge = EdgeRecord(
            id=entity_uuid("edge", f"{master_record.uuid}->{topic.uuid}:routes_to"),
            source_uuid=master_record.uuid,
            target_uuid=topic.uuid,
            source_kind="index",
            target_kind="index",
            relationship_type="routes_to",
            confidence=1.0,
            provenance="hierarchy",
            note="Master index routes to topic index.",
        )
        edges.append(edge)
        node_edges[topic.index_key].append(edge)

    for hub in hub_records:
        edge = EdgeRecord(
            id=entity_uuid("edge", f"{master_record.uuid}->{hub.uuid}:routes_to"),
            source_uuid=master_record.uuid,
            target_uuid=hub.uuid,
            source_kind="index",
            target_kind="index",
            relationship_type="routes_to",
            confidence=1.0,
            provenance="hierarchy",
            note="Master index routes to hub note.",
        )
        edges.append(edge)

    # index memberships and resource-term relations
    for resource in resources:
        topic_uuid = topic_lookup[resource.primary_topic_key].uuid
        edges.append(
            EdgeRecord(
                id=entity_uuid("edge", f"{topic_uuid}->{resource.uuid}:indexes"),
                source_uuid=topic_uuid,
                target_uuid=resource.uuid,
                source_kind="index",
                target_kind="resource",
                relationship_type="indexes",
                confidence=0.98,
                provenance="topic_assignment",
                note="Resource belongs to this topic.",
            )
        )
        for secondary in resource.secondary_topic_keys:
            if secondary in topic_lookup:
                edges.append(
                    EdgeRecord(
                        id=entity_uuid("edge", f"{topic_lookup[secondary].uuid}->{resource.uuid}:indexes"),
                        source_uuid=topic_lookup[secondary].uuid,
                        target_uuid=resource.uuid,
                        source_kind="index",
                        target_kind="resource",
                        relationship_type="indexes",
                        confidence=0.72,
                        provenance="secondary_topic_assignment",
                        note="Resource overlaps this secondary topic.",
                    )
                )
        for pattern_title in resource.patterns:
            pattern_key = None
            for key, record in pattern_lookup.items():
                if record.title == pattern_title.replace("Pattern - ", "") or record.title == pattern_title:
                    pattern_key = key
                    break
            if not pattern_key:
                for key, record in pattern_lookup.items():
                    if record.title == pattern_title.replace("Pattern - ", ""):
                        pattern_key = key
                        break
            if pattern_key:
                edges.append(
                    EdgeRecord(
                        id=entity_uuid("edge", f"{resource.uuid}->{pattern_lookup[pattern_key].uuid}:implements_pattern"),
                        source_uuid=resource.uuid,
                        target_uuid=pattern_lookup[pattern_key].uuid,
                        source_kind="resource",
                        target_kind="pattern",
                        relationship_type="implements_pattern",
                        confidence=0.9,
                        provenance="topic_pattern_assignment",
                        note="Resource aligns with a reusable pattern.",
                    )
                )
        for term_key in resource.glossary_terms:
            try:
                glossary_record = resolve_glossary_record(term_key, glossary_lookup)
            except KeyError:
                continue
            if glossary_record.term_key in glossary_lookup:
                edges.append(
                    EdgeRecord(
                        id=entity_uuid("edge", f"{resource.uuid}->{glossary_record.uuid}:mentions_term"),
                        source_uuid=resource.uuid,
                        target_uuid=glossary_record.uuid,
                        source_kind="resource",
                        target_kind="glossary",
                        relationship_type="mentions_term",
                        confidence=0.88,
                        provenance="topic_vocabulary",
                        note="Resource note mentions the glossary term.",
                    )
                )

    # glossary relations
    for glossary in glossary_records:
        for related in GLOSSARY_BY_KEY[glossary.term_key].related_terms:
            try:
                related_record = resolve_glossary_record(related, glossary_lookup)
            except KeyError:
                continue
            if related_record.term_key in glossary_lookup:
                edges.append(
                    EdgeRecord(
                        id=entity_uuid("edge", f"{glossary.uuid}->{related_record.uuid}:related_to"),
                        source_uuid=glossary.uuid,
                        target_uuid=related_record.uuid,
                        source_kind="glossary",
                        target_kind="glossary",
                        relationship_type="related_to",
                        confidence=0.86,
                        provenance="glossary_seed",
                        note="Glossary term relation from ontology seed.",
                    )
                )

    # shared taxonomy edges
    taxonomy_dimensions = [
        ("ecosystem", 0.74, {"Unknown", "Mixed"}),
        ("interface_protocol", 0.68, {"Unknown"}),
        ("deployment_target", 0.64, {"Unknown", "Server"}),
    ]
    for dimension, confidence, skip_values in taxonomy_dimensions:
        grouped: dict[str, list[ResourceRecord]] = defaultdict(list)
        for resource in resources:
            value = getattr(resource, dimension, None)
            if not value or value in skip_values:
                continue
            grouped[value].append(resource)
        for value, group in grouped.items():
            if len(group) < 2:
                continue
            ordered_group = sorted(group, key=lambda item: item.display_name.lower())
            for idx, source in enumerate(ordered_group):
                for target in ordered_group[idx + 1 :]:
                    if source.primary_topic_key == target.primary_topic_key:
                        continue
                    edges.append(
                        EdgeRecord(
                            id=entity_uuid("edge", f"{source.uuid}->{target.uuid}:related_to:{dimension}:{slugify(value)}"),
                            source_uuid=source.uuid,
                            target_uuid=target.uuid,
                            source_kind="resource",
                            target_kind="resource",
                            relationship_type="related_to",
                            confidence=confidence,
                            provenance=f"taxonomy_overlap:{dimension}",
                            note=f"Resources share {dimension}={value}.",
                        )
                    )

    # resource-to-resource pair edges
    pair_edges = [
        ("twbs/bootstrap", "necolas/normalize.css", "complements", "Front-end foundation pair."),
        ("twbs/bootstrap", "animate-css/animate.css", "complements", "Design-system and motion pair."),
        ("twbs/bootstrap", "Modernizr/Modernizr", "complements", "Layout and feature-detection pair."),
        ("react/react", "twbs/bootstrap", "complements", "Component UI and layout system pair."),
        ("react/react", "necolas/normalize.css", "complements", "UI composition and style normalization."),
        ("hashicorp/terraform", "puppetlabs/puppet", "related_to", "Infrastructure automation overlap."),
        ("hashicorp/terraform", "chef/chef", "related_to", "Infrastructure automation overlap."),
        ("puppetlabs/puppet", "chef/chef", "related_to", "Config management overlap."),
        ("prometheus/prometheus", "netdata/netdata", "complements", "Observability complement."),
        ("prometheus/prometheus", "statsd/statsd", "complements", "Metrics pipeline complement."),
        ("getsentry/sentry", "prometheus/prometheus", "complements", "Error tracking and observability complement."),
        ("simbody/simbody", "astropy/astropy", "related_to", "Scientific computation overlap."),
        ("astropy/astropy", "sympy/sympy", "complements", "Scientific analysis complement."),
        ("orsinium-labs/generated-awesomeness", "pracdata/awesome-open-source-data-engineering", "related_to", "Curated list overlap."),
        ("orsinium-labs/generated-awesomeness", "The-Cool-Coders/Project-Ideas-And-Resources", "related_to", "Curated list overlap."),
        ("Azure-Samples/semantic-kernel-advanced-usage", "vercel-labs/skills", "related_to", "Agentic workflow overlap."),
        ("G-Research/siembol", "scadastrangelove/awesome-ai-security-tools", "related_to", "Security-adjacent overlap."),
        ("GSA/data.gov", "not-a-bank/open-banking-tracker-data", "related_to", "Open-data overlap."),
        ("ngageoint/geoq", "GSA/data.gov", "related_to", "Public-data and geospatial overlap."),
        ("usds/playbook", "cfpb/open-source-checklist", "related_to", "Civic guidance overlap."),
        ("alphagov/whitehall", "usds/playbook", "related_to", "Public-sector guidance overlap."),
    ]
    for source_key, target_key, relationship, note in pair_edges:
        source = resource_lookup.get(source_key)
        target = resource_lookup.get(target_key)
        if not source or not target:
            continue
        edges.append(
            EdgeRecord(
                id=entity_uuid("edge", f"{source.uuid}->{target.uuid}:{relationship}"),
                source_uuid=source.uuid,
                target_uuid=target.uuid,
                source_kind="resource",
                target_kind="resource",
                relationship_type=relationship,
                confidence=0.92 if relationship == "complements" else 0.78,
                provenance="pair_override",
                note=note,
            )
        )

    # topic overlap edges
    for topic in TOPICS:
        topic_record = topic_lookup[topic.key]
        for other_key in topic.overlaps:
            if other_key not in topic_lookup:
                continue
            other = topic_lookup[other_key]
            if topic_record.uuid == other.uuid:
                continue
            edges.append(
                EdgeRecord(
                    id=entity_uuid("edge", f"{topic_record.uuid}->{other.uuid}:overlaps_with"),
                    source_uuid=topic_record.uuid,
                    target_uuid=other.uuid,
                    source_kind="index",
                    target_kind="index",
                    relationship_type="overlaps_with",
                    confidence=0.7,
                    provenance="topic_overlap",
                    note="Topic index overlaps with related domain.",
                )
            )

    return edges, node_edges


def make_term_occurrences(resources: list[ResourceRecord], glossary_records: list[GlossaryRecord]) -> list[OccurrenceRecord]:
    glossary_lookup = {record.term_key: record for record in glossary_records}
    occurrences: list[OccurrenceRecord] = []
    for resource in resources:
        sections: list[tuple[str, str]] = [("title", resource.display_name), ("summary", resource.summary)]
        sections.extend((f"mechanics[{idx}]", text) for idx, text in enumerate(resource.mechanics))
        sections.extend((f"use_cases[{idx}]", text) for idx, text in enumerate(resource.use_cases))
        for term_key, term in glossary_lookup.items():
            aliases = [term.canonical_word, term.term_key, *term.aliases]
            for source_location, text in sections:
                if not any(alias.lower() in text.lower() for alias in aliases):
                    continue
                role = source_location.split("[", 1)[0]
                confidence = 0.9 if role == "summary" else 0.82 if role in {"mechanics", "use_cases"} else 0.76
                occurrences.append(
                    OccurrenceRecord.model_validate(
                        {
                            "id": entity_uuid("occurrence", f"{term.uuid}::{resource.uuid}::{resource.note_path}::{source_location}"),
                            "term_uuid": term.uuid,
                            "resource_uuid": resource.uuid,
                            "note_path": resource.note_path,
                            "observed_context": text[:160],
                            "source_location": source_location,
                            "term_role": role,
                            "sense_label": term.sense_label,
                            "confidence": confidence,
                            "provenance": "topic_and_summary_scan",
                        }
                    )
                )
    return occurrences


def generate_library(seed_file: Path = SEED_FILE) -> dict[str, Any]:
    init_dirs()
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)
    runtime = load_lmstudio_runtime()

    master_record = build_master_index_record()
    topic_records = build_topic_index_records(master_record.uuid)
    hub_records = build_hub_index_records(master_record.uuid)

    for record in [master_record, *topic_records, *hub_records]:
        upsert_index(conn, record)

    urls = read_seed_urls(seed_file)
    resources: list[ResourceRecord] = []
    topic_to_resources: dict[str, list[ResourceRecord]] = defaultdict(list)
    review_resources: list[ResourceRecord] = []
    resources_by_key: dict[str, ResourceRecord] = {}
    resources_by_uuid: dict[str, ResourceRecord] = {}
    evidence_by_uuid: dict[str, list[EvidenceSnippetCandidate]] = {}
    github_metadata_by_uuid: dict[str, GitHubRepositoryMetadata | None] = {}
    github_runtime = load_github_runtime()
    for url in urls:
        record, topic, profile, evidence_snippets, github_metadata = build_resource_record(url, seed_file.name, runtime, github_runtime)
        resources.append(record)
        resources_by_key[record.repo_key] = record
        resources_by_uuid[record.uuid] = record
        evidence_by_uuid[record.uuid] = evidence_snippets
        github_metadata_by_uuid[record.uuid] = github_metadata
        if record.status == "review_pending":
            review_resources.append(record)
        else:
            topic_to_resources[topic.key].append(record)
        upsert_resource(conn, record)
        upsert_taxonomy(conn, build_taxonomy_record(record))
        insert_aliases(conn, record.uuid, record.aliases)
        for snippet in evidence_snippets:
            insert_evidence_snippet(conn, record.uuid, snippet)

    pattern_records = build_pattern_records()
    for record in pattern_records:
        upsert_pattern(conn, record)

    glossary_records = build_glossary_records(resources)
    for record in glossary_records:
        upsert_glossary(conn, record)

    glossary_lookup = {record.term_key: record for record in glossary_records}
    occurrences = make_term_occurrences(resources, glossary_records)
    for occurrence in occurrences:
        insert_occurrence(conn, occurrence)

    # semantic indexes and resource output
    topic_map = {topic.key: topic for topic in TOPICS}
    for topic in TOPICS:
        approved = topic_to_resources.get(topic.key, [])
        review_for_topic = [record for record in review_resources if record.primary_topic_key == topic.key]
        topic_index = next(record for record in topic_records if record.index_key == topic.key)
        write_topic_note(topic, approved, review_for_topic, pattern_records, glossary_lookup, {record.index_key: record for record in topic_records})
        for resource in approved:
            sibling_pool = [item for item in approved if item.uuid != resource.uuid]
            write_resource_note(resource, topic, pattern_records, glossary_lookup, sibling_pool, evidence_by_uuid.get(resource.uuid, []), github_metadata_by_uuid.get(resource.uuid))
            insert_membership(conn, topic_index.uuid, resource.uuid, "primary", 0.98, "topic_assignment")
            insert_edge(conn, EdgeRecord(
                id=entity_uuid("edge", f"{topic_index.uuid}->{resource.uuid}:indexes"),
                source_uuid=topic_index.uuid,
                target_uuid=resource.uuid,
                source_kind="index",
                target_kind="resource",
                relationship_type="indexes",
                confidence=0.98,
                provenance="topic_assignment",
                note="Resource belongs to topic index.",
            ))
            for secondary_topic in resource.secondary_topic_keys:
                if secondary_topic in topic_map:
                    secondary_index = next(record for record in topic_records if record.index_key == secondary_topic)
                    insert_membership(conn, secondary_index.uuid, resource.uuid, "secondary", 0.72, "secondary_topic_assignment")
        for resource in review_for_topic:
            insert_review(conn, resource.uuid, resource.review_reason or "Needs manual review", resource.note_path)
            write_resource_note(resource, topic, pattern_records, glossary_lookup, [], evidence_by_uuid.get(resource.uuid, []), github_metadata_by_uuid.get(resource.uuid))

    # pattern notes
    for pattern_record in pattern_records:
        pattern_spec = next(spec for spec in PATTERNS if spec.key == pattern_record.pattern_key)
        write_pattern_note(pattern_record, pattern_spec, glossary_lookup, resources_by_key)

    # glossary notes
    occurrence_map: dict[str, list[OccurrenceRecord]] = defaultdict(list)
    for occurrence in occurrences:
        term = next(record for record in glossary_records if record.uuid == occurrence.term_uuid)
        resource = next(record for record in resources if record.uuid == occurrence.resource_uuid)
        occurrence_map[term.term_key].append(occurrence)
        insert_edge(conn, EdgeRecord(
            id=entity_uuid("edge", f"{resource.uuid}->{term.uuid}:mentions_term"),
            source_uuid=resource.uuid,
            target_uuid=term.uuid,
            source_kind="resource",
            target_kind="glossary",
            relationship_type="mentions_term",
            confidence=0.88,
            provenance="term_occurrence",
            note="Resource mentions glossary term.",
        ))
    for record in glossary_records:
        term_spec = GLOSSARY_BY_KEY[record.term_key]
        write_glossary_note(record, term_spec, occurrence_map.get(record.term_key, []), resources_by_uuid)

    # hub notes
    write_taxonomy_note(resources)
    write_text(GLOSSARY_DIR / "Glossary Index.md", note_header(
        "Glossary Index",
        textwrap.dedent(
            f"""
            ## Purpose
            The glossary centralizes canonical definitions, aliases, related terms, and observed contexts to prevent semantic drift.

            ## Terms
            {chr(10).join(f'- [[Glossary - {record.canonical_word}]]' for record in glossary_records)}
            """
        ).strip(),
        {
            "type": "glossary_hub",
            "status": "active",
            "term_count": len(glossary_records),
        },
    ))
    write_text(PATTERN_DIR / "Pattern Index.md", note_header(
        "Pattern Index",
        textwrap.dedent(
            f"""
            ## Purpose
            The pattern layer captures reusable architectural ideas that recur across repositories.

            ## Patterns
            {chr(10).join(f'- [[Pattern - {record.title}]]' for record in pattern_records)}
            """
        ).strip(),
        {
            "type": "pattern_hub",
            "status": "active",
            "pattern_count": len(pattern_records),
        },
    ))
    write_review_note(review_resources)

    # master note
    approved_counts = {topic.key: len(topic_to_resources.get(topic.key, [])) for topic in TOPICS}
    write_text(INDEX_DIR / "Master Index.md", build_master_note(approved_counts, hub_records))

    # topic canvases and root canvas
    master_canvas = build_root_canvas(master_record, topic_records, hub_records)
    write_text(CANVAS_DIR / "Library Map.canvas", canvas_json(master_canvas))
    canvas_count = 1
    for topic in TOPICS:
        topic_record = next(record for record in topic_records if record.index_key == topic.key)
        canvas = build_topic_canvas(topic, topic_record, topic_to_resources.get(topic.key, []), [record for record in review_resources if record.primary_topic_key == topic.key], glossary_lookup)
        write_text(TOPIC_CANVAS_DIR / f"Topic - {topic.title}.canvas", canvas_json(canvas))
        canvas_count += 1

    # edge generation
    edges, _ = build_edges(master_record, topic_records, hub_records, resources, pattern_records, glossary_records)
    for edge in edges:
        insert_edge(conn, edge)
    conn.commit()
    save_github_metadata_cache(github_runtime)

    # glossary and pattern notes are already on disk; now record the run
    note_count = len(list(INDEX_DIR.glob("*.md"))) + len(list(RESOURCE_DIR.glob("*.md"))) + len(list(GLOSSARY_DIR.glob("*.md"))) + len(list(PATTERN_DIR.glob("*.md"))) + len(list(REVIEW_DIR.glob("*.md")))
    insert_ingestion_run(
        conn,
        seed_file.name,
        len(resources),
        len(resources),
        len(glossary_records),
        len(pattern_records),
        len(edges),
        note_count,
        canvas_count,
    )
    conn.commit()

    summary = {
        "seed_file": seed_file.name,
        "resources": len(resources),
        "approved_resources": sum(len(v) for v in topic_to_resources.values()),
        "review_resources": len(review_resources),
        "taxonomy_rows": len(resources),
        "glossary_terms": len(glossary_records),
        "patterns": len(pattern_records),
        "edges": len(edges),
        "notes": note_count,
        "canvases": canvas_count,
        "database": str(DB_PATH.relative_to(VAULT_ROOT)),
        "lmstudio_enabled": runtime.settings.enabled,
        "lmstudio_available": runtime.available,
    }
    write_text(LOG_DIR / "last_run.json", json.dumps(summary, indent=2, ensure_ascii=False))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap the solutions library vault from repository seeds.")
    parser.add_argument("--seed-file", type=Path, default=SEED_FILE, help="Path to the repository seed list markdown file.")
    args = parser.parse_args()
    summary = generate_library(args.seed_file)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
