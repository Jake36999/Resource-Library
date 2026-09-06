---
uuid: "e483c113-b9f0-542d-91a1-8dab5b253b20"
canonical_url: "https://github.com/whole-tale/provenance-examples"
repo_key: "whole-tale/provenance-examples"
owner: "whole-tale"
repo_name: "provenance-examples"
aliases: ["whole-tale/provenance-examples", "https://github.com/whole-tale/provenance-examples"]
type: "dataset"
primary_topic: "Data Lineage & Provenance"
secondary_topics: ["Scientific Simulation & Math"]
ecosystem: "Mixed"
domain_primary: "Data_Lineage"
maturity_stage: "Reference"
license_class: "Unknown"
deployment_target: "Local_Only"
interface_protocol: "CLI"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Run Provenance Capture"]
glossary_terms: ["Provenance", "Research Compendium", "Dataset"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Unknown"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 5
github_description: "Constructed and real-world examples for evaluation of provenance capture methods"
github_language: "Dockerfile"
github_license_spdx: "NOASSERTION"
github_default_branch: "master"
github_stars: 0
github_pushed_at: "2020-03-18T20:41:29Z"
---
# whole-tale - provenance-examples

## Bottom Line
Six complete research compendia — four real published analyses and two constructed ones — assembled specifically as test material for evaluating whether a provenance-capture method actually captures what happened.

## What It Solves
- Evaluate a provenance tool against real analyses, not against a toy script written to make it look good.
- Have a known-answer corpus: constructed one-step and multi-step examples where the correct provenance graph is decided in advance.
- Reproduce someone else's analysis end to end, including its data and its environment.

## Architecture & Mechanics
- Each example is a self-contained directory under `examples/` carrying its own data, code, README and environment definition — the compendium form, where the analysis travels with everything it needs.
- The corpus is deliberately mixed: `onestep/` (10 files) and `multistep/` (10) are *constructed*, so expected provenance is known; the other four are real published work, so they carry real mess.
- Environments are pinned per example (`.yml` files, plus a repository-root `Dockerfile`), which is what makes re-execution rather than re-reading possible.
- R dominates (9 `.r`, 2 `.rmd`), reflecting where the source analyses came from; there are 2 Python files and one notebook.
- **Not read:** any example's code or README. The corpus design above is read off the directory structure and the repository's stated purpose.

## What Is Inside
- **Four real analyses** — `Density-Dependence-in-Annual-Plant-Species-in-the-San-Joaquin-Desert` (21 files, with field data: `phytometer_data_trials_2018.csv`, `plant locations.csv`), `trait-perception-accuracy` (14), `ajps` (9, political-science replication data: `newspapers_count.csv`, `precincts0711.csv`, `replication_file.csv`), `water-tale` (9, including a Jupyter notebook `wt_quickstart.ipynb`).
- **Two constructed controls** — `onestep/` and `multistep/`, 10 files each: the known-answer cases a provenance evaluation needs.
- **Seven real research CSVs** spanning ecology, political science and simulation output — usable as test data well beyond provenance work.
- **Six SVGs**, which given the purpose are most likely rendered provenance graphs.
- **Not here:** any provenance tool. This is the material tools are pointed at.

## Transferable Capability
**Build an evaluation corpus with both constructed cases and real ones, and keep them separate.** The constructed pair — one step and many steps — gives a known answer, so a failure is unambiguous; the real analyses supply the mess that a constructed case cannot fake. Neither half is sufficient: a tool that only passes the controls has been tested against its own assumptions, and a tool that only runs on real material produces output nobody can mark. The second transferable idea is the **compendium**: bundle data, code, environment and narrative in one directory so that re-running is possible rather than merely re-reading.

**Alternative to:** evaluating a capture tool on whatever the author had lying around, and to distributing an analysis as a paper plus a code link, where the environment that made it work is gone. **Applies wherever** something must be verified as *actually reproducible* — a build, a training run, a report, a claimed result.

## Taxonomy
- Ecosystem: Mixed
- Domain Primary: Data_Lineage
- Maturity Stage: Reference
- License Class: Unknown
- Deployment Target: Local_Only
- Interface Protocol: CLI
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Point a provenance or lineage capture tool at these six and compare what it reports against the constructed cases' known answers.
- Reuse the compendium directory layout for any analysis that must survive being handed to someone else.
- Take the seven research CSVs as small, real, messy test data for anything that ingests tabular material.

## Reading Notes
**No licence file and no licence reported by GitHub**, which matters more here than usual: the contents include third-party published research data (the AJPS replication files, the San Joaquin field data) whose own terms are not restated anywhere in the tree. Read it, do not redistribute from it, and check each example's provenance before reusing its data. Last pushed 2020-03-18; the Whole Tale project it belongs to has moved on, so treat this as a fixed corpus rather than a maintained one.

## Semantic Links
- [parent_topic:: [[Topic - Data Lineage & Provenance]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[recipy - recipy]]]
- [related_to:: [[asreview]]]
- [related_to:: [[stephanie-wang - lineage-stash-artifact]]]
- [implements_pattern:: [[Pattern - Run Provenance Capture]]]
- [mentions_term:: [[Glossary - Provenance]]]
- [mentions_term:: [[Glossary - Research Compendium]]]
- [mentions_term:: [[Glossary - Dataset]]]

## Evidence
- Source URL: https://github.com/whole-tale/provenance-examples
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; no example, data file or README was opened, and no licence file exists to read

## GitHub Snapshot

- Description: Constructed and real-world examples for evaluation of provenance capture methods
- Language: Dockerfile
- License (SPDX): NOASSERTION
- Default Branch: master
- Stars: 0
- Pushed At: 2020-03-18T20:41:29Z

## Evidence Anchors
- [github_repo] description :: Constructed and real-world examples for evaluation of provenance capture methods (confidence 0.95)
- [github_repo] language :: Dockerfile (confidence 0.90)
- [github_repo] license :: NOASSERTION (confidence 0.90)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 75 paths at HEAD (confidence 0.95)
