---
uuid: "11286920-9d0f-5a83-934e-0bc7d7aecde2"
canonical_url: "https://github.com/reichenbch/RAG-examples"
repo_key: "reichenbch/RAG-examples"
owner: "reichenbch"
repo_name: "RAG-examples"
aliases: ["reichenbch/RAG-examples", "https://github.com/reichenbch/RAG-examples"]
type: "tutorial"
primary_topic: "Knowledge Management"
secondary_topics: ["ML Training & MLOps"]
ecosystem: "Python"
domain_primary: "Knowledge_Management"
maturity_stage: "Reference"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Python_SDK"
data_locality: "Local_First"
hardware_footprint: "Low_VRAM"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Vector Similarity Search", "Model Inference Pipeline"]
glossary_terms: ["Retrieval-Augmented Generation", "Embedding", "Vector Database", "Semantic Search"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: "Retrieval Augmented Generation Examples - Original, GPT based, Semantic Search based."
github_language: "Jupyter Notebook"
github_license_spdx: "MIT"
github_default_branch: "main"
github_stars: 65
github_topics: ["faiss", "langchain", "ml", "nlp-machine-learning", "rag"]
github_pushed_at: "2024-02-01T16:20:02Z"
---
# reichenbch - RAG-examples

## Bottom Line
Three notebooks placing today's RAG frameworks next to the original Meta RAG model they descend from, plus a multilingual variant — the comparison that shows how much of the idea was in the 2020 paper and how much is framework convenience.

## What It Solves
- Distinguish the RAG idea from the RAG toolchain by seeing both implemented.
- Retrieve across languages, where the query and the corpus are not in the same one.
- Read a whole RAG implementation in one notebook rather than across a framework.

## Architecture & Mechanics
- The three notebooks are the argument: `Meta Original RAG Model Implementation.ipynb` (the 2020 end-to-end trained model), `LangChain LLamaIndex RAG.ipynb` (the framework-composed version), and `LaBSE + RAG - Multilingual Support.ipynb`.
- The multilingual case is handled by the *embedding* choice — LaBSE maps many languages into one space — which locates cross-lingual retrieval in the encoder rather than in a translation step.
- A pre-built FAISS index is committed (`faiss_doc_idx/`), so the notebooks can be read and run without an indexing pass.
- `gradio_app.py` gives the three approaches a shared interface to be tried through.
- **Not read:** any notebook. The comparison above is read from the notebook filenames and the repository's stated purpose.

## What Is Inside
- **Three contrasting notebooks** at the repository root — the original Meta RAG model, the LangChain/LlamaIndex composition, and the LaBSE multilingual variant.
- **A committed FAISS index** — `faiss_doc_idx/` with a `.faiss` and a `.pkl` file, plus `dataset.txt` and `test_data.csv`: the corpus, the index and the queries are all present.
- **Five design images** — `bot_design1_*.png`, `bot_design2_*.png`: two architectures drawn out.
- **`gradio_app.py`** — a small shared interface over the approaches.
- **Not here:** anything beyond the three notebooks. Sixteen files in total.

## Transferable Capability
**Keep the original formulation of an idea alongside its convenient descendants.** Frameworks make a technique easy and simultaneously make its boundaries invisible — what was a research result becomes a default nobody can evaluate. Implementing both lets a reader see which parts of the behaviour come from the idea and which from the library, which is the only way to judge whether the library's choices suit a different problem. The **multilingual case is a second, sharper lesson**: putting cross-lingual capability in the embedding rather than in a translation stage removes a whole pipeline stage and its error, by choosing a different representation.

**Alternative to:** learning a technique through one framework, which conflates the idea with an implementation of it. **Applies wherever** a method has been absorbed into tooling and the original constraints are no longer visible to the people relying on it.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Knowledge_Management
- Maturity Stage: Reference
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Python_SDK
- Data Locality: Local_First
- Hardware Footprint: Low_VRAM
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Read the Meta original notebook alongside the framework one before accepting a framework's RAG defaults.
- Take the LaBSE approach when a corpus and its queries are in different languages.
- Reuse the committed FAISS index and `test_data.csv` as a ready-made small retrieval fixture.

## Reading Notes
Last pushed 2024-02-01 — the LangChain and LlamaIndex APIs it uses have moved considerably since, so the framework notebook will need repair. The Meta original notebook ages far better, which is itself the point the repository makes. Sixty-five stars, sixteen files: small, and worth it for the comparison rather than for any single implementation.

## Semantic Links
- [parent_topic:: [[Topic - Knowledge Management]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[run-llama - llama_index]]]
- [related_to:: [[lancedb - vectordb-recipes]]]
- [related_to:: [[diicellman - dspy-rag-fastapi]]]
- [implements_pattern:: [[Pattern - Vector Similarity Search]]]
- [implements_pattern:: [[Pattern - Model Inference Pipeline]]]
- [mentions_term:: [[Glossary - Retrieval-Augmented Generation]]]
- [mentions_term:: [[Glossary - Embedding]]]
- [mentions_term:: [[Glossary - Vector Database]]]
- [mentions_term:: [[Glossary - Semantic Search]]]

## Evidence
- Source URL: https://github.com/reichenbch/RAG-examples
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; no notebook was opened

## GitHub Snapshot

- Description: Retrieval Augmented Generation Examples - Original, GPT based, Semantic Search based.
- Language: Jupyter Notebook
- License (SPDX): MIT
- Default Branch: main
- Stars: 65
- Pushed At: 2024-02-01T16:20:02Z
- Topics: faiss, langchain, ml, nlp-machine-learning, rag

## Evidence Anchors
- [github_repo] description :: Retrieval Augmented Generation Examples - Original, GPT based, Semantic Search based. (confidence 0.95)
- [github_repo] language :: Jupyter Notebook (confidence 0.90)
- [github_repo] license :: MIT (confidence 0.90)
- [github_repo] topics :: faiss, langchain, ml, nlp-machine-learning, rag (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 16 paths at HEAD (confidence 0.95)
