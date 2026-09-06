---
uuid: "c3392c6f-ee91-5139-ae56-fc45b159e32e"
canonical_url: "https://github.com/Azure-Samples/academic-knowledge-analytics-visualization"
repo_key: "Azure-Samples/academic-knowledge-analytics-visualization"
owner: "Azure-Samples"
repo_name: "academic-knowledge-analytics-visualization"
aliases: ["Azure-Samples/academic-knowledge-analytics-visualization", "https://github.com/Azure-Samples/academic-knowledge-analytics-visualization"]
type: "reference_implementation"
primary_topic: "Knowledge Management"
secondary_topics: ["Data APIs & Big Data"]
ecosystem: "Data_Platform"
domain_primary: "Knowledge_Management"
maturity_stage: "Abandoned"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "GUI"
data_locality: "Distributed"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Knowledge Graph Routing", "Metadata Harvesting", "Analytical Query Engine"]
glossary_terms: ["Knowledge Graph", "OLAP", "Dataset", "Taxonomy"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 5
github_description: "Various examples to perform big data analytics over Microsoft Academic Graph and visualize the results."
github_language: "C#"
github_license_spdx: "MIT"
github_default_branch: "master"
github_stars: 62
github_pushed_at: "2020-10-21T01:35:55Z"
---
# Azure-Samples - academic-knowledge-analytics-visualization

## Bottom Line
Analytics over the Microsoft Academic Graph — a citation and authorship graph of hundreds of millions of papers — written as thirteen U-SQL scripts with thirteen matching Power BI reports, which is what querying a graph of that size looked like before graph databases were expected to handle it.

## What It Solves
- Compute over a graph too large for any single graph database to hold.
- Answer bibliometric questions — influence, collaboration, field evolution — as batch jobs.
- Get from a distributed query result to a visual report without an intermediate application.

## Architecture & Mechanics
- The approach is deliberately not a graph database: thirteen `.usql` scripts run distributed batch queries over the graph *as files*, treating traversal as a join problem rather than as pointer chasing.
- Every script is paired with a Power BI artefact — 13 `.pbix` (reports) and 13 `.pbit` (templates) — so a query and its presentation are one deliverable. The template/report split means someone else can point the same visual at their own result.
- 13 C# files supply the user-defined functions that U-SQL alone cannot express.
- 41 images against 18 Markdown files: the documentation is mostly screenshots, which is a real limitation for a reader who cannot run it.
- **Not read:** any U-SQL, C# or report file. The above is read off file extensions, counts and the pairing between them.

## What Is Inside
- **Thirteen U-SQL analytics scripts** — `src/AcademicAnalytics/` (66 files total), each a distributed batch query over the academic graph.
- **Thirteen Power BI reports and thirteen templates** — `.pbix` and `.pbit`, paired one-to-one with the scripts.
- **Thirteen C# user-defined functions** — the escape hatch where declarative querying runs out.
- **Forty-one screenshots** — `images/`: the primary documentation, and 334 MB of the repository's weight.
- **Not here:** the Microsoft Academic Graph itself, which was retired at the end of 2021. See Reading Notes.

## Transferable Capability
**Treat graph traversal as a distributed join when the graph will not fit anywhere.** Above a certain size the graph-database assumption inverts: pointer chasing needs locality, and locality is exactly what you lose when the data is spread across a cluster, so a batch join expressed declaratively wins. Knowing where that crossover lies is the durable knowledge here, and it is not obvious from either side. The second, cheaper idea is **pairing every query with a report template**: shipping the visualisation as a template rather than a finished report means the analysis is reusable by someone with different data, which is the difference between publishing a result and publishing a method.

**Alternative to:** loading everything into a graph database, which is right up to a size and catastrophic past it; and to publishing query results as static charts, which cannot be re-pointed at new data. **Applies wherever** relationship analysis must run over data too large for a single specialised store — citation networks, dependency graphs, transaction networks, telemetry.

## Taxonomy
- Ecosystem: Data_Platform
- Domain Primary: Knowledge_Management
- Maturity Stage: Abandoned
- License Class: Permissive
- Deployment Target: Server
- Interface Protocol: GUI
- Data Locality: Distributed
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Read the U-SQL scripts as worked bibliometric queries — influence, collaboration, field evolution — translatable to any distributed SQL engine.
- Adopt the query-plus-template pairing so an analysis ships with a reusable presentation rather than a screenshot.
- Use it as the reference point for when a graph outgrows a graph database.

## Reading Notes
**Archived, last pushed 2020-10-21, and the data source no longer exists** — the Microsoft Academic Graph was retired at the end of 2021, so nothing here can be run as written. It is catalogued for the *method*: distributed batch analytics over a very large graph, and the query-plus-template pairing. Two further limits: U-SQL is specific to Azure Data Lake Analytics, itself now legacy, and the documentation is 41 screenshots against 18 Markdown files, so a reader who cannot execute it is reading pictures. OpenAlex is the usual successor dataset for anyone wanting to apply the queries to live data.

## Semantic Links
- [parent_topic:: [[Topic - Knowledge Management]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[neo4j-labs - neocarta]]]
- [related_to:: [[asreview]]]
- [related_to:: [[duckdb - duckdb]]]
- [related_to:: [[khairulislam - ML-conferences]]]
- [implements_pattern:: [[Pattern - Knowledge Graph Routing]]]
- [implements_pattern:: [[Pattern - Metadata Harvesting]]]
- [implements_pattern:: [[Pattern - Analytical Query Engine]]]
- [mentions_term:: [[Glossary - Knowledge Graph]]]
- [mentions_term:: [[Glossary - OLAP]]]
- [mentions_term:: [[Glossary - Dataset]]]
- [mentions_term:: [[Glossary - Taxonomy]]]

## Evidence
- Source URL: https://github.com/Azure-Samples/academic-knowledge-analytics-visualization
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata, the complete file tree at HEAD, and the LICENSE.md file; no U-SQL script, C# file or report was opened

## GitHub Snapshot

- Description: Various examples to perform big data analytics over Microsoft Academic Graph and visualize the results.
- Language: C#
- License (SPDX): MIT
- Default Branch: master
- Stars: 62
- Pushed At: 2020-10-21T01:35:55Z

## Evidence Anchors
- [github_repo] description :: Various examples to perform big data analytics over Microsoft Academic Graph and visualize the results. (confidence 0.95)
- [github_repo] language :: C# (confidence 0.90)
- [github_repo] license :: MIT (confidence 0.90)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 115 paths at HEAD (confidence 0.95)
