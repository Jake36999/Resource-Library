---
uuid: "ad6c364a-66a5-54ac-a451-da4e994a7245"
canonical_url: "https://github.com/cst/cst"
repo_key: "cst/cst"
owner: "cst"
repo_name: "cst"
aliases: ["cst/cst", "https://github.com/cst/cst"]
type: "developer_tool"
primary_topic: "Code Intelligence & Structural Parsing"
secondary_topics: []
ecosystem: "Web_Frontend"
domain_primary: "Code_Intelligence"
maturity_stage: "Abandoned"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "CLI"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Lossless Syntax Tree"]
glossary_terms: ["Concrete Syntax Tree", "Abstract Syntax Tree", "Codemod"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: ":herb: JavaScript Concrete Syntax Tree "
github_language: "JavaScript"
github_license_spdx: "MIT"
github_default_branch: "master"
github_stars: 463
github_topics: ["ast", "babylon", "cst"]
github_pushed_at: "2022-12-06T19:46:59Z"
---
# cst - cst

## Bottom Line
A JavaScript concrete syntax tree built as a layer over Babylon's abstract tree, adding back the whitespace, comments and token positions that the abstract tree throws away, with an index so lookups do not walk the whole tree.

## What It Solves
- Edit JavaScript source and print it back with everything untouched still byte-identical.
- Get token-level positions for a tree produced by a parser that only reports node ranges.
- Look up a node by position quickly enough to drive an editor.

## Architecture & Mechanics
- It does not parse. Babylon parses; `cst` builds a concrete tree over that result. The abstract tree is the input, not the output — a layering choice with a clear consequence, since it inherits Babylon's language support for free and its limits along with it.
- `src/elements/` is 103 of the 118 source files: one element type per JavaScript construct. The tree's fidelity is spent almost entirely on enumerating node kinds.
- Indexing is treated as an explicit, measurable decision — `test/benchmarks/elements/indexElements.js` and `noIndexElements.js` are a *paired* benchmark, so the cost of the index is recorded rather than assumed.
- `src/plugins/` (8 files) leaves room for behaviour to be added without changing the element types.
- **Not read:** any JavaScript source. The layering and the element/plugin split are read off directory structure and the benchmark filenames.

## What Is Inside
- **103 element types** — `src/elements/`, one per JavaScript construct: the concrete inventory of what the tree can represent.
- **A paired index benchmark** — `test/benchmarks/elements/indexElements.js` against `noIndexElements.js`, plus `test/benchmarks/benchmarks.js`. Rare and worth borrowing: the with/without comparison for an optimisation is committed, not just claimed.
- **Third-party conformance testing** — `test/3rdParty/babylon` (a submodule), `test/3rdParty/index.js`, and `test/3rdParty/xfail.json`: the project runs Babylon's own suite and keeps an explicit list of known failures.
- **104 test files against 118 source files** — near parity.
- **`docs/cst-example.png`** — the only documentation asset in the tree.
- **Not here:** a parser, a formatter, or support for anything Babylon cannot read.

## Transferable Capability
**Add fidelity as a layer over an existing parser instead of writing a new one.** The concrete tree is derived from the abstract one plus the original text, which buys the whole of someone else's language coverage and confines your work to what they discarded. The price is a hard ceiling at the underlying parser's capability, and a dependency on its release cadence — which is visible in this repository's own history. Two smaller mechanisms are independently worth taking: an **`xfail` list**, which turns *we run their suite and some of it fails* into a reviewable file, and a **paired benchmark**, which records what an optimisation actually bought instead of asserting it.

**Alternative to:** writing a full concrete parser, as [[nene - sql-parser-cst]] does, which costs far more and answers to nobody; and to string patching, which preserves everything by understanding nothing. **Applies wherever** an existing analyser is nearly right and the gap is recoverable from the original input.

## Taxonomy
- Ecosystem: Web_Frontend
- Domain Primary: Code_Intelligence
- Maturity Stage: Abandoned
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: CLI
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Study the layering when a project needs lossless edits and an abstract parser already exists for the language.
- Copy the `xfail.json` convention for any project that runs an upstream conformance suite it does not fully pass.
- Copy the paired with/without benchmark for any optimisation whose cost is being taken on trust.

## Reading Notes
**Last pushed 2022-12-06 and not touched since**, against 463 stars — the star count reflects the idea, not current maintenance. It is classified `Abandoned` on that evidence. More consequentially, it is built on **Babylon**, which was renamed `@babel/parser` in 2018; a layer over a parser inherits that parser's fate, which is the concrete form of the risk its own architecture takes on. Read it for the design. Do not adopt it for new work without checking what it resolves to today.

## Semantic Links
- [parent_topic:: [[Topic - Code Intelligence & Structural Parsing]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[Instagram - LibCST]]]
- [related_to:: [[nene - sql-parser-cst]]]
- [related_to:: [[ajaxorg - treehugger]]]
- [related_to:: [[tree-sitter - tree-sitter]]]
- [implements_pattern:: [[Pattern - Lossless Syntax Tree]]]
- [mentions_term:: [[Glossary - Concrete Syntax Tree]]]
- [mentions_term:: [[Glossary - Abstract Syntax Tree]]]
- [mentions_term:: [[Glossary - Codemod]]]

## Evidence
- Source URL: https://github.com/cst/cst
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; no JavaScript source or test file was opened

## GitHub Snapshot

- Description: :herb: JavaScript Concrete Syntax Tree 
- Language: JavaScript
- License (SPDX): MIT
- Default Branch: master
- Stars: 463
- Pushed At: 2022-12-06T19:46:59Z
- Topics: ast, babylon, cst

## Evidence Anchors
- [github_repo] description :: :herb: JavaScript Concrete Syntax Tree  (confidence 0.95)
- [github_repo] language :: JavaScript (confidence 0.90)
- [github_repo] license :: MIT (confidence 0.90)
- [github_repo] topics :: ast, babylon, cst (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 235 paths at HEAD (confidence 0.95)
