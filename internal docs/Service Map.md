---
type: "service_map"
status: "active"
created: "2026-09-04"
purpose: "what this system is made of, what each part does, and what each part's job is when stated without reference to this system"
services: 22
---

# Service Map

## Why This Exists

You cannot search for prior work on a component you have not named. The catalogue could
describe seventeen external systems in domain-neutral terms and still be unable to say what
*it* was made of — so a question like "is there a better way to do the thing our integrity
checker does" had nowhere to start.

Each entry below carries three things. **Role** is what it does here. **Job, stated
agnostically** is the same thing said without this system's vocabulary, which is what a query
against the catalogue can actually be built from. **Reference** names sources already
catalogued that address the same job, whether or not they were built for anything like this.

The third column is the point. It is also the column most likely to be wrong, because it is a
judgement rather than a fact — treat it as a starting set, not an answer.

---

## Write path — the intake

| Service | Role | Job, stated agnostically | Reference |
| --- | --- | --- | --- |
| `scout.discovery` | Finds candidate repositories from seed queries and by expanding catalogued lists | Enumerate candidates from a source you do not control, under a rate limit, without duplicating what you already hold | [[public-apis - public-apis]] · [[not-a-bank - open-banking-tracker-data]] · [[prometheus]] |
| `scout.rank` | Scores candidates on six weighted signals | Order a queue of unequal candidates using several unreliable signals, with no ground truth to calibrate against | [[snorkel-team - snorkel]] · [[NorskRegnesentral - skweak]] |
| `scout.domains` | The closed domain register; the scout may report `unmatched` but may not invent a key | Constrain what a classifier may output to a set only a person can change | [[SigmaHQ - sigma]] · [[open-metadata - OpenMetadata]] |
| `scout.evaluate` | Enriches, ranks, freezes a cohort, writes the cohort note | Batch work into reviewable units and make the unit, not the item, the thing approved | [[apache - airflow]] · [[asreview]] |
| `scout.deep_dive` | Escalates the top fraction to a slower, closer read | Spend an expensive step only where a cheap one says it will pay | [[asreview]] · [[semgrep - semgrep]] |
| `librarian.clone` | Shallow fetch and disposal of a source | Acquire material for inspection and guarantee its removal afterwards | [[hashicorp - terraform]] |
| `librarian.intake` | Clone → investigate → summarise → discard | Derive a durable description from material you do not keep | [[recipy - recipy]] · [[HCAI-Lab-GT - capabilibara]] |
| `librarian.toolchain` | Adapter to an external investigation pipeline | Call a capability that may be absent, and degrade to a named partial result rather than failing | [[hashicorp - terraform]] · [[netdata]] |

## Store — derived and disposable

| Service | Role | Job, stated agnostically | Reference |
| --- | --- | --- | --- |
| `librarian.notes` | Parses the vault; the only place that decides what a note *is* | Turn a directory of documents into typed records, with one authority on the shape | [[Instagram - LibCST]] · [[syntax-tree - mdast]] |
| `librarian.content_model` | Reads [[Note Content Model]], which is the schema | Hold a schema as a readable artefact and validate against it rather than generating from it | [[syntax-tree - mdast]] · [[open-metadata - OpenMetadata]] · [[stac-utils - pystac]] |
| `librarian.index` | Vault → SQLite rows, chunks, links, FTS5 | Build a disposable derived store that can be deleted and rebuilt with nothing lost | [[duckdb - duckdb]] · [[dbt-labs - dbt-core]] |
| `librarian.views` | Regenerates the taxonomy matrix, topic membership and route-map counts | Derive every presentation from one source of truth so no copy can be wrong | [[dbt-labs - dbt-core]] · [[github - government.github.com]] · [[twbs - bootstrap]] |
| `librarian.embed` | Optional vectors, brute-force cosine | Add an approximate retrieval path that must never become a dependency | [[run-llama - llama_index]] |
| `librarian.graph` | Communities, filtered centrality, community reports | Find groupings nobody assigned, and describe each one so the whole can be asked about | [[microsoft - graphrag]] · [[neo4j-labs - neocarta]] |
| `librarian.access_points` | Extracts, stores and verifies addresses found in notes | Pull a small class of durable pointers out of material you otherwise refuse to copy | [[urchade - GLiNER]] · [[public-apis - public-apis]] |

