---
type: "reference"
status: "active"
purpose: "everything the implementation needs that does not live in this vault"
created: "2026-09-01"
audience: "an implementation session with only D:\\Resource-Library connected"
---

# External Dependencies Reference

## Why This Note Exists
An implementation session working in `D:\Resource-Library` cannot see `F:\Mark-XLVIII-main`, does not have the conversation this design came from, and cannot run commands on the host. Everything below was read from those systems directly and is transcribed here so the build does not have to guess.

**Verify before trusting.** These signatures were read on 2026-09-01. If the code has moved on, the code wins — but do not assume it has.

---

## 1. The ToolSet (`F:\Mark-XLVIII-main\ToolSet`)

The catalogue's deep dive **calls this**. It does not reimplement it. Ask for the folder to be connected before starting work that touches it.

### 1.1 Layout
```
ToolSet/
├── local_tool_assist_mcp/          the orchestration + policy layer
│   ├── workflow.py                 run_guided_repository_investigation()
│   ├── tool_registry.py            REGISTRY, ALLOWED_SCRIPT_NAMES, get_entry()
│   ├── policy.py                   PolicyError + check functions
│   ├── schemas.py                  session validation
│   ├── runner.py                   subprocess execution
│   ├── session.py                  session lifecycle, TOOLCHAIN_ROOT
│   ├── mcp_server.py               MCP surface, _dispatch_* functions
│   ├── compiler.py                 handoff report compilation
│   └── local_tool_assist_session.schema.json
├── aletheia_toolchain/             the scripts the registry may run
│   ├── create_file_map_v3.py       manifest scanner
│   ├── manifest_doctor.py          manifest validator
│   ├── semantic_slicer_v7.0.py     the slicer (83 KB)
│   ├── architecture_validator.py
│   ├── pipeline_gatekeeper.py
│   ├── tool_command_linter.py
│   ├── workspace_packager_v2.4.py
│   ├── notebook_packager_v3.1.py
│   └── semantic_project_config.schema.json
├── semantic_slicer_v6.0.py         older standalone slicer
├── create_file_map_v2.py           older standalone scanner
└── package_repo_mcp.py
```

### 1.2 The entry point
```python
# local_tool_assist_mcp/workflow.py
def run_guided_repository_investigation(
    objective: str,
    target_repo: str,
    profile: str = "default",      # "default" is mapped to "safe" internally
    allow_slice: bool = False,     # False stops at REVIEW_REQUIRED
    output_root: str = "",
    _registry=None,                # injection points for testing
    _toolchain_root=None,
) -> dict
```

Returns `{"status": ..., "session_id": ..., "events": [...], "artifacts": {...}}` where `status` is one of `complete`, `blocked`, `review_required`, `error`.

On `complete`, `artifacts` contains `final_markdown`, `final_python_bundle`, `archive_yaml`.

### 1.3 Event sequence
```python
GUIDED_STATUS_EVENTS = (
    "INTAKE_CREATED", "SCAN_COMPLETE",
    "MANIFEST_PASS", "MANIFEST_WARN", "MANIFEST_BLOCK",
    "REVIEW_REQUIRED", "SLICE_COMPLETE", "REPORT_COMPILED",
    "ARCHIVED", "ERROR",
)
```

Flow: create session → `scan_directory` → `validate_manifest` → **BLOCK aborts and archives** → if `allow_slice` is false, return `review_required` → `run_semantic_slice` → compile report → archive.

A `POLICY_BLOCK` status from the slice step also returns `review_required`, carrying a `policy` dict.

### 1.4 The closed registry
```python
@dataclass(frozen=True)
class ToolEntry:
    action: str
    canonical_tool_name: str = ""
    script_name: str = ""
    working_directory: str = "aletheia_toolchain"
    allowed_outputs: Sequence[str] = ()          # ("json", "md", "csv")
    exit_code_map: Mapping[int, str] = {}        # {0:"ok",1:"error",2:"usage_error"}
    io_requirements: Mapping[str, object] = {}
    write_permissions: Sequence[str] = ()        # ("session_dir/intermediate",)
    timeout_seconds: int = 60
    requires_review_approval: bool = False
    build_flags: Callable                        # (params, session_dir) -> List[str]
    collect_artifacts: Callable                  # (params, session_dir) -> dict
    primary_json_report_key: Optional[str] = None

ALLOWED_SCRIPT_NAMES: frozenset = frozenset(e.script_name for e in REGISTRY.values())
def get_entry(action_name: str) -> ToolEntry   # raises ValueError if unregistered
```

