---
uuid: "52e2ac42-b0c8-5f8d-a10d-b3c1fc946001"
canonical_url: "https://github.com/fynnfluegge/codeqai"
repo_key: "fynnfluegge/codeqai"
owner: "fynnfluegge"
repo_name: "codeqai"
aliases: ["fynnfluegge/codeqai", "https://github.com/fynnfluegge/codeqai"]
type: "developer_tool"
primary_topic: "Code Intelligence & Structural Parsing"
secondary_topics: ["Knowledge Management", "ML Training & MLOps"]
ecosystem: "Python"
domain_primary: "Code_Intelligence"
maturity_stage: "Abandoned"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "CLI"
data_locality: "Local_First"
hardware_footprint: "Low_VRAM"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Semantic Code Retrieval", "Structural Code Search", "Model Inference Pipeline"]
glossary_terms: ["Semantic Search", "Vector Database", "Embedding", "Training Data Attribution"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: "Local first semantic code search and chat | Leverage custom copilots with fine-tuning datasets from code in Alpaca, Conversational, Completion and Instruction format"
github_language: "Python"
github_license_spdx: "Apache-2.0"
github_default_branch: "main"
github_stars: 492
github_topics: ["codellama", "faiss", "gpt", "huggingface", "langchain", "llama2", "llamacpp", "llm", "ollama", "openai", "sentence-transformers"]
github_pushed_at: "2025-12-12T13:40:27Z"
---
# fynnfluegge - codeqai

## Bottom Line
Local-first semantic code search and chat that splits code at syntactic boundaries using tree-sitter before embedding it, and can then export the same repository as a fine-tuning dataset in four instruction formats.

## What It Solves
- Search and ask questions about a codebase with the model running locally.
- Chunk code at function and class boundaries rather than by character count, so a retrieved fragment is a whole thing.
- Turn a repository into training data without writing an extraction pipeline.

## Architecture & Mechanics
- `codeqai/treesitter/` is 16 of the 31 source files — over half the implementation is the *splitting* layer. Chunking at syntax boundaries is not a small addition to embedding search; it is the larger half of it.
- The vector layer is FAISS with a tested store (`tests/vector_store_test.py`, `tests/fixtures/vector_entries.py`), keeping retrieval local and file-based rather than requiring a server.
- A second, separable output path exists: `codeqai/dataset_extractor.py` writes the parsed repository out as `datasets/alpaca_dataset.json`, `completion_dataset.json` and `conversational_dataset.json` — the same parse serving both retrieval and training-data production.
- Environments are pinned per platform: `conda-linux-64.lock`, `conda-osx-64.lock`, `conda-win-64.lock` plus `poetry.lock`.
- **Not read:** any Python source. The proportions above come from file counts and directory names.

## What Is Inside
- **A tree-sitter splitting layer** — `codeqai/treesitter/`, 16 files, larger than the rest of the tool.
- **Three exported dataset formats** — `datasets/alpaca_dataset.json`, `completion_dataset.json`, `conversational_dataset.json`, produced by `codeqai/dataset_extractor.py`. Present as committed examples, so the output format is inspectable without running anything.
- **A fine-tuning notebook** — `notebooks/alpaca_fine_tuning_qwen_2_5_coder_3B.ipynb`: the downstream half of the dataset story, worked through end to end.
- **Locked environments for three platforms** — the conda lock files, which for a local-model tool is the difference between working and not.
- **A Streamlit configuration** (`.streamlit/`) alongside the CLI.
- **Not here:** a hosted service. Every provider it supports — Ollama, llama.cpp, sentence-transformers, or a hosted API — is a configuration choice, not a requirement.

## Transferable Capability
**Parse first, then embed.** A retrieved fragment that begins mid-function is worse than useless: it reads as complete and is not. Splitting at boundaries the language already defines removes the chunk-size hyperparameter entirely, and the cost is visible here as half the codebase. The second, more interesting idea is that **one parse serves two consumers**: the same structural split that makes retrieval accurate also makes a clean training set, so the expensive step is paid once. That is a general shape — a well-chosen intermediate representation usually has more than one customer.

**Alternative to:** fixed-size or overlapping-window chunking, which is trivial to implement and produces fragments that straddle definitions; and to writing a separate extraction pipeline when the same repository is needed as training data. **Applies wherever** a document has structure that a naive splitter would ignore — legislation, specifications, structured records, transcripts with turns.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Code_Intelligence
- Maturity Stage: Abandoned
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: CLI
- Data Locality: Local_First
- Hardware Footprint: Low_VRAM
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Adopt the parse-then-embed order in any retrieval system currently chunking by character count.
- Inspect the three committed dataset JSONs to see instruction-format differences without generating them.
- Read `codeqai/dataset_extractor.py`'s outputs as a model for deriving training data from a structural parse you already have.

## Reading Notes
**Archived on GitHub, last pushed 2025-12-12.** It is settled rather than stalled — the code is complete and readable — but it will not track changes in the model providers it wraps, and that is where a tool like this ages first. The tree-sitter splitting layer and the dataset extractor are the parts most worth lifting; both are separable from the chat interface that dates fastest.

## Semantic Links
- [parent_topic:: [[Topic - Code Intelligence & Structural Parsing]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[tree-sitter - tree-sitter]]]
- [related_to:: [[sturdy-dev - semantic-code-search]]]
- [related_to:: [[hamelsmu - code_search]]]
- [related_to:: [[jgravelle - jcodemunch-mcp]]]
- [implements_pattern:: [[Pattern - Semantic Code Retrieval]]]
- [implements_pattern:: [[Pattern - Structural Code Search]]]
- [implements_pattern:: [[Pattern - Model Inference Pipeline]]]
- [mentions_term:: [[Glossary - Semantic Search]]]
- [mentions_term:: [[Glossary - Vector Database]]]
- [mentions_term:: [[Glossary - Embedding]]]
- [mentions_term:: [[Glossary - Training Data Attribution]]]

## Evidence
- Source URL: https://github.com/fynnfluegge/codeqai
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; no Python source, notebook or dataset file was opened

## GitHub Snapshot

- Description: Local first semantic code search and chat | Leverage custom copilots with fine-tuning datasets from code in Alpaca, Conversational, Completion and Instruction format
- Language: Python
- License (SPDX): Apache-2.0
- Default Branch: main
- Stars: 492
- Pushed At: 2025-12-12T13:40:27Z
- Topics: codellama, faiss, gpt, huggingface, langchain, llama2, llamacpp, llm, ollama, openai, sentence-transformers

## Evidence Anchors
- [github_repo] description :: Local first semantic code search and chat | Leverage custom copilots with fine-tuning datasets from code in Alpaca, Conversational, Completion and Instruction format (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: Apache-2.0 (confidence 0.90)
- [github_repo] topics :: codellama, faiss, gpt, huggingface, langchain, llama2, llamacpp, llm, ollama, openai, sentence-transformers (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 51 paths at HEAD (confidence 0.95)
