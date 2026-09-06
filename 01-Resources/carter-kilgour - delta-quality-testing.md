---
uuid: "368b4668-9f4d-5c84-8dcc-7eca4f661e1c"
canonical_url: "https://github.com/carter-kilgour/delta-quality-testing"
repo_key: "carter-kilgour/delta-quality-testing"
owner: "carter-kilgour"
repo_name: "delta-quality-testing"
aliases: ["carter-kilgour/delta-quality-testing", "https://github.com/carter-kilgour/delta-quality-testing"]
type: "reference_implementation"
primary_topic: "Data Lineage & Provenance"
secondary_topics: ["Data APIs & Big Data"]
ecosystem: "Data_Platform"
domain_primary: "Data_Lineage"
maturity_stage: "Reference"
license_class: "Unknown"
deployment_target: "Server"
interface_protocol: "Python_SDK"
data_locality: "Distributed"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Medallion Layering", "Reference Architecture"]
glossary_terms: ["Medallion Architecture", "Data Engineering", "Dataset"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Unknown"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 5
github_description: "Lighting Talk Data & AI Summit Europe 2020 - Data Quality Testing in the Medallion Architecture"
github_language: "Python"
github_license_spdx: "NOASSERTION"
github_default_branch: "master"
github_stars: 9
github_pushed_at: "2020-12-04T07:12:25Z"
---
# carter-kilgour - delta-quality-testing

## Bottom Line
A sixteen-file demonstration of running data-quality tests as a pipeline job inside a medallion architecture, so that a quality check is a scheduled step with a result rather than a notebook someone remembers to run.

## What It Solves
- Make a quality check a first-class pipeline job instead of an ad-hoc script.
- Place the check at the layer boundary where the data has been cleaned but not yet aggregated.
- Keep the test suite in the same repository and the same test runner as the pipeline code.

## Architecture & Mechanics
- The split is the whole idea: `pipelines/jobs/run_quality_tests.py` is the *job* that runs checks in production, and `tests/silver/weather/temperatures_test.py` is the *check* itself, written as an ordinary pytest test with a `conftest.py`.
- The test tree mirrors the medallion layer it guards — `tests/silver/` — so a check's position in the architecture is expressed by where its file lives.
- `main.py` and `simpleExecute.py` sit at the root as two entry points, alongside `setup.py` and `requirements.txt`; the repository is packaged, not just a folder of scripts.
- **Not read:** any Python file. The job-versus-check separation above is inferred from paths and filenames.

## What Is Inside
- **The job/check split** — `pipelines/jobs/run_quality_tests.py` and `pipelines/utils/`, against `tests/silver/weather/temperatures_test.py` and `tests/conftest.py`. Four files carry the entire argument.
- **`PresentationSlides.pdf`** — the Data & AI Summit Europe 2020 lightning talk this repository accompanies. The reasoning is in the slides, not in the code; a reader who skips the PDF gets the mechanism without the case for it.
- **A packaged Python project** — `setup.py`, `requirements.txt`, two root entry points, and a `.vscode/` configuration.
- **Not here:** any data. The weather example is a shape, not a dataset.

## Transferable Capability
**Express a quality gate as an ordinary test, and schedule the test suite as a production job.** The value is that one artefact serves two audiences without being written twice: the same file a developer runs locally is the thing that runs nightly and fails the pipeline. Encoding the gate's *position* in the directory path — which stage's output it guards — means the architecture is legible from `ls` rather than from documentation that drifts.

**Alternative to:** a bespoke rules engine with its own DSL and its own runner, which cannot be executed from a developer's machine; and to assertions buried inside transformation code, which cannot be listed, counted or reported on. **Applies wherever** a correctness condition must hold in production and be checkable in development — schema contracts, invariants at a service boundary, generated-artefact validity.

## Taxonomy
- Ecosystem: Data_Platform
- Domain Primary: Data_Lineage
- Maturity Stage: Reference
- License Class: Unknown
- Deployment Target: Server
- Interface Protocol: Python_SDK
- Data Locality: Distributed
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Adopt the job-runs-the-test-suite pattern for a pipeline whose checks currently live inside transformation code.
- Read the slides for the argument, then the four files for the mechanism; in that order.
- Compare against the heavier declarative approach in [[dbt-labs - dbt-core]] when deciding whether a quality DSL earns its keep.

## Reading Notes
**No licence file and none reported by GitHub**, so it is excluded from every licence-constrained answer. Last pushed 2020-12-04 and unchanged since; the Delta and Databricks APIs it targets have moved considerably, so treat the code as an illustration of the arrangement rather than something to run. The reasoning lives in `PresentationSlides.pdf`, which was not opened.

## Semantic Links
- [parent_topic:: [[Topic - Data Lineage & Provenance]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[dbt-labs - dbt-core]]]
- [related_to:: [[Victor-Kipruto-Rop - medallion-lakehouse-platform]]]
- [related_to:: [[DataWithBaraa - databricks_bootcamp_2026]]]
- [related_to:: [[corzosoft - azure-edm-reference-data-platform]]]
- [implements_pattern:: [[Pattern - Medallion Layering]]]
- [implements_pattern:: [[Pattern - Reference Architecture]]]
- [mentions_term:: [[Glossary - Medallion Architecture]]]
- [mentions_term:: [[Glossary - Data Engineering]]]
- [mentions_term:: [[Glossary - Dataset]]]

## Evidence
- Source URL: https://github.com/carter-kilgour/delta-quality-testing
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; no Python file or the slide deck was opened, and no licence file exists to read

## GitHub Snapshot

- Description: Lighting Talk Data & AI Summit Europe 2020 - Data Quality Testing in the Medallion Architecture
- Language: Python
- License (SPDX): NOASSERTION
- Default Branch: master
- Stars: 9
- Pushed At: 2020-12-04T07:12:25Z

## Evidence Anchors
- [github_repo] description :: Lighting Talk Data & AI Summit Europe 2020 - Data Quality Testing in the Medallion Architecture (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: NOASSERTION (confidence 0.90)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 16 paths at HEAD (confidence 0.95)
