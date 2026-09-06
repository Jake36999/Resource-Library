---
type: "roadmap"
status: "active"
created: "2026-09-04"
purpose: "from measured weak spots to a standalone tool with three surfaces, in stages with exit criteria"
supersedes: "Finalisation Plan"
---

# Finalisation Plan 2026-09-04

## How This Plan Is Ordered

Six stages, and the order is not preference. Each one either removes debt the
next would inherit, or produces the evidence the next needs to be decided.

Two rules apply throughout, and they are why this is a plan rather than a wish
list. **Nothing ships unmeasured** — every retrieval change goes through
`librarian relevance`, which runs both instruments against one index in one
pass. And **a service that has never run is a liability, not an asset** — three
of them are in Stage 1 precisely because the catalogue currently claims
capabilities nobody has exercised.

**Three surfaces, one engine.** A person searches, an agent calls, and an
assistant does both on the person's behalf. All three read the same `consult`
functions, and keeping that true is the most important architectural decision in
this plan - the moment a surface grows its own retrieval logic they start
disagreeing and nobody can tell which is right.

`F:\Mark-XLVIII-main` solves this with a daemon and thin JSON-RPC shims
(`lmstudio_fastmcp_shim.py` talks to a bridge over a loopback socket). That is
correct at its scale and **over-engineering here**: for a single-user tool,
three thin surfaces importing one library need no daemon, no socket and no
serialisation boundary. Revisit only if a surface must outlive a process.

There is deliberately **no performance work**. `index` rebuilds 344 notes in
0.6 s and a query returns in well under a second. The cost that actually hurts
is *effort per source* and *effort per correct answer*, and Stage 6 addresses
those. Optimising a 0.6 s step would be complexity creep of exactly the kind
this catalogue exists to notice.

---

## Stage 0 — Clear the measured debt

Everything here is already identified by an instrument. No investigation, no
design, no risk.

| Work | Why it is debt | Cost |
| --- | --- | --- |
| Apply the 6 `licence_undercaptured` findings | `license_class` **eliminates**, so each is silently withheld from every constrained answer | Small |
| Link the 4 application records to their resources | `application_count` is 0 for all 130, so the proven-use bonus has never fired | Small |
| Finish the freshness sweep — 33 of 130 checked | The rest stopped at the unauthenticated 60/hour limit; a `GITHUB_TOKEN` raises it to 5,000 | Small |
| Survey the 15 resources with no component data | 113 of 128 are surveyed; the rest predate the surveyor | Small |
| Backfill `metadata_captured_at` on 39 notes | Freshness cannot reason about staleness without a capture date | Small |

**Exit:** `integrity` reports 0 warnings across 21 checks; 128/128 surveyed;
130/130 freshness-checked.

---

## Stage 1 — Run what was built and never run, then keep or delete it

`embed`, `graph` and `access_points` each have code, tests, degradation paths
and **zero rows**. Their dependencies are installed and reachable, so this is
not blocked — it is unexercised. Each leaves this stage either *measured and
kept* or *deleted with a recorded reason*.

- **`embed`** — build vectors, add a configuration to `rank_configs.json`, run
  `librarian relevance`. The eval already showed embeddings changed nothing on
  its twenty questions; the scenario test is a different instrument and may
  disagree. **Decide on the number, not on the fact that it exists.**
- **`graph`** — communities over 344 notes answer one question nothing else
  answers: does the topic taxonomy a person assigned match the structure the
  links imply? A disagreement is a finding about the taxonomy, and
  `GRAPH_ADVISORY_ONLY` already says what may be done about it.
- **`access_points`** — no demand has appeared in any use of this system.
  The default here is **deletion**, not retention. Keeping an unused subsystem
  because it was specified is how 46 modules become 60.

**Exit:** no service in the Service Map has zero rows and no recorded reason.
Expect at least one deletion; a stage that keeps everything has not been run
honestly.

---

