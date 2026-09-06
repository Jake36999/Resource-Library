---
pattern_key: "schema_first_codegen"
aliases: ["single source of truth schema"]
type: "pattern"
status: "active"
examples: ["open-metadata - OpenMetadata"]
glossary_terms: ["Schema", "Metadata Catalog", "API"]
topic_keys: ["data_api_big_data", "architecture_playbooks"]
---

# Pattern - Schema-First Codegen

## Definition
Define every entity and API shape once in a machine-readable schema, and generate the models for every language that touches them, so no binding is hand-written and none can drift from the definition.

## Why It Matters
- Drift between a specification and its implementations stops being possible rather than being merely discouraged. Generated code is a pure sink; nothing edits it back.
- The schema becomes a reviewable artefact in its own right — a change to the data model is a diff on the schema, not an archaeology exercise across three languages.
- The cost is a build step and the discipline never to hand-edit generated output; the moment someone does, the guarantee is gone.

## Example Repositories
- [[open-metadata - OpenMetadata]]

## Related Glossary
- [[Glossary - Schema]]
- [[Glossary - Metadata Catalog]]
- [[Glossary - API]]

## Related Topics
- [[Topic - Data APIs & Big Data]]
- [[Topic - Architecture & Developer Playbooks]]
