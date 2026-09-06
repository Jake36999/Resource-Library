---
type: "design_spec"
status: "draft for approval"
stage: "2 of 2 - design"
version: "0.5"
created: "2026-09-01"
depends_on: "[[Research - System Definition]]"
scope: "architecture, policies, runtime dynamics, workbench, contracts and build order"
---

# Design Specification

## Scope Discipline
This is a **queryable reference with a supervised intake**. It identifies and locates solutions; it does not extract them. It is not an agent platform, not a search engine, not a package manager.

The boundary matters more than any other decision here. Extraction happens when a person opens a source, in a workbench, for one engagement. The system's job ends at *here is where to look and why* — and the only extraction it performs is the scouting needed to improve a source's description. Every section below is written to be the smallest thing that satisfies the target, because the failure mode for a tool like this is not being too simple — it is never being finished.

Where an existing tool does the job, this specification calls it rather than describing a replacement.

---

## 1. System Shape

```
                        ┌──────────────────────────┐
   Mode C (read)  ──────►      CONSULT SURFACE     │   fast · stateless · read-only
   person or agent      │  six typed query kinds   │
                        └───────────┬──────────────┘
                                    │ reads
                        ┌───────────▼──────────────┐
                        │        THE VAULT         │   markdown = truth
                        │  + derived search index  │   sqlite = derived
                        └───────────▲──────────────┘
                                    │ writes (gated)
                        ┌───────────┴──────────────┐
   Mode A (sweep) ──────►    INTAKE ORCHESTRATOR   │   slow · gated · resumable
   Mode B (directed) ───►   closed action registry │
                        └───────────┬──────────────┘
                                    │ calls, never reimplements
                        ┌───────────▼──────────────┐
                        │   EXISTING TOOLCHAIN     │
                        │ run_guided_repository_   │
                        │ investigation + slicer   │
                        └───────────┬──────────────┘
                                    │ provisions
                        ┌───────────▼──────────────┐
   Mode D (engage) ─────►       THE WORKBENCH      │   ephemeral · isolated
   user only            │  sandbox · runnable      │   execution permitted here
                        │  destroyed on close      │   and nowhere else
                        └──────────────────────────┘
```

Three properties follow from this shape and should be treated as invariants.

**Markdown is truth.** SQLite and any vector index are derived and disposable — rebuildable from the vault at any time. If they disagree with the notes, they are wrong.

**Reads and writes are separate subsystems** with separate budgets: reads optimise for latency, writes for correctness.

**The intake calls the toolchain.** It does not contain a second implementation of scanning or slicing.

---

## 2. Policies

Policies are code with named codes, following the pattern already established in `local_tool_assist_mcp/policy.py`. A refusal must say which rule refused and why.

### 2.1 Structural invariants
| Code | Rule |
| --- | --- |
| `READ_ONLY_CONSULT` | Mode C may not write to the vault. The single exception is appending an application record. |
| `EXECUTION_SANDBOX_ONLY` | Fetched source code runs only inside a workbench sandbox, only in Mode D, only when a person opened it. The intake keeps `allow_command_execution: false` unchanged. |
| `DOCUMENT_BEFORE_DESTROY` | A workbench cannot be closed until its application record exists. The value is extracted before the sandbox is discarded, or it is lost. |
| `CLOSED_ACTION_REGISTRY` | Only registered actions run. An unregistered name is an error, never an improvisation. |
| `NO_ARBITRARY_SHELL` | No component constructs a command line from model output. Models emit params; code builds commands. |
| `NO_SCHEMA_DRIFT` | Note schema, taxonomy axes and domain keys change only by editing their authoritative Markdown. No process may add a field. |
| `MARKDOWN_IS_TRUTH` | Derived stores are never authoritative. Any conflict resolves to the note. |
| `EVIDENCE_REQUIRED` | No factual field is written without a fetched source. "Unknown" is a valid value; a plausible guess is not. |
| `FAILURE_MUST_BE_LOUD` | An operation that can fail must be unable to fail silently. A check ships with a demonstration that it fires; a corpus-relative threshold ships with the distribution it was cut from; a result carries the fields its constraints acted on; a transformation that finds nothing to change says so. Thirty-five implementation defects were reviewed and the ones that survived days rather than minutes were, without exception, the ones that produced no signal. |
| `RUN_BEFORE_CLAIM` | A service is not listed in [[Service Map]] until it has produced a row, an answer, or a recorded refusal. Nine services were built, correct and never run; a specification satisfied is not a capability held. |
| `THRESHOLD_CARRIES_ITS_DISTRIBUTION` | Any constant derived from corpus statistics ships with the function that re-derives it. Two thresholds were correct when set and wrong within one intake. |
| `LOCATE_DO_NOT_ADJUDICATE` | The catalogue identifies and describes; the user decides what to do with a source. A property may lower a rank when it predicts *irrelevance*; it may never zero one because the system has assumed a use. Age, popularity and licence are facts to report. See the audit below. |
| `POSTURE_DECIDES_CONSEQUENCE` | A licence class is recorded as read, always. What it *costs* is read from `usage.distribution_posture`, not from the classifier. Under `private` every class permits donor, reference and tool use, because nothing built here is distributed; under `distributed` the strict reading returns. One config key, two behaviours, and the recorded facts identical under both. |
| `NO_PERSISTENT_SOURCE_GRAPH` | No graph of a catalogued source outlives the workbench that built it. |
| `GRAPH_IS_DERIVED` | Community assignments live in the index, never in note frontmatter. |
| `GRAPH_ADVISORY_ONLY` | A community is an observation. It may not create, rename or reassign a topic, domain or pattern. |
| `CENTRALITY_MUST_BE_FILTERED` | Hubs, glossary notes and language builtins are excluded before any centrality is computed. |

