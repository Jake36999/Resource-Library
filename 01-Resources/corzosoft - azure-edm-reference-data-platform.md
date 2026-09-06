---
uuid: "c65d4717-001b-5926-9d33-2025cd8254c9"
canonical_url: "https://github.com/corzosoft/azure-edm-reference-data-platform"
repo_key: "corzosoft/azure-edm-reference-data-platform"
owner: "corzosoft"
repo_name: "azure-edm-reference-data-platform"
aliases: ["corzosoft/azure-edm-reference-data-platform", "https://github.com/corzosoft/azure-edm-reference-data-platform"]
type: "reference_implementation"
primary_topic: "Data Lineage & Provenance"
secondary_topics: ["Data APIs & Big Data", "Infrastructure & Observability"]
ecosystem: "Data_Platform"
domain_primary: "Data_Lineage"
maturity_stage: "Reference"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "CLI"
data_locality: "Distributed"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Reference Data Mastering", "Reference Architecture", "Infrastructure as Code", "Run Provenance Capture"]
glossary_terms: ["Data Lineage", "Column-Level Lineage", "Golden Source", "Infrastructure as Code"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 5
github_description: "Open-source EDM-style reference data platform simulator for Azure with SQL, Python, ADF, Bicep, audit, lineage, validation, and survivorship examples."
github_language: "Python"
github_license_spdx: "MIT"
github_default_branch: "main"
github_stars: 0
github_pushed_at: "2026-05-19T00:03:46Z"
---
# corzosoft - azure-edm-reference-data-platform

## Bottom Line
A runnable simulation of an enterprise reference-data platform — vendor feeds arriving from two suppliers, validated, reconciled, survived into a golden record, and tracked for lineage — with the Azure infrastructure to stand it up expressed as Bicep.

## What It Solves
- Show what a reference-data platform actually contains, when the real ones are all behind a licence and a procurement process.
- Decide which vendor's value wins when two suppliers disagree about the same security, and record why.
- Exercise validation, reconciliation and lineage against sample feeds before wiring the real ones.

## Architecture & Mechanics
- Four layers are present as separate directories rather than as prose: `src/edm_reference_platform` (nine Python modules), `sql/` (eight numbered migrations, ending at `007_golden_source_views.sql`), `adf/` (Azure Data Factory pipelines, datasets and linked services as JSON), and `infra/bicep/` (five templates: `main`, `sql`, `storage`, `keyvault`, `monitor`).
- Survivorship — which competing value becomes the golden record — is written down as a document (`docs/survivorship-rules.md`) *and* has a corresponding test, so the rule and its check are both artefacts.
- The five tests name the platform's five obligations exactly: `test_cli`, `test_file_validator`, `test_lineage`, `test_quality_report`, `test_reconciliation`.
- **Not read:** any module body. The layering above is read off the tree and the documentation filenames.

## What Is Inside
- **Two vendors' worth of sample feed** — `sample-data/`: `vendor_a_securities.csv`, `vendor_a_prices.csv`, `vendor_b_securities.csv`, `vendor_b_prices.csv`, `ratings.csv`. The deliberate overlap between vendor A and vendor B is what makes reconciliation and survivorship demonstrable rather than described.
- **Eight SQL migrations** — `sql/`, numbered, terminating in `007_golden_source_views.sql`: the schema evolution of a mastering database, in order.
- **Five operational documents** — `docs/`: `azure-deployment-guide.md`, `data-quality-rules.md`, `survivorship-rules.md`, `runbook.md`, and `interview-demo-script.md`, which walks the system end to end as a demonstration.
- **Azure infrastructure as code** — `infra/bicep/` (5 templates) and `adf/` (3 pipelines, 1 dataset, 1 linked service) — plus `docker-compose.yml` for running it without Azure.
- **Not here:** a vendor connector, an entitlement model, or any real market data. The feeds are synthetic.

## Transferable Capability
**Resolve conflicting statements about the same entity into one record, and keep the reason the winner won.** The shape is general: multiple sources describe the same thing, they disagree, a declared precedence decides, and the decision must survive audit. Two design choices carry over independently of the domain — writing the precedence rules as a *document with a matching test*, so the rule cannot drift from its enforcement, and shipping overlapping sample inputs, so the conflict path is exercised by default instead of being the case nobody runs.

**Alternative to:** last-write-wins, which resolves the conflict without recording that there was one; and to manual stewardship, which resolves it correctly and leaves no rule behind. **Applies wherever** several sources assert facts about one subject and something downstream needs a single answer plus a defence of it — catalogue merges, identity resolution, configuration precedence, conflicting sensor readings.

## Taxonomy
- Ecosystem: Data_Platform
- Domain Primary: Data_Lineage
- Maturity Stage: Reference
- License Class: Permissive
- Deployment Target: Server
- Interface Protocol: CLI
- Data Locality: Distributed
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Take the survivorship-rule-plus-test pairing into any system where a precedence rule is currently only in someone's head.
- Use the numbered SQL migrations as a worked schema for a mastering store.
- Stand the whole thing up via `docker-compose.yml` to study reconciliation without an Azure subscription.

## Reading Notes
Zero stars and one week of commits (2026-05-18 to 2026-05-19), and `docs/interview-demo-script.md` makes the intent explicit: this was built as a portfolio piece. That is not a reason to discount it — a portfolio piece is optimised for being *legible*, which is exactly what makes it useful as a reference — but it does mean nothing here has been run at volume, and the Bicep has not been proven against a real subscription by anyone but its author.

## Semantic Links
- [parent_topic:: [[Topic - Data Lineage & Provenance]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[Victor-Kipruto-Rop - medallion-lakehouse-platform]]]
- [related_to:: [[PHACDataHub - data-mesh-ref-impl]]]
- [related_to:: [[open-metadata - OpenMetadata]]]
- [related_to:: [[carter-kilgour - delta-quality-testing]]]
- [implements_pattern:: [[Pattern - Reference Data Mastering]]]
- [implements_pattern:: [[Pattern - Reference Architecture]]]
- [implements_pattern:: [[Pattern - Infrastructure as Code]]]
- [mentions_term:: [[Glossary - Data Lineage]]]
- [mentions_term:: [[Glossary - Column-Level Lineage]]]
- [mentions_term:: [[Glossary - Golden Source]]]
- [mentions_term:: [[Glossary - Infrastructure as Code]]]

## Evidence
- Source URL: https://github.com/corzosoft/azure-edm-reference-data-platform
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata, the complete file tree at HEAD, and the LICENSE file; no source, SQL or Bicep file was opened

## GitHub Snapshot

- Description: Open-source EDM-style reference data platform simulator for Azure with SQL, Python, ADF, Bicep, audit, lineage, validation, and survivorship examples.
- Language: Python
- License (SPDX): MIT
- Default Branch: main
- Stars: 0
- Pushed At: 2026-05-19T00:03:46Z

## Evidence Anchors
- [github_repo] description :: Open-source EDM-style reference data platform simulator for Azure with SQL, Python, ADF, Bicep, audit, lineage, validation, and survivorship examples. (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: MIT (confidence 0.90)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 57 paths at HEAD (confidence 0.95)
