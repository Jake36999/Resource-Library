---
uuid: "cb41b42e-f10d-5bb9-902b-14a37bea8311"
canonical_url: "https://github.com/statsd/statsd"
repo_key: "statsd/statsd"
owner: "statsd"
repo_name: "statsd"
aliases: ["statsd/statsd", "https://github.com/statsd/statsd"]
type: "infrastructure_tool"
primary_topic: "Infrastructure & Observability"
secondary_topics: ["Security & SIEM", "Government & Civic Tech"]
ecosystem: "Observability"
domain_primary: "Infrastructure"
maturity_stage: "Production_Ready"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "CLI"
data_locality: "Distributed"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Infrastructure as Code", "Observability Pipeline"]
glossary_terms: ["Infrastructure as Code", "Monitoring", "Observability", "Telemetry", "Metrics"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
evidence_count: 6
github_description: "Daemon for easy but powerful stats aggregation"
github_language: "JavaScript"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "master"
github_stars: 0
github_topics: ["graphite", "javascript", "metrics", "nodejs", "statsd"]
github_homepage: ""
github_pushed_at: "2025-05-20T07:22:42Z"
github_updated_at: "2026-08-30T20:30:59Z"
---

# statsd

## Bottom Line
A small network daemon that listens on UDP or TCP for lines like `metricname:value|type`, aggregates them over a flush interval, and forwards the result to backends such as Graphite.

## What It Solves
- Let an application emit a metric without knowing anything about the storage behind it.
- Avoid declaring metrics in advance — a new name simply starts existing when first sent.
- Make instrumentation non-blocking and failure-tolerant by defaulting to fire-and-forget UDP.

## Architecture & Mechanics
- A listener accepts counters, timers, gauges and sets in a one-line text format over UDP or TCP.
- An aggregation stage batches values in memory across a flush interval, ten seconds by default.
- Pluggable backends persist each flush to one or more external systems.
- Because the transport is UDP by default, a dropped packet loses a sample rather than blocking the application.

## What Is Inside
- **A small, readable reference implementation** — `lib/` (8 files) and `backends/` (3). The whole daemon is 35 `.js` files, which is why it is worth reading rather than only using: the metric aggregation and flush cycle fit in one sitting.
- **The protocol documentation is the durable part** — `docs/` (15 files): `backend.md` (how to write one), `admin_interface.md`, `metric_types.md`, `graphite.md`, `additional_tools.md`. The StatsD line protocol outlived the implementation and is documented here.
- **Client examples in other languages** — `examples/`: `go/` (3 files) and `examples/Etsy/StatsD.pm` (Perl), plus `exampleConfig.js` and `exampleProxyConfig.js`.
- **Packaging for the era** — `debian/` (16 files), `.upstart` and `.service` unit files, a `Dockerfile` and `docker-compose.yml`.
- **15 test files** in `test/`, including Graphite backend legacy-format tests that document the wire format by example.

## Transferable Capability
**Put a tiny, dumb intermediary between the thing producing measurements and the system storing them.** The producer emits a single line and forgets; the intermediary batches, aggregates and forwards. Because it is trivial and fire-and-forget, instrumenting something costs almost nothing and cannot slow it down or fail it. The durable artefact here is not the implementation but **the line format**, which outlived it and is implemented independently many times over.

**Alternative to:** having the producer talk to the storage system directly, which couples them and makes instrumentation expensive enough to skip. **Applies wherever** you want the cost of recording something to be low enough that nobody argues about it.

## Taxonomy
- Ecosystem: Observability
- Domain Primary: Infrastructure
- Maturity Stage: Production_Ready
- License Class: Permissive
- Deployment Target: Server
- Interface Protocol: CLI
- Data Locality: Distributed
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Add counters and timers to an application with minimal ceremony and no client-side aggregation.
- Fan the same metric stream out to several destinations through multiple backends.
- Study push-based collection as the counterpart to Prometheus's pull model.

## Semantic Links
- [parent_topic:: [[Topic - Infrastructure & Observability]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[NatLabRockies - api-umbrella]]]
- [related_to:: [[puppetlabs - puppet]]]
- [related_to:: [[chef]]]
- [implements_pattern:: [[Pattern - Infrastructure as Code]]]
- [implements_pattern:: [[Pattern - Observability Pipeline]]]
- [mentions_term:: [[Glossary - Infrastructure as Code]]]
- [mentions_term:: [[Glossary - Monitoring]]]
- [mentions_term:: [[Glossary - Observability]]]
- [mentions_term:: [[Glossary - Telemetry]]]
- [mentions_term:: [[Glossary - Metrics]]]

## Evidence
- Source URL: https://github.com/statsd/statsd
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names MIT (reproduced in full). The GitHub API reported `UNKNOWN`, which is why this was read directly.

## GitHub Snapshot

- Description: Daemon for easy but powerful stats aggregation
- Language: JavaScript
- License: Unknown (UNKNOWN)
- Default Branch: master
- Stars: 0
- Watchers: 0
- Homepage: None provided
- Archived: no
- Disabled: no
- Pushed At: 2025-05-20T07:22:42Z
- Updated At: 2026-08-30T20:30:59Z
- Topics: graphite, javascript, metrics, nodejs, statsd

## Evidence Anchors
- [github_repo] description :: Daemon for easy but powerful stats aggregation (confidence 0.95)
- [github_repo] topics :: graphite, javascript, metrics, nodejs, statsd (confidence 0.82)
- [github_repo] language :: JavaScript (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
