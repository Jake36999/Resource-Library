---
uuid: "23ae49b6-e2a5-50ec-84fd-6d631e6aafbf"
canonical_url: "https://github.com/public-apis/public-apis"
repo_key: "public-apis/public-apis"
owner: "public-apis"
repo_name: "public-apis"
aliases: ["public-apis/public-apis", "https://github.com/public-apis/public-apis"]
type: "reference_list"
primary_topic: "Data APIs & Big Data"
secondary_topics: ["Curated Aggregators & Reference Lists"]
ecosystem: "Markdown"
domain_primary: "Data"
maturity_stage: "Reference"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Markdown"
data_locality: "Stateless"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Curated Resource Curation", "ETL API Ingestion"]
glossary_terms: ["API", "Endpoint", "Dataset", "Rate Limit", "Curation"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-08-31"
evidence_count: 4
github_description: "A collective list of free APIs"
github_language: "Python"
github_license_spdx: "MIT"
github_default_branch: "master"
github_stars: 473711
github_topics: ["api", "apis", "dataset", "development", "free", "list", "lists", "open-source", "public", "public-api", "public-apis", "resources", "software"]
github_homepage: "https://APILayer.com/"
github_pushed_at: "2026-08-30T16:27:33Z"
container: true
container_kind: "api_directory"
expansion_status: "pending"
expansion_selector: "markdown_table:README.md"
child_count: 0
---
# public-apis - public-apis

## Bottom Line
The largest maintained directory of free and public APIs, tabulated by category with auth type, HTTPS support and CORS policy for each entry.

## What It Solves
- Find a data source for a prototype without trawling vendor marketing pages.
- Compare auth requirements and CORS behaviour before committing to an integration.
- Seed a data-ingestion catalogue with hundreds of candidate endpoints.

## Architecture & Mechanics
- Entries are markdown tables grouped by domain category.
- Each row records description, auth mechanism, HTTPS and CORS support.
- Contribution tooling validates link health and table formatting on pull requests.
- The list is mirrored by a JSON API for programmatic consumption.

## What Is Inside
- **23 files, and the tooling is more interesting than the list** — `README.md` is the resource, but `scripts/validate/` and `scripts/tests/` (3 files each) enforce its format automatically: link liveness, alphabetisation, column structure and duplicate detection, run by `.github/workflows/validate_links.yml`.
- **Why that matters here:** it is the clearest small example in the catalogue of *a curated list treated as validated data* rather than as prose. The scripts are directly adaptable to any link corpus, including this vault's own.
- **No vendored content.** Every API entry is an outbound link with auth, HTTPS and CORS recorded as columns — which makes the list filterable, and is the reason it outlasted its many imitators.

## Transferable Capability
**Record each entry against the same small set of properties, so a compilation can be filtered instead of only read.** Deciding in advance what will be recorded about every item is what converts a list into something answerable — *which of these need no credentials* is a question a table can answer and prose cannot. The enforcement matters as much as the schema: **checked automatically on every change**, so the structure survives contribution.

**Alternative to:** a list of names and links, where every question requires reading everything. **Applies to every compilation** whose entries differ along dimensions somebody will want to filter on — which is the difference between a directory and a reference.

## Taxonomy
- Ecosystem: Markdown
- Domain Primary: Data
- Maturity Stage: Reference
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Markdown
- Data Locality: Stateless
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Shortlist candidate APIs when scoping a new data product.
- Bulk-import entries as seed rows for a catalogue or knowledge graph.
- Teach API integration with low-friction, no-key endpoints.

## Semantic Links
- [parent_topic:: [[Topic - Data APIs & Big Data]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [expansion_spec:: [[Schema Extension - Containers and Papers]]]
- [related_to:: [[not-a-bank - open-banking-tracker-data]]]
- [related_to:: [[ckan - ckan]]]
- [related_to:: [[GSA - data.gov]]]
- [implements_pattern:: [[Pattern - Curated Resource Curation]]]
- [implements_pattern:: [[Pattern - ETL API Ingestion]]]
- [mentions_term:: [[Glossary - API]]]
- [mentions_term:: [[Glossary - Endpoint]]]
- [mentions_term:: [[Glossary - Dataset]]]
- [mentions_term:: [[Glossary - Rate Limit]]]
- [mentions_term:: [[Glossary - Curation]]]

## Evidence
- Source URL: https://github.com/public-apis/public-apis
- Source kind: GitHub REST metadata plus maintainer documentation
- Ingestion mode: agent-curated note authored against live repository metadata
- Metadata captured: 2026-08-31

## GitHub Snapshot

- Description: A collective list of free APIs
- Language: Python
- License (SPDX): MIT
- Default Branch: master
- Stars: 473711
- Homepage: https://APILayer.com/
- Pushed At: 2026-08-30T16:27:33Z
- Topics: api, apis, dataset, development, free, list, lists, open-source, public, public-api, public-apis, resources, software

## Evidence Anchors
- [github_repo] description :: A collective list of free APIs (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: MIT (confidence 0.90)
- [github_repo] topics :: api, apis, dataset, development, free, list, lists, open-source, public, public-api, public-apis, resources, software (confidence 0.85)
