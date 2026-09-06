---
uuid: "f494ba6c-7a8f-58a9-84f6-f3e0bdcf9aee"
canonical_url: "https://github.com/github/government.github.com"
repo_key: "github/government.github.com"
owner: "github"
repo_name: "government.github.com"
aliases: ["github/government.github.com", "https://github.com/github/government.github.com"]
type: "civic_tech_resource"
primary_topic: "Government & Civic Tech"
secondary_topics: ["Data APIs & Big Data", "Infrastructure & Observability"]
ecosystem: "Geo_Data"
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
glossary_terms: ["Civic Tech", "Open Government", "Discovery", "Public Service", "Playbook"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "CC0-1.0"
source_file: "repositories to chart.md"
evidence_count: 6
github_description: "Gather, curate, and feature stories of public servants and civic hackers using GitHub as part of their open government innovations"
github_language: "HTML"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "gh-pages"
github_stars: 0
github_topics: ["government", "open-government", "stories"]
github_homepage: "http://government.github.com/"
github_pushed_at: "2026-08-24T20:25:11Z"
github_updated_at: "2026-08-29T17:54:04Z"
---

# github - government.github.com

## Bottom Line
A Jekyll site on GitHub Pages that collects stories of public servants and civic hackers using GitHub in government work, alongside a data-driven directory of civic-technology and government organisations.

## What It Solves
- Show working examples of open practice in government rather than arguing for it in principle.
- Make government organisations using GitHub discoverable to each other.
- Give civic technologists precedents to cite internally.

## Architecture & Mechanics
- A Jekyll static site built and hosted on GitHub Pages.
- Data files drive a community page listing organisations in civic tech, government and research.
- Stories are contributed by the community through pull requests.
- It is explicitly a tool for and by the community rather than an official product.

## What Is Inside
- **A Jekyll site, and 357 of its 454 files are vendored `node_modules`** — mostly GitHub's own Octicons (186) and Primer CSS packages. The real content is much smaller than the file count suggests.
- **The content** — `_data/` (3 files) is the list of government organisations on GitHub and is what the site is actually for; `_posts/` (10), `_includes/`, `_layouts/`, and `docs/` with three pages worth reading on their own: `accessibility.md`, `best-practices.md`, `gov-cloud.html`.
- **Data quality enforced by CI** — `.github/workflows/ensure-alphabetize.yml` and `ensure-orgs.yml` validate the organisation list on every change, which is a small, copyable pattern for a curated data file.
- **179 SVG files**, almost all icon assets rather than diagrams.
- **Where the value is:** the organisation dataset and the two policy documents. The site machinery is not reusable.

## Transferable Capability
**Keep the compilation as validated data and enforce its rules mechanically, so the list cannot rot into inconsistency.** Ordering, membership and structure checked on every change means the corpus stays usable as a corpus rather than degrading into prose that happens to contain facts.

**Alternative to:** a curated list maintained by convention, which is correct until two people disagree quietly. **Applies to any maintained collection** where the rules of membership are stated and could therefore be checked.

## Taxonomy
- Ecosystem: Geo_Data
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
- Find precedents for open-source practice in the public sector.
- Discover government organisations working openly on GitHub.
- Study data-file-driven static sites as a low-maintenance directory pattern.

## Reading Notes
**The licence is stated in the readme, not in a LICENSE
file.** It reads CC0-1.0 — a public-domain dedication, appropriate for what this is, which is
curated content rather than software. Prose is weaker evidence than a licence file by
construction, so this reading is recorded as needing confirmation rather than settled.

## Semantic Links
- [parent_topic:: [[Topic - Government & Civic Tech]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[alphagov - whitehall]]]
- [related_to:: [[GSA - data.gov]]]
- [related_to:: [[usds - playbook]]]
- [implements_pattern:: [[Pattern - Civic Tech Playbook]]]
- [mentions_term:: [[Glossary - Civic Tech]]]
- [mentions_term:: [[Glossary - Open Government]]]
- [mentions_term:: [[Glossary - Discovery]]]
- [mentions_term:: [[Glossary - Public Service]]]
- [mentions_term:: [[Glossary - Playbook]]]

## Evidence
- Source URL: https://github.com/github/government.github.com
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the readme on 2026-09-03: readme names CC0-1.0 (referred to only). The GitHub API reported `UNKNOWN`, which is why this was read directly.  **Composite - needs a person to confirm.**

## GitHub Snapshot

- Description: Gather, curate, and feature stories of public servants and civic hackers using GitHub as part of their open government innovations
- Language: HTML
- License: Unknown (UNKNOWN)
- Default Branch: gh-pages
- Stars: 0
- Watchers: 0
- Homepage: http://government.github.com/
- Archived: no
- Disabled: no
- Pushed At: 2026-08-24T20:25:11Z
- Updated At: 2026-08-29T17:54:04Z
- Topics: government, open-government, stories

## Evidence Anchors
- [github_repo] description :: Gather, curate, and feature stories of public servants and civic hackers using GitHub as part of their open government innovations (confidence 0.95)
- [github_repo] topics :: government, open-government, stories (confidence 0.82)
- [github_repo] language :: HTML (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
