---
type: "content_model"
status: "active"
created: "2026-09-03"
authority: "This note is the schema. `integrity.py` parses it; nothing else defines note shape."
shapes: 5
---

# Note Content Model

## How This Note Is Used

This note **is** the note schema. `librarian/integrity.py` parses the tables below and
validates the vault against them, so the schema changes by editing this file and in no other
way. That is `NO_SCHEMA_DRIFT` made operational rather than aspirational: before this note
existed, the required shape of a resource note lived in three places — prose in
[[Design Specification]], hand-written assertions in `integrity.py`, and implicit knowledge in
`notes.py` — and none of them could be checked against the others.

The approach is deliberately the weaker of the two available. **OpenMetadata** generates its
Java, Python and TypeScript models from 904 JSON Schemas, so no binding can drift because none
is hand-written. **mdast** writes the format down in prose and lets implementations vary, which
is why mdast implementations exist outside JavaScript. For a vault where Markdown is truth and
the tooling is one small Python package, the mdast answer is the right size: *validate, do not
generate*. See [[Research Report 2026-09-03 - Lineage, Parsing and Graph Reasoning]] §5.4.

**A field is required when something in the system reads it.** That is the whole test. The
promoted columns in `resource_facet`, the filters `find_donor` eliminates on, the counts
`gap_fit` weights, the links traversal follows — those are required. Everything else a note
happens to carry is optional, because requiring a field nothing reads only makes notes harder
to write.

## Shapes

A shape is identified by the note's folder and its `type`, not by its filename.

| Shape | Identified by |
| --- | --- |
| resource | layer `resource` or `review`, and a `canonical_url` |
| topic | `type: topic_index` |
| pattern | `type: pattern` |
| glossary | `type: glossary_term` |
| application | `type: application_record` |

Hub and index notes — [[Master Index]], [[Pattern Index]], [[Glossary Index]],
[[Review Queue]], this note — match no shape and are not validated. They are written for
people, and constraining their prose would buy nothing.

## Frontmatter — resource

| Field | Requirement |
| --- | --- |
| uuid | required |
| canonical_url | required |
| repo_key | required |
| type | required |
| primary_topic | required |
| status | required |
| license | required |
| ecosystem | required |
| domain_primary | required |
| maturity_stage | required |
| license_class | required |
| deployment_target | required |
| interface_protocol | required |
| data_locality | required |
| hardware_footprint | required |
| security_compliance | required |
| agent_surface | required |
| github_stars | required |
| github_pushed_at | required |
| owner | optional |
| repo_name | optional |
| aliases | optional |
| secondary_topics | optional |
| patterns | optional |
| glossary_terms | optional |
| maturity | optional |
| sensitivity | optional |
| source_file | optional |
| ingestion_agent | optional |
| metadata_captured_at | optional |
| evidence_count | optional |
| container | optional |
| expansion_status | optional |
| github_description | optional |
| github_language | optional |
| github_license_spdx | optional |
| github_default_branch | optional |
| github_topics | optional |
| github_homepage | optional |

`github_license_spdx` is **optional and must never be corrected**. It records what the GitHub
API returned. Where it disagrees with `license`, the disagreement is the finding — see
[[Licence Resolution 2026-09-03]].

## Frontmatter — topic

| Field | Requirement |
| --- | --- |
| topic_key | required |
| type | required |
| status | required |
| inclusion_criteria | required |
| resource_count | required |
| review_count | required |
| canonical_vocabulary | optional |
| patterns | optional |
| glossary_terms | optional |
| created | optional |

`resource_count` is required because `scout.rank.gap_fit` reads it and carries the largest
ranking weight. It is maintained by `librarian views`, never by hand.

## Frontmatter — pattern

| Field | Requirement |
| --- | --- |
| pattern_key | required |
| type | required |
| status | required |
| aliases | optional |
| examples | optional |
| glossary_terms | optional |
| topic_keys | optional |

## Frontmatter — glossary

