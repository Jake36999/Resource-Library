---
pattern_key: "vector_similarity_search"
aliases: ["nearest neighbour search", "embedding search"]
type: "pattern"
status: "active"
examples: ["lancedb - vectordb-recipes", "qdrant - examples", "DiceTechJobs - SolrConfigExamples"]
glossary_terms: ["Vector Database", "Embedding", "Semantic Search"]
topic_keys: ["knowledge_management"]
---

# Pattern - Vector Similarity Search

## Definition
Represent every item as a point in a continuous space and answer a query by finding the points nearest to it, so that similarity of meaning becomes proximity of position rather than overlap of spelling.

## Why It Matters
- It answers the question a term index cannot: *find the thing that does this*, when the asker does not know what it was called.
- The costs are the ones nobody quotes — the index must be rebuilt when the embedding model changes, and a result carries no explanation of why it matched.
- The infrastructure it seems to require is negotiable. [[DiceTechJobs - SolrConfigExamples]] obtained it from an inverted index a decade before vector databases existed, which is worth knowing before adding a second datastore.

## Example Repositories
- [[lancedb - vectordb-recipes]]
- [[qdrant - examples]]
- [[DiceTechJobs - SolrConfigExamples]]

## Related Glossary
- [[Glossary - Vector Database]]
- [[Glossary - Embedding]]
- [[Glossary - Semantic Search]]

## Related Topics
- [[Topic - Knowledge Management]]
- [[Topic - Code Intelligence & Structural Parsing]]
