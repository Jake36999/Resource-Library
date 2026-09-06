---
uuid: "a64656aa-715f-5c5a-99d8-09033027ca5a"
canonical_url: "https://github.com/vercel-labs/skills"
repo_key: "vercel-labs/skills"
owner: "vercel-labs"
repo_name: "skills"
aliases: ["vercel-labs/skills", "https://github.com/vercel-labs/skills"]
type: "ai_resource"
primary_topic: "Agentic AI & Models"
secondary_topics: ["Architecture & Developer Playbooks"]
ecosystem: "Markdown"
domain_primary: "Agentic_AI"
maturity_stage: "Active"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Python_SDK"
data_locality: "Local_First"
hardware_footprint: "Low_VRAM"
security_compliance: "Uncertified"
agent_surface: "Procedural"
patterns: ["Agent Orchestration", "Model Inference Pipeline"]
glossary_terms: ["Agent", "Prompt", "LLM", "Inference", "TTS", "STT", "Multimodal Model"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
evidence_count: 5
github_description: "The open agent skills tool - npx skills"
github_language: "TypeScript"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "main"
github_stars: 0
github_topics: []
github_homepage: "https://skills.sh"
github_pushed_at: "2026-08-18T20:28:34Z"
github_updated_at: "2026-08-31T17:12:45Z"
---

# vercel-labs - skills

## Bottom Line
A CLI for managing Agent Skills — reusable instruction sets defined in SKILL.md files with YAML frontmatter — that installs them into the right directory for any of 75-plus coding agents, so the same skill works across Claude Code, Cursor and others.

## What It Solves
- Stop each coding agent needing its own copy of the same custom instructions.
- Share workflows across a team and across agents through one distributable format.
- Install and update skills as dependencies instead of copying files by hand.

## Architecture & Mechanics
- Skills are discovered as SKILL.md files carrying YAML frontmatter metadata, from a repository or local directory.
- Installation targets agent-specific directories via symlink or copy, per-project or globally.
- Commands include `npx skills add`, `find` and `update`, against a registry at skills.sh.
- Sources include GitHub and GitLab URLs and local paths, with authentication for private repositories.

## What Is Inside
- **A TypeScript CLI for installing agent skills, not a skill collection** — `src/` (49 files, 97 `.ts` overall) with `src/providers/` (4) resolving skills from different sources and `src/prompts/` (1).
- **The tests are the larger half** — `tests/` (44 files) and 61 test paths; `scripts/execute-tests.ts` is a custom runner, and `src/add.test.ts` / `src/add-prompt.test.ts` sit beside the code they test.
- **One skill ships with it** — `skills/find-skills/SKILL.md`, which is the self-referential example: a skill for discovering skills.
- **Agent-facing repository conventions** — `AGENTS.md` at the root, and `.github/ISSUE_TEMPLATE/agent-request.yml` — an issue template specifically for requesting agent support, plus a `.github/workflows/agents.yml`.
- **Third-party attribution kept explicitly** — `ThirdPartyNoticeText.txt`.
- **Why it is catalogued:** as the clearest small example of skill distribution being treated as a package-manager problem, which is directly relevant to how this vault might distribute its own procedures.

## Transferable Capability
**Treat reusable procedure as a distributable artefact with a resolver, rather than as documentation to be copied.** Once a procedure has a name, a source and an install step, it can be versioned, shared and updated — which is the difference between a practice that spreads and one that is re-invented in every repository. That the tool ships a procedure for finding procedures is the demonstration.

**Alternative to:** conventions written in a contributing guide, which are read once and diverge immediately. **Applies wherever** the same procedure should be executed the same way by different people or agents in different places.

## Taxonomy
- Ecosystem: Markdown
- Domain Primary: Agentic_AI
- Maturity Stage: Active
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Python_SDK
- Data Locality: Local_First
- Hardware Footprint: Low_VRAM
- Security Compliance: Uncertified
- Agent Surface: Procedural

## Integration & Use Cases
- Distribute a team's agent workflows as installable units.
- Study a portable format that abstracts over incompatible agent conventions.
- Manage agent instructions with dependency-style tooling.

## Semantic Links
- [parent_topic:: [[Topic - Agentic AI & Models]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[Azure-Samples - semantic-kernel-advanced-usage]]]
- [related_to:: [[awslabs - awsome-distributed-ai]]]
- [related_to:: [[armanakbari - Awsome-Efficient-DLMs]]]
- [implements_pattern:: [[Pattern - Agent Orchestration]]]
- [implements_pattern:: [[Pattern - Model Inference Pipeline]]]
- [mentions_term:: [[Glossary - Agent]]]
- [mentions_term:: [[Glossary - Prompt]]]
- [mentions_term:: [[Glossary - LLM]]]
- [mentions_term:: [[Glossary - Inference]]]
- [mentions_term:: [[Glossary - TTS]]]
- [mentions_term:: [[Glossary - STT]]]
- [mentions_term:: [[Glossary - Multimodal Model]]]

## Evidence
- Source URL: https://github.com/vercel-labs/skills
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names MIT (reproduced in full). The GitHub API reported `UNKNOWN`, which is why this was read directly.

## GitHub Snapshot

- Description: The open agent skills tool - npx skills
- Language: TypeScript
- License: Unknown (UNKNOWN)
- Default Branch: main
- Stars: 0
- Watchers: 0
- Homepage: https://skills.sh
- Archived: no
- Disabled: no
- Pushed At: 2026-08-18T20:28:34Z
- Updated At: 2026-08-31T17:12:45Z
- Topics: None provided

## Evidence Anchors
- [github_repo] description :: The open agent skills tool - npx skills (confidence 0.95)
- [github_repo] language :: TypeScript (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
- [seed] repositories to chart.md :: - [ ] https://github.com/vercel-labs/skills.git (confidence 0.50)
