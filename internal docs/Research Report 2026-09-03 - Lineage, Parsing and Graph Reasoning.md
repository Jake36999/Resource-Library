---
type: "research_report"
status: "active"
created: "2026-09-03"
sources_examined: 17
sources_catalogued: 17
domains_added: 1
topics_created: 3
authority: "advisory - this report proposes; [[Design Specification]] governs"
related_working_file: "[[Scouting Working File 2026-09-03]]"
---

# Research Report 2026-09-03 - Lineage, Parsing and Graph Reasoning

## What This Is

Seventeen repositories were scouted and catalogued across five clusters: lakehouse and
lineage, structural parsing, weak supervision, graph reasoning, and provenance. Phase one
documented all seventeen before any judgement was formed about usefulness. This is phase
two: what any of it means for this system.

Every repository is now a resource note. The per-source evidence — what was read versus
skimmed, and the six questions answered for each — is in
[[Scouting Working File 2026-09-03]]. That file is the record this report is built on, and
where a claim here is thinner than it sounds, that file says so.

**Method.** One GitHub REST call per source for metadata (no `GITHUB_TOKEN`; 60 requests
per hour). Structure read from a depth-1 blobless clone, with individual files fetched by
`git show`. **No fetched code was executed** — Docker is not running on this host, so no
workbench was available and none was needed. Clones were deleted afterwards.

**What changed in the vault.** 17 resource notes, 22 glossary terms, 11 patterns, 3 topic
indexes, 1 new domain key (`code_intelligence`, on approval), 17 rows appended to
[[Taxonomy Index]], and route-map updates in [[Master Index]]. `librarian index` counts 264
notes and 2,053 chunks; `librarian integrity` reports **0 errors** and 29 warnings, all of
them pre-existing `taxonomy_matrix_agrees` drift on notes this pass did not touch.

**One thing got worse, was investigated, and is now fixed.** `librarian eval` held hit@5
1.00 (20/20) and recall@5 0.97 after the pass, but **MRR fell 0.91 → 0.84**. That was not the
new notes competing — it exposed two pre-existing defects in the read path. Both have been
repaired and the eval now reports **MRR 0.93**, above the pre-pass baseline on a corpus a
quarter larger. See §0; it is the highest-value finding in this report and it came from
checking the damage rather than from any source.

---

## 0. The Finding The Pass Produced By Accident

This was not on the list. It came out of checking whether the pass had damaged retrieval, and
it is the cheapest high-value item in the report.

`librarian eval` scores hit@5 1.00 and recall@5 0.97 before and after, but MRR dropped 0.91 →
0.84. Three questions with known answers slipped to rank 4. The obvious hypothesis — that
seventeen new notes are legitimately competing — is wrong. Running the worst case by hand:

```
query donor "run twelve dependent jobs nightly and recover from partial failure ..."
  [resource] run-llama - llama_index   1.000
      why: matched 'run' in the note name
  [resource] recipy - recipy           0.522
      why: matched 'run' in ## Semantic Links
  [resource] asreview                  0.510
      why: matched 'partial' in ## Integration & Use Cases
  [resource] apache - airflow          0.509
      why: matched 'jobs', 'recover', 'partial', 'failure' in ## What It Solves
```

The correct answer matched **four** query terms in the section that describes what it solves,
and lost to a note whose *filename* contains the token `run`. Two separate defects, both
pre-existing, both invisible until the corpus grew:

**Defect 1 — a name match on any single token outranks a four-term body match.** `run-llama`
contains `run`. Nothing weights a name hit by how discriminating the matched token is, so a
stopword-grade match on a filename takes first place outright.

**Defect 2 — 17% of the searchable corpus is boilerplate.** Of 2,053 indexed chunks, **346 are
pure link and metadata blocks**: 88 `## Semantic Links`, 81 `## Evidence`, 81
`## Evidence Anchors`, 81 `## GitHub Snapshot`, 15 `## Related`. These contain no prose. They
can only ever produce spurious matches — which is exactly how `recipy` took second place, by
matching `run` inside a list of wiki-links. The `why` string reported it honestly, which is
how it was caught; the explain-every-result rule earned its keep here.

**The fix, and it is now applied.** `notes.py` gained a `NON_PROSE_HEADINGS` set that
`chunk_note` skips, and `consult.by_name` gained two things it lacked: an ordering by match
quality, and a qualification rule. Hits were previously ordered by *whatever order SQLite
returned the rows in*, and that position becomes the RRF rank — so row order was silently
deciding relevance.

The qualification rule took two attempts, and the second is the interesting one. The first
version asked only how much of the **query** a single-term name hit covered, which correctly
rejected `run` in `run-llama` — and also broke an existing test asserting that
`orient("plumbing scheduler queue")` reaches `Topic - Plumbing`, which matches one term of
three, the same coverage. That test was right and the rule was too blunt. The rule now asks
both questions: a single-term name hit qualifies when the term is most of what was **asked
for**, *or* most of what the note is **called**. `plumbing` is most of `Topic - Plumbing`;
`run` is a sixth of `run-llama - llama_index`.

**Measured, one variable at a time, on the same 264-note corpus with vectors out of the
picture:**

| Configuration | hit@5 | recall@5 | MRR | chunks |
| --- | --- | --- | --- | --- |
| Baseline (both defects present) | 1.00 | 0.97 | 0.84 | 2,057 |
| Chunking fix only | 1.00 | 0.97 | **0.77** | 1,342 |
| Name-match fix only | 1.00 | 0.97 | 0.86 | 2,057 |
| **Both** | 1.00 | 0.97 | **0.93** | 1,342 |

**The chunking fix alone makes retrieval worse, and that is the most useful thing in this
table.** Removing 715 boilerplate chunks shrinks the text ranking, which hands *more* relative
weight to the name ranking — the very ranking that was broken. The boilerplate was partially
masking the name-match defect by giving the text side more mass. They are not two independent
improvements that happen to compose; the first is only safe once the second is in place. Ship
them together or not at all.

0.93 is also **above the 0.91 the README recorded before this pass**, on a corpus a quarter
larger. `hit@5` and `recall@5` were already saturated and did not move; MRR was the only
instrument that could see any of this, which is an argument for keeping a metric that is not
yet at ceiling.

**Verification.** 109 librarian tests and 48 scout tests pass (157 total, up from 150 — seven
new tests pin these decisions). Two of the new tests were confirmed to **fail** with the fixes
disabled and pass with them, so they discriminate rather than merely describe. `integrity`
reports 0 errors.

**Why this ranked above everything else in this report.** It was a defect in the read path,
degrading every query rather than one query kind; the fix was an afternoon; and — unlike every
other candidate here — the instrument to prove it already existed and already had a baseline.
It also means the pre-existing MRR figure understated what filters and FTS5 can do, which
strengthens §2.1's argument that vectors are not the next investment.

