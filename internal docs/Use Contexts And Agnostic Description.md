---
type: "design_note"
status: "active"
created: "2026-09-04"
authority: "governs how sources are described; [[Source Documentation Standard]] carries the obligation, this note carries the reason"
audience: "anyone writing a resource note, and anyone designing the read surface"
---

# Use Contexts And Agnostic Description

## Who Actually Uses This

Not the person building the catalogue. The catalogue is nearly built, and after that the only
changes are additions to the application layer and the deepening of descriptions as more is
learned about a source.

The user is someone in the middle of research and development, with a task in hand, who wants
to know in under a minute whether anything already exists that bears on it. They are not
browsing. They will not read fourteen notes. They arrive with a problem shaped by *their*
architecture, not by the catalogue's categories, and they leave the moment the answer looks
like work.

That changes what "working" means. **Recall is not the measure.** A system that returns the
right note for a question phrased in the catalogue's own vocabulary has proved only that it
can find what it already knows how to describe.

## The Four Contexts A Query Arrives In

Predicting these is what lets the read surface behave like a reference guide rather than a
search box. They are not equally served today.

| Context | What the user is actually asking | Query kind | State |
| --- | --- | --- | --- |
| **Designing** | "I am planning something new — what shapes exist for this?" | `orient`, `find_pattern` | Partly served. Patterns exist; the *comparison* between competing shapes does not. |
| **Solving** | "I have this specific problem — has someone solved it?" | `find_donor` | Best served. Constraints eliminate, results explain themselves. |
| **Sourcing** | "I need a thing with these properties — a dataset, a model, a corpus, a grammar" | `find_data` | Newly served. `What Is Inside` is what made it possible to ask for a corpus rather than a project. |
| **Comparing** | "Something in my architecture does this — what else does it, and differently?" | *none* | **Not served.** This is the gap. |

The fourth is the one that matters most and is the one the catalogue was worst at, because
answering it requires knowing what a source does **independently of what it is**.

## The Failure Mode: Description Written In Its Own Domain

A note that describes a source in the vocabulary of the source's own field is findable only by
someone already standing in that field. The catalogue then works perfectly for questions
nobody needed to ask it.

Worked example, and the one that named the problem:

> **Medallion architecture** — described in its own terms, it is a lakehouse convention:
> Bronze, Silver, Gold, Delta tables, Spark. Described agnostically, it is **grading material
> by level of refinement, so that every stage is reproducible from the one before it and a
> mistake is corrected by replaying rather than by recovering.**

The second reading is the useful one, and it is not about data engineering at all. This vault
has raw scouting output, curated notes and derived views — the same three grades, with the same
replay property, and nobody would ever have found the lakehouse note while thinking about it.
The first reading makes the source invisible outside its field. The second makes it a candidate
anywhere the shape recurs.

Every source in the catalogue has both readings. Only one of them was being written down.

## The Stewardship Trap

There is a specific failure this catalogue exists to counteract, and it is worth stating
plainly because it is the reason the fourth context matters.

Given an existing system and a goal it is not meeting, the default behaviour — of people and of
models — is to **optimise within the architecture already chosen**. Each step is locally
reasonable. Cumulatively they produce a loop of small refinements, and the question *is this
the right approach at all* never gets asked, because asking it invalidates the work already
done.

A recorded instance: a Python physics simulation hitting compute and out-of-memory limits.
Repeated rounds of optimisation, and repeated advice to keep optimising. The actual answer was
a different execution model entirely — GPU array programming — and it arrived by accident
rather than by recommendation. When that in turn hit its own limits, the same pattern repeated:
confident assurance that no alternative existed, until a second alternative was found, also by
accident. Both were mature, widely used, and would have been obvious to anyone who had been
looking for *a different way to do the same job* rather than *a better way to do it this way*.

The lesson is not that the advice was wrong. It is that **nothing in the process was ever
asked to enumerate alternatives at the level of the job rather than the level of the tool.**
A catalogue that describes each source in its own domain's terms cannot answer that question
either — it can only tell you more about what you already have.

So: a failure to consider the options does not merely cost an optimisation. It stalls the
project, and it does so invisibly, because the loop feels like progress.

## What This Requires Of A Note

One addition, and it is a discipline rather than a slot:

**`## Transferable Capability`** — what the source does, stated **without its domain's
vocabulary**, and what that makes it an alternative to.

Two tests while writing it:

1. **Could this sentence be read by someone in an unrelated field and still mean something?**
   If it needs "lakehouse", "syntax tree" or "weak supervision" to parse, it is the domain
   description again.
2. **Does it say what decision this would change?** Not "useful for X" — what it would
   *replace*, *remove* or *make unnecessary*. `duckdb` removes a server. `recipy` removes the
   requirement to declare provenance. `mdast` removes the need for two tools to agree in
   advance.

And one prohibition, which follows from the whole argument: **do not write it toward this
system's current design.** The moment a capability is described as "useful for our scout
pipeline" it has been narrowed to the architecture that happens to exist, which is the
stewardship trap wearing the catalogue's clothes. Describe the capability; let the reader
decide what it is for. If a specific application here is worth recording, it goes in
`Integration & Use Cases` as one instance among possible others — never as the definition.

## What This Requires Of Retrieval

- **Comparison, not just lookup.** Two sources doing the same job by different means should be
  reachable from one query. Agnostic capability text is what makes that possible at all;
  whether it needs a dedicated query kind is an open question, deliberately left open until
  the text exists to test against.
- **Every result still explains itself.** A cross-domain match is exactly the case where a user
  will disbelieve the result, so the `why` matters more here, not less.
- **The catalogue may not decide relevance.** Its job is to put the candidate in front of a
  person with enough specificity to judge. Filtering to what seems on-topic is how the fourth
  context gets closed off again.

## What This Note Does Not Claim

That agnostic description is easy, or that it can be done once. A capability statement written
today reflects what was understood today; the whole point of `Integration & Use Cases` and
[[Application Index]] is that use teaches things description cannot anticipate. Notes are
expected to deepen.

Nor does it claim the four contexts are complete. They are the ones that could be named from
current use. A fifth will appear, and the correct response is to widen this note rather than to
force the query into one of four boxes — the same reason
[[Source Documentation Standard]] is a floor and an obligation rather than a checklist.

## Related
- [[Source Documentation Standard]] — the obligation this note supplies the reason for
- [[Note Content Model]] — where `Transferable Capability` is declared and checked
- [[Applicable Techniques From The 2026-09 Cohort]] — worked agnostic readings of seventeen sources
- [[Design Specification]] — the six query kinds, and the retrieval cost ladder
- [[Master Index]]
