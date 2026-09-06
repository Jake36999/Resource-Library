---
uuid: "649b2519-5433-5442-811f-475fad3b4b12"
canonical_url: "https://github.com/duckdb/duckdb"
repo_key: "duckdb/duckdb"
owner: "duckdb"
repo_name: "duckdb"
aliases: ["duckdb/duckdb", "https://github.com/duckdb/duckdb"]
type: "data_platform"
primary_topic: "Data APIs & Big Data"
secondary_topics: ["Scientific Simulation & Math", "Geospatial & Earth Data"]
ecosystem: "Data_Platform"
domain_primary: "Data"
maturity_stage: "Production_Ready"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Python_SDK"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "Documented"
patterns: ["Analytical Query Engine", "ETL API Ingestion", "Schema Mapping"]
glossary_terms: ["OLAP", "Schema", "Dataset", "Data Engineering"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-05"
evidence_count: 4
github_description: "DuckDB is an analytical in-process SQL database management system"
github_language: "C++"
github_license_spdx: "MIT"
github_default_branch: "main"
github_stars: 40866
github_topics: ["analytics", "database", "embedded-database", "olap", "sql"]
github_homepage: "http://www.duckdb.org"
github_pushed_at: "2026-09-04T21:57:55Z"
---
# duckdb - duckdb

## Bottom Line
An embedded columnar OLAP engine — SQLite's deployment model with a vectorised analytical executor — that queries Parquet, CSV and Arrow directly with no server to run.

## What It Solves
- Run warehouse-class analytical SQL on a laptop against files, without standing up infrastructure.
- Query Parquet and CSV in place rather than loading them into a database first.
- Hand analysts one dependency-free binary instead of a cluster.

## Architecture & Mechanics
- The engine runs in-process, linked into the host application or Python session.
- A columnar, vectorised executor processes batches rather than row-at-a-time.
- Zero-copy integration with Arrow and Pandas avoids serialisation overhead.
- Extensions add httpfs, spatial, full-text search and remote object-store access.

## What Is Inside
- **The test suite is the largest thing here and is independently valuable** — `test/` (6,157 files), of which `test/sql/` is 4,821 and the dominant extension is **4,818 `.test` files in sqllogictest format**, plus 790 `.test_slow`. A large, portable, engine-neutral SQL conformance corpus.
- **Adversarial testing as first-class directories** — `test/fuzzer/` (283), `test/ossfuzz/` (72), `test/issues/` (231, one regression per reported bug), `test/optimizer/` (211).
- **A benchmark suite covering the standard workloads** — `benchmark/` (1,918 files, 1,156 `.benchmark`): `micro/` (400), `recursive_cte/` (231), `imdb/` (229 — the join-order benchmark), `tpch/` (165), `large/` (143), `clickbench/` (133), `imdb_plan_cost/` (115), and ingestion benchmarks comparing CSV, Parquet and native paths.
- **1,586 data files and 1,805 CSVs** — `data/`, including `data/geoparquet/generate_test_data.py` and a CSV-sniffer corpus. Useful to anyone testing a parser, not only a database.
- **The engine, by stage** — `src/`: `include/` (1,621), `function/` (268), `execution/` (254), `parser/` (247), `planner/` (229), `optimizer/` (154). The stage boundaries are legible enough to read a query's life through.
- **Extensions in-tree** — `extension/` (1,263) including `tpcds/dsdgen/` with the TPC-DS schema as SQL.
- **A published API spec** — `api_spec/v2/schema/schema.yaml`. Agent instructions at `AGENTS.md` and `CLAUDE.md`.

## Transferable Capability
**Remove the server.** Do the heavy computation inside the process that needs the answer, against files where they already are, with no service to run, secure, version or connect to. The whole class of operational concern disappears rather than being managed. The second property: read the material in place rather than importing it first, so there is no copy to keep in step.

**Alternative to:** standing up a service to answer questions that only one process ever asks; and to an import step whose purpose is to make data queryable, which creates a second copy that can be stale. **Applies wherever** analysis is being done by one consumer over material that already exists in a readable form.

## Taxonomy
- Ecosystem: Data_Platform
- Domain Primary: Data
- Maturity Stage: Production_Ready
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Python_SDK
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: Documented

## Integration & Use Cases
- Prototype analytical queries over a data lake before committing to a warehouse.
- Replace hand-written Pandas aggregations with declarative SQL on the same frames.
- Study modern vectorised query execution in a readable codebase.

## Semantic Links
- [parent_topic:: [[Topic - Data APIs & Big Data]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[apache - airflow]]]
- [related_to:: [[dbt-labs - dbt-core]]]
- [related_to:: [[geopandas - geopandas]]]
- [implements_pattern:: [[Pattern - Analytical Query Engine]]]
- [implements_pattern:: [[Pattern - ETL API Ingestion]]]
- [implements_pattern:: [[Pattern - Schema Mapping]]]
- [mentions_term:: [[Glossary - OLAP]]]
- [mentions_term:: [[Glossary - Schema]]]
- [mentions_term:: [[Glossary - Dataset]]]
- [mentions_term:: [[Glossary - Data Engineering]]]

## Evidence
- Source URL: https://github.com/duckdb/duckdb
- Source kind: GitHub REST metadata plus maintainer documentation
- Ingestion mode: agent-curated note authored against live repository metadata
- Metadata captured: 2026-08-31

## GitHub Snapshot

- Description: DuckDB is an analytical in-process SQL database management system
- Language: C++
- License (SPDX): MIT
- Default Branch: main
- Stars: 40866
- Homepage: http://www.duckdb.org
- Pushed At: 2026-08-31T19:22:04Z
- Topics: analytics, database, embedded-database, olap, sql

## Evidence Anchors
- [github_repo] description :: DuckDB is an analytical in-process SQL database management system (confidence 0.95)
- [github_repo] language :: C++ (confidence 0.90)
- [github_repo] license :: MIT (confidence 0.90)
- [github_repo] topics :: analytics, database, embedded-database, olap, sql (confidence 0.85)
