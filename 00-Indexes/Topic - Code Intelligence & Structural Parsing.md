---
topic_key: "code_intelligence"
type: "topic_index"
status: "active"
canonical_vocabulary: ["parser", "abstract syntax tree", "concrete syntax tree", "incremental parsing", "structural search", "metavariable", "codemod", "static analysis", "grammar"]
inclusion_criteria: "Parsers and parser generators, syntax-tree specifications, structural code query engines, semantic code search, codemod frameworks, and the program analysis built directly on top of them."
patterns: ["structural_code_search", "lossless_syntax_tree"]
glossary_terms: ["Abstract Syntax Tree", "Concrete Syntax Tree", "Incremental Parsing", "Structural Search", "Metavariable", "Static Analysis", "Taint Analysis", "Codemod"]
resource_count: 16
review_count: 0
created: "2026-09-03"
---

# Topic - Code Intelligence & Structural Parsing

## Inclusion Criteria
Parsers and parser generators, syntax-tree specifications, structural code query engines, semantic code search, codemod frameworks, and the program analysis built directly on top of them.

## Canonical Vocabulary
- parser
- abstract syntax tree
- concrete syntax tree
- incremental parsing
- structural search
- metavariable
- codemod
- static analysis
- grammar

## Why This Topic Exists
Tools that reason about code all begin at the same place: turning text into a tree. The choices made at that step — whether formatting survives, whether a half-written file still parses, whether the tree can be queried — determine what every layer above it can do. This topic holds that machinery, separately from the linters and scanners that consume it.

## Mechanics
- Turns source text into a tree, either by a generated table-driven parser or a hand-written one, and defines what that tree keeps and discards.
- Offers a way to ask questions of the tree — an S-expression query, a pattern in the target language, or a declarative matcher over node types.
- Draws a deliberate line at semantics: types, name binding and cross-file reachability are layers above, and where a source crosses that line it is usually the commercial half of the product.

## Typical Use Cases
- Find every occurrence of a construct across a codebase, regardless of formatting.
- Rewrite code mechanically and produce a diff small enough to review.
- Build editor tooling, code navigation or highlighting over a language with no existing support.

## Approved Resources
- [[tree-sitter - tree-sitter]]
- [[semgrep - semgrep]]
- [[Instagram - LibCST]]
- [[syntax-tree - mdast]]
- [[ajaxorg - treehugger]]
- [[bstee615 - tree-climber]]
- [[cst - cst]]
- [[fynnfluegge - codeqai]]
- [[hamelsmu - code_search]]
- [[javaparser - javaparser]]
- [[jgravelle - jcodemunch-mcp]]
- [[nene - sql-parser-cst]]
- [[s-expressionists - Concrete-Syntax-Tree]]
- [[semgrep - mcp]]
- [[sturdy-dev - semantic-code-search]]
- [[whitequark - ast]]

## Review Queue
- None yet.

## Related Patterns
- [[Pattern - Structural Code Search]]
- [[Pattern - Lossless Syntax Tree]]

## Related Glossary
- [[Glossary - Abstract Syntax Tree]]
- [[Glossary - Concrete Syntax Tree]]
- [[Glossary - Incremental Parsing]]
- [[Glossary - Structural Search]]
- [[Glossary - Metavariable]]
- [[Glossary - Static Analysis]]
- [[Glossary - Taint Analysis]]
- [[Glossary - Codemod]]

## Related Topics
- [[Topic - Architecture & Developer Playbooks]]
- [[Topic - Knowledge Management]]
