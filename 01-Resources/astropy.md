---
uuid: "73cf8fd6-1275-507b-96a9-33b68cf69d8c"
canonical_url: "https://github.com/astropy/astropy"
repo_key: "astropy/astropy"
owner: "astropy"
repo_name: "astropy"
aliases: ["astropy/astropy", "https://github.com/astropy/astropy"]
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
glossary_terms: ["Astronomy", "Simulation", "Symbolic Mathematics", "Active Learning"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "BSD-3-Clause"
source_file: "repositories to chart.md"
evidence_count: 6
github_description: "Astronomy and astrophysics core library"
github_language: "Python"
github_license: "Unknown"
github_license_spdx: "BSD-3-CLAUSE"
github_default_branch: "main"
github_stars: 0
github_topics: ["astronomy", "astrophysics", "astropy", "python", "science"]
github_homepage: "https://www.astropy.org"
github_pushed_at: "2026-09-04T15:16:40Z"
github_updated_at: "2026-08-31T13:00:03Z"
---

# astropy

## Bottom Line
The core Python library for astronomy, created to end fragmentation across the field's tooling by providing one shared implementation of coordinates, units, time and file formats that other packages can build on.

## What It Solves
- Stop every astronomy package reimplementing coordinate transforms, unit handling and FITS parsing.
- Make units and physical quantities first-class, so dimensional mistakes fail loudly rather than silently.
- Give the community peer-reviewed, standardised implementations of routine operations.

## Architecture & Mechanics
- Subpackages cover celestial coordinates, time scales, units and quantities, tables, and file I/O with FITS as the central format.
- Quantities carry units through arithmetic, so conversions and errors surface at the operation.
- Further subpackages handle photometry, spectra and cosmology calculations.
- It is community-driven and NumFOCUS-sponsored, with an affiliated-package ecosystem building on the core.

## What Is Inside
- **A subpackage-per-domain library** — `astropy/`: `io/` (361 files: FITS, VOTable, ASCII, HDF5 readers), `wcs/` (155, world coordinate systems), `coordinates/` (134), `cosmology/` (129), `utils/` (93), `units/` (70), `modeling/` (61), `timeseries/` (60). Each is usable on its own.
- **Vendored C libraries with their own licences** — `cextern/`: `wcslib` (58), `expat` (23), `cfitsio` (9), and a `licenses/` directory (14 files) tracking them. A worked example of vendoring done accountably.
- **Published XML Schemas for a data format** — `astropy/io/votable/data/VOTable.v1.1.xsd` through `v1.4.xsd`, four versions kept side by side.
- **Real astronomical test data** — 55 `.fits`, 52 `.hdr` and 43 `.dat` files across the test suites, plus coordinate-accuracy reference CSVs (`astropy/coordinates/tests/accuracy/data/fk4_no_e_fk5.csv` and siblings) that pin transformations against independently computed values.
- **426 documentation files** — including `docs/whatsnew/` (28 releases), `docs/changes/` (86 fragments), and `docs/development/` (21) which documents the project's own governance and review process.
- **760 test paths**, a CI benchmark workflow, and a `.pyinstaller/` directory that tests the packaged binary.
- **Governance in-tree** — `GOVERNANCE.md`, `CITATION`, `CITATION.cff`.

## Transferable Capability
**Build one coherent library out of independently useful parts, each usable without the others.** The value is in the boundaries: a coordinate system, a unit system, a file format reader and a modelling framework each stand alone, so adopting one costs nothing in the others. Two further practices: **vendor dependencies visibly, with their licences tracked beside them**, and **pin transformations against independently computed reference values**, so correctness is checked against something other than the implementation's own opinion.

**Alternative to:** a framework that must be adopted whole; and to a test suite that only checks the code agrees with itself. **Applies wherever** a domain has several separable concerns and correctness has an external reference.

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
- Handle astronomical coordinates and times without writing the conversions.
- Read and write FITS data in an analysis pipeline.
- Study unit-aware numerics as a way of catching a whole class of scientific bug.

## Semantic Links
- [parent_topic:: [[Topic - Scientific Simulation & Math]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[simbody]]]
- [related_to:: [[sympy]]]
- [related_to:: [[LaurentRDC - scikit-ued]]]
- [implements_pattern:: [[Pattern - Scientific Simulation]]]
- [implements_pattern:: [[Pattern - Symbolic Computation]]]
- [mentions_term:: [[Glossary - Astronomy]]]
- [mentions_term:: [[Glossary - Simulation]]]
- [mentions_term:: [[Glossary - Symbolic Mathematics]]]
- [mentions_term:: [[Glossary - Active Learning]]]

## Evidence
- Source URL: https://github.com/astropy/astropy
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names BSD-3-Clause (reproduced in full). The GitHub API reported `UNKNOWN`, which is why this was read directly.

## GitHub Snapshot

- Description: Astronomy and astrophysics core library
- Language: Python
- License: Unknown (UNKNOWN)
- Default Branch: main
- Stars: 0
- Watchers: 0
- Homepage: https://www.astropy.org
- Archived: no
- Disabled: no
- Pushed At: 2026-08-31T12:50:06Z
- Updated At: 2026-08-31T13:00:03Z
- Topics: astronomy, astrophysics, astropy, python, science

## Evidence Anchors
- [github_repo] description :: Astronomy and astrophysics core library (confidence 0.95)
- [github_repo] topics :: astronomy, astrophysics, astropy, python, science (confidence 0.82)
- [github_repo] language :: Python (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
