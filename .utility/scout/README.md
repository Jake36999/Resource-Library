# Scouting Pipeline

Continuous, resumable growth of the Resource Library. Design and rationale:
`00-Indexes/Schema Extension - Scouting Pipeline.md`.

## The shape of it

```
discover  ->  scout   ->  rank      ->  freeze   ->  dive       ->  publish
(no model)   (4B local)  (no model)    (no model)   (14B local    (no model)
                                                     or hosted)
```

Finding is cheap and deterministic. Judging is arithmetic, so it is
reproducible and explainable. Only reading is expensive, and it always
happens in descending order of expected value.

## Run it

```powershell
cd D:\Resource-Library
python -m scout status                 # where everything stands
python -m scout cycle                  # discover -> ... -> freeze a cohort
python -m scout dive                   # work the cohort, best first
python -m scout publish                # hand dossiers to the build script
python .utility\build_solutions_library.py
```

Run from `.utility` if `scout` is not on the path:
`python -m scout.cli status`.

## Why the stages are separate commands

`config/runtime.json` on this host sets `max_task_models_loaded: 1` against a
GTX 1080 and an RX 5500 XT. One task model is resident at a time, so the 4B
scout and the 14B reviewer must run as distinct passes. Interleaving them
would spend more wall-clock swapping models than doing work. `cycle`
deliberately stops before `dive` for exactly this reason.

## Interruption

Stop it whenever you like. State lives in SQLite, not memory:

- completed deep dives are `catalogued` with their dossier written;
- the item in flight keeps its lease until it expires, then is reclaimed;
- everything else stays `queued`.

The next `dive` resumes at the highest-ranked incomplete item. Nothing is
repeated and the most valuable sources are always finished first.

## Ranking

Six weighted signals, all from data already collected, all stored per item in
`scout_signal` so any position can be explained:

| Signal | Weight | Reads |
| --- | --- | --- |
| gap_fit | 30 | how thin the destination topic is |
| corroboration | 20 | independent rediscovery |
| vitality | 15 | last push, archived flag |
| reusability | 15 | licence class |
| adoption | 10 | log-scaled stars |
| depth | 10 | docs/, papers/, README size |

Weights live in `library_config.json` under `scout.weights`. Change them and
re-run `rank`; nothing else needs touching.

Two choices worth knowing about. Stars are log-scaled so a 200k-star
framework cannot bury a 500-star library that actually fits the gap. Licence
is a ranking input rather than metadata, because a catalogue about
integrating solutions should rank what you are allowed to integrate.

## Credentials

Environment only, never written to disk or config:

- `GITHUB_TOKEN` - raises the API limit from 60/hr to 5000/hr. Without it,
  `discover` and `enrich` will hit the ceiling quickly.
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` - only used when
  `scout.escalation_provider` is set and an item meets the escalation
  policy (a paper, top decile of its cohort, or low scout confidence).

## Tests

```powershell
python -m pytest .utility\scout\tests -q
```

46 tests covering the ranker's behaviour, queue and lease recovery, domain
parsing, and the full pipeline with the model and network faked.
