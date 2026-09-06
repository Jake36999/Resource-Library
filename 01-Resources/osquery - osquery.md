---
uuid: "7cd2dfc5-4be4-5213-b190-2ce21edb6322"
canonical_url: "https://github.com/osquery/osquery"
repo_key: "osquery/osquery"
owner: "osquery"
repo_name: "osquery"
aliases: ["osquery/osquery", "https://github.com/osquery/osquery"]
type: "security_tool"
primary_topic: "Security & SIEM"
secondary_topics: ["Infrastructure & Observability", "Data APIs & Big Data"]
ecosystem: "Security_Analytics"
domain_primary: "Security"
maturity_stage: "Production_Ready"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "CLI"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Security_Adjacent"
agent_surface: "Documented"
patterns: ["Endpoint Instrumentation", "Threat Detection Pipeline", "Schema Mapping"]
glossary_terms: ["Endpoint Instrumentation", "Threat Detection", "Schema", "Monitoring"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Apache-2.0 OR GPL-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-08-31"
evidence_count: 5
github_description: "SQL powered operating system instrumentation, monitoring, and analytics."
github_language: "C++"
github_license_spdx: "NOASSERTION"
github_default_branch: "master"
github_stars: 23533
github_topics: ["hacktoberfest", "intrusion-detection", "monitoring", "security", "sql"]
github_homepage: "https://osquery.io"
github_pushed_at: "2026-08-25T16:33:00Z"
---
# osquery - osquery

## Bottom Line
Exposes the operating system as a relational database, so processes, sockets, users, kernel modules and installed packages can be queried with ordinary SQL.

## What It Solves
- Ask fleet-wide security questions without writing a bespoke collector for each data source.
- Turn ad-hoc incident triage into a repeatable, reviewable SQL query.
- Schedule differential queries so state changes become events.

## Architecture & Mechanics
- Virtual tables wrap OS APIs so each subsystem appears as a queryable table.
- A SQLite-backed engine plans and executes queries against those virtual tables.
- Scheduled query packs run on an interval and emit added/removed row diffs as events.
- An optional remote (TLS) plugin lets a central server distribute packs and collect results.

## What Is Inside
- **Table definitions are a separate, declarative layer** — `specs/` (289 files, 287 `.table`): `darwin/` (71), `windows/` (56), `posix/` (55), `linux/` (41), `utility/` (9), `sleuthkit/` (3). Each `.table` file declares a table's columns and platform in a small DSL, and the C++ implementation is generated around it. That separation of *schema declaration* from *collection code* is the transferable design, and it is why the SQL surface stays coherent across three operating systems.
- **The implementations** — `osquery/tables/` (573 files) mirroring the specs, plus `osquery/events/` (96, the subscriber model), `osquery/sql/` (27), `osquery/core/` (58), `osquery/worker/` (35).
- **Extension examples you can copy** — `external/examples/config_plugin/` and `external/examples/read_only_table/`, each a minimal working plugin with its CMake.
- **Fuzzing corpora as scripts** — `tools/harnesses/osqueryfuzz_config_corpus.sh` and `osqueryfuzz_sqlquery_corpus.sh`.
- **Benchmarks per subsystem** — `osquery/database/benchmarks/`, `osquery/events/benchmarks/`, `osquery/filesystem/darwin/benchmarks/plist_benchmarks.cpp`.
- **Both licences shipped side by side** — `LICENSE-Apache-2.0` and `LICENSE-GPL-2.0`; see `Reading Notes` for why that matters.
- **Agent-facing config** — `.cursor/rules/build-format.mdc` and `.cursorignore`.

## Transferable Capability
**Expose the state of a running system as something you can query, instead of as a set of commands whose output must be parsed.** Once state is tabular the questions become composable — joins, filters, aggregates — and the same question works everywhere the tables exist. The structural move worth taking on its own: **declare each table's shape in a small separate definition and generate the plumbing around it**, so the collection code and the published shape cannot drift, and one coherent surface spans three very different platforms.

**Alternative to:** a library of commands and bespoke parsing per platform. **Applies wherever** the same questions must be asked of heterogeneous things whose native interfaces differ.

## Taxonomy
- Ecosystem: Security_Analytics
- Domain Primary: Security
- Maturity Stage: Production_Ready
- License Class: Permissive
- Deployment Target: Server
- Interface Protocol: CLI
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Security_Adjacent
- Agent Surface: Documented

## Integration & Use Cases
- Build a lightweight endpoint detection layer on top of scheduled query packs.
- Answer compliance questions across heterogeneous hosts with one query language.
- Study the virtual-table pattern for exposing system state as data.

## Reading Notes
**Dual-licensed, and the LICENSE says so in machine-readable form:**
`SPDX-License-Identifier: Apache-2.0 OR GPL-2.0-only`. `OR` is a choice offered to you, not a
combination binding you, so the permissive option is what you may rely on and the catalogue
classifies it Permissive. Read the wrong way round it would be filed Copyleft and would
vanish from every permissive-constrained query — which is exactly what happened during the
2026-09 backfill before the rule was corrected.

## Semantic Links
- [parent_topic:: [[Topic - Security & SIEM]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[wazuh - wazuh]]]
- [related_to:: [[falcosecurity - falco]]]
- [related_to:: [[duckdb - duckdb]]]
- [implements_pattern:: [[Pattern - Endpoint Instrumentation]]]
- [implements_pattern:: [[Pattern - Threat Detection Pipeline]]]
- [implements_pattern:: [[Pattern - Schema Mapping]]]
- [mentions_term:: [[Glossary - Endpoint Instrumentation]]]
- [mentions_term:: [[Glossary - Threat Detection]]]
- [mentions_term:: [[Glossary - Schema]]]
- [mentions_term:: [[Glossary - Monitoring]]]

## Evidence
- Source URL: https://github.com/osquery/osquery
- Source kind: GitHub REST metadata plus maintainer documentation
- Ingestion mode: agent-curated note authored against live repository metadata
- Metadata captured: 2026-08-31
- Licence resolved from the LICENSE on 2026-09-03: LICENSE declares SPDX-License-Identifier: Apache-2.0 OR GPL-2.0. The GitHub API reported `NOASSERTION`, which is why this was read directly.  **Composite - needs a person to confirm.**

## GitHub Snapshot

- Description: SQL powered operating system instrumentation, monitoring, and analytics.
- Language: C++
- License (SPDX): NOASSERTION
- Default Branch: master
- Stars: 23533
- Homepage: https://osquery.io
- Pushed At: 2026-08-25T16:33:00Z
- Topics: hacktoberfest, intrusion-detection, monitoring, security, sql

## Evidence Anchors
- [github_repo] description :: SQL powered operating system instrumentation, monitoring, and analytics. (confidence 0.95)
- [github_repo] language :: C++ (confidence 0.90)
- [github_repo] license :: NOASSERTION (confidence 0.90)
- [github_repo] topics :: hacktoberfest, intrusion-detection, monitoring, security, sql (confidence 0.85)
