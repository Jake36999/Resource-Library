---
uuid: "5005ae96-f411-5651-ae1b-38305fc8bc5d"
canonical_url: "https://github.com/twbs/bootstrap"
repo_key: "twbs/bootstrap"
owner: "twbs"
repo_name: "bootstrap"
aliases: ["twbs/bootstrap", "https://github.com/twbs/bootstrap"]
type: "frontend_library"
primary_topic: "Frontend & Design Systems"
secondary_topics: ["Architecture & Developer Playbooks", "CAD & SaaS Design"]
ecosystem: "Web_CSS"
domain_primary: "Frontend"
maturity_stage: "Production_Ready"
license_class: "Permissive"
deployment_target: "Browser"
interface_protocol: "Web_UI"
data_locality: "Stateless"
hardware_footprint: "Browser_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Component-Based UI", "Feature Detection"]
glossary_terms: ["Component Library", "Responsive Design", "CSS Reset", "DOM", "Feature Detection"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
evidence_count: 6
github_description: "The most popular HTML, CSS, and JavaScript framework for developing responsive, mobile first projects on the web."
github_language: "MDX"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "main"
github_stars: 0
github_topics: ["bootstrap", "css", "css-framework", "html", "javascript", "sass", "scss"]
github_homepage: "https://getbootstrap.com"
github_pushed_at: "2026-08-31T17:05:41Z"
github_updated_at: "2026-08-31T16:51:30Z"
---

# twbs - bootstrap

## Bottom Line
A mobile-first CSS and JavaScript framework providing a responsive grid, styled components and utility classes, customisable by overriding Sass variables before compilation rather than fighting compiled CSS.

## What It Solves
- Get a consistent, responsive layout without designing a grid system first.
- Restyle the whole framework by changing variables rather than overriding rules.
- Ship a familiar component vocabulary that developers already recognise.

## Architecture & Mechanics
- Compiled CSS ships as separable pieces — grid, Reboot and utilities can be used without the rest.
- JavaScript components are bundled with Popper.js for positioning.
- Customisation happens in the `/scss` sources: override variables and mixins, then compile.
- Distribution covers npm, yarn, Composer and NuGet; documentation is built with Astro.

## What Is Inside
- **The documentation site is bigger than the library** — `site/` (454 files: 110 `.mdx`, 104 `.astro`) against `scss/` (102) and `js/src/` (26). The site is a working Astro application and is itself a reference for building versioned documentation.
- **Design tokens as data** — `site/data/breakpoints.yml`, `site/data/examples.yml` and others, so the documentation and the build read the same values rather than restating them.
- **173 example paths** — `site/src/assets/examples/` carries complete page layouts (including RTL variants such as `album-rtl/`), and `build/zip-examples.mjs` packages them for download.
- **Sass organised as a system** — `scss/`: `mixins/` (27), `helpers/` (12), `forms/` (9), `utilities/`, and `scss/tests/` (10) which tests the Sass itself.
- **Cross-browser verification in CI** — `.github/workflows/browserstack.yml`, plus `bundlewatch.yml` enforcing bundle size and `calibreapp-image-actions.yml` compressing images on PR.
- **Prebuilt output committed** — `dist/` (44 files), which is why the CDN links work against a tag.

## Transferable Capability
**Give a system a small set of named decisions and derive everything from them, so consistency is structural rather than remembered.** Spacing, breakpoints and scale defined once and referenced everywhere means a change propagates instead of needing to be hunted. The separable practice: **hold those decisions as data that both the build and the documentation read**, so the documentation cannot describe values the system does not use.

**Alternative to:** values repeated wherever needed, where consistency is a matter of discipline; and to documentation restating constants. **Applies wherever** many parts must agree about a small number of choices.

## Taxonomy
- Ecosystem: Web_CSS
- Domain Primary: Frontend
- Maturity Stage: Production_Ready
- License Class: Permissive
- Deployment Target: Browser
- Interface Protocol: Web_UI
- Data Locality: Stateless
- Hardware Footprint: Browser_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Lay out a responsive interface quickly with a documented grid.
- Produce a themed design system by overriding Sass variables.
- Import only the grid or utilities where a full framework is unwanted.

## Semantic Links
- [parent_topic:: [[Topic - Frontend & Design Systems]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[animate-css - animate.css]]]
- [related_to:: [[nathansmith - 960-Grid-System]]]
- [related_to:: [[necolas - normalize.css]]]
- [implements_pattern:: [[Pattern - Component-Based UI]]]
- [implements_pattern:: [[Pattern - Feature Detection]]]
- [mentions_term:: [[Glossary - Component Library]]]
- [mentions_term:: [[Glossary - Responsive Design]]]
- [mentions_term:: [[Glossary - CSS Reset]]]
- [mentions_term:: [[Glossary - DOM]]]
- [mentions_term:: [[Glossary - Feature Detection]]]

## Evidence
- Source URL: https://github.com/twbs/bootstrap
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names MIT (reproduced in full). The GitHub API reported `UNKNOWN`, which is why this was read directly.

## GitHub Snapshot

- Description: The most popular HTML, CSS, and JavaScript framework for developing responsive, mobile first projects on the web.
- Language: MDX
- License: Unknown (UNKNOWN)
- Default Branch: main
- Stars: 0
- Watchers: 0
- Homepage: https://getbootstrap.com
- Archived: no
- Disabled: no
- Pushed At: 2026-08-31T17:05:41Z
- Updated At: 2026-08-31T16:51:30Z
- Topics: bootstrap, css, css-framework, html, javascript, sass, scss

## Evidence Anchors
- [github_repo] description :: The most popular HTML, CSS, and JavaScript framework for developing responsive, mobile first projects on the web. (confidence 0.95)
- [github_repo] topics :: bootstrap, css, css-framework, html, javascript, sass, scss (confidence 0.82)
- [github_repo] language :: MDX (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
