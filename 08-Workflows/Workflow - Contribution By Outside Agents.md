---
type: "workflow"
status: "active"
created: "2026-09-09"
mode: "C+"
applies_to: "agents working from a project repository, and the library agent that serves them"
---

# Workflow - Contribution By Outside Agents

## What This Is For

Four projects — `Mark-XLVIII`, `quantule_mapper`, `knowledge_compiler_engine`,
`network_management` — are about to use this catalogue and add to it. Without a
protocol, "log what you find" means four agents writing markdown into
`01-Resources/` with nothing checking it until `librarian integrity` runs
afterwards. A thousand notes nobody can trust looks exactly like a thousand
notes, and the failure is silent.

So contribution is a request, a search, and an admission, with a different
actor responsible for each.

## The Two Agents

| | **project agent** | **library agent** |
| --- | --- | --- |
| Runs in | one of the four project repositories | this vault |
| Knows | what the project actually needs and why | the catalogue and the taxonomy |
| Tier | `consult` | `contribute` |
| Model | whatever the project uses | a local model is enough |
| Writes | application records | briefs, dispositions, staged proposals |
| Cannot | search on the project's behalf cheaply | judge whether a source suits a project it cannot see |

The split exists for two reasons. A project agent that goes and reads forty
repositories has forty repositories in its context and pays for all of them.
And filling ten closed enumerations from a survey is constrained choice, which
a local model does well enough to run for free — while deciding whether a
source suits a project is judgment, which it does not.

## The Sequence

```
project agent                library agent                 person / project agent
─────────────                ─────────────                 ──────────────────────
open_brief ────────────────► list_briefs
   │                         claim_brief
   │ (coverage answered           │
   │  immediately - the           │ search, fetch, survey
   │  need may already            │
   │  be catalogued)              ├─ propose_resource ──►  staging
   │                              ├─ decide_candidate
   │                              │    rejected + reason
   │                              └─ close_brief
   │                                   │
   ◄───────────────────────────────────┘
   read the brief, read staging
   promote_proposal (writes the Bottom Line) ────────────► 01-Resources/
   apply it
   record_application ─────────────────────────────────► 09-Applications/
```

## 1. The Brief — And Why It Cannot Be A Topic List

A project agent that asks for *"CSI sensing models"* will be handed RuView,
accurately charted and positively described, and will lose the same leg of the
same project twice. The fact that disqualified RuView was never about RuView:
its sense model assumes ESP32 input shape, and only something that knows the
project has an Intel 5300 knows to ask.

`open_brief` therefore **requires** at least one disqualifier and refuses
without one, naming `BRIEF_REQUIRED`.

```bash
librarian brief open \
  --project network_management \
  --need "a sensing model that consumes raw Intel 5300 CSI" \
  --rules-out "must not assume ESP32 CSI shape" \
  --rules-out "must not require preprocessed amplitude-only input" \
  --constraint "license_class=Permissive|Weak_Copyleft" \
  --constraint "deployment_target=Local_Only"
```

Three fields, three jobs:

- **`--need`** in the asker's own words. This is what retrieval matches on, and
  the catalogue is measured on queries phrased this way (the scenario test).
- **`--constraint`** closed-vocabulary axis values. These *eliminate*; a value
  outside its enumeration is refused rather than silently matching nothing.
- **`--rules-out`** the assumptions a candidate must not make. Free text,
  because this is the part no taxonomy can anticipate.

Opening a brief answers coverage immediately. If the catalogue already holds
the answer, the brief says so and nobody spends a model:

```
coverage    covered - the best answer accounts for 2 of 4 distinctive terms,
            and 4 sources agree
```

## 2. The Search — Data Only

The library agent claims the brief and works it. For each candidate it fetches
the repository, surveys the file listing, and stages what it found:

```python
propose_resource(
    repo_key="acme/csi-reader",
    canonical_url="https://github.com/acme/csi-reader",
    axes={...},                      # the ten closed enumerations
    evidence={"survey": "2026-09-09-csi.json", "file_count": 88,
              "fetched_at": "...", "source": "github api"},
    brief_id="network-management-2cfd43c0",
    sections={"What Is Inside": "...",
              "Architecture & Mechanics": "...",
              "Integration & Use Cases": "..."})
```

Four refusals, each by name:

| Refusal | When |
| --- | --- |
| `EVIDENCE_REQUIRED` | no survey and no fetched metadata — a field nobody fetched is a guess |
| `NO_SCHEMA_DRIFT` | an axis value outside its enumeration |
| `STAGING_BEFORE_VAULT` | the source is already catalogued; the reply names the note |
| `INTERPRETATION_IS_NOT_MACHINE_WORK` | the proposal carried a `Bottom Line` |

