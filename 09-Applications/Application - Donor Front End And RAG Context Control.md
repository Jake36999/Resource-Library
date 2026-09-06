---
type: "application_record"
project: "Agent application with retrieval memory"
stage: "architecture and build"
status: "active"
resources_used: ["open-source UI application (donor front end)", "open-source RAG/context-control implementation"]
patterns_discovered: ["single-store retrieval via a discriminating vector", "donor front end", "reusing an existing MCP surface"]
domains: ["agentic_ai_models", "frontend_design_systems", "knowledge_management"]
outcome: "front end and context layer both sourced rather than built; database count reduced from several to one"
---

# Application - Donor Front End And RAG Context Control

## What Was Needed
An application needing a competent, optimised front end and a way to control what context reached the model — with neither being the interesting part of the project, and both being expensive to build well.

## What Was Found And Taken
Two repositories, used in completely different ways.

The first was chosen for its interface and application style, and used as a **donor front end**: the codebase was taken as the starting shell rather than referenced. The selection criterion was not features but that the UI was already optimised and coherent, so it could be inherited rather than designed.

The second supplied a **design pattern rather than code**. It handled context control by adding a specific discriminating vector into the RAG memory database, which let one store serve what would otherwise have required several separate databases. The same repository also exposed MCP features and workflows that could be adopted directly, removing the design cost of that layer too.

## What It Replaced
Designing and building a front end, a multi-database context architecture, and an MCP integration surface from scratch. The second repository is the sharper saving: the multi-database design was already assumed necessary, and the pattern removed the requirement rather than implementing it faster.

## Patterns And Insights
**A vector can act as a discriminator, not just a similarity coordinate.** Adding a dimension that separates classes of memory means one index can serve several logical stores. The instinct to reach for separate databases per memory type is usually a modelling failure rather than a storage requirement — and this is exactly the kind of structural idea that is invisible in a repository description and only surfaces in someone else's implementation.

**Front ends are donatable in a way back ends usually are not.** Interface code is comparatively self-contained, so a well-made one transplants. That makes "would this donate well" a real selection criterion, distinct from "is this good software".

## What The Catalogue Should Learn
Three requirements fall out of this.

1. **Record donation suitability.** A resource that transplants cleanly is a different kind of asset from one you depend on. This is not captured by any current taxonomy axis, and it is the axis that mattered most here.
2. **Index architectural consequences, not just capabilities.** "Removes the need for multiple databases" is the sentence that made this repository valuable, and no field currently holds that kind of claim. The `Patterns And Insights` section of these records is where it lives until the resource schema catches up.
3. **Make MCP and integration surfaces searchable.** Adopting an existing MCP implementation was a significant saving and is not currently a searchable property.

## Semantic Links
- [application_hub:: [[Application Index]]]
- [related_workflow:: [[Workflow - Build A Knowledge Catalogue]]]
- [related_topic:: [[Topic - Agentic AI & Models]]]
- [related_topic:: [[Topic - Frontend & Design Systems]]]
