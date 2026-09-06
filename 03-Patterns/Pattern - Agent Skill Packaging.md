---
pattern_key: "agent_skill_packaging"
aliases: ["executable procedure", "skill directory"]
type: "pattern"
status: "active"
examples: ["MisterIcy - provenance", "vercel-labs - skills", "MazzaWill - neo4j-python-pandas-py2neo-v3"]
glossary_terms: ["Skill", "Agent", "Model Context Protocol"]
topic_keys: ["agentic_ai_models"]
---

# Pattern - Agent Skill Packaging

## Definition
Package a working procedure as a directory an agent can execute — an instruction file, the scripts it invokes, and the reference material it consults — rather than as prose a reader has to interpret.

## Why It Matters
- It draws a line most documentation does not: what the agent reads at execution time is separated from what a person reads to understand the approach.
- Procedures without a recorded origin are unamendable, because nobody downstream can tell a considered constraint from an arbitrary one. [[MisterIcy - provenance]] is built entirely on that claim.
- A convention placed where the tooling reads it is enforced; the same convention in a wiki is remembered, which is not the same thing.

## Example Repositories
- [[MisterIcy - provenance]]
- [[vercel-labs - skills]]
- [[MazzaWill - neo4j-python-pandas-py2neo-v3]]

## Related Glossary
- [[Glossary - Skill]]
- [[Glossary - Agent]]
- [[Glossary - Model Context Protocol]]

## Related Topics
- [[Topic - Agentic AI & Models]]
- [[Topic - Knowledge Management]]
