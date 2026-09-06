---
pattern_key: "endpoint_instrumentation"
aliases: ["host telemetry collection"]
type: "pattern"
status: "active"
examples: ["osquery - osquery", "wazuh - wazuh"]
glossary_terms: ["Endpoint Instrumentation", "Telemetry", "Monitoring"]
topic_keys: ["security_siem", "infrastructure_observability"]
---

# Pattern - Endpoint Instrumentation

## Definition
Agents on individual hosts expose local state and events through a uniform interface so fleet-wide questions resolve to one query rather than many bespoke collectors.

## Why It Matters
- Gives the vault a reusable architectural concept for graph traversal.
- Helps compare repositories that solve the same problem in different ways.

## Example Repositories
- [[osquery - osquery]]
- [[wazuh - wazuh]]

## Related Glossary
- [[Glossary - Endpoint Instrumentation]]
- [[Glossary - Telemetry]]
- [[Glossary - Monitoring]]

## Related Topics
- [[Topic - Security & SIEM]]
- [[Topic - Infrastructure & Observability]]
