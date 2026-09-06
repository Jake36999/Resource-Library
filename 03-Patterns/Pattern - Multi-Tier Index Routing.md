---
pattern_key: "multi_tier_index_routing"
aliases: ["index selection"]
type: "pattern"
status: "active"
examples: ["run-llama - llama_index"]
glossary_terms: ["Retrieval-Augmented Generation", "Knowledge Graph", "Semantic Layer"]
topic_keys: ["knowledge_management"]
---

# Pattern - Multi-Tier Index Routing

## Definition
Maintain several structurally different indexes over the same corpus — vector, keyword, summary, tree, graph, structured — and route each query to the index whose structure suits the shape of the question.

## Why It Matters
- Different questions have different shapes. “Where is X mentioned” is lexical, “what is this about” is a summary, “what connects A and B” is a graph walk; one index answers one of them well.
- It makes the routing decision explicit and inspectable rather than hiding it inside a single retriever's scoring.
- The cost is that every index must be built and kept fresh, and the router becomes a component that itself needs evaluating.

## Example Repositories
- [[run-llama - llama_index]]

## Related Glossary
- [[Glossary - Retrieval-Augmented Generation]]
- [[Glossary - Knowledge Graph]]
- [[Glossary - Semantic Layer]]

## Related Topics
- [[Topic - Knowledge Management]]