**Confidence: high.** Measured directly, four configurations, against this vault.

---

## The Short Version

Ranked by expected value to this system, not by how impressive the source is.

| # | Candidate | Source | Value | Cost | Confidence |
| --- | --- | --- | --- | --- | --- |
| 1 | ~~Stop indexing link blocks; qualify name matches~~ **— applied** | Measured in this pass (§0) | MRR 0.84 → 0.93; 35% of the chunk corpus was boilerplate | Done | High — measured in four configurations |
| 2 | ~~Resolve composite licences from the LICENSE file~~ **— applied and backfilled** | Observed across LibCST, mdast, semgrep | `Unknown` fell from 52 of 81 to 11; permissive-constrained queries went from offering 24 resources to 54 | Done | High — 52 repositories read; see [[Licence Resolution 2026-09-03]] |
| 3 | ~~Regenerate derived views deterministically~~ **— applied** | Observed in this pass | `librarian views`; integrity went from 29 warnings to 0 | Done | High — idempotent, tested |
| 4 | Community reports over the vault graph | microsoft/graphrag | A capability the system has no equivalent for | Small-medium | Medium-high |
| 5 | ~~A written content model for note types~~ **— applied** | syntax-tree/mdast · open-metadata/OpenMetadata | `NO_SCHEMA_DRIFT` is now enforced by four checks reading [[Note Content Model]] | Done | High — each check verified to fire on a deliberate break |
| 6 | Estimate ranking-signal reliability instead of hand-setting weights | snorkel-team/snorkel | Replaces six hand-tuned numbers with measured ones | Medium | Medium |
| 7 | semgrep as a registered workbench action | semgrep/semgrep | `find_technique` gains real evidence instead of description | Medium | Medium |
| 8 | Zero-shot extraction for access points | urchade/GLiNER | Extends a regex extractor that is at its ceiling | Medium | Low-medium |
| 9 | ~~Detect moved canonical URLs~~ **— applied** | Observed in capabilibara, neocarta | Prevents silent duplicate candidates and dying canonical URLs | Done | High — hit twice in seventeen |

Everything else in the cohort is a **deliberate rejection**, argued in section 6.

Items 1, 2, 3 and 9 are **done** — applied, measured and covered by tests. Every correction
to something already built is now closed. Items 4–6 are new capability; items 7–8 are gated
on the workbench and on a model being reachable, neither of which is true on this host
today.

**One consequence of item 2 needs a decision, and is recorded in §11.** The resolver works,
but the catalogue was never backfilled: **52 of 81 resources still carry
`license_class: Unknown`**, including react, prometheus, sympy, gdal and bootstrap. Until
that backfill runs, `find_donor` with a permissive constraint is refusing two thirds of the
catalogue.
The detail for each is in section 5, whose subsections are numbered independently of this
ranking; the rank is named in each heading.

---

## 1. Where A Source Does Something This System Has No Equivalent For

### 1.1 Community summarisation — graphrag

Spec §4B.1 permits community detection over the vault's own link graph, and `graph.py`
implements it. Communities are computed, stored in the index, and used advisorily. There
the capability stops.

graphrag does one more thing, and it is the thing that makes graph retrieval work:
`summarize_communities` writes a **natural-language report for each community at each level
of the hierarchy**, and `global_search` answers whole-corpus questions by map-reducing over
those reports. The insight is not the graph. It is that a question like *what is in here*
has no answer in any single node, so the answer must be precomputed at the level of the
cluster.

This system has the same shaped gap. `orient()` returns topics, resources and aggregators —
all things somebody assigned. A community that nobody assigned, spanning three topics, has
no description and therefore cannot be returned. The catalogue can say what is where; it
cannot say what it has become.

**Not a contradiction of `GRAPH_ADVISORY_ONLY`.** A community report is an observation
written down, exactly like the community assignment it describes. It creates no topic,
renames nothing, and lives in the disposable index. The ruling forbids the graph from
authoring the taxonomy; it does not forbid the graph from describing itself, and it should
be read that way explicitly before anyone builds this.

### 1.2 Signal reliability without ground truth — snorkel

`scout/rank.py` has six signals — `gap_fit`, `corroboration`, `vitality`, `reusability`,
`adoption`, `depth` — combined with weights that are hand-set in `DEFAULT_WEIGHTS`
(30/20/15/15/10/10). Those numbers are somebody's judgement, and there is no instrument
that could tell you whether they are wrong.

Snorkel's `LabelModel` is a direct answer to that class of problem: given several noisy
voters and no ground truth, estimate each voter's accuracy from the **structure of
agreement and disagreement between them**, by completing the inverse generalized covariance
matrix of their junction tree. `LFAnalysis` reports the diagnostics separately — coverage,
overlap, conflict, empirical accuracy per voter.

The signals here are exactly that: six noisy voters on "is this worth cataloguing". The
system already has the labels the estimate would be validated against — every published
resource note is a positive, every declined candidate a negative.

There is a specific defect this predicts. `corroboration` (independent rediscovery) and
`adoption` (star count) are almost certainly **not** conditionally independent — both read
popularity. A model assuming independence would double-count them, which is precisely the
failure mode `skweak` was built to handle in a different setting. That is not a hypothesis
about the code; it is a hypothesis about the world that the code encodes, and it is testable.

### 1.3 A machine-checkable note schema — OpenMetadata

`NO_SCHEMA_DRIFT` says the note schema, taxonomy axes and domain keys change only by
editing their authoritative Markdown. It is a policy with no enforcement mechanism. There
is no artefact anywhere in the vault that states what fields a resource note must have.
`integrity.py` asserts a handful of properties in hand-written Python; `notes.py` knows the
shape implicitly; the Design Specification describes it in prose.

OpenMetadata's answer is 904 JSON Schemas from which the Java, Python and TypeScript models
are all generated. Drift stops being discouraged and starts being impossible, because no
binding is hand-written. mdast makes the smaller version of the same point: its load-bearing
section is the **content model** — type unions saying which nodes may contain which — which
is what makes a tree checkable rather than merely traversable.

The vault has no content model. This pass wrote seventeen notes with nine taxonomy axes,
and nothing but care prevented a typo in `hardware_footprint` from silently removing a
resource from every constrained `find_donor` query.

### 1.4 Content-addressed identity — recipy

recipy hashes every input and output file and searches by hash rather than path, so
provenance survives a rename. The vault identifies resources by `canonical_url` and
`repo_key`; `scout.db.url_hash()` keys on the URL string.

**Two of seventeen sources had moved.** `eilab-gt/capabilibara` 301-redirects to
`HCAI-Lab-GT/capabilibara`; `neo4j-field/neocarta` redirects to `neo4j-labs/neocarta`. In
both cases the repository's own README still points at the old path. Nothing in the intake
would notice: a rediscovered repo at its old URL becomes a new candidate, and a rediscovered
repo at its new URL becomes a duplicate of one already catalogued. Twelve percent of this
cohort, from a sample of seventeen.

