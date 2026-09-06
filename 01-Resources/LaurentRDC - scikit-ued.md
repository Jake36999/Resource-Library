---
uuid: "0027eda8-157c-5558-af1c-8f5d973a0295"
canonical_url: "https://github.com/LaurentRDC/scikit-ued"
repo_key: "LaurentRDC/scikit-ued"
owner: "LaurentRDC"
repo_name: "scikit-ued"
aliases: ["LaurentRDC/scikit-ued", "https://github.com/LaurentRDC/scikit-ued"]
type: "scientific_library"
primary_topic: "Scientific Simulation & Math"
secondary_topics: ["Data APIs & Big Data", "Geospatial & Earth Data"]
ecosystem: "Python"
domain_primary: "Scientific_Computation"
maturity_stage: "Production_Ready"
license_class: "Copyleft"
deployment_target: "Local_Only"
interface_protocol: "Python_SDK"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Scientific Simulation", "Symbolic Computation"]
glossary_terms: ["Simulation", "Symbolic Mathematics", "Astronomy", "Active Learning"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "GPL-3.0"
source_file: "repositories to chart.md"
evidence_count: 6
github_description: "Collection of algorithms and routines for (ultrafast) electron diffraction and scattering"
github_language: "Python"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "master"
github_stars: 0
github_topics: ["diffraction", "electron-microscopy", "python", "science", "scikit", "ultrafast-electron"]
github_homepage: "http://scikit-ued.readthedocs.io"
github_pushed_at: "2026-07-19T01:34:12Z"
github_updated_at: "2026-08-13T10:00:35Z"
---

# LaurentRDC - scikit-ued

## Bottom Line
A Python toolkit for ultrafast electron diffraction and scattering, automating the processing steps between raw diffraction images and interpretable structural dynamics.

## What It Solves
- Remove baselines from powder diffraction data, a routinely tedious step.
- Process and visualise diffraction images without hand-written per-experiment code.
- Give ultrafast structural-dynamics researchers a tested shared toolkit.

## Architecture & Mechanics
- Baseline removal uses dual-tree complex wavelet transforms rather than simple fitting.
- Diffraction pattern analysis routines handle the standard processing chain.
- Crystal structure utilities come via the companion `crystals` package.
- Interactive visualisation supports inspecting diffraction images during analysis; tested across Python 3.7+.

## What Is Inside
- **A domain library split by method** — `skued/`: `image/` (19 files, alignment, symmetry detection, powder centring), `simulation/` (13, including electrostatic potential computed from `aspherical.yaml` atomic parameters), `baseline/` (12, dual-tree complex wavelet baseline removal), `time_series/` (12, fitting and selection), `io/` (12, readers for diffraction formats).
- **Nineteen tutorials with their data checked in** — `docs/tutorials/` ships real diffraction images (`Cr_1.tif`, `Cr_2.tif`, `ab_initio_monolayer_mos2.tif`) beside the `.rst` that walks through them, so every tutorial is reproducible with no download step.
- **Test data as `.npz` and `.npy` arrays** — 6 and 2 respectively, beside 40 test files organised per subpackage (`skued/baseline/tests/test_dtcwt.py` and similar).
- **A command-line entry point** — documented at `docs/cmdline.rst`.
- **Why it is worth opening beyond its field:** the baseline-removal implementation and the tutorial-with-bundled-data convention both transfer to any signal-processing work.

## Transferable Capability
**Separate the correction of an instrument's artefacts from the analysis of its signal.** Raw measurement carries the shape of the measuring apparatus as well as the thing measured; removing that systematically, as its own step, means the analysis afterwards can be simple and the correction can be checked independently. The separable practice: **ship the tutorial's data with the tutorial**, so every documented procedure is reproducible with no external fetch.

**Alternative to:** correction folded into analysis, where the two cannot be validated apart. **Applies wherever** an observation carries the signature of how it was taken.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Scientific_Computation
- Maturity Stage: Production_Ready
- License Class: Copyleft
- Deployment Target: Local_Only
- Interface Protocol: Python_SDK
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Process ultrafast electron diffraction data reproducibly.
- Apply wavelet-based baseline removal to noisy powder diffraction.
- Study a narrow, well-tested scientific package serving one experimental technique.

## Semantic Links
- [parent_topic:: [[Topic - Scientific Simulation & Math]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[simbody]]]
- [related_to:: [[astropy]]]
- [related_to:: [[sympy]]]
- [implements_pattern:: [[Pattern - Scientific Simulation]]]
- [implements_pattern:: [[Pattern - Symbolic Computation]]]
- [mentions_term:: [[Glossary - Simulation]]]
- [mentions_term:: [[Glossary - Symbolic Mathematics]]]
- [mentions_term:: [[Glossary - Astronomy]]]
- [mentions_term:: [[Glossary - Active Learning]]]

## Evidence
- Source URL: https://github.com/LaurentRDC/scikit-ued
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names GPL-3.0 (reproduced in full). The GitHub API reported `UNKNOWN`, which is why this was read directly.

## GitHub Snapshot

- Description: Collection of algorithms and routines for (ultrafast) electron diffraction and scattering
- Language: Python
- License: Unknown (UNKNOWN)
- Default Branch: master
- Stars: 0
- Watchers: 0
- Homepage: http://scikit-ued.readthedocs.io
- Archived: no
- Disabled: no
- Pushed At: 2026-07-19T01:34:12Z
- Updated At: 2026-08-13T10:00:35Z
- Topics: diffraction, electron-microscopy, python, science, scikit, ultrafast-electron

## Evidence Anchors
- [github_repo] description :: Collection of algorithms and routines for (ultrafast) electron diffraction and scattering (confidence 0.95)
- [github_repo] topics :: diffraction, electron-microscopy, python, science, scikit, ultrafast-electron (confidence 0.82)
- [github_repo] language :: Python (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
