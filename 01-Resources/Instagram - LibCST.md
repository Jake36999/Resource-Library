---
uuid: "bd1fd03d-cbc0-5da5-89a1-28b8662897cf"
canonical_url: "https://github.com/Instagram/LibCST"
repo_key: "Instagram/LibCST"
owner: "Instagram"
repo_name: "LibCST"
aliases: ["Instagram/LibCST", "https://github.com/Instagram/LibCST"]
type: "developer_tool"
primary_topic: "Code Intelligence & Structural Parsing"
secondary_topics: ["Architecture & Developer Playbooks"]
ecosystem: "Python"
domain_primary: "Code_Intelligence"
maturity_stage: "Production_Ready"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Python_SDK"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Lossless Syntax Tree", "Structural Code Search"]
glossary_terms: ["Concrete Syntax Tree", "Abstract Syntax Tree", "Codemod", "Structural Search"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT (with PSF dual-licensed parser files and one Apache-2.0 file)"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-03"
evidence_count: 5
github_description: "A concrete syntax tree parser and serializer library for Python that preserves many aspects of Python's abstract syntax tree"
github_language: "Python"
github_license_spdx: "NOASSERTION"
github_default_branch: "main"
github_stars: 1940
github_topics: []
github_homepage: "https://libcst.readthedocs.io/"
github_pushed_at: "2026-08-11T05:22:09Z"
---
# Instagram - LibCST

## Bottom Line
A Python tree that keeps every comment, space and parenthesis as a field on the node that owns it — so it navigates like an AST but prints back byte-identically — wrapped in a codemod framework that is larger than the parser.

## What It Solves
- Rewrite Python across a large codebase and produce a diff containing only the intended change.
- Parse Python 3.0 through 3.15 syntax from whatever interpreter you happen to be running.
- Ask questions a syntax tree cannot answer alone — what scope binds this name, what type is this expression — without leaving the tree.

## Architecture & Mechanics
- `libcst/_nodes/` (66 files) defines the tree; whitespace is a field on its owning node rather than a sibling, which is the whole design compromise.
- `libcst/codemod/` is the largest subsystem at 73 files: a command abstraction, a process-pool runner, a context, a CLI, a test harness, and ready-made commands such as `remove_unused_imports` and `convert_percent_format_to_fstring`.
- `libcst/metadata/` (29 files) computes what the tree does not contain — scope, qualified names, positions, parents — and `type_inference_provider` shells out to Pyre for real types.
- `libcst/matchers/` expresses patterns declaratively instead of as nested `isinstance` checks; `native/` is a Rust parser with its own grammar and benchmarks.

## What Is Inside
- **A codemod framework** — `libcst/codemod/` is the largest subsystem at 73 files: `_command.py`,
  `_runner.py` (process pool), `_context.py`, `_testing.py`, a CLI, and `commands/` with
  ready-made transforms (`remove_unused_imports`, `rename`, `convert_percent_format_to_fstring`,
  `convert_union_to_or`, `convert_namedtuple_to_dataclass`, `add_trailing_commas`).
- **The tree** — `libcst/_nodes/` (66 files), with whitespace as a field on its owning node.
- **Two parsers** — `libcst/_parser/` (53 files, pure Python, partly derived from `parso`) and
  `native/libcst/` (Rust, with its own `Grammar` file and `benches/parser_benchmark.rs`).
- **Metadata providers** — `libcst/metadata/`: `scope_provider`, `name_provider`,
  `position_provider`, `parent_node_provider`, `expression_context_provider`,
  `type_inference_provider` (shells out to Pyre), `full_repo_manager` for cross-file providers.
- **Declarative matchers** — `libcst/matchers/`, patterns as data rather than nested `isinstance`.
- **A runnable tutorial** — `docs/source/tutorial.ipynb`, linked from Binder.

## Transferable Capability
**Model a document so that changing one part of it leaves every other byte identical.** The trick is where the incidental detail lives: attach spacing and commentary to the element that owns it, rather than making it a peer, so navigation stays simple while nothing is discarded. The consequence is that a mechanical change produces a reviewable difference instead of a rewritten file — which is the difference between an automated change that can be merged and one that cannot.

A separable second idea: **compute the facts a structure does not contain as detachable providers over it** — scope, identity, position, inferred type — so the structure stays minimal and the analyses stay optional.

**Alternative to:** representations that discard what they consider insignificant, which forces a reformat on every edit; and to bolting analysis results onto the structure itself. **Applies wherever** something must be modified mechanically and reviewed by a person afterwards.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Code_Intelligence
- Maturity Stage: Production_Ready
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Python_SDK
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Run an API migration across thousands of files as a reviewable change.
- Write a lint rule that needs scope information, not just syntax.
- Borrow the codemod runner and test harness rather than the parser.

## Reading Notes
The GitHub API reports the licence as **NOASSERTION/Other** because `LICENSE` is a composite: contributions are MIT, eleven parser and tokenizer files derived from the standard library and `parso` are dual MIT/PSF, and `libcst/_add_slots.py` is Apache-2.0. All three are permissive. Separately, the description calls this a parser and serializer; by file count it is a codemod platform with a parser inside it.

## Semantic Links
- [parent_topic:: [[Topic - Code Intelligence & Structural Parsing]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[tree-sitter - tree-sitter]]]
- [related_to:: [[semgrep - semgrep]]]
- [implements_pattern:: [[Pattern - Lossless Syntax Tree]]]
- [implements_pattern:: [[Pattern - Structural Code Search]]]
- [mentions_term:: [[Glossary - Concrete Syntax Tree]]]
- [mentions_term:: [[Glossary - Abstract Syntax Tree]]]
- [mentions_term:: [[Glossary - Codemod]]]
- [mentions_term:: [[Glossary - Structural Search]]]

## Evidence
- Source URL: https://github.com/Instagram/LibCST
- Source kind: GitHub REST metadata plus the repository tree and files, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-03
- Depth of read: recorded per source in [[Scouting Working File 2026-09-03]]

## GitHub Snapshot

- Description: A concrete syntax tree parser and serializer library for Python that preserves many aspects of Python's abstract syntax tree
- Language: Python
- License (SPDX): NOASSERTION
- Default Branch: main
- Stars: 1940
- Homepage: https://libcst.readthedocs.io/
- Pushed At: 2026-08-11T05:22:09Z
- Topics: Unknown

## Evidence Anchors
- [github_repo] description :: A concrete syntax tree parser and serializer library for Python that preserves many aspects of Python's abstract syntax tree (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: NOASSERTION (confidence 0.90)
- [github_repo] topics :: Unknown (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-03 (confidence 0.95)
