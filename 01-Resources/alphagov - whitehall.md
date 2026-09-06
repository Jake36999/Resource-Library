---
uuid: "26de675c-fdf7-55b8-8a49-778b65f1cc75"
canonical_url: "https://github.com/alphagov/whitehall"
repo_key: "alphagov/whitehall"
owner: "alphagov"
repo_name: "whitehall"
aliases: ["alphagov/whitehall", "https://github.com/alphagov/whitehall"]
type: "civic_tech_resource"
primary_topic: "Government & Civic Tech"
secondary_topics: ["Data APIs & Big Data", "Infrastructure & Observability"]
ecosystem: "Mixed"
domain_primary: "Civic_Tech"
maturity_stage: "Active"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "Web_UI"
data_locality: "Distributed"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Civic Tech Playbook"]
glossary_terms: ["Civic Tech", "Open Government", "Playbook", "Public Service"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
evidence_count: 6
github_description: "Publishes government content on GOV.UK"
github_language: "Ruby"
github_license: "Unknown"
github_license_spdx: "MIT"
github_default_branch: "main"
github_stars: 0
github_topics: ["govuk"]
github_homepage: "https://docs.publishing.service.gov.uk/apps/whitehall.html"
github_pushed_at: "2026-09-04T11:50:38Z"
github_updated_at: "2026-08-30T12:47:03Z"
---

# alphagov - whitehall

## Bottom Line
The Ruby on Rails publishing application that UK government departments use to author and manage GOV.UK content — the editorial back office behind the public site, not the site itself.

## What It Solves
- Give non-technical government publishers a controlled way to publish to a national website.
- Enforce editorial workflow and auditing on public-sector content.
- Keep publishing consistent across many departments with different needs.

## Architecture & Mechanics
- A Rails application following GOV.UK conventions, run within the GOV.UK Docker environment.
- Content workflows move documents through drafting, review and publication states.
- Auditing records who changed what, which matters for public accountability.
- Internationalisation support covers content published in multiple languages.
- It integrates with the wider GOV.UK publishing platform rather than rendering the public site directly.

## What Is Inside
- **A large Rails application, and the interesting part is the editorial model** — `app/` (1,146 files): `models/` (237), `views/` (449), `presenters/` (71), `services/` (42), `components/` (54). This is the publishing system behind GOV.UK departmental content, so the domain model is *editions, workflow states and attachments*, not pages.
- **Architecture decision records with diagrams** — `docs/adr/`, and unusually the diagrams are **PlantUML source checked in beside the rendered SVG** (`0002-new-asset-model/existing_asset_model.puml` and `.svg`, `existing_scenario.puml` and `.svg`). 42 diagram paths in total.
- **A component library documented as data** — `app/views/components/docs/*.yml` describes each GOV.UK component (`datetime_fields`, `govspeak_editor`, `image_cropper`, `inset_prompt`) in machine-readable form rather than in prose.
- **847 test-related paths** — `test/unit/` (436), `test/functional/` (113), `test/factories/` (105), `test/fixtures/` (54), plus 55 `.feature` files with `features/step_definitions/` (59) for Cucumber acceptance tests.
- **230 database migrations, including data migrations** — `db/migrate/` (141) and `db/data_migration/` (89), the latter carrying real-world renames as CSV (`reslug_her_majesty_to_his_majesty.csv`, `reslug_dit_to_dbt.csv`). A worked record of how a large public site handles content-model change.
- **A published JSON Schema** — `public/configurable-document-type.schema.json`.

## Transferable Capability
**Model the process by which something becomes publishable, not just the thing published.** The unit is a revision with a state and a route through review, so who may change what and when is expressed in the model rather than in convention. The separable practice: **treat changes to the content model itself as recorded, replayable migrations** — including the awkward real-world ones — so the history of what the model meant is preserved rather than overwritten.

**Alternative to:** storing current content and handling review by process outside the system. **Applies wherever** material is produced by several people with different authority and the route to publication is itself the thing that must be reliable.

## Taxonomy
- Ecosystem: Mixed
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
- Study a large production editorial workflow serving many organisations.
- Reference how publishing and rendering are separated in GOV.UK's architecture.
- Examine auditing requirements for public-sector content.

## Semantic Links
- [parent_topic:: [[Topic - Government & Civic Tech]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[GSA - data.gov]]]
- [related_to:: [[usds - playbook]]]
- [related_to:: [[github - government.github.com]]]
- [implements_pattern:: [[Pattern - Civic Tech Playbook]]]
- [mentions_term:: [[Glossary - Civic Tech]]]
- [mentions_term:: [[Glossary - Open Government]]]
- [mentions_term:: [[Glossary - Playbook]]]
- [mentions_term:: [[Glossary - Public Service]]]

## Evidence
- Source URL: https://github.com/alphagov/whitehall
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names MIT (reproduced in full). The GitHub API reported `UNKNOWN`, which is why this was read directly.

## GitHub Snapshot

- Description: Publishes government content on GOV.UK
- Language: Ruby
- License: Unknown (UNKNOWN)
- Default Branch: main
- Stars: 0
- Watchers: 0
- Homepage: https://docs.publishing.service.gov.uk/apps/whitehall.html
- Archived: no
- Disabled: no
- Pushed At: 2026-08-31T07:03:59Z
- Updated At: 2026-08-30T12:47:03Z
- Topics: govuk

## Evidence Anchors
- [github_repo] description :: Publishes government content on GOV.UK (confidence 0.95)
- [github_repo] topics :: govuk (confidence 0.82)
- [github_repo] language :: Ruby (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
