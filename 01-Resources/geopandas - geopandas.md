---
uuid: "ba922b28-9a5d-5f56-aafd-f53b2cb12dbf"
canonical_url: "https://github.com/geopandas/geopandas"
repo_key: "geopandas/geopandas"
owner: "geopandas"
repo_name: "geopandas"
aliases: ["geopandas/geopandas", "https://github.com/geopandas/geopandas"]
type: "geospatial_library"
primary_topic: "Geospatial & Earth Data"
secondary_topics: ["Data APIs & Big Data", "Scientific Simulation & Math"]
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
patterns: ["Spatial Indexing", "Schema Mapping"]
glossary_terms: ["Geospatial Data", "Vector Data", "Coordinate Reference System", "GeoJSON", "Dataset"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "BSD-3-Clause"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-05"
evidence_count: 4
github_description: "Python tools for geographic data"
github_language: "Python"
github_license_spdx: "BSD-3-Clause"
github_default_branch: "main"
github_stars: 5237
github_topics: ["geoparquet", "geospatial", "pandas", "python", "spatial"]
github_homepage: "http://geopandas.org/"
github_pushed_at: "2026-09-04T21:48:18Z"
---
# geopandas - geopandas

## Bottom Line
Adds a geometry column to the Pandas DataFrame, so spatial joins, overlays and reprojection become ordinary dataframe operations in the scientific-Python stack.

## What It Solves
- Do spatial analysis without leaving Pandas for a GIS desktop application.
- Join tabular attributes to geometry with familiar merge semantics.
- Read and write GeoJSON, Shapefile, GeoPackage and GeoParquet through one interface.

## Architecture & Mechanics
- A GeoSeries stores Shapely geometries as a Pandas extension array.
- GEOS provides the predicate and overlay operations underneath.
- An R-tree spatial index accelerates joins and nearest-neighbour queries.
- Pyogrio/Fiona and PROJ supply file I/O and CRS transformation.

## What Is Inside
- **A small library with a large I/O test corpus** — `geopandas/` (247 files) of which `tests/` is 132 and `io/` is 85. The interesting part for outsiders is `geopandas/io/tests/data/`: 59 `.geojson`, 37 `.arrow`, 24 `.parquet`, including a **GeoParquet conformance set organised by spec version** (`data/arrow/geoparquet/1.1.0/data-linestring-encoding_native.parquet`) and GeoArrow examples per geometry encoding (`example-linestring-interleaved.arrow`, `example-linestring-wkb.arrow`).
- **Version-pinned GDAL fixtures** — `test_data_gdal350.parquet`, `test_data_gdal390.parquet`, so behaviour differences between GDAL releases are testable rather than anecdotal.
- **Eighteen tutorial notebooks** — `doc/source/docs/user_guide/`: `spatial_indexing.ipynb`, `interactive_mapping.ipynb`, `sampling.ipynb` and others, each runnable.
- **Set operations explained with SVG** — `doc/source/_static/binary_geo-intersection.svg`, `binary_geo-difference.svg` and siblings; the geometry predicates are documented pictorially.
- **An ASV benchmark suite** — `benchmarks/`: `clip.py`, `geom_methods.py` and others, so performance claims are measured.
- **Reproducible CI environments** — `ci/envs/` pins a conda environment per Python version and per dependency set.

## Transferable Capability
**Add one dimension to an existing, well-understood abstraction rather than inventing a parallel one.** By making the special thing a column in a familiar table, everything already known about tables continues to work and only the genuinely new operations must be learned. The separable practice: **hold conformance fixtures organised by specification version and by the version of the tool that wrote them**, so behaviour differences between releases become testable facts rather than folklore.

**Alternative to:** a separate specialised structure with its own vocabulary for everything, including the parts that were never special. **Applies wherever** a domain adds one property to data that otherwise behaves ordinarily.

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
- Join administrative boundaries to point observations for aggregation.
- Prepare geospatial features for machine-learning pipelines.
- Study extension-array design for adding domain types to Pandas.

## Semantic Links
- [parent_topic:: [[Topic - Geospatial & Earth Data]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[OSGeo - gdal]]]
- [related_to:: [[opengeos - leafmap]]]
- [related_to:: [[duckdb - duckdb]]]
- [implements_pattern:: [[Pattern - Spatial Indexing]]]
- [implements_pattern:: [[Pattern - Schema Mapping]]]
- [mentions_term:: [[Glossary - Geospatial Data]]]
- [mentions_term:: [[Glossary - Vector Data]]]
- [mentions_term:: [[Glossary - Coordinate Reference System]]]
- [mentions_term:: [[Glossary - GeoJSON]]]
- [mentions_term:: [[Glossary - Dataset]]]

## Evidence
- Source URL: https://github.com/geopandas/geopandas
- Source kind: GitHub REST metadata plus maintainer documentation
- Ingestion mode: agent-curated note authored against live repository metadata
- Metadata captured: 2026-08-31

## GitHub Snapshot

- Description: Python tools for geographic data
- Language: Python
- License (SPDX): BSD-3-Clause
- Default Branch: main
- Stars: 5237
- Homepage: http://geopandas.org/
- Pushed At: 2026-08-31T18:34:56Z
- Topics: geoparquet, geospatial, pandas, python, spatial

## Evidence Anchors
- [github_repo] description :: Python tools for geographic data (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: BSD-3-Clause (confidence 0.90)
- [github_repo] topics :: geoparquet, geospatial, pandas, python, spatial (confidence 0.85)
