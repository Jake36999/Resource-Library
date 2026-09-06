---
uuid: "11a8ee47-e628-5f89-b688-73362f3300c6"
canonical_url: "https://github.com/semgrep/semgrep"
repo_key: "semgrep/semgrep"
owner: "semgrep"
repo_name: "semgrep"
aliases: ["semgrep/semgrep", "https://github.com/semgrep/semgrep"]
type: "developer_tool"
primary_topic: "Code Intelligence & Structural Parsing"
secondary_topics: ["Security & SIEM", "Architecture & Developer Playbooks"]
ecosystem: "Mixed"
domain_primary: "Code_Intelligence"
maturity_stage: "Production_Ready"
license_class: "Weak_Copyleft"
deployment_target: "Local_Only"
interface_protocol: "CLI"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Security_Adjacent"
agent_surface: "Callable"
patterns: ["Structural Code Search"]
glossary_terms: ["Structural Search", "Metavariable", "Static Analysis", "Taint Analysis", "Abstract Syntax Tree"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "LGPL-2.1"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-03"
evidence_count: 5
github_description: "Lightweight static analysis for many languages. Find bug variants with patterns that look like source code."
github_language: "OCaml"
github_license_spdx: "LGPL-2.1"
github_default_branch: "develop"
github_stars: 16500
github_topics: ["c", "go", "java", "javascript", "python", "r2c", "ruby", "sast", "semgrep", "static-analysis", "static-code-analysis", "typescript"]
github_homepage: "https://semgrep.dev"
github_pushed_at: "2026-09-01T19:51:53Z"
---
# semgrep - semgrep

## Bottom Line
Rules written in the syntax of the language being searched, with `$X` for any expression and `...` for any sequence, matched against a single generic AST that 37 languages are normalised into — so one pattern finds a construct regardless of formatting, and sometimes regardless of language.

## What It Solves
- Find every instance of a specific code shape across a polyglot codebase, without writing a regular expression nobody can review.
- Turn a security or style decision into an enforceable rule that runs in CI and in the editor.
- Track whether untrusted input can reach a dangerous call, within a function.

## Architecture & Mechanics
- `languages/` holds 37 language directories and `.gitmodules` declares 36 tree-sitter grammar submodules, all forked — the forks exist because the grammar must also parse patterns containing metavariables and ellipses.
- Everything normalises into `src/ast_generic`, one generic AST shared by all languages, which is what allows a rule to cross language boundaries.
- `src/matching` binds metavariables structurally; `src/il` is an intermediate language; `src/tainting` follows sources to sinks; `src/prefiltering` discards files that cannot match before the expensive work starts.
- `src/metachecking` validates rules themselves, `src/fixing` applies autofixes, and `src/spacegrep`/`aliengrep` degrade gracefully for languages with no grammar.

## What Is Inside
- **An OCaml engine** — `src/`, by subsystem: `ast_generic` (the single generic AST all
  languages normalise into), `matching`, `il` (intermediate language), `tainting` (source-to-sink
  dataflow), `prefiltering`, `fixing` (autofix), `sca` (dependency scanning), `metachecking`
  (rules that validate rules), `spacegrep` and `aliengrep` (degraded matching for languages with
  no grammar), `osemgrep` (an in-progress OCaml rewrite of the CLI).
- **37 language directories** — `languages/`, from `bash` to `terraform`, including
  `move_on_aptos`, `circom`, `promql`, `ql`.
- **36 forked tree-sitter grammars** — declared as submodules in `.gitmodules`, all under
  `returntocorp`/semgrep. Forked because a grammar must also parse patterns containing
  metavariables and ellipses.
- **A Python CLI** — `cli/src/semgrep/`, including `commands/mcp.py` and `commands/ci.py`.
- **Agent instructions** — `AGENTS.md` and `CLAUDE.md` at top level.
- **Not here:** the rule corpus. That is `semgrep/semgrep-rules`, a separate repository.

## Transferable Capability
**Search by the shape of a thing rather than by its characters, using a pattern written in the same form as what you are looking for, with holes that match anything and bind what they matched.** Formatting, naming and intervening material stop being obstacles. The deeper move is **normalising many different concrete forms into one common representation**, so a single question can be asked across all of them — bought at the cost of depth, which is why the harder analyses need more than the common form.

A third idea, small and easily missed: **rules that check rules**, so the pattern language validates its own patterns. The engine is also reachable as a callable interface for an automated consumer, so the same structural question can be asked by a person, by a build, or by an agent without three different integrations.

**Alternative to:** text search, which cannot express structure; and to bespoke analysis written per format, which does not compose. **Applies wherever** many instances share a shape you can describe but not enumerate — auditing, migration, conformance, or asking one question of a heterogeneous corpus.

## Taxonomy
- Ecosystem: Mixed
- Domain Primary: Code_Intelligence
- Maturity Stage: Production_Ready
- License Class: Weak_Copyleft
- Deployment Target: Local_Only
- Interface Protocol: CLI
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Security_Adjacent
- Agent Surface: Callable

## Integration & Use Cases
- Codify a review comment as a rule so it is never made by hand again.
- Audit a codebase for a known-bad pattern after a disclosure.
- Study how many concrete grammars are collapsed into one generic AST.

## Reading Notes
Two constraints stated in the repository itself. The licence is **LGPL-2.1** (`LICENSE`, confirmed by `COPYRIGHT`), so this is weak copyleft, not permissive. And the README says against its own interest that Community Edition "can only analyze code within the boundaries of a single function or file" — cross-file and cross-function analysis, dataflow reachability and the 20,000+ Pro rules are the commercial platform. The open engine is real; the capability that makes SAST accurate is not in it.

## Semantic Links
- [parent_topic:: [[Topic - Code Intelligence & Structural Parsing]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[tree-sitter - tree-sitter]]]
- [related_to:: [[SigmaHQ - sigma]]]
- [related_to:: [[Instagram - LibCST]]]
- [implements_pattern:: [[Pattern - Structural Code Search]]]
- [mentions_term:: [[Glossary - Structural Search]]]
- [mentions_term:: [[Glossary - Metavariable]]]
- [mentions_term:: [[Glossary - Static Analysis]]]
- [mentions_term:: [[Glossary - Taint Analysis]]]
- [mentions_term:: [[Glossary - Abstract Syntax Tree]]]

## Evidence
- Source URL: https://github.com/semgrep/semgrep
- Source kind: GitHub REST metadata plus the repository tree and files, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-03
- Depth of read: recorded per source in [[Scouting Working File 2026-09-03]]

## GitHub Snapshot

- Description: Lightweight static analysis for many languages. Find bug variants with patterns that look like source code.
- Language: OCaml
- License (SPDX): LGPL-2.1
- Default Branch: develop
- Stars: 16500
- Homepage: https://semgrep.dev
- Pushed At: 2026-09-01T19:51:53Z
- Topics: c, go, java, javascript, python, r2c, ruby, sast, semgrep, static-analysis, static-code-analysis, typescript

## Evidence Anchors
- [github_repo] description :: Lightweight static analysis for many languages. Find bug variants with patterns that look like source code. (confidence 0.95)
- [github_repo] language :: OCaml (confidence 0.90)
- [github_repo] license :: LGPL-2.1 (confidence 0.90)
- [github_repo] topics :: c, go, java, javascript, python, r2c, ruby, sast, semgrep, static-analysis, static-code-analysis, typescript (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-03 (confidence 0.95)
