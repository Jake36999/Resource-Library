---
type: "review"
status: "active"
created: "2026-09-03"
reviews: "[[Research Report 2026-09-03 - Lineage, Parsing and Graph Reasoning]]"
verdict: "inspection genuine; container classification failed on a schema gap"
---

# Review 2026-09-03 - Research Pass and Container Gap

## 1. The Question Asked

*Did they actually look at the sources using the tools available, and assess what each of them offers?*

**Yes.** The evidence is in the counts and the internal vocabulary, neither of which survives a README skim.

| Note | Detail recorded | Why it is proof of inspection |
| --- | --- | --- |
| `ganarajpr - awesome-dspy` | "a single 96-line Markdown file pointing at roughly sixty DSPy projects"; names STORM, xmc.dspy, dspy-redteam | Line count requires opening the file; the three named projects are rows inside it |
| `tree-sitter - tree-sitter` | "the `prepare_grammar` stage splits one grammar into two — a syntax grammar over non-terminals and a lexical grammar over terminals — before parse tables are built" | `prepare_grammar` is an internal stage name, not README vocabulary |
| `open-metadata - OpenMetadata` | "904 JSON Schemas, from which the Java, Python and TypeScript models are generated"; "120+ ingestion connectors" | Both are directory counts, not stated figures |
| `syntax-tree - mdast` | "two abstract interfaces (`Literal`, `Parent`) and nineteen concrete nodes, written in a Web IDL-like grammar" | Requires reading the spec body and counting |
| `syntax-tree - mdast` | licence recorded as `CC-BY-4.0 (stated in readme; GitHub API reports no licence)` | Correct evidence discipline — records the conflict rather than resolving it silently |

The report's §0 is stronger still, and was not asked for. It measured MRR before and after the pass (0.91 → 0.84), diagnosed two pre-existing defects — a single-token name match outranking a four-term body match (`run-llama` winning on the token `run` over `apache - airflow`), and 346 of 2,053 chunks being pure boilerplate — then measured four fix configurations. The finding that matters: **the chunking fix alone made retrieval worse** (0.77), because removing boilerplate handed more relative weight to the broken name ranking. "Ship them together or not at all." Final MRR 0.93, above the pre-pass 0.91 on a corpus a quarter larger.

That is a session that tested its own work and reported a regression it caused. Take the substantive claims seriously.

## 2. The Underspecified Probe — What Happened

The probe was whether directory-type sources would be flagged as containers without being told.

**Result: one of six.** Only `ganarajpr - awesome-dspy` carries `container: true` + `expansion_status: pending`, and even that record is incomplete — no `container_kind`, no `expansion_selector`, so the intake pipeline cannot act on it.

Unflagged, despite each note's own prose describing the directory property explicitly:

- `tree-sitter` — an ecosystem of separately-versioned grammar repositories
- `syntax-tree - mdast` — the spec anchoring the unified/remark utility ecosystem
- `open-metadata - OpenMetadata` — 904 schemas and 120+ connectors
- `run-llama - llama_index` — LlamaHub
- `semgrep - semgrep` — the public rule registry

## 3. Diagnosis — This Is A Schema Gap, Not Carelessness

`container_kind` currently admits five values:

```
awesome_list | link_directory | api_directory | bibliography | code_collection
```

Every one of them describes **a document that lists things**. None describes **a tool or specification that anchors an ecosystem of separately-versioned satellite artefacts**. The agent detected the property — it wrote it in prose in each note — and had nowhere to put it. Given a schema with no fitting value, writing the observation in prose and leaving the field unset is the correct behaviour under the vault's own rule *do not stretch an existing key to fit*.

This matters because it changes the remedy. A carelessness diagnosis leads to better instructions, which decay. A schema diagnosis leads to a fix that holds.

It also generalises: the same blind spot means `awesome_list` was applied where a directory *of documents* existed, but nothing in the taxonomy captures "the material is in the satellites, and the satellites are versioned and governed separately from the anchor." That distinction determines the expansion strategy — an awesome-list is expanded by parsing a README once, whereas an ecosystem anchor is expanded by enumerating a registry or an org, which is a live query with a freshness rule attached.

## 4. Why This Is The Highest-Value Thread Open

These sources are the route to formalised methods and design patterns the system was built without. Concretely, expanding the five unflagged containers reaches:

- tree-sitter's grammar corpus — every one a worked example of a formal grammar for a real language
- mdast's utility ecosystem — dozens of small, single-purpose AST transforms; the reference library for tree manipulation as a discipline
- OpenMetadata's 904 schemas — a production-grade data model expressed as machine-readable contracts, which is directly the artefact class this vault's own schema work has been improvising
- LlamaHub — retrieval and connector patterns
- semgrep's rule registry — detection-as-code at volume, and the abstract-rule/backend-compilation pattern already recorded from sigma, seen in a second independent implementation

That is the difference between the current design and one informed by production practice.

## 5. Plan

### 5.1 Close the schema gap *(first — everything else depends on the vocabulary)*
Extend `container_kind` with a sixth value, `ecosystem_anchor`: a source whose value lies substantially in separately-versioned satellite artefacts it anchors, governs or specifies. Add a companion field `expansion_source` distinguishing how satellites are enumerated:

- `readme_parse` — parse the anchor's own document (existing behaviour, the five current kinds)
- `registry_query` — query a published index (semgrep rules, LlamaHub)
- `org_enumeration` — enumerate an organisation's repositories (tree-sitter grammars, syntax-tree utilities)
- `schema_directory` — enumerate a directory of specification files (OpenMetadata)

Record the open question this raises rather than deciding it now: an `org_enumeration` container has no fixed child set, so `expansion_status: complete` is not meaningful for it — it needs a `last_enumerated` date and a staleness rule instead.

### 5.2 Backfill the six records
Set `container: true`, `container_kind`, `expansion_source`, `expansion_selector`, `expansion_status: pending` on tree-sitter, mdast, OpenMetadata, llama_index, semgrep; complete the incomplete awesome-dspy record. Manifest-first, as Part One of the schema extension already rules — one `Manifest - <parent>.md` per container, not a note per child.

### 5.3 Prove the extractor on one container before the other five
`ganarajpr - awesome-dspy` is the right proving run and not `public-apis` as originally planned: 96 lines and ~60 entries is small enough to verify by hand, and it exercises the dedupe-by-`repo_key` path against notes that already exist. `public-apis` at ~1,400 rows proves throughput, not correctness, and should follow.

### 5.4 Then, and only then, expand OpenMetadata
Its 904 schemas are the prize and the trap. They are not resources in the catalogue's sense — they are a data model to *learn from*, not sources to list. The likely correct outcome is a small number of pattern notes plus one manifest, not 904 anything. Decide that before running the extractor, not after.

### 5.5 Outstanding, unchanged
- Regenerate `05-Canvases` — stale by 23 resources.
- Confirm the licence regression is fully closed by `Licence Resolution 2026-09-03`, and that trap §2.1 (build-script clobbering) cannot fire again.
- Review report §1–§12. Three candidate changes (5.1, 5.2, 5.4) are already marked **applied 2026-09-03**; §11 Proposals Requiring A Decision has not been read and nothing in it should be endorsed until it has.

## Related
- [[Research Report 2026-09-03 - Lineage, Parsing and Graph Reasoning]]
- [[Schema Extension - Containers and Papers]]
- [[Design Specification]]
- [[Implementation Brief]]