## Stage 2 — Close the one bounded gap, or declare it closed

Query understanding is the only weak spot where the problem is *understood* and
the remedy is not. The evidence is unusually firm:

- Five overlap-derived signals, none separating answerable from unanswerable —
  and the unanswerable scenarios match **more** terms than the median
  answerable one (`coverage.calibrate()`).
- Two segmentation remedies, both worse than doing nothing: deletion 5 misses
  against 4, weighting 7 (`queryunderstanding`).

**It cannot be solved by re-weighting words.** What remains is a representation
of what a question is *about*, which means a model over the query. The
comparison is already set up: add a configuration and run `librarian relevance`.

Two outcomes and both are acceptable:

- It works. `config-validation-surface` passes, `coverage` starts separating
  *adjacent but wrong* from *covered*, and the system can be trusted to say
  "I do not hold this" for more than out-of-domain questions.
- It does not. The gap is then declared **corpus-shaped rather than
  ranking-shaped** and closed: the catalogue answers what it holds, and holding
  more is Stage 4's job, not the ranker's.

**Exit:** a measured result either way, recorded in `rank_configs.json` so it
cannot be re-litigated from memory.

---

## Stage 3 — Separate the tool from the vault

**This is the architectural blocker to everything after it**, and it is a
genuine design defect rather than packaging work.

The code lives *inside* the vault: `VAULT_ROOT = UTILITY_ROOT.parent`, computed
at import from the module's own location. The override exists and is
**half-wired** — 15 call sites use `vault_root()` and respect
`CATALOGUE_VAULT`; **17 use the frozen constant and silently do not**,
including `DATA_ROOT`, which is where the databases and surveys live. So
pointing the tool at another vault today half-works, which is worse than not
working: the index would be read from one place and written to another.

Alongside it, absolute paths to this machine are compiled into defaults —
`F:\uv-data\bin\graphify.exe`, `D:\Aletheia_project\DEV_TOOLS\ToolSet`,
`F:\knowledge\...` — in `adapters/`, `librarian/config.py`, `preflight.py` and
`library_config.json`.

Work:

1. One resolution path. `vault_root()` everywhere; `VAULT_ROOT` becomes its
   default, not a parallel truth. `DATA_ROOT` and `DATABASE_DIR` derive from it
   at call time, not at import.
2. Machine paths move out of code into config, with discovery-by-probing where
   a default is genuinely useful (`toolchain.py` already does this correctly and
   is the model).
3. A test that runs the whole read path against a vault in `tmp_path` with
   `CATALOGUE_VAULT` set — which is the only thing that will keep this true.

**Exit:** `CATALOGUE_VAULT=/elsewhere python -m librarian status` works on an
empty directory and says what is missing, on a machine with none of these
drives.

**This stage got more load-bearing.** A web app is a process that *serves* a
vault rather than a script that lives in one, so half-wired vault resolution
stops being a portability nicety and becomes a correctness bug: the server would
read an index from one place and write to another.

---

## Stage 3a — The model interaction layer (MCP)

**Correction to the assessment: this is largely built.** `librarian.mcp_server`
is 220 lines, registers ten tools, marks `record_application` as the only write,
exposes `read_only_tools()`, and `python -m librarian serve --list` returns
cleanly. The `mcp` package is installed. What is missing is not the server; it
is everything that makes a server usable by someone who did not write it.

Four things, three of them lifted from `F:\Mark-XLVIII-main` rather than invented:

1. **FastMCP instead of the hand-rolled `build_server()`.**
   `Agent_backend/backend/lmstudio_fastmcp_shim.py` uses
   `from mcp.server.fastmcp import FastMCP` with `@mcp.tool()` decorators, which
   is materially less code than the SDK path this currently gates on.