Thirteen registered actions. The four that matter here:

| Action | Script | Timeout | Approval | Required params |
| --- | --- | --- | --- | --- |
| `scan_directory` | `create_file_map_v3.py` | 120 s | no | `target_repo`, optional `profile` |
| `validate_manifest` | `manifest_doctor.py` | 60 s | no | `manifest_csv` |
| `run_semantic_slice` | `semantic_slicer_v7.0.py` | 300 s | **yes** | `manifest_csv`, `target_repo` |
| `lint_tool_command` | `tool_command_linter.py` | 30 s | no | `command` |

Others registered: `validate_architecture`, `gate_pipeline`, `audit_bundle_diff`, `package_workspace`, `package_notebook`, `watch_runtime_end`, `report_oom_forensics`, `correlate_runtime_slice`, `package_runtime`.

### 1.5 Artifacts each action produces
All under `session_dir / "intermediate"`:

| Action | Artifact keys |
| --- | --- |
| `scan_directory` | `manifest_csv` → `file_map.csv`, `manifest_health_json` → `file_map_health.json` |
| `validate_manifest` | `manifest_doctor_json` → `manifest_doctor.json`, `manifest_doctor_md` |
| `run_semantic_slice` | `slicer_json` → `semantic_slice.json` |

**`semantic_slice.json` is the deep dive's evidence and the workbench's working index.** Per the design it is ephemeral — used, then destroyed with the workbench.

### 1.6 Manifest columns
`create_file_map` writes: `root`, `rel_path`, `abs_path`, `ext`, `size`, `mtime_iso`, `sha1`.

Flags built by the registry: `--roots`, `--out`, `--health-report`, `--hash`, `--profile`.

### 1.7 Policy codes
```python
@dataclass(frozen=True)
class PolicyError(Exception):
    code: str
    message: str
    blocked: bool = True
    def to_result(self) -> dict: ...
```

| Code | Raised when |
| --- | --- |
| `NO_ARBITRARY_SHELL` | script not in `ALLOWED_SCRIPT_NAMES` |
| `SESSION_OWNED_READ_ONLY` | read outside the output root or session scope |
| `NO_TOOLCHAIN_READ` | read inside the toolchain itself |
| `NO_OUTPUTS_IN_TOOLCHAIN` | write inside the toolchain |
| `MANIFEST_REQUIRED` | slicing without a manifest |
| `DOCTOR_REQUIRED` | slicing without a doctor report |
| `DOCTOR_PASS_WARN_REQUIRED` | doctor status is not PASS or WARN |
| `REVIEW_APPROVAL_REQUIRED` | `review_state.slice_approved` is false and not dev mode |
| `REMOTE_MCP_AUTH_REQUIRED` | remote MCP without `LTA_MCP_AUTH_TOKEN` |
| `SECRET_IN_ARTIFACT` | api key / token / secret pattern found in artifact text |

Dev-mode escape hatch: `LTA_DEV_MODE=1`. **Do not use it in the catalogue's intake.**

### 1.8 The session invariant
`schemas.py` validates against `LocalToolAssistSession/v1.0` and enforces:

```
execution_mode.allow_command_execution  MUST be false
```

Required top-level keys: `schema_version`, `session_id`, `created_at`, `updated_at`, `request`, `execution_mode`, `review_state`, `policy`, `artifacts`, `steps`, `redaction`.

Required `review_state` keys: `scan_reviewed`, `manifest_reviewed`, `slice_approved`, `approved_by`, `approved_at`, `approval_notes`.

**This invariant is not to be relaxed.** The workbench is a separate subsystem with its own policy; the intake keeps this exactly as it is.

### 1.9 Config vocabulary already defined
`aletheia_toolchain/semantic_project_config.schema.json`, titled *Aletheia Semantic Project Config*, version 1.0:

`schema_version`, `project_identity`, `source_scope`, `profiles`, `architecture_expectations`, `risk_rules`, `runtime_dynamics`, `gates`, `plugins`.

