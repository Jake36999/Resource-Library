---
uuid: "7b382a64-4a22-56bc-9523-d45341a21a10"
canonical_url: "https://github.com/CadQuery/cadquery"
repo_key: "CadQuery/cadquery"
owner: "CadQuery"
repo_name: "cadquery"
aliases: ["CadQuery/cadquery", "https://github.com/CadQuery/cadquery"]
type: "cad_tool"
primary_topic: "CAD & SaaS Design"
secondary_topics: ["Scientific Simulation & Math", "Architecture & Developer Playbooks"]
ecosystem: "CAD_Modeling"
domain_primary: "Design"
maturity_stage: "Production_Ready"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Python_SDK"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["CAD Workflow", "Parametric Modeling"]
glossary_terms: ["CAD", "Parametric Modeling", "Boundary Representation"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-05"
evidence_count: 5
github_description: "A python parametric CAD scripting framework based on OCCT"
github_language: "Python"
github_license_spdx: "NOASSERTION"
github_default_branch: "master"
github_stars: 5671
github_topics: ["3d", "brep", "cad", "cadquery", "dxf", "modeling", "occt", "opencascade", "parametric", "python", "step", "stl"]
github_homepage: "https://cadquery.org"
github_pushed_at: "2026-09-04T18:30:09Z"
---
# CadQuery - cadquery

## Bottom Line
Parametric B-rep modelling as an ordinary Python library — a fluent selector API over the OpenCascade kernel that produces real STEP solids, not meshes.

## What It Solves
- Script precise CAD geometry from Python without leaving the scientific-Python toolchain.
- Export true B-rep STEP files that downstream CAM and CAE tools accept.
- Select faces and edges by rule so models survive dimension changes.

## Architecture & Mechanics
- A fluent API chains workplane operations, keeping a stack of the geometry produced so far.
- Selector strings pick faces, edges and vertices declaratively instead of by index.
- OCCT performs the underlying boundary-representation operations.
- Results export to STEP, STL, DXF or SVG, and render in Jupyter via viewer add-ons.

## What Is Inside
- **The library** — `cadquery/` (39 files), with the OpenCascade binding isolated in `cadquery/occ_impl/` (21 files) and extension points in `cadquery/plugins/` and `cadquery/contrib/`.
- **Thirty numbered worked examples** — `examples/Ex001_Simple_Block.py` through the series, plus `examples/CQ_examples.ipynb` collecting them as a notebook. This is the fastest way into the API and is why the repository is worth opening even if you do not adopt it.
- **A reStructuredText manual** — `doc/` (75 files, 21 `.rst`), including `doc/examples.rst`, an import/export section with rendered SVG showing each option's effect (`doc/_static/importexport/`), and a custom Sphinx extension in `doc/ext/`.
- **Real CAD test fixtures** — `tests/testdata/`: `.dxf` drawings (`gear.dxf`, `MC 12x31.dxf`, `1001.dxf`), an `OpenSans-Regular.ttf` for text-on-solid tests.
- **Packaging you can copy** — `conda/` recipes, an Apptainer build workflow, `images/dockerfile`, and CI across GitHub Actions, AppVeyor and Azure Pipelines.

## Transferable Capability
**Wrap a powerful, awkward engine in a fluent interface that composes, so the common case is short and the engine stays reachable.** The value is the selection language — naming parts of a thing by their properties rather than by index — which is what makes a script survive a change to the model it operates on. The separable practice: **a numbered sequence of worked examples building from trivial to complete**, which teaches an API faster than reference documentation.

**Alternative to:** using a capable engine's own interface directly, where correct code is verbose enough that nobody writes it twice; and to positional references, which break silently when the thing changes. **Applies wherever** a capable but hostile engine needs a usable face.

## Taxonomy
- Ecosystem: CAD_Modeling
- Domain Primary: Design
- Maturity Stage: Production_Ready
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Python_SDK
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Generate part families programmatically inside a Python data or simulation pipeline.
- Produce manufacturing-grade STEP output from code under test.
- Study fluent-API design applied to geometry construction.

## Semantic Links
- [parent_topic:: [[Topic - CAD & SaaS Design]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[FreeCAD - FreeCAD]]]
- [related_to:: [[openscad - openscad]]]
- [implements_pattern:: [[Pattern - CAD Workflow]]]
- [implements_pattern:: [[Pattern - Parametric Modeling]]]
- [mentions_term:: [[Glossary - CAD]]]
- [mentions_term:: [[Glossary - Parametric Modeling]]]
- [mentions_term:: [[Glossary - Boundary Representation]]]

## Evidence
- Source URL: https://github.com/CadQuery/cadquery
- Source kind: GitHub REST metadata plus maintainer documentation
- Ingestion mode: agent-curated note authored against live repository metadata
- Metadata captured: 2026-08-31
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names Apache-2.0 (reproduced in full). The GitHub API reported `NOASSERTION`, which is why this was read directly.

## GitHub Snapshot

- Description: A python parametric CAD scripting framework based on OCCT
- Language: Python
- License (SPDX): NOASSERTION
- Default Branch: master
- Stars: 5671
- Homepage: https://cadquery.org
- Pushed At: 2026-08-31T19:05:44Z
- Topics: 3d, brep, cad, cadquery, dxf, modeling, occt, opencascade, parametric, python, step, stl

## Evidence Anchors
- [github_repo] description :: A python parametric CAD scripting framework based on OCCT (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: NOASSERTION (confidence 0.90)
- [github_repo] topics :: 3d, brep, cad, cadquery, dxf, modeling, occt, opencascade, parametric, python, step, stl (confidence 0.85)
