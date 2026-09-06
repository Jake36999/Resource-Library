---
uuid: "ce64d9a8-bd41-55c7-a77f-fed4329c123c"
canonical_url: "https://github.com/puppetlabs/puppet"
repo_key: "puppetlabs/puppet"
owner: "puppetlabs"
repo_name: "puppet"
aliases: ["puppetlabs/puppet", "https://github.com/puppetlabs/puppet"]
type: "infrastructure_tool"
primary_topic: "Infrastructure & Observability"
secondary_topics: ["Security & SIEM", "Government & Civic Tech"]
ecosystem: "Mixed"
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
license: "Apache-2.0"
source_file: "repositories to chart.md"
evidence_count: 5
github_description: "Server automation framework and application"
github_language: "Ruby"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "main"
github_stars: 0
github_topics: []
github_homepage: "https://puppet.com/open-source/#osp"
github_pushed_at: "2026-08-06T13:05:18Z"
github_updated_at: "2026-08-31T15:40:28Z"
---

# puppetlabs - puppet

## Bottom Line
Declarative configuration management across Linux, Unix and Windows: administrators describe the intended state of a machine centrally, and agents on each node perform whatever administrative work brings it there.

## What It Solves
- Replace repeated manual administration — users, packages, service configuration — with one central specification.
- Apply the same intent across mixed operating systems without rewriting it for each.
- Detect and correct drift, since agents re-apply the specification on a schedule.

## Architecture & Mechanics
- A central specification describes desired state; agents on managed nodes enforce it.
- The core engine is over 99% Ruby, with HTTP API endpoints for remote management.
- Resource abstraction lets one declaration map onto different platform implementations.
- Acceptance tests, performance benchmarks and internationalisation are maintained in-repo alongside the engine.

## What Is Inside
- **The test estate is the bulk and the most reusable part** — `spec/` (1,235 files): `unit/` (685), `spec/fixtures/` (424), `integration/` (69), plus `shared_behaviours/`, `shared_contexts/` and `shared_examples/` — a worked example of factoring RSpec so behaviour contracts are declared once and applied across many types.
- **Acceptance tests against real machines** — `acceptance/` (351 files): `tests/` (225), `config/` (66), and fixtures that include compiled C# mock installers (`MockInstaller.cs`, `MockService.cs`) and a complete fake RPM repository with its SQLite metadata (`acceptance/fixtures/el-repo/repodata/*.sqlite.bz2`). Realistic package-manager test material that is hard to construct.
- **A benchmark suite with written scenarios** — `benchmarks/` (107 files), each directory carrying a `description` file explaining what it measures (`catalog_memory/` and siblings).
- **The HTTP API documented and schema'd** — `api/docs/` (`http_catalog.md`, `http_certificate.md`, `http_api_index.md`) with `api/schemas/catalog.json`, `environments.json`, `error.json`.
- **The resource type library** — `lib/puppet/` (1,019 files), one type and provider per manageable resource; 181 `.pp` manifest files across examples and tests.

## Transferable Capability
**Compile a description of desired state into a plan for a specific target, and separate the compiling from the applying.** Because the plan is an artefact, it can be inspected, diffed and tested before anything is changed — the answer to *what will this do* is available without doing it. The related testing idea: **declare behaviour contracts once and apply them across many implementations**, so every resource kind is held to the same standard without repeating the tests.

**Alternative to:** apply-and-see, where the only way to learn what a change does is to make it. **Applies wherever** a change is expensive to reverse and its effects are worth knowing in advance.

## Taxonomy
- Ecosystem: Mixed
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
- Standardise configuration across a heterogeneous estate.
- Correct configuration drift automatically rather than by audit.
- Compare Puppet's declarative model against Chef's more imperative recipes.

## Semantic Links
- [parent_topic:: [[Topic - Infrastructure & Observability]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[NatLabRockies - api-umbrella]]]
- [related_to:: [[chef]]]
- [related_to:: [[hashicorp - terraform]]]
- [implements_pattern:: [[Pattern - Infrastructure as Code]]]
- [implements_pattern:: [[Pattern - Observability Pipeline]]]
- [mentions_term:: [[Glossary - Infrastructure as Code]]]
- [mentions_term:: [[Glossary - Monitoring]]]
- [mentions_term:: [[Glossary - Observability]]]
- [mentions_term:: [[Glossary - Telemetry]]]
- [mentions_term:: [[Glossary - Metrics]]]

## Evidence
- Source URL: https://github.com/puppetlabs/puppet
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names Apache-2.0 (reproduced in full). The GitHub API reported `UNKNOWN`, which is why this was read directly.

## GitHub Snapshot

- Description: Server automation framework and application
- Language: Ruby
- License: Unknown (UNKNOWN)
- Default Branch: main
- Stars: 0
- Watchers: 0
- Homepage: https://puppet.com/open-source/#osp
- Archived: no
- Disabled: no
- Pushed At: 2026-08-06T13:05:18Z
- Updated At: 2026-08-31T15:40:28Z
- Topics: None provided

## Evidence Anchors
- [github_repo] description :: Server automation framework and application (confidence 0.95)
- [github_repo] language :: Ruby (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
- [seed] repositories to chart.md :: - [ ] https://github.com/puppetlabs/puppet.git (confidence 0.50)
