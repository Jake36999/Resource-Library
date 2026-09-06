---
uuid: "f3bac3a9-3d2c-5d9c-985f-a60c79e2b1a1"
canonical_url: "https://github.com/khairulislam/ML-conferences"
repo_key: "khairulislam/ML-conferences"
owner: "khairulislam"
repo_name: "ML-conferences"
aliases: ["khairulislam/ML-conferences", "https://github.com/khairulislam/ML-conferences"]
type: "curated_list"
primary_topic: "Curated Aggregators & Reference Lists"
secondary_topics: ["ML Training & MLOps"]
ecosystem: "Markdown"
domain_primary: "Discovery"
maturity_stage: "Active"
license_class: "Permissive"
deployment_target: "Browser"
interface_protocol: "Web_UI"
data_locality: "Local_First"
hardware_footprint: "Browser_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Curated Resource Curation", "Open Data Portal"]
glossary_terms: ["Reference List", "Dataset", "Curation"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: "List of ML conferences with important dates and accepted paper list"
github_language: "Jupyter Notebook"
github_license_spdx: "MIT"
github_default_branch: "main"
github_stars: 254
github_topics: ["ai", "computer-science", "conferences", "machine-learning", "nlp", "software-engineering", "vision"]
github_homepage: "https://khairulislam.github.io/ML-conferences"
github_pushed_at: "2026-08-17T20:51:23Z"
---
# khairulislam - ML-conferences

## Bottom Line
A conference deadline and acceptance-rate tracker that keeps its content as CSV and renders it as a static site — so the same material is readable by a person in a browser and by a program without scraping.

## What It Solves
- Know when submissions close, across eight major venues, in one place.
- Get acceptance rates over time as data rather than as a claim in a blog post.
- Reuse the underlying data without parsing HTML.

## Architecture & Mechanics
- Content and presentation are separated: `docs/data/` holds `conferences.csv`, `conferences_metadata.csv` and `acceptance_rates_yearly.csv`, while `docs/css/` and `docs/js/` render them. The CSV is the source of truth and the site is a view over it.
- The CSS is split by concern — `base.css`, `components.css`, `deadlines.css`, `stats.css` — indicating deadlines and statistics are two distinct views of the same data.
- `utils/miner.ipynb` is the collection half: the accepted-paper lists are mined rather than transcribed, with `utils/AAAI_2024_Papers.csv` as an output.
- `docs/DESIGN.md` documents the site's own design decisions, which is unusual for a repository of this size.
- **Not read:** any CSV, notebook or design document. The structure above is read off filenames and directory layout.

## What Is Inside
- **Three CSVs that are the actual product** — `docs/data/conferences.csv`, `conferences_metadata.csv`, `acceptance_rates_yearly.csv`. **Acceptance rates by year across venues, as structured data**, is the part hardest to obtain elsewhere.
- **Thirty-seven accepted-paper PDFs** — `accepted-papers/` split by venue: AAAI (9), CVPR (5), IJCAI (5), ICCV (4), ICLR (4), ICML (4), NeurIPS (4), KDD (1). 81 MB.
- **A mining notebook** — `utils/miner.ipynb` with `utils/AAAI_2024_Papers.csv`: how the lists were built.
- **`docs/DESIGN.md`** — the site's design decisions, written down.
- **Not here:** the papers themselves. `accepted-papers/` holds the venue listings, not the research.

## Transferable Capability
**Keep the data as data and let the site be a view over it.** A tracker whose content lives in the HTML has one consumer; one whose content lives in CSV has every consumer, including the site itself. That single decision is what makes a curated dataset reusable, and it costs nothing at the time. **Publishing the mining notebook** is the second half: it makes the collection reproducible and repairable by someone other than the author, which is what stops a tracker dying when its maintainer stops.

**Alternative to:** a Markdown table, which is readable and must be parsed to be used; and to a database behind an API, which is more capable and needs operating. **Applies wherever** a curated collection should be usable by both people and programs — which is nearly always, and is the same problem this catalogue solves by keeping Markdown as truth and treating the index as derived.

## Taxonomy
- Ecosystem: Markdown
- Domain Primary: Discovery
- Maturity Stage: Active
- License Class: Permissive
- Deployment Target: Browser
- Interface Protocol: Web_UI
- Data Locality: Local_First
- Hardware Footprint: Browser_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Take `acceptance_rates_yearly.csv` directly for any analysis of publication trends.
- Copy the data-in-CSV, view-in-static-site arrangement for any curated tracker.
- Read `utils/miner.ipynb` before hand-transcribing any listing that could be mined.

## Reading Notes
Actively maintained (last pushed 2026-08-17), 254 stars. Note the weight before cloning: **81 MB, almost all of it the 37 accepted-paper PDFs**, while the reusable part — the three CSVs — is a few kilobytes. Coverage is the major venues only; regional and specialist conferences are absent, which is a scope decision rather than an oversight but does limit it as a complete picture.

## Semantic Links
- [parent_topic:: [[Topic - Curated Aggregators & Reference Lists]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[soulbliss - NLP-conference-compendium]]]
- [related_to:: [[Azure-Samples - academic-knowledge-analytics-visualization]]]
- [related_to:: [[asreview]]]
- [related_to:: [[public-apis - public-apis]]]
- [implements_pattern:: [[Pattern - Curated Resource Curation]]]
- [implements_pattern:: [[Pattern - Open Data Portal]]]
- [mentions_term:: [[Glossary - Reference List]]]
- [mentions_term:: [[Glossary - Dataset]]]
- [mentions_term:: [[Glossary - Curation]]]

## Evidence
- Source URL: https://github.com/khairulislam/ML-conferences
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata, the complete file tree at HEAD, and the LICENSE file; no CSV, notebook or design document was opened

## GitHub Snapshot

- Description: List of ML conferences with important dates and accepted paper list
- Language: Jupyter Notebook
- License (SPDX): MIT
- Default Branch: main
- Stars: 254
- Homepage: https://khairulislam.github.io/ML-conferences
- Pushed At: 2026-08-17T20:51:23Z
- Topics: ai, computer-science, conferences, machine-learning, nlp, software-engineering, vision

## Evidence Anchors
- [github_repo] description :: List of ML conferences with important dates and accepted paper list (confidence 0.95)
- [github_repo] language :: Jupyter Notebook (confidence 0.90)
- [github_repo] license :: MIT (confidence 0.90)
- [github_repo] topics :: ai, computer-science, conferences, machine-learning, nlp, software-engineering, vision (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 64 paths at HEAD (confidence 0.95)
