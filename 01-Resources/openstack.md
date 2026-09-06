---
uuid: "b56e126d-399b-5a63-a14c-51018256c69b"
canonical_url: "https://github.com/openstack/openstack"
repo_key: "openstack/openstack"
owner: "openstack"
repo_name: "openstack"
aliases: ["openstack/openstack", "https://github.com/openstack/openstack"]
type: "infrastructure_tool"
primary_topic: "Infrastructure & Observability"
secondary_topics: ["Security & SIEM", "Government & Civic Tech"]
ecosystem: "Python"
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
github_description: "Repository tracking all OpenStack repositories as submodules. Mirror of code maintained at opendev.org."
github_language: "Python"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "master"
github_stars: 0
github_topics: []
github_homepage: "https://opendev.org/openstack/openstack"
github_pushed_at: "2026-08-31T17:00:58Z"
github_updated_at: "2026-08-31T17:13:05Z"
---

# openstack

## Bottom Line
Not OpenStack itself but a superproject: a read-only repository of git submodules pinning the exact commit of every OpenStack component that was tested together, so each commit here is a combination known to work.

## What It Solves
- Identify which versions of hundreds of interdependent projects were validated as a set.
- Avoid assembling a working combination by hand across separately versioned repositories.
- Give a single reference point for a release built from many moving parts.

## Architecture & Mechanics
- The repository contains git submodules rather than source, each pointing at a component repository on opendev.org.
- Submodules span core services such as Nova and Cinder through to Ansible roles and deployment charms.
- Each commit corresponds to a combination the Zuul CI system tested together.
- The result is a sequence of explicitly validated snapshots rather than a codebase.

## What Is Inside
- **691 files at the root and nothing else — this is a manifest repository, not code.** Each entry is a pointer to one of OpenStack's ~690 component repositories (`barbican-specs`, `charm-designate`, `cookbook-openstack-block-storage`, `ansible-role-atos-hsm`, `oslo.db`, `oslo.log`…). Cloning it gets you the index, not the platform.
- **What the index reveals** — the shape of the project: 73 IaC paths are `ansible-role-*` and `ansible-config_template` entries; 17 are Chef `cookbook-openstack-*`; a large block is `charm-*` Juju charms; another is `*-specs` repositories holding design specifications separately from implementations.
- **The one document worth reading here** — `README.rst`, which explains the governance model that produces this layout.
- **What to do with it:** treat it as a directory for locating the component you actually want. The reference architecture people usually mean is in the individual `*-specs` repositories, and the deployment tooling is in `openstack-ansible-*`, `charm-*` or `cookbook-*` depending on which ecosystem you are in.

## Transferable Capability
**Publish an index of parts rather than a bundle of them, and keep the design argument in a different place from the implementation.** Specifications live in their own repositories, so a decision can be reviewed, disagreed with and superseded without touching code, and the code cannot silently become the only record of what was intended.

**Alternative to:** a single repository containing everything, where the boundaries between components exist only as directory names; and to design intent recorded in commit messages. **Applies wherever** a system is large enough that its parts have different lifecycles — and the specification-separate-from-implementation idea applies at any size.

## Taxonomy
- Ecosystem: Python
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
- Pin a known-good combination of OpenStack components.
- Study the superproject pattern for coordinating a very large multi-repository system.
- Trace which component versions were exercised together by CI.

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
- Source URL: https://github.com/openstack/openstack
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names Apache-2.0 (reproduced in full). The GitHub API reported `UNKNOWN`, which is why this was read directly.

## GitHub Snapshot

- Description: Repository tracking all OpenStack repositories as submodules. Mirror of code maintained at opendev.org.
- Language: Python
- License: Unknown (UNKNOWN)
- Default Branch: master
- Stars: 0
- Watchers: 0
- Homepage: https://opendev.org/openstack/openstack
- Archived: no
- Disabled: no
- Pushed At: 2026-08-31T17:00:58Z
- Updated At: 2026-08-31T17:13:05Z
- Topics: None provided

## Evidence Anchors
- [github_repo] description :: Repository tracking all OpenStack repositories as submodules. Mirror of code maintained at opendev.org. (confidence 0.95)
- [github_repo] language :: Python (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
- [seed] repositories to chart.md :: - [ ] https://github.com/openstack/openstack.git (confidence 0.50)
