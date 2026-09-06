---
uuid: "894676bf-7a58-508e-a977-265840973a02"
canonical_url: "https://github.com/getsentry/sentry"
repo_key: "getsentry/sentry"
owner: "getsentry"
repo_name: "sentry"
aliases: ["getsentry/sentry", "https://github.com/getsentry/sentry"]
type: "infrastructure_tool"
primary_topic: "Infrastructure & Observability"
secondary_topics: ["Security & SIEM", "Government & Civic Tech"]
ecosystem: "Python"
domain_primary: "Infrastructure"
maturity_stage: "Production_Ready"
license_class: "Source_Available"
license_verified: "manual 2026-09-01"
deployment_target: "Server"
interface_protocol: "CLI"
data_locality: "Distributed"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "Procedural"
patterns: ["Infrastructure as Code", "Observability Pipeline"]
glossary_terms: ["Infrastructure as Code", "Monitoring", "Observability", "Telemetry", "Metrics"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "FSL-1.1"
source_file: "repositories to chart.md"
evidence_count: 5
github_description: "Developer-first error tracking and performance monitoring"
github_language: "Python"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "master"
github_stars: 0
github_topics: ["apm", "crash-reporting", "crash-reports", "csp-report", "devops", "django", "error-logging", "error-monitoring", "fair-source", "hacktoberfest", "monitor", "monitoring", "python", "sentry", "tag-production"]
github_homepage: "https://sentry.io"
github_pushed_at: "2026-08-31T17:20:53Z"
github_updated_at: "2026-08-31T16:47:41Z"
---

# getsentry - sentry

## Bottom Line
Error tracking and performance monitoring that ingests exceptions from SDKs across twenty-plus languages, groups repeat occurrences of the same fault into one issue, and keeps the stack trace and request context needed to diagnose it.

## What It Solves
- Turn a flood of individual exceptions into a ranked list of distinct problems.
- Preserve the context a stack trace alone lacks — release, user, request, breadcrumbs — at the moment of failure.
- Distinguish a newly introduced fault from a long-standing one, which is what decides whether to roll back.

## Architecture & Mechanics
- Official SDKs in over twenty languages capture exceptions and send structured events to the server.
- A Django/Python backend ingests and processes events; a TypeScript frontend renders issues, traces and replays.
- Fingerprinting groups occurrences of the same underlying fault into a single issue with a count and a first-seen release.
- Session replay and tracing sit alongside errors, so a fault can be followed back through the request path.
- It can be self-hosted or used as a service.

> Sentry uses a 'fair source' licence, not an OSI-approved open-source licence. Read the terms before embedding it in a product.

## What Is Inside
- **20,838 files, split almost evenly between a Django backend and a React front end** — `src/sentry/` (5,307 Python) and `static/app/` (8,481 files, 8,431 `.tsx`). `tests/` is 5,186 with 4,659 under `tests/sentry/`.
- **Snapshot testing at scale** — 1,496 `.pysnap` files, plus 2,382 fixture paths. Worth studying if you are deciding whether snapshot tests survive a codebase this size.
- **A documented public API generated from code** — `api-docs/` (45 files) with `components/schemas/` and `components/parameters/`, `src/sentry/apidocs/examples/` (per-endpoint example payloads), and CI that diffs the OpenAPI output on every PR (`.github/workflows/openapi-diff.yml`).
- **Benchmarks as committed executables** — `bin/benchmark-span-buffer`, `bin/benchmark_codeowners/`, `bin/benchmark_detectors`; 271 benchmark paths.
- **Integration test tiers against real services** — `tests/snuba/` (117), `tests/relay_integration/` (36), `tests/symbolicator/` (22), `tests/acceptance/` (55).
- **Ninety-eight agent-instruction paths, the most in this catalogue** — `.agents/skills/` with `SKILL.md`, `SPEC.md` and `references/` per skill, covering `analytics`, `react-component-documentation`, `generate-snapshot-tests`, `hybrid-cloud-test-gen` (with `references/api-gateway-tests.md`), plus an `agents.toml` at the root. If you want to see what a large codebase's agent-facing contribution layer looks like when taken seriously, this is the example.
- **Licence is the catch** — FSL-1.1, source-available, not open source; see `Reading Notes`.

## Transferable Capability
**Capture the state surrounding a failure at the moment it happens, and group failures by what makes them the same rather than by when they occurred.** A stream of individual failures is unreadable; the same failures collapsed into a class, counted, with one full example retained, is actionable. The grouping rule is the whole design — too coarse and distinct problems merge, too fine and one problem looks like a thousand. Separately, and unrelated to error handling: **the contribution procedure is written as executable skills with their own specifications and reference material**, so the mechanical parts of a change - test layout, documentation shape, generated artefacts - are performed rather than remembered.

**Alternative to:** logs, which record everything at the same priority and require you to already know what to look for. **Applies wherever** the same problem recurs and the useful question is *which problem is worst* rather than *what happened at 14:03*.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Infrastructure
- Maturity Stage: Production_Ready
- License Class: Source_Available
- Deployment Target: Server
- Interface Protocol: CLI
- Data Locality: Distributed
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: Procedural

## Integration & Use Cases
- Catch application faults that metrics register only as a rate change.
- Attribute a new class of error to the release that introduced it.
- Study issue grouping as the answer to alert fatigue in error reporting.

## Reading Notes
**Source-available under FSL-1.1, not open source.** The API reports
nothing; the licence was verified by hand on 2026-09-01 and recorded in
`.utility/library_config.json`. The Functional Source License permits use, modification and
redistribution except for competing commercial offerings, and converts to Apache-2.0 after two
years. Self-hosting for internal use is squarely permitted; building a product on it is not.

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
- Source URL: https://github.com/getsentry/sentry
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01

## GitHub Snapshot

- Description: Developer-first error tracking and performance monitoring
- Language: Python
- License: Functional Source License (fair source) (FSL-1.1) - GitHub reports this as unidentified
- Default Branch: master
- Stars: 0
- Watchers: 0
- Homepage: https://sentry.io
- Archived: no
- Disabled: no
- Pushed At: 2026-08-31T17:20:53Z
- Updated At: 2026-08-31T16:47:41Z
- Topics: apm, crash-reporting, crash-reports, csp-report, devops, django, error-logging, error-monitoring, fair-source, hacktoberfest, monitor, monitoring, python, sentry, tag-production

## Evidence Anchors
- [github_repo] description :: Developer-first error tracking and performance monitoring (confidence 0.95)
- [github_repo] topics :: apm, crash-reporting, crash-reports, csp-report, devops, django, error-logging, error-monitoring, fair-source, hacktoberfest, monitor, monitoring (confidence 0.82)
- [github_repo] language :: Python (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