## Read path — consult

| Service | Role | Job, stated agnostically | Reference |
| --- | --- | --- | --- |
| `consult.eligible` | Hard filters; an unknown value is eliminated, never demoted | Remove candidates that cannot satisfy a stated requirement, rather than ranking them lower | [[PHACDataHub - data-mesh-ref-impl]] · [[semgrep - semgrep]] |
| `consult.by_name` / `lexical` | Name, frontmatter and full-text retrieval | Find records by several different kinds of match and keep each kind distinguishable | [[run-llama - llama_index]] · [[duckdb - duckdb]] |
| `consult._search` | Fuses the rankings by Reciprocal Rank Fusion | Combine several orderings without calibrating their scores against each other | [[snorkel-team - snorkel]] · [[run-llama - llama_index]] |
| `consult` query kinds | Six typed questions, each returning a different shape | Serve several distinct question shapes from one store, choosing the structure per question | [[run-llama - llama_index]] · [[microsoft - graphrag]] |
| `librarian.evalset` | Twenty questions with known answers | Measure a change against a fixed instrument instead of an argument about whether it helped | [[asreview]] · [[duckdb - duckdb]] · [[hashicorp - terraform]] |

## Freshness, coverage and feedback — added 2026-09-04

| Service | Role | Job, stated agnostically | Reference |
| --- | --- | --- | --- |
| `scout.survey` | Decomposes a repository into components without reading its code | Derive structure from material you refuse to copy, cheaply enough to do it for everything | [[tree-sitter - tree-sitter]] · [[jgravelle - jcodemunch-mcp]] |
| `librarian.freshness` | Re-checks recorded claims against upstream; reports, never edits | Detect that a description and the thing it describes have diverged, without deciding what to do about it | [[dbt-labs - dbt-core]] · [[prometheus]] |
| `librarian.coverage` | Whether an answer is worth trusting, in absolute terms | Say "I do not hold this" instead of returning the best available irrelevance | [[asreview]] · [[jgravelle - jcodemunch-mcp]] |
| `librarian.duplicates` | Candidate near-duplicate sources; reports, never merges | Find records that describe one thing before a reader has to notice, and leave the merge to a person | [[asreview]] · [[corzosoft - azure-edm-reference-data-platform]] |
| `librarian.provenance` | The catalogue's own structural claims, against the surveys | Attribute a derived statement to the input that supports it, and make the link checkable | [[recipy - recipy]] · [[whole-tale - provenance-examples]] |
| `librarian.usesignal` | What an answer turned out to be worth | Accumulate judgements about your own output so ranking can eventually be fitted rather than argued | [[elastic - elastic-labs]] · [[snorkel-team - snorkel]] |
| `consult.find_components` | Addresses inside a source, not just the source | Return the part of a thing that answers the question, at the grain the question was asked | [[jgravelle - jcodemunch-mcp]] · [[tree-sitter - tree-sitter]] |
| `librarian.queryunderstanding` | Separates the ask from the context it arrives in | Distinguish a request from the situation described around it | [[urchade - GLiNER]] · [[guillaumegenthial - sequence_tagging]] |
| `librarian.relevance` | Ranking configurations, side by side on one index | Compare methods by expressing each as a configuration over shared stages | [[elastic - elastic-labs]] · [[JayLZhou - GraphRAG]] |

**Three of these are switched off, and that is the finding.**
`queryunderstanding` was implemented in two forms and both measured worse than
doing nothing; `usesignal` reads nothing because there is no data yet;
`coverage` reports `thin` — meaning *no opinion* — for every question that is
not from outside the collection entirely. Each is kept because the harness to
judge it exists and the next attempt should start from the measurement rather
than repeat it.

### Progress, 2026-09-05

**A1 (debt) partly cleared.** Integrity warnings **10 → 4**. Sixteen notes
re-captured from stored freshness readings. The remaining four are the
application records, and they are **blocked on a person**: all four describe
their sources anonymously (*"the first"*, *"an open-source UI application"*), so
only whoever did the work can link them. Guessing would fabricate provenance.

