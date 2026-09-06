---
uuid: "7412c069-0d3b-5d23-a46b-6977bfc3695b"
canonical_url: "https://github.com/donnemartin/system-design-primer"
repo_key: "donnemartin/system-design-primer"
owner: "donnemartin"
repo_name: "system-design-primer"
aliases: ["donnemartin/system-design-primer", "https://github.com/donnemartin/system-design-primer"]
type: "reference_playbook"
primary_topic: "Architecture & Developer Playbooks"
secondary_topics: ["Curated Aggregators & Reference Lists", "Infrastructure & Observability"]
ecosystem: "Markdown"
domain_primary: "Architecture"
maturity_stage: "Reference"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Markdown"
data_locality: "Stateless"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Reference Architecture", "System Design Reference", "Curated Resource Curation"]
glossary_terms: ["Architecture", "System Design", "Scalability", "Playbook"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "CC-BY-4.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-08-31"
evidence_count: 5
github_description: "Learn how to design large-scale systems. Prep for the system design interview. Includes Anki flashcards."
github_language: "Python"
github_license_spdx: "NOASSERTION"
github_default_branch: "master"
github_stars: 367016
github_topics: ["design", "design-patterns", "design-system", "development", "interview", "interview-practice", "interview-questions", "programming", "python", "system", "web", "web-application", "webapp"]
github_homepage: ""
github_pushed_at: "2026-03-20T01:52:19Z"
---
# donnemartin - system-design-primer

## Bottom Line
A structured curriculum in large-scale system design: the vocabulary of scaling (caching, sharding, consistency, CDNs, queues) plus fully worked design exercises.

## What It Solves
- Give engineers shared vocabulary for scaling trade-offs rather than ad-hoc argument.
- Provide worked examples of designing a system end to end under constraints.
- Compress scattered distributed-systems knowledge into one navigable document.

## Architecture & Mechanics
- Topics are organised from primitives (DNS, CDN, load balancer) up to full architectures.
- Each concept is paired with explicit trade-offs rather than a single recommendation.
- Design exercises supply a problem, constraints and a worked solution with diagrams.
- Anki decks encode the material for spaced repetition.

## What Is Inside
- **86 worked solutions, not just prose** — `solutions/system_design/` (68 files) and `solutions/object_oriented_design/` (18). Each is a directory containing a README with the design walkthrough *and* runnable Python.
- **Six Jupyter notebooks** — `solutions/object_oriented_design/call_center/call_center.ipynb`, `deck_of_cards/deck_of_cards.ipynb`, `hash_table/hash_map.ipynb` and others: the OO design exercises are executable, not diagrams.
- **The diagram sources are checked in** — 17 `.graffle` files alongside 54 rendered PNGs, so the architecture diagrams can be edited rather than only viewed.
- **Spaced-repetition decks** — `resources/flash_cards/` ships three Anki `.apkg` files covering system design, exercises and object-oriented design.
- **Translations** — README in Japanese, Simplified Chinese and Traditional Chinese.
- **Where the value is:** the solutions directory. The README is what everyone reads; the runnable solutions and the editable diagram sources are what almost nobody knows are there.

## Transferable Capability
**Pair each explanation with something executable, so understanding can be checked rather than assumed.** A design discussion that ends at a diagram leaves the reader unable to tell whether they followed it; the same discussion with a runnable solution makes comprehension testable. The separable practice: **keep the editable source of every diagram beside the rendered image**, so the figures can be corrected and reused rather than only viewed.

**Alternative to:** explanation as prose and diagrams; and to images with no source. **Applies wherever** material is meant to teach and the reader has no way to check they understood.

## Taxonomy
- Ecosystem: Markdown
- Domain Primary: Architecture
- Maturity Stage: Reference
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Markdown
- Data Locality: Stateless
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Onboard engineers into architectural decision-making.
- Use the worked exercises as templates for real design documents.
- Cross-reference scaling concepts when evaluating other resources in this catalogue.

## Semantic Links
- [parent_topic:: [[Topic - Architecture & Developer Playbooks]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[ByteByteGoHq - system-design-101]]]
- [related_to:: [[DovAmir - awesome-design-patterns]]]
- [related_to:: [[mhadidg - software-architecture-books]]]
- [implements_pattern:: [[Pattern - Reference Architecture]]]
- [implements_pattern:: [[Pattern - System Design Reference]]]
- [implements_pattern:: [[Pattern - Curated Resource Curation]]]
- [mentions_term:: [[Glossary - Architecture]]]
- [mentions_term:: [[Glossary - System Design]]]
- [mentions_term:: [[Glossary - Scalability]]]
- [mentions_term:: [[Glossary - Playbook]]]

## Evidence
- Source URL: https://github.com/donnemartin/system-design-primer
- Source kind: GitHub REST metadata plus maintainer documentation
- Ingestion mode: agent-curated note authored against live repository metadata
- Metadata captured: 2026-08-31
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names CC-BY-4.0 (reproduced in full). The GitHub API reported `NOASSERTION`, which is why this was read directly.

## GitHub Snapshot

- Description: Learn how to design large-scale systems. Prep for the system design interview. Includes Anki flashcards.
- Language: Python
- License (SPDX): NOASSERTION
- Default Branch: master
- Stars: 367016
- Homepage: None listed
- Pushed At: 2026-03-20T01:52:19Z
- Topics: design, design-patterns, design-system, development, interview, interview-practice, interview-questions, programming, python, system, web, web-application, webapp

## Evidence Anchors
- [github_repo] description :: Learn how to design large-scale systems. Prep for the system design interview. Includes Anki flashcards. (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: NOASSERTION (confidence 0.90)
- [github_repo] topics :: design, design-patterns, design-system, development, interview, interview-practice, interview-questions, programming, python, system, web, web-application, webapp (confidence 0.85)
