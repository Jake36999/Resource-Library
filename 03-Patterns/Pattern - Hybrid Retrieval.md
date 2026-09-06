---
pattern_key: "hybrid_retrieval"
aliases: ["fusion retrieval", "multi-strategy search"]
type: "pattern"
status: "active"
examples: ["roomi-fields - rtfm", "elastic - elastic-labs", "JayLZhou - GraphRAG"]
glossary_terms: ["Semantic Search", "Vector Database", "Reranking"]
topic_keys: ["knowledge_management"]
---

# Pattern - Hybrid Retrieval

## Definition
Run several retrieval strategies over the same corpus and combine their rankings, on the grounds that lexical, semantic and structural matching fail in different places and their union is more robust than any one of them tuned harder.

## Why It Matters
- Lexical search misses a synonym; semantic search misses an exact identifier or a rare token; a graph misses anything unconnected. The failures are not correlated, which is precisely why combining them works.
- The combination step is a real design decision. Reciprocal rank fusion needs no score calibration between rankings; weighted score blending needs the scores to mean the same thing, and they usually do not.
- It is the honest response to discovering that improving one ranker has stopped paying. This catalogue reached it the same way, and the largest single gain came from fixing a defect in the lexical half rather than from adding a fourth strategy.

## Example Repositories
- [[roomi-fields - rtfm]]
- [[elastic - elastic-labs]]
- [[JayLZhou - GraphRAG]]

## Related Glossary
- [[Glossary - Semantic Search]]
- [[Glossary - Vector Database]]
- [[Glossary - Reranking]]

## Related Topics
- [[Topic - Knowledge Management]]
- [[Topic - Code Intelligence & Structural Parsing]]