---

## 2. Where A Source Contradicts A Decision — And Who Is Right

### 2.1 Vectors are not the next retrieval investment. The system already suspected this; the sources confirm it.

`librarian/README.md` records that adding embeddings changed none of the eval numbers
(hit@5 1.00, recall@5 0.97, MRR 0.91 from filters and FTS5 alone). Implementation Brief
Step 4 nevertheless queues embeddings and fusion as the next retrieval work.

Two sources argue the improvement is on a different axis entirely. llama_index's largest
core subpackage is `indices/` (93 files), and its content is not one index with options —
it is **structurally different index types**: vector, keyword table, list, tree,
document-summary, knowledge graph, property graph, structured — with a router that picks
between them. graphrag makes the sharper version: its `basic` mode is plain vector search,
included specifically so you can watch it fail on the questions global search answers.

**The sources are right, and the Implementation Brief should be reordered.** The questions
this catalogue cannot answer are not similarity questions asked slightly badly. They are
questions of a different shape — *what is in here*, *what clusters with what*, *what has
this become* — and no amount of better cosine similarity reaches them. Step 4 as written
buys latency improvements to queries that already score 1.00; §1.1 buys a query kind that
does not exist. Where they compete for the same afternoon, §1.1 wins.

### 2.2 `NO_PERSISTENT_SOURCE_GRAPH` is the right rule with the wrong reason

Ruling R1 forbids storing any graph of a catalogued source beyond the workbench that built
it. The stated reason: sixty-four sources at five thousand nodes each is three hundred
thousand nodes of other people's internals, "the component library this design has already
rejected, in graph form."

The parsing cluster complicates that reasoning. §3.4 already carves out access points as
permissible because they are "addresses, not content — pointers outward, not copies
inward". A tree-sitter tag index or a semgrep match set is the same category: file, line,
symbol name. It is a pointer. The stated justification — that it becomes a snippet library —
does not actually cover it, because there is no snippet.

**The rule survives anyway, on a better argument.** A symbol location index ages
independently of its origin exactly as a snippet does: the line moves, the symbol is
renamed, and the index confidently points at the wrong place. Access points survive that
objection only because §3.4 pairs them with `verified_at` and a reachability check. A symbol
index has no equivalent of reachability, so it cannot be kept honest. The rule should stay,
and its justification should be rewritten from "it becomes a component library" to "it
cannot be kept verifiable" — which also explains why access points are the exception rather
than making them look like an inconsistency.

### 2.3 Precompute at write time — and the system already agrees with itself

graphrag and llama_index disagree about where the work goes. graphrag spends heavily at
indexing time — LLM entity extraction, hierarchical clustering, a written report per
community per level — so that query time is a lookup. llama_index keeps ingestion light and
puts the work into retrieval, reranking and synthesis on every query.

Spec §5 already resolves this for this system: *"Reads and writes are separate subsystems
with separate budgets: reads optimise for latency, writes for correctness."* Consult targets
under 30 seconds; a sweep is allowed hours. A vault written rarely and read often should be
on graphrag's side of that argument, and §1.1 is exactly what taking that side looks like.

### 2.4 The one place a source contradicts the system and is wrong

Every heavyweight source in this cohort — OpenMetadata, neocarta, data-mesh-ref-impl,
graphrag — assumes infrastructure: a JVM, a search cluster, Neo4j, Kubernetes, an LLM
budget. Their collective implicit argument is that a catalogue at this level of ambition
needs a platform beneath it.

For 263 notes, that is wrong, and the eval numbers are the evidence: filters plus FTS5 over
SQLite already return the right answer first for twenty of twenty questions. The
infrastructure those projects need is a consequence of organisational scale, not of the
capability. Adopting any of it would trade a working system for a heavier one, which spec §8
names as a listed failure mode.

---

## 3. What Is Being Done By Hand That One Of These Makes Deterministic

This section is short and unusually well evidenced, because this pass performed each of
these by hand and can therefore say exactly what it cost.

**Composite licence resolution.** The GitHub API's `spdx_id` was wrong or absent for three
of seventeen sources. LibCST reports `NOASSERTION` because its LICENSE is a composite — MIT
contributions, eleven files dual MIT/PSF, one Apache-2.0 file. mdast reports **no licence**
while its readme says CC-BY-4.0. semgrep reports LGPL-2.1 correctly, but only reading
`COPYRIGHT` confirms it. Three sources had no licence at all
(medallion-lakehouse-platform, awesome-dspy, gudu), which is a genuine `Unknown` and
correctly excludes them from permissive-constrained queries. `license_class` is a field that
**eliminates** in `find_donor`, so an error here silently removes a resource from every
constrained answer. `license_override_for()` already exists in `library_config.json`; the
missing piece is a deterministic fallback that fetches `LICENSE` when SPDX is null or
NOASSERTION, and flags a composite for review rather than guessing.

**Derived-view regeneration.** [[Taxonomy Index]] is a derived view the operating rules say
is "regenerated by the build, never edited by hand". This pass hand-appended seventeen rows,
because `build_solutions_library.py` can overwrite hand-written resource notes
([[Implementation Brief]] §2.1) and running it was the larger risk. The deviation is
recorded in the matrix itself. It should not have been necessary: regenerating the matrix is
reading nine frontmatter fields from every resource note and writing a table, which is about
twenty lines. A `views.py` that regenerates the matrix and the topic route-map counts,
separate from the whole-vault build, removes this class of hand-edit permanently.

**Topic resource counts.** `gap_fit` carries the largest ranking weight (30) and reads
`domain_resource_count` — a hand-maintained number in topic frontmatter. This pass edited it
by hand (Data APIs & Big Data 6 → 11, three new topics set to 4). A count derived from the
index cannot go stale; a count typed into frontmatter goes stale the moment anyone forgets.
Spec §4B.4 already contemplates a measured `gap_fit` from community size behind a config
flag; the simpler half of that — count what exists rather than trusting a declaration — needs
no graph at all.

**Note-structure validation.** `integrity.py` checks the taxonomy matrix with a regular
expression (`MATRIX_ROW`). mdast's argument applies directly: a document parsed into a tree
with a stated content model can be asserted against structurally — *every resource note has
exactly these H2 sections, in this order, each non-empty* — where a regex over Markdown is
a guess that mostly works.

---

## 4. Capabilities That Become Available And Are On No Roadmap

**An `overview` query kind.** With community reports (§1.1), the catalogue could answer
"what does this vault actually cover" from measured structure rather than from the topic
list somebody maintained. That is a seventh retrieval context, and the six in spec §3 do not
include it.

