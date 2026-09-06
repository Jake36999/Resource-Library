---
uuid: "22f1f5d5-c622-5fb8-a9df-a1b4de17525a"
canonical_url: "https://github.com/awsdocs/amazon-comprehend-developer-guide"
repo_key: "awsdocs/amazon-comprehend-developer-guide"
owner: "awsdocs"
repo_name: "amazon-comprehend-developer-guide"
aliases: ["awsdocs/amazon-comprehend-developer-guide", "https://github.com/awsdocs/amazon-comprehend-developer-guide"]
type: "specification"
primary_topic: "ML Training & MLOps"
secondary_topics: ["Curated Aggregators & Reference Lists"]
ecosystem: "Markdown"
domain_primary: "ML_Training"
maturity_stage: "Abandoned"
license_class: "Copyleft"
deployment_target: "Local_Only"
interface_protocol: "Markdown"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Curated Resource Curation"]
glossary_terms: ["Named Entity Recognition", "API", "Reference List"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "CC-BY-SA-4.0 (documentation) and MIT (sample code)"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 5
github_description: "The open source version of the Amazon Comprehend docs. You can submit feedback & requests for changes by submitting issues in this repo or by making proposed changes & submitting a pull request"
github_language: "Unknown"
github_license_spdx: "NOASSERTION"
github_default_branch: "archived"
github_stars: 21
github_pushed_at: "2023-06-15T20:30:43Z"
---
# awsdocs - amazon-comprehend-developer-guide

## Bottom Line
The archived remains of AWS's experiment in publishing product documentation as an open repository — the guide's Markdown has been withdrawn, leaving the licensing structure and the contribution process as what is actually still here.

## What It Solves
- Show how a vendor structured documentation licensing when documentation and sample code carry different terms.
- Record what an open-documentation contribution process looked like.
- Demonstrate the failure mode of the arrangement: the content can be withdrawn while the repository remains.

## Architecture & Mechanics
- Licensing is split deliberately across three files: `LICENSE` (CC-BY-SA-4.0, the prose), `LICENSE-SAMPLECODE` (a modified MIT, the code), and `LICENSE-SUMMARY` explaining which applies to what. That separation is the whole substance of what remains.
- `CONTRIBUTING.md` sets out how external corrections were accepted into vendor documentation — the mechanism the experiment existed to test.
- Six paths remain. The Markdown chapters the repository was created to hold are gone.
- **Read:** `LICENSE-SUMMARY` and `LICENSE`, fetched directly and read in full, which is how the split above is stated rather than inferred.

## What Is Inside
- **A three-part licence structure** — `LICENSE` (CC-BY-SA-4.0), `LICENSE-SAMPLECODE` (modified MIT), `LICENSE-SUMMARY` (which governs which).
- **`CONTRIBUTING.md`** — the process for contributing corrections to vendor documentation.
- **Six paths, three of them Markdown.** Archived, last pushed 2023-06-15.
- **Not here:** the developer guide. AWS moved its documentation back behind its own publishing pipeline and removed the content; only the shell remains.

## Transferable Capability
**Licence prose and sample code separately, and say in a third file which applies where.** A documentation repository contains two different things with different reuse expectations: text that should be attributed and shared alike, and snippets that must be copyable into proprietary work without obligation. One licence cannot serve both, and the summary file exists because a reader with two licences and no map will guess.

The more uncomfortable lesson is about **durability**: an open documentation repository is only open while the publisher continues to publish there. Everything here except the licences was withdrawn, and the archived repository is now a monument to the arrangement rather than an instance of it. **Applies wherever** a dependency's availability rests on a publisher's continuing choice rather than on a licence grant — mirror anything you rely on.

## Taxonomy
- Ecosystem: Markdown
- Domain Primary: ML_Training
- Maturity Stage: Abandoned
- License Class: Copyleft
- Deployment Target: Local_Only
- Interface Protocol: Markdown
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Copy the three-file licensing structure for any repository mixing documentation and reusable sample code.
- Cite it as the concrete case when arguing that externally hosted documentation must be mirrored, not linked.
- Read `CONTRIBUTING.md` if designing a process for accepting external corrections to first-party documentation.

## Reading Notes
**Archived and effectively empty.** GitHub reported the licence as NOASSERTION; the licence files were fetched and read directly, and the composite is CC-BY-SA-4.0 for prose plus a modified MIT for sample code — classified at the more restrictive half, `Copyleft`, with the composite flagged in [[Licence Resolution 2026-09-03]] for a person to confirm, since the correct answer depends on which half is being reused. Catalogued deliberately as a **negative result**: it documents an abandoned approach to open documentation and the exact way that approach fails, which is information the surviving copy of the guide does not carry.

## Semantic Links
- [parent_topic:: [[Topic - ML Training & MLOps]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[aws-samples - amazon-comprehend-examples]]]
- [related_to:: [[open-metadata - docs-v1-legacy]]]
- [related_to:: [[cfpb - open-source-checklist]]]
- [implements_pattern:: [[Pattern - Curated Resource Curation]]]
- [mentions_term:: [[Glossary - Named Entity Recognition]]]
- [mentions_term:: [[Glossary - API]]]
- [mentions_term:: [[Glossary - Reference List]]]

## Evidence
- Source URL: https://github.com/awsdocs/amazon-comprehend-developer-guide
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata, the complete file tree at HEAD, and LICENSE plus LICENSE-SUMMARY read in full

## GitHub Snapshot

- Description: The open source version of the Amazon Comprehend docs. You can submit feedback & requests for changes by submitting issues in this repo or by making proposed changes & submitting a pull request
- Language: Unknown
- License (SPDX): NOASSERTION
- Default Branch: archived
- Stars: 21
- Pushed At: 2023-06-15T20:30:43Z

## Evidence Anchors
- [github_repo] description :: The open source version of the Amazon Comprehend docs. You can submit feedback & requests for changes by submitting issues in this repo or by making proposed changes & submitting a pull request (confidence 0.95)
- [github_repo] language :: Unknown (confidence 0.90)
- [github_repo] license :: NOASSERTION (confidence 0.90)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 6 paths at HEAD (confidence 0.95)
