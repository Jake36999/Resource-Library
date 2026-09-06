---
uuid: "745ee75a-eea5-53e7-b063-43502a171090"
canonical_url: "https://github.com/apache/airflow"
repo_key: "apache/airflow"
owner: "apache"
repo_name: "airflow"
aliases: ["apache/airflow", "https://github.com/apache/airflow"]
type: "data_platform"
primary_topic: "Data APIs & Big Data"
secondary_topics: ["Infrastructure & Observability", "Architecture & Developer Playbooks"]
ecosystem: "Data_Platform"
domain_primary: "Data"
maturity_stage: "Production_Ready"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "Python_SDK"
data_locality: "Distributed"
hardware_footprint: "High_Memory"
security_compliance: "Uncertified"
agent_surface: "Procedural"
patterns: ["ETL API Ingestion", "Data Orchestration", "Observability Pipeline"]
glossary_terms: ["Data Orchestration", "DAG", "ELT", "Data Engineering", "API"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-05"
evidence_count: 4
github_description: "Apache Airflow - A platform to programmatically author, schedule, and monitor workflows"
github_language: "Python"
github_license_spdx: "Apache-2.0"
github_default_branch: "main"
github_stars: 46666
github_topics: ["airflow", "apache", "apache-airflow", "automation", "dag", "data-engineering", "data-integration", "data-orchestrator", "data-pipelines", "data-science", "elt", "etl", "machine-learning", "mlops", "orchestration", "python", "scheduler", "workflow", "workflow-engine", "workflow-orchestration"]
github_homepage: "https://airflow.apache.org/"
github_pushed_at: "2026-09-04T23:41:54Z"
---
# apache - airflow

## Bottom Line
The reference open-source workflow orchestrator: pipelines are Python code defining a DAG of tasks, which a scheduler executes with retries, backfills and dependency awareness.

## What It Solves
- Express data pipeline dependencies explicitly instead of chaining cron jobs.
- Recover from partial failure by retrying or backfilling only the affected tasks.
- Integrate heterogeneous systems through a large provider/operator ecosystem.

## Architecture & Mechanics
- DAG files are Python modules parsed into a graph of tasks and dependencies.
- A scheduler resolves which task instances are runnable per logical date and queues them.
- Executors (Local, Celery, Kubernetes) decide where task processes actually run.
- A metadata database holds run state; the web UI reads it for lineage, logs and retries.

## What Is Inside
- **A monorepo where the providers dwarf the core** — `providers/` is 7,954 of 13,938 files: `google` (1,143), `amazon` (914), `apache` (818), `common` (528), `microsoft` (379), `fab` (218), `openlineage` (210), `edge3` (190). Each provider is an independently released package with its own tests and docs, and that separation is the reusable design.
- **The core** — `airflow-core/src/` (1,986), with `airflow-core/docs/` (406), `newsfragments/` (128, a changelog-fragment convention) and **`airflow-core/adr/` (8 architecture decision records)**.
- **A development environment as a product** — `dev/breeze/` (490 files) is a full CLI for reproducible local builds and CI parity; `dev/airflow_perf/` carries a synthetic `elastic_dag.py` for scaling tests; `dev/stats/explore_pr_candidates.ipynb` analyses the project's own PR flow.
- **A generated API surface** — 96 schema paths under `api_fastapi/`, including OpenAPI documents and TypeScript query clients generated from them (`openapi-gen/queries/`).
- **A task SDK split out** — `task-sdk/` (297 files), the boundary between what a task may call and the scheduler.
- **Deployment** — `chart/` (270 files, the official Helm chart), `Dockerfile` and `Dockerfile.ci`, and a documented `docker-compose` quickstart under `airflow-core/docs/howto/docker-compose/`.
- **Sixty-three agent-instruction paths** — `.agents/skills/` carries `SKILL.md` files for tasks like `prepare-providers-documentation`, `aip-user-stories`, `airflow-new-sdk`, plus `dev/skill-evals/`. Contribution procedure written for agents, in one of the largest Python projects there is.

## Transferable Capability
**Express work as a dependency graph and let a scheduler decide what may run, so ordering is derived rather than written.** The payoff is recovery: because each unit is separately addressable and its dependencies are known, a failure can be resumed from the failed unit instead of from the beginning. A second, separable move is **releasing the connectors on their own cadence from the engine**, so integration with a hundred external systems does not slow the core. A third: **the contribution procedure itself is executable** - a task-shaped skill per repetitive job - which is how a project this size keeps mechanical conventions consistent across contributors who will never read the whole guide.

**Alternative to:** ordering encoded as a script, where the sequence exists only as the order of lines and a partial failure means starting over; and to a monolith where every integration is a core concern. **Applies wherever** multi-step work has dependencies and any step can fail.

## Taxonomy
- Ecosystem: Data_Platform
- Domain Primary: Data
- Maturity Stage: Production_Ready
- License Class: Permissive
- Deployment Target: Server
- Interface Protocol: Python_SDK
- Data Locality: Distributed
- Hardware Footprint: High_Memory
- Security Compliance: Uncertified
- Agent Surface: Procedural

## Integration & Use Cases
- Orchestrate ingestion from public APIs into a warehouse on a schedule.
- Coordinate ML training and evaluation steps with explicit dependencies.
- Study scheduler design and idempotent task semantics.

## Semantic Links
- [parent_topic:: [[Topic - Data APIs & Big Data]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[dbt-labs - dbt-core]]]
- [related_to:: [[duckdb - duckdb]]]
- [related_to:: [[pracdata - awesome-open-source-data-engineering]]]
- [implements_pattern:: [[Pattern - ETL API Ingestion]]]
- [implements_pattern:: [[Pattern - Data Orchestration]]]
- [implements_pattern:: [[Pattern - Observability Pipeline]]]
- [mentions_term:: [[Glossary - Data Orchestration]]]
- [mentions_term:: [[Glossary - DAG]]]
- [mentions_term:: [[Glossary - ELT]]]
- [mentions_term:: [[Glossary - Data Engineering]]]
- [mentions_term:: [[Glossary - API]]]

## Evidence
- Source URL: https://github.com/apache/airflow
- Source kind: GitHub REST metadata plus maintainer documentation
- Ingestion mode: agent-curated note authored against live repository metadata
- Metadata captured: 2026-08-31

## GitHub Snapshot

- Description: Apache Airflow - A platform to programmatically author, schedule, and monitor workflows
- Language: Python
- License (SPDX): Apache-2.0
- Default Branch: main
- Stars: 46666
- Homepage: https://airflow.apache.org/
- Pushed At: 2026-08-31T19:05:24Z
- Topics: airflow, apache, apache-airflow, automation, dag, data-engineering, data-integration, data-orchestrator, data-pipelines, data-science, elt, etl, machine-learning, mlops, orchestration, python, scheduler, workflow, workflow-engine, workflow-orchestration

## Evidence Anchors
- [github_repo] description :: Apache Airflow - A platform to programmatically author, schedule, and monitor workflows (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: Apache-2.0 (confidence 0.90)
- [github_repo] topics :: airflow, apache, apache-airflow, automation, dag, data-engineering, data-integration, data-orchestrator, data-pipelines, data-science, elt, etl, machine-learning, mlops, orchestration, python, scheduler, workflow, workflow-engine, workflow-orchestration (confidence 0.85)
