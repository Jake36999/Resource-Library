---
type: "assessment"
status: "active"
created: "2026-09-04"
purpose: "what twenty-four analyses have in common, what none of them looked at, and the shape to build to"
analyses_reviewed: 24
---

# Meta Analysis And Final Shape

## Part 1 — What Recurs Across Twenty-Four Analyses

Read together rather than one at a time, the reviews in `internal docs/` say
something none of them says alone. Almost every defect found in this project
belongs to one of **five shapes**, and each shape has recurred enough times that
the next instance should be predicted rather than discovered.

### Shape 1 — Built, correct, and never run (nine instances)

`embed` · `graph` · `access_points` · `mcp_server` · `workbench` · the intake
pipeline · `_proven_use_bonus` · `shallow_clone` over a network · the duplicate
floor set above its own maximum.

Every one has code, tests and a degradation path. Every one has zero rows, zero
invocations, or — in two cases — a defect that could only exist because nothing
ever exercised it. `shallow_clone` failed DNS on every call for the life of the
project; the duplicate check reported *no duplicates found* from a threshold
above the highest similarity in the corpus.

**The generalisation: a specification satisfied is not a capability held.** This
project has been unusually good at building what was specified and unusually bad
at running it once. Nine instances is not carelessness, it is a structural
property of building from a design document.

### Shape 2 — Evidence counted that was not evidence (six instances)

Caveat text read as a claim · verbosity as a ranking signal · stopwords matching
note names · `interface_protocol: "REST"` matching *the rest of the system* ·
no stemming · out-of-scope terms driving a result.

All six are the same error: **a token that appears is treated as a token that
means**. Each was found by measurement and none by reading the code.

### Shape 3 — The system deciding on the user's behalf (three instances, one policy)

`reusability` scoring an unlicensed source `0.0` · `vitality` scoring an
archived one `0.0` · `adoption` scoring an unstarred one `0.0`.

Each a hard zero under a double-digit weight, each awarded for a property that
only matters under an assumption nobody had stated. Now `LOCATE_DO_NOT_ADJUDICATE`
with an audit table, and the audit is the artefact that matters — it makes the
fourth instance findable before it ships.

### Shape 4 — A constant fitted to a corpus that then moved (two instances)

`SELECTIVITY_CEILING` at 0.34 · `SEMANTIC_FLOOR` at 0.18.

Both were correct when set and wrong within one intake. **Any threshold derived
from corpus statistics needs a `distribution()` beside it**, and only
`duplicates` currently has one.

### Shape 5 — Two implementations of one thing (four instances)

Two tokenisers · two stopword lists · two GitHub clients · two clone paths.

Each pair diverged silently and each divergence caused a defect — `scope` versus
`scope.` being the clearest. All four were found by accident while building
something else.

### What the pattern says about the method

The method has been sound where it was applied: five ranking hypotheses were
measured and rejected, one published claim was retracted when it failed to
reproduce, and three thresholds were re-derived from data rather than defended.
That discipline is why this list can be written at all.

But **every one of these was found by building or measuring, and none by
reviewing.** Fourteen documents of analysis preceded them and predicted none.
That is the meta-finding: *analysis in this project has been good at deciding
what to do and poor at finding what is wrong.* The instruments find defects; the
documents organise intent. Treating a review as a substitute for a run is the
mistake that produced Shape 1 nine times.

---

## Part 2 — What None Of The Analyses Examined

Five gaps, ordered by how much they undermine what is claimed elsewhere.

### 2.1 The unit of retrieval is the whole note, and that was never argued for

Every query returns `kind: resource` — a repository. Meanwhile the data layer
holds **2,761 directories and 4,877 component paths**, and none of it is
reachable through a query. `librarian components signal grammars` returns
repositories that contain grammars; it cannot return the grammars.

The notes themselves make the case against this. `What Is Inside` exists because
*a source's most valuable content is routinely not what its abstract describes* —
GLiNER's relation-extraction heads, elastic-labs' `relevance-workbench`,
duckdb's 4,818 sqllogictest files. Each is the answer to a question, each lives
inside a repository whose note is about something else, and none can be returned.

[[jgravelle - jcodemunch-mcp]] is catalogued here and its entire thesis is that
**symbol-level retrieval beats file-level** because the reader's attention is
finite. The catalogue holds that argument and does not apply it to itself.

