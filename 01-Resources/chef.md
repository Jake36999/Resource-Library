---
uuid: "ee81f567-3570-5cd7-a64c-4162dd2bc9b7"
canonical_url: "https://github.com/chef/chef"
repo_key: "chef/chef"
owner: "chef"
repo_name: "chef"
aliases: ["chef/chef", "https://github.com/chef/chef"]
type: "infrastructure_tool"
primary_topic: "Infrastructure & Observability"
secondary_topics: ["Security & SIEM", "Government & Civic Tech"]
ecosystem: "Infrastructure_Automation"
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
evidence_count: 6
github_description: "Chef Infra, a powerful automation platform that transforms infrastructure into code automating how infrastructure is configured, deployed and managed across any environment, at any scale"
github_language: "Ruby"
github_license: "Unknown"
github_license_spdx: "APACHE-2.0"
github_default_branch: "main"
github_stars: 0
github_topics: ["automation", "cfgmgt", "chef", "deployment", "devops", "hacktoberfest", "infrastructure"]
github_homepage: "http://www.chef.io/chef/"
github_pushed_at: "2026-09-04T22:23:43Z"
github_updated_at: "2026-08-30T18:33:21Z"
---

# chef

## Bottom Line
Configuration management that applies Ruby-defined recipes to machines through an agent, converging each node to a declared state idempotently rather than running a script once and hoping.

## What It Solves
- Keep fleets of machines in a known configuration instead of drifting away from it.
- Re-run the same definition safely, since converging an already-correct system changes nothing.
- Express configuration in a real programming language when declarative syntax runs out.

## Architecture & Mechanics
- A chef-client agent runs on each managed node and enforces the configuration defined for it.
- Recipes group into cookbooks; resources declare desired state and providers know how to reach it on each platform.
- Convergence is idempotent — the agent inspects current state and acts only where it differs.
- The codebase is over 98% Ruby, with shell and PowerShell layers for cross-platform support, and kitchen-tests exercising real operating systems.

## What Is Inside
- **Half the repository is its test suite** — `spec/` (1,135 files): `unit/` (530), `spec/data/` (379 fixtures including real package databases at `spec/data/apt/var/www/apt/db/*.db`), `functional/` (139, tests that actually touch a system), `integration/` (29) and `stress/` (3). 1,267 test-related paths in total.
- **The resource DSL is the reusable idea** — `lib/chef/` (811 files) with one class per manageable resource (package, service, file, user, mount…), each declaring desired state and its own idempotent provider. That pattern transfers to any convergence system.
- **Design documents kept in-tree** — `docs/dev/design_documents/` (`action_collection.md`, `cookbook_root_aliases.md`, `ohai_cookbook_segment.md`) and `docs/dev/how_to/`, including running a cookbook as a Habitat package.
- **End-to-end verification against real machines** — `kitchen-tests/` (96 files) with `cookbooks/` (66), driven by Test Kitchen; `spec/integration/target_mode/support/docker/linux-ssh/Dockerfile` provides a target host.
- **A release pipeline as configuration** — `.expeditor/` (41 files) defines build, promote and test stages declaratively rather than as scripts.

## Transferable Capability
**Declare the state a thing should be in, and let a provider work out what to do about it — including doing nothing.** The unit is the desired outcome, not the command, which makes repeated application safe and makes the description of a system readable as a specification. The second move: **one resource kind per manageable concern, each with its own provider per platform**, so platform differences are contained rather than spread through the description.

**Alternative to:** scripts of commands, which are correct once and unsafe to re-run; and to platform conditionals scattered through the description. **Applies wherever** something must be brought to a known state repeatedly, from an unknown starting state.

## Taxonomy
- Ecosystem: Infrastructure_Automation
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
- Manage server configuration where logic and conditionals are genuinely needed.
- Compare agent-based convergence against agentless push models.
- Study idempotent resource providers as a durable automation pattern.

## Semantic Links
- [parent_topic:: [[Topic - Infrastructure & Observability]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[NatLabRockies - api-umbrella]]]
- [related_to:: [[puppetlabs - puppet]]]
- [related_to:: [[hashicorp - terraform]]]
- [implements_pattern:: [[Pattern - Infrastructure as Code]]]
- [implements_pattern:: [[Pattern - Observability Pipeline]]]
- [mentions_term:: [[Glossary - Infrastructure as Code]]]
- [mentions_term:: [[Glossary - Monitoring]]]
- [mentions_term:: [[Glossary - Observability]]]
- [mentions_term:: [[Glossary - Telemetry]]]
- [mentions_term:: [[Glossary - Metrics]]]

## Evidence
- Source URL: https://github.com/chef/chef
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names Apache-2.0 (reproduced in full). The GitHub API reported `UNKNOWN`, which is why this was read directly.

## GitHub Snapshot

- Description: Chef Infra, a powerful automation platform that transforms infrastructure into code automating how infrastructure is configured, deployed and managed across any environment, at any scale
- Language: Ruby
- License: Unknown (UNKNOWN)
- Default Branch: main
- Stars: 0
- Watchers: 0
- Homepage: http://www.chef.io/chef/
- Archived: no
- Disabled: no
- Pushed At: 2026-08-31T16:23:14Z
- Updated At: 2026-08-30T18:33:21Z
- Topics: automation, cfgmgt, chef, deployment, devops, hacktoberfest, infrastructure

## Evidence Anchors
- [github_repo] description :: Chef Infra, a powerful automation platform that transforms infrastructure into code automating how infrastructure is configured, deployed and managed across any environment, at any scale (confidence 0.95)
- [github_repo] topics :: automation, cfgmgt, chef, deployment, devops, hacktoberfest, infrastructure (confidence 0.82)
- [github_repo] language :: Ruby (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
