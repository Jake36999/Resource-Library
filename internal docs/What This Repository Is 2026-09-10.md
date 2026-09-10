---
type: "assessment"
status: "active"
created: "2026-09-10"
purpose: "a definition of the system, a descriptive breakdown of the repository, and what it is and is not like"
---

# What This Repository Is

## The One-Sentence Definition

> **A catalogue of open-source software that someone has actually read, with the
> evidence attached, built so that a person or an agent can find proven prior
> work before writing any — and built so that neither can put a claim into it
> that nothing fetched.**

Two halves, deliberately separable:

- **the vault** — 347 Markdown notes in Obsidian. The truth. Hand-editable,
  human-readable, and authoritative over everything derived from it.
- **`librarian`** — 38 Python modules, 14,440 lines, standard library except
  PyYAML and numpy. Indexes the vault and answers questions against it from a
  terminal, a browser, or a model.

Nothing in the tool depends on this particular vault. `CATALOGUE_VAULT` points
it anywhere, which is what makes the system separable from the data.

---

## What Problem It Actually Solves

Not *"find a library"* — GitHub does that. The problem is narrower and harder:

> *Is this something I can use as donor code, as a reference, or as a tool —
> given what I can actually run, and given what I already know will not work?*

A search engine cannot answer that, because the disqualifying fact is usually
about **the asker**, not the source. RuView is charted accurately, is well
regarded, and was still the wrong answer for `network_management` — its sense
model assumes ESP32 input shape and the hardware is an Intel 5300. No taxonomy
anticipates that. It only enters the system if the request carries it.

That single failure is the reason `open_brief` refuses a request without
disqualifiers, and it is the clearest statement of what this system is for.

---

## The Repository, Folder By Folder

| Path | Holds | Count |
| --- | --- | --- |
| `01-Resources/` | one note per source — the substance | 128 |
| `02-Glossary/` | terms, defined once, linked | 113 |
| `03-Patterns/` | recurring solution shapes, independent of any source | 47 |
| `00-Indexes/` | Master Index, topic indexes, the taxonomy register | 17 |
| `internal docs/` | design specification, assessments, service map | 26 |
| `08-Workflows/` | how the intake and consult modes actually run | 7 |
| `09-Applications/` | what was used, when, and what it was worth | 6 |
| `04-Reviews/`, `06-Papers/` | long reads; academic sources with their PDFs | 5 |
| `05-Canvases/` | the workflow map, the library map | 2 |
| `.Data/` | surveys (evidence), briefs, queue, seeds, derived databases | — |
| `.utility/librarian/` | the tool | 38 modules |
| `.utility/scout/` | the intake pipeline: discover, rank, freeze, dive, publish | 13 modules |

Derived stores are never committed. A fresh clone is 21 MB and rebuilds its
index in under a second.

---

## The Three Layers, And Why They Are Kept Apart

This is the load-bearing idea. Each layer may assert different things, and the
system refuses to let a lower one claim what only a higher one can.

| Layer | Where | May assert | Who may write it |
| --- | --- | --- | --- |
| **Data** | `.Data/surveys/` | *this path exists; this licence was declared* | any agent, including a 4B local model |
| **Information** | `01-Resources/` | *what it does and what it is for, with evidence cited* | a person, or an agent that used it |
| **Knowledge** | `03-Patterns/`, `09-Applications/` | *what worked, what it replaced, what the catalogue should learn* | a person |

The split is not bureaucracy. It is the line along which work can be automated:
filling ten closed enumerations from a file listing is constrained choice, and a
small model does it well enough to run overnight for free. Writing the sentence
a reader acts on is interpretation, and the same model writes plausible mush
that passes every structural check there is.

`INTERPRETATION_IS_NOT_MACHINE_WORK` enforces exactly that boundary.

---

## The Surfaces

Three front ends, **one engine**. The CLI, the MCP server and the web page all
call the same `consult.find_donor`, so they cannot disagree about what the
catalogue contains.

| Surface | Command | For |
| --- | --- | --- |
| Terminal | `librarian query donor "..."` | asking directly |
| Browser | `librarian web` | narrowing by axis, catalogue-style |
| Model | `librarian serve --tier ...` | an agent, over MCP |

26 subcommands; 20 MCP tools across three permission tiers.

### The tiers

```
consult      12 tools   reads + one append to 09-Applications/
contribute   19 tools   + briefs, queue, staged proposals — cannot alter a note
curate       20 tools   + promotion into 01-Resources/
```

