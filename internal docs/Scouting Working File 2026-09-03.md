---
type: "working_file"
status: "complete"
created: "2026-09-03"
purpose: "evidence trail for the phase-one scouting pass; the notes are written from this"
repositories: 17
---

# Scouting Working File 2026-09-03

Method: one `GET /repos/{owner}/{repo}` per source for metadata (no `GITHUB_TOKEN`,
60 req/hr). Structure read from a blobless shallow clone
(`--depth 1 --filter=blob:none --no-checkout`), files fetched individually with
`git show`. No fetched code was executed. Clones deleted after the pass.

Each block answers the six questions and states **what was read** versus skimmed.

---

## 1. shenhuan2021/gudu-sql-omni-introduce

**Read:** full tree (16 files), `README.md`, `Topics`,
`articles/gudu-sql-omni-how-sql-lineage-works-offline-vscode.md`. Skimmed the other
article filenames.

**What it actually does.** Nothing executable. It is a folder of thirteen marketing
articles about a closed-source commercial VS Code extension called Gudu SQL Omni, sold
by Gudusoft — the company behind the SQLFlow lineage service. There is no parser, no
library, no example project, no code of any kind.

**Problem and for whom.** It solves a marketing problem for Gudusoft, not a technical
problem for a data engineer. The README's closing sections are a `Keywords` block
("SQL lineage, column lineage, data lineage, SQL parser, ETL debugging...") and a
request to star the repository — the shape of search-engine bait, not documentation.

**Moving parts.** `README.md` (a landing page), `Topics` (a bare list of ten GitHub
topic strings, apparently staged for the repo settings), and `articles/`. One article is
nested at `articles/articles/`, which suggests the tree is assembled rather than
maintained.

**Environment assumptions.** That the reader will install a proprietary VS Code
extension. The articles claim fully-local parsing across 30+ SQL dialects with no
upload — a genuine architectural claim about a product this repository does not contain.

**Deliberately not done.** It does not implement, demonstrate or open-source anything.
The README states plainly: "This repository is currently under construction."

**Maturity.** 2 stars, no licence, no language detected, created 2026-04-06, last pushed
2026-05-03 — one month of activity, then nothing for four months.

**The finding.** The source list described this as "column-level SQL parsing and lineage
from transformations". It is not that. The one thing of value is descriptive: the article
on offline lineage sets out the pipeline Gudu's engine uses — lexer/parser → AST →
semantic analysis (column mapping plus function dependency) → lineage graph — which is a
clear statement of how column-level lineage is derived in general, and is transferable as
a *description* even though no implementation is offered. Catalogue it so nobody spends a
second afternoon discovering the same thing.

---

## 2. HCAI-Lab-GT/capabilibara

**Read:** full tree (37 files), `README.md`, `CITATION.cff`, `hf_space/README.md`,
`hf_space/app.py`. Not read: `Capability_Provenance_in_Language_Models.pdf` (the paper
itself), the website JavaScript.

**What it actually does.** It hosts the *project website* for a COLM 2026 paper on
training-data attribution, plus a Hugging Face Space demo. It does not contain the
attribution pipeline. The README describes an intended `src/` layout
(`data_attribution/`, `dolma/`, `unlearning/`) — that directory does not exist in the
tree. What exists is `public/` (a Bulma static site with GSAP animations), the paper PDF,
a `dev-server.mjs`, a deploy script, and `hf_space/`.

**Problem and for whom.** The *research* asks which regions of a pretraining corpus are
load-bearing for a specific capability, and validates the answer by unlearning those
regions and measuring the damage. That is capability provenance, for interpretability
researchers. The *repository* currently serves the paper's audience, not its users.

**Moving parts, as described rather than shipped.** Dolma3 de-duplicated and classified
into WebOrganizer's 24 topic × 24 format taxonomy → a 5.68M-document stratified working
set across 576 bins → benchmark query gradients from OLMo3-7B Instruct, document
gradients from OLMo3-7B Base → gradient-based TDA via TrackStar (Bergson) → a signed
576×4 bin-level influence matrix → influence-targeted versus matched-random unlearning
(LoRA, NGDiff). Stated cost: ~37K H200-equivalent GPU-hours.

**Environment assumptions.** Python 3.12, uv, two vendored dependencies (Bergson,
ai2-olmes), and cluster-scale GPU. Nothing a workstation reproduces.

**Deliberately not done.** Document-level attribution scores are withheld by design; only
aggregate bin-level statistics are to be released. The README is honest about the gap — a
`code pending release` badge, a roadmap with the code port unticked, and every pending
section marked.

**Maturity.** 7 stars, 0 forks, created 2026-07-04, pushed 2026-08-23. AGPL-3.0 for code,
CC BY-SA 4.0 for website content. The arXiv paper (2606.19625) resolves. Pre-release.

**Two findings worth recording.**

1. **Canonical location moved.** `eilab-gt/capabilibara` returns a 301 redirect to
   `HCAI-Lab-GT/capabilibara`; the README's own clone command and badges still point at
   the old path. The path in the source list is the current one.
2. **The public demo renders synthetic data with no user-visible disclaimer.**
   `hf_space/app.py` line 31 reads
   `# Generate synthetic influence baseline data matching paper distributions for 576 bins`,
   followed by `np.random.seed(42)` and `np.random.randn(24, 24)` with hand-applied
   offsets. The Space's own README advertises a "Matrix Explorer" over "576 corpus bins"
   and an "Influence Breakdown" across four named benchmarks, and says nothing about the
   values being generated. The repository README is scrupulous about the code being
   unreleased; the demo is not scrupulous about the numbers being invented. Anyone citing
   a figure read off that heatmap would be citing `np.random.randn`.

---

## 3. syntax-tree/mdast

**Read:** full tree (7 files), the whole of `readme.md` (1,710 lines — it *is* the
specification), `package.json`.

**What it actually does.** It defines a data format. mdast is a specification for
representing Markdown as a syntax tree, written in a Web IDL-like grammar. There is no
parser here: the repository contains the readme, a logo, a package manifest, an `.npmrc`
and two CI workflows. Nothing else.

**Problem and for whom.** Every tool that transforms Markdown needs an agreed shape for
"a document". Without one, each tool invents its own tree and none of them compose. mdast
is the contract that lets the unified/remark ecosystem share hundreds of utilities. Its
users are tool authors, not document authors.

**Moving parts.** It extends **unist**, a generic syntax-tree format, and inherits its
utility ecosystem. Two abstract interfaces (`Literal`, `Parent`); nineteen concrete nodes
(`Blockquote`, `Break`, `Code`, `Definition`, `Emphasis`, `Heading`, `Html`, `Image`,
`ImageReference`, `InlineCode`, `Link`, `LinkReference`, `List`, `ListItem`, `Paragraph`,
`Root`, `Strong`, `Text`, `ThematicBreak`); four mixins (`Alternative`, `Association`,
`Reference`, `Resource`); one enumeration (`referenceType`). The piece that does the real
work is the **content model**: `FlowContent`, `ListContent`, `PhrasingContent` and
`Content` are type unions saying which nodes may contain which others. That is what makes
a tree checkable rather than merely traversable. Extensions for GFM, frontmatter and MDX
are documented as extensions, explicitly not as core.