Reuse these names where they fit rather than inventing parallel ones.

---

## 2. MARK XLVIII runtime (`F:\Mark-XLVIII-main\Mark-XLVIII-main`)

Relevant because it defines the model environment the catalogue shares.

### 2.1 Hardware, from `config/runtime.json`
```json
"lmstudio_host_profile": {
  "runtime": "llama.cpp Vulkan via LM Studio",
  "system_ram_gb": 31.93,
  "gpus": [
    {"name": "NVIDIA GeForce GTX 1080", "vram_gb": 8.08, "preferred_role": "primary"},
    {"name": "AMD Radeon RX 5500 XT",  "vram_gb": 7.98, "preferred_role": "secondary"}
  ],
  "mixed_vendor": true
}
```

### 2.2 The constraint that shapes the pipeline
```json
"max_task_models_loaded": 1,
"task_model_ttl_seconds": 300,
"warm_model_preference_enabled": true,
"model_generation_lease_seconds": 2400
```

**One resident task model.** Scouting and deep diving must run as separate batched passes, never interleaved per item. This is why the CLI has separate commands and why `cycle` deliberately stops before `dive`.

### 2.3 Model routes
```
worker     qwen/qwen3-4b-2507              ← the scout pass
research   qwen2.5-14b-deepresearch-i1     ← the deep dive
           marco-deepresearch-8b
embedding  text-embedding-nomic-embed-text-v1.5@q4_k_m
vision     qwen/qwen3-vl-4b
```

Endpoints: `http://localhost:1234/v1` (OpenAI-compatible), `http://localhost:1234/api/v1` (LM Studio native).

Context lengths are per-model in `lmstudio_model_load_profiles`; the 4B worker is configured at 4096, the 14B research model at 8192 with KV cache off-GPU.

### 2.4 Other reusable pieces
| Path | What it offers |
| --- | --- |
| `actions/web_search.py` | `structured_web_search()`, `_github_repo_search()`, `_expanded_open_source_queries()` — dedupe and `retrieved_at` already handled |
| `core/repo_slicer.py` | `slice_python_source()`, `dedupe_slices()`, `render_slices()`, `_CallCollector`. Note: closure is done by graphify (2A), not by building on these |
| `actions/dual_orchestrator.py` | `WorkflowRuntime`, `compile_workflow`, approval envelopes, `bounded_evidence_block(..., label="UNTRUSTED EVIDENCE")` |
| `actions/project_learning.py` | repository inventory and file selection weighting |
| `core/model_router.py` | OpenAI/local routing, fallback, provenance, model leases |

---

## 2A. graphify

Installed at `F:\uv-data\bin\graphify.exe`. Governed by section 4B of [[Design Specification]] — **two permitted uses, no others.**

### 2A.1 Invocation
```
graphify <query|explain|path> <question> [target_b] --graph <graph.json> [--budget N]
```
`MARK actions/graphify_query.py` wraps this. Config in `runtime.json`: `graphify_enabled`, `graphify_bin`, `graphify_timeout_seconds` (30).

### 2A.2 Output schema
NetworkX node-link JSON. The existing MARK graph, read 2026-09-01: **4,844 nodes, 11,133 edges.**

```jsonc
{
  "directed": true, "multigraph": false,
  "graph": {}, "hyperedges": [],
  "built_at_commit": "<40-char sha>",
  "nodes": [{
    "id": "actions_browser_control",       // stable slug
    "label": "browser_control.py",
    "norm_label": "browser_control.py",
    "file_type": "code",                   // code | rationale | document | concept
    "source_file": "actions/browser_control.py",
    "source_location": "L1",
    "_origin": "ast",
    "community": 15,                       // detected cluster id
    "community_name": "browser_control"
  }],
  "links": [{
    "source": "actions_browser_control",
    "target": "actions_browser_control_browser_control",
    "relation": "contains",
    "confidence": "EXTRACTED",             // EXTRACTED | INFERRED
    "confidence_score": 1.0,
    "weight": 1.0,
    "source_file": "actions/browser_control.py",
    "source_location": "L804",
    "_origin": "ast",
    "context": "..."                       // present on ~59% of edges
  }]
}
```

