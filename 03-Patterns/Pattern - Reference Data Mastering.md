---
pattern_key: "reference_data_mastering"
aliases: ["golden record", "survivorship"]
type: "pattern"
status: "active"
examples: ["corzosoft - azure-edm-reference-data-platform", "open-metadata - OpenMetadata", "ckan - ckan"]
glossary_terms: ["Golden Source", "Data Lineage", "Schema"]
topic_keys: ["data_lineage_provenance"]
---

# Pattern - Reference Data Mastering

## Definition
Reconcile several sources that describe the same entity into one record, using declared precedence rules to decide which competing value survives, and keeping the reason the winner won.

## Why It Matters
- The requirement is almost never *merge these*; it is *merge these and be able to defend the result later*, which makes the recorded reason the deliverable rather than a by-product.
- Precedence rules drift from their enforcement unless they are paired. [[corzosoft - azure-edm-reference-data-platform]] keeps `survivorship-rules.md` and `test_lineage.py` together for that reason.
- Test inputs must actually conflict. Sample data where the sources agree exercises none of the logic the system exists for.

## Example Repositories
- [[corzosoft - azure-edm-reference-data-platform]]
- [[open-metadata - OpenMetadata]]
- [[ckan - ckan]]

## Related Glossary
- [[Glossary - Golden Source]]
- [[Glossary - Data Lineage]]
- [[Glossary - Schema]]

## Related Topics
- [[Topic - Data Lineage & Provenance]]
- [[Topic - Data APIs & Big Data]]