**Two corrections owed and made.** The assessment claimed the six
`licence_undercaptured` sources were *silently withheld from every constrained
answer*. They were not: the 2026-09-03 backfill had already resolved every one
from LICENSE text, so `license_class` was `Permissive` throughout and nothing
was withheld. Only the `github_license_spdx` snapshot was stale. `freshness` now
splits that into `licence_stale_api_field` (recorded, does not warn) and
`licence_undercaptured` (warns, genuinely eliminated), and gained
`licence_class_disagrees` for the actually dangerous case — a note resolved to
`Permissive` against an API now reporting GPL. That last one fires correctly on
a synthetic case and **finds nothing across the corpus**, so no source is
mis-classified.

**A2 (component retrieval) built.** `consult.find_components` returns addresses
— `mdebellis/SemanticKG-Design > docs/peopleOntology/ontology.nt` — alongside
notes, capped at three and appended rather than interleaved. Both instruments
are byte-identical with it on and off, which is a proof of **no cost** and not a
proof of benefit; neither can supply the latter, because both score note names
only. Component-granularity scenarios are the missing instrument and they wait
on externally-authored ones.

Two defects were introduced and caught within minutes, both by existing tests:

- **Components bypassed `eligible`**, so a query constrained to `Permissive`
  returned addresses inside sources the constraint had just eliminated. Nine
  tests failed at once. *Constraints eliminate* is the invariant this system
  rests on, and a component is part of its source, not an exception to it.
- **Substring matching returned `app/sidekiq` and `components/SideNav`** for a
  query about ranking configurations *side by side* — Shape 2 from
  [[Meta Analysis And Final Shape 2026-09-04]], reintroduced by hand within a
  day of naming it. Fixed with the whole-segment matcher that already existed.

The surveyor now stores **full path listings** rather than ten-path samples,
because component retrieval could reach `relevance-workbench` and `goldset` at
depth 1-2 and could not reach `sqllogictest` or `multitask` at all. Surveys
written before 2026-09-05 carry samples; the difference is recorded rather than
papered over.

**Blocked:** the GitHub API budget is exhausted (0 of 60 unauthenticated), so
seventeen unsurveyed resources and the remaining freshness sweep wait for the
reset or a `GITHUB_TOKEN`.

### Stage 4 done, 2026-09-06 — the person surface

`librarian web` serves one page from `127.0.0.1` and holds **no retrieval
logic**. Every number on it comes from `consult.find_donor`, the same call the
CLI and the MCP server make, so the three surfaces cannot disagree about what
the catalogue contains. Standard library only — no framework, no build step, no
CDN — because a tool for reading a local vault should work with the network
unplugged, and every remote asset is a way for it to stop working later.

It is a **product catalogue, not a search engine**, which was the user's
correction and the right one: the objects are strongly typed across ten closed
axes, and a person narrowing candidates wants to see how those axes fall across
*the set they have*. Drop-downs are built from `facet_counts` over the result
set, so `Domain: Code_Intelligence (13)` is the size of what survives choosing
it, not a number from the vocabulary.

Four things were fixed by looking at it rather than by reasoning about it:

- **Clicking a facet's label did nothing.** The listener was bound to the
  checkbox after each render; a click on the label text ticked the box natively
  and never reached the handler. The page then showed a filter the engine had
  not applied — the worst available outcome, and invisible. Delegated listeners
  bound once to the containers.
- **`hidden` did not hide.** `.facet label { display: flex }` beats the user
  agent's `[hidden] { display: none }`, so the show-more cap silently showed
  everything.
- **The counters invited an arithmetic the engine never did.** `matched +
  filtered_out ≠ considered` is documented in `consult` — filters run first and
  most survivors match no term — but printing both totals in one line reads as
  a subtraction. Rewritten as two ordered steps: *117 of 130 removed by
  Licence: Copyleft · 4 of the remaining 13 match your words*, which reconciles.
- **An axis with one surviving value is dropped from the sidebar**, correctly,
  but that removed the only control holding an active constraint. Applied
  filters are now removable chips of their own.

Three page-level tests enforce claims that would otherwise rot quietly: no
`https://` asset reaches the page, `AXIS_LABELS` covers every `FACET_FIELDS`
axis (`NO_SCHEMA_DRIFT` across the surface boundary), and the script contains
no sorting or scoring. Each was demonstrated firing before being trusted,
per `FAILURE_MUST_BE_LOUD`.

### Stage 3b engine, and a cold agent test that found seven defects

