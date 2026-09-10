---
type: "workflow"
status: "active"
created: "2026-09-09"
mode: "C"
applies_to: "an agent working inside a project repository, not inside this vault"
---

# Agent Instructions - Using The Library

The block below is meant to be pasted into a project's `CLAUDE.md` or agent
config. Everything after it is the reasoning, for a person deciding whether to.

---

## The Drop-In Block

```markdown
## The Resource Library

A catalogue of open-source software somebody has actually read, with evidence.
It is reachable over MCP (`librarian serve --tier consult`).

### Before you reach for anything external

Call `find_donor` with what you need in your own words. If the catalogue holds
something, you get a note with what it does, what it is made of at the file
level, and — sometimes — a record of a time it was used and what that was
worth. Read that before you read a README.

If nothing matches, the reply says so plainly ("nothing here covers this").
That is a real answer. Do not treat a weak match as an endorsement.

### Whenever you use a source, log it. Always.

    log_use(repo_key_or_url, project, why)

One call, a URL is fine, no ceremony, and you owe nothing further. Three
possible answers:

- **catalogued** — it is already here, and the reply names the note. Go read it.
- **queued** — new. It joins the enrichment queue; a library agent will fetch,
  survey and chart it. Nothing is claimed about it until then.
- **seen_again** — someone else already logged it. The sighting count went up,
  which is how the queue gets ordered.

Log it even if you only skimmed it. Log it even if you rejected it — say so in
`why`. The queue is cheap; rediscovering the same source next quarter is not.

### When you need something the catalogue does not have

    open_brief(project, need, disqualifiers, constraints)

**`disqualifiers` is required and it is the part that matters.** State what a
candidate must not assume, require or depend on. Not the topic — the
constraint that would make an otherwise-perfect match useless to you.

    need:          "a sensing model that consumes raw Intel 5300 CSI"
    disqualifiers: ["must not assume ESP32 CSI shape",
                    "must not require preprocessed amplitude-only input"]
    constraints:   {"license_class": ["Permissive", "Weak_Copyleft"],
                    "deployment_target": ["Local_Only"]}

Opening a brief immediately tells you whether the catalogue already covers it,
so the cheapest possible outcome comes back first. Then get on with your work.
A library agent picks the brief up separately; do not wait on it.

### When something you took actually worked

    record_application(project, stage, outcome, what_was_needed,
                       what_was_found_and_taken, what_it_replaced,
                       what_the_catalogue_should_learn)

`what_the_catalogue_should_learn` is what turns a diary entry into a
requirement. Any source you name that is not catalogued is queued
automatically — you do not need to log it separately.

### What you may not do

You cannot write a note. That is deliberate: a resource note carries a
sentence a reader acts on, and it is written by whoever stands behind it after
reading the source. Propose through the queue and it gets charted properly.
```

---

## Why The Disqualifier Field Is Mandatory

This is the whole design, and it comes from a specific loss.

`network_management` needed a CSI sensing model. RuView was found, was
reasonable, was researched, and was charted accurately. It still cost a leg of
the project — because its sense model assumes ESP32 input shape and the
hardware is an Intel 5300.

No taxonomy anticipates that. No amount of describing RuView better would have
caught it. The disqualifying fact was a fact **about the asker**, and the only
place it can enter the system is the request.

So `open_brief` refuses a brief without one, naming `BRIEF_REQUIRED`:

> a brief must state at least one disqualifier — what a candidate must not
> assume, require or depend on. Without it this is a topic list, and a topic
> list cannot rule anything out.

A good disqualifier is falsifiable against a README. Compare:

| Weak | Strong |
| --- | --- |
| must be good quality | must not require a hosted control plane |
| should be modern | must not have its last release before 2023 |
| must be easy to use | must not assume ESP32 CSI shape |
| must be fast | must not require a GPU |

The screening model is asked what the documentation **contradicts**, not
whether the project is suitable — asked for suitability a small model agrees;
asked for a contradiction it has to point at a sentence.

## Why Logging Use Is The Highest-Value Call On The Surface

The catalogue's weakest layer is not its resources, it is its **applications**:
what was used, what it replaced, what it was worth. That layer cannot be
scraped, cannot be generated, and does not fill by charting more repositories.
It fills only when someone doing real work says so.

`log_use` is designed to cost nothing so that it actually happens: one call, a
URL is acceptable, duplicates are free, and it claims nothing. The `why` you
give is stored as *reported by you* and never as a fact about the project — but
it is the only part of the eventual note that will come from real use rather
than from a README, and it is the most valuable sentence in it.

## What Happens To What You Log

```
log_use  ──►  queue  ──►  librarian populate queue  ──►  staging  ──►  promote  ──►  note
              .Data/      local model, unattended       .Data/       a person
```

The middle step is a local model on LM Studio doing four kinds of small job —
reading a file listing, choosing from a closed enumeration, summarising
documentation, screening against constraints. It is deliberately not trusted
with the interpretation: `Bottom Line` and `What It Solves` are **refused**
from any machine and written at promotion by whoever stands behind the note.

The design rule is `INTERPRETATION_IS_NOT_MACHINE_WORK`, and it exists because
a small model fills enumerations well and writes plausible mush, and mush
passes every structural check there is.

## What The Catalogue Owes You In Return

- **A straight answer about coverage.** "Nothing here covers this" is returned
  as plainly as a match, and constraints that removed the best answer are
  reported rather than hidden.
- **Evidence, not vibes.** Every factual field on a note came from a fetched
  source. `Unknown` is a valid value; a plausible guess is not.
- **No adjudication.** The catalogue tells you what a thing is and what its
  licence says. It does not decide what you are allowed to do with it
  (`LOCATE_DO_NOT_ADJUDICATE`).

## Related
- [[Workflow - Contribution By Outside Agents]] — the full protocol, both sides
- [[Design Specification]] — the policy codes named in every refusal
- [[Workflow Index]] — the other workflows
- [[Master Index]]
