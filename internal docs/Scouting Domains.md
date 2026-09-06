---
type: "domain_register"
status: "proposed"
existing_topics: 15
proposed_domains: 16
promoted: ["data_lineage_provenance"]
authority: "This note is authoritative. The scout may not invent a domain; it may only report `unmatched`."
---

# Scouting Domains

## How This Note Is Used
Each domain below supplies the scout with seed queries and a boundary. A domain becomes a real `Topic - <name>` index only once scouting has produced enough material to fill it — creating empty topic indexes ahead of content is what left this vault with two topics at zero resources.

`tier: 1` domains enter the scouting rotation immediately. `tier: 2` are held in reserve; promote one when a tier-1 domain saturates, which the gap-fit ranking signal will make obvious.

## Existing Topics
Already established and in rotation: Curated Aggregators, Agentic AI & Models, Data APIs & Big Data, Geospatial & Earth Data, Infrastructure & Observability, Security & SIEM, Frontend & Design Systems, Scientific Simulation & Math, Government & Civic Tech, CAD & SaaS Design, Architecture & Developer Playbooks.

## Proposed Domains

### Tier 1 - Enter Rotation Now

**Data Lineage & Provenance** (`data_lineage_provenance`) — **promoted 2026-09-04.**
Now a real index at [[Topic - Data Lineage & Provenance]] with eight resources, and
`Data_Lineage` is a permitted `domain_primary` value in [[Note Content Model]]. The
condition this note sets — enough material to fill it — was met by the second scouting
cohort. The boundary below held up in practice and is worth keeping: two of the eight,
[[recipy - recipy]] and [[shenhuan2021 - gudu-sql-omni-introduce]], had been filed under
`data_api_big_data` and were moved.
Where data came from and what produced it: SQL lineage parsers, column-level impact
analysis, run and workflow provenance capture, provenance interchange formats, and the
attribution of an artefact to the inputs and code that made it. Kept separate from
`data_api_big_data`, which is catalogues, portals and APIs — that domain answers *what
data exists*, this one answers *where it came from and what breaks if it changes*.
Seed queries: `sql lineage parser open source`, `column level lineage`, `openlineage integration`, `data provenance capture python`, `workflow provenance tracking`

**Code Intelligence & Structural Parsing** (`code_intelligence`)
Parsers and parser generators, abstract and concrete syntax trees, structural code query,
semantic code search, program analysis and codemod tooling. Distinct from
`testing_verification`, which covers static analysis as a *quality gate*; this covers the
parsing and querying machinery that such tools are built on, and the syntax-tree
specifications that let them interoperate.
Seed queries: `incremental parser generator`, `concrete syntax tree library`, `structural code search`, `abstract syntax tree specification`, `codemod framework`

**ML Training & MLOps** (`ml_training_mlops`)
Distinct from Agentic AI, which covers inference and orchestration. This covers what happens before a model is served: training frameworks, fine-tuning, experiment tracking, feature stores, vector databases, quantisation, evaluation harnesses.
Seed queries: `open source experiment tracking mlops`, `fine-tuning framework LLM`, `vector database open source`, `model quantization toolkit`, `llm evaluation harness`

**Signal, Audio & Speech** (`signal_audio_speech`)
DSP, speech recognition, synthesis, audio analysis. Directly load-bearing for this environment, which already runs Vosk and Orpheus locally — the catalogue should know its own dependencies.
Seed queries: `open source speech recognition offline`, `text to speech neural open source`, `digital signal processing library python`, `audio feature extraction`

**Computer Vision & Imaging** (`vision_imaging`)
Detection, segmentation, OCR, image pipelines, document understanding. Adjacent to the existing geospatial topic but distinct in method.
Seed queries: `open source OCR engine`, `object detection framework`, `document layout analysis`, `image processing pipeline library`

**Knowledge Management & PKM** (`knowledge_management`)
Note systems, Obsidian plugins, graph tooling, RAG infrastructure, semantic search, personal knowledge bases. This catalogue is itself an instance of this domain; it should be able to reason about its own architecture.
Seed queries: `obsidian plugin knowledge graph`, `open source RAG framework`, `semantic search self hosted`, `personal knowledge management open source`

**Distributed Systems & Data Movement** (`distributed_systems`)
Queues, streaming, consensus, replication, event sourcing, CDC. The plumbing under most of the Infrastructure topic, but a different body of theory.
Seed queries: `open source message queue`, `stream processing framework`, `raft consensus implementation`, `change data capture open source`

**Testing, QA & Formal Methods** (`testing_verification`)
Property-based testing, fuzzing, contract testing, static analysis, model checking, proof assistants. Under-catalogued relative to how much project maturity depends on it.
Seed queries: `property based testing library`, `fuzzing framework open source`, `static analysis tool`, `model checker formal verification`

