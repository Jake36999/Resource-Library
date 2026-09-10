# Resource Library

A catalogue of open-source software, read and written down so that the next
person with a problem can find what already solves it before building anything.

It is two things kept deliberately apart. **An Obsidian vault** of notes, each
one describing a source that was actually opened and read — what it does, what
it is made of, and what it would be worth borrowing. And **`librarian`**, a
small Python tool that indexes those notes and answers questions against them
from a terminal, a browser, or a model.

The question it exists to answer is narrow and it is always the same:

> *Is this something I can use as donor code, as a reference, or as a tool?*

Everything else — the taxonomy, the ranking, the integrity checks — is
machinery for answering that faster than reading a hundred repositories again.

---

## Why a catalogue and not a search engine

Searching GitHub returns what is popular. Searching this returns what someone
has already read and formed a view on, with the evidence attached.

The difference shows up in what a result carries. A source here has ten
taxonomy axes, a stated bottom line, a list of what it solves, a record of what
its repository actually contains at the file level, and — where one exists — an
account of a time it was used and what that was worth. None of that is
inferrable from a stars count.

The cost is that the catalogue is small and always will be, relative to the
ecosystem. It is built on the wager that a hundred sources you have read beat a
million you have not.

---

## Data, information, knowledge

The vault is layered, and the layers are not decoration — each one is allowed
to say different things, and the system refuses to let a lower layer claim what
only a higher one can.

| Layer | Where it lives | What it may assert |
| --- | --- | --- |
| **Data** | `.Data/surveys/` — file listings and metadata, exactly as fetched | Facts about a repository: this path exists, this licence was declared |
| **Information** | `01-Resources/` — one note per source | What it does and what it is for, with evidence cited |
| **Knowledge** | `03-Patterns/`, `09-Applications/` — patterns and application records | What worked, what it replaced, and what the catalogue should learn |

A pattern may generalise across sources. A resource note may not. A survey may
not draw a conclusion at all. Keeping these apart is what makes it possible to
correct one without rewriting the others.

---

## The vault

```
00-Indexes/       17   Master Index, topic indexes, the taxonomy register
01-Resources/    128   one note per source — the substance
02-Glossary/     113   terms, defined once and linked
03-Patterns/      47   recurring solution shapes, independent of any source
04-Reviews/        3   longer reads of a single source
06-Papers/         2   academic sources, with the PDFs
08-Workflows/      5   how the intake and consult modes actually run
09-Applications/   6   what was used, when, and what it was worth
internal docs/    26   design specification, assessments, service map
.Data/                 surveys (evidence), seeds, derived databases
.utility/              the librarian tool and the scouting pipeline
```

`internal docs/` is where the reasoning lives. If you want to know why
something is the way it is, [Design Specification](internal%20docs/Design%20Specification.md)
states the rules and [Service Map](internal%20docs/Service%20Map.md) records
what has actually been run, defect by defect.

---

## The tool

```bash
cd .utility && python -m librarian web
```

Three surfaces, one engine. The CLI, the MCP server and the web page all call
the same `consult.find_donor`, so they cannot disagree about what the catalogue
contains — which matters more than it sounds, because the moment a front end
starts scoring things itself, nobody can tell which surface is right.

| Surface | Command | For |
| --- | --- | --- |
| Terminal | `python -m librarian query donor "..."` | Asking directly |
| Browser | `python -m librarian web` | Narrowing by axis, catalogue-style |
| Model | `python -m librarian serve` | An agent, over MCP (stdio or loopback HTTP) |

The web page is a product catalogue rather than a search box: the objects are
strongly typed across ten closed axes, so the drop-downs are built from the
result set and a count is the size of what survives choosing it. It binds
`127.0.0.1` and refuses anything else.

### The rest of the commands

```
status      what the index holds and what is reachable
index       rebuild the derived store from the vault
integrity   run the vault assertions
coverage    does the catalogue actually cover this question?
components  filter sources by what they are made of, at the file level
freshness   re-check recorded facts against upstream; reports, never edits
duplicates  candidate near-duplicates; reports, never merges
provenance  check the catalogue's own structural claims against the surveys
relevance   compare ranking configurations side by side on one index
eval        run the retrieval evaluation set
scenario    the domain search test — real problems, described in their terms
workbench   open a source in a sandbox, engage with it, document, close
used        record what an answer was worth
brief       research requests: what a project needs, and what was ruled out
queue       sources in use that are not catalogued yet
populate    run the unattended local-model scout (LM Studio)
staging     the airlock: proposals awaiting a human sentence before they land
```

