---
type: "schema_spec"
status: "proposed"
version: "1.0"
supersedes: "none"
affects: ["01-Resources", "04-Reviews", "06-Papers", "00-Indexes", "03-Patterns", "02-Glossary"]
new_folders: ["06-Papers"]
new_resource_fields: ["container", "container_kind", "expansion_status", "child_count", "listed_in"]
new_note_types: ["research_paper", "container_child"]
---

# Schema Extension - Containers and Papers

## Why This Exists
The catalogue currently makes two assumptions that no longer hold.

The first is that one repository equals one resource. That is false for aggregator repositories. `public-apis` lists roughly 1,400 APIs; `awesome-jupyter` lists several hundred projects. The note for such a repository records *that a list exists*, not *what is in it*, so the catalogue's most resource-dense entries contribute the least retrievable knowledge.

The second is that every catalogued thing is software. It is not. A large share of the useful material on GitHub is written rather than executable — white papers, preprints, specifications, and reference reports. A paper has no default branch, no star-based maturity signal, and its licence is rarely the axis anyone cares about. Forcing it into the repository schema loses what actually matters: authors, venue, year, and a stable identifier.

Both gaps point the same way. This vault becomes an encyclopaedia rather than a repository list at the moment theory and implementation meet on the same page — and the join is the pattern layer.

## Part One - Container Expansion

### The Idea
A container is a resource whose value is its contents. It keeps its own note, but that note is promoted from leaf to hub: it gains a manifest of children, and each meaningful child becomes a resource in its own right, linked back to the parent.

### New Frontmatter on Container Resources
- `container: true`
- `container_kind`: one of `awesome_list`, `link_directory`, `api_directory`, `bibliography`, `code_collection`
- `expansion_status`: `pending`, `partial`, `complete`, or `declined`
- `child_count`: integer, count of extracted children
- `expansion_selector`: how children were located, e.g. `markdown_table:README.md`, `bullet_links:README.md`

### New Frontmatter on Extracted Children
- `listed_in`: array of parent note names
- `discovery_source`: `container_expansion`
- `promotion_status`: `child_only`, `promoted`, or `rejected`

A child begins as `child_only` — present, searchable, linked, but not a full note. It is promoted to a full resource note only when something makes it worth the cost: a human marks it, or it appears in two or more independent containers, which is a strong signal of consensus.

### Semantic Links
- On the child: `[listed_in:: [[parent note]]]`
- On the parent: `[expands_to:: [[child note]]]`

### Extraction Rules
1. Parse the parent's README for markdown tables and bullet lists containing links.
2. Keep the row's own annotation as the child's description; do not invent one.
3. Normalise any `github.com/owner/repo` link into a `repo_key` so children deduplicate against existing resources by key, not by title.
4. A child whose `repo_key` already exists as a full resource note does not create a new note — it adds a `listed_in` edge to the existing one. This is where the graph gets genuinely valuable: it reveals which catalogued tools multiple curators independently endorse.
5. Dead links, and rows resolving to a 404, are recorded with `promotion_status: rejected` rather than dropped, so the same dead entry is not re-examined on every run.

### Cost Control
Full expansion of every container would add thousands of notes and swamp the graph view. The default is a **manifest-first** expansion: children are written as rows in a single `Manifest - <parent>.md` note per container, and only promoted children become standalone notes. One file per container, not fourteen hundred.

## Part Two - The Paper Layer

### Folder
`06-Papers`, sibling to `01-Resources`, with `Paper Index.md` as its hub.

### Frontmatter for `type: "research_paper"`
- `title`, `authors` (array), `year`, `venue`
- `identifier_kind`: `arxiv`, `doi`, `handle`, `url`, or `none`
- `identifier`: the stable id itself
- `canonical_url`
- `paper_kind`: `preprint`, `peer_reviewed`, `white_paper`, `specification`, `technical_report`, `thesis`
- `source_repo`: repo_key, when the paper was found in or accompanies a repository
- `implemented_by`: array of resource note names that implement the paper's method
- `patterns`, `glossary_terms`: shared with the resource layer, unchanged
- `evidence_count`, `status`, `sensitivity`: as in the resource layer

### Body Sections
`Bottom Line`, `Claim`, `Method`, `Evidence & Limits`, `Relevance to This Catalogue`, `Semantic Links`, `Citation`.

`Evidence & Limits` is mandatory and is the section that keeps the layer honest: sample size, benchmark, what the authors themselves flag as a limitation. A catalogue that records claims without limits is worse than no catalogue, because it launders uncertainty into apparent fact.

### Why Papers Share the Glossary and Pattern Layers
A paper describing a detection technique and a repository implementing it should resolve to the same `Pattern - Detection as Code` note. That shared spine is the whole point: an agent traversing a pattern finds the theory, the implementation, and the vocabulary in one hop, instead of three disconnected silos.

### Sourcing
Papers reach the vault three ways, in descending order of reliability:
1. A `papers/` or `docs/` directory, or a citation block, inside an already-catalogued repository.
2. A bibliography container expanded under Part One.
3. Explicit addition by the user.

Metadata comes from the arXiv or Crossref API — deterministic, like the GitHub fetch — never from a language model's recollection of a title. The same division of labour applies here as everywhere in this pipeline: fetch facts, infer judgement.

## Implementation Order
1. Add the container fields to existing aggregator notes and mark them `expansion_status: pending`. *(done)*
2. Create `06-Papers` with its hub and note template. *(done)*
3. Build the manifest extractor for one container as a proving run, ideally `public-apis`.
4. Add the arXiv/Crossref fetch adapter alongside the GitHub one.
5. Extend the Taxonomy Index with a papers matrix, or add a `layer` column so both kinds share one table.

## Open Questions
- Should a promoted child inherit the parent's topic, or be routed independently? Independent routing is more correct and more expensive.
- Do papers belong in the Taxonomy Index at all? Most of its nine axes are meaningless for a document.
- What is the retention rule for a container whose upstream list has been archived — freeze the manifest, or mark every child stale?
