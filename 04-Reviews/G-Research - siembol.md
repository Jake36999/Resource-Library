---
uuid: "ef93ddff-407b-56ef-9dd3-684aa7a79045"
canonical_url: "https://github.com/G-Research/siembol"
repo_key: "G-Research/siembol"
owner: "G-Research"
repo_name: "siembol"
aliases: ["G-Research/siembol", "https://github.com/G-Research/siembol"]
type: "security_resource"
primary_topic: "Security & SIEM"
secondary_topics: ["Infrastructure & Observability", "Data APIs & Big Data"]
ecosystem: "Python"
domain_primary: "Security"
maturity_stage: "Abandoned"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "CLI"
data_locality: "Distributed"
hardware_footprint: "CPU_Only"
security_compliance: "Security_Adjacent"
agent_surface: "None"
patterns: ["Threat Detection Pipeline"]
glossary_terms: ["SIEM", "Threat Detection", "Enrichment", "Alerting"]
status: "review_pending"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "security_adjacent"
license: "Apache-2.0"
source_file: "repositories to chart.md"
evidence_count: 6
github_description: "An open-source, real-time Security Information & Event Management tool based on big data technologies, providing a scalable, advanced security analytics framework. "
github_language: "Java"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "main"
github_stars: 0
github_topics: ["big-data", "cloud", "gr-oss", "metron", "security", "siem"]
github_homepage: "https://siembol.io/"
github_pushed_at: "2025-04-03T11:34:38Z"
github_updated_at: "2026-08-04T23:20:06Z"
---

# G-Research - siembol

## Bottom Line
A real-time SIEM built on big-data streaming infrastructure that normalises, enriches and alerts on security events at scale — archived by G-Research in April 2025 and explicitly no longer maintained.

> Archived by G-Research on 3 April 2025 and explicitly unmaintained. Retained for architectural reference only.

## What It Solves
- Centralise log collection and detect attacks across distributed infrastructure.
- Normalise heterogeneous security events into a common form before applying detection logic.
- Enrich events with context at ingestion rather than at query time.

## Architecture & Mechanics
- Apache Storm provides the stream processing layer for real-time event handling.
- ZooKeeper coordinates distributed configuration across the components.
- The pipeline stages are normalisation, enrichment, then rule evaluation and alerting.
- Archived on 3 April 2025; the repository states it is no longer maintained and invites forking.

## What Is Inside
- **A five-service Java platform, one directory per stage** — `parsing/` (121 files: `parsing-core`, `parsing-app`, a Storm topology), `enriching/` (42), `alerting/` (84, with a rules compiler and a correlation engine), `responding/` (99), `siembol-common/` (95). 619 `.java` files in total.
- **A configuration editor as a first-class product** — `config-editor/` (392 files), an Angular UI (`config-editor-ui`, 214) over `config-editor-core`, `-services`, `-rest` and `-sync`. The premise is that detection rules are edited by analysts through a schema-driven form, so `siembol-common/.../jsonschema/JsonSchemaValidator.java` and the UI's `schema.service.ts` are the load-bearing pieces.
- **Deployment you can lift** — `deployment/helm-k8s/` (45 files including a Kafka traffic generator with `demo_messages.json`), `deployment/docker/` (Dockerfiles per service), `storm-topology-manager/`, `siembol-monitoring/`, and quickstart install scripts for PowerShell and shell.
- **Real parser test corpora** — `parsing/parsing-core/src/test/resources/` includes NetFlow v9 samples; 224 test paths overall.
- **Documentation as a site** — `docs/` (73 files) with deployment how-tos (Kerberos setup, Helm customisation) and an architecture SVG.
- **Held for review** as security-adjacent; the transferable idea is schema-driven rule editing, not the detection content.

## Transferable Capability
**Let the people who own the rules edit them directly, through a form generated from the schema, rather than through the people who own the code.** When a change requires a deployment, the rate of change is set by the deployment process rather than by need. Generating the editing interface from the schema means the interface cannot drift from what the system accepts, and validation happens before anything is saved.

**Alternative to:** configuration edited as files by whoever has access, validated only when it fails. **Applies wherever** the person who knows what the rule should be is not the person who can deploy it.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Security
- Maturity Stage: Abandoned
- License Class: Permissive
- Deployment Target: Server
- Interface Protocol: CLI
- Data Locality: Distributed
- Hardware Footprint: CPU_Only
- Security Compliance: Security_Adjacent
- Agent Surface: None

## Integration & Use Cases
- Study the architecture of a streaming SIEM built on Storm.
- Reference the normalise-enrich-alert pipeline shape when designing detection systems.
- Treat as a historical reference, not a deployment candidate.

## Semantic Links
- [parent_topic:: [[Topic - Security & SIEM]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [implements_pattern:: [[Pattern - Threat Detection Pipeline]]]
- [mentions_term:: [[Glossary - SIEM]]]
- [mentions_term:: [[Glossary - Threat Detection]]]
- [mentions_term:: [[Glossary - Enrichment]]]
- [mentions_term:: [[Glossary - Alerting]]]

## Evidence
- Source URL: https://github.com/G-Research/siembol
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names Apache-2.0 (reproduced in full). The GitHub API reported `UNKNOWN`, which is why this was read directly.

## GitHub Snapshot

- Description: An open-source, real-time Security Information & Event Management tool based on big data technologies, providing a scalable, advanced security analytics framework. 
- Language: Java
- License: Unknown (UNKNOWN)
- Default Branch: main
- Stars: 0
- Watchers: 0
- Homepage: https://siembol.io/
- Archived: yes
- Disabled: no
- Pushed At: 2025-04-03T11:34:38Z
- Updated At: 2026-08-04T23:20:06Z
- Topics: big-data, cloud, gr-oss, metron, security, siem

## Evidence Anchors
- [github_repo] description :: An open-source, real-time Security Information & Event Management tool based on big data technologies, providing a scalable, advanced security analytics framework. (confidence 0.95)
- [github_repo] topics :: big-data, cloud, gr-oss, metron, security, siem (confidence 0.82)
- [github_repo] language :: Java (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
