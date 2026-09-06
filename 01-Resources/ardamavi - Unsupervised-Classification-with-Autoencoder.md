---
uuid: "89bfc4fc-7daa-5f29-a88f-b72fe54a9931"
canonical_url: "https://github.com/ardamavi/Unsupervised-Classification-with-Autoencoder"
repo_key: "ardamavi/Unsupervised-Classification-with-Autoencoder"
owner: "ardamavi"
repo_name: "Unsupervised-Classification-with-Autoencoder"
aliases: ["ardamavi/Unsupervised-Classification-with-Autoencoder", "https://github.com/ardamavi/Unsupervised-Classification-with-Autoencoder"]
type: "tutorial"
primary_topic: "ML Training & MLOps"
secondary_topics: []
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
patterns: ["Model Inference Pipeline", "Programmatic Labelling"]
glossary_terms: ["Embedding", "Annotated Example", "Dataset"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: "Using Autoencoders for classification as unsupervised machine learning algorithms with Deep Learning."
github_language: "Jupyter Notebook"
github_license_spdx: "Apache-2.0"
github_default_branch: "master"
github_stars: 48
github_topics: ["autoencoder", "deep-learning", "machine-learning"]
github_pushed_at: "2018-08-02T06:43:18Z"
---
# ardamavi - Unsupervised-Classification-with-Autoencoder

## Bottom Line
Two notebooks demonstrating classification without labels by training an autoencoder to reconstruct its input and then clustering in the compressed representation it was forced to learn — shipped with 1,399 images so it runs immediately.

## What It Solves
- Group data into classes when no labels exist and none can be obtained.
- Obtain a useful representation from a task that supervises itself.
- Run the demonstration without sourcing a dataset first.

## Architecture & Mechanics
- The move is indirect and that is the lesson: reconstruction is not the goal. Forcing data through a narrow bottleneck and demanding it come back out makes the bottleneck learn what actually distinguishes the inputs, and clustering happens there.
- Two notebooks are present, one general (`Unsupervised Classification With Autoencoder.ipynb`) and one applied to the bundled dataset (`Examples/Dog-Cat/`), so the method and an instance of it are separate.
- `Examples/Dog-Cat/Data/get_dataset.py` accompanies the committed images, so the corpus can be rebuilt as well as read.
- **Not read:** either notebook. The method is the standard one the title names; the code was not opened.

## What Is Inside
- **1,399 committed JPEGs** — `Examples/Dog-Cat/Data/Train_Data/`: **97% of this repository is training images**, which is a deliberate choice that makes the demonstration runnable on checkout, and which makes the file count meaningless as a measure of code.
- **Two notebooks** — the method, and the method applied.
- **`Examples/Dog-Cat/Data/get_dataset.py`** — the corpus rebuild path.
- **Not here:** a library, a CLI or any evaluation. Four files at the root and 1,401 under `Examples/`.

## Transferable Capability
**Invent a task whose supervision is free, and keep the representation it forces rather than its output.** Reconstruction supervises itself — the input is the target — so any unlabelled corpus becomes trainable, and the bottleneck ends up holding the distinctions that mattered. This is the same manoeuvre as training a summariser to obtain a search embedding: **the artefact you want is the intermediate, not the output.** Bundling the data is a second, smaller lesson about tutorials: a demonstration that requires a download first is one most readers never see run.

**Alternative to:** labelling a sample and training a supervised classifier, which is better when labels are obtainable; and to clustering raw inputs, which fails on high-dimensional data because distance stops meaning anything. **Applies wherever** a corpus must be organised and nobody has said what the categories are — log clustering, document grouping, anomaly detection, deduplication.

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
- Read it as the compact statement of self-supervised representation learning before reaching for a pretrained encoder.
- Apply the bottleneck-then-cluster approach to an unlabelled corpus that needs organising.
- Compare with [[hamelsmu - code_search]], which uses the same keep-the-representation manoeuvre with a different proxy task.

## Reading Notes
Last pushed 2018-08-02, Keras-era, and 48 stars — this is a teaching artefact, not a technique to adopt as it stands; modern self-supervised methods (contrastive and masked-prediction approaches) produce substantially better representations. Note the shape before cloning: **32 MB and 1,405 files, of which 1,399 are cat and dog photographs.** Bundling them makes the notebook immediately runnable and makes every file-count statistic about this repository misleading.

## Semantic Links
- [parent_topic:: [[Topic - ML Training & MLOps]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[hamelsmu - code_search]]]
- [related_to:: [[JackieZhangdx - WeakSupervisedSegmentationList]]]
- [related_to:: [[knodle - knodle]]]
- [implements_pattern:: [[Pattern - Model Inference Pipeline]]]
- [implements_pattern:: [[Pattern - Programmatic Labelling]]]
- [mentions_term:: [[Glossary - Embedding]]]
- [mentions_term:: [[Glossary - Annotated Example]]]
- [mentions_term:: [[Glossary - Dataset]]]

## Evidence
- Source URL: https://github.com/ardamavi/Unsupervised-Classification-with-Autoencoder
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata, the complete file tree at HEAD, and the LICENSE file; neither notebook was opened

## GitHub Snapshot

- Description: Using Autoencoders for classification as unsupervised machine learning algorithms with Deep Learning.
- Language: Jupyter Notebook
- License (SPDX): Apache-2.0
- Default Branch: master
- Stars: 48
- Pushed At: 2018-08-02T06:43:18Z
- Topics: autoencoder, deep-learning, machine-learning

## Evidence Anchors
- [github_repo] description :: Using Autoencoders for classification as unsupervised machine learning algorithms with Deep Learning. (confidence 0.95)
- [github_repo] language :: Jupyter Notebook (confidence 0.90)
- [github_repo] license :: Apache-2.0 (confidence 0.90)
- [github_repo] topics :: autoencoder, deep-learning, machine-learning (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 1405 paths at HEAD (confidence 0.95)
