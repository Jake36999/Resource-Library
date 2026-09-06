---
uuid: "df768ffc-b925-5566-8e5a-a1da88770971"
canonical_url: "https://github.com/shenhuan2021/gudu-sql-omni-introduce"
repo_key: "shenhuan2021/gudu-sql-omni-introduce"
owner: "shenhuan2021"
repo_name: "gudu-sql-omni-introduce"
aliases: ["shenhuan2021/gudu-sql-omni-introduce", "https://github.com/shenhuan2021/gudu-sql-omni-introduce"]
type: "vendor_content"
primary_topic: "Data Lineage & Provenance"
secondary_topics: ["Data APIs & Big Data", "Code Intelligence & Structural Parsing", "Curated Aggregators & Reference Lists"]
ecosystem: "Markdown"
domain_primary: "Discovery"
maturity_stage: "Abandoned"
license_class: "Unknown"
deployment_target: "Local_Only"
interface_protocol: "Markdown"
data_locality: "Stateless"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: []
glossary_terms: ["Data Lineage", "Abstract Syntax Tree", "Schema"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Unknown"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-03"
evidence_count: 5
github_description: "Gudu SQL Omni tutorials, SQL lineage analysis guides, column-level lineage examples, and VS Code plugin best practices for data engineers."
github_language: "Unknown"
github_license_spdx: "Unknown"
github_default_branch: "main"
github_stars: 2
github_topics: []
github_homepage: "Unknown"
github_pushed_at: "2026-05-03T02:28:33Z"
---
# shenhuan2021 - gudu-sql-omni-introduce

## Bottom Line
Thirteen marketing articles about a closed-source commercial VS Code extension, with no parser, no library and no code of any kind — catalogued as a negative result so the next search stops here.

## What It Solves
- Nothing executable. It promotes Gudu SQL Omni, a proprietary product from Gudusoft.
- One article does explain, clearly, how column-level lineage is derived in general — that description is the only transferable content.
- Recorded so that a search for open-source SQL lineage does not spend a second afternoon here.

## Architecture & Mechanics
- `README.md` is a landing page; `Topics` is a bare list of ten GitHub topic strings staged for the repository settings; `articles/` holds the content, with one article nested at `articles/articles/` — an assembled tree rather than a maintained one.
- The described product pipeline, which lives elsewhere: lexer and parser → abstract syntax tree → semantic analysis (column mapping plus function dependency) → lineage graph as JSON and visualisation.
- The product's claim is fully local parsing across 30+ SQL dialects with no upload — a real architectural position, about software this repository does not contain.

## What Is Inside
- **Thirteen marketing articles and nothing else** — `articles/`, on offline lineage parsing,
  VS Code plugin reviews, an Oracle-to-PostgreSQL migration guide, a DataHub sidecar, and
  governance workflow. One is nested at `articles/articles/`.
- **A staged topic list** — `Topics`, ten GitHub topic strings apparently waiting to be pasted
  into the repository settings.
- **The one piece of transferable content** —
  `articles/gudu-sql-omni-how-sql-lineage-works-offline-vscode.md` states the lineage pipeline
  in general terms: lexer and parser → AST → semantic analysis (column mapping plus function
  dependency) → lineage graph as JSON and visualisation.
- **Not here:** any parser, library, example project or code of any kind.

## Transferable Capability
**Derive dependency between fields by parsing the transformation rather than by observing the data.** Read the instruction that produced a value, resolve which inputs it drew on, and follow that transitively — so the question *what breaks if I change this* is answered from the definition rather than from a sample. Precise where the transformation is written down; blind to anything computed outside it.

**Alternative to:** inferring relationships statistically from values, which is cheap and approximate; and to hand-maintained documentation of what feeds what, which is accurate on the day it is written. **Applies wherever** derived artefacts are produced by written instructions — queries, build rules, note frontmatter derived from other notes, or any pipeline whose steps are declarative enough to read.

*The description of this method is all this source contains; the implementation is proprietary.*

## Taxonomy
- Ecosystem: Markdown
- Domain Primary: Discovery
- Maturity Stage: Abandoned
- License Class: Unknown
- Deployment Target: Local_Only
- Interface Protocol: Markdown
- Data Locality: Stateless
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Read one article for a plain statement of how column-level lineage is computed.
- Do not expect to install, run or read any implementation.
- Use as an example of a repository whose description and contents diverge completely.

## Reading Notes
The source list described this as “column-level SQL parsing and lineage from transformations”. It is not that. 2 stars, no licence, no detected language, created 2026-04-06 and last pushed 2026-05-03 — one month of activity, then silence. The README itself says “This repository is currently under construction” and closes with a `Keywords` block and a request for stars. A negative result, recorded as carefully as a positive one.

## Semantic Links
- [parent_topic:: [[Topic - Data Lineage & Provenance]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[open-metadata - OpenMetadata]]]
- [related_to:: [[semgrep - semgrep]]]
- [mentions_term:: [[Glossary - Data Lineage]]]
- [mentions_term:: [[Glossary - Abstract Syntax Tree]]]
- [mentions_term:: [[Glossary - Schema]]]

## Evidence
- Source URL: https://github.com/shenhuan2021/gudu-sql-omni-introduce
- Source kind: GitHub REST metadata plus the repository tree and files, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-03
- Depth of read: recorded per source in [[Scouting Working File 2026-09-03]]

## GitHub Snapshot

- Description: Gudu SQL Omni tutorials, SQL lineage analysis guides, column-level lineage examples, and VS Code plugin best practices for data engineers.
- Language: Unknown
- License (SPDX): Unknown
- Default Branch: main
- Stars: 2
- Homepage: Unknown
- Pushed At: 2026-05-03T02:28:33Z
- Topics: Unknown

## Evidence Anchors
- [github_repo] description :: Gudu SQL Omni tutorials, SQL lineage analysis guides, column-level lineage examples, and VS Code plugin best practices for data engineers. (confidence 0.95)
- [github_repo] language :: Unknown (confidence 0.90)
- [github_repo] license :: Unknown (confidence 0.90)
- [github_repo] topics :: Unknown (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-03 (confidence 0.95)
