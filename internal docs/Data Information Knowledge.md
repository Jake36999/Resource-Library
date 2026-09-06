---
type: "design_spec"
status: "active"
created: "2026-09-04"
authority: "The layering this catalogue is organised by. Names what each layer may assert and what it may not."
---

# Data Information Knowledge

## Why This Note Exists

The catalogue had grown three storage layers, two retrieval instruments, a
scouting pipeline and a ranking model without ever writing down **what kind of
claim each part is entitled to make**. That gap is what let a ranking signal
score an unlicensed repository at zero — a judgement about *use* dressed up as
a fact about *worth* — and it is what let a complete file-tree survey of 113
repositories be collected, summarised into prose, and then thrown away.

This note is the layering. It is short on purpose.

## The Three Layers

**Data** is a component, registered and logged, before anything is concluded
from it. `nene/sql-parser-cst` has 141 files under `test/`. `SigmaHQ/sigma` has
4,521 paths matching the grammar signal. `javaparser/javaparser` has four
licence files at its root. Each is a fact with a source and a date, and none of
them means anything yet.

**Information** is what emerges from how those data points relate. That
`javaparser-symbol-solver-testing` is 1,436 files against a 578-file core is
data twice over; that *resolution, not parsing, is where the difficulty is* is
information, and it exists only because two counts were put next to each other.
Short summaries, metadata, runtime dynamics: this is the layer the resource
notes are written at.

**Knowledge** is what the thing can be used for. And the honest position when
scouting is that **the only knowledge available is that a source can be used
for what it says it is for.** A tree survey and a README support the claim that
tree-sitter parses incrementally; they do not support any claim about how it
behaves in a pipeline nobody has run.

That ceiling is not permanent, and the way through it is specific: **new
knowledge requires either a new perspective on the data or a new interpretation
of the information.** Not more reading. Reading the same tree again produces
the same knowledge. Putting the tree next to a question nobody had asked
before — *which of these ship agent-executable procedures?* — is a new
perspective on data already held, and it produced a taxonomy axis. Applying a
source in a real project and recording what happened is a new interpretation,
and it produces the only knowledge in this catalogue that did not come from its
sources' own claims.

## Where Each Layer Lives

| Layer | Artefact | Who writes it | What it may assert |
| --- | --- | --- | --- |
| Data | `.Data/surveys/*.json`, `source_components.sqlite` | A fetch, mechanically | That this component was present at this commit on this date |
| Information | `01-Resources/*.md` — `Bottom Line`, `Architecture & Mechanics`, `What Is Inside`, taxonomy | A person, from the data | What the components mean together, marked `**Not read:**` where inferred |
| Knowledge | `Transferable Capability`, `Integration & Use Cases`, `09-Applications/*.md` | A person, from information plus use | What it can be used for — and, in an application record, what it actually did |

The separation is load-bearing rather than tidy. A resource note that asserts
runtime behaviour nobody observed has smuggled knowledge into the information
layer, and the reader cannot tell. That is why every inferred claim in a note
carries `**Not read:**` naming exactly what was inferred, and why
`## Evidence` states depth of read per source.

## The Two Directions

### Populating: repository → data → information → knowledge

Decompose first. Register the components as data — cheaply, mechanically, and
in bulk, because lightweight data is the thing you can afford to collect for
everything. Relate the data to get information. Stop at what the source claims
for itself, and say so.

This is why scouting is a decomposed pipeline and not a summarisation step. A
summary written directly from a README skips the data layer entirely, and
everything downstream then rests on somebody else's marketing. It is also why
the survey files are kept: **the data layer outlives the conclusions drawn from
it**, and a new question asked in a year can be answered from stored data
rather than by re-fetching 113 repositories.

### Using: minimal data in → information → knowledge → application

An agent arriving with a problem should spend as little as possible to get
oriented:

1. **Filter on data.** `librarian components vocab`, then `components signal`.
   No prose is read. 113 sources narrow to a handful structurally.
2. **Read information.** `librarian query donor "..."` returns notes with a
   `why` assembled from what actually matched, plus `permitted_uses`. This is
   where the decision about *what to open* is made.
3. **Extract knowledge.** Open the source. The catalogue locates; it does not
   extract, and that boundary is `EXECUTION_SANDBOX_ONLY`.
4. **Apply, then record.** An application record in `09-Applications/` is the
   only artefact here that carries knowledge the sources did not supply, and
   its `What The Catalogue Should Learn` section is what turns a diary entry
   into a requirement.

Each step is more expensive than the one before it, and each is entered
deliberately. An agent that goes straight to reading notes has skipped the
cheap filter; one that goes straight to cloning has skipped the decision.

### And for a person, none of this

A human opens Obsidian, looks at the topics, and reads. **A metadata library is
worse than useless to somebody who wants to browse** — it is a layer of
indirection between them and the thing they came for. That is the reason
`.Data` is dot-prefixed and invisible, the reason internal documentation was
moved out of `00-Indexes` on 2026-09-04, and the reason the navigational
surface is fifteen topics and a taxonomy matrix rather than a query language.

The two audiences want opposite things and the structure serves both by keeping
them apart, not by compromising between them.

## What This Note Constrains

- A new store belongs in `.Data/` and must be rebuildable from something that
  is not itself derived. If it cannot be deleted safely, it is not derived, and
  it needs to be argued for.
- A new field on a resource note is information or knowledge. If it is a raw
  component fact, it belongs in the component store, where it can be filtered.
- A new ranking signal must be checked against `LOCATE_DO_NOT_ADJUDICATE`
  (`Design Specification` §2.1a) — the layer confusion that policy names is
  knowledge asserted at the data layer, which is exactly what this note forbids.
- **Data is collected in bulk and cheaply; knowledge is not.** Any proposal to
  make scouting produce more knowledge per source should first be checked
  against whether it is actually producing more *claims* per source.

## Related
- [[Design Specification]] — the policies, including `LOCATE_DO_NOT_ADJUDICATE`
- [[Source Documentation Standard]] — what a note owes a reader, at the information layer
- [[Note Content Model]] — the schema, and which sections are claims
- [[Use Contexts And Agnostic Description]] — why capability is stated without domain vocabulary
- [[Service Map]] — the services, and what each is measured by
- [[Master Index]]
