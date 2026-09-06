---
uuid: "a1106f69-3f73-50ca-9406-b105820c8eae"
canonical_url: "https://github.com/openscad/openscad"
repo_key: "openscad/openscad"
owner: "openscad"
repo_name: "openscad"
aliases: ["openscad/openscad", "https://github.com/openscad/openscad"]
type: "cad_tool"
primary_topic: "CAD & SaaS Design"
secondary_topics: ["Architecture & Developer Playbooks"]
ecosystem: "CAD_Modeling"
domain_primary: "Design"
maturity_stage: "Production_Ready"
license_class: "Copyleft"
deployment_target: "Desktop"
interface_protocol: "CLI"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["CAD Workflow", "Parametric Modeling"]
glossary_terms: ["CAD", "Parametric Modeling", "Product Design"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "GPL-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-08-31"
evidence_count: 5
github_description: "OpenSCAD - The Programmers Solid 3D CAD Modeller"
github_language: "C++"
github_license_spdx: "NOASSERTION"
github_default_branch: "master"
github_stars: 10076
github_topics: ["3d", "3d-graphics", "3d-models", "3d-printing", "c-plus-plus", "c-plus-plus-17", "cad", "dxf-files", "linux", "macos", "opengl", "openscad", "qt5", "qt6", "windows"]
github_homepage: "https://www.openscad.org"
github_pushed_at: "2026-08-31T07:17:15Z"
---
# openscad - openscad

## Bottom Line
A solid modeller with no interactive drawing at all: geometry is described entirely in a small declarative script language and compiled into a mesh.

## What It Solves
- Make CAD models diffable, reviewable and generatable like source code.
- Parameterise a design so one variable produces a whole family of parts.
- Automate model production in build pipelines with no GUI involved.

## Architecture & Mechanics
- A functional script language composes primitives with boolean operations (union, difference, intersection).
- Constructive solid geometry is evaluated into a mesh via CGAL or the Manifold engine.
- A preview renderer gives fast OpenGL feedback before the exact render pass.
- The command line renders headlessly to STL, DXF, SVG or PNG.

## What Is Inside
- **Two thirds of the repository is its regression corpus** — `tests/` (2,486 files): `tests/regression/` (1,747) and `tests/data/` (713). The comparison artefacts are the interesting part: **1,296 `.png` renders, 624 `.scad` models, 243 `.csg` compiled trees and 126 `.echo` output logs**, so each test pins a model, its compiled representation and its rendered image together. That is a complete visual-regression corpus for constructive solid geometry.
- **The application, by layer** — `src/`: `gui/` (185), `core/` (148, including the language evaluator), `geometry/` (60), `glview/` (62), `io/` (39), `libsvg/` (35, an in-tree SVG parser), `ext/` (79).
- **66 example models grouped by difficulty** — `examples/Advanced/` includes `GEB.scad` and `animation.scad`; `.github/workflows/test-examples.yml` runs them, so the examples cannot silently break.
- **Design documentation as diagrams** — `doc/OpenSCAD-classes.graffle` with a rendered PDF, and `OpenSCAD-compile.graffle`.
- **Icon themes as a data set** — `resources/icons/` (185 files, 217 SVG overall) with light and dark variants.

## Transferable Capability
**Describe an artefact as a program, so it can be diffed, reviewed, parameterised and generated.** The description becomes text under version control rather than an opaque document, which is what makes collaboration and variation possible at all. The separable practice, and the more transferable one: **pin each test with its source, its intermediate compiled form and its rendered output together**, so a regression is located at the stage where it happened rather than only observed at the end.

**Alternative to:** direct manipulation, which is faster to start and impossible to review; and to visual tests that show something changed without saying where. **Applies wherever** an artefact is generated and its generation can regress.

## Taxonomy
- Ecosystem: CAD_Modeling
- Domain Primary: Design
- Maturity Stage: Production_Ready
- License Class: Copyleft
- Deployment Target: Desktop
- Interface Protocol: CLI
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Generate parametric enclosures and brackets from a single scripted source.
- Version-control mechanical design alongside firmware in the same repository.
- Study constructive solid geometry as a modelling paradigm.

## Semantic Links
- [parent_topic:: [[Topic - CAD & SaaS Design]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[FreeCAD - FreeCAD]]]
- [related_to:: [[CadQuery - cadquery]]]
- [implements_pattern:: [[Pattern - CAD Workflow]]]
- [implements_pattern:: [[Pattern - Parametric Modeling]]]
- [mentions_term:: [[Glossary - CAD]]]
- [mentions_term:: [[Glossary - Parametric Modeling]]]
- [mentions_term:: [[Glossary - Product Design]]]

## Evidence
- Source URL: https://github.com/openscad/openscad
- Source kind: GitHub REST metadata plus maintainer documentation
- Ingestion mode: agent-curated note authored against live repository metadata
- Metadata captured: 2026-08-31
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names GPL-2.0 (reproduced in full). The GitHub API reported `NOASSERTION`, which is why this was read directly.

## GitHub Snapshot

- Description: OpenSCAD - The Programmers Solid 3D CAD Modeller
- Language: C++
- License (SPDX): NOASSERTION
- Default Branch: master
- Stars: 10076
- Homepage: https://www.openscad.org
- Pushed At: 2026-08-31T07:17:15Z
- Topics: 3d, 3d-graphics, 3d-models, 3d-printing, c-plus-plus, c-plus-plus-17, cad, dxf-files, linux, macos, opengl, openscad, qt5, qt6, windows

## Evidence Anchors
- [github_repo] description :: OpenSCAD - The Programmers Solid 3D CAD Modeller (confidence 0.95)
- [github_repo] language :: C++ (confidence 0.90)
- [github_repo] license :: NOASSERTION (confidence 0.90)
- [github_repo] topics :: 3d, 3d-graphics, 3d-models, 3d-printing, c-plus-plus, c-plus-plus-17, cad, dxf-files, linux, macos, opengl, openscad, qt5, qt6, windows (confidence 0.85)
