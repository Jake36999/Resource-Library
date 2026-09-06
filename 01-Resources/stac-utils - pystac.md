---
uuid: "beace521-0a25-51d7-b6c1-c3231c24d8dd"
canonical_url: "https://github.com/stac-utils/pystac"
repo_key: "stac-utils/pystac"
owner: "stac-utils"
repo_name: "pystac"
aliases: ["stac-utils/pystac", "https://github.com/stac-utils/pystac"]
type: "geospatial_library"
primary_topic: "Geospatial & Earth Data"
secondary_topics: ["Data APIs & Big Data"]
ecosystem: "Geo_Data"
domain_primary: "Geospatial"
maturity_stage: "Production_Ready"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Python_SDK"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["STAC Ingestion", "Spatial Indexing", "Open Data Portal"]
glossary_terms: ["STAC", "Satellite Imagery", "Geospatial Data", "Dataset", "Schema"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-08-31"
evidence_count: 4
github_description: "Python library for working with any SpatioTemporal Asset Catalog (STAC)"
github_language: "Python"
github_license_spdx: "NOASSERTION"
github_default_branch: "main"
github_stars: 458
github_topics: []
github_homepage: "https://pystac.readthedocs.io"
github_pushed_at: "2026-08-25T06:06:57Z"
---
# stac-utils - pystac

## Bottom Line
The reference Python implementation of the SpatioTemporal Asset Catalog spec — build, read, validate and walk catalogues of Earth-observation assets described as linked JSON.

## What It Solves
- Describe imagery archives with a standard, machine-readable metadata schema.
- Traverse catalogues of satellite scenes without bespoke per-provider parsers.
- Validate catalogue JSON against the spec and its extensions before publishing.

## Architecture & Mechanics
- Catalog, Collection and Item objects mirror the STAC spec's core types.
- Items carry geometry, datetime, properties and links to asset files.
- Static catalogues are plain linked JSON; a client extension talks to STAC API servers.
- Extensions (EO, projection, raster) add typed access to domain metadata fields.

## What Is Inside
- **The validation schemas are bundled, and that is the finding** — `core/pystac/validation/jsonschemas/` ships the STAC specification itself as JSON Schema, versioned (`stac-spec/v1.1.0/bands.json`, `basics.json` and siblings) alongside GeoJSON's own `Feature.json` and `Geometry.json`. You can validate STAC offline, and you can read the spec as machine-readable schema rather than as prose.
- **Extensions as independent packages** — `extensions/` (326 files), one per STAC extension with its own `pyproject.toml`: `version/` (38), `scientific/` (28), `file/` (25), `projection/` (23), `eo/` (20), `sat/` (19), `pointcloud/` (17), `datacube/`, `classification/`. A worked example of a plugin ecosystem inside one repository.
- **376 data files of real catalogues** — `tests/data-files/`, including historical spec versions (`examples/0.8.1/…`) and label-extension examples with SpaceNet building footprints (`AOI_2_Vegas_img2636.json`, `AOI_3_Paris_img1648.json`). A ready-made corpus for anyone parsing STAC or testing migration across spec versions.
- **Recorded HTTP interactions** — `tests/cassettes/` (34) and per-extension cassettes, so network behaviour is testable offline.
- **An example catalogue you can walk** — `docs/example-catalog/` with real Landsat-8 items.
- **Seven notebooks** — `docs/quickstart.ipynb`, `tutorials/creating-a-landsat-stac.ipynb`, `tutorials/adding-new-and-custom-extensions.ipynb`.
- **A benchmark suite** — `benchmarks/` (9 files).

## Transferable Capability
**Ship the specification as machine-readable schema alongside the library, so conformance can be checked without a network and read without prose.** The specification stops being a document you interpret and becomes an artefact you validate against. The second structural move: **each extension is an independently versioned package**, so the core stays small and an extension can move at its own pace or be abandoned without consequence.

**Alternative to:** validation that requires reaching a remote registry, and a specification that exists only as prose; and to extensions as core features, which forces every user to carry every extension. **Applies wherever** a format has a core plus optional parts contributed by different people.

## Taxonomy
- Ecosystem: Geo_Data
- Domain Primary: Geospatial
- Maturity Stage: Production_Ready
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Python_SDK
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Publish an internal imagery archive as a static, crawlable STAC catalogue.
- Query public Earth-observation catalogues as an ingestion step.
- Study a linked-JSON approach to dataset cataloguing.

## Semantic Links
- [parent_topic:: [[Topic - Geospatial & Earth Data]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[OSGeo - gdal]]]
- [related_to:: [[opengeos - leafmap]]]
- [related_to:: [[ngageoint - geoq]]]
- [implements_pattern:: [[Pattern - STAC Ingestion]]]
- [implements_pattern:: [[Pattern - Spatial Indexing]]]
- [implements_pattern:: [[Pattern - Open Data Portal]]]
- [mentions_term:: [[Glossary - STAC]]]
- [mentions_term:: [[Glossary - Satellite Imagery]]]
- [mentions_term:: [[Glossary - Geospatial Data]]]
- [mentions_term:: [[Glossary - Dataset]]]
- [mentions_term:: [[Glossary - Schema]]]

## Evidence
- Source URL: https://github.com/stac-utils/pystac
- Source kind: GitHub REST metadata plus maintainer documentation
- Ingestion mode: agent-curated note authored against live repository metadata
- Metadata captured: 2026-08-31
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names Apache-2.0 (reproduced in full). The GitHub API reported `NOASSERTION`, which is why this was read directly.

## GitHub Snapshot

- Description: Python library for working with any SpatioTemporal Asset Catalog (STAC)
- Language: Python
- License (SPDX): NOASSERTION
- Default Branch: main
- Stars: 458
- Homepage: https://pystac.readthedocs.io
- Pushed At: 2026-08-25T06:06:57Z
- Topics: None listed

## Evidence Anchors
- [github_repo] description :: Python library for working with any SpatioTemporal Asset Catalog (STAC) (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: NOASSERTION (confidence 0.90)
