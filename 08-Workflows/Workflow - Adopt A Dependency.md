---
type: "workflow"
status: "active"
triggers: ["should we use", "evaluate a library", "adopt a dependency", "which tool should we pick", "is this repo any good", "vendor a library", "build or buy", "technology selection"]
preconditions: ["you can state the problem without naming a tool", "you know roughly how long the resulting system must live"]
stages: ["State the problem without a tool in it", "Screen on constraints, not merits", "Compare the survivors", "Test the exit before the entry", "Record the decision"]
exit_criteria: "a written decision naming the alternatives rejected and the condition that would reverse it"
anti_patterns: ["comparing features before checking the licence", "ranking by stars", "evaluating what you would need in year three"]
---

# Workflow - Adopt A Dependency

## Situation
Something in this catalogue looks like it solves your problem. Before it becomes load-bearing in your system, spend an hour deciding properly. The cost of removing a dependency is roughly the square of how long it has been in place.

## Decide First
**Can you state the problem without naming a tool?** "We need Airflow" is not a problem. "We need to run twelve dependent jobs nightly and recover from partial failure without re-running everything" is. Only the second lets you tell whether a candidate fits, or whether you need a dependency at all.

**How long must the result live?** A fortnight's prototype and a five-year platform justify completely different rigour. Most of what follows is wasted effort on a prototype and negligent to skip on a platform.

## Stage 1 - State the problem without a tool in it
Write the problem, the constraints that are genuinely fixed (language, deployment target, data residency, budget, hardware), and the one behaviour that would make a candidate useless.

**Why now:** every later stage filters against this. Without it you will compare candidates on their strengths rather than on your needs, which is how the most-marketed option wins.

## Stage 2 - Screen on constraints, not merits
Constraints eliminate; merits only rank. Screen in this order, cheapest first, and stop at the first failure.

**Licence.** Check first, because it is binary and cannot be engineered around. This vault records `license_class` on every resource for exactly this: `Permissive` integrates anywhere, `Weak_Copyleft` (LGPL, MPL) can usually be linked without relicensing your own code, `Copyleft` may oblige you to publish, `Unknown` means GitHub could not identify the licence and a human must read the file. Two resources here — [[hashicorp - terraform]] and [[getsentry - sentry]] — carry licences GitHub reports only as "Other"; both have moved to source-available terms that are not open source in the usual sense. That is precisely the class of fact that must surface before adoption, not after.

**Vitality.** Last push, archived flag, release cadence. A dead project can still be the right answer if you are prepared to own it — but that must be a decision, not a discovery.

**Deployment fit.** `deployment_target`, `hardware_footprint` and `data_locality` in the taxonomy exist to fail candidates fast. A tool needing a GPU or a distributed cluster is disqualified on a single laptop, whatever its merits.

**Not yet:** do not read the documentation or compare features. Most candidates die here, and reading about them first makes you reluctant to let them.

## Stage 3 - Compare the survivors
Usually two or three remain. Now compare, on your problem rather than in general.

Use [[Taxonomy Index]] to line them up across the nine axes at once — that is the one job it does better than reading three notes. Then check whether the survivors implement the same pattern or different ones: two tools under the same `Pattern` note are interchangeable in shape and differ in execution; two under different patterns are a genuine architectural fork and deserve more thought.

[[cfpb - open-source-checklist]] is the readiness checklist worth running here — it was written for public-sector adoption, so it asks the awkward maintenance and governance questions that enthusiasm skips.

**Why now:** with constraints already applied, every remaining option is viable, so comparison is about fit rather than elimination.

## Stage 4 - Test the exit before the entry
The question that separates a decision from an enthusiasm: **if this turns out wrong in a year, what does removing it cost?**

Cheap to remove: it sits behind an interface you control, its data is in a portable format, and a competing implementation exists. Expensive: its idioms spread through your code, its storage format is proprietary, and it has no peer.

Prefer the cheap-exit option even at some feature cost. In this catalogue the difference is visible between [[duckdb - duckdb]] — a file you can query with something else tomorrow — and a platform whose data model is only legible to itself.

**Why now:** exit cost is invisible once you have started building, and it is the factor most often discovered too late.

## Stage 5 - Record the decision
One short note: the problem, what you chose, **what you rejected and why**, and the condition that would make you revisit it.

The rejections are the valuable half. Six months on, someone will ask "why didn't we use X" and without a record the discussion is re-run from memory. Name a reversal condition too — "if we exceed 50 GB, revisit" — so the decision has an expiry rather than hardening into an assumption.

**Why now:** this is the cheapest artefact in the workflow and the one most often skipped.

## Not Yet - The Steel Framing
- **A formal proof-of-concept for every candidate.** Justified for a platform choice, waste for a library. Screen first; build a spike only for a genuine tie.
- **Benchmarking.** Only once you have a workload that resembles yours. Published benchmarks measure someone else's problem.
- **Vendoring or forking.** A response to a specific failure, not a precaution.
- **A full SBOM and licence-scanning pipeline.** Right for a shipping product, overhead for the first three dependencies.

## Exit Criteria
A written decision naming the rejected alternatives and a condition that would reverse it. If you cannot name what you rejected, you did not choose — you accepted.

## Applies These Patterns
- [[Pattern - Reference Architecture]]
- [[Pattern - Curated Resource Curation]]

## Related
- [[Taxonomy Index]]
- [[Library Assessment 2026-09]]
- [[Workflow - Build A Knowledge Catalogue]]
