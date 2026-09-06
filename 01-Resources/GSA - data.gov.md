---
uuid: "1d39d28a-e651-5dc5-aead-785eb48c0a06"
canonical_url: "https://github.com/GSA/data.gov"
repo_key: "GSA/data.gov"
owner: "GSA"
repo_name: "data.gov"
aliases: ["GSA/data.gov", "https://github.com/GSA/data.gov"]
type: "civic_tech_resource"
primary_topic: "Government & Civic Tech"
secondary_topics: ["Data APIs & Big Data", "Infrastructure & Observability"]
ecosystem: "Python"
domain_primary: "Civic_Tech"
maturity_stage: "Active"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "Web_UI"
data_locality: "Distributed"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Open Data Portal", "Civic Tech Playbook"]
glossary_terms: ["API", "Dataset", "Open Data", "Schema", "Civic Tech", "Public Service", "Open Government", "Playbook"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "CC0-1.0"
source_file: "repositories to chart.md"
evidence_count: 6
github_description: "Main repository for the data.gov service"
github_language: "Python"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "main"
github_stars: 0
github_topics: ["ansible", "infrastructure", "provisioning", "stack", "terraform"]
github_homepage: "https://data.gov"
github_pushed_at: "2026-08-27T19:28:30Z"
github_updated_at: "2026-08-30T19:24:15Z"
---

# GSA - data.gov

## Bottom Line
The coordination repository for the US data.gov platform rather than its application code: it tracks the team's work and holds the shared GitHub Actions workflows and infrastructure templates that the platform's other repositories invoke.

## What It Solves
- Coordinate a platform split across several independently deployed repositories.
- Share deployment, security scanning and restart procedures rather than duplicating them per component.
- Give the public a single place to see how a national data platform is run.

## Architecture & Mechanics
- The platform itself is a set of microservices in separate repositories: a static www site on Cloud.gov Pages, catalog and inventory sites both running CKAN 2.11.2, and a harvesting service.
- This repository houses shared GitHub Actions workflow templates that the others call.
- Infrastructure templates standardise deployment and security scanning across components.
- Team planning and issue tracking are conducted here in the open.

## What Is Inside
- **64 files, and almost none of it is the portal.** This repository is the *operations and coordination* repo for data.gov, not its software — the catalogue itself is CKAN, catalogued separately.
- **What is actually here** — `.github/` (29 files, 16 workflows) automating issue triage, app restarts and metrics reports; `metrics/datagov_metrics/` (a small Python package with `pyproject.toml`); `egress/acl/` (6 `.acl` files defining permitted outbound network destinations); `bin/` (7 operational scripts); `ckan/` (a route-checking test and `org_dataset_count.sh`).
- **The one document worth reading** — `docs/open-data-worldwide.md`, a survey of open-data portals in other jurisdictions.
- **Where the value is:** as a worked example of how a public open-data programme is *run* — egress allowlists, restart runbooks as workflows, metrics reporting — rather than as portal software. Read [[ckan - ckan]] for the platform.

## Transferable Capability
**Run the operations of a programme as reviewable artefacts rather than as knowledge held by whoever is on call.** Restart procedures, permitted outbound destinations and reporting all expressed as checked-in definitions, so operating the thing is inspectable and transferable. The narrow, transferable piece: **an explicit allow-list of where a system may talk to**, which turns an implicit trust boundary into a reviewed one.

**Alternative to:** runbooks in prose and network rules configured out of band. **Applies wherever** something must keep running across changes of staff, and wherever egress should be a decision rather than a default.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Civic_Tech
- Maturity Stage: Active
- License Class: Permissive
- Deployment Target: Server
- Interface Protocol: Web_UI
- Data Locality: Distributed
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Study how a national open-data platform is decomposed and operated.
- Reference CKAN deployed at national scale.
- Adopt shared CI templates as a pattern for multi-repository platforms.

## Semantic Links
- [parent_topic:: [[Topic - Government & Civic Tech]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[alphagov - whitehall]]]
- [related_to:: [[usds - playbook]]]
- [related_to:: [[github - government.github.com]]]
- [implements_pattern:: [[Pattern - Open Data Portal]]]
- [implements_pattern:: [[Pattern - Civic Tech Playbook]]]
- [mentions_term:: [[Glossary - API]]]
- [mentions_term:: [[Glossary - Dataset]]]
- [mentions_term:: [[Glossary - Open Data]]]
- [mentions_term:: [[Glossary - Schema]]]
- [mentions_term:: [[Glossary - Civic Tech]]]
- [mentions_term:: [[Glossary - Public Service]]]
- [mentions_term:: [[Glossary - Open Government]]]
- [mentions_term:: [[Glossary - Playbook]]]

## Evidence
- Source URL: https://github.com/GSA/data.gov
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names CC0-1.0 (referred to only). The GitHub API reported `UNKNOWN`, which is why this was read directly.

## GitHub Snapshot

- Description: Main repository for the data.gov service
- Language: Python
- License: Unknown (UNKNOWN)
- Default Branch: main
- Stars: 0
- Watchers: 0
- Homepage: https://data.gov
- Archived: no
- Disabled: no
- Pushed At: 2026-08-27T19:28:30Z
- Updated At: 2026-08-30T19:24:15Z
- Topics: ansible, infrastructure, provisioning, stack, terraform

## Evidence Anchors
- [github_repo] description :: Main repository for the data.gov service (confidence 0.95)
- [github_repo] topics :: ansible, infrastructure, provisioning, stack, terraform (confidence 0.82)
- [github_repo] language :: Python (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
