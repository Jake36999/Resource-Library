---
uuid: "82f2943a-341a-5e7b-80cf-690b64203d92"
canonical_url: "https://github.com/animate-css/animate.css"
repo_key: "animate-css/animate.css"
owner: "animate-css"
repo_name: "animate.css"
aliases: ["animate-css/animate.css", "https://github.com/animate-css/animate.css"]
type: "frontend_library"
primary_topic: "Frontend & Design Systems"
secondary_topics: ["Architecture & Developer Playbooks", "CAD & SaaS Design"]
ecosystem: "Web_CSS"
domain_primary: "Frontend"
maturity_stage: "Production_Ready"
license_class: "Source_Available"
license_verified: "manual 2026-09-01"
deployment_target: "Browser"
interface_protocol: "Web_UI"
data_locality: "Stateless"
hardware_footprint: "Browser_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Component-Based UI", "Feature Detection"]
glossary_terms: ["Component Library", "Responsive Design", "CSS Reset", "Feature Detection", "DOM"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "Hippocratic-2.1"
source_file: "repositories to chart.md"
evidence_count: 5
github_description: "🍿 A cross-browser library of CSS animations. As easy to use as an easy thing."
github_language: "CSS"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "main"
github_stars: 0
github_topics: ["animation", "css", "css-animations", "stylesheets"]
github_homepage: "https://animate.style/"
github_pushed_at: "2024-07-29T19:34:21Z"
github_updated_at: "2026-08-31T15:16:23Z"
---

# animate-css - animate.css

## Bottom Line
A library of ready-made CSS animations applied by adding class names to elements — no keyframes to write — and it honours prefers-reduced-motion so animations disable themselves for users who have asked for that.

## What It Solves
- Add conventional motion without hand-writing keyframes for each effect.
- Respect motion-sensitivity preferences by default rather than as an afterthought.
- Keep animation entirely in CSS, with no JavaScript animation runtime.

## Architecture & Mechanics
- Each effect is a prefixed utility class such as `animate__bounce`, applied to the element.
- The stylesheet is installed via npm or yarn and imported like any other CSS.
- A `prefers-reduced-motion` media query disables animations for users whose system requests it.
- There is no JavaScript: applying and removing classes is the whole interface.

> Released under the Hippocratic License, which places ethical restrictions on use and is not an OSI-approved open-source licence.

## What Is Inside
- **101 CSS animations, one file each, grouped by behaviour** — `source/`: `attention_seekers/` (13), `fading_entrances/` (13), `fading_exits/` (13), `bouncing_entrances/` (5), `bouncing_exits/` (5), `flippers/` (5), `rotating_entrances/` (5), `rotating_exits/` (5), and the rest. Each file is a standalone keyframe definition, which is the reusable unit whether or not you take the library.
- **A build pipeline in ESM** — 7 `.mjs` files assembling `animate.css` from `source/`.
- **A documentation site with a live playground** — `docsSource/sections/` (10) and `docs/modules/playground.mjs`.
- **Almost no JavaScript and no tests.** 106 of 150 files are `.css`. The repository is a stylesheet and its generator.
- **Licence matters more than the code here** — Hippocratic-2.1, which reads like MIT until its ethical-use clauses; see `Reading Notes`.

## Transferable Capability
**Package each effect as a standalone unit with a stable name, so it can be applied by reference rather than reimplemented.** Naming a behaviour and making the name the interface is what turns a technique into a vocabulary. Whether the collection is adopted is separable from whether the individual unit is useful — each file stands alone.

**Alternative to:** re-deriving a common effect each time it is needed, with a slightly different result each time. **Applies wherever** a set of variations on a technique recurs and would benefit from shared names.

## Taxonomy
- Ecosystem: Web_CSS
- Domain Primary: Frontend
- Maturity Stage: Production_Ready
- License Class: Source_Available
- Deployment Target: Browser
- Interface Protocol: Web_UI
- Data Locality: Stateless
- Hardware Footprint: Browser_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Add entrance, exit and attention animations to an interface quickly.
- Inherit reduced-motion handling rather than implementing it.
- Study class-driven animation as a CSS-only technique.

## Reading Notes
**Hippocratic-2.1 — permissive in shape, restricted in
substance.** The API reports nothing; the licence was verified by hand on 2026-09-01 and
recorded in `.utility/library_config.json`. It reads like MIT until the ethical-use clauses,
which impose conditions no OSI licence does and which some organisations' policies refuse
outright. Classified `Source_Available`, so it is excluded from permissive-only queries — an
exclusion that surprises people, because the library itself is a few hundred lines of CSS.

## Semantic Links
- [parent_topic:: [[Topic - Frontend & Design Systems]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[twbs - bootstrap]]]
- [related_to:: [[nathansmith - 960-Grid-System]]]
- [related_to:: [[necolas - normalize.css]]]
- [implements_pattern:: [[Pattern - Component-Based UI]]]
- [implements_pattern:: [[Pattern - Feature Detection]]]
- [mentions_term:: [[Glossary - Component Library]]]
- [mentions_term:: [[Glossary - Responsive Design]]]
- [mentions_term:: [[Glossary - CSS Reset]]]
- [mentions_term:: [[Glossary - Feature Detection]]]
- [mentions_term:: [[Glossary - DOM]]]

## Evidence
- Source URL: https://github.com/animate-css/animate.css
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01

## GitHub Snapshot

- Description: 🍿 A cross-browser library of CSS animations. As easy to use as an easy thing.
- Language: CSS
- License: Hippocratic License (Hippocratic-2.1) - GitHub reports this as unidentified
- Default Branch: main
- Stars: 0
- Watchers: 0
- Homepage: https://animate.style/
- Archived: no
- Disabled: no
- Pushed At: 2024-07-29T19:34:21Z
- Updated At: 2026-08-31T15:16:23Z
- Topics: animation, css, css-animations, stylesheets

## Evidence Anchors
- [github_repo] description :: 🍿 A cross-browser library of CSS animations. As easy to use as an easy thing. (confidence 0.95)
- [github_repo] topics :: animation, css, css-animations, stylesheets (confidence 0.82)
- [github_repo] language :: CSS (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
