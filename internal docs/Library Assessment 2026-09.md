---
type: "assessment"
status: "active"
assessed_on: "2026-09-01"
resource_notes: 64
total_notes: 173
verdict: "structurally sound, semantically thin, and not yet usable at the point of need"
---

# Library Assessment - September 2026

## Verdict
The vault is structurally excellent and semantically hollow. It has 64 resources, 76 glossary terms, 28 patterns and a nine-axis taxonomy, all correctly cross-linked. What it does not yet have is content that distinguishes one resource from another, or any way to reach the right material at the moment it is needed.

Three findings, in order of how much they cost.

## Finding 1 - Thirty-nine notes describe their topic, not themselves

Measured across the 41 bootstrap-era resource notes: their `What It Solves` sections collapse into **11 distinct blocks**, and 36 of the 41 share one of just six topic templates.

| Notes sharing one identical block | Template |
| --- | --- |
| 9 | "Automate deployments and configuration management…" |
| 6 | "Simulate bodies or physical systems…" |
| 6 | "Build or compare UI systems…" |
| 6 | "Scan for candidate tools or approaches…" |
| 5 | "Prototype assistants and agent workflows…" |
| 4 | "Study public-sector open-source practices…" |

The sharpest example is `[[asreview]]`, a tool for machine-assisted screening of research literature. Its note claims it solves:

> Simulate bodies or physical systems. Derive symbolic expressions or solve algebraic problems.

It says the same thing `[[sympy]]` says, because both were filed under Scientific Simulation and the section was filled from the topic, not the source. The only resource-specific sentence in those notes is the GitHub description.

This matters more than a cosmetic complaint. The whole promise of the catalogue is that an agent can retrieve *the right tool* for a problem. Retrieval over `What It Solves`, `Architecture & Mechanics` and `Integration & Use Cases` currently returns the topic every time. Roughly 60% of the resource layer is, for retrieval purposes, empty.

The 23 notes added this session and any future deep-dive output do not have this defect, because both are written from fetched evidence rather than a template.

## Finding 2 - The library is organised by what things are, never by what you are doing

Every index answers an ontological question: what kind of thing is this, what domain does it belong to, what pattern does it implement. Nothing answers the situational question: *I am about to do X — what here is relevant, and in what order?*

This is why the catalogue has not been used even by the project that built it. Which leads to the third finding.

## Finding 3 - We built the catalogue without reading it

Twelve resources already in this vault bear directly on the problems this project has spent its time solving from scratch:

| Resource | The problem it had already solved |
| --- | --- |
| [[asreview]] | Active learning: rank a corpus so the most informative item is screened next, human in the loop. This is the scouting cohort problem, exactly. |
| [[ckan - ckan]] | Dataset catalogue with extensible metadata schemas, harvesting between portals, faceted search, full API. A catalogue schema was designed here from first principles anyway. |
| [[dbt-labs - dbt-core]] | Dependency DAG inferred from `ref()` calls, plus declarative schema tests. The vault's link graph is that DAG; link-integrity checking is that test suite. |
| [[apache - airflow]] | Task DAG with retries, backfill and idempotency. A queue with leases and retry caps was hand-rolled instead. |
| [[stac-utils - pystac]] | A linked-JSON catalogue spec with validation and typed extensions. The paper layer was specified without consulting it. |
| [[SigmaHQ - sigma]] | Abstract definition plus field mapping plus per-backend compilation — the container and schema-mapping problem in another domain. |
| [[public-apis - public-apis]] | A directory of ~1,400 entries kept honest by automated link-health checks in CI. Dead-link handling was specified from scratch. |
| [[duckdb - duckdb]] | In-process OLAP over files. The whole vault's frontmatter could be queried as a table today, with no server. |
| [[osquery - osquery]] | State exposed as SQL virtual tables — the same idea applied to a filesystem. |
| [[cfpb - open-source-checklist]] | Checklist-as-governance for adopting open source. |
| [[goldbergyoni - nodebestpractices]] | The practice / rationale / consequence structure, which is the form a good workflow note takes. |
| [[orsinium-labs - generated-awesomeness]] | Lists that are generated rather than hand-maintained. |

None of these were consulted. The catalogue was treated as an output, never as an input — waiting for steel while sitting on a stack of usable timber.

## Two smaller defects

**The canvases are stale.** Every file in `05-Canvases` still dates from the original build. `Topic - Security & SIEM.canvas` contains two nodes and shows the topic as empty; it now holds five approved resources. The visual layer is displaying a library that no longer exists. Regenerating requires a build run.

**The root router does not route to a third of the vault.** `[[Master Index]]` lists eleven topics and four hubs. It does not reach `[[Paper Index]]`, the three schema specifications, or this note. A router that cannot reach its own newest layers is not doing its job.

## What Follows From This

In priority order:

1. **Rewrite the 39 templated notes from fetched evidence.** This is the single highest-value work available, and the scout pipeline's deep-dive stage already does exactly this job — the seed URLs are present, so it is a matter of running it rather than building anything.
2. **Add the situational layer** — `08-Workflows`, which this assessment is delivered alongside.
3. **Apply the twelve resources above to this project's own design**, starting with DuckDB for vault-wide queries and dbt's schema-test idea for link integrity.
4. Regenerate canvases; extend the Master Index.

Do not scout new material at volume until item 1 is done. Adding a thousand thin entries to six hundred thin entries makes the retrieval problem worse, not better.

## Related
- [[Workflow Index]]
- [[Workflow - Build A Knowledge Catalogue]]
- [[Schema Extension - Scouting Pipeline]]
- [[Master Index]]
