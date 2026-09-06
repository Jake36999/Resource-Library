---
type: "technique_register"
status: "active"
created: "2026-09-03"
sources_drawn_from: 17
purpose: "what is reusable in the cohort, where it sits in the source, and what it would do here"
authority: "advisory - a register of what was found, not a decision to adopt"
---

# Applicable Techniques From The 2026-09 Cohort

## Why This Note Exists Separately From The Research Report

[[Research Report 2026-09-03 - Lineage, Parsing and Graph Reasoning]] ranks candidate changes
by expected value and argues for a build order. It answers *what should we do next*.

This note answers a different question: **what is in these sources that anybody here might
need, for a purpose nobody has thought of yet.** The two are not the same, and conflating them
is how a catalogue loses its point. A technique that ranks last for the current roadmap may be
the exact thing someone needs in six months, and it will only be findable if it was written
down when it was seen — with enough specificity that a search can reach it.

The failure mode this exists to prevent: a source summarised abstractly is a source whose
niche method is invisible. "GLiNER does zero-shot NER" is true and nearly useless. "GLiNER
scores every candidate span up to length 12 against label embeddings by sigmoid dot product,
and its bi-encoder variant lets you precompute those label embeddings so a hundred entity
types stay affordable" is findable by someone with a hundred entity types and no GPU.

Entries are grouped by what they would serve here, not by which source they came from.

---

## 1. Pipeline And Retrieval Design

### Community summarisation — microsoft/graphrag
**Where:** `packages/graphrag/graphrag/index/operations/summarize_communities/`, and
`query/structured_search/global_search/` which consumes it.
**What it is:** after clustering, write a natural-language report per community per hierarchy
level, and answer whole-corpus questions by map-reducing over those reports rather than over
retrieved chunks.
**Why it matters here:** a question about the *whole* has no answer in any single note, so
retrieval cannot reach it at any quality of ranking.
**Status: adopted**, without the model — `librarian graph` now writes a report per community
assembled from facts the index holds. See §5.3 of the research report.

### Structurally different indexes, and a router that picks — run-llama/llama_index
**Where:** `llama-index-core/llama_index/core/indices/` (93 files: `vector_store`,
`keyword_table`, `list`, `tree`, `document_summary`, `knowledge_graph`, `property_graph`,
`struct_store`, `composability`), plus `core/selectors/` and the router.
**What it is:** not one index with options — different *structures*, each answering a different
question shape, with an explicit routing decision between them.
**Why it matters here:** the vault's eval is saturated on hit@5 with filters and FTS5 alone,
which means the remaining gains are not ranking gains. "Where is X mentioned" is lexical;
"what is this about" is a summary index; "what connects A and B" is a graph walk. The
`document_summary` index in particular — retrieve by a summary of each note, then read the
note — maps onto a vault of 265 notes almost exactly.

### The retrieval cost ladder, confirmed from outside — llama_index and graphrag both
Both projects narrow before they read: prefiltering, then structure, then text. The vault's
own tiered ladder (spec §3.0) is the same shape, arrived at independently. Worth recording as
corroboration rather than as a change.

### Precompute at write time — graphrag against llama_index
graphrag spends heavily at index time so query time is a lookup; llama_index keeps ingestion
light and works per query. The vault is written in supervised passes and read constantly, so
it belongs on graphrag's side — which spec §5's separate read and write budgets already say.

---

## 2. Data And Memory Contracts

### Schema-first, with generated bindings — open-metadata/OpenMetadata
**Where:** `openmetadata-spec/src/main/resources/json/schema/` — 904 JSON Schemas, 380 of them
entities; `openmetadata-ui/src/generated/` is described in `ARCHITECTURE.md` as "a pure sink".
**What it is:** every entity and API shape defined once; Java, Python and TypeScript models
generated from it, so no binding is hand-written and none can drift.
**Applied here in its weak form:** [[Note Content Model]] declares shape and closed axis values
and `integrity.py` validates against it — *validate, do not generate*. The strong form would
mean generating `notes.py`, which is more machinery than a Markdown vault needs.

