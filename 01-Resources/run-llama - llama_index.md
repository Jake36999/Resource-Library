---
uuid: "ef99ceaa-ea01-5c38-8f1e-204ef004c8dd"
canonical_url: "https://github.com/run-llama/llama_index"
repo_key: "run-llama/llama_index"
owner: "run-llama"
repo_name: "llama_index"
aliases: ["run-llama/llama_index", "https://github.com/run-llama/llama_index"]
type: "ai_framework"
primary_topic: "Knowledge Management"
secondary_topics: ["Agentic AI & Models", "Data APIs & Big Data"]
ecosystem: "Python"
domain_primary: "Knowledge_Management"
maturity_stage: "Production_Ready"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Python_SDK"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "Callable"
patterns: ["Multi-Tier Index Routing"]
glossary_terms: ["Retrieval-Augmented Generation", "Knowledge Graph", "LLM", "Agent"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-03"
evidence_count: 5
github_description: "LlamaIndex is the leading document agent and OCR platform"
github_language: "Python"
github_license_spdx: "MIT"
github_default_branch: "main"
github_stars: 52000
github_topics: ["agents", "application", "data", "fine-tuning", "framework", "llamaindex", "llm", "multi-agents", "rag", "vector-database"]
github_homepage: "https://developers.llamaindex.ai"
github_pushed_at: "2026-09-03T03:05:30Z"
---
# run-llama - llama_index

## Bottom Line
Offers structurally different indexes over the same corpus — vector, keyword, summary, tree, document-summary, knowledge graph, property graph, structured — and a router that picks between them, on top of roughly 300 integration packages that have already adapted everything to one set of interfaces.

## What It Solves
- Stop rewriting the same twenty retrieval components for every application.
- Match the index structure to the question shape instead of forcing everything through vector similarity.
- Swap the vector store, the model or the loader without rewriting the application around it.

## Architecture & Mechanics
- `core/indices/` is the largest core subpackage (91 files) and holds genuinely different index types — `vector_store`, `keyword_table`, `list`, `tree`, `document_summary`, `knowledge_graph`, `property_graph`, `struct_store` — plus `composability` for indexes over indexes.
- `selectors`, `objects` and the router choose which index answers a given query; that decision is an explicit component rather than a scoring detail.
- Around it: `node_parser` (26 files), `response_synthesizers` (13, with refine, compact and tree-summarize strategies), `postprocessor` (11, reranking and filtering), `evaluation` (25), `memory`, `agent`, and an event-driven `workflow` layer.
- `llama-index-integrations/` is the bulk: roughly 9,000 files across 300+ packages — 1,941 reader files, 1,144 LLM adapters, 958 vector stores, 839 tools, 683 embeddings.

## What Is Inside
- **A core framework** — `llama-index-core/llama_index/core/`, largest subpackages by file
  count: `indices/` (93), `query_engine/` (26), `node_parser/` (25), `evaluation/` (25),
  `instrumentation/` (25), `storage/` (22), `agent/` (17), `tools/` (15), `workflow/` (14),
  `response_synthesizers/` (13), `postprocessor/` (11), `memory/` (11).
- **The index taxonomy** — `core/indices/`: `vector_store`, `keyword_table`, `list`, `tree`,
  `document_summary`, `knowledge_graph`, `property_graph`, `struct_store`, `multi_modal`,
  `composability` (indexes over indexes), plus `core/selectors/` and the router.
- **~9,000 files of integrations** — `llama-index-integrations/` across 300+ packages: readers
  (1,941 files), LLM adapters (1,144), vector stores (958), tools (839), embeddings (683),
  storage (525), postprocessors (260), retrievers (143), graph stores (90), graph_rag (15).
- **Separate instrumentation and dev tooling** — `llama-index-instrumentation/`, `llama-dev/`.

## Transferable Capability
**Keep several structurally different ways of finding things over the same material, and choose between them per question.** Questions have shapes: some are about a specific token, some about the gist of a thing, some about what connects two things, some about aggregate values. One organising structure answers one shape well and the rest badly, and averaging them is worse than choosing. Making the choice an explicit component means it can be inspected and corrected.

**Alternative to:** a single index tuned until it is mediocre at everything; and to routing hidden inside a scoring function where nobody can see which strategy answered. **Applies wherever** the questions asked of a collection are not all of the same kind — which is to say, wherever real users arrive.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Knowledge_Management
- Maturity Stage: Production_Ready
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Python_SDK
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: Callable

## Integration & Use Cases
- Assemble a retrieval application without writing loaders and adapters.
- Study the index taxonomy as a menu of retrieval structures, independent of the framework.
- Use a single integration package — one reader, one vector store — without adopting the whole.

## Reading Notes
**The GitHub description is about a different product.** It reads "LlamaIndex is the leading document agent and OCR platform", which describes LlamaParse, the company's commercial platform; the README distinguishes them carefully. This repository is the open-source retrieval framework. Classifying it from metadata alone would file it as OCR.

## Semantic Links
- [parent_topic:: [[Topic - Knowledge Management]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[microsoft - graphrag]]]
- [related_to:: [[neo4j-labs - neocarta]]]
- [related_to:: [[ganarajpr - awesome-dspy]]]
- [implements_pattern:: [[Pattern - Multi-Tier Index Routing]]]
- [mentions_term:: [[Glossary - Retrieval-Augmented Generation]]]
- [mentions_term:: [[Glossary - Knowledge Graph]]]
- [mentions_term:: [[Glossary - LLM]]]
- [mentions_term:: [[Glossary - Agent]]]

## Evidence
- Source URL: https://github.com/run-llama/llama_index
- Source kind: GitHub REST metadata plus the repository tree and files, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-03
- Depth of read: recorded per source in [[Scouting Working File 2026-09-03]]

## GitHub Snapshot

- Description: LlamaIndex is the leading document agent and OCR platform
- Language: Python
- License (SPDX): MIT
- Default Branch: main
- Stars: 52000
- Homepage: https://developers.llamaindex.ai
- Pushed At: 2026-09-03T03:05:30Z
- Topics: agents, application, data, fine-tuning, framework, llamaindex, llm, multi-agents, rag, vector-database

## Evidence Anchors
- [github_repo] description :: LlamaIndex is the leading document agent and OCR platform (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: MIT (confidence 0.90)
- [github_repo] topics :: agents, application, data, fine-tuning, framework, llamaindex, llm, multi-agents, rag, vector-database (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-03 (confidence 0.95)
