---
type: "research"
status: "active"
stage: "1 of 2 - research"
created: "2026-09-01"
sequel: "[[Design Specification]]"
scope: "targets, retrieval contexts, operating modes, and what already exists"
---

# Research - System Definition

## Purpose Of This Document
Before the design specification, three questions need answering with evidence rather than assumption: **what is this for**, **when is it used and in what way**, and **what already exists that we should be calling instead of building**.

The third question is answered first, because it changes the shape of the other two.

---

## Part 1 - What Already Exists

The instruction was to avoid hubris and look at the existing tools before building. Doing so changes the plan substantially. The deep-dive machinery this catalogue needs is **already built, already gated, and already policed** in `F:\Mark-XLVIII-main\ToolSet`.

### 1.1 The repository investigation pipeline exists
`local_tool_assist_mcp/workflow.py` provides `run_guided_repository_investigation(objective, target_repo, profile, allow_slice)`, which emits a deterministic event sequence:

```
INTAKE_CREATED → SCAN_COMPLETE → MANIFEST_{PASS|WARN|BLOCK}
              → REVIEW_REQUIRED → SLICE_COMPLETE
              → REPORT_COMPILED → ARCHIVED
```

This is precisely the deep dive the catalogue's Stage 5 needs. It scans a repository into a manifest, validates the manifest, blocks on failure, requires approval before the expensive step, slices, compiles a report, and archives the session. **The catalogue should call this, not reimplement it.**

The supporting toolchain in `aletheia_toolchain/` is substantial and complete: `create_file_map_v3.py` (manifest), `manifest_doctor.py` (validation), `semantic_slicer_v7.0.py` (83 KB), `architecture_validator.py`, `pipeline_gatekeeper.py`, `tool_command_linter.py`.

### 1.2 The governance model asked for is already implemented
The requirement was: centralised orchestration, additions discouraged, agents must use the system rather than build new tools. That control already exists as code.

`tool_registry.py` defines a **closed registry** of thirteen actions. Each `ToolEntry` binds an action name to exactly one script, a working directory, allowed output types, a timeout, and a `requires_review_approval` flag. Critically:

```python
ALLOWED_SCRIPT_NAMES: frozenset = frozenset(e.script_name for e in REGISTRY.values())
```

An agent cannot run a script that is not registered. `policy.py` enforces the rest with named, machine-readable codes: `NO_ARBITRARY_SHELL`, `SESSION_OWNED_READ_ONLY`, `NO_TOOLCHAIN_READ`, `NO_OUTPUTS_IN_TOOLCHAIN`, `MANIFEST_REQUIRED`, `DOCTOR_PASS_WARN_REQUIRED`, `REVIEW_APPROVAL_REQUIRED`, `SECRET_IN_ARTIFACT`.

And `schemas.py` makes one invariant structural rather than procedural:

> `execution_mode.allow_command_execution` must be `false`

**This is the answer to "stop agents building tools instead of using the system", and it is already written.** The catalogue should adopt the same pattern rather than inventing a second governance model that would inevitably diverge from it.

### 1.3 The parameter-as-tool-call pattern already exists
The proposal was a JSON schema letting an inference model produce a search parameter as a tool call. `tool_registry.py` already does this:

```python
build_flags(params: dict, session_dir: Path) -> List[str]
```

A model produces a **params dictionary**, never a command line. The registry converts params to flags, validates required keys, and raises on anything missing. The model's output surface is a small typed object; the command line is constructed by code the model cannot influence.

`semantic_project_config.schema.json` already defines the configuration vocabulary too — `profiles`, `architecture_expectations`, `risk_rules`, `runtime_dynamics`, `gates`, `plugins`. The words used to describe the system's runtime behaviour already have schema definitions behind them.

### 1.4 What the catalogued sources contribute
Four of the resources already in this vault bear directly on the remaining design decisions.

