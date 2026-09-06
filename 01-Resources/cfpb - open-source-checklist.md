---
uuid: "30cf8f8c-d27b-5437-b78d-ceb81c9d0d23"
canonical_url: "https://github.com/cfpb/open-source-checklist"
repo_key: "cfpb/open-source-checklist"
owner: "cfpb"
repo_name: "open-source-checklist"
aliases: ["cfpb/open-source-checklist", "https://github.com/cfpb/open-source-checklist"]
type: "curated_aggregator"
primary_topic: "Curated Aggregators & Reference Lists"
secondary_topics: ["Government & Civic Tech", "Architecture & Developer Playbooks"]
ecosystem: "Markdown"
domain_primary: "Discovery"
maturity_stage: "Abandoned"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Markdown"
data_locality: "Stateless"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Curated Resource Curation", "Civic Tech Playbook", "Reference Architecture"]
glossary_terms: ["Playbook", "Open Government", "Architecture", "Curation", "Taxonomy", "Reference List", "Discovery", "Annotated Example"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "CC0-1.0"
source_file: "repositories to chart.md"
evidence_count: 5
github_description: "check internal repos against open source checklist requirements"
github_language: "JavaScript"
github_license: "Unknown"
github_license_spdx: "CC0-1.0"
github_default_branch: "master"
github_stars: 0
github_topics: []
github_homepage: ""
github_pushed_at: "2019-01-18T22:44:03Z"
github_updated_at: "2026-08-30T18:32:16Z"
---

# cfpb - open-source-checklist

## Bottom Line
The Consumer Financial Protection Bureau's tooling for releasing internal code publicly: a checklist of licensing, documentation and scrubbing requirements, plus scripts that strip internal references before publication.

## What It Solves
- Make open-sourcing internal code a repeatable process rather than a case-by-case judgement.
- Catch internal hostnames, URLs and references before they are published by accident.
- Apply consistent licensing and documentation standards across an organisation's releases.

## Architecture & Mechanics
- The checklist enumerates the licensing, documentation and code-scrubbing requirements for release.
- Shell scripts, principally `scrub.sh`, remove internal references and GitHub Enterprise URLs from a codebase.
- Node.js dependencies support the processing steps.
- The stated aim is automating the bureau's checklist for easy release of internal source code.

## What Is Inside
- **Sixteen files, five of them Markdown.** The checklist itself is the resource: what a US federal agency requires before publishing code publicly — licensing, security review, documentation, contribution policy.
- **A little tooling around it** — `bin/` and `cmds/` (one script each), a `.env_SAMPLE`, and three PNG screenshots.
- **Why it is catalogued** — as a governance artefact rather than software. It is the shortest available statement of what an organisation must decide before open-sourcing anything, and it is directly reusable as a template.
- **Dormant.** Nothing here is executable in any meaningful sense, and the content is the point.

## Transferable Capability
**Enumerate the decisions that must be made before an irreversible step, and force them to be made explicitly.** Publishing is one-way; the value is in listing what will be regretted if skipped — licensing, sensitive material, ownership, contribution policy — so each becomes a decision with a name rather than an omission.

**Alternative to:** discovering the omitted decision after the step that made it irreversible. **Applies before any one-way action** — publication, deletion, a change to a shared contract, or accepting an outside dependency.

## Taxonomy
- Ecosystem: Markdown
- Domain Primary: Discovery
- Maturity Stage: Abandoned
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Markdown
- Data Locality: Stateless
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Adopt a release checklist before open-sourcing internal work.
- Automate pre-publication scrubbing rather than reviewing by eye.
- Study checklist-as-governance as a form for organisational standards.

## Semantic Links
- [parent_topic:: [[Topic - Curated Aggregators & Reference Lists]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[orsinium-labs - generated-awesomeness]]]
- [related_to:: [[pracdata - awesome-open-source-data-engineering]]]
- [related_to:: [[The-Cool-Coders - Project-Ideas-And-Resources]]]
- [implements_pattern:: [[Pattern - Curated Resource Curation]]]
- [implements_pattern:: [[Pattern - Civic Tech Playbook]]]
- [implements_pattern:: [[Pattern - Reference Architecture]]]
- [mentions_term:: [[Glossary - Playbook]]]
- [mentions_term:: [[Glossary - Open Government]]]
- [mentions_term:: [[Glossary - Architecture]]]
- [mentions_term:: [[Glossary - Curation]]]
- [mentions_term:: [[Glossary - Taxonomy]]]
- [mentions_term:: [[Glossary - Reference List]]]
- [mentions_term:: [[Glossary - Discovery]]]
- [mentions_term:: [[Glossary - Annotated Example]]]

## Evidence
- Source URL: https://github.com/cfpb/open-source-checklist
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names CC0-1.0 (reproduced in full). The GitHub API reported `UNKNOWN`, which is why this was read directly.

## GitHub Snapshot

- Description: check internal repos against open source checklist requirements
- Language: JavaScript
- License: Unknown (UNKNOWN)
- Default Branch: master
- Stars: 0
- Watchers: 0
- Homepage: None provided
- Archived: yes
- Disabled: no
- Pushed At: 2019-01-18T22:44:03Z
- Updated At: 2026-08-30T18:32:16Z
- Topics: None provided

## Evidence Anchors
- [github_repo] description :: check internal repos against open source checklist requirements (confidence 0.95)
- [github_repo] language :: JavaScript (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
- [seed] repositories to chart.md :: - [ ] https://github.com/cfpb/open-source-checklist.git (confidence 0.50)
