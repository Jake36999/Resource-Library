---
type: "master_index"
status: "active"
purpose: "root router"
topic_count: 15
workflow_count: 4
layers: ["workflows", "topics", "resources", "papers", "glossary", "patterns", "reviews", "scouting"]
---

# Master Index

## Start Here

**If you are trying to do something**, go to [[Workflow Index]]. It routes by situation and presents material in the order it becomes useful. This is the entry point for agents.

**If you are looking for a kind of thing**, use the Route Map below. It routes by category.

The distinction matters: the route map answers *what is this?*, the workflow layer answers *what do I do now?* Most failed lookups here are the second question asked of the first structure.

## Route Map
- [[Topic - Curated Aggregators & Reference Lists]] (9 approved)
- [[Topic - Agentic AI & Models]] (5 approved)
- [[Topic - Data APIs & Big Data]] (12 approved)
- [[Topic - Geospatial & Earth Data]] (5 approved)
- [[Topic - Infrastructure & Observability]] (9 approved)
- [[Topic - Security & SIEM]] (5 approved)
- [[Topic - Frontend & Design Systems]] (6 approved)
- [[Topic - Scientific Simulation & Math]] (7 approved)
- [[Topic - Government & Civic Tech]] (4 approved)
- [[Topic - CAD & SaaS Design]] (4 approved)
- [[Topic - Architecture & Developer Playbooks]] (7 approved)
- [[Topic - Code Intelligence & Structural Parsing]] (16 approved)
- [[Topic - Knowledge Management]] (20 approved)
- [[Topic - Data Lineage & Provenance]] (8 approved)
- [[Topic - ML Training & MLOps]] (11 approved)

## Hubs
- [[Workflow Index]] - situational entry point
- [[Taxonomy Index]] - all resources across nine comparison axes
- [[Glossary Index]] - canonical meanings and observed contexts
- [[Pattern Index]] - reusable structures across domains
- [[Paper Index]] - written research alongside software
- [[Review Queue]] - held pending manual review

## Where Things Live

- **`01-Resources/`, `02-Glossary/`, `03-Patterns/`, `04-Reviews/`, `06-Papers/`,
  `09-Applications/`** - the sources and their descriptors. This is what the
  catalogue is *for*.
- **`00-Indexes/`** - navigation only: this note, the taxonomy matrix, and the
  fifteen topics.
- **`internal docs/`** - how the system itself is built, specified and measured.
  Separated from `00-Indexes` on 2026-09-04 so the system's own construction
  notes stop competing with source descriptors for a reader's attention.
- **`.utility/`, `.Data/`** - dot-prefixed, so Obsidian does not show them. Code
  and operational state in the first; fetched data and derived stores in the
  second. See `.Data/README.md`, which is written for an agent rather than a
  person.

## Internal Documentation

The design record, in the order it is worth reading:

- [[Data Information Knowledge]] - the layering everything else is organised by
- [[Design Specification]] - what the system is, why it is shaped that way, and the named policies
- [[Implementation Brief]] - where to start and in what order
- [[System Implementation Status]] - what is built, what it proved, what is open
- [[System Assessment 2026-09-04]] - what is actually populated, what is missing, and what it would take to beat writing this from scratch
- [[Meta Analysis And Final Shape 2026-09-04]] - what twenty-four analyses have in common, what none looked at, and the shape to build to
- [[Implementation Defect Analysis 2026-09-06]] - thirty-five defects from building, what they share, and the rule that would have caught most
- [[Finalisation Plan 2026-09-04]] - six stages from measured weak spots to a standalone tool
- [[Service Map]] - each part's job stated agnostically, and what already does that job
- [[Note Content Model]] - the note schema and the closed axis values
- [[Source Documentation Standard]] - what a resource note owes a reader
- [[Use Contexts And Agnostic Description]] - who uses this and why descriptions must be domain-neutral
- [[Scouting Domains]] - the authoritative domain register
- [[Schema Extension - Containers and Papers]] - aggregator expansion and the paper layer
- [[Schema Extension - Scouting Pipeline]] - automated discovery, ranking and deep dive
- [[Licence Resolution 2026-09-03]] - what was read, and what a person still owes
- [[Scouting Working File 2026-09-03]], [[Scouting Working File 2026-09-04]] - the evidence trails

## Three Ways In

**A person** reads. Open a topic and follow it; nothing below this line is
needed.

**An agent with a problem** should spend as little as possible getting
oriented, in this order - each step costs more than the last:

```
python -m librarian components vocab            # what can I filter on
python -m librarian components signal grammars  # narrow structurally, no prose
python -m librarian query donor "<need>"        # read what survived
```

**Anyone measuring the system** uses `librarian eval` for the index,
`librarian scenario` for whether it answers real questions, and
`librarian relevance` to compare ranking configurations without confounding a
ranking change with a corpus change.

The catalogue locates prior work. It does not extract it.