2. **Progressive disclosure.** The capability-registry handbook there stages
   context as *L0 card → L1 manifest → playbook → function schema*, loading the
   exact parameters only immediately before dispatch. Ten tools with nine filter
   axes is a great deal of schema to put in every prompt; a cheap L0 list an
   agent narrows before asking for a schema is the same *data → information →
   knowledge* progression [[Data Information Knowledge]] already describes, one
   layer up.
3. **stdio and loopback HTTP, localhost-only, with a local token and an origin
   allowlist.** stdio for an agent launched as a subprocess, HTTP for the web
   app in Stage 3c. The security posture is theirs and is right.
4. **Effect classification at dispatch.** Their `tool_dispatcher` classifies
   every operation as read-only, local write, external side effect, destructive,
   or workflow-authorised, and the handbook states the rule this system needs
   verbatim: *registry metadata is not permission*. Discovering that a tool
   exists does not authorise calling it. `CLOSED_ACTION_REGISTRY` already says
   so; this makes it enforceable at the MCP boundary rather than only inside.

One convergent finding worth recording: that handbook documents fixing
`_search_cards()` because it scored capabilities by **substring** rather than
word-tokenised matching, so `in` matched inside `installing`. That is the same
defect class as `interface_protocol: "REST"` matching *the rest of the system*
here. Two independent systems, same bug, same fix — good evidence it deserves a
standing check rather than a one-off correction.

**Exit:** an agent that has never seen this project can start the server, list
capabilities, narrow, fetch one schema, call it, and be refused *by name* when
it asks for something unregistered. Packaged as a Claude skill so installing it
is one step.

---

## Stage 3b — The user interaction layer (web app)

**A faceted item-search page**, in the shape of a product catalogue rather than
a web search engine. The distinction is not cosmetic: a search engine offers a
box and a ranked list, and a catalogue offers a box, a ranked list, **and a set
of drop-downs derived from what the current results actually contain**.

That is the right shape here because the objects being searched are already
strongly typed. Every resource carries nine closed taxonomy axes plus
`permitted_uses`, and a person narrowing a set of candidates wants to see what
the axes *look like across the set they have* — not a fixed sidebar of every
value the vocabulary permits.

### Facets are computed from the result set, never from the vocabulary

A drop-down shows only the values present in the current results, each with its
count, and disappears entirely when an axis does not vary. Searching *parser*
should offer `ecosystem: Mixed (4), Web_Frontend (3), Python (2)` — not the full
fourteen-value enumeration with eleven zeroes.

Two reasons this matters more here than in a shop:

- **It makes the corpus legible.** A facet with one value is telling you the
  catalogue holds only one kind of answer to this question, which is a coverage
  statement the ranked list cannot make.
- **It makes elimination previewable.** `consult.eligible` *removes* candidates
  rather than demoting them, so a facet count is exactly the size of the set
  that survives choosing it. The user sees the cost of a constraint before
  paying it, which is the honest version of a filter.

### Design constraints that fall out of decisions already made

- **Filters eliminate, and the UI must show that.** Selecting *Permissive*
  removes results; it does not reorder them. `Response.filtered_out` and
  `Constraints.describe()` already carry the count and the reason, and showing
  them is what stops a user thinking the catalogue is small when it is filtered.
- **Every result already carries its own `why`**, assembled from what matched
  and never generated. That belongs under each result, not behind a disclosure
  triangle.
- **Metadata as tags beside each item.** The nine axes and `permitted_uses`,
  rendered as tags next to the title, link and description — each one clickable
  as a filter, which is what makes the tag row a navigation surface rather than
  decoration.
- **`coverage` has a verdict and the UI must not bury it.** *Uncovered* reads as
  a statement, not as an empty page. A tool that says *nothing here covers this*
  is the point of having built one.
- **Two grains after A2.** A repository and a component within one are different
  kinds of result and must look different. Deciding how before the first pixel
  is cheaper than retrofitting it.
- **No retrieval logic in the front end.** Facet counts come from the same
  `Response`; the page aggregates what it was given and computes nothing about
  relevance.