This is the single largest unexamined assumption in the project, and unusually
it is cheap to test: the component store already exists.

### 2.2 Every instrument is self-authored, and both measure the same author's frame

The eval's twenty questions, the thirty scenarios, the 128 notes and the nine
taxonomy axes were written by the same process. `useful@5 0.87` means *the
retrieval finds what its author expected*, which is a much weaker claim than it
reads as.

The scenario test was built specifically to escape this — real components in
their own team's vocabulary — and it only half escapes, because the scenarios
were still written by someone who knew the corpus. The two deliberate negative
controls are the honest part; everything else is a closed loop.

**No analysis has stated this as a limit on the numbers it reports**, and every
retrieval claim in `Service Map` inherits it.

### 2.3 The corpus is a convenience sample and `gap_fit` compounds it

128 repositories from one seed list reflecting one person's interests. Nothing
here is a sample of anything, which is fine for a private reference guide and is
**not fine for `gap_fit`**, the highest-weighted scouting signal at 30 points.
`gap_fit` rewards filling a topic that is thin — but the topics exist because of
what was already added, so it preferentially deepens existing interests and
reports that as coverage.

The composite-analogue table found this from the other side: the two empty rows
were the two capability gaps. Nothing has connected the two observations.

### 2.4 The taxonomy has never been validated against anything

Nine closed axes, one assigner, no second opinion, no test that any axis predicts
anything. `Data_Lineage` was added on argument, not evidence. `graph` would
partly test this — do the communities the links imply match the topics a person
assigned? — and has never run, which is Shape 1 again.

### 2.5 Nothing distinguishes *relevant* from *good*

`depth` and `adoption` gesture at quality; neither reads a line of code. A
source can be exactly the right shape and badly made, and the catalogue would
rank it identically. `NO_PERSISTENT_SOURCE_GRAPH` and the no-extraction boundary
are the reason, and they are correct — but the consequence has never been
written down: **this system locates candidates and cannot judge craft.** A user
who expects otherwise will be misled by a confident `why`.

---

## Part 3 — The Final Shape

Stated once, definitively, so the implementation plan has something to build to.

### What it is

**A reference guide that locates prior work and explains why, across three
surfaces over one engine, with three layers that each state only what they can
support.**

### The layers (unchanged, and load-bearing)

| Layer | Artefact | Asserts |
| --- | --- | --- |
| Data | `.Data/surveys/`, `source_components.sqlite` | This component was present at this commit on this date |
| Information | resource notes | What the components mean together, with inference marked |
| Knowledge | `Transferable Capability`, application records | What it can be used for; what it actually did |

### The surfaces (three, one engine)

| Surface | For | Entry |
| --- | --- | --- |
| CLI | maintenance and measurement | `python -m librarian …` |
| MCP | an agent, headless | `librarian serve` |
| Web | a person searching, and an assistant beside them | localhost |

No surface holds retrieval logic. All three call `consult`.

### The invariants (existing, and now complete)

`MARKDOWN_IS_TRUTH` · `NO_SCHEMA_DRIFT` · `EVIDENCE_REQUIRED` ·
`CLOSED_ACTION_REGISTRY` · `DOCUMENT_BEFORE_DESTROY` · `GRAPH_ADVISORY_ONLY` ·
`NO_PERSISTENT_SOURCE_GRAPH` · `POSTURE_DECIDES_CONSEQUENCE` ·
`LOCATE_DO_NOT_ADJUDICATE`

**Two to add**, both earned by Part 1:

- **`RUN_BEFORE_CLAIM`** — a service is not in the Service Map until it has
  produced a row, an answer or a recorded refusal. Shape 1, nine instances.
- **`THRESHOLD_CARRIES_ITS_DISTRIBUTION`** — any constant derived from corpus
  statistics ships with the function that re-derives it. Shape 4, two instances.

### What it explicitly is not

- Not a code search engine. It locates repositories and, after §2.1 is closed,
  components within them. It does not read code and cannot judge craft (§2.5).
- Not a live index of GitHub. It holds what was deliberately added; `freshness`
  keeps that honest and `coverage` says when the answer is not here.