### 2.1a The adjudication audit

`LOCATE_DO_NOT_ADJUDICATE` was written on 2026-09-04 after the same defect was found three
times in one afternoon, each time as a **hard zero** under a double-digit weight. A zero is
not a low rank; it is invisibility, and it was being awarded for properties that only matter
under an assumption nobody had stated.

The assumption was that a source is a *building block* — something to be depended on — so
anything obstructing dependency makes it worthless. That describes a tool for selecting
microservices. It does not describe this catalogue, which is a reference guide: it locates
and describes prior work, a person reads it and decides, and the decision is theirs.

| Signal | Weight | Was | Adjudicating? | Now |
| --- | --- | --- | --- | --- |
| `reusability` | 15 | `Unknown` → 0.0 | **Yes** — assumed the user would only ever integrate and distribute | Scaled by `usage.distribution_posture`. Under `private`, a 15% spread that breaks ties and buries nothing |
| `vitality` | 15 | `archived` → 0.0 | **Yes** — its own docstring said *a dead repository teaches history, not practice*, and teaching history is the job | Scaled by `usage.catalogue_role`. Under `reference`, archived scores 0.55: settled is a virtue in something you intend to read |
| `adoption` | 10 | 0 stars → 0.0 | **Yes** — treated *nobody has found this* as a verdict, in a tool whose purpose is finding things nobody has found | Floor of 0.35 under `reference`; the log scale above it is unchanged |
| `corroboration` | 20 | 1 mention → 0.2 | Borderline — being cited by several sources is weak evidence, but it is evidence, and it never zeroes | Unchanged, and flagged here so the next reader can argue with it |
| `depth` | 10 | thin readme → low | No — how much material there is to read is directly relevant to a reference guide | Unchanged |
| `gap_fit` | 30 | saturated topic → low | No — a judgement about the *catalogue's* coverage, not about the source's worth | Unchanged |

Measured effect, scoring four real candidates under both roles: a popular, maintained,
permissively-licensed repository scores **identically** either way (57.2). An archived one
rises 19%, a zero-star one 7%, and a source penalised on all three axes at once —
[[hannesfrank - Course-Knowledge-Graphs]], from 2018, unstarred and unlicensed, and a
perfectly good graded fixture set — rises 106%. Nothing was made *better* than a strong
candidate; things stopped being invisible.

**The distinction that survives.** A constraint the user states is theirs and must eliminate:
`find_donor` with `hardware_footprint=CPU_Only` should return nothing else, and *we do not
know* is not an answer to *what runs on a laptop*. An unstated preference baked into a
ranking weight is the system's, and that is where the fallacy lives. The test is whether the
property predicts **irrelevance to the question asked**, or merely **unfitness for a use
nobody specified**.

This is a recurring failure mode rather than three bugs, and it will recur. Any new ranking
signal should be checked against the table above before it ships.

### 2.2 Intake gates
Mirroring the existing pipeline's gates, which are already proven:

| Gate | Blocks until |
| --- | --- |
| `MANIFEST_REQUIRED` | The source has been scanned into a manifest |
| `DOCTOR_PASS_WARN_REQUIRED` | Manifest validation returns PASS or WARN, never BLOCK |
| `REVIEW_APPROVAL_REQUIRED` | Expensive slicing is approved (auto-approved in Mode A within an approved cohort; explicit in Mode B) |
| `COHORT_FROZEN_REQUIRED` | No deep dive begins before its cohort is frozen and written to a visible note |
| `SENSITIVITY_REVIEW` | Dual-use material goes to the review queue and is never auto-approved |

### 2.3 The extension policy
The requirement was to discourage additions and stop agents building tools rather than using the system. Three rules, in force order:

1. **A new capability must enter the registry or it does not exist.** There is no side door. An agent that needs something the registry lacks reports that it is blocked; it does not write a script.
2. **Registry changes require the user.** A new `ToolEntry` is a user-approved change, not an agent decision.
3. **A blocked agent surfaces the gap, and that is the desired behaviour.** A `CLOSED_ACTION_REGISTRY` refusal naming the missing capability is a feature: it produces a decision point instead of a proliferation of one-off scripts.

The enforcement is the same as the existing toolchain's — the allowed set is a frozenset derived from the registry, so it cannot be extended at runtime.

---

## 3. The Consult Surface (Mode C)

Six query kinds, matching the six retrieval contexts. Each returns a different type. Implemented once as a Python module, exposed over MCP.

```
orient(topic|keywords)          → { topics[], resources[], aggregators[] }
find_donor(need, constraints)   → { candidates[] with licence, maturity, fit }
find_pattern(problem)           → { pattern, examples[], related_patterns[] }
find_technique(what, where?)    → { locations[]: source, path, symbol, excerpt }
find_data(subject, purpose)     → { datasets[], validation_criteria[] }
find_precedent(resource|topic)  → { application_records[] }
```

Plus two utilities: `get_note(name)` and `record_application(record)` — the one permitted write.

### 3.0 The retrieval cost ladder
Retrieval is tiered by what it costs to consult, and each tier narrows the set handed to the next. The system is not a place to find out *what everything is*; it is a place to find out *what is where*.

