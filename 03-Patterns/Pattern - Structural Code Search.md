---
pattern_key: "structural_code_search"
aliases: ["semantic grep"]
type: "pattern"
status: "active"
examples: ["semgrep - semgrep", "tree-sitter - tree-sitter", "Instagram - LibCST"]
glossary_terms: ["Structural Search", "Abstract Syntax Tree", "Metavariable", "Static Analysis"]
topic_keys: ["code_intelligence"]
---

# Pattern - Structural Code Search

## Definition
Query source code against its parsed tree rather than its characters, using a pattern written in the shape of the thing being looked for, with placeholders that match any subtree and bind what they matched.

## Why It Matters
- Formatting, naming and intervening code stop being obstacles: one pattern finds every instance of a construct however it was written.
- The pattern is reviewable by anyone who can read the language, which a regular expression over the same construct is not.
- It sets a hard boundary that is easy to forget: matching is structural, so anything requiring meaning — types, name resolution, reachability across files — has to be built as a separate layer above it.

## Example Repositories
- [[semgrep - semgrep]]
- [[tree-sitter - tree-sitter]]
- [[Instagram - LibCST]]

## Related Glossary
- [[Glossary - Structural Search]]
- [[Glossary - Abstract Syntax Tree]]
- [[Glossary - Metavariable]]
- [[Glossary - Static Analysis]]

## Related Topics
- [[Topic - Code Intelligence & Structural Parsing]]
