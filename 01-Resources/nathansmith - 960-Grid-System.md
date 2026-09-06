---
uuid: "06a2b838-89a7-55c9-ae7f-c3a8e664886a"
canonical_url: "https://github.com/nathansmith/960-Grid-System"
repo_key: "nathansmith/960-Grid-System"
owner: "nathansmith"
repo_name: "960-Grid-System"
aliases: ["nathansmith/960-Grid-System", "https://github.com/nathansmith/960-Grid-System"]
type: "frontend_library"
primary_topic: "Frontend & Design Systems"
secondary_topics: ["Architecture & Developer Playbooks", "CAD & SaaS Design"]
ecosystem: "Web_CSS"
domain_primary: "Frontend"
maturity_stage: "Production_Ready"
license_class: "Unknown"
deployment_target: "Browser"
interface_protocol: "Web_UI"
data_locality: "Stateless"
hardware_footprint: "Browser_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Component-Based UI", "Feature Detection"]
glossary_terms: ["Responsive Design", "Component Library", "CSS Reset", "Feature Detection", "DOM"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "Unknown"
source_file: "repositories to chart.md"
evidence_count: 4
github_description: "The 960 Grid System is an effort to streamline web development workflow."
github_language: "CSS"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "master"
github_stars: 0
github_topics: []
github_homepage: "http://960.gs"
github_pushed_at: "2020-08-01T19:11:33Z"
github_updated_at: "2026-08-30T17:34:25Z"
---

# nathansmith - 960-Grid-System

## Bottom Line
An early fixed-width CSS grid built on a 960-pixel container divided into 12 or 16 columns with consistent gutters, shipped alongside matching templates for design tools so designers and developers worked to the same measurements.

> No releases and no recent commit activity. Catalogued as a historical reference rather than a current option.

## What It Solves
- Give designers and developers one shared set of measurements to work to.
- Lay out columns predictably before CSS had grid or flexbox.
- Move from a design comp to markup without recalculating widths.

## Architecture & Mechanics
- A `960.css` stylesheet defines container, column and gutter widths, included alongside optional reset and text stylesheets.
- The 960-pixel container divides into 12 or 16 columns of consistent width.
- Templates ship for Fireworks, Photoshop, OmniGraffle and Visio, plus printable sketch sheets.
- The approach is fixed-width, predating responsive design; the repository has no releases and no recent commits.

## What Is Inside
- **Mostly design-tool templates, not code** — `templates/` (64 of 117 files) carries the grid as native documents for QuarkXPress (15), InDesign (9), Illustrator (6), Corel Draw (3), Expression Design (3), Fireworks (3), Acorn (3), Inkscape and OmniGraffle. 12 `.qxp` and 4 `.psd` files.
- **The CSS is a small part** — `code/css/` (25 files: `960.css`, `960_12_col.css`, `960_24_col.css`, `reset.css`, `text.css`) with `code/demo.html` and `code/demo_24_col.html` showing each in use.
- **Editor plugins** — `app_plugins/fireworks/` (6) and `app_plugins/photoshop/` (2) to draw the grid inside the design tool.
- **Vector grid overlays** — `templates/inkscape/960_grid_12_col.svg`, `16_col`, `24_col`.
- **Why the shape matters:** this is a *design system artefact* more than a library — the value was always the shared grid across design and code, which is why two thirds of it targets tools that no longer dominate. Historically important, practically superseded.

## Transferable Capability
**Agree one spatial scheme and express it in every medium the work passes through**, so a layout means the same thing in the tool where it is drawn and the medium where it is built. The value was never the arithmetic; it was that two roles could refer to the same structure without translating.

**Alternative to:** each stage of a workflow using its own measurements and reconciling by eye. **Applies wherever** an artefact is handed between tools and something must survive the handover — the same problem [[penpot - penpot]] later attacked by collapsing the tools instead.

## Taxonomy
- Ecosystem: Web_CSS
- Domain Primary: Frontend
- Maturity Stage: Production_Ready
- License Class: Unknown
- Deployment Target: Browser
- Interface Protocol: Web_UI
- Data Locality: Stateless
- Hardware Footprint: Browser_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Study how layout was standardised before native CSS grid existed.
- Understand the design-tool-to-code handoff that grid templates were solving.
- Reference a historical baseline when evaluating modern layout systems.

## Reading Notes
**No licence found**, which is a notable gap for a source
this old and this widely copied — 960.gs predates the convention of shipping a LICENSE file,
and its terms were historically stated on its website rather than in the repository. Treat the
absence as unresolved rather than as permission.

## Semantic Links
- [parent_topic:: [[Topic - Frontend & Design Systems]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[twbs - bootstrap]]]
- [related_to:: [[animate-css - animate.css]]]
- [related_to:: [[necolas - normalize.css]]]
- [implements_pattern:: [[Pattern - Component-Based UI]]]
- [implements_pattern:: [[Pattern - Feature Detection]]]
- [mentions_term:: [[Glossary - Responsive Design]]]
- [mentions_term:: [[Glossary - Component Library]]]
- [mentions_term:: [[Glossary - CSS Reset]]]
- [mentions_term:: [[Glossary - Feature Detection]]]
- [mentions_term:: [[Glossary - DOM]]]

## Evidence
- Source URL: https://github.com/nathansmith/960-Grid-System
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01

## GitHub Snapshot

- Description: The 960 Grid System is an effort to streamline web development workflow.
- Language: CSS
- License: Unknown (UNKNOWN)
- Default Branch: master
- Stars: 0
- Watchers: 0
- Homepage: http://960.gs
- Archived: no
- Disabled: no
- Pushed At: 2020-08-01T19:11:33Z
- Updated At: 2026-08-30T17:34:25Z
- Topics: None provided

## Evidence Anchors
- [github_repo] description :: The 960 Grid System is an effort to streamline web development workflow. (confidence 0.95)
- [github_repo] language :: CSS (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
- [seed] repositories to chart.md :: - [ ] https://github.com/nathansmith/960-Grid-System.git (confidence 0.50)
