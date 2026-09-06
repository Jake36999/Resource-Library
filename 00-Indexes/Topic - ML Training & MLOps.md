---
topic_key: "ml_training_mlops"
type: "topic_index"
status: "active"
canonical_vocabulary: ["weak supervision", "labelling function", "training data", "named entity recognition", "zero-shot", "attribution", "fine-tuning", "evaluation"]
inclusion_criteria: "What happens before a model is served: training-data construction, weak supervision, extraction models, fine-tuning frameworks, experiment tracking, evaluation harnesses, and attribution of model behaviour back to training data. Distinct from Agentic AI, which covers inference and orchestration."
patterns: ["programmatic_labelling", "zero_shot_entity_extraction"]
glossary_terms: ["Weak Supervision", "Labelling Function", "Named Entity Recognition", "Zero-Shot Extraction", "Training Data Attribution", "Active Learning"]
resource_count: 11
review_count: 0
created: "2026-09-03"
---

# Topic - ML Training & MLOps

## Inclusion Criteria
What happens before a model is served: training-data construction, weak supervision, extraction models, fine-tuning frameworks, experiment tracking, evaluation harnesses, and attribution of model behaviour back to training data. Distinct from Agentic AI, which covers inference and orchestration.

## Canonical Vocabulary
- weak supervision
- labelling function
- training data
- named entity recognition
- zero-shot
- attribution
- fine-tuning
- evaluation

## Why This Topic Exists
Training data, not architecture, is usually what decides whether a model works, and it is the part with no library to install. The sources here treat label creation as an engineering problem with code, tests and version control, rather than as an annotation budget.

## Mechanics
- Generates labels from many imperfect sources and reconciles them statistically instead of trusting any one.
- Or sidesteps labels entirely, by making the label set an inference-time argument to a model trained to compare spans against arbitrary type names.
- Traces behaviour backwards, from a capability to the corpus regions that produced it.

## Typical Use Cases
- Build a training set for a domain with no annotated corpus.
- Extract structured entities from text without a labelled dataset or a GPU.
- Analyse coverage, overlap and conflict between heuristic labellers before trusting them.

## Approved Resources
- [[snorkel-team - snorkel]]
- [[urchade - GLiNER]]
- [[NorskRegnesentral - skweak]]
- [[HCAI-Lab-GT - capabilibara]]
- [[ardamavi - Unsupervised-Classification-with-Autoencoder]]
- [[aws-samples - amazon-comprehend-examples]]
- [[awsdocs - amazon-comprehend-developer-guide]]
- [[guillaumegenthial - sequence_tagging]]
- [[JackieZhangdx - WeakSupervisedSegmentationList]]
- [[knodle - knodle]]
- [[msgi - nlp-journey]]

## Review Queue
- None yet.

## Related Patterns
- [[Pattern - Programmatic Labelling]]
- [[Pattern - Zero-Shot Entity Extraction]]

## Related Glossary
- [[Glossary - Weak Supervision]]
- [[Glossary - Labelling Function]]
- [[Glossary - Named Entity Recognition]]
- [[Glossary - Zero-Shot Extraction]]
- [[Glossary - Training Data Attribution]]
- [[Glossary - Active Learning]]

## Related Topics
- [[Topic - Agentic AI & Models]]
- [[Topic - Knowledge Management]]
