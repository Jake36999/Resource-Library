---
uuid: "6085599a-0ebc-5ece-a991-8508ce6508c7"
canonical_url: "https://github.com/gap-system/gap"
repo_key: "gap-system/gap"
owner: "gap-system"
repo_name: "gap"
aliases: ["gap-system/gap", "https://github.com/gap-system/gap"]
type: "scientific_library"
primary_topic: "Scientific Simulation & Math"
secondary_topics: ["Data APIs & Big Data", "Geospatial & Earth Data"]
ecosystem: "Geo_Data"
domain_primary: "Scientific_Computation"
maturity_stage: "Production_Ready"
license_class: "Copyleft"
deployment_target: "Local_Only"
interface_protocol: "Python_SDK"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "Documented"
patterns: ["Scientific Simulation", "Symbolic Computation"]
glossary_terms: ["Symbolic Mathematics", "Simulation", "Astronomy", "Active Learning"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "GPL-2.0"
source_file: "repositories to chart.md"
evidence_count: 6
github_description: "Main development repository for GAP - Groups, Algorithms, Programming, a System for Computational Discrete Algebra"
github_language: "GAP"
github_license: "Unknown"
github_license_spdx: "GPL-2.0"
github_default_branch: "master"
github_stars: 0
github_topics: ["algebra", "computer-algebra", "computer-algebra-system", "discrete-mathematics", "group-theory", "math", "mathematics", "representation-theory"]
github_homepage: "https://www.gap-system.org"
github_pushed_at: "2026-09-04T22:59:29Z"
github_updated_at: "2026-08-31T14:55:43Z"
---

# gap-system - gap

## Bottom Line
A computational discrete algebra system centred on group theory, combining its own programming language, a library of thousands of algebraic algorithms, and large datasets of classified mathematical objects.

## What It Solves
- Compute with groups, rings and related structures where general numeric tools do not apply.
- Reuse decades of implemented algebraic algorithms instead of reimplementing them.
- Query classified data — groups of a given order and similar catalogues — directly.

## Architecture & Mechanics
- A dedicated programming language for expressing algebraic computation.
- A library of thousands of functions implementing algorithms over discrete structures.
- Data libraries of classified objects ship with the system.
- The tree separates core source, library, documentation and tests, with an HPC variant for parallel work; licensed GPL-2.0.

## What Is Inside
- **A computer algebra system whose library is written in its own language** — `lib/` (515 files): 275 `.gi` implementation and 215 `.gd` declaration files. The C kernel is `src/` (202 files, 1,080 `.c` overall including vendored code).
- **A 1,128-file test corpus in a literate format** — `tst/`: `testinstall/` (325), `testbugfix/` (525, one regression per fixed bug), `teststandard/` (65), `testspecial/` (116), `test-compile/` (33). The 934 `.tst` files are input-and-expected-output transcripts, so they double as worked examples.
- **Documentation examples are executed** — `doc/ref/extractexamples.g` and `runexamples.g` pull the examples out of the manual and run them, so the documentation cannot silently rot. 189 example paths.
- **A benchmark suite with a written protocol** — `benchmark/` (43 files) organised by problem (`doublecoset/` and others), each with its own test scripts.
- **A parallel variant kept side by side** — `hpcgap/` (448 files), the shared-memory concurrent version.
- **Vendored dependencies dominate the file count** — `extern/gmp` (2,156) and `extern/zlib` (242); 921 `.asm` files are GMP's assembly.
- **A WebAssembly build** — `etc/emscripten/` with a web template and Dockerfile. `AGENTS.md` in-tree.

## Transferable Capability
**Write the library in the language the system provides, so that the extension path and the implementation path are the same path.** Anything the maintainers can build, a user can build, using the same facilities and the same idioms — the boundary between core and contribution disappears. The separable practice worth copying anywhere: **express regression tests as transcripts of input and expected output**, so every test doubles as a worked example and the test suite is readable as documentation.

**Alternative to:** a core in one language with extensions in another, where the extension surface is always narrower than the core's own. **Applies wherever** users are expected to extend a system substantially.

## Taxonomy
- Ecosystem: Geo_Data
- Domain Primary: Scientific_Computation
- Maturity Stage: Production_Ready
- License Class: Copyleft
- Deployment Target: Local_Only
- Interface Protocol: Python_SDK
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: Documented

## Integration & Use Cases
- Perform group-theoretic computation in research mathematics.
- Look up classified algebraic structures rather than deriving them.
- Study a domain-specific language built around one mathematical field.

## Semantic Links
- [parent_topic:: [[Topic - Scientific Simulation & Math]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[simbody]]]
- [related_to:: [[astropy]]]
- [related_to:: [[sympy]]]
- [implements_pattern:: [[Pattern - Scientific Simulation]]]
- [implements_pattern:: [[Pattern - Symbolic Computation]]]
- [mentions_term:: [[Glossary - Symbolic Mathematics]]]
- [mentions_term:: [[Glossary - Simulation]]]
- [mentions_term:: [[Glossary - Astronomy]]]
- [mentions_term:: [[Glossary - Active Learning]]]

## Evidence
- Source URL: https://github.com/gap-system/gap
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names GPL-2.0 (reproduced in full). The GitHub API reported `UNKNOWN`, which is why this was read directly.

## GitHub Snapshot

- Description: Main development repository for GAP - Groups, Algorithms, Programming, a System for Computational Discrete Algebra
- Language: GAP
- License: Unknown (UNKNOWN)
- Default Branch: master
- Stars: 0
- Watchers: 0
- Homepage: https://www.gap-system.org
- Archived: no
- Disabled: no
- Pushed At: 2026-08-31T15:02:46Z
- Updated At: 2026-08-31T14:55:43Z
- Topics: algebra, computer-algebra, computer-algebra-system, discrete-mathematics, group-theory, math, mathematics, representation-theory

## Evidence Anchors
- [github_repo] description :: Main development repository for GAP - Groups, Algorithms, Programming, a System for Computational Discrete Algebra (confidence 0.95)
- [github_repo] topics :: algebra, computer-algebra, computer-algebra-system, discrete-mathematics, group-theory, math, mathematics, representation-theory (confidence 0.82)
- [github_repo] language :: GAP (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