### A written content model with a containment rule — syntax-tree/mdast
**Where:** the whole of `readme.md`; the load-bearing part is the **content model** section,
where `FlowContent`, `ListContent` and `PhrasingContent` are type unions saying which nodes may
contain which.
**What it is:** the thing that makes a tree *checkable* rather than merely traversable.
**Applicable but not yet applied:** the vault's content model constrains which fields and
sections exist, not which links may point at which. A containment rule — a glossary note may
not `implements_pattern`; an application record must reach a resource — is the same idea one
level up, and `integrity.py` has the link table to enforce it with.

### Policy as a schema, not as code — PHACDataHub/data-mesh-ref-impl
**Where:** `paradire/analytics/acg/`, especially `src/directives.ts`; design in
`paradire/doc/part-ii.md`.
**What it is:** the data-sharing policy is a GraphQL schema whose custom directives — `@hash`,
`@restrict`, `@selectable`, `@date` — transform each field, reconfigurable at runtime by
posting a new ruleset to a Kafka topic. The policy and the API contract are one artefact.
**Where it would apply here:** the MCP surface (Implementation Brief step 11) has to decide
what an external agent may see. Expressing that as annotations on the note schema, rather than
as filtering code, would make it reviewable by whoever owns the decision.

### Bidirectional, portable serialisation of a semantic layer — neo4j-labs/neocarta
**Where:** `neocarta/connectors/osi/`, against the
[Open Semantic Interchange](https://github.com/open-semantic-interchange/OSI) spec.
**What it is:** alone among its connectors, OSI both ingests *and* exports — a graph subgraph
round-trips to spec-compliant YAML with column ordering preserved.
**Why it matters here:** a catalogue whose taxonomy can only be read by its own tooling is a
catalogue nobody else can check. Not urgent; worth knowing exists.

### Identity by content, not by location — recipy/recipy
**Where:** `CHANGELOG.md` v0.3.0; the hashing is in `recipy/log.py`.
**What it is:** every input and output file is content-hashed, and search is by hash by
default, so provenance survives a rename.
**Where it would apply here:** two of seventeen sources had moved path during this cohort. The
redirect check now catches renames; content addressing would catch the harder case of the same
material appearing under a different name.

---

## 3. Scouting And Intake

### Structural search as the evidence step — semgrep/semgrep
**Where:** `src/ast_generic` (one generic AST all 37 languages normalise into), `src/matching`,
`src/tainting`, `src/prefiltering`; the grammars are 36 forked tree-sitter submodules declared
in `.gitmodules`.
**What it is:** a pattern written in the syntax of the target language, with `$X` metavariables
and `...` ellipses, matched against the parsed program.
**Where it would apply here:** `find_technique` currently ends at tier 3 — "open a workbench to
confirm". One semgrep rule turns "this repository probably handles backpressure" into
file-and-line evidence, across languages, without writing a parser. **Licence constraint:**
LGPL-2.1, so it may be invoked as a subprocess and never vendored.
**Also worth stealing regardless:** `src/metachecking` — rules that validate rules. The vault's
equivalent is checks that validate the content model, which does not exist yet.

### Incremental parsing, and a query language over the tree — tree-sitter/tree-sitter
**Where:** runtime in `lib/src/` (plain C: `subtree.c`, `reusable_node.h`,
`get_changed_ranges.c`, `stack.c`); the query engine in `lib/src/query.c`, documented at
`docs/src/using-parsers/queries/`.
**What it is, in two parts that are worth separating:**
- *Incremental reparse* — reuse the previous tree and reparse only what an edit invalidated.
- *S-expression queries over a syntax tree* — node types, named fields
  (`left: (member_expression object: (call_expression))`), negated fields (`!type_parameters`),
  captures and predicates.
**Where the second applies here:** the vault is 265 Markdown documents with strict structure,
and every structural assertion in `integrity.py` is currently a regular expression. A tree plus
a query language is the principled version. tree-sitter has a Markdown grammar; mdast is the
model. Nothing in the catalogue does this yet, and §10 of the research report records that no
"semgrep for Markdown" appears to exist.
**Caveat worth carrying:** `docs/src/5-implementation.md` documents the CLI thoroughly and then
stops at "## The Runtime — WIP". The incremental algorithm is documented only in the C source.

### Lossless trees, and metadata providers over them — Instagram/LibCST
**Where:** `libcst/_nodes/` (66 files, whitespace attached as a *field* on its owning node
rather than as a sibling); `libcst/matchers/` (declarative patterns instead of nested
`isinstance`); `libcst/metadata/` (29 files — `scope_provider`, `name_provider`,
`position_provider`, `type_inference_provider` shelling out to Pyre, `full_repo_manager` for
providers needing more than one file).
**What is transferable independently of Python:** the *metadata provider* idea — a tree carries
syntax, and separately computed providers attach the facts the tree does not contain. A vault
note's tree does not know its own community, centrality, or licence resolution; those are
providers over it.
**Structural note:** by file count `libcst/codemod/` (73 files) is the largest subsystem. The
repository is a codemod platform with a parser inside it, which its own description does not say.

### Weak supervision as the shape for any multi-signal judgement — snorkel-team/snorkel
**Where:** `snorkel/labeling/model/label_model.py` (the mechanism is in the class docstring),
`snorkel/labeling/analysis.py` (`LFAnalysis`: coverage, overlap, conflict, empirical accuracy),
`snorkel/slicing/` (the least-known subsystem).
**Two separable ideas:**
- *Estimate voter reliability with no ground truth* — build the junction tree of the labelling
  functions' dependency graph, compute the inverse generalized covariance, complete it
  matrix-completion style. `scout/rank.py` has six hand-weighted signals and no instrument that
  could say whether the weights are wrong.
- *Slicing* — make "performance on this named subset" a first-class tracked object. The eval
  set is 20 questions with no notion of slices; per-intent or per-topic recall would be the
  same idea.
**Do not install it:** Python 3.11 exactly, plus PyTorch, for maths that is about fifty lines
of numpy in the conditionally-independent case.

### Sequence-aware aggregation, and the axis it separates — NorskRegnesentral/skweak
**Where:** `skweak/aggregation.py` separates the *shape* of the label space
(`TextAggregatorMixin`, `SequenceAggregatorMixin`, `MultilabelAggregatorMixin`) from the
*method* of reconciliation (`voting.py` majority, `generative.py` NaiveBayes and HMM).
`skweak/doclevel.py` propagates a decision across a document.
**The transferable part:** that separation is good design regardless of the domain — deciding
*what shape of thing you are labelling* and *how you reconcile disagreement* are independent
choices, and most implementations tangle them.
**Unmaintained by its authors' own statement.** Read it; do not depend on it.

### Zero-shot extraction against a runtime schema — urchade/GLiNER
**Where:** `docs/architectures.md` sets out the mechanism; `gliner/modeling/span_rep.py`,
`gliner/multitask/` for the QA, relation-extraction and open-extraction heads.
**How it works, specifically:** entity labels and text go through one bidirectional encoder
with a learned `[ENT]` token before each label; the `[ENT]` outputs become label embeddings;
every candidate span up to length **12** is represented from its first and last token; a span
matches a label when the sigmoid of their dot product passes a threshold. The **bi-encoder**
variant encodes labels separately so their embeddings can be precomputed, which is what makes
100+ entity types affordable.
**Where it would apply here:** `access_points.py` is a fixed set of regexes and is at its
ceiling. A zero-shot extractor makes the extraction schema a runtime argument — endpoints,
auth schemes, rate limits today; technique names, data formats, licence obligations tomorrow —
without new code or training. Runs on CPU. Ranked last in the research report because its value
on documentation prose is untested, not because the mechanism is unclear.
**Also:** the `Relex` head does joint entity *and relation* extraction in one pass, which is
knowledge-graph construction without a second model.

### Auto-classification as a reconciliation stack — open-metadata/OpenMetadata
**Where:** `ingestion/src/metadata/pii/` — Presidio recognisers with local patches, a NER pass
(`ner.py`), column-name patterns, engineered features, `tag_scoring.py`, `conflict_resolver.py`.
**Why it is here:** this is weak supervision arrived at independently, inside a data catalogue,
with no reference to the literature. Three sources in this cohort converge on *many noisy
labellers, scored and reconciled* and only two call it that. That convergence is the strongest
argument that the shape is right.

### Connector-per-source harvesting — OpenMetadata and neocarta
**Where:** `ingestion/src/metadata/ingestion/source/` (71 database connectors alone; 120+
overall, each resolved through a `service_spec.py`); neocarta's `connectors/_base.py` and its
`.claude/skills/neocarta-add-source-connector/` contract.
**The design decision worth copying:** in OpenMetadata the ingestion framework **writes through
the same public REST API everyone else uses** — it is a client, not a privileged path. The
vault's intake writes Markdown directly, which is the equivalent discipline, and it is worth
keeping deliberately rather than by accident.

---

## 4. Documentation And Working Practice

### An architecture document that states its own provenance — open-metadata/OpenMetadata
**Where:** `ARCHITECTURE.md`.
**What makes it unusual:** it declares how its numbers were obtained ("module edges from the
POMs; package/import counts by grep/Tarjan"), traces three request paths concretely, gives a
"look here first" column per module, and names where its layering **fails** rather than
describing an intended architecture. In an 18,794-file repository, which is the opposite of the
usual relationship between project size and documentation honesty.
**Directly applicable:** the vault's own design documents describe intent. A measured companion
— what the link graph actually looks like, where the layering does not hold — is now partly
available from the community reports.

### Contribution conventions as executable procedure
**Where:** OpenMetadata's `skills/` (a 184-file `.claude-plugin` covering connector building,
connector audit, code review, TDD, systematic debugging, Playwright validation, PR checklists);
neocarta's `.claude/skills/neocarta-add-source-connector/` with a `SKILL.md`, a written contract
and a `driver.py`; semgrep's top-level `AGENTS.md` and `CLAUDE.md`.
**Why it is recorded:** three of seventeen sources ship agent instructions for their own
contributors, and the pass did not set out to look for this. It changes what "reusable" means
for a source, and the taxonomy has no axis for it.

### Diagram source checked in beside the render — neo4j-labs/neocarta
**Where:** `assets/mermaid/data_model/*.mmd` alongside `assets/images/data_model/*.png`, one
pair per model, each next to the package README it documents.
**Small and worth copying:** a diagram whose source is diffable is a diagram that can be
reviewed.

### Quarantine rather than filter — Victor-Kipruto-Rop/medallion-lakehouse-platform
**Where:** `src/transformations/bronze_to_silver.py`.
**What it is:** invalid rows are written to `_quarantine/transactions/date=.../` and counted in
a warning, not dropped.
**Directly applicable:** the intake currently logs, marks and skips a bad source. Keeping the
rejected material somewhere inspectable is the difference between a pipeline you can debug and
one you can only rerun.

---

## 5. What Was Looked For And Not Found

Recorded because a gap is a finding, and because these are the searches to repeat.

- **An open-source column-level SQL lineage engine.** The cohort's lead turned out to be
  marketing copy for a proprietary product; the one adequate implementation is inside a
  platform needing a JVM, a database and a search cluster. `sqlglot` and the OpenLineage
  specification are the obvious next leads and were not on the list. This is why
  `data_lineage_provenance` is now in [[Scouting Domains]].
- **A structural query tool for Markdown.** semgrep exists for code; mdast supplies the model
  and remark the utilities, but nothing lets you write a pattern shaped like the document you
  are looking for. For a system whose truth is Markdown this is a real absence, and possibly
  something to build rather than find.
- **Weak supervision over a ranking rather than a classification.** Snorkel's label model
  assumes discrete classes; scouting scores candidates on a continuum. Nothing in the cohort
  addresses noisy voters over an ordering.
- **A published retrieval eval set.** graphrag and llama_index both ship evaluation modules;
  neither ships a fixed question set with published numbers the way `librarian eval` does. This
  system is ahead of both on that specific discipline.

## Related
- [[Research Report 2026-09-03 - Lineage, Parsing and Graph Reasoning]] — the ranked assessment
- [[Scouting Working File 2026-09-03]] — the per-source evidence
- [[Note Content Model]] — where `What Is Inside` is declared
- [[Master Index]]
