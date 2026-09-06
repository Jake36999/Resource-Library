---
pattern_key: "schema_mapping"
aliases: ["field normalisation"]
type: "pattern"
status: "active"
examples: ["SigmaHQ - sigma", "ckan - ckan", "OSGeo - gdal"]
glossary_terms: ["Schema", "Dataset", "Enrichment"]
topic_keys: ["data_api_big_data", "security_siem"]
---

# Pattern - Schema Mapping

## Definition
An abstract field vocabulary is translated onto each concrete system's schema, so logic written once survives changes of backing store or vendor.

## Why It Matters
- Gives the vault a reusable architectural concept for graph traversal.
- Helps compare repositories that solve the same problem in different ways.

## Example Repositories
- [[SigmaHQ - sigma]]
- [[ckan - ckan]]
- [[OSGeo - gdal]]

## Related Glossary
- [[Glossary - Schema]]
- [[Glossary - Dataset]]
- [[Glossary - Enrichment]]

## Related Topics
- [[Topic - Data APIs & Big Data]]
- [[Topic - Security & SIEM]]
