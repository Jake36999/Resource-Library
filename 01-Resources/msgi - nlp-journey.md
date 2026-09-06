---
uuid: "dedbd067-a438-5916-b4b5-62133c89dcab"
canonical_url: "https://github.com/msgi/nlp-journey"
repo_key: "msgi/nlp-journey"
owner: "msgi"
repo_name: "nlp-journey"
aliases: ["msgi/nlp-journey", "https://github.com/msgi/nlp-journey"]
type: "curated_list"
primary_topic: "ML Training & MLOps"
secondary_topics: ["Curated Aggregators & Reference Lists", "Agentic AI & Models"]
ecosystem: "Markdown"
domain_primary: "ML_Training"
maturity_stage: "Active"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Markdown"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Curated Resource Curation"]
glossary_terms: ["Reference List", "LLM", "Named Entity Recognition", "Embedding"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: "Documents, papers and codes related to  Natural Language Processing, including Topic Model, Word Embedding, Named Entity Recognition, Text Classificatin, Text Generation, Text Similarity, Machine Translation)，etc. "
github_language: "Python"
github_license_spdx: "Apache-2.0"
github_default_branch: "master"
github_stars: 1629
github_topics: ["deep-learning", "paper"]
github_homepage: "https://github.com/msgi/nlp-journey"
github_pushed_at: "2026-02-11T17:42:41Z"
---
# msgi - nlp-journey

## Bottom Line
A long-running NLP reading list that has been rewritten rather than extended as the field changed — the classical-NLP survey it began as in 2019 has largely given way to from-scratch implementations of transformer components.

## What It Solves
- See what a practitioner's view of the field kept and discarded across seven years.
- Read minimal implementations of the components inside a transformer.
- Get a curated entry point that is not padded to look comprehensive.

## Architecture & Mechanics
- The repository is small — fourteen files — for 1,629 stars, because it has been *pruned*. A list that removes entries is making an editorial claim; one that only appends is making none.
- What remains as code is `llm-tutorial/`: `activations/activations.py` and `normalizations/layer_norm.py` — the small pieces inside a transformer block, implemented individually rather than described.
- `llm-chat/` (8 files) is the applied half.
- The description in GitHub metadata still lists the 2019 topics — topic models, word embeddings, text similarity, machine translation — while the tree holds transformer internals, so the metadata and the contents disagree by several years.
- **Not read:** the README or any Python file. The above is read from the tree, the file names and the mismatch with the stated description.

## What Is Inside
- **From-scratch transformer components** — `llm-tutorial/activations/activations.py`, `llm-tutorial/normalizations/layer_norm.py`, with `llm-tutorial/README.md`. Small, specific, and the parts most explanations skip past.
- **`llm-chat/`** — 8 files, the applied side.
- **Fourteen paths, 157 kB**, last pushed 2026-02-11.
- **Not here:** the classical NLP material the GitHub description still advertises. It was removed rather than archived, so the list's own history is not recoverable from the tree.

## Transferable Capability
**A curated list earns its value by what it removes.** Appending is free and produces a list nobody can use; deleting is an editorial judgement and is the entire service being offered. The visible consequence here is a repository that shrank while its audience grew. The accompanying practice — **implementing the small components individually rather than explaining them** — is how a reading list stays honest about what its author actually understands.

The failure to copy is equally instructive: **the description was not updated when the contents were replaced**, so the metadata advertises a list that no longer exists. For anything discovered through search, the description *is* the artefact most readers see, and letting it drift from the contents makes the collection unfindable by its real subject and misleading on its advertised one.

**Alternative to:** an exhaustive awesome-list, which is complete and undiscriminating. **Applies wherever** a collection is maintained over years and the temptation is to add rather than to choose.

## Taxonomy
- Ecosystem: Markdown
- Domain Primary: ML_Training
- Maturity Stage: Active
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Markdown
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Read `llm-tutorial/` for minimal implementations of activation and normalisation layers.
- Use it as an example of pruning as curation when designing a reference collection meant to last.
- Note the description drift as a concrete cost of not maintaining metadata alongside content.

## Reading Notes
Two mismatches to know about. **The GitHub description is years out of date** — it lists topic models, word embeddings and machine translation, none of which are in the tree — so a search that finds this by its description will find something else. And **much of the content is in Chinese**, including the description itself, which the English topic tags do not signal. Actively maintained (last pushed 2026-02-11).

## Semantic Links
- [parent_topic:: [[Topic - ML Training & MLOps]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[fighting41love - funNLP]]]
- [related_to:: [[guillaumegenthial - sequence_tagging]]]
- [related_to:: [[soulbliss - NLP-conference-compendium]]]
- [related_to:: [[armanakbari - Awsome-Efficient-DLMs]]]
- [implements_pattern:: [[Pattern - Curated Resource Curation]]]
- [mentions_term:: [[Glossary - Reference List]]]
- [mentions_term:: [[Glossary - LLM]]]
- [mentions_term:: [[Glossary - Named Entity Recognition]]]
- [mentions_term:: [[Glossary - Embedding]]]

## Evidence
- Source URL: https://github.com/msgi/nlp-journey
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata, the complete file tree at HEAD, and the LICENSE file; no README or Python file was opened

## GitHub Snapshot

- Description: Documents, papers and codes related to  Natural Language Processing, including Topic Model, Word Embedding, Named Entity Recognition, Text Classificatin, Text Generation, Text Similarity, Machine Translation)，etc. 
- Language: Python
- License (SPDX): Apache-2.0
- Default Branch: master
- Stars: 1629
- Homepage: https://github.com/msgi/nlp-journey
- Pushed At: 2026-02-11T17:42:41Z
- Topics: deep-learning, paper

## Evidence Anchors
- [github_repo] description :: Documents, papers and codes related to  Natural Language Processing, including Topic Model, Word Embedding, Named Entity Recognition, Text Classificatin, Text Generation, Text Similarity, Machine Translation)，etc.  (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: Apache-2.0 (confidence 0.90)
- [github_repo] topics :: deep-learning, paper (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 14 paths at HEAD (confidence 0.95)
