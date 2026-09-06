---
uuid: "6da20f95-28a4-539b-b1dc-02b32b5ebe73"
canonical_url: "https://github.com/sympy/sympy"
repo_key: "sympy/sympy"
owner: "sympy"
repo_name: "sympy"
aliases: ["sympy/sympy", "https://github.com/sympy/sympy"]
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
glossary_terms: ["Symbolic Mathematics", "Simulation", "Astronomy", "Active Learning"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "BSD-3-Clause AND MIT"
source_file: "repositories to chart.md"
evidence_count: 6
github_description: "A computer algebra system written in pure Python"
github_language: "Python"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "master"
github_stars: 0
github_topics: ["computer-algebra", "hacktoberfest", "math", "python", "science"]
github_homepage: "https://sympy.org/"
github_pushed_at: "2026-08-29T17:14:43Z"
github_updated_at: "2026-08-31T14:09:15Z"
---

# sympy

## Bottom Line
A computer algebra system written in pure Python: expressions are symbolic objects that can be differentiated, integrated, simplified and solved exactly, with no compiled dependencies.

## What It Solves
- Manipulate mathematics exactly rather than numerically, keeping symbols as symbols.
- Do algebra inside a Python program without an external CAS or a compiled toolchain.
- Derive an expression symbolically, then generate numerical code from it.

## Architecture & Mechanics
- Symbols are declared as objects and combined into expression trees rather than evaluated.
- A core symbolic representation layer underpins every module.
- Specialised modules cover calculus, linear algebra, equation solving, simplification and series expansion.
- An `isympy` console supports interactive exploration; being pure Python, it installs anywhere Python runs.

## What Is Inside
- **A subpackage per branch of mathematics** — `sympy/`: `physics/` (225 files), `polys/` (201, the polynomial manipulation core), `matrices/` (92), `parsing/` (87), `core/` (86), `printing/` (78), `functions/` (61).
- **`sympy/parsing/` is the part with reach beyond SymPy** — parsers for LaTeX, Mathematica, Maxima and C/Fortran source, including 16 `.al` ANTLR-generated files for the LaTeX grammar. If you need to read mathematical notation into a structured form, this is a working implementation.
- **415 documentation files with worked derivations** — `doc/src/`, including explanation pages that carry their own SVG figures (`physics/biomechanics/hill-type-muscle-model.svg`, `physics/mechanics/PinJoint.svg`); 53 diagrams overall.
- **Doctests are the test strategy** — `bin/doctest` and `bin/coverage_doctest.py` measure documentation coverage as well as code coverage, so the examples in the docs are executed. 765 test paths.
- **A benchmark suite** — `sympy/benchmarks/` (`bench_discrete_log.py`, `bench_meijerint.py` and others).
- **A WebAssembly build path** — `.github/workflows/emscripten.yml`, so SymPy runs in a browser.

## Transferable Capability
**Manipulate expressions as structure rather than evaluating them to numbers**, so a relationship can be rearranged, simplified, differentiated or solved while it is still general. The separable capability with much wider reach: **readers for several human notation systems**, turning written mathematical notation into a manipulable form. The testing practice is worth taking too — **the documentation's examples are the test suite**, executed on every change, so no example can silently rot.

**Alternative to:** numeric evaluation, which answers for one input and discards the relationship; and to documentation whose correctness nobody checks. **Applies wherever** the general form is more useful than a particular answer, or wherever documentation must stay true.

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
- Derive and simplify expressions inside a scientific pipeline.
- Solve equations symbolically before committing to a numerical method.
- Study expression trees as a representation for exact mathematics.

## Reading Notes
**Two licences in the LICENSE file, both permissive.** BSD-3-Clause governs SymPy
itself; MIT covers vendored components. The GitHub API reported nothing at all, which is why
this note previously carried `Unknown` and was excluded from every permissive-constrained
query despite being one of the most reusable sources in the catalogue.

## Semantic Links
- [parent_topic:: [[Topic - Scientific Simulation & Math]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[simbody]]]
- [related_to:: [[astropy]]]
- [related_to:: [[LaurentRDC - scikit-ued]]]
- [implements_pattern:: [[Pattern - Scientific Simulation]]]
- [implements_pattern:: [[Pattern - Symbolic Computation]]]
- [mentions_term:: [[Glossary - Symbolic Mathematics]]]
- [mentions_term:: [[Glossary - Simulation]]]
- [mentions_term:: [[Glossary - Astronomy]]]
- [mentions_term:: [[Glossary - Active Learning]]]

## Evidence
- Source URL: https://github.com/sympy/sympy
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names BSD-3-Clause, MIT (2 reproduced in full, 0 referred to). The GitHub API reported `UNKNOWN`, which is why this was read directly.  **Composite - needs a person to confirm.**

## GitHub Snapshot

- Description: A computer algebra system written in pure Python
- Language: Python
- License: Unknown (UNKNOWN)
- Default Branch: master
- Stars: 0
- Watchers: 0
- Homepage: https://sympy.org/
- Archived: no
- Disabled: no
- Pushed At: 2026-08-29T17:14:43Z
- Updated At: 2026-08-31T14:09:15Z
- Topics: computer-algebra, hacktoberfest, math, python, science

## Evidence Anchors
- [github_repo] description :: A computer algebra system written in pure Python (confidence 0.95)
- [github_repo] topics :: computer-algebra, hacktoberfest, math, python, science (confidence 0.82)
- [github_repo] language :: Python (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
