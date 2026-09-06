---
uuid: "6ae54ddf-aad4-55f4-8234-24974ea14d4e"
canonical_url: "https://github.com/falcosecurity/falco"
repo_key: "falcosecurity/falco"
owner: "falcosecurity"
repo_name: "falco"
aliases: ["falcosecurity/falco", "https://github.com/falcosecurity/falco"]
type: "security_tool"
primary_topic: "Security & SIEM"
secondary_topics: ["Infrastructure & Observability"]
ecosystem: "Security_Analytics"
domain_primary: "Security"
maturity_stage: "Production_Ready"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "CLI"
data_locality: "Distributed"
hardware_footprint: "CPU_Only"
security_compliance: "Security_Adjacent"
agent_surface: "None"
patterns: ["Runtime Security Monitoring", "Detection as Code", "Threat Detection Pipeline"]
glossary_terms: ["Threat Detection", "Runtime Security", "Detection Rule", "Alerting"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-05"
evidence_count: 4
github_description: "Cloud Native Runtime Security"
github_language: "C++"
github_license_spdx: "Apache-2.0"
github_default_branch: "master"
github_stars: 9319
github_topics: ["cloud-native", "cncf", "cncf-project", "containers", "ebpf", "falco", "hacktoberfest", "kubernetes", "runtime-security", "security"]
github_homepage: "https://falco.org"
github_pushed_at: "2026-09-04T09:39:09Z"
---
# falcosecurity - falco

## Bottom Line
A CNCF runtime security engine that taps kernel syscalls via eBPF and evaluates them against declarative rules to detect anomalous container and host behaviour in real time.

## What It Solves
- Detect container escapes, unexpected shells and privilege changes as they happen rather than after log aggregation.
- Express security policy as version-controlled YAML rules instead of vendor console clicks.
- Add runtime signal to a Kubernetes stack that otherwise only has admission-time controls.

## Architecture & Mechanics
- An eBPF probe (or kernel module) streams syscall events from the host into userspace.
- A rules engine matches events against conditions with Kubernetes and container metadata joined in.
- Outputs are emitted to stdout, gRPC or falcosidekick for fan-out to alerting systems.
- Rules ship as a versioned ruleset that can be extended per environment.

## What Is Inside
- **A small repository for its reputation** — 365 files. The detection engine is `userspace/engine/` (48) and the daemon `userspace/falco/` (77); the kernel-side event capture lives in `falcosecurity/libs`, not here.
- **Rules are YAML and are the interface** — 70 `.yaml` files; the shipped rule sets define macros, lists and conditions over syscall fields, which is the reusable pattern independent of Falco.
- **Design proposals kept as documents** — `proposals/` (23 files), a written record of how features were argued before being built.
- **Two test tiers** — `unit_tests/` (32) and `e2e_tests/` (20), plus a CI action that drives an **event generator** against a live install (`.github/actions/event-generator-tests/`) rather than mocking syscalls.
- **A production Helm chart** — `chart/falco/` (49 files), and a `docker/docker-compose/` quickstart.
- **Go alongside C++** — 17 `.go` files for tooling; the core is 91 `.cpp` / 57 `.h`.

## Transferable Capability
**Watch what a system actually does at the boundary it cannot avoid crossing, rather than what it declares.** Anything can misrepresent itself in its own logs; nothing can perform an action without making the underlying request. Observing at that layer makes the observation independent of the cooperation of the observed. The rules are data, with named conditions and reusable fragments, so what counts as suspicious is editable without touching the observer.

**Alternative to:** trusting a subject's own account of itself. **Applies wherever** the thing being watched has an interest in the answer, or is simply unreliable about it.

## Taxonomy
- Ecosystem: Security_Analytics
- Domain Primary: Security
- Maturity Stage: Production_Ready
- License Class: Permissive
- Deployment Target: Server
- Interface Protocol: CLI
- Data Locality: Distributed
- Hardware Footprint: CPU_Only
- Security Compliance: Security_Adjacent
- Agent Surface: None

## Integration & Use Cases
- Instrument a Kubernetes cluster with runtime detections feeding an existing SIEM.
- Study eBPF-based observation as an alternative to agent log parsing.
- Model detection-as-code workflows for a security team.

## Semantic Links
- [parent_topic:: [[Topic - Security & SIEM]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[wazuh - wazuh]]]
- [related_to:: [[osquery - osquery]]]
- [related_to:: [[SigmaHQ - sigma]]]
- [implements_pattern:: [[Pattern - Runtime Security Monitoring]]]
- [implements_pattern:: [[Pattern - Detection as Code]]]
- [implements_pattern:: [[Pattern - Threat Detection Pipeline]]]
- [mentions_term:: [[Glossary - Threat Detection]]]
- [mentions_term:: [[Glossary - Runtime Security]]]
- [mentions_term:: [[Glossary - Detection Rule]]]
- [mentions_term:: [[Glossary - Alerting]]]

## Evidence
- Source URL: https://github.com/falcosecurity/falco
- Source kind: GitHub REST metadata plus maintainer documentation
- Ingestion mode: agent-curated note authored against live repository metadata
- Metadata captured: 2026-08-31

## GitHub Snapshot

- Description: Cloud Native Runtime Security
- Language: C++
- License (SPDX): Apache-2.0
- Default Branch: master
- Stars: 9319
- Homepage: https://falco.org
- Pushed At: 2026-08-31T09:32:54Z
- Topics: cloud-native, cncf, cncf-project, containers, ebpf, falco, hacktoberfest, kubernetes, runtime-security, security

## Evidence Anchors
- [github_repo] description :: Cloud Native Runtime Security (confidence 0.95)
- [github_repo] language :: C++ (confidence 0.90)
- [github_repo] license :: Apache-2.0 (confidence 0.90)
- [github_repo] topics :: cloud-native, cncf, cncf-project, containers, ebpf, falco, hacktoberfest, kubernetes, runtime-security, security (confidence 0.85)