| Field | Requirement |
| --- | --- |
| term_key | required |
| canonical_word | required |
| type | required |
| status | required |
| sense_label | optional |
| aliases | optional |
| related_terms | optional |
| topic_keys | optional |

## Frontmatter — application

| Field | Requirement |
| --- | --- |
| type | required |
| project | required |
| stage | required |
| resources_used | required |
| outcome | required |
| patterns_discovered | optional |
| domains | optional |
| attested_by | optional |
| date_range | optional |

## Sections — resource

| Order | Section | Requirement |
| --- | --- | --- |
| 1 | Bottom Line | required |
| 2 | What It Solves | required |
| 3 | Architecture & Mechanics | required |
| 4 | What Is Inside | optional |
| 5 | Transferable Capability | optional |
| 6 | Taxonomy | required |
| 7 | Integration & Use Cases | required |
| 8 | Reading Notes | optional |
| 9 | Semantic Links | required |
| 10 | Evidence | required |
| 11 | GitHub Snapshot | required |
| 12 | Evidence Anchors | optional |

**`Transferable Capability` is what makes a source findable from outside its own field.**
`Bottom Line` says what a source is in its domain's terms, which is findable only by someone
already standing in that domain. This section says what it *does*, stated without that
vocabulary, and what that makes it an alternative to. Medallion layering described as a
lakehouse convention is invisible to anyone not building a lakehouse; described as *grading
material by refinement so a mistake is corrected by replay*, it is a candidate anywhere that
shape recurs. See [[Use Contexts And Agnostic Description]] for why this is the difference
between a reference guide and a list of links.

It is optional for the same reason as the section below: it must be earned, not filled in. And
it carries one prohibition — **it may not be written toward this system's current design**. A
capability described as "useful for our pipeline" has been narrowed to the architecture that
happens to exist, which defeats the purpose.

**`What Is Inside` is the section that makes a niche need findable**, and it is the one most
easily skipped. `Bottom Line` says what a source is and `Architecture & Mechanics` says how it
works; neither says *what kind of material is in there* — code, a specification, grammars,
worked examples, benchmark data, notebooks, rule corpora, diagrams — or **where**.

That distinction decides whether the catalogue works. "GLiNER does zero-shot NER" is true and
nearly useless. "`docs/architectures.md` sets out nine architecture variants; `gliner/multitask/`
carries QA, relation-extraction and summarisation heads over the same backbone; `benchmarks/`
has recorded results" is findable by somebody who needs a relation-extraction head and has no
idea GLiNER has one. A source's most valuable content is routinely not what its abstract
describes, and an abstract description of it is how a library loses that content permanently.

Paths are **addresses, not content**, which is the same argument §3.4 of
[[Design Specification]] uses to permit access points as the one durable extract. An inventory
points outward; it does not copy inward.

It is optional because it must never be filled in from a README. A note gains one when
somebody has actually read the tree, and its absence marks a source nobody has opened.

**As of 2026-09-03 every resource note has one.** All 81 sources were read from a blobless
clone and their trees surveyed; see [[Source Documentation Standard]] for the obligation and
[[Research Report 2026-09-03 - Lineage, Parsing and Graph Reasoning]] §0 for what the added
specificity did to retrieval. The section stays optional in the schema because a future
source enters the catalogue before anyone has opened it, and that state must be
representable rather than papered over.

**`Reading Notes` is optional on purpose, and its absence is a signal rather than a defect.**
It holds the finding that fits nowhere else — a project in declared maintenance mode behind a
large star count, a composite licence, a demo rendering synthetic data. A note without one is
a source nobody has re-read since the note was written, which makes the gap queryable and
makes it a natural input to a re-read queue. It must never become a slot to fill: 45 notes
currently have none, and forty-odd near-identical sections would damage retrieval measurably.

## Sections — topic

| Order | Section | Requirement |
| --- | --- | --- |
| 1 | Inclusion Criteria | required |
| 2 | Canonical Vocabulary | required |
| 3 | Why This Topic Exists | required |
| 4 | Mechanics | required |
| 5 | Typical Use Cases | required |
| 6 | Approved Resources | required |
| 7 | Review Queue | required |
| 8 | Related Patterns | required |
| 9 | Related Glossary | required |
| 10 | Related Topics | required |