| Tier | Holds | Cost | Answers |
| --- | --- | --- | --- |
| 1. Index | Names, locators, tags, taxonomy values, access points | Cheap, wide | What is where |
| 2. Metadata | Structured fields, licence, activity, use counts | Low | Which of those are worth reading |
| 3. Notes | Prose descriptions, patterns, application records | Expensive, for person or agent | Which one to actually open |
| 4. The source | The code, the data, the paper | Highest — outside the system | The answer itself |

A query descends the ladder, and each tier must shrink the candidate set enough to justify the next. A retrieval design that hands a person twenty notes to read has failed at tier 2, not tier 3.

Tier 4 is deliberately outside the system. Reaching it means opening a workbench, and that is a person's decision.

### 3.1 Constraints are filters, not scores
`find_donor` takes constraints — licence class, deployment target, hardware footprint — and **eliminates** on them. A GPU-only tool is not a lower-ranked answer for a laptop; it is not an answer. This is the single most common way tool-recommendation systems produce confidently useless output.

### 3.2 Retrieval implementation
Ordered by build sequence, each stage usable before the next exists:

1. **Structured filters** over frontmatter. Serves R2 and much of R1 immediately, with no search machinery at all.
2. **FTS5 / BM25** over note text. Serves the specific-token queries embeddings handle worst.
3. **Vectors** with `nomic-embed-text`, brute-force cosine in numpy. At roughly 1–2k chunks this is microseconds. **No ANN index** until well past 100k chunks.
4. **Fusion** by Reciprocal Rank Fusion over the lexical and vector rankings.
5. **Graph** traversal for R3 — pattern links are already in the notes.

Every result carries its reason. A result that cannot explain itself is a result that cannot be trusted or tuned.

### 3.3 `find_technique` — a locator, not an extractor
This query returns **where to look**, not the technique itself.

```
find_technique("how is backpressure handled")
  → search descriptions, metadata, tags and application records
  → return candidate sources, each with the evidence that suggests it
  → say plainly: open a workbench to confirm
```

**A slice is a component of a source, not a source.** Keeping a permanent index of extracted symbols would build a library of decontextualised snippets — code fragments detached from the reason they existed, ageing independently of their origin, and competing with the source note for authority. That is a worse artefact than no index at all.

So slices are **ephemeral**. They are produced inside a workbench, used during the engagement, and destroyed with it. What survives an engagement is not the extract but the **improved description of the source**: the resource note gains what was learned, and the application record gains why it mattered. The finding upgrades the documentation rather than accumulating beside it.

The consequence for retrieval is that tier 1 and 2 do the narrowing, tier 3 confirms, and tier 4 — the source itself — supplies the actual technique. `find_technique` is honest about ending at tier 3.

### 3.4 Access points are the exception
One class of extract is a locator rather than content, and those **are** indexed permanently: API endpoints, data ports, service URLs, dataset download roots, authentication schemes and rate limits.

They qualify because they are addresses, not code. They answer *what is where* directly, they are small, they do not decay into decontextualised fragments, and they are exactly what a project needs when it matures from method-finding into data-gathering — the need identified in [[Application - Quantum Simulation Project]].

```
access_points:  source · kind · url · auth · rate_limit · formats · verified_at
```

Populated by the scouting pass from documentation, verified by reachability check, and refreshed on the freshness schedule. This is the one place the system holds something extracted from inside a source, and it is held because it is a pointer outward, not a copy inward.

---

## 4. The Intake Orchestrator (Modes A and B)

### 4.1 Shared pipeline
Both writing modes use one path. Mode B skips discovery.

```
Mode A: discover → scout → rank → freeze cohort → deep dive → publish
Mode B:            scout → rank → freeze cohort → deep dive → publish
                   └── ranking here orders the work, it does not select it
```

Most of this exists in `.utility/scout/`. The change this specification makes is to **Stage 5**: instead of the current single-model review, the deep dive delegates.

### 4.2 Deep dive, delegated
```python
result = run_guided_repository_investigation(
    objective=f"catalogue {repo_key} for {domain_key}",
    target_repo=local_clone_path,
    profile="safe",
    allow_slice=True,          # cohort approval satisfies the gate
)
```

Consume `semantic_slice.json` and the compiled report as the deep dive's evidence, then write the dossier. The slice is retained and indexed — it is what later serves `find_technique` for that source.

This replaces roughly the whole of the current `deep_dive.review()` with a call, and gains manifest validation, architecture checks, secret scanning and session archiving for free.

**Open question for approval:** the toolchain expects a local path, so cataloguing means a shallow clone. Disk cost is real; the alternative is a slice built from the GitHub tree API, which is weaker. Recommendation: shallow clone, slice, then delete the clone and keep the slice.

### 4.3 Search parameters as typed tool calls
Following the registry's `build_flags(params, session_dir)` pattern. A model produces params; code builds the command.

```json
{
  "$id": "catalogue/search_params/v1",
  "type": "object",
  "additionalProperties": false,
  "required": ["intent", "terms"],
  "properties": {
    "intent":   {"enum": ["orient","donor","pattern","technique","data","precedent"]},
    "terms":    {"type": "array", "items": {"type": "string"}, "minItems": 1, "maxItems": 8},
    "domain":   {"type": "string", "description": "must exist in the domain register"},
    "filters": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "license_class":     {"enum": ["Permissive","Weak_Copyleft","Copyleft","Source_Available","Unknown"]},
        "deployment_target": {"type": "string"},
        "hardware_footprint":{"type": "string"},
        "max_age_days":      {"type": "integer", "minimum": 1}
      }
    },
    "source":   {"type": "string", "description": "repo_key, for intent=technique"},
    "limit":    {"type": "integer", "minimum": 1, "maximum": 50, "default": 10}
  }
}
```

