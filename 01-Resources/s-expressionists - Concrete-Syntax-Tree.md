---
uuid: "e62d1103-21a2-5644-886d-cca606385932"
canonical_url: "https://github.com/s-expressionists/Concrete-Syntax-Tree"
repo_key: "s-expressionists/Concrete-Syntax-Tree"
owner: "s-expressionists"
repo_name: "Concrete-Syntax-Tree"
aliases: ["s-expressionists/Concrete-Syntax-Tree", "https://github.com/s-expressionists/Concrete-Syntax-Tree"]
type: "developer_tool"
primary_topic: "Code Intelligence & Structural Parsing"
secondary_topics: ["Architecture & Developer Playbooks"]
ecosystem: "Mixed"
domain_primary: "Code_Intelligence"
maturity_stage: "Active"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "CLI"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Lossless Syntax Tree"]
glossary_terms: ["Concrete Syntax Tree", "Abstract Syntax Tree"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "BSD-2-Clause"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: "Concrete Syntax Trees represent s-expressions with source information"
github_language: "Common Lisp"
github_license_spdx: "BSD-2-Clause"
github_default_branch: "master"
github_stars: 62
github_topics: ["compiler", "parsing", "syntax-tree"]
github_homepage: "https://s-expressionists.github.io/Concrete-Syntax-Tree/"
github_pushed_at: "2025-08-22T14:12:42Z"
---
# s-expressionists - Concrete-Syntax-Tree

## Bottom Line
A Common Lisp library that attaches source location to s-expressions without changing what they are — solving the problem of a language whose parser hands you data with no record of where the data came from.

## What It Solves
- Report an error at the line the user wrote, in a language where reading source produces plain data.
- Destructure a form against a lambda list and keep source positions attached to every extracted part.
- Give a macro or compiler enough position information to be diagnosable, without a separate parser.

## Architecture & Mechanics
- The problem is specific to homoiconic languages: `read` returns a cons tree that *is* the program, with the source text discarded. A CST wraps each cons in an object that also carries its origin, so the shape is preserved and the position is recovered.
- Conversion runs both ways and each direction is its own file: `cst-from-expression.lisp` and `cstify.lisp` build a CST; `listify.lisp` and `cons-cst.lisp` go back.
- The `Lambda-list/` directory (20 files, with its own grammar files and test suite) is the largest component after the core — destructuring while preserving source information is where the real difficulty lies, not in wrapping conses.
- Conditions are separated from their wording: `conditions.lisp` defines them, `condition-reporters-english.lisp` phrases them. Diagnostics are translatable by construction.
- **Not read:** any Lisp source. The above is inferred from filenames, which in this repository are unusually descriptive.

## What Is Inside
- **A Texinfo manual** — `documentation/`: `chapter-introduction.texi`, `chapter-user-manual.texi`, `chapter-internals.texi` and a Makefile. Rare in this catalogue: a parsing library with a real manual rather than a README.
- **A lambda-list grammar as data** — `Lambda-list/grammar.lisp`, `grammar-symbols.lisp`, `standard-grammars.lisp`, with `Lambda-list/Test/` including `random-lambda-list.lisp` and `compare-parse-trees.lisp` — a generator and a differential comparison, i.e. property-based testing of the destructurer.
- **Separated diagnostics** — `conditions.lisp` and `condition-reporters-english.lisp`: the error taxonomy and its English wording are different files.
- **21 Lisp files at the repository root**, which is Common Lisp convention rather than disorder; `concrete-syntax-tree.asd` is the system definition that orders them.
- **Not here:** a reader. It works with what `read` gives you; it does not replace it.

## Transferable Capability
**Attach origin to a value without changing the value's shape, so that existing code keeps working and new code can ask where something came from.** This is the general form of a recurring problem: a representation is correct but has lost the link back to what produced it, and diagnostics, auditing and traceability all fail downstream for the same reason. Wrapping rather than replacing is what makes the fix adoptable — nothing already written has to change. Two techniques here transfer directly: **generating random inputs and comparing two implementations' outputs** as the way to test a destructurer, and **separating an error's identity from its wording** so messages can be translated or rephrased without touching the logic.

**Alternative to:** a side table mapping values to positions, which breaks as soon as values are copied or shared; and to giving up on positions, which is what most homoiconic tooling historically did. **Applies wherever** provenance must ride along with data through transformations — which is the same shape as the lineage problem in [[Topic - Data Lineage & Provenance]], approached from the language side.

## Taxonomy
- Ecosystem: Mixed
- Domain Primary: Code_Intelligence
- Maturity Stage: Active
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: CLI
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Use it to give a Lisp macro or compiler diagnostics that point at the user's source rather than at expanded forms.
- Read `Lambda-list/Test/random-lambda-list.lisp` as a compact example of property-based testing against a reference implementation.
- Study the wrap-don't-replace approach when position information must be threaded through an existing pipeline that cannot be rewritten.

## Reading Notes
Sixty-two stars understates it: this underpins the SICL compiler work, and its audience is small and specialised rather than casual. Actively maintained (last pushed 2025-08-22). Its documentation is a genuine outlier in this topic — a Texinfo manual with an internals chapter, where comparable projects ship a README — and that alone makes it worth reading even for someone who will never write Common Lisp.

## Semantic Links
- [parent_topic:: [[Topic - Code Intelligence & Structural Parsing]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[whitequark - ast]]]
- [related_to:: [[Instagram - LibCST]]]
- [related_to:: [[cst - cst]]]
- [related_to:: [[nene - sql-parser-cst]]]
- [implements_pattern:: [[Pattern - Lossless Syntax Tree]]]
- [mentions_term:: [[Glossary - Concrete Syntax Tree]]]
- [mentions_term:: [[Glossary - Abstract Syntax Tree]]]

## Evidence
- Source URL: https://github.com/s-expressionists/Concrete-Syntax-Tree
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; no Lisp source or Texinfo chapter was opened

## GitHub Snapshot

- Description: Concrete Syntax Trees represent s-expressions with source information
- Language: Common Lisp
- License (SPDX): BSD-2-Clause
- Default Branch: master
- Stars: 62
- Homepage: https://s-expressionists.github.io/Concrete-Syntax-Tree/
- Pushed At: 2025-08-22T14:12:42Z
- Topics: compiler, parsing, syntax-tree

## Evidence Anchors
- [github_repo] description :: Concrete Syntax Trees represent s-expressions with source information (confidence 0.95)
- [github_repo] language :: Common Lisp (confidence 0.90)
- [github_repo] license :: BSD-2-Clause (confidence 0.90)
- [github_repo] topics :: compiler, parsing, syntax-tree (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 91 paths at HEAD (confidence 0.95)
