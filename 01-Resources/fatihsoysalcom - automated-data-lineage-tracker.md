---
uuid: "445ca50c-ddfd-554f-8fe4-fc2c66c6ff72"
canonical_url: "https://github.com/fatihsoysalcom/automated-data-lineage-tracker"
repo_key: "fatihsoysalcom/automated-data-lineage-tracker"
owner: "fatihsoysalcom"
repo_name: "automated-data-lineage-tracker"
aliases: ["fatihsoysalcom/automated-data-lineage-tracker", "https://github.com/fatihsoysalcom/automated-data-lineage-tracker"]
type: "reference_implementation"
primary_topic: "Data Lineage & Provenance"
secondary_topics: ["Data APIs & Big Data"]
ecosystem: "Python"
domain_primary: "Data_Lineage"
maturity_stage: "Reference"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Python_SDK"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Run Provenance Capture", "Schema Mapping"]
glossary_terms: ["Data Lineage", "Column-Level Lineage", "Provenance"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 5
github_description: "This example demonstrates how to implement automated data lineage tracking within a Python ETL pipeline. It captures metadata, dataset dependencies, and column-level transformations dynamically during execution, outputting both a visual ASCII lineage map and a structured JSON lineage manifest."
github_language: "Python"
github_license_spdx: "MIT"
github_default_branch: "main"
github_stars: 0
github_pushed_at: "2026-07-04T06:09:58Z"
---
# fatihsoysalcom - automated-data-lineage-tracker

## Bottom Line
A single Python module that records dataset dependencies and column-level transformations while an ETL job is running, and emits both an ASCII lineage map for a human and a JSON lineage manifest for a machine.

## What It Solves
- Know which columns a derived field was computed from, without standing up a metadata platform to find out.
- Capture lineage at the moment a transformation executes rather than reconstructing it afterwards from SQL text.
- Produce a lineage record small enough to commit next to the pipeline it describes.

## Architecture & Mechanics
- The whole implementation is one file, `lineage_tracker.py`, in a repository of three files. There is no package, no service and no storage layer.
- Lineage is captured *dynamically during execution* — the repository's own framing — which places it opposite the static-parse approach taken by SQL lineage parsers such as [[shenhuan2021 - gudu-sql-omni-introduce]].
- Two outputs are produced from the same capture: an ASCII map, which is read by a person, and a structured JSON manifest, which is read by something else.
- **Not read:** the module's source. The mechanics above are taken from the repository's own description and the file tree, not from the code.

## What Is Inside
- **The entire implementation** — `lineage_tracker.py`, one file. The repository holds three paths in total: `LICENSE`, `README.md` and that module.
- **No tests, no examples directory, no packaging.** 5 kB, published 2026-07-04 and unchanged since.
- **Not here:** any integration with a runner, catalogue or warehouse. It is the capture idea in isolation.

## Transferable Capability
**Record what produced a value at the moment it is produced, rather than inferring it later from the text of the instructions.** Runtime capture sees what a static reader cannot — the branch actually taken, the column actually populated, the input actually read — and it costs nothing to obtain because the process is already running. The dual output is the second transferable part: the same capture serves a person browsing an ASCII tree and a machine consuming a manifest, without either being a lossy rendering of the other.

**Alternative to:** parsing the transformation text to work out what depends on what, which is correct only for the paths the parser understands, and to a full metadata platform, which is the same idea with a server, a schema registry and an operational burden. **Applies wherever** a derivation must be explained after the fact — a build, a report, a model's training inputs, a document assembled from sources.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Data_Lineage
- Maturity Stage: Reference
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Python_SDK
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Read it as the minimum viable shape of a lineage record before adopting something larger.
- Lift the manifest structure into a pipeline that has no lineage capture and cannot justify a platform.
- Compare runtime capture against static SQL parsing when deciding how a pipeline should be made explicable.

## Reading Notes
Zero stars, three files, one commit day. Judged as a project it is negligible; judged as an *exhibit* it is the clearest statement of the runtime-capture position in the catalogue, precisely because nothing else is in the way. Treat it as a sketch to read, not a dependency to take. Nothing here has been executed and the module body was not opened, so the claim that capture is dynamic rests on the author's description alone.

## Semantic Links
- [parent_topic:: [[Topic - Data Lineage & Provenance]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[shenhuan2021 - gudu-sql-omni-introduce]]]
- [related_to:: [[recipy - recipy]]]
- [related_to:: [[corzosoft - azure-edm-reference-data-platform]]]
- [implements_pattern:: [[Pattern - Run Provenance Capture]]]
- [mentions_term:: [[Glossary - Data Lineage]]]
- [mentions_term:: [[Glossary - Column-Level Lineage]]]
- [mentions_term:: [[Glossary - Provenance]]]

## Evidence
- Source URL: https://github.com/fatihsoysalcom/automated-data-lineage-tracker
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata, the complete file tree at HEAD, and the LICENSE file; no source file was opened

## GitHub Snapshot

- Description: This example demonstrates how to implement automated data lineage tracking within a Python ETL pipeline. It captures metadata, dataset dependencies, and column-level transformations dynamically during execution, outputting both a visual ASCII lineage map and a structured JSON lineage manifest.
- Language: Python
- License (SPDX): MIT
- Default Branch: main
- Stars: 0
- Pushed At: 2026-07-04T06:09:58Z

## Evidence Anchors
- [github_repo] description :: This example demonstrates how to implement automated data lineage tracking within a Python ETL pipeline. It captures metadata, dataset dependencies, and column-level transformations dynamically during execution, outputting both a visual ASCII lineage map and a structured JSON lineage manifest. (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: MIT (confidence 0.90)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 3 paths at HEAD (confidence 0.95)
