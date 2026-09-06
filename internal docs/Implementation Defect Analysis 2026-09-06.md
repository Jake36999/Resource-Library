---
type: "assessment"
status: "active"
created: "2026-09-06"
purpose: "every defect found while implementing stages 0-3b, what they share, and the one rule that would have caught most of them"
defects_reviewed: 35
---

# Implementation Defect Analysis

## Why This Is A Separate Analysis

[[Meta Analysis And Final Shape 2026-09-04]] read twenty-four *design*
documents and found five recurring shapes. This reads the *implementation* of
stages 0 to 3b — roughly thirty-five defects found in two days of building —
and asks the same question of a different body of evidence.

It reaches a different answer, and a sharper one.

## The Census

| Origin | Count | Examples |
| --- | --- | --- |
| Pre-existing, found by running something | 8 | `shallow_clone` broken on Windows since it was written; `application_count` zero for all 130; the first cohort's licences never captured |
| Introduced while building, caught by tests within minutes | ~20 | components bypassing `eligible` (9 tests failed at once); substring matching returning `sidekiq` for `side`; a duplicate floor above its own maximum |
| My claims outrunning verification | 4 | the assessment said six sources were "silently withheld" — none was; the plan said adopt FastMCP — it was already in use |
| Introduced by the editing method itself | 6 | a `str.replace` that matched nothing; another that matched the wrong occurrence; `\uv-data` read as a unicode escape; `\n` becoming a literal newline and leaving `cli.py` unparseable |

**More defects were introduced than found.** That is not alarming on its own —
detection latency was minutes and almost every one was caught by a test written
for a different purpose. What matters is the shape of the ones that were *not*
caught quickly.

## What They Share

Sorting by cause rather than by symptom, almost every defect has one property:

> **The failure produced no signal.**

- `str.replace` returns the input unchanged when nothing matches. No exception,
  no warning. Several "fixes" this session did not apply and were discovered
  only by reading output afterwards.
- A similarity floor of 0.18 against a corpus whose maximum is 0.144 reports
  *no duplicates found* — indistinguishable from a clean corpus.
- `license_class="permissive"` matched nothing and reported *130 candidates
  failed a constraint*: a true sentence about a false premise.
- A path frozen at import wrote the index to the wrong vault and raised nothing.
- `cli.py` was left syntactically broken while **292 tests passed**.
- `scout.config.DB_PATH` pointed at a deleted file for a day. Found by this
  analysis, not by use.

Contrast the loud ones. Components bypassing `eligible` failed **nine tests
simultaneously** and was fixed in four minutes. The difference is not severity —
that one was the worst correctness defect of the session — it is that something
was watching.

**So the overarching issue is not a category of bug. It is that this system, and
the process building it, both default to silence when something goes wrong.**

## Three Places The Silence Is Structural

Each is measurable, and each was measured for this note rather than asserted.

### 1. Declared invariants that nothing enforces

`THRESHOLD_CARRIES_ITS_DISTRIBUTION` was added on 2026-09-04. Today the
codebase has **eleven corpus-relative thresholds and four re-derivation
functions**:

| Has one | Does not |
| --- | --- |
| `COMPONENT_SELECTIVITY_CEILING`, `SEMANTIC_FLOOR`, `STRONG_ACCOUNT`/`THIN_ACCOUNT` (via `calibrate`), cosine variants (via `separation_probe`) | `SELECTIVITY_CEILING`, `NAME_MIN_QUERY_COVERAGE`, `NAME_MIN_NAME_COVERAGE`, `CORROBORATION_STRUCTURAL`, `CORROBORATION_DECLARED`, `CONTEXT_WEIGHT`, `EXCLUDED_WEIGHT` |

Seven of eleven violate an invariant this project wrote down for itself two days
ago — including `SELECTIVITY_CEILING`, the one whose staleness caused the
defect that motivated the invariant. **A rule with no check is a preference.**

### 2. Checks nobody has shown can fail

There are **21 integrity checks and 13 have a test that makes them fire**. The
other eight have only ever been observed passing, which is the same evidential
position as the duplicate floor above its own maximum: a green result that
cannot distinguish *nothing is wrong* from *this cannot detect anything*.

The two checks added this session were both demonstrated firing before being
trusted — `every_topic_is_routable` on a stripped Master Index,
`licence_class_disagrees` on a synthetic mismatch. That was done by instinct and
should be required.

### 3. Presentation that does not carry enforcement

Four separate defects were one thing wearing different clothes:

- components *were* filtered but did not show `license_class`, so a cold agent
  concluded the constraint had been bypassed;
- the duplicate score *said* semantic evidence mattered most and *ranked* by
  directory shape, because the components had incomparable ranges;
- `find_donor`'s schema omitted the enum its own validator enforced;
- a constraint removed the best answer and the response read exactly like a
  successful one.

In every case the system behaved correctly and **described itself wrongly**, and
in every case a caller acting on the description would be misled. Presentation
that diverges from enforcement is worse than no presentation, because it is
believed.

## What Actually Caught Things

Worth recording, because it argues for where to spend next:

| Mechanism | Defects caught | Latency |
| --- | --- | --- |
| Existing tests written for other reasons | ~14 | minutes |
| Reading output instead of trusting exit codes | ~8 | minutes |
| The cold agent test | 7 | one run |
| This analysis | 2 | two days |
| Nothing — found by chance later | ~4 | a day |

The cold agent test is the standout: seven defects from a single run, of which
**five were in surfaces that had tests passing**. Tests assert the behaviour
their author imagined; a stranger exercises the behaviour the author assumed was
obvious. They are not substitutes.

## The Rule

One invariant would have caught the majority, and it generalises across code,
checks and process:

> **`FAILURE_MUST_BE_LOUD`** — an operation that can fail must be unable to fail
> silently. A check ships with a demonstration that it fires. A threshold ships
> with the distribution it was derived from. A transformation that finds nothing
> to change raises rather than returning its input. A result carries the fields
> the constraints acted on.

Concretely, five things follow, in order of what they would have prevented:

1. **Every `str.replace` in a patch asserts its match.** Six defects this
   session came from an edit that silently did nothing or hit the wrong
   occurrence. This is a process rule and it costs one line.
2. **Every integrity check has a test that makes it fire.** Eight do not.
3. **Every corpus-relative threshold has a re-derivation function**, and an
   integrity check asserts the pairing rather than the docstring claiming it.
   Seven do not.
4. **Every result carries the fields its constraints filtered on.** Done for
   components; not audited elsewhere.
5. **A cold agent test is part of finishing a surface**, not a nicety. Seven
   defects for one run is the best yield of any mechanism used here.

## What This Does Not Say

It does not say the defect rate is too high. Twenty introduced defects in two
days of building, nearly all caught within minutes, is a working system — the
tests are doing their job and the corrections are cheap. The problem is
entirely in the tail: the small number that were silent survived days, and two
of them (`shallow_clone`, `application_count`) survived the entire life of the
project.

It also does not say the process should slow down. Three of the four
verification failures were corrected within the same session by running the
thing rather than describing it, which is the habit that matters and is already
in place.

## Related
- [[Meta Analysis And Final Shape 2026-09-04]] — the same question asked of the design documents
- [[Design Specification]] — where `FAILURE_MUST_BE_LOUD` belongs
- [[Service Map]] — the per-stage record these defects came from
- [[System Assessment 2026-09-04]] — the "built and never run" census
- [[Master Index]]
