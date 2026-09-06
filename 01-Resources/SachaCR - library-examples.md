---
uuid: "1c97cf43-0ebb-5d25-87b8-97cd6c6cf29f"
canonical_url: "https://github.com/SachaCR/library-examples"
repo_key: "SachaCR/library-examples"
owner: "SachaCR"
repo_name: "library-examples"
aliases: ["SachaCR/library-examples", "https://github.com/SachaCR/library-examples"]
type: "reference_implementation"
primary_topic: "Knowledge Management"
secondary_topics: ["Architecture & Developer Playbooks"]
ecosystem: "Web_Frontend"
domain_primary: "Architecture"
maturity_stage: "Abandoned"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "REST"
data_locality: "Stateless"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "Documented"
patterns: ["Ontology-Driven Design", "Reference Architecture", "Policy As Schema"]
glossary_terms: ["Ontology", "Design Pattern", "Dependency Injection", "Schema"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 5
github_description: "A library management app example with Ontologic"
github_language: "TypeScript"
github_license_spdx: "MIT"
github_default_branch: "main"
github_stars: 0
github_pushed_at: "2026-08-18T10:43:49Z"
---
# SachaCR - library-examples

## Bottom Line
A library-management application written to demonstrate ontology-driven domain design: the domain layer is thirty of fifty-one source files, the invariants are documented as an article, and the tests are written in Gherkin against the domain rather than against the API.

## What It Solves
- See a bounded context defined by an ontology rather than by a database schema.
- Express business invariants as domain rules that tests can check directly.
- Keep the domain independent of the framework it is served through.

## Architecture & Mechanics
- The proportions state the thesis: `src/domain/` is 30 of 51 source files, `src/presentation/` is 17, `src/infrastructure/` is 4. The domain is the largest layer and the persistence layer is nearly nothing — the inversion of a typical application.
- The domain is subdivided by role — `entities/`, `repositories/`, `use-cases/` — and each has its own `__tests__/` directory alongside it, so a rule and its check sit together.
- Tests are behavioural and domain-facing: `book.entity.test.ts`, `loan.entity.test.ts`, `searchBook.test.ts`, `addBook.test.ts` — the vocabulary is the domain's, not HTTP's.
- The Gherkin-domain-test convention is itself packaged for tooling: `.cursor/rules/unit-tests-gherkin-domain.mdc` and `.cursor/skills/vitest-gherkin-domain-tests/SKILL.md` — the house style written down where an agent will read it.
- **Not read:** any TypeScript file or article. The layer proportions are file counts; the Gherkin convention is read from the rule and skill filenames.

## What Is Inside
- **Two design articles** — `docs/articles/01-bounded-context-and-ontologic.md` and `02-invariants.md`. The reasoning is here; the code is the demonstration.
- **A domain layer that dominates** — `src/domain/` (30 files) against `src/infrastructure/` (4). Worth looking at purely for the ratio.
- **Tests colocated with the domain** — `src/domain/entities/book/__tests__/`, `loan/__tests__/`, `src/domain/use-cases/__tests__/`, `src/domain/repositories/__tests__/`.
- **A house testing convention as agent-readable rules** — `.cursor/rules/unit-tests-gherkin-domain.mdc`, `.cursor/skills/vitest-gherkin-domain-tests/SKILL.md`.
- **A NestJS application** — `nest-cli.json`, `vitest.config.ts`, `pnpm-lock.yaml`.
- **Not here:** a database, or the `Ontologic` library the description names, which is an external dependency.

## Transferable Capability
**Let the domain model be the largest thing in the codebase and the persistence layer the smallest.** When a schema drives the design, the application ends up shaped like its storage and the invariants live in scattered validation code. Inverting that — ontology first, storage as a detail — makes the rules statable in one place and testable without a database. The ratio here (30 files against 4) is the measurable form of the claim.

The second transferable practice is **writing the house convention where the tooling will read it**: `.cursor/rules/` and a `SKILL.md` make the testing style enforceable by an agent rather than dependent on review. That is the general move of turning a convention from something remembered into something applied.

**Alternative to:** schema-first design, which is faster to start and pushes meaning into the persistence layer; and to a style guide in a wiki, which is not consulted at the moment code is written. **Applies wherever** business rules must survive a change of storage or framework.

## Taxonomy
- Ecosystem: Web_Frontend
- Domain Primary: Architecture
- Maturity Stage: Abandoned
- License Class: Permissive
- Deployment Target: Server
- Interface Protocol: REST
- Data Locality: Stateless
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: Documented

## Integration & Use Cases
- Read `docs/articles/02-invariants.md` before deciding where a business rule should live.
- Copy the colocated `__tests__/` layout so a rule and its check cannot drift apart.
- Take the `.cursor/rules` plus `SKILL.md` approach for any convention currently enforced only by code review.

## Reading Notes
**Archived, last pushed 2026-08-18**, and it was only created 2026-04-02 — a short-lived demonstration accompanying two articles rather than a maintained project, which is the appropriate lifespan for what it is. Zero stars. Note that `Ontologic`, the library the description names as the point of the example, is not in the tree; judging the approach requires looking at that dependency too, which was not done here.

## Semantic Links
- [parent_topic:: [[Topic - Knowledge Management]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[mdebellis - SemanticKG-Design]]]
- [related_to:: [[DovAmir - awesome-design-patterns]]]
- [related_to:: [[goldbergyoni - nodebestpractices]]]
- [implements_pattern:: [[Pattern - Ontology-Driven Design]]]
- [implements_pattern:: [[Pattern - Reference Architecture]]]
- [implements_pattern:: [[Pattern - Policy As Schema]]]
- [mentions_term:: [[Glossary - Ontology]]]
- [mentions_term:: [[Glossary - Design Pattern]]]
- [mentions_term:: [[Glossary - Dependency Injection]]]
- [mentions_term:: [[Glossary - Schema]]]

## Evidence
- Source URL: https://github.com/SachaCR/library-examples
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata, the complete file tree at HEAD, and the LICENSE file; no TypeScript source or article was opened

## GitHub Snapshot

- Description: A library management app example with Ontologic
- Language: TypeScript
- License (SPDX): MIT
- Default Branch: main
- Stars: 0
- Pushed At: 2026-08-18T10:43:49Z

## Evidence Anchors
- [github_repo] description :: A library management app example with Ontologic (confidence 0.95)
- [github_repo] language :: TypeScript (confidence 0.90)
- [github_repo] license :: MIT (confidence 0.90)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 64 paths at HEAD (confidence 0.95)