`additionalProperties: false` throughout, `domain` validated against the register, enums closed. The model's entire influence is one small typed object — it cannot widen its own permissions, and an invalid domain is a validation error rather than a silent miss.

---

## 4A. The Workbench (Mode D)

The decision is to clone rather than use the tree API, but not to keep the clones. A workbench is an **ephemeral sandbox** holding one source while a person actually engages with it, destroyed once the value has been written down. A hundred repositories are read; none are kept.

### 4A.1 Reconciling execution with the existing invariant
The toolchain enforces `execution_mode.allow_command_execution == false` as a schema invariant, and that must not be relaxed — it is what makes the intake safe to run unattended.

The resolution is that **the workbench is a separate subsystem with its own policy**, not a loosened intake. The intake never executes fetched code. The workbench does, under different rules: person-initiated only, isolated, ephemeral, and never reachable from Mode A or Mode C.

| | Intake (A/B) | Workbench (D) |
| --- | --- | --- |
| Runs fetched code | Never | Yes, sandboxed |
| Initiated by | Schedule or agent | A person, explicitly |
| Network | Fetch only | Off after clone, by default |
| Lifetime | Per source, seconds | Per engagement, hours |
| Survives | Notes and slices | Nothing but extracted artefacts |

### 4A.2 Lifecycle
```
workbench open <repo_key>
  → shallow clone into the sandbox        (depth 1, single branch)
  → scan_directory      → manifest
  → validate_manifest   → doctor; BLOCK aborts and destroys
  → run_semantic_slice  → symbol index
  → closure(target)     → what is actually required to run it
  → hand the person a live, runnable environment

   ... engagement: read, run, modify, test, extract ...

workbench document
  → write the application record (required)

workbench close
  → refuse unless a record exists         (DOCUMENT_BEFORE_DESTROY)
  → persist: slice index, closure manifest, dossier, application record,
             any excerpts the person marked as keep
  → destroy: clone, virtualenv, installed packages, caches, all runtime state
```

`close` is the command that clears the sandbox. Its refusal condition is the mechanism that makes application records accumulate: the record is not a chore to remember afterwards, it is the price of closing the workbench.

### 4A.3 Dependency closure
The point of running the slicer here is not only to find a technique but to answer *what else is needed for this to run*.

**Use graphify for this, not a bespoke implementation** — see section 4B.2. Its `calls`, `imports` and `contains` edges plus `path` queries are closure already, with confidence and community context. The steps below describe what closure must produce, not a second thing to write.

Closure over a target symbol:

1. Seed with the target — a function, class or module.
2. Follow intra-repository imports and calls transitively, recording each symbol reached.
3. Collect external requirements from `requirements.txt`, `pyproject.toml` or lockfiles, restricted to packages the reached symbols actually import.
4. Emit a **closure manifest**: the minimum file and dependency set that makes the target runnable.

This manifest is durable and is arguably the most valuable artefact the workbench produces. It is the difference between "this repository contains a good scheduler" and "these nine files and four packages are the scheduler, and here is how they connect" — which is exactly what makes a donor transplantable.

Closure is a static approximation. Dynamic imports, plugin registries and reflection defeat it, so the manifest records confidence and marks unresolved edges rather than pretending completeness. Running the code in the sandbox is how the gaps get found.

### 4A.4 Sandbox mechanics
Requirements, in priority order: filesystem isolation from the host, no host credentials, no network by default, resource limits, and single-command destruction.

**Recommendation: a container** (Docker or Podman). Isolation is adequate, `docker rm -f` *is* the clear command, and image layers make a clean state trivial to restore. On this host a WSL2 instance is the fallback; a bare virtualenv is not sufficient, since it isolates packages but not the filesystem.

Non-negotiable settings:

- No host mounts except the workbench directory itself.
- No environment variables inherited — no `GITHUB_TOKEN`, no API keys.
- Network disabled after the clone completes; re-enabled only on explicit request, and recorded in the session when it is.
- Memory and CPU capped, so a runaway process cannot take the machine down.
- Non-root inside the container.

### 4A.5 The risk, stated plainly
Executing code from repositories discovered by automated scouting is the highest-risk operation in this entire system. A scouted repository is untrusted by definition, and a malicious one runs with whatever the sandbox grants it.

Three controls follow, and they are the reason the mode is separated rather than folded into the intake:

1. **Never during a sweep.** Mode A is unattended, and unattended execution of unreviewed code is the failure this design exists to prevent. Workbenches are opened by a person.
2. **No credentials, ever.** The most valuable thing on the machine is the token set. The sandbox never sees it.
3. **Network off by default.** Exfiltration and dependency-confusion attacks both need egress. Requiring an explicit request per session makes it a decision rather than an assumption.

None of this makes running unknown code safe. It makes the blast radius a container that was going to be destroyed anyway.

### 4A.6 What persists
| Artefact | Kept | Why |
| --- | --- | --- |
| Improved source description | Yes | What was learned, written into the resource note |
| Application record | Yes, required | Why it mattered and what it replaced |
| Access points found | Yes | Addresses, not content — see 3.4 |
| Closure summary | Yes, as prose | "The scheduler is nine files and four dependencies" belongs in the note |
| Slice index | **No** | A component of a source, not a source. Ephemeral by design |
| Raw excerpts | **No** | Quote inside the note where the wording matters; do not stockpile |
| The clone | **No** | Recoverable from origin at any time |
| Virtualenv, packages, caches | **No** | Rebuildable |

