---
uuid: "e00dfd54-c51d-58fb-93f6-a03d31a24030"
canonical_url: "https://github.com/bstee615/tree-climber"
repo_key: "bstee615/tree-climber"
owner: "bstee615"
repo_name: "tree-climber"
aliases: ["bstee615/tree-climber", "https://github.com/bstee615/tree-climber"]
type: "developer_tool"
primary_topic: "Code Intelligence & Structural Parsing"
secondary_topics: ["Architecture & Developer Playbooks"]
ecosystem: "Python"
domain_primary: "Code_Intelligence"
maturity_stage: "Active"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "CLI"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "Documented"
patterns: ["Program Graph Construction", "Structural Code Search"]
glossary_terms: ["Control Flow Graph", "Abstract Syntax Tree", "Static Analysis", "Taint Analysis"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: "Program analysis tools built on tree-sitter (https://github.com/tree-sitter/tree-sitter)."
github_language: "Python"
github_license_spdx: "MIT"
github_default_branch: "master"
github_stars: 72
github_topics: ["hacktoberfest"]
github_pushed_at: "2025-11-24T18:16:50Z"
---
# bstee615 - tree-climber

## Bottom Line
Program analysis built on top of tree-sitter: it takes the syntax tree and derives the graphs that syntax alone cannot give you — control flow, data flow, and the combined code property graph — for C and Java, with a browser viewer for the result.

## What It Solves
- Get a control-flow graph from source without a compiler front end or a build that succeeds.
- Follow a value from where it is assigned to where it is used, across statements.
- See the resulting graph, rather than reading it as an adjacency list.

## Architecture & Mechanics
- The layering is the point: tree-sitter supplies the syntax tree, and `src/tree_climber/` (56 files) derives control flow and data flow from it. Nothing here parses; everything here is what parsing does not give you.
- The three graph kinds are separate and separately tested: `test/c_cfg` (6), `test/java_cfg` (5), `test/dfg` (5), plus `test/parse_trees` (5) checking the input assumption itself.
- Visualisation is in-tree, not an afterthought: `src/tree_climber/viz/` with `test_api.py`, and vendored front-end libraries under `lib/vis-9.1.2/` and `lib/tom-select/`.
- Language support is grounded in machine-readable grammar data: `docs/grammars/c/node-types.json` and `docs/grammars/java/node-types.json` — the node vocabulary the analysis must handle, as data rather than as knowledge in someone's head.
- **Not read:** any Python source. The layering and graph kinds are read off directory names, test names and the repository's stated purpose.

## What Is Inside
- **A design-document trail** — `docs/plans/` (8 files) including `extending-languages.md`, `def-use-solver-plan.md`, and two dated bug-fix plans (`fix-dfg-parameter-alias-2025-08-15.md`, `fix-function-call-cfg-edges-2025-08-14.md`), plus `docs/plans/test-plans/` with per-language comprehensive testing plans. The reasoning behind changes is committed, not just the changes.
- **Rendered example graphs** — `test/example.c` with `example.c_cfg.png`, `example.c_cpg.png` and `example.c_cpg_bigraph.png`: the same program as three different graphs, side by side.
- **Grammar node-type data** — `docs/grammars/c/node-types.json`, `docs/grammars/java/node-types.json`.
- **A viewer with vendored front-end libraries** — `src/tree_climber/viz/`, `lib/vis-9.1.2/`, `lib/tom-select/`.
- **`CLAUDE.md` and `.claude/settings.json`** at the root — agent instructions are present, though there is no callable interface.
- **Not here:** a parser, and any language but C and Java. `docs/plans/extending-languages.md` is the route to more.

## Transferable Capability
**Derive the graphs you need from a syntax tree you did not have to build.** Control flow and data flow are not in the syntax — they are computed from it — and separating the two layers means the derivation is portable to any language the underlying parser already handles. The wider lesson is about *which* representation answers a question: syntax answers what was written, control flow answers what can run in what order, data flow answers what depends on what, and asking the wrong graph gives a confidently wrong answer.

The practice worth stealing independently of the analysis is the **committed plan directory**: dated design and fix documents alongside the code, so a later reader can see what the author was trying to do and not just what they did.

**Alternative to:** a compiler-based analysis framework, which needs a project that builds; and to pattern-matching over syntax, which cannot express *reaches* or *happens before*. **Applies wherever** dependency or ordering must be derived from a structure that only records shape — build graphs, pipeline dependencies, document cross-references.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Code_Intelligence
- Maturity Stage: Active
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: CLI
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: Documented

## Integration & Use Cases
- Build a taint or reachability analysis over C or Java without requiring the project to compile.
- Read `docs/plans/` as a compact worked example of keeping design reasoning next to the code it explains.
- Use the three rendered graphs of `test/example.c` to teach the difference between syntax, control flow and a code property graph.

## Reading Notes
Seventy-two stars and a single GitHub topic of `hacktoberfest` understate what is here: this is a research-adjacent implementation of graph constructions that are usually locked inside much heavier frameworks, and the `docs/plans/` trail makes it unusually readable. Last pushed 2025-11-24. Two limits to be clear about: **C and Java only**, and the analysis inherits whatever tree-sitter's grammars get right or wrong — which is a dependency on someone else's grammar quality, not on this project's.

## Semantic Links
- [parent_topic:: [[Topic - Code Intelligence & Structural Parsing]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[tree-sitter - tree-sitter]]]
- [related_to:: [[semgrep - semgrep]]]
- [related_to:: [[javaparser - javaparser]]]
- [implements_pattern:: [[Pattern - Program Graph Construction]]]
- [implements_pattern:: [[Pattern - Structural Code Search]]]
- [mentions_term:: [[Glossary - Control Flow Graph]]]
- [mentions_term:: [[Glossary - Abstract Syntax Tree]]]
- [mentions_term:: [[Glossary - Static Analysis]]]
- [mentions_term:: [[Glossary - Taint Analysis]]]

## Evidence
- Source URL: https://github.com/bstee615/tree-climber
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; no Python source, plan document or grammar file was opened

## GitHub Snapshot

- Description: Program analysis tools built on tree-sitter (https://github.com/tree-sitter/tree-sitter).
- Language: Python
- License (SPDX): MIT
- Default Branch: master
- Stars: 72
- Pushed At: 2025-11-24T18:16:50Z
- Topics: hacktoberfest

## Evidence Anchors
- [github_repo] description :: Program analysis tools built on tree-sitter (https://github.com/tree-sitter/tree-sitter). (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: MIT (confidence 0.90)
- [github_repo] topics :: hacktoberfest (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 127 paths at HEAD (confidence 0.95)
