---
pattern_key: "policy_as_schema"
aliases: ["governance by directive"]
type: "pattern"
status: "active"
examples: ["PHACDataHub - data-mesh-ref-impl"]
glossary_terms: ["Schema", "Data Mesh", "API"]
topic_keys: ["data_api_big_data", "government_civic_tech"]
---

# Pattern - Policy As Schema

## Definition
Express what a consumer may ask for and what they may receive as annotations on a schema rather than as code in a gateway, so the access policy and the API contract are the same reviewable artefact.

## Why It Matters
- A policy written as a schema can be diffed, reviewed and versioned by people who are not engineers — which is exactly who owns the policy.
- Field-level transformations (hash it, redact it, coarsen it, drop it) compose declaratively where the equivalent gateway code would branch.
- It suits federations where parties cannot pool data but must agree on questions: the agreement is a file both sides hold.

## Example Repositories
- [[PHACDataHub - data-mesh-ref-impl]]

## Related Glossary
- [[Glossary - Schema]]
- [[Glossary - Data Mesh]]
- [[Glossary - API]]

## Related Topics
- [[Topic - Data APIs & Big Data]]
- [[Topic - Government & Civic Tech]]