**Structural query over the vault's own Markdown.** The vault is 263 Markdown files with a
strict, repeated section structure. Nothing in the system can ask a structural question of
them. mdast supplies the model, and any Markdown AST library supplies the implementation.
This would make integrity assertions declarative and would let a person ask, for instance,
which resource notes have an `Architecture & Mechanics` section shorter than three bullets —
a direct measure of the "seed note" problem [[Library Assessment 2026-09]] identified.

**Extraction against a schema defined per run.** GLiNER makes the entity type list a runtime
argument. `access_points.py` is currently a fixed set of regexes for URLs, auth schemes and
rate limits. A zero-shot extractor could be pointed at a different schema — technique names,
data formats, model requirements, licence obligations — without new code and without
training. This is the least certain item in the report and is ranked accordingly.

**A field for agent-facing repositories.** Not a capability so much as a gap the pass
exposed. Three of seventeen ship agent instructions for their own contributors:
OpenMetadata's `skills/` (a 184-file `.claude-plugin`), neocarta's `.claude/skills/`
connector recipes, and semgrep's top-level `AGENTS.md` and `CLAUDE.md`. The taxonomy has no
axis for it, and for a catalogue whose stated purpose is helping "co-operating agents find
proven prior work", whether a source is legible to an agent is a real property.

---

## 5. Candidate Changes In Detail

### 5.1 Licence resolution fallback — *rank 2 · **applied 2026-09-03***

**What it is.** In the intake, when the GitHub API returns `spdx_id` of `null` or
`NOASSERTION`, fetch the repository's `LICENSE` (and `COPYRIGHT`, if present) and classify
from its text; where the text names more than one licence, record the composite and route
the note to review rather than picking one.

**What it offers.** Correctness in the single field that eliminates. Three of seventeen
sources this pass would have been mis-filed by the API value alone.

**How the system changes.** `scout/rank.py::license_class()` gains a text path;
`build_solutions_library.py::license_override_for()` gains a fetch step before falling back
to config; `04-Reviews/` gains a reason code for composite licences.

**Cost.** One extra request per source with an unknown licence, cached. No new dependency.
Fully reversible — delete the fallback and behaviour returns to today's.

**What was actually built.** `scout.rank.license_from_text()` is a pure classifier;
`scout.discovery.fetch_license_text()` and `resolve_license()` do the fetching;
`scout.evaluate.enrich_depth()` calls it, so the extra request is spent only on candidates
whose SPDX came back unresolved. Four rules, in priority order:

1. **An explicit `SPDX-License-Identifier` expression wins outright.** osquery's LICENSE is
   four lines of prose and one line of `Apache-2.0 OR GPL-2.0-only`; guessing at the prose
   while that sits in the same file would be indefensible.
2. **`OR` is a choice, `AND` is a conjunction.** A reuser offered Apache *or* GPL may rely on
   Apache, so the *least* restrictive licence governs. A file that is MIT with a vendored
   PSF component binds both, so the *most* restrictive governs. Reading osquery the wrong way
   round would have removed a permissively usable project from every permissive-only query.
3. **GPL-family cross-references are not separate licences.** Every GPL-family text names its
   siblings — LGPL-2.1 refers to the GPL throughout, GPL-3.0 names the AGPL and the LGPL in
   its closing sections. The discriminator is position: a licence document opens with its own
   title. Before this rule, semgrep read as Copyleft and netdata as four licences.
4. **A readme is read only when there is no LICENSE, and never trusted outright.**
   `syntax-tree/mdast` states `[CC-BY-4.0][license]` in one readme line and ships no LICENSE
   file. Recording that as Unknown loses a written answer; recording it as settled overstates
   a prose mention. It resolves, and it is flagged for review.

Anything composite, anything resting on a readme, and anything unresolved sets
`license_review_required`, because the correct answer there is a person reading it — a
confident single answer would be the plausible guess `EVIDENCE_REQUIRED` forbids.

**Verified against ten real LICENSE files**, every one read live during this session: LibCST
(MIT AND Apache-2.0 AND PSF-2.0, Permissive, review), semgrep (LGPL-2.1, Weak_Copyleft),
mdast (CC-BY-4.0 from the readme, review), osquery (Apache-2.0 OR GPL-2.0, Permissive,
review), netdata (GPL-3.0), suricata (GPL-2.0), terraform (BUSL-1.1, Source_Available),
capabilibara (AGPL-3.0), duckdb (MIT), geopandas (BSD-3-Clause). Nine new tests in
`scout/tests/test_rank.py` pin the decisions.

**Confidence.** High, for the mechanism. The **backfill has not been run** — see §11.

### 5.2 `views.py` — deterministic derived views — *rank 3 · **applied 2026-09-03***

**What it is.** A module that regenerates [[Taxonomy Index]] and the topic route-map counts
from note frontmatter, separately from `build_solutions_library.py`.

**What it offers.** Removes the hand-edit this pass was forced into, and removes the stale
`resource_count` that `gap_fit` trusts. It also clears the 29 pre-existing
`taxonomy_matrix_agrees` warnings, which are all old rows whose `license_class` in the
matrix disagrees with the note.

**How the system changes.** New `librarian/views.py`; a `librarian views` CLI command;
[[Master Index]] operating rules gain a named command for "regenerated by the build". The
existing integrity check becomes a real gate rather than a standing warning.

**Cost.** Roughly twenty lines plus a test. No dependency. Trivially reversible.

**What was actually built.** `librarian/views.py`, a `librarian views [--check]` command,
and a twelfth integrity check (`derived_views_current`, a warning — the fix is a command,
not a correction). It owns three views: the taxonomy matrix, topic membership with
`resource_count`/`review_count`, and the route-map counts.

Two design decisions are worth stating, because both are places a derived view could
overreach:

- **It reconciles membership but never reorders.** The view owns *which* resources a topic
  holds, because that is a fact about their frontmatter. It does not own the *order* — the
  existing lists run in the order things were catalogued, and alphabetising fourteen of them
  would be a derived view rewriting authored content to suit itself.
- **It never invents a frontmatter field.** Adding one would be schema drift, which is not a
  view's business.

**It also found a defect this report's own pass introduced.** The seventeen rows added by
hand on 2026-09-03 were appended to the end of the file, which put them *inside*
`## Cross-Analysis` rather than in the matrix — seventeen duplicate rows that nothing could
see, because nothing was reading the matrix structurally. `views.py` now strips matrix rows
found outside the matrix section, and a test pins it.

**Measured outcome:** `integrity` went from **29 warnings to 0**. All 29 were
`taxonomy_matrix_agrees` — the matrix disagreeing with its notes about `license_class`,
the field `find_donor` eliminates on. Running the view twice changes nothing.

