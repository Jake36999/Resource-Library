# Opening prompt — research and cataloguing session

*Paste everything below into a new session. Connect `D:\Resource-Library` first.*

---

You are running a research and cataloguing pass for the Resource Library, an Obsidian vault at `D:\Resource-Library`. It is a catalogue of open-source resources built so that people and co-operating agents can find proven prior work quickly instead of rediscovering it.

I have a list of repositories I found while researching a particular area. I want them catalogued properly, and then I want to know what is actually in them.

## Before you start

Read these, in this order, so you understand the conventions you are writing into:

1. `00-Indexes/Master Index.md` — the router, and the operating rules at the bottom
2. `00-Indexes/Implementation Brief.md` — current state of the system
3. `00-Indexes/Design Specification.md` — how the system is meant to work
4. `00-Indexes/Scouting Domains.md` — the authoritative domain register
5. Three or four existing notes in `01-Resources/` — the format you will be matching
6. `09-Applications/Application Index.md` — how use is recorded

`.utility/librarian/README.md` describes tooling that already exists. Use it where it helps.

## Phase one — scout and document

**Complete phase one entirely before beginning phase two.** Do not start forming opinions about usefulness while you are still gathering. The purpose of the separation is that a judgement formed early narrows what you look at afterwards.

For each repository below, work through the same sequence the library's automated pipeline follows:

**Locate and verify.** Confirm the repository exists at the path given, and record its canonical location. Fetch its live metadata — description, language, licence, activity, topics, stars. Never write a metadata field from memory; if the API does not give it, record `Unknown`. Check whether it is already catalogued before creating anything.

**Read the source, not the summary.** Read the README, then go further: documentation directories, architecture notes, specifications, example code, tests. A repository's README describes what its authors want you to notice. Its structure describes what it actually does. Where those differ, the structure is the more interesting fact.

**Classify.** Assign a domain from the register. If nothing fits, record it as unmatched and say what a fitting domain would have been — do not invent a domain key or stretch an existing one to fit.

**Document.** Write a resource note matching the existing format exactly. Every section must describe *this* source specifically. If two of your notes could be swapped without either becoming wrong, both are too generic and need rewriting. Record the licence class accurately, including where a licence is source-available rather than open source. Flag anything dual-use for the review queue rather than approving it yourself.

**Link.** Connect the note to the patterns, glossary terms and topics it genuinely relates to. Create new pattern or glossary notes where a source introduces a concept the vault has no word for — that is a legitimate addition, unlike inventing a domain.

Answer these for every repository, in the note or in your working file:

- What does it actually do, stated so someone who has never heard of it would understand?
- What problem is it solving, and for whom?
- How does it work — what are the moving parts and how do they fit together?
- What does it assume about the environment it runs in?
- What does it deliberately *not* do?
- What is its maturity, and what is the evidence for that?

## The repositories

**Lakehouse architecture and data lineage**
- `Victor-Kipruto-Rop/medallion-lakehouse-platform` — Bronze/Silver/Gold layering
- `PHACDataHub/data-mesh-ref-impl` — enterprise data mesh reference implementation
- `open-metadata/OpenMetadata` — active metadata, auto-tagging, lineage across databases
- `shenhuan2021/gudu-sql-omni-introduce` — column-level SQL parsing and lineage from transformations
- `recipy/recipy` — lightweight run-time data provenance in Python

**Structural parsing and abstract syntax trees**
- `tree-sitter/tree-sitter` — incremental parsing, concrete syntax trees
- `Instagram/LibCST` — Python CST preserving whitespace and formatting
- `semgrep/semgrep` — structural code querying rather than text matching
- `syntax-tree/mdast` — the Markdown abstract syntax tree specification

**Semantic extraction and weak supervision**
- `snorkel-team/snorkel` — programmatic labelling via heuristic functions
- `urchade/GLiNER` — generalist named entity recognition without fine-tuning
- `NorskRegnesentral/skweak` — weak supervision for NLP entity extraction

**Graph reasoning, search and inference**
- `microsoft/graphrag` — entity extraction into a knowledge graph for multi-hop reasoning
- `run-llama/llama_index` — retrieval orchestration and multi-tier indexing
- `neo4j-labs/neocarta` — semantic layer graphs for agent query routing
- `ganarajpr/awesome-dspy` — programming language models rather than prompting them
- `HCAI-Lab-GT/capabilibara` — AI capability provenance, mapping training data influence

Some of these may be small, abandoned, or not what their description suggests. Record that finding as carefully as you would record a good one — a negative result stops the next person re-examining it.

If following a reference inside one of these leads somewhere clearly relevant, catalogue that too and say why you followed it. Do not restrict yourself to the list where the list is obviously incomplete.

## Phase two — assessment

Only once every repository above is documented, work out what any of it means for the library itself.

The system you have been reading about is one design among many possible ones. Some of these sources will have solved problems it has solved, differently. Some will have solved problems it has not recognised as problems. Some will make assumptions it does not make, and be right to.

Assess against that, not against a checklist of the current design. Specifically, I am **not** only asking what could be optimised. I want to know:

- Where does a source do something the system has no equivalent for at all?
- Where does a source contradict a decision the system has made — and where, on the evidence, is the source right?
- What capability would become available that is not currently on any roadmap?
- What is being done here by hand that one of these makes deterministic?
- What would a source cost to adopt — in dependencies, complexity, operational burden and reversibility?
- What should be deliberately *not* adopted, and why? A well-argued rejection is as useful as a recommendation.
- Which of these overlap with each other, and where an overlap exists, which is the better fit and why?

Be willing to conclude that something changes the shape of the system rather than a detail of it. Be equally willing to conclude that a well-regarded project has nothing to offer here.

## The report

Write it to `00-Indexes/` as a dated research report, and link it from the Master Index.

For each candidate change, give me:

- **What it is** — the source, and the specific thing within it
- **What it offers** — the capability or property gained, concretely
- **How the system would change** — which components, which documents, which decisions are affected
- **What it costs** — dependencies, complexity, operational burden, and how hard it would be to reverse
- **Confidence** — how much of this you verified against the source versus inferred, and where you are uncertain

Then, separately:

- Which candidates you would sequence first, and why that order
- What you found that surprised you
- What you looked for and could not find
- Where the sources disagree with each other, and what that disagreement tells us

Rank by expected value to the system, not by how impressive the source is.

## How to work

Fetch and verify rather than recall. Every factual claim needs a source, and `Unknown` is a valid answer where a plausible guess is not.

Distinguish what a source claims from what you confirmed. If you read the README but not the code, say so.

Cover the whole list before going deep on the most interesting one. Depth on the first three and a paragraph on the rest is the failure mode here — the point of an even pass is that you cannot know in advance where the useful thing is.

Tell me when you are wrong about something, including if it means undoing work you have already done.

If something blocks you — a rate limit, an unreachable repository, a tool that will not run — say so plainly and carry on with what you can reach. Do not work around a blocked capability by building a replacement for it.

Start with phase one.
