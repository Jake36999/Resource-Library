---
pattern_key: "medallion_layering"
aliases: ["bronze silver gold", "multi-hop architecture"]
type: "pattern"
status: "active"
examples: ["Victor-Kipruto-Rop - medallion-lakehouse-platform", "dbt-labs - dbt-core", "apache - airflow"]
glossary_terms: ["Medallion Architecture", "ELT", "Data Engineering", "Schema"]
topic_keys: ["data_api_big_data"]
---

# Pattern - Medallion Layering

## Definition
Stage data through named layers of increasing refinement — raw and immutable, then cleaned
and conformed, then modelled for use — where every layer is derivable from the one before
it, and nothing is ever edited in place.

## Why It Matters
- Because the raw layer is append-only and complete, a transformation bug is fixed by
  replaying rather than by recovering. The expensive failure — having thrown away the only
  copy of what actually arrived — is designed out.
- The layer boundaries are also the natural places to put quality gates, so a failed
  expectation can halt a pipeline before bad data reaches anything downstream.
- It gives consumers a defensible answer to "which table should I query", which is otherwise
  decided by whoever asks first.
- The discipline it demands is that rejected rows go somewhere. Quarantining invalid records
  with a counted warning, rather than filtering them silently, is what turns a layer boundary
  into a place you can debug.

## Example Repositories
- [[Victor-Kipruto-Rop - medallion-lakehouse-platform]]
- [[dbt-labs - dbt-core]]
- [[apache - airflow]]

## Related Glossary
- [[Glossary - Medallion Architecture]]
- [[Glossary - ELT]]
- [[Glossary - Data Engineering]]
- [[Glossary - Schema]]

## Related Topics
- [[Topic - Data APIs & Big Data]]
