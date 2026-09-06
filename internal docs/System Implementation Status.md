---
type: "status"
status: "active"
created: "2026-09-02"
implements: "[[Design Specification]]"
sequence: "[[Implementation Brief]]"
code: ".utility/librarian/"
authority: "where this note and working, tested code disagree, the code is current truth"
---

# System Implementation Status

## What Exists

The system end of the catalogue is built and tested in `.utility/librarian/`,
alongside the scouting pipeline in `.utility/scout/` that it extends. Run
`python -m librarian status` from `.utility` for the live picture; this note
records what was built and what it proved.

| Brief step | Component | State |
| --- | --- | --- |
| 1 | `index.py` - vault → SQLite + FTS5 | Built. 208 notes, 1,547 chunks, 1,844 links in 0.33 s |
| 2 | `integrity.py` - eleven assertions | Built. 0 errors against the vault |
| 3 | `consult.py` - the six queries, filters first | Built. hit@5 1.00 on the eval set |
| 4 | Embeddings + RRF fusion | Built. 1,547 chunks at 768 dims, optional |
| 5 | The eval set | Built. 20 questions with known answers |
| 6 | `toolchain.py` - the ToolSet adapter | Built. Works with the ToolSet absent |
| 7 | Deep dive rewired to call it | Built. Behind `scout.toolchain_evidence` |
| 8 | Access points | Built. Extraction, storage, reachability check |
| 9 | `graph.py` - the vault graph | Built. 11 communities via graphify |
| 10 | `workbench.py` - Mode D | Built. Docker sandbox, `open`/`document`/`close` |
| 11 | MCP surface | Built. Nine read tools, one write |

150 tests pass - 48 existing, 102 new. None requires Docker, LM Studio, network
access or the ToolSet; every external is injected.

## What It Proved

**Retrieval works on filters and lexical search alone.** Twenty questions,
`hit@5 1.00`, `recall@5 0.97`, `MRR 0.91`, roughly 0.15 s per query. Adding
embeddings changed none of those numbers on this set. That is worth knowing
before anyone spends time tuning vectors: at this vault's size the expensive
half of the retrieval stack is not currently earning its cost, and the eval set
is what makes that visible rather than arguable.

**The vault's links are sound.** Every wikilink resolves, no two resources
share a `Bottom Line` or `What It Solves` block, and every resource has a
canonical URL and a licence class. The rewrite held.

## What The Checks Found

Two findings that belong to the catalogue rather than to the code.

**The taxonomy matrix disagrees with the notes on 29 axis values**, almost all
of them `license_class`. The matrix says `Permissive` where the frontmatter
says `Unknown`, because the matrix retains values from the topic-template
bootstrap while the frontmatter carries what GitHub actually returned. The note
is truth, so the matrix is stale and a build run should fix it - but the
underlying fact is that **49 of 64 resources have `license_class: Unknown`**,
and a filter is only as useful as the field it filters on. `find_donor` with
`license_class=Permissive` currently eliminates three quarters of the
catalogue, correctly and unhelpfully. Refreshing licence metadata is the single
highest-value content task available.

**Two communities disagree with their topic assignment.** Community 0 spans the
aggregators and the architecture playbooks; community 1 puts the CAD tools with
the frontend design systems. Both are reported, neither is applied - a
community is an observation, and [[Scouting Domains]] remains the sole
authority over what a topic is.

## Decisions Taken In Implementation

Recorded because they resolve ambiguities in the specification rather than
merely following it.

**Slices are not indexed, including in the intake.** Section 4.2 says the slice
"is retained and indexed"; decision 7.2 settles the opposite, and section 3.3
explains why. The later ruling wins: the intake reads a slice as evidence,
writes a structural summary into the dossier, and deletes both the slice and
the clone. There is no permanent index of extracted symbols anywhere.

**`find_technique` ends at tier 3 and says so.** It returns candidate sources
and the evidence that suggests them, plus `open a workbench on X to confirm`.
It never fetches, clones or slices - which is what keeps the read path safe to
expose to a third-party agent.

**`find_data` returns validation criteria from application records.** Section 3
promises them; the brief promises access points. Both are returned, with the
criteria drawn from a record's `patterns_discovered` rather than generated, so
nothing is invented to fill the field.

**The ToolSet is probed, not hard-coded.** [[External Dependencies Reference]]
records `F:\Mark-XLVIII-main\ToolSet`; the host currently has it under
`D:\Aletheia_project\DEV_TOOLS\ToolSet`. Candidates are tried in order, so
neither location is load-bearing.

**Centrality excludes topic indexes as well as hubs and glossary notes.** Being
a good answer to *where does this live* and being structurally central are
different claims, and every note in a topic points at its index.

## Still Open

These were open decisions in the specification and remain judgement calls.

1. **The sweep stopping rule** has no concrete threshold. asreview's
   diminishing-returns criterion is the model; the number is unchosen.
2. **`measured_gap_fit`** is implemented behind a config flag and off. Swapping
   a ranking signal's basis needs measuring against the eval set first.
3. **The eval set is twenty questions written from the vault as it stands.** It
   will need extending as the catalogue grows, and questions whose answers
   leave the vault must be re-pointed rather than left failing - a test
   enforces that they all still resolve.
4. **`record_application` needs no approval**, and agent-written records are
   marked `attested_by: agent` so they can be weighted differently later.

## Related
- [[Design Specification]]
- [[Implementation Brief]]
- [[External Dependencies Reference]]
- [[Finalisation Plan]]
- [[Library Assessment 2026-09]]
