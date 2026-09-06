---
type: "application_record"
project: "Distributed home infrastructure, monitoring and embedded work"
stage: "operating and extending"
status: "active"
resources_used: ["systems monitoring tooling", "CSI pipeline components"]
patterns_discovered: ["monitoring earns its place at the point of failure", "own-hardware testing as a learning method"]
domains: ["infrastructure_observability", "robotics_embedded", "crypto_identity"]
outcome: "hardware faults diagnosed and resolved; infrastructure now spans three routers with university compute over SSH"
---

# Application - Distributed Systems And Monitoring

## What Was Needed
Monitoring became a priority under the most direct pressure possible: a machine crashing roughly every thirty minutes and struggling to load a browser. Earlier work on a CSI pipeline had touched the area, but this was the point at which it stopped being optional. The hardware has since been largely replaced and the machine now runs well.

## What Was Found And Taken
Systems monitoring tooling, applied to a failing machine rather than a healthy one — which is a different exercise. Diagnosing an unstable system means using monitoring to *find* a fault rather than to confirm continued health, and the tooling that suits each is not necessarily the same.

## What It Replaced
Guesswork, and quite possibly replacing the wrong components.

## Patterns And Insights
**Monitoring proves itself against a failure you already have.** Instrumenting a healthy system produces dashboards nobody reads; instrumenting a failing one produces an answer. This is the reasoning behind the ordering in [[Workflow - Stand Up Observability]] — name the failure first.

**Understanding a system deeply means testing it, on hardware you own.** Running one's own devices under test is how the boundary between what is documented and what is actually true gets found.

## Current Infrastructure And Direction
Three routers running a distributed computer system, soon to be paired with university resources reachable over SSH for heavy workloads — which frees local capacity for self-hosting web applications and sites.

The intended direction is hardware hacking and embedded development: working close to the metal to understand how the systems in daily use actually function.

## What The Catalogue Should Learn
1. **Promote the embedded and hardware domain.** `robotics_embedded` is currently held in reserve and should enter rotation, extended to cover firmware, hardware interfaces, protocol analysis and RF.
2. **Index self-hosting as a deployment context.** Distributed home infrastructure with burst capacity over SSH is a real and under-served target — the taxonomy's `deployment_target` axis should distinguish it from cloud and single-machine.
3. **Security tooling routes through the existing gate.** The vault already separates defensive from dual-use material: offensive and dual-use resources carry `sensitivity: review_required` and are held in [[Review Queue]] rather than approved automatically. Embedded, firmware, protocol and network-analysis material is ordinary catalogue content and routes normally.
4. **Distributed and heterogeneous compute is a resource requirement in its own right.** Job scheduling across mixed local and remote capacity is a real need this setup creates.

## Semantic Links
- [application_hub:: [[Application Index]]]
- [related_topic:: [[Topic - Infrastructure & Observability]]]
- [related_workflow:: [[Workflow - Stand Up Observability]]]
