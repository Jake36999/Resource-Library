---
uuid: "d5a0256c-9234-585a-ae45-5fd8399a23db"
canonical_url: "https://github.com/SigmaHQ/sigma"
repo_key: "SigmaHQ/sigma"
owner: "SigmaHQ"
repo_name: "sigma"
aliases: ["SigmaHQ/sigma", "https://github.com/SigmaHQ/sigma"]
type: "detection_ruleset"
primary_topic: "Security & SIEM"
secondary_topics: ["Curated Aggregators & Reference Lists"]
ecosystem: "Security_Analytics"
domain_primary: "Security"
maturity_stage: "Production_Ready"
license_class: "Unknown"
deployment_target: "Local_Only"
interface_protocol: "Markdown"
data_locality: "Stateless"
hardware_footprint: "CPU_Only"
security_compliance: "Security_Adjacent"
agent_surface: "None"
patterns: ["Detection as Code", "Threat Detection Pipeline", "Schema Mapping"]
glossary_terms: ["Detection Rule", "SIEM", "Threat Detection", "Schema"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "NOASSERTION"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-08-31"
evidence_count: 4
github_description: "Main Sigma Rule Repository"
github_language: "Python"
github_license_spdx: "NOASSERTION"
github_default_branch: "master"
github_stars: 10963
github_topics: ["elasticsearch", "ids", "logging", "monitoring", "security", "siem", "signatures", "splunk", "sysmon"]
github_homepage: "https://sigmahq.io/"
github_pushed_at: "2026-08-31T02:41:06Z"
---
# SigmaHQ - sigma

## Bottom Line
A vendor-neutral YAML signature format for log-based detections, plus the community rule library that uses it — write a detection once and compile it to Splunk, Elastic, Sentinel or others.

## What It Solves
- Escape per-vendor query syntax lock-in for detection content.
- Share and diff detections as reviewable text in version control.
- Bootstrap coverage from a maintained public rule corpus rather than starting blank.

## Architecture & Mechanics
- Each rule is a YAML document with logsource, detection selections and a condition expression.
- A field-mapping layer translates generic field names onto a specific product's schema.
- Backends compile the abstract rule into the target platform's native query language.
- Rules carry metadata (status, level, ATT&CK tags) usable for triage and coverage mapping.

## What Is Inside
- **3,145 detection rules as YAML**, filed by platform: `rules/windows/` (2,410), `cloud/` (225), `linux/` (210), `application/` (99, including 16 Kubernetes audit rules), `macos/` (69), `network/` (53), `web/` (45), `identity/` (24). This corpus is the reason to come here.
- **Three further tiers with different confidence** — `rules-emerging-threats/` (498, filed by year 2019–2026), `rules-threat-hunting/` (141, lower precision by design), `rules-placeholder/` (24), and `deprecated/` (175) with a `deprecated.csv` recording what was retired and why.
- **Regression data containing real event logs** — `regression_data/` (1,382 files) including **459 `.evtx` Windows event log files**. Genuine event samples are hard to come by and are useful well beyond Sigma.
- **Log source guides** — `documentation/logsource-guides/` explains, per source, what must be enabled for a rule to fire at all (`windows/category/process_creation.md`, `windows/category/ps_module.md`, `other/antivirus.md`). That operational half is what rule corpora usually omit.
- **Validation as code** — `tests/validate-sigma-schema/validate.py`, with CI for regression tests, schema tests and a known-false-positive list (`.github/workflows/known-FPs.csv`).
- **Coverage mapped to ATT&CK** — `sigma_attack_nav_coverage.svg`.
- **Not here:** the converters. `sigma-cli` and `pySigma` are separate repositories; this is the rule corpus and its schema.

## Transferable Capability
**Write the thing you are looking for once, in a form independent of any system that will look for it, and translate it per system at the point of use.** The description of a signal and the mechanics of searching for it are different concerns; fusing them means the description is trapped in whichever engine was current when it was written. Two further ideas ride along: **tier the corpus by confidence** rather than pretending every entry is equally reliable, and **record what must be switched on for a check to work at all** — the operational precondition that corpora usually omit.

**Alternative to:** expressing what you are looking for in the query language of the system you happen to run. **Applies wherever** knowledge about what to detect outlives the tools used to detect it.

## Taxonomy
- Ecosystem: Security_Analytics
- Domain Primary: Security
- Maturity Stage: Production_Ready
- License Class: Unknown
- Deployment Target: Local_Only
- Interface Protocol: Markdown
- Data Locality: Stateless
- Hardware Footprint: CPU_Only
- Security Compliance: Security_Adjacent
- Agent Surface: None

## Integration & Use Cases
- Seed a new SIEM deployment with community detection coverage.
- Maintain detections in git with pull-request review, then compile per platform.
- Study a portable abstraction over incompatible query dialects.

## Reading Notes
**Its licence is real but deliberately unrecognised here.** Sigma ships a
LICENSE file containing the **Detection Rule License (DRL)**, a licence written specifically
for shareable detection content and present in no SPDX lookup table. The catalogue therefore
records `Unknown`, which excludes it from constrained queries — the right behaviour, since
"we could not classify this" must never be quieter than "we classified it and it was fine".
Anyone adopting Sigma rules should read the DRL rather than assume; it is permissive in
intent but carries attribution expectations that a generic open-source assumption misses.

## Semantic Links
- [parent_topic:: [[Topic - Security & SIEM]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[wazuh - wazuh]]]
- [related_to:: [[falcosecurity - falco]]]
- [related_to:: [[OISF - suricata]]]
- [implements_pattern:: [[Pattern - Detection as Code]]]
- [implements_pattern:: [[Pattern - Threat Detection Pipeline]]]
- [implements_pattern:: [[Pattern - Schema Mapping]]]
- [mentions_term:: [[Glossary - Detection Rule]]]
- [mentions_term:: [[Glossary - SIEM]]]
- [mentions_term:: [[Glossary - Threat Detection]]]
- [mentions_term:: [[Glossary - Schema]]]

## Evidence
- Source URL: https://github.com/SigmaHQ/sigma
- Source kind: GitHub REST metadata plus maintainer documentation
- Ingestion mode: agent-curated note authored against live repository metadata
- Metadata captured: 2026-08-31

## GitHub Snapshot

- Description: Main Sigma Rule Repository
- Language: Python
- License (SPDX): NOASSERTION
- Default Branch: master
- Stars: 10963
- Homepage: https://sigmahq.io/
- Pushed At: 2026-08-31T02:41:06Z
- Topics: elasticsearch, ids, logging, monitoring, security, siem, signatures, splunk, sysmon

## Evidence Anchors
- [github_repo] description :: Main Sigma Rule Repository (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: NOASSERTION (confidence 0.90)
- [github_repo] topics :: elasticsearch, ids, logging, monitoring, security, siem, signatures, splunk, sysmon (confidence 0.85)
