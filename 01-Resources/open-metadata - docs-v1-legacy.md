---
uuid: "c8565868-2647-51e6-ac82-b9b262af0195"
canonical_url: "https://github.com/open-metadata/docs-v1-legacy"
repo_key: "open-metadata/docs-v1-legacy"
owner: "open-metadata"
repo_name: "docs-v1-legacy"
aliases: ["open-metadata/docs-v1-legacy", "https://github.com/open-metadata/docs-v1-legacy"]
type: "specification"
primary_topic: "Data APIs & Big Data"
secondary_topics: ["Knowledge Management", "Architecture & Developer Playbooks"]
ecosystem: "Web_Frontend"
domain_primary: "Data"
maturity_stage: "Abandoned"
license_class: "Unknown"
deployment_target: "Browser"
interface_protocol: "Web_UI"
data_locality: "Stateless"
hardware_footprint: "Browser_Only"
security_compliance: "Uncertified"
agent_surface: "Documented"
patterns: ["Schema-First Codegen", "Metadata Harvesting", "Policy As Schema"]
glossary_terms: ["Metadata Catalog", "Schema", "Data Lineage", "Model Context Protocol"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Unknown"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: "OpenMetadata docs page source code "
github_language: "TypeScript"
github_license_spdx: "NOASSERTION"
github_default_branch: "main"
github_stars: 5
github_topics: ["docs", "openmetadata"]
github_homepage: "https://docsv1.netlify.app"
github_pushed_at: "2026-02-16T05:46:34Z"
---
# open-metadata - docs-v1-legacy

## Bottom Line
The retired documentation site for OpenMetadata, and — more usefully — a frozen snapshot of three complete product versions side by side, in which 2,412 pages document generated JSON Schemas and 626 shared partials show how that was kept consistent across all three.

## What It Solves
- Read three versions of a large product's documentation simultaneously and see what changed.
- Study how documentation for hundreds of generated schemas is maintained without hand-writing each page.
- Recover documentation for an older OpenMetadata release that the current site no longer serves.

## Architecture & Mechanics
- Versions are directories, complete and parallel: `content/v1.10.x` (1,603 files), `content/v1.11.x` (1,626), `content/v1.12.x-SNAPSHOT` (1,627). Nothing is diffed away, so any page can be compared across three releases directly.
- `content/partials/` (626 files) is the mechanism that makes that affordable — shared fragments included into many pages, versioned alongside them (`partials/v1.10/`, `v1.11/`, `v1.12/`). The same connector instruction appears once and is included everywhere it applies.
- **2,412 of the 5,483 Markdown files document JSON Schemas** — `main-concepts/metadata-standard/schemas/…`. Nearly half the documentation is the schema layer, which is the visible consequence of OpenMetadata generating its models from 904 schemas.
- The site is Next.js with Markdoc (`markdoc/tags/` 32 files, `markdoc/nodes/` 6), so the documentation has a component vocabulary of its own rather than being plain Markdown.
- **Not read:** any content page, partial or component. The above is read off the tree, path prefixes and file counts.

## What Is Inside
- **Three complete documentation versions**, 1,600+ files each, held in parallel rather than superseding one another.
- **626 shared partials** — `content/partials/`, versioned, including `connectors/test-connection.md` repeated per version: how one instruction stays correct across hundreds of pages.
- **2,412 schema documentation pages** — the metadata standard, enumerated.
- **Governance workflow examples** — `how-to-guides/data-governance/workflows/examples/`: `tag-approval-workflow.md`, `table-documentation-tiering-workflow.md`, `set-tags-to-mlmodels-workflow.md`. Worked examples of automated governance, present in all three versions.
- **Agent-facing documentation** — 57 paths under `how-to-guides/mcp/` including `claude.md`, `goose.md`, `connect.md`, `reference.md`: a data catalogue documenting its own MCP surface.
- **ER-diagram documentation** — `how-to-guides/data-discovery/er-diagrams.md` in each version, plus `images/docs-structure.drawio.png`.
- **A Markdoc component library** — `markdoc/tags/` (32 components) and `markdoc/nodes/` (6).
- **4,946 images** and 2.2 GB. See Reading Notes.

## Transferable Capability
**Factor documentation into partials and version the partials with the content.** The scale problem here is real — one instruction that applies to seventy connectors across three releases is 210 places to be wrong — and the answer is the same one code uses: write it once, include it everywhere, and version the included thing alongside its includers. **Keeping whole versions in parallel** rather than diffing them is the second decision: it costs disk and makes *what changed between releases* answerable by direct comparison, which no changelog does as well.

The third observation is a measurement rather than a technique. **Half of this documentation describes generated schemas.** That is the true cost of schema-first generation — the models cannot drift, and the documentation surface grows with the schema count — and it is the concrete counterweight to the *generate, do not hand-write* argument.

**Alternative to:** one live version with history in git, which is smaller and makes cross-version comparison a research task; and to hand-written pages per schema, which drift immediately. **Applies wherever** documentation must cover many near-identical things across several supported versions.

## Taxonomy
- Ecosystem: Web_Frontend
- Domain Primary: Data
- Maturity Stage: Abandoned
- License Class: Unknown
- Deployment Target: Browser
- Interface Protocol: Web_UI
- Data Locality: Stateless
- Hardware Footprint: Browser_Only
- Security Compliance: Uncertified
- Agent Surface: Documented

## Integration & Use Cases
- Study `content/partials/` before writing documentation for a product with many similar integrations.
- Use it to recover documentation for an OpenMetadata release the live site no longer serves.
- Read the schema-page count as the empirical price of schema-first generation, alongside [[open-metadata - OpenMetadata]].

## Reading Notes
**Archived, and enormous: 10,759 files and 2.2 GB, of which 4,946 are images.** A blobless clone lists the tree cheaply; a full clone should not be undertaken casually. **No licence file and none reported by GitHub** — for a documentation repository that is a genuine problem, since the whole content is prose whose reuse terms are unstated, and it is excluded from every licence-constrained answer here. Catalogued for the *documentation architecture* rather than for the product it documents; [[open-metadata - OpenMetadata]] is the live source.

## Semantic Links
- [parent_topic:: [[Topic - Data APIs & Big Data]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[open-metadata - OpenMetadata]]]
- [related_to:: [[awsdocs - amazon-comprehend-developer-guide]]]
- [related_to:: [[syntax-tree - mdast]]]
- [related_to:: [[mdebellis - SemanticKG-Design]]]
- [implements_pattern:: [[Pattern - Schema-First Codegen]]]
- [implements_pattern:: [[Pattern - Metadata Harvesting]]]
- [implements_pattern:: [[Pattern - Policy As Schema]]]
- [mentions_term:: [[Glossary - Metadata Catalog]]]
- [mentions_term:: [[Glossary - Schema]]]
- [mentions_term:: [[Glossary - Data Lineage]]]
- [mentions_term:: [[Glossary - Model Context Protocol]]]

## Evidence
- Source URL: https://github.com/open-metadata/docs-v1-legacy
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; no content page, partial or component was opened, and no licence file exists to read

## GitHub Snapshot

- Description: OpenMetadata docs page source code 
- Language: TypeScript
- License (SPDX): NOASSERTION
- Default Branch: main
- Stars: 5
- Homepage: https://docsv1.netlify.app
- Pushed At: 2026-02-16T05:46:34Z
- Topics: docs, openmetadata

## Evidence Anchors
- [github_repo] description :: OpenMetadata docs page source code  (confidence 0.95)
- [github_repo] language :: TypeScript (confidence 0.90)
- [github_repo] license :: NOASSERTION (confidence 0.90)
- [github_repo] topics :: docs, openmetadata (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 10759 paths at HEAD (confidence 0.95)