**Confidence.** High. Idempotent, tested (eight tests in `librarian/tests/test_views.py`),
and the hand-edit note in [[Taxonomy Index]] has been removed because its reason no longer
holds.

### 5.3 Community reports over the vault graph — *rank 4*

**What it is.** Extend `graph.py`: after community detection, generate a short written
summary of each community — its members, the links that bind it, and what it appears to be
about — store it in the derived index, and surface it from `orient()` and a new overview
path.

**What it offers.** The system's first answer to a whole-catalogue question. Also a
measured, *explainable* alternative to `gap_fit`'s declared `resource_count`: a community
that is structurally thin can say so in a sentence, which a number cannot.

**How the system changes.** `graph.py` gains a summarisation step; the index gains a
`community_report` table; `consult.py` gains a path that returns reports with a `why`;
[[Design Specification]] §4B.1 gains an explicit statement that summarising a community is
permitted use 1 and not a breach of `GRAPH_ADVISORY_ONLY`.

**Cost.** The honest cost is a model call per community at build time, which introduces the
system's first write-path model dependency outside the scout pass — and LM Studio is not
currently reachable on this host. `R8 — degrade, do not fail` must therefore hold: no
reports rather than an error. A template-assembled summary (members, shared patterns, shared
glossary terms) is a genuine non-model fallback and should be built first. Reversible: the
reports live in the disposable index.

**Confidence.** Medium-high on the mechanism, which was read in graphrag's
`summarize_communities/` and `query/structured_search/global_search`. Lower on the value,
which is inferred from graphrag's design rather than measured on this vault — 263 notes is
two orders of magnitude smaller than the corpora graphrag was built for, and it is possible
the communities are too small to be worth summarising. **That is measurable before
building**: run `librarian graph` and look at the community sizes.

### 5.4 A note content model, and AST-based integrity — *rank 5 · **applied 2026-09-03***

**What it is.** One JSON Schema per note layer — resource, topic, pattern, glossary,
application — stating required frontmatter fields, the closed enumerations for the nine
taxonomy axes, and the required body sections in order. `integrity.py` validates against it
instead of against hand-written assertions; the search-params schema already in spec §4.3
becomes one member of the same set rather than a one-off.

**What it offers.** `NO_SCHEMA_DRIFT` becomes enforceable. A typo in a taxonomy value stops
being a silent elimination from `find_donor`. It also makes the axes' permitted values
*written down* for the first time — this pass had to introduce three new `domain_primary`
values (`Code_Intelligence`, `Knowledge_Management`, `ML_Training`) and could not check them
against anything, because nothing enumerates that axis.

**What it costs.** Medium. Five schemas, a validator, and rewriting several checks in
`integrity.py`. The real cost is discipline: a schema that is allowed to lag the notes is
worse than no schema. OpenMetadata's answer — generate the bindings so nothing can be
hand-written — is the strong form, and is more than this vault needs; the weak form
(validate, do not generate) is the right size here.

**Confidence.** Medium-high. Verified that OpenMetadata does this and how; inferred that the
lighter version suits a Markdown vault.

### 5.5 Ranking-signal reliability — *rank 6, after 5.2*

**What it is.** Treat the six ranking signals as labelling functions. Compute Snorkel-style
diagnostics first — coverage, overlap, conflict, and correlation between signals — over the
existing candidate history in `solutions_library.sqlite`, using published-or-declined as the
label. Only then consider replacing `DEFAULT_WEIGHTS` with estimated ones.

**What it offers.** Six hand-set numbers become measured ones, with a specific prediction to
test first: that `corroboration` and `adoption` are correlated and currently double-counted.

**How the system changes.** A new `scout/analysis.py`; `DEFAULT_WEIGHTS` gains a measured
alternative behind a config flag, compared against the eval set before adoption — the same
discipline spec §4B.4 already requires for the `gap_fit` change.

**Cost.** Medium, and the dependency question matters. **Do not install Snorkel**: it pins
Python 3.11 exactly (0.10.0's only breaking change was adopting 3.11 and dropping every
other version), which would constrain the whole toolchain, and it drags in PyTorch. The
diagnostics are numpy. The label model itself is roughly fifty lines of numpy for the
conditionally-independent case. Take the method, not the package.

**Confidence.** Medium. The mechanism was read in `label_model.py`'s docstring and the
subsystem layout, not in the estimation code. Whether the signals have enough recorded
history to estimate from is unverified and is the first thing to check.

### 5.6 semgrep as a registered workbench action — *rank 7, gated on the workbench*

**What it is.** Register `semgrep` in the closed action registry as a subprocess with a
bounded timeout (as ruling R5 already requires of graphify), invoked **inside a workbench
only**, so that `find_technique`'s "open a workbench on X to confirm" step is followed by an
actual structural search rather than a manual read.

**What it offers.** Today `find_technique` is honest that it ends at tier 3 — descriptions
and metadata. A semgrep rule turns "this repository probably handles backpressure" into
file-and-line evidence, across 37 languages, without writing a parser. It is the single
largest improvement available to the weakest of the six query kinds.

**How the system changes.** `librarian/workbench.py` gains a search action; the registry
gains an entry; `find_technique`'s `next_step` can name a rule to run. Nothing is persisted —
matches die with the workbench, exactly as slices do, so `NO_PERSISTENT_SOURCE_GRAPH` and
§4A.6 are untouched.

**Cost and the licence question.** semgrep is **LGPL-2.1**, which is weak copyleft. Invoking
a binary as a subprocess is not linking, so this use is clean — but it means semgrep may
never be vendored or imported, and `find_donor` under a permissive constraint must continue
to exclude it. Operationally: a binary to install, and the Community Edition's own stated
limit — analysis "within the boundaries of a single function or file" — so cross-file
questions will not be answered. Reversible: unregister the action.

**Confidence.** Medium. The capability and the licence were verified in the repository. The
value to `find_technique` is inferred, and cannot be tested until the workbench exists —
Docker is not running on this host, which blocks Implementation Brief Steps 10 and 11
regardless of anything in this report.

### 5.7 Zero-shot extraction for access points — *rank 8, or not at all*

**What it is.** Add GLiNER as an optional second pass in `access_points.py`, extracting
against a label list (`api endpoint`, `authentication scheme`, `rate limit`, `data format`)
where the regexes find nothing.

**What it offers.** The current extractor is a fixed set of patterns for URLs, `/graphql`,
`/sparql`, OAuth strings and rate-limit phrasings. It is at its ceiling: anything phrased
unusually is invisible to it. A zero-shot extractor changes the schema by editing strings.

**Cost.** A real model dependency — PyTorch, transformers, and a weights download from
Hugging Face on first use — for a subsystem that is currently pure regex and has no
dependencies at all. It also introduces non-determinism into a field the design intends to
*verify* (`verified_at`, `reachable`), so every extracted point would still need the
reachability check to earn its place.

