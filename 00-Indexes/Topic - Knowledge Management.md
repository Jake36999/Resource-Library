---
topic_key: "knowledge_management"
type: "topic_index"
status: "active"
canonical_vocabulary: ["retrieval", "RAG", "knowledge graph", "semantic layer", "community detection", "index", "embedding", "query routing", "MCP"]
inclusion_criteria: "Retrieval frameworks, graph-based reasoning over documents, semantic layers and catalogues built for agents, note and knowledge-base systems, and the indexing and routing machinery underneath them."
patterns: ["graph_community_summarisation", "multi_tier_index_routing", "metadata_harvesting", "knowledge_graph_routing"]
glossary_terms: ["Retrieval-Augmented Generation", "Community Detection", "Knowledge Graph", "Semantic Layer", "Model Context Protocol", "Metadata Catalog"]
resource_count: 20
review_count: 0
created: "2026-09-03"
---

# Topic - Knowledge Management

## Inclusion Criteria
Retrieval frameworks, graph-based reasoning over documents, semantic layers and catalogues built for agents, note and knowledge-base systems, and the indexing and routing machinery underneath them.

## Canonical Vocabulary
- retrieval
- RAG
- knowledge graph
- semantic layer
- community detection
- index
- embedding
- query routing
- MCP

## Why This Topic Exists
This catalogue is itself an instance of this domain, which is the reason to hold it: a system that cannot reason about its own architecture is missing the material it most needs. The sources here have solved retrieval, graph construction and agent-facing query surfaces in ways worth comparing against the design in [[Design Specification]].

## Mechanics
- Builds one or more indexes over a corpus — vector, lexical, summary, graph — and chooses between them at query time.
- Extracts structure from unstructured text, either with a language model or with cheaper linguistic methods, and clusters the result.
- Exposes the result to a person or an agent through a typed query surface, increasingly over the Model Context Protocol.

## Typical Use Cases
- Answer corpus-level questions that chunk retrieval cannot reach.
- Give an agent enough context about a data landscape to route a query correctly.
- Compare retrieval designs before committing to one.

## Approved Resources
- [[microsoft - graphrag]]
- [[run-llama - llama_index]]
- [[neo4j-labs - neocarta]]
- [[ganarajpr - awesome-dspy]]
- [[Azure-Samples - academic-knowledge-analytics-visualization]]
- [[Azure-Samples - graphrag-accelerator]]
- [[DiceTechJobs - SolrConfigExamples]]
- [[diicellman - dspy-rag-fastapi]]
- [[elastic - elastic-labs]]
- [[hannesfrank - Course-Knowledge-Graphs]]
- [[JayLZhou - GraphRAG]]
- [[lancedb - vectordb-recipes]]
- [[MazzaWill - neo4j-python-pandas-py2neo-v3]]
- [[mdebellis - SemanticKG-Design]]
- [[qdrant - examples]]
- [[reichenbch - RAG-examples]]
- [[roomi-fields - rtfm]]
- [[run-llama - LlamaIndexTS]]
- [[SachaCR - library-examples]]
- [[thinktecture-labs - semantic-kernel-semanticsearch]]

## Review Queue
- None yet.

## Related Patterns
- [[Pattern - Graph Community Summarisation]]
- [[Pattern - Multi-Tier Index Routing]]
- [[Pattern - Metadata Harvesting]]
- [[Pattern - Knowledge Graph Routing]]

## Related Glossary
- [[Glossary - Retrieval-Augmented Generation]]
- [[Glossary - Community Detection]]
- [[Glossary - Knowledge Graph]]
- [[Glossary - Semantic Layer]]
- [[Glossary - Model Context Protocol]]
- [[Glossary - Metadata Catalog]]

## Related Topics
- [[Topic - Agentic AI & Models]]
- [[Topic - Data APIs & Big Data]]
- [[Topic - Code Intelligence & Structural Parsing]]