The asymmetry is the whole idea. What is expensive to recreate is a person's understanding of what mattered — so that gets written into the description. Everything that is cheap to recreate, including the slice and the clone, is discarded.

The closure result is kept as **prose in the source note**, not as a queryable code index: "the scheduler isolates to nine files and four packages, entry point X" is a descriptor of the source. A stored dependency graph of its symbols would be a component library by another name.

---

## 4B. The Graph Layer (graphify)

`graphify` builds a typed, directed graph with community detection and per-edge confidence. It is already installed (`F:\uv-data\bin\graphify.exe`) and already produces a graph of the MARK platform. It has **two permitted uses here and no others.**

The rulings below are strict because this is the component most likely to expand past its remit. A graph tool invites you to graph everything, and graphing everything is precisely the mistake this catalogue has already decided against.

### 4B.1 Permitted use 1 — the vault graph (persistent, derived)
Community detection over **the catalogue's own note link graph**. The vault is already a graph: typed edges (`implements_pattern`, `mentions_term`, `parent_topic`, `related_to`, `applied_resource`, `listed_in`) across every layer. Nothing needs fetching; the data exists.

What it earns:

- **A measured alternative to `gap_fit`.** That signal currently reads a hand-maintained `resource_count` per topic. Community sizes show where the catalogue is *structurally* thin rather than where a topic was declared thin.
- **A principled backend for R3 pattern search**, replacing ad-hoc link walking.
- **Cross-topic clusters** — groupings nobody assigned, which are findings about the catalogue's real shape.

### 4B.2 Permitted use 2 — workbench mapping (ephemeral)
A graph of **one source, inside one workbench, for one engagement.** Community detection gives the repository's natural module boundaries rather than its directory layout; `graphify path A B` answers what connects two things; `rationale_for` edges carry the reasoning.

**This replaces `closure.py`.** The `calls`, `imports` and `contains` edges plus `path` queries already are dependency closure, with confidence scores and community context attached. Do not build a second closure implementation.

### 4B.3 The rulings

**R1 — `NO_PERSISTENT_SOURCE_GRAPH`.** No graph of any catalogued source may be stored beyond the workbench that produced it. Sixty-four sources at roughly five thousand nodes each is three hundred thousand nodes of other people's internals, ageing independently of their origins. That is the component library this design has already rejected, in graph form.

**R2 — `GRAPH_IS_DERIVED`.** The vault graph is a derived artefact in the disposable index. Deleting it must lose nothing. Community assignments are **never written into note frontmatter** — that would be schema drift, and it would let the graph start authoring the taxonomy.

**R3 — `GRAPH_ADVISORY_ONLY`.** A community is an observation, not a category. The graph may not create, rename, merge or reassign a topic, a domain key or a pattern. [[Scouting Domains]] remains the sole authority. Where communities and topics disagree, emit a **report for a person**; never an automatic change.

**R4 — `CENTRALITY_MUST_BE_FILTERED`.** Raw in-degree surfaces utility noise. In the existing MARK graph the top nodes are `Any`, `Path`, `_cfg()`, `load_runtime_config()` — type annotations and config loaders, not architecture.

The vault has the exact same failure waiting: every resource note links `taxonomy_hub:: [[Taxonomy Index]]`, so the hubs would dominate trivially. Therefore:

- Hub and index notes are **excluded from centrality**, not merely down-weighted.
- Glossary notes are excluded — they are referenced by construction, not by significance.
- For source graphs, language builtins and framework primitives are excluded by stoplist.
- Any centrality figure that reaches a ranking signal is log-dampened, as star counts already are.

**R5 — `GRAPH_VIA_REGISTRY`.** `graphify` is a subprocess and therefore enters the closed action registry as a registered action, with a bounded timeout, or it does not run. It is not exempt from `NO_ARBITRARY_SHELL` because it happens to be useful.

**R6 — Never on the read path.** Mode C must not invoke `graphify`. It is a subprocess with a multi-second cost; consult reads precomputed community assignments from the index and nothing more.

**R7 — Never during intake.** Modes A and B build no graphs. Scouting produces descriptions; graphs belong to engagement.

**R8 — Degrade, do not fail.** If `graphify` is absent, disabled or times out, the vault graph falls back to no communities and the workbench falls back to the slice. Nothing in the system may become dependent on its presence.

**R9 — Carry confidence through.** Edges are `EXTRACTED` or `INFERRED`. Anything derived from `INFERRED` edges must say so. An inferred relationship presented as an extracted one is exactly the laundering of uncertainty the catalogue exists to prevent.

**R10 — Pin what the graph described.** graphify records `built_at_commit`. Store it with any persisted graph, and for the vault graph store the index build stamp. A graph that cannot say what state it described is not evidence.

### 4B.4 What this changes in the build
| Was | Now |
| --- | --- |
| `closure.py` over `repo_slicer` primitives | Deleted — graphify path/edges do this |
| `gap_fit` from declared `resource_count` | Optional measured variant from community size, behind a config flag, compared before adoption |
| R3 pattern search by link walking | Community-aware traversal, same interface |

The `gap_fit` change is deliberately **not** automatic. Swapping a ranking signal's basis is exactly the kind of change that must be measured against the eval set before it is trusted.


