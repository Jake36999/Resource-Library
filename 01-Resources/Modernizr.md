---
uuid: "3171da63-3e8a-5cb8-b5ac-11c71e91753f"
canonical_url: "https://github.com/Modernizr/Modernizr"
repo_key: "Modernizr/Modernizr"
owner: "Modernizr"
repo_name: "Modernizr"
aliases: ["Modernizr/Modernizr", "https://github.com/Modernizr/Modernizr"]
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
glossary_terms: ["Feature Detection", "DOM", "Component Library", "Responsive Design", "CSS Reset"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
evidence_count: 6
github_description: "Modernizr is a JavaScript library that detects HTML5 and CSS3 features in the user’s browser."
github_language: "JavaScript"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "master"
github_stars: 0
github_topics: ["css3-features", "feature-detection", "hacktoberfest", "javascript", "javascript-library", "modernizr"]
github_homepage: "https://www.npmjs.com/package/modernizr"
github_pushed_at: "2026-08-12T16:31:33Z"
github_updated_at: "2026-08-31T03:28:00Z"
---

# Modernizr

## Bottom Line
A JavaScript library that tests which HTML5 and CSS3 features the current browser actually supports, exposing the results as classes on the html element and properties on a global object so code can branch on capability rather than on browser identity.

## What It Solves
- Branch on what a browser can do instead of guessing from its user-agent string.
- Make progressive enhancement mechanical: style the supported path and the fallback separately in CSS.
- Avoid shipping detection code for features you never test.

## Architecture & Mechanics
- Individual feature detects run at load and record their results.
- Results appear as classes on the html element, so CSS can target them directly.
- The same results are exposed as properties on a global Modernizr object for JavaScript.
- A CLI and programmatic API build a custom bundle containing only the detects you need.

## What Is Inside
- **305 individual feature detections, one file each** — `feature-detects/` organised by area: `css/` (86), `input/` (16), `es6/` (14), `img/` (13), `network/` (12), `dom/` (11), `elem/` (10), `es5/` (9). Each file is a self-contained test carrying a metadata comment block, and that file is the reusable unit whether or not you use Modernizr itself.
- **A build system that reads those comments** — `lib/` and `bin/`, emitting a custom build containing only the detections asked for.
- **The test harness is the interesting half** — `test/browser/` (62 files) runs the detections in a real browser; `test/node/`, `test/universal/` and `test/mocks/` cover the rest. 86 test-related paths against 48 source files.
- **Translated documentation** — README in Hindi, Indonesian, Georgian, Portuguese (Brazil) and Spanish alongside English.
- **What to take:** a capability probe as a standalone file with machine-readable metadata, and the browser-matrix harness around it.

## Transferable Capability
**Test for the capability you need rather than identifying who you are talking to, because identity is a proxy that goes wrong and capability is the actual question.** The structural move: **each probe is a standalone file carrying machine-readable metadata about what it tests**, so a build can include exactly the probes asked for and the collection stays additive rather than monolithic.

**Alternative to:** branching on the identity of the counterparty, which requires a maintained table of who supports what and is wrong for anything unanticipated. **Applies wherever** behaviour must adapt to an environment whose capabilities vary and cannot be enumerated in advance.

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
- Apply progressive enhancement driven by capability rather than browser sniffing.
- Style supported and unsupported paths purely in CSS.
- Study feature detection as the durable alternative to version targeting.

## Semantic Links
- [parent_topic:: [[Topic - Frontend & Design Systems]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[twbs - bootstrap]]]
- [related_to:: [[animate-css - animate.css]]]
- [related_to:: [[nathansmith - 960-Grid-System]]]
- [implements_pattern:: [[Pattern - Component-Based UI]]]
- [implements_pattern:: [[Pattern - Feature Detection]]]
- [mentions_term:: [[Glossary - Feature Detection]]]
- [mentions_term:: [[Glossary - DOM]]]
- [mentions_term:: [[Glossary - Component Library]]]
- [mentions_term:: [[Glossary - Responsive Design]]]
- [mentions_term:: [[Glossary - CSS Reset]]]

## Evidence
- Source URL: https://github.com/Modernizr/Modernizr
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names MIT (reproduced in full). The GitHub API reported `UNKNOWN`, which is why this was read directly.

## GitHub Snapshot

- Description: Modernizr is a JavaScript library that detects HTML5 and CSS3 features in the user’s browser.
- Language: JavaScript
- License: Unknown (UNKNOWN)
- Default Branch: master
- Stars: 0
- Watchers: 0
- Homepage: https://www.npmjs.com/package/modernizr
- Archived: no
- Disabled: no
- Pushed At: 2026-08-12T16:31:33Z
- Updated At: 2026-08-31T03:28:00Z
- Topics: css3-features, feature-detection, hacktoberfest, javascript, javascript-library, modernizr

## Evidence Anchors
- [github_repo] description :: Modernizr is a JavaScript library that detects HTML5 and CSS3 features in the user’s browser. (confidence 0.95)
- [github_repo] topics :: css3-features, feature-detection, hacktoberfest, javascript, javascript-library, modernizr (confidence 0.82)
- [github_repo] language :: JavaScript (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
