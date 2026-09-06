---
uuid: "f880e8e8-5b27-5c15-bd5c-604ec7af4294"
canonical_url: "https://github.com/DataWithBaraa/databricks_bootcamp_2026"
repo_key: "DataWithBaraa/databricks_bootcamp_2026"
owner: "DataWithBaraa"
repo_name: "databricks_bootcamp_2026"
aliases: ["DataWithBaraa/databricks_bootcamp_2026", "https://github.com/DataWithBaraa/databricks_bootcamp_2026"]
type: "tutorial"
primary_topic: "Data APIs & Big Data"
secondary_topics: ["Data Lineage & Provenance"]
ecosystem: "Data_Platform"
domain_primary: "Data"
maturity_stage: "Active"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "Python_SDK"
data_locality: "Distributed"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Medallion Layering", "Data Orchestration", "Reference Architecture"]
glossary_terms: ["Medallion Architecture", "Data Engineering", "ELT", "Semantic Layer"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: "End-to-end Data Lakehouse project built on Databricks, following the Medallion Architecture (Bronze, Silver, Gold). Covers real-world data engineering and analytics workflows using Spark, PySpark, SQL, Delta Lake, and Unity Catalog. Designed for learning, portfolio building, and job interviews."
github_language: "Jupyter Notebook"
github_license_spdx: "MIT"
github_default_branch: "main"
github_stars: 405
github_topics: ["ai", "apache-spark", "data-analytics", "data-engineering", "data-engineering-project", "data-lakehouse", "data-pipeline", "databricks", "etl", "lakehouse", "medallion-architecture", "protfolio-project", "pyspark", "python", "spark", "spark-sql", "unity-catalog"]
github_homepage: "https://www.youtube.com/playlist?list=PLNcg_FV9n7qZoxVkw-KPhcmgLWjHWVUc9"
github_pushed_at: "2026-01-19T18:31:09Z"
---
# DataWithBaraa - databricks_bootcamp_2026

## Bottom Line
A complete medallion-architecture lakehouse in fourteen notebooks, with two versions of the bronze layer — a basic one and an improved one — kept side by side so the difference between a first attempt and a considered one is readable.

## What It Solves
- Follow a lakehouse from raw files to dimensional model without gaps between the steps.
- See what a naive ingestion layer gets wrong, by comparing it to the corrected version.
- Practise on multi-source data that needs joining rather than one clean table.

## Architecture & Mechanics
- The three layers are three directories, so the architecture is the file system: `script/bronze` (2 notebooks), `script/silver` (7), `script/gold` (4).
- **`bronze_layer(basic).ipynb` and `bronze_layer_(improved).ipynb` are both kept.** The improvement is legible as a diff instead of being folded silently into a finished answer — the single most useful thing in the repository.
- The gold layer is dimensional and named as such: `gold_dim_customers`, `gold_dim_products`, `gold_fact_sales`, plus `gold_orchestration.ipynb` — the point where a lakehouse becomes a star schema, and the orchestration that sequences it.
- Sources are deliberately plural: `datasets/engineering/source_crm/` (`cust_info.csv`, `prd_info.csv`) plus further sources, so the silver layer has real integration work to do rather than a single cleanup.
- **Not read:** any notebook. The layering is read off directory and file names.

## What Is Inside
- **Two versions of the bronze layer** — basic and improved, both committed.
- **Fourteen notebooks** — bronze (2), silver (7), gold (4), plus orchestration. Silver being the largest is correct and instructive: cleaning and conforming is where the work is.
- **Ten CSVs across two audiences** — `datasets/engineering/` (CRM and other source systems, for the pipeline) and `datasets/analysts/` (`sales_dataset/` with `dim_customers.csv`, `dim_products.csv`, `fact_sales.csv`, and an `hr_dataset/`), for the analysis side.
- **A YouTube playlist** as the homepage — the explanation is video, and the repository is the artefact that accompanies it.
- **Not here:** Databricks, Unity Catalog, or any Spark cluster. All are assumed.

## Transferable Capability
**Keep the naive version next to the improved one.** Teaching material almost always presents only the finished answer, which hides the reasoning entirely — the reader sees what to do and learns nothing about why the obvious approach fails. Committing both makes the improvement inspectable and turns a tutorial into an argument. The **layering principle** underneath is separately portable: grading material by refinement, with each stage rebuildable from the one before, means a mistake is corrected by replaying rather than by patching in place — a shape that applies to any staged transformation, not only to data lakehouses.

**Alternative to:** a single finished pipeline, which is shorter and unfalsifiable; and to a written list of best practices, which cannot be run against the mistake it warns about. **Applies wherever** a process has an obvious wrong answer that is worth showing — which is most processes worth teaching.

## Taxonomy
- Ecosystem: Data_Platform
- Domain Primary: Data
- Maturity Stage: Active
- License Class: Permissive
- Deployment Target: Server
- Interface Protocol: Python_SDK
- Data Locality: Distributed
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Read the two bronze notebooks together before designing an ingestion layer.
- Take the both-versions convention into any internal teaching material or design record.
- Reuse `datasets/` as multi-source sample data for pipeline work outside Databricks entirely.

## Reading Notes
405 stars in under a year, created 2026-01-14 — visible and new. Two limits: it assumes Databricks and Unity Catalog throughout, so the *architecture* transfers and the code does not; and the explanation lives in a YouTube playlist rather than in the repository, so a reader who only clones gets the artefacts without the reasoning. The GitHub description states the intent plainly — learning, portfolio and interviews — and it should be judged as that rather than as production material.

## Semantic Links
- [parent_topic:: [[Topic - Data APIs & Big Data]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[Victor-Kipruto-Rop - medallion-lakehouse-platform]]]
- [related_to:: [[carter-kilgour - delta-quality-testing]]]
- [related_to:: [[dbt-labs - dbt-core]]]
- [related_to:: [[PHACDataHub - data-mesh-ref-impl]]]
- [implements_pattern:: [[Pattern - Medallion Layering]]]
- [implements_pattern:: [[Pattern - Data Orchestration]]]
- [implements_pattern:: [[Pattern - Reference Architecture]]]
- [mentions_term:: [[Glossary - Medallion Architecture]]]
- [mentions_term:: [[Glossary - Data Engineering]]]
- [mentions_term:: [[Glossary - ELT]]]
- [mentions_term:: [[Glossary - Semantic Layer]]]

## Evidence
- Source URL: https://github.com/DataWithBaraa/databricks_bootcamp_2026
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata, the complete file tree at HEAD, and the LICENSE file; no notebook or CSV was opened

## GitHub Snapshot

- Description: End-to-end Data Lakehouse project built on Databricks, following the Medallion Architecture (Bronze, Silver, Gold). Covers real-world data engineering and analytics workflows using Spark, PySpark, SQL, Delta Lake, and Unity Catalog. Designed for learning, portfolio building, and job interviews.
- Language: Jupyter Notebook
- License (SPDX): MIT
- Default Branch: main
- Stars: 405
- Homepage: https://www.youtube.com/playlist?list=PLNcg_FV9n7qZoxVkw-KPhcmgLWjHWVUc9
- Pushed At: 2026-01-19T18:31:09Z
- Topics: ai, apache-spark, data-analytics, data-engineering, data-engineering-project, data-lakehouse, data-pipeline, databricks, etl, lakehouse, medallion-architecture, protfolio-project, pyspark, python, spark, spark-sql, unity-catalog

## Evidence Anchors
- [github_repo] description :: End-to-end Data Lakehouse project built on Databricks, following the Medallion Architecture (Bronze, Silver, Gold). Covers real-world data engineering and analytics workflows using Spark, PySpark, SQL, Delta Lake, and Unity Catalog. Designed for learning, portfolio building, and job interviews. (confidence 0.95)
- [github_repo] language :: Jupyter Notebook (confidence 0.90)
- [github_repo] license :: MIT (confidence 0.90)
- [github_repo] topics :: ai, apache-spark, data-analytics, data-engineering, data-engineering-project, data-lakehouse, data-pipeline, databricks, etl, lakehouse, medallion-architecture, protfolio-project, pyspark, python, spark, spark-sql, unity-catalog (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 27 paths at HEAD (confidence 0.95)
