# The Librarian

The read surface, derived index and workbench for the Resource Library.
Design and rationale: `internal docs/Design Specification.md`; the layering
everything is organised by: `internal docs/Data Information Knowledge.md`;
order of work: `internal docs/Implementation Brief.md`.

The catalogue **identifies and locates** solutions. It does not extract them.
Every answer ends at *here is where to look and why*; opening a source is a
person's decision, and it happens in a workbench.

## The shape of it

```
   Mode C  consult   ──►  six typed queries      fast · stateless · read-only
                              │ reads
                          THE VAULT              markdown = truth
                          + derived index        sqlite = disposable
                              ▲ writes (gated)
   Mode A  sweep     ──►  intake orchestrator    slow · gated · resumable
   Mode B  directed  ──►  closed action registry
                              │ calls, never reimplements
                          THE TOOLSET            investigation + slicer
                              │ provisions
   Mode D  engage    ──►  the workbench          ephemeral · isolated
                                                 execution lives here only
```

Three invariants. **Markdown is truth** - delete `catalogue_index.sqlite` and
rebuild it; nothing is lost. **Reads and writes are separate subsystems** with
separate budgets. **The intake calls the toolchain** rather than containing a
second copy of it.

## Run it

```powershell
cd D:\Resource-Library\.utility

python -m librarian status          # what the index holds, what is reachable
python -m librarian components vocab  # the data layer: what can be filtered on
python -m librarian freshness       # re-check recorded facts upstream; reports, never edits
python -m librarian coverage "..."  # does the catalogue actually cover this?
python -m librarian duplicates      # candidate near-duplicate sources
python -m librarian provenance      # the catalogue's own claims, against the surveys
python -m librarian used --status   # how much use signal has accumulated
python -m librarian index           # vault -> SQLite + FTS5   (~0.4 s)
python -m librarian views           # regenerate the derived views from the notes
python -m librarian views --check   # report their drift; write nothing
python -m librarian integrity --check frontmatter_complete   # one named check
python -m librarian integrity       # the vault assertions; non-zero on error
python -m librarian eval            # 20 questions with known answers
python -m librarian scenario        # the domain search test, described in a user's words
python -m librarian relevance       # ranking configurations side by side, one index
python -m librarian embed           # optional vectors, needs LM Studio (~6 min)
python -m librarian graph           # communities + filtered centrality
python -m librarian access          # extract and list access points
```

Ask it something:

```powershell
python -m librarian query donor "run dependent jobs nightly and recover" --license-class Permissive
python -m librarian query technique "how is backpressure handled"
python -m librarian query precedent "apache - airflow"
python -m librarian note "apache - airflow"
```

`index` first. Everything else reads what it built.

## What each module is for

| Module | Does | Notes |
| --- | --- | --- |
| `notes.py` | Parses the vault | The only place that decides what a note *is* |
| `index.py` | Vault → SQLite + FTS5 | Disposable; rebuild is idempotent |
| `integrity.py` | Seventeen dbt-style assertions | Errors fail a run; warnings do not |
| `content_model.py` | Reads the note schema | The schema is a note, not a JSON file |
| `views.py` | Notes -> the derived views | The only thing that may write them |
| `consult.py` | The six queries + the one write | Filters eliminate; every result says why |
| `embed.py` | Vectors + brute-force cosine | Optional. No ANN index, deliberately |
| `graph.py` | Vault communities, filtered centrality | graphify, permitted use 1 |
| `toolchain.py` | Adapter to the ToolSet | Works with it absent |
| `clone.py` | Shallow clone, and disposal | Commands built in code, never from text |
| `intake.py` | Clone → investigate → summarise → discard | Slice used, never kept |
| `access_points.py` | Addresses: extract, store, verify | The one persisted extract |
| `workbench.py` | Mode D: open, document, close | graphify, permitted use 2 |
| `mcp_server.py` | Agent surface | One write, no path to Mode D |
| `evalset.py` | Retrieval evaluation | Build it before tuning, not after |
| `scenariotest.py` | The domain search test | Real components, described in their own words |
| `relevance.py` | Ranking configurations, compared | One index, one pass; a losing option is kept, not deleted |
| `components.py` | The data layer | What sources are *made of*, as rows; derived from `.Data/surveys/` and disposable |
| `freshness.py` | Recorded claims vs upstream | Writes readings, never edits a note |
| `coverage.py` | Is this answer worth trusting? | Catches out-of-collection questions; says `thin` (no opinion) otherwise |
| `duplicates.py` | Near-duplicate sources | Reports candidates; merges nothing |
| `provenance.py` | Claims vs the surveys behind them | 99% of 211 structural numbers trace to a row |
| `usesignal.py` | What an answer was worth | Accumulating; reads into ranking only once there is data |
| `queryunderstanding.py` | Ask vs context | Off - both forms measured worse than doing nothing |
| `scout/survey.py` | Repository -> components | The method that built the catalogue, promoted from a scratchpad |

