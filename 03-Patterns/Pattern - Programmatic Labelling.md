---
pattern_key: "programmatic_labelling"
aliases: ["weak supervision pipeline"]
type: "pattern"
status: "active"
examples: ["snorkel-team - snorkel", "NorskRegnesentral - skweak", "open-metadata - OpenMetadata"]
glossary_terms: ["Weak Supervision", "Labelling Function", "Named Entity Recognition"]
topic_keys: ["ml_training_mlops"]
---

# Pattern - Programmatic Labelling

## Definition
Replace hand annotation with many small programs that each vote a label or abstain, then estimate how far to trust each one from the pattern of agreement and disagreement between them, and combine the votes into a single probabilistic label.

## Why It Matters
- Labels become code: reviewable, versioned, and re-runnable over the whole corpus when the definition changes. A hand-labelled set cannot survive a changed definition.
- The accuracy estimate needs no ground truth. Voters that agree with the consensus more often are weighted up, and the structure of the disagreement carries the information.
- The shape recurs far outside machine learning. A catalogue that classifies sources with several imperfect signals is doing this, whether or not it names it.

## Example Repositories
- [[snorkel-team - snorkel]]
- [[NorskRegnesentral - skweak]]
- [[open-metadata - OpenMetadata]]

## Related Glossary
- [[Glossary - Weak Supervision]]
- [[Glossary - Labelling Function]]
- [[Glossary - Named Entity Recognition]]

## Related Topics
- [[Topic - ML Training & MLOps]]