**Confidence.** Low-medium, and it is ranked last deliberately. GLiNER's mechanism was read
in `docs/architectures.md` and is well described; whether it helps *on documentation prose*
was not tested, and the honest answer is that nobody knows until it is tried on the vault's
own corpus. If the regex extractor's recall has never been measured, measure that before
adding a model.

### 5.8 Canonical URL redirect detection — *rank 9; adopt any time, it is trivial*

**What it is.** Follow redirects on the metadata fetch and compare the returned `full_name`
against the requested one; when they differ, record the old path as an alias and the new as
canonical.

**What it offers.** Prevents duplicate candidates and dead canonical URLs. `aliases` already
exists in the note schema and is exactly the right home for the old path.

**Cost.** One flag on the request. Fully reversible.

**Confidence.** High. Two of seventeen sources exhibited this in one pass.

---

## 6. What Should Deliberately Not Be Adopted

A well-argued rejection is as useful as a recommendation, so these are argued rather than
listed.

**graphrag, as software.** Take the community-report idea; do not take the package. It is in
**declared maintenance mode** — the README's first line says it "won't be accepting new PRs
or implementing new features" — which means adopting it is adopting a frozen dependency. Its
indexing is expensive by its own warning, its prompts are expected to be tuned per corpus,
and most decisively: it *builds* a graph from unstructured text, which is the one part this
vault does not need. The graph already exists as typed wiki-links written by hand.
Everything graphrag would extract, the vault already knows.

**llama_index, as the retrieval layer.** Its index taxonomy is the most useful idea in the
cohort for thinking about retrieval, and its integration count — roughly 9,000 files across
300+ packages — is exactly why it must not be adopted here. It would replace a working
retrieval surface that scores 1.00 hit@5 with a dependency tree larger than the entire
vault. Spec §8 lists "never finishing because each component invites a more advanced
version" as the failure mode; this is what that looks like.

**neocarta and Neo4j.** neocarta is the closest analogue to this system in the whole cohort —
harvest metadata, model it as a graph, serve it to agents over MCP — and reading it is
worthwhile. Adopting it is not: its entire query layer is Cypher, so Neo4j becomes a
non-negotiable service for a 263-note vault that SQLite answers in microseconds. It is also
explicitly experimental. **One thing should be taken for free**: neocarta keeps its Cypher
in `_mcp/cypher/` and its tool definitions in `_mcp/tools/`, separately. When
`mcp_server.py` grows past a handful of tools, that separation — the query is data, the tool
is the contract around it — is worth copying.

**OpenMetadata, as a catalogue.** Wrong by two orders of magnitude: a JVM, MySQL or
Postgres, Elasticsearch or OpenSearch, and Airflow, to catalogue what a folder of Markdown
already holds. Take the schema-first idea in its weak form (§5.4) and take two documentation
practices: an `ARCHITECTURE.md` that **states how its own numbers were obtained** and names
where its layering fails rather than describing an intended architecture, and a "look here
first" column per component. Both are free.

**Snorkel and skweak as dependencies.** Argued in §5.5 for Snorkel. skweak additionally
requires spaCy as its document model and is **unmaintained by its authors' own statement** —
"Skweak is no longer actively maintained (if you are interested to take over the project,
give us a shout)". Its HMM aggregator is the better design for sequence problems, and this
system has none.

**recipy.** Do not install it. Its last release was 2016, its patch list still names
`pandas.Panel` and `to_msgpack` — both removed from pandas years ago, so those patches
cannot bind — and it has 90 open issues with dead CI. Take the two ideas: interception at
the I/O boundary rather than declaration, and identity by content hash (§1.4).

**tree-sitter and LibCST, for this system.** Both are excellent and neither has a job here.
tree-sitter is the substrate a tool builder needs; this system would consume it only through
semgrep, which already vendors 36 forked grammars. LibCST is Python-only and its value is
codemods, which this system does not perform. They are catalogued because a future donor
search will want them, not because anything here should use them.

**capabilibara, data-mesh-ref-impl and gudu-sql-omni-introduce.** Nothing to adopt from any
of the three. capabilibara has no attribution code in it at all. data-mesh-ref-impl is six
unconnected proof-of-concepts, last touched twenty months ago, assuming fourteen Kubernetes
clusters. gudu is marketing copy for a proprietary product. Each is catalogued as a negative
result so that nobody spends a second afternoon on it — which is the whole argument for
recording negative findings as carefully as positive ones.

One idea does survive from data-mesh-ref-impl, and it is worth naming: PARADIRE's Access
Control Gateway expresses its data-sharing policy as a **GraphQL schema whose custom
directives** — `@hash`, `@restrict`, `@selectable`, `@date` — hash, redact, remove or coarsen
each field. The policy is a diffable artefact owned by the people who own the policy, and it
is simultaneously the API contract. This system's policies are Python with named codes, which
is the right choice for structural invariants that must never be data. But if a future
version ever needs to express *what an external agent may see* — a real possibility given the
MCP surface in Step 11 — that is the design to reach for.

---

## 7. Where The Sources Overlap, And Which Fits Better

**graphrag vs llama_index vs neocarta — all three build a graph for retrieval.** For this
system, **none of them is the right adoption**, and that is the finding. The vault's graph
is already written by hand as typed links; `graph.py` already clusters it. What is missing is
one step — summarisation — which graphrag names most clearly and which is small to build
locally. Reading order if only one is read: graphrag for the idea, neocarta for the serving
architecture, llama_index for the index taxonomy.

**snorkel vs skweak — near-total overlap.** Snorkel is the better fit: instance-level
labelling matches the ranking problem, Apache-2.0, no spaCy, and it is at least
maintenance-active. skweak wins only for span-level sequence labelling, and its HMM matters
only when adjacent decisions depend on each other. That said, skweak's *architecture* is the
better teacher — it separates the **shape** of the label space from the **method** of
reconciliation as independent choices, and that separation is worth copying even in a
fifty-line numpy implementation.

**GLiNER vs snorkel/skweak — not actually overlapping.** GLiNER extracts entities from text
against a runtime label set; the weak-supervision tools reconcile competing votes. A pipeline
would use both: GLiNER as one labelling function among several, reconciled by the label
model. Filing them in the same topic is correct; treating them as alternatives is not.

**tree-sitter vs semgrep vs LibCST — a dependency chain, not a choice.** semgrep is built on
36 forked tree-sitter grammars; the forks exist because a grammar must also parse *patterns*
containing metavariables. For this system's one plausible use — evidence for
`find_technique` — semgrep is the right level: one YAML rule instead of a parser plus a query
plus a traversal. tree-sitter would be right only if building something custom. LibCST is
right only for Python codemods.