---

## 5. Runtime Dynamics

Three profiles, following the vocabulary already in `semantic_project_config.schema.json`.

| | **consult** | **directed** | **sweep** | **workbench** |
| --- | --- | --- | --- | --- |
| Trigger | Query | User/agent list | Schedule or manual | Person, explicitly |
| Priority | Latency | Correctness, some latency | Correctness absolutely | Interactivity |
| Target | <30 s | Minutes per source | Hours per cohort | Open in <2 min |
| Model use | None, or one small call | Local research model | Local worker, then research | On request only |
| Writes | None (bar application records) | Full, gated | Full, gated | Sandbox only, then extract |
| Executes code | Never | Never | Never | Yes, isolated |
| Failure | Return partial + say so | Halt and report | Log, skip, continue | Surface to the person |
| Concurrency | Many | One | One | One or two |
| Resumable | N/A | Per source | Per source | Session survives until closed |

### 5.1 Why reads never invoke a model by default
A consult that calls a model inherits its latency and its capacity to invent. Structured filters plus lexical plus vector search over verified notes cannot fabricate a resource, because it can only return things that exist. Keep it that way; a model may summarise results afterwards, but must not stand between the query and the index.

### 5.2 Model batching
`max_task_models_loaded: 1` on this host. Stages batch and never interleave: the entire scout pass runs on the worker model, the model is released, then the deep-dive pass runs. Enforced by making them separate commands rather than a single orchestrated run.

### 5.3 Failure posture
Sweep is unattended, so it must never stop on a single bad source: log, mark, skip, continue. Directed has a person waiting, so it halts and reports. Consult degrades — a partial answer that says what is missing beats a spinner.

---

## 6. What Gets Built

Ordered so each step is useful before the next exists.

| # | Component | Depends on | Size |
| --- | --- | --- | --- |
| 1 | `index.py` — vault → SQLite rows + FTS5 | — | Small |
| 2 | `consult.py` — the six query functions, filters first | 1 | Medium |
| 3 | `integrity.py` — dbt-style assertions | 1 | Small |
| 4 | Embeddings + RRF fusion | 1, 2 | Small |
| 5 | `toolchain.py` — adapter to the existing pipeline | — | Small |
| 6 | Deep dive rewired to call it | 5 | Small |
| 7 | `access_points` extraction + index + reachability check | 1, 6 | Small |
| 8 | MCP server exposing consult + `record_application` | 2 | Small |
| 9 | Eval set of 20 questions with known answers | 2 | Small |
| 10 | `workbench.py` — open, document, close lifecycle | 5 | Medium |
| 11 | Container sandbox provisioning + teardown | 10 | Small |
| 12 | `graph.py` — vault community detection into the index | 1 | Small |
| 13 | graphify registered as an action; workbench mapping + closure summary | 10, 12 | Small |

Items 1–3 are worth doing regardless of everything else: they make the vault queryable and self-checking. Item 5 is the one that deletes code rather than adding it.

**Not building:** a UI, a graph database, an ANN index, a second orchestrator, a web crawler, or any component whose absence is not currently costing something.

---

## 7. Open Decisions

These need answers before build, and are genuinely open.

1. ~~Clone or tree API for slicing?~~ **Settled: clone into an ephemeral workbench** (section 4A). Shallow clone, slice, compute closure, engage, document, destroy. Nothing is kept on disk but the artefacts.
2. ~~How much of the slice is indexed?~~ **Settled: none of it.** A slice is a component of a source, not a source. Slices live and die inside a workbench; what persists is the improved description. The sole exception is access points (section 3.4), which are addresses rather than content.
3. **Does `record_application` need approval?** Recommendation: no, but mark records written by agents as `attested_by: agent` so they can be weighted differently.
4. **Where does the consult surface run?** In-process for local use, or as a persistent MCP server? Recommendation: a module first, MCP wrapper once the module is stable.
5. **What is the stopping rule for a sweep?** asreview's diminishing-returns criterion is the model. Needs a concrete threshold.

## 8. What Would Make This Fail

Stated so the failure modes are recognisable early.

- **Building the search before fixing the content.** Already avoided once; the rewrite came first.
- **Letting Mode C write.** The catalogue would reshape around whatever agents happened to be doing, plausibly at every step.
- **Reimplementing the toolchain** because calling it seemed awkward, producing two divergent pipelines.
- **Adding a vector database at this scale**, buying operational burden for latency that was never a problem.
- **Graphing everything.** A graph tool invites universal application. Two permitted uses, ruled in section 4B; anything else is scope creep wearing a useful hat.
- **Accumulating a snippet library.** Indexing extracted components would produce code fragments detached from their origin, ageing independently, competing with the source note for authority. Avoided by making slices ephemeral.
- **Letting a sweep open a workbench.** Unattended execution of unreviewed code is the one thing this design must never do.
- **Mounting credentials into a sandbox** for convenience, which converts a contained risk into an uncontained one.
- **Never finishing** because each component invites a more advanced version. Every item in section 6 has a defined stopping point; reaching it is the goal.

---

## 9. Component Contracts

Signatures are the interface. Implementations may differ; these shapes may not, because the tests and the MCP surface are written against them.

### 9.1 `index.py` — the derived store
```python
def build(vault_root: Path, db_path: Path, *, rebuild: bool = False) -> IndexStats
def refresh(vault_root: Path, db_path: Path, since: datetime) -> IndexStats
def chunks_for(note_name: str) -> list[Chunk]

@dataclass(frozen=True)
class IndexStats:
    notes: int; chunks: int; links: int
    duration_s: float; errors: list[str]

@dataclass(frozen=True)
class Chunk:
    note: str; layer: str; ordinal: int
    heading: str; text: str
```

