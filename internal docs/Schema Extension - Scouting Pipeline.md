---
type: "schema_spec"
status: "proposed"
version: "1.0"
depends_on: "[[Schema Extension - Containers and Papers]]"
host_platform: "MARK XLVIII (F:\\Mark-XLVIII-main)"
stages: ["discovered", "scouted", "ranked", "queued", "deep_dive", "catalogued", "rejected", "deferred"]
new_tables: ["scout_queue", "scout_cohort", "scout_signal"]
---

# Schema Extension - Scouting Pipeline

## Purpose
Grow the catalogue continuously without a human choosing every source, and without spending an expensive model on material that will not earn its place.

The pipeline separates three jobs that are usually conflated: **finding** a source, **judging** whether it is worth reading properly, and **reading** it. Finding is cheap and high-volume. Judging must be reproducible. Reading is expensive and should only ever happen in descending order of expected value.

## The Governing Principle
MARK XLVIII already states the rule this design depends on:

> Retrieved/web/worker content is untrusted evidence and cannot grant permission or expand workflow scope.

The scout is a worker producing untrusted evidence. It never decides what enters the catalogue. It observes, tags, and files. A deterministic evaluator ranks, and only ranked, cohort-frozen items are read properly. This keeps a 4B model's enthusiasm out of the encyclopaedia.

## Hardware Constraint That Shapes Everything
`config/runtime.json` sets `max_task_models_loaded: 1` against a GTX 1080 (8 GB) and RX 5500 XT (8 GB) under mixed-vendor Vulkan. One task model is resident at a time.

Therefore **stages batch; they do not interleave.** The scout model stays loaded and works the entire discovered backlog. Only then is it released and the research model loaded for deep dives. A per-item swap between a 4B scout and a 14B researcher would spend more wall-clock on model loading than on inference. `task_model_ttl_seconds: 300` and `warm_model_preference_enabled: true` already favour this shape — the pipeline must not fight them.

## Stage 0 - Domain Seeds
Themes and their seed queries live in [[Scouting Domains]], which is Markdown and therefore authoritative. The scout may not invent a domain; it may only report that a source fits none of them, which surfaces as a candidate new theme for human review.

## Stage 1 - Discovery (deterministic, no model)
Reuses `actions/web_search.py`, which already contains exactly the right primitives: `_github_repo_search`, `_expanded_open_source_queries`, `_open_source_research_results`, and `structured_web_search` with backend dedupe and `retrieved_at` stamping.

Sources of candidates, in order of yield:
1. GitHub search API against each domain's seed queries.
2. `structured_web_search` for non-GitHub material — docs sites, specifications, papers.
3. Container expansion per [[Schema Extension - Containers and Papers]] — already-catalogued awesome-lists are the densest vein available and cost nothing to mine.
4. Citation and reference sections of already-catalogued papers.

Output is a `scout_queue` row at state `discovered`. No model has run yet.

**Deduplication happens here, not later.** Exact match on `repo_key` or normalised URL, then near-duplicate detection using the embedding model already configured (`text-embedding-nomic-embed-text-v1.5`, `rag_embedding_url`). A candidate matching an existing resource does not become a new row — it increments that resource's corroboration count and adds a `listed_in` edge. This is the cheapest and most valuable signal the pipeline produces.

## Stage 2 - Scout (local worker model)
Model: the `worker` route — `qwen/qwen3-4b-2507`, 4096 context. Small, fast, resident for the whole batch.

Input per candidate is deliberately bounded: title, description, declared topics, language, and the first ~2 KB of README. Not the repository. The scout is answering *"what is this and where does it belong"*, not *"is this good"*.

Output is constrained JSON — `response_format: {"type": "json_schema"}`, which the patched LM Studio adapter now supports, so the model cannot append commentary after the object:

- `archetype` — library, framework, dataset, reference_list, specification, paper, tool, service
- `domain_key` — one of the approved domains, or `unmatched`
- `tags` — three to eight lowercase keywords
- `one_line` — a single factual sentence, no evaluation
- `sensitivity` — normal or review_required
- `confidence` — 0.0 to 1.0

Row advances to `scouted`. A scout failure is logged and the row stays `discovered` for retry; it never blocks the batch, and per the patched dispatcher it no longer disables the model for the remainder of the run.

## Stage 3 - Evaluator (deterministic, no model)
**The ranker is code, not a model.** A 4B model asked to score importance produces numbers that are neither reproducible across runs nor comparable between items — and a queue ordered by noise is worse than a queue ordered by arrival, because it looks principled. Every input below is already in hand by this stage.

Composite score, 0-100:

| Signal | Weight | Rationale |
| --- | --- | --- |
| Gap fit | 30 | Scores highest when the target topic has fewest approved resources. Coverage breadth is the catalogue's actual goal. |
| Corroboration | 20 | Independent curated lists or queries that surfaced it. Two or more is a strong consensus signal. |
| Vitality | 15 | `pushed_at` recency, not archived, not disabled. A dead repository teaches history, not practice. |
| Reusability | 15 | Licence class: Permissive 15, Weak_Copyleft 10, Copyleft 5, Unknown/Other 0. For a library about *integrating* solutions, licence is a ranking input, not a footnote. |
| Adoption | 10 | Log-scaled stars. Log-scaled deliberately: a 500-star geospatial library can matter more to a project than another 200k-star JS framework, and linear stars would bury it. |
| Depth signal | 10 | Presence of `docs/`, `papers/`, a specification, or a substantial README. Predicts whether a deep dive will actually yield material. |

