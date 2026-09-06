---
uuid: "4c5ea6e9-5ea8-54d7-b8f8-a2d32c5a5ee1"
canonical_url: "https://github.com/netdata/netdata"
repo_key: "netdata/netdata"
owner: "netdata"
repo_name: "netdata"
aliases: ["netdata/netdata", "https://github.com/netdata/netdata"]
type: "infrastructure_tool"
primary_topic: "Infrastructure & Observability"
secondary_topics: ["Security & SIEM", "Government & Civic Tech"]
ecosystem: "Go"
domain_primary: "Infrastructure"
maturity_stage: "Production_Ready"
license_class: "Copyleft"
deployment_target: "Server"
interface_protocol: "CLI"
data_locality: "Distributed"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "Callable"
patterns: ["Infrastructure as Code", "Observability Pipeline"]
glossary_terms: ["Infrastructure as Code", "Monitoring", "Observability", "Telemetry", "Metrics"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "GPL-3.0"
source_file: "repositories to chart.md"
evidence_count: 6
github_description: "The fastest path to AI-powered full stack observability, even for lean teams."
github_language: "Go"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "master"
github_stars: 0
github_topics: ["ai", "alerting", "cncf", "data-visualization", "database", "devops", "docker", "grafana", "influxdb", "kubernetes", "linux", "machine-learning", "mcp", "mongodb", "monitoring", "mysql", "netdata", "observability", "postgresql", "prometheus"]
github_homepage: "https://www.netdata.cloud"
github_pushed_at: "2026-08-31T17:17:26Z"
github_updated_at: "2026-08-31T16:49:10Z"
---

# netdata

## Bottom Line
Per-second infrastructure monitoring that auto-discovers what a node is running, trains an anomaly model per metric at the edge, and shows dashboards immediately — deliberately positioned against stacks that collect few metrics at low resolution and cost a great deal to run.

## What It Solves
- Get useful visibility on a node in minutes, without first designing what to collect.
- Keep per-second resolution across many hosts, where most stacks downsample to keep costs manageable.
- Surface anomalies without anyone having written a threshold, via unsupervised models trained per metric.

## Architecture & Mechanics
- An agent on each node auto-discovers services and collects metrics through 800+ integrations with no configuration.
- Samples go into a purpose-built time-series database claiming roughly half a byte per sample.
- Machine learning runs at the edge on the agent itself, training per-metric models and flagging anomalies locally.
- Agents stream to parent nodes for centralisation, so the topology scales horizontally rather than through one central store.
- Collection, storage, learning, alerting and visualisation are all in the one binary rather than assembled from separate tools.

## What Is Inside
- **A polyglot agent where Go now dominates** — `src/` (11,364 files): `go/` (7,489, 3,393 `.go`), `collectors/` (1,082), `crates/` (925 Rust, 786 `.rs`), `health/` (526, the alerting rules), `libnetdata/` (498 C), `web/` (273), `daemon/` (134).
- **Collectors are the reusable unit** — `src/go/plugin/go.d/collector/` has one directory per monitored system, each with its own `testdata/` of captured real responses (`clickhouse/testdata/resp_longest_query_time.csv` and hundreds of siblings). 872 fixture paths. If you need a sample response from a specific piece of infrastructure, it is probably in here.
- **Alert definitions as data** — `src/health/` (526 files), health rules expressed declaratively rather than as code.
- **An integrations catalogue with published schemas** — `integrations/` (101 files) plus `integrations/schemas/` (`agent_notification.json`, `authentication.json` and others).
- **A documentation map as machine-readable data** — `docs/.map/map.yaml` with `map.schema.json`, and `docs/diagrams/` where PlantUML source (`config.puml`) is built by `build.sh` into checked-in SVG.
- **Anomaly detection with a written explanation** — `src/ml/notebooks/netdata_anomaly_detection_deepdive.ipynb`.
- **197 agent-instruction paths, the largest in this catalogue** — `.agents/skills/` with `SKILL.md`, `how-tos/`, `recipes/` and executable `scripts/`, covering `integrations-lifecycle` (with `recipes/add-go-collector.md`), `project-health-alert-authoring`, `project-prometheus-profiles` (with its own `test_validate_profile.py` and a how-to on building synthetic fixtures), `codacy-audit`, and `project-query-corpus`. Contribution procedure written as executable agent skills, at a scale nothing else here approaches.

## Transferable Capability
**Collect at a resolution fine enough that the shape of an event survives, rather than at whatever interval keeps storage cheap.** Most detail is discarded before anyone knows whether it mattered; keeping it briefly, close to where it was produced, means the question can still be asked afterwards. Two separable moves: **one self-contained collector per observed system, each carrying captured real responses as its own test material**, and **rules expressed as data rather than as code**, so the thing being watched for can be changed without changing the watcher. A third, entirely separable idea: **ship the contribution procedure as something executable rather than something to read** - a recipe per task, with its own scripts and checks - so a contributor performs the procedure instead of interpreting it.

**Alternative to:** aggregating at collection time, which decides in advance which questions may be asked. **Applies wherever** the interesting event is brief and the interesting question is asked afterwards.

## Taxonomy
- Ecosystem: Go
- Domain Primary: Infrastructure
- Maturity Stage: Production_Ready
- License Class: Copyleft
- Deployment Target: Server
- Interface Protocol: CLI
- Data Locality: Distributed
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: Callable

## Integration & Use Cases
- Put monitoring on a handful of machines quickly, with dashboards from the first minute.
- Compare edge-side anomaly detection against centralised rule evaluation.
- Study how aggressive per-sample compression makes high-resolution retention affordable.

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
- Source URL: https://github.com/netdata/netdata
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names GPL-3.0 (reproduced in full). The GitHub API reported `UNKNOWN`, which is why this was read directly.

## GitHub Snapshot

- Description: The fastest path to AI-powered full stack observability, even for lean teams.
- Language: Go
- License: Unknown (UNKNOWN)
- Default Branch: master
- Stars: 0
- Watchers: 0
- Homepage: https://www.netdata.cloud
- Archived: no
- Disabled: no
- Pushed At: 2026-08-31T17:17:26Z
- Updated At: 2026-08-31T16:49:10Z
- Topics: ai, alerting, cncf, data-visualization, database, devops, docker, grafana, influxdb, kubernetes, linux, machine-learning, mcp, mongodb, monitoring, mysql, netdata, observability, postgresql, prometheus

## Evidence Anchors
- [github_repo] description :: The fastest path to AI-powered full stack observability, even for lean teams. (confidence 0.95)
- [github_repo] topics :: ai, alerting, cncf, data-visualization, database, devops, docker, grafana, influxdb, kubernetes, linux, machine-learning (confidence 0.82)
- [github_repo] language :: Go (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