Rules: rebuilding from empty must be idempotent; a note appears exactly once; deleting the database loses nothing, because Markdown is truth.

### 9.2 `consult.py` — the read surface
Every function returns the same envelope, so callers and the MCP layer handle one shape:

```python
@dataclass(frozen=True)
class Result:
    kind: str                 # resource | topic | pattern | application | dataset | access_point
    name: str                 # the note name, or the access point id
    why: str                  # REQUIRED - the reason this matched
    score: float              # 0..1, comparable only within one response
    fields: dict              # kind-specific payload

@dataclass(frozen=True)
class Response:
    intent: str               # orient | donor | pattern | technique | data | precedent
    results: list[Result]
    filtered_out: int         # how many candidates the hard filters eliminated
    tier_reached: int         # 1 index · 2 metadata · 3 notes
    next_step: str            # what the caller should do next, in plain language
    partial: bool = False     # true when something was unavailable
    notes: list[str] = ()     # what was unavailable, if anything
```

`why` is not optional and must not be generated by a model — it is assembled from which filters passed and which terms matched. `next_step` carries the cost ladder into the response: `find_technique` will often say *open a workbench on X to confirm*.

### 9.3 `integrity.py` — assertions
```python
@dataclass(frozen=True)
class Violation:
    check: str; note: str; detail: str
    severity: str             # error | warning

def run_all(vault_root: Path) -> list[Violation]
def run_check(name: str, vault_root: Path) -> list[Violation]
CHECKS: dict[str, Callable[[Path], list[Violation]]]
```

Exit non-zero on any `error`. Warnings do not fail a run but are reported.

### 9.4 `toolchain.py` — the adapter
```python
@dataclass(frozen=True)
class InvestigationResult:
    status: str               # complete | blocked | review_required | error
    session_id: str
    events: list[dict]
    slice_path: Path | None
    report_path: Path | None
    blocked_by: str | None    # MANIFEST_BLOCK | POLICY_BLOCK | None
    policy: dict | None

def investigate(repo_path: Path, objective: str, *,
                allow_slice: bool = False,
                profile: str = "safe") -> InvestigationResult

def toolchain_available() -> tuple[bool, str]
```

`blocked_by` must distinguish a failed manifest from a refused approval — they need different responses and a generic error hides that. `toolchain_available()` lets everything degrade cleanly when `F:\Mark-XLVIII-main` is not connected.

### 9.5 `workbench.py` — Mode D
```python
@dataclass(frozen=True)
class Workbench:
    id: str; repo_key: str; container: str
    path: Path; opened_at: str
    documented: bool

def open(repo_key: str, *, depth: int = 1) -> Workbench
def status(workbench_id: str) -> Workbench
def document(workbench_id: str, record: dict) -> Path
def close(workbench_id: str, *, force: bool = False) -> CloseResult

@dataclass(frozen=True)
class CloseResult:
    persisted: list[str]      # note updates, application record, access points
    destroyed: list[str]      # container, clone, caches
    refused: str | None       # DOCUMENT_BEFORE_DESTROY when undocumented
```

`close` without a record returns `refused="DOCUMENT_BEFORE_DESTROY"` and changes nothing. `force=True` exists for a genuinely abandoned engagement and must be logged with a reason.

**`open` must be unreachable from Mode A.** Enforce it in code, not by convention: the sweep entry point should not import this module.

### 9.6 `closure.py` — dependency closure
```python
@dataclass(frozen=True)
class Closure:
    target: str               # module, class or function
    files: list[str]          # intra-repo files reached
    packages: list[str]       # external requirements actually imported
    unresolved: list[str]     # dynamic imports, plugin lookups, reflection
    confidence: float         # 0..1, degraded by unresolved edges

def compute(slice_path: Path, target: str, repo_path: Path) -> Closure
def summarise(closure: Closure) -> str     # the prose that goes into the note
```

`summarise()` is what persists. The `Closure` object itself dies with the workbench — storing symbol graphs would be a component library by another name.

---

## 10. Data Contracts

### 10.1 Index tables
Derived, disposable, rebuildable. Separate database from `solutions_library.sqlite` so a rebuild cannot disturb the queue.

