---
uuid: "599052cb-b43e-5760-a03f-6bd2cda6ab9f"
canonical_url: "https://github.com/MazzaWill/neo4j-python-pandas-py2neo-v3"
repo_key: "MazzaWill/neo4j-python-pandas-py2neo-v3"
owner: "MazzaWill"
repo_name: "neo4j-python-pandas-py2neo-v3"
aliases: ["MazzaWill/neo4j-python-pandas-py2neo-v3", "https://github.com/MazzaWill/neo4j-python-pandas-py2neo-v3"]
type: "tutorial"
primary_topic: "Knowledge Management"
secondary_topics: ["Data APIs & Big Data", "Agentic AI & Models"]
ecosystem: "Python"
domain_primary: "Knowledge_Management"
maturity_stage: "Active"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "Python_SDK"
data_locality: "Distributed"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "Procedural"
patterns: ["Knowledge Graph Routing", "Schema Mapping", "Agent Skill Packaging", "ETL API Ingestion"]
glossary_terms: ["Knowledge Graph", "Retrieval-Augmented Generation", "Schema", "Skill"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: "Excel-to-Neo4j knowledge graph examples: legacy py2neo v3 plus modern Neo4j GraphRAG/vector search."
github_language: "Python"
github_license_spdx: "MIT"
github_default_branch: "master"
github_stars: 579
github_topics: ["ai-agents", "codex-skill", "excel", "graphrag", "knowledge-graph", "neo4j", "pandas", "py2neo", "python"]
github_pushed_at: "2026-09-01T21:06:02Z"
---
# MazzaWill - neo4j-python-pandas-py2neo-v3

## Bottom Line
A spreadsheet-to-knowledge-graph worked example that has been kept alive across a decade of tooling change — the original 2018 py2neo pipeline sits next to a modern Neo4j GraphRAG version, and the method is packaged as an agent skill.

## What It Solves
- Turn a business spreadsheet into a graph without designing the model from scratch.
- See the same modelling problem solved with two generations of tooling.
- Give an agent a runnable procedure for building a graph from tabular data.

## Architecture & Mechanics
- Two implementations of one problem coexist deliberately: the legacy path (`dataToNeo4jClass/`, `invoice_neo4j.py`, `neo4j_matrix.py`, `neo4j_to_dataframe.py`) and `examples/modern_invoice_graphrag/` (11 files) with vector search and GraphRAG.
- The modern example is the tested one — `tests/modern_invoice_graphrag/` covers `test_app`, `test_cypher`, `test_embeddings`, `test_model` — so the four things that can go wrong are named and separated.
- The method is also packaged as an agent skill: `skills/neo4j-knowledge-graph/` with `SKILL.md`, `references/modeling.md`, `references/cypher-and-graphrag.md`, `scripts/profile_table.py` and an `agents/openai.yaml`. The reference material is what the skill reads rather than what a person reads.
- `scripts/profile_table.py` — profiling the source table before modelling — is a step most tutorials skip; it has its own test (`tests/skill_neo4j_knowledge_graph/test_profile_table.py`).
- **Not read:** any Python file or skill document. The above is read off the tree and the test names.

## What Is Inside
- **A real Excel input** — `Invoice_data_Demo.xls` at the root, plus `examples/modern_invoice_graphrag/sample_invoice_rows.csv`. The demonstration starts from a business file rather than from a clean CSV.
- **Two generations side by side** — `dataToNeo4jClass/` (py2neo v3, 2018) and `examples/modern_invoice_graphrag/` (vector search, GraphRAG, 2026).
- **An agent skill with its own reference library** — `skills/neo4j-knowledge-graph/`: `SKILL.md`, `references/modeling.md`, `references/cypher-and-graphrag.md`, `scripts/profile_table.py`.
- **`jieba_code/`** — Chinese word segmentation, alongside a Chinese README (`README.zh-CN.md`) and Chinese docs throughout. The repository is bilingual, which its English description does not reveal.
- **Full project governance** — `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md`, `CHANGELOG.md`, and four issue templates, for a fifty-one-file tutorial.
- **Not here:** Neo4j. Every path assumes a running instance.

## Transferable Capability
**Keep the old implementation next to the new one, and profile the source before modelling it.** Migrating a tutorial usually means deleting the previous version, which destroys the most useful comparison a reader could make: what the tooling change actually altered, and what stayed the same because it was inherent to the problem. Preserving both makes the durable part of the method visible. **Profiling the input first** — what columns exist, what their cardinality is, what is actually a key — is the step that decides the graph model, and skipping it is why most spreadsheet-to-graph attempts produce a graph shaped like the spreadsheet rather than like the domain.

The third idea is **packaging the method as an agent-runnable skill with its own reference material**, separating what the agent consults from what a person reads.

**Alternative to:** modelling from the column headers, which reproduces the spreadsheet's accidental structure; and to rewriting a tutorial in place, which loses the diff. **Applies wherever** tabular data must become a connected model — catalogues, registries, entity resolution, anything currently living in a spreadsheet.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Knowledge_Management
- Maturity Stage: Active
- License Class: Permissive
- Deployment Target: Server
- Interface Protocol: Python_SDK
- Data Locality: Distributed
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: Procedural

## Integration & Use Cases
- Run `scripts/profile_table.py` against a source table before deciding on nodes and relationships.
- Read the two implementations together to separate what py2neo did from what the modelling problem requires.
- Take `skills/neo4j-knowledge-graph/` as a model for packaging a data-modelling procedure an agent can execute.

## Reading Notes
579 stars accumulated since 2018 and still pushed 2026-09-01 — an old tutorial that has been genuinely maintained rather than merely left up, which is unusual enough to be the main reason to trust it. Two things the English framing hides: a substantial amount of the material is in Chinese, and `jieba_code/` is Chinese-language segmentation that has nothing to do with the invoice example. The `codex-skill` GitHub topic and the `agents/openai.yaml` indicate the skill is aimed at more than one agent runtime.

## Semantic Links
- [parent_topic:: [[Topic - Knowledge Management]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[neo4j-labs - neocarta]]]
- [related_to:: [[mdebellis - SemanticKG-Design]]]
- [related_to:: [[microsoft - graphrag]]]
- [related_to:: [[MisterIcy - provenance]]]
- [implements_pattern:: [[Pattern - Knowledge Graph Routing]]]
- [implements_pattern:: [[Pattern - Schema Mapping]]]
- [implements_pattern:: [[Pattern - Agent Skill Packaging]]]
- [implements_pattern:: [[Pattern - ETL API Ingestion]]]
- [mentions_term:: [[Glossary - Knowledge Graph]]]
- [mentions_term:: [[Glossary - Retrieval-Augmented Generation]]]
- [mentions_term:: [[Glossary - Schema]]]
- [mentions_term:: [[Glossary - Skill]]]

## Evidence
- Source URL: https://github.com/MazzaWill/neo4j-python-pandas-py2neo-v3
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata, the complete file tree at HEAD, and the LICENSE file; no Python file, skill document or spreadsheet was opened

## GitHub Snapshot

- Description: Excel-to-Neo4j knowledge graph examples: legacy py2neo v3 plus modern Neo4j GraphRAG/vector search.
- Language: Python
- License (SPDX): MIT
- Default Branch: master
- Stars: 579
- Pushed At: 2026-09-01T21:06:02Z
- Topics: ai-agents, codex-skill, excel, graphrag, knowledge-graph, neo4j, pandas, py2neo, python

## Evidence Anchors
- [github_repo] description :: Excel-to-Neo4j knowledge graph examples: legacy py2neo v3 plus modern Neo4j GraphRAG/vector search. (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: MIT (confidence 0.90)
- [github_repo] topics :: ai-agents, codex-skill, excel, graphrag, knowledge-graph, neo4j, pandas, py2neo, python (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 51 paths at HEAD (confidence 0.95)
