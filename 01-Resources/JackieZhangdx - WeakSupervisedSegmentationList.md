---
uuid: "20e3ed76-3222-5c51-a68b-273c958df610"
canonical_url: "https://github.com/JackieZhangdx/WeakSupervisedSegmentationList"
repo_key: "JackieZhangdx/WeakSupervisedSegmentationList"
owner: "JackieZhangdx"
repo_name: "WeakSupervisedSegmentationList"
aliases: ["JackieZhangdx/WeakSupervisedSegmentationList", "https://github.com/JackieZhangdx/WeakSupervisedSegmentationList"]
type: "curated_list"
primary_topic: "ML Training & MLOps"
secondary_topics: ["Curated Aggregators & Reference Lists"]
ecosystem: "Markdown"
domain_primary: "ML_Training"
maturity_stage: "Abandoned"
license_class: "Unknown"
deployment_target: "Local_Only"
interface_protocol: "Markdown"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Curated Resource Curation", "Programmatic Labelling"]
glossary_terms: ["Weak Supervision", "Annotated Example", "Reference List"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Unknown"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 5
github_description: "This repository contains lists of state-or-art weakly supervised semantic segmentation works"
github_language: "Unknown"
github_license_spdx: "NOASSERTION"
github_default_branch: "master"
github_stars: 598
github_pushed_at: "2019-04-29T02:23:54Z"
---
# JackieZhangdx - WeakSupervisedSegmentationList

## Bottom Line
A two-file survey of weakly supervised semantic segmentation, organised by *what kind of supervision was available* — image labels, boxes, scribbles, points — which is the axis that actually determines which method applies to your data.

## What It Solves
- Find segmentation methods that work with the annotation you already have, rather than the annotation you cannot afford.
- See the field organised by supervision strength instead of by publication year.
- Separate weakly supervised work from fully unsupervised work, which are routinely conflated.

## Architecture & Mechanics
- The organising axis is the contribution: sorting by supervision signal turns a reading list into a decision procedure, because *what labels do I have* is the first question and every method's applicability follows from it.
- The split into two files — `README.md` and `unsup.md` — draws the line between weakly supervised and fully unsupervised, which are different problems with different expectations.
- `img/dataset.PNG` is present, most likely a comparison table of datasets rendered as an image; that choice makes it unsearchable, which matters for a list whose value is being findable.
- **Not read:** either Markdown file. The organising principle is stated by the repository's own description; the specific categories were not verified.

## What Is Inside
- **Two curated lists** — `README.md` (weakly supervised) and `unsup.md` (unsupervised).
- **Five images** — including `img/dataset.PNG`.
- **Seven paths in total.** 598 stars, last pushed 2019-04-29.
- **Not here:** code, implementations or licence. It is a bibliography.

## Transferable Capability
**Organise a survey by the constraint the reader arrives with, not by the taxonomy of the field.** A reader comes with a fixed situation — these are the labels I have — and the useful question is which methods that situation admits. Sorting by supervision type answers it directly; sorting by year, venue or architecture leaves the reader to do the mapping themselves, which is the work they came to avoid. The general principle is that **a reference list is a routing structure, and its axis should be whatever the reader cannot change.**

**Alternative to:** a chronological bibliography, which records the field's history and answers no question; and to a search engine, which requires already knowing the vocabulary. **Applies wherever** options must be filtered by a fixed constraint — hardware available, licence permitted, data on hand, budget.

## Taxonomy
- Ecosystem: Markdown
- Domain Primary: ML_Training
- Maturity Stage: Abandoned
- License Class: Unknown
- Deployment Target: Local_Only
- Interface Protocol: Markdown
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Use it to identify which segmentation approaches your existing annotation admits before commissioning more labelling.
- Take the sort-by-constraint principle into any catalogue or reference list, including this one.
- Read `unsup.md` separately when the honest answer is that there are no labels at all.

## Reading Notes
**Frozen at 2019-04-29 and no licence.** For a bibliography in a fast-moving subfield, six years is decisive: the organising principle survives, the entries do not, and anything after 2019 is missing entirely. Read it for the axis, not the contents. The dataset comparison being a PNG rather than a table is a small but real failure — it cannot be searched, quoted or updated, which is the recurring cost of putting structured information into an image.

## Semantic Links
- [parent_topic:: [[Topic - ML Training & MLOps]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[snorkel-team - snorkel]]]
- [related_to:: [[knodle - knodle]]]
- [related_to:: [[NorskRegnesentral - skweak]]]
- [related_to:: [[ardamavi - Unsupervised-Classification-with-Autoencoder]]]
- [implements_pattern:: [[Pattern - Curated Resource Curation]]]
- [implements_pattern:: [[Pattern - Programmatic Labelling]]]
- [mentions_term:: [[Glossary - Weak Supervision]]]
- [mentions_term:: [[Glossary - Annotated Example]]]
- [mentions_term:: [[Glossary - Reference List]]]

## Evidence
- Source URL: https://github.com/JackieZhangdx/WeakSupervisedSegmentationList
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; neither Markdown file was opened, and no licence file exists to read

## GitHub Snapshot

- Description: This repository contains lists of state-or-art weakly supervised semantic segmentation works
- Language: Unknown
- License (SPDX): NOASSERTION
- Default Branch: master
- Stars: 598
- Pushed At: 2019-04-29T02:23:54Z

## Evidence Anchors
- [github_repo] description :: This repository contains lists of state-or-art weakly supervised semantic segmentation works (confidence 0.95)
- [github_repo] language :: Unknown (confidence 0.90)
- [github_repo] license :: NOASSERTION (confidence 0.90)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 7 paths at HEAD (confidence 0.95)
