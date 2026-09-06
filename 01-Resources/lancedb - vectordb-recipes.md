---
uuid: "22743ccd-330a-5893-82c8-c864e03d0cda"
canonical_url: "https://github.com/lancedb/vectordb-recipes"
repo_key: "lancedb/vectordb-recipes"
owner: "lancedb"
repo_name: "vectordb-recipes"
aliases: ["lancedb/vectordb-recipes", "https://github.com/lancedb/vectordb-recipes"]
type: "tutorial"
primary_topic: "Knowledge Management"
secondary_topics: ["Agentic AI & Models", "ML Training & MLOps"]
ecosystem: "Python"
domain_primary: "Knowledge_Management"
maturity_stage: "Active"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Python_SDK"
data_locality: "Local_First"
hardware_footprint: "Low_VRAM"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Vector Similarity Search", "Hybrid Retrieval", "Model Inference Pipeline"]
glossary_terms: ["Vector Database", "Embedding", "Retrieval-Augmented Generation", "Chunking", "Reranking", "Multimodal Model"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: "Resource, examples & tutorials for multimodal AI, RAG and agents using vector search and LLMs"
github_language: "Jupyter Notebook"
github_license_spdx: "Apache-2.0"
github_default_branch: "main"
github_stars: 973
github_topics: ["agents", "ai", "deep-learning", "embeddings", "fine-tuning", "gpt", "gpt-4-vision", "lancedb", "langchain", "llama-index", "llms", "machine-learning", "multimodal", "multimodal-ai", "openai", "rag", "vector-database"]
github_pushed_at: "2026-04-24T11:29:16Z"
---
# lancedb - vectordb-recipes

## Bottom Line
Several hundred runnable recipes for vector search — 101 notebooks and 314 example directories covering retrieval variants, multimodal search, agents and evaluation — organised so a specific technique can be found and copied rather than read about.

## What It Solves
- See a retrieval variant working end to end before deciding whether it is worth building.
- Compare chunking strategies, rerankers and RAG architectures against each other rather than one at a time.
- Search across modalities — image, audio, video, text — using the same store.

## Architecture & Mechanics
- Three tiers with different purposes: `tutorials/` (50 files) teaches one technique at a time, `examples/` (314) shows an integration, and `applications/` (256) is a working app. A reader chooses depth rather than wading through one flat directory.
- Techniques are named at the directory level, which is what makes the collection navigable: `different-types-text-chunking-in-RAG`, `cohere-reranker`, `Multi-Head-RAG-from-Scratch`, `Local-RAG-from-Scratch`, `Corrective-RAG-with_Langgraph`, `Agentic_RAG`, `RAG-with_MatryoshkaEmbed-Llamaindex`.
- Superseded material is *kept and marked* rather than deleted: `examples/archived_examples/` (37) and `applications/archived_applications/` (64). The history of what was tried stays visible.
- Examples are tested in CI (`.github/workflows/examples-test.yml`, `compile_testing.js`), which is what stops a collection this size rotting silently.
- **Not read:** any notebook or example. The organisation above is read off directory names and counts.

## What Is Inside
- **A chunking comparison** — `tutorials/different-types-text-chunking-in-RAG`: the parameter most retrieval systems pick arbitrarily, examined directly.
- **Multiple RAG architectures side by side** — `Agentic_RAG`, `Multi-Head-RAG-from-Scratch`, `Local-RAG-from-Scratch`, `Corrective-RAG-with_Langgraph`, `Multilingual_RAG`, `multi-document-agentic-rag`, `cognee-RAG`.
- **An evaluation application** — `applications/evaluate_RAG/`, six files: measuring retrieval rather than demonstrating it.
- **Multimodal retrieval** — `examples/multimodal_video_search`, `applications/multimodal-search` (19 files), `ecommerce_reverse_image_search`, plus audio work in `Chatbot_with_Parler_TTS`.
- **A JavaScript/Node track** — `applications/node/` (141 files), which is a substantial body of non-Python material that the repository's Python-centric framing hides.
- **101 notebooks and 63 images**, 296 MB in total; `examples/archived_examples/` and `applications/archived_applications/` preserve 101 superseded examples.
- **Not here:** the database. This is the recipe book; LanceDB is the dependency.

## Transferable Capability
**Publish the variations, not just the recommended path, and test them so the collection cannot rot.** A recipe collection is a decision aid: its value is that a reader can compare *chunking strategy A against B* or *reranker on against off* without building either. Three organising choices make that work at this scale — naming the technique in the directory so the collection is searchable by intent, tiering by depth so a reader picks a level rather than a file, and running the examples in CI so the promise that they work is checked rather than asserted. Archiving instead of deleting is the fourth: what was tried and abandoned is evidence too.

**Alternative to:** a documentation site, which explains and cannot be run; a single quickstart, which shows one path; and to a blog series, which cannot be tested and drifts. **Applies wherever** a design decision has several defensible answers and the honest response is to show them working.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Knowledge_Management
- Maturity Stage: Active
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Python_SDK
- Data Locality: Local_First
- Hardware Footprint: Low_VRAM
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Go to `tutorials/different-types-text-chunking-in-RAG` before choosing a chunk size for anything.
- Lift `applications/evaluate_RAG` as a starting point for measuring a retrieval system rather than describing it.
- Copy the tiered, technique-named directory scheme for any example collection expected to exceed about fifty entries.

## Reading Notes
Vendor-published, so the framing consistently favours LanceDB; the *techniques* are portable but the storage decision is pre-made throughout. Note also that a third of the collection is archived — 101 of roughly 570 examples — which is a mark of honesty rather than neglect, but does mean the top-level count overstates what is current. The Node track (141 files) is easy to miss entirely and is the second-largest body of code in the repository.

## Semantic Links
- [parent_topic:: [[Topic - Knowledge Management]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[qdrant - examples]]]
- [related_to:: [[elastic - elastic-labs]]]
- [related_to:: [[run-llama - llama_index]]]
- [related_to:: [[roomi-fields - rtfm]]]
- [implements_pattern:: [[Pattern - Vector Similarity Search]]]
- [implements_pattern:: [[Pattern - Hybrid Retrieval]]]
- [implements_pattern:: [[Pattern - Model Inference Pipeline]]]
- [mentions_term:: [[Glossary - Vector Database]]]
- [mentions_term:: [[Glossary - Embedding]]]
- [mentions_term:: [[Glossary - Retrieval-Augmented Generation]]]
- [mentions_term:: [[Glossary - Chunking]]]
- [mentions_term:: [[Glossary - Reranking]]]
- [mentions_term:: [[Glossary - Multimodal Model]]]

## Evidence
- Source URL: https://github.com/lancedb/vectordb-recipes
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; no notebook, example or application was opened

## GitHub Snapshot

- Description: Resource, examples & tutorials for multimodal AI, RAG and agents using vector search and LLMs
- Language: Jupyter Notebook
- License (SPDX): Apache-2.0
- Default Branch: main
- Stars: 973
- Pushed At: 2026-04-24T11:29:16Z
- Topics: agents, ai, deep-learning, embeddings, fine-tuning, gpt, gpt-4-vision, lancedb, langchain, llama-index, llms, machine-learning, multimodal, multimodal-ai, openai, rag, vector-database

## Evidence Anchors
- [github_repo] description :: Resource, examples & tutorials for multimodal AI, RAG and agents using vector search and LLMs (confidence 0.95)
- [github_repo] language :: Jupyter Notebook (confidence 0.90)
- [github_repo] license :: Apache-2.0 (confidence 0.90)
- [github_repo] topics :: agents, ai, deep-learning, embeddings, fine-tuning, gpt, gpt-4-vision, lancedb, langchain, llama-index, llms, machine-learning, multimodal, multimodal-ai, openai, rag, vector-database (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 686 paths at HEAD (confidence 0.95)