### What this adds to the engine

One function: given a `Response`, return per-axis value counts over its results.
It belongs beside `consult`, not in the page, so the MCP surface and the
assistant get the same facets without reimplementing them.

**Exit:** a person can search, narrow by drop-downs that reflect the actual
result set, see why each result matched and what was eliminated, click a tag to
filter, and be told plainly when the catalogue holds no answer.

---

## Stage 3c — The assistant layer

Gated by 3a and 3b, and designed now rather than built. On a search the view
splits: conversation on the left, the standard results page on the right. The
assistant is an MCP client against the Stage 3a server, so it has exactly the
capabilities an agent has and no privileged path — the same rule that keeps
`consult` the single engine.

The reason to design it now and wire it later is that two decisions in 3a and 3b
are hard to reverse afterwards: whether the MCP surface can be driven over
loopback HTTP by a browser-hosted client, and whether a result carries enough
structure (`why`, `matched`, `permitted_uses`, and a coverage verdict) for a
conversation to **cite** it rather than paraphrase it. Both are cheap now and
expensive later.

**Exit for this stage now:** the 3a schema and the 3b result shape are recorded
as adequate for an assistant, with any gap named.

---

## Stage 3d — Local models for the information layer

The pipeline [[Data Information Knowledge]] describes is *data → information →
knowledge*, and the first arrow is already mechanical: `scout.survey` produces
the data layer with no model at all. The second arrow — a surveyed tree becoming
a `Bottom Line`, a `What Is Inside`, a taxonomy classification — is what
currently costs a Claude session per cohort, and is the part worth automating
locally. **The third arrow stays human.** Knowledge is what a source can be used
for, and new knowledge needs a new perspective on data or a new interpretation
of information; a model paraphrasing a tree produces neither.

LM Studio already serves a usefully varied set, and the task should pick the
model rather than the reverse:

| Task | Shape needed | Available now |
| --- | --- | --- |
| Draft `What Is Inside` from a surveyed tree | Mid-size instruct, long context | `qwen/qwen3.5-9b`, `qwen/qwen3-8b` |
| Classify against the closed axes | Small, constrained output | `qwen/qwen3-4b-2507` |
| Embeddings | Purpose-built embedder | `text-embedding-nomic-embed-text-v1.5` (`@q8_0`, `@q4_k_m`) |
| Read a scanned or image-only source | OCR / vision-language | `unlimited-ocr`, `qwen/qwen3-vl-4b` |
| Digest a large repository's own writing | Long-context research | `qwen2.5-14b-deepresearch-i1`, `marco-deepresearch-8b` |

Two constraints to hold. **Cross-vendor runtime** narrows the field to models
that will run across both GPUs, and that is a selection criterion *before*
capability rather than after. And **a drafted note is a draft**: `integrity`,
`provenance` and `distinct_resource_prose` already exist to catch generic prose
and unsupported numbers, so the acceptance test is a local draft that passes all
three — far stronger than *reads well*.

**Exit:** one cohort's information layer drafted locally, passing the same
checks a hand-written note passes, with the failure rate recorded. A high rate
is a result too: it says which arrow still needs a better model.

---

## Stage 4 — Cover the comparables, and prove the write path

Two rows in the composite-analogue table have no entry, and they are the same
two capability gaps the assessment named. That is not coincidence — **the
catalogue's blind spots and its coverage gaps are one list** — and it argues for
scouting against a map of grouped functions rather than seed queries.

| Missing | Grouped function it represents |
| --- | --- |
| **Backstage** | Catalogue entities, own them, document them, score them — the closest whole-system analogue to this project |
| **Renovate / Dependabot / OSV** | Inventory → watch upstream → alert on change; the freshness pattern, done properly |
| Vespa | Query understanding → retrieve → rank → rerank, as one system |
| DataHub / Amundsen | The second and third opinions on metadata cataloguing |

