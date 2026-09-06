---
term_key: "medallion-architecture"
canonical_word: "Medallion Architecture"
sense_label: "canonical"
aliases: ["bronze silver gold"]
related_terms: ["ELT", "Data Engineering", "Schema"]
type: "glossary_term"
status: "active"
topic_keys: ["data_api_big_data"]
---

# Glossary - Medallion Architecture

## Definition
A layering convention for a data lakehouse: Bronze holds raw data exactly as it arrived, Silver holds cleaned and conformed records, Gold holds the business-level models. Each layer is derivable from the one before it, so a mistake is corrected by replaying rather than by recovering.

## Aliases
- bronze silver gold

## Related Terms
- [[Glossary - ELT]]
- [[Glossary - Data Engineering]]
- [[Glossary - Schema]]

## Observed Contexts
| Resource | Role | Sense | Context | Source |
| --- | --- | --- | --- | --- |
| (none yet) | - | - |

## Sense Notes
- Sense label: canonical
- This note is the canonical meaning for this sense, not merely a spelling variant.
