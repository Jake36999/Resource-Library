---
pattern_key: "ontology_driven_design"
aliases: ["model-first design", "bounded context modelling"]
type: "pattern"
status: "active"
examples: ["mdebellis - SemanticKG-Design", "SachaCR - library-examples", "open-metadata - OpenMetadata"]
glossary_terms: ["Ontology", "SPARQL", "Schema", "Taxonomy"]
topic_keys: ["knowledge_management"]
---

# Pattern - Ontology-Driven Design

## Definition
Define what things are and how they relate before deciding how they are stored, and treat that model — not the database schema — as the authority the rest of the system is derived from or validated against.

## Why It Matters
- When storage drives the design, meaning ends up scattered across validation code and the model is whatever the tables happen to permit. [[SachaCR - library-examples]] makes the inversion measurable: thirty domain files against four for persistence.
- Different jobs need different formalisms, and collapsing them is the usual failure. [[mdebellis - SemanticKG-Design]] keeps OWL for what things are, SHACL for what must hold and SKOS for how terms relate.
- A queryable model can be validated by queries that should return nothing, which removes the need for a separate validation framework — the check is written in the language the model already speaks.

## Example Repositories
- [[mdebellis - SemanticKG-Design]]
- [[SachaCR - library-examples]]
- [[open-metadata - OpenMetadata]]

## Related Glossary
- [[Glossary - Ontology]]
- [[Glossary - SPARQL]]
- [[Glossary - Schema]]
- [[Glossary - Taxonomy]]

## Related Topics
- [[Topic - Knowledge Management]]
- [[Topic - Architecture & Developer Playbooks]]
