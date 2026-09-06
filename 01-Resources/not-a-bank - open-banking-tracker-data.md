---
uuid: "22f85866-642f-5d06-b578-52c51d30b1bc"
canonical_url: "https://github.com/not-a-bank/open-banking-tracker-data"
repo_key: "not-a-bank/open-banking-tracker-data"
owner: "not-a-bank"
repo_name: "open-banking-tracker-data"
aliases: ["not-a-bank/open-banking-tracker-data", "https://github.com/not-a-bank/open-banking-tracker-data"]
type: "data_api_resource"
primary_topic: "Data APIs & Big Data"
secondary_topics: ["Government & Civic Tech", "Geospatial & Earth Data"]
ecosystem: "Python"
domain_primary: "Data"
maturity_stage: "Active"
license_class: "Unknown"
deployment_target: "Server"
interface_protocol: "REST"
data_locality: "Distributed"
hardware_footprint: "High_Memory"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Open Data Portal"]
glossary_terms: ["API", "Dataset", "Open Data", "Endpoint", "Schema", "Rate Limit"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "Unknown"
source_file: "repositories to chart.md"
evidence_count: 5
github_description: "The open banking API directory"
github_language: "Python"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "master"
github_stars: 0
github_topics: ["api", "bank", "banking", "data", "finance", "fintech", "institutions", "obie", "openbanking", "psd2", "tracker"]
github_homepage: "https://www.openbankingtracker.com/"
github_pushed_at: "2026-08-24T22:56:27Z"
github_updated_at: "2026-08-25T12:55:00Z"
---

# not-a-bank - open-banking-tracker-data

## Bottom Line
The dataset behind an open banking API directory: JSON records for account providers and API aggregators, tracking over thirty data points each — sandboxes, APIs, breaches, app availability — validated against JSON schemas.

## What It Solves
- Map which financial institutions are reachable through which aggregator, by country.
- Track open banking coverage as data rather than prose.
- Keep a community dataset consistent through schema validation.

## Architecture & Mechanics
- JSON files split into `data/account-providers/` for banks and `data/api-aggregators/` for platforms such as Plaid and Tink.
- Over thirty data points per organisation, including sandbox availability, APIs offered, known data breaches and mobile apps.
- Every record is validated against a JSON schema, so contributions cannot drift structurally.
- The repository is the data layer; the directory is rendered from it.

## What Is Inside
- **This is a dataset, not software: 57,919 JSON files.** `data/account-providers/` alone is **57,828 files, one per bank or credit union worldwide**, each recording identifiers, API availability, aggregator coverage and metadata. `data/api-aggregators/` (80) and `data/third-party-providers/` (3) cover the other side of the market.
- **Scrapers that keep it current** — `scrapers/` (11 files) and `scripts/` (11), with `scraped-data/` holding raw pulls from GoCardless and Flinks.
- **Validation in CI** — `.github/workflows/validate-data.yml` checks every record on change, and `pr-comment.yml` reports the diff; a worked example of treating a large data corpus as a reviewable artefact.
- **Why this matters far beyond banking:** it is one of the larger openly licensed entity datasets available with per-record provenance, and it is completely invisible from any abstract description of the project. Anyone needing a real-world corpus of institutional records — for entity resolution, for testing extraction, for name-matching — should look here.
- **Two malformed paths exist in the tree** (`"data/` with a stray quote), a small sign of scraper output committed without normalisation.

## Transferable Capability
**Treat a large reference corpus as a reviewed artefact: one record per file, validated on every change, with the difference reported.** Because each entity is a separate file, a change is legible as a change to one thing rather than as a diff in a database dump, and correctness becomes a matter of review rather than trust in a pipeline.

**Alternative to:** a corpus maintained as one large file or behind an API, where contributions cannot be reviewed and provenance per record is lost. **Applies to any curated corpus** that others are expected to trust and contribute to — and the corpus itself is usable wherever a large set of real institutional records is needed.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Data
- Maturity Stage: Active
- License Class: Unknown
- Deployment Target: Server
- Interface Protocol: REST
- Data Locality: Distributed
- Hardware Footprint: High_Memory
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Query open banking coverage programmatically rather than reading a directory.
- Study schema-validated JSON as a contribution model for community datasets.
- Use as a worked example of separating dataset from presentation.

## Reading Notes
**A LICENSE file is present but matches no known
licence.** For a *data* resource this matters more than for a code one: the catalogue's
interest here is the dataset, and redistributing a dataset under undetermined terms is a
different risk from reading source code under them.

## Semantic Links
- [parent_topic:: [[Topic - Data APIs & Big Data]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [implements_pattern:: [[Pattern - Open Data Portal]]]
- [mentions_term:: [[Glossary - API]]]
- [mentions_term:: [[Glossary - Dataset]]]
- [mentions_term:: [[Glossary - Open Data]]]
- [mentions_term:: [[Glossary - Endpoint]]]
- [mentions_term:: [[Glossary - Schema]]]
- [mentions_term:: [[Glossary - Rate Limit]]]

## Evidence
- Source URL: https://github.com/not-a-bank/open-banking-tracker-data
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01

## GitHub Snapshot

- Description: The open banking API directory
- Language: Python
- License: Unknown (UNKNOWN)
- Default Branch: master
- Stars: 0
- Watchers: 0
- Homepage: https://www.openbankingtracker.com/
- Archived: no
- Disabled: no
- Pushed At: 2026-08-24T22:56:27Z
- Updated At: 2026-08-25T12:55:00Z
- Topics: api, bank, banking, data, finance, fintech, institutions, obie, openbanking, psd2, tracker

## Evidence Anchors
- [github_repo] description :: The open banking API directory (confidence 0.95)
- [github_repo] topics :: api, bank, banking, data, finance, fintech, institutions, obie, openbanking, psd2, tracker (confidence 0.82)
- [github_repo] language :: Python (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
