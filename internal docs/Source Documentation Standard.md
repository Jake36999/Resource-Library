---
type: "standard"
status: "active"
created: "2026-09-03"
authority: "binding on anyone or anything writing a resource note; [[Note Content Model]] enforces its floor"
applies_to: "every resource note, written by a person or an agent"
---

# Source Documentation Standard

## The Failure This Exists To Prevent

A catalogue of sources that describes each one abstractly is a **list of links**. It is not a
reference guide and it is not a research tool, because the thing a person or an agent most
often needs from a source is not what the source is *about* — it is some specific method,
schema, worked example, dataset or design decision sitting inside it that its own summary never
mentions.

That failure is silent. Nobody ever discovers the note that would have answered their question
if only it had said what was in the repository, because a search for the thing they needed
returns nothing and they conclude the catalogue does not have it. The catalogue looks fine. It
is simply not doing the job.

The gap is not a coding gap. It is a **method and scope gap in the writing**: a note written to
answer "what is this?" when it also has to answer "would this repay opening, for a need its
authors never anticipated?"

## The Obligation

> **A resource note must let a reader who has never heard of the source decide whether to open
> it, for a purpose the note's author did not have in mind.**

Everything below serves that sentence. Where a rule below and that sentence disagree, the
sentence wins and the rule is wrong.

Three consequences follow, and they are the whole standard:

1. **Describe the source, not the category.** If a note could be swapped with another and
   neither would become false, both are wrong. `distinct_resource_prose` catches the crudest
   version of this; it cannot catch a note that is merely generic.
2. **Say what is actually in there, and where.** Kind of material, not just subject. Paths, not
   just claims. An inventory is an address, not a copy — the same argument
   [[Design Specification]] §3.4 uses to permit access points as a durable extract.
3. **Record what would change a judgement.** A licence that is not what it appears, a project
   in maintenance mode behind a large star count, a demo showing synthetic data, a capability
   held back for the commercial edition. These are the facts that decide adoption and they
   never appear in a description.

## The Floor

Enforced by [[Note Content Model]]. A note that does not clear this is incomplete, not merely
thin.

| Must answer | Where it lives |
| --- | --- |
| What does it do, for someone who has never heard of it? | `Bottom Line` |
| What problem, and for whom? | `What It Solves` |
| How does it work — the moving parts, named? | `Architecture & Mechanics` |
| What kind of material is in there, and at what paths? | `What Is Inside` |
| What is it, along the nine axes? | `Taxonomy` |
| What would somebody use it for here? | `Integration & Use Cases` |
| What would change a reader's judgement? | `Reading Notes` |
| Where did every fact come from? | `Evidence` |

`What Is Inside` and `Reading Notes` are **optional in the schema and expected in practice.**
They are optional because they must never be filled from a README — a note earns them by
somebody opening the source. Their absence is a signal, not a defect: it marks a source nobody
has read. It is never an invitation to invent one.

**This was tested rather than asserted.** On 2026-09-03 all 81 sources were re-read from
blobless clones and given an inventory. Retrieval improved: `librarian eval` went from
MRR 0.93 to **0.94** while the searchable corpus grew by roughly 150 chunks, and queries that
previously returned nothing now resolve — *"windows event log samples for testing detection
rules"* returns SigmaHQ first, explaining itself from `## What Is Inside`. Specificity is not
in tension with retrieval quality; it is what retrieval quality is made of, provided the
ranking rewards matching more of a query rather than less.

## Why This Is Not A Checklist

A closed checklist would reproduce the exact failure it is meant to prevent. A writer working
through fixed questions records the answers to those questions and stops, and everything the
checklist did not anticipate goes unrecorded — which is the definition of the problem, since
the valuable content is by definition the content nobody anticipated.

So the standard is deliberately **a floor plus an obligation**, not a form. The floor is
checkable and is checked. The obligation is a judgement, and it is the writer's job.

The test to apply while writing, in place of a checklist:

> *If someone came to this catalogue looking for the most specific, unusual thing this source
> contains — would this note put it in front of them?*

If the honest answer is no, the note is not finished, whatever sections it has.

## What Counts As Worth Recording

Not a closed list. A prompt for the kind of thing that is routinely lost, drawn from what the
2026-09 cohort turned out to contain — see
[[Applicable Techniques From The 2026-09 Cohort]] for the worked examples.

- **Methods stated but not obvious from the subject.** GLiNER's span scoring caps candidate
  spans at length 12. tree-sitter's grammars split into a syntax grammar and a lexical grammar
  before parse tables are built. Neither is findable from "does NER" or "parses code".
- **Material a reader might want independently of the source's purpose.** skweak ships Norwegian
  sentiment lexicons and a tokenised Wikidata subset. graphrag ships a worked corpus *with its
  computed outputs* as parquet. Somebody needs those without needing the tool.
- **Structure that contradicts the description.** LibCST calls itself a parser; by file count
  its largest subsystem is a codemod framework. semgrep's multi-language support is 36 forked
  tree-sitter grammars, which matters to anyone considering tree-sitter.
- **Where the boundary of the free thing sits.** semgrep Community Edition analyses within one
  function or file; cross-file analysis is the commercial platform. That is the whole adoption
  decision for a security use.
- **Documents worth reading on their own.** OpenMetadata's `ARCHITECTURE.md` declares how its
  own numbers were measured. PARADIRE's Part IV is a written account of what was not achieved.
- **What is deliberately absent.** capabilibara documents a `src/` tree that does not exist in
  the repository. Recording that is worth more than any description of what it would contain.
- **Applications spotted in passing.** If reading a source suggests a use here, log it in
  `Integration & Use Cases` and, if it is a reusable structure rather than a one-off, as a
  pattern. A realised use goes to [[Application Index]]; a *potential* one belongs in the note,
  because the next reader cannot re-derive it.

