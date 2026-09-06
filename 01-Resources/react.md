---
uuid: "0b6118f8-a760-5a27-913f-fcbeab75eb33"
canonical_url: "https://github.com/react/react"
repo_key: "react/react"
owner: "react"
repo_name: "react"
aliases: ["react/react", "https://github.com/react/react"]
type: "frontend_library"
primary_topic: "Frontend & Design Systems"
secondary_topics: ["Architecture & Developer Playbooks", "CAD & SaaS Design"]
ecosystem: "Web_Frontend"
domain_primary: "Frontend"
maturity_stage: "Production_Ready"
license_class: "Permissive"
deployment_target: "Browser"
interface_protocol: "Web_UI"
data_locality: "Stateless"
hardware_footprint: "Browser_Only"
security_compliance: "Uncertified"
agent_surface: "Procedural"
patterns: ["Component-Based UI", "Feature Detection"]
glossary_terms: ["Component Library", "DOM", "Responsive Design", "CSS Reset", "Feature Detection"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
evidence_count: 6
github_description: "The library for web and native user interfaces."
github_language: "JavaScript"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "main"
github_stars: 0
github_topics: ["declarative", "frontend", "javascript", "library", "react", "ui"]
github_homepage: "https://react.dev"
github_pushed_at: "2026-08-31T17:20:00Z"
github_updated_at: "2026-08-31T16:41:26Z"
---

# react

## Bottom Line
A JavaScript library for building user interfaces from components: you describe what the UI should look like for a given state, and React works out the minimum set of updates needed when that state changes.

## What It Solves
- Avoid hand-written DOM mutation logic, the historical source of most UI bugs.
- Compose complex interfaces from small independently reasoned pieces.
- Target several environments — browser, server, native — from one component model.

## Architecture & Mechanics
- Components declare what the interface should be for a given state; React reconciles the result against what is rendered.
- The reconciliation algorithm computes which components actually need updating when state changes.
- The repository is split into packages separating core logic from renderers.
- Renderers target different environments: ReactDOM for the browser, server rendering via Node, React Native for mobile. Licensed MIT.

## What Is Inside
- **The compiler is now the larger half** — `compiler/` (4,215 files) against `packages/` (2,154). `compiler/packages/` (3,945) holds the optimising compiler, `compiler/crates/` (131 files, 120 `.rs`) a Rust implementation, `compiler/apps/playground/` a live sandbox, and `compiler/docs/` (`DESIGN_GOALS.md`, `DEVELOPMENT_GUIDE.md`, `RUST_CRATE_RELEASES.md`).
- **4,199 fixture paths — the compiler is tested by corpus.** `compiler/fixtures/` contains one input program per optimisation case with its expected output, named for the behaviour they pin. This is the largest worked example in the catalogue of snapshot-testing a compiler.
- **The runtime packages, separable** — `packages/`: `react-reconciler/` (176, the algorithm independent of any renderer), `react-dom/` (226), `react-dom-bindings/` (94), `react-server/` (88), `react-devtools-shared/` (614), `react-devtools-extensions/` (110).
- **Integration fixtures as runnable apps** — `fixtures/`: `dom/` (101), `packaging/` (84, verifying published artefacts), `flight/` (44), `legacy-jsx-runtimes/` (42), `flight-ssr-bench/` (38, a server-rendering benchmark with its own bench server), `nesting/` (20, multiple React versions on one page).
- **1,997 Markdown files**, largely per-fixture and per-package documentation.
- **Agent tooling in-tree** — `.claude/` at the root (`instructions.md`, `settings.json`, `skills/extract-errors/SKILL.md`, `skills/test/SKILL.md`) and a second `.claude/` inside `compiler/`; 28 agent-instruction paths.

## Transferable Capability
**Describe what the result should look like for a given state, and let the machinery work out the change.** Removing the transition from the author's responsibility is what makes complex interfaces tractable — you specify destinations, not journeys. The structural move: **separate the algorithm that computes changes from the thing that applies them**, so the same core drives entirely different outputs. The separable practice: **test a transformation by corpus** — one input and its expected output per behaviour — which is how a change of that complexity stays reviewable. A separable practice: **the repository's own working procedures are shipped as executable instructions** rather than described, so the mechanical parts of contributing are performed the same way by everyone.

**Alternative to:** mutating a structure step by step and tracking what must change; and to a renderer fused to one output medium. **Applies wherever** a derived representation must track changing state.

## Taxonomy
- Ecosystem: Web_Frontend
- Domain Primary: Frontend
- Maturity Stage: Production_Ready
- License Class: Permissive
- Deployment Target: Browser
- Interface Protocol: Web_UI
- Data Locality: Stateless
- Hardware Footprint: Browser_Only
- Security Compliance: Uncertified
- Agent Surface: Procedural

## Integration & Use Cases
- Build interactive interfaces without imperative DOM manipulation.
- Share component logic across web and native targets.
- Study reconciliation as a general technique for declarative rendering.

## Semantic Links
- [parent_topic:: [[Topic - Frontend & Design Systems]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[twbs - bootstrap]]]
- [related_to:: [[animate-css - animate.css]]]
- [related_to:: [[nathansmith - 960-Grid-System]]]
- [implements_pattern:: [[Pattern - Component-Based UI]]]
- [implements_pattern:: [[Pattern - Feature Detection]]]
- [mentions_term:: [[Glossary - Component Library]]]
- [mentions_term:: [[Glossary - DOM]]]
- [mentions_term:: [[Glossary - Responsive Design]]]
- [mentions_term:: [[Glossary - CSS Reset]]]
- [mentions_term:: [[Glossary - Feature Detection]]]

## Evidence
- Source URL: https://github.com/react/react
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names MIT (reproduced in full). The GitHub API reported `UNKNOWN`, which is why this was read directly.

## GitHub Snapshot

- Description: The library for web and native user interfaces.
- Language: JavaScript
- License: Unknown (UNKNOWN)
- Default Branch: main
- Stars: 0
- Watchers: 0
- Homepage: https://react.dev
- Archived: no
- Disabled: no
- Pushed At: 2026-08-31T17:20:00Z
- Updated At: 2026-08-31T16:41:26Z
- Topics: declarative, frontend, javascript, library, react, ui

## Evidence Anchors
- [github_repo] description :: The library for web and native user interfaces. (confidence 0.95)
- [github_repo] topics :: declarative, frontend, javascript, library, react, ui (confidence 0.82)
- [github_repo] language :: JavaScript (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