This stage does double duty: it is the first cohort run through
`scout.survey` end to end, which is the only way to prove the write path works
at scale. It has run once, on a third of the corpus, and both 2026-09 cohorts
were charted by scripts that no longer exist.

**Exit:** a cohort surveyed, charted and indexed without a scratchpad; the
analogue table has no empty rows; `librarian components build` picks the new
surveys up with no code change.

---

## Stage 5 — Consolidate, then package

Consolidation **before** packaging, because packaging freezes whatever shape
exists. 46 modules and 12,202 lines is not large, but it grew by accretion and
some of it is answering questions nobody asked.

**Consolidate:**

- The CLI has 21 subcommands added one at a time. They fall into four groups —
  *ask* (`query`, `note`, `coverage`), *maintain* (`index`, `views`,
  `components`, `freshness`, `integrity`), *measure* (`eval`, `scenario`,
  `relevance`, `provenance`, `duplicates`), *act* (`workbench`, `used`,
  `serve`). Group them, and say so in `--help`, before anyone learns 21 names.
- Whatever Stage 1 deleted comes out of the Service Map, the README and the
  Design Specification at the same time, not later.
- One tokeniser, one stopword list, one GitHub client, one clone. Three
  duplicates of these were found and removed on 2026-09-04 by accident; the
  fourth should be found on purpose.

**Package:**

- `pyproject.toml`, a `librarian` console entry point, pinned dependencies, and
  the optional extras made explicit (`[embeddings]`, `[mcp]`, `[scout]`) so the
  degradation paths that already exist are visible at install time.
- `librarian init` — an empty directory to a working catalogue: folder
  structure, `Note Content Model`, an empty `Scouting Domains`, a Master Index.
  Without this the tool is only usable by someone who already has this vault.
- The MCP server as the agent surface, since that is how an agent is meant to
  arrive.

**Exit:** `pip install`, `librarian init`, `librarian query` on a clean machine
with an empty vault.

---

## Stage 6 — Optimise the costs that actually hurt

Neither of these is runtime.

**Effort per source.** Charting 49 sources took a day of authoring. The
surveyor now supplies the data layer mechanically, so the remaining cost is the
prose — `Bottom Line`, `What Is Inside`, `Transferable Capability`. The
measurable target: a note that passes `integrity`, `provenance` and
`distinct_resource_prose` in materially less time, without the generic prose
those checks exist to prevent. `provenance` at 99% supported is the guard that
makes this safe to attempt.

**Effort per correct answer.** The user-facing cost is reading notes that
turned out to be wrong. `coverage` reduces it when it can say *uncovered*;
Stage 2 decides whether it can ever say *thin means no*. `usesignal` starts
paying here once there are events — `readiness()` says 200 across 40 distinct
queries, and until then reading it would learn one person's week.

**Exit:** both measured, both improved, or a recorded reason why not.

---

## What This Plan Deliberately Excludes

- **Runtime performance.** No measured problem exists. Revisit if the corpus
  passes roughly 1,000 notes, where the brute-force cosine in `embed` and the
  O(n²) pair scan in `duplicates` become the first things to look at — both are
  known and neither matters yet.
- **A second human surface beyond the two named.** Obsidian stays the reading
  surface and Stage 3b is the searching one; they do different jobs and neither
  replaces the other. A third would need a reason.
- **More scenarios before Stage 2 resolves.** Thirty scenarios currently probe
  the 81-resource corpus and none asks about lineage, parsing or retrieval.
  Adding more now would measure the ranker against a corpus it is about to
  stop being the constraint on.

## Related
- [[System Assessment 2026-09-04]] — the measured weak spots this plan targets
- [[Data Information Knowledge]] — the layering the stages respect
- [[Service Map]] — the inventory Stage 1 and Stage 5 prune
- [[Design Specification]] — the policies, including `LOCATE_DO_NOT_ADJUDICATE`
- [[Master Index]]
