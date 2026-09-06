---
pattern_key: "data_orchestration"
aliases: ["workflow orchestration"]
type: "pattern"
status: "active"
examples: ["apache - airflow"]
glossary_terms: ["Data Orchestration", "DAG", "Data Engineering"]
topic_keys: ["data_api_big_data", "infrastructure_observability"]
---

# Pattern - Data Orchestration

## Definition
Task dependencies are declared as a DAG and executed by a scheduler that owns ordering, retries, backfill and observability, replacing chained cron jobs.

## Why It Matters
- Gives the vault a reusable architectural concept for graph traversal.
- Helps compare repositories that solve the same problem in different ways.

## Example Repositories
- [[apache - airflow]]

## Related Glossary
- [[Glossary - Data Orchestration]]
- [[Glossary - DAG]]
- [[Glossary - Data Engineering]]

## Related Topics
- [[Topic - Data APIs & Big Data]]
- [[Topic - Infrastructure & Observability]]