## The rules that are enforced, not just documented

- **Constraints eliminate.** `find_donor` with `license_class=Permissive`
  returns nothing else - including nothing whose licence is unknown. A GPU-only
  tool is not a lower-ranked answer for a laptop; it is not an answer.
- **Every result explains itself.** `why` is assembled from which filters
  passed and which terms matched. It is never written by a model, and it never
  claims a match that did not happen.
- **Mode C writes exactly one thing.** `record_application`, gated by
  `policy.check_consult_write`. Everything else refuses with a named code.
- **The action registry is a frozenset.** An unregistered name is an error.
  An agent that needs something the registry lacks reports being blocked; that
  refusal is the intended behaviour, not a failure.
- **A sweep cannot open a workbench.** Enforced twice: the sweep path does not
  import `workbench`, and `open()` refuses while `LIBRARIAN_MODE` says sweep.
- **`close` refuses without a record.** `DOCUMENT_BEFORE_DESTROY`. The record
  is the price of closing the workbench, not a chore to remember afterwards.
- **Slices are ephemeral.** The intake reads one as evidence and deletes it.
  There is no permanent index of extracted symbols, because that would be a
  snippet library ageing independently of its origins.
- **Communities live in the index, never in frontmatter.** A graph may observe;
  it may not author the taxonomy. Disagreements produce a report for a person.
- **Derived views are generated, never typed.** `views.py` owns the taxonomy
  matrix, topic membership and the route-map counts, and regenerating twice
  changes nothing. It reconciles *membership* but never reorders a list a
  person curated. `integrity` warns when a view has drifted, because
  `scout.rank.gap_fit` reads `resource_count` and carries the largest ranking
  weight - a stale count mis-ranks every candidate for that topic, quietly.
- **Nothing is scored to zero for a property the user did not ask about.**
  `LOCATE_DO_NOT_ADJUDICATE`. The catalogue identifies and describes; the
  person decides what to do with a source. Three signals were each awarding a
  hard zero under a double-digit weight - an unlicensed repository, an archived
  one, an unstarred one - and a zero is not a low rank, it is invisibility.
  Each assumed the user meant to *depend* on the source. `usage.catalogue_role`
  and `usage.distribution_posture` scale them instead; a stated constraint
  still eliminates, because that one is the user's. See the audit in
  `00-Indexes/Design Specification.md` §2.1a, and add any new signal to it.
- **A licence is read, not assumed.** When GitHub returns NOASSERTION or
  nothing, the intake fetches the LICENSE and classifies it. An explicit
  `SPDX-License-Identifier` expression wins outright; `OR` there is a choice,
  so the least restrictive licence governs, while everything else is a
  conjunction and the most restrictive one does. Prose is read for *which*
  licences are present, never for how they combine - inferring a choice from
  wording matched GPL boilerplate and reported two copyleft projects as
  permissive. Composites are flagged for a person rather than resolved.
  `license_class` is the field `find_donor` eliminates on when you ask for one,
  so a wrong value silently removes a resource from a constrained answer - or,
  worse, silently adds one that does not belong.
- **A licence costs what the posture says it costs.** `usage.distribution_posture`
  in `library_config.json` is `private`: this catalogue serves R&D on tooling
  that is not published, so reading a source, running it and copying from it
  trigger no obligation, whatever its licence. Every result therefore carries
  `permitted_uses` - `donor`, `reference`, `tool` - which is the question
  anybody actually asks a licence, and under this posture the answer is all
  three for every class. `scout.rank.reusability` follows the same switch: its
  strict scale scored an unlicensed source a hard `0.0`, which under a 15-point
  weight removed it from contention, and twelve of the 2026-09-04 cohort are
  unlicensed. Set the posture to `distributed` before publishing any of this
  and both revert to the strict reading in one edit.

