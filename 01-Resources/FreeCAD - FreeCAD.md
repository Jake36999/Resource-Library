---
uuid: "c5c821cb-6460-5007-b431-0f4cc960a023"
canonical_url: "https://github.com/FreeCAD/FreeCAD"
repo_key: "FreeCAD/FreeCAD"
owner: "FreeCAD"
repo_name: "FreeCAD"
aliases: ["FreeCAD/FreeCAD", "https://github.com/FreeCAD/FreeCAD"]
type: "cad_tool"
primary_topic: "CAD & SaaS Design"
secondary_topics: ["Scientific Simulation & Math"]
ecosystem: "CAD_Modeling"
domain_primary: "Design"
maturity_stage: "Production_Ready"
license_class: "Weak_Copyleft"
deployment_target: "Desktop"
interface_protocol: "GUI"
data_locality: "Local_First"
hardware_footprint: "High_Memory"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["CAD Workflow", "Parametric Modeling", "Scientific Simulation"]
glossary_terms: ["CAD", "Parametric Modeling", "Boundary Representation", "Product Design"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "LGPL-2.1"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-05"
evidence_count: 4
github_description: "Official source code of FreeCAD, a free and opensource multiplatform 3D parametric modeler."
github_language: "C++"
github_license_spdx: "LGPL-2.1"
github_default_branch: "main"
github_stars: 33171
github_topics: ["3d", "3d-printing", "architecture", "bim", "cad", "cam", "civil-engineering", "coin", "engineering", "fem", "freecad", "linux", "macos", "mechanical-engineering", "opencascade", "windows"]
github_homepage: "https://www.freecad.org"
github_pushed_at: "2026-09-04T23:16:18Z"
---
# FreeCAD - FreeCAD

## Bottom Line
A full parametric 3D modeller built on OpenCascade, organised into swappable workbenches covering mechanical part design, FEM, CAM, BIM and more.

## What It Solves
- Model mechanical parts parametrically without a commercial CAD licence.
- Keep design intent editable — change a driving dimension and downstream features rebuild.
- Move between modelling, simulation and manufacturing prep inside one file format.

## Architecture & Mechanics
- A document holds a dependency graph of parametric features rather than static geometry.
- OpenCascade provides the boundary-representation kernel for solids and surfaces.
- Workbenches are modular UIs over the same document model, each adding domain tools.
- Everything exposed to the GUI is scriptable from Python, so models can be generated programmatically.

## What Is Inside
- **13,288 files, and the shape matters more than the size** — `src/Mod/` alone is 8,972 files: FreeCAD is a set of workbenches (BIM, FEM, Part, Path, Sketcher, Material…) over a common kernel, so the interesting unit is a workbench directory rather than the application.
- **The kernel and GUI** — `src/App/` (298), `src/Base/` (231), `src/Gui/` (1,840, including 2,365 SVG icons across the tree).
- **Vendored third-party libraries with their own documentation** — `src/3rdParty/` (1,042 files), including `FastSignals` (with `docs/migration-from-boost-signals2.md`) and `libE57Format` with its own test data.
- **Example models and preset data** — `data/examples/` ships `.FCStd` documents (`ArchDetail`, `AssemblyExample`, `BIMExample`); `src/Mod/BIM/Presets/` carries `profiles.csv`, `pset_definitions.csv`, `qto_definitions.csv` — IFC property-set definitions usable independently of FreeCAD.
- **A large test estate** — 1,033 test-related paths, `tests/src/` (211) and `tests/visual/` (38) for visual regression, plus `src/Mod/BIM/bimtests/fixtures/`.
- **Material models as data** — `src/Mod/Material/Resources/Models/` holds renderer definitions (Appleseed, Carpaint, Cycles) as YAML.
- **Packaging for four platforms** — `package/WindowsInstaller/`, `rattler-build/`, `fedora/`, `ubuntu/`; `src/Base/Parameter.xsd` is the schema for its parameter store.

## Transferable Capability
**Record the intent behind a shape rather than the shape itself, and keep the history so intent can be revised.** A description built from operations and constraints answers *why is this dimension what it is*; a description built from surfaces cannot. The structural move worth taking on its own: **one self-contained workbench per discipline over a shared kernel**, so unrelated concerns do not have to agree about anything except the model underneath.

**Alternative to:** capturing the result of a decision instead of the decision, so revising it means starting again; and to a monolith where every discipline's features are core. **Applies wherever** an artefact is derived from parameters that will change.

## Taxonomy
- Ecosystem: CAD_Modeling
- Domain Primary: Design
- Maturity Stage: Production_Ready
- License Class: Weak_Copyleft
- Deployment Target: Desktop
- Interface Protocol: GUI
- Data Locality: Local_First
- Hardware Footprint: High_Memory
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Produce STEP/STL output for fabrication from a parametric source model.
- Script repeatable part families from Python rather than hand-modelling variants.
- Study a mature plugin architecture layered over a geometry kernel.

## Semantic Links
- [parent_topic:: [[Topic - CAD & SaaS Design]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[openscad - openscad]]]
- [related_to:: [[CadQuery - cadquery]]]
- [implements_pattern:: [[Pattern - CAD Workflow]]]
- [implements_pattern:: [[Pattern - Parametric Modeling]]]
- [implements_pattern:: [[Pattern - Scientific Simulation]]]
- [mentions_term:: [[Glossary - CAD]]]
- [mentions_term:: [[Glossary - Parametric Modeling]]]
- [mentions_term:: [[Glossary - Boundary Representation]]]
- [mentions_term:: [[Glossary - Product Design]]]

## Evidence
- Source URL: https://github.com/FreeCAD/FreeCAD
- Source kind: GitHub REST metadata plus maintainer documentation
- Ingestion mode: agent-curated note authored against live repository metadata
- Metadata captured: 2026-08-31

## GitHub Snapshot

- Description: Official source code of FreeCAD, a free and opensource multiplatform 3D parametric modeler.
- Language: C++
- License (SPDX): LGPL-2.1
- Default Branch: main
- Stars: 33171
- Homepage: https://www.freecad.org
- Pushed At: 2026-08-31T04:23:35Z
- Topics: 3d, 3d-printing, architecture, bim, cad, cam, civil-engineering, coin, engineering, fem, freecad, linux, macos, mechanical-engineering, opencascade, windows

## Evidence Anchors
- [github_repo] description :: Official source code of FreeCAD, a free and opensource multiplatform 3D parametric modeler. (confidence 0.95)
- [github_repo] language :: C++ (confidence 0.90)
- [github_repo] license :: LGPL-2.1 (confidence 0.90)
- [github_repo] topics :: 3d, 3d-printing, architecture, bim, cad, cam, civil-engineering, coin, engineering, fem, freecad, linux, macos, mechanical-engineering, opencascade, windows (confidence 0.85)
