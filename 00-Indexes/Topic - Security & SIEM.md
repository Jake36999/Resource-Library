---
topic_key: "security_siem"
type: "topic_index"
status: "active"
canonical_vocabulary: ["SIEM", "threat detection", "enrichment", "alerting", "event processing", "security analytics"]
inclusion_criteria: "Security analytics, SIEM pipelines, threat enrichment, adversarial tooling, or other security-adjacent resources that benefit from manual review."
patterns: ["threat_detection_pipeline", "event_enrichment", "security_analytics", "endpoint_instrumentation", "observability_pipeline", "runtime_security_monitoring", "detection_as_code", "schema_mapping"]
glossary_terms: ["SIEM", "Threat Detection", "Enrichment", "Alerting", "Endpoint Instrumentation", "Runtime Security", "Detection Rule", "Schema", "Monitoring", "Intrusion Detection", "Telemetry"]
resource_count: 5
review_count: 1
---

# Topic - Security & SIEM

## Inclusion Criteria
Security analytics, SIEM pipelines, threat enrichment, adversarial tooling, or other security-adjacent resources that benefit from manual review.

## Canonical Vocabulary
- SIEM
- threat detection
- enrichment
- alerting
- event processing
- security analytics

## Why This Topic Exists
Threat detection, security enrichment, event processing, and dual-use security-adjacent tooling.

## Mechanics
- Ingests and normalizes events before applying threat logic or enrichment.
- Often includes alerts, detections, and contextual joins.
- May be dual-use and therefore should be review-gated before publication.

## Typical Use Cases
- Study security event pipelines.
- Compare threat detection or enrichment patterns.
- Hold security-adjacent resources in a review queue until approved.

## Approved Resources
- [[wazuh - wazuh]]
- [[falcosecurity - falco]]
- [[osquery - osquery]]
- [[SigmaHQ - sigma]]
- [[OISF - suricata]]

## Review Queue
- [[G-Research - siembol]]

## Related Patterns
- [[Pattern - Threat Detection Pipeline]]
- [[Pattern - Endpoint Instrumentation]]
- [[Pattern - Observability Pipeline]]
- [[Pattern - Runtime Security Monitoring]]
- [[Pattern - Detection as Code]]
- [[Pattern - Schema Mapping]]

## Related Glossary
- [[Glossary - SIEM]]
- [[Glossary - Threat Detection]]
- [[Glossary - Enrichment]]
- [[Glossary - Alerting]]
- [[Glossary - Endpoint Instrumentation]]
- [[Glossary - Runtime Security]]
- [[Glossary - Detection Rule]]
- [[Glossary - Schema]]
- [[Glossary - Monitoring]]
- [[Glossary - Intrusion Detection]]
- [[Glossary - Telemetry]]

## Related Topics
- [[Topic - Infrastructure & Observability]]
- [[Topic - Data APIs & Big Data]]
