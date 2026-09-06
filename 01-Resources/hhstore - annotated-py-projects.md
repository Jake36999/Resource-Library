---
uuid: "f37df8fe-beb0-5c1e-8538-1dc93dce0344"
canonical_url: "https://github.com/hhstore/annotated-py-projects"
repo_key: "hhstore/annotated-py-projects"
owner: "hhstore"
repo_name: "annotated-py-projects"
aliases: ["hhstore/annotated-py-projects", "https://github.com/hhstore/annotated-py-projects"]
type: "curated_aggregator"
primary_topic: "Curated Aggregators & Reference Lists"
secondary_topics: ["Architecture & Developer Playbooks", "Frontend & Design Systems"]
ecosystem: "Markdown"
domain_primary: "Discovery"
maturity_stage: "Reference"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Markdown"
data_locality: "Stateless"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Curated Resource Curation", "Reference Architecture"]
glossary_terms: ["Architecture", "Async", "ASGI", "Dependency Injection", "Curation", "Taxonomy", "Reference List", "Discovery", "Annotated Example"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
evidence_count: 6
github_description: "fastapi/flask/sanic/asyncio/bottle/webpy 等源码注解合集"
github_language: "Python"
github_license: "Unknown"
github_license_spdx: "UNKNOWN"
github_default_branch: "master"
github_stars: 0
github_topics: ["annotated", "anyio", "asyncio", "bottle", "fastapi", "flask", "python", "sanic", "starlette", "webpy"]
github_homepage: ""
github_pushed_at: "2023-12-21T00:05:44Z"
github_updated_at: "2026-08-21T02:11:23Z"
---

# hhstore - annotated-py-projects

## Bottom Line
Source code of well-known Python web frameworks and async libraries with line-level annotations added, kept as a study resource — including several versions of the same project so its evolution can be traced.

## What It Solves
- Learn how a real framework is implemented rather than only how to use it.
- Follow unfamiliar code with commentary rather than reading it cold.
- See how a design changed across versions of the same project.

## Architecture & Mechanics
- Annotated source for FastAPI, Flask, Sanic, Bottle and Webpy, plus asyncio, anyio and starlette.
- Annotations are added inline to the original source rather than written as separate prose.
- Multiple versions of some projects are kept side by side to show evolution.
- Annotations are largely in Chinese.

## What Is Inside
- **Vendored source of eight real projects, annotated line by line in Chinese** — this is not a link list. `fastapi/fastapi-0.103.1/` (585 files), `asyncio/asyncio-3.4.3/` (75), `starlette/starlette-0.31.1/` (73), `anyio/anyio-4.0.0/` (64), `sanic/sanic-0.1.9/` (61), `flask/` (25), `bottle/` (5), `webpy/` (2). 837 `.py` files in total.
- **Each copy is version-pinned in its directory name**, so the annotations refer to a fixed state of the code rather than drifting against upstream — an unusually disciplined choice for this kind of project.
- **The upstream examples and docs come with it** — `asyncio-3.4.3/examples/` (`crawl.py`, `cache_clt.py`, `cache_svr.py`), FastAPI's `docs_src/` tutorial sources including `separate_openapi_schemas/` variants per Python version. 466 example paths overall.
- **What it is actually for:** reading a framework's internals with a guide, one release at a time. FastAPI, Starlette and AnyIO together are a complete ASGI stack, annotated at the same moment, which is hard to assemble any other way.
- **Caveat:** the annotations are in Chinese, and the vendored copies are frozen at 2023-era releases.

## Transferable Capability
**Freeze a specific version of a real system and annotate it in place, so the explanation and the code cannot drift apart.** Commentary written against a moving target is wrong within a release; pinning the version makes the annotation permanently true of *something*. The related move: **annotate several layers of one stack captured at the same moment**, so the interactions between them are legible in a way no single project's documentation shows.

**Alternative to:** explaining a system from the outside while it changes underneath; and to reading one layer at a time. **Applies wherever** somebody must understand how a real system actually works rather than how it is described.

## Taxonomy
- Ecosystem: Markdown
- Domain Primary: Discovery
- Maturity Stage: Reference
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Markdown
- Data Locality: Stateless
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Study framework internals with guidance.
- Compare how several Python web frameworks solve the same problems.
- Trace design changes across versions of one codebase.

## Semantic Links
- [parent_topic:: [[Topic - Curated Aggregators & Reference Lists]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[orsinium-labs - generated-awesomeness]]]
- [related_to:: [[pracdata - awesome-open-source-data-engineering]]]
- [related_to:: [[The-Cool-Coders - Project-Ideas-And-Resources]]]
- [implements_pattern:: [[Pattern - Curated Resource Curation]]]
- [implements_pattern:: [[Pattern - Reference Architecture]]]
- [mentions_term:: [[Glossary - Architecture]]]
- [mentions_term:: [[Glossary - Async]]]
- [mentions_term:: [[Glossary - ASGI]]]
- [mentions_term:: [[Glossary - Dependency Injection]]]
- [mentions_term:: [[Glossary - Curation]]]
- [mentions_term:: [[Glossary - Taxonomy]]]
- [mentions_term:: [[Glossary - Reference List]]]
- [mentions_term:: [[Glossary - Discovery]]]

## Evidence
- Source URL: https://github.com/hhstore/annotated-py-projects
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names MIT (reproduced in full). The GitHub API reported `UNKNOWN`, which is why this was read directly.

## GitHub Snapshot

- Description: fastapi/flask/sanic/asyncio/bottle/webpy 等源码注解合集
- Language: Python
- License: Unknown (UNKNOWN)
- Default Branch: master
- Stars: 0
- Watchers: 0
- Homepage: None provided
- Archived: no
- Disabled: no
- Pushed At: 2023-12-21T00:05:44Z
- Updated At: 2026-08-21T02:11:23Z
- Topics: annotated, anyio, asyncio, bottle, fastapi, flask, python, sanic, starlette, webpy

## Evidence Anchors
- [github_repo] description :: fastapi/flask/sanic/asyncio/bottle/webpy 等源码注解合集 (confidence 0.95)
- [github_repo] topics :: annotated, anyio, asyncio, bottle, fastapi, flask, python, sanic, starlette, webpy (confidence 0.82)
- [github_repo] language :: Python (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