The faceting half of 3b is in the engine, not the page: `consult.facet_counts`
returns per-axis value counts over **the candidate set**, so a drop-down offers
`license_class: Permissive (26), Copyleft (4)` rather than the full enumeration
with zeroes. Two properties fall out of decisions already made — a count is the
size of the surviving set, because filters eliminate rather than demote, so the
reader sees the cost of a constraint before paying it; and an axis that does not
vary is omitted, which is a coverage statement the ranked list cannot make.

**Then a second agent was pointed at the surface with no documentation and told
to report friction.** It found seven defects. All seven reproduced, and the two
worst produced confidently wrong answers:

| Finding | Status |
| --- | --- |
| A constraint removed the only correct answer and the response never said so | Fixed — `advisories` names what was eliminated |
| `license_class` enum absent from `find_donor`'s schema, and a case mismatch returned `0 matched` instead of an error | Fixed — `axis_vocabulary()` from [[Note Content Model]]; unknown values refused with the permitted list |
| Component rows carried `license_class: None` under a licence constraint | Fixed — they were correctly filtered but did not *show* it; a constraint you cannot verify held is one a caller must assume did not |
| `matched + filtered_out` did not reconcile; `limit=N` returned N+1 | Fixed — `considered`/`matched`/`filtered_out` named, and components moved to their own field so `limit` means sources |
| Facets advertised seven axes `find_donor` rejected with a raw `TypeError` | Fixed — it accepts all ten |
| An out-of-domain answer looked identical to a good one | Fixed — the `coverage` verdict now reaches the response and changes `next_step` |
| `tier_reached` / `partial` undocumented | Open |

Its sharpest observation was about a wrong answer rather than an error: asked
for a permissively-licensed SQL parser, the catalogue silently dropped
[[nene - sql-parser-cst]] (GPL-2.0) and returned an *mdast* Markdown spec at the
top with the same cheerful next step as a good answer. The honest response is
that the only SQL concrete-syntax-tree parser here is copyleft. It now says so.

**And fixing this broke `cli.py` syntactically while 292 tests passed**, because
nothing in the suite imported it. A green suite over an unparseable entry point
is measuring the wrong thing; `test_cli_smoke` now imports every shipped module.

### Stage 3a done, 2026-09-06 — the agent surface is usable by a stranger

**A correction first: FastMCP was already in use.** The plan said to adopt it;
`build_server()` had been calling `mcp.server.fastmcp` since it was written.
One of four items was already done, and saying so is cheaper than quietly
dropping it.

The three that were not:

**Progressive disclosure.** `capabilities()` returns a short card per tool -
purpose, when to use it, declared effect - and names `capability_schema(name)`
as the next call. Ten tools with nine filter axes is far too much schema to put
in front of an agent that has not yet decided what it is doing; a card is a few
dozen tokens. The staging is lifted from the capability registry in
`F:/Mark-XLVIII-main` (L0 card → L1 manifest → playbook → schema) and is the
same cheap-first progression as [[Data Information Knowledge]] one layer up.

**Effect classification, declared and separately enforced.** Every tool now
carries the standard MCP annotations - `readOnlyHint`, `destructiveHint`,
`idempotentHint`, `openWorldHint` - so a client can reason about a tool before
calling it. But the MCP specification states plainly that *annotations are
hints, not security guarantees*, and the Mark-XLVIII handbook states the same
rule in its own words: *registry metadata is not permission*. Two independent
sources, one conclusion, so `check_permitted` enforces separately from
`EFFECTS` and a test corrupts the annotation table to prove that widening the
description does not widen what is allowed.

**Two transports, loopback only.** stdio for an agent launched as a subprocess,
`--http` for the web app in Stage 3b. A non-loopback `--host` is refused
outright rather than warned about: a catalogue of one person's research has no
business on a network interface, and refusing is cheaper than explaining the
consequences of allowing. `--read-only` removes `record_application` from the
surface entirely rather than merely refusing it when called.

Verified against the real server rather than asserted: it builds, exposes 12
tools, the annotations arrive on the client side, `capabilities` is callable,
`--read-only` genuinely omits the write, and the HTTP transport binds 127.0.0.1.

**Fourteen tests**, the sharpest being that a refusal names the rule and lists
what *is* registered — a blocked agent should surface a decision, not a stack
trace.

### Stage 3 done, 2026-09-06 — the tool is separable from the vault

