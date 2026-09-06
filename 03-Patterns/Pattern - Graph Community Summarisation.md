---
pattern_key: "graph_community_summarisation"
aliases: ["community reports"]
type: "pattern"
status: "active"
examples: ["microsoft - graphrag"]
glossary_terms: ["Community Detection", "Knowledge Graph", "Retrieval-Augmented Generation"]
topic_keys: ["knowledge_management"]
---

# Pattern - Graph Community Summarisation

## Definition
Detect communities in a graph, then write and store a natural-language summary of each community at each level of the hierarchy, so that questions about the whole corpus are answered from precomputed summaries instead of from retrieved fragments.

## Why It Matters
- It answers the question retrieval cannot: “what are the themes here” has no single passage containing the answer, so chunk retrieval always fails at it.
- The hierarchy is the useful part — the same corpus is summarised at several granularities, and the query picks the level.
- The cost is real and paid up front, at indexing time, per corpus. A summary is also a derived artefact that goes stale when the graph beneath it changes.

## Example Repositories
- [[microsoft - graphrag]]

## Related Glossary
- [[Glossary - Community Detection]]
- [[Glossary - Knowledge Graph]]
- [[Glossary - Retrieval-Augmented Generation]]

## Related Topics
- [[Topic - Knowledge Management]]
