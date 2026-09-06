---
pattern_key: "lossless_syntax_tree"
aliases: ["concrete syntax preservation"]
type: "pattern"
status: "active"
examples: ["Instagram - LibCST", "tree-sitter - tree-sitter", "syntax-tree - mdast"]
glossary_terms: ["Concrete Syntax Tree", "Abstract Syntax Tree", "Codemod"]
topic_keys: ["code_intelligence"]
---

# Pattern - Lossless Syntax Tree

## Definition
Parse a document into a tree that retains every byte of the original — whitespace, comments, punctuation — so that modifying one node and printing the tree back out changes only what was modified.

## Why It Matters
- It is the difference between a refactoring tool that produces a reviewable diff and one that reformats every file it touches.
- The design tension is that a faithful tree is unpleasant to navigate. The usable resolutions attach trivia to the node it belongs to rather than making it a sibling.
- It applies well beyond code: any format with a round-trip requirement — Markdown, configuration, structured documents — has the same problem.

## Example Repositories
- [[Instagram - LibCST]]
- [[tree-sitter - tree-sitter]]
- [[syntax-tree - mdast]]

## Related Glossary
- [[Glossary - Concrete Syntax Tree]]
- [[Glossary - Abstract Syntax Tree]]
- [[Glossary - Codemod]]

## Related Topics
- [[Topic - Code Intelligence & Structural Parsing]]
