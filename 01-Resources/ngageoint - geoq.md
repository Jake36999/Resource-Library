---
uuid: "aadd3d2d-ca03-5214-800d-700c66080555"
canonical_url: "https://github.com/ngageoint/geoq"
repo_key: "ngageoint/geoq"
owner: "ngageoint"
repo_name: "geoq"
aliases: ["ngageoint/geoq", "https://github.com/ngageoint/geoq"]
type: "geospatial_resource"
primary_topic: "Geospatial & Earth Data"
secondary_topics: ["Government & Civic Tech", "Data APIs & Big Data"]
ecosystem: "Geo_Data"
domain_primary: "Geospatial"
maturity_stage: "Active"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "REST"
data_locality: "Distributed"
hardware_footprint: "High_Memory"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Spatial Ingestion"]
glossary_terms: ["Geospatial Data", "GeoJSON", "STAC", "Satellite Imagery"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
evidence_count: 5
github_description: "Django web application to collect geospatial features and manage feature collection among groups of users"
github_language: "JavaScript"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "develop"
github_stars: 0
github_topics: []
github_homepage: ""
github_pushed_at: "2022-12-08T09:45:02Z"
github_updated_at: "2026-08-29T04:04:07Z"
---

# ngageoint - geoq

## Bottom Line
A geographic tasking system that divides a large area of interest into roughly 1 km grid cells, assigns them to team members, and tracks which have been worked — so a mapping effort covers everything once rather than duplicating some areas and missing others.

## What It Solves
- Coordinate many people observing a large area without overlapping or leaving gaps.
- Make progress visible so groups know what remains and what is done.
- Break an unmanageable area into assignable units of work.

## Architecture & Mechanics
- A large area of interest is subdivided into small grid cells, around a kilometre across.
- Cells are assigned to workers and carry a workflow status through to completion.
- Transparency of status across all groups is the mechanism that prevents duplicated effort.
- Developed by the National Geospatial-Intelligence Agency with MITRE; MIT licensed.

## What Is Inside
- **A Django application organised by concern** — `geoq/`: `core/` (186 files), `static/` (336, mostly vendored front-end assets), `accounts/` (50), `maps/` (45), `workflow/` (20), `feedback/` (21), `proxy/` (11). The `workflow/` and `core/` apps carry the actual model: projects, jobs, areas of interest and per-feature assignment.
- **Seeded reference data** — `geoq/core/fixtures/initial_data.json` and `sample_projects/`, plus `geoq/static/world_cells/counties/cb_2013_us_county_20m.dbf`, a US county shapefile component bundled for the grid system.
- **One focused operator document** — `docs/ADDING-LAYERS.md`, on registering map services.
- **Deployment** — `Dockerfile`, `docker-compose.yml` and a separate `docker-production.yml`.
- **Thin on tests** — 13 test paths across the apps. Judge accordingly.

## Transferable Capability
**Divide a large piece of work into addressable units and track the state of each, so many people can contribute to one task without colliding.** The value is the assignment and completion model — who has which unit, which are done, which need review — which is independent of what the units contain.

**Alternative to:** coordinating a distributed effort by communication, where progress is whatever people report. **Applies wherever** a body of work is too large for one person and must be partitioned, claimed and reassembled.

## Taxonomy
- Ecosystem: Geo_Data
- Domain Primary: Geospatial
- Maturity Stage: Active
- License Class: Permissive
- Deployment Target: Server
- Interface Protocol: REST
- Data Locality: Distributed
- Hardware Footprint: High_Memory
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Coordinate distributed mapping or damage assessment after an event.
- Study grid-based work allocation as a coordination pattern beyond geospatial work.
- Reference an agency-built open-source geospatial workflow tool.

## Semantic Links
- [parent_topic:: [[Topic - Geospatial & Earth Data]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [implements_pattern:: [[Pattern - Spatial Ingestion]]]
- [mentions_term:: [[Glossary - Geospatial Data]]]
- [mentions_term:: [[Glossary - GeoJSON]]]
- [mentions_term:: [[Glossary - STAC]]]
- [mentions_term:: [[Glossary - Satellite Imagery]]]

## Evidence
- Source URL: https://github.com/ngageoint/geoq
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names MIT (reproduced in full). The GitHub API reported `UNKNOWN`, which is why this was read directly.

## GitHub Snapshot

- Description: Django web application to collect geospatial features and manage feature collection among groups of users
- Language: JavaScript
- License: Unknown (UNKNOWN)
- Default Branch: develop
- Stars: 0
- Watchers: 0
- Homepage: None provided
- Archived: no
- Disabled: no
- Pushed At: 2022-12-08T09:45:02Z
- Updated At: 2026-08-29T04:04:07Z
- Topics: None provided

## Evidence Anchors
- [github_repo] description :: Django web application to collect geospatial features and manage feature collection among groups of users (confidence 0.95)
- [github_repo] language :: JavaScript (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
- [seed] repositories to chart.md :: - [ ] https://github.com/ngageoint/geoq.git (confidence 0.50)
