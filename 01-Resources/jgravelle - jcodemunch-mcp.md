---
uuid: "844b04db-477a-548a-8877-767699779efc"
canonical_url: "https://github.com/jgravelle/jcodemunch-mcp"
repo_key: "jgravelle/jcodemunch-mcp"
owner: "jgravelle"
repo_name: "jcodemunch-mcp"
aliases: ["jgravelle/jcodemunch-mcp", "https://github.com/jgravelle/jcodemunch-mcp"]
type: "agent_toolkit"
primary_topic: "Code Intelligence & Structural Parsing"
secondary_topics: ["Agentic AI & Models", "Knowledge Management"]
ecosystem: "Python"
domain_primary: "Code_Intelligence"
maturity_stage: "Active"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "REST"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "Callable"
patterns: ["Structural Code Search", "Semantic Code Retrieval", "Multi-Tier Index Routing"]
glossary_terms: ["Model Context Protocol", "Abstract Syntax Tree", "Evidence Snippet", "Structural Search"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: "Cut AI token costs 95%+ on code exploration. The leading MCP server for precise, symbol-level GitHub code retrieval via tree-sitter AST. Works with Claude Code, Cursor & any MCP client. 313B+ tokens saved."
github_language: "Python"
github_license_spdx: "NOASSERTION"
github_default_branch: "main"
github_stars: 2651
github_topics: ["ai-coding", "ast", "claude", "claude-code", "cline", "code-intelligence", "codex", "context-window", "copilot", "cursor", "developer-tools", "gemini-cli", "llm", "mcp", "mcp-server", "model-context-protocol", "opencode", "token-optimization", "tree-sitter", "windsurf"]
github_homepage: "https://jcodemunch.com/"
github_pushed_at: "2026-09-04T03:12:20Z"
---
# jgravelle - jcodemunch-mcp

## Bottom Line
An agent-callable server that returns individual symbols from a repository rather than whole files, using a tree-sitter parse to cut the retrieval unit down to the function or class actually asked about — and which measures whether that retrieval was right, in a benchmark suite larger than most projects' test suites.

## What It Solves
- Answer a question about one function without loading the file, the module and everything they import.
- Give an agent a retrieval interface it can call directly, rather than a search box a person drives.
- Know whether the retrieval was correct, rather than whether it returned something.

## Architecture & Mechanics
- Retrieval is symbol-level and structural: a tree-sitter parse identifies definitions, so the unit returned is a symbol and its span rather than a file or a fixed-size chunk.
- The server speaks MCP, which is what makes it callable by an agent with no person in the loop; `mcpb/server/main.py` and `src/jcodemunch_mcp/` (277 files) hold the implementation.
- Retrieval quality is treated as a measured property, not a claim. `benchmarks/` (134 files) is split by what is being measured: `goldset/` (34) is a fixed corpus with known answers, `route_recall/` (13) asks whether the right route was chosen, `description_smells/` (7) inspects the *descriptions* themselves, `replay/` (6) re-runs recorded sessions against a golden output, and `rust_fidelity/` and `racket_fidelity/` check parsing per language.
- Four JSON Schemas define what an answer must contain: `schemas/retrieval-verdict.schema.json`, `evidence-receipt.schema.json`, `confidence-provenance.schema.json`, `ranked-context-response.schema.json`. An answer is required to carry its own evidence and the provenance of its confidence.
- **Not read:** any Python source or schema body. The above is read off the tree, the schema and benchmark filenames, and the repository's own description.

## What Is Inside
- **A benchmark suite treated as a first-class component** — `benchmarks/` with `METHODOLOGY.md`, `REPRODUCING.md`, `RAG_COMPARISON_NOTES.md`, dated A/B records (`ab-test-dead-code-2026-03-18.md`, `ab-test-naming-audit-2026-03-18.md`), and a `goldset/corpus/` containing real code in Python, Go and Racket. A second harness, `munch-bench/`, has its own corpus, tests and results.
- **`benchmarks/description_smells/`** — seven files whose subject is the quality of the descriptions themselves rather than the code. Directly relevant to any catalogue whose retrieval depends on how its entries are written.
- **Four answer schemas** — `schemas/`: `retrieval-verdict`, `evidence-receipt`, `confidence-provenance`, `ranked-context-response`. The shape of a defensible answer, written down.
- **Test fixtures across a wide language range** — `tests/fixtures/` (63 directories), including `al/sample.al` and `arduino/sample.ino`; plus `tests/encoding/` (5), for the failure mode nobody plans for.
- **An unusually large root documentation set** — `ARCHITECTURE.md`, `CAPABILITIES.md`, `CONFIGURATION.md`, `CONTEXT_PROVIDERS.md`, `CLI-AND-ENV.md`, `CLIENTS.md`, `AGENT_HINTS.md`, `AGENT_HOOKS.md`, `AGENT_INSTALL_UNIVERSAL.md`, plus `AGENTS.md` and `CLAUDE.md`; 283 agent-instruction paths in total, and a `.jcodemunch.jsonc` config at the root.
- **`docs/cicd/`** — `AUDIT.md`, `DESIGN.md`, `FINDINGS.md`, `RUNBOOK.md`, `VERIFICATION.md`: the pipeline's own design and findings kept as documents.
- **A VS Code extension** (`vscode-extension/`) and an OpenTelemetry example (`examples/otel-collector/`).
- **Not here:** the index for your repository. It parses on demand rather than shipping a corpus.

## Transferable Capability
**Make the unit of retrieval the unit of meaning, and make the answer carry its own evidence.** Two independent ideas travel together here. The first is that returning a *whole document* when the question concerns one part of it wastes the reader's attention in proportion to how much of the document is irrelevant — a structural parse lets the boundary be a real boundary rather than a byte offset. The second is stronger and rarer: **define the shape of a defensible answer as a schema**, so a result must state what it matched, how confident it is and where that confidence came from, and cannot be a bare ranked list.

The third transferable thing is the measurement discipline. Separating *did we find it* (goldset) from *did we choose the right route* (route recall) from *are the descriptions any good* (description smells) means a regression can be attributed instead of merely observed — three questions that a single accuracy number silently averages together.

**Alternative to:** whole-file retrieval, which is correct and expensive; embedding-only search, which finds by resemblance and cannot say why; and to grep, which finds by spelling. **Applies wherever** a large corpus must be sampled precisely for a reader with a fixed attention budget — which includes any catalogue that answers questions about sources it does not include.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Code_Intelligence
- Maturity Stage: Active
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: REST
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: Callable

## Integration & Use Cases
- Read `benchmarks/METHODOLOGY.md` and the `route_recall` and `description_smells` layout before designing a retrieval evaluation of your own.
- Take the four answer schemas as a model for making a retrieval result self-justifying rather than merely ranked.
- Run it as an MCP server against a codebase to compare symbol-level retrieval against file-level retrieval on real questions.

## Reading Notes
Two things to weigh. The headline claims — 95% token reduction, 313 billion tokens saved — are the project's own marketing, stated in its GitHub description and on `jcodemunch.com`; the benchmark tree is unusually substantial and the methodology is committed, but **none of it was opened here**, so the numbers are recorded as claimed, not confirmed. Second, GitHub reported the licence as NOASSERTION; the `LICENSE` file was fetched and read and is the MIT licence reproduced in full, so `license_class` is Permissive on direct evidence rather than on the API's word. For this catalogue specifically it is the closest comparable system in the collection — an agent-facing retrieval service that measures its own answers — and the `description_smells` benchmark addresses a failure this catalogue has measured in itself.

## Semantic Links
- [parent_topic:: [[Topic - Code Intelligence & Structural Parsing]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[tree-sitter - tree-sitter]]]
- [related_to:: [[semgrep - mcp]]]
- [related_to:: [[roomi-fields - rtfm]]]
- [related_to:: [[fynnfluegge - codeqai]]]
- [related_to:: [[sturdy-dev - semantic-code-search]]]
- [implements_pattern:: [[Pattern - Structural Code Search]]]
- [implements_pattern:: [[Pattern - Semantic Code Retrieval]]]
- [implements_pattern:: [[Pattern - Multi-Tier Index Routing]]]
- [mentions_term:: [[Glossary - Model Context Protocol]]]
- [mentions_term:: [[Glossary - Abstract Syntax Tree]]]
- [mentions_term:: [[Glossary - Evidence Snippet]]]
- [mentions_term:: [[Glossary - Structural Search]]]

## Evidence
- Source URL: https://github.com/jgravelle/jcodemunch-mcp
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata, the complete file tree at HEAD, and the LICENSE file read in full; no source, schema or benchmark document was opened

## GitHub Snapshot

- Description: Cut AI token costs 95%+ on code exploration. The leading MCP server for precise, symbol-level GitHub code retrieval via tree-sitter AST. Works with Claude Code, Cursor & any MCP client. 313B+ tokens saved.
- Language: Python
- License (SPDX): NOASSERTION
- Default Branch: main
- Stars: 2651
- Homepage: https://jcodemunch.com/
- Pushed At: 2026-09-04T03:12:20Z
- Topics: ai-coding, ast, claude, claude-code, cline, code-intelligence, codex, context-window, copilot, cursor, developer-tools, gemini-cli, llm, mcp, mcp-server, model-context-protocol, opencode, token-optimization, tree-sitter, windsurf

## Evidence Anchors
- [github_repo] description :: Cut AI token costs 95%+ on code exploration. The leading MCP server for precise, symbol-level GitHub code retrieval via tree-sitter AST. Works with Claude Code, Cursor & any MCP client. 313B+ tokens saved. (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: NOASSERTION (confidence 0.90)
- [github_repo] topics :: ai-coding, ast, claude, claude-code, cline, code-intelligence, codex, context-window, copilot, cursor, developer-tools, gemini-cli, llm, mcp, mcp-server, model-context-protocol, opencode, token-optimization, tree-sitter, windsurf (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 1141 paths at HEAD (confidence 0.95)
