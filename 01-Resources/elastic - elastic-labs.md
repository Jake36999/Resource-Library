---
uuid: "5f2c9c44-33ed-517f-af45-3a48314cc5b0"
canonical_url: "https://github.com/elastic/elastic-labs"
repo_key: "elastic/elastic-labs"
owner: "elastic"
repo_name: "elastic-labs"
aliases: ["elastic/elastic-labs", "https://github.com/elastic/elastic-labs"]
type: "tutorial"
primary_topic: "Knowledge Management"
secondary_topics: ["Infrastructure & Observability", "Security & SIEM"]
ecosystem: "Python"
domain_primary: "Knowledge_Management"
maturity_stage: "Active"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "REST"
data_locality: "Distributed"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "Documented"
patterns: ["Hybrid Retrieval", "Vector Similarity Search", "Observability Pipeline"]
glossary_terms: ["Semantic Search", "Vector Database", "Chunking", "Retrieval-Augmented Generation", "Reranking"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: "Notebooks & Example Apps for Search, Observability, and Security with Elasticsearch"
github_language: "Jupyter Notebook"
github_license_spdx: "Apache-2.0"
github_default_branch: "main"
github_stars: 1127
github_topics: ["ai", "applications", "chatgpt", "chatlog", "elastic", "elasticsearch", "genai", "genaistack", "langchain", "langchain-python", "openai", "openai-chatgpt", "python", "search", "vector", "vectordatabase"]
github_pushed_at: "2026-08-26T14:22:31Z"
---
# elastic - elastic-labs

## Bottom Line
A thousand-file working archive from Elastic's own engineering writing: notebooks, complete example apps and datasets covering search, observability and security, with the retrieval material notable for treating chunking and relevance as measurable rather than settled.

## What It Solves
- Follow a retrieval technique from an article to code that runs, with the data included.
- Compare relevance configurations against each other on the same corpus.
- See a whole RAG application — ingestion, API, frontend, deployment — rather than a snippet.

## Architecture & Mechanics
- The repository is organised by artefact type rather than by topic: `notebooks/` (96) teach, `example-apps/` (267) are complete deployable applications, `supporting-blog-content/` (618) is the code behind individual articles, and `datasets/` holds shared corpora.
- `notebooks/` is itself split by concern — `search` (30), `integrations` (27), `langchain` (12), `document-chunking` (7), `ingestion-and-chunking` (4), `model-upgrades` (4), `generative-ai` (4) — so chunking, ingestion and upgrades are separate subjects rather than steps in one tutorial.
- Notebooks are executed in CI by a purpose-built runner: `bin/nbtest`, `bin/find-notebooks-to-test.sh`, `.nbtest.yml` files and explicit `_nbtest.teardown.*.ipynb` notebooks. Teardown is a first-class artefact because these notebooks create real indices.
- Every app ships its own deployment: 19 container files, `docker/docker-compose-elastic.yml`, and `k8s/` manifests.
- **Not read:** any notebook or application. The structure above is read off directory names, file counts and the test-harness filenames.

## What Is Inside
- **A relevance workbench** — `example-apps/relevance-workbench/` (55 files, with its own API, frontend and Dockerfiles): an application whose entire purpose is comparing ranking configurations side by side. The most directly reusable idea in the repository for anyone tuning retrieval.
- **Chunking as its own subject** — `notebooks/document-chunking/`: `tokenization.ipynb`, `with-index-pipelines.ipynb`, `with-langchain-splitters.ipynb`, `configuring-chunking-settings-for-inference-endpoints.ipynb` — two chunking approaches compared, plus their teardown notebooks.
- **Shared datasets** — `datasets/book_summaries_1000_chunked.json`, `datasets/workplace-documents.json`, `notebooks/search/listings.csv`, and a learning-to-rank corpus `movies-corpus.jsonl.gz`. Real evaluation material, reusable outside Elastic entirely.
- **Four complete applications** — `chatbot-rag-app` (87 files), `internal-knowledge-search` (57), `search-tutorial` (50), `openai-embeddings` (14), plus `elasticsearch-mcp-server`.
- **A notebook CI harness** — `bin/nbtest` and the `_nbtest.teardown.*` convention: how to test notebooks that create real state.
- **A hybrid-search worked example with a real catalogue** — `supporting-blog-content/hybrid-search-for-an-e-commerce-product-catalogue/` (31 files); also `building-multimodal-rag-with-elasticsearch-gotham` (28) and `navigating-an-elastic-vector-database` (16).
- **Not here:** Elasticsearch. Every example assumes a cluster.

## Transferable Capability
**Make relevance a thing you compare, and make the comparison an application.** The workbench is the transferable object: a running surface where two ranking configurations answer the same queries side by side turns an argument about relevance into an observation. Second, **treat chunking as a subject with alternatives rather than a preprocessing step** — the notebooks compare index pipelines against library splitters, which is exactly the decision most retrieval systems make once, silently, and never revisit.

The third idea is operational and easy to overlook: **notebooks that create real state need a committed teardown**, or the collection becomes untestable and then untrue.

**Alternative to:** tuning relevance by intuition and shipping; and to documentation that describes a technique without leaving anything runnable behind. **Applies wherever** ranking quality matters and there is currently no way to see one configuration against another.

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
- Agent Surface: Documented

## Integration & Use Cases
- Take `relevance-workbench` as the model for a side-by-side ranking comparison in any search system.
- Read `notebooks/document-chunking/` before fixing a chunking strategy.
- Reuse `datasets/` and the learning-to-rank corpus as evaluation material independent of Elasticsearch.

## Reading Notes
Vendor-published and it shows: everything assumes an Elasticsearch cluster, and the retrieval conclusions are drawn inside that assumption. The portable parts are the *methods* — the workbench pattern, the chunking comparison, the notebook teardown convention — and the datasets. Note the shape of the repository: 618 of 1,006 files are `supporting-blog-content`, tied to individual articles of varying age, so freshness varies enormously across the tree even though the repository as a whole is actively pushed.

## Semantic Links
- [parent_topic:: [[Topic - Knowledge Management]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[lancedb - vectordb-recipes]]]
- [related_to:: [[qdrant - examples]]]
- [related_to:: [[DiceTechJobs - SolrConfigExamples]]]
- [related_to:: [[roomi-fields - rtfm]]]
- [implements_pattern:: [[Pattern - Hybrid Retrieval]]]
- [implements_pattern:: [[Pattern - Vector Similarity Search]]]
- [implements_pattern:: [[Pattern - Observability Pipeline]]]
- [mentions_term:: [[Glossary - Semantic Search]]]
- [mentions_term:: [[Glossary - Vector Database]]]
- [mentions_term:: [[Glossary - Chunking]]]
- [mentions_term:: [[Glossary - Retrieval-Augmented Generation]]]
- [mentions_term:: [[Glossary - Reranking]]]

## Evidence
- Source URL: https://github.com/elastic/elastic-labs
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; no notebook, application or dataset was opened

## GitHub Snapshot

- Description: Notebooks & Example Apps for Search, Observability, and Security with Elasticsearch
- Language: Jupyter Notebook
- License (SPDX): Apache-2.0
- Default Branch: main
- Stars: 1127
- Pushed At: 2026-08-26T14:22:31Z
- Topics: ai, applications, chatgpt, chatlog, elastic, elasticsearch, genai, genaistack, langchain, langchain-python, openai, openai-chatgpt, python, search, vector, vectordatabase

## Evidence Anchors
- [github_repo] description :: Notebooks & Example Apps for Search, Observability, and Security with Elasticsearch (confidence 0.95)
- [github_repo] language :: Jupyter Notebook (confidence 0.90)
- [github_repo] license :: Apache-2.0 (confidence 0.90)
- [github_repo] topics :: ai, applications, chatgpt, chatlog, elastic, elasticsearch, genai, genaistack, langchain, langchain-python, openai, openai-chatgpt, python, search, vector, vectordatabase (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 1006 paths at HEAD (confidence 0.95)
