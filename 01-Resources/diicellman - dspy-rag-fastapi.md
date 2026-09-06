---
uuid: "b1e62649-e6da-5f39-8c07-58150255a222"
canonical_url: "https://github.com/diicellman/dspy-rag-fastapi"
repo_key: "diicellman/dspy-rag-fastapi"
owner: "diicellman"
repo_name: "dspy-rag-fastapi"
aliases: ["diicellman/dspy-rag-fastapi", "https://github.com/diicellman/dspy-rag-fastapi"]
type: "reference_implementation"
primary_topic: "Knowledge Management"
secondary_topics: ["Agentic AI & Models"]
ecosystem: "Python"
domain_primary: "Knowledge_Management"
maturity_stage: "Reference"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "REST"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Model Inference Pipeline", "Vector Similarity Search"]
glossary_terms: ["Retrieval-Augmented Generation", "Prompt", "ASGI", "API"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 5
github_description: "FastAPI wrapper around DSPy"
github_language: "Python"
github_license_spdx: "MIT"
github_default_branch: "main"
github_stars: 296
github_pushed_at: "2024-03-11T14:34:00Z"
---
# diicellman - dspy-rag-fastapi

## Bottom Line
A twenty-six-file demonstration of putting DSPy behind an HTTP API — which is the question DSPy raises and does not answer, because a framework that compiles its own prompts has to decide when compilation happens relative to serving.

## What It Solves
- Serve a DSPy program as an ordinary web API rather than running it from a script.
- Separate the compiled program from the request path.
- Deploy the whole thing, frontend included, with one compose file.

## Architecture & Mechanics
- Backend and frontend are separate services with separate Dockerfiles, joined by `compose.yml` at the root — the smallest complete deployable shape.
- `backend/app/` is nine files: FastAPI, the DSPy program, and the retrieval wiring. The demonstration is the arrangement, not the volume.
- Paul Graham's essay (`backend/data/example/paul_graham_essay.txt`) is the corpus, which is the conventional DSPy and LlamaIndex example text — chosen so a reader can compare behaviour against other tutorials using the same document.
- **Not read:** any Python source. The above is inferred from the tree, the framework's known shape and the repository's stated purpose.

## What Is Inside
- **A nine-file FastAPI backend** — `backend/app/`, with its own Dockerfile.
- **A three-page frontend** — `frontend/pages/`, with its own Dockerfile.
- **`compose.yml`** at the root — the two services joined.
- **The conventional example corpus** — `backend/data/example/paul_graham_essay.txt`.
- **Not here:** tests, evaluation, or any DSPy optimisation run. Twenty-six files in total.

## Transferable Capability
**When a framework generates part of itself, decide explicitly where that generation happens relative to serving.** DSPy compiles prompts from examples and a metric; that step is expensive and non-deterministic, so it cannot sit in a request path — which forces a build-time-versus-request-time boundary that a script never has to draw. The general shape recurs whenever a system optimises itself: **the artefact produced by optimisation is a deployable, and it needs versioning, storage and a rollback story like any other build output.**

**Alternative to:** running the optimiser in-process on each request, which is slow and irreproducible; and to hand-written prompts, which need no build step and no versioning because there is nothing generated to version. **Applies wherever** a component is compiled, trained or tuned before it can serve — models, query plans, generated clients.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Knowledge_Management
- Maturity Stage: Reference
- License Class: Permissive
- Deployment Target: Server
- Interface Protocol: REST
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Read it as the smallest complete answer to *how do I serve a DSPy program* before designing a larger one.
- Take the compose-plus-two-Dockerfiles shape as a minimal deployable for any model-backed API with a UI.
- Compare with [[ganarajpr - awesome-dspy]] for the surrounding ecosystem this demonstrates one slice of.

## Reading Notes
Last pushed 2024-03-11, and DSPy's API has changed substantially since — treat the arrangement as the lesson and the code as period-specific. Note also that the URL in the source list carried a stray trailing character (`dspy-rag-fastapi.git3`); the repository charted here is `diicellman/dspy-rag-fastapi`, confirmed by fetching it directly. Nothing here evaluates or optimises anything, which is ironic for a DSPy example and worth knowing before opening it.

## Semantic Links
- [parent_topic:: [[Topic - Knowledge Management]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[ganarajpr - awesome-dspy]]]
- [related_to:: [[reichenbch - RAG-examples]]]
- [related_to:: [[thinktecture-labs - semantic-kernel-semanticsearch]]]
- [implements_pattern:: [[Pattern - Model Inference Pipeline]]]
- [implements_pattern:: [[Pattern - Vector Similarity Search]]]
- [mentions_term:: [[Glossary - Retrieval-Augmented Generation]]]
- [mentions_term:: [[Glossary - Prompt]]]
- [mentions_term:: [[Glossary - ASGI]]]
- [mentions_term:: [[Glossary - API]]]

## Evidence
- Source URL: https://github.com/diicellman/dspy-rag-fastapi
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; no Python source was opened

## GitHub Snapshot

- Description: FastAPI wrapper around DSPy
- Language: Python
- License (SPDX): MIT
- Default Branch: main
- Stars: 296
- Pushed At: 2024-03-11T14:34:00Z

## Evidence Anchors
- [github_repo] description :: FastAPI wrapper around DSPy (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: MIT (confidence 0.90)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 26 paths at HEAD (confidence 0.95)
