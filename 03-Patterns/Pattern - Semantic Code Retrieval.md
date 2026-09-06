---
pattern_key: "semantic_code_retrieval"
aliases: ["natural language code search"]
type: "pattern"
status: "active"
examples: ["sturdy-dev - semantic-code-search", "fynnfluegge - codeqai", "jgravelle - jcodemunch-mcp"]
glossary_terms: ["Semantic Search", "Embedding", "Abstract Syntax Tree"]
topic_keys: ["code_intelligence"]
---

# Pattern - Semantic Code Retrieval

## Definition
Find code by describing what it does rather than naming it, by embedding units of code into the same space as the language used to describe them — where the unit is chosen at a syntactic boundary rather than by character count.

## Why It Matters
- The boundary decision dominates the outcome. A fragment starting mid-function reads as complete and is not; splitting at definitions removes the chunk-size parameter entirely, and in [[fynnfluegge - codeqai]] that splitting layer is over half the codebase.
- Getting code and prose into one space needs either a model trained for it or a proxy task that forces the alignment — [[hamelsmu - code_search]] trains a summariser and keeps the encoder.
- Retrieval unit and answer unit are the same choice: [[jgravelle - jcodemunch-mcp]] returns symbols precisely because the consumer is an agent with a fixed attention budget.

## Example Repositories
- [[sturdy-dev - semantic-code-search]]
- [[fynnfluegge - codeqai]]
- [[jgravelle - jcodemunch-mcp]]

## Related Glossary
- [[Glossary - Semantic Search]]
- [[Glossary - Embedding]]
- [[Glossary - Abstract Syntax Tree]]

## Related Topics
- [[Topic - Code Intelligence & Structural Parsing]]
- [[Topic - Knowledge Management]]
