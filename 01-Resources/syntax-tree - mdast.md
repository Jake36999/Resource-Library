---
uuid: "21cb389e-87a9-52fc-974a-3b59d7c6ec6b"
canonical_url: "https://github.com/syntax-tree/mdast"
repo_key: "syntax-tree/mdast"
owner: "syntax-tree"
repo_name: "mdast"
aliases: ["syntax-tree/mdast", "https://github.com/syntax-tree/mdast"]
type: "specification"
primary_topic: "Code Intelligence & Structural Parsing"
secondary_topics: ["Architecture & Developer Playbooks"]
ecosystem: "Markdown"
domain_primary: "Code_Intelligence"
maturity_stage: "Production_Ready"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Markdown"
data_locality: "Stateless"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Lossless Syntax Tree"]
glossary_terms: ["Abstract Syntax Tree", "Schema", "Concrete Syntax Tree"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "CC-BY-4.0 (stated in readme; GitHub API reports no licence)"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-03"
evidence_count: 5
github_description: "Markdown Abstract Syntax Tree format"
github_language: "Unknown"
github_license_spdx: "Unknown"
github_default_branch: "main"
github_stars: 1473
github_topics: ["ast", "markdown", "syntax-tree", "unist"]
github_homepage: "https://unifiedjs.com"
github_pushed_at: "2026-02-04T18:45:51Z"
---
# syntax-tree - mdast

## Bottom Line
Not a parser — a written contract. One document defines the node types, fields and containment rules for representing Markdown as a tree, which is what lets hundreds of unrelated utilities in the unified ecosystem operate on each other's output.

## What It Solves
- Stop every Markdown tool inventing its own document shape and being unable to compose.
- Make a tree checkable rather than merely traversable, by saying which nodes may contain which.
- Give implementations in any language a common target, rather than one library's internals.

## Architecture & Mechanics
- Extends **unist**, a generic syntax-tree format, and inherits its utility ecosystem.
- Two abstract interfaces (`Literal`, `Parent`) and nineteen concrete nodes, written in a Web IDL-like grammar with a worked Markdown-to-tree example for each.
- Four mixins (`Alternative`, `Association`, `Reference`, `Resource`) carry fields shared across unrelated node types.
- The content model — `FlowContent`, `ListContent`, `PhrasingContent`, `Content` — is the load-bearing part: type unions that constrain which nodes may nest inside which.
- GFM, frontmatter and MDX node types are documented as extensions, explicitly outside the core.

## What Is Inside
- **One document, and it is the specification** — `readme.md`, 1,710 lines: 2 abstract
  interfaces, 19 concrete node types each with a worked Markdown-to-tree example, 4 mixins,
  1 enumeration, the content model as type unions, and documented extensions for GFM,
  frontmatter and MDX.
- **Nothing else executable** — `package.json` is `"private": true` at version `0.0.0` and
  exists only to run `remark` over the readme.
- **Not here:** any parser. Implementations live in the remark and unified ecosystems.

## Transferable Capability
**Write down the shape of a thing so independent implementations can interoperate without coordinating.** The load-bearing part is not the list of element kinds but the **containment rule** — which kinds may appear inside which — because that is what makes an instance *checkable* rather than merely traversable. Written as prose rather than shipped as a library, which is why implementations exist in languages its authors never touched.

**Alternative to:** one reference implementation that everyone must adopt, where the format is whatever that code happens to do; and to a schema listing fields without stating what may nest in what. **Applies wherever** several tools must operate on each other's output — and to any collection of documents whose structural rules are currently enforced by convention and pattern-matching rather than declared.

## Taxonomy
- Ecosystem: Markdown
- Domain Primary: Code_Intelligence
- Maturity Stage: Production_Ready
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Markdown
- Data Locality: Stateless
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Implement a Markdown tool in a language the unified ecosystem does not cover.
- Validate that a generated tree is well-formed against a written content model.
- Study how to specify a document format so independent implementations interoperate.

## Reading Notes
Licence, carefully: the GitHub API returns **no licence**. `package.json` says MIT but is `"private": true` at version `0.0.0` and exists only to run `remark` over the readme. The readme's own License section says **CC-BY-4.0 © Titus Wormer** — a content licence rather than an OSI software licence, which is the right kind for a document. Zero open issues and a slow commit rate are maturity signals here, not decay: a released specification that stops changing is working.

## Semantic Links
- [parent_topic:: [[Topic - Code Intelligence & Structural Parsing]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[tree-sitter - tree-sitter]]]
- [related_to:: [[Instagram - LibCST]]]
- [implements_pattern:: [[Pattern - Lossless Syntax Tree]]]
- [mentions_term:: [[Glossary - Abstract Syntax Tree]]]
- [mentions_term:: [[Glossary - Schema]]]
- [mentions_term:: [[Glossary - Concrete Syntax Tree]]]

## Evidence
- Source URL: https://github.com/syntax-tree/mdast
- Source kind: GitHub REST metadata plus the repository tree and files, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-03
- Depth of read: recorded per source in [[Scouting Working File 2026-09-03]]

## GitHub Snapshot

- Description: Markdown Abstract Syntax Tree format
- Language: Unknown
- License (SPDX): Unknown
- Default Branch: main
- Stars: 1473
- Homepage: https://unifiedjs.com
- Pushed At: 2026-02-04T18:45:51Z
- Topics: ast, markdown, syntax-tree, unist

## Evidence Anchors
- [github_repo] description :: Markdown Abstract Syntax Tree format (confidence 0.95)
- [github_repo] language :: Unknown (confidence 0.90)
- [github_repo] license :: Unknown (confidence 0.90)
- [github_repo] topics :: ast, markdown, syntax-tree, unist (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-03 (confidence 0.95)
