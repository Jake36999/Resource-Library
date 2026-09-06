---
uuid: "30fb2915-5f9b-524a-ab57-163617177614"
canonical_url: "https://github.com/opengeos/leafmap"
repo_key: "opengeos/leafmap"
owner: "opengeos"
repo_name: "leafmap"
aliases: ["opengeos/leafmap", "https://github.com/opengeos/leafmap"]
type: "geospatial_library"
primary_topic: "Geospatial & Earth Data"
secondary_topics: ["Frontend & Design Systems", "Data APIs & Big Data"]
ecosystem: "Geo_Data"
domain_primary: "Geospatial"
maturity_stage: "Active"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Python_SDK"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Spatial Indexing", "STAC Ingestion"]
glossary_terms: ["Geospatial Data", "Satellite Imagery", "STAC", "GeoJSON", "Raster"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-08-31"
evidence_count: 4
github_description: "A Python package for interactive mapping and geospatial analysis with minimal coding in a Jupyter environment"
github_language: "Python"
github_license_spdx: "MIT"
github_default_branch: "master"
github_stars: 3768
github_topics: ["data-science", "dataviz", "folium", "geoparquet", "geopython", "geospatial", "geospatial-analysis", "gis", "ipyleaflet", "jupyter", "jupyter-notebook", "leafmap", "mapping", "plotly", "python", "solara", "streamlit", "streamlit-webapp", "whiteboxtools"]
github_homepage: "https://leafmap.org"
github_pushed_at: "2026-08-30T16:50:00Z"
---
# opengeos - leafmap

## Bottom Line
Interactive geospatial mapping and analysis in Jupyter with very little code — a unified façade over ipyleaflet, folium, MapLibre and friends, wired to STAC and cloud raster sources.

## What It Solves
- Get an interactive analytical map on screen in a couple of lines inside a notebook.
- Switch plotting backends without rewriting the mapping code.
- Pull cloud-optimised GeoTIFFs and STAC collections straight into a notebook view.

## Architecture & Mechanics
- A common Map API wraps several rendering backends behind one interface.
- Layer helpers load local files, XYZ tiles, COGs and STAC items directly.
- Analysis helpers wrap WhiteboxTools and raster utilities for in-notebook processing.
- The same maps embed into Streamlit and Solara apps for sharing.

## What Is Inside
- **244 Jupyter notebooks — the notebooks are the product.** `docs/notebooks/` (119) and `docs/maplibre/` (117) each demonstrate one capability (`3d_buildings.ipynb`, `3d_choropleth.ipynb`, `3d_indoor_mapping.ipynb`), and the library exists to make them short. Only 39 `.py` files sit under `leafmap/`.
- **Sample geospatial data bundled** — `docs/data/` (34 files: `countries.dbf`, `states.csv`, `hex_data.csv`), `examples/data/` (40), `leafmap/data/` (6), plus 9 `.geojson`. Every notebook runs without a download.
- **Workshop material** — `docs/workshops/` (9 files), conference-length tutorials with their own narrative.
- **A JOSS paper** — `paper/` (3 files), so the design rationale is citable.
- **An agent-facing CI step** — `.github/workflows/claude-code-review.yml`.
- **Thin test suite** — `tests/` is 6 files; correctness is demonstrated by the notebooks rather than asserted.

## Transferable Capability
**Make the example the deliverable and the library the means.** When a capability is demonstrated by something runnable that produces a result in a few lines, the documentation problem and the API design problem collapse into one — an awkward interface shows up immediately as a long example. The enabling practice: **bundle the sample material**, so nothing has to be fetched before anything works.

**Alternative to:** reference documentation describing an interface, where the reader must assemble the first working thing themselves. **Applies wherever** adoption depends on somebody getting a result in the first few minutes.

## Taxonomy
- Ecosystem: Geo_Data
- Domain Primary: Geospatial
- Maturity Stage: Active
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Python_SDK
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Explore Earth-observation data interactively before building a pipeline.
- Publish a lightweight geospatial dashboard from notebook code.
- Teach GIS concepts without desktop software installation.

## Semantic Links
- [parent_topic:: [[Topic - Geospatial & Earth Data]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[OSGeo - gdal]]]
- [related_to:: [[geopandas - geopandas]]]
- [related_to:: [[stac-utils - pystac]]]
- [implements_pattern:: [[Pattern - Spatial Indexing]]]
- [implements_pattern:: [[Pattern - STAC Ingestion]]]
- [mentions_term:: [[Glossary - Geospatial Data]]]
- [mentions_term:: [[Glossary - Satellite Imagery]]]
- [mentions_term:: [[Glossary - STAC]]]
- [mentions_term:: [[Glossary - GeoJSON]]]
- [mentions_term:: [[Glossary - Raster]]]

## Evidence
- Source URL: https://github.com/opengeos/leafmap
- Source kind: GitHub REST metadata plus maintainer documentation
- Ingestion mode: agent-curated note authored against live repository metadata
- Metadata captured: 2026-08-31

## GitHub Snapshot

- Description: A Python package for interactive mapping and geospatial analysis with minimal coding in a Jupyter environment
- Language: Python
- License (SPDX): MIT
- Default Branch: master
- Stars: 3768
- Homepage: https://leafmap.org
- Pushed At: 2026-08-30T16:50:00Z
- Topics: data-science, dataviz, folium, geoparquet, geopython, geospatial, geospatial-analysis, gis, ipyleaflet, jupyter, jupyter-notebook, leafmap, mapping, plotly, python, solara, streamlit, streamlit-webapp, whiteboxtools

## Evidence Anchors
- [github_repo] description :: A Python package for interactive mapping and geospatial analysis with minimal coding in a Jupyter environment (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: MIT (confidence 0.90)
- [github_repo] topics :: data-science, dataviz, folium, geoparquet, geopython, geospatial, geospatial-analysis, gis, ipyleaflet, jupyter, jupyter-notebook, leafmap, mapping, plotly, python, solara, streamlit, streamlit-webapp, whiteboxtools (confidence 0.85)
