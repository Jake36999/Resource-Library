---
pattern_key: "etl_api_ingestion"
aliases: ["pipeline ingestion"]
type: "pattern"
status: "active"
examples: ["apache - airflow", "dbt-labs - dbt-core", "ckan - ckan"]
glossary_terms: ["API", "Dataset", "ELT", "Data Orchestration"]
topic_keys: ["data_api_big_data"]
---

# Pattern - ETL API Ingestion

## Definition
Data is pulled from external endpoints on a schedule, landed durably, then reshaped — with retries, idempotency and backfill treated as first-class concerns.

## Why It Matters
- Gives the vault a reusable architectural concept for graph traversal.
- Helps compare repositories that solve the same problem in different ways.

## Example Repositories
- [[apache - airflow]]
- [[dbt-labs - dbt-core]]
- [[ckan - ckan]]

## Related Glossary
- [[Glossary - API]]
- [[Glossary - Dataset]]
- [[Glossary - ELT]]
- [[Glossary - Data Orchestration]]

## Related Topics
- [[Topic - Data APIs & Big Data]]
