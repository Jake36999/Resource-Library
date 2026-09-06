---
uuid: "492aff88-5927-5769-9b16-7662eb0e3b5a"
canonical_url: "https://github.com/prometheus/prometheus"
repo_key: "prometheus/prometheus"
owner: "prometheus"
repo_name: "prometheus"
aliases: ["prometheus/prometheus", "https://github.com/prometheus/prometheus"]
type: "infrastructure_tool"
primary_topic: "Infrastructure & Observability"
secondary_topics: ["Security & SIEM", "Government & Civic Tech"]
ecosystem: "Go"
domain_primary: "Infrastructure"
maturity_stage: "Production_Ready"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "CLI"
data_locality: "Distributed"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "Documented"
patterns: ["Infrastructure as Code", "Observability Pipeline"]
glossary_terms: ["Infrastructure as Code", "Monitoring", "Observability", "Telemetry", "Metrics"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
evidence_count: 6
github_description: "The Prometheus monitoring system and time series database."
github_language: "Go"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "main"
github_stars: 0
github_topics: ["alerting", "graphing", "hacktoberfest", "metrics", "monitoring", "prometheus", "time-series"]
github_homepage: "https://prometheus.io/"
github_pushed_at: "2026-08-31T16:30:43Z"
github_updated_at: "2026-08-31T16:42:10Z"
---

# prometheus

## Bottom Line
A monitoring system built on a pull model: it scrapes HTTP metrics endpoints from targets it discovers, stores them as time series identified by a name plus key-value labels, and evaluates rules over them in PromQL to raise alerts.

## What It Solves
- Monitor a changing set of targets without maintaining a list of what to poll, using service discovery.
- Slice metrics along arbitrary dimensions after collection, rather than deciding the breakdown when instrumenting.
- Keep monitoring working when the rest of the estate is degraded, since each server is autonomous and needs no distributed storage.

## Architecture & Mechanics
- An HTTP pull model scrapes targets at a set interval; targets come from service discovery or static config.
- The data model is multi-dimensional: a metric name plus label key-value pairs identifies each time series.
- Samples are stored locally on each server node, so nodes are independent rather than clustered.
- PromQL evaluates expressions over those series for both graphing and alert rules.
- A push gateway covers batch jobs too short-lived to be scraped, and federation lets one server scrape another.

## What Is Inside
- **Service discovery is the largest reusable surface** — `discovery/` (222 files) with one implementation per platform: `moby/` (33), `aws/` (21), `kubernetes/` (16), `linode/` (16), `ovhcloud/` (13), `openstack/` (9), `file/` (9) and more. Each is a self-contained pattern for enumerating targets from an external system.
- **A 218-file configuration test corpus** — `config/testdata/` holds valid and deliberately invalid Prometheus configurations, which is the fastest way to learn the config surface and a ready-made corpus for anyone parsing it. 434 fixture paths overall.
- **The storage engine, readable on its own** — `tsdb/` (168 files) including `chunkenc/` with its own benchmarks; the time-series compression design is documented in code rather than only in papers.
- **The remote-write protocol as protobuf** — `prompb/remote.proto`, `prompb/io/prometheus/write/v2/types.proto`, `prompb/io/prometheus/client/metrics.proto`. This is the contract other systems implement, and it is versioned in-tree.
- **Fuzzing corpus generation** — `util/fuzzing/corpus.go` and `corpus_gen/`.
- **Architecture drawn** — `documentation/images/architecture.svg` and `internal_architecture.svg`; `documentation/examples/` carries runnable configurations.
- **Agent instructions** — `AGENTS.md` and `CLAUDE.md`.

## Transferable Capability
**Have the collector find its own targets by asking the environment what exists, rather than being told.** In a landscape that changes without notifying you, an enumerated list of things to watch is wrong immediately; a rule for discovering them stays correct. The second property is **pull rather than push**: the collector decides when to look, so a subject that has stopped responding is detectable, which a silent subject that was supposed to report is not.

**Alternative to:** a maintained list of what to observe; and to observation that depends on the observed thing choosing to speak. **Applies wherever** the set of things to keep track of changes faster than anyone updates the list.

## Taxonomy
- Ecosystem: Go
- Domain Primary: Infrastructure
- Maturity Stage: Production_Ready
- License Class: Permissive
- Deployment Target: Server
- Interface Protocol: CLI
- Data Locality: Distributed
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: Documented

## Integration & Use Cases
- Instrument services where the target set changes constantly, such as a Kubernetes cluster.
- Express an alert as a query over dimensions rather than a fixed threshold on one counter.
- Study the pull-based collection model as an alternative to agents pushing to a central sink.

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
- Source URL: https://github.com/prometheus/prometheus
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names Apache-2.0 (reproduced in full). The GitHub API reported `UNKNOWN`, which is why this was read directly.

## GitHub Snapshot

- Description: The Prometheus monitoring system and time series database.
- Language: Go
- License: Unknown (UNKNOWN)
- Default Branch: main
- Stars: 0
- Watchers: 0
- Homepage: https://prometheus.io/
- Archived: no
- Disabled: no
- Pushed At: 2026-08-31T16:30:43Z
- Updated At: 2026-08-31T16:42:10Z
- Topics: alerting, graphing, hacktoberfest, metrics, monitoring, prometheus, time-series

## Evidence Anchors
- [github_repo] description :: The Prometheus monitoring system and time series database. (confidence 0.95)
- [github_repo] topics :: alerting, graphing, hacktoberfest, metrics, monitoring, prometheus, time-series (confidence 0.82)
- [github_repo] language :: Go (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
