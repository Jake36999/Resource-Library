---
uuid: "d44ba4fa-0326-5247-831f-17f153e49f14"
canonical_url: "https://github.com/sturdy-dev/semantic-code-search"
repo_key: "sturdy-dev/semantic-code-search"
owner: "sturdy-dev"
repo_name: "semantic-code-search"
aliases: ["sturdy-dev/semantic-code-search", "https://github.com/sturdy-dev/semantic-code-search"]
type: "developer_tool"
primary_topic: "Code Intelligence & Structural Parsing"
secondary_topics: ["Knowledge Management"]
ecosystem: "Python"
domain_primary: "Code_Intelligence"
maturity_stage: "Abandoned"
license_class: "Copyleft"
deployment_target: "Local_Only"
interface_protocol: "CLI"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Semantic Code Retrieval"]
glossary_terms: ["Semantic Search", "Embedding", "Vector Database"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "AGPL-3.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: "Search your codebase with natural language • CLI • No data leaves your computer"
github_language: "Python"
github_license_spdx: "AGPL-3.0"
github_default_branch: "main"
github_stars: 403
github_topics: ["ai", "codesearch"]
github_pushed_at: "2023-05-14T13:53:27Z"
---
# sturdy-dev - semantic-code-search

## Bottom Line
A six-file command-line tool that embeds the functions in a git repository and searches them by meaning, with the whole model running locally so no code is sent anywhere.

## What It Solves
- Find the function that does a thing when you do not know what it was called.
- Search a codebase semantically without uploading it to a service.
- Get that capability as a single CLI rather than as an index server to operate.

## Architecture & Mechanics
- Six files under `src/semantic_code_search/` are the entire tool. The embedding model is the dependency; the tool is the plumbing around it.
- Scope is the git repository, which is what keeps it a CLI: there is no server, no daemon and no cross-repository index.
- The local-only claim is architectural rather than a policy — the model runs on the machine, so *no data leaves your computer* is a consequence of where the computation happens.
- **Not read:** any Python source. The above is from the repository's own description and its size.

## What Is Inside
- **Six source files** — `src/semantic_code_search/` — plus `setup.py`, `setup.cfg` and `requirements.txt`. Fourteen paths in total.
- **`docs/example-results.png`** — the only demonstration of output in the tree.
- **Not here:** a vector database, a server, tests, or any language-specific parsing. It is deliberately the smallest thing that works.

## Transferable Capability
**Search by meaning where the corpus already has natural boundaries, and keep the computation next to the data.** Two decisions do the work. The first is choosing the *function* as the retrieval unit — a boundary the language already defines, so no chunking heuristic is needed and no result straddles two unrelated things. The second is running the model locally, which converts a privacy policy into an architectural fact: there is no endpoint to trust because there is no endpoint.

**Alternative to:** grep, which requires knowing the name; a hosted code-search service, which requires sending the code; and an embedding pipeline with a vector store, which is the same capability with an operational footprint. **Applies wherever** a corpus has natural units and a small, private, name-independent search would be enough — notes, tickets, configuration, documentation.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Code_Intelligence
- Maturity Stage: Abandoned
- License Class: Copyleft
- Deployment Target: Local_Only
- Interface Protocol: CLI
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Use it directly on a repository where you know the behaviour you want and not the vocabulary the author used.
- Read it as the minimum shape of local semantic search before reaching for a vector database.
- Compare with [[fynnfluegge - codeqai]], which adds chat and fine-tuning datasets to roughly the same core.

## Reading Notes
**AGPL-3.0**, which is the most consequential fact here: for a tool that might be embedded in a service, the network clause governs, and it is excluded from every permissive-constrained answer in this catalogue. Last pushed 2023-05-14 and unchanged since — classified `Abandoned` on that evidence; the embedding-model ecosystem it depends on has moved substantially in the interval, so expect the pinned dependencies to be the obstacle rather than the code.

## Semantic Links
- [parent_topic:: [[Topic - Code Intelligence & Structural Parsing]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[fynnfluegge - codeqai]]]
- [related_to:: [[hamelsmu - code_search]]]
- [related_to:: [[jgravelle - jcodemunch-mcp]]]
- [implements_pattern:: [[Pattern - Semantic Code Retrieval]]]
- [mentions_term:: [[Glossary - Semantic Search]]]
- [mentions_term:: [[Glossary - Embedding]]]
- [mentions_term:: [[Glossary - Vector Database]]]

## Evidence
- Source URL: https://github.com/sturdy-dev/semantic-code-search
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; no Python source was opened

## GitHub Snapshot

- Description: Search your codebase with natural language • CLI • No data leaves your computer
- Language: Python
- License (SPDX): AGPL-3.0
- Default Branch: main
- Stars: 403
- Pushed At: 2023-05-14T13:53:27Z
- Topics: ai, codesearch

## Evidence Anchors
- [github_repo] description :: Search your codebase with natural language • CLI • No data leaves your computer (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: AGPL-3.0 (confidence 0.90)
- [github_repo] topics :: ai, codesearch (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 14 paths at HEAD (confidence 0.95)
