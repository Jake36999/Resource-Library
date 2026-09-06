---
uuid: "503e22ac-a195-5752-9b35-325f357bf5af"
canonical_url: "https://github.com/semgrep/mcp"
repo_key: "semgrep/mcp"
owner: "semgrep"
repo_name: "mcp"
aliases: ["semgrep/mcp", "https://github.com/semgrep/mcp"]
type: "agent_toolkit"
primary_topic: "Code Intelligence & Structural Parsing"
secondary_topics: ["Security & SIEM", "Agentic AI & Models"]
ecosystem: "Python"
domain_primary: "Code_Intelligence"
maturity_stage: "Abandoned"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "REST"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Security_Adjacent"
agent_surface: "Callable"
patterns: ["Structural Code Search", "Detection as Code"]
glossary_terms: ["Model Context Protocol", "Static Analysis", "Metavariable", "Detection Rule"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: "A MCP server for using Semgrep to scan code for security vulnerabilities."
github_language: "Python"
github_license_spdx: "MIT"
github_default_branch: "main"
github_stars: 685
github_topics: ["mcp", "semgrep"]
github_homepage: "https://mcp.semgrep.ai"
github_pushed_at: "2025-10-28T22:32:31Z"
---
# semgrep - mcp

## Bottom Line
A thin MCP server that exposes Semgrep's structural scanning to an agent — sixteen Python files whose whole job is turning an existing, well-tested analysis engine into something an agent can call.

## What It Solves
- Let an agent run a real static analysis pass instead of guessing at vulnerabilities from reading code.
- Reach an established rule corpus through an agent interface, without reimplementing any of it.
- Deploy that interface into a cluster, where an agent runtime already lives.

## Architecture & Mechanics
- The whole server is `src/semgrep_mcp/`, nine files. Semgrep does the work; this maps MCP calls onto it and returns results. The wrapper is deliberately thin, which is the design.
- Two transports ship as worked examples rather than as documentation: `examples/sse_client.py` and `examples/streamable_http_client.py`.
- Deployment is treated as part of the product: a `Dockerfile` at the root and a full Helm chart under `chart/semgrep-mcp/` (7 files — deployment, ingress, service, helpers).
- The one substantive unit test is `tests/unit/test_safe_join.py` — path joining, i.e. the traversal boundary. In a server that takes paths from a caller, that is the security-critical function, and it is the one with a dedicated test.
- **Not read:** any Python source. The thin-wrapper reading is from file counts and the repository's stated purpose.

## What Is Inside
- **A nine-file server** — `src/semgrep_mcp/`, and six workflows under `.github/workflows/`.
- **A production Helm chart** — `chart/semgrep-mcp/`: deployment, service, ingress, helpers and `Chart.yaml`. Unusual for a repository this size, and useful as a compact worked example of packaging an MCP server for a cluster.
- **Two transport clients** — `examples/sse_client.py`, `examples/streamable_http_client.py`: the same server reached two ways.
- **`tests/unit/test_safe_join.py`** — the path-traversal guard, tested by name.
- **Not here:** Semgrep, or any rule. Both are dependencies; see [[semgrep - semgrep]].

## Transferable Capability
**Expose an existing engine through a new protocol without absorbing it.** The wrapper stays small because it declines to own the hard part: sixteen files against an analysis engine of many thousands. The consequence worth naming is that the wrapper inherits the engine's correctness *and* its lifecycle — this repository is archived while Semgrep is not, and a wrapper is exactly the kind of component whose abandonment is invisible until the protocol moves. The second thing to take is the **shape of the packaging**: Dockerfile plus Helm chart plus two transport examples is a complete answer to *how would I actually run this*, in fewer files than most projects spend on the question.

**Alternative to:** reimplementing analysis inside an agent tool, which duplicates rules that already exist and ages badly; and to shelling out to a CLI and parsing its stdout, which works until the output format changes. **Applies wherever** a capable tool predates the interface people now want to reach it through.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Code_Intelligence
- Maturity Stage: Abandoned
- License Class: Permissive
- Deployment Target: Server
- Interface Protocol: REST
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Security_Adjacent
- Agent Surface: Callable

## Integration & Use Cases
- Read it as a minimal, complete template for wrapping an existing CLI as an MCP server, deployment included.
- Take the Helm chart as the shortest worked example of running an agent-callable service in a cluster.
- Give an agent a real scanning capability by pointing it at this rather than at pattern-matching prose.

## Reading Notes
**Archived, last pushed 2025-10-28.** Semgrep itself is active; this wrapper is not, and the gap matters more for a protocol adapter than for most components, because MCP is still moving. 685 stars indicate it was widely picked up before being retired — check whether an official successor exists before adopting. Also note `.gitmodules` at the root: part of what the repository refers to is not in it.

## Semantic Links
- [parent_topic:: [[Topic - Code Intelligence & Structural Parsing]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[semgrep - semgrep]]]
- [related_to:: [[jgravelle - jcodemunch-mcp]]]
- [related_to:: [[roomi-fields - rtfm]]]
- [implements_pattern:: [[Pattern - Structural Code Search]]]
- [implements_pattern:: [[Pattern - Detection as Code]]]
- [mentions_term:: [[Glossary - Model Context Protocol]]]
- [mentions_term:: [[Glossary - Static Analysis]]]
- [mentions_term:: [[Glossary - Metavariable]]]
- [mentions_term:: [[Glossary - Detection Rule]]]

## Evidence
- Source URL: https://github.com/semgrep/mcp
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; no Python source or chart template was opened

## GitHub Snapshot

- Description: A MCP server for using Semgrep to scan code for security vulnerabilities.
- Language: Python
- License (SPDX): MIT
- Default Branch: main
- Stars: 685
- Homepage: https://mcp.semgrep.ai
- Pushed At: 2025-10-28T22:32:31Z
- Topics: mcp, semgrep

## Evidence Anchors
- [github_repo] description :: A MCP server for using Semgrep to scan code for security vulnerabilities. (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: MIT (confidence 0.90)
- [github_repo] topics :: mcp, semgrep (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 49 paths at HEAD (confidence 0.95)
