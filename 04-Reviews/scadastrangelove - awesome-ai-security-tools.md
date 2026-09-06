---
uuid: "8f1f0c83-3abd-567c-b029-5cf5708516bc"
canonical_url: "https://github.com/scadastrangelove/awesome-ai-security-tools"
repo_key: "scadastrangelove/awesome-ai-security-tools"
owner: "scadastrangelove"
repo_name: "awesome-ai-security-tools"
aliases: ["scadastrangelove/awesome-ai-security-tools", "https://github.com/scadastrangelove/awesome-ai-security-tools"]
type: "curated_aggregator"
primary_topic: "Curated Aggregators & Reference Lists"
secondary_topics: ["Security & SIEM"]
ecosystem: "Markdown"
domain_primary: "Discovery"
maturity_stage: "Reference"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Markdown"
data_locality: "Stateless"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Curated Resource Curation", "Threat Detection Pipeline", "Reference Architecture"]
glossary_terms: ["SIEM", "Threat Detection", "Enrichment", "Curation", "Taxonomy", "Reference List", "Discovery", "Annotated Example"]
status: "review_pending"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "security_adjacent"
license: "CC0-1.0"
source_file: "repositories to chart.md"
evidence_count: 6
github_description: "A curated list of public-source, research, and commercial tools for AI security and AI-assisted cybersecurity — autotriage, agent security, AI/ML supply chain, pentest agents, AI SAST, LLM-driven fuzzing, threat intelligence, SOC/SIEM triage, reverse engineering, LLM red-teaming, and more."
github_language: "Python"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "main"
github_stars: 0
github_topics: ["agentic-ai", "agents", "awesome", "awesome-list", "awesome-lists", "llm", "security"]
github_homepage: ""
github_pushed_at: "2026-08-31T11:09:04Z"
github_updated_at: "2026-08-31T11:16:55Z"
---

# scadastrangelove - awesome-ai-security-tools

## Bottom Line
A curated index of AI security and AI-assisted security tooling, organised by security function rather than tool type, with a legend marking each entry open-source, research, commercial-hybrid or restrictively licensed.

> Dual-use: catalogues offensive tooling including autonomous pentest agents alongside defensive tools. Held in review per the topic's inclusion criteria.

## What It Solves
- Separate genuinely open tooling from commercial and research code in a fast-moving area.
- Find tools by the security job they do rather than by the technology they use.
- Surface licensing and maintenance caveats before adoption rather than after.

## Architecture & Mechanics
- A type legend marks entries open-source, research, commercial-hybrid or restrictively licensed.
- Categories are functional: autotriage, agent and coding-agent protection, supply-chain and model security, autonomous pentest agents, narrow ML tools, LLM-powered static analysis, threat modelling, fuzzing, threat intelligence, SOC and SIEM triage, reverse engineering, red-teaming and guardrails, honeypots, and CTF benchmarks.
- Each entry carries GitHub metrics, maintenance status and related projects.
- Editorial notes flag licensing restrictions and security considerations per entry.

## What Is Inside
- **Ten files, and the README is generated** — `gen_readme.py` builds it from `data/` (2 JSON files), so the machine-readable data is the source of truth and the Markdown is output. That inverts the usual awesome-list arrangement and makes the corpus queryable.
- **Validated on change** — `.github/workflows/validate.yml` checks the data files, so entries cannot drift into an unparseable state.
- **Why the structure is worth noting** — of the curated lists in this catalogue, this and `public-apis` are the only two that treat the list as data rather than as prose. For anyone building a scouting pipeline, that is the pattern to copy.
- **Held for review** as dual-use security material; the structural lesson is separable from the content.

## Transferable Capability
**Keep a compilation as structured data and generate its readable form, rather than maintaining the readable form directly.** The moment a list is data it can be validated, queried, filtered and merged; the moment it is prose it can only be read and eventually contradicts itself. The generated document is output, never the source.

**Alternative to:** a curated list maintained as a document, where consistency is a matter of care and there is no way to ask it a question. **Applies to every compilation** — including catalogues that hold their own records as documents and generate their views.

## Taxonomy
- Ecosystem: Markdown
- Domain Primary: Discovery
- Maturity Stage: Reference
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Markdown
- Data Locality: Stateless
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Select AI security tooling with licensing and maintenance visible up front.
- Study functional rather than technological categorisation of a tool space.
- Assess the AI security landscape by capability coverage.

## Semantic Links
- [parent_topic:: [[Topic - Curated Aggregators & Reference Lists]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [implements_pattern:: [[Pattern - Curated Resource Curation]]]
- [implements_pattern:: [[Pattern - Threat Detection Pipeline]]]
- [implements_pattern:: [[Pattern - Reference Architecture]]]
- [mentions_term:: [[Glossary - SIEM]]]
- [mentions_term:: [[Glossary - Threat Detection]]]
- [mentions_term:: [[Glossary - Enrichment]]]
- [mentions_term:: [[Glossary - Curation]]]
- [mentions_term:: [[Glossary - Taxonomy]]]
- [mentions_term:: [[Glossary - Reference List]]]
- [mentions_term:: [[Glossary - Discovery]]]
- [mentions_term:: [[Glossary - Annotated Example]]]

## Evidence
- Source URL: https://github.com/scadastrangelove/awesome-ai-security-tools
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names CC0-1.0 (referred to only). The GitHub API reported `UNKNOWN`, which is why this was read directly.

## GitHub Snapshot

- Description: A curated list of public-source, research, and commercial tools for AI security and AI-assisted cybersecurity — autotriage, agent security, AI/ML supply chain, pentest agents, AI SAST, LLM-driven fuzzing, threat intelligence, SOC/SIEM triage, reverse engineering, LLM red-teaming, and more.
- Language: Python
- License: Unknown (UNKNOWN)
- Default Branch: main
- Stars: 0
- Watchers: 0
- Homepage: None provided
- Archived: no
- Disabled: no
- Pushed At: 2026-08-31T11:09:04Z
- Updated At: 2026-08-31T11:16:55Z
- Topics: agentic-ai, agents, awesome, awesome-list, awesome-lists, llm, security

## Evidence Anchors
- [github_repo] description :: A curated list of public-source, research, and commercial tools for AI security and AI-assisted cybersecurity — autotriage, agent security, AI/ML supply chain, pentest agents, AI SAST, LLM-driven fuzzing, threat intellig [truncated] (confidence 0.95)
- [github_repo] topics :: agentic-ai, agents, awesome, awesome-list, awesome-lists, llm, security (confidence 0.82)
- [github_repo] language :: Python (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
