"""The unattended library agent: search, fetch, survey, classify, stage.

## What this is

The thing that runs overnight on a local model and fills staging. It never
touches the vault — everything it produces goes through `propose`, which means
everything it produces is subject to the same four refusals as any other agent's
work, and none of it reaches a reader without a person writing the Bottom Line.

## The sequence, and why it is in this order

```
  queries      one model call     turn a need into search terms
  search       GitHub             candidates, cheapest first
  already?     local              skip anything catalogued, with the note named
  fetch        GitHub             metadata and README
  screen       one model call     does anything here contradict the brief?   <- cheap, first
  survey       git ls-tree        the file listing, blobless
  axes         ten model calls    one enumeration each
  topic        one model call     which existing heading
  describe     three model calls  inside / mechanics / uses
  propose      local              stage it, with the evidence attached
```

The screen is third from the top because it is one small call and it removes
most candidates. Doing the fourteen calls first and screening after would work
and would waste an order of magnitude more time — which matters when the budget
is a night rather than a token bill.

## Failure is per candidate, never per run

A model refusal, a rate limit, a repository that will not clone: each is
recorded against that candidate and the run continues. An unattended job that
stops on the first awkward repository is an unattended job nobody runs twice.
The counts at the end distinguish *screened out* from *refused* from *errored*,
because those are three different problems with three different fixes.
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from . import brief as brief_mod
from . import content_model, derive, enrich, policy
from . import propose as propose_mod
from . import scouttasks
from .localmodel import LocalModel, ModelRefused, ModelUnavailable, RunLog
from .config import vault_root

# Ranked before anything is fetched. Everything else costs network.
MAX_CANDIDATES_PER_QUERY = 10


@dataclass
class Fetchers:
    """The network side, injected so the whole runner is testable offline.

    Same pattern the scout tests already use: no test may require GitHub, a
    clone, or a running LM Studio.
    """

    search: Callable[[str], list[dict[str, Any]]]
    repo: Callable[[str], dict[str, Any]]
    readme: Callable[[str], str]
    survey: Callable[[str], dict[str, Any]]
    # The LICENSE file itself. GitHub reports no usable licence for a great
    # many repositories that plainly have one, and `license_class` is what
    # `find_donor` eliminates on - an empty one removes the source from every
    # constrained answer.
    licence: Callable[[str], str] = lambda key: ""

    @classmethod
    def live(cls) -> "Fetchers":
        """Wire to the scouting pipeline, which already handles tokens, rate
        limits and the blobless clone. Imported lazily: `librarian` ships
        without `scout` and must not fail to import when it is absent."""
        from scout import discovery, survey as survey_mod
        from scout.config import ScoutConfig

        from .webfetch import Fetcher as WebFetcher

        cfg = ScoutConfig()
        web = WebFetcher()

        def readme(repo_key: str) -> str:
            """`raw.githubusercontent.com` first, the API only if it fails.

            The API's readme endpoint costs one of sixty calls an hour; raw
            costs none. On an unauthenticated budget that is the difference
            between charting twenty-eight repositories in a window and
            charting fifty-six.
            """
            page = web.readme(repo_key)
            if page.ok:
                return page.text
            return discovery.fetch_readme(repo_key, cfg)

        def licence(repo_key: str) -> str:
            """Also from raw, and also free of the API budget."""
            for name in ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING",
                         "LICENCE", "LICENSE-MIT"):
                page = web.get(f"https://raw.githubusercontent.com/"
                               f"{repo_key}/HEAD/{name}")
                if page.ok:
                    return page.text
            return ""

        return cls(
            search=lambda q: discovery.search_github(q, cfg,
                                                     per_page=MAX_CANDIDATES_PER_QUERY),
            repo=lambda k: discovery.fetch_repo(k, cfg),
            readme=readme,
            survey=lambda k: survey_mod.survey_one(k, cfg),
            licence=licence,
        )


def topics(vault: Path | None = None) -> list[str]:
    """The subject headings that already exist. A new one is a human decision
    (`NO_SCHEMA_DRIFT`), so the model picks from what is there."""
    root = Path(vault) if vault else vault_root()
    found = sorted(p.stem[len("Topic - "):]
                   for p in (root / "00-Indexes").glob("Topic - *.md"))
    return found


# ------------------------------------------------------------- one candidate

def chart_one(repo_key: str, model: LocalModel, fetchers: Fetchers, *,
              brief: brief_mod.Brief | None = None,
              proposed_by: str = "library-agent",
              vault: Path | None = None,
              log: RunLog | None = None) -> dict[str, Any]:
    """Take one repository from a name to a staged proposal.

    Returns a verdict dict rather than raising, because the caller is a loop
    over candidates and one awkward repository must not end the run.
    """
    log = log or RunLog()
    root = Path(vault) if vault else vault_root()

    existing = propose_mod.already_catalogued(repo_key, root)
    if existing:
        return {"repo_key": repo_key, "outcome": "already_catalogued",
                "note": existing,
                "reason": f"already catalogued as {existing}"}

    try:
        meta = fetchers.repo(repo_key)
        readme = fetchers.readme(repo_key)
    except Exception as exc:                                # noqa: BLE001
        log.errors += 1
        return {"repo_key": repo_key, "outcome": "error",
                "reason": f"could not fetch: {exc}"}

    # The screen first: one small call that removes most candidates.
    if brief is not None:
        try:
            verdict = model.run(
                scouttasks.SCREEN, readme or meta.get("description", ""),
                question=scouttasks.screen_question(
                    brief.need, list(brief.disqualifiers)))
        except ModelRefused as exc:
            log.refused += 1
            return {"repo_key": repo_key, "outcome": "refused",
                    "reason": str(exc)}
        if verdict.get("verdict") == "reject":
            log.screened_out += 1
            contradicts = "; ".join(verdict.get("contradicts") or [])
            return {"repo_key": repo_key, "outcome": "screened_out",
                    "reason": (verdict.get("reason", "") +
                               (f" [{contradicts}]" if contradicts else ""))}

    try:
        survey = fetchers.survey(repo_key)
    except Exception as exc:                                # noqa: BLE001
        # A repository that will not clone is still worth charting from its
        # README; the note simply carries less evidence and says so.
        survey = {}
        log.say(f"{repo_key}: no file listing ({exc})")

    shape = scouttasks.survey_chunk(survey)
    evidence_text = _evidence_text(meta, readme, shape)

    # Read what can be read before asking anything. A model asked for a
    # licence with the SPDX identifier in front of it answered `Unknown`; a
    # model asked for the ecosystem with `main language: TypeScript` in front
    # of it answered `Python`. Asking is strictly worse than reading.
    try:
        licence_text = fetchers.licence(repo_key)
    except Exception:                                       # noqa: BLE001
        licence_text = ""
    known = derive.derive_axes(meta, survey, evidence_text,
                               licence_text=licence_text,
                               paths=survey.get("paths") or (),
                               repo_key=repo_key,
                               permitted=content_model.load(root).axis_values)
    try:
        axes = {**known,
                **classify_axes(evidence_text, model, vault=root,
                                skip=set(known) | set(derive.PATH_DEFINED))}
        topic = pick_topic(evidence_text, model, vault=root)
        sections = describe(readme, shape, model, evidence=evidence_text)
    except ModelRefused as exc:
        log.refused += 1
        return {"repo_key": repo_key, "outcome": "refused", "reason": str(exc)}
    except ModelUnavailable as exc:
        raise                                                # ends the run, correctly

    evidence = {
        "survey": survey.get("survey_file") or survey.get("source") or "",
        "file_count": survey.get("file_count") or survey.get("files") or 0,
        "fetched_at": meta.get("fetched_at") or meta.get("pushed_at") or "",
        "source": "github api + blobless clone" if survey else "github api",
        "charted_by": proposed_by,
    }
    if not evidence["survey"] and not evidence["file_count"]:
        evidence["source"] = "github api"
        evidence.setdefault("fetched_at", "")

    metadata = _metadata(meta, topic)
    try:
        proposal = propose_mod.propose(
            repo_key, meta.get("html_url") or f"https://github.com/{repo_key}",
            axes, evidence, brief_id=brief.brief_id if brief else "",
            proposed_by=proposed_by, metadata=metadata, sections=sections,
            vault=root)
    except (policy.PolicyError, ValueError) as exc:
        return {"repo_key": repo_key, "outcome": "rejected", "reason": str(exc)}

    log.proposed += 1
    ready = propose_mod.readiness(proposal, root)
    return {"repo_key": repo_key, "outcome": "proposed",
            "proposal_id": proposal.proposal_id, **ready}


def _evidence_text(meta: dict[str, Any], readme: str, shape: str) -> str:
    """One chunk per call, but the axis calls all want the same mixed view:
    what it says about itself, plus what it is actually made of."""
    parts = []
    if meta.get("description"):
        parts.append(f"description: {meta['description']}")
    if meta.get("language"):
        parts.append(f"main language: {meta['language']}")
    if meta.get("license_spdx") or meta.get("spdx"):
        parts.append(f"declared licence: {meta.get('license_spdx') or meta.get('spdx')}")
    if meta.get("archived"):
        parts.append("the repository is archived")
    if meta.get("pushed_at"):
        parts.append(f"last pushed: {meta['pushed_at']}")
    if shape:
        parts.append("\nrepository contents:\n" + shape)
    if readme:
        parts.append("\ndocumentation:\n" + readme)
    return "\n".join(parts)


def _metadata(meta: dict[str, Any], topic: str) -> dict[str, Any]:
    out: dict[str, Any] = {"primary_topic": topic}
    mapping = {
        "github_description": "description", "github_language": "language",
        "github_default_branch": "default_branch", "github_homepage": "homepage",
        "github_topics": "topics",
    }
    for target, source in mapping.items():
        if meta.get(source) not in (None, "", []):
            out[target] = meta[source]
    if meta.get("stars") is not None or meta.get("stargazers_count") is not None:
        out["github_stars"] = meta.get("stars", meta.get("stargazers_count"))
    if meta.get("pushed_at"):
        out["github_pushed_at"] = meta["pushed_at"]
    spdx = meta.get("license_spdx") or meta.get("spdx")
    if spdx:
        out["github_license_spdx"] = spdx
        out["license"] = spdx
    out.setdefault("license", "Unknown")
    out.setdefault("type", "infrastructure_tool")
    return out


# --------------------------------------------------------------- the tasks

def classify_axes(evidence: str, model: LocalModel,
                  vault: Path | None = None,
                  skip: set[str] | None = None) -> dict[str, str]:
    """One call per axis, for the axes no metadata field can answer.

    A model asked for ten enumerations in one object drifts: it repeats a value
    across axes, or picks the first plausible one and stops reading. Asked
    *which of these four words describes how mature this is*, with the four
    words in front of it, it is dependable.

    **An unconfident answer is dropped rather than recorded.** The schema asks
    for `confident` precisely so it can be honoured; taking the value anyway
    would make the flag decoration. A missing axis is reported by `readiness`
    and filled by a person, which is what `EVIDENCE_REQUIRED` means when it
    says a plausible guess is not a value.
    """
    model_note = content_model.load(Path(vault) if vault else vault_root())
    if not model_note.axis_values:
        raise ModelRefused("the vault declares no axis enumerations to choose "
                           "from; classification would be unconstrained")

    skip = skip or set()
    out: dict[str, str] = {}
    for axis, permitted in model_note.axis_values.items():
        if axis in skip:
            continue
        answer = model.run(scouttasks.axis_profile(axis, list(permitted)),
                           evidence, question=scouttasks.axis_question(axis))
        value = answer.get("value", "")
        if value in permitted and answer.get("confident") is not False:
            out[axis] = value
    return out


def pick_topic(evidence: str, model: LocalModel,
               vault: Path | None = None) -> str:
    available = topics(vault)
    if not available:
        return ""
    answer = model.run(scouttasks.topic_profile(available), evidence,
                       question=scouttasks.TOPIC_QUESTION)
    return answer.get("topic", "")


def describe(readme: str, shape: str, model: LocalModel, *,
             evidence: str = "", dropped: list[str] | None = None
             ) -> dict[str, str]:
    """The three sections a machine is allowed to write.

    Not `Bottom Line` and not `What It Solves` — those are refused at the
    airlock. These three are lists of things the evidence contains, which is a
    different kind of claim from a sentence a reader acts on.

    Every bullet is checked against the text the model was given. The first
    live run produced *"Uses tree-sitter for parsing"* for a project whose
    documentation never mentions tree-sitter — an invented name, in a section a
    machine is allowed to write. Allowing that section requires checking it.
    """
    sections: dict[str, str] = {}
    dropped = dropped if dropped is not None else []
    if shape:
        bullets = model.run(scouttasks.INSIDE, shape,
                            question=scouttasks.INSIDE_QUESTION)
        # Grounded against the whole evidence, not only the chunk the model
        # saw. The shape chunk is a terse histogram - `src: 120`, `.ts: 250` -
        # so a correct bullet phrased in English ("TypeScript source under
        # src/") scored as ungrounded against it. Checking the superset still
        # catches an invented name, which is the shape these failures take.
        sections["What Is Inside"] = _render(bullets.get("bullets"),
                                             evidence or shape, dropped)
    if readme:
        source = evidence or readme
        mechanics = model.run(scouttasks.MECHANICS, readme,
                              question=scouttasks.MECHANICS_QUESTION)
        sections["Architecture & Mechanics"] = _render(
            mechanics.get("bullets"), source, dropped)
        uses = model.run(scouttasks.USES, readme,
                         question=scouttasks.USES_QUESTION)
        rendered = _render(uses.get("bullets"), source, dropped)
        if rendered:
            sections["Integration & Use Cases"] = rendered
    return {k: v for k, v in sections.items() if v}


def _render(bullets: Any, source: str = "", dropped: list[str] | None = None
            ) -> str:
    if not isinstance(bullets, list):
        return ""
    cleaned = [str(b).strip().lstrip("-").strip() for b in bullets
               if str(b).strip()]
    if source:
        cleaned, ungrounded = derive.grounded(cleaned, source)
        if dropped is not None:
            dropped.extend(ungrounded)
    return "\n".join(f"- {b}" for b in cleaned)


def search_queries(need: str, model: LocalModel) -> list[str]:
    """Let the model translate a need into the field's own vocabulary.

    The gap this closes is the one the whole catalogue is measured on: a person
    describes a problem in their words and the ecosystem names it in its own.
    Degrades to the need itself, which is a poor query and better than none.
    """
    try:
        answer = model.run(scouttasks.QUERIES, need,
                           question=scouttasks.QUERIES_QUESTION)
    except (ModelRefused, ModelUnavailable):
        return [need]
    queries = [str(q).strip() for q in answer.get("queries", []) if str(q).strip()]
    return queries or [need]


# ----------------------------------------------------------------- the runs

def run_brief(brief_id: str, *, model: LocalModel, fetchers: Fetchers,
              limit: int = 8, agent: str = "library-agent",
              vault: Path | None = None) -> RunLog:
    """Work one brief: search, screen, chart, and dispose of everything seen.

    Every candidate ends with a disposition on the brief, including the ones
    that were rejected — so when a person comes to close it, the negative
    results are already written and the reason is the model's own words about
    what the text contradicted.
    """
    log = RunLog()
    record = brief_mod.claim(brief_id, agent)

    seen: set[str] = set()
    for query in search_queries(record.need, model):
        try:
            results = fetchers.search(query)
        except Exception as exc:                            # noqa: BLE001
            log.errors += 1
            log.say(f"search '{query}' failed: {exc}")
            continue
        for item in results:
            key = item.get("repo_key") or item.get("full_name") or ""
            if not key or key in seen:
                continue
            seen.add(key)
            if log.proposed >= limit:
                break
            log.considered += 1
            outcome = chart_one(key, model, fetchers, brief=record,
                                proposed_by=agent, vault=vault, log=log)
            _dispose(brief_id, key, outcome, log)
        if log.proposed >= limit:
            break
    return log


def _dispose(brief_id: str, repo_key: str, outcome: dict[str, Any],
             log: RunLog) -> None:
    """Every candidate seen gets a disposition, so closing is possible later."""
    kind = outcome.get("outcome")
    if kind == "proposed":
        return                                   # `propose` disposed of it
    reason = outcome.get("reason", "") or kind or "no reason recorded"
    try:
        brief_mod.add_candidate(brief_id, repo_key, found_by="library-agent")
        brief_mod.decide(brief_id, repo_key, brief_mod.REJECTED, reason=reason)
    except (policy.PolicyError, ValueError) as exc:         # pragma: no cover
        log.say(f"{repo_key}: could not record disposition ({exc})")


def run_queue(*, model: LocalModel, fetchers: Fetchers, limit: int = 10,
              agent: str = "library-agent",
              vault: Path | None = None,
              progress: Callable[[str], None] | None = None) -> RunLog:
    """Drain the enrichment queue: sources someone already used.

    No screen here — nobody is asking whether these fit a brief. They are
    already in use, which is the strongest signal the catalogue ever gets, and
    the only question is what they are.
    """
    log = RunLog()
    say = progress or (lambda line: None)
    # Queued entries plus claims nobody is holding any more. A run that was
    # killed does not have to be cleaned up before the next one starts.
    pending = enrich.workable()[:limit]
    say(f"{len(pending)} queued entr{'y' if len(pending) == 1 else 'ies'} to chart")
    for index, entry in enumerate(pending, 1):
        log.considered += 1
        say(f"[{index}/{len(pending)}] {entry.repo_key} ...")
        started = time.monotonic()
        enrich.claim(entry.entry_id, agent)
        outcome = chart_one(entry.repo_key, model, fetchers,
                            proposed_by=agent, vault=vault, log=log)
        say(f"[{index}/{len(pending)}] {entry.repo_key} -> "
            f"{outcome.get('outcome')} ({time.monotonic() - started:.0f}s)")
        # Execution state and business state in one place: the queue entry
        # itself records what happened, so a run killed after this point loses
        # nothing but its in-memory counters.
        kind = outcome.get("outcome")
        if kind == "proposed":
            enrich.resolve(entry.entry_id, enrich.PROPOSED,
                           proposal_id=outcome["proposal_id"])
        elif kind == "already_catalogued":
            enrich.resolve(entry.entry_id, enrich.CATALOGUED,
                           note=outcome.get("note", ""))
        else:
            enrich.resolve(entry.entry_id, enrich.SKIPPED,
                           resolution=outcome.get("reason", kind or "unknown"))
        log.say(f"{entry.repo_key}: {kind} - {outcome.get('reason', '')}".strip(" -"))
    return log
