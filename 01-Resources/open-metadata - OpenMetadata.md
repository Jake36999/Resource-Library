---
uuid: "cf4fa5fb-6fe2-5971-afed-c157047b6246"
canonical_url: "https://github.com/open-metadata/OpenMetadata"
repo_key: "open-metadata/OpenMetadata"
owner: "open-metadata"
repo_name: "OpenMetadata"
aliases: ["open-metadata/OpenMetadata", "https://github.com/open-metadata/OpenMetadata"]
type: "data_platform"
primary_topic: "Data APIs & Big Data"
secondary_topics: ["Knowledge Management", "Infrastructure & Observability"]
ecosystem: "Data_Platform"
domain_primary: "Data"
maturity_stage: "Production_Ready"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "REST"
data_locality: "Distributed"
hardware_footprint: "High_Memory"
security_compliance: "Uncertified"
agent_surface: "Callable"
patterns: ["Metadata Harvesting", "Schema-First Codegen", "Programmatic Labelling"]
glossary_terms: ["Metadata Catalog", "Data Lineage", "Semantic Layer", "Schema", "Model Context Protocol"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-03"
evidence_count: 5
github_description: "The Open Context Layer for Data and AI ,  OpenMetadata is the open platform for building trusted data context and business semantics for humans, AI assistants, and agents."
github_language: "TypeScript"
github_license_spdx: "Apache-2.0"
github_default_branch: "main"
github_stars: 15098
github_topics: ["context", "context-layer", "data-catalog", "data-collaboration", "data-contracts", "data-discovery", "data-governance", "data-lineage", "data-observability", "data-profiling", "data-quality", "datadiscovery", "dataquality", "mcp", "mcp-server", "metadata", "metadata-management", "ontologies", "ontologies-api", "semantics"]
github_homepage: "https://open-metadata.org"
github_pushed_at: "2026-09-03T15:55:24Z"
---
# open-metadata - OpenMetadata

## Bottom Line
A metadata catalogue whose entire type system is 904 JSON Schemas, from which the Java, Python and TypeScript models are generated — so no binding can drift — fed by 120+ ingestion connectors that reach the backend through the same public REST API everyone else uses.

## What It Solves
- Nobody knowing what data exists, who owns it, or what breaks when a column changes.
- Column-level lineage across warehouses, pipelines and dashboards, derived from query logs and pipeline definitions rather than declared by hand.
- Finding sensitive columns automatically instead of by survey.

## Architecture & Mechanics
- One Java backend (Dropwizard/JAX-RS) over MySQL or Postgres and Elasticsearch or OpenSearch, a React SPA, and a Python ingestion framework — `ARCHITECTURE.md` traces all three request paths concretely.
- **Schema-first**: `openmetadata-spec` holds 904 JSON Schemas (380 entity, 245 API, 121 type) and every language binding is generated from them; the UI's `generated/` tree is described as a pure sink that nothing imports upward into.
- **Ingestion is a client, not a privileged path**: a connector source yields entities through a producer/processor topology and the sink POSTs them to the same REST API.
- **Auto-classification is a weak-supervision stack in disguise**: `ingestion/src/metadata/pii/` combines Presidio recognisers, a NER pass, column-name patterns, engineered features, a `tag_scoring.py` stage and a `conflict_resolver.py`.
- Search uses shaded Elasticsearch and OpenSearch clients relocated behind `es.*`/`os.*` so both can link at once.

## What Is Inside
- **904 JSON Schemas** — `openmetadata-spec/src/main/resources/json/schema/`: 380 entity,
  245 api, 121 type, 48 configuration, 48 metadataIngestion, 32 governance, 30 security,
  22 auth, 21 dataInsight, 17 events, 13 tests. Java, Python and TypeScript models are generated
  from these.
- **120+ ingestion connectors** — `ingestion/src/metadata/ingestion/source/`, 71 for databases
  alone, each resolved through a `service_spec.py`.
- **A PII classification stack** — `ingestion/src/metadata/pii/`: `algorithms/classifiers.py`,
  `column_patterns.py`, `feature_extraction.py`, `presidio_recognizer_factory.py`,
  `presidio_patches.py`, `tag_scoring.py`, plus `conflict_resolver.py` and `ner.py`.
- **Lineage plumbing** — `ingestion/src/airflow_provider_openmetadata/lineage/` (backend,
  callback, operator, runner) and per-connector lineage workflows
  (`examples/workflows/*_lineage.yaml`).
- **An MCP server** — `openmetadata-mcp/`.
- **A 184-file contributor plugin** — `skills/` with `.claude-plugin`, covering connector
  building and audit, code review, TDD, systematic debugging, Playwright validation and PR
  checklists. Alongside `AGENTS.md`, `CLAUDE.md`, `.claude/rules/` and `openspec/`.
- **Documents worth reading on their own** — `ARCHITECTURE.md` (measured, with a "look here
  first" column), `THREAT_MODEL.md`, `INCIDENT_RESPONSE.md`, and an ADR on governance workflows.

## Transferable Capability
**Define every shape once in a machine-readable schema and generate every language's version of it, so no representation can drift from the definition.** Nothing that touches the data is hand-written, so agreement between components stops being a discipline and becomes a property. The second, separable move: the component that populates the store writes through the same public interface as every other client, so there is no privileged path that can diverge from the documented one.

**Alternative to:** a specification written in prose with implementations kept in step by review; and to an ingestion path with special access, which is how a system acquires two incompatible ways of doing the same thing. A third capability, separable from both: **the catalogue is reachable as a set of typed questions an automated consumer can call**, and the contribution procedure around it is shipped as executable skills rather than as a written guide. **Applies wherever** more than one thing must agree about the shape of a record — languages, services, or a schema and the tooling that validates it.

## Taxonomy
- Ecosystem: Data_Platform
- Domain Primary: Data
- Maturity Stage: Production_Ready
- License Class: Permissive
- Deployment Target: Server
- Interface Protocol: REST
- Data Locality: Distributed
- Hardware Footprint: High_Memory
- Security Compliance: Uncertified
- Agent Surface: Callable

## Integration & Use Cases
- Stand up an organisation-wide catalogue with lineage and governance.
- Take the schema-first codegen discipline and leave the platform.
- Study `ARCHITECTURE.md` as a model of a documentation artefact that states its own provenance.

## Reading Notes
Two observations about the repository as an artefact. `ARCHITECTURE.md` declares how its own numbers were obtained — "module edges from the POMs; package/import counts by grep/Tarjan" — gives a “look here first” column per module, and states where layering **fails** rather than describing an intended architecture. And the project ships an agent plugin for its own contributors: `skills/` is a 184-file `.claude-plugin` covering connector building, connector audit, code review, TDD and PR checklists, alongside `AGENTS.md`, `CLAUDE.md` and an `openspec/` directory. Operationally this is a platform, not a library: a JVM, a relational database, a search cluster and Airflow are all required.

## Semantic Links
- [parent_topic:: [[Topic - Data APIs & Big Data]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[neo4j-labs - neocarta]]]
- [related_to:: [[ckan - ckan]]]
- [related_to:: [[apache - airflow]]]
- [related_to:: [[snorkel-team - snorkel]]]
- [implements_pattern:: [[Pattern - Metadata Harvesting]]]
- [implements_pattern:: [[Pattern - Schema-First Codegen]]]
- [implements_pattern:: [[Pattern - Programmatic Labelling]]]
- [mentions_term:: [[Glossary - Metadata Catalog]]]
- [mentions_term:: [[Glossary - Data Lineage]]]
- [mentions_term:: [[Glossary - Semantic Layer]]]
- [mentions_term:: [[Glossary - Schema]]]
- [mentions_term:: [[Glossary - Model Context Protocol]]]

## Evidence
- Source URL: https://github.com/open-metadata/OpenMetadata
- Source kind: GitHub REST metadata plus the repository tree and files, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-03
- Depth of read: recorded per source in [[Scouting Working File 2026-09-03]]

## GitHub Snapshot

- Description: The Open Context Layer for Data and AI ,  OpenMetadata is the open platform for building trusted data context and business semantics for humans, AI assistants, and agents.
- Language: TypeScript
- License (SPDX): Apache-2.0
- Default Branch: main
- Stars: 15098
- Homepage: https://open-metadata.org
- Pushed At: 2026-09-03T15:55:24Z
- Topics: context, context-layer, data-catalog, data-collaboration, data-contracts, data-discovery, data-governance, data-lineage, data-observability, data-profiling, data-quality, datadiscovery, dataquality, mcp, mcp-server, metadata, metadata-management, ontologies, ontologies-api, semantics

## Evidence Anchors
- [github_repo] description :: The Open Context Layer for Data and AI ,  OpenMetadata is the open platform for building trusted data context and business semantics for humans, AI assistants, and agents. (confidence 0.95)
- [github_repo] language :: TypeScript (confidence 0.90)
- [github_repo] license :: Apache-2.0 (confidence 0.90)
- [github_repo] topics :: context, context-layer, data-catalog, data-collaboration, data-contracts, data-discovery, data-governance, data-lineage, data-observability, data-profiling, data-quality, datadiscovery, dataquality, mcp, mcp-server, metadata, metadata-management, ontologies, ontologies-api, semantics (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-03 (confidence 0.95)
