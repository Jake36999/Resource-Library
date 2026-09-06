---
uuid: "219ded9d-e458-5f56-8048-56b068aa8340"
canonical_url: "https://github.com/ajaxorg/treehugger"
repo_key: "ajaxorg/treehugger"
owner: "ajaxorg"
repo_name: "treehugger"
aliases: ["ajaxorg/treehugger", "https://github.com/ajaxorg/treehugger"]
type: "developer_tool"
primary_topic: "Code Intelligence & Structural Parsing"
secondary_topics: []
ecosystem: "Web_Frontend"
domain_primary: "Code_Intelligence"
maturity_stage: "Abandoned"
license_class: "Permissive"
deployment_target: "Browser"
interface_protocol: "CLI"
data_locality: "Local_First"
hardware_footprint: "Browser_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Structural Code Search", "Lossless Syntax Tree"]
glossary_terms: ["Abstract Syntax Tree", "Structural Search", "Codemod"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 5
github_description: "JavaScript AST (Abstract Syntax Tree) transformation tools"
github_language: "JavaScript"
github_license_spdx: "MIT"
github_default_branch: "master"
github_stars: 483
github_homepage: "http://ajaxorg.github.com/treehugger/test.html"
github_pushed_at: "2020-02-13T00:15:13Z"
---
# ajaxorg - treehugger

## Bottom Line
A seventeen-file JavaScript AST transformation library from the Cloud9 editor, whose distinguishing idea is a term-rewriting match-and-replace vocabulary over trees rather than an imperative visitor.

## What It Solves
- Express a code transformation as a pattern and a replacement rather than as tree-walking code.
- Run structural analysis inside a browser-based editor, where no compiler toolchain is available.
- Keep the matching language small enough that transformations are readable as rules.

## Architecture & Mechanics
- `lib/treehugger/` is 11 files; `lib/acorn/` is 3 — the Acorn parser is vendored in, so the library ships with its front end rather than depending on one.
- The design lineage is term rewriting (the Stratego tradition): patterns match tree shapes and bind parts of them, and traversal strategies are composed rather than hand-written.
- `test.html` at the repository root, and `http://ajaxorg.github.com/treehugger/test.html` as its stated homepage, mean the test suite is a web page — this predates headless browser test runners as normal practice.
- **Not read:** any JavaScript source. The rewriting design is attributed from the project's stated purpose and its provenance in Cloud9, not confirmed in code.

## What Is Inside
- **The whole library in 11 files** — `lib/treehugger/`, including `lib/treehugger/js/parse_test.js`.
- **A vendored Acorn** — `lib/acorn/` (3 files): the parser is inside the repository rather than declared as a dependency.
- **`lib/demo.js`** and **`test.html`** — the only runnable examples, and the test suite, both browser-oriented.
- **Not here:** any language but JavaScript, and any recent packaging. `package.json` is present; the surrounding conventions are from 2011.

## Transferable Capability
**Describe a transformation as a rule — this shape becomes that shape — rather than as a procedure that walks and mutates.** A rule is inspectable, composable and reversible in a way a visitor method is not; a reader can see what a rewrite does without simulating it. The related idea is **composable traversal strategies**: separate *what to change* from *where to look for it*, so the same rule can be applied once, everywhere, or bottom-up without being rewritten each time. Both come from term rewriting and both survive translation to any tree-shaped data.

**Alternative to:** a visitor with a method per node type, which is more flexible and much harder to read as a specification; and to textual patching. **Applies wherever** structured data is transformed by rules a person should be able to review — configuration migration, document conversion, schema evolution.

## Taxonomy
- Ecosystem: Web_Frontend
- Domain Primary: Code_Intelligence
- Maturity Stage: Abandoned
- License Class: Permissive
- Deployment Target: Browser
- Interface Protocol: CLI
- Data Locality: Local_First
- Hardware Footprint: Browser_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Read it for the rewriting vocabulary before building an imperative transformer over any tree.
- Study `lib/demo.js` as a compact statement of what rule-based tree editing looks like in JavaScript.
- Contrast the vendored-parser choice with the layered approach in [[cst - cst]], which depends on its parser instead.

## Reading Notes
**Archived by its owner and last pushed 2020-02-13.** GitHub reports it as archived, so the repository is read-only upstream — this is a settled artefact, not a stalled one, and it is classified `Abandoned` on that basis rather than as a judgement of quality. 483 stars for 17 files is a comment on the idea's reach. Its origin is the Cloud9 IDE, which explains both the browser orientation and the fact that its test suite is an HTML page.

## Semantic Links
- [parent_topic:: [[Topic - Code Intelligence & Structural Parsing]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[cst - cst]]]
- [related_to:: [[semgrep - semgrep]]]
- [related_to:: [[Instagram - LibCST]]]
- [implements_pattern:: [[Pattern - Structural Code Search]]]
- [implements_pattern:: [[Pattern - Lossless Syntax Tree]]]
- [mentions_term:: [[Glossary - Abstract Syntax Tree]]]
- [mentions_term:: [[Glossary - Structural Search]]]
- [mentions_term:: [[Glossary - Codemod]]]

## Evidence
- Source URL: https://github.com/ajaxorg/treehugger
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; no JavaScript source was opened

## GitHub Snapshot

- Description: JavaScript AST (Abstract Syntax Tree) transformation tools
- Language: JavaScript
- License (SPDX): MIT
- Default Branch: master
- Stars: 483
- Homepage: http://ajaxorg.github.com/treehugger/test.html
- Pushed At: 2020-02-13T00:15:13Z

## Evidence Anchors
- [github_repo] description :: JavaScript AST (Abstract Syntax Tree) transformation tools (confidence 0.95)
- [github_repo] language :: JavaScript (confidence 0.90)
- [github_repo] license :: MIT (confidence 0.90)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 25 paths at HEAD (confidence 0.95)
