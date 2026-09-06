---
type: "workflow"
status: "active"
triggers: ["pull data from an API", "ingest a dataset", "build a data pipeline", "ETL", "scrape a source", "load data into a warehouse", "integrate a third party feed"]
preconditions: ["you know one question the data must answer", "you have checked whether you are allowed to use it"]
stages: ["Find the source and read its terms", "Pull one page by hand", "Land it raw, unchanged", "Transform where the data is", "Schedule it only once it is boring"]
exit_criteria: "the pipeline runs unattended, fails loudly, and re-running it changes nothing"
anti_patterns: ["orchestration before a working script", "transforming during ingestion", "a warehouse before the data justifies one"]
---

# Workflow - Ingest An External Data Source

## Situation
There is data somewhere else that you need here. This has a well-worn order, and most of the pain comes from doing the last step first.

## Decide First
**What question must the data answer?** It determines which fields matter, which drives how much you keep and how you shape it. "All of it, just in case" is how a pipeline becomes a liability.

**Are you allowed?** Terms of use, rate limits, personal data. Cheap to check now, expensive to discover after you depend on it.

## Stage 1 - Find the source and read its terms
If you do not have a source yet, [[public-apis - public-apis]] is a directory of free and public APIs recording auth type, HTTPS and CORS for each — enough to shortlist before writing code. For public and government data, [[GSA - data.gov]] and [[ckan - ckan]] portals expose catalogues with structured metadata and an API behind the browsing UI; the CKAN API is usually a better integration point than the site it renders.

Read the rate limits now and write them down. They will shape the design, and finding them by getting blocked is a bad way to learn.

**Why now:** the source's shape constrains everything downstream, and swapping sources later invalidates the work.

## Stage 2 - Pull one page by hand
One request. Look at the actual response. Not the documentation — the response.

Documentation is aspirational; the payload is true. Nulls where the docs promise values, dates in three formats, pagination that behaves differently on the last page. You want these surprises now, in a scratch script, not inside an orchestrator.

**Why now:** every assumption you make here is one you would otherwise encode into a pipeline and debug later at ten times the cost.

**Not yet:** no scheduler, no framework, no warehouse. A script and your eyes.

## Stage 3 - Land it raw, unchanged
Write the response to storage exactly as received, before any parsing. Then transform from the stored copy.

This single decision saves more time than anything else here. When your parser turns out to be wrong — and it will — you re-parse from the raw copy instead of re-fetching, which may not even be possible if the source is rate-limited, paid, or mutable. It also gives you a truthful record of what the source actually said on a given day.

Keep the fetch dumb: retrieve, store, record what was retrieved and when. No cleverness in the fetch layer.

**Exit criterion:** you can delete every derived file and rebuild from raw.

## Stage 4 - Transform where the data is
Now shape it into the thing that answers your question.

For anything up to tens of gigabytes, [[duckdb - duckdb]] is the strong default: an in-process OLAP engine that queries Parquet, CSV and JSON files directly, with no server to run and no loading step. It removes the largest premature decision in most pipelines — that you need a warehouse — and if you outgrow it, the SQL transfers.

Once transformations multiply, [[dbt-labs - dbt-core]] adds the discipline: models are SQL files, dependencies are inferred from `ref()` calls rather than maintained by hand, and schema tests assert your assumptions so a broken upstream fails the build instead of quietly producing wrong numbers. Both sit under [[Pattern - Analytical Query Engine]] and [[Pattern - Schema Mapping]].

If the source is geospatial, the shape is different and specialised: [[OSGeo - gdal]] for format translation and reprojection, [[geopandas - geopandas]] for analysis, [[stac-utils - pystac]] for Earth-observation catalogues.

**Why now:** transformation is where the question gets answered; everything before was logistics.

**Not yet:** do not add a warehouse until DuckDB or its equivalent genuinely cannot cope. "We'll need it eventually" has funded a great many idle clusters.

## Stage 5 - Schedule it only once it is boring
When the pipeline has run by hand several times and stopped surprising you, automate it.

[[apache - airflow]] is the reference implementation of [[Pattern - Data Orchestration]]: tasks as a DAG, with retries, backfill and dependency awareness — the things cron cannot do. Its value is entirely in failure handling, which is why it comes *after* the pipeline works. Orchestrating a pipeline you do not yet trust means debugging two systems at once.

Three properties to get right, none of which are the scheduler's job:

- **Idempotency.** Re-running the same period produces the same result. Without this, retries corrupt.
- **Failure is loud.** A pipeline that fails silently is worse than none, because downstream consumers keep trusting stale data.
- **Backfill works.** You will need to reprocess history. Design for it now; retrofitting is painful.

**Why now:** automation multiplies whatever it is given. Automate something reliable and you get reliability at scale.

## Not Yet - The Steel Framing
- **A warehouse.** Local files and an in-process engine take you remarkably far.
- **Streaming.** Batch until latency is a stated requirement with a number attached.
- **A data catalogue for your own outputs.** Right at fifty datasets, overhead at three.
- **Great orchestration for one job.** One nightly job is a cron entry and a loud failure alert.

## Exit Criteria
It runs unattended, fails loudly, and re-running it changes nothing. Then answer the question you wrote at the start — and if the data does not answer it, that is the finding, not a failure.

## Applies These Patterns
- [[Pattern - ETL API Ingestion]]
- [[Pattern - Data Orchestration]]
- [[Pattern - Analytical Query Engine]]
- [[Pattern - Open Data Portal]]

## Related
- [[Topic - Data APIs & Big Data]]
- [[Workflow - Adopt A Dependency]]
