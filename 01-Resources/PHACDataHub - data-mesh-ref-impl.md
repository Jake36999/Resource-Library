---
uuid: "797be245-edc7-5970-be60-3560c2f57ef1"
canonical_url: "https://github.com/PHACDataHub/data-mesh-ref-impl"
repo_key: "PHACDataHub/data-mesh-ref-impl"
owner: "PHACDataHub"
repo_name: "data-mesh-ref-impl"
aliases: ["PHACDataHub/data-mesh-ref-impl", "https://github.com/PHACDataHub/data-mesh-ref-impl"]
type: "reference_implementation"
primary_topic: "Data APIs & Big Data"
secondary_topics: ["Government & Civic Tech", "Architecture & Developer Playbooks"]
ecosystem: "Mixed"
domain_primary: "Data"
maturity_stage: "Abandoned"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "CLI"
data_locality: "Distributed"
hardware_footprint: "High_Memory"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Policy As Schema", "Reference Architecture"]
glossary_terms: ["Data Mesh", "Metadata Catalog", "Knowledge Graph", "Schema"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-03"
evidence_count: 5
github_description: "Data Mesh Reference Implementation with standalone example use cases"
github_language: "TypeScript"
github_license_spdx: "Apache-2.0"
github_default_branch: "main"
github_stars: 8
github_topics: ["docker", "kafka", "neo4j", "neodash", "nlp"]
github_homepage: "Unknown"
github_pushed_at: "2025-01-14T17:58:40Z"
---
# PHACDataHub - data-mesh-ref-impl

## Bottom Line
Six unconnected public-health proof-of-concepts under one repository name, of which one matters: PARADIRE's Access Control Gateway, where the federation's data-sharing policy is a GraphQL schema whose custom directives hash, redact, coarsen or drop each field.

## What It Solves
- Sharing health data between jurisdictions that are not permitted to pool it — the province keeps its data, the federal government sends queries, and a gateway constrains both the query and the result.
- Making a data-sharing agreement into an artefact both parties can read, diff and version, rather than a body of gateway code.
- Demonstrating in-stream event processing, ontology-derived knowledge graphs and NLP pipelines on real public-health data, one worked example at a time.

## Architecture & Mechanics
- The tree is six standalone stacks sharing no code: `paradire/` (544 files, federated analytics), `movie/` (117, an NLP recommendation cluster), `nlp_pipeline/` (115, GPHIN with human analysts), `usvdm/` (108, Kafka vaccination streams), `faers/` (97, FDA adverse events), `kg/` (65, a Disease Ontology knowledge graph), plus `pipelayer/`.
- The Access Control Gateway is a Kafka worker: a YAML ruleset is compiled into a GraphQL schema with the policy expressed as custom directives — `@hash` (one-way hash), `@restrict` (replace with `** restricted **`), `@selectable` (remove the field), `@date` (coarsen to a format mask), `@topic` (bind to a Kafka topic).
- The ruleset is reconfigurable at runtime by posting to the `acg-config-connector` topic, and the gateway is decoupled from both ends, connecting only to the two event brokers.
- `paradire/doc/` is four parts, each with a declared audience, ending with “Looking forward with hindsight” — a written review of what was not achieved.

## What Is Inside
- **Six unconnected proof-of-concepts sharing no code** — `paradire/` (544 files, federated
  analytics across 13 provincial clusters and one federal), `movie/` (117, an NLP recommendation
  cluster), `nlp_pipeline/` (115, GPHIN with human analysts), `usvdm/` (108, Kafka vaccination
  streams), `faers/` (97, FDA adverse events), `kg/` (65, a Disease Ontology knowledge graph),
  `pipelayer/` (79).
- **The piece worth the visit** — `paradire/analytics/acg/`: a Kafka worker compiling a YAML
  ruleset into a GraphQL schema, with the policy as custom directives in `src/directives.ts`
  (`@hash`, `@restrict`, `@selectable`, `@date`, `@topic`).
- **Four-part design documentation** — `paradire/doc/part-i.md` through `part-iv.md`, each with
  a declared audience; Part II is the gateway design, Part IV is "Looking forward with
  hindsight", a written review of what was not achieved.
- **Deployment topology** — separate compose files for federal cluster, provincial cluster,
  and the gateway with and without governance.
- **Experiments left in place** — `paradire/experiments/graphql-kafka`, `graphql-neo4j`.

## Transferable Capability
**Express what a party may ask for, and what they may receive, as annotations on a schema rather than as code in a gateway.** The permitted questions and the permitted answers become one diffable, reviewable artefact, editable by whoever owns the decision rather than by whoever maintains the filter. Per-field treatments compose declaratively — obscure this, coarsen that, remove the other — and the ruleset can be replaced while running.

**Alternative to:** access control implemented as branching logic inside the service that serves the data, where the policy exists only as the behaviour of code and can be read only by reading it. **Applies wherever** two parties must agree in advance on what may be asked and what may be returned, and the agreement needs to outlive the implementation — federated queries, tenant isolation, redaction, or any interface exposed to something you do not control.

## Taxonomy
- Ecosystem: Mixed
- Domain Primary: Data
- Maturity Stage: Abandoned
- License Class: Permissive
- Deployment Target: Server
- Interface Protocol: CLI
- Data Locality: Distributed
- Hardware Footprint: High_Memory
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Read PARADIRE Part II before designing any cross-organisation data-sharing gateway.
- Take the policy-as-schema idea into any setting where a non-engineer owns the policy.
- Treat each subdirectory as an independent worked example, never as a framework.

## Reading Notes
**“Reference implementation” here means worked examples, not a deployable architecture.** There is no shared data-mesh framework and nothing is packaged for reuse; adopting it as a template would be a mistake. Environment assumptions are heavy and specific — the knowledge-graph case opens by requiring a cloud VM with an Nvidia T4, and PARADIRE assumes fourteen Kubernetes clusters. Last pushed 2025-01-14, roughly twenty months stale at the time of this pass. Real institutional work with real documentation, no longer being touched.

## Semantic Links
- [parent_topic:: [[Topic - Data APIs & Big Data]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[Victor-Kipruto-Rop - medallion-lakehouse-platform]]]
- [related_to:: [[GSA - data.gov]]]
- [related_to:: [[open-metadata - OpenMetadata]]]
- [implements_pattern:: [[Pattern - Policy As Schema]]]
- [implements_pattern:: [[Pattern - Reference Architecture]]]
- [mentions_term:: [[Glossary - Data Mesh]]]
- [mentions_term:: [[Glossary - Metadata Catalog]]]
- [mentions_term:: [[Glossary - Knowledge Graph]]]
- [mentions_term:: [[Glossary - Schema]]]

## Evidence
- Source URL: https://github.com/PHACDataHub/data-mesh-ref-impl
- Source kind: GitHub REST metadata plus the repository tree and files, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-03
- Depth of read: recorded per source in [[Scouting Working File 2026-09-03]]

## GitHub Snapshot

- Description: Data Mesh Reference Implementation with standalone example use cases
- Language: TypeScript
- License (SPDX): Apache-2.0
- Default Branch: main
- Stars: 8
- Homepage: Unknown
- Pushed At: 2025-01-14T17:58:40Z
- Topics: docker, kafka, neo4j, neodash, nlp

## Evidence Anchors
- [github_repo] description :: Data Mesh Reference Implementation with standalone example use cases (confidence 0.95)
- [github_repo] language :: TypeScript (confidence 0.90)
- [github_repo] license :: Apache-2.0 (confidence 0.90)
- [github_repo] topics :: docker, kafka, neo4j, neodash, nlp (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-03 (confidence 0.95)
