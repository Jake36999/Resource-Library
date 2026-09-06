---
pattern_key: "observability_pipeline"
aliases: ["telemetry pipeline"]
type: "pattern"
status: "active"
examples: ["prometheus/prometheus", "netdata/netdata", "statsd/statsd", "getsentry/sentry", "wazuh/wazuh", "OISF/suricata", "apache/airflow"]
glossary_terms: ["Monitoring", "Observability", "Telemetry", "Metrics"]
topic_keys: ["infrastructure_observability"]
---

# Pattern - Observability Pipeline

## Definition
A telemetry architecture that collects, stores, queries, and alerts on metrics or events.

## Why It Matters
- Gives the vault a reusable architectural concept for graph traversal.
- Helps compare repositories that solve the same problem in different ways.

## Example Repositories
- [[prometheus]]
- [[netdata]]
- [[statsd]]
- [[getsentry - sentry]]
- [[wazuh - wazuh]]
- [[OISF - suricata]]
- [[apache - airflow]]

## Related Glossary
- [[Glossary - Monitoring]]
- [[Glossary - Observability]]
- [[Glossary - Telemetry]]
- [[Glossary - Metrics]]

## Related Topics
- [[Topic - Infrastructure & Observability]]
