"""A small synthetic vault, and the fakes that keep these tests offline.

No test may require Docker, LM Studio, network access or the ToolSet. Every
one of those is injected, following the `FakeLM` pattern the scout tests
already use - which is what makes the suite runnable on a laptop with none of
the host's services running.
"""
from __future__ import annotations

import textwrap
from pathlib import Path

import pytest


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).lstrip(), encoding="utf-8")
    return path


def resource(name: str, *, topic: str, licence: str = "Permissive",
             target: str = "Server", footprint: str = "CPU_Only",
             bottom_line: str = "", solves: str = "", extra: str = "",
             patterns: tuple[str, ...] = (), container: bool = False) -> str:
    pattern_links = "\n".join(f"- [implements_pattern:: [[{p}]]]" for p in patterns)
    return f"""
    ---
    canonical_url: "https://github.com/example/{name.replace(' ', '-')}"
    repo_key: "example/{name.replace(' ', '-')}"
    type: "infrastructure_tool"
    primary_topic: "{topic}"
    domain_primary: "Infrastructure"
    ecosystem: "Python"
    maturity_stage: "Production_Ready"
    license_class: "{licence}"
    deployment_target: "{target}"
    interface_protocol: "CLI"
    data_locality: "Local_First"
    hardware_footprint: "{footprint}"
    security_compliance: "Uncertified"
    github_stars: 100
    github_pushed_at: "2026-08-01T00:00:00Z"
    {"container: true" if container else ""}
    {'expansion_status: "pending"' if container else ""}
    ---

    # {name}

    ## Bottom Line
    {bottom_line or f"{name} is a distinct thing that does distinct work."}

    ## What It Solves
    {solves or f"- The specific problem that only {name} addresses."}

    ## Integration & Use Cases
    {extra or "- Used where the problem appears."}

    ## Semantic Links
    - [parent_topic:: [[Topic - {topic}]]]
    - [taxonomy_hub:: [[Taxonomy Index]]]
    {pattern_links}
    """


@pytest.fixture()
def vault(tmp_path: Path) -> Path:
    """A vault with one of everything the system reasons about."""
    root = tmp_path / "vault"

    write(root / "00-Indexes" / "Taxonomy Index.md", """
    ---
    type: "taxonomy_hub"
    status: "active"
    ---

    # Taxonomy Index

    ## Resource Matrix
    | Resource | Ecosystem | Domain | Maturity | License | Target | Protocol | Locality | Footprint | Security |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | [[widget-scheduler]] | Python | Infrastructure | Production_Ready | Permissive | Server | CLI | Local_First | CPU_Only | Uncertified |
    """)

    write(root / "internal docs" / "Scouting Domains.md", """
    ---
    type: "domain_register"
    status: "proposed"
    ---

    # Scouting Domains

    ### Tier 1 - Enter Rotation Now

    **Distributed Systems** (`distributed_systems`)
    Queues, streaming, consensus.
    Seed queries: `open source message queue`
    """)

    write(root / "00-Indexes" / "Topic - Plumbing.md", """
    ---
    topic_key: "plumbing"
    type: "topic_index"
    status: "active"
    canonical_vocabulary: ["scheduler", "queue", "retry"]
    inclusion_criteria: "Scheduling and queueing tools."
    resource_count: 2
    ---

    # Topic - Plumbing

    ## Inclusion Criteria
    Scheduling and queueing tools.
    """)

    write(root / "01-Resources" / "widget-scheduler.md", resource(
        "widget-scheduler", topic="Plumbing",
        bottom_line="Runs dependent jobs on a schedule and recovers from partial failure.",
        solves="- Re-running an entire nightly batch after one task fails.",
        patterns=("Pattern - Job Scheduling",)))

    write(root / "01-Resources" / "gadget-queue.md", resource(
        "gadget-queue", topic="Plumbing", licence="Copyleft", target="Local_Only",
        footprint="High_Memory",
        bottom_line="A durable message queue for local-first workloads.",
        solves="- Losing messages when a consumer restarts."))

    write(root / "01-Resources" / "awesome-plumbing.md", resource(
        "awesome-plumbing", topic="Plumbing", licence="Unknown", container=True,
        bottom_line="A curated list of plumbing tools.",
        solves="- Finding candidates without reading the whole ecosystem."))

    write(root / "03-Patterns" / "Pattern - Job Scheduling.md", """
    ---
    pattern_key: "job_scheduling"
    type: "pattern"
    status: "active"
    topic_keys: ["plumbing"]
    ---

    # Pattern - Job Scheduling

    ## Definition
    Ordering dependent work so a failure resumes rather than restarts.

    ## Related Topics
    - [[Topic - Plumbing]]
    """)

    write(root / "09-Applications" / "Application - Nightly Batch.md", """
    ---
    type: "application_record"
    project: "Nightly batch"
    stage: "delivery"
    resources_used: ["widget-scheduler"]
    patterns_discovered: ["validation by identifiable signal"]
    domains: ["distributed_systems"]
    outcome: "the batch recovers instead of restarting"
    attested_by: "user"
    ---

    # Application - Nightly Batch

    ## What Was Needed
    A way to rerun only the failed part of a nightly batch.

    ## What Was Found And Taken
    widget-scheduler, for its dependency graph and retry semantics.

    ## What It Replaced
    A shell script that restarted everything.

    ## What The Catalogue Should Learn
    Recovery semantics matter more than feature lists for batch tooling.

    ## Semantic Links
    - [applied_resource:: [[widget-scheduler]]]
    - [related_topic:: [[Topic - Plumbing]]]
    """)

    write(root / "02-Glossary" / "Glossary - Scheduler.md", """
    ---
    term_key: "scheduler"
    type: "glossary_term"
    status: "active"
    topic_keys: ["plumbing"]
    ---

    # Glossary - Scheduler

    ## Definition
    A component that decides when work runs.
    """)

    return root


@pytest.fixture()
def db(tmp_path: Path) -> Path:
    return tmp_path / "index.sqlite"


@pytest.fixture()
def built(vault: Path, db: Path) -> Path:
    from librarian import index as index_mod
    index_mod.build(vault, db, rebuild=True)
    return db


@pytest.fixture(autouse=True)
def offline(monkeypatch):
    """Vectors are unavailable unless a test says otherwise.

    Retrieval must be correct without them, and a test that quietly reached a
    running LM Studio would hide that.
    """
    from librarian import embed as embed_mod
    monkeypatch.setattr(embed_mod, "search",
                        lambda conn, query, cfg=None, limit=50, layers=None:
                        ([], "vector search disabled in tests"))
