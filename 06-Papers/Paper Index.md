---
type: "paper_hub"
status: "active"
paper_count: 0
schema: "[[Schema Extension - Containers and Papers]]"
---

# Paper Index

## Purpose
The paper layer holds written research — preprints, peer-reviewed papers, white papers, specifications and technical reports — as first-class catalogue entries alongside software resources.

A paper and the repository implementing its method share the same pattern and glossary notes, so traversing a pattern reaches the theory and the implementation together rather than either alone.

## Papers
- None yet.

## Operating Rules
- Bibliographic metadata is fetched deterministically from arXiv or Crossref, never recalled by a language model.
- Every paper note carries an `Evidence & Limits` section. A claim recorded without its limits is worse than no record.
- A paper implemented by a catalogued repository links to it with `[implemented_by:: [[resource]]]`, and the repository links back with `[implements_paper:: [[paper]]]`.
- Papers route through the same topic indexes as resources; they do not get a parallel topic tree.

## Related Hubs
- [[Master Index]]
- [[Pattern Index]]
- [[Glossary Index]]
- [[Taxonomy Index]]