```sql
CREATE TABLE note (
  name          TEXT PRIMARY KEY,
  layer         TEXT NOT NULL,      -- resource | topic | pattern | glossary
                                    -- application | workflow | paper | index
  path          TEXT NOT NULL,
  type          TEXT,
  frontmatter   TEXT NOT NULL,      -- full JSON, for fields not promoted below
  body          TEXT NOT NULL,
  mtime         REAL NOT NULL,
  indexed_at    TEXT NOT NULL
);

-- promoted columns: the hard filters, which must be fast and exact
CREATE TABLE resource_facet (
  name                TEXT PRIMARY KEY REFERENCES note(name),
  repo_key            TEXT,
  canonical_url       TEXT,
  primary_topic       TEXT,
  domain_primary      TEXT,
  ecosystem           TEXT,
  maturity_stage      TEXT,
  license_class       TEXT,         -- Permissive | Weak_Copyleft | Copyleft
                                    -- Source_Available | Unknown
  deployment_target   TEXT,
  interface_protocol  TEXT,
  data_locality       TEXT,
  hardware_footprint  TEXT,
  security_compliance TEXT,
  is_container        INTEGER NOT NULL DEFAULT 0,
  pushed_at           TEXT,
  stars               INTEGER,
  application_count   INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX idx_facet_filters
  ON resource_facet(license_class, deployment_target, hardware_footprint);

CREATE TABLE link (
  src TEXT NOT NULL, dst TEXT NOT NULL,
  relation TEXT,                    -- implements_pattern | mentions_term
                                    -- applied_resource | parent_topic | ...
  PRIMARY KEY (src, dst, relation)
);
CREATE INDEX idx_link_dst ON link(dst);

CREATE TABLE chunk (
  id INTEGER PRIMARY KEY,
  note TEXT NOT NULL REFERENCES note(name),
  ordinal INTEGER NOT NULL,
  heading TEXT, text TEXT NOT NULL
);
CREATE VIRTUAL TABLE chunk_fts USING fts5(
  text, heading, note UNINDEXED, content='chunk', content_rowid='id'
);

CREATE TABLE embedding (
  chunk_id INTEGER PRIMARY KEY REFERENCES chunk(id),
  model TEXT NOT NULL,
  vector BLOB NOT NULL,             -- float32 little-endian
  dims INTEGER NOT NULL
);
```

### 10.2 Access points — the one persisted extract
```sql
CREATE TABLE access_point (
  id            TEXT PRIMARY KEY,   -- sha256(source + url)[:16]
  source        TEXT NOT NULL,      -- repo_key or note name
  kind          TEXT NOT NULL,      -- rest_api | graphql | dataset_download
                                    -- websocket | sparql | service_port | feed
  url           TEXT NOT NULL,
  auth          TEXT,               -- none | api_key | oauth2 | basic | unknown
  rate_limit    TEXT,
  formats       TEXT,               -- JSON array: json, csv, parquet, xml
  description   TEXT,
  verified_at   TEXT,
  reachable     INTEGER,            -- 1 ok · 0 failed · NULL never checked
  notes         TEXT
);
CREATE INDEX idx_access_source ON access_point(source);
CREATE INDEX idx_access_kind   ON access_point(kind);
```

These qualify for permanent storage because they are **addresses, not content** — pointers outward rather than copies inward. Everything else extracted from inside a source is ephemeral.

### 10.3 Search parameters
The typed object a model may produce, defined in §4.3. `additionalProperties: false` throughout, `domain` validated against [[Scouting Domains]], enums closed. A model's entire influence on retrieval is one small validated object.

### 10.4 Application record
Frontmatter contract for `09-Applications/`:

```yaml
type: "application_record"        # required
project: string                   # required
stage: string                     # required
resources_used: [string]          # required, may be empty
patterns_discovered: [string]
domains: [string]                 # must exist in the register
outcome: string                   # required
attested_by: "user" | "agent"     # required when written by a tool
date_range: string
```

Body must contain `What Was Needed`, `What Was Found And Taken`, `What It Replaced`, and `What The Catalogue Should Learn`. The last is the one that turns a diary entry into a requirement.

---

## 11. Testing Requirements

The existing 48 tests in `.utility/scout/tests/` are the model: behaviour is pinned by tests that state the decision in the assertion message.

**Required coverage for new components:**

| Component | Must prove |
| --- | --- |
| `index.py` | Rebuild is idempotent; every note indexed once; a deleted database loses nothing |
| `consult.py` | Hard filters eliminate rather than down-rank; every result has a `why`; unavailable subsystems produce `partial=True`, never an exception |
| `integrity.py` | A deliberately broken link fails exactly one check, naming the note |
| `toolchain.py` | Works with the toolchain absent; BLOCK and POLICY_BLOCK map to distinct outcomes |
| `workbench.py` | `close` refuses without a record; `open` is unreachable from the sweep path; teardown removes the container even when the engagement errored |
| `closure.py` | Unresolved dynamic imports lower confidence rather than being omitted silently |

**Everything external is faked in tests.** No test may require Docker, LM Studio, network access or the ToolSet. The existing `FakeLM` in `test_pipeline.py` is the pattern.

**One integration script**, separate from the test suite and not run in CI, exercises the real stack on the host. `preflight.py` is its first half.

---

## 12. Handover Map

| Question | Document |
| --- | --- |
| Where do I start? | [[Implementation Brief]] |
| What am I building and why? | This document |
| What are the APIs outside this folder? | [[External Dependencies Reference]] |
| Why is it shaped this way? | [[Research - System Definition]] |
| What is wrong with the catalogue today? | [[Library Assessment 2026-09]] |
| What order does the wider plan run in? | [[Finalisation Plan]] |
| How is a source ranked for intake? | [[Schema Extension - Scouting Pipeline]] |
| What must a note contain? | [[Note Content Model]] |
| What does a note owe its reader? | [[Source Documentation Standard]] |
| What are the domains and who may change them? | [[Scouting Domains]] |
| How should the result be used? | [[Workflow Index]] |
| What has the catalogue already been used for? | [[Application Index]] |

**Conflict rule:** this specification governs intent. The [[Implementation Brief]] governs sequence. Where either disagrees with working, tested code, the code is the current truth and the document is a defect to be fixed.

## Related
- [[Implementation Brief]]
- [[External Dependencies Reference]]
- [[Research - System Definition]]
- [[Finalisation Plan]]
- [[Schema Extension - Scouting Pipeline]]
- [[Note Content Model]]
- [[Source Documentation Standard]]
- [[Application Index]]
