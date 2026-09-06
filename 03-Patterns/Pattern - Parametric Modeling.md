---
pattern_key: "parametric_modeling"
aliases: ["feature-based modeling"]
type: "pattern"
status: "active"
examples: ["FreeCAD - FreeCAD", "CadQuery - cadquery", "openscad - openscad"]
glossary_terms: ["Parametric Modeling", "CAD", "Boundary Representation"]
topic_keys: ["cad_saas_design"]
---

# Pattern - Parametric Modeling

## Definition
Geometry is stored as a dependency graph of parameters and features, so editing a driving value regenerates all dependent shapes instead of requiring a redraw.

## Why It Matters
- Gives the vault a reusable architectural concept for graph traversal.
- Helps compare repositories that solve the same problem in different ways.

## Example Repositories
- [[FreeCAD - FreeCAD]]
- [[CadQuery - cadquery]]
- [[openscad - openscad]]

## Related Glossary
- [[Glossary - Parametric Modeling]]
- [[Glossary - CAD]]
- [[Glossary - Boundary Representation]]

## Related Topics
- [[Topic - CAD & SaaS Design]]
