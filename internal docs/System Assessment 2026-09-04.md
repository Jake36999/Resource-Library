---
type: "assessment"
status: "active"
created: "2026-09-04"
purpose: "what is actually built, what is missing, and what it would take to beat writing this from scratch"
resources: 128
---

# System Assessment 2026-09-04

## What Was Measured, Not Argued

Every number below came from the running system on 2026-09-04, not from the
documentation. That distinction turned out to matter more than expected.

| Claim in the docs | What the system holds |
| --- | --- |
| A scouting pipeline: discover → rank → evaluate → deep dive → intake | `solutions_library.sqlite` holds **41** resources; the vault holds **128**. `ingestion_runs: 1` |
| Optional embeddings, model available | `embedding` rows: **0** |
| Access-point extraction | `access_point` rows: **0** |
| Graph communities, graphify available | `note_community` rows: **0** |
| Mode D workbench, `close` refuses without a record | `.utility/workbenches/`: **empty** |
| Application records carry the only original knowledge | **4** records against 128 resources |

## The Largest Finding: The Documented Pipeline Did Not Build The Library

Both 2026-09 cohorts — 113 of the 128 resources — were charted by ad-hoc
scripts written in a scratchpad and deleted afterwards. The intake pipeline
that [[Service Map]] describes has run **once**, over a third of the corpus.

This is not a small documentation defect. It means:

- The write path is **unexercised at scale**. It has tests, it has degradation
  paths, and it has never survived contact with 49 repositories in one run.
- The method that actually works — fetch metadata under a rate limit, blobless
  clone, `ls-tree`, classify paths into signals, author against the tree — is
  now recorded in `.Data/surveys/` as *output* and in
  [[Scouting Working File 2026-09-04]] as *prose*, but **not as code anyone can
  run**. The next cohort starts by rewriting it.
- [[Data Information Knowledge]] says the data layer should outlive the
  conclusions drawn from it. That is now true of the survey files and false of
  the surveyor.

**This is the first thing to fix**, and it is mostly a promotion rather than a
build: the scratchpad scripts worked, and the shape they proved should become
`scout.survey` alongside `scout.rank`.

## Three Services That Are Built, Available, And Have Never Run

`embed`, `access_points` and `graph` each have code, tests and a documented
degradation path, and each has zero rows in the index. LM Studio and graphify
are both installed and reachable — so this is not a blocked capability, it is an
unrun one.

The honest reading is that they were built because the specification listed
them, not because a measured need appeared. Two of them have a defensible case
for running now and one does not:

- **`embed`** — worth running, and worth running *as an experiment with a
  result*, because the eval already showed embeddings changed nothing on those
  twenty questions. The scenario test is a different instrument and might
  disagree. `librarian relevance` can now settle it.
- **`graph`** — communities over 343 notes would say whether the topic taxonomy
  a person assigned matches the structure the links imply. That is a real
  question and nothing else answers it.
- **`access_points`** — no demand has appeared. Leaving it unrun and saying so
  is better than running it to make a number non-zero.

## Missing Components

Ordered by what each would actually change.

### 1. Freshness — nothing re-checks anything

All metadata was captured on three days. 39 of 128 notes carry no
`metadata_captured_at` at all. `github_pushed_at` is a snapshot, `archived` is a
snapshot, and a repository archived tomorrow stays `Active` here indefinitely.

This is the single mechanism that separates a catalogue from a photograph of
one, and its absence is what will make this system wrong rather than merely
incomplete. **`dbt source freshness` is the closest thing already catalogued** —
[[dbt-labs - dbt-core]] treats staleness as a first-class, testable property of
a source rather than as an operational chore.

A minimal version is cheap: one conditional-request API call per source per
week, comparing `pushed_at` and `archived`, writing a `freshness` row into the
data layer and warning when a note's claim and the world diverge. It costs no
prose and it never edits a note — it reports.

### 2. Query understanding — the ask is not separated from its context

`config-validation-surface` fails under **every** ranking configuration in
`rank_configs.json`. Its description names a storage engine and a query layer as
explicitly *out of scope*, and those terms drive the result. No corpus-side knob
fixes this because the problem is not in the corpus.

Every genuine request contains context that is not the request. Two things
already in the library address exactly this: [[urchade - GLiNER]] does zero-shot
entity extraction and could be pointed at the **query** rather than at documents,
and [[guillaumegenthial - sequence_tagging]] is the readable statement of why
sequence labelling needs a structured output layer. Neither has been tried here.

### 3. No feedback from use back to ranking

`record_application` is the one write Mode C permits, and there are four
records. Nothing learns from what was actually opened, taken or rejected.

This is the difference between a search engine and a search box.
[[elastic - elastic-labs]] ships a learning-to-rank corpus and a relevance
workbench for precisely this loop; the workbench half has been adopted here and
the feedback half has not.

### 4. No near-duplicate detection across sources

`distinct_resource_prose` catches two notes that could be swapped. Nothing
catches two *sources* that do the same job. At 128 that is manageable by memory;
at 400 it is not, and the failure is silent — the catalogue simply starts
answering one question with three entries that are the same answer.

[[asreview]] is the reference: deduplication is a named stage of systematic
review, before screening, because reviewers cannot be trusted to notice.

### 5. The catalogue does not apply its own lineage topic to itself

