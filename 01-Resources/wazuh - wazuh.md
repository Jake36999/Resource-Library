---
uuid: "91e59208-c3c9-5bf1-a7ae-371c8fb486a4"
canonical_url: "https://github.com/wazuh/wazuh"
repo_key: "wazuh/wazuh"
owner: "wazuh"
repo_name: "wazuh"
aliases: ["wazuh/wazuh", "https://github.com/wazuh/wazuh"]
type: "security_platform"
primary_topic: "Security & SIEM"
secondary_topics: ["Infrastructure & Observability", "Government & Civic Tech"]
ecosystem: "Security_Analytics"
domain_primary: "Security"
maturity_stage: "Production_Ready"
license_class: "Copyleft"
deployment_target: "Server"
interface_protocol: "REST"
data_locality: "Distributed"
hardware_footprint: "High_Memory"
security_compliance: "Security_Adjacent"
agent_surface: "None"
patterns: ["Threat Detection Pipeline", "Endpoint Instrumentation", "Observability Pipeline"]
glossary_terms: ["SIEM", "Threat Detection", "Enrichment", "Alerting", "Endpoint Instrumentation"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "BSD-2-Clause AND GPL-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-08-31"
evidence_count: 5
github_description: "Wazuh - The Open Source Security Platform. Unified XDR and SIEM protection for endpoints and cloud workloads."
github_language: "C++"
github_license_spdx: "NOASSERTION"
github_default_branch: "main"
github_stars: 16733
github_topics: ["cloud-security", "compliance", "configuration-assessement", "container-security", "cybersecurity", "file-integrity-monitoring", "incident-response", "infosec", "log-analysis", "malware-detection", "pci-dss", "security", "security-audit", "security-automation", "security-hardening", "security-tools", "siem", "vulnerability-detection", "wazuh", "xdr"]
github_homepage: "https://wazuh.com/"
github_pushed_at: "2026-08-31T19:03:17Z"
---
# wazuh - wazuh

## Bottom Line
A unified open-source SIEM and XDR platform that collects agent telemetry from endpoints and cloud workloads, then correlates it into detections, compliance findings and alerts.

## What It Solves
- Centralise host, container and cloud log data into one searchable security store.
- Run file-integrity, vulnerability and configuration-assessment checks on fleets without per-tool licensing.
- Map raw events to compliance frameworks such as PCI DSS for audit evidence.

## Architecture & Mechanics
- Lightweight agents ship endpoint telemetry to a central manager over an authenticated channel.
- The manager decodes and normalises events, then evaluates rulesets to raise alerts.
- An indexer and dashboard layer (OpenSearch-derived) provides retention, search and visualisation.
- Modules bolt on vulnerability detection, SCA and cloud-provider log pulls.

## What Is Inside
- **A new rules engine is the centre of gravity** — `src/engine/` (1,168 files) with `src/engine/ruleset/schemas/` publishing `engine-schema.json`, `ecs_types.json` and `allowed-fields.json`: the detection schema is machine-readable and validated, not conventional. 51 schema paths overall.
- **The agent and manager in C/C++** — `src/`: `shared_modules/` (571), `wazuh_modules/` (507), `data_provider/` (364, system inventory collection), `remoted/` (222), plus `src/unit_tests/` (583).
- **Integration tests that stand up real environments** — `tests/integration/` (608 files) and `api/test/integration/env/` with per-role Dockerfiles including deliberately *old* agent images (`base_old.Dockerfile`, `new.Dockerfile`) for upgrade testing. 50 container paths.
- **Benchmarks inside the engine** — `src/engine/source/base/benchmark/src/eventParser_bench.cpp`, `agentcache/benchmark/`; 165 benchmark paths.
- **GeoIP and MMDB test databases** — `src/engine/source/geo/test/src/testdb.mmdb`, `testdb-asn.mmdb`, usable for testing any MaxMind reader.
- **370 configuration templates** — `etc/templates/`, the shipped ruleset and decoder configuration.
- **An unusually large CI surface** — 149 CI paths, with composite actions per packaging step (`.github/actions/5_builderpackage_*`) covering build, smoke-install and uninstall verification per platform.

## Transferable Capability
**Publish the shape of what you collect as a validated schema, so that everything downstream can rely on field names existing and meaning the same thing.** Signals assembled from many sources are worthless if each source names things differently; normalising to a declared schema at the point of collection makes everything after it simpler. The separable operational idea: **test upgrades by standing up deliberately old versions alongside new ones**, so the migration path is exercised rather than assumed.

**Alternative to:** each collector emitting its own vocabulary and consumers translating; and to upgrade paths verified only in production. **Applies wherever** many producers feed one consumer.

## Taxonomy
- Ecosystem: Security_Analytics
- Domain Primary: Security
- Maturity Stage: Production_Ready
- License Class: Copyleft
- Deployment Target: Server
- Interface Protocol: REST
- Data Locality: Distributed
- Hardware Footprint: High_Memory
- Security Compliance: Security_Adjacent
- Agent Surface: None

## Integration & Use Cases
- Stand up a self-hosted SIEM for a small estate without commercial per-GB pricing.
- Compare agent-based collection against agentless log shipping.
- Study how detection rules and compliance mappings are structured in production.

## Reading Notes
**Copyleft, despite a permissive licence also being present.** The LICENSE
reproduces both **BSD-2-Clause and GPL-2.0**; the GPL is the binding one, so the catalogue
classifies it Copyleft. This is the case that exposed a defect in the resolver: an early
version read the GPL's own "either version 2 of the License, or (at your option) any later
version" boilerplate as an offer of choice and reported Wazuh as Permissive. It is not. For
a security platform likely to be modified and redistributed, the distinction is the
difference between a routine adoption and a legal review.

## Semantic Links
- [parent_topic:: [[Topic - Security & SIEM]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[falcosecurity - falco]]]
- [related_to:: [[OISF - suricata]]]
- [related_to:: [[SigmaHQ - sigma]]]
- [implements_pattern:: [[Pattern - Threat Detection Pipeline]]]
- [implements_pattern:: [[Pattern - Endpoint Instrumentation]]]
- [implements_pattern:: [[Pattern - Observability Pipeline]]]
- [mentions_term:: [[Glossary - SIEM]]]
- [mentions_term:: [[Glossary - Threat Detection]]]
- [mentions_term:: [[Glossary - Enrichment]]]
- [mentions_term:: [[Glossary - Alerting]]]
- [mentions_term:: [[Glossary - Endpoint Instrumentation]]]

## Evidence
- Source URL: https://github.com/wazuh/wazuh
- Source kind: GitHub REST metadata plus maintainer documentation
- Ingestion mode: agent-curated note authored against live repository metadata
- Metadata captured: 2026-08-31
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names BSD-2-Clause, GPL-2.0 (2 reproduced in full, 0 referred to). The GitHub API reported `NOASSERTION`, which is why this was read directly.  **Composite - needs a person to confirm.**

## GitHub Snapshot

- Description: Wazuh - The Open Source Security Platform. Unified XDR and SIEM protection for endpoints and cloud workloads.
- Language: C++
- License (SPDX): NOASSERTION
- Default Branch: main
- Stars: 16733
- Homepage: https://wazuh.com/
- Pushed At: 2026-08-31T19:03:17Z
- Topics: cloud-security, compliance, configuration-assessement, container-security, cybersecurity, file-integrity-monitoring, incident-response, infosec, log-analysis, malware-detection, pci-dss, security, security-audit, security-automation, security-hardening, security-tools, siem, vulnerability-detection, wazuh, xdr

## Evidence Anchors
- [github_repo] description :: Wazuh - The Open Source Security Platform. Unified XDR and SIEM protection for endpoints and cloud workloads. (confidence 0.95)
- [github_repo] language :: C++ (confidence 0.90)
- [github_repo] license :: NOASSERTION (confidence 0.90)
- [github_repo] topics :: cloud-security, compliance, configuration-assessement, container-security, cybersecurity, file-integrity-monitoring, incident-response, infosec, log-analysis, malware-detection, pci-dss, security, security-audit, security-automation, security-hardening, security-tools, siem, vulnerability-detection, wazuh, xdr (confidence 0.85)
