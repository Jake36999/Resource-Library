---
uuid: "8e400a48-2504-52ad-9add-a168656bc773"
canonical_url: "https://github.com/ckan/ckan"
repo_key: "ckan/ckan"
owner: "ckan"
repo_name: "ckan"
aliases: ["ckan/ckan", "https://github.com/ckan/ckan"]
type: "data_platform"
primary_topic: "Data APIs & Big Data"
secondary_topics: ["Government & Civic Tech", "Geospatial & Earth Data"]
ecosystem: "Data_Platform"
domain_primary: "Data"
maturity_stage: "Production_Ready"
license_class: "Copyleft"
deployment_target: "Server"
interface_protocol: "REST"
data_locality: "Distributed"
hardware_footprint: "High_Memory"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Open Data Portal", "Schema Mapping", "ETL API Ingestion"]
glossary_terms: ["Open Data", "Dataset", "Data Portal", "API", "Schema"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "AGPL-3.0 AND BSD-3-Clause"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-05"
evidence_count: 5
github_description: "CKAN is an open-source DMS for powering data hubs and data portals. CKAN makes it easy to publish, share and use data."
github_language: "Python"
github_license_spdx: "NOASSERTION"
github_default_branch: "master"
github_stars: 5105
github_topics: ["api", "catalog", "ckan", "ckanext", "data", "digitalpublicgoods", "dpg", "open-data", "python", "sdg16"]
github_homepage: "https://ckan.org/"
github_pushed_at: "2026-09-02T11:52:45Z"
---
# ckan - ckan

## Bottom Line
The data management system behind a large share of national and municipal open-data portals, providing dataset catalogues, harvesting, versioned metadata and a full REST API.

## What It Solves
- Publish datasets with consistent, searchable metadata rather than a folder of files.
- Harvest catalogues from other portals to federate discovery.
- Expose everything the web UI shows through an API for machine consumers.

## Architecture & Mechanics
- Datasets are modelled as packages with resources, tags and extensible metadata schemas.
- Solr powers faceted search over catalogue metadata.
- A DataStore layer offers tabular query access to uploaded resources.
- An extension system (ckanext) adds harvesters, spatial search and auth integrations.

## What Is Inside
- **A plugin-first core** — `ckan/` (1,618 files) and `ckanext/` (803), where the extensions are the demonstration: `activity/` (219), `datatablesview/` (111), `datastore/` (60, a queryable per-dataset table store), `tabledesigner/` (38), `datapusher/` (25), `tracking/` (23).
- **A theming tutorial that is itself a working extension** — `ckanext/example_theme_docs/` (90 files) steps through customisation as a sequence of runnable plugins (`custom_config_setting/`, and siblings), which is a documentation pattern worth copying.
- **API usage examples in four languages, as templates** — `ckanext/datastore/templates/datastore/api_examples/`: `curl.html`, `javascript.html`, `powershell.html` and more, rendered into the UI beside the data they describe.
- **Two complete front-end themes** — `ckan/public/` (335) and `ckan/public-midnight-blue/` (330), with matching template trees, showing how far the theming layer actually reaches.
- **Internationalisation at scale** — `ckan/i18n/` (115 files).
- **115 database migrations** with Alembic (`ckan/migration/`), 294 test paths, Cypress browser tests (`cypress/`, 28), and a devcontainer with a Postgres init script that creates the test database.
- **Documentation for operators, not just developers** — `doc/maintaining/` (32) including install-from-docker-compose, `doc/theming/` (17), `doc/extensions/` (15).

## Transferable Capability
**Make the extension mechanism the primary structure, then build the product out of extensions so the mechanism is proved by use.** A plugin surface that the core itself does not depend on is a plugin surface nobody has tested. The related teaching move: **document the extension points as a sequence of working extensions**, each one runnable, rather than as prose about how extending works.

**Alternative to:** a core with hooks added afterwards for other people; and to extension documentation written as description. **Applies wherever** a system must be adapted by people who did not build it — and the second idea applies to any documentation that explains a mechanism the reader is expected to use.

## Taxonomy
- Ecosystem: Data_Platform
- Domain Primary: Data
- Maturity Stage: Production_Ready
- License Class: Copyleft
- Deployment Target: Server
- Interface Protocol: REST
- Data Locality: Distributed
- Hardware Footprint: High_Memory
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Stand up an organisational or municipal open-data portal.
- Federate dataset discovery across several existing catalogues.
- Study metadata modelling for heterogeneous public datasets.

## Reading Notes
**Its licence is not the permissive one a data-portal reader might assume.** The GitHub
API reports `NOASSERTION`; the LICENSE reproduces **AGPL-3.0 and BSD-3-Clause** in full, and
the AGPL governs. That matters more than usual for this particular source: CKAN is deployed
as a network service, and the AGPL's distribution trigger includes serving users over a
network, so running a modified CKAN publicly carries a source obligation that neither the
BSD portion nor the API's silence would warn you about.

## Semantic Links
- [parent_topic:: [[Topic - Data APIs & Big Data]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[GSA - data.gov]]]
- [related_to:: [[public-apis - public-apis]]]
- [related_to:: [[github - government.github.com]]]
- [implements_pattern:: [[Pattern - Open Data Portal]]]
- [implements_pattern:: [[Pattern - Schema Mapping]]]
- [implements_pattern:: [[Pattern - ETL API Ingestion]]]
- [mentions_term:: [[Glossary - Open Data]]]
- [mentions_term:: [[Glossary - Dataset]]]
- [mentions_term:: [[Glossary - Data Portal]]]
- [mentions_term:: [[Glossary - API]]]
- [mentions_term:: [[Glossary - Schema]]]

## Evidence
- Source URL: https://github.com/ckan/ckan
- Source kind: GitHub REST metadata plus maintainer documentation
- Ingestion mode: agent-curated note authored against live repository metadata
- Metadata captured: 2026-08-31
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names AGPL-3.0, BSD-3-Clause (2 reproduced in full, 0 referred to). The GitHub API reported `NOASSERTION`, which is why this was read directly.  **Composite - needs a person to confirm.**

## GitHub Snapshot

- Description: CKAN is an open-source DMS for powering data hubs and data portals. CKAN makes it easy to publish, share and use data.
- Language: Python
- License (SPDX): NOASSERTION
- Default Branch: master
- Stars: 5105
- Homepage: https://ckan.org/
- Pushed At: 2026-08-31T03:50:32Z
- Topics: api, catalog, ckan, ckanext, data, digitalpublicgoods, dpg, open-data, python, sdg16

## Evidence Anchors
- [github_repo] description :: CKAN is an open-source DMS for powering data hubs and data portals. CKAN makes it easy to publish, share and use data. (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: NOASSERTION (confidence 0.90)
- [github_repo] topics :: api, catalog, ckan, ckanext, data, digitalpublicgoods, dpg, open-data, python, sdg16 (confidence 0.85)