| Source | What it settles |
| --- | --- |
| [[SigmaHQ - sigma]] | The abstract-rule pattern: one definition, a field-mapping layer, per-backend compilation. This is the model for a search parameter that must work across the vault, an AST slice and a web search without being rewritten three times. |
| [[asreview]] | Ranked review with a human oracle and a defensible stopping rule. Already reflected in the cohort design; its stopping-rule idea is not yet adopted and should be. |
| [[dbt-labs - dbt-core]] | Declarative tests that fail the build. The integrity check model for the vault. |
| [[public-apis - public-apis]] | Link-health validation in CI. The freshness model. |

### 1.5 Conclusion of Part 1
**Build almost nothing new.** The remaining work is an adapter between the catalogue and an existing gated toolchain, plus a retrieval layer the toolchain does not provide. That is a much smaller system than the one implied before this research.

---

## Part 2 - Retrieval Contexts

The observation driving this section: a user opening the catalogue at the start of a project needs something entirely different from a user hunting a technique buried inside one file of one repository. A single ranked list serves neither well.

Six contexts, each returning a **different unit of answer**. This is the core finding: the tool does not vary only its ranking, it varies **what it hands back**.

### R1 - Orientation
*"I am starting something in this area. What exists?"*
**Returns: a set.** Breadth beats precision; the user does not yet know the right vocabulary, so exact matching fails. Served by topic indexes, aggregator entries and the taxonomy. Recall matters, ranking barely does.

### R2 - Donor search
*"I need a component I can transplant into my project."*
**Returns: a repository.** The deciding factors are licence class, self-containment, maturity and how cleanly it separates from its context — not features. Hard filters dominate. This is the context behind [[Application - Donor Front End And RAG Context Control]], and the catalogue currently records no donation-suitability signal at all.

### R3 - Pattern search
*"How do people structure a solution to this?"*
**Returns: a pattern, with examples.** The answer is not one source — it is the shape several sources share. Served by the pattern layer, which exists precisely because this context does. Answering with a repository list is a failure mode here.

### R4 - Technique search
*"How is this actually done, in code?"*
**Returns: a location inside a source** — `path/file.py::Class.method`, or a passage in a document. The repository is not the answer; the answer is a fragment of it.

**Corrected during design.** The catalogue answers this by naming *where to look* — candidate sources with the evidence that suggests them — not by returning the code. Slices are produced in a workbench, used, and destroyed; what persists is the improved description of the source. A permanent index of extracted symbols would be a library of decontextualised snippets, which is a worse artefact than none. See sections 3.3 and 3.4 of [[Design Specification]].

### R5 - Data and validation search
*"What datasets exist, and what signals indicate correct behaviour?"*
**Returns: a dataset, plus validation criteria.** Identified in [[Application - Quantum Simulation Project]] as the need that appears when a project matures past method-finding. Poorly served today: datasets are a reserve domain and validation criteria are not modelled at all.

### R6 - Precedent search
*"Has this been used here before, and did it work?"*
**Returns: an application record.** Cheapest to serve, highest confidence, and only possible because the application layer now exists.

### Why this matters for design
Each context implies a different retrieval strategy:

| Context | Strategy | Unit |
| --- | --- | --- |
| R1 Orientation | Taxonomy traversal, low precision | Set of resources |
| R2 Donor | Hard filters first, then rank | Repository |
| R3 Pattern | Graph query over pattern links | Pattern + examples |
| R4 Technique | Descriptions, tags, use records | Candidate sources + where to look |
| R5 Data | Filtered search over dataset entries | Dataset + criteria |
| R6 Precedent | Direct lookup | Application record |

A single `search()` returning a ranked list of notes serves R1, R3 and R6 adequately, R2 poorly, and R4 and R5 not at all. **The retrieval interface must be typed by context.**

---

## Part 3 - Operating Modes

The end-state is an updating static tool. Four modes; two write to the catalogue, one runs code, one only reads.

