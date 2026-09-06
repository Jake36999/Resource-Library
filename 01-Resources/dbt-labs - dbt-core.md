---
uuid: "013af06b-140a-5e9d-be87-b4fe4f6a61ba"
canonical_url: "https://github.com/dbt-labs/dbt-core"
repo_key: "dbt-labs/dbt-core"
owner: "dbt-labs"
repo_name: "dbt-core"
aliases: ["dbt-labs/dbt-core", "https://github.com/dbt-labs/dbt-core"]
type: "data_platform"
primary_topic: "Data APIs & Big Data"
secondary_topics: ["Architecture & Developer Playbooks"]
ecosystem: "Data_Platform"
domain_primary: "Data"
maturity_stage: "Production_Ready"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "CLI"
data_locality: "Distributed"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "Procedural"
patterns: ["ETL API Ingestion", "Schema Mapping", "Analytical Query Engine"]
glossary_terms: ["ELT", "Data Engineering", "Schema", "Dataset"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-05"
evidence_count: 4
github_description: "dbt enables data analysts and engineers to transform their data using the same practices that software engineers use to build applications."
github_language: "Rust"
github_license_spdx: "Apache-2.0"
github_default_branch: "main"
github_stars: 13747
github_topics: ["analytics", "business-intelligence", "data-modeling", "dbt-viewpoint", "elt", "pypa", "slack"]
github_homepage: "https://getdbt.com"
github_pushed_at: "2026-09-05T00:08:06Z"
---
# dbt-labs - dbt-core

## Bottom Line
Brings software engineering discipline to the transform half of ELT: models are templated SQL SELECTs that dbt compiles, orders by inferred dependency, materialises and tests.

## What It Solves
- Replace tangles of stored procedures with version-controlled, reviewable SQL models.
- Infer the transformation DAG automatically from model references instead of maintaining it by hand.
- Assert data quality with declarative tests that run in the same pipeline.

## Architecture & Mechanics
- Models are SQL files with Jinja templating; `ref()` calls declare dependencies.
- A compiler resolves refs into a DAG and emits warehouse-native SQL.
- Materialisation strategies (view, table, incremental, snapshot) control physical output.
- Schema tests and documentation are declared in YAML beside the models.

## What Is Inside
- **This is no longer the Python dbt.** The repository is now a Rust workspace: `crates/` is 3,994 of 4,093 files, 1,453 `.rs`. Anyone expecting the Python package should read this before cloning.
- **The crates, and what each one is** — `dbt-jinja` (894 files: a Jinja implementation in Rust, with its own `benchmarks/`), `dbt-docs-server` (784), `dbt-loader` (632, project parsing), `dbt-adapter` (202), `dbt-schemas` (86), `dbt-telemetry` (94), `dbt-common` (90), plus `dbt-metricflow`, `dbt-csv`, `dbt-index-core`, `dbt-cloud-api`, `adbc-record-replay`.
- **628 `.sql` files and 330 fixture paths** — `crates/dbt-adapter/tests/duckdb_attach_fixtures/` is a directory per scenario, each with its `catalogs.yml` and an `output.snap` snapshot; 262 `.snap` files overall. A worked example of snapshot-testing a compiler.
- **Metric authoring documented with runnable examples** — `crates/dbt-metricflow/docs/authoring-metrics.md` with `examples/duckdb_orders.sql` and `duckdb_orders_manifest.json`.
- **An OpenAPI description of the cloud API** — `crates/dbt-cloud-api/openapi-v3.yaml`; 198 schema paths overall.
- **Changelog as dated fragments** — `.changes/unreleased/Features-20260826-233022.yaml` and similar, a convention that avoids merge conflicts on a shared changelog.
- **Agent instructions in-tree** — `.agents/skills/` (13 paths) including `adapters-annotate-references/` with `SKILL.md` and executable `scripts/annotate.py`, `scripts/find_upstream.py`, plus a `.claude/` directory.

## Transferable Capability
**Infer the dependency graph from the references in the work itself, rather than asking anyone to declare it.** If each unit names what it draws on, the order is a consequence and cannot drift from reality. Two things ride on that: assertions about the result live beside the definition rather than in a separate suite, and documentation of what feeds what is generated rather than maintained. A third capability, and the one most often needed: **recompute only what changed rather than everything**, so the cost of an update tracks the size of the change rather than the size of the whole. A rebuild that costs the same whether one thing moved or a thousand did is a rebuild people stop running.

**Alternative to:** a hand-maintained ordering that is correct until someone forgets; and to quality checks kept somewhere other than the thing they check. **Applies wherever** derived artefacts reference the artefacts they derive from — which includes a set of notes whose links state their own dependencies.

## Taxonomy
- Ecosystem: Data_Platform
- Domain Primary: Data
- Maturity Stage: Production_Ready
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: CLI
- Data Locality: Distributed
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: Procedural

## Integration & Use Cases
- Structure a warehouse's transformation layer as a reviewed, tested codebase.
- Generate lineage documentation automatically from model references.
- Study dependency inference from source-code references.

## Semantic Links
- [parent_topic:: [[Topic - Data APIs & Big Data]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[apache - airflow]]]
- [related_to:: [[duckdb - duckdb]]]
- [related_to:: [[pracdata - awesome-open-source-data-engineering]]]
- [implements_pattern:: [[Pattern - ETL API Ingestion]]]
- [implements_pattern:: [[Pattern - Schema Mapping]]]
- [implements_pattern:: [[Pattern - Analytical Query Engine]]]
- [mentions_term:: [[Glossary - ELT]]]
- [mentions_term:: [[Glossary - Data Engineering]]]
- [mentions_term:: [[Glossary - Schema]]]
- [mentions_term:: [[Glossary - Dataset]]]

## Evidence
- Source URL: https://github.com/dbt-labs/dbt-core
- Source kind: GitHub REST metadata plus maintainer documentation
- Ingestion mode: agent-curated note authored against live repository metadata
- Metadata captured: 2026-08-31

## GitHub Snapshot

- Description: dbt enables data analysts and engineers to transform their data using the same practices that software engineers use to build applications.
- Language: Rust
- License (SPDX): Apache-2.0
- Default Branch: main
- Stars: 13747
- Homepage: https://getdbt.com
- Pushed At: 2026-08-31T19:15:17Z
- Topics: analytics, business-intelligence, data-modeling, dbt-viewpoint, elt, pypa, slack

## Evidence Anchors
- [github_repo] description :: dbt enables data analysts and engineers to transform their data using the same practices that software engineers use to build applications. (confidence 0.95)
- [github_repo] language :: Rust (confidence 0.90)
- [github_repo] license :: Apache-2.0 (confidence 0.90)
- [github_repo] topics :: analytics, business-intelligence, data-modeling, dbt-viewpoint, elt, pypa, slack (confidence 0.85)
