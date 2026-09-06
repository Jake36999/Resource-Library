---
uuid: "bf6c6364-c440-5487-875a-cdcdb1635171"
canonical_url: "https://github.com/JayLZhou/GraphRAG"
repo_key: "JayLZhou/GraphRAG"
owner: "JayLZhou"
repo_name: "GraphRAG"
aliases: ["JayLZhou/GraphRAG", "https://github.com/JayLZhou/GraphRAG"]
type: "research_artifact"
primary_topic: "Knowledge Management"
secondary_topics: ["Agentic AI & Models"]
ecosystem: "Python"
domain_primary: "Knowledge_Management"
maturity_stage: "Reference"
license_class: "Unknown"
deployment_target: "Local_Only"
interface_protocol: "Python_SDK"
data_locality: "Local_First"
hardware_footprint: "Low_VRAM"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Knowledge Graph Routing", "Graph Community Summarisation", "Hybrid Retrieval"]
glossary_terms: ["Knowledge Graph", "Retrieval-Augmented Generation", "Community Detection", "Semantic Search"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Unknown"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 5
github_description: "In-depth study of the graphrag "
github_language: "Python"
github_license_spdx: "NOASSERTION"
github_default_branch: "master"
github_stars: 1539
github_pushed_at: "2025-07-01T17:41:28Z"
---
# JayLZhou - GraphRAG

## Bottom Line
A VLDB 2025 study that decomposes graph-based retrieval into interchangeable stages — graph construction, indexing, chunking, retrieval, query — and implements ten published methods against that common framework so they can be compared rather than each believed on its own terms.

## What It Solves
- Compare graph-RAG methods on the same data and the same stages, instead of on each author's own benchmark.
- Identify which stage a method's benefit actually comes from.
- Reuse one implementation of the shared machinery across ten variants.

## Architecture & Mechanics
- The decomposition *is* the contribution, and it is visible in the directory layout: `Core/Graph`, `Core/Index`, `Core/Chunk`, `Core/Retriever`, `Core/Query`, `Core/Storage`, `Core/Prompt`, `Core/Schema`. Any method is then a configuration over these stages rather than a separate program.
- `Option/Method/` holds ten YAML files — one per published method. Because the stages are shared, the difference between two methods is a diff between two configurations, which is exactly what makes them comparable.
- `Core/Schema/` (8 files: `ChunkSchema`, `CommunitySchema`, `EntityRelation`, `GraphSchema`, `Message`, `RetrieverContext`) fixes the interfaces between stages, which is the precondition for swapping any one of them.
- Evaluation runs against a shared dataset — `Data/HotpotQA/Corpus.json` with `Data/QueryDataset.py` — rather than per-method data.
- **Not read:** any Python source or method configuration. The decomposition above is read off the directory structure and the schema filenames.

## What Is Inside
- **The paper** — `VLDB2025_GraphRAG.pdf`, committed at the repository root. The reasoning and the results are in it; the code alone will not tell you what was concluded.
- **Ten method configurations** — `Option/Method/`, one YAML per published graph-RAG method, over one shared implementation.
- **Eight stage schemas** — `Core/Schema/`: the interfaces that make the stages interchangeable.
- **A shared evaluation corpus** — `Data/HotpotQA/Corpus.json`, plus `experiment.yml` at the root.
- **`Doc/workflow.png`** — the pipeline as a diagram, and the only documentation asset besides the paper.
- **Not here:** a licence, and any packaging. `.pyc` files are committed, which places this firmly as a research artefact rather than a library.

## Transferable Capability
**Decompose a family of competing methods into shared stages, then express each method as a configuration over those stages.** This converts an unfalsifiable comparison — every author benchmarking their own system on their own data — into an experiment where one variable moves at a time. It also localises benefit: if two methods differ only in the retrieval stage and one wins, the advantage is attributable. The precondition is **fixing the interfaces between stages as schemas**, without which the stages cannot be swapped and the whole approach collapses back into ten separate programs.

**Alternative to:** reading ten papers and believing each one's evaluation; and to re-implementing each method independently, which reintroduces the differences you were trying to control for. **Applies wherever** several approaches claim to solve the same problem and no shared frame exists to test them in — which is the ordinary situation when choosing between tools.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Knowledge_Management
- Maturity Stage: Reference
- License Class: Unknown
- Deployment Target: Local_Only
- Interface Protocol: Python_SDK
- Data Locality: Local_First
- Hardware Footprint: Low_VRAM
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Read the paper first, then `Option/Method/` to see how each published method reduces to a configuration.
- Take the stage-plus-schema decomposition into any comparison of competing approaches, in or out of retrieval.
- Use `Core/Schema/` as a worked example of interfaces that make components genuinely swappable rather than nominally so.

## Reading Notes
**No licence file and none reported by GitHub.** For an academic artefact that is common and it is still binding: this is readable, not reusable, and it is excluded from every licence-constrained answer here. Committed `.pyc` files and no packaging confirm the intent — this accompanies a paper. The comparison framework is the durable contribution and it outlives whichever method currently wins; 1,539 stars for an artefact with no licence suggests the framework is what people came for.

## Semantic Links
- [parent_topic:: [[Topic - Knowledge Management]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[microsoft - graphrag]]]
- [related_to:: [[Azure-Samples - graphrag-accelerator]]]
- [related_to:: [[neo4j-labs - neocarta]]]
- [related_to:: [[run-llama - llama_index]]]
- [implements_pattern:: [[Pattern - Knowledge Graph Routing]]]
- [implements_pattern:: [[Pattern - Graph Community Summarisation]]]
- [implements_pattern:: [[Pattern - Hybrid Retrieval]]]
- [mentions_term:: [[Glossary - Knowledge Graph]]]
- [mentions_term:: [[Glossary - Retrieval-Augmented Generation]]]
- [mentions_term:: [[Glossary - Community Detection]]]
- [mentions_term:: [[Glossary - Semantic Search]]]

## Evidence
- Source URL: https://github.com/JayLZhou/GraphRAG
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; the paper, source and configurations were not opened, and no licence file exists to read

## GitHub Snapshot

- Description: In-depth study of the graphrag 
- Language: Python
- License (SPDX): NOASSERTION
- Default Branch: master
- Stars: 1539
- Pushed At: 2025-07-01T17:41:28Z

## Evidence Anchors
- [github_repo] description :: In-depth study of the graphrag  (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: NOASSERTION (confidence 0.90)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 137 paths at HEAD (confidence 0.95)