**Environment assumptions.** None at runtime — it is prose. It assumes TypeScript users
will install `@types/mdast`, and that implementations live elsewhere.

**Deliberately not done.** It does not enumerate every Markdown extension ("It is not a
goal of this specification to list all possible extensions"), does not parse, does not
render, and does not tie itself to JavaScript despite the ecosystem being JavaScript.

**Maturity.** Mature and stable. 1,473 stars, created 2015-12-24, pushed 2026-02-04,
latest released version 5.0.0, zero open issues. The low change rate is the maturity
signal, not a decay signal — a released specification that stops changing is working.

**Licence, carefully.** The GitHub API returns **no licence** for this repository.
`package.json` says `"license": "MIT"` but is marked `"private": true` and versioned
`0.0.0` — it exists to run `remark` over the readme, not to publish a package. The
readme's own License section says **CC-BY-4.0 © Titus Wormer**. The document is the
artefact, so CC-BY-4.0 is the operative licence; it is a content licence rather than an
OSI software licence, and the note records both the API's silence and the readme's claim.

---

## 4. ganarajpr/awesome-dspy

**Read:** the whole repository — it is one file, `README.md`, 96 lines.

**What it actually does.** A curated link list about DSPy in the `awesome-*` format.
Roughly sixty links across Projects, Blogs/Articles, Twitter Threads, a Newsletter,
Videos, Tutorials and Papers.

**Problem and for whom.** Discovery. DSPy's own documentation covers the library; this
covers what people built with it and wrote about it. For someone deciding whether DSPy
suits a problem, the Projects section is the fastest survey available.

**Moving parts.** None. A single flat Markdown file with section headings, maintained by
pull request.

**Environment assumptions.** That the reader will go elsewhere. Every entry is an outbound
link; nothing is vendored or archived, so the list decays as its targets do.

**Deliberately not done.** It does not describe DSPy, does not rank or review entries, and
applies no visible inclusion bar — recent additions include a crypto-payment adapter and a
pay-per-call search API alongside the research projects, which is worth knowing before
treating the list as curated in the strong sense.

**Maturity.** 579 stars, 52 forks, created 2024-02-22, pushed 2026-06-17. Actively
accepting entries. **No licence at all** — the API returns none and there is no LICENSE
file, so reuse of the compilation is legally undetermined.

**The important distinction.** The source list described this entry as "programming
language models rather than prompting them". That is DSPy's thesis, and DSPy is
`stanfordnlp/dspy` — a different repository, which this one merely points at. Catalogued
as an aggregator; `stanfordnlp/dspy` is followed separately as a reference worth taking.

---

## 5. Victor-Kipruto-Rop/medallion-lakehouse-platform

**Read:** full tree (84 files), `README.md`, `src/transformations/bronze_to_silver.py`,
line counts across the core modules. Skimmed: Terraform modules, Great Expectations
suites, dbt models, CI workflows.

**What it actually does.** A complete, coherent skeleton of a medallion-architecture
lakehouse: Airflow DAGs orchestrating Bronze → Silver → Gold over PySpark and Delta Lake
on S3, dbt for the Gold marts, Great Expectations as the quality gate, Terraform for the
buckets and IAM, Docker Compose for a local Airflow/Postgres/MinIO stack, and GitHub
Actions for lint, test and deploy.

**Problem and for whom.** It answers "what does a full medallion stack look like when
every layer is present" — for someone assembling a first lakehouse who needs the *shape*,
including the parts that are easy to forget (quarantine paths, environment validation, a
production-hardening checklist, a rollback line in the deployment checklist).

**Moving parts.** `src/ingestion/extract_to_bronze.py` lands raw JSON partitioned
`year=/month=/day=`; `src/transformations/bronze_to_silver.py` explodes the records,
enforces `TRANSACTIONS_SCHEMA`, casts, deduplicates by key, and **splits invalid rows into
a `_quarantine/` path rather than dropping them**; `src/analytics/silver_to_gold.py`
builds the marts; `dags/medallion_etl_dag.py` sequences it with task groups; the Great
Expectations checkpoints gate each Silver and Gold write so a failed expectation halts the
DAG instead of propagating bad data.

**Environment assumptions.** AWS specifically — S3 buckets by name, EKS, ECR, `s3a://`
paths throughout; Spark 3.5 and Delta Lake 3.x; Airflow 2.x; environment variables
(`BRONZE_BUCKET`, `SILVER_BUCKET`) present at task runtime.

**Deliberately not done.** It carries one source (`payment_gateway`) and one table
(`transactions`). There is no streaming path, no catalogue, no lineage capture, no
multi-tenant story.

**Maturity — and the gap between claim and evidence.** The description says
"production-grade" and the README says it again. The repository was **created 2026-08-22
and last pushed 2026-08-23**: roughly eleven hours of history, 8 stars, 0 forks, 0 open
issues, **no licence file at all**. The core Python is around 500 lines. Nothing here is
wrong — the code that exists is clean, typed, structured, logged with `structlog`, and
tested — but "production-grade" describes the *shape* it imitates, not evidence of
production. Catalogue it as a reference implementation and say so, because a reader
filtering on the description would over-trust it.

**Transferable idea.** The quarantine split — invalid rows written to
`_quarantine/transactions/date=.../` and counted in a warning, rather than filtered away
silently — is the piece worth taking regardless of the rest.

---

## 6. snorkel-team/snorkel

**Read:** full tree (190 files), `README.md`, `CHANGELOG.md`, the whole `snorkel/`
package listing, `snorkel/labeling/model/label_model.py` (class docstrings and config).
Skimmed: `docs/packages/*.rst`. Not read: the tutorials repository, which lives
separately at `snorkel-team/snorkel-tutorials`.

**What it actually does.** It lets you build a training set without hand-labelling one.
You write *labelling functions* — small Python functions that vote a label or abstain on
each example, from a keyword, a regex, a heuristic, an existing model, a knowledge base
— apply them to unlabelled data, and Snorkel estimates how accurate each function is and
combines their votes into probabilistic labels you can train an ordinary model on.

**Problem and for whom.** Hand-labelling is the bottleneck in supervised ML, and it does
not survive a changed label definition — one taxonomy change and the whole set is stale.
Labelling functions are code, so they can be edited, reviewed, versioned and re-run. For
ML teams with domain experts but no annotation budget.

**Moving parts — and the repository is larger than its reputation.** Four subsystems, not
one:

- `labeling/` — the `@labeling_function` decorator, appliers with pandas, Dask and Spark
  backends, `LFAnalysis` (coverage, overlap, conflict, empirical accuracy), and
  `LabelModel`.
- `augmentation/` — transformation functions and sampling policies for data augmentation.
- `slicing/` — *slicing functions* that name a subset of the data, a slice-aware
  classifier, and a monitor. This is the least-known part and arguably the most
  interesting: it makes "performance on this named subset" a first-class, tracked object
  rather than an ad-hoc notebook check.
- `classification/` — a multi-task classifier with a trainer, checkpointer and schedulers.

**The mechanism that matters.** `LabelModel` (`labeling/model/label_model.py`) learns
`P(LF | Y)` — each labelling function's conditional probability of emitting the true
unobserved label — **without any ground truth**. Its docstring names the method: build the
junction tree of the LF dependency graph, compute the inverse generalized covariance
matrix, and complete it matrix-completion style against the empirical statistics (Ratner
et al., *Training Complex Models with Multi-Task Weak Supervision*, AAAI 2019). Accuracy
is recovered from the agreement and disagreement structure among the voters alone. By
default it assumes the LFs are conditionally independent given `Y`.

**Environment assumptions.** Python 3.11 exactly (0.10.0 removed every other minor
version), PyTorch, and a `numpy` label matrix in memory for the label model; the appliers
scale out, the model does not. Windows is explicitly discouraged in favour of Docker or
WSL.

**Deliberately not done.** It does not label for you — the functions are yours. It does
not train the end model for you in the general case (`classification/` exists, but the
documented path is "take the probabilistic labels elsewhere"). It has no active-learning
loop and no annotation UI.

**Maturity — with a caveat the star count hides.** 6,005 stars and heavy citation, but
the README's own top section is an announcement that the team moved to **Snorkel Flow**, a
commercial platform: "Moving forward, we will be focusing our efforts on Snorkel Flow."
The last real release in `CHANGELOG.md` is **0.10.0, 2023-02-27**, and its only breaking
change was adding Python 3.11 and dropping everything else — a compatibility release, not
a feature release. Apache-2.0, pushed 2026-06-08. The correct reading is a stable,
influential, effectively finished research library whose maintainers' attention is
elsewhere, not an abandoned one.

---

## 7. NorskRegnesentral/skweak

**Read:** full tree (67 files), `README.md`, `LICENSE.txt`, and the class structure of
every module in `skweak/` (`base`, `aggregation`, `generative`, `voting`, `analysis`,
`doclevel`, `gazetteers`, `heuristics`). Skimmed: the `examples/` NER and sentiment
pipelines.

**What it actually does.** The same weak-supervision idea as Snorkel, but for **spans in
text** rather than whole examples, and built directly on spaCy `Doc` objects. You write
annotators that mark spans with labels, then aggregate their disagreeing annotations into
one layer.

**Problem and for whom.** Named-entity and sequence-labelling tasks in domains or
languages with no annotated corpus — the README's framing is resource-poor languages and
task-specific labels with no pre-existing dataset. Its own examples are English CoNLL-2003
and MUC-6 NER plus **Norwegian** sentiment (NoReC), which is the case it was actually
built for.

**Moving parts.** The design separates three things cleanly, and the separation is the
interesting part:

- **Annotators** (`base.py`): `SpanAnnotator`, `TextAnnotator`, `CombinedAnnotator`.
  Concrete kinds in `heuristics.py` (`FunctionAnnotator`, `RegexAnnotator`,
  `TokenConstraintAnnotator`, `SpanConstraintAnnotator`, `SpanEditorAnnotator`,
  `VicinityAnnotator`) and `gazetteers.py` (a `Trie` plus `GazetteerAnnotator` for large
  dictionaries).
- **Aggregator shape** (`aggregation.py`): `TextAggregatorMixin` for whole-document
  labels, `SequenceAggregatorMixin` for token sequences, `MultilabelAggregatorMixin` for
  overlapping labels.
- **Aggregator method**: `voting.py` (majority) or `generative.py` (`NaiveBayes` for text,
  **`HMM` for sequences**, fitted by EM).

The HMM is the substantive difference from Snorkel. A sequence label depends on its
neighbours — `I-PER` after `B-PER` is likely, after `O` is not — so the aggregator models
transitions rather than treating each token as independent. `doclevel.py` adds
`DocumentHistoryAnnotator` and `DocumentMajorityAnnotator`, which propagate a decision
across a document: if "Barack Obama" was tagged `PERSON` in paragraph one, a bare "Obama"
in paragraph nine inherits the evidence.

**Environment assumptions.** spaCy ≥ 3.0 as the document model, `hmmlearn` ≥ 0.3, numpy,
pandas, Python ≥ 3.6. Some examples need downloaded spaCy pipelines. It assumes your data
can be represented as spaCy `Doc`s — that is not a light assumption, it is the whole
integration surface.

**Deliberately not done.** It does not train the final model; step 3 of its own procedure
is "use whichever framework you prefer". No augmentation, no slicing, no UI.

**Maturity.** MIT (Norsk Regnesentral, the Norwegian Computing Center), 926 stars, ACL
2021 system-demonstration paper. **The README states it plainly: "Skweak is no longer
actively maintained (if you are interested to take over the project, give us a shout)."**
Last push 2024-09-02, 7 open issues. Documentation lives in the GitHub Wiki, which is
outside the repository and was not read. This is a finished, unmaintained research
toolkit — usable, but nobody is coming to fix it.

---

## 8. urchade/GLiNER

**Read:** full tree (166 files), `README.md`, `docs/architectures.md`, the `gliner/`
package listing, `LICENSE`. Skimmed: `benchmarks/`, `configs/`, `docs/convert_to_onnx.md`.
Not read: the training code in detail, or the arXiv paper (2311.08526).

**What it actually does.** It extracts entities of *any type you name at inference time*,
from a small encoder model that runs on a CPU. You pass the text and a list of labels —
`["person", "date", "organization"]`, or `["reagent", "assay", "cell line"]` — and it
returns spans tagged with those labels. No fine-tuning, no training data, no predefined
label set.

**Problem and for whom.** Classic NER models are locked to the entity types they were
trained on; LLMs are flexible but expensive and large. GLiNER takes the third position:
zero-shot flexibility at encoder cost. For anyone extracting structured facts from text at
volume without a GPU budget or a labelled corpus.

**Moving parts.** `docs/architectures.md` sets out the mechanism concretely. In the
original **UniEncoderSpan**: entity labels and the input sequence are concatenated and run
through one BERT-like bidirectional encoder, separated by `[SEP]`, with a learned `[ENT]`
token before each label. The `[ENT]` output representations become the label embeddings
after a two-layer feed-forward refinement. Every candidate span up to length 12 is
represented from its first and last token embeddings. A span belongs to a label if the
sigmoid of their dot product passes a threshold, trained with binary cross-entropy. That
is the whole model — a similarity between a span vector and a label vector.

Nine variants extend it along three axes: **encoding** (uni-encoder shares context;
**bi-encoder** encodes labels separately so their embeddings can be *pre-computed*, which
is what makes 100+ label types viable), **prediction level** (span versus token/BIO, the
latter better for long entities), and **head** (plain, generative decoder for open-vocabulary
label discovery, or `Relex` relation layers for joint entity-and-relation extraction —
knowledge-graph construction in one pass). A `StreamingSpan` variant uses a causal decoder
with reusable prompt and text caches for incremental inference over live transcripts and
logs. `gliner/multitask/` adds classification, open extraction, question answering,
relation extraction and summarisation heads over the same backbone.

**Environment assumptions.** Modest ones, deliberately: `pip install gliner`, models
pulled from Hugging Face, CPU-first with INT8 quantisation, `torch.compile` and ONNX
export documented as first-class, optional Ray Serve for serving, a `Containerfile` in
`gliner/serve/`. It assumes network access to Hugging Face on first use.

**Deliberately not done.** It is extraction, not understanding — no coreference, no entity
linking to a knowledge base, no schema induction. The README pushes those to "the
Ecosystem", meaning other people's projects.

**Maturity.** Apache-2.0, 3,603 stars, 299 forks, created 2023-11-14 and **pushed
2026-09-03 — the day of this pass**. A published paper (arXiv 2311.08526), a documentation
site, a benchmark suite with recorded results (`benchmarks/bench_batch_decode_results.json`),
Discord and subreddit communities, and models on Hugging Face. Actively developed and
production-oriented; 96 open issues is proportionate to that traffic.

---

## 9. recipy/recipy

**Read:** full tree (171 files), `README.md`, `docs/how_does_it_work.rst`,
`docs/patched_modules.rst`, `CHANGELOG.md`, the `recipy/` package listing. Skimmed:
`integration_test/`.

**What it actually does.** You add `import recipy` as the first line of a Python script.
From then on, every file the script reads or writes is logged to a local database along
with the script path, arguments, Python version, git commit and origin, environment, and
any warnings. Later, `recipy search graph.png` tells you which run produced that file.

**Problem and for whom.** The researcher's version of "where did this come from" — you
have `graph.png` from six months ago and no idea which script, which inputs, or which
commit made it. For scientists and analysts working in scripts rather than pipelines, who
will not adopt a workflow engine.

**Moving parts, and this is the clever bit.** `docs/how_does_it_work.rst` is explicit:
recipy installs a patch object into `sys.meta_path`, so when a target library is later
imported, recipy wraps that library's reading and writing functions before the user's code
gets it. That is why `import recipy` must be the very first line — the hook has to be in
place before the import it intends to intercept. `docs/patched_modules.rst` lists the
targets function by function: `pandas` (`read_csv`, `to_csv`, `to_hdf`, …), `numpy`
(`loadtxt`, `save`, `savez`, …), `matplotlib.pyplot.savefig`, `lxml.etree`, `bs4`, `gdal`
(`Open`, `Driver.Create`), `sklearn` svmlight, `nibabel` across eight image formats,
`tifffile`, `imageio`. Storage is TinyDB — a pure-Python JSON store, chosen to remove the
MongoDB requirement earlier versions had. There is a CLI (`search`, `latest`, `annotate`,
`diff`) and a bundled web GUI.

**The idea worth keeping.** From v0.3.0: every input and output file is **content-hashed**,
and search is by hash rather than path by default. Send `graph.png` to a colleague who
renames it `RobinsGraph.png`, and its provenance still resolves. Identity by content, not
by location.

**Environment assumptions.** That your I/O goes through one of the patched libraries.
Built-in `open()` is *not* patched — you must use `recipy.open` instead — and the README
explains why: libraries use `open` internally, so wrapping it would log every file the
whole stack touched rather than the ones you meant.

**Deliberately not done.** It records *that* a file was read and a file was written, never
what happened in between. There is no column-level or field-level lineage, no DAG, no
transformation semantics. It is a run-level ledger, and it says so.

**Maturity — abandoned, and the evidence is unambiguous.** Apache-2.0, 435 stars, created
2015. The newest entry in `CHANGELOG.md` is **v0.3.0, 2016-09-13**. Last push 2022-01-12.
**90 open issues.** CI is `.travis.yml` and `appveyor.yml`, both long dead as free
services. The patched-module list is a 2016 snapshot of scientific Python — it names
`pandas.Panel` and `to_msgpack`, both removed from pandas years ago, so the patches for
them cannot bind. The documentation still discusses Python 2 encoding parameters. This is
a good idea in an unmaintained implementation: worth reading for the `sys.meta_path`
technique and the content-hash identity, not worth installing.

---

## 10. tree-sitter/tree-sitter

**Read:** full tree (616 files), `README.md`, `LICENSE`, `docs/src/5-implementation.md`,
`docs/src/using-parsers/queries/1-syntax.md`, the `docs/src/` and `lib/src/` listings.
Skimmed: `crates/` layout, `lib/binding_rust/`, `lib/binding_web/`. Not read: the C
runtime source itself.

**What it actually does.** Two things that the name conflates. It is a **parser
generator**: you write a grammar in a JavaScript DSL (`grammar.js`) and the CLI emits a
standalone C parser (`parser.c`). And it is a **runtime library**: `libtree-sitter`, plain
C with no dependencies, which uses those parsers to build a concrete syntax tree and — the
point of the whole project — *update* that tree incrementally when the source changes,
reparsing only what moved.

**Problem and for whom.** Editors and developer tools need a syntax tree of a file that is
being typed into: fast enough for every keystroke, and still useful when the file is
half-written and syntactically broken. Regex highlighting is wrong; a compiler front end is
too slow and gives up on errors. Its users are tool authors — editors, linters, code
navigation, anything that needs structure rather than text.

**Moving parts.** The CLI (`crates/cli`, `crates/generate`) evaluates `grammar.js` by
shelling out to `node`, normalises it to JSON against a published schema, and runs it
through the `prepare_grammar` transformations, which **split one grammar into two**: a
syntax grammar over non-terminals and a lexical grammar over terminals. Parse tables are
built from those, and emitted as C. The runtime (`lib/src/`) is the other half:
`subtree.c` and `reusable_node.h` hold the persistent tree structure that makes reuse
possible, `stack.c` is the GLR-style parse stack that handles ambiguity, `lexer.c` drives
the generated tables, and `get_changed_ranges.c` computes what an edit actually
invalidated. `query.c` implements a separate and independently useful capability: an
**S-expression query language** over the tree, with node types, named fields
(`left: (member_expression object: (call_expression))`), negated fields (`!type_parameters`),
captures and predicates. `crates/highlight` and `crates/tags` build syntax highlighting and
code-navigation tags on top of queries.

**Environment assumptions.** For the runtime, almost none — that is the design goal:
"dependency-free so that the runtime library (which is written in pure C) can be embedded
in any application". Bindings ship for Rust and WebAssembly in-tree. The *generator*
assumes Node.js, since grammars are JavaScript. There is one parser per language and it
must be compiled and loaded.

**Deliberately not done.** No semantics. Tree-sitter gives you a concrete syntax tree, and
nothing about types, name resolution, scope or cross-file relationships. That boundary is
what keeps it small and universal, and it is why everything downstream of it — semgrep
included — has to build its own semantic layer.

**Two observations from the structure rather than the README.**

1. **GitHub reports the language as Rust; the embeddable artefact is C.** The Rust is the
   generator and CLI, which the implementation notes say is "a build tool; it is no longer
   needed once a parser has been generated". Filtering this repository by language would
   mislead about what you would actually link against.
2. **The marquee feature is the least documented.** `docs/src/5-implementation.md` covers
   the CLI in detail and then ends: "## The Runtime — WIP". The incremental reparsing
   algorithm — the reason the project exists — is documented only in the C source.

**Maturity.** MIT, 26,847 stars, 2,856 forks, created 2013-11-06, **pushed 2026-09-03, the
day of this pass**. 99 open issues against that scale. A Zenodo DOI, a documentation book,
a playground, Discord and Matrix channels, ABI versioning documented
(`docs/src/using-parsers/7-abi-versions.md`). Infrastructure-grade and load-bearing for
much of the modern editor ecosystem.

---

## 11. Instagram/LibCST

**Read:** full tree (461 files), `README.rst`, `LICENSE`, the `libcst/` and `native/`
listings, `libcst/metadata/` and `libcst/codemod/` file lists. Not read: the node
definitions or the Rust parser source.

**What it actually does.** It parses Python into a tree that keeps **everything** —
comments, whitespace, parentheses, trailing commas — so you can modify one node and print
the file back out with every other line byte-identical. Python's built-in `ast` throws all
of that away, which is why `ast`-based rewriting reformats files it never meant to touch.

**Problem and for whom.** Automated refactoring across a large codebase. If a codemod
reformats every file it visits, the diff is unreviewable and the change will not land. For
anyone maintaining a codebase big enough that a rename has to be a program — which is the
problem Instagram had, and the reason this exists.

**The design compromise, in its own words.** A true concrete syntax tree is faithful but
unusable — every token, every trivia node. An AST is usable but lossy. LibCST's claim is a
"lossless CST that looks and feels like an AST": whitespace is not a sibling node but a
*field on the node it belongs to*, so `BinaryOperation(left=Integer(value='1'),
operator=Add(whitespace_before=SimpleWhitespace(' '), whitespace_after=...))`. You
navigate an AST-shaped tree and the formatting rides along attached to it.

**Moving parts — and the structure disagrees with the description.** The GitHub
description calls it "a concrete syntax tree parser and serializer library". By file count
the largest subsystem is not the parser:

- `libcst/codemod/` — **73 files**, the biggest. A codemod framework: `_command.py`,
  `_runner.py` with a process pool, `_context.py`, a CLI, a test harness, and a library of
  ready-made commands (`remove_unused_imports`, `rename`, `convert_percent_format_to_fstring`,
  `convert_union_to_or`, `convert_namedtuple_to_dataclass`, `add_trailing_commas`).
- `libcst/_nodes/` — 66 files, the node definitions.
- `libcst/_parser/` — 53 files, the pure-Python parser, partly derived from `parso`.
- `libcst/metadata/` — 29 files, and the underrated one. Providers that compute facts a
  syntax tree does not contain: `scope_provider` (name binding and scope), `name_provider`
  (qualified names), `position_provider`, `parent_node_provider`,
  `expression_context_provider`, and `type_inference_provider`, which shells out to **Pyre**
  for real type information. `full_repo_manager.py` runs providers that need more than one
  file.
- `libcst/matchers/` — 13 files, a declarative pattern-matching layer over the tree, so you
  express "an `Assign` whose value is a `Call` to `dict`" as data rather than nested `isinstance`.
- `native/` — a Rust parser (`native/libcst/`, with its own `Grammar` and benchmarks), the
  performance answer to the pure-Python one.

So: LibCST is a **codemod platform** whose parser is one component. Someone cataloguing it
as "a Python parser" would miss the part most likely to be worth borrowing.

**Environment assumptions.** Python 3.0 → 3.15 source is parseable (it parses versions
other than the interpreter running it, which is the point for a migration tool). A Rust
toolchain for building from source. `type_inference_provider` needs Pyre installed and a
configured project — the type metadata is opt-in and heavyweight.

**Deliberately not done.** It is Python-only, by design. It does not format
(that is Black's job), does not lint, and does not decide what to change — it gives you a
tree that survives modification.

**Licence, carefully.** The GitHub API reports **NOASSERTION / "Other"** because `LICENSE`
is a composite. Reading it: contributions are **MIT**; nine parser files derived from the
standard library and `parso`, plus two Rust tokenizer files, are **dual MIT and PSF**; and
`libcst/_add_slots.py`, taken from `dataclasses`, is **Apache-2.0**. All three are
permissive, so `license_class: Permissive` is right, but the field cannot simply say "MIT".

**Maturity.** 1,940 stars, 228 forks, created 2019-08-06, pushed 2026-08-11, 173 open
issues. Meta-maintained (the copyright is "Meta Platforms, Inc. and affiliates"), with a
`MAINTAINERS.md`, a documentation site, a Binder notebook tutorial, and a CI build matrix.
Production-grade and in continuous use.

---

## 12. semgrep/semgrep

**Read:** full tree (10,064 files), `README.md`, `LICENSE`, `COPYRIGHT`, `.gitmodules`,
the `src/`, `languages/` and `cli/src/semgrep/` listings. Not read: the OCaml engine
source, or the rule corpus (which lives in `semgrep/semgrep-rules`, a separate repository).

**What it actually does.** It searches code by structure instead of by text. You write a
pattern that *looks like the code you are looking for*, with `$X` for "any expression" and
`...` for "any sequence", and Semgrep matches it against the parsed program rather than the
characters. `$X = 1; $Y = $X + 1` finds the assignment however it is spaced, named or
parenthesised. Rules are YAML, and can compose patterns with `pattern-inside`,
`pattern-not`, and taint sources and sinks.

**Problem and for whom.** grep finds strings; a linter finds what its authors anticipated.
The gap is "I want to find every instance of *this specific shape* in our code, in six
languages, today" — an insecure deserialisation, a deprecated call, a policy violation. For
security engineers and platform teams who need enforceable, reviewable, version-controlled
rules.

**Moving parts.** A three-layer design, visible in `src/`:

- **Parsing to a shared shape.** `languages/` holds 37 language directories, and
  `.gitmodules` declares **36 tree-sitter grammar submodules**, all forks under
  `returntocorp`/semgrep. The forks exist because the grammar has to parse not only the
  language but *patterns written in that language* containing metavariables and ellipses.
  Everything is then normalised into `src/ast_generic` — **one generic AST all 37 languages
  map into** — which is what lets a single rule cross language boundaries.
- **Matching.** `src/matching` performs structural matching with metavariable binding;
  `src/il` is an intermediate language for analysis; `src/tainting` implements taint
  tracking from sources to sinks; `src/prefiltering` cheaply eliminates files that cannot
  match before the expensive work starts.
- **Everything around it.** `src/rule` and `src/metachecking` — rules that check rules;
  `src/fixing` — autofix; `src/sca` — dependency scanning; `src/spacegrep` and
  `src/aliengrep` — degraded generic matching for languages with no grammar;
  `src/osemgrep` — an OCaml reimplementation of the Python CLI, in progress alongside
  `cli/`, which is still the Python entry point.

**Environment assumptions.** Analysis is local by default and the README is emphatic:
"by default, code is never uploaded". A rule registry at semgrep.dev is fetched unless you
supply local rules. The build assumes OCaml plus opam plus Python — a genuinely awkward
toolchain, which is why almost everyone installs the binary.

**Deliberately not done — and this is the finding.** The README states it against its own
interest: "Semgrep Community Edition will miss many true positives as it can only analyze
code within the boundaries of a **single function or file**." Cross-file and cross-function
analysis, dataflow reachability, the AI triage assistant, and the 20,000+ proprietary rules
are all Semgrep AppSec Platform, not this repository. The open engine is real and useful,
but the capability that makes SAST accurate is deliberately held back. Anyone adopting the
open tool for security should read that paragraph before, not after.

**Licence.** **LGPL-2.1** (`LICENSE`, confirmed in `COPYRIGHT`: "GNU Lesser General Public
License (LGPL) version 2.1"). That is `Weak_Copyleft` — it does not fall under a permissive
constraint, and a `find_donor` query restricted to permissive licences must not return it.

**Maturity.** 16,500 stars, 1,047 forks, created 2019-12-13, pushed 2026-09-01. Default
branch is `develop`. 913 open issues, proportionate to a tool at this scale.
Commercially backed by Semgrep Inc., which is both why it is well maintained and why the
open/paid line sits where it does. Incidental observation: the repository ships an
`AGENTS.md` and a `CLAUDE.md` at top level, and `cli/src/semgrep/commands/mcp.py` — the
tool now has an agent-facing surface in-tree.

---

## 13. neo4j-labs/neocarta

**Read:** full tree (516 files), `README.md` (the first ~250 lines plus the CLI command
table), the `neocarta/` package listing including `_mcp/`, `_cli/`, `connectors/`,
`data_model/` and `enrichment/`. Skimmed: `assets/mermaid/`, `datasets/`, `.claude/skills/`.

**What it actually does.** It reads metadata out of your databases — table and column
names, foreign keys, sample values, business glossary terms, metric definitions, query
history — and builds a **semantic layer graph in Neo4j** from it. Then it serves that graph
to an AI agent as MCP tools, so the agent can find out what data exists, what it means, how
it joins, and which database holds it, before writing a query.

**Problem and for whom.** Text-to-SQL fails not because models cannot write SQL but because
they do not know the landscape: which of four `customer` tables is current, what `status_cd`
means, which warehouse to route to. Neocarta's answer is to make that knowledge a graph and
put it in front of the agent as a retrieval step. For teams putting agents in front of more
than one database.

**Moving parts.** Three stages, cleanly separated in the package:

- **Ingest** — `connectors/` for BigQuery (schema and logs), Databricks, Dataplex,
  Snowflake, JDBC, CSV, query logs, and OSI. Only metadata crosses into Neo4j; the data
  stays in the source.
- **Model** — `data_model/` is the interesting half, split by *kind of knowledge* rather
  than by source: `schema/rdbms` and `schema/lpg`, `glossary`, `governance`, `metadata`,
  `query`, `instance`, `osi`. Each has its own Pydantic models, its own README and its own
  checked-in mermaid diagram under `assets/mermaid/data_model/`.
- **Serve** — `_mcp/` exposes tools (`catalog`, `full_text_search`, `vector_search`,
  `hybrid_search`, `hybrid_business_term_search`, `osi_catalog`, `osi_definitions`,
  `osi_domain`) and — the structural detail worth copying — keeps the **Cypher in
  `_mcp/cypher/`, separate from the tool definitions in `_mcp/tools/`**. The query is data;
  the tool is the contract around it. `enrichment/embeddings/` adds optional vectors over
  chosen node labels via LiteLLM or OpenAI, which is what turns `vector_search` and
  `hybrid_search` on.

**Environment assumptions.** A running Neo4j with credentials in the environment; Python;
network access to whichever warehouse you connect; an embedding provider if you want
semantic search. It assumes Neo4j is acceptable as infrastructure — that is the largest
assumption in the project, and it is not negotiable, since the entire query layer is Cypher.

**Deliberately not done.** It does not move data, does not execute analytical queries
against the sources, and does not do the text-to-SQL itself — it supplies the context an
agent needs to do that well. The README is explicit that "only the metadata crosses into
Neo4j".

**Two further observations.**

1. **The OSI connector is bidirectional.** Every other connector ingests. The OSI connector
   both loads an [Open Semantic Interchange](https://github.com/open-semantic-interchange/OSI)
   YAML semantic model into Neo4j *and* exports a subgraph back out as spec-compliant YAML,
   preserving column ordering and `ai_context` structure. A semantic layer with a portable,
   text-diffable serialisation is a different proposition from one locked in a database.
2. **The repository ships Claude Code skills for its own contributors.** `.claude/skills/`
   contains `neocarta-add-source-connector` and `neocarta-add-connector-cli-command`, each
   with a `SKILL.md`, a written contract document, and a `driver.py`. Contribution
   conventions are expressed as agent-executable procedure rather than prose in
   CONTRIBUTING.md.

**Maturity.** Apache-2.0, 106 stars, 25 forks, created 2026-01-21, pushed 2026-08-24. On
PyPI. The README is emphatic about status: *"This library is not a Neo4j product. It is a
Neo4j Labs project supported by the Neo4j field team"*, with a `Status: Experimental` badge.
**Canonical location moved:** the CI badge points at `neo4j-field/neocarta`, and that path
now 301-redirects to `neo4j-labs/neocarta`. Young, well-organised, and explicitly
experimental — the documentation quality runs ahead of the maturity.

---

## 14. microsoft/graphrag

**Read:** full tree (908 files), `README.md`, the `packages/` layout, the full
`index/workflows/`, `index/operations/` and `query/structured_search/` listings,
`docs/` index. Not read: the operation source itself, or the GraphRAG arXiv paper
(2404.16130).

**What it actually does.** It turns a pile of unstructured documents into a knowledge graph
and a set of hierarchical summaries, so an LLM can answer questions that span the whole
corpus rather than the few chunks a vector search happens to return. Ask "what are the main
themes in this material" of ordinary RAG and it fails, because no single chunk contains the
answer. GraphRAG answers it from precomputed summaries of graph communities.

**Problem and for whom.** Sensemaking over a private corpus — narrative, investigative and
analytic work where the question is about the whole rather than a passage. For teams with
document collections and a budget for indexing.

**Moving parts.** The indexing side is a pipeline of named workflows
(`index/workflows/`), each a step: `load_input_documents` → `create_base_text_units` →
`extract_graph` → `finalize_graph` → `create_communities` → `create_community_reports` →
`generate_text_embeddings`, with a parallel `update_*` family for incremental re-indexing.
The operations underneath are where the design shows:

- **`extract_graph`** prompts an LLM to pull entities and relationships out of each text
  unit, then `summarize_descriptions` merges the many descriptions of the same entity into
  one.
- **`extract_graph_nlp`** and `build_noun_graph/` are the alternative, non-LLM path —
  noun-phrase extraction by CFG, regex or syntactic parsing, with a validator and stop-word
  list. Much cheaper, no model calls at graph-construction time.
- **`cluster_graph`** runs hierarchical community detection (Leiden), producing communities
  at several levels of granularity.
- **`summarize_communities`** writes a natural-language **community report** for each
  community at each level — the artefact that makes global questions answerable.
- `extract_covariates`/`claim_extractor` pulls claims attached to entities;
  `prune_graph` trims the result.

Query offers four modes (`query/structured_search/`): **local** (start from matched
entities and walk out), **global** (map-reduce over community reports), **drift** (dynamic
community selection combined with local search), and **basic** (plain vector search, for
comparison). Since the last restructure the repository is a monorepo of eight packages —
`graphrag-cache`, `-chunking`, `-common`, `-input`, `-llm`, `-storage`, `-vectors` and
`graphrag` itself — each independently versioned with its own notebooks.

**Environment assumptions.** An LLM API with real budget. The README carries its own
warning: "GraphRAG indexing can be an expensive operation, please read all of the
documentation to understand the process and costs involved, and start small." Intermediate
state is Parquet on disk, vectors default to LanceDB, configuration is a generated YAML plus
prompt files, and prompts are expected to be **tuned per corpus** — there is a whole prompt
tuning guide, and out-of-the-box results are explicitly not the best case.

**Deliberately not done.** It is not a serving layer, not a database, and not an agent
framework. It builds an index and answers questions over it.

**Maturity — and this is the headline.** 35,819 stars, 3,758 forks, pushed 2026-09-02 —
every popularity signal says thriving. The first line of the README says otherwise:

> "GraphRAG is a research project... Since our first release in July 2024 the capabilities
> of frontier models have changed dramatically... **This project is largely in maintenance
> mode, and won't be accepting new PRs or implementing new features.** We'll perform bug
> fixes and dependency updates as appropriate, particularly to address CVEs."

MIT licensed, and `RAI_TRANSPARENCY.md` plus "not an officially supported Microsoft
offering" are both present. The recent commits are maintenance, not development. Any
ranking signal that reads stars and `pushed_at` would score this as one of the most active
sources in this cohort; the README says it is closed to new work. That gap is the finding.

---

## 15. run-llama/llama_index

**Read:** full tree (9,848 files), `README.md`, the monorepo layout, the `llama_index/core/`
submodule listing with file counts, the `core/indices/` type listing, and per-category
integration counts. Not read: any individual implementation.

**What it actually does.** It is the plumbing between your data and a language model:
readers that load documents from anywhere, parsers that split them, several different
*kinds* of index over the result, retrievers and query engines that get relevant material
back out, and an agent/workflow layer that strings those into applications.

**Problem and for whom.** Every retrieval application needs the same twenty pieces —
loaders, chunkers, embedding clients, a vector store, a retriever, a reranker, a response
synthesiser, evaluation — and writing them is neither interesting nor differentiating. For
application developers building over private data.

**Moving parts — the part that earns its place here is the index taxonomy.** `core/indices/`
is the single largest core subpackage (93 files) and offers structurally different indexes,
not one index with options:

- `vector_store` — embeddings and similarity, the familiar one.
- `keyword_table` — keyword-to-node mapping, lexical.
- `list` (summary) — sequential, for "summarise everything".
- `tree` — hierarchical summaries built bottom-up, queried top-down.
- `document_summary` — retrieve by a summary of each document, then read the document.
- `knowledge_graph` and `property_graph` — triples and labelled property graphs.
- `struct_store` — over SQL and dataframes.
- `composability` — indexes composed *over other indexes*, and `objects`/`selectors`/
  `router` to route a query to whichever index suits it.

That is the "multi-tier indexing" claim made concrete: different structures answer different
question shapes, and a router chooses. Around it sit `node_parser` (25 files),
`response_synthesizers` (13, with refine/compact/tree-summarize strategies),
`postprocessor` (11, reranking and filtering), `evaluation` (25), `memory`, `agent`,
`workflow` (event-driven), and a separate `llama-index-instrumentation` package.

**The scale, measured.** `llama-index-integrations/` holds roughly 9,000 files across 300+
plugin packages: **1,941** files of readers, **1,144** of LLM adapters, **958** of vector
stores, **839** of tools, **683** of embeddings, 525 of storage, 260 of postprocessors, 143
of retrievers, 90 of graph stores. The core is a set of interfaces; the value is that
everything has already been adapted to them.

**Environment assumptions.** `llama-index-core` plus whichever integrations you install —
the namespace convention (`llama_index.core.x` versus `llama_index.x.y`) is how you tell
which you are using. Most paths assume a model API. It does not assume a particular vector
store, which is the point.

**Deliberately not done.** It is not a model, not a database, and not a UI. It also
deliberately does not pick for you — the breadth that makes it useful is the same breadth
that makes it heavy.

**Maturity.** MIT, 52,000 stars, 8,075 forks, created 2022-11-02, pushed 2026-09-03. 696
open issues. A `CITATION.cff`, a `STALE.md` policy, a `llama-dev` tooling package, and
per-package release automation.

**Description drift, worth recording.** The GitHub description reads "LlamaIndex is the
leading document agent and OCR platform". That describes **LlamaParse**, the company's
commercial platform, not this repository — which the README distinguishes carefully
("LlamaIndex OSS ... **Parse** is our enterprise platform"). Metadata-only classification
would file this as an OCR product. It is a retrieval framework.

---

## 16. open-metadata/OpenMetadata

**Read:** full tree (18,794 files), `README.md`, the whole of `ARCHITECTURE.md` Parts 1–2,
`LICENSE`, the `openmetadata-spec` schema tree, the `ingestion/src/metadata/pii/` listing,
the `skills/` listing, and top-level module file counts. Not read: any Java or TypeScript
source.

**What it actually does.** It is a metadata catalogue for an organisation's data: it crawls
your databases, warehouses, dashboards, pipelines and ML models; records what exists;
tracks **lineage** — which table feeds which, down to the column, derived by parsing query
logs and pipeline definitions; classifies sensitive columns automatically; holds a business
glossary and data contracts; and serves all of it over REST, a UI, and an MCP server.

**Problem and for whom.** In an organisation of any size nobody knows what data exists,
where it came from, who owns it, or what breaks if a column changes. For data platform and
governance teams — and, increasingly by its own framing, for agents: the description now
reads "the Open Context Layer for Data and AI".

**Moving parts.** `ARCHITECTURE.md` is unusually good and states the system in three paths:

- **Path A, an API request** — Dropwizard/JAX-RS resource in `service/resources/` →
  repository in `service/jdbi3/` (`EntityRepository`) → `CollectionDAO`/`EntityDAO` (129
  sub-DAOs) → MySQL/Postgres, fanning out to change events and a search index write.
- **Path B, an ingestion run** — a Python connector `<Name>Source` under
  `ingestion/.../source/`, resolved by `service_spec.py`, yields entities through a topology
  of producers and processors, and the sink **POSTs them to the same REST API**. The
  ingestion framework is a client, not a privileged path. There are 71 database connectors
  alone; the architecture doc counts 120+ overall.
- **Path C, a search query** — UI → `SearchResource` → `service/search/` (294 files) →
  Elasticsearch or OpenSearch through *shaded* clients relocated behind `es.*`/`os.*` so
  both can link simultaneously.

**The design decision that matters most.** `openmetadata-spec` holds **904 JSON Schemas**
(380 entity, 245 API, 121 type, 48 configuration, 48 metadata-ingestion, 32 governance…),
and the Java, Python and TypeScript models are all *generated from them*. The schema is the
single source of truth and the three language bindings cannot drift from it, because none of
them is hand-written. `openmetadata-ui/src/generated/` is described in the architecture doc
as "a pure sink" — nothing imports upward into it.

**Auto-classification, mechanically.** `ingestion/src/metadata/pii/` is not a regex list.
It combines Microsoft **Presidio** recognisers (with local patches and a recogniser
factory), a NER pass (`ner.py`), column-name patterns (`column_patterns.py`), engineered
features (`feature_extraction.py`), a **`tag_scoring.py`** stage and a
**`conflict_resolver.py`**. That is the weak-supervision shape — many noisy labellers,
scored and reconciled — arrived at independently, in a data catalogue rather than an ML
library.

**Environment assumptions.** Substantial: a JVM, MySQL or Postgres, Elasticsearch or
OpenSearch, and Airflow for scheduled ingestion. Docker Compose and a Kubernetes operator
are both provided because the dependency set makes manual installation impractical. This is
a platform, not a library.

**Deliberately not done.** It stores metadata, never the data. It does not transform or
query your warehouse; it describes it.

**Maturity.** Apache-2.0, 15,098 stars, 2,353 forks, created 2021-08-01, **pushed
2026-09-03**. ~3 GB repository. 900 open issues at that scale. `THREAT_MODEL.md`,
`INCIDENT_RESPONSE.md`, a `.snyk` policy, an ADR, integration tests as a first-class module.
Commercially backed by Collate. Production-grade.

**Two observations about the repository as an artefact, not the product.**

1. **`ARCHITECTURE.md` states its own provenance.** "Structural claims trace to the measured
   module graph or a file path; numbers come from a read-only audit of this tree (module
   edges from the POMs; package/import counts by grep/Tarjan)." It gives a "look here first"
   column per module, and it names where layering *fails* — "the packages are **not**
   acyclically layered" — instead of describing an intended architecture. That is a
   documentation pattern, and a rare one.
2. **The project ships an agent plugin for its own contributors.** `skills/` (184 files) is
   a `.claude-plugin` with skills for connector building, connector auditing, code review,
   TDD, systematic debugging, Playwright validation and PR checklists, alongside `AGENTS.md`,
   `CLAUDE.md`, `.claude/rules/` and an `openspec/` directory. Contribution standards as
   executable procedure rather than prose.

---

## 17. PHACDataHub/data-mesh-ref-impl

**Read:** full tree (1,152 files), `README.md`, `kg/README.md`, `paradire/doc/README.md`,
`paradire/analytics/acg/README.md`, directory file counts. Not read: the TypeScript or
Python sources, or `paradire/doc/part-i.md` through `part-iv.md`.

**What it actually does — and it is not one thing.** The name says "Data Mesh Reference
Implementation". The structure says: six unrelated proof-of-concept projects from the
Public Health Agency of Canada's Data Management and Innovation area, each with its own
Docker Compose stack, scripts and README, sharing no code:

| Case | Files | What it is |
| --- | --- | --- |
| `paradire/` | 544 | Federated health analytics across 13 provincial/territorial clusters and one federal cluster |
| `movie/` | 117 | A plug-and-play NLP cluster for movie recommendation |
| `nlp_pipeline/` | 115 | The GPHIN NLP pipeline with human analysts in the loop |
| `usvdm/` | 108 | Vaccination data management with in-stream Kafka event processing |
| `faers/` | 97 | Loading and exposing FDA Adverse Event Reporting System data |
| `pipelayer/` | 79 | Pipeline tooling |
| `kg/` | 65 | A knowledge graph built from the Disease Ontology in Neo4j |

There is no shared data-mesh framework and no deployable product. "Reference
implementation" here means "worked examples", and reading it as a template to adopt would
be a mistake.

**Problem and for whom.** Public-health data sharing across jurisdictions that cannot pool
their data — a real constraint that produces an unusual architecture. For government data
architects with the same problem.

**The transferable idea: the Access Control Gateway.** PARADIRE's `analytics/acg/` is the
piece worth the visit. A province keeps its data; the federal government sends analytics
queries; the ACG sits between them as a Kafka worker and enforces **field-level
transformation rules defined in a YAML ruleset that is compiled into a GraphQL schema, with
the policy expressed as custom directives**: `@hash` (one-way hash the field), `@restrict`
(replace the value with `** restricted **`), `@selectable` (remove the field entirely),
`@date` (coarsen a date to a format mask), `@topic` (bind a query to a Kafka topic). The
ruleset is **reconfigurable at runtime** by posting to the `acg-config-connector` topic, and
the gateway is deliberately decoupled from both ends, connecting only to the two event
brokers.

The design move is that the *policy is a schema*, not a body of code. What a partner may ask
and what they may receive is a typed, diffable, reviewable artefact — and the same artefact
is the API contract. The documentation is genuinely good: `paradire/doc/` is four parts,
each with a declared audience, and Part IV is "Looking forward with hindsight", a written
review of what was not achieved.

**Environment assumptions.** Heavy and specific. The knowledge-graph case opens with "you
need to setup a VM in the cloud with at least a Nvidia T4 GPU". PARADIRE assumes fourteen
Kubernetes clusters, Kafka on each, Neo4j, GraphQL gateways and a FHIR server. Nothing here
runs on a laptop.

**Deliberately not done.** No case is generalised, none is packaged for reuse, and there is
no attempt to extract a common framework from six attempts at similar problems.

**Maturity.** Apache-2.0, 8 stars, 3 forks, created 2023-01-25, **last pushed 2025-01-14 —
roughly twenty months stale at the time of this pass**, 9 open issues. Real institutional
work with real documentation behind it, no longer being touched. Read PARADIRE's Part II for
the gateway design; do not expect the code to run.

---

## Cross-cutting observations from the pass

**Four of the seventeen are not what a metadata filter would say they are.** `capabilibara`
is a website, not a pipeline. `gudu-sql-omni-introduce` is marketing copy, not a parser.
`graphrag` is in declared maintenance mode behind 35.8k stars and a same-week push.
`llama_index`'s GitHub description advertises the company's commercial OCR platform rather
than the framework in the repository. In each case the structure was the honest signal and
the description was not.

**Three are explicitly finished or unmaintained, and say so in their own README:** skweak
("no longer actively maintained"), graphrag ("largely in maintenance mode"), snorkel (the
team "focusing their efforts on Snorkel Flow"). `recipy` says nothing but has not shipped a
release since 2016. That is four of seventeen — an unusually high proportion, and a reason
the catalogue's `pushed_at`-based vitality signal needs the README read alongside it.

**Two canonical locations had moved.** `eilab-gt/capabilibara` → `HCAI-Lab-GT/capabilibara`
and `neo4j-field/neocarta` → `neo4j-labs/neocarta`, both via 301. In both cases the
repository's own README still points at the old path.

**Three independently arrived at the same shape.** Snorkel's `LabelModel`, skweak's HMM
aggregator, and OpenMetadata's PII classifier all take many unreliable labellers, score
them, and reconcile the conflict. Only two of the three call it weak supervision.

**Two of the seventeen ship agent instructions for their own contributors** — OpenMetadata's
`skills/` plugin (184 files) and neocarta's `.claude/skills/` connector recipes — and a
third, semgrep, carries `AGENTS.md` and `CLAUDE.md` at top level. That was not something
this pass set out to look for.