`CATALOGUE_VAULT=/elsewhere python -m librarian status` now works on an empty
directory, reports what is missing, and writes its index into **that** vault.

The defect was not that the override was absent; it was that it was
**half-wired**, which is worse. Fifteen call sites asked `vault_root()` and
respected it; seventeen used a module constant computed at import from the
package's own location and silently did not — including the one deciding where
the databases lived. Pointing the tool elsewhere read the index from one place
and wrote it to another, with nothing raising and nothing warning.

The cause is general and worth naming: **a path resolved at import cannot follow
an environment variable set afterwards.** `DATA_ROOT`, `DATABASE_DIR`,
`INDEX_DB_PATH`, `COMPONENT_DB` and `SURVEY_DIR` were all constants captured as
default arguments. They are now functions — `data_root()`, `database_dir()`,
`index_db_path()`, `component_db_path()`, `survey_dir()` — and the old constants
remain only as their defaults.

Machine paths left the package at the same time. `graphify_bin` and
`toolchain_candidates` default to empty and live in `library_config.json`; the
two adapters read their roots from the same file instead of carrying
`F:\knowledge\...` in a module. `toolchain.py` had always probed rather than
hard-coded and was the model. Nothing regressed: graphify and the ToolSet are
still found, now by configuration rather than by compilation.

`scout` gained its own `vault_root()` rather than importing librarian's, so the
two packages share a contract (the environment variable) and not an import.

**Six tests hold this true**, including the two that matter: every resolver
follows the override, and a run against another vault does not touch this one.
The failure they guard against is invisible — nothing raises, the answers are
merely wrong.

### Stage 2 closed, 2026-09-05 — the gap is corpus-shaped

Eight representations of a query have now been measured against the same thirty
scenarios, and **none separates a question the catalogue answers from one it
merely holds adjacent material for**:

| Representation | Lift over "always answerable" |
| --- | --- |
| five lexical overlap signals | none; unanswerable matched *more* |
| cosine, whole query | **+0%** |
| cosine, segmented ask only | **+0%** |
| cosine, the hand-written `component` phrase | **+0%** |

The last row settles it. `component` is a short phrase written by hand to say
exactly what is being asked, with no surrounding context to dilute it, and a
threshold on it does no better than assuming every question is answerable.

Cosine at least points the *right way* — the answerable median exceeds the
unanswerable one in all three variants, where the lexical signals had it
backwards — but a consistent shift you cannot threshold is not a decision
procedure.

**This is the expected result, not a disappointing one.** The unanswerable
scenarios are questions the catalogue holds genuinely adjacent material for.
Telling *I have this* from *I have things like this* cannot be done from the
question however it is represented, because the difference lies in whether the
retrieved thing actually answers it — a judgement about the **result**, not the
query.

So Stage 2 closes on its second stated outcome. Holding more material is Stage
4's job, not the ranker's. `coverage.separation_probe()` re-runs the comparison;
with only five unanswerable scenarios this bounds the effect size rather than
proving zero, so it should be re-run when the set gains negatives.

### A3 — RUN_BEFORE_CLAIM applied, 2026-09-05

Three services had code, tests and **zero rows**. Each was run.

| Service | Outcome | Verdict |
| --- | --- | --- |
| `graph` | 11 communities over 346 notes, **4 disagreements with the assigned taxonomy** | **Keep.** It answers a question nothing else can |
| `access_points` | 1 access point from 130 sources | **Works; near-idle.** See below |
| `embed` | eval MRR **0.917 → 0.950**, strong@5 0.77 → 0.80, scenario MRR −0.019 | **Keep.** Decided on the number |

**`graph` earns its place immediately.** The four disagreements are the §2.4
taxonomy validation nothing else could perform, and every one is plausible
rather than noise: the SIEM tools (`siembol`, `suricata`, `sigma`, `falco`)
cluster with Infrastructure, the geospatial tools (`gdal`, `geopandas`, `geoq`)
cluster with Data, and the CAD tools (`cadquery`, `FreeCAD`, `openscad`) cluster
with Frontend & Design. The links between those pairs are real. `GRAPH_ADVISORY_ONLY`
means this is a report for a person and reassigns nothing.

