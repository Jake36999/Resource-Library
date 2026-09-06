---
uuid: "3329e8d5-d498-51df-b45c-a249e5b32472"
canonical_url: "https://github.com/run-llama/LlamaIndexTS"
repo_key: "run-llama/LlamaIndexTS"
owner: "run-llama"
repo_name: "LlamaIndexTS"
aliases: ["run-llama/LlamaIndexTS", "https://github.com/run-llama/LlamaIndexTS"]
type: "developer_tool"
primary_topic: "Knowledge Management"
secondary_topics: ["Agentic AI & Models"]
ecosystem: "Web_Frontend"
domain_primary: "Knowledge_Management"
maturity_stage: "Abandoned"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "Python_SDK"
data_locality: "Distributed"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "Documented"
patterns: ["Hybrid Retrieval", "Vector Similarity Search", "Agent Orchestration", "Model Inference Pipeline"]
glossary_terms: ["Retrieval-Augmented Generation", "Chunking", "Embedding", "Vector Database", "Agent"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: "Data framework for your LLM applications. Focus on server side solution"
github_language: "TypeScript"
github_license_spdx: "MIT"
github_default_branch: "main"
github_stars: 3077
github_topics: ["agent", "chatbot", "claude-ai", "create-llama", "embedding", "groq-ai", "javascript", "llama", "llama-index", "llama3", "llamaindex", "llm", "node", "nodejs", "openai", "react", "typescript"]
github_homepage: "https://ts.llamaindex.ai"
github_pushed_at: "2026-03-11T20:07:07Z"
---
# run-llama - LlamaIndexTS

## Bottom Line
The TypeScript implementation of LlamaIndex, built as a monorepo where every model provider, reader and vector store is a separate package — so an application depends on the four integrations it uses rather than on all of them.

## What It Solves
- Build retrieval-augmented applications in TypeScript, including in edge and serverless runtimes.
- Depend on one model provider without installing the other forty.
- Swap a vector store or a document reader without changing application code.

## Architecture & Mechanics
- `packages/providers/` is 335 files — the single largest component. Provider breadth is the product, and it is expensive: each integration is code somebody must keep working.
- `packages/core/` (171 files) holds the abstractions, with `packages/core/src/schema/` defining the node and response types that make providers interchangeable.
- `packages/env/` (47 files) exists solely to abstract the runtime — Node, edge, browser — which is what a TypeScript port has to solve and the Python original never faced.
- Testing is layered by cost: `unit/` (14 files) for logic, `e2e/` (131) with real provider fixtures, and `resolution-tests/` (8), which verify that the package graph resolves correctly under different module systems — a monorepo-specific failure mode caught deliberately.
- **Not read:** any TypeScript source. The proportions above are file counts and directory names.

## What Is Inside
- **335 provider integration files** — `packages/providers/`: the inventory of what connects to what.
- **295 example files** — `examples/` split by concern: `models` (71), `storage` (71), `agents` (25), `rag` (22), `readers` (22), `multimodal` (12), plus `deprecated/` (15) kept rather than deleted.
- **A documentation site in-tree** — `docs/src/` (151 files, 103 `.mdx`) with tutorial sequences under `framework/tutorials/agents/` numbered 1 to 4.
- **Resolution tests** — `resolution-tests/`: checking that a consumer can actually import the packages, which is a distinct class of bug from anything the unit tests cover.
- **Extensive agent instructions** — 39 paths including `CLAUDE.md` at the root and separate ones for `docs/` and `e2e/`, plus `packages/tools/` (28) and `packages/wasm-tools/` (14).
- **Snapshot tests** — 17 `.snap` files, and real fixtures under `e2e/fixtures/llm/` for Anthropic, OpenAI and Ollama.
- **Not here:** the Python LlamaIndex, which is [[run-llama - llama_index]] and a separate project with a separate lifecycle.

## Transferable Capability
**Make each integration a separately installable package, and test that the package graph resolves.** Breadth of integration is what a framework is bought for and also what makes it heavy; splitting per provider means a consumer pays for what they use, and an unmaintained integration can be abandoned without breaking anyone else. The cost is a new failure class — packages that build individually and cannot be imported together — which is why `resolution-tests/` is the interesting directory here: **a monorepo needs a test that the composition works, not only that the parts do.**

The **runtime-abstraction package** is the third idea: isolating every environment difference into one small package means the rest of the codebase can be written once for Node, edge and browser.

**Alternative to:** a single package with optional dependencies, which is simpler and installs everything; and to a plugin registry, which defers the compatibility problem to runtime. **Applies wherever** one library must integrate with many external services and consumers only ever need a few.

## Taxonomy
- Ecosystem: Web_Frontend
- Domain Primary: Knowledge_Management
- Maturity Stage: Abandoned
- License Class: Permissive
- Deployment Target: Server
- Interface Protocol: Python_SDK
- Data Locality: Distributed
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: Documented

## Integration & Use Cases
- Read `packages/env/` before porting anything that must run in Node, edge and browser runtimes.
- Copy the `resolution-tests/` idea into any monorepo publishing multiple interdependent packages.
- Use `examples/` as a per-concern reference — models, storage, agents, readers — rather than reading the framework documentation end to end.

## Reading Notes
**Archived, last pushed 2026-03-11**, at 3,077 stars. That is the fact that governs adoption: the TypeScript port is retired while the Python project remains active, so anything built on it is building on a frozen base. The architecture is still worth reading — the per-provider packaging and the runtime-abstraction package are good answers to real problems — but check what run-llama recommends for TypeScript now before depending on it.

## Semantic Links
- [parent_topic:: [[Topic - Knowledge Management]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[run-llama - llama_index]]]
- [related_to:: [[lancedb - vectordb-recipes]]]
- [related_to:: [[roomi-fields - rtfm]]]
- [implements_pattern:: [[Pattern - Hybrid Retrieval]]]
- [implements_pattern:: [[Pattern - Vector Similarity Search]]]
- [implements_pattern:: [[Pattern - Agent Orchestration]]]
- [implements_pattern:: [[Pattern - Model Inference Pipeline]]]
- [mentions_term:: [[Glossary - Retrieval-Augmented Generation]]]
- [mentions_term:: [[Glossary - Chunking]]]
- [mentions_term:: [[Glossary - Embedding]]]
- [mentions_term:: [[Glossary - Vector Database]]]
- [mentions_term:: [[Glossary - Agent]]]

## Evidence
- Source URL: https://github.com/run-llama/LlamaIndexTS
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; no TypeScript source, example or documentation page was opened

## GitHub Snapshot

- Description: Data framework for your LLM applications. Focus on server side solution
- Language: TypeScript
- License (SPDX): MIT
- Default Branch: main
- Stars: 3077
- Homepage: https://ts.llamaindex.ai
- Pushed At: 2026-03-11T20:07:07Z
- Topics: agent, chatbot, claude-ai, create-llama, embedding, groq-ai, javascript, llama, llama-index, llama3, llamaindex, llm, node, nodejs, openai, react, typescript

## Evidence Anchors
- [github_repo] description :: Data framework for your LLM applications. Focus on server side solution (confidence 0.95)
- [github_repo] language :: TypeScript (confidence 0.90)
- [github_repo] license :: MIT (confidence 0.90)
- [github_repo] topics :: agent, chatbot, claude-ai, create-llama, embedding, groq-ai, javascript, llama, llama-index, llama3, llamaindex, llm, node, nodejs, openai, react, typescript (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 1467 paths at HEAD (confidence 0.95)
