---
uuid: "73482af4-e409-5bf5-bf74-32d06da2a9c9"
canonical_url: "https://github.com/Victor-Kipruto-Rop/medallion-lakehouse-platform"
repo_key: "Victor-Kipruto-Rop/medallion-lakehouse-platform"
owner: "Victor-Kipruto-Rop"
repo_name: "medallion-lakehouse-platform"
aliases: ["Victor-Kipruto-Rop/medallion-lakehouse-platform", "https://github.com/Victor-Kipruto-Rop/medallion-lakehouse-platform"]
type: "reference_implementation"
primary_topic: "Data APIs & Big Data"
secondary_topics: ["Architecture & Developer Playbooks", "Infrastructure & Observability"]
ecosystem: "Data_Platform"
domain_primary: "Data"
maturity_stage: "Reference"
license_class: "Unknown"
deployment_target: "Server"
interface_protocol: "Python_SDK"
data_locality: "Distributed"
hardware_footprint: "High_Memory"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Medallion Layering", "ETL API Ingestion", "Data Orchestration"]
glossary_terms: ["Medallion Architecture", "ELT", "Data Engineering", "Schema"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Unknown"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-03"
evidence_count: 5
github_description: "A production-grade data engineering platform implementing the Bronze → Silver → Gold medallion architecture for scalable data ingestion, transformation, quality, governance, and analytics."
github_language: "Python"
github_license_spdx: "Unknown"
github_default_branch: "main"
github_stars: 8
github_topics: ["aws", "data", "engineerin", "lakehouse", "medallion"]
github_homepage: "Unknown"
github_pushed_at: "2026-08-23T01:24:23Z"
---
# Victor-Kipruto-Rop - medallion-lakehouse-platform

## Bottom Line
A complete Bronze/Silver/Gold skeleton with every surrounding layer present at once — Airflow, PySpark, Delta Lake, dbt, Great Expectations, Terraform, Docker Compose, CI — around roughly 500 lines of pipeline covering one source and one table.

## What It Solves
- Showing what a full medallion stack looks like when nothing is left out, including the parts usually forgotten.
- Wiring quality gates into orchestration, so a failed expectation halts the DAG rather than propagating bad data.
- Giving a first lakehouse a shape to copy: which directory holds what, and what the CI should check.

## Architecture & Mechanics
- `extract_to_bronze.py` lands raw JSON partitioned `year=/month=/day=`.
- `bronze_to_silver.py` explodes records, enforces `TRANSACTIONS_SCHEMA`, casts, deduplicates by key, and **splits invalid rows into a `_quarantine/` path with a counted warning rather than filtering them away** — the one idea here worth taking on its own.
- `silver_to_gold.py` builds the marts; the dbt project models them again for BI; `medallion_etl_dag.py` sequences everything with task groups.
- Great Expectations checkpoints gate each Silver and Gold write; Terraform provisions the three buckets, the pipeline IAM role and an ECR repository, with compute as a separate module.

## What Is Inside
- **A complete stack skeleton, one file deep** — `src/ingestion/extract_to_bronze.py` (43
  lines), `src/transformations/bronze_to_silver.py` (99), `src/analytics/silver_to_gold.py`
  (74), `dags/medallion_etl_dag.py` (82), `src/common/spark_session.py` (61). Roughly 500 lines
  of pipeline in total, covering one source and one table.
- **Every surrounding layer present** — `terraform/` (storage and compute modules with
  per-environment tfvars), `docker/` (Airflow, Spark, Compose), `dbt_project/` (staging and
  marts models, a reconciliation test), `gx/` (Great Expectations suites and checkpoints for
  Silver and Gold), `.github/workflows/` (lint, test, deploy DAGs, deploy infrastructure).
- **Checklists worth reading independently** — `.github/production-hardening-checklist.md` and
  the deployment validation checklist in `README.md`.
- **Test fixtures** — `tests/fixtures/raw_transactions.json`, plus unit tests for
  transformations, schemas, cloud storage and production hardening.

## Transferable Capability
**Grade material by how refined it is, and make every grade reproducible from the one below it.** Keep the raw form exactly as it arrived and never edit it; derive a cleaned form from that; derive the form people actually use from the cleaned one. Because nothing is edited in place, a mistake anywhere is corrected by *replaying* rather than by recovering, and the cost of being wrong drops to the cost of re-running.

The second discipline is that rejected material goes somewhere inspectable rather than being dropped — a quarantine, counted, not a filter.

**Alternative to:** editing a single working copy and hoping the edits were right; any pipeline where the only way back from a bad transformation is a backup. **Applies wherever** material passes through stages of refinement and the stages might be wrong — ingestion, annotation, summarisation, indexing, or a catalogue whose raw scouting output, curated descriptions and derived views are the same three grades.

## Taxonomy
- Ecosystem: Data_Platform
- Domain Primary: Data
- Maturity Stage: Reference
- License Class: Unknown
- Deployment Target: Server
- Interface Protocol: Python_SDK
- Data Locality: Distributed
- Hardware Footprint: High_Memory
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Copy the repository layout and CI checks when starting a lakehouse from nothing.
- Take the quarantine pattern into an existing pipeline that currently drops bad rows.
- Read the production-hardening and deployment checklists as a list of things to remember.

## Reading Notes
**The description and the evidence disagree, and the note says so.** Both the GitHub description and the README say “production-grade”. The repository was created 2026-08-22 and last pushed 2026-08-23 — roughly eleven hours of history — with 8 stars, 0 forks, 0 open issues and **no licence file at all**, which is why `license_class` is `Unknown` and a permissive-only constraint must exclude it. The code that exists is clean, typed and tested; “production-grade” describes the shape it imitates, not evidence of production. It is a reference implementation, and a decent one.

## Semantic Links
- [parent_topic:: [[Topic - Data APIs & Big Data]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[apache - airflow]]]
- [related_to:: [[dbt-labs - dbt-core]]]
- [related_to:: [[PHACDataHub - data-mesh-ref-impl]]]
- [implements_pattern:: [[Pattern - Medallion Layering]]]
- [implements_pattern:: [[Pattern - ETL API Ingestion]]]
- [implements_pattern:: [[Pattern - Data Orchestration]]]
- [mentions_term:: [[Glossary - Medallion Architecture]]]
- [mentions_term:: [[Glossary - ELT]]]
- [mentions_term:: [[Glossary - Data Engineering]]]
- [mentions_term:: [[Glossary - Schema]]]

## Evidence
- Source URL: https://github.com/Victor-Kipruto-Rop/medallion-lakehouse-platform
- Source kind: GitHub REST metadata plus the repository tree and files, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-03
- Depth of read: recorded per source in [[Scouting Working File 2026-09-03]]

## GitHub Snapshot

- Description: A production-grade data engineering platform implementing the Bronze → Silver → Gold medallion architecture for scalable data ingestion, transformation, quality, governance, and analytics.
- Language: Python
- License (SPDX): Unknown
- Default Branch: main
- Stars: 8
- Homepage: Unknown
- Pushed At: 2026-08-23T01:24:23Z
- Topics: aws, data, engineerin, lakehouse, medallion

## Evidence Anchors
- [github_repo] description :: A production-grade data engineering platform implementing the Bronze → Silver → Gold medallion architecture for scalable data ingestion, transformation, quality, governance, and analytics. (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: Unknown (confidence 0.90)
- [github_repo] topics :: aws, data, engineerin, lakehouse, medallion (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-03 (confidence 0.95)