- Not multi-user, not published, not a product. `usage.distribution_posture`
  and `usage.catalogue_role` encode that, and both flip in one edit if it changes.
- Not an extractor. `EXECUTION_SANDBOX_ONLY` and the workbench boundary hold.

---

## Part 4 — Implementation Plan

Revises [[Finalisation Plan 2026-09-04]]. The stages there are right; Part 2
adds one stage before them and changes what two of them must prove.

### Phase A — Make the claims true (days, not weeks)

**A1. Stage 0 debt.** Unchanged and first: six licences, four application links,
the freshness sweep, fifteen surveys, thirty-nine capture dates.
*Exit: `integrity` 0 warnings.*

**A2. Component retrieval — §2.1.** The new work, and it goes early because
everything downstream inherits the unit of retrieval. Add `kind: component` to
`Result`: a query matching `grammars` may return
`nene/sql-parser-cst › src/parser.pegjs` alongside the note. The data exists; the
work is a ranking that mixes two grains without letting the fine one flood the
coarse one. **Measured through `librarian relevance` like everything else**, with
a new scenario set phrased at component granularity.
*Exit: a measured verdict, and `RUN_BEFORE_CLAIM` satisfied for the data layer's
read path.*

**A3. Stage 1, with `RUN_BEFORE_CLAIM` applied.** Run `embed`, `graph`,
`access_points`; keep on a number or delete with a reason. `graph` now has a
second job from §2.4: report where the link structure disagrees with the assigned
taxonomy.
*Exit: no Service Map row without a row, an answer, or a recorded refusal.*

### Phase B — Make the measurements mean something

**B1. An externally-authored instrument — §2.2.** The cheapest honest fix: ten
scenarios written from a source *outside* this project's authorship — a real
question from another repository's issue tracker, a colleague's problem, an
archived Stack Overflow question. Not more self-written scenarios.
*Exit: both instruments reported with their provenance, and any gap between
self-authored and external scores stated rather than averaged away.*

**B2. Stage 2 — query understanding, or close it.** Unchanged, but B1 must land
first: deciding whether a model over the query helps, using only self-authored
questions, would measure the model against the author's phrasing.

**B3. Correct `gap_fit` for selection bias — §2.3.** It currently rewards
deepening what already exists. Rebase it on the composite-analogue map — grouped
functions the catalogue should cover — rather than on topic counts it produced
itself.
*Exit: `gap_fit` reads from a map of intended coverage, not from its own history.*

### Phase C — Make it a tool

**C1. Stage 3 — separate the tool from the vault.** Unchanged, and now gating
three things rather than one.

**C2. Stage 3a — MCP hardening.** FastMCP, progressive disclosure, stdio plus
loopback HTTP, effect classification at dispatch. Packaged as a skill.

**C3. Stage 3b — the web app.** Search-engine layout, metadata as tags, filters
that visibly eliminate, `why` under every result, `coverage` never buried. After
A2 this must also present two grains — a repository and a component within one —
which is a design decision worth making before the first pixel.

**C4. Stage 3c — the assistant, designed not wired.** Confirm the MCP schema and
result shape support citation rather than paraphrase.

### Phase D — Reduce the cost of being right

**D1. Stage 3d — local models for the information layer.** Acceptance is
`integrity` + `provenance` + `distinct_resource_prose`, not readability.

**D2. Stage 4 — cover the comparables**, through `scout.survey` end to end,
proving the write path.

**D3. Stage 5 — consolidate, then package.** Add to it: the fourth duplicate
implementation, found on purpose (Shape 5).

**D4. Stage 6 — the costs that hurt**, and add §2.5 to the documentation: state
plainly that this locates candidates and does not judge craft.

### What is deliberately still excluded

Runtime performance · a daemon or socket boundary between surfaces · more
self-authored scenarios before B1 · multi-user anything · any judgement of code
quality.

## Related
- [[System Assessment 2026-09-04]] — the measured state this reasons over
- [[Finalisation Plan 2026-09-04]] — the stages Phase C and D execute
- [[Data Information Knowledge]] — the layering Part 3 restates
- [[Design Specification]] — where the two new invariants belong
- [[Service Map]] — the inventory `RUN_BEFORE_CLAIM` will prune
- [[Master Index]]