[[Topic - Data Lineage & Provenance]] holds eight sources about attributing an
artefact to the inputs that produced it. Meanwhile a note's claim that a
repository has 4,521 grammar files is traceable to `.Data/surveys/` only by a
human reading both. There is no machine-readable link from an information-layer
claim to the data-layer row supporting it.

[[Data Information Knowledge]] asserts the layering; nothing enforces it. A
`claim → survey row` link would make `**Not read:**` checkable rather than
merely honest.

### 6. The knowledge layer is 3% populated

By the system's own model, application records hold the only knowledge that did
not come from a source's own claims. Four records against 128 resources means
the catalogue is almost entirely *information* — accurate, well-evidenced, and
still second-hand.

This is not a component to build. It is a consequence of the system never having
been used in anger, and it will close by use or not at all.

## Composite Analogues Worth Comparing Against

Grouped by the function they perform as a whole, which is the level this system
should be compared at. **Only two of the six are catalogued**, and that is a
coverage gap in exactly the class most useful to this project.

| Grouped function | Composite systems | In the library? |
| --- | --- | --- |
| Catalogue entities, own them, document them, score them | **Backstage** (Software Catalog + TechDocs + Scorecards) | **No** — the closest whole-system analogue and it is absent |
| Ingest → classify → describe → search → lineage → govern | **OpenMetadata**, DataHub, Amundsen | [[open-metadata - OpenMetadata]] only |
| Search → screen → stopping rule → extract → record | **asreview**, Covidence, Rayyan | [[asreview]] only |
| Index → query understanding → retrieve → rank → rerank → evaluate | Elasticsearch, Solr, **Vespa** | [[elastic - elastic-labs]], [[DiceTechJobs - SolrConfigExamples]]; Vespa absent |
| Ingest → chunk → embed → retrieve → rerank → synthesise → cite | **llama_index**, **rtfm**, Haystack | [[run-llama - llama_index]], [[roomi-fields - rtfm]] |
| Inventory → watch upstream → alert on change | **Renovate**, Dependabot, OSV | **No** — and this is the freshness gap |

The two rows with no entry are the two capability gaps named above. That is not
a coincidence: **the catalogue's blind spots and its coverage gaps are the same
list**, which is itself an argument for scouting against a map of grouped
functions rather than against seed queries.

**Backstage is the highest-value single addition.** Its Software Catalog models
entities, ownership and relationships; TechDocs keeps documentation next to what
it documents; Scorecards assert quality properties declaratively. All three map
onto services here, and it is the only system in this table built for the
*same* job — an internal catalogue people are meant to actually use.

## What It Would Take To Beat Vibe-Coding This

The fair comparison is a weekend build: point something at a list of
repositories, embed the READMEs, expose a chat box. Being honest about where
that wins matters more than listing where this one does.

### Where this already wins, and would keep winning

- **It is measured.** Two instruments, 30 scenarios, a ranking workbench that
  cannot confuse a ranking change with a corpus change. A weekend build has no
  idea whether it works, and no way to find out.
- **Descriptions come from surveyed trees, not READMEs.** That is why the notes
  can say [[hamelsmu - code_search]] is 97% vendored fastai and
  [[ardamavi - Unsupervised-Classification-with-Autoencoder]] is 1,399
  photographs. No README says that, so no README-embedding system can.
- **Constraints eliminate and answers carry evidence.** `why` is assembled from
  what matched and is never generated, so a wrong answer is diagnosable.
- **A structural data layer.** 113 surveys, filterable without reading prose.
- **Named policies with tests.** `LOCATE_DO_NOT_ADJUDICATE` exists because the
  same defect appeared three times; a weekend build repeats it silently.

### Where it currently loses

- **Currency.** A vibe-coded tool hitting the GitHub API live is *more accurate
  about today* than this is. This is the freshness gap, and it is the one that
  matters most.
- **Coverage.** 128 sources against all of GitHub. For a question the catalogue
  does not cover, a web search wins outright — and the catalogue cannot
  currently *say* it does not cover something, except through the scenario test.
- **Cost of adding a source.** Currently a manual authoring pass. A weekend
  build ingests a URL in seconds. The quality difference is real and so is the
  throughput difference.
- **The knowledge layer.** Four application records. A tool nobody has used is
  not yet better than a tool nobody has built.

### The shortest path to a tool that is genuinely better

1. **Promote the surveyor to code.** `scout.survey` — the method that actually
   built the library, runnable. Closes the throughput gap and makes the write
   path real.
2. **Add freshness.** Weekly conditional re-check, `freshness` rows in the data
   layer, an integrity warning when a note's claim and the world diverge.
   Closes the currency gap, which is the one a weekend build wins on.
3. **Answer "I do not cover this".** A coverage report from the component store
   plus the scenario misses, so a query with no good answer says so instead of
   returning its best four irrelevant notes. This is what makes it safe to trust.
4. **Query understanding.** Separate the ask from its context. One measured
   experiment with GLiNER over the query, settled with `librarian relevance`.
5. **Use it, and record four more applications.** Nothing else moves the
   knowledge layer.

Items 1–3 are what turn this from a well-built snapshot into a tool. Items 4–5
are what make it better than the alternative rather than merely more careful
than it.

## Related
- [[Data Information Knowledge]] — the layering these gaps are described against
- [[Service Map]] — the inventory this assessment was checked against
- [[Design Specification]] — the policies, including `LOCATE_DO_NOT_ADJUDICATE`
- [[System Implementation Status]] — what was built, and when
- [[Master Index]]
