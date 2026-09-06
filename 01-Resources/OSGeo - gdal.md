---
uuid: "e800f70c-7201-580e-b4f4-792c573b70e8"
canonical_url: "https://github.com/OSGeo/gdal"
repo_key: "OSGeo/gdal"
owner: "OSGeo"
repo_name: "gdal"
aliases: ["OSGeo/gdal", "https://github.com/OSGeo/gdal"]
type: "geospatial_library"
primary_topic: "Geospatial & Earth Data"
secondary_topics: ["Data APIs & Big Data", "Scientific Simulation & Math"]
ecosystem: "Geo_Data"
domain_primary: "Geospatial"
maturity_stage: "Production_Ready"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "CLI"
data_locality: "Local_First"
hardware_footprint: "High_Memory"
security_compliance: "Uncertified"
agent_surface: "Documented"
patterns: ["Spatial Indexing", "Schema Mapping", "ETL API Ingestion"]
glossary_terms: ["Geospatial Data", "Raster", "Vector Data", "Coordinate Reference System", "Satellite Imagery"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Apache-2.0 AND BSD-3-Clause AND ISC AND MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-08-31"
evidence_count: 5
github_description: "GDAL is an open source MIT licensed translator library for raster and vector geospatial data formats."
github_language: "C++"
github_license_spdx: "NOASSERTION"
github_default_branch: "master"
github_stars: 6040
github_topics: ["geospatial-data", "raster", "remote-sensing", "vector"]
github_homepage: "https://gdal.org"
github_pushed_at: "2026-08-31T14:19:31Z"
---
# OSGeo - gdal

## Bottom Line
The translation layer nearly every geospatial tool sits on: one abstract data model for raster and vector, with drivers for well over two hundred formats and reprojection built in.

## What It Solves
- Read and write almost any geospatial format through a single API instead of per-format libraries.
- Reproject between coordinate reference systems reliably.
- Process imagery larger than memory through windowed and tiled access.

## Architecture & Mechanics
- An abstract dataset model separates format drivers from consuming code.
- Raster and vector (OGR) sides share the driver and CRS infrastructure.
- PROJ handles datum and coordinate-system transformation.
- Virtual formats (VRT) and /vsicurl/ allow lazy, remote and composed datasets.

## What Is Inside
- **The test suite is more than half the repository, and it is the most valuable part for outsiders** — `autotest/` is 6,922 of 12,305 files: `autotest/gdrivers/` (3,048) holds sample files for hundreds of raster formats, `autotest/ogr/` (2,535) the same for vector. 536 `.tif` files and 114 golden-output fixtures. If you need a real file in an obscure geospatial format, it is probably in here.
- **Format drivers as separable units** — `frmts/` (1,585), one directory per raster format (`grib` 205, `pcidsk` 155, `gtiff` 142, `wms` 57); `ogr/ogrsf_frmts/` (1,034) the same for vector.
- **Machine-readable CLI contracts** — `apps/data/*.schema.json`: `gdal_algorithm.schema.json`, `gdalinfo_output.schema.json`, `ogrinfo_output.schema.json`, `gdalmdiminfo_output.schema.json`. The tools' output is a documented schema, not just text.
- **861 documentation source files** — `doc/source/`, with 233 images and its own sample data (`doc/data/circle.geojson`, `doc/data/fortune.tif`).
- **Bindings generated from one interface definition** — `swig/` (286 files) for Python, Java, C# and others.
- **A benchmark suite run in CI** — `autotest/benchmark/`, with its own conftest.
- **Governance and agent instructions in-tree** — `GOVERNANCE.md`, `CITATION.cff`, and an `AGENTS.md`.

## Transferable Capability
**Put one translation layer between many incompatible formats and everything that consumes them, so a consumer learns one interface instead of hundreds.** The design decision that makes it survive is that each format is a separable driver behind a common model, so adding a format costs nobody anything and dropping one breaks only its users. The separable artefact, valuable on its own: **a very large corpus of real files in obscure formats**, assembled to test the readers and usable by anyone testing anything else.

**Alternative to:** each consumer handling each format, which is quadratic and guarantees inconsistency. **Applies wherever** many incompatible representations describe the same kind of thing.

## Taxonomy
- Ecosystem: Geo_Data
- Domain Primary: Geospatial
- Maturity Stage: Production_Ready
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: CLI
- Data Locality: Local_First
- Hardware Footprint: High_Memory
- Security Compliance: Uncertified
- Agent Surface: Documented

## Integration & Use Cases
- Normalise a mixed archive of imagery and vector files into one working format.
- Build cloud-native raster pipelines reading COGs directly from object storage.
- Study driver-based abstraction over a very heterogeneous format landscape.

## Reading Notes
**Four licences, reproduced in full, in one file.** The LICENSE names **Apache-2.0,
BSD-3-Clause, ISC and MIT** — all permissive, so the classification is safe — but the
composite is a symptom of what GDAL is: a translation layer wrapping a very large number of
third-party format drivers, many of which arrive with their own terms. The repository-level
licence is not the whole answer for a build that enables a specific driver set; the driver's
own licence is.

## Semantic Links
- [parent_topic:: [[Topic - Geospatial & Earth Data]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[geopandas - geopandas]]]
- [related_to:: [[opengeos - leafmap]]]
- [related_to:: [[stac-utils - pystac]]]
- [implements_pattern:: [[Pattern - Spatial Indexing]]]
- [implements_pattern:: [[Pattern - Schema Mapping]]]
- [implements_pattern:: [[Pattern - ETL API Ingestion]]]
- [mentions_term:: [[Glossary - Geospatial Data]]]
- [mentions_term:: [[Glossary - Raster]]]
- [mentions_term:: [[Glossary - Vector Data]]]
- [mentions_term:: [[Glossary - Coordinate Reference System]]]
- [mentions_term:: [[Glossary - Satellite Imagery]]]

## Evidence
- Source URL: https://github.com/OSGeo/gdal
- Source kind: GitHub REST metadata plus maintainer documentation
- Ingestion mode: agent-curated note authored against live repository metadata
- Metadata captured: 2026-08-31
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names Apache-2.0, BSD-3-Clause, ISC, MIT (4 reproduced in full, 0 referred to). The GitHub API reported `NOASSERTION`, which is why this was read directly.  **Composite - needs a person to confirm.**

## GitHub Snapshot

- Description: GDAL is an open source MIT licensed translator library for raster and vector geospatial data formats.
- Language: C++
- License (SPDX): NOASSERTION
- Default Branch: master
- Stars: 6040
- Homepage: https://gdal.org
- Pushed At: 2026-08-31T14:19:31Z
- Topics: geospatial-data, raster, remote-sensing, vector

## Evidence Anchors
- [github_repo] description :: GDAL is an open source MIT licensed translator library for raster and vector geospatial data formats. (confidence 0.95)
- [github_repo] language :: C++ (confidence 0.90)
- [github_repo] license :: NOASSERTION (confidence 0.90)
- [github_repo] topics :: geospatial-data, raster, remote-sensing, vector (confidence 0.85)