**`embed` keeps its place on the eval, not on faith.** 2,201 chunks embedded.
The eval gains 0.033 of MRR and `strong@5` gains 0.03; scenario MRR loses 0.019
and cross-domain 0.03, and the miss count is unchanged at five — but the misses
*trade*: vectors surface `chef` for `works-only-when-everything-is-up`, a
scenario that had never had an acceptable answer reach the top five since it was
written, and lose two others. A gain on the instrument that guards the index and
a wash on the one that guards the point.

**`access_points` is a decision for a person.** It ran, it works, and it
extracted one row from 130 sources — which reflects the corpus rather than the
code, since almost everything catalogued is a library or a tool rather than a
service. It now satisfies `RUN_BEFORE_CLAIM`; whether one row justifies a
subsystem is a judgement, and deleting it is irreversible, so it is recorded
here rather than actioned.

### A1 completed, 2026-09-05

All 130 sources are surveyed. The seventeen that predated the surveyor were run
**through `scout.survey` end to end with zero failures** — the first cohort ever
processed without a scratchpad, which is the write-path proof Stage 4 was going
to have to produce.

Those seventeen carry **full path listings** rather than ten-path samples, and
the difference is immediately visible: `urchade/GLiNER > gliner/multitask` is
now reachable by query and was not before. `duckdb`'s `sqllogictest` corpus
still is not, because duckdb was surveyed on 2026-09-03 and carries samples —
so the sampled/full split is a real, observable property of the store rather
than a footnote.

The data layer now holds **43,183 full paths** alongside 5,624 sampled ones.

### Two defects found by running, 2026-09-05

- **`provenance` flagged a hedged number as a contradiction.** `tree-sitter`'s
  note says *"~30 files"* against a survey recording 28. Reporting that as an
  error punishes exactly the honest approximation that makes a note readable;
  hedged numbers are now `unsupported` rather than `contradicted`.
- **Two genuine drifts in `llama_index`** — 93 files against 91, 25 against 26 —
  because the repository changed between its 2026-09-03 survey and 2026-09-05.
  That is the check doing its job, and the corresponding test was over-strict:
  it asserted *zero* contradictions, which would fail every time a source
  legitimately changes. It now asserts a low rate.

### What building them found

Each was built against a gap named in [[System Assessment 2026-09-04]], and four
of them turned up a defect that was already there:

- **`clone.shallow_clone` had never worked over the network on this machine.**
  It built a subprocess environment from nothing — `{GIT_TERMINAL_PROMPT,
  GIT_ASKPASS, PATH}` — which on Windows drops `SystemRoot`, so every clone
  failed at `getaddrinfo() thread failed to start`. It failed at DNS, before any
  network policy applied, which is why it read as a connectivity problem. The
  empty `workbenches/` directory and the single recorded intake run are
  consistent with this never having worked.
- **The proven-use bonus had never fired.** `application_count` was zero for all
  130 resources, because the four application records name their sources in
  prose rather than linking them. Fully built, correctly wired, receiving
  nothing.
- **The first cohort systematically under-recorded licences.** The first real
  freshness pass found six sources whose notes say `UNKNOWN` where the API
  reports MIT, Apache-2.0, BSD-3-Clause or CC0. `license_class` eliminates, so
  each was being silently withheld from every constrained answer.
- **The surveyor duplicated the shared GitHub client, worse.** The scratchpad
  version used a bare `urlopen` against a 60/hour unauthenticated limit while
  `discovery` already handled tokens and rate limits.

## Guards and surfaces

| Service | Role | Job, stated agnostically | Reference |
| --- | --- | --- | --- |
| `librarian.integrity` | Sixteen assertions over the vault | Assert properties of a corpus declaratively, separating what fails a run from what only warns | [[dbt-labs - dbt-core]] · [[SigmaHQ - sigma]] · [[stac-utils - pystac]] |
| `librarian.policy` | Named refusal codes; a closed action registry | Refuse by naming the rule that refused, so a blocked caller surfaces a decision rather than improvising | [[PHACDataHub - data-mesh-ref-impl]] · [[NatLabRockies - api-umbrella]] |
| `librarian.workbench` | Mode D: open, document, close; `close` refuses without a record | Make the valuable by-product of a temporary environment the price of destroying it | [[recipy - recipy]] · [[cfpb - open-source-checklist]] |
| `librarian.mcp_server` | The agent surface; read-only but one write | Expose a capability to a consumer you do not control, with the permitted actions enumerated | [[neo4j-labs - neocarta]] · [[open-metadata - OpenMetadata]] · [[vercel-labs - skills]] |
| `librarian.webapp` | The person surface; loopback-only, dependency-free, no retrieval logic | Put a third front end on one engine without letting it acquire an opinion of its own | [[nene - sql-parser-cst]] · [[open-metadata - OpenMetadata]] |