The old guarantee was *exactly one tool writes*. That stopped being true when
outside agents were allowed to contribute, and its honest successor is not a
longer write list but a statement of **what each write can reach**: seven write,
two create a note, one creates a note in `01-Resources/` — and it is not in the
tier a research agent runs at.

---

## The Retrieval

Lexical BM25 over FTS5, fused with cosine over local embeddings, with a
coverage stage and hard elimination on ten closed taxonomy axes. Constraints
**eliminate** rather than re-rank, and the response says how many they removed.

Two instruments, both run against a live index:

- **`librarian eval`** — 20 queries, MRR 0.95, hit@5 1.00
- **`librarian scenario`** — 30 problems phrased in the asker's own words rather
  than the catalogue's: useful@5 0.83, strong@5 0.80, MRR 0.66

Neither number is comparable across sessions, and the tool says so: both
instruments read the vault, the vault contains this system's own design
documents, and editing one moves the score with no ranking change at all.

`librarian relevance` compares 23 ranking configurations side by side on one
index, including the ones that were **measured and rejected** — kept selectable
so the rejection stays reproducible.

---

## The Rules It Holds Itself To

22 named policy codes, enforced in code. Every refusal names one. The ones that
shape everything else:

| Code | What it forbids |
| --- | --- |
| `EVIDENCE_REQUIRED` | a factual field with no fetched source. `Unknown` is valid; a plausible guess is not |
| `MARKDOWN_IS_TRUTH` | a derived store outranking a note |
| `NO_SCHEMA_DRIFT` | any process adding a field or an axis value |
| `LOCATE_DO_NOT_ADJUDICATE` | the system deciding what you may do with a source |
| `POSTURE_DECIDES_CONSEQUENCE` | a licence class carrying a consequence the distribution posture did not set |
| `INTERPRETATION_IS_NOT_MACHINE_WORK` | a machine writing the sentence a reader acts on |
| `FAILURE_MUST_BE_LOUD` | an operation that can fail silently |
| `DOCUMENT_BEFORE_DESTROY` | discarding a sandbox, or a research session, before its record exists |
| `RUN_BEFORE_CLAIM` | listing a service that has never produced a row |
| `THRESHOLD_CARRIES_ITS_DISTRIBUTION` | a corpus-relative constant with no re-derivation function |

`LOCATE_DO_NOT_ADJUDICATE` is the one most systems get wrong and is worth
stating plainly: **the catalogue identifies and describes; the user decides.**
A licence is recorded as read, always. What it *costs* is read from the
distribution posture — under `private` every class permits donor, reference and
tool use, because nothing built here is distributed. One config key, two
behaviours, identical recorded facts.

---

## The Current State

| | |
| --- | --- |
| notes indexed | 347 (2,223 chunks, 3,259 links) |
| catalogued sources | 128, fully classified |
| tests | 435 passing, 1 skipped |
| integrity | 0 errors, 13 warnings across 23 checks |
| staged, awaiting a human sentence | 42 |
| queued for enrichment | 45 |
| application records | 6 — **the weakest layer, and the one that matters most** |

Six application records against 128 sources is the honest weak spot. That layer
cannot be scraped, cannot be generated, and does not fill by charting more
repositories. It fills only when someone doing real work says what a source was
worth — which is why `log_use` is designed to cost one call and claim nothing.

---

## What It Is Like, And Where It Differs

### Backstage + Tech Radar — the institutional comparable