**OpenMetadata vs neocarta — the same architecture at two scales.** Both harvest metadata by
connector, model it, and serve it to agents over MCP; both were built in the last few years
for the same reason. neocarta is the one to read (Python, focused, 516 files); OpenMetadata
is the one to learn practices from (schema-first codegen, measured architecture
documentation). Neither is the one to run.

**recipy vs OpenMetadata on provenance — a genuine disagreement, examined in §8.**

---

## 8. Where The Sources Disagree With Each Other

Disagreements between sources are more informative than any single source's opinion, because
they mark the places where the problem is genuinely undecided.

**Precompute versus compute on demand.** graphrag spends heavily at index time so query time
is a lookup; llama_index keeps ingestion light and works hard per query. This is a real
architectural fork, and it maps exactly onto spec §5's separate budgets for reads and writes.
*What it tells us:* the right side depends on the read/write ratio, and this vault's is
extreme — written in supervised passes, read constantly. The system has already chosen; §1.1
is what following that choice through looks like.

**How much semantics belongs in the parser.** tree-sitter refuses semantics entirely to stay
universal and dependency-free. semgrep normalises 37 languages into one generic AST — and
then discovers it needs an intermediate language, a taint engine, and still cannot see past a
single function in its open edition. *What it tells us:* normalising many languages into one
representation buys breadth and costs depth, and depth is exactly where the commercial line
gets drawn. Any future plan to "just parse everything into a common form" should expect the
same cost curve.

**Whether labellers are independent.** Snorkel's default label model assumes conditional
independence given the true label. skweak's HMM exists precisely because that assumption is
wrong when adjacent decisions are coupled. *What it tells us:* the assumption is the model,
not a detail of it — and it predicts the specific defect in §1.2, that `corroboration` and
`adoption` both read popularity and would be double-counted by the naive form.

**Where provenance is captured.** recipy intercepts at the library call, which is complete
for what it patches but bounded by a list that ages badly. OpenMetadata parses query logs
after the fact, which is incomplete but requires no cooperation from the thing being observed.
*What it tells us:* interception is available only when you control the code. This system does
control its own code — every write already passes through `index.py` — so the recipy side is
cheaply available here in a way it is not for a data platform observing warehouses it does not
own.

**What a specification is for.** mdast writes the format down in prose and lets
implementations vary, which is why mdast implementations exist outside JavaScript.
tree-sitter ships the implementation and treats its grammar DSL as the specification, which
is why a tree-sitter grammar is portable but a tree-sitter *tool* is not. *What it tells us:*
this vault's schema question (§5.4) is the same choice. A written content model that
`integrity.py` validates against is the mdast answer; generating `notes.py` from a schema is
the OpenMetadata answer. For a system where Markdown is truth and the tooling is small, the
mdast answer is the right size.

---

## 9. What Surprised Me

**Four of seventeen were not what their metadata says**, and in every case the *structure*
was the honest signal. graphrag carries 35,819 stars and was pushed the day before this pass,
and its README's first line declares maintenance mode. llama_index's GitHub description
advertises the company's commercial OCR platform, not the framework in the repository.
capabilibara documents a `src/` tree that does not exist. gudu describes a parser and
contains thirteen marketing articles. The catalogue's `vitality` signal reads `pushed_at`;
none of these four would be caught by it.

**A public research demo renders synthetic data with no user-visible disclaimer.**
capabilibara's Hugging Face Space advertises a "Matrix Explorer" over "576 corpus bins" and
an "Influence Breakdown" across four named benchmarks. Line 31 of `hf_space/app.py` reads
`# Generate synthetic influence baseline data matching paper distributions`, followed by
`np.random.seed(42)`. The repository README is scrupulous that the code is unreleased; the
demo is not scrupulous that the numbers are invented. This is recorded without accusation —
the intent is plainly a placeholder — but anyone quoting a figure from that heatmap would be
quoting a random number generator.

**Three projects independently built weak supervision and only two call it that.** Snorkel's
`LabelModel`, skweak's HMM aggregator, and OpenMetadata's PII classifier
(`ingestion/src/metadata/pii/`: Presidio recognisers, a NER pass, column-name patterns,
engineered features, `tag_scoring.py`, `conflict_resolver.py`) are the same shape — many
noisy labellers, scored, reconciled. The third arrived at it inside a data catalogue with no
reference to the literature. That the pattern recurs unprompted is the strongest argument
that §1.2 is a real gap here too.

**The repository is becoming an agent-facing artefact.** Three of seventeen ship agent
instructions in-tree, and this was not something the pass set out to look for. It changes
what "reusable" means for a source, and the taxonomy has no way to express it.

**The best architecture document in the cohort is in the largest codebase.**
OpenMetadata's `ARCHITECTURE.md` — 18,794 files behind it — declares how its own numbers were
measured, traces three request paths concretely, gives a "look here first" column per module,
and states where its layering *fails*. That is the opposite of the usual relationship between
project size and documentation honesty.

---

## 10. What I Looked For And Could Not Find

**An open-source column-level SQL lineage engine.** This was the point of the lineage cluster
and it is the clearest miss. `gudu-sql-omni-introduce` was the lead and turned out to be
marketing for a proprietary product. OpenMetadata does column-level lineage well but only
inside a platform requiring a JVM, a relational database, a search cluster and Airflow. The
standalone library that parses SQL and emits column-level lineage was not in this cohort;
`sqlglot` and the OpenLineage specification are the obvious next leads and neither was on the
list. **This is the strongest argument for a `data_lineage_provenance` domain** — the cluster
that motivated the search has no adequate entry in the catalogue.

**A structural query tool for Markdown.** semgrep exists for code; the vault is 263 Markdown
files with strict structure and nothing equivalent. mdast supplies the model and the remark
ecosystem supplies the utilities, but there is no "semgrep for Markdown" — no tool where you
write a pattern shaped like the document you are looking for. For a system whose truth is
Markdown, that is a notable absence, and possibly a small thing worth building rather than
finding.

**Weak supervision for ranking rather than classification.** Snorkel's label model assumes
discrete classes. The scouting problem is scoring candidates on a continuum. Nothing in the
cohort addresses noisy voters over an ordering, which is a limitation of §5.5 that should be
understood before it is built.

**A published retrieval eval set.** Both graphrag and llama_index ship evaluation modules;
neither ships a canonical question set with published numbers the way `librarian eval` does
(hit@5 1.00, recall@5 0.97, MRR 0.91 over twenty questions). This system is ahead of both on
that specific discipline, which was not what I expected to find.

**A running Docker daemon or LM Studio on this host.** Verified during the pass: the Docker
API is unreachable and nothing answers on `127.0.0.1:1234`. This blocks Implementation Brief
Steps 10 and 11 entirely, blocks §5.6 here, and forces §5.3's non-model fallback to be built
first. It is an environment fact rather than a design problem, and it is stated plainly
rather than worked around.

---

## 11. Proposals Requiring A Decision

