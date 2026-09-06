---
uuid: "12205153-6d73-5f3b-a407-420acc4ff033"
canonical_url: "https://github.com/penpot/penpot"
repo_key: "penpot/penpot"
owner: "penpot"
repo_name: "penpot"
aliases: ["penpot/penpot", "https://github.com/penpot/penpot"]
type: "design_platform"
primary_topic: "CAD & SaaS Design"
secondary_topics: ["Frontend & Design Systems"]
ecosystem: "Web_Frontend"
domain_primary: "Design"
maturity_stage: "Production_Ready"
license_class: "Weak_Copyleft"
deployment_target: "Server"
interface_protocol: "Web_UI"
data_locality: "Distributed"
hardware_footprint: "High_Memory"
security_compliance: "Uncertified"
agent_surface: "Callable"
patterns: ["SaaS Product Design", "Component-Based UI"]
glossary_terms: ["SaaS", "Product Design", "Component Library", "Design Prototyping"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MPL-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-08-31"
evidence_count: 4
github_description: "Penpot: The open-source design platform for Product teams that need scalable collaboration."
github_language: "Clojure"
github_license_spdx: "MPL-2.0"
github_default_branch: "develop"
github_stars: 59430
github_topics: ["clojure", "clojurescript", "design", "prototyping", "ui", "ux-design", "ux-experience"]
github_homepage: "https://penpot.app"
github_pushed_at: "2026-08-31T16:52:54Z"
---
# penpot - penpot

## Bottom Line
A self-hostable design and prototyping platform built on open web standards — SVG as the native file format — giving teams a Figma-shaped workflow without a proprietary cloud.

## What It Solves
- Keep design files on infrastructure the organisation controls.
- Remove the designer/developer format gap by storing designs as standards-based SVG.
- Collaborate on components, design tokens and prototypes in the browser.

## Architecture & Mechanics
- A ClojureScript front end renders the canvas directly as SVG in the browser.
- A Clojure back end handles multi-user sessions, persistence and asset storage.
- Design systems are expressed as shared libraries of components and tokens across files.
- Prototype links and flows layer interaction on top of static boards.

## What Is Inside
- **A ClojureScript front end and Clojure back end** — `frontend/src/` (1,047 files, 846 `.cljs`), `backend/` (502), `common/` (310, 253 `.cljc` shared across both). The shared-code boundary is the interesting structural choice.
- **A WebAssembly renderer** — `render-wasm/` (144 files), the newer rendering path.
- **Visual regression testing with committed snapshots** — `frontend/playwright/` (415 files) including `render-wasm-specs/shapes.spec.js-snapshots/` where the snapshot filenames are the bug numbers they pin (`BUG-13551---Blurs-affecting-other-elements-1.png`, `BUG-13610---Huge-inner-strokes-1.png`). A worked example of tying a rendering regression to its issue.
- **A plugin system with its own documentation** — `plugins/` (444 files) and `docs/plugins/`.
- **An MCP server in-tree** — `mcp/` (92 files) with `docs/mcp/`.
- **Substantial user and technical guides** — `docs/user-guide/` (34), `docs/technical-guide/` (31), `docs/contributing-guide/` (7), plus 665 images.
- **Sample assets** — `sample_media/icons/` (991 files) shipped for demos and tests.
- **Agent tooling from two vendors** — `.opencode/skills/` (`bat-cat`, `code-review`, `create-commit`) and `.serena/memories/docs/core.md`; 20 agent-instruction paths.

## Transferable Capability
**Keep the design and the implementation in the same representation, so handover stops being a translation step.** Where the artefact a designer manipulates is the artefact an engineer reads, the class of error introduced by transcription disappears. The separable practice worth copying regardless: **name each visual regression snapshot after the defect it pins**, so the test suite records why every check exists and a failure is immediately traceable to a decision. Separately: **the system exposes itself as a callable interface for automated consumers**, and ships its own working procedures as executable skills rather than as contributor documentation.

**Alternative to:** design tools whose output must be re-created in another medium. **Applies wherever** two roles work on the same thing through different tools, and wherever visual output can regress.

## Taxonomy
- Ecosystem: Web_Frontend
- Domain Primary: Design
- Maturity Stage: Production_Ready
- License Class: Weak_Copyleft
- Deployment Target: Server
- Interface Protocol: Web_UI
- Data Locality: Distributed
- Hardware Footprint: High_Memory
- Security Compliance: Uncertified
- Agent Surface: Callable

## Integration & Use Cases
- Self-host a design tool for teams with data-residency constraints.
- Maintain a shared design system that front-end code can consume as tokens.
- Study a large real-world ClojureScript application architecture.

## Semantic Links
- [parent_topic:: [[Topic - CAD & SaaS Design]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[twbs - bootstrap]]]
- [related_to:: [[react]]]
- [related_to:: [[square - square.github.io]]]
- [implements_pattern:: [[Pattern - SaaS Product Design]]]
- [implements_pattern:: [[Pattern - Component-Based UI]]]
- [mentions_term:: [[Glossary - SaaS]]]
- [mentions_term:: [[Glossary - Product Design]]]
- [mentions_term:: [[Glossary - Component Library]]]
- [mentions_term:: [[Glossary - Design Prototyping]]]

## Evidence
- Source URL: https://github.com/penpot/penpot
- Source kind: GitHub REST metadata plus maintainer documentation
- Ingestion mode: agent-curated note authored against live repository metadata
- Metadata captured: 2026-08-31

## GitHub Snapshot

- Description: Penpot: The open-source design platform for Product teams that need scalable collaboration.
- Language: Clojure
- License (SPDX): MPL-2.0
- Default Branch: develop
- Stars: 59430
- Homepage: https://penpot.app
- Pushed At: 2026-08-31T16:52:54Z
- Topics: clojure, clojurescript, design, prototyping, ui, ux-design, ux-experience

## Evidence Anchors
- [github_repo] description :: Penpot: The open-source design platform for Product teams that need scalable collaboration. (confidence 0.95)
- [github_repo] language :: Clojure (confidence 0.90)
- [github_repo] license :: MPL-2.0 (confidence 0.90)
- [github_repo] topics :: clojure, clojurescript, design, prototyping, ui, ux-design, ux-experience (confidence 0.85)
