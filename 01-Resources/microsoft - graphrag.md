---
uuid: "b767bb19-825d-570c-afe4-b6d852b0ff60"
canonical_url: "https://github.com/microsoft/graphrag"
repo_key: "microsoft/graphrag"
owner: "microsoft"
repo_name: "graphrag"
aliases: ["microsoft/graphrag", "https://github.com/microsoft/graphrag"]
type: "ai_framework"
primary_topic: "Knowledge Management"
secondary_topics: ["Agentic AI & Models"]
ecosystem: "Python"
domain_primary: "Knowledge_Management"
maturity_stage: "Active"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "CLI"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "Procedural"
patterns: ["Graph Community Summarisation"]
glossary_terms: ["Retrieval-Augmented Generation", "Community Detection", "Knowledge Graph", "LLM"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-03"
evidence_count: 5
github_description: "A modular graph-based Retrieval-Augmented Generation (RAG) system"
github_language: "Python"
github_license_spdx: "MIT"
github_default_branch: "main"
github_stars: 35819
github_topics: ["gpt", "gpt-4", "gpt4", "graphrag", "llm", "llms", "rag"]
github_homepage: "https://microsoft.github.io/graphrag/"
github_pushed_at: "2026-09-02T01:41:10Z"
---
# microsoft - graphrag

## Bottom Line
Answers the question chunk retrieval cannot — “what are the themes in this corpus” — by extracting a graph from the documents, detecting communities in it, and writing a summary of each community at each level so global questions are served from precomputed reports rather than retrieved fragments.

## What It Solves
- Sensemaking over a private corpus, where the answer is a property of the whole and appears in no single passage.
- Multi-hop questions that require connecting entities mentioned in different documents.
- Comparing graph-based retrieval against plain vector search on the same corpus, since a `basic` mode is included for exactly that.

## Architecture & Mechanics
- Indexing is a pipeline of named workflows: `load_input_documents` → `create_base_text_units` → `extract_graph` → `finalize_graph` → `create_communities` → `create_community_reports` → `generate_text_embeddings`, with a parallel `update_*` family for incremental re-indexing.
- `extract_graph` prompts a model for entities and relationships per text unit and `summarize_descriptions` merges the many descriptions of one entity; `extract_graph_nlp` and `build_noun_graph/` are the cheaper non-LLM path, using CFG, regex or syntactic noun-phrase extraction with a validator and stop-word list.
- `cluster_graph` runs hierarchical (Leiden) community detection; `summarize_communities` writes the community report per community per level; `extract_covariates` attaches claims; `prune_graph` trims.
- Four query modes: **local** (walk out from matched entities), **global** (map-reduce over community reports), **drift** (dynamic community selection plus local), **basic** (vector only).
- Now a monorepo of eight independently versioned packages — cache, chunking, common, input, llm, storage, vectors, and graphrag itself.

## What Is Inside
- **An indexing pipeline as named workflows** — `packages/graphrag/graphrag/index/workflows/`:
  `create_base_text_units`, `extract_graph`, `extract_graph_nlp`, `finalize_graph`,
  `create_communities`, `create_community_reports`, `generate_text_embeddings`, and a parallel
  `update_*` family for incremental re-indexing.
- **The operations underneath** — `index/operations/`: `extract_graph/graph_extractor.py`,
  `summarize_communities/` (the community-report builder), `summarize_descriptions/`,
  `extract_covariates/claim_extractor.py`, `cluster_graph.py`, `prune_graph.py`, and
  `build_noun_graph/np_extractors/` — a **non-LLM graph construction path** using CFG, regex
  and syntactic noun-phrase extraction with a validator and stop-word list.
- **Four query strategies** — `query/structured_search/`: `local_search`, `global_search`,
  `drift_search`, `basic_search`.
- **A worked corpus with its outputs** — `docs/data/operation_dulce/` and
  `docs/examples_notebooks/inputs/`, including the resulting `entities.parquet`,
  `communities.parquet`, `community_reports.parquet`, `covariates.parquet` and a LanceDB store.
- **Seven notebooks** — `docs/examples_notebooks/`, including `drift_search.ipynb`,
  `global_search_with_dynamic_community_selection.ipynb` and three index-migration notebooks.
- **Eight independently versioned packages** — `graphrag-cache`, `-chunking`, `-common`,
  `-input`, `-llm`, `-storage`, `-vectors`, `graphrag`.

## Transferable Capability
**Answer questions about a whole collection by summarising its natural groupings in advance, rather than by retrieving fragments at the moment of asking.** A question about the whole has no answer in any single part, so no amount of better retrieval reaches it; the answer has to be precomputed at the level of the group. Doing so hierarchically gives the same collection described at several levels of granularity, and the question selects the level.

The separable prior step: **derive the groupings from the material's own connections rather than assigning them**, which surfaces structure nobody imposed. A practice worth noting independently of the method: **the project's own working procedures are shipped as executable instructions**, so the mechanical parts of contributing are performed rather than interpreted.

**Alternative to:** retrieval-and-read, which can only answer questions whose answer sits somewhere specific; and to a hand-maintained taxonomy, which reflects what its author expected. **Applies wherever** somebody needs to know what a body of material *amounts to* rather than where a fact is inside it.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Knowledge_Management
- Maturity Stage: Active
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: CLI
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: Procedural

## Integration & Use Cases
- Index a document collection where the questions are about themes rather than passages.
- Take the community-report idea alone: summarise detected clusters and store the summaries.
- Take the noun-phrase graph path when the LLM extraction cost is prohibitive.

## Reading Notes
**Popularity and activity both mislead here.** 35,819 stars and a push the day before this pass, yet the first line of the README is a warning: "This project is largely in maintenance mode, and won't be accepting new PRs or implementing new features. We'll perform bug fixes and dependency updates as appropriate, particularly to address CVEs." The recent commits are maintenance. Also note the README's own cost warning — indexing is expensive — and that prompts are expected to be tuned per corpus, with a dedicated guide, because out-of-the-box results are explicitly not the best case.

## Semantic Links
- [parent_topic:: [[Topic - Knowledge Management]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[run-llama - llama_index]]]
- [related_to:: [[neo4j-labs - neocarta]]]
- [related_to:: [[urchade - GLiNER]]]
- [implements_pattern:: [[Pattern - Graph Community Summarisation]]]
- [mentions_term:: [[Glossary - Retrieval-Augmented Generation]]]
- [mentions_term:: [[Glossary - Community Detection]]]
- [mentions_term:: [[Glossary - Knowledge Graph]]]
- [mentions_term:: [[Glossary - LLM]]]

## Evidence
- Source URL: https://github.com/microsoft/graphrag
- Source kind: GitHub REST metadata plus the repository tree and files, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-03
- Depth of read: recorded per source in [[Scouting Working File 2026-09-03]]

## GitHub Snapshot

- Description: A modular graph-based Retrieval-Augmented Generation (RAG) system
- Language: Python
- License (SPDX): MIT
- Default Branch: main
- Stars: 35819
- Homepage: https://microsoft.github.io/graphrag/
- Pushed At: 2026-09-02T01:41:10Z
- Topics: gpt, gpt-4, gpt4, graphrag, llm, llms, rag

## Evidence Anchors
- [github_repo] description :: A modular graph-based Retrieval-Augmented Generation (RAG) system (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: MIT (confidence 0.90)
- [github_repo] topics :: gpt, gpt-4, gpt4, graphrag, llm, llms, rag (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-03 (confidence 0.95)
