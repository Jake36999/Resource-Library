---
uuid: "077d5c12-81d6-5280-95db-9c76a1427d43"
canonical_url: "https://github.com/whitequark/ast"
repo_key: "whitequark/ast"
owner: "whitequark"
repo_name: "ast"
aliases: ["whitequark/ast", "https://github.com/whitequark/ast"]
type: "developer_tool"
primary_topic: "Code Intelligence & Structural Parsing"
secondary_topics: []
ecosystem: "Mixed"
domain_primary: "Code_Intelligence"
maturity_stage: "Production_Ready"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "CLI"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Lossless Syntax Tree", "Structural Code Search"]
glossary_terms: ["Abstract Syntax Tree", "Codemod"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 5
github_description: "A library for working with Abstract Syntax Trees."
github_language: "Ruby"
github_license_spdx: "MIT"
github_default_branch: "master"
github_stars: 210
github_pushed_at: "2025-03-19T18:48:50Z"
---
# whitequark - ast

## Bottom Line
Four Ruby files providing an immutable syntax-tree node and a processor that walks it — the substrate the Ruby parsing ecosystem is built on, deliberately containing no parser of its own.

## What It Solves
- Share one node representation across tools that would otherwise each invent their own.
- Transform a tree safely, by construction, because nodes cannot be mutated in place.
- Keep the tree abstraction independent of any particular language or parser.

## Architecture & Mechanics
- Immutability is the design decision everything else follows from: a node is never edited, only replaced. A transformation therefore returns a new tree and cannot corrupt the one it was given, which is what makes chained rewrites safe without defensive copying.
- Four files under `lib/ast/` constitute the whole library. There is no parser, no grammar and no language knowledge in it.
- The processor is a visitor: a tool declares handlers for the node types it cares about and inherits a correct traversal for everything else.
- **Not read:** any Ruby source. The immutability and visitor claims come from the library's stated purpose and its size, not from the code.

## What Is Inside
- **Four source files** — `lib/ast/` — and that is the library. 17 paths in the entire repository.
- **Two documentation files at the root** — `README.md` and `README.YARD.md`, plus `.yardopts`: the API documentation is generated, and its configuration is committed.
- **`CHANGELOG.md`** — for a library this small and this widely depended upon, the changelog is the interface contract.
- **Two spec files** — `spec/ast_spec.rb` and `spec/helper.rb`.
- **Not here:** a parser. `whitequark/parser`, the Ruby parser most tools actually use, is a separate project that depends on this one.

## Transferable Capability
**Publish the shared data structure as its own artefact, smaller than any of its users.** When several tools must exchange trees, the alternative is each defining a nearly-identical node and converting at every boundary. A four-file dependency that changes rarely is cheap for everyone to adopt and hard for anyone to fork, which is what makes an ecosystem converge. **Immutability is the second half**: making the node unmodifiable turns *did that transformation corrupt the tree* into a question that cannot be asked, at the cost of allocation.

**Alternative to:** a tree type bundled inside a parser, which forces every consumer to depend on the parser; and to hash or dictionary nodes, which impose no shape and so guarantee no compatibility. **Applies wherever** independent tools must pass a structure between them — document models, intermediate representations, event payloads, plugin interfaces.

## Taxonomy
- Ecosystem: Mixed
- Domain Primary: Code_Intelligence
- Maturity Stage: Production_Ready
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: CLI
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Adopt as the node type for any Ruby tool that will exchange trees with the wider ecosystem.
- Read it as the minimum viable interchange type before defining a bespoke node in another language.
- Compare with [[syntax-tree - mdast]], which makes the same *specify the shape, not the implementation* bet for Markdown.

## Reading Notes
Judge this by dependents, not by its own size or star count — the number that matters is how much of the Ruby analysis ecosystem is built on these four files, and that number is not in the repository. Last pushed 2025-03-19: alive, and changing rarely, which for an interchange type is the correct behaviour rather than neglect.

## Semantic Links
- [parent_topic:: [[Topic - Code Intelligence & Structural Parsing]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[syntax-tree - mdast]]]
- [related_to:: [[Instagram - LibCST]]]
- [related_to:: [[javaparser - javaparser]]]
- [related_to:: [[s-expressionists - Concrete-Syntax-Tree]]]
- [implements_pattern:: [[Pattern - Lossless Syntax Tree]]]
- [implements_pattern:: [[Pattern - Structural Code Search]]]
- [mentions_term:: [[Glossary - Abstract Syntax Tree]]]
- [mentions_term:: [[Glossary - Codemod]]]

## Evidence
- Source URL: https://github.com/whitequark/ast
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata, the complete file tree at HEAD, and the LICENSE.MIT file; no Ruby source was opened

## GitHub Snapshot

- Description: A library for working with Abstract Syntax Trees.
- Language: Ruby
- License (SPDX): MIT
- Default Branch: master
- Stars: 210
- Pushed At: 2025-03-19T18:48:50Z

## Evidence Anchors
- [github_repo] description :: A library for working with Abstract Syntax Trees. (confidence 0.95)
- [github_repo] language :: Ruby (confidence 0.90)
- [github_repo] license :: MIT (confidence 0.90)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 17 paths at HEAD (confidence 0.95)
