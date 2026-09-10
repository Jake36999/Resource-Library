---
type: "workflow_hub"
status: "active"
purpose: "situational router"
workflow_count: 4
axis: "what you are doing, not what things are"
---

# Workflow Index

## Why This Layer Exists
The topic, taxonomy, pattern and glossary layers all answer the same shape of question: *what is this thing?* That is the right way to organise a library and the wrong way to use one.

At the moment of use nobody asks "what belongs to Infrastructure & Observability". They ask "I have a service in production and no idea when it breaks — what do I do first?" The gap between those two questions is why a well-built catalogue can sit unread beside the project that built it.

A workflow note answers the second kind of question. It is keyed to a **situation**, ordered by **stage**, and it is as explicit about what to ignore for now as about what to reach for.

## The Ordering Rule
Every workflow here obeys one principle, and it is the reason the layer exists at all:

> Use the material that is adequate now. Do not stall waiting for the material that would be ideal later.

Scaffold with timber. Steel goes up when the frame is ready for it, and not before — and a catalogue whose entries all arrive at once, unordered, is a pile of steel delivered on day one. Each workflow therefore has a **Not Yet** section naming what people habitually reach for too early, and why it costs them.

## Workflows

| Situation | Workflow |
| --- | --- |
| Building a catalogue, knowledge base or internal reference | [[Workflow - Build A Knowledge Catalogue]] |
| Deciding whether to adopt an external dependency | [[Workflow - Adopt A Dependency]] |
| Getting a running system to tell you when it breaks | [[Workflow - Stand Up Observability]] |
| Pulling an external data source into something usable | [[Workflow - Ingest An External Data Source]] |
| Letting an agent in another project add to this catalogue | [[Workflow - Contribution By Outside Agents]] |
| Telling a project agent how to use and feed the catalogue | [[Agent Instructions - Using The Library]] |

## For Agents

A co-operating agent should enter here, not at [[Master Index]]. The topic tree is for enumeration; this layer is for action.

**Matching protocol.** Every workflow note carries a `triggers` array in its frontmatter. Match the user's stated task against those triggers first. On a match, load that workflow note *before* loading any resource note: it tells you which resources matter now and which are noise at this stage, which is the difference between a useful answer and a list.

**Contract.** Each workflow guarantees the same frontmatter keys:

- `triggers` — phrases that should route here
- `preconditions` — what must be true or decided before the workflow applies
- `stages` — ordered stage names, each a section in the body
- `exit_criteria` — how to know the workflow is finished
- `anti_patterns` — what is commonly reached for too early

**Rules of use.**

1. Present material for the current stage only. Handing over stage four's options while the reader is at stage one is the failure this layer exists to prevent.
2. A stage names resources *and* the reason they apply now. A bare link is not an answer.
3. If no workflow matches, say so and fall back to [[Master Index]]. Do not improvise a workflow — an invented sequence carries the authority of the vault without its scrutiny.
4. Resource notes marked `maturity: seed` are described from a template rather than their source (see [[Library Assessment 2026-09]]). Treat their `What It Solves` and `Integration & Use Cases` sections as unverified until the note is rewritten.

## Writing A New Workflow
A workflow earns its place when a sequence has been walked twice and the ordering mattered. Keep to the shape: Situation, Decide First, numbered Stages with a *why now* for each resource, Not Yet, Exit Criteria. Prose over bullets where the reasoning matters; a workflow that only lists tools has become a topic index with extra steps.

## Related
- [[Library Assessment 2026-09]]
- [[Master Index]]
- [[Pattern Index]]