### 2A.3 Relations observed
`calls` 4496 · `contains` 1905 · `method` 1851 · `references` 1054 · `rationale_for` 577 · `imports` 571 · `imports_from` 220 · `uses` 218 · `indirect_call` 140 · `inherits` 60 · `extends` 39 · `re_exports` 2

`rationale_for` is a semantic edge, not a structural one — it links a rationale node to the code it explains. Node `file_type` spread: code 3986, rationale 577, document 242, concept 39. **It already ingests prose**, which is why the vault graph in 4B.1 is viable.

Confidence spread: `EXTRACTED` 10,701 · `INFERRED` 432.

### 2A.4 The centrality caveat — read before using any centrality
Top nodes by raw in-degree in the existing graph:

```
84  Any            83  Path             77  _cfg()
69  load_runtime_config()   66  resolve_config()   60  Path
```

These are type annotations and config loaders. **Raw centrality surfaces utility noise, not architecture.** The vault has the identical failure waiting: every resource note carries `taxonomy_hub:: [[Taxonomy Index]]`, and glossary notes are referenced by construction. Ruling `CENTRALITY_MUST_BE_FILTERED` (spec 4B.3) requires hubs, glossary notes and language builtins to be **excluded**, not down-weighted, before anything is computed.

### 2A.5 Not in scope
The user is separately exploring multi-level abstraction for graphify's node grading. That is their work on the MARK graph, **not** part of this catalogue. Do not anticipate it in this build.

### 2A.6 headroom
Evaluated and **not adopted** — it did not deliver what was claimed. The `remember_*` block in `runtime.json` is disabled. Ignore both; no adapter, no dependency, no fallback path.

---

## 3. Host and access facts

| Fact | Value |
| --- | --- |
| Host | `main-bedroom-pc`, Windows (win32 x64) |
| Vault | `D:\Resource-Library` |
| ToolSet | `F:\Mark-XLVIII-main\ToolSet` — connect the folder before using it |
| LM Studio | `http://127.0.0.1:1234/v1`, local server must be **started**, not merely installed |
| Docker | Installed; Desktop must be running |
| Python | 3.11+ on the host |

### 3.1 Credentials
Environment only. Never written to config, logs, notes or workflow payloads.

- `GITHUB_TOKEN` — raises the REST limit from 60/hr to 5000/hr. Without it, discovery stalls within two domains.
- `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` — only read when `scout.escalation_provider` is set.
- `LTA_MCP_AUTH_TOKEN`, `LTA_DEV_MODE` — ToolSet only.

### 3.2 Rate limits worth designing around
- GitHub REST: 60/hr unauthenticated, 5000/hr with a token.
- GitHub **search**: 10/min unauthenticated, 30/min authenticated — much tighter than REST. `discovery.discover_domain` already sleeps 2 s between queries.
- Search occasionally omits very large repositories from multi-`repo:` queries. Observed with `facebook/react` and `kamranahmedse/developer-roadmap`. Fall back to single-repo REST calls.

---

## 4. Verified licence facts

GitHub reports these as `NOASSERTION`; all three were read manually. They are recorded in `.utility/library_config.json` under `license_overrides`, and the build now prefers overrides over the API.

| Repository | Actual licence | Class |
| --- | --- | --- |
| `hashicorp/terraform` | Business Source License 1.1 | `Source_Available` |
| `getsentry/sentry` | Functional Source License (fair source) | `Source_Available` |
| `animate-css/animate.css` | Hippocratic License | `Source_Available` |

`Source_Available` means readable but restricted, and **not** OSI open source. It is distinct from `Unknown`, which means undetermined. `scout/rank.py` scores it 0.1 for reusability — below Copyleft, above Unknown.

## 5. Other verified facts worth not rediscovering

- `G-Research/siembol` was **archived on 3 April 2025** and is explicitly unmaintained.
- `openstack/openstack` is a **superproject of git submodules**, not OpenStack's source.
- `GSA/data.gov` is a coordination repository; the platform itself is several CKAN instances in other repositories.
- The `react` note carries `repo_key: react/react` because GitHub's API returned that `full_name` for the requested path. `fetch_github_metadata` now logs divergences to `.utility/logs/github_redirects.log`; let a live run settle it rather than editing by hand.

## Related
- [[Design Specification]]
- [[Implementation Brief]]
- [[Research - System Definition]]
