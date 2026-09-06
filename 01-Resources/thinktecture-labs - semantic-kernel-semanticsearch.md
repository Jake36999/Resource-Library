---
uuid: "fabfd159-899e-5ae4-a378-abf3c0d1a40c"
canonical_url: "https://github.com/thinktecture-labs/semantic-kernel-semanticsearch"
repo_key: "thinktecture-labs/semantic-kernel-semanticsearch"
owner: "thinktecture-labs"
repo_name: "semantic-kernel-semanticsearch"
aliases: ["thinktecture-labs/semantic-kernel-semanticsearch", "https://github.com/thinktecture-labs/semantic-kernel-semanticsearch"]
type: "reference_implementation"
primary_topic: "Knowledge Management"
secondary_topics: ["Agentic AI & Models"]
ecosystem: "Mixed"
domain_primary: "Knowledge_Management"
maturity_stage: "Reference"
license_class: "Unknown"
deployment_target: "Local_Only"
interface_protocol: "CLI"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Vector Similarity Search", "Model Inference Pipeline"]
glossary_terms: ["Semantic Search", "Embedding", "Retrieval-Augmented Generation"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Unknown"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: "Example how to implement a question & answer flow using semantic search with OpenAI - by using C# & Semantic Kernel"
github_language: "C#"
github_license_spdx: "NOASSERTION"
github_default_branch: "main"
github_stars: 27
github_topics: ["dotnet", "embeddings", "generative-ai", "llms", "openai", "semantic-kernel", "semantic-search"]
github_pushed_at: "2024-05-06T11:26:06Z"
---
# thinktecture-labs - semantic-kernel-semanticsearch

## Bottom Line
A minimal C# question-and-answer flow over semantic search, built on Semantic Kernel — thirteen files, five of them the application, with the vector store as a local SQLite-style file rather than a service.

## What It Solves
- See retrieval-augmented question answering in .NET rather than Python.
- Run the whole flow locally, with the embedding store as a file on disk.
- Keep the example small enough that the flow itself is visible.

## Architecture & Mechanics
- Five files under `src/SkSemanticSearch/` constitute the application; the rest of the repository is solution scaffolding and editor configuration.
- A `.db` file is committed in the tree, so the embedding store is local and file-based — there is no vector service in the picture.
- Semantic Kernel supplies the orchestration; this repository supplies the arrangement, which is the whole demonstration.
- **Not read:** any C# source. The above is inferred from the file tree and the repository's stated purpose.

## What Is Inside
- **A five-file C# application** — `src/SkSemanticSearch/`, with a `.csproj` and a solution file.
- **A committed `.db` file** — the embedding store, present in the repository, which is what makes the example runnable without provisioning anything.
- **Thirteen paths in total**, including `.vs/` and `.vscode/` editor state that was committed by accident rather than by design.
- **Not here:** a licence file, tests, or any documentation beyond the README.

## Transferable Capability
**Keep the vector store as a file until scale forces otherwise.** An embedding index for a modest corpus is a few megabytes; making it a file removes provisioning, network failure, synchronisation and cost from a system that has none of those problems yet. The general form is: *choose the smallest storage substrate that satisfies the actual corpus size*, and treat the upgrade to a service as a decision to be triggered by measurement rather than made in advance.

**Alternative to:** a vector database service, which is correct at scale and pure overhead below it. **Applies wherever** an index is small, single-writer and rebuildable — which describes most internal corpora.

## Taxonomy
- Ecosystem: Mixed
- Domain Primary: Knowledge_Management
- Maturity Stage: Reference
- License Class: Unknown
- Deployment Target: Local_Only
- Interface Protocol: CLI
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Read it as the smallest complete .NET retrieval-augmented flow when the surrounding stack is C# rather than Python.
- Use the file-backed store as the default for a corpus that has not yet outgrown one machine.
- Compare with [[roomi-fields - rtfm]], which makes the same embedded-storage bet at much larger scale.

## Reading Notes
**No licence file and none reported by GitHub**, so it is excluded from every licence-constrained answer; read it, do not lift from it. Last pushed 2024-05-06, and Semantic Kernel's APIs have changed substantially since — expect the arrangement to be instructive and the code not to compile. The committed `.vs/` directory is editor state that should not be in the tree, which is a fair indication of how finished this is.

## Semantic Links
- [parent_topic:: [[Topic - Knowledge Management]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[Azure-Samples - semantic-kernel-advanced-usage]]]
- [related_to:: [[roomi-fields - rtfm]]]
- [related_to:: [[diicellman - dspy-rag-fastapi]]]
- [implements_pattern:: [[Pattern - Vector Similarity Search]]]
- [implements_pattern:: [[Pattern - Model Inference Pipeline]]]
- [mentions_term:: [[Glossary - Semantic Search]]]
- [mentions_term:: [[Glossary - Embedding]]]
- [mentions_term:: [[Glossary - Retrieval-Augmented Generation]]]

## Evidence
- Source URL: https://github.com/thinktecture-labs/semantic-kernel-semanticsearch
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; no C# source was opened, and no licence file exists to read

## GitHub Snapshot

- Description: Example how to implement a question & answer flow using semantic search with OpenAI - by using C# & Semantic Kernel
- Language: C#
- License (SPDX): NOASSERTION
- Default Branch: main
- Stars: 27
- Pushed At: 2024-05-06T11:26:06Z
- Topics: dotnet, embeddings, generative-ai, llms, openai, semantic-kernel, semantic-search

## Evidence Anchors
- [github_repo] description :: Example how to implement a question & answer flow using semantic search with OpenAI - by using C# & Semantic Kernel (confidence 0.95)
- [github_repo] language :: C# (confidence 0.90)
- [github_repo] license :: NOASSERTION (confidence 0.90)
- [github_repo] topics :: dotnet, embeddings, generative-ai, llms, openai, semantic-kernel, semantic-search (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 13 paths at HEAD (confidence 0.95)
