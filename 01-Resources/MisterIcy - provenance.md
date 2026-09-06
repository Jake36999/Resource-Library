---
uuid: "f4382eeb-46eb-519b-89ff-382796020754"
canonical_url: "https://github.com/MisterIcy/provenance"
repo_key: "MisterIcy/provenance"
owner: "MisterIcy"
repo_name: "provenance"
aliases: ["MisterIcy/provenance", "https://github.com/MisterIcy/provenance"]
type: "agent_toolkit"
primary_topic: "Data Lineage & Provenance"
secondary_topics: ["Agentic AI & Models", "Architecture & Developer Playbooks"]
ecosystem: "Markdown"
domain_primary: "Agentic_AI"
maturity_stage: "Active"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Markdown"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "Procedural"
patterns: ["Agent Skill Packaging", "Agent Orchestration"]
glossary_terms: ["Provenance", "Agent", "Skill"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 5
github_description: "🏺⛏️ Provenance — field-tested Claude Code skills with a documented origin. Every method has a history; this is mine."
github_language: "Python"
github_license_spdx: "Apache-2.0"
github_default_branch: "main"
github_stars: 0
github_pushed_at: "2026-08-30T11:16:11Z"
---
# MisterIcy - provenance

## Bottom Line
A plugin of executable agent skills whose organising claim is that each method carries a documented origin — the skill says not only what to do but where the procedure came from and why it is shaped that way.

## What It Solves
- Reuse a working procedure without losing the reasoning that made it work.
- Give an agent a runnable skill rather than a paragraph of advice it has to interpret.
- Bootstrap new skills and subagents from a skill that knows how skills are built.

## Architecture & Mechanics
- Five skills sit under `skills/`, each a directory with a `SKILL.md` plus its own scripts and references: `skill-creator` (13 files), `subagent-creator` (6), `git-committer` (3), `git-committer-setup` (2), `pr-description-sync` (1).
- The two largest skills are reflexive — they create skills and subagents — so the repository contains its own generator, which is why the skill count is small and the file count is not.
- Six agent definitions under `agents/`, four hooks under `hooks/` (three of them shell scripts), and two monitors give the plugin lifecycle points beyond the skills themselves.
- Both `AGENTS.md` and `CLAUDE.md` sit at the root, alongside `.claude-plugin/` and `.claude/settings.json`: instructions for a reader and configuration for a runner, kept apart.
- **Not read:** any `SKILL.md`. The structure above is read off the tree; the provenance claim is the repository's own.

## What Is Inside
- **Five packaged skills** — `skills/skill-creator/` and `skills/subagent-creator/` are the substantial ones; `git-committer`, `git-committer-setup` and `pr-description-sync` are narrow and concrete.
- **Six agent definitions** — `agents/`, and four `hooks/` including three shell scripts under `hooks/scripts/`.
- **32 Markdown files against 3 Python and 5 shell files.** The artefact here is written procedure, not code; that ratio is the point rather than an omission.
- **`CHANGELOG.md`** at the root of a skills repository — the provenance claim made operational, since a method with a history needs somewhere to record it.
- **Not here:** anything that runs without an agent host. The plugin is inert on its own.

## Transferable Capability
**Ship a procedure together with the record of where it came from, so a later reader can tell a considered decision from an arbitrary one.** A bare instruction is unamendable: nobody downstream knows which parts were load-bearing, so either all of it is treated as sacred or all of it is discarded. Attaching the origin makes the procedure *editable* — the reason is checkable against present circumstances. The second transferable idea is the **self-generating package**: the artefact contains the procedure for producing more of itself, which is what keeps a growing set of procedures consistent without a style guide nobody reads.

**Alternative to:** a wiki page of tips, which cannot be executed, and to a script, which executes but explains nothing. **Applies wherever** know-how must outlive the person who has it — runbooks, review checklists, onboarding, house conventions.

## Taxonomy
- Ecosystem: Markdown
- Domain Primary: Agentic_AI
- Maturity Stage: Active
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Markdown
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: Procedural

## Integration & Use Cases
- Read `skills/skill-creator/` as a worked model before writing packaged procedures of your own.
- Adopt the origin-plus-changelog convention for any procedure library that will be edited by people who did not write it.
- Take `git-committer` and `pr-description-sync` as small, self-contained examples of a skill with a narrow job.

## Reading Notes
The name will mislead a search. This is *provenance of methods* — where a working practice came from — and has nothing to do with the data lineage that the rest of this topic is about. It is filed here because the underlying capability is the same one (an artefact that carries its own derivation), and because a reader who arrives from either sense should find it; but a query about column-level lineage that returns this has not been answered. Zero stars and first pushed 2026-08-17: new, and its author is its only user so far.

## Semantic Links
- [parent_topic:: [[Topic - Data Lineage & Provenance]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[vercel-labs - skills]]]
- [related_to:: [[Azure-Samples - semantic-kernel-advanced-usage]]]
- [related_to:: [[MazzaWill - neo4j-python-pandas-py2neo-v3]]]
- [implements_pattern:: [[Pattern - Agent Skill Packaging]]]
- [implements_pattern:: [[Pattern - Agent Orchestration]]]
- [mentions_term:: [[Glossary - Provenance]]]
- [mentions_term:: [[Glossary - Agent]]]
- [mentions_term:: [[Glossary - Skill]]]

## Evidence
- Source URL: https://github.com/MisterIcy/provenance
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; no SKILL.md, agent definition or hook was opened

## GitHub Snapshot

- Description: 🏺⛏️ Provenance — field-tested Claude Code skills with a documented origin. Every method has a history; this is mine.
- Language: Python
- License (SPDX): Apache-2.0
- Default Branch: main
- Stars: 0
- Pushed At: 2026-08-30T11:16:11Z

## Evidence Anchors
- [github_repo] description :: 🏺⛏️ Provenance — field-tested Claude Code skills with a documented origin. Every method has a history; this is mine. (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: Apache-2.0 (confidence 0.90)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 49 paths at HEAD (confidence 0.95)
