---
type: "application_hub"
status: "active"
record_count: 4
purpose: "evidence of use - what was taken from a source, when, and what it saved"
---

# Application Index

## Why This Layer Exists
A resource note says what something is. An application record says what happened when it was actually used: which repository was chosen, what was taken from it, at what stage of a project, and what that avoided building.

This is the layer that makes the catalogue compound rather than merely accumulate. Three things only exist here:

- **Stage evidence.** Knowing a resource was useful *at the point of choosing a front end* is worth more than knowing it is a UI framework. It tells the next person when to reach for it.
- **Transferable patterns.** The most valuable finds are usually structural rather than functional — a way of organising something that had not occurred to you. Those are invisible in a repository description and only surface in use.
- **Avoided cost.** "This removed the need for a second database" is the kind of claim that justifies the whole catalogue, and it can only be recorded after the fact.

## How A Record Is Used
Applications are cited *from* resource notes and topic indexes, so a person or agent evaluating a resource can see whether it has been used, for what, and whether it worked. An unproven resource is not disqualified — but a proven one should be preferred, and the catalogue should be able to say which is which.

For agents: when recommending a resource, check for application records citing it first. A recorded use with a named outcome outranks a plausible-sounding description every time.

## Records

| Project | Domain | What the catalogue supplied |
| --- | --- | --- |
| [[Application - Donor Front End And RAG Context Control]] | AI systems, frontend | A UI donor plus a context-control pattern that collapsed several databases into one |
| [[Application - Quantum Simulation Project]] | Scientific simulation | Volumetric methods, solvers, verification techniques, then comparison datasets |
| [[Application - Agent Harnesses And Training Pipelines]] | Agentic AI, ML training | Harness patterns and pipeline structure across a two-year capability ramp |
| [[Application - Distributed Systems And Monitoring]] | Infrastructure, embedded | Monitoring under failure conditions; now embedded and network learning |

## Writing A Record
Write one when a source materially changed what you built or how long it took. Not every use — the ones where the answer to *what did this save* is specific.

Required frontmatter: `project`, `stage`, `resources_used`, `outcome`. The body must answer:

1. **What was needed** — the problem, before any resource was found.
2. **What was taken** — code, a design pattern, a dataset, a method, or only an idea.
3. **What it replaced** — the thing you would otherwise have built, and roughly what that would have cost.
4. **What the catalogue should learn** — the requirement this exposes, so the next search is better than this one was.

Point four is the one that matters. A record that only says what happened is a diary entry; a record that says what the catalogue should have had ready is a specification.

## Related
- [[Workflow Index]]
- [[Library Assessment 2026-09]]
- [[Master Index]]