## Sections — pattern

| Order | Section | Requirement |
| --- | --- | --- |
| 1 | Definition | required |
| 2 | Why It Matters | required |
| 3 | Example Repositories | required |
| 4 | Related Glossary | required |
| 5 | Related Topics | required |

## Sections — glossary

| Order | Section | Requirement |
| --- | --- | --- |
| 1 | Definition | required |
| 2 | Aliases | required |
| 3 | Related Terms | required |
| 4 | Observed Contexts | required |
| 5 | Sense Notes | required |

## Sections — application

| Order | Section | Requirement |
| --- | --- | --- |
| 1 | What Was Needed | required |
| 2 | What Was Found And Taken | required |
| 3 | What It Replaced | required |
| 4 | What The Catalogue Should Learn | required |

## Claim Sections And Caveat Sections

Retrieval does not treat these alike, so the schema must name which is which.
`consult.CLAIM_SECTIONS` is the authority in code; this is what it means.

**Claim** — `Bottom Line`, `What It Solves`, `Architecture & Mechanics`, `What Is Inside`,
`Transferable Capability`, `Integration & Use Cases`, `Taxonomy`. A term match here is evidence
the source does the thing, and counts toward ranking.

**Caveat** — `Reading Notes`, `Evidence`. A term match here is evidence about the source, often
the opposite of a claim, and earns no ranking credit. Still searchable: *which sources are
abandoned* is a real question.

The consequence for anyone writing a note: **a capability stated only in a caveat or an
inventory is unfindable.** See [[Source Documentation Standard]], *Recorded Is Not Findable*.

## Axis Values

The nine taxonomy axes are **closed enumerations**. A value outside these lists is an error,
not a new category: `find_donor` eliminates on several of these fields, so a typo does not
degrade a result, it removes a resource from every constrained answer silently.

Adding a value means editing this table, deliberately, and saying why in the note that
prompted it.

**2026-09-09 - six languages added to `ecosystem`:** `Rust`, `TypeScript`,
`JavaScript`, `Java`, `CSharp`, `CPlusPlus`. The first intake outside the original
cohort's subject matter left `ecosystem` empty on nearly every source, because the
enumeration had no value for the language the repository was actually written in.
`librarian.derive` returns nothing rather than forcing `Mixed`, which would say
something false about a single-language repository - so the gap surfaced as a field
a person had to fill on almost every note.

`CSharp` and `CPlusPlus` rather than `C#` and `C++`: FTS5's `porter unicode61`
tokenizer reduces both punctuated forms to the single token `c`, so a search for one
matches the other and every stray `c` besides. Measured, not assumed. The rest of
this enumeration has always been punctuation-free (`Web_CSS`, `Data_Platform`) for
the same reason.

Ruby, PHP, Kotlin, Swift and Haskell still have no value. They are left unmapped
deliberately: an axis that is empty says so, and one that is wrong does not.

| Axis | Permitted values |
| --- | --- |
| ecosystem | CAD_Modeling, CPlusPlus, CSharp, Data_Platform, Geo_Data, Go, Infrastructure_Automation, Java, JavaScript, Markdown, Mixed, Model_Serving, Observability, Python, Rust, Security_Analytics, Shell, TypeScript, Web_CSS, Web_Frontend |
| domain_primary | Agentic_AI, Architecture, Civic_Tech, Code_Intelligence, Data, Data_Lineage, Design, Discovery, Frontend, Geospatial, Infrastructure, Knowledge_Management, ML_Training, Scientific_Computation, Security |
| maturity_stage | Abandoned, Active, Production_Ready, Reference |
| license_class | Copyleft, Permissive, Source_Available, Unknown, Weak_Copyleft |
| deployment_target | Browser, Desktop, Local_Only, Server |
| interface_protocol | CLI, GUI, Markdown, Python_SDK, REST, Web_UI |
| data_locality | Distributed, Local_First, Stateless |
| hardware_footprint | Browser_Only, CPU_Only, High_Memory, Low_VRAM |
| security_compliance | Security_Adjacent, Uncertified |
| agent_surface | Callable, Documented, None, Procedural |

