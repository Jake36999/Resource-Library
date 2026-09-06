---
uuid: "9769f38d-af0b-5789-8094-a4fe8379a15e"
canonical_url: "https://github.com/guillaumegenthial/sequence_tagging"
repo_key: "guillaumegenthial/sequence_tagging"
owner: "guillaumegenthial"
repo_name: "sequence_tagging"
aliases: ["guillaumegenthial/sequence_tagging", "https://github.com/guillaumegenthial/sequence_tagging"]
type: "ml_framework"
primary_topic: "ML Training & MLOps"
secondary_topics: ["Code Intelligence & Structural Parsing"]
ecosystem: "Python"
domain_primary: "ML_Training"
maturity_stage: "Reference"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Python_SDK"
data_locality: "Local_First"
hardware_footprint: "Low_VRAM"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Zero-Shot Entity Extraction", "Model Inference Pipeline"]
glossary_terms: ["Named Entity Recognition", "Annotated Example", "Embedding"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: "Named Entity Recognition (LSTM + CRF) - Tensorflow"
github_language: "Python"
github_license_spdx: "Apache-2.0"
github_default_branch: "master"
github_stars: 1952
github_topics: ["bi-lstm", "characters-embeddings", "conditional-random-fields", "crf", "glove", "named-entity-recognition", "ner", "state-of-art", "tensorflow"]
github_homepage: "https://guillaumegenthial.github.io/sequence-tagging-with-tensorflow.html"
github_pushed_at: "2020-10-16T09:18:22Z"
---
# guillaumegenthial - sequence_tagging

## Bottom Line
A fifteen-file reference implementation of the bidirectional-LSTM-with-CRF entity recogniser — the architecture that defined the task for half a decade — kept small enough that the whole method is legible in one sitting.

## What It Solves
- Understand why sequence labelling needs a structured output layer rather than independent per-token decisions.
- See character-level and word-level representations combined in one model.
- Read a complete NER training pipeline that is not buried in a framework.

## Architecture & Mechanics
- The CRF layer is the whole point: tagging each token independently produces impossible sequences, so the model scores the *sequence* and decodes the best consistent path. That constraint-satisfaction step is what the architecture contributes.
- Two representations are combined — characters, which handle words never seen in training, and GloVe word vectors, which carry meaning. Neither alone is sufficient, and the combination is the second contribution.
- The pipeline is four scripts, in order: `build_data.py`, `train.py`, `evaluate.py`, and a `makefile` that runs them. Nine Python files in total, with `model/` holding six.
- **Not read:** any Python file. The architecture is the well-documented one the repository names; the code was not opened.

## What Is Inside
- **A complete pipeline in four scripts** — `build_data.py`, `train.py`, `evaluate.py`, `makefile`, plus `model/` (6 files).
- **`data/test.txt`** — a small tagged sample, enough to run the pipeline end to end without obtaining CoNLL.
- **Fifteen paths in total, 56 kB.** 1,952 stars, which is a comment on the value of a readable reference implementation rather than on the volume of code.
- **Not here:** the training corpus, the GloVe vectors, and any packaging. All three are downloads the makefile arranges.

## Transferable Capability
**When outputs are dependent, score the whole sequence rather than each element independently.** Independent per-position decisions can produce combinations that are individually plausible and jointly impossible; adding a layer that scores transitions and decodes the best consistent path fixes it structurally rather than by post-hoc cleanup. That shape recurs far outside language — anywhere a prediction is a sequence of related decisions rather than a set of unrelated ones. The second idea is **combining representations that fail differently**: character-level handles the unseen, word-level handles the known, and the combination covers both gaps.

**Alternative to:** independent per-token classification followed by rule-based repair, which is simpler and pushes the structure into brittle post-processing. **Applies wherever** a structured output must be internally consistent — segmentation, alignment, parsing, state sequences, any labelling with grammar-like constraints.

## Taxonomy
- Ecosystem: Python
- Domain Primary: ML_Training
- Maturity Stage: Reference
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Python_SDK
- Data Locality: Local_First
- Hardware Footprint: Low_VRAM
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Read it to understand why a structured output layer is needed before adopting a transformer tagger that includes one implicitly.
- Take the character-plus-word representation idea into any task with out-of-vocabulary inputs.
- Use it as the historical baseline against [[urchade - GLiNER]], which reaches the same task with no task-specific training at all.

## Reading Notes
**TensorFlow 1.x, last pushed 2020-10-16.** It will not run on a current TensorFlow, and it should not be adopted — transformer taggers and zero-shot extractors have superseded it comprehensively on accuracy and on setup cost. It is catalogued as a **reference**: 1,952 stars for fifteen files means it was how a great many people learned the architecture, and the reason a CRF layer exists is a durable piece of knowledge that its successors assume rather than explain.

## Semantic Links
- [parent_topic:: [[Topic - ML Training & MLOps]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[urchade - GLiNER]]]
- [related_to:: [[NorskRegnesentral - skweak]]]
- [related_to:: [[msgi - nlp-journey]]]
- [related_to:: [[hamelsmu - code_search]]]
- [implements_pattern:: [[Pattern - Zero-Shot Entity Extraction]]]
- [implements_pattern:: [[Pattern - Model Inference Pipeline]]]
- [mentions_term:: [[Glossary - Named Entity Recognition]]]
- [mentions_term:: [[Glossary - Annotated Example]]]
- [mentions_term:: [[Glossary - Embedding]]]

## Evidence
- Source URL: https://github.com/guillaumegenthial/sequence_tagging
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata, the complete file tree at HEAD, and the LICENSE.txt file; no Python file was opened

## GitHub Snapshot

- Description: Named Entity Recognition (LSTM + CRF) - Tensorflow
- Language: Python
- License (SPDX): Apache-2.0
- Default Branch: master
- Stars: 1952
- Homepage: https://guillaumegenthial.github.io/sequence-tagging-with-tensorflow.html
- Pushed At: 2020-10-16T09:18:22Z
- Topics: bi-lstm, characters-embeddings, conditional-random-fields, crf, glove, named-entity-recognition, ner, state-of-art, tensorflow

## Evidence Anchors
- [github_repo] description :: Named Entity Recognition (LSTM + CRF) - Tensorflow (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: Apache-2.0 (confidence 0.90)
- [github_repo] topics :: bi-lstm, characters-embeddings, conditional-random-fields, crf, glove, named-entity-recognition, ner, state-of-art, tensorflow (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 15 paths at HEAD (confidence 0.95)
