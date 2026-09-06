# Solutions Library Utility Workspace

This hidden directory holds the operational layer for the solutions library vault.

## What lives here
- `librarian/`: the consult surface, derived index, integrity checks, toolchain
  adapter and workbench. Start with `librarian/README.md`.
- `scout/`: the intake pipeline - discover, scout, rank, freeze, dive, publish.
- `build_solutions_library.py`: bootstrap and regeneration script.
- `library_config.json`: folder layout and external source configuration.
- `prompts/`: Scout, Chart, Catalog, Entity Extraction, and Glossary prompts.
- `adapters/`: read-only wrappers for the external systems named in the plan.
- `logs/`: run logs, token budgets, and validation output.
- `staging/`: temporary input material before publication.
- `review_queue/`: quarantine for security-adjacent or uncertain resources.

## How to run
From the vault root:

```powershell
python .utility\build_solutions_library.py
```

The bootstrap process will:
- create the SQLite catalog in `.utility/`
- generate the Master Index, topic sub-indexes, glossary notes, and pattern notes
- generate the visible resource notes from `repositories to chart.md`
- emit Canvas maps for the root topology and topic views

The script is idempotent. Re-running it updates generated files from the same source of truth.

## Consulting the catalogue

```powershell
python -m librarian index                      # vault -> derived store
python -m librarian query donor "what I need"  # ask it something
python -m librarian integrity                  # assert the vault is sound
```

`librarian/README.md` covers the rest. The index is disposable: delete
`catalogue_index.sqlite` and rebuild it, because Markdown is truth.
