---
type: "implementation_brief"
status: "active"
created: "2026-09-01"
audience: "an implementation session, working from this vault, without prior context"
authority: "[[Design Specification]] governs what and why; this note governs where to start"
---

# Implementation Brief

## Read This First
You are implementing a **queryable reference with a supervised intake** for the catalogue in `D:\Resource-Library`. It identifies and locates solutions; it does not extract them.

Three documents, in this order:

1. **This brief** — current state, order of work, traps.
2. **[[Design Specification]]** — the authority on what to build and why. Where this brief and the spec disagree, the spec wins.
3. **[[External Dependencies Reference]]** — the APIs, paths and environment facts that are not in this folder.

Two more give the reasoning if a decision seems arbitrary: [[Research - System Definition]] and [[Library Assessment 2026-09]].

## The One Sentence
Make the catalogue answerable: a person or agent with a problem should reach the right prior work in under thirty seconds, and the intake should be able to grow it unattended without making it worse.

---

## 1. Current State

### 1.1 The vault
| Layer | Contents |
| --- | --- |
| `00-Indexes/` | Master Index, Taxonomy Index, 11 topic indexes, specs, assessment, plans |
| `01-Resources/` | 62 resource notes |
| `02-Glossary/` | 76 terms + index |
| `03-Patterns/` | 28 patterns + index |
| `04-Reviews/` | 2 held resources + Review Queue |
| `05-Canvases/` | **Stale** — predates 23 resources and 13 patterns |
| `06-Papers/` | Index + template, no papers yet |
| `07-Scouting/` | Created on first cohort freeze |
| `08-Workflows/` | Index + 4 workflows |
| `09-Applications/` | Index + template + 4 records |

All 64 resource notes carry live GitHub metadata and prose written from fetched documentation. The 41 that were originally filled from topic templates have been rewritten — every `What It Solves` block is now distinct. Do not regress this.

### 1.2 What is already built in `.utility/`
```
.utility/
├── build_solutions_library.py     213 KB — generates the vault from the seed list
├── library_config.json            folders, lmstudio, github, scout, license_overrides
├── preflight.py                   environment check — run this first
├── adapters/lmstudio.py           patched client
├── prompts/                       scout, chart, catalog, entity, glossary, metadata
├── staging/github_repo_metadata.json    41 repos, correct values
└── scout/                         the intake pipeline, 48 passing tests
```

### 1.3 The scout package API
Working and tested. Build on it; do not replace it.

```python
scout.config    ScoutConfig.load() · DEFAULT_WEIGHTS · github_token() · escalation_key()
scout.db        STATES · connect() · init() · add_candidate() · update() · fetch_state()
                counts() · record_signals() · signals_for() · claim_next() · release()
                freeze_cohort() · active_cohort() · url_hash() · owner_token()
scout.rank      license_class() · gap_fit() · corroboration() · vitality() · reusability()
                adoption() · depth() · score_candidate() · explain() · Signal
scout.domains   Domain · parse() · load() · rotation() · resource_counts()
scout.discovery search_github() · probe_depth() · discover_domain() · container_notes()
                expand_container() · fetch_readme() · repo_key_from_url() · RateLimited
scout.scout_pass    build_prompt() · scout_row() · run_batch()
scout.evaluate  run() · enrich_depth() · freeze() · write_cohort_note()
                existing_catalogue_keys() · DOMAIN_TO_TOPIC
scout.deep_dive gather_evidence() · should_escalate() · review() · run() · publish()
scout.lm        client_for() · escalate() · LMUnavailable
scout.cli       status · discover · expand · scout · enrich · rank · freeze · dive
                publish · cycle
```

Run the tests before changing anything: `python -m pytest .utility\scout\tests -q` → 48 passing.

### 1.4 What does not exist yet
The consult surface, the index, integrity checks, the toolchain adapter, the workbench, access-point extraction. That is the work.

---

## 2. Traps

Each of these has already cost time. None is discoverable from the folder alone.

### 2.1 The build script can overwrite the rewritten notes
`build_solutions_library.py` regenerates notes from its database. The 41 rewritten notes were edited **directly**, so a build run may reinstate templated text.

**Before running it: back up `01-Resources/` and `04-Reviews/`, run, then diff.** If it clobbers them, fix the build to read the rewritten sections — do not stop running the build, and do not re-edit by hand.