## Degradation

Nothing here becomes a dependency. Each of these is a `partial=True` and a
reason, never an exception:

| Absent | Effect |
| --- | --- |
| LM Studio | Filters + FTS5 only; `Response.notes` says vectors were skipped |
| numpy | Same |
| graphify | No communities; centrality still computed |
| `Note Content Model` | No shape checks, reported as a warning; everything else runs |
| `.Data/surveys` | No component store; `components` reports absence rather than failing |
| The ToolSet | Deep dive falls back to documentation-only evidence |
| Docker | `workbench open` refuses unless `allow_no_container=True` |
| git | Intake reports `clone_failed` for that source and continues |

## Tests

```powershell
python -m pytest .utility\librarian\tests -q      # 125
python -m pytest .utility\scout\tests -q          # 62
```

No test needs Docker, LM Studio, network access or the ToolSet. Every external
is injected, following the `FakeLM` pattern the scout tests already use.

## Retrieval, as it stands

Twenty questions with known answers, `python -m librarian eval`:

```
hit@5     1.00   (20/20)
recall@5  1.00
MRR       0.94
```

Reached with structured filters and FTS5 alone. Adding embeddings changed none
of those numbers on this set - worth knowing before anyone spends effort tuning
vectors, and the reason the eval set is built alongside step 3 rather than
after step 4.

These numbers moved a long way and every move was a defect, not a tuning knob.
Chunking link and metadata blocks into the text index; `by_name` returning hits
in SQLite's row order, which becomes the RRF rank; `rrf` summing one note's
many matching sections, so verbosity ranked; a caveat read as a claim;
`interface_protocol: "REST"` matching the word *rest*; and finally no stemming
at all, so `institution` reached nothing while `institutional` reached four
chunks.

**The last one was found by `librarian scenario`, not by this eval, and it was
the largest.** These twenty questions are phrased the way the notes are
written, so they cannot see a morphology failure. The domain search test
describes a real component in its own team's words and asks whether anything
useful comes back; enabling the `porter` tokenizer moved it from 0.64 to 0.77
and moved this eval from 0.92 to 0.94 as a side effect. Keep both: this one
guards the index, that one guards the point.

See `00-Indexes/Service Map.md` for the scenario results and what still fails.

## Three layers, and which one you are in

`internal docs/Data Information Knowledge.md` is the short version and worth
reading before changing anything here.

- **Data** — `.Data/surveys/*.json` and `source_components.sqlite`. Components,
  registered. Asserts only that something was present at a commit on a date.
- **Information** — the resource notes. What those components mean together,
  with `**Not read:**` marking every inference.
- **Knowledge** — `Transferable Capability`, and the application records, which
  hold the only claims here that did not come from a source's own description.

A new store belongs in `.Data/` and must be rebuildable from something that is
not itself derived. A new field on a note is information or knowledge; if it is
a raw component fact it belongs in the component store, where it can be
filtered across the whole collection instead of read one note at a time.

## Things that were built, measured, and turned off

Kept, not deleted, because a rejected option nobody can re-run is folklore
rather than a finding. Each has a configuration in `rank_configs.json` or a
`calibrate()` and can be re-measured in one command.

- **Query segmentation** (`queryunderstanding`). Separating the ask from the
  context it arrives in. The segmenter works — on the scenario it was built for
  it correctly excludes `storage`, `engine`, `query` and `layer` — and removing
  those terms still makes retrieval worse, in both the deletion form (5 misses
  against 4) and the weighted form (7). Together with `coverage.calibrate()`,
  which found no overlap-derived signal that separates answerable from
  unanswerable, this bounds the problem: **it cannot be solved lexically.** The
  evidenced next step is a model over the query, and the harness to judge one
  already exists.
- **IDF-weighted coverage ordering** (`coverage_order="idf"`). Loses at every
  ceiling. Document frequency cannot separate *rare and meaningful* from *rare
  and incidental*.
- **Reading the use signal into ranking** (`usesignal.weights`). Correct and
  unused: with zero events it would encode nothing. `usesignal.readiness()`
  says when that changes.
