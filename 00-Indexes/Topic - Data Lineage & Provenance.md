---
topic_key: "data_lineage_provenance"
type: "topic_index"
status: "active"
canonical_vocabulary: ["lineage", "provenance", "column-level lineage", "survivorship", "golden source", "reproducibility", "impact analysis", "capture", "compendium"]
inclusion_criteria: "Where data came from and what produced it: SQL lineage parsers, column-level impact analysis, run and workflow provenance capture, reference-data reconciliation and survivorship, provenance interchange formats, and the attribution of an artefact to the inputs and code that made it."
patterns: ["run_provenance_capture", "reference_data_mastering"]
glossary_terms: ["Data Lineage", "Provenance", "Column-Level Lineage", "Golden Source", "Causal Logging", "Research Compendium"]
resource_count: 8
review_count: 0
created: "2026-09-04"
---

# Topic - Data Lineage & Provenance

## Inclusion Criteria
Where data came from and what produced it: SQL lineage parsers, column-level impact analysis, run and workflow provenance capture, reference-data reconciliation and survivorship, provenance interchange formats, and the attribution of an artefact to the inputs and code that made it.

## Canonical Vocabulary
- lineage
- provenance
- column-level lineage
- survivorship
- golden source
- reproducibility
- impact analysis
- capture
- compendium

## Why This Topic Exists
[[Topic - Data APIs & Big Data]] answers *what data exists*. This topic answers *where it came from and what breaks if it changes*, which is a different question with different machinery behind it, and the register has kept the two apart since it was written. It became a real index on 2026-09-04, when the second scouting cohort supplied enough material to fill it; [[recipy - recipy]] and [[shenhuan2021 - gudu-sql-omni-introduce]] were moved here from Data APIs & Big Data at the same time, because a lineage index that omitted the two lineage tools already catalogued would have been incoherent.

**The word carries two senses and they are not interchangeable.** *Data lineage* is the derivation of a value from the inputs and code that produced it — column-level dependency, impact analysis, reproducibility. *Causal lineage* is the dependency between computations, recorded so a distributed system can recover a failure by redoing only the affected work; [[stephanie-wang - lineage-stash-artifact]] is that sense. A third sense appears in [[MisterIcy - provenance]], where what is tracked is the origin of a *method* rather than of data. All three are catalogued here because the underlying capability is the same — an artefact that carries its own derivation — but a query about one is not answered by a source about another, and any note here should say which sense it means.

## Mechanics
- Capture is either **static** — parse the transformation text and infer dependencies, as a SQL lineage parser does — or **dynamic**, recording what actually happened while the job ran. Static sees every path and only the paths it can parse; dynamic sees only the path taken and sees it exactly.
- Granularity is the design decision: dataset-level lineage is cheap and rarely actionable, column-level lineage is what makes impact analysis answer a real question.
- The output is usually two artefacts from one capture — something a person reads and something a machine consumes — and treating either as a rendering of the other loses information.
- Reproducibility is the strongest form of the claim: not a record of what happened, but enough of the environment to make it happen again.

## Typical Use Cases
- Determine what breaks downstream if a column is renamed, retyped or removed.
- Defend a derived figure to an auditor by showing the inputs and the rules that produced it.
- Reconcile several vendors' accounts of the same entity and record which value won and why.
- Re-execute a published analysis, environment included, rather than only re-reading it.

## Approved Resources
- [[shenhuan2021 - gudu-sql-omni-introduce]]
- [[recipy - recipy]]
- [[corzosoft - azure-edm-reference-data-platform]]
- [[fatihsoysalcom - automated-data-lineage-tracker]]
- [[whole-tale - provenance-examples]]
- [[stephanie-wang - lineage-stash-artifact]]
- [[carter-kilgour - delta-quality-testing]]
- [[MisterIcy - provenance]]

## Review Queue
- None yet.

## Related Patterns
- [[Pattern - Run Provenance Capture]]
- [[Pattern - Reference Data Mastering]]

## Related Glossary
- [[Glossary - Data Lineage]]
- [[Glossary - Provenance]]
- [[Glossary - Column-Level Lineage]]
- [[Glossary - Golden Source]]
- [[Glossary - Causal Logging]]
- [[Glossary - Research Compendium]]

## Related Topics
- [[Topic - Data APIs & Big Data]]
- [[Topic - Knowledge Management]]
- [[Topic - Code Intelligence & Structural Parsing]]