Neither of these was actioned; both are the user's call.

**~~A `data_lineage_provenance` domain.~~ — approved and added.** Five sources filed into
[[Topic - Data APIs & Big Data]] this pass and two of them do not belong there.
`recipy - recipy` and `shenhuan2021 - gudu-sql-omni-introduce` are lineage and provenance
tooling; that topic is dataset catalogues, portals and APIs. §10 showed the domain was also
*under*-served — the search that motivated this cohort did not find what it was looking for,
which is exactly the condition `gap_fit` exists to detect and cannot while the domain has no
key. It is now in [[Scouting Domains]] as a tier-1 rotation target.

**No topic index was created for it**, and that is the register's own rule rather than
caution: a domain becomes a topic only once scouting has filled it, and two sources is not
enough. The lineage and provenance glossary and pattern notes now carry the new key, so the
concepts are filed correctly even though the resources are not yet.

**The licence backfill has run.** All 52 unresolved resources were read: **41 resolved, 11
still `Unknown`**, and `find_donor` under a permissive constraint went from offering 24
resources to 54. Eight of the 41 rest on a judgement a person should confirm — composites,
one dual licence, and three read from a readme — and they are listed in
[[Licence Resolution 2026-09-03]] with the reasoning for each. The eleven that remain
`Unknown` are findings rather than gaps: repositories that ship no licence at all, or ship
one no lookup table recognises (SigmaHQ's Detection Rule License among them).

The run also produced its own correction, recorded in that note: an early version inferred a
licence *choice* from wording, matched GPL boilerplate, and reported ckan and wazuh as
Permissive when both are copyleft. That is the one direction of error this field must never
make. A choice is now inferred only from an explicit SPDX `OR` expression, and a test pins
it.

**`## Reading Notes` is now part of the resource-note shape, and 45 notes have none.**
The section was introduced by this pass to hold the finding that fits nowhere else — graphrag
being in declared maintenance mode behind 35,819 stars, LibCST's licence being a composite,
capabilibara's demo rendering synthetic data. It has since been propagated to the 19 older
notes that earned one from evidence gathered here: eight whose licence turned out to be a
composite, dual or prose-only declaration, eight with no usable licence at all, and three that
are source-available while looking open.

**`## What Is Inside` has since been propagated to all 81 resource notes** by re-reading every
source from a blobless clone and surveying its tree — no REST quota, nothing written from a
README. That pass is what turned the abstract objection into a measured one: it surfaced
57,911 bank records in `not-a-bank`, 459 Windows `.evtx` samples in SigmaHQ, 4,818
sqllogictest files in duckdb, 4,199 compiler fixtures in react and a 691-entry manifest (not
code) in `openstack` — none of which any description of those projects would have suggested.
It also found that **agent-facing repositories are now common rather than notable**: netdata
carries 197 agent-instruction paths, sentry 98, airflow 63, react 28, penpot 20, and gdal,
prometheus, duckdb, osquery and vercel-labs all ship some form. Retrieval improved rather than
degraded, MRR 0.93 → 0.94.

The remaining **45 older notes have no Reading Notes and were deliberately left without one.**
Their licences resolved cleanly and nothing else about them was re-read this session, so any
section written for them would either restate the Taxonomy block or be invented. An empty or
formulaic section would also be actively harmful: `## Reading Notes` is prose and is indexed,
and §0 measured what forty-odd near-identical chunks do to retrieval.

The absence is the useful signal, and it is queryable — a resource note without a Reading Notes
section is one nobody has re-read since it was written. That makes it a natural candidate for
an integrity *warning* and a natural input to the re-read queue, and the section belongs in the
content model proposed in §5.4 as **optional but tracked**, never as a required slot to fill.

**~~Three new `domain_primary` values were introduced and could not be checked.~~ — resolved.**
`Code_Intelligence`, `Knowledge_Management` and `ML_Training` were asserted by this pass with
nothing to validate them against, because until [[Note Content Model]] existed no artefact
enumerated the nine axes. They are now declared there, alongside every other value the
catalogue actually uses, and `axis_values_known` fails on anything outside those lists. The
three are no longer assertions; they are decisions, recorded where a decision belongs.

---

## 12. Confidence And What Was Not Verified

Stated plainly, because the difference matters more than the conclusions.

**Measured on this vault during the pass:** the MRR regression, both retrieval defects, and
the four-configuration comparison that produced the fix in §0 (`librarian eval` before and after, one query run by hand, and a chunk-heading count
against `catalogue_index.sqlite`); the integrity result; the note, chunk and link counts.

**Verified directly against source files:** every metadata field in all seventeen notes (one
REST call each, nothing from memory); every repository tree; the licence texts of LibCST,
mdast, semgrep and skweak; the mechanism descriptions in tree-sitter's
`docs/src/5-implementation.md` and query syntax docs, GLiNER's `docs/architectures.md`,
recipy's `docs/how_does_it_work.rst` and `patched_modules.rst`, OpenMetadata's
`ARCHITECTURE.md`, PARADIRE's ACG README, neocarta's README and package layout, graphrag's
workflow and operation listings, llama_index's core subpackage layout with file counts;
snorkel's `LabelModel` class docstring; the maintenance statements in graphrag's, skweak's
and snorkel's READMEs; both 301 redirects; the synthetic-data comment in
`hf_space/app.py`; and this vault's own `rank.py`, `access_points.py`, `integrity.py` and
`DEFAULT_WEIGHTS`.

**Read as documentation, not as code:** graphrag's retrieval quality claims, semgrep's
accuracy claims, GLiNER's benchmark results, OpenMetadata's lineage derivation, snorkel's
estimation procedure beyond its docstring. No implementation in any of the seventeen was read
line by line, and **no fetched code was executed anywhere in this pass.**

**Inferred, and flagged as such where it appears above:** that community reports will be
useful at 263 notes (§5.3 — measurable now by inspecting community sizes); that the ranking
signals have enough recorded history to estimate from (§5.5 — checkable in
`solutions_library.sqlite`); that GLiNER helps on documentation prose (§5.7 — untested, which
is why it is ranked last); that semgrep improves `find_technique` in practice (§5.6 —
untestable until a workbench exists).

**Not read at all:** capabilibara's paper PDF; skweak's GitHub Wiki, which is its only
documentation; the semgrep rule corpus, which lives in a separate repository; every
individual implementation file in llama_index and OpenMetadata.

---

## Related
- [[Scouting Working File 2026-09-03]] — the per-source evidence this report is built on
- [[Design Specification]] — the authority this report proposes against
- [[Implementation Brief]] — the build order §2.1 proposes reordering
- [[Scouting Domains]] — the register, and the `code_intelligence` addition
- [[Library Assessment 2026-09]] — the previous assessment of the catalogue itself
- [[Master Index]]
