---
uuid: "9151da86-c86a-5160-a5ee-505634af0d02"
canonical_url: "https://github.com/stephanie-wang/lineage-stash-artifact"
repo_key: "stephanie-wang/lineage-stash-artifact"
owner: "stephanie-wang"
repo_name: "lineage-stash-artifact"
aliases: ["stephanie-wang/lineage-stash-artifact", "https://github.com/stephanie-wang/lineage-stash-artifact"]
type: "research_artifact"
primary_topic: "Data Lineage & Provenance"
secondary_topics: ["Infrastructure & Observability"]
ecosystem: "Python"
domain_primary: "Data_Lineage"
maturity_stage: "Reference"
license_class: "Unknown"
deployment_target: "Server"
interface_protocol: "CLI"
data_locality: "Distributed"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Run Provenance Capture"]
glossary_terms: ["Provenance", "Data Lineage", "Causal Logging"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Unknown"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 5
github_description: "Scripts for plotting and example data"
github_language: "Python"
github_license_spdx: "NOASSERTION"
github_default_branch: "master"
github_stars: 1
github_pushed_at: "2022-02-11T03:55:35Z"
---
# stephanie-wang - lineage-stash-artifact

## Bottom Line
The measurement artefact behind the Lineage Stash work: recorded latency data and plotting scripts comparing recovery in a distributed system that logs causal lineage against one that checkpoints, across deterministic and non-deterministic workloads and varying failure counts.

## What It Solves
- Show what recovery actually costs, in latency, rather than arguing about it from first principles.
- Separate the cost of *recording* lineage from the cost of *using* it after a failure.
- Give a comparison harness that spans three unrelated workload shapes rather than one favourable benchmark.

## Architecture & Mechanics
- The repository is data and plotting, not a system: `data/` holds recorded runs, and the scripts turn them into the figures.
- Three workload families are measured separately — `data/streaming` (17 files), `data/allreduce` (10) and `data/microbenchmark` (10) — which is what lets a reader see whether a result holds across shapes or only in one.
- Filenames carry the experimental variables: `deterministic-latency-64-workers.png`, `nondeterministic-8-failures-latency-64-workers.png`, `uncommitted-lineage-64-workers.csv`. Determinism, worker count and failure count are all varied.
- Two workload drivers are included in-tree rather than referenced: `flink-wordcount/` (Java, 16 files) and `mpi-bench/` (16 files).
- **Not read:** any script or result file. The experimental design above is inferred from filenames and directory structure.

## What Is Inside
- **Recorded latency measurements** — `data/microbenchmark/`, `data/streaming/`, `data/allreduce/`: CSVs of raw latency at 4 and 64 workers, tarballs of full runs, and 20 rendered PNGs. The comparison of *deterministic* against *non-deterministic* execution, and of 1 against 8 failures, is present as separate recorded runs.
- **`uncommitted-lineage-64-workers.csv`** — the size of the lineage not yet durable, which is the quantity the whole approach trades against.
- **Two workload drivers** — `flink-wordcount/src` (6 Java files, a Maven `pom.xml`, and `.template` config) and `mpi-bench/` with 13 shell scripts.
- **213 MB in a 71-file repository**, almost all of it recorded data. This is an evidence archive, not a library.
- **Not here:** the Lineage Stash implementation itself. This repository holds what was measured, not what was measured.

## Transferable Capability
**Publish the measurements, the workload drivers and the plotting code together, so a claim about performance can be re-derived rather than believed.** The design worth copying is the factorial layout: each varied condition — determinism, scale, failure count — is a separate recorded run with the condition in its filename, so the reader can check whether a result survives a change of workload instead of taking one headline number. The underlying technique is equally portable: **keep a record of what caused what, so that after a failure only the affected work is redone**, trading a small steady cost during normal operation against a large one during recovery.

**Alternative to:** periodic checkpointing, which pays nothing while running and re-does everything after a fault; and to publishing a paper with a chart and no data behind it. **Applies wherever** a recovery or reproducibility claim needs to be defensible — and wherever a benchmark needs to be believed by someone who did not run it.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Data_Lineage
- Maturity Stage: Reference
- License Class: Unknown
- Deployment Target: Server
- Interface Protocol: CLI
- Data Locality: Distributed
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Copy the factorial directory-and-filename layout for any benchmark whose result depends on more than one condition.
- Study the deterministic-versus-non-deterministic figures when choosing between causal logging and checkpointing for a stateful pipeline.
- Use the Flink and MPI drivers as ready-made workloads for a recovery experiment of your own.

## Reading Notes
Two things to be honest about. There is **no licence file and GitHub reports no licence**, so nothing here may be assumed reusable — it is readable, not takeable, and it is filtered out of every licence-constrained answer for that reason. And the name is a trap for retrieval: *lineage* here means causal dependency between computations for fault recovery, which is a different sense from the *data lineage* of column-level provenance elsewhere in this topic. Both senses are real and they are not interchangeable.

## Semantic Links
- [parent_topic:: [[Topic - Data Lineage & Provenance]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[apache - airflow]]]
- [related_to:: [[recipy - recipy]]]
- [implements_pattern:: [[Pattern - Run Provenance Capture]]]
- [mentions_term:: [[Glossary - Provenance]]]
- [mentions_term:: [[Glossary - Data Lineage]]]
- [mentions_term:: [[Glossary - Causal Logging]]]

## Evidence
- Source URL: https://github.com/stephanie-wang/lineage-stash-artifact
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; no data, script or result file was opened, and no licence file exists to read

## GitHub Snapshot

- Description: Scripts for plotting and example data
- Language: Python
- License (SPDX): NOASSERTION
- Default Branch: master
- Stars: 1
- Pushed At: 2022-02-11T03:55:35Z

## Evidence Anchors
- [github_repo] description :: Scripts for plotting and example data (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: NOASSERTION (confidence 0.90)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 71 paths at HEAD (confidence 0.95)
