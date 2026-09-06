---
uuid: "468200fa-c8cb-52b9-adef-bab39845a087"
canonical_url: "https://github.com/recipy/recipy"
repo_key: "recipy/recipy"
owner: "recipy"
repo_name: "recipy"
aliases: ["recipy/recipy", "https://github.com/recipy/recipy"]
type: "developer_tool"
primary_topic: "Data Lineage & Provenance"
secondary_topics: ["Data APIs & Big Data", "Scientific Simulation & Math"]
ecosystem: "Python"
domain_primary: "Data"
maturity_stage: "Abandoned"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Python_SDK"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Run Provenance Capture"]
glossary_terms: ["Provenance", "Data Lineage", "Dataset"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-03"
evidence_count: 5
github_description: "Effortless method to record provenance in Python"
github_language: "Python"
github_license_spdx: "Apache-2.0"
github_default_branch: "master"
github_stars: 435
github_topics: ["database", "provenance", "python", "recipy", "reproducible-research", "science"]
github_homepage: "https://recipy.readthedocs.io"
github_pushed_at: "2022-01-12T23:24:38Z"
---
# recipy - recipy

## Bottom Line
`import recipy` as the first line of a script, and every file it reads or writes is logged with the code version, arguments and environment — provenance captured by patching libraries through `sys.meta_path`, so nothing has to be declared.

## What It Solves
- Not knowing which script, inputs or commit produced a result file six months later.
- Provenance for people who work in scripts and will never adopt a workflow engine.
- Finding a file's history after it has been renamed, because search is by content hash, not path.

## Architecture & Mechanics
- A patch object is installed into `sys.meta_path`, so when a target library is imported recipy wraps its reading and writing functions before user code receives it — which is why `import recipy` must be the first line.
- `docs/patched_modules.rst` names the targets function by function: pandas, numpy, `matplotlib.pyplot.savefig`, lxml, bs4, GDAL, sklearn svmlight, nibabel across eight image formats, tifffile, imageio.
- Runs are stored in TinyDB, a pure-Python JSON store chosen to remove the MongoDB requirement earlier versions had; a CLI offers `search`, `latest`, `annotate` and `diff`, with a bundled web GUI.
- Built-in `open()` is deliberately **not** patched — libraries use it internally, so wrapping it would log everything the whole stack touched; `recipy.open` is the opt-in.

## What Is Inside
- **The patching machinery** — `recipy/`: `PatchImporter.py`, `PatchSimple.py`,
  `PatchMultipleWrappers.py`, `PatchScientific.py`, `PatchBaseScientific.py`,
  `PatchFileOpenLike.py`, `PatchWarnings.py`, `log.py`.
- **The explanation** — `docs/how_does_it_work.rst` sets out the `sys.meta_path` interception
  clearly enough to reimplement from; `docs/creating_patches.rst` is a guide to adding one;
  `docs/patched_modules.rst` lists every wrapped function per library; `docs/databaseSchema.rst`
  documents the run record.
- **An integration test suite over real file formats** — `integration_test/packages/data/`
  carries sample files for GDAL (tiff), nibabel (eight neuroimaging formats), iris (netCDF),
  lxml, bs4, imageio.
- **A Jupyter magic** — `TestRecipyMagic.ipynb`.

## Transferable Capability
**Capture where something came from at the moment it is produced, by intercepting the act of writing rather than by asking the author to declare it.** Provenance that must be remembered is not recorded; provenance captured at the boundary is. The second idea is separable and arguably larger: **identify artefacts by their content rather than their location**, so the record survives renaming, copying, and being sent to someone else.

**Alternative to:** documentation of how a result was produced, written afterwards by the person least motivated to write it; and to path-based identity, which breaks the moment a file moves. **Applies wherever** outputs outlive the memory of how they were made — analysis, generated documents, model artefacts, or a catalogue that wants to know which pass produced a given note.

*The implementation is abandoned; the two ideas are not.*

## Taxonomy
- Ecosystem: Python
- Domain Primary: Data
- Maturity Stage: Abandoned
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Python_SDK
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Read it for the two ideas rather than the implementation: import-hook interception, and identity by content hash.
- Understand the boundary of run-level provenance before choosing it over lineage.
- Study `docs/how_does_it_work.rst` as a clear explanation of a `sys.meta_path` patch.

## Reading Notes
**Abandoned, unambiguously.** The newest `CHANGELOG.md` entry is v0.3.0 (2016-09-13); last push 2022-01-12; 90 open issues; CI is Travis and AppVeyor, both long dead as free services. The patched-module list is a 2016 snapshot that still names `pandas.Panel` and `to_msgpack`, both removed from pandas years ago, so those patches cannot bind. It also records only *that* a file was read and another written, never what happened between — no column-level lineage, no DAG, no transformation semantics. A good idea in an implementation that has stopped.

## Semantic Links
- [parent_topic:: [[Topic - Data Lineage & Provenance]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[open-metadata - OpenMetadata]]]
- [related_to:: [[HCAI-Lab-GT - capabilibara]]]
- [related_to:: [[asreview]]]
- [implements_pattern:: [[Pattern - Run Provenance Capture]]]
- [mentions_term:: [[Glossary - Provenance]]]
- [mentions_term:: [[Glossary - Data Lineage]]]
- [mentions_term:: [[Glossary - Dataset]]]

## Evidence
- Source URL: https://github.com/recipy/recipy
- Source kind: GitHub REST metadata plus the repository tree and files, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-03
- Depth of read: recorded per source in [[Scouting Working File 2026-09-03]]

## GitHub Snapshot

- Description: Effortless method to record provenance in Python
- Language: Python
- License (SPDX): Apache-2.0
- Default Branch: master
- Stars: 435
- Homepage: https://recipy.readthedocs.io
- Pushed At: 2022-01-12T23:24:38Z
- Topics: database, provenance, python, recipy, reproducible-research, science

## Evidence Anchors
- [github_repo] description :: Effortless method to record provenance in Python (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: Apache-2.0 (confidence 0.90)
- [github_repo] topics :: database, provenance, python, recipy, reproducible-research, science (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-03 (confidence 0.95)