That last one is the important one. **A machine may not write the sentence a
reader acts on.** A small local model fills enumerations well and writes
plausible mush, and mush passes every structural check there is. Leave `Bottom
Line` and `What It Solves` empty; they are written at promotion.

Every proposal comes back with `ready` and `blocked_on`, so an agent learns
what is still missing while it still has the connection open:

```json
{"ready": false,
 "blocked_on": ["resource note is missing required frontmatter 'github_stars'",
                "resource note is missing required section '## Architecture & Mechanics'"]}
```

## 3. Closing — Where The Negative Results Come From

Every research session finds ten things and uses one. The nine are normally
lost, and next quarter somebody pays to rediscover that they do not work.

A brief will not close while any candidate is undecided, and a rejection
without a reason is refused (`DISPOSITION_REQUIRED`). So the by-product of
doing the work is exactly the record nobody otherwise writes:

```
+ acme/csi-reader: acme-csi-reader-380a5f
- ruview/ruview:   sense model assumes ESP32 CSI shape; will not take Intel
                   5300 subcarrier layout without a rewrite
~ someone/unlooked-at: ran out of session budget
```

This is [[Design Specification]]'s `DOCUMENT_BEFORE_DESTROY` one level up from
the workbench: the same rule that stops a sandbox being discarded before its
record exists, applied to a research session before its candidates are.

`--discard` exists for a session that runs out of budget. It is not silent —
each dropped candidate is recorded as `discarded` with a reason.

## 4. Promotion — The Only Write A Reader Sees

```bash
librarian staging list
librarian staging show <proposal_id>          # renders the note as it would be
librarian staging promote <proposal_id> \
  --bottom-line "Reads raw Intel 5300 CSI logs without assuming the ESP32
                 subcarrier layout, which is where RuView could not follow." \
  --what-it-solves "- Getting Intel 5300 CSI into a model without rewriting
                    its input stage." \
  --topic "Security & Detection"
```

Promotion runs the vault's own integrity checks against the note *before*
writing it — literally the same three functions `librarian integrity` calls,
on a one-note list, rather than a second copy of the rules that would drift.
A note the vault would reject is reported, not written:

```
rejected - the vault would not accept this note:
  - resource note is missing required section '## Architecture & Mechanics'
```

## 5. The Unattended Runner

```bash
librarian populate queue --limit 10     # chart what people reported using
librarian populate brief <brief_id>     # work one request
```

Fourteen small calls per candidate on a local model, each given one job and one
chunk and told nothing about the catalogue. Roughly 20 seconds per candidate.
It stages; it never writes a note.

Four axes are **not** put to the model at all — `license_class`,
`ecosystem`, `maturity_stage` and `hardware_footprint` are read from the
fetched metadata, because a model asked for a licence with the SPDX identifier
in front of it answered `Unknown`. An unconfident answer on the remaining six
is dropped rather than recorded, and every generated bullet is checked against
the evidence it was given.

See [[Agent Instructions - Using The Library]] for the block to paste into a
project.

## The Tiers

```bash
librarian serve --tier contribute     # the library agent
librarian serve --tier consult        # a project agent
librarian serve --tier curate         # a person, or a trusted reviewer
```

A tool outside the tier is **not registered at all** rather than registered and
refused — an agent should not see a capability it can never reach.

| Tier | Adds | Can reach |
| --- | --- | --- |
| `consult` | the ten read tools, `record_application` | `09-Applications/` |
| `contribute` | briefs, dispositions, staged proposals | the above, plus `.Data/` |
| `curate` | `promote_proposal` | the above, plus `01-Resources/` |

The old guarantee was *exactly one tool writes*. That stopped being true when
contribution was added, and the honest successor is not a longer write list but
a statement of what each write can reach: **seven tools write, two create a
note, and exactly one creates a note in `01-Resources/`.** A library agent
running at `contribute` holds none of them but the application append — the
reachable damage is a directory of JSON.

## What This Does Not Do

- **It does not fill the patterns layer.** Briefs and proposals produce
  resource notes and application records. A pattern is *derived* — the same
  shape noticed across several applications — and nothing here creates one.
  `librarian communities` can propose a cluster under `GRAPH_ADVISORY_ONLY`;
  a person writes the note. Revisit once [[Application Index]] has thirty-odd
  entries rather than six.
- **It does not judge whether a source is any good.** That is the project
  agent's job, and `librarian used` is how the answer gets back.
- **It does not run the local model.** The surface is ready for one; wiring
  LM Studio behind `propose_resource` is separate work.

## Related
- [[Design Specification]] — the policy codes each refusal names
- [[Note Content Model]] — the enumerations `propose_resource` validates against
- [[Workflow Index]] — the other workflows
- [[Master Index]]
