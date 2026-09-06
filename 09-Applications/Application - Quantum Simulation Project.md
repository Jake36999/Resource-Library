---
type: "application_record"
project: "Quantum physics simulation"
stage: "inception through maturity"
date_range: "2025 - ongoing"
status: "active"
resources_used: ["volumetric simulation repositories", "optimised mathematical solvers", "verification technique implementations", "experimental datasets"]
patterns_discovered: ["validation by identifiable signal", "resource needs shift from method to data as a project matures"]
domains: ["scientific_simulation_math", "datasets_benchmarks", "ml_training_mlops"]
outcome: "simulation approach assembled from prior work; validation later grounded against real experimental data"
---

# Application - Quantum Simulation Project

## What Was Needed
Started in 2025. Simulating quantum physics required three separate things that no single source provided: a way to represent and compute over volumes, mathematical solvers fast enough to be usable, and techniques for verifying that the simulation was doing something real rather than something merely stable.

## What Was Found And Taken
Multiple repositories, each contributing a different piece. Volumetric simulation approaches informed how the domain was represented. Optimised solvers supplied methods that would have taken a long time to derive and longer to make fast. Verification techniques supplied the methods for checking correctness.

Most of this was **inspiration and method rather than code** — the value was in seeing how the problem had been decomposed by people who had already done it.

As the project matured the requirement changed shape entirely. Comparison against other experiments became necessary, which meant finding and accessing relevant **datasets**, and then identifying the correct **validation points**: the identifiable signals indicating that the simulation was producing behaviour and dynamics within the right envelope.

## What It Replaced
Deriving numerical methods and verification strategy from first principles, and — at the later stage — having no external ground truth at all, which would have left the simulation unfalsifiable.

## Patterns And Insights
**Validation by identifiable signal.** The useful question is not "is the output correct" but "does the output contain the specific signals that correct behaviour is known to produce". This turns verification from a judgement into a check, and it transfers well beyond physics — it is the same idea as a schema test in a data pipeline or a detection rule in security monitoring.

**A project's resource needs change category as it matures.** Early on the need was for *methods*; later it was for *data and validation points*. These are different searches with different vocabulary, and a catalogue organised only by subject will serve the first well and the second badly.

## What The Catalogue Should Learn
1. **Datasets are a first-class resource type, not a footnote to software.** The mature phase of this project needed datasets more than code, and the current taxonomy treats them as an afterthought. The reserve domain `datasets_benchmarks` should be promoted.
2. **Index by project stage as well as by subject.** "Methods for simulating X" and "datasets for validating X" are different queries. The workflow layer is the right place for this, and a simulation workflow should exist.
3. **Capture verification techniques as patterns.** They transfer across domains far better than the simulation methods they accompany, and they are currently invisible.

## Semantic Links
- [application_hub:: [[Application Index]]]
- [related_topic:: [[Topic - Scientific Simulation & Math]]]
- [related_topic:: [[Topic - Data APIs & Big Data]]]