`agent_surface` records what an agent can do with the repository *without a person in the
loop*, and it is a ladder rather than a set of labels: `None`; `Documented` (an `AGENTS.md`,
`CLAUDE.md`, `.cursor/` or equivalent — instructions a person or agent reads); `Procedural`
(executable skills under `.claude/skills/`, `.agents/skills/`, `.opencode/skills/` — a
procedure an agent can run); `Callable` (the source *is* an agent-invocable interface, usually an MCP server). A source is recorded at the highest rung it reaches.

The axis was added on 2026-09-04 because the evidence demanded it: 19 of 81 sources carry
some surface, several of them substantial — netdata 197 agent-instruction paths, sentry 98,
airflow 63. A catalogue whose purpose is helping agents find prior work could not say which
of its own sources an agent could act on.

`Data_Lineage` was added on 2026-09-04, and it is the worked example of what this table is for.
[[Scouting Domains]] has listed `data_lineage_provenance` as a tier-1 domain since it was written,
with an explicit boundary against `data_api_big_data`: that domain answers *what data exists*, this
one answers *where it came from and what breaks if it changes*. The register could declare the
domain; it could not create the axis value, because this note is the only thing that may. The second
scouting cohort supplied eight resources sitting squarely inside that boundary, which is the
condition the register sets for a domain becoming a real index, so both were done at once -
[[Topic - Data Lineage & Provenance]] and this row. Nothing was recategorised to justify the
addition: [[recipy - recipy]] and [[shenhuan2021 - gudu-sql-omni-introduce]] moved because a lineage
index omitting the two lineage tools already catalogued would have been incoherent, and that move is
recorded in the topic note rather than left to be discovered.

`Code_Intelligence`, `Knowledge_Management` and `ML_Training` were introduced by the 2026-09
pass and could not be checked against anything, because until this note existed no artefact
enumerated these axes. Writing them here is what converts them from asserted to declared.

## When This Note Is Absent

A vault with no content model **degrades to no shape checks and says so**, as a warning
rather than an error. That follows the posture the rest of the system already takes: LM Studio
absent means filters and lexical search only, graphify absent means no communities, the
toolchain absent means documentation-only evidence. A catalogue that has not adopted a schema
is not in violation of one.

A model that *exists and will not parse* is a different thing and is an **error** — somebody
wrote it and it is wrong. In that case the checks that depend on it stand down rather than
reporting every note as malformed, so the one real defect is not buried under several hundred
false ones.

## What This Model Does Not Do

**It is the floor, not the standard.** [[Source Documentation Standard]] says what a note owes
a reader and why that cannot be reduced to a checkable list; this note is the part of it a
machine can enforce. A note passing every check here can still fail the standard, and usually
by being generic.

It does not validate prose quality, and it should not try. That a resource note has a
`Bottom Line` is checkable; that the Bottom Line is *any good* is not, and the check that
matters there already exists — `distinct_resource_prose` fails when two notes could be
swapped without either becoming wrong.

It does not enumerate `type` for resources. That field records what a source *is*
(`data_platform`, `developer_tool`, `ml_framework`, `specification`, `curated_list`) and the
vocabulary is still growing; closing it now would freeze a taxonomy that has not settled.

It does not generate anything. `notes.py` stays hand-written and this note stays a
specification, which is the mdast bargain: the cost is that a change here does not
automatically reach the code, and the check is what catches the gap.

## Related
- [[Source Documentation Standard]] — the obligation this schema sets a floor under
- [[Design Specification]] — `NO_SCHEMA_DRIFT`, and the note schema in prose
- [[Taxonomy Index]] — the nine axes as a comparison view
- [[Scouting Domains]] — the domain register, which is a different authority
- [[Research Report 2026-09-03 - Lineage, Parsing and Graph Reasoning]] — why this exists
- [[Master Index]]
