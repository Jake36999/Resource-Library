---
pattern_key: "spatial_indexing"
aliases: ["geometry index"]
type: "pattern"
status: "active"
examples: ["geopandas - geopandas", "OSGeo - gdal", "opengeos - leafmap"]
glossary_terms: ["Geospatial Data", "Vector Data", "Coordinate Reference System"]
topic_keys: ["geospatial_earth_data"]
---

# Pattern - Spatial Indexing

## Definition
Geometries are organised into a tree structure (typically R-tree) so spatial joins and proximity queries prune candidates instead of comparing every pair.

## Why It Matters
- Gives the vault a reusable architectural concept for graph traversal.
- Helps compare repositories that solve the same problem in different ways.

## Example Repositories
- [[geopandas - geopandas]]
- [[OSGeo - gdal]]
- [[opengeos - leafmap]]

## Related Glossary
- [[Glossary - Geospatial Data]]
- [[Glossary - Vector Data]]
- [[Glossary - Coordinate Reference System]]

## Related Topics
- [[Topic - Geospatial & Earth Data]]
