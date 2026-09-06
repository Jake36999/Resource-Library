---
uuid: "00fd7d30-e336-5c12-8d4e-4d667e5ace2c"
canonical_url: "https://github.com/DiceTechJobs/SolrConfigExamples"
repo_key: "DiceTechJobs/SolrConfigExamples"
owner: "DiceTechJobs"
repo_name: "SolrConfigExamples"
aliases: ["DiceTechJobs/SolrConfigExamples", "https://github.com/DiceTechJobs/SolrConfigExamples"]
type: "reference_implementation"
primary_topic: "Knowledge Management"
secondary_topics: ["Data APIs & Big Data"]
ecosystem: "Mixed"
domain_primary: "Knowledge_Management"
maturity_stage: "Reference"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "REST"
data_locality: "Distributed"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Vector Similarity Search", "Hybrid Retrieval"]
glossary_terms: ["Semantic Search", "Embedding", "Vector Database"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: "Examples of Solr configuration entries for Solr plugins and Conceptual Search\\Semantic Search from Simon Hughes Dice.com"
github_language: "Unknown"
github_license_spdx: "Apache-2.0"
github_default_branch: "master"
github_stars: 26
github_topics: ["conceptual-search", "dice", "information-retrieval", "lucene", "semantic-search", "solr", "solr-plugin", "synonym-files"]
github_homepage: "http://www.dice.com"
github_pushed_at: "2016-10-16T17:34:23Z"
---
# DiceTechJobs - SolrConfigExamples

## Bottom Line
Six files of Solr configuration showing how semantic search was done before vector databases existed: word vectors encoded into a custom Lucene field type, with a top-N field type for the ranking stage.

## What It Solves
- Add meaning-based matching to a Lucene index without leaving Lucene.
- Rank by conceptual similarity when the only available primitive is a term index.
- Reuse an existing search deployment rather than standing up a second, vector-shaped one.

## Architecture & Mechanics
- `vector_field_type.xml` is the mechanism: vectors are encoded so that an inverted index — designed for tokens — can be made to score similarity. This is the trick the whole approach rests on.
- `top_n_field_type.xml` handles the second half, keeping only the strongest signals so that scoring stays tractable at index scale.
- `solrconfig_snippets.xml` is the wiring: the request handlers and components that make the field types usable from a query.
- `job_titles.txt` is the domain vocabulary — this came out of Dice.com, a jobs marketplace, and the vocabulary is what the conceptual search was over.
- **Not read:** the XML. The mechanism above is inferred from the filenames and the repository's stated purpose.

## What Is Inside
- **Three XML configuration files** — `vector_field_type.xml`, `top_n_field_type.xml`, `solrconfig_snippets.xml`. That is the entire technical content.
- **`job_titles.txt`** — a domain vocabulary list, reusable as a synonym or entity source for anything working with employment data.
- **Six files in total**, 17 kB, last pushed 2016-10-16.
- **Not here:** the plugins these configurations activate, or the code that builds the vectors. Both live in sibling DiceTechJobs repositories; this is the configuration half alone.

## Transferable Capability
**Get a new capability out of existing infrastructure by changing the encoding rather than the system.** Semantic ranking was achieved here by representing vectors so that an inverted index could score them — no new datastore, no second copy of the corpus, no additional operational surface. That manoeuvre recurs constantly and is usually cheaper than it looks: the question *what would I have to encode differently for the system I already run to answer this* is worth asking before adding a component. The **top-N truncation** is the accompanying lesson — a similarity system is made affordable by discarding most of the signal, and choosing what to discard is the design.

**Alternative to:** a dedicated vector database, which is the same capability with a second system to run and keep in sync; and to reranking outside the index, which cannot use index-time information. **Applies wherever** a capability seems to demand new infrastructure and the existing store might be persuadable.

## Taxonomy
- Ecosystem: Mixed
- Domain Primary: Knowledge_Management
- Maturity Stage: Reference
- License Class: Permissive
- Deployment Target: Server
- Interface Protocol: REST
- Data Locality: Distributed
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Read it before assuming semantic search requires a vector database, particularly where a Lucene or Solr deployment already exists.
- Take `job_titles.txt` as a domain vocabulary for employment-related entity work.
- Use it as the historical baseline when comparing modern vector stores: it shows what the pre-2017 answer cost.

## Reading Notes
**Last pushed 2016-10-16 — a decade old, and deliberately catalogued as a historical reference rather than a live option.** It is also *incomplete by design*: these are configuration snippets for plugins that live in other DiceTechJobs repositories, so nothing here runs on its own. Its value is that it makes the pre-vector-database era concrete — which is exactly what is needed to judge whether a modern vector store earns its operational cost, or is being adopted because it is the current default.

## Semantic Links
- [parent_topic:: [[Topic - Knowledge Management]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[elastic - elastic-labs]]]
- [related_to:: [[lancedb - vectordb-recipes]]]
- [related_to:: [[qdrant - examples]]]
- [implements_pattern:: [[Pattern - Vector Similarity Search]]]
- [implements_pattern:: [[Pattern - Hybrid Retrieval]]]
- [mentions_term:: [[Glossary - Semantic Search]]]
- [mentions_term:: [[Glossary - Embedding]]]
- [mentions_term:: [[Glossary - Vector Database]]]

## Evidence
- Source URL: https://github.com/DiceTechJobs/SolrConfigExamples
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata, the complete file tree at HEAD, and the LICENSE.md file; no XML configuration file was opened

## GitHub Snapshot

- Description: Examples of Solr configuration entries for Solr plugins and Conceptual Search\Semantic Search from Simon Hughes Dice.com
- Language: Unknown
- License (SPDX): Apache-2.0
- Default Branch: master
- Stars: 26
- Homepage: http://www.dice.com
- Pushed At: 2016-10-16T17:34:23Z
- Topics: conceptual-search, dice, information-retrieval, lucene, semantic-search, solr, solr-plugin, synonym-files

## Evidence Anchors
- [github_repo] description :: Examples of Solr configuration entries for Solr plugins and Conceptual Search\Semantic Search from Simon Hughes Dice.com (confidence 0.95)
- [github_repo] language :: Unknown (confidence 0.90)
- [github_repo] license :: Apache-2.0 (confidence 0.90)
- [github_repo] topics :: conceptual-search, dice, information-retrieval, lucene, semantic-search, solr, solr-plugin, synonym-files (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 6 paths at HEAD (confidence 0.95)
