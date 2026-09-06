---
uuid: "ff829f43-96ac-5d98-9838-738d2dcdf181"
canonical_url: "https://github.com/OISF/suricata"
repo_key: "OISF/suricata"
owner: "OISF"
repo_name: "suricata"
aliases: ["OISF/suricata", "https://github.com/OISF/suricata"]
type: "security_tool"
primary_topic: "Security & SIEM"
secondary_topics: ["Infrastructure & Observability"]
ecosystem: "Security_Analytics"
domain_primary: "Security"
maturity_stage: "Production_Ready"
license_class: "Copyleft"
deployment_target: "Server"
interface_protocol: "CLI"
data_locality: "Distributed"
hardware_footprint: "High_Memory"
security_compliance: "Security_Adjacent"
agent_surface: "None"
patterns: ["Threat Detection Pipeline", "Detection as Code", "Observability Pipeline"]
glossary_terms: ["Intrusion Detection", "Threat Detection", "Detection Rule", "Telemetry"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "GPL-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-08-31"
evidence_count: 4
github_description: "Suricata is a network Intrusion Detection System, Intrusion Prevention System and Network Security Monitoring engine developed by the OISF and the Suricata community."
github_language: "C"
github_license_spdx: "GPL-2.0"
github_default_branch: "main"
github_stars: 6586
github_topics: ["cybersecurity", "ids", "intrusion-detection-system", "intrusion-prevention-system", "ips", "network-monitor", "network-monitoring", "nsm", "security", "suricata", "threat-hunting"]
github_homepage: "https://suricata.io"
github_pushed_at: "2026-08-31T13:05:43Z"
---
# OISF - suricata

## Bottom Line
A high-performance network IDS, IPS and network security monitor that inspects traffic against signatures and emits rich protocol metadata as structured EVE JSON.

## What It Solves
- Detect malicious traffic patterns at the network layer where endpoint agents cannot reach.
- Produce protocol-level telemetry (HTTP, TLS, DNS, flow) for hunting and correlation.
- Run inline as a prevention layer or passively as a monitoring sensor.

## Architecture & Mechanics
- Packets are captured (AF_PACKET, PF_RING, netmap) and reassembled into flows and streams.
- A multi-threaded detection engine matches signatures against decoded protocol fields.
- Protocol parsers emit structured EVE JSON records regardless of whether a rule fires.
- Rulesets such as Emerging Threats are loaded and reloaded without restarting.

## What Is Inside
- **A C engine with a Rust half** — `src/` (1,204 files, 646 `.c` / 589 `.h`) and `rust/` (525): `rust/src/` (263) holds newer protocol parsers, `rust/htp/` (215) is the vendored HTTP parser, plus `rust/ffi/`, `rust/derive/` (proc macros for parser boilerplate), and the `suricatasc` / `suricatactl` CLI tools.
- **A 358-file user guide that includes a developer guide** — `doc/userguide/devguide/codebase/` covers unit testing in both C and Rust and fuzz testing; `devguide/extending/app-layer/` documents how to add a protocol parser and ships **message-sequence-chart diagrams** (`.msc` source beside rendered PNG) for DNS and HTTP/2 transaction flows.
- **Plugin templates you can copy** — `examples/plugins/` carries both a Rust skeleton (`altemplate`, with its own `Cargo.toml` and `.cargo/config.toml`) and a C one.
- **Rule and dataset material** — `rules/` (34 `.rules` files) and `doc/userguide/rules/datasets.rst` with worked examples such as `detect-unique-tlds`.
- **Serious QA infrastructure** — `qa/coccinelle/` (13 semantic-patch rules enforcing C invariants at review time), `qa/live/` (28), `qa/gnuplot/` for profiling output, `.clusterfuzzlite/` with its own Dockerfile, and 154 `.t` test files.
- **Performance documented as a first-class section** — packet profiling and rule profiling each have their own guide pages.

## Transferable Capability
**Inspect a stream as it passes rather than after it lands, deciding in one pass and at line rate.** Storing first and analysing later is simpler and loses the ability to act; the constraint of a single pass is what forces the design. The separable teaching artefact: **the protocol-parser extension path is documented with sequence diagrams whose source is checked in**, so how a stateful conversation is tracked is legible rather than folklore.

**Alternative to:** capture-then-analyse, which trades timeliness for convenience. **Applies wherever** volume makes storage-first impractical or a decision must be made while the material is still in flight.

## Taxonomy
- Ecosystem: Security_Analytics
- Domain Primary: Security
- Maturity Stage: Production_Ready
- License Class: Copyleft
- Deployment Target: Server
- Interface Protocol: CLI
- Data Locality: Distributed
- Hardware Footprint: High_Memory
- Security Compliance: Security_Adjacent
- Agent Surface: None

## Integration & Use Cases
- Deploy a passive network sensor feeding EVE JSON into a SIEM.
- Compare network-layer detection against host-based approaches.
- Study high-throughput packet processing and protocol parsing architecture.

## Semantic Links
- [parent_topic:: [[Topic - Security & SIEM]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[wazuh - wazuh]]]
- [related_to:: [[SigmaHQ - sigma]]]
- [related_to:: [[falcosecurity - falco]]]
- [implements_pattern:: [[Pattern - Threat Detection Pipeline]]]
- [implements_pattern:: [[Pattern - Detection as Code]]]
- [implements_pattern:: [[Pattern - Observability Pipeline]]]
- [mentions_term:: [[Glossary - Intrusion Detection]]]
- [mentions_term:: [[Glossary - Threat Detection]]]
- [mentions_term:: [[Glossary - Detection Rule]]]
- [mentions_term:: [[Glossary - Telemetry]]]

## Evidence
- Source URL: https://github.com/OISF/suricata
- Source kind: GitHub REST metadata plus maintainer documentation
- Ingestion mode: agent-curated note authored against live repository metadata
- Metadata captured: 2026-08-31

## GitHub Snapshot

- Description: Suricata is a network Intrusion Detection System, Intrusion Prevention System and Network Security Monitoring engine developed by the OISF and the Suricata community.
- Language: C
- License (SPDX): GPL-2.0
- Default Branch: main
- Stars: 6586
- Homepage: https://suricata.io
- Pushed At: 2026-08-31T13:05:43Z
- Topics: cybersecurity, ids, intrusion-detection-system, intrusion-prevention-system, ips, network-monitor, network-monitoring, nsm, security, suricata, threat-hunting

## Evidence Anchors
- [github_repo] description :: Suricata is a network Intrusion Detection System, Intrusion Prevention System and Network Security Monitoring engine developed by the OISF and the Suricata community. (confidence 0.95)
- [github_repo] language :: C (confidence 0.90)
- [github_repo] license :: GPL-2.0 (confidence 0.90)
- [github_repo] topics :: cybersecurity, ids, intrusion-detection-system, intrusion-prevention-system, ips, network-monitor, network-monitoring, nsm, security, suricata, threat-hunting (confidence 0.85)
