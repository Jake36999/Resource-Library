---
pattern_key: "zero_shot_entity_extraction"
aliases: ["label-at-inference extraction"]
type: "pattern"
status: "active"
examples: ["urchade - GLiNER"]
glossary_terms: ["Zero-Shot Extraction", "Named Entity Recognition", "Inference"]
topic_keys: ["ml_training_mlops"]
---

# Pattern - Zero-Shot Entity Extraction

## Definition
Extract entities of arbitrary types by passing the type names as input at inference time and scoring candidate spans against the encoded labels, so the schema of what is being extracted is a runtime argument rather than a training-time commitment.

## Why It Matters
- Changing what you extract becomes editing a list of strings, not assembling a corpus and retraining.
- Encoding labels separately from the text lets their embeddings be precomputed, which is what makes a hundred entity types affordable.
- It runs at encoder cost on a CPU, which puts extraction inside reach of pipelines that could never justify a model API call per document.

## Example Repositories
- [[urchade - GLiNER]]

## Related Glossary
- [[Glossary - Zero-Shot Extraction]]
- [[Glossary - Named Entity Recognition]]
- [[Glossary - Inference]]

## Related Topics
- [[Topic - ML Training & MLOps]]
