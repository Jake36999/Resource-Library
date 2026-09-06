---
pattern_key: "program_graph_construction"
aliases: ["control flow graph construction", "code property graph"]
type: "pattern"
status: "active"
examples: ["bstee615 - tree-climber", "semgrep - semgrep", "javaparser - javaparser"]
glossary_terms: ["Control Flow Graph", "Abstract Syntax Tree", "Static Analysis", "Taint Analysis"]
topic_keys: ["code_intelligence"]
---

# Pattern - Program Graph Construction

## Definition
Derive graphs that syntax does not contain — control flow, data flow, call relationships — from a syntax tree, so questions about ordering and dependency can be asked of a structure that actually encodes them.

## Why It Matters
- Syntax records what was written. *Can this run before that*, and *does this value reach there*, are answered by different graphs, and asking the wrong one produces a confidently wrong answer.
- Building on a parser that does not need a compiling project — as [[bstee615 - tree-climber]] does on tree-sitter — makes the analysis available on broken, partial or unbuildable code, which is most code under examination.
- The derivation inherits the parser's grammar quality, so an error in the underlying grammar surfaces as a wrong edge rather than as a parse failure.

## Example Repositories
- [[bstee615 - tree-climber]]
- [[semgrep - semgrep]]
- [[javaparser - javaparser]]

## Related Glossary
- [[Glossary - Control Flow Graph]]
- [[Glossary - Abstract Syntax Tree]]
- [[Glossary - Static Analysis]]
- [[Glossary - Taint Analysis]]

## Related Topics
- [[Topic - Code Intelligence & Structural Parsing]]
- [[Topic - Security & SIEM]]
