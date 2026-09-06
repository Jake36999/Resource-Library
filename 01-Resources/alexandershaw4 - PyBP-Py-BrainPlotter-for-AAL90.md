---
uuid: "2a0973de-3d8c-5317-9472-fc0bf49cdfba"
canonical_url: "https://github.com/alexandershaw4/PyBP-Py-BrainPlotter-for-AAL90"
repo_key: "alexandershaw4/PyBP-Py-BrainPlotter-for-AAL90"
owner: "alexandershaw4"
repo_name: "PyBP-Py-BrainPlotter-for-AAL90"
aliases: ["alexandershaw4/PyBP-Py-BrainPlotter-for-AAL90", "https://github.com/alexandershaw4/PyBP-Py-BrainPlotter-for-AAL90"]
type: "developer_tool"
primary_topic: "Scientific Simulation & Math"
secondary_topics: ["Geospatial & Earth Data"]
ecosystem: "Python"
domain_primary: "Scientific_Computation"
maturity_stage: "Reference"
license_class: "Unknown"
deployment_target: "Desktop"
interface_protocol: "GUI"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Scientific Simulation", "Spatial Indexing"]
glossary_terms: ["Simulation", "Dataset", "Coordinate Reference System"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Unknown"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: "Visualisation & processing of MEG data and networks on meshes. A bunch of functions, examples and a gui."
github_language: "Python"
github_license_spdx: "NOASSERTION"
github_default_branch: "master"
github_stars: 11
github_topics: ["alignment", "atlas", "brain-imaging", "data-visualization", "electroencephalography", "magnetoencephalography", "mesh-processing", "neuroimaging", "overlay", "visualization"]
github_pushed_at: "2019-10-11T09:01:00Z"
---
# alexandershaw4 - PyBP-Py-BrainPlotter-for-AAL90

## Bottom Line
A brain-network plotter that projects values measured at atlas regions onto a three-dimensional cortical mesh, solving the alignment between a coarse labelled parcellation and a fine geometric surface that do not share a coordinate system.

## What It Solves
- Display values defined on ninety labelled regions over a mesh of many thousands of vertices.
- Align an atlas and a mesh that were produced in different coordinate spaces.
- Overlay a network — edges between regions — on the same anatomy as the values.

## Architecture & Mechanics
- The alignment problem is the substance: the AAL90 atlas gives ninety labelled regions, the ICBM152 mesh gives a dense surface, and neither is defined in the other's space. Projection means deciding which mesh vertices belong to which region and how a region's value spreads across them.
- Two representations are handled separately — `OverlayData.txt` (per-region values, projected onto the surface) and `Network.edge` (relationships between regions, drawn as connections). Scalar and relational data need different treatment.
- `AALv.txt` is the atlas vertex list, and `BrainMesh_ICBM152_smoothed.gii` plus `NewSmoothed.gii` are the mesh — both committed, so the alignment can be inspected rather than trusted.
- `InflateGiftiMeshUsingPythonInMatlab.m` is a MATLAB bridge, and `New_PyBP.spec` is a PyInstaller specification — this was distributed as a desktop binary to people who would not install Python.
- **Not read:** any Python file. The above is inferred from filenames, formats and the repository's stated purpose.

## What Is Inside
- **Committed anatomical meshes** — `BrainMesh_ICBM152_smoothed.gii`, `NewSmoothed.gii` and ten `.gii` files in total: standard cortical surfaces, reusable for any visualisation on the same anatomy.
- **The atlas and worked sample data** — `AALv.txt` (atlas vertices), `OverlayData.txt` (per-region values), `Network.edge` (region-to-region relationships). A complete worked example of both data shapes.
- **A vendored copy of nibabel** — `nibabel/`, 480 of 512 paths, including 194 committed `.pyc` files. **Ninety-four per cent of this repository is a vendored dependency**; the project itself is roughly thirty files at the root.
- **A PyInstaller specification and a GUI** — `New_PyBP.spec`, `PyBPGUI.png`, four screenshots.
- **`UserScript.py`** — the intended entry point for a user rather than a developer.
- **Not here:** a licence, tests, or packaging. The dependency was vendored instead.

## Transferable Capability
**Projecting values from a coarse labelled partition onto a fine continuous geometry is a general problem, and it is mostly about the coordinate systems not matching.** The domain here is neuroimaging, but the shape — regions with values, a mesh with vertices, no shared frame — is identical to choropleth mapping, thermal or stress fields on a CAD surface, sensor readings over a floor plan, or any aggregate quantity displayed over the geometry it was aggregated from. The separation of **scalar overlays from relational edges** is the modelling decision worth taking: values on regions and connections between regions are different data needing different visual treatment, and conflating them is the usual mistake.

**Alternative to:** plotting regions as flat coloured blocks, which loses the geometry; and to interpolating without an explicit alignment step, which produces a picture that is confidently misregistered. **Applies wherever** aggregated values must be shown over the geometry they came from.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Scientific_Computation
- Maturity Stage: Reference
- License Class: Unknown
- Deployment Target: Desktop
- Interface Protocol: GUI
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Read the projection approach when displaying region-aggregated values over any continuous surface, in or out of neuroimaging.
- Reuse the committed `.gii` meshes as standard cortical surfaces for other visualisation work.
- Take the scalar-versus-relational separation into any overlay design where both kinds of data must be shown.

## Reading Notes
**No licence file and none reported by GitHub**, so it is excluded from licence-constrained answers — which is a real loss here, because the committed meshes would otherwise be reusable. Eleven stars, created 2017, and it **vendors nibabel including 194 committed `.pyc` files**: 480 of 512 paths are the dependency, so any assessment based on repository size will be wrong. The GUI and the PyInstaller spec indicate the audience was researchers rather than developers, which explains both the vendoring and the absence of packaging.

## Semantic Links
- [parent_topic:: [[Topic - Scientific Simulation & Math]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[simbody]]]
- [related_to:: [[opengeos - leafmap]]]
- [related_to:: [[LaurentRDC - scikit-ued]]]
- [implements_pattern:: [[Pattern - Scientific Simulation]]]
- [implements_pattern:: [[Pattern - Spatial Indexing]]]
- [mentions_term:: [[Glossary - Simulation]]]
- [mentions_term:: [[Glossary - Dataset]]]
- [mentions_term:: [[Glossary - Coordinate Reference System]]]

## Evidence
- Source URL: https://github.com/alexandershaw4/PyBP-Py-BrainPlotter-for-AAL90
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; no Python file, mesh or data file was opened, and no licence file exists to read

## GitHub Snapshot

- Description: Visualisation & processing of MEG data and networks on meshes. A bunch of functions, examples and a gui.
- Language: Python
- License (SPDX): NOASSERTION
- Default Branch: master
- Stars: 11
- Pushed At: 2019-10-11T09:01:00Z
- Topics: alignment, atlas, brain-imaging, data-visualization, electroencephalography, magnetoencephalography, mesh-processing, neuroimaging, overlay, visualization

## Evidence Anchors
- [github_repo] description :: Visualisation & processing of MEG data and networks on meshes. A bunch of functions, examples and a gui. (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: NOASSERTION (confidence 0.90)
- [github_repo] topics :: alignment, atlas, brain-imaging, data-visualization, electroencephalography, magnetoencephalography, mesh-processing, neuroimaging, overlay, visualization (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 512 paths at HEAD (confidence 0.95)
