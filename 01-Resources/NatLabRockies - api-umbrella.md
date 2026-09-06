---
uuid: "118c38f4-98f4-524c-9bc3-e044dcc023ee"
canonical_url: "https://github.com/NatLabRockies/api-umbrella"
repo_key: "NatLabRockies/api-umbrella"
owner: "NatLabRockies"
repo_name: "api-umbrella"
aliases: ["NatLabRockies/api-umbrella", "https://github.com/NatLabRockies/api-umbrella"]
type: "infrastructure_tool"
primary_topic: "Infrastructure & Observability"
secondary_topics: ["Data APIs & Big Data", "Security & SIEM", "Government & Civic Tech"]
ecosystem: "Data_Platform"
domain_primary: "Infrastructure"
maturity_stage: "Production_Ready"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "CLI"
data_locality: "Distributed"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Open Data Portal", "Infrastructure as Code", "Observability Pipeline"]
glossary_terms: ["API", "Endpoint", "Schema", "Rate Limit", "Infrastructure as Code", "Monitoring", "Observability", "Telemetry", "Metrics"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
evidence_count: 6
github_description: "Open source API management platform"
github_language: "Ruby"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "main"
github_stars: 0
github_topics: ["api-gateway", "api-management", "api-manager", "lua", "luajit", "nginx", "openresty"]
github_homepage: ""
github_pushed_at: "2026-08-29T00:23:45Z"
github_updated_at: "2026-08-25T08:40:29Z"
---

# NatLabRockies - api-umbrella

## Bottom Line
An API management gateway that fronts several backend APIs with one endpoint, handling API keys, rate limiting and analytics in the proxy layer so each service does not implement them separately.

## What It Solves
- Stop reimplementing authentication, throttling and usage analytics in every API.
- Present APIs written in different languages, on different servers, behind one consistent endpoint and key scheme.
- Get usage analytics across all APIs without instrumenting each one.

## Architecture & Mechanics
- Nginx with OpenResty and Lua forms the gateway, applying policy to requests in flight.
- A configuration and admin backend manages API definitions, keys and rate limits.
- PostgreSQL holds configuration and account data; OpenSearch stores request analytics.
- Deployments front existing services rather than replacing them, so backends stay unchanged.

## What Is Inside
- **A polyglot gateway** — `src/api-umbrella/` (910 files): 254 `.lua` files are the nginx/OpenResty request path, 193 `.js` and 85 `.hbs` the Ember admin UI, 70 `.etlua` configuration templates.
- **A test suite larger than most projects** — `test/` (399 files; 446 test-related paths overall): `test/proxy/` (145) exercises gateway behaviour directly, `test/apis/` (94), `test/admin_ui/` (45) drives the UI, `test/factories/` (17), plus a GeoIP test database at `test/support/geoip/GeoIP2-City-Test.mmdb`.
- **An OpenAPI description of its own admin API** — `docs/admin/api-swagger.yml` and `docs/_static/admin-api-swagger.yml`.
- **Process supervision as templates** — `templates/etc/perp/` defines every service (envoy, an Ember dev server, an example Hugo website) as a `perp` runscript, a legible alternative to systemd unit sprawl.
- **Architecture drawn, not described** — `docs/images/overview.svg`, `gatekeeper.svg`, `router.svg`.
- **Deployment and package verification** — `Dockerfile`, `Dockerfile-opensearch`, `Dockerfile-postgres`, a Jenkinsfile, and `build/package/verify/spec/` which tests the *installed package* rather than the source tree.

## Transferable Capability
**Put a single layer in front of many services to handle everything that is not the service's job** — identifying the caller, rationing use, recording what happened — so no individual service implements any of it and none can implement it differently. The corollary is that the policy lives in one reviewable place rather than as a convention repeated hopefully across many.

**Alternative to:** each service handling its own identification and limits, which guarantees inconsistency and makes changing the policy an N-service task. **Applies wherever** several things are exposed to callers you do not control and the rules for callers should not be part of what is being called.

## Taxonomy
- Ecosystem: Data_Platform
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
- Put key management and rate limiting in front of APIs that lack them.
- Publish a coherent developer-facing API surface over disparate internal services.
- Study a production gateway used by api.data.gov and the NREL Developer Network.

## Semantic Links
- [parent_topic:: [[Topic - Infrastructure & Observability]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[puppetlabs - puppet]]]
- [related_to:: [[chef]]]
- [related_to:: [[hashicorp - terraform]]]
- [implements_pattern:: [[Pattern - Open Data Portal]]]
- [implements_pattern:: [[Pattern - Infrastructure as Code]]]
- [implements_pattern:: [[Pattern - Observability Pipeline]]]
- [mentions_term:: [[Glossary - API]]]
- [mentions_term:: [[Glossary - Endpoint]]]
- [mentions_term:: [[Glossary - Schema]]]
- [mentions_term:: [[Glossary - Rate Limit]]]
- [mentions_term:: [[Glossary - Infrastructure as Code]]]
- [mentions_term:: [[Glossary - Monitoring]]]
- [mentions_term:: [[Glossary - Observability]]]
- [mentions_term:: [[Glossary - Telemetry]]]

## Evidence
- Source URL: https://github.com/NatLabRockies/api-umbrella
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names MIT (reproduced in full). The GitHub API reported `UNKNOWN`, which is why this was read directly.

## GitHub Snapshot

- Description: Open source API management platform
- Language: Ruby
- License: Unknown (UNKNOWN)
- Default Branch: main
- Stars: 0
- Watchers: 0
- Homepage: None provided
- Archived: no
- Disabled: no
- Pushed At: 2026-08-29T00:23:45Z
- Updated At: 2026-08-25T08:40:29Z
- Topics: api-gateway, api-management, api-manager, lua, luajit, nginx, openresty

## Evidence Anchors
- [github_repo] description :: Open source API management platform (confidence 0.95)
- [github_repo] topics :: api-gateway, api-management, api-manager, lua, luajit, nginx, openresty (confidence 0.82)
- [github_repo] language :: Ruby (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
