---
uuid: "905e2afa-30ab-56e0-be39-b6cf49eee06a"
canonical_url: "https://github.com/nene/sql-parser-cst"
repo_key: "nene/sql-parser-cst"
owner: "nene"
repo_name: "sql-parser-cst"
aliases: ["nene/sql-parser-cst", "https://github.com/nene/sql-parser-cst"]
type: "developer_tool"
primary_topic: "Code Intelligence & Structural Parsing"
secondary_topics: ["Data APIs & Big Data"]
ecosystem: "Mixed"
domain_primary: "Code_Intelligence"
maturity_stage: "Active"
license_class: "Copyleft"
deployment_target: "Local_Only"
interface_protocol: "CLI"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Lossless Syntax Tree", "Structural Code Search"]
glossary_terms: ["Concrete Syntax Tree", "Abstract Syntax Tree", "Data Lineage"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "GPL-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 5
github_description: "Parses SQL into Concrete Syntax Tree (CST)"
github_language: "TypeScript"
github_license_spdx: "GPL-2.0"
github_default_branch: "master"
github_stars: 189
github_pushed_at: "2026-08-23T18:01:22Z"
---
# nene - sql-parser-cst

## Bottom Line
A SQL parser that keeps every comment, every piece of whitespace and every quirk of the original text in the tree, across five dialects — so SQL can be rewritten and printed back out unchanged except where it was deliberately changed.

## What It Solves
- Rewrite SQL programmatically without reformatting the parts nobody asked to touch.
- Parse the same statement across dialects that disagree, without maintaining five parsers.
- Give a tool a tree over SQL rather than a regex, which is the precondition for column-level analysis.

## Architecture & Mechanics
- One PEG grammar, `src/parser.pegjs`, compiled by ts-pegjs into TypeScript, produces the whole parser. Dialect differences are conditions in that one grammar, not five forks.
- The `src/cst/` directory (51 files) is the node-type definition — the shape of the tree is written down as types rather than being whatever the parser happens to emit.
- `src/showNode/` (47 files) is nearly the same size as `src/cst/`: printing back out is treated as a first-class concern requiring one printer per node kind, which is what *lossless* costs.
- The test tree is organised by SQL construct, not by dialect — `test/expr` (25), `test/select` (24), `test/ddl` (23), `test/proc` (19), `test/literal` (10), `test/dml` (5), `test/dcl` (3) — with dialect-specific directories (`test/postgresql`, `test/bigquery`) only where behaviour genuinely diverges.
- **Not read:** the grammar or any TypeScript source. The structure above is read off directory names and file counts.

## What Is Inside
- **A PEG grammar for five SQL dialects** — `src/parser.pegjs`, one file.
- **141 test files organised by SQL construct**, which doubles as an inventory of what the parser accepts: expressions, selects, DDL, stored procedures, literals, DML, DCL, and dialect-specific behaviour for PostgreSQL and BigQuery.
- **A performance suite with real SQL** — `perf/`: `data-bigquery.sql`, `data-mysql.sql`, `data-sqlite.sql`, `data-select.sql`, `data-case.sql`, driven by `perf/perf-test.ts`. Five dialects' worth of sample SQL, usable as test input on its own.
- **A printer per node type** — `src/showNode/`, 47 files, the half of the project that makes round-tripping possible.
- **`AUTHORS`** at the root, and `LICENSE` — GPL-2.0, which is unusual for a JavaScript parsing library and consequential; see Reading Notes.
- **Not here:** any execution or planning. It parses SQL; it does not know what a table is.

## Transferable Capability
**Keep the parts of a document that carry no meaning to the machine but every bit of meaning to the person who wrote it.** Comments, spacing and quoting style are exactly what a compiler discards and exactly what makes a diff reviewable. Preserving them turns a parser from an analysis tool into a *rewriting* tool, and the cost is visible here: the printer is nearly as large as the type definitions, because losslessness is paid for one node kind at a time. The organising choice worth copying is **testing by construct and specialising by dialect only where behaviour diverges**, which keeps the common case in one place instead of duplicated five ways.

**Alternative to:** an abstract syntax tree, which is smaller and cannot round-trip; to string manipulation, which round-trips perfectly and understands nothing; and to a formatter, which normalises everything including what you did not touch. **Applies wherever** a machine edits a document a person will read afterwards — configuration, schemas, generated code, structured prose.

## Taxonomy
- Ecosystem: Mixed
- Domain Primary: Code_Intelligence
- Maturity Stage: Active
- License Class: Copyleft
- Deployment Target: Local_Only
- Interface Protocol: CLI
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Build a SQL migration or refactoring tool that leaves unrelated lines byte-identical.
- Use the tree as the substrate for column-level lineage, where a purely textual approach cannot see structure.
- Take the five dialects' `perf/*.sql` files as ready-made SQL test input for anything else that reads SQL.

## Reading Notes
**GPL-2.0**, which for a library that gets linked into tooling is the fact that decides whether it can be used at all. It is filtered out of any permissive-constrained answer here, correctly. That places it in direct contrast with [[shenhuan2021 - gudu-sql-omni-introduce]], which addresses adjacent ground under different terms — if a SQL tree is needed inside a product, the licence, not the feature set, is likely to be the deciding comparison. Actively maintained: last pushed 2026-08-23.

## Semantic Links
- [parent_topic:: [[Topic - Code Intelligence & Structural Parsing]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[shenhuan2021 - gudu-sql-omni-introduce]]]
- [related_to:: [[Instagram - LibCST]]]
- [related_to:: [[cst - cst]]]
- [related_to:: [[tree-sitter - tree-sitter]]]
- [implements_pattern:: [[Pattern - Lossless Syntax Tree]]]
- [implements_pattern:: [[Pattern - Structural Code Search]]]
- [mentions_term:: [[Glossary - Concrete Syntax Tree]]]
- [mentions_term:: [[Glossary - Abstract Syntax Tree]]]
- [mentions_term:: [[Glossary - Data Lineage]]]

## Evidence
- Source URL: https://github.com/nene/sql-parser-cst
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; no grammar or TypeScript source file was opened

## GitHub Snapshot

- Description: Parses SQL into Concrete Syntax Tree (CST)
- Language: TypeScript
- License (SPDX): GPL-2.0
- Default Branch: master
- Stars: 189
- Pushed At: 2026-08-23T18:01:22Z

## Evidence Anchors
- [github_repo] description :: Parses SQL into Concrete Syntax Tree (CST) (confidence 0.95)
- [github_repo] language :: TypeScript (confidence 0.90)
- [github_repo] license :: GPL-2.0 (confidence 0.90)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 292 paths at HEAD (confidence 0.95)
