---
uuid: "8d0c61c0-5299-560c-9c6f-1a4b724d79d2"
canonical_url: "https://github.com/Azure-Samples/graphrag-accelerator"
repo_key: "Azure-Samples/graphrag-accelerator"
owner: "Azure-Samples"
repo_name: "graphrag-accelerator"
aliases: ["Azure-Samples/graphrag-accelerator", "https://github.com/Azure-Samples/graphrag-accelerator"]
type: "reference_implementation"
primary_topic: "Knowledge Management"
secondary_topics: ["Infrastructure & Observability", "Agentic AI & Models"]
ecosystem: "Python"
domain_primary: "Knowledge_Management"
maturity_stage: "Abandoned"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "REST"
data_locality: "Distributed"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Knowledge Graph Routing", "Graph Community Summarisation", "Infrastructure as Code", "Reference Architecture"]
glossary_terms: ["Knowledge Graph", "Retrieval-Augmented Generation", "Community Detection", "Infrastructure as Code"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 5
github_description: "One-click deploy of a Knowledge Graph powered RAG (GraphRAG) in Azure"
github_language: "Python"
github_license_spdx: "MIT"
github_default_branch: "main"
github_stars: 2409
github_homepage: "https://github.com/microsoft/graphrag"
github_pushed_at: "2025-05-27T13:56:40Z"
---
# Azure-Samples - graphrag-accelerator

## Bottom Line
The operational half of GraphRAG: the API, the Kubernetes deployment and the twenty-six Bicep templates needed to run graph-based retrieval as a hosted service — which is the part a research repository leaves out and the part that decides whether it can be adopted.

## What It Solves
- Run GraphRAG as a service with an API, rather than as a library invoked from a notebook.
- See what the infrastructure for graph-based retrieval actually costs, itemised.
- Deploy it without assembling the cloud resources by hand.

## Architecture & Mechanics
- The split is clean: `backend/graphrag_app/` (24 files) is the API, `infra/` (54 files) is everything needed to run it, and `frontend/` (19, Streamlit) is a demonstration surface rather than a product.
- The infrastructure is itemised as 26 Bicep templates under `infra/core/`, one per resource — AKS, API Management, Azure OpenAI, AI Search, container registry. Reading the directory listing tells you the true dependency footprint of hosted graph retrieval faster than any architecture document.
- `openapi.json` at the repository root fixes the API contract, and `infra/core/apim/apim.graphrag-api.bicep` places API Management in front of it.
- Helm charts (`infra/helm/graphrag/`) and a managed-application definition (`infra/managed-app/`) give two further deployment shapes.
- **Not read:** any Python, Bicep or notebook file. The above is read off the tree and the resource-named template filenames.

## What Is Inside
- **Twenty-six Bicep templates** — `infra/core/`, one per Azure resource: the honest inventory of what this needs to run.
- **A synthetic test dataset with GraphRAG's own outputs** — `backend/tests/data/synthetic-dataset/output/`: eight Parquet files including `create_final_communities.parquet`, `create_final_community_reports.parquet`, `create_final_entities.parquet`, `create_final_covariates.parquet`, with an `ABOUT.md`. **The intermediate artefacts of a graph-RAG pipeline, committed and inspectable without running anything** — the most useful thing here for someone trying to understand what GraphRAG actually produces.
- **An OpenAPI specification** — `openapi.json` at the root, and a second under `infra/core/apim/`.
- **Two deployment guides** — `docs/DEPLOYMENT-GUIDE.md`, `docs/DEVELOPMENT-GUIDE.md`, plus `docs/assets/graphrag-architecture-diagram.png` and its editable `.vsdx`.
- **`TRANSPARENCY.md`** at the root — Microsoft's disclosure of intended use and limitations, a document type rare elsewhere in this catalogue.
- **Two quickstart notebooks** — `notebooks/1-Quickstart.ipynb`, `2-Advanced_Getting_Started.ipynb`.
- **Not here:** GraphRAG itself, which is [[microsoft - graphrag]].

## Transferable Capability
**Publish the deployment as an artefact, because it is where the real cost of an approach becomes visible.** A method described in a paper has no footprint; the same method expressed as twenty-six infrastructure templates has an unmistakable one, and that listing answers *can we afford this* faster than any evaluation. The second and more portable idea is **committing the pipeline's intermediate outputs**: the Parquet files here let a reader inspect what entity extraction and community reporting actually produced without running the pipeline, which turns an opaque process into an inspectable one.

**Alternative to:** a research repository that leaves operation as an exercise, and to deployment documentation, which describes resources instead of declaring them. **Applies wherever** a technique must be judged on total cost rather than on its results — and wherever a multi-stage pipeline is hard to debug because nobody can see what the middle stages emit.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Knowledge_Management
- Maturity Stage: Abandoned
- License Class: Permissive
- Deployment Target: Server
- Interface Protocol: REST
- Data Locality: Distributed
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Read `infra/core/` as the itemised cost of hosted graph retrieval before committing to the approach.
- Open the committed Parquet outputs to understand GraphRAG's intermediate artefacts without running a pipeline.
- Take the commit-your-intermediates practice into any multi-stage pipeline whose middle is currently invisible.

## Reading Notes
**Archived, last pushed 2025-05-27.** Azure resource APIs and GraphRAG both moved on, so the Bicep should be read as a record of the footprint rather than run. 2,409 stars for an accelerator that is now read-only: the deployment shape was clearly what people wanted, and its retirement leaves that gap open. The committed Parquet outputs are the part with the longest useful life, because they document what the pipeline produces regardless of how it is deployed.

## Semantic Links
- [parent_topic:: [[Topic - Knowledge Management]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[microsoft - graphrag]]]
- [related_to:: [[JayLZhou - GraphRAG]]]
- [related_to:: [[neo4j-labs - neocarta]]]
- [related_to:: [[hashicorp - terraform]]]
- [implements_pattern:: [[Pattern - Knowledge Graph Routing]]]
- [implements_pattern:: [[Pattern - Graph Community Summarisation]]]
- [implements_pattern:: [[Pattern - Infrastructure as Code]]]
- [implements_pattern:: [[Pattern - Reference Architecture]]]
- [mentions_term:: [[Glossary - Knowledge Graph]]]
- [mentions_term:: [[Glossary - Retrieval-Augmented Generation]]]
- [mentions_term:: [[Glossary - Community Detection]]]
- [mentions_term:: [[Glossary - Infrastructure as Code]]]

## Evidence
- Source URL: https://github.com/Azure-Samples/graphrag-accelerator
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; no Python, Bicep, notebook or Parquet file was opened

## GitHub Snapshot

- Description: One-click deploy of a Knowledge Graph powered RAG (GraphRAG) in Azure
- Language: Python
- License (SPDX): MIT
- Default Branch: main
- Stars: 2409
- Homepage: https://github.com/microsoft/graphrag
- Pushed At: 2025-05-27T13:56:40Z

## Evidence Anchors
- [github_repo] description :: One-click deploy of a Knowledge Graph powered RAG (GraphRAG) in Azure (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: MIT (confidence 0.90)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 167 paths at HEAD (confidence 0.95)
