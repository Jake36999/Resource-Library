---
uuid: "55d0e21f-f9b2-56b1-8725-4a3bc064bca9"
canonical_url: "https://github.com/qdrant/examples"
repo_key: "qdrant/examples"
owner: "qdrant"
repo_name: "examples"
aliases: ["qdrant/examples", "https://github.com/qdrant/examples"]
type: "tutorial"
primary_topic: "Knowledge Management"
secondary_topics: ["Agentic AI & Models"]
ecosystem: "Python"
domain_primary: "Knowledge_Management"
maturity_stage: "Active"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "REST"
data_locality: "Distributed"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Vector Similarity Search", "Hybrid Retrieval", "Knowledge Graph Routing"]
glossary_terms: ["Vector Database", "Embedding", "Semantic Search", "Reranking", "Multimodal Model"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 5
github_description: "A collection of examples and tutorials for Qdrant vector search engine"
github_language: "Jupyter Notebook"
github_license_spdx: "Apache-2.0"
github_default_branch: "master"
github_stars: 220
github_pushed_at: "2026-09-02T10:18:48Z"
---
# qdrant - examples

## Bottom Line
Qdrant's example collection, structured as courses rather than as a folder of demos — including a five-module course on multi-vector search, which is the technique most vector-search introductions skip.

## What It Solves
- Learn vector search as a sequence with a shape, not as disconnected snippets.
- Understand multi-vector retrieval, where one item carries several embeddings rather than one.
- See retrieval over documents-as-images, where the page is embedded rather than its extracted text.

## Architecture & Mechanics
- Three parallel course tracks with different pacing: `beginners-course/` (5 modules), `course/` (5 days), and `course-multi-vector-search/` (modules 0–3, 20 files) — the last being the substantive one.
- The `qdrant_101_*` series splits by *data type* rather than by feature: `qdrant_101_text_data`, `qdrant_101_image_data` (21 files), `qdrant_101_audio_data`, `qdrant_101_getting_started`. The lesson is that modality changes the problem.
- One example is a complete production-shaped application rather than a notebook: `ecommerce-search-golang/` (51 files, Go backend with a TypeScript frontend, three Dockerfiles and a compose file).
- **Not read:** any notebook or Go source. The above is read off directory names and file counts.

## What Is Inside
- **A multi-vector search course** — `course-multi-vector-search/`, modules 0 to 3: the case where one item has several embeddings, which most introductions omit and which changes how ranking works.
- **ColPali and ColQwen2 material** — `colpali-and-binary-quantization/colpali_demo_binary.ipynb` and `pdf-retrieval-at-scale/ColPali_ColQwen2_Tutorial.ipynb`: retrieving PDFs by embedding page images rather than extracted text, with binary quantisation for cost.
- **A GraphRAG-with-Neo4j example** — `graphrag_neo4j/`: a vector store and a graph store used together, from the vector side.
- **A production-shaped Go application** — `ecommerce-search-golang/` with a 40-file frontend, two Dockerfiles and a compose file. The only non-notebook, non-Python full application here.
- **Real corpora** — `sci-fi-books/top_100_scifi_books_full.csv`, `self-query/winemag-data-130k-v2.csv` (130,000 wine reviews), `time-based-sharding/social-media-posts.csv`.
- **Sharding by time** — `time-based-sharding/`: a data-layout concern rather than a retrieval one, and rarer in example collections.
- **Not here:** the database. Every example assumes a Qdrant instance.

## Transferable Capability
**Teach retrieval by modality and by cardinality, not by API surface.** Two structural choices carry over. Splitting by data type — text, image, audio — makes visible that the embedding problem changes shape with the input, which a feature-organised tutorial hides. And treating **multiple vectors per item** as its own subject names a design decision most systems make by default: whether an item is one point or several changes what a nearest-neighbour result even means. The ColPali material generalises further: **embed the artefact as it appears rather than a text extraction of it**, which sidesteps extraction error entirely for anything visually structured.

**Alternative to:** one-embedding-per-document, which is simpler and loses within-document distinctions; and to text-extraction pipelines for visual documents, where the extractor becomes the accuracy ceiling. **Applies wherever** the thing being searched has internal structure or is not natively text — documents with layout, records with several facets, media.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Knowledge_Management
- Maturity Stage: Active
- License Class: Permissive
- Deployment Target: Server
- Interface Protocol: REST
- Data Locality: Distributed
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Work through `course-multi-vector-search/` before deciding an item gets one vector.
- Read the ColPali notebooks when a PDF corpus is losing information in text extraction.
- Take `ecommerce-search-golang/` as a worked example of vector search inside a conventional service rather than a notebook.

## Reading Notes
Vendor-published, so Qdrant is assumed throughout; the *techniques* — multi-vector, ColPali page embedding, time-based sharding — are portable, the client code is not. Actively maintained (last pushed 2026-09-02). The `wine reviews` and `sci-fi books` CSVs are usable as general-purpose retrieval test corpora regardless of what store you use.

## Semantic Links
- [parent_topic:: [[Topic - Knowledge Management]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[lancedb - vectordb-recipes]]]
- [related_to:: [[elastic - elastic-labs]]]
- [related_to:: [[microsoft - graphrag]]]
- [implements_pattern:: [[Pattern - Vector Similarity Search]]]
- [implements_pattern:: [[Pattern - Hybrid Retrieval]]]
- [implements_pattern:: [[Pattern - Knowledge Graph Routing]]]
- [mentions_term:: [[Glossary - Vector Database]]]
- [mentions_term:: [[Glossary - Embedding]]]
- [mentions_term:: [[Glossary - Semantic Search]]]
- [mentions_term:: [[Glossary - Reranking]]]
- [mentions_term:: [[Glossary - Multimodal Model]]]

## Evidence
- Source URL: https://github.com/qdrant/examples
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; no notebook, Go source or dataset was opened

## GitHub Snapshot

- Description: A collection of examples and tutorials for Qdrant vector search engine
- Language: Jupyter Notebook
- License (SPDX): Apache-2.0
- Default Branch: master
- Stars: 220
- Pushed At: 2026-09-02T10:18:48Z

## Evidence Anchors
- [github_repo] description :: A collection of examples and tutorials for Qdrant vector search engine (confidence 0.95)
- [github_repo] language :: Jupyter Notebook (confidence 0.90)
- [github_repo] license :: Apache-2.0 (confidence 0.90)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 177 paths at HEAD (confidence 0.95)
