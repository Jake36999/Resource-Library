---
uuid: "67f58c52-8ad5-581f-b57d-c6dbfe054f11"
canonical_url: "https://github.com/simbody/simbody"
repo_key: "simbody/simbody"
owner: "simbody"
repo_name: "simbody"
aliases: ["simbody/simbody", "https://github.com/simbody/simbody"]
type: "scientific_library"
primary_topic: "Scientific Simulation & Math"
secondary_topics: ["Data APIs & Big Data", "Geospatial & Earth Data"]
ecosystem: "Mixed"
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
glossary_terms: ["Simulation", "Symbolic Mathematics", "Astronomy", "Active Learning"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
evidence_count: 6
github_description: "High-performance C++ multibody dynamics/physics library for simulating articulated biomechanical and mechanical systems like vehicles, robots, and the human skeleton."
github_language: "C++"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "master"
github_stars: 0
github_topics: ["biomechanics", "multibody-dynamics", "physics-engine", "physics-simulation", "robotics"]
github_homepage: "https://simtk.org/home/simbody"
github_pushed_at: "2026-08-25T16:50:51Z"
github_updated_at: "2026-08-30T13:18:07Z"
---

# simbody

## Bottom Line
A C++ multibody dynamics engine that simulates articulated mechanical and biomechanical systems — skeletons, linkages, vehicles — computing rigid-body motion in O(n) time with a Featherstone-style algorithm.

## What It Solves
- Simulate jointed systems efficiently, where naive formulations scale badly with body count.
- Handle constraints, contact and both forward and inverse dynamics in one engine.
- Give domain applications a physics core rather than requiring each to write its own.

## Architecture & Mechanics
- Three subsystems: SimTKcommon for foundations, SimTKmath for numerics, and Simbody for the dynamics engine.
- An O(n) Featherstone-style articulated-body algorithm computes motion for jointed chains.
- Constraint handling, contact modelling and OpenGL visualisation are provided alongside.
- It is a library, not an application — embedded in OpenSim for biomechanics and Gazebo for robotics.

## What Is Inside
- **Three layered libraries, usable separately** — `SimTKcommon/` (190 files: `BigMatrix/`, `Mechanics/`, `Random/`, `Simulation/`), `SimTKmath/` (478: `Optimizers/` 217, `Integrators/` 138, `Geometry/` 52, `LinearAlgebra/` 17), and `Simbody/` (285) which builds multibody dynamics on top. The optimiser and integrator collections are the reusable part for anyone doing numerical work outside biomechanics.
- **121 examples, and a second set of ad-hoc ones** — `examples/` plus `Simbody/tests/adhoc/` (`PendulumExample.cpp`, `GeometryPlayground.cpp`, `OpenSimPartyDemoCable.cpp`) which are exploratory programs kept beside the tests.
- **31 `.stl` meshes** shipped for the visualiser and geometry tests.
- **A testing header as a public API** — `SimTKcommon/include/SimTKcommon/Testing.h`, so downstream projects use the same assertions; 178 test paths.
- **Design documentation as PDFs with source** — `SimTKcommon/doc/Simmatrix.doc` and `.pdf`.
- **Prebuilt Windows dependencies vendored** — `Platform/Windows/lib_x64/libblas.lib`, `liblapack.lib`, and 12 `.dll` files, which is why the Windows build works without a Fortran toolchain.

## Transferable Capability
**Separate the numerical machinery from the domain that motivates it, and publish both.** Solvers, integrators and geometry stand alone; the domain layer is one client of them among possible others. The separable practice: **ship the testing assertions as part of the public interface**, so downstream projects hold themselves to the same standard rather than inventing their own.

**Alternative to:** numerical methods buried inside the application that needed them, where reusing one means extracting it. **Applies wherever** a specialised system contains general machinery that others would want.

## Taxonomy
- Ecosystem: Mixed
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
- Embed multibody physics in a simulation tool rather than writing an engine.
- Run inverse dynamics to recover the forces implied by an observed motion.
- Study O(n) articulated-body formulations against naive alternatives.

## Semantic Links
- [parent_topic:: [[Topic - Scientific Simulation & Math]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[astropy]]]
- [related_to:: [[sympy]]]
- [related_to:: [[LaurentRDC - scikit-ued]]]
- [implements_pattern:: [[Pattern - Scientific Simulation]]]
- [implements_pattern:: [[Pattern - Symbolic Computation]]]
- [mentions_term:: [[Glossary - Simulation]]]
- [mentions_term:: [[Glossary - Symbolic Mathematics]]]
- [mentions_term:: [[Glossary - Astronomy]]]
- [mentions_term:: [[Glossary - Active Learning]]]

## Evidence
- Source URL: https://github.com/simbody/simbody
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names Apache-2.0 (reproduced in full). The GitHub API reported `UNKNOWN`, which is why this was read directly.

## GitHub Snapshot

- Description: High-performance C++ multibody dynamics/physics library for simulating articulated biomechanical and mechanical systems like vehicles, robots, and the human skeleton.
- Language: C++
- License: Unknown (UNKNOWN)
- Default Branch: master
- Stars: 0
- Watchers: 0
- Homepage: https://simtk.org/home/simbody
- Archived: no
- Disabled: no
- Pushed At: 2026-08-25T16:50:51Z
- Updated At: 2026-08-30T13:18:07Z
- Topics: biomechanics, multibody-dynamics, physics-engine, physics-simulation, robotics

## Evidence Anchors
- [github_repo] description :: High-performance C++ multibody dynamics/physics library for simulating articulated biomechanical and mechanical systems like vehicles, robots, and the human skeleton. (confidence 0.95)
- [github_repo] topics :: biomechanics, multibody-dynamics, physics-engine, physics-simulation, robotics (confidence 0.82)
- [github_repo] language :: C++ (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
