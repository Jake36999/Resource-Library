---
pattern_key: "runtime_security_monitoring"
aliases: ["workload runtime detection"]
type: "pattern"
status: "active"
examples: ["falcosecurity - falco"]
glossary_terms: ["Runtime Security", "Threat Detection", "Telemetry"]
topic_keys: ["security_siem", "infrastructure_observability"]
---

# Pattern - Runtime Security Monitoring

## Definition
Hostile behaviour is detected by observing workloads as they execute — syscalls, process trees, network activity — rather than by scanning artefacts beforehand.

## Why It Matters
- Gives the vault a reusable architectural concept for graph traversal.
- Helps compare repositories that solve the same problem in different ways.

## Example Repositories
- [[falcosecurity - falco]]

## Related Glossary
- [[Glossary - Runtime Security]]
- [[Glossary - Threat Detection]]
- [[Glossary - Telemetry]]

## Related Topics
- [[Topic - Security & SIEM]]
- [[Topic - Infrastructure & Observability]]