**Privacy, Cryptography & Identity** (`crypto_identity`)
Cryptographic libraries, zero-knowledge tooling, authentication and authorisation, privacy-preserving computation, secrets management. Kept separate from Security & SIEM, which is detection and response — this is construction.
Seed queries: `cryptography library audited`, `zero knowledge proof toolkit`, `open source identity provider`, `secrets management self hosted`

**Manufacturing, CNC & Additive** (`manufacturing_fabrication`)
Slicers, G-code, toolpath generation, machine control, fabrication workflows. The natural downstream of the existing CAD topic — a parametric model is only useful if something can make it.
Seed queries: `open source 3d printing slicer`, `CNC toolpath generation`, `g-code sender open source`, `CAM open source`

### Tier 2 - Reserve

**Robotics & Embedded** (`robotics_embedded`) — ROS, RTOS, firmware, motion planning, edge deployment.
Seed queries: `ROS2 package`, `real time operating system embedded`, `motion planning library`

**Datasets & Benchmarks** (`datasets_benchmarks`) — Corpora, evaluation suites, leaderboards, data cards. Pairs naturally with the paper layer.
Seed queries: `open dataset repository`, `benchmark suite machine learning`, `evaluation dataset`

**Licensing & Compliance Tooling** (`licensing_compliance`) — SBOM generation, licence scanning, dependency auditing, policy-as-code. Directly serves this catalogue's own reusability signal.
Seed queries: `SBOM generator open source`, `license compliance scanner`, `policy as code`

**Documentation & Diagramming Systems** (`documentation_systems`) — Docs-as-code, static site generators, diagram-as-text, API documentation.
Seed queries: `documentation site generator`, `diagram as code`, `API documentation generator`

**Energy, Climate & Environment** (`energy_climate`) — Grid modelling, climate datasets, emissions accounting, environmental sensing.
Seed queries: `open source energy system model`, `climate data toolkit`, `carbon accounting open source`

**Human Interface & Accessibility** (`interface_accessibility`) — Accessibility tooling, input devices, HCI toolkits, assistive technology.
Seed queries: `accessibility testing tool`, `screen reader open source`, `assistive technology software`

## Domain Selection Notes
Three principles shaped this list rather than simply naming popular fields.

**Adjacency to existing coverage.** Manufacturing extends CAD; distributed systems underpins Infrastructure; crypto complements Security. New domains that touch existing ones produce cross-links, and cross-links are what make the vault traversable rather than merely large.

**Self-knowledge.** Knowledge Management and Signal/Audio both describe systems this environment already runs. A catalogue that cannot explain its own stack is missing the material it most needs.

**Neglected but load-bearing.** Testing and Licensing are unglamorous and rarely curated, which is exactly why cataloguing them pays — the gap-fit signal will rank them highly, and they determine whether anything else can actually be adopted.

## Register Changes
`code_intelligence` was added on 2026-09-03, on user approval, during the pass recorded in
[[Research Report 2026-09-03 - Lineage, Parsing and Graph Reasoning]]. Four sources in that
cohort — tree-sitter, LibCST, semgrep and mdast — matched no existing domain, and
`testing_verification` would have taken only one of the four. The register's rule is that a
scout may report `unmatched` but may not invent a key; this addition is the editing of the
authoritative note that the rule requires instead.

`data_lineage_provenance` was added on the same date, on a separate approval, for a gap the
same pass found and deliberately did not act on at the time. Three sources — OpenMetadata,
recipy and Gudu SQL Omni — file under `data_api_big_data` because it is the closest
existing topic, not a good one: that topic is catalogues, portals and APIs, and provenance
is a different question about the same material.

The stronger argument for it is a negative result. The pass set out to find an open-source
column-level SQL lineage engine and **did not find one**: its most promising lead turned out
to be marketing copy for a proprietary product, and the one adequate implementation is
buried inside a platform requiring a JVM, a database and a search cluster. A domain the
catalogue searched and could not fill is exactly the condition `gap_fit` exists to detect,
and it cannot detect it while the domain has no key.

**Neither domain has a topic index yet, and that is deliberate.** The register's own rule is
that a domain becomes a `Topic - <name>` index only once scouting has produced enough
material to fill it; `data_lineage_provenance` currently has two sources that would move
into it, which is not enough. It enters the rotation as a discovery target, and the topic
gets created when the material exists.

## Related
- [[Schema Extension - Scouting Pipeline]]
- [[Schema Extension - Containers and Papers]]
- [[Master Index]]
