---
uuid: "0bf61893-2a64-534e-875e-b5ba40f3497f"
canonical_url: "https://github.com/roomi-fields/rtfm"
repo_key: "roomi-fields/rtfm"
owner: "roomi-fields"
repo_name: "rtfm"
aliases: ["roomi-fields/rtfm", "https://github.com/roomi-fields/rtfm"]
type: "developer_tool"
primary_topic: "Knowledge Management"
secondary_topics: ["Agentic AI & Models", "Code Intelligence & Structural Parsing"]
ecosystem: "Python"
domain_primary: "Knowledge_Management"
maturity_stage: "Active"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "REST"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "Callable"
patterns: ["Hybrid Retrieval", "Multi-Tier Index Routing", "Knowledge Graph Routing", "Agent Skill Packaging"]
glossary_terms: ["Model Context Protocol", "Semantic Search", "Knowledge Graph", "Chunking", "Retrieval-Augmented Generation"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: "The open retrieval layer for AI coding agents. Indexes code, docs, legal, research, data — 22 parsers (incl. EPUB, DOCX, ODT), FTS5 + semantic search, knowledge graph. Serves surgical context via MCP. Open source, local, free."
github_language: "Python"
github_license_spdx: "MIT"
github_default_branch: "main"
github_stars: 24
github_topics: ["ai-agents", "claude", "claude-code", "code-search", "context-engineering", "developer-tools", "embeddings", "fts", "json-schema", "knowledge-base", "knowledge-graph", "mcp", "mcp-server", "notebooklm", "obsidian", "python", "rag", "retrieval", "semantic-search", "sqlite"]
github_homepage: "https://roomi-fields.github.io/rtfm/"
github_pushed_at: "2026-09-03T19:07:06Z"
---
# roomi-fields - rtfm

## Bottom Line
A local retrieval layer that indexes a heterogeneous document corpus through twenty-two format parsers, combines SQLite full-text search with semantic search and a knowledge graph, and serves the result to an agent over MCP — with its own benchmark papers committed alongside.

## What It Solves
- Give an agent a small, precise slice of a large corpus instead of whole documents.
- Index formats a code-oriented indexer ignores — EPUB, DOCX, ODT, XML, HTML — in the same store as source.
- Run the whole thing locally, with no corpus leaving the machine and no service to pay for.

## Architecture & Mechanics
- Three retrieval strategies are combined rather than chosen between: SQLite FTS5 for lexical matching, embeddings for semantic matching, and a knowledge graph for relationships. Each answers a question the others cannot.
- SQLite is the whole storage layer. There is no server, no vector database process and no graph database — which is what makes *local and free* an architectural property rather than a pricing claim.
- `rtfm/parsers/` is 31 files: twenty-two formats, one parser each. Breadth of input is bought file by file, and it is the largest single component after the tests.
- Delivery is over MCP (`rtfm/_mcp/server.py`, `rtfm/mcp.py`, `.mcp.json`, `server.json`), so the consumer is an agent rather than a person with a search box.
- Five packaged skills sit under `skills/` — `search`, `expand`, `install-embeddings`, `install-pdf`, `install-pdf-full` — which makes optional heavy dependencies an explicit, agent-runnable installation step rather than a hard requirement.
- **Not read:** any Python source or benchmark document. The architecture above is read off the tree, the directory names and the repository's own description.

## What Is Inside
- **Committed benchmark papers** — `docs/benchmarks/`: `benchmark_paper.md`, `benchmark_results.md`, `featurebench.md`, and A/B analyses (`ab_test_b10_analysis.md`), several with French translations. A retrieval project that publishes its own measurements in-tree is rare and is the most valuable thing here for anyone building a comparable system.
- **`docs/comparisons/`** — the project's own positioning against alternatives, which is worth reading critically rather than accepting.
- **Twenty-two format parsers** — `rtfm/parsers/` (31 files), covering EPUB, DOCX, ODT and more alongside code and Markdown.
- **Sixty test files** — `rtfm/tests/`, including real-format samples (`sample_bofip.html`, `sample_cgi.xml`) and `test_cross_corpus_move.py`, which tests the case where a document changes corpus.
- **Five agent skills** — `skills/search/`, `skills/expand/`, plus three installation skills; `.claude/CLAUDE.md`, `.claude-plugin/`, `hooks/` (5), `commands/` (2).
- **`schemas/rtfm-mapping-v1.json`** — a versioned mapping schema, and `PRIVACY.md` at the root.
- **`docs/architecture.md`** and an mkdocs site (`mkdocs.yml`).
- **Not here:** a hosted service or a model. Embeddings are an optional install.

## Transferable Capability
**Combine retrieval strategies that fail differently, and keep the whole store in one embedded file.** Lexical search fails on vocabulary mismatch, semantic search fails on exact identifiers and rare tokens, and a graph fails on anything unrelated — combining them means a query has three chances to be answered by whichever mechanism suits it, and the union is more robust than any tuning of one. Putting all three in SQLite is the second, quieter decision: a single-file store means the index is disposable and rebuildable, backup is a copy, and there is no process to operate.

The third transferable practice is **publishing your own benchmarks in the repository**. It makes a retrieval claim checkable by a reader who has not run anything, and it makes a regression visible to the maintainer.

**Alternative to:** a hosted RAG service, which is the same capability with the corpus somewhere else; a vector database, which handles one of the three strategies and needs operating; and to grep, which is one strategy and no infrastructure at all. **Applies wherever** a heterogeneous corpus must be searched precisely by something with a limited attention budget.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Knowledge_Management
- Maturity Stage: Active
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: REST
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: Callable

## Integration & Use Cases
- Read `docs/benchmarks/` and `docs/architecture.md` before designing a hybrid retrieval layer of your own.
- Study the parser directory as a worked inventory of what indexing a mixed-format corpus actually costs.
- Run it as an MCP server over a documentation corpus to compare hybrid retrieval against embedding-only retrieval on real questions.

## Reading Notes
**This is the closest analogue in the catalogue to the system that holds it** — Markdown corpus, SQLite plus FTS5, optional embeddings, a graph used for relationships, an MCP surface, benchmarks kept in-tree. That makes it the most useful single comparison here and also the one to read most sceptically: `docs/comparisons/` is the project's own account of how it beats alternatives, and none of the benchmark documents were opened. New and fast-moving — created 2026-02-20, twenty-four stars — so treat it as a design to learn from rather than a dependency to take.

## Semantic Links
- [parent_topic:: [[Topic - Knowledge Management]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[jgravelle - jcodemunch-mcp]]]
- [related_to:: [[run-llama - llama_index]]]
- [related_to:: [[microsoft - graphrag]]]
- [related_to:: [[neo4j-labs - neocarta]]]
- [related_to:: [[lancedb - vectordb-recipes]]]
- [implements_pattern:: [[Pattern - Hybrid Retrieval]]]
- [implements_pattern:: [[Pattern - Multi-Tier Index Routing]]]
- [implements_pattern:: [[Pattern - Knowledge Graph Routing]]]
- [implements_pattern:: [[Pattern - Agent Skill Packaging]]]
- [mentions_term:: [[Glossary - Model Context Protocol]]]
- [mentions_term:: [[Glossary - Semantic Search]]]
- [mentions_term:: [[Glossary - Knowledge Graph]]]
- [mentions_term:: [[Glossary - Chunking]]]
- [mentions_term:: [[Glossary - Retrieval-Augmented Generation]]]

## Evidence
- Source URL: https://github.com/roomi-fields/rtfm
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata, the complete file tree at HEAD, and the LICENSE file; no source, benchmark or architecture document was opened

## GitHub Snapshot

- Description: The open retrieval layer for AI coding agents. Indexes code, docs, legal, research, data — 22 parsers (incl. EPUB, DOCX, ODT), FTS5 + semantic search, knowledge graph. Serves surgical context via MCP. Open source, local, free.
- Language: Python
- License (SPDX): MIT
- Default Branch: main
- Stars: 24
- Homepage: https://roomi-fields.github.io/rtfm/
- Pushed At: 2026-09-03T19:07:06Z
- Topics: ai-agents, claude, claude-code, code-search, context-engineering, developer-tools, embeddings, fts, json-schema, knowledge-base, knowledge-graph, mcp, mcp-server, notebooklm, obsidian, python, rag, retrieval, semantic-search, sqlite

## Evidence Anchors
- [github_repo] description :: The open retrieval layer for AI coding agents. Indexes code, docs, legal, research, data — 22 parsers (incl. EPUB, DOCX, ODT), FTS5 + semantic search, knowledge graph. Serves surgical context via MCP. Open source, local, free. (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: MIT (confidence 0.90)
- [github_repo] topics :: ai-agents, claude, claude-code, code-search, context-engineering, developer-tools, embeddings, fts, json-schema, knowledge-base, knowledge-graph, mcp, mcp-server, notebooklm, obsidian, python, rag, retrieval, semantic-search, sqlite (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 183 paths at HEAD (confidence 0.95)
