---
type: "roadmap"
status: "active"
created: "2026-09-01"
goal: "ready for population at volume and for use as a working reference"
phases: ["Correctness", "Retrieval", "Use", "Scale"]
blocking_order: "each phase gates the next; do not run scouting at volume before phase 2 is done"
---

# Finalisation Plan

## What "Ready" Means
Two conditions, and the second is the one usually skipped.

**Ready to populate:** material can be added at volume without making the catalogue worse. That requires the intake to produce distinct, evidence-backed entries and the ranker to order them sensibly — both now true, but neither yet proven against a real run.

**Ready to apply:** a person or agent with a problem reaches the right material at the right moment. That requires retrieval that works on meaning as well as words, and a record of what has actually been useful. The application layer now exists; the search does not.

The four phases below are ordered so that each is worth doing before the next. The single most expensive mistake available is running phase 4 before phase 2.

---

## Phase 1 - Correctness (mostly done)

| Item | State |
| --- | --- |
| Live GitHub metadata on every note | Done |
| 41 templated notes rewritten from fetched evidence | Done |
| Licence classes corrected, `Source_Available` distinguished | Done |
| Licence overrides survive a rebuild | Done |
| Root router reaches every layer | Done |
| **Regenerate the canvases** | **Outstanding** |
| **Run the build end to end and confirm nothing regresses** | **Outstanding** |

The canvases still show the library as it stood before 23 resources and 13 patterns were added. They are generated artefacts, so this is a build run, not an editing job — but until it happens the visual layer is confidently wrong.

The build run also matters as a regression test: this session edited notes directly, and the build regenerates them from the database. **Run it once and diff before trusting it**, because anything the build recomputes from a template will overwrite hand-written content. If it does, the fix is to make the build read the rewritten sections rather than to stop running it.

---

## Phase 2 - Retrieval (the gate)

Nothing downstream is worth doing until search works. The rewrite made this possible; it did not make it exist.

### 2.1 Hybrid search over the vault
The architecture, in the order it should be built:

**Index.** Parse every note's frontmatter and body into rows: note name, layer, all taxonomy axes, and chunked prose. SQLite is the right home — it already holds the queue and it gives BM25 through FTS5 with no extra dependency.

**Lexical first.** FTS5 with BM25 answers the queries that matter most and vectors handle worst: *does anything here read Parquet*. Rare, specific tokens are exactly what embeddings blur.

**Vectors second.** Embed chunks with `nomic-embed-text`, already configured in LM Studio. At this scale — roughly one to two thousand chunks — brute-force cosine in numpy takes microseconds. **Do not add an ANN index.** `sqlite-vec` or DuckDB's VSS extension become worth it somewhere north of a hundred thousand chunks, and not before.

**Filters, not scores.** Licence class, deployment target and hardware footprint eliminate candidates rather than ranking them. A GPU-only tool is not a slightly worse answer on a laptop; it is not an answer. This is the axis the application records show mattering most.

**Fusion.** Combine lexical and vector rankings with Reciprocal Rank Fusion — robust, needs no score calibration, and each contributor stays inspectable.

**Explain every result.** Same discipline as the scout ranker: return why a result matched, not just that it did.

### 2.2 Integrity tests
Borrow dbt's idea — declarative assertions that fail the build:

- every wikilink resolves;
- no two resources share a `Bottom Line` or `What It Solves` block (the check that caught the original defect);
- every resource has a canonical URL and a licence class;
- every `container: true` note has an expansion status;
- no note references a topic key absent from the register.

### 2.3 Retrieval evaluation set
Twenty real questions with known-correct answers, drawn from the application records. *"What can I use to control RAG context without multiple databases?"* should return the donor front-end record. Without this you cannot tell whether a retrieval change helped.

---

## Phase 3 - Use

### 3.1 Finish the application layer
Four records exist. They need wiring in both directions: a resource note should show which applications cite it, and the `applied_in` count should feed retrieval as a proven-use signal. A resource with a recorded successful use should outrank a plausible stranger.

### 3.2 Agent access surface
Agents currently read Markdown. That works but is imprecise. An MCP server over the vault exposing `search`, `get_note`, `get_workflow`, `list_by_taxonomy` and `record_application` would make it a queryable service. `record_application` matters most: if writing a record is a tool call at the end of a task, records will accumulate; if it is a manual chore, they will not.

The `mcp-builder` skill and the existing MARK XLVIII MCP server are both prior art here.

### 3.3 More workflows
Four exist. The application records name the gaps directly: **Simulate A Physical System**, **Train Or Fine-Tune A Model**, **Deploy To Constrained Hardware**, **Self-Host A Service**. Write each only once its sequence has been walked, not speculatively.

### 3.4 Freshness
Resources go stale. A bulk refresh of activity signals plus a link-health check, on a schedule, with anything unreachable flagged rather than silently kept. `public-apis` does exactly this in CI and is the model.

---

## Phase 4 - Scale

Only after phase 2 passes.

**Container expansion**, starting with one aggregator as a proving run — manifest-first, so the graph is not swamped. **Scouting at volume** through the pipeline that already exists, one cohort at a time, checking the first cohort's output by hand before trusting the second. **The paper layer**, whose arXiv and Crossref adapter is still to be written.

**Domain register additions** the application records make necessary:

| Domain | Why |
| --- | --- |
| Promote `robotics_embedded` to tier 1 | Firmware, hardware interfaces, protocol and RF work is an active direction |
| Promote `datasets_benchmarks` to tier 1 | The mature phase of a simulation project needs data more than code |
| Add `quantitative_trading` | Market data, backtesting, risk, execution |
| Add `emulation_game_systems` | Models that orchestrate or play games; emulation |
| Add `efficient_inference` | Quantisation, distillation, constrained-hardware deployment |
| Add `distributed_compute` | Scheduling across mixed local and remote capacity |

---

## Sequencing

```
Phase 1  canvases + a clean build run          [days]
   |
Phase 2  hybrid search + integrity tests + eval set   ← the gate
   |
Phase 3  application wiring, MCP surface, workflows
   |
Phase 4  containers, scouting at volume, papers
```

Phases 3 and 4 can overlap. Phase 2 cannot be overlapped with phase 4: scouting into a catalogue whose retrieval is unproven produces volume that hides the problem instead of exposing it.

## The One Rule
Every phase is ordered by the same principle the workflow layer states: **use what is adequate now rather than waiting for what would be ideal later.** SQLite with FTS5 and brute-force cosine is adequate for a catalogue of this size and will remain so for a long time. A vector database, an ANN index and a bespoke UI are the steel framing — worth having when the frame is ready for them, and a way of not finishing if insisted on first.

## Related
- [[Library Assessment 2026-09]]
- [[Application Index]]
- [[Workflow Index]]
- [[Schema Extension - Scouting Pipeline]]
- [[Scouting Domains]]
