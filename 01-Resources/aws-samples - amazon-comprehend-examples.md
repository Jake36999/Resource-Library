---
uuid: "85a4f51d-3e11-50a3-a423-5f50ace9a5d2"
canonical_url: "https://github.com/aws-samples/amazon-comprehend-examples"
repo_key: "aws-samples/amazon-comprehend-examples"
owner: "aws-samples"
repo_name: "amazon-comprehend-examples"
aliases: ["aws-samples/amazon-comprehend-examples", "https://github.com/aws-samples/amazon-comprehend-examples"]
type: "tutorial"
primary_topic: "ML Training & MLOps"
secondary_topics: ["Data APIs & Big Data", "Security & SIEM"]
ecosystem: "Python"
domain_primary: "ML_Training"
maturity_stage: "Reference"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "REST"
data_locality: "Distributed"
hardware_footprint: "CPU_Only"
security_compliance: "Security_Adjacent"
agent_surface: "None"
patterns: ["Zero-Shot Entity Extraction", "Programmatic Labelling", "ETL API Ingestion"]
glossary_terms: ["Named Entity Recognition", "Annotated Example", "Enrichment", "Knowledge Graph"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT-0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 5
github_description: "A sample set of notebooks demonstrating Amazon Comprehend capabilities."
github_language: "Jupyter Notebook"
github_license_spdx: "MIT-0"
github_default_branch: "master"
github_stars: 47
github_pushed_at: "2023-11-28T18:26:32Z"
---
# aws-samples - amazon-comprehend-examples

## Bottom Line
Notebooks for Amazon Comprehend covering the parts that are actually hard — converting human annotation output into training format, extracting entities from PDFs that have layout, and redacting personal information in the storage path rather than in an application.

## What It Solves
- Get from a human annotation tool's output into a trainable format without writing the conversion twice.
- Extract entities from PDFs, where text order and layout are the problem rather than the model.
- Redact personal data as it is read, so no application can accidentally receive it.

## Architecture & Mechanics
- `comprehend_groundtruth_integration/` is 33 of 69 files — **half the repository is annotation-format conversion**, which is an accurate reflection of where effort goes in a custom-model project and is invisible from any product page.
- The PII example works at the storage layer: `s3_object_lambda_pii_protection_blog/` splits into `redaction/` and `access-control/`, so redaction happens on read and the application never handles the original. Two different controls, kept separate.
- The events tutorial turns extraction output into a graph (`notebooks/events_graph.py`, `compact_nx.html`), which is the step from *entities found* to *entities related*.
- The PDF entity recogniser has its own helper package (`building-custom-entity-recognizer-for-PDFs/helperPackage/`), because layout handling does not fit in a notebook.
- **Not read:** any notebook or Python file. The proportions above are file counts and directory names.

## What Is Inside
- **Annotation-format conversion tooling** — `comprehend_groundtruth_integration/src/` (32 files): the largest component, and the least glamorous.
- **Realistic document samples** — `building-custom-classifier/sample-docs/`: `CMS1500.png` (a US health insurance claim form), `discharge-summary.pdf`, `doctors-notes.pdf`, `drivers_license.png`, `insurance_card.png`, `insurance_invoice.png`. **Document types with real layout, useful as test material for any document-understanding work**, independent of Comprehend.
- **A finance events dataset and graph** — `amazon_comprehend_events_tutorial/data/sample_finance_dataset.txt`, `notebooks/events_graph.py`, `compact_nx.html`, and a captured API model (`comprehend-2017-11-27.normal.json`).
- **PII redaction at the storage layer** — `s3_object_lambda_pii_protection_blog/redaction/` and `access-control/`.
- **Training data for a custom classifier** — `building-custom-classifier/train-data/comprehend_train_data.csv`.
- **Not here:** the service. Everything requires an AWS account, and the model is not inspectable.

## Transferable Capability
**Put redaction in the read path, not in the application.** If sensitive data can only be obtained through an interface that removes it, then no downstream consumer can leak what it never received — a structural guarantee rather than a discipline that must hold everywhere. Separating *redaction* from *access control* is part of the same design: one decides what a caller sees, the other decides whether they call at all.

The second transferable observation is empirical and useful for planning: **half of a custom-model project is annotation format conversion.** The model is the interesting part and the smallest part; anyone budgeting such a project from the model outward will be wrong.

**Alternative to:** filtering sensitive fields in each consuming application, which is correct in every application until one is added; and to redacting at write time, which loses the original irreversibly. **Applies wherever** sensitive data must be widely readable in a reduced form — logs, analytics, support tooling, model training corpora.

## Taxonomy
- Ecosystem: Python
- Domain Primary: ML_Training
- Maturity Stage: Reference
- License Class: Permissive
- Deployment Target: Server
- Interface Protocol: REST
- Data Locality: Distributed
- Hardware Footprint: CPU_Only
- Security Compliance: Security_Adjacent
- Agent Surface: None

## Integration & Use Cases
- Take the S3 Object Lambda redaction pattern as the model for any read-path filtering, on any storage layer.
- Reuse `building-custom-classifier/sample-docs/` as realistic test documents for layout-aware extraction work.
- Read `comprehend_groundtruth_integration/` to size the annotation-conversion effort before starting a custom-model project.

## Reading Notes
Vendor samples for a managed service, so the model is a black box and nothing here is portable to a self-hosted extractor without rewriting. **MIT-0** — the no-attribution MIT variant — which is unusually permissive and worth noting, since it means the sample documents and conversion code can be reused without an attribution obligation. Last pushed 2023-11-28; the surrounding AWS SDKs have moved, and committed `.pyc` files indicate this was not packaged with care.

## Semantic Links
- [parent_topic:: [[Topic - ML Training & MLOps]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[awsdocs - amazon-comprehend-developer-guide]]]
- [related_to:: [[urchade - GLiNER]]]
- [related_to:: [[NorskRegnesentral - skweak]]]
- [related_to:: [[not-a-bank - open-banking-tracker-data]]]
- [implements_pattern:: [[Pattern - Zero-Shot Entity Extraction]]]
- [implements_pattern:: [[Pattern - Programmatic Labelling]]]
- [implements_pattern:: [[Pattern - ETL API Ingestion]]]
- [mentions_term:: [[Glossary - Named Entity Recognition]]]
- [mentions_term:: [[Glossary - Annotated Example]]]
- [mentions_term:: [[Glossary - Enrichment]]]
- [mentions_term:: [[Glossary - Knowledge Graph]]]

## Evidence
- Source URL: https://github.com/aws-samples/amazon-comprehend-examples
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata, the complete file tree at HEAD, and the LICENSE file; no notebook or Python file was opened

## GitHub Snapshot

- Description: A sample set of notebooks demonstrating Amazon Comprehend capabilities.
- Language: Jupyter Notebook
- License (SPDX): MIT-0
- Default Branch: master
- Stars: 47
- Pushed At: 2023-11-28T18:26:32Z

## Evidence Anchors
- [github_repo] description :: A sample set of notebooks demonstrating Amazon Comprehend capabilities. (confidence 0.95)
- [github_repo] language :: Jupyter Notebook (confidence 0.90)
- [github_repo] license :: MIT-0 (confidence 0.90)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 69 paths at HEAD (confidence 0.95)
