---
topic_key: "data_api_big_data"
type: "topic_index"
status: "active"
canonical_vocabulary: ["API", "dataset", "endpoint", "schema", "open data", "rate limit", "catalog", "ingestion"]
inclusion_criteria: "Open data portals, public APIs, dataset catalogs, API tracking projects, and big-data resource lists."
patterns: ["open_data_portal", "etl_api_ingestion", "schema_mapping", "curated_resource_curation", "data_orchestration", "observability_pipeline", "analytical_query_engine"]
glossary_terms: ["API", "Dataset", "Open Data", "Endpoint", "Schema", "Rate Limit", "Curation", "Data Orchestration", "DAG", "ELT", "Data Engineering", "OLAP", "Data Portal"]
resource_count: 12
review_count: 0
---

# Topic - Data APIs & Big Data

## Inclusion Criteria
Open data portals, public APIs, dataset catalogs, API tracking projects, and big-data resource lists.

## Canonical Vocabulary
- API
- dataset
- endpoint
- schema
- open data
- rate limit
- catalog
- ingestion

## Why This Topic Exists
Data portals, API layers, and repository collections useful for ingestion, retrieval, analytics, and source discovery.

## Mechanics
- Exposes structured data through endpoints, catalogs, or retrieval layers.
- Frequently needs schema mapping, auth handling, and rate-limit awareness.
- Often feeds ETL, analytics, or scientific workflows.

## Typical Use Cases
- Build ingestion pipelines for public or partner data.
- Compare accessible datasets and API shapes.
- Seed analytics or knowledge-graph projects with reliable sources.

## Approved Resources
- [[not-a-bank - open-banking-tracker-data]]
- [[public-apis - public-apis]]
- [[apache - airflow]]
- [[duckdb - duckdb]]
- [[ckan - ckan]]
- [[dbt-labs - dbt-core]]
- [[open-metadata - OpenMetadata]]
- [[Victor-Kipruto-Rop - medallion-lakehouse-platform]]
- [[PHACDataHub - data-mesh-ref-impl]]
- [[DataWithBaraa - databricks_bootcamp_2026]]
- [[open-metadata - docs-v1-legacy]]
- [[polkadot-java - api]]

## Review Queue
- None yet.

## Fit Note 2026-09-03
Five sources were filed here by the pass recorded in
[[Research Report 2026-09-03 - Lineage, Parsing and Graph Reasoning]]. Three are a
clean fit; two are not. `recipy` and `shenhuan2021 - gudu-sql-omni-introduce` are
lineage and provenance tooling, and this topic is dataset catalogues and APIs. They
are here because it is the closest existing topic. `data_lineage_provenance` has since been
added to [[Scouting Domains]], but it has no topic index yet and will not get one until
scouting fills it — creating a topic ahead of its content is the mistake that left this
vault with two empty topics. These two move when it does.

## Related Patterns
- [[Pattern - Open Data Portal]]
- [[Pattern - Spatial Ingestion]]
- [[Pattern - Curated Resource Curation]]
- [[Pattern - ETL API Ingestion]]
- [[Pattern - Data Orchestration]]
- [[Pattern - Observability Pipeline]]
- [[Pattern - Analytical Query Engine]]
- [[Pattern - Schema Mapping]]

## Related Glossary
- [[Glossary - API]]
- [[Glossary - Dataset]]
- [[Glossary - Open Data]]
- [[Glossary - Endpoint]]
- [[Glossary - Schema]]
- [[Glossary - Rate Limit]]
- [[Glossary - Curation]]
- [[Glossary - Data Orchestration]]
- [[Glossary - DAG]]
- [[Glossary - ELT]]
- [[Glossary - Data Engineering]]
- [[Glossary - OLAP]]
- [[Glossary - Data Portal]]

## Related Topics
- [[Topic - Government & Civic Tech]]
- [[Topic - Geospatial & Earth Data]]