[Backstage](https://backstage.io) catalogues the software an organisation
**owns and runs**: services, ownership, on-call, TechDocs alongside the code.
Its Tech Radar plugin tracks adoption stance — *Adopt, Trial, Assess, Hold*.

Two differences, and the second is a disagreement rather than a gap:

- Backstage catalogues what you **operate**; this catalogues what you might
  **borrow from**. Different question, different fields.
- **A Tech Radar adjudicates.** *Hold* is an instruction. This system refuses to
  issue one — `LOCATE_DO_NOT_ADJUDICATE`. Age, popularity and licence are facts
  to report, never grounds to withhold. For a team of one that is clearly right;
  for an organisation of a thousand a radar is clearly right. The distinction is
  worth keeping conscious.

### OWASP Dependency-Track — adjacent, opposite direction

Catalogues the dependencies you **ship**, for vulnerability and licence risk,
from an SBOM. Inventory of what is already in the build. This is an inventory of
what has been *read and might be borrowed*, which is upstream of that decision.

### Code-intelligence MCP servers — the same protocol, the other axis

A 2026 cluster of tools — call-graph and AST indexers, Tree-sitter knowledge
graphs, local semantic-graph search — index **one codebase deeply** for an agent
working *inside* it. This indexes **many codebases shallowly** for an agent
deciding *which* codebase to borrow from. They compose rather than compete:
choose the source here, then point one of those at it.

`oraios/serena` is the strongest example and the obvious upgrade path for
`librarian.components`, which today retrieves at *file* level from a listing
where serena retrieves at *symbol* level through language servers.

### gitingest — the closest thing to our ingestion, and the most instructive

See the next section. It is worth its own.

---

## gitingest, Read At Source

`coderamp-labs/gitingest` turns any repository into "a prompt-friendly text
ingest for LLMs". It is a free hosted service, which raised the right question:
*how is that cost-effective?*

The answer, read from `src/gitingest/output_formatter.py` — **6.9 KB, five
functions, and not one model call**:

```python
summary, tree, content = ingest("path/to/directory")
```

- `summary` — repository name, branch, file count, estimated token count.
  Arithmetic.
- `tree` — an ASCII directory tree. String building.
- `content` — every file's raw text, concatenated with separators.

Its limits are `MAX_FILES = 10_000` and `MAX_TOTAL_SIZE_BYTES = 500 MB`.

### So, to answer the question directly

**Do they give a per-function breakdown?** No.
**Do they describe a script's role?** No.
**How do they package and sequence it?** Header, then tree, then raw
concatenated contents. That is the whole format.

**It performs no abstraction whatsoever**, and *that is precisely why it is
free*. There is no inference to pay for — it is `git clone`, walk, filter,
concatenate. The cost is bandwidth and CPU. The reading is deferred to the
consumer's model, at the consumer's expense.

### What that means for us

It is the **opposite** of what this system does, and the contrast is clarifying:

| | gitingest | librarian |
| --- | --- | --- |
| unit | one repository, entire | one source, ten axes + prose |
| inference cost | zero | ~110 s of local model per source |
| output | 50k – 2M tokens | ~400 tokens |
| lifetime | discarded after one prompt | durable, indexed, re-queried |
| who reads it | the consumer's frontier model | a small local model, then a person |
| answers | *what is in this repository* | *which repository, and can I use it* |

They are **transport** and **retention**. Neither substitutes for the other.

### The idea worth taking

Not "rebuild a repository" — the user is right that we do not need that. The
idea worth taking is a **capability digest**: the tree and raw contents of *just
the files that implement one named capability*, packaged gitingest-style.

That is a third thing, and neither tool has it:

- gitingest can package cheaply but **does not know which files matter** — so it
  ships all of them.
- this system **already knows which files matter** — the surveys carry complete
  path listings, `components` classifies them by material kind, and
  `agent_surface` already proves a path ladder can be read reliably (0.958) —
  but it ships a 400-token note, which is too small to rebuild anything from.

**We already own the expensive half. gitingest demonstrates the cheap half.**
A digest scoped to a capability would cost no inference, exactly as gitingest
costs none, and would be targeted precisely because the analysis was already
done. As the user puts it: given to a model, that *is* a schema.

The open question is the right grain — whether a capability is a directory, a
signal class, or a hand-named set of paths — and that is a measurement, not a
guess. It should be settled the way `agent_surface` and `interface_protocol`
were: against the 128 sources already charted, with a number, and abandoned if
the number is bad.

---

## Honest Weaknesses

1. **Six application records.** The knowledge layer is nearly empty. Everything
   else is scaffolding for it.
2. **42 proposals stuck in the airlock**, blocked on `deployment_target` and
   `data_locality` — two axes nothing can read and which were left empty rather
   than guessed. Promotion needs a person.
3. **`interface_protocol` has no derivation**, measured at 0.409 and rejected.
4. **The taxonomy strains on new subject matter.** Six languages were added on
   2026-09-09; Ruby, PHP, Kotlin, Swift, Haskell and Zig still have no
   `ecosystem` value.
5. **The corpus is small enough that ranking work has nothing to bite on** —
   eight query representations measured +0% lift over doing nothing. The gap is
   corpus-shaped.

---

## Related
- [[Design Specification]] — the rules, in full
- [[Service Map]] — every stage, defect by defect, with what was measured
- [[Data Information Knowledge]] — the layering, argued
- [[Note Content Model]] — the schema, authoritative
- [[Agent Instructions - Using The Library]] — the drop-in block for a project
- [[Master Index]]
