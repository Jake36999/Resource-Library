---
type: "workflow"
status: "active"
triggers: ["build a catalogue", "build a knowledge base", "internal reference library", "index our resources", "second brain", "documentation index", "curate resources", "knowledge graph of tools"]
preconditions: ["you know who reads it - a person, an agent, or both", "you can name one question it must answer on day one"]
stages: ["Decide the unit", "Get something usable in a week", "Make retrieval honest", "Automate the intake", "Keep it from rotting"]
exit_criteria: "a person or agent asks a real question and gets a specific, correct answer faster than by searching the web"
anti_patterns: ["designing the schema before cataloguing anything", "bulk ingestion before retrieval is tested", "hand-maintaining a list that could be generated"]
---

# Workflow - Build A Knowledge Catalogue

## Situation
You have accumulated more useful material than you can hold in your head, and you want a catalogue that you and your agents can traverse. This vault is one, so this workflow is written partly from its own scars — see [[Library Assessment 2026-09]] for what went wrong here.

## Decide First
Two questions, before any tooling.

**Who reads it?** A catalogue for people optimises for browsing and recall. A catalogue for agents optimises for structured fields and predictable link shapes. If the answer is both, the structured fields win, because a human can read a structured note but an agent cannot reliably read prose.

**What is the one question it must answer on day one?** Not a category list — a question. "Which of our tools can read Parquet?" is a question. "Data tools" is a category. If you cannot state the question, you are not ready to build; you are collecting.

## Stage 1 - Decide the unit
The unit of the catalogue is the thing that gets one entry. Get this wrong and everything downstream inherits the error.

The trap is the container. An awesome-list is one repository but a thousand resources; a monorepo is one entry but twelve tools. [[public-apis - public-apis]] is the clearest case in this vault: a single note stands in for roughly 1,400 APIs, which means the note records that the list exists and nothing about what is in it.

Decide now whether containers are entries, contents, or both — and if both, how a content entry points back at its container. [[Schema Extension - Containers and Papers]] is the resolution used here.

**Why now:** the unit determines the schema, and the schema is the thing you cannot cheaply change once you have four hundred notes.

## Stage 2 - Get something usable in a week
Catalogue thirty entries by hand, in whatever format is fastest, and answer your day-one question with them. Thirty is enough to expose a bad schema and cheap enough to throw away.

Use [[cfpb - open-source-checklist]] as the shape of the intake questions — it is a governance checklist for adopting open source, and its fields are close to what a resource entry needs. [[goldbergyoni - nodebestpractices]] is worth reading not for Node but for its *form*: every item is a claim, a rationale, and a consequence for ignoring it. That structure survives translation into a catalogue entry better than a description does.

**Why now:** a schema validated against thirty real entries is worth more than one designed against an imagined thousand.

**Not yet:** do not write an ingestion pipeline. You do not know what you are ingesting into.

## Stage 3 - Make retrieval honest
This is the stage this vault skipped, and the cost was 39 notes that describe their topic instead of themselves.

Before adding anything more, take five entries from different categories and read only their retrieval fields — the ones an agent would match against. If two entries from the same category are indistinguishable, your intake is filling fields from the category template rather than the source. Fix the intake before you scale it; every entry added afterwards inherits the defect.

The test worth stealing is [[dbt-labs - dbt-core]]'s: declarative assertions that run in the pipeline, so a broken relationship fails the build rather than being discovered months later. A catalogue's equivalents are *every link resolves*, *no two entries share a description*, *every entry has a source URL*.

[[stac-utils - pystac]] shows the stricter version of the same idea — a published spec, with validation against it, and typed extensions for domain fields. Worth adopting once your schema has stopped moving.

**Why now:** retrieval quality is the product. Volume added before this stage multiplies the defect.

**Exit criterion:** two entries in the same category return visibly different answers to your day-one question.

## Stage 4 - Automate the intake
Only now does a pipeline make sense, because now you know what a good entry looks like.

Three things, in order. **Fetch facts deterministically** — descriptions, licences, dates, activity all come from an API, never from a language model's recollection. **Let a small model do classification only** — filing and tagging, not judgement. **Rank what to process next**, because you will always have a longer candidate list than budget.

That last one is a solved problem you already have on the shelf: [[asreview]] does active-learning screening for systematic literature reviews, which is precisely "given far too many candidates and a human who can only read some, choose the next most informative one". The design in [[Schema Extension - Scouting Pipeline]] arrives at the same shape independently; reading asreview first would have been quicker.

If the source you are cataloguing is itself a list, generate rather than curate — [[orsinium-labs - generated-awesomeness]] is the argument for it.

**Not yet:** do not turn on bulk scouting until Stage 3 passes. This is the single most expensive mistake available here.

## Stage 5 - Keep it from rotting
Three decay modes, each with a countermeasure already in this vault.

*Entries go stale.* Record when each was last verified and re-check on a schedule. Activity signals (last push, archived flags) are cheap to refresh in bulk.

*Links rot.* [[public-apis - public-apis]] validates link health in CI on every pull request. A directory nobody checks becomes a directory of 404s.

*The visual layer drifts.* This vault's canvases still show the library as it stood before 23 resources were added. Any derived view must be regenerated by the build, never edited by hand, or it becomes a confident picture of a library that no longer exists.

## Not Yet - The Steel Framing
Things worth having eventually that will stall you if you insist on them at the start:

- **A graph database.** Markdown files with links are a graph. Add a real graph store when a query you actually need is impossible, not before.
- **Embeddings and semantic search.** Excellent at four hundred entries, pointless at thirty, and it hides bad entries behind plausible similarity scores rather than exposing them.
- **A published schema specification.** Write it once the schema has survived two months without a breaking change.
- **A UI.** Obsidian, a directory of Markdown, or a spreadsheet is a UI. Building one before the content is worth reading is the purest form of this mistake.

## Exit Criteria
Someone asks a real question, gets a specific and correct answer, and it was faster than searching the web. If the answer is a category rather than a resource, return to Stage 3.

## Applies These Patterns
- [[Pattern - Curated Resource Curation]]
- [[Pattern - Knowledge Graph Routing]]
- [[Pattern - Schema Mapping]]
- [[Pattern - Reference Architecture]]

## Related
- [[Library Assessment 2026-09]]
- [[Schema Extension - Containers and Papers]]
- [[Schema Extension - Scouting Pipeline]]
- [[Workflow - Adopt A Dependency]]