### Mode A - Sweep (write)
Keyword-driven discovery: search using identifiable terms to find relevant, similar or supporting sources, rank them, and work the queue.

Autonomous, unattended, **reliability over speed**. It runs slowly on purpose. A sweep that takes six hours and never corrupts the catalogue is worth more than one that takes twenty minutes and occasionally writes a malformed note, because the second requires supervision and therefore is not really autonomous at all.

### Mode B - Directed intake (write)
A user or agent supplies a list of sources to add. Same pipeline, discovery skipped, ranking used only to order the work.

Latency matters slightly more here — someone is usually waiting — but correctness still wins. The mode exists because the most valuable sources are often ones a person already knows about.

### Mode D - Workbench (engage)
Added during design, not present in the original three-mode framing. A person opens one source in an ephemeral sandbox, works with it — including running it — extracts what matters, documents the application, and destroys the sandbox.

It exists because Mode C answers *what exists* but cannot answer *does this actually work and what does it take to run*. That question needs execution, and execution needs isolation. See section 4A of [[Design Specification]].

### Mode C - Consult (read only)
Everything else. A third party — person or agent — working on their own project, looking for relevant material.

**One-way.** Mode C cannot add sources, change schemas, alter rankings or extend the taxonomy. Its single permitted write is appending an application record, which adds evidence without changing structure.

This restriction is the load-bearing one. A consulting agent that can write to the catalogue will, over time, reshape it around whatever it happened to be doing — and the reshaping will look reasonable at each step.

### Distribution of use
Modes A and B are rare and deliberate. Mode C is the overwhelming majority of all use. The system should therefore be optimised for Mode C being fast, safe and stateless, with A and B as slow, gated, supervised operations.

---

## Part 4 - Targets

What this system is for, stated so success is checkable.

**Primary.** Reduce the time between "I need to solve X" and "here is proven prior work on X", from hours of searching to minutes of querying.

**Secondary.** Preserve the reasoning behind past choices, so a decision made once is not re-litigated from memory.

**Tertiary.** Make prior art reachable by agents as reliably as by people, so an agent building something can consult precedent rather than inventing from its own priors.

### Explicit non-targets
Naming these prevents scope creep, which is the main risk to a tool of this kind.

- **Not a search engine for the open web.** It indexes what has been catalogued, deliberately.
- **Not a package manager.** It says what exists and whether it fits; it does not install.
- **Not a documentation host.** It points at sources; it does not mirror them.
- **Not a general agent platform.** It is a queryable reference with a supervised intake.
- **Not real-time.** Freshness is measured in days. Anything needing live data should query the source.

### Success criteria
1. A Mode C query in one of the six contexts returns a usable answer in under thirty seconds.
2. A Mode A sweep runs unattended to completion and leaves the catalogue valid by every integrity check.
3. An interrupted sweep loses no completed work.
4. A third-party agent can consult the catalogue without any ability to alter it.
5. Application records accumulate without being chased, because recording one is a single tool call.

---

## Findings Carried Into Design

1. **Call the existing toolchain.** `run_guided_repository_investigation` is the deep dive. Do not write a second one.
2. **Copy the existing governance pattern.** Closed action registry, named policy codes, params-not-commands, `allow_command_execution: false`.
3. **Type the retrieval interface by context.** Six contexts, six return types. Not one ranked list.
4. **R4 is the differentiator and needs the slicer.** Everything else can be served from note text and metadata.
5. **Mode C is the common case and must be read-only.** Optimise for it; gate the others heavily.
8. **Execution belongs in a separate, person-initiated sandbox** — never in the intake, never unattended.
6. **Reliability over speed on writes; speed on reads.** These are different subsystems with different budgets.
7. **Adopt asreview's stopping rule.** A sweep should be able to conclude that further scouting in a domain is unlikely to add value, and stop.

## Related
- [[Design Specification]]
- [[Finalisation Plan]]
- [[Library Assessment 2026-09]]
- [[Application Index]]
