---
uuid: "c5c14b6a-ed98-5cb9-bcf5-b3131e2c873a"
canonical_url: "https://github.com/snorkel-team/snorkel"
repo_key: "snorkel-team/snorkel"
owner: "snorkel-team"
repo_name: "snorkel"
aliases: ["snorkel-team/snorkel", "https://github.com/snorkel-team/snorkel"]
type: "ml_framework"
primary_topic: "ML Training & MLOps"
secondary_topics: ["Agentic AI & Models"]
ecosystem: "Python"
domain_primary: "ML_Training"
maturity_stage: "Production_Ready"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Python_SDK"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Programmatic Labelling"]
glossary_terms: ["Weak Supervision", "Labelling Function", "Active Learning"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-03"
evidence_count: 5
github_description: "A system for quickly generating training data with weak supervision"
github_language: "Python"
github_license_spdx: "Apache-2.0"
github_default_branch: "main"
github_stars: 6005
github_topics: ["ai", "data-augmentation", "data-science", "data-slicing", "labeling", "machine-learning", "python", "snorkel", "training-data", "weak-supervision"]
github_homepage: "https://snorkel.org"
github_pushed_at: "2026-06-08T19:59:20Z"
---
# snorkel-team - snorkel

## Bottom Line
Estimates how accurate each of your noisy labelling functions is **without any ground truth** — from the inverse generalized covariance of their agreement structure — and uses those estimates to combine their votes into probabilistic training labels.

## What It Solves
- Produce a training set from heuristics, patterns and existing models instead of an annotation budget.
- Survive a changed label definition: labelling functions are code, so they are edited and re-run rather than re-annotated.
- Measure whether a set of heuristics is any good — coverage, overlap, conflict and empirical accuracy — before trusting it.

## Architecture & Mechanics
- `@labeling_function` decorated callables vote a class or abstain; appliers run them over pandas, Dask or Spark.
- `LabelModel` learns `P(LF | Y)` by building the junction tree of the LF dependency graph and completing its inverse generalized covariance matrix against the empirical statistics (Ratner et al., AAAI 2019); conditional independence given `Y` is the default assumption.
- `augmentation/` adds transformation functions and sampling policies for data augmentation.
- `slicing/` — the least-known subsystem — makes a named subset of the data a first-class object with a slice-aware classifier and a monitor, so per-slice performance is tracked rather than checked ad hoc.

## What Is Inside
- **Four subsystems, not one** — `snorkel/labeling/` (the `@labeling_function` decorator,
  appliers with pandas/Dask/Spark backends, `analysis.py` for coverage/overlap/conflict, and
  `model/label_model.py`); `snorkel/augmentation/` (transformation functions and sampling
  policies); `snorkel/slicing/` (slicing functions, a slice-aware classifier, `monitor.py`);
  `snorkel/classification/` (multi-task classifier, trainer, checkpointer, schedulers).
- **The mechanism, written down** — the `LabelModel` class docstring names the method and cites
  Ratner et al., AAAI 2019.
- **Synthetic data generation** — `snorkel/synthetic/synthetic_data.py`, for testing the label
  model against known ground truth.
- **Not here:** the tutorials. Those are `snorkel-team/snorkel-tutorials`.

## Transferable Capability
**Estimate how much to trust each of several unreliable judges without ever seeing a correct answer**, by reading the structure of their agreement and disagreement. Judges that agree with the emerging consensus more often are weighted up; the pattern of conflict carries the information. The premise underneath is that **judgements should be written as programs rather than recorded as decisions**, so they can be reviewed, versioned and re-run when the definition changes — a set of hand-made decisions cannot survive a changed definition, and code can.

A separable third idea: **name the subsets you care about and track performance on each**, so quality is measured where it matters rather than only in aggregate.

**Alternative to:** a single authoritative judge; to hand-tuned weights, which nothing can tell you are wrong; and to one overall quality number that hides the case you care about. **Applies wherever** several imperfect signals must be combined and no ground truth exists to calibrate them against — including any ranking assembled from hand-weighted components.

## Taxonomy
- Ecosystem: Python
- Domain Primary: ML_Training
- Maturity Stage: Production_Ready
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Python_SDK
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Bootstrap a classifier in a domain where labels do not exist.
- Reconcile several imperfect classifiers into one calibrated output.
- Borrow the slicing idea: name the subsets that matter and monitor each one separately.

## Reading Notes
Read the maturity carefully. 6,005 stars and heavy citation, but the README's own top section announces that the team moved to **Snorkel Flow**, a commercial platform, and the newest entry in `CHANGELOG.md` is 0.10.0 (2023-02-27) whose only breaking change was adopting Python 3.11 and dropping every other version. Stable, influential and effectively finished — not abandoned, but not advancing either.

## Semantic Links
- [parent_topic:: [[Topic - ML Training & MLOps]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[NorskRegnesentral - skweak]]]
- [related_to:: [[urchade - GLiNER]]]
- [related_to:: [[open-metadata - OpenMetadata]]]
- [implements_pattern:: [[Pattern - Programmatic Labelling]]]
- [mentions_term:: [[Glossary - Weak Supervision]]]
- [mentions_term:: [[Glossary - Labelling Function]]]
- [mentions_term:: [[Glossary - Active Learning]]]

## Evidence
- Source URL: https://github.com/snorkel-team/snorkel
- Source kind: GitHub REST metadata plus the repository tree and files, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-03
- Depth of read: recorded per source in [[Scouting Working File 2026-09-03]]

## GitHub Snapshot

- Description: A system for quickly generating training data with weak supervision
- Language: Python
- License (SPDX): Apache-2.0
- Default Branch: main
- Stars: 6005
- Homepage: https://snorkel.org
- Pushed At: 2026-06-08T19:59:20Z
- Topics: ai, data-augmentation, data-science, data-slicing, labeling, machine-learning, python, snorkel, training-data, weak-supervision

## Evidence Anchors
- [github_repo] description :: A system for quickly generating training data with weak supervision (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: Apache-2.0 (confidence 0.90)
- [github_repo] topics :: ai, data-augmentation, data-science, data-slicing, labeling, machine-learning, python, snorkel, training-data, weak-supervision (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-03 (confidence 0.95)