Agents in other repositories reach the catalogue over MCP at one of three
tiers. `consult` reads and appends application records; `contribute` adds
briefs and staged proposals and **cannot alter a note**; `curate` adds
promotion into the vault. See
[Workflow - Contribution By Outside Agents](08-Workflows/Workflow%20-%20Contribution%20By%20Outside%20Agents.md).

---

## Getting it running

Python 3.11+. `librarian` itself is standard library except for PyYAML, which
parses note frontmatter, and numpy, which does the cosine arithmetic — both
degrade rather than fail if absent. pydantic is used by the scouting pipeline.

```bash
pip install -r .utility/requirements.txt   # PyYAML, numpy, pydantic
cd .utility
python -m librarian index                  # build the derived store
python -m librarian components build       # build the component store from surveys/
python -m librarian integrity              # confirm the vault holds together
```

A clone contains no databases — they are derived and rebuild in under a second.
Semantic search additionally needs an embedding model served by
[LM Studio](https://lmstudio.ai) at `http://127.0.0.1:1234/v1`; without one,
retrieval falls back to lexical and says so rather than quietly getting worse.

`CATALOGUE_VAULT` points the tool at a different vault, which is how the test
suite and any second copy work.

---

## What is truth and what is disposable

`MARKDOWN_IS_TRUTH`. The notes are authoritative; everything derived from them
is rebuildable and is not committed.

- **`01-Resources/` and the rest of the vault** — the truth. Edited by hand.
- **`.Data/surveys/`** — evidence. What a blobless shallow clone returned on a
  known date, never edited. Structural claims in the notes are checked against
  these, and normalising one in place would destroy the thing that makes it
  evidence.
- **`.Data/Databases/`** — disposable. Delete them, rebuild them. Not tracked.

A conflict between a database and its source resolves to the source, always.

---

## The rules it holds itself to

These are enforced in code, not by convention. The full list is in the design
specification; these are the ones that shape everything else.

| | |
| --- | --- |
| `LOCATE_DO_NOT_ADJUDICATE` | The catalogue identifies and describes; the user decides what to do with a source. Age, popularity and licence are facts to report, not grounds to withhold. |
| `POSTURE_DECIDES_CONSEQUENCE` | A licence is recorded as read, always. What it *costs* depends on whether the work is distributed — one config key, two behaviours, identical recorded facts. |
| `EVIDENCE_REQUIRED` | No factual field without a fetched source. "Unknown" is a valid value; a plausible guess is not. |
| `FAILURE_MUST_BE_LOUD` | An operation that can fail must be unable to fail silently. A check ships with a demonstration that it fires; a corpus-relative threshold ships with the function that re-derives it. |
| `RUN_BEFORE_CLAIM` | A service is not listed as working until it has produced a row, an answer, or a recorded refusal. |
| `NO_SCHEMA_DRIFT` | Taxonomy axes and domain keys change only by editing their authoritative Markdown. No process adds a field. |
| `EXECUTION_SANDBOX_ONLY` | Fetched code runs only inside a workbench, only when a person opened it, never during an unattended sweep. |
| `DOCUMENT_BEFORE_DESTROY` | A workbench cannot be closed until its application record exists. |

The fourth one was written after reviewing thirty-five implementation defects.
The ones that survived days rather than minutes were, without exception, the
ones that produced no signal.

---

## Where it currently stands

347 notes indexed, 130 catalogued sources with full taxonomy, 3,259 links.
Integrity: 0 errors, 13 warnings across 23 checks. Retrieval evaluation MRR
0.95, hit@5 1.00 over 20 queries; the harder scenario test — real problems
described in the asker's own words rather than the catalogue's — reaches
useful@5 0.83 and strong@5 0.80 across all 30.

**Two things to know before extending it.**

Several ranking constants are cut from the current corpus and will drift as it
grows. `SELECTIVITY_CEILING` is the clearest case: a term appearing in more
than half the answerable notes cannot discriminate, and which terms those are
changes with every intake. `python -m librarian relevance` re-measures the
configurations side by side on one index, and the distribution functions
re-derive the thresholds. Both should be run after any large addition.

The scenario and evaluation instruments both read the vault, and the vault
contains this system's own design documents. Editing an internal note moves the
scores with no ranking change at all. Numbers are only comparable within a
single run.

---

## Status

Private, and for personal use. The **data** — catalogued sources, application
records, what was used and when — is specific to one person's work and is not
intended to be published. The **system** may be separated out later so that
others can build an internal library the same way; nothing in the tool depends
on the contents of this particular vault, and `CATALOGUE_VAULT` already points
it anywhere.

Next: extend the library substantially, then revisit the ranking and the
taxonomy against a wider range of source material, and integrate the local
model workflows for the data-to-information stage.
