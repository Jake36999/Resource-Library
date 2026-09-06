---
uuid: "14ce2d93-e1c7-5cbf-939c-2a3e7704aaf7"
canonical_url: "https://github.com/javaparser/javaparser"
repo_key: "javaparser/javaparser"
owner: "javaparser"
repo_name: "javaparser"
aliases: ["javaparser/javaparser", "https://github.com/javaparser/javaparser"]
type: "developer_tool"
primary_topic: "Code Intelligence & Structural Parsing"
secondary_topics: ["Architecture & Developer Playbooks"]
ecosystem: "Mixed"
domain_primary: "Code_Intelligence"
maturity_stage: "Production_Ready"
license_class: "Weak_Copyleft"
deployment_target: "Local_Only"
interface_protocol: "CLI"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Lossless Syntax Tree", "Structural Code Search", "Schema-First Codegen"]
glossary_terms: ["Abstract Syntax Tree", "Symbol Solver", "Codemod", "Static Analysis"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "LGPL-3.0 or Apache-2.0 (see Reading Notes)"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: "Java 1-25 Parser and Abstract Syntax Tree for Java with advanced analysis functionalities."
github_language: "Java"
github_license_spdx: "NOASSERTION"
github_default_branch: "master"
github_stars: 6146
github_topics: ["abstract-syntax-tree", "ast", "code-analysis", "code-generation", "code-generator", "java", "javadoc", "javaparser", "javasymbolsolver", "parser", "syntax-tree"]
github_homepage: "https://javaparser.org"
github_pushed_at: "2026-09-04T03:09:45Z"
---
# javaparser - javaparser

## Bottom Line
A parser for every version of Java from 1 to 25 that produces a modifiable syntax tree, plus a separate symbol solver that answers what a name in that tree actually refers to — the step where parsing stops and understanding begins.

## What It Solves
- Analyse or rewrite Java source without running a compiler and without losing formatting.
- Answer *which declaration does this identifier resolve to*, across a classpath, which a parse tree alone cannot.
- Support a language whose syntax has changed twenty-five times without forking the parser for each version.

## Architecture & Mechanics
- Two independently useful halves ship in one repository: `javaparser-core` (578 files) parses and models, `javaparser-symbol-solver-core` (174 files) resolves names against a classpath. The second depends on the first; the first does not need the second.
- The parser is *generated*, not hand-written: `javaparser-core/src/main/javacc/java.jj` is the JavaCC grammar. Java's twenty-five versions are absorbed by editing one grammar rather than twenty-five parsers.
- Two further modules exist only to generate code from the model — `javaparser-core-generators` (44 files) and `javaparser-core-metamodel-generator` (7). The AST node classes are derived from a metamodel rather than typed by hand, which is why several hundred node types stay consistent.
- Serialisation is a separate module (`javaparser-core-serialization`), keeping the tree representation independent of any wire format.
- **Not read:** the grammar or any Java source. The module division and the generator relationship are read off the tree, the module names and `doc/component_diagram.puml`.

## What Is Inside
- **The largest test corpus in this catalogue's parsing family** — 1,833 test paths and 545 `.txt` files. `javaparser-symbol-solver-testing` alone is 1,436 files, more than twice the size of the core it tests: resolution, not parsing, is where the difficulty is.
- **A JavaCC grammar** — `javaparser-core/src/main/javacc/java.jj`: one file defining Java 1–25.
- **Behaviour-driven specifications** — `javaparser-core-testing-bdd/` with 9 `.story` files, a form of test that reads as prose.
- **Named regression fixtures** — `javaparser-core-testing/src/test/resources/com/github/javaparser/issue_samples/`, files named `Issue290.java.txt`, `Issue412.java.expected.txt`: each bug preserved as an input and its expected output.
- **A resolution cycle fixture** — `javaparser-symbol-solver-testing/src/test/resources/static_import_cycle_fixture/`: five files constructing a static-import cycle, the hard case written down.
- **`doc/component_diagram.puml`** — the module relationships as a diagram, and effectively the only architectural documentation in-tree.
- **Four licence files** — `LICENSE`, `LICENSE.APACHE`, `LICENSE.LGPL`, `LICENSE.GPL`. See Reading Notes.
- **Not here:** a code formatter or a linter. It gives you the tree and the resolution; the judgement is yours.

## Transferable Capability
**Separate parsing from resolution, and treat resolution as the harder problem.** A parse tree tells you the shape of a document; it cannot tell you what a name in it points at, because that answer depends on everything else in scope. Splitting the two lets each be replaced, tested and paid for independently — and the test ratio here, over two-to-one in favour of resolution, is the empirical argument for the split. Two further mechanisms carry over: **generate the node types from a metamodel** so a large type hierarchy cannot drift, and **derive the parser from a grammar** so evolving syntax is a diff to one file.

**Alternative to:** regular expressions over source, which cannot see scope; to running the real compiler, which needs a buildable project and gives back no editable tree; and to hand-written node classes, which drift as soon as they outnumber the people maintaining them. **Applies wherever** references must be followed through a structured document — configuration that refers to other configuration, schemas that import schemas, cross-referenced prose.

## Taxonomy
- Ecosystem: Mixed
- Domain Primary: Code_Intelligence
- Maturity Stage: Production_Ready
- License Class: Weak_Copyleft
- Deployment Target: Local_Only
- Interface Protocol: CLI
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Build a codemod or migration tool over `javaparser-core`, adding the symbol solver only when a rewrite depends on what a name resolves to.
- Study the metamodel generator before hand-writing a large AST type hierarchy in any language.
- Take the `issue_samples` convention — input and expected output preserved per bug — for any parser's regression suite.

## Reading Notes
**The licence needs a decision from a person, and this catalogue has deliberately not made it.** `LICENSE` states in prose that JavaParser is available under *either* the LGPL or the Apache licence and that the user chooses. That is a genuine dual licence and the permissive half would qualify almost any use. But this catalogue infers a choice only from an explicit SPDX `OR` expression, never from prose — a wording heuristic previously matched GPL boilerplate and reported two copyleft projects as permissive, so the rule was tightened and this is the cost of that decision. It is therefore classified at the more restrictive half, `Weak_Copyleft`, and appears in [[Licence Resolution 2026-09-03]] for confirmation. If confirmed, it becomes available to permissive-only queries. Note also that the tree contains `LICENSE.GPL` — that is present because the LGPL is written as an extension to it, not because JavaParser is GPL.

## Semantic Links
- [parent_topic:: [[Topic - Code Intelligence & Structural Parsing]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[tree-sitter - tree-sitter]]]
- [related_to:: [[Instagram - LibCST]]]
- [related_to:: [[cst - cst]]]
- [related_to:: [[whitequark - ast]]]
- [related_to:: [[semgrep - semgrep]]]
- [implements_pattern:: [[Pattern - Lossless Syntax Tree]]]
- [implements_pattern:: [[Pattern - Structural Code Search]]]
- [implements_pattern:: [[Pattern - Schema-First Codegen]]]
- [mentions_term:: [[Glossary - Abstract Syntax Tree]]]
- [mentions_term:: [[Glossary - Symbol Solver]]]
- [mentions_term:: [[Glossary - Codemod]]]
- [mentions_term:: [[Glossary - Static Analysis]]]

## Evidence
- Source URL: https://github.com/javaparser/javaparser
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata, the complete file tree at HEAD, and all four licence files read in full; no Java source or grammar file was opened

## GitHub Snapshot

- Description: Java 1-25 Parser and Abstract Syntax Tree for Java with advanced analysis functionalities.
- Language: Java
- License (SPDX): NOASSERTION
- Default Branch: master
- Stars: 6146
- Homepage: https://javaparser.org
- Pushed At: 2026-09-04T03:09:45Z
- Topics: abstract-syntax-tree, ast, code-analysis, code-generation, code-generator, java, javadoc, javaparser, javasymbolsolver, parser, syntax-tree

## Evidence Anchors
- [github_repo] description :: Java 1-25 Parser and Abstract Syntax Tree for Java with advanced analysis functionalities. (confidence 0.95)
- [github_repo] language :: Java (confidence 0.90)
- [github_repo] license :: NOASSERTION (confidence 0.90)
- [github_repo] topics :: abstract-syntax-tree, ast, code-analysis, code-generation, code-generator, java, javadoc, javaparser, javasymbolsolver, parser, syntax-tree (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 2674 paths at HEAD (confidence 0.95)
