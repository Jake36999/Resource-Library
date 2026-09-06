---
uuid: "a249374f-517e-5897-8069-84c422b99fd6"
canonical_url: "https://github.com/urchade/GLiNER"
repo_key: "urchade/GLiNER"
owner: "urchade"
repo_name: "GLiNER"
aliases: ["urchade/GLiNER", "https://github.com/urchade/GLiNER"]
type: "ml_model"
primary_topic: "ML Training & MLOps"
secondary_topics: ["Agentic AI & Models", "Knowledge Management"]
ecosystem: "Python"
domain_primary: "ML_Training"
maturity_stage: "Production_Ready"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Python_SDK"
data_locality: "Local_First"
hardware_footprint: "Low_VRAM"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Zero-Shot Entity Extraction"]
glossary_terms: ["Zero-Shot Extraction", "Named Entity Recognition", "Inference"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-03"
evidence_count: 5
github_description: "Generalist and Lightweight Model for Named Entity Recognition (Extract any entity types from texts)"
github_language: "Python"
github_license_spdx: "Apache-2.0"
github_default_branch: "main"
github_stars: 3603
github_topics: ["information-extraction", "large-language-models", "named-entity-recognition", "natural-language-processing", "prompt-tuning"]
github_homepage: "https://urchade.github.io/GLiNER"
github_pushed_at: "2026-09-03T13:10:22Z"
---
# urchade - GLiNER

## Bottom Line
Pass the entity types you want as a list of strings at inference time and get tagged spans back — a small bidirectional encoder scoring every candidate span against every supplied label, competitive with far larger models and fast enough on a CPU.

## What It Solves
- Extract entity types that were never in any training set, without fine-tuning or labelled data.
- Change what is extracted by editing a list of strings rather than assembling a corpus.
- Run extraction at volume without a GPU budget or a per-document model API call.

## Architecture & Mechanics
- In the original span architecture, labels and text are concatenated through one encoder with a learned `[ENT]` token before each label; the `[ENT]` outputs become label embeddings after a two-layer feed-forward refinement.
- Every candidate span up to length 12 is represented from its first and last token; a span matches a label when the sigmoid of their dot product crosses a threshold, trained with binary cross-entropy. The model is a similarity between a span vector and a label vector.
- Nine variants trade off three axes: **bi-encoder** encodes labels separately so their embeddings can be precomputed — which is what makes 100+ types viable — token-level variants use BIO tagging for long entities, and decoder or `Relex` heads add open-vocabulary label generation or joint relation extraction.
- `multitask/` reuses the backbone for classification, open extraction, question answering, relation extraction and summarisation; INT8, `torch.compile`, ONNX export and Ray Serve are documented paths.

## What Is Inside
- **Nine architecture variants** — `gliner/modeling/` (`span_rep.py`, `encoder.py`, `decoder.py`,
  `cache.py`, `scorers.py`, `loss_functions.py`), documented variant by variant in
  `docs/architectures.md` with a comparison table.
- **Multitask heads over one backbone** — `gliner/multitask/`: `classification.py`,
  `open_extraction.py`, `question_answering.py`, `relation_extraction.py`, `summarization.py`.
- **Deployment paths** — `gliner/onnx/`, `gliner/serve/` with a `Containerfile`,
  `docs/convert_to_onnx.md`, INT8 and `torch.compile` documented.
- **A benchmark suite with recorded results** — `benchmarks/`: `bench_gliner_e2e.py`,
  `bench_int8.py`, `bench_streaming_modes.py`, `bench_batch_decode_results.json`, and a
  `dice_loss_study/` with ablation training and visualisation scripts.
- **Training configuration by architecture** — `configs/`: `config_span.yaml`,
  `config_token.yaml`, `config_biencoder.yaml`, `config_decoder.yaml`, `config_relex.yaml`,
  `config_streaming_span.yaml`.
- **Data preparation** — `data/process_nuner.py`, `data/process_pilener.py`.

## Transferable Capability
**Make the schema of what you are extracting an argument supplied at the moment of use, rather than a commitment made when the extractor was built.** The extractor compares candidate fragments against the descriptions it is given, so changing what you extract is editing a list of words rather than assembling examples and rebuilding. Because the descriptions can be prepared in advance and reused, many categories cost little more than a few.

**Alternative to:** an extractor fixed to the categories it was built for, where a new category means a new corpus and a new build; and to asking a large general model per item, where flexibility is paid for in cost and latency on every call. **Applies wherever** what you need to pull out of material changes faster than you can rebuild the thing that pulls it — and to any fixed-pattern extractor that has reached the limit of what patterns can express.

## Taxonomy
- Ecosystem: Python
- Domain Primary: ML_Training
- Maturity Stage: Production_Ready
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Python_SDK
- Data Locality: Local_First
- Hardware Footprint: Low_VRAM
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Pull structured facts out of documentation or transcripts against a schema you define per run.
- Build knowledge-graph triples in one pass with the joint relation-extraction head.
- Replace an LLM extraction call in a pipeline where cost or latency rules it out.

## Reading Notes
The most actively developed source in this cohort — pushed on the day of the pass, with a paper (arXiv 2311.08526), a documentation site, a recorded benchmark suite and an ONNX path. First use downloads weights from Hugging Face, so it is not offline until the model is cached.

## Semantic Links
- [parent_topic:: [[Topic - ML Training & MLOps]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[snorkel-team - snorkel]]]
- [related_to:: [[NorskRegnesentral - skweak]]]
- [related_to:: [[microsoft - graphrag]]]
- [implements_pattern:: [[Pattern - Zero-Shot Entity Extraction]]]
- [mentions_term:: [[Glossary - Zero-Shot Extraction]]]
- [mentions_term:: [[Glossary - Named Entity Recognition]]]
- [mentions_term:: [[Glossary - Inference]]]

## Evidence
- Source URL: https://github.com/urchade/GLiNER
- Source kind: GitHub REST metadata plus the repository tree and files, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-03
- Depth of read: recorded per source in [[Scouting Working File 2026-09-03]]

## GitHub Snapshot

- Description: Generalist and Lightweight Model for Named Entity Recognition (Extract any entity types from texts)
- Language: Python
- License (SPDX): Apache-2.0
- Default Branch: main
- Stars: 3603
- Homepage: https://urchade.github.io/GLiNER
- Pushed At: 2026-09-03T13:10:22Z
- Topics: information-extraction, large-language-models, named-entity-recognition, natural-language-processing, prompt-tuning

## Evidence Anchors
- [github_repo] description :: Generalist and Lightweight Model for Named Entity Recognition (Extract any entity types from texts) (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: Apache-2.0 (confidence 0.90)
- [github_repo] topics :: information-extraction, large-language-models, named-entity-recognition, natural-language-processing, prompt-tuning (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-03 (confidence 0.95)