Penalties and diversions:
- Duplicate of an existing resource: rejected, converted to a corroboration edge.
- `sensitivity: review_required`: diverted to the existing review queue, never ranked.
- Unreachable URL: `rejected`, recorded so it is not rediscovered every cycle.

Weights live in `config/runtime.json` so ranking can be retuned without touching code, and every score is stored with its component breakdown in `scout_signal` — a rank you cannot explain is a rank you cannot trust.

## Stage 4 - Cohort Gate
When rows at state `ranked` reach the threshold (default 100, `scout_cohort_size`), a cohort is frozen: rows are assigned a `cohort_id`, their rank order is snapshotted, and `Scout Cohort <id>.md` is written to the vault so the ordering is visible and challengeable before any expensive work begins.

Scouting continues into the next cohort while the current one is being consumed. The two stages are decoupled by the queue, which is the whole point of having one.

## Stage 5 - Deep Dive (descending rank, resumable)
Items are consumed **strictly in descending rank**, one at a time, under a lease. `model_generation_lease_seconds: 2400` already exists for this.

Per item: fetch README and documentation, run `core/repo_slicer.py` for ranked, deduplicated code structure rather than raw file text, then the existing chart, entity extraction, glossary resolution and metadata enrichment passes. Commit the note, update the indexes, mark `catalogued`.

Escalation policy — local first, escalate on evidence:
- Default: the `research` route (`qwen2.5-14b-deepresearch-i1`).
- Escalate to Claude or OpenAI when local confidence falls below threshold, when the item is in the top decile of its cohort, or when it is a paper (where a misread claim is worse than no entry).
- `planner_provider: openai` with a session-only key already governs this; the pipeline adds no new credential path.

**Resumability is the point of the ordering.** The cursor is a row state in SQLite, not a variable in memory. An interrupted session leaves every completed item `catalogued` and the remainder `queued`; the next run resumes at the highest-ranked incomplete item. Work is never repeated and the most valuable sources are always finished first.

## Table Definitions

```sql
CREATE TABLE IF NOT EXISTS scout_queue (
  id                INTEGER PRIMARY KEY,
  url               TEXT NOT NULL,
  url_hash          TEXT NOT NULL UNIQUE,
  repo_key          TEXT,
  title             TEXT,
  discovery_query   TEXT,
  discovery_backend TEXT,
  domain_key        TEXT,
  archetype         TEXT,
  tags              TEXT,
  one_line          TEXT,
  sensitivity       TEXT DEFAULT 'normal',
  scout_confidence  REAL,
  score             REAL,
  cohort_id         TEXT,
  state             TEXT NOT NULL DEFAULT 'discovered',
  attempts          INTEGER NOT NULL DEFAULT 0,
  last_error        TEXT,
  lease_owner       TEXT,
  lease_expires_at  TEXT,
  note_path         TEXT,
  discovered_at     TEXT NOT NULL,
  updated_at        TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_scout_state_score ON scout_queue(state, score DESC);
CREATE INDEX IF NOT EXISTS idx_scout_cohort ON scout_queue(cohort_id, score DESC);

CREATE TABLE IF NOT EXISTS scout_signal (
  queue_id   INTEGER NOT NULL REFERENCES scout_queue(id),
  signal     TEXT NOT NULL,
  value      REAL NOT NULL,
  weight     REAL NOT NULL,
  detail     TEXT,
  PRIMARY KEY (queue_id, signal)
);

CREATE TABLE IF NOT EXISTS scout_cohort (
  cohort_id   TEXT PRIMARY KEY,
  frozen_at   TEXT NOT NULL,
  size        INTEGER NOT NULL,
  consumed    INTEGER NOT NULL DEFAULT 0,
  note_path   TEXT
);
```

`attempts` with a cap prevents a permanently failing source from being retried forever. `lease_owner` and `lease_expires_at` let an abandoned lease be reclaimed rather than deadlocking the queue.

## Failure Modes This Design Accepts
- **Scout mislabels a domain.** Cost is one misfiled row, corrected at deep-dive time. Acceptable.
- **Ranking is wrong for a specific item.** Cohorts are visible before consumption and can be reordered by hand. The weights are configuration.
- **The catalogue becomes shallow and broad.** The genuine risk of automated scouting. Mitigated by gap fit being the largest weight — once a topic is well covered it stops attracting new work — and by the cohort note making breadth-versus-depth visible each cycle rather than after a thousand entries.

## Open Questions
- Should the deep dive re-rank within a cohort as facts arrive, or honour the frozen order? Frozen is simpler and auditable; re-ranking is more optimal and harder to trust.
- Does an `unmatched` domain accumulate until it justifies a new topic, and at what count?
- Should corroboration count across cohorts, so a source seen repeatedly over months eventually forces its way up?
