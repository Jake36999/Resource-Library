---
uuid: "72243ca1-a35e-58ef-8784-18c675098e47"
canonical_url: "https://github.com/mdebellis/SemanticKG-Design"
repo_key: "mdebellis/SemanticKG-Design"
owner: "mdebellis"
repo_name: "SemanticKG-Design"
aliases: ["mdebellis/SemanticKG-Design", "https://github.com/mdebellis/SemanticKG-Design"]
type: "specification"
primary_topic: "Knowledge Management"
secondary_topics: ["Data APIs & Big Data", "Architecture & Developer Playbooks"]
ecosystem: "Mixed"
domain_primary: "Knowledge_Management"
maturity_stage: "Active"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "CLI"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Ontology-Driven Design", "Knowledge Graph Routing", "Schema Mapping", "Policy As Schema"]
glossary_terms: ["Ontology", "SPARQL", "Knowledge Graph", "Taxonomy", "Schema"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "CC-BY-4.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 5
github_description: "For ontology, code and other supporting examples and tools for the book: Designing Semantic Knowledge Graphs: A Guide to Utilizing Semantic Web Technologies for Agile Data Management"
github_language: "Python"
github_license_spdx: "NOASSERTION"
github_default_branch: "main"
github_stars: 1
github_pushed_at: "2026-09-01T14:49:17Z"
---
# mdebellis - SemanticKG-Design

## Bottom Line
The complete worked material behind a book on designing semantic knowledge graphs: twenty OWL/Turtle ontologies, twenty-six SPARQL query and update files, SHACL shapes, a published ontology website, and a full data product built on top of it — the whole method, executable, chapter by chapter.

## What It Solves
- Learn ontology design from artefacts that run rather than from diagrams.
- See validation, taxonomy and querying applied to one consistent model across a dozen chapters.
- Understand how a knowledge graph becomes a data product with REST, GraphQL and streaming surfaces.

## Architecture & Mechanics
- The repository is organised as the book is: `chapter_1`, `chapter_3`, `chapter_7`, `chapter_8`, `chapter_9`, `chapter_12`, `chapter_13`, each holding the listings and exercises for that chapter. Material is addressable by where it was explained.
- Three distinct modelling vocabularies are used for three different jobs, and kept separate — OWL for the ontology, SHACL for validation shapes (`Listing_3-23_to_3-24_Employee_Shape.ttl`), and SKOS for taxonomy (`chapter_12/consulting_skos_taxonomy.ttl`, `skos_glossary.ttl`). Which formalism suits which job is the lesson.
- Queries are split by dialect and purpose: 14 `.sparql`, 12 `.rq` (query) and 6 `.ru` (update) files.
- `tests/verify/` holds eleven SPARQL files with names like `01-class-label-en.sparql` — **the ontology is tested by querying it for violations**, and `tests/robot_report.tsv` is a committed ROBOT validation report.
- **Not read:** any ontology, query or Python file. The above is read off filenames, which in this repository are unusually explicit.

## What Is Inside
- **Twenty Turtle ontologies** — including `chapter_12/consulting_ontology.ttl`, `consulting_semantic_taxonomy.ttl`, `consulting_skos_taxonomy.ttl`, `skos_glossary.ttl`, and `ontologies/people_ontology_test_data.ttl`.
- **A published ontology website** — `docs/peopleOntology/` (40 files): `index.html`, `index-en.html`, `ontology.jsonld`, `ontology.nt`, an `.htaccess` for content negotiation and a `406.html`. **A complete worked example of publishing an ontology so that a browser and a machine each get the right representation from the same URI** — content negotiation done properly, which is described far more often than it is demonstrated.
- **A data product built on the graph** — `data_product/` (37 files): `data_product_src/` (16), `queries/` split into `access/` and `catalog/` (11 total, e.g. `product-to-dataset.rq`, `datasets-in-catalog.rq`), plus `REST/`, `graphql/`, `kafka/` and `rag-bot/` directories.
- **Ontology tests** — `tests/verify/` (11 SPARQL checks), `tests/basic_kg_tests.sparql`, and a committed `robot_report.tsv`.
- **Exercises with worked answers** — `chapter_1/exercises/` (5), `chapter_3/exercises/` (8), including a pizza-ontology tutorial.
- **An ingestion example with validation** — `chapter_8/data_ingestion/`: `ingestion_example.ttl`, `trending_snapshot_validation.ttl`, `processed_data/TestPipelineReport.md`.
- **A candid artefact** — `chapter_7/Listing_7-1_SPARQL_Test_Data_Generated_by_ChatGPT.ru`: the test data's origin is stated in its filename.
- **Not here:** the book. This is its companion material.

## Transferable Capability
**Use a different formalism for each job, and test the model by querying it for its own violations.** The separation of OWL (what things are), SHACL (what must hold) and SKOS (how terms relate) is the transferable discipline — collapsing them into one vocabulary is the usual mistake, and it produces a model that can neither be validated nor browsed. The **query-as-test** idea generalises well beyond semantic web work: if the model is queryable, a constraint can be written as a query that should return nothing, so validation needs no separate framework and every check is expressed in the language the model already speaks.

The third thing worth taking is the **content-negotiated publication** in `docs/peopleOntology/`: one identifier serving a human-readable page and a machine-readable serialisation, which is the general answer to *how should a schema be published so both audiences can use it*.

**Alternative to:** an ad-hoc JSON schema plus prose conventions, which cannot express relationships between terms and cannot be reasoned over; and to a diagram, which cannot be validated at all. **Applies wherever** a vocabulary must be shared across teams or systems and the meaning of a term needs to survive the person who defined it.

## Taxonomy
- Ecosystem: Mixed
- Domain Primary: Knowledge_Management
- Maturity Stage: Active
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: CLI
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Read `tests/verify/` before building a validation layer for any structured model — the constraints-as-queries approach may remove the need for one.
- Take `docs/peopleOntology/` as the worked example when publishing a schema or vocabulary that both people and machines must consume.
- Study `data_product/` for how a knowledge graph acquires REST, GraphQL and streaming surfaces without duplicating the model.

## Reading Notes
GitHub reported the licence as NOASSERTION; the `LICENSE` file was fetched and read and is **CC-BY-4.0** — appropriate for book material, and it does mean attribution is required for anything reused. One star, and that number is meaningless here: this is companion material to a published book, and its audience arrives through the book rather than through GitHub. Actively maintained (last pushed 2026-09-01). Of everything in this cohort, this is the source most directly applicable to the design of a catalogue like the one holding it — ontology, taxonomy, glossary and validation treated as separate, testable artefacts.

## Semantic Links
- [parent_topic:: [[Topic - Knowledge Management]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[neo4j-labs - neocarta]]]
- [related_to:: [[open-metadata - OpenMetadata]]]
- [related_to:: [[SachaCR - library-examples]]]
- [related_to:: [[MazzaWill - neo4j-python-pandas-py2neo-v3]]]
- [implements_pattern:: [[Pattern - Ontology-Driven Design]]]
- [implements_pattern:: [[Pattern - Knowledge Graph Routing]]]
- [implements_pattern:: [[Pattern - Schema Mapping]]]
- [implements_pattern:: [[Pattern - Policy As Schema]]]
- [mentions_term:: [[Glossary - Ontology]]]
- [mentions_term:: [[Glossary - SPARQL]]]
- [mentions_term:: [[Glossary - Knowledge Graph]]]
- [mentions_term:: [[Glossary - Taxonomy]]]
- [mentions_term:: [[Glossary - Schema]]]

## Evidence
- Source URL: https://github.com/mdebellis/SemanticKG-Design
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata, the complete file tree at HEAD, and the LICENSE file read in full; no ontology, query or Python file was opened

## GitHub Snapshot

- Description: For ontology, code and other supporting examples and tools for the book: Designing Semantic Knowledge Graphs: A Guide to Utilizing Semantic Web Technologies for Agile Data Management
- Language: Python
- License (SPDX): NOASSERTION
- Default Branch: main
- Stars: 1
- Pushed At: 2026-09-01T14:49:17Z

## Evidence Anchors
- [github_repo] description :: For ontology, code and other supporting examples and tools for the book: Designing Semantic Knowledge Graphs: A Guide to Utilizing Semantic Web Technologies for Agile Data Management (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: NOASSERTION (confidence 0.90)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 160 paths at HEAD (confidence 0.95)