## Recorded Is Not Findable

The failure this section exists for was measured, not imagined. Several sources ship an
agent-facing contribution surface. It was recorded in frontmatter, inventoried in
`What Is Inside`, and **no query for that capability could reach any of them** — because
retrieval scores what a note *claims*, and the fact had only been written where it could be
read.

So the sections a note carries are not interchangeable:

| Kind | Sections | What a match there means |
| --- | --- | --- |
| **Claim** | `Bottom Line`, `What It Solves`, `Architecture & Mechanics`, `What Is Inside`, `Transferable Capability`, `Integration & Use Cases`, `Taxonomy` | the source does this |
| **Caveat** | `Reading Notes`, `Evidence` | this is true *about* the source |

Retrieval counts the first and not the second, and it must: `shenhuan2021 - gudu-sql-omni-introduce`
once outranked `dbt-labs - dbt-core` on terms sitting inside the sentence *"It is not that."*

Two rules follow, and they are the whole of it:

1. **If a source can do a thing, a claim section says so.** Recording it in frontmatter or
   listing it in an inventory is necessary and not sufficient. `recorded_property_is_findable`
   checks the case it can check — a substantive `agent_surface` with no prose behind it — but
   most of this is a judgement, and the judgement is: *would somebody searching for this
   capability find this note?*
2. **A source has more than one capability, and the separable ones each get stated.** A note
   that names only a source's headline is findable only by people who already want the
   headline. Where a second capability stands on its own, say so and mark it separable.

## Two Failure Classes, And They Need Different Responses

When a search that should have worked did not, the instinct is to widen a description. That is
right half the time and actively harmful the other half.

| | **Description gap** | **Coverage gap** |
| --- | --- | --- |
| What happened | The material is in the catalogue; nothing says it in a claim section | Nothing in the catalogue does this |
| How to tell | The fact is in an inventory, a caveat, or frontmatter | No source has it, in any section |
| Response | Widen a claim section, using the source's own evidence | Scout for it; record the gap until then |
| The wrong response | Scouting for something already held | Writing the missing capability into a note that does not have it |

The second wrong response is the dangerous one, because it makes the test pass and the
catalogue lie.

## Never Write Toward The Test

`librarian scenario` measures whether somebody mid-project can find what they need. It is
worthless the moment notes are written to satisfy it. So:

- **A capability statement must be one you would have written had the scenario never existed.**
  If it borrows the scenario's vocabulary, it is an echo and it measures nothing.
- **Correct a scenario only on the merits, and record the correction in the file.** One
  scenario listed `duckdb - duckdb` as a strong answer for making a rebuild incremental. duckdb
  does no incremental anything; the expectation was wrong when written. That correction is
  noted inside `scenarios.json`, next to the scenario, so a reader can judge whether it was
  honest.
- **A miss you cannot close honestly stays a miss.** One scenario still fails: the catalogue
  holds the right answers and no lexical query reaches them, because *"recompute only what
  changed"* and *"keep the rebuild cheap as the corpus grows"* share no words. Widening the
  note until the words match would be writing toward the test. It is recorded as the first
  measured case for semantic retrieval instead.

## Evidence Rules

These are not negotiable and they are what keeps the standard from degrading into fluent
invention.

- **Read the structure, not only the README.** A README says what its authors want noticed; the
  tree says what is there. Where they differ, the tree is the more interesting fact and both go
  in the note.
- **Every factual field comes from a fetched source.** `Unknown` is a valid value. A plausible
  guess is a defect (`EVIDENCE_REQUIRED`).
- **Say what was read.** A note written from documentation alone says so in `Evidence`. Depth of
  reading is itself evidence a later reader needs.
- **Never write an inventory from a description.** If the tree was not opened, `What Is Inside`
  is absent. An invented inventory is worse than none, because it cannot be distinguished from a
  real one.
- **A negative result is recorded as carefully as a positive one.** "Marketing copy for a
  proprietary product, no code" stops the next person spending an afternoon. Abandonment,
  synthetic demos and missing code are findings.

## Scope Control

The counter-risk is real: a note that records everything is as unusable as one that records
nothing, and an unbounded writing task never finishes.

- **Even coverage before depth.** Every source in a cohort gets the floor before any source gets
  more. Depth on the first three and a paragraph on the rest is the failure mode — the point of
  an even pass is that you cannot know in advance where the useful thing is.
- **Inventory by kind, not by file.** `What Is Inside` names directories, counts and the handful
  of paths that decide relevance. It is not a directory listing; a listing is available from the
  source and carries no judgement.
- **Roughly 400 to 800 words of prose.** Not a limit to hit, an observation about where the
  useful range has fallen. Much shorter is usually generic; much longer is usually a listing.
- **Update rather than append.** When a source is re-read, correct the note. Notes are not logs;
  [[Application Index]] and the dated reports carry history.

## When A Note Is Wrong

Correct it and say so in `Evidence`. Do not delete a finding because it has become inconvenient
or because a later reading disagrees — record what changed and when. Two of the seventeen
sources in the 2026-09 cohort had moved repository path, and four were materially not what their
metadata claimed; a note that quietly re-aligns with a description loses the finding that made
it worth having.

## Related
- [[Note Content Model]] — the schema, and the floor this standard names
- [[Use Contexts And Agnostic Description]] — who the reader is, and why domain framing hides a source
- [[Applicable Techniques From The 2026-09 Cohort]] — worked examples of what gets missed
- [[Design Specification]] — `EVIDENCE_REQUIRED`, and why access points are the permitted extract
- [[Scouting Working File 2026-09-03]] — what a per-source evidence trail looks like
- [[Master Index]]
