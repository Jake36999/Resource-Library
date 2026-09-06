---
uuid: "8a6ba114-ab2a-5df6-9054-4f190826b9a7"
canonical_url: "https://github.com/knodle/knodle"
repo_key: "knodle/knodle"
owner: "knodle"
repo_name: "knodle"
aliases: ["knodle/knodle", "https://github.com/knodle/knodle"]
type: "ml_framework"
primary_topic: "ML Training & MLOps"
secondary_topics: ["Knowledge Management"]
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
patterns: ["Programmatic Labelling", "Model Inference Pipeline"]
glossary_terms: ["Weak Supervision", "Labelling Function", "Annotated Example", "Training Data Attribution"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: "A PyTorch-based open-source framework that provides methods for improving the weakly annotated data and allows researchers to efficiently develop and compare their own methods. "
github_language: "Python"
github_license_spdx: "Apache-2.0"
github_default_branch: "develop"
github_stars: 108
github_topics: ["ai", "classification", "denoising-methods", "knodle", "machine-learning", "natural-language-procressing", "python", "pytorch", "relation-extraction", "snorkel", "weak-supervision", "weakly-supervised-learning"]
github_homepage: "http://knodle.cc"
github_pushed_at: "2024-09-10T13:53:28Z"
---
# knodle - knodle

## Bottom Line
A weak-supervision framework whose organising idea is a single data structure — rules, a rule-to-instance mapping, and a rule-to-class mapping — that every denoising method operates on, so competing methods become interchangeable rather than incomparable.

## What It Solves
- Compare weak-supervision denoising methods without reimplementing each one's data pipeline.
- Train on noisy, rule-derived labels while accounting for the noise rather than ignoring it.
- Separate the labelling rules from the model that learns despite them.

## Architecture & Mechanics
- Everything reduces to one representation, and the directory layout follows: `knodle/trainer/` (30 files) holds the methods, `knodle/transformation/` (7) converts between forms, `knodle/evaluation/` (6) scores, `knodle/model/` (5) is deliberately thin.
- Because every trainer consumes the same input structure, swapping one for another is a constructor change — which is what makes the comparison the framework exists for actually possible.
- The framework's boundary is the interesting design choice: models are somebody else's (PyTorch), rules are the user's, and this owns only the denoising in between.
- Tests mirror the package exactly — `tests/trainer` (11), `tests/transformation` (7), `tests/evaluation` (1), `tests/data` (2).
- **Not read:** any Python source. The structure above is read off directory names and file counts, and the data-structure claim from the project's stated purpose.

## What Is Inside
- **Four fully worked dataset preparations** — `examples/data_preprocessing/`: `MIMIC_III_dataset/`, `MIMIC_CXR_dataset/` (both clinical), `imdb_dataset/`, and `police_killing_dataset/`. **These are the most valuable part**: getting from a real dataset to weak-supervision inputs is the step that stops most attempts, and it is worked through four times on genuinely different data.
- **Two labelling strategies contrasted on one dataset** — `police_killing_dataset/data_preprocessing_with_regex.ipynb` against `preprocessing_with_kb.ipynb`: rules from patterns, rules from a knowledge base, same target.
- **A work-in-progress relation-extraction preparation** — `examples/data_preprocessing/tac_based_dataset/[WIP]_patterns_aka_lfs/`, marked as unfinished in its own directory name.
- **Eleven notebooks** across those preparations, plus `examples/trainer/` (15 files) demonstrating the methods.
- **A committed style guide** — `STYLE_GUIDE.md` alongside `.flake8` and `.pre-commit-config.yaml`.
- **Not here:** the datasets. MIMIC in particular requires credentialed access, so those notebooks describe a path you must be authorised to walk.

## Transferable Capability
**Fix one data structure that all competing methods must consume, and the methods become comparable.** The hard part of comparing approaches is rarely the algorithms; it is that each arrives with its own input format, its own preprocessing and its own assumptions, so any difference in results is unattributable. Defining the interchange first — here, rules plus two mappings — moves the cost once, up front, and pays it back on every subsequent comparison. **Keeping the framework's boundary narrow** is the second decision: owning only the denoising step, and deferring models and rules to others, is why the abstraction stayed small enough to be usable.

**Alternative to:** hand-labelling, which is accurate and does not scale; and to using noisy labels as if they were clean, which trains the model to reproduce the rules' mistakes. **Applies wherever** supervision is cheap and approximate and the errors are systematic rather than random — which includes automated tagging, classification from heuristics, and any labelling produced by a model.

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
- Read `examples/data_preprocessing/` before attempting weak supervision on a real dataset; it is the step most guides skip.
- Compare the regex and knowledge-base labelling notebooks on the police-killing dataset to see what the rule source changes.
- Take the fix-the-interchange-first approach into any comparison of methods that each bring their own pipeline.

## Reading Notes
Last pushed 2024-09-10 and 108 stars — an academic framework rather than a maintained product, and it sits in [[snorkel-team - snorkel]]'s shadow, which is the comparison a reader will want and which this repository does not make for you. The clinical examples (MIMIC-III, MIMIC-CXR) need credentialed data access, so two of the four preparations are unrunnable for most readers; they remain readable and are still the clearest part of the repository.

## Semantic Links
- [parent_topic:: [[Topic - ML Training & MLOps]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[snorkel-team - snorkel]]]
- [related_to:: [[NorskRegnesentral - skweak]]]
- [related_to:: [[urchade - GLiNER]]]
- [related_to:: [[JackieZhangdx - WeakSupervisedSegmentationList]]]
- [implements_pattern:: [[Pattern - Programmatic Labelling]]]
- [implements_pattern:: [[Pattern - Model Inference Pipeline]]]
- [mentions_term:: [[Glossary - Weak Supervision]]]
- [mentions_term:: [[Glossary - Labelling Function]]]
- [mentions_term:: [[Glossary - Annotated Example]]]
- [mentions_term:: [[Glossary - Training Data Attribution]]]

## Evidence
- Source URL: https://github.com/knodle/knodle
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata, the complete file tree at HEAD, and the LICENSE file; no Python source or notebook was opened

## GitHub Snapshot

- Description: A PyTorch-based open-source framework that provides methods for improving the weakly annotated data and allows researchers to efficiently develop and compare their own methods. 
- Language: Python
- License (SPDX): Apache-2.0
- Default Branch: develop
- Stars: 108
- Homepage: http://knodle.cc
- Pushed At: 2024-09-10T13:53:28Z
- Topics: ai, classification, denoising-methods, knodle, machine-learning, natural-language-procressing, python, pytorch, relation-extraction, snorkel, weak-supervision, weakly-supervised-learning

## Evidence Anchors
- [github_repo] description :: A PyTorch-based open-source framework that provides methods for improving the weakly annotated data and allows researchers to efficiently develop and compare their own methods.  (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: Apache-2.0 (confidence 0.90)
- [github_repo] topics :: ai, classification, denoising-methods, knodle, machine-learning, natural-language-procressing, python, pytorch, relation-extraction, snorkel, weak-supervision, weakly-supervised-learning (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 142 paths at HEAD (confidence 0.95)