---

## What This Map Is For

Three uses, and the second is the one that was missing.

1. **Orientation.** What exists, and where a change belongs.
2. **Cross-reference.** The agnostic column is a query. Running it against the catalogue asks
   *what else does this job, possibly by another name* — which is the question
   [[Use Contexts And Agnostic Description]] argues nothing was ever asked.
3. **Test material.** The scenario harness (`librarian scenario`) builds test cases by taking a
   component from here or from a catalogued system, describing it in its own vocabulary, and
   asking whether the catalogue surfaces anything useful. The map is what makes those scenarios
   possible to write.

## What The Test Found

`librarian scenario --sample 0`, 30 scenarios. Two are marked in the corpus as expected to
fail; a scenario set containing only answerable questions measures nothing.

| Measure | 16 scenarios | 30 scenarios | After stemming | 128 resources | Current |
| --- | --- | --- | --- | --- | --- |
| useful@5 | 0.88 | 0.80 | 0.93 | 0.87 | **0.90** |
| strong@5 | 0.81 | 0.73 | 0.80 | 0.80 | **0.83** |
| MRR | 0.71 | 0.64 | 0.77 | 0.70 | **0.69** |
| cross-domain | — | 0.43 | 0.63 | 0.53 | **0.53** |

The fourth column is the same thirty scenarios after the 2026-09-04 cohort took the corpus
from 81 resources to 128; three of four measures fell. The fifth is current. **Only the last
two columns are comparable with each other**, and even then loosely — every column before it
was measured against a different vault, including different index notes. See the retraction
below.

**The metric changed between the first two columns and the change was a correction, not a
result.** `cross-domain` was measured against the two or three topics a scenario said an answer
might come from, so it reported *answers from topics nobody anticipated* and called that
alternative discovery. It now measures against `home_topic` — the single field the asker is
working in — which is what the phrase always meant. The old number is still printed as
`unanticipated` so the two are never confused.

**The largest single finding was stemming.** The full-text index had none, so `institution`
matched nothing while `institutional` matched four chunks. A source describing itself as a
corpus of *institutional records* was unreachable to anyone asking about institutions. Enabling
the `porter` tokenizer moved every measure at once — scenario MRR 0.64 → 0.77, cross-domain
0.43 → 0.63, and the twenty-question eval from 0.92 to 0.94. Nothing in the eval could have
found this: its questions are phrased the way the notes are written.

### What growing the corpus cost, what fixed it, and one claim retracted

**A retraction first.** An earlier version of this section reported that raising
`SELECTIVITY_CEILING` from 0.34 to 0.50 recovered a scenario outright, with a sweep table
behind it. That measurement was real and it does not reproduce. Between taking it and
re-taking it, five index notes in this vault were edited and re-indexed — and **document
frequency was being computed over every note in the vault**, so editing design documents
changed which query terms counted as selective. On the current corpus, 0.34 and 0.50 are
indistinguishable on `useful@5`. The gain was genuine and it was not the ceiling.

That confound is the reason `librarian relevance` now exists.

### The relevance workbench

Taken from [[elastic - elastic-labs]], whose `relevance-workbench` is an application whose
whole purpose is putting two ranking configurations side by side on the same corpus, and
from [[JayLZhou - GraphRAG]], which makes ten published methods comparable by expressing
each as a configuration over shared stages rather than as ten programs.

```
python -m librarian relevance                  # every configuration, one index, one pass
python -m librarian relevance --only current,coverage-bm25
```

Configurations live in `rank_configs.json` as data, so adding one is not a code edit, and
**a configuration that lost is kept rather than deleted** — a rejected option nobody can
re-run is folklore, not a finding. Every row runs against one index in one process, which is
the property the retraction above turned on: a number from a previous session cannot be
compared with one from this session, because both instruments read the vault and the vault
contains this system's own notes.

### What it found immediately

