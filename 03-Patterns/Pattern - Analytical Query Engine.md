---
pattern_key: "analytical_query_engine"
aliases: ["OLAP engine"]
type: "pattern"
status: "active"
examples: ["duckdb - duckdb", "dbt-labs - dbt-core"]
glossary_terms: ["OLAP", "Schema", "Data Engineering"]
topic_keys: ["data_api_big_data"]
---

# Pattern - Analytical Query Engine

## Definition
Columnar storage plus vectorised execution optimised for scanning and aggregating many rows over few columns, rather than transactional row-level access.

## Why It Matters
- Gives the vault a reusable architectural concept for graph traversal.
- Helps compare repositories that solve the same problem in different ways.

## Example Repositories
- [[duckdb - duckdb]]
- [[dbt-labs - dbt-core]]

## Related Glossary
- [[Glossary - OLAP]]
- [[Glossary - Schema]]
- [[Glossary - Data Engineering]]

## Related Topics
- [[Topic - Data APIs & Big Data]]
