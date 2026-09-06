---
uuid: "84a52949-047c-53fe-b890-b7523418c534"
canonical_url: "https://github.com/tree-sitter/tree-sitter"
repo_key: "tree-sitter/tree-sitter"
owner: "tree-sitter"
repo_name: "tree-sitter"
aliases: ["tree-sitter/tree-sitter", "https://github.com/tree-sitter/tree-sitter"]
type: "developer_tool"
primary_topic: "Code Intelligence & Structural Parsing"
secondary_topics: ["Architecture & Developer Playbooks"]
ecosystem: "Mixed"
domain_primary: "Code_Intelligence"
maturity_stage: "Production_Ready"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "CLI"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Structural Code Search", "Lossless Syntax Tree"]
glossary_terms: ["Incremental Parsing", "Concrete Syntax Tree", "Abstract Syntax Tree", "Structural Search"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-03"
evidence_count: 5
github_description: "An incremental parsing system for programming tools"
github_language: "Rust"
github_license_spdx: "MIT"
github_default_branch: "master"
github_stars: 26847
github_topics: ["c", "incremental", "parser", "parsing", "rust", "tree-sitter", "wasm"]
github_homepage: "https://tree-sitter.github.io"
github_pushed_at: "2026-09-03T14:35:55Z"
---
# tree-sitter - tree-sitter

## Bottom Line
A parser generator plus a dependency-free C runtime that keeps a concrete syntax tree correct while the file is being typed into, reparsing only what an edit actually invalidated and still producing a usable tree from broken source.

## What It Solves
- Give an editor a live syntax tree fast enough to update on every keystroke.
- Get structure out of a half-written file, where a compiler front end would simply fail.
- Add first-class tooling for a language nobody has written tooling for, by writing a grammar instead of a parser.

## Architecture & Mechanics
- A grammar is JavaScript (`grammar.js`); the CLI evaluates it via `node`, normalises it to a schema-checked JSON form, and generates a standalone C parser.
- The `prepare_grammar` stage splits one grammar into two — a syntax grammar over non-terminals and a lexical grammar over terminals — before parse tables are built.
- The runtime (`lib/src/`) is plain C: `subtree.c` and `reusable_node.h` hold the persistent tree that makes reuse possible, `stack.c` handles ambiguity, `get_changed_ranges.c` decides what an edit invalidated.
- `query.c` adds an S-expression query language over the tree, with node types, named fields, negated fields, captures and predicates; `crates/highlight` and `crates/tags` are built on it.

## What Is Inside
- **A C runtime you would embed** — `lib/src/` (~30 files, plain C, no dependencies):
  `subtree.c` and `reusable_node.h` hold the persistent tree, `stack.c` the GLR parse stack,
  `get_changed_ranges.c` the edit-invalidation logic, `query.c` the S-expression query engine.
- **A parser generator in Rust** — `crates/generate` (grammar → parse tables → `parser.c`),
  `crates/cli`, plus `crates/highlight` and `crates/tags` built on queries.
- **A documentation book** — `docs/src/`: `creating-parsers/` (6 chapters, including
  `4-external-scanners.md`), `using-parsers/` with a four-part `queries/` section, `cli/`
  reference per subcommand, and `5-implementation.md` which covers the generator and stops at
  "## The Runtime — WIP".
- **Machine-readable schemas** — `docs/src/assets/schemas/`: `grammar.schema.json`,
  `node-types.schema.json`, `config.schema.json`, `test-summary.schema.json`.
- **Bindings in-tree** — `lib/binding_rust/`, `lib/binding_web/` (TypeScript over WASM).
- **Not here:** the language grammars. Each lives in its own repository.

## Transferable Capability
**Keep an always-current structural model of a document that is being edited, by re-deriving only what an edit invalidated.** Two properties make it usable where full re-analysis would not be: it stays correct on incomplete or broken input, returning a usable structure rather than an error, and its cost is proportional to the change rather than to the document. A separate and independently valuable capability rides on the same structure: **a pattern language for asking questions of a tree** — matching by node kind, by named position, by absence of a part, capturing what matched.

**Alternative to:** re-processing a whole document on every change, which is why most structural tooling runs on save rather than continuously; and to matching structure with text patterns, which cannot express containment or position. **Applies wherever** structure must be tracked through change — live editing, incremental indexing, or a corpus re-derived far more often than it is written.

## Taxonomy
- Ecosystem: Mixed
- Domain Primary: Code_Intelligence
- Maturity Stage: Production_Ready
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: CLI
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Build syntax highlighting, folding or code navigation for an unsupported language.
- Extract structure from source files as the parsing layer beneath an analysis tool.
- Study incremental parsing and error recovery in a readable, self-contained C runtime.

## Reading Notes
Two things the metadata will mislead on. GitHub reports the language as **Rust**, but the Rust is the generator and CLI — a build tool that is not needed once a parser exists; the artefact you embed is C. And `docs/src/5-implementation.md` documents the CLI thoroughly and then stops at "## The Runtime — WIP": the incremental algorithm that is the project's reason for existing is documented only in its source.

## Semantic Links
- [parent_topic:: [[Topic - Code Intelligence & Structural Parsing]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[semgrep - semgrep]]]
- [related_to:: [[Instagram - LibCST]]]
- [related_to:: [[syntax-tree - mdast]]]
- [implements_pattern:: [[Pattern - Structural Code Search]]]
- [implements_pattern:: [[Pattern - Lossless Syntax Tree]]]
- [mentions_term:: [[Glossary - Incremental Parsing]]]
- [mentions_term:: [[Glossary - Concrete Syntax Tree]]]
- [mentions_term:: [[Glossary - Abstract Syntax Tree]]]
- [mentions_term:: [[Glossary - Structural Search]]]

## Evidence
- Source URL: https://github.com/tree-sitter/tree-sitter
- Source kind: GitHub REST metadata plus the repository tree and files, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-03
- Depth of read: recorded per source in [[Scouting Working File 2026-09-03]]

## GitHub Snapshot

- Description: An incremental parsing system for programming tools
- Language: Rust
- License (SPDX): MIT
- Default Branch: master
- Stars: 26847
- Homepage: https://tree-sitter.github.io
- Pushed At: 2026-09-03T14:35:55Z
- Topics: c, incremental, parser, parsing, rust, tree-sitter, wasm

## Evidence Anchors
- [github_repo] description :: An incremental parsing system for programming tools (confidence 0.95)
- [github_repo] language :: Rust (confidence 0.90)
- [github_repo] license :: MIT (confidence 0.90)
- [github_repo] topics :: c, incremental, parser, parsing, rust, tree-sitter, wasm (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-03 (confidence 0.95)
