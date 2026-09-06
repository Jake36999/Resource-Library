---
uuid: "35571da8-1de3-51f2-acef-520bce3e5f9a"
canonical_url: "https://github.com/usds/playbook"
repo_key: "usds/playbook"
owner: "usds"
repo_name: "playbook"
aliases: ["usds/playbook", "https://github.com/usds/playbook"]
type: "civic_tech_resource"
primary_topic: "Government & Civic Tech"
secondary_topics: ["Architecture & Developer Playbooks", "Data APIs & Big Data", "Infrastructure & Observability"]
ecosystem: "Web_CSS"
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
glossary_terms: ["Playbook", "Civic Tech", "Open Government", "Public Service"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "CC0-1.0"
source_file: "repositories to chart.md"
evidence_count: 5
github_description: "The Digital Services Playbook"
github_language: "SCSS"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "gh-pages"
github_stars: 0
github_topics: []
github_homepage: "https://playbook.cio.gov/"
github_pushed_at: "2025-10-20T18:18:28Z"
github_updated_at: "2026-08-26T14:47:09Z"
---

# usds - playbook

## Bottom Line
The US Digital Services Playbook: a set of numbered plays describing practices for building government digital services that work, each drawn from approaches proven in the private sector and in successful government projects.

## What It Solves
- Give agencies concrete practices rather than abstract policy.
- Make the reasons government IT projects fail addressable as named, checkable plays.
- Provide shared language for arguing about how a service should be built.

## Architecture & Mechanics
- Plays are Markdown files in a `_plays` folder, built into a site with Jekyll and Sass.
- Each play states a practice and the checklist that indicates it is being followed.
- The published site is playbook.cio.gov.
- Changes are proposed by pull request or through GitHub's in-browser editor, keeping revision open.

## What Is Inside
- **Thirteen plays, one file each** — `_plays/` is the resource: each play is a short Markdown document with a checklist and key questions, covering user research, agile delivery, procurement and deployment.
- **The rest is a Jekyll theme** — `assets/_sass/` (88 files, including a vendored Bourbon), `_includes/`, `_layouts/`, `pages/`. 89 of 143 files are `.scss`.
- **Two `.docx` files** — printable versions of the playbook, which is how it circulates in the organisations it targets.
- **Where the value is:** the thirteen plays, readable in twenty minutes and directly quotable. The site machinery is not reusable and the content is the artefact.

## Transferable Capability
**State a practice as a short set of questions to ask rather than as a procedure to follow.** A question survives contexts a procedure cannot, because it forces the reader to supply their own situation instead of matching it against an assumed one. Deliberately small — thirteen units, readable in one sitting — because a body of guidance too large to hold in mind is not consulted.

**Alternative to:** a methodology with steps, which fits the situation it was written for and misleads elsewhere. **Applies wherever** guidance must survive contexts its authors did not anticipate — the same problem this catalogue's own [[Source Documentation Standard]] addresses by pairing a floor with an obligation.

## Taxonomy
- Ecosystem: Web_CSS
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
- Adopt a checklist for digital service delivery.
- Reference an authoritative source when arguing for user research or iterative delivery.
- Study plays-plus-checklists as a durable form for organisational guidance.

## Reading Notes
**CC0-1.0, declared in the readme rather than a LICENSE file.** That is
the usual arrangement for US government works, which are not subject to copyright domestically
in the first place. The content is the artefact here, so a content dedication is the right
instrument — but the reading rests on prose and is marked for confirmation.

## Semantic Links
- [parent_topic:: [[Topic - Government & Civic Tech]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[alphagov - whitehall]]]
- [related_to:: [[GSA - data.gov]]]
- [related_to:: [[github - government.github.com]]]
- [implements_pattern:: [[Pattern - Civic Tech Playbook]]]
- [mentions_term:: [[Glossary - Playbook]]]
- [mentions_term:: [[Glossary - Civic Tech]]]
- [mentions_term:: [[Glossary - Open Government]]]
- [mentions_term:: [[Glossary - Public Service]]]

## Evidence
- Source URL: https://github.com/usds/playbook
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the readme on 2026-09-03: readme names CC0-1.0 (referred to only). The GitHub API reported `UNKNOWN`, which is why this was read directly.  **Composite - needs a person to confirm.**

## GitHub Snapshot

- Description: The Digital Services Playbook
- Language: SCSS
- License: Unknown (UNKNOWN)
- Default Branch: gh-pages
- Stars: 0
- Watchers: 0
- Homepage: https://playbook.cio.gov/
- Archived: no
- Disabled: no
- Pushed At: 2025-10-20T18:18:28Z
- Updated At: 2026-08-26T14:47:09Z
- Topics: None provided

## Evidence Anchors
- [github_repo] description :: The Digital Services Playbook (confidence 0.95)
- [github_repo] language :: SCSS (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
- [seed] repositories to chart.md :: - [ ] https://github.com/usds/playbook.git (confidence 0.50)