**The denominator was wrong, in the opposite direction to the earlier diagnosis.** Document
frequency counted all 343 notes, but only 132 — `resource`, `review`, `paper` — can ever be
an answer. The other 211 are short glossary, pattern, topic and design notes, and they
dilute the count. Measured over notes that can actually be returned:

| term | df over all notes | df over answerable notes |
| --- | --- | --- |
| `read` | 0.53 | **0.96** |
| `file` | 0.48 | **0.93** |
| `files` | 0.38 | **0.86** |
| `test` | 0.39 | **0.73** |

So the earlier finding — *the ceiling wrongly discarded `file` and `files`* — was backwards.
Those terms appear in nearly every resource note and discriminate nothing; the wrong
denominator was letting them through. `selectivity_scope="answerable"` is the default from
2026-09-04.

**The two knobs interact, which is why they had to be gridded rather than tested singly.**
Ordering covered notes by the BM25 score FTS5 already computed — instead of by a raw count
of matched terms, which treats `service` and `malformed` as equally decisive — is *worse*
under the old denominator and *best* under the corrected one:

| scope | ceiling | coverage order | eval MRR | useful@5 | strong@5 | misses |
| --- | --- | --- | --- | --- | --- | --- |
| all | 0.50 | terms | 0.942 | 0.87 | 0.80 | 4 |
| all | 0.50 | bm25 | 0.908 | 0.83 | 0.77 | 5 |
| answerable | 0.50 | terms | 0.942 | 0.83 | 0.80 | 5 |
| **answerable** | **0.50** | **bm25** | **0.917** | **0.90** | **0.83** | **3** |

Shipped as the last row. The cost is stated plainly: **eval MRR falls from 0.942 to 0.917,
which is exactly one of the twenty questions moving from rank 1 to rank 2**, with `hit@5` and
`recall@5` both unchanged at 1.00. Bought with it: two scenarios recovered and the best
`strong@5` of any configuration in the grid. That trade favours the instrument that measures
the point over the one that measures the index, which is the standing preference here.

`coverage-off` scores worse than `current` on both misses and cross-domain, so the coverage
stage does earn its place — worth knowing, since nothing had previously tested whether it did.

**`config-validation-surface` fails under every configuration in the grid**, so neither knob
is its cause. Its description names a storage engine and a query layer as explicitly *out of
scope*, and those are the terms driving the result: the ask and the surrounding context are
not distinguished. That is a real problem and a general one — every genuine request contains
context that is not the request — and it is open.

**What the test still cannot see.** All thirty scenarios were written against the
81-resource corpus, so none probes lineage, parsing, retrieval or ontology design.

Earlier runs found three more, all of the same kind — evidence being counted that was not
evidence:

- a caveat read as a claim (`Reading Notes` terms sitting inside *"It is not that"*);
- verbosity as a ranking signal (`rrf` summing one note's many matching sections);
- taxonomy identifiers matching prose (`interface_protocol: "REST"` matching *the rest of the
  system*).

**Two scenarios still fail by design, and are kept as negative controls rather than as
open work.** Neither is a live concern; both exist to make the instrument honest, because a
scenario set containing only answerable questions measures nothing:

- `gpu-execution-alternative` — *the execution model itself may be the constraint*. Nothing in
  the catalogue covers array programming or accelerator models. It is the scenario that
  motivated [[Use Contexts And Agnostic Description]], and it is kept for that reason rather
  than as a gap anyone is being asked to close — the project it came from is long finished.
- `works-only-when-everything-is-up` — *degrade when a dependency is absent*. This system holds
  that property strongly and almost no catalogued source is *described* by it. A coverage gap
  that is also a warning: the property is well documented here and would not be found here
  either, by anyone searching rather than reading.

## What It Does Not Claim

The Reference column is a hypothesis per row, not a finding. Some entries are strong — the
ranking service really is doing what weak supervision does, and the derived-store service
really is doing what a build tool does. Others are a stretch recorded honestly so it can be
argued with. **A wrong entry here is more useful than a blank one**, because it is falsifiable
and a blank is not.

## Related
- [[Use Contexts And Agnostic Description]] — why the agnostic column exists
- [[Design Specification]] — the intended architecture these services implement
- [[Applicable Techniques From The 2026-09 Cohort]] — what each referenced source actually offers
- [[Master Index]]
