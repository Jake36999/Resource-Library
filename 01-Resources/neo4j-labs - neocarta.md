---
uuid: "827d567c-bdfc-5e4d-aed9-882841c3046f"
canonical_url: "https://github.com/neo4j-labs/neocarta"
repo_key: "neo4j-labs/neocarta"
owner: "neo4j-labs"
repo_name: "neocarta"
aliases: ["neo4j-labs/neocarta", "https://github.com/neo4j-labs/neocarta"]
type: "ai_framework"
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
agent_surface: "Callable"
patterns: ["Metadata Harvesting", "Multi-Tier Index Routing"]
glossary_terms: ["Semantic Layer", "Metadata Catalog", "Knowledge Graph", "Model Context Protocol"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-03"
evidence_count: 5
github_description: "Library built for generating semantic layer graphs for query routing, query generation and data discovery"
github_language: "Python"
github_license_spdx: "Apache-2.0"
github_default_branch: "main"
github_stars: 106
github_topics: []
github_homepage: "Unknown"
github_pushed_at: "2026-08-24T21:46:10Z"
---
# neo4j-labs - neocarta

## Bottom Line
Harvests schema, glossary, metric definitions and query history from warehouses into a Neo4j semantic-layer graph, then serves that graph to an agent as MCP tools — so the agent learns the landscape before it writes a query, and only metadata ever leaves the source.

## What It Solves
- Text-to-SQL that fails because the model does not know which of four `customer` tables is current or what `status_cd` means.
- Routing a question to the right database when there is more than one.
- Giving business meaning — glossary terms, governed metrics — a place to live next to the schema it describes.

## Architecture & Mechanics
- **Ingest**: connectors for BigQuery schema and logs, Databricks, Dataplex, Snowflake, JDBC, CSV, query logs and OSI. Only metadata crosses into Neo4j.
- **Model**: `data_model/` is split by kind of knowledge rather than by source — `schema/rdbms`, `schema/lpg`, `glossary`, `governance`, `metadata`, `query`, `instance`, `osi` — each with its own models, README and a checked-in mermaid diagram beside the rendered image.
- **Serve**: `_mcp/` exposes catalog, full-text, vector, hybrid and business-term search tools, and keeps the Cypher in `_mcp/cypher/` **separate from the tool definitions** in `_mcp/tools/` — the query is data, the tool is the contract around it.
- `enrichment/embeddings/` optionally embeds chosen node labels via LiteLLM or OpenAI, which is what enables the vector and hybrid tools.

## What Is Inside
- **Connectors** — `neocarta/connectors/`: `bigquery/` (schema and query logs, each with
  `connector.py`, `extract.py`, `models.py`), `databricks/`, `dataplex/`, `snowflake/`, `jdbc/`,
  `csv/`, `query_log/`, and `osi/` — the only bidirectional one.
- **A data model split by kind of knowledge** — `neocarta/data_model/`: `schema/rdbms`,
  `schema/lpg`, `glossary`, `governance`, `metadata`, `query`, `instance`, `osi`. Each has its
  own Pydantic models and its own README.
- **An MCP server with query and contract separated** — `neocarta/_mcp/cypher/` holds the Cypher
  (`catalog`, `full_text_search`, `vector_search`, `hybrid_search`, `osi_catalog`,
  `osi_definitions`, `osi_domain`, `osi_metric_search`); `neocarta/_mcp/tools/` holds the tool
  definitions over them.
- **Diagram source beside the render** — `assets/mermaid/data_model/*.mmd` paired with
  `assets/images/data_model/*.png`, ten models including `sql-graph-data-model-expanded`,
  `governance-data-model` and `query-log-data-model`.
- **Sample datasets** — `datasets/`: an ACME warehouse as SQL and as a 33-table OSI YAML model,
  an e-commerce dataset, and 15 CSV metadata tables.
- **Contributor skills** — `.claude/skills/neocarta-add-source-connector/` and
  `neocarta-add-connector-cli-command/`, each with a `SKILL.md`, a written contract and a
  `driver.py`.

## Transferable Capability
**Give an automated consumer a model of the landscape before it acts, rather than expecting it to infer the landscape from the request.** Gather what things mean, how they relate and what has been asked of them before; hold that as a connected model; expose it as a small set of typed questions the consumer can ask first. Only the description travels — the material itself stays where it is.

A structural detail worth taking on its own: **keep the stored query separate from the interface that offers it.** The query is data and can be edited; the interface is a contract and should not move because a query changed.

**Alternative to:** giving a consumer raw structure and hoping context is inferred; and to embedding queries inside the interface definitions that expose them. **Applies wherever** something must act competently across a landscape it did not build and cannot see all of.

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
- Agent Surface: Callable

## Integration & Use Cases
- Put a semantic layer in front of agents querying more than one warehouse.
- Borrow the separation of stored queries from tool definitions for any MCP surface.
- Study a graph data model that separates schema, glossary, governance and query history.

## Reading Notes
Two things to know. The **OSI connector is bidirectional** — alone among the connectors it both loads an Open Semantic Interchange YAML model into Neo4j and exports a subgraph back out as spec-compliant YAML, giving the semantic layer a portable, diffable serialisation. And the **canonical location moved**: the CI badge points at `neo4j-field/neocarta`, which 301-redirects here. Status is explicitly experimental — "not a Neo4j product... a Neo4j Labs project supported by the Neo4j field team" — and the documentation quality runs ahead of the maturity. The whole query layer is Cypher, so Neo4j is a non-negotiable dependency.

## Semantic Links
- [parent_topic:: [[Topic - Knowledge Management]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[open-metadata - OpenMetadata]]]
- [related_to:: [[microsoft - graphrag]]]
- [related_to:: [[run-llama - llama_index]]]
- [implements_pattern:: [[Pattern - Metadata Harvesting]]]
- [implements_pattern:: [[Pattern - Multi-Tier Index Routing]]]
- [mentions_term:: [[Glossary - Semantic Layer]]]
- [mentions_term:: [[Glossary - Metadata Catalog]]]
- [mentions_term:: [[Glossary - Knowledge Graph]]]
- [mentions_term:: [[Glossary - Model Context Protocol]]]

## Evidence
- Source URL: https://github.com/neo4j-labs/neocarta
- Source kind: GitHub REST metadata plus the repository tree and files, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-03
- Depth of read: recorded per source in [[Scouting Working File 2026-09-03]]

## GitHub Snapshot

- Description: Library built for generating semantic layer graphs for query routing, query generation and data discovery
- Language: Python
- License (SPDX): Apache-2.0
- Default Branch: main
- Stars: 106
- Homepage: Unknown
- Pushed At: 2026-08-24T21:46:10Z
- Topics: Unknown

## Evidence Anchors
- [github_repo] description :: Library built for generating semantic layer graphs for query routing, query generation and data discovery (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: Apache-2.0 (confidence 0.90)
- [github_repo] topics :: Unknown (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-03 (confidence 0.95)
