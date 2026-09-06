---
uuid: "3122a696-78fe-5fd5-90a9-2c65775d4aa4"
canonical_url: "https://github.com/hashicorp/terraform"
repo_key: "hashicorp/terraform"
owner: "hashicorp"
repo_name: "terraform"
aliases: ["hashicorp/terraform", "https://github.com/hashicorp/terraform"]
type: "infrastructure_tool"
primary_topic: "Infrastructure & Observability"
secondary_topics: ["Security & SIEM", "Government & Civic Tech"]
ecosystem: "Go"
domain_primary: "Infrastructure"
maturity_stage: "Production_Ready"
license_class: "Source_Available"
license_verified: "manual 2026-09-01"
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
license: "BUSL-1.1"
source_file: "repositories to chart.md"
evidence_count: 5
github_description: "Terraform enables you to safely and predictably create, change, and improve infrastructure. It is a source-available tool that codifies APIs into declarative configuration files that can be shared amongst team members, treated as code, edited, reviewed, and versioned."
github_language: "Go"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "main"
github_stars: 0
github_topics: ["cloud", "cloud-management", "graph", "infrastructure-as-code", "terraform"]
github_homepage: "http://developer.hashicorp.com/terraform"
github_pushed_at: "2026-08-31T15:01:32Z"
github_updated_at: "2026-08-31T15:05:57Z"
---

# hashicorp - terraform

## Bottom Line
Declarative infrastructure provisioning: you describe the resources you want, Terraform builds a dependency graph, and it shows you an execution plan of exactly what will change before anything is touched.

## What It Solves
- See what a change will do to live infrastructure before applying it, rather than discovering it afterwards.
- Reproduce an environment from version-controlled configuration instead of remembered console steps.
- Coordinate resources across several providers in one dependency-ordered run.

## Architecture & Mechanics
- Configuration files declare desired resources; the CLI reconciles them against recorded state.
- A graph engine resolves dependencies between resources and parallelises the ones that are independent.
- The plan step renders the diff — create, update, destroy — as an artefact to review before applying.
- A provider plugin system adapts the same core to each cloud, SaaS or on-premises API.

> Terraform moved to the Business Source License 1.1 and is source-available, not open source. This is a licence to read carefully before adoption.

## What Is Inside
- **The testdata is the resource** — 2,846 fixture paths and 1,757 `.tf` files, almost all under `internal/*/testdata/`, each directory a named scenario (`apply-check/`, `apply-error/`, `apply-empty/`, `dynamic-module-sources/`) with its configuration and expected outcome. 210 `.tfstate` files show real state-file shapes across versions. If you need valid or deliberately broken HCL, or a state file to parse, this is where it is.
- **The provider protocol as protobuf** — `docs/plugin-protocol/tfplugin5.proto` and `tfplugin6.proto`, plus `internal/cloudplugin/cloudproto1/`. The plugin boundary is a published, versioned contract, which is the transferable design.
- **Equivalence testing as a separate discipline** — `testing/equivalence-tests/` (475 files) checks that a change produces identical output across a corpus, with its own CI action (`.github/actions/equivalence-test/`).
- **The core, by concern** — `internal/`: `command/` (1,560), `terraform/` (838, the graph and evaluation), `configs/` (500, HCL loading), `stacks/` (488), `backend/` (239), `states/` (91).
- **An architecture document** — `docs/architecture.md`, plus VS Code debug configurations for stepping through the test suite (`docs/debugging-configs/`).
- **Changelog as dated fragments** — `.changes/v1.15/`, `.changes/v1.16/` with one YAML per entry.
- **Licence is the catch** — BUSL-1.1, source-available; see `Reading Notes`.

## Transferable Capability
**Keep an explicit record of what you believe exists, and reconcile it against reality to derive the change.** The stored belief is what makes the difference computable: without it you can only create or destroy, not converge. The second, separable idea is **a published, versioned protocol at the plugin boundary**, so the thing being managed and the thing managing it can be built and released by different people.

**Alternative to:** issuing commands and hoping, with no representation of what should exist; and to plugins as in-process code, which couples every integration's release to the core's. **Applies wherever** something long-lived must be brought to a described state and the difference matters more than the destination.

## Taxonomy
- Ecosystem: Go
- Domain Primary: Infrastructure
- Maturity Stage: Production_Ready
- License Class: Source_Available
- Deployment Target: Server
- Interface Protocol: CLI
- Data Locality: Distributed
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Provision an environment reproducibly and review changes as a diff.
- Manage resources spanning several providers with correct ordering.
- Study plan-then-apply as a general safety pattern for destructive automation.

## Reading Notes
**Source-available, not open source, and the API will not tell you.**
GitHub reports `NOASSERTION`; a manual check recorded on 2026-09-01 in
`.utility/library_config.json` confirms **BUSL-1.1**, the Business Source License. The source
is readable and modifiable, but production use competing with HashiCorp's offering is
restricted until each version's change date. Every version before the relicense remains
MPL-2.0, which is why forks exist — if Terraform is being evaluated as a donor rather than a
tool, the fork lineage matters more than this repository does.

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
- Source URL: https://github.com/hashicorp/terraform
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01

## GitHub Snapshot

- Description: Terraform enables you to safely and predictably create, change, and improve infrastructure. It is a source-available tool that codifies APIs into declarative configuration files that can be shared amongst team members, treated as code, edited, reviewed, and versioned.
- Language: Go
- License: Business Source License 1.1 (BUSL-1.1) - GitHub reports this as unidentified
- Default Branch: main
- Stars: 0
- Watchers: 0
- Homepage: http://developer.hashicorp.com/terraform
- Archived: no
- Disabled: no
- Pushed At: 2026-08-31T15:01:32Z
- Updated At: 2026-08-31T15:05:57Z
- Topics: cloud, cloud-management, graph, infrastructure-as-code, terraform

## Evidence Anchors
- [github_repo] description :: Terraform enables you to safely and predictably create, change, and improve infrastructure. It is a source-available tool that codifies APIs into declarative configuration files that can be shared amongst team members, t [truncated] (confidence 0.95)
- [github_repo] topics :: cloud, cloud-management, graph, infrastructure-as-code, terraform (confidence 0.82)
- [github_repo] language :: Go (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