### 2.2 The device shell has been unavailable
`device_bash` (the host's isolated Linux VM) failed to start throughout the design session. Docker and LM Studio could not be reached from the design side at all. If you also cannot reach them, that is the reason, and it is not a fault in this code. `preflight.py` distinguishes the cases.

### 2.3 Fixes that must not be reverted
These are deliberate. Reverting any of them reintroduces a diagnosed bug.

| File | Change | Why |
| --- | --- | --- |
| `build_solutions_library.py` | `load_github_metadata_cache` accepts both dataclass and raw API shapes | Only four field names differ between the shapes; a mismatch silently zeroed stars and licence while every sibling field survived |
| `build_solutions_library.py` | `parse_json_object` falls back to `raw_decode` | A model that emits an object then keeps talking produced `Extra data: line N` |
| `build_solutions_library.py` | `strip_json_fence` no longer truncates first-brace-to-last-brace | That truncation spanned two objects and made the error worse |
| `build_solutions_library.py` | `call_lmstudio_stage` disables the model only after 3 consecutive **transport** failures | Previously one timeout on the first repository silently disabled enrichment for the entire run |
| `build_solutions_library.py` | `license_override_for()` prefers config over the API | GitHub returns NOASSERTION for every source-available licence |
| `adapters/lmstudio.py` | timeout 45 → 300 s, warm-up 900 s | Model load alone exceeded the old budget; every historical failure was a timeout |
| `adapters/lmstudio.py` | `response_format` support | Constrained decoding is the durable fix for malformed JSON |
| `scout/rank.py` | `Source_Available` licence class | Distinguishes "restricted" from "undetermined" |

### 2.4 Stage batching is not optional
`max_task_models_loaded: 1` on this host. The scout pass and the deep dive must run as separate batched passes. `cycle` stops before `dive` deliberately. Do not "helpfully" merge them.

### 2.5 graphify is fenced deliberately
It has exactly two permitted uses (spec §4B) and eight rulings constraining them. The temptation is to graph every catalogued source; that rebuilds the component library the design rejected. If a third use seems necessary, raise it — do not add it.

### 2.6 Rate limits
GitHub **search** is 10/min unauthenticated and 30/min authenticated — far tighter than the 5000/hr REST limit. Discovery already sleeps 2 s between queries. Without `GITHUB_TOKEN` set, expect discovery to stall after roughly two domains.

---

## 3. Order Of Work

Each item is independently useful. Do not start the next until the current one's acceptance criteria pass.

### Step 1 — `index.py`
Parse every note into SQLite. Frontmatter into typed columns, prose into chunks, FTS5 over the chunks.

**Accept when:** a full rebuild from an empty database completes in under 30 s for the current vault; every note appears exactly once; rebuilding twice produces identical row counts; the index is deletable and regenerable with no data loss (Markdown is truth).

### Step 2 — `integrity.py`
Declarative assertions, in the spirit of dbt tests. Minimum set:

- every wikilink resolves to a note that exists;
- no two resources share a `Bottom Line` or a `What It Solves` block;
- every resource has `canonical_url` and `license_class`;
- every `container: true` note has an `expansion_status`;
- no note references a `topic_key` absent from [[Scouting Domains]] or the topic indexes;
- every frontmatter block parses.

**Accept when:** it runs clean against the current vault, and deliberately breaking a link makes exactly one assertion fail with a message naming the note and the link.

### Step 3 — `consult.py`, filters only
The six typed functions from spec §3, backed at first by structured filters and FTS5 alone. No embeddings yet.

```python
orient(topic_or_keywords, limit=10)            -> {topics, resources, aggregators}
find_donor(need, constraints, limit=10)        -> {candidates}
find_pattern(problem, limit=5)                 -> {pattern, examples, related}
find_technique(what, source=None, limit=10)    -> {candidates, where_to_look}
find_data(subject, purpose=None, limit=10)     -> {datasets, access_points}
find_precedent(resource_or_topic)              -> {application_records}
get_note(name)                                 -> {frontmatter, body}
record_application(record)                     -> {path}
```

Constraints **eliminate**; they never merely down-rank. Every result carries a `why`.

**Accept when:** the eval set (step 5) scores above 0.7 recall@5 using filters and lexical search alone, and `find_donor` with `license_class=Permissive` returns nothing non-permissive.

### Step 4 — embeddings and fusion
Embed chunks with `text-embedding-nomic-embed-text-v1.5` via LM Studio. Brute-force cosine in numpy. Fuse with Reciprocal Rank Fusion.

**No ANN index.** At 1–2k chunks brute force is microseconds; an index buys nothing and costs operational burden.

**Accept when:** eval recall improves over step 3 and no query exceeds 30 s cold.

### Step 5 — the eval set
Twenty questions with known-correct answers, drawn from the application records in `09-Applications/` and the workflows in `08-Workflows/`. Example: *"what can control RAG context without multiple databases?"* should surface [[Application - Donor Front End And RAG Context Control]].

Build this **alongside** step 3, not after. Without it you cannot tell whether step 4 helped.

**Accept when:** it runs as a single command and prints per-question hit/miss plus aggregate recall@5.

### Step 6 — `toolchain.py`
The adapter to `run_guided_repository_investigation`. See [[External Dependencies Reference]] §1.

**Accept when:** it returns a normalised result for a small local repository, surfaces every event, and maps `MANIFEST_BLOCK` and `POLICY_BLOCK` to distinct outcomes rather than a generic error. It must be exercisable with the toolchain absent (injection points exist: `_registry`, `_toolchain_root`).

### Step 7 — rewire the deep dive
Replace most of `deep_dive.review()` with a `toolchain.py` call. This **removes** code and gains manifest validation, architecture checks and secret scanning.

**Accept when:** the existing deep-dive tests still pass with the toolchain faked, and a real run produces a dossier whose evidence came from the slice rather than the README alone.

### Step 8 — access points
Extract API endpoints, data ports, auth schemes and rate limits during scouting. Index them permanently — they are addresses, not content, and the only extract the design keeps. Verify reachability on the freshness schedule.

**Accept when:** `find_data` returns access points with a `verified_at`, and an unreachable endpoint is flagged rather than silently dropped.

### Step 9 — `graph.py`, the vault graph
Community detection over the vault's own link graph, written into the derived index. Read the rulings in spec §4B before writing a line — this is the component most likely to expand past its remit.

**Accept when:** communities are computed and stored in the index only, never in note frontmatter; hub, index and glossary notes are excluded from centrality; deleting the index and rebuilding reproduces the same assignments; and graphify being absent degrades to no communities rather than an error.

**Do not** let it rename, merge or create a topic. Where communities and topics disagree, print a report.

### Step 10 — the workbench
Docker sandbox per spec §4A: `open`, `document`, `close`. `close` refuses without an application record (`DOCUMENT_BEFORE_DESTROY`).

Use graphify inside it for mapping and closure (spec §4B.2). **There is no `closure.py` to write.**

**Accept when:** a container runs with `--network none`, capped memory and CPU, no inherited environment; `preflight.py` confirms no egress; `close` refuses without a record and destroys everything on success; and **no code path lets Mode A open one**.

### Step 11 — MCP surface
Wrap `consult.py` plus `record_application`. Read-only except that one write.

**Accept when:** an agent can consult the catalogue and has no reachable tool that mutates it.

---

## 4. Standing Rules

**Markdown is truth.** SQLite and vectors are derived and disposable. Any conflict resolves to the note. Never write a fact into the index that is not in a note.

**Evidence or "unknown".** No factual field is written without a fetched source. A plausible guess is a defect.

**Closed registry.** New capability enters the registry or it does not exist. If you are blocked, say so and name the gap — do not write a side-door script. That refusal is the intended behaviour.

**Explain every result.** A rank or a match that cannot say why is one nobody can trust or tune. This is already the pattern in `rank.py`; keep it.

**Tests are the specification of behaviour.** The 48 existing tests encode decisions — that gap-fit can outweigh popularity, that a live lease is not stolen, that the scout cannot invent a domain key. If a change breaks one, understand the decision before changing the test.

**Reliability over speed on writes; speed on reads.** Different subsystems, different budgets.

---

## 5. Out Of Scope

Do not build, however tempting: a UI, a graph database, an ANN index, a web crawler, a second orchestrator, a package installer, a permanent index of code slices, or any component whose absence is not currently costing something.

The failure mode for this project is not being too simple. It is never being finished.

---

## 6. Definition Of Done

1. A query in each of the six retrieval contexts returns a usable answer in under 30 s.
2. Integrity checks pass against the whole vault.
3. A sweep runs unattended to completion and leaves the vault valid.
4. An interrupted sweep loses no completed work.
5. A third-party agent can consult but has no path to alter the catalogue.
6. A workbench opens, is documented, and closes clean — leaving an improved note and no clone.

## Related
- [[Design Specification]]
- [[External Dependencies Reference]]
- [[Research - System Definition]]
- [[Library Assessment 2026-09]]
- [[Finalisation Plan]]
