---
uuid: "1584736e-cbc6-51d6-9ce6-727e64badd1e"
canonical_url: "https://github.com/asreview/asreview"
repo_key: "asreview/asreview"
owner: "asreview"
repo_name: "asreview"
aliases: ["asreview/asreview", "https://github.com/asreview/asreview"]
type: "scientific_library"
primary_topic: "Scientific Simulation & Math"
secondary_topics: ["Data APIs & Big Data", "Geospatial & Earth Data"]
ecosystem: "Python"
domain_primary: "Scientific_Computation"
maturity_stage: "Production_Ready"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Python_SDK"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Scientific Simulation", "Symbolic Computation"]
glossary_terms: ["Active Learning", "Simulation", "Symbolic Mathematics", "Astronomy"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
evidence_count: 5
github_description: "Active learning for systematic reviews"
github_language: "Python"
github_license: "Apache License 2.0"
github_license_spdx: "Apache-2.0"
github_default_branch: "main"
github_stars: 1000
github_topics: ["active-learning", "asreview", "deep-learning", "language-model", "learning-algorithms", "literature", "llm", "natural-language-processing", "neural-network", "research", "systematic-literature-reviews", "systematic-reviews", "utrecht-university"]
github_homepage: "https://asreview.ai"
github_pushed_at: "2026-09-03T00:33:09Z"
github_updated_at: "2026-08-31T15:19:53Z"
---

# asreview

## Bottom Line
Machine-assisted screening for systematic reviews: the human labels records as relevant or not, and after each decision the model re-ranks every unlabelled record so the most likely relevant one is shown next.

## What It Solves
- Cut the effort of screening thousands of candidate papers to find the few that qualify.
- Reach the relevant records early, so screening can stop once returns diminish rather than after reading everything.
- Keep the human as the decision-maker while the machine handles prioritisation.

## Architecture & Mechanics
- Records are imported from CSV, RIS or XLSX, optionally seeded with known relevant and irrelevant examples.
- An active learning loop retrains on every human label and re-orders the unlabelled pool.
- The reviewer acts as the oracle: the model proposes, the human decides, and every decision is saved and editable.
- Performance monitoring indicates when further screening is unlikely to surface anything new, giving a defensible stopping point.

## What Is Inside
- **A screening tool where the web app is most of the code** — `asreview/webapp/` (292 of 336 package files, 154 `.js`), over a small Python core: `models/` (10), `data/` (8), `project/` (11), `state/`, `database/`, `simulation/`.
- **The part worth borrowing is the simulation harness** — `asreview/simulation/` plus `docs/source/lab/simulation_api_example.ipynb`: it replays a screening decision sequence against a labelled dataset so an active-learning strategy can be measured rather than asserted. That is a stopping-rule and evaluation design, transferable to any human-in-the-loop ranking problem.
- **Real bibliographic test data** — `tests/demo_data/` (37 files) including 17 `.ris` citation files and CSVs; `tests/asreview_files/` holds `.asreview` project archives, including deliberately invalid ones (`asreview-demo-project-invalid-classifier.asreview`) for round-trip testing.
- **A documented project file format** — `docs/source/technical/example_api_asreview_file.ipynb` walks through the `.asreview` archive structure.
- **Architecture drawn** — `docs/figures/architecture.png` and `ASReviewLAB_explanation.png`.
- **119 test paths** across core, webapp and database, with `docker-compose.yml` for integration tests.

## Transferable Capability
**Let a person judge, and let the machine decide only what to show them next.** The order of examination is the automated decision; the judgement stays human. The consequence is that the value is measured as *how much did not have to be examined* rather than as accuracy, which changes what you build. The separable and undervalued idea: **a replay harness that runs a decision strategy against an already-judged corpus**, so a change to the ordering can be measured rather than argued about, and the stopping rule becomes a testable question.

**Alternative to:** automating the judgement itself; and to changing a ranking on the basis of a plausible story about why it is better. **Applies wherever** a person must review many candidates and the ordering is where the leverage is.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Scientific_Computation
- Maturity Stage: Production_Ready
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Python_SDK
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Screen a large literature corpus with a fraction of the reading.
- Adopt the active-learning loop for any ranked review queue with a human in the loop and a limited budget.
- Study a defensible stopping rule for partial review of a corpus.

## Semantic Links
- [parent_topic:: [[Topic - Scientific Simulation & Math]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[simbody]]]
- [related_to:: [[astropy]]]
- [related_to:: [[sympy]]]
- [implements_pattern:: [[Pattern - Scientific Simulation]]]
- [implements_pattern:: [[Pattern - Symbolic Computation]]]
- [mentions_term:: [[Glossary - Active Learning]]]
- [mentions_term:: [[Glossary - Simulation]]]
- [mentions_term:: [[Glossary - Symbolic Mathematics]]]
- [mentions_term:: [[Glossary - Astronomy]]]

## Evidence
- Source URL: https://github.com/asreview/asreview
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01

## GitHub Snapshot

- Description: Active learning for systematic reviews
- Language: Python
- License: Apache License 2.0 (Apache-2.0)
- Default Branch: main
- Stars: 1000
- Watchers: 1000
- Homepage: https://asreview.ai
- Archived: no
- Disabled: no
- Pushed At: 2026-08-31T16:45:45Z
- Updated At: 2026-08-31T15:19:53Z
- Topics: active-learning, asreview, deep-learning, language-model, learning-algorithms, literature, llm, natural-language-processing, neural-network, research, systematic-literature-reviews, systematic-reviews, utrecht-university

## Evidence Anchors
- [github_repo] description :: Active learning for systematic reviews (confidence 0.95)
- [github_repo] topics :: active-learning, asreview, deep-learning, language-model, learning-algorithms, literature, llm, natural-language-processing, neural-network, research, systematic-literature-reviews, systematic-reviews (confidence 0.82)
- [github_repo] language :: Python (confidence 0.74)
- [github_repo] license :: Apache License 2.0 (Apache-2.0) (confidence 0.90)
