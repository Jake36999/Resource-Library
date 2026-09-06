---
pattern_key: "metadata_harvesting"
aliases: ["connector-based cataloguing"]
type: "pattern"
status: "active"
examples: ["open-metadata - OpenMetadata", "neo4j-labs - neocarta"]
glossary_terms: ["Metadata Catalog", "Data Lineage", "Semantic Layer", "Discovery"]
topic_keys: ["data_api_big_data", "knowledge_management"]
---

# Pattern - Metadata Harvesting

## Definition
Build a catalogue by running one connector per source system that reads structure and description — schemas, columns, keys, query history, ownership — and writes only that metadata into a central store, leaving the data itself where it is.

## Why It Matters
- The catalogue stays small and legally simple: it holds addresses and descriptions, never copies. Nothing is duplicated and nothing sensitive moves.
- It puts the burden in the right place — one connector per source, written once — and makes the connector interface the thing that must be well designed.
- The failure mode is staleness: harvested metadata is a snapshot, so the catalogue needs a refresh schedule and a way to say how old a fact is.

## Example Repositories
- [[open-metadata - OpenMetadata]]
- [[neo4j-labs - neocarta]]

## Related Glossary
- [[Glossary - Metadata Catalog]]
- [[Glossary - Data Lineage]]
- [[Glossary - Semantic Layer]]
- [[Glossary - Discovery]]

## Related Topics
- [[Topic - Data APIs & Big Data]]
- [[Topic - Knowledge Management]]
