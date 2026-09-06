# .Data — the storage layer

Not user-facing. This folder is dot-prefixed so Obsidian does not show it, and
nothing here is written for a person to read as prose. It holds what was
*fetched* and what is *derived from it*, kept apart from the notes that
interpret it.

If you are an agent or a model arriving without context, the entry point is not
this file. It is:

```
python -m librarian components vocab
```

which answers *what can I filter on here* without needing this document, the
schema, or a guess.

## What is in here

```
.Data/
  Databases/
    catalogue_index.sqlite      derived from the vault; delete it, rebuild it
    source_components.sqlite    derived from surveys/; delete it, rebuild it
    solutions_library.sqlite    the scouting pipeline's own store
  surveys/
    2026-09-03-cohort.json      64 repositories, as fetched
    2026-09-04-cohort.json      49 repositories, as fetched
    2026-09-04-agent-surface.json
    2026-09-04-licences.json
  seeds/
    repositories to chart.md    the work queue the cohorts came from
```

**`surveys/` is the durable artefact and is never edited.** Each file is what a
`git ls-tree -r HEAD` returned against a blobless shallow clone on a known
date, plus the GitHub metadata fetched alongside it. Normalising one in place
would destroy the thing that makes it evidence. The two cohorts are in
genuinely different formats and that difference is absorbed on read, in
`librarian/components.py::_signal_rows`, not on disk.

**Everything in `Databases/` is disposable.** All three are rebuildable:

```
python -m librarian index               # catalogue_index.sqlite, from the vault
python -m librarian components build    # source_components.sqlite, from surveys/
```

`MARKDOWN_IS_TRUTH` applies to the first and `surveys/` is truth for the
second. A conflict between a database and its source resolves to the source,
always.

## The component store, field by field

One row per component fact. No row draws a conclusion.

| Table | Grain | Columns |
| --- | --- | --- |
| `source` | one repository | `repo_key`, `note`, `cohort`, `file_count`, `language`, `spdx`, `stars`, `archived`, `pushed_at` |
| `directory` | one directory in one repository | `repo_key`, `parent`, `name`, `files`, `depth` (1 = top level, 2 = below it) |
| `extension` | one file extension in one repository | `repo_key`, `extension`, `files` |
| `signal` | one material kind in one repository | `repo_key`, `signal`, `files` |
| `signal_path` | up to ten example paths per signal | `repo_key`, `signal`, `path` |
| `root_file` | one file at the repository root | `repo_key`, `name` |
| `meta` | schema version, which surveys were read | `key`, `value` |

`signal` is the interesting one. It classifies paths by the kind of material
they are — `tests`, `fixtures`, `grammars`, `schemas`, `benchmarks`,
`notebooks`, `docs`, `examples`, `data`, `diagrams`, `containers`, `iac`,
`agent_instructions` — by pattern-matching the path. It is coarse and it is
honest about being coarse: a match means the path looked like that kind of
thing, not that a person confirmed it.

**A caution about `files` on the `signal` table.** For the 2026-09-03 cohort the
survey stored a *truncated* path sample plus a companion count; taking the
sample's length would have recorded 10 tests for a repository with 847, for 64
of 113 sources. The count is read from the companion. `signal_path` is a
sample, never a complete list — do not count rows there and expect the total.

## What this layer is for

`components vocab` → `components signal <name>` → `components profile <repo>`
is a filtering path that touches no prose. It is meant to be the cheap first
step: narrow 113 sources structurally, *then* read the few notes that survive.

It answers questions the notes cannot, because the notes are written one source
at a time: *which sources ship a grammar*, *which carry more test material than
implementation*, *what does a repository with an MCP server usually also
contain*.

It cannot answer *which of these should I use*. That is a judgement, it needs
the prose, and it needs a person. See
`internal docs/Data Information Knowledge.md`.

## What is deliberately not here

- **No conclusions, rankings or scores.** Those are information and knowledge,
  and they live in `01-Resources/` where a person wrote them and signed for them.
- **No source code.** Paths are addresses, never contents. The catalogue
  identifies and locates; it does not extract.
- **No clones.** Every clone made during a survey was deleted once its tree was
  listed.
