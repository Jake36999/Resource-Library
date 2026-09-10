"""The MCP surface: consult, plus the one permitted write.

An agent that reaches the catalogue through this server can ask all six
question kinds and can record an application. It has **no reachable tool that
mutates the catalogue** otherwise - no index rebuild, no intake, no workbench,
no shell. That is the point: a read surface with one narrow write is safe to
expose to a third party, and an agent platform is not.

FastMCP is an optional dependency, following the pattern in the ToolSet's own
`mcp_server.py`. The module stays importable without it so the tool functions
can be tested directly, which is also how the "no reachable mutation" property
is asserted rather than assumed.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from . import brief as brief_mod
from . import consult
from . import enrich as enrich_mod
from . import index as index_mod
from . import policy
from . import propose as propose_mod
from .config import CatalogueConfig, index_db_path, vault_root

SERVER_NAME = "resource-library"
SERVER_INSTRUCTIONS = """The Resource Library: a queryable reference for prior work.

It identifies and locates solutions; it does not extract them. Answers end at
"here is where to look and why". Opening a source is a person's decision.

Ask with the query kind that matches your question:
  orient          what is here, and where does this subject live
  find_donor      what could I take, given what I can actually run
  find_pattern    has this shape of problem been solved before
  find_technique  where would I look to see how this is done
  find_data       what data exists, and how do I reach it
  find_precedent  has this been used before, and what happened

Constraints in find_donor eliminate rather than re-rank: a GPU-only tool is
not a lower-ranked answer for a laptop, it is not an answer. Every result
carries a `why`. When you finish a piece of work that used something from
here, call record_application - an unrecorded use teaches the catalogue
nothing."""


def _response(response: consult.Response) -> dict[str, Any]:
    return response.to_dict()


# ------------------------------------------------------------------- tools

def tool_orient(topic_or_keywords: str, limit: int = 10) -> dict[str, Any]:
    """What is here, and where does this subject live?"""
    return _response(consult.orient(topic_or_keywords, limit))


def tool_find_donor(need: str, license_class: str = "", deployment_target: str = "",
                    hardware_footprint: str = "", ecosystem: str = "",
                    domain_primary: str = "", maturity_stage: str = "",
                    interface_protocol: str = "", data_locality: str = "",
                    security_compliance: str = "", agent_surface: str = "",
                    max_age_days: int = 0, limit: int = 10) -> dict[str, Any]:
    """What could I take, given what I can actually run.

    Every one of the ten taxonomy axes filters, and each **eliminates**: a
    GPU-only tool is not a lower-ranked answer for a laptop, it is not an
    answer. Values are case-sensitive; an unrecognised one is refused with the
    permitted list rather than silently matching nothing.

    The response carries `facets` - the values present among the candidates,
    with counts - and every axis listed there is accepted here. `advisories`
    says when a constraint removed a higher-scoring candidate, or when nothing
    in the catalogue really covers the question.
    """
    constraints = {k: v for k, v in {
        "license_class": license_class, "deployment_target": deployment_target,
        "hardware_footprint": hardware_footprint, "ecosystem": ecosystem,
        "domain_primary": domain_primary, "maturity_stage": maturity_stage,
        "interface_protocol": interface_protocol, "data_locality": data_locality,
        "security_compliance": security_compliance, "agent_surface": agent_surface,
        "max_age_days": max_age_days or None}.items() if v}
    try:
        return _response(consult.find_donor(need, constraints, limit))
    except ValueError as exc:
        return {"error": "invalid_params", "detail": str(exc),
                "axes": {a: list(v) for a, v in consult.axis_vocabulary().items()}}


def tool_find_pattern(problem: str, limit: int = 5) -> dict[str, Any]:
    """Has this shape of problem been solved before, and by what?"""
    return _response(consult.find_pattern(problem, limit))


def tool_find_technique(what: str, source: str = "", limit: int = 10) -> dict[str, Any]:
    """Where would I look to see how this is done?

    Returns candidate sources and the evidence that suggests them. It does not
    return the technique: that lives in the source, and reaching it means
    opening a workbench, which a person does.
    """
    return _response(consult.find_technique(what, source or None, limit))


def tool_find_data(subject: str, purpose: str = "", limit: int = 10) -> dict[str, Any]:
    """What data exists for this, and how do I reach it?"""
    return _response(consult.find_data(subject, purpose or None, limit))


def tool_find_precedent(resource_or_topic: str, limit: int = 10) -> dict[str, Any]:
    """Has this been used before, and what happened?"""
    return _response(consult.find_precedent(resource_or_topic, limit))


def tool_get_note(name: str) -> dict[str, Any]:
    """The full note: frontmatter, body and both directions of its links."""
    return consult.get_note(name)


def tool_search(params: dict[str, Any]) -> dict[str, Any]:
    """One typed object: {intent, terms, domain?, filters?, source?, limit?}.

    Closed enums, no additional properties, and `domain` validated against the
    register - so an invalid domain is an error rather than a silent miss.
    """
    try:
        return _response(consult.dispatch(params))
    except ValueError as exc:
        return {"error": "invalid_params", "detail": str(exc),
                "schema": consult.SEARCH_PARAMS_SCHEMA}


def tool_record_application(project: str, stage: str, outcome: str,
                            what_was_needed: str, what_was_found_and_taken: str,
                            what_it_replaced: str,
                            what_the_catalogue_should_learn: str,
                            resources_used: list[str] | None = None,
                            applied_resources: list[str] | None = None,
                            patterns_discovered: list[str] | None = None,
                            domains: list[str] | None = None,
                            date_range: str = "") -> dict[str, Any]:
    """Record what a resource was used for. The one write this surface permits.

    `what_the_catalogue_should_learn` is required and is the section that
    turns a diary entry into a requirement. Records written through this tool
    are marked `attested_by: agent`.
    """
    record = {
        "project": project, "stage": stage, "outcome": outcome,
        "date_range": date_range,
        "resources_used": resources_used or [],
        "applied_resources": applied_resources or [],
        "patterns_discovered": patterns_discovered or [],
        "domains": domains or [],
        "sections": {
            "What Was Needed": what_was_needed,
            "What Was Found And Taken": what_was_found_and_taken,
            "What It Replaced": what_it_replaced,
            "What The Catalogue Should Learn": what_the_catalogue_should_learn,
        },
    }
    try:
        return consult.record_application(record, attested_by="agent")
    except (ValueError, FileExistsError) as exc:
        return {"error": "rejected", "detail": str(exc)}


def tool_catalogue_status() -> dict[str, Any]:
    """What the index holds and when it was last built."""
    counts = index_mod.counts()
    counts["vault_root"] = str(vault_root())
    counts["index_db"] = str(index_db_path())
    counts["stale"] = index_mod.is_stale()
    return counts


# The whole surface. Nothing outside this dict is reachable through MCP, and
# exactly one entry writes.
def tool_log_use(repo_key_or_url: str, project: str = "",
                 why: str = "") -> dict[str, Any]:
    """Tell the catalogue you are using something. One call, no ceremony.

    Use this the moment you reach for a repository, whether or not you expect
    it to be here. Three possible answers:

    - **catalogued** — it is already charted, and the reply names the note.
      Read that before going further; somebody has already done this work.
    - **queued** — new to the catalogue. It joins the enrichment queue and a
      library agent will fetch, survey and stage it. Nothing is claimed about
      it until then, and you owe nothing further.
    - **seen_again** — already queued by someone else. The sighting count went
      up, which is how the queue gets ordered.

    `why` is one sentence about what you are using it for. It is stored as
    *reported by you*, never as a fact about the project, and it is the only
    part of the eventual note that will come from real use rather than a README.
    """
    try:
        return enrich_mod.log_use(repo_key_or_url, reported_by="agent",
                                  project=project, why=why)
    except ValueError as exc:
        return {"error": "rejected", "detail": str(exc)}


def tool_list_queue(status: str = "queued") -> dict[str, Any]:
    """Sources someone is using that the catalogue does not hold yet."""
    return {"queue": [e.to_dict() for e in enrich_mod.all_entries(status)]}


# ------------------------------------------------------- contribution (tier 2)
#
# Everything below writes, and none of it except `promote_proposal` can touch a
# note a reader will see. That is the whole safety argument for letting an
# unattended agent contribute: the reachable damage is a directory of JSON.

def tool_open_brief(project: str, need: str, disqualifiers: list[str],
                    constraints: dict[str, list[str]] | None = None
                    ) -> dict[str, Any]:
    """State what your project needs, in a form the library can act on.

    `disqualifiers` is required: what a candidate must not assume, require or
    depend on. Without it this is a topic list, and a topic list cannot rule
    anything out - which is how a source gets charted accurately and is still
    the wrong answer.

    Returns the brief plus what the catalogue *already* holds for this need, so
    a brief that needs no research says so before anyone spends a model on it.
    """
    try:
        record = brief_mod.open_brief(project, need, disqualifiers,
                                      constraints or {}, created_by="agent")
    except (ValueError, policy.PolicyError) as exc:
        return {"error": "rejected", "detail": str(exc)}
    return record.to_dict()


def tool_list_briefs(status: str = "") -> dict[str, Any]:
    """Briefs, optionally filtered to open / claimed / closed."""
    return {"briefs": [b.to_dict() for b in brief_mod.all_briefs(status)]}


def tool_claim_brief(brief_id: str, agent: str) -> dict[str, Any]:
    """Take responsibility for a brief before working it."""
    try:
        return brief_mod.claim(brief_id, agent).to_dict()
    except policy.PolicyError as exc:
        return exc.to_result()


def tool_propose_resource(repo_key: str, canonical_url: str,
                          axes: dict[str, str], evidence: dict[str, Any],
                          brief_id: str = "",
                          metadata: dict[str, Any] | None = None,
                          sections: dict[str, str] | None = None
                          ) -> dict[str, Any]:
    """Stage a source for the catalogue. Writes to staging, never to the vault.

    Fill the structured fields from what you fetched. Leave `Bottom Line` and
    `What It Solves` alone - those are written at promotion by whoever stands
    behind the note, and this tool refuses them.

    `evidence` must show the source was actually fetched: a `survey` name, a
    `file_count`, or a `fetched_at` with a `source`.
    """
    try:
        proposal = propose_mod.propose(
            repo_key, canonical_url, axes or {}, evidence or {},
            brief_id=brief_id, proposed_by="agent",
            metadata=metadata, sections=sections)
    except (ValueError, policy.PolicyError) as exc:
        return {"error": "rejected", "detail": str(exc)}
    # Say now what promotion would refuse later. A proposal that sits in staging
    # looking finished and can never be promoted is worse than a refusal.
    return {**proposal.to_dict(), **propose_mod.readiness(proposal)}


def tool_decide_candidate(brief_id: str, repo_key: str, disposition: str,
                          reason: str = "") -> dict[str, Any]:
    """Record what happened to one candidate. A rejection needs a reason."""
    try:
        return brief_mod.decide(brief_id, repo_key, disposition,
                                reason=reason).to_dict()
    except (ValueError, policy.PolicyError) as exc:
        return {"error": "rejected", "detail": str(exc)}


def tool_close_brief(brief_id: str, summary: str,
                     discard_undisposed: bool = False) -> dict[str, Any]:
    """End a research session. Refuses while any candidate is undecided.

    Every candidate must be `proposed`, `rejected` (with a reason) or explicitly
    discarded. The reasons are the point: *its sense model assumes ESP32 input
    shape* is worth more to the next search than most positive entries, and it
    exists only if written here.
    """
    try:
        return brief_mod.close(brief_id, summary,
                               discard_undisposed=discard_undisposed).to_dict()
    except policy.PolicyError as exc:
        return exc.to_result()


def tool_list_proposals(status: str = "") -> dict[str, Any]:
    """What is waiting in staging."""
    return {"proposals": [p.to_dict() for p in propose_mod.all_proposals(status)]}


# ---------------------------------------------------------- curation (tier 3)

def tool_promote_proposal(proposal_id: str, bottom_line: str,
                          what_it_solves: str, primary_topic: str = "",
                          sections: dict[str, str] | None = None
                          ) -> dict[str, Any]:
    """Write a staged proposal into the vault. The only tool that writes truth.

    Requires the interpretation - the sentence a reader acts on - because a
    note whose Bottom Line was generated is a note nobody has read. The result
    is `rejected` with the violations if the vault's own integrity checks would
    not accept the note.
    """
    try:
        return propose_mod.promote(proposal_id, bottom_line, what_it_solves,
                                   primary_topic=primary_topic,
                                   sections=sections, promoted_by="agent")
    except (ValueError, FileExistsError, policy.PolicyError) as exc:
        return {"error": "rejected", "detail": str(exc)}


TOOLS: dict[str, Callable[..., Any]] = {
    "orient": tool_orient,
    "find_donor": tool_find_donor,
    "find_pattern": tool_find_pattern,
    "find_technique": tool_find_technique,
    "find_data": tool_find_data,
    "find_precedent": tool_find_precedent,
    "get_note": tool_get_note,
    "search": tool_search,
    "record_application": tool_record_application,
    "catalogue_status": tool_catalogue_status,
    "log_use": tool_log_use,
    "list_queue": tool_list_queue,
    # tier 2 - contribution. Writes, but only into `.Data/`.
    "open_brief": tool_open_brief,
    "list_briefs": tool_list_briefs,
    "claim_brief": tool_claim_brief,
    "propose_resource": tool_propose_resource,
    "decide_candidate": tool_decide_candidate,
    "close_brief": tool_close_brief,
    "list_proposals": tool_list_proposals,
    # tier 3 - curation. The only tool that writes a note a reader will see.
    "promote_proposal": tool_promote_proposal,
}

# Three tiers, because "exactly one tool writes" stopped being true the moment
# outside agents were allowed to contribute - and the honest replacement is not
# a longer write list but a statement of *what each write can reach*.
#
#   consult     read, plus one append to `09-Applications/`
#   contribute  the above, plus briefs and staged proposals in `.Data/`
#   curate      the above, plus promotion into `01-Resources/`
#
# A library agent runs at `contribute` and cannot alter a single note a reader
# sees. Promotion is a separate grant because it is the only step that changes
# that, and the step that requires a sentence somebody stands behind.
CONSULT_TOOLS = frozenset({
    "orient", "find_donor", "find_pattern", "find_technique", "find_data",
    "find_precedent", "get_note", "search", "catalogue_status",
    # `log_use` sits at consult on purpose. It is the cheapest possible
    # contribution and the one most worth making frictionless: it writes a
    # queue entry in `.Data/`, claims nothing, and turns "I reached for this"
    # into a charted source without the caller stopping to chart anything.
    "record_application", "log_use", "list_queue",
})
CONTRIBUTE_TOOLS = frozenset({
    "open_brief", "list_briefs", "claim_brief", "propose_resource",
    "decide_candidate", "close_brief", "list_proposals",
})
CURATE_TOOLS = frozenset({"promote_proposal"})

TIERS: dict[str, frozenset[str]] = {
    "consult": CONSULT_TOOLS,
    "contribute": CONSULT_TOOLS | CONTRIBUTE_TOOLS,
    "curate": CONSULT_TOOLS | CONTRIBUTE_TOOLS | CURATE_TOOLS,
}

# Tier membership and effect are different questions: `list_briefs` is a read
# that happens to live in the contribute tier. Deriving one from the other would
# mark it a write and hide it from a read-only server.
WRITE_TOOLS = frozenset({
    "record_application", "log_use", "open_brief", "claim_brief",
    "propose_resource", "decide_candidate", "close_brief", "promote_proposal",
})
# The writes that can reach a note a reader will open. Named rather than
# described, so "a contribute agent cannot alter the vault" is a property a
# test can assert instead of a claim in a docstring.
VAULT_WRITE_TOOLS = frozenset({"record_application"}) | CURATE_TOOLS


def read_only_tools() -> frozenset[str]:
    return frozenset(TOOLS) - WRITE_TOOLS


# ------------------------------------------------- effect, declared and enforced

# The protocol's own vocabulary for what a tool does. `readOnlyHint`,
# `destructiveHint`, `idempotentHint` and `openWorldHint` are standard MCP
# annotations, so a client that has never seen this server can reason about a
# tool before calling it.
#
# The specification is explicit that **annotations are hints, not security
# guarantees**, and `F:/Mark-XLVIII-main`'s capability handbook says the same
# thing in its own words: *registry metadata is not permission*. Two independent
# statements of one rule, so it is enforced separately below rather than trusted
# here. `EFFECTS` describes; `check_permitted` decides.
EFFECTS: dict[str, dict[str, bool]] = {
    name: {"readOnlyHint": True, "destructiveHint": False,
           "idempotentHint": True, "openWorldHint": False}
    for name in ("orient", "find_donor", "find_pattern", "find_technique",
                 "find_data", "find_precedent", "get_note", "search",
                 "catalogue_status", "capabilities", "capability_schema")
}
# Reads that happen to live in the contribution tier.
EFFECTS.update({
    name: {"readOnlyHint": True, "destructiveHint": False,
           "idempotentHint": True, "openWorldHint": False}
    for name in ("list_briefs", "list_proposals")
})

# Writes into `.Data/` only. Not destructive - nothing here can remove or alter
# a note - and not idempotent, because each call moves a brief along.
EFFECTS.update({
    name: {"readOnlyHint": False, "destructiveHint": False,
           "idempotentHint": False, "openWorldHint": False}
    for name in ("open_brief", "claim_brief", "propose_resource",
                 "decide_candidate", "close_brief")
})

# The one that writes a note. `destructiveHint` stays False because promotion
# only ever creates - it refuses rather than overwriting an existing note - but
# it is the single call on this surface that changes what a reader sees.
EFFECTS["list_queue"] = {
    "readOnlyHint": True, "destructiveHint": False,
    "idempotentHint": True, "openWorldHint": False,
}
# Idempotent by design: logging the same source twice increments a sighting
# count rather than creating a second entry, so an agent may call it freely.
EFFECTS["log_use"] = {
    "readOnlyHint": False, "destructiveHint": False,
    "idempotentHint": True, "openWorldHint": False,
}

EFFECTS["promote_proposal"] = {
    "readOnlyHint": False, "destructiveHint": False,
    "idempotentHint": False, "openWorldHint": False,
}

EFFECTS["record_application"] = {
    # Appends one note. Not destructive, and emphatically not idempotent: two
    # identical calls are two records, which is why `consult.record_application`
    # refuses a duplicate rather than overwriting.
    "readOnlyHint": False, "destructiveHint": False,
    "idempotentHint": False, "openWorldHint": False,
}


class ToolRefused(PermissionError):
    """Raised by name, so a blocked caller surfaces a decision rather than a
    stack trace. `CLOSED_ACTION_REGISTRY` made enforceable at the boundary."""


def check_permitted(name: str, *, allow_writes: bool = True,
                    tier: str = "curate") -> None:
    """The dispatch guard. Discovering a tool does not authorise calling it.

    Two refusals, both by name:

    - a tool outside `TOOLS` is not a typo to be guessed at, it is unregistered;
    - a write when the server was started read-only.

    This is deliberately not derived from `EFFECTS`. An annotation is something
    the server *says*; this is something the server *does*, and if the two ever
    disagree the enforcement is the one that holds.
    """
    if name not in TOOLS:
        raise ToolRefused(
            f"unregistered_tool: {name!r} is not in this server's registry. "
            f"Registered: {', '.join(sorted(TOOLS))}. The registry is closed - "
            f"an agent that needs something absent should report being blocked "
            f"rather than improvise.")
    permitted = TIERS.get(tier)
    if permitted is None:
        raise ToolRefused(
            f"unknown_tier: {tier!r}. Tiers: {', '.join(sorted(TIERS))}.")
    if name not in permitted:
        holder = next((t for t in ("consult", "contribute", "curate")
                       if name in TIERS[t]), "none")
        raise ToolRefused(
            f"tier_refused: {name!r} is not in the {tier!r} tier. It is "
            f"granted at {holder!r}. This server was started at {tier!r} "
            f"deliberately - restart it with --tier {holder} if that is "
            f"the intent, rather than working around it.")
    if not allow_writes and name in WRITE_TOOLS:
        raise ToolRefused(
            f"read_only_server: {name!r} writes, and this server was started "
            f"with --read-only. Restart without that flag to permit it.")


# --------------------------------------------------------- progressive disclosure

# What a capability card says, and deliberately not what its parameters are.
# Ten tools with nine filter axes is a great deal of schema to put in front of
# an agent that has not yet decided what it is doing; a card is a few dozen
# tokens and narrows the choice. The exact parameters arrive from
# `capability_schema` immediately before a call.
#
# Lifted from the capability registry in `F:/Mark-XLVIII-main`, which stages
# context as L0 card -> L1 manifest -> playbook -> function schema. This is the
# same progression as data -> information -> knowledge one layer up: cheap
# first, expensive only once it is worth it.
CARDS: dict[str, dict[str, Any]] = {
    "log_use": {
        "purpose": "Say you are using a source; get its note or queue it",
        "use_when": "the moment you reach for any repository",
        "note": "answers 'we already have this' before you spend time on it"},
    "list_queue": {"purpose": "Sources in use that are not catalogued yet",
                   "use_when": "you are a library agent looking for work"},
    "open_brief": {
        "purpose": "Ask the library to find something, with constraints",
        "use_when": "your project needs sources you do not have yet",
        "note": "states what must be ruled out, not just the topic"},
    "list_briefs": {"purpose": "Requests outstanding, claimed or closed",
                    "use_when": "you are a library agent looking for work"},
    "claim_brief": {"purpose": "Take responsibility for one brief",
                    "use_when": "before you start researching it"},
    "propose_resource": {
        "purpose": "Stage a source you fetched, into the airlock",
        "use_when": "you have evidence and the structured fields",
        "note": "cannot touch the vault; interpretation is refused here"},
    "decide_candidate": {
        "purpose": "Say what happened to something you considered",
        "use_when": "you ruled a source in or out",
        "note": "a rejection reason is the negative result nobody writes down"},
    "close_brief": {"purpose": "End the session; refuses while anything is undecided",
                    "use_when": "the research is finished"},
    "list_proposals": {"purpose": "What is waiting in staging",
                       "use_when": "you are about to review or promote"},
    "promote_proposal": {
        "purpose": "Write a staged proposal into the catalogue",
        "use_when": "you have read it and can say what it is for",
        "note": "requires the Bottom Line; this is the only write a reader sees"},
    "orient": {"purpose": "What is here, and where does a subject live",
               "use_when": "you do not yet know what the catalogue covers"},
    "find_donor": {"purpose": "What could I take, given what I can actually run",
                   "use_when": "you need a component and have real constraints",
                   "note": "constraints eliminate; they do not re-rank"},
    "find_pattern": {"purpose": "Has this shape of problem been solved before",
                     "use_when": "the question is structural rather than concrete"},
    "find_technique": {"purpose": "Where would I look to see how this is done",
                       "use_when": "you want to read an implementation"},
    "find_data": {"purpose": "What data exists, and how do I reach it",
                  "use_when": "you need a corpus, fixtures or a dataset"},
    "find_precedent": {"purpose": "Has this been used before, and what happened",
                       "use_when": "you want evidence of use rather than a claim"},
    "get_note": {"purpose": "One note in full, with both directions of its links",
                 "use_when": "you have chosen something and want everything on it"},
    "search": {"purpose": "One typed query object across every intent",
               "use_when": "you are composing a query programmatically"},
    "catalogue_status": {"purpose": "What the index holds and how stale it is",
                         "use_when": "before trusting an answer about coverage"},
    "record_application": {"purpose": "Record what a source was used for",
                           "use_when": "you finished work that used something here",
                           "note": "the only write this surface permits"},
}


def tool_capabilities() -> dict[str, Any]:
    """Every capability as a short card. Start here; fetch schemas later.

    Returns purpose, when to use it, and its declared effect - enough to choose
    without loading ten parameter schemas.
    """
    return {
        "server": SERVER_NAME,
        "reads": [dict(name=n, **CARDS.get(n, {}), effect=EFFECTS.get(n, {}))
                  for n in sorted(read_only_tools())],
        "writes": [dict(name=n, **CARDS.get(n, {}), effect=EFFECTS.get(n, {}))
                   for n in sorted(WRITE_TOOLS)],
        "next": "call capability_schema(name) for the exact parameters of one "
                "tool, immediately before calling it",
    }


def tool_capability_schema(name: str) -> dict[str, Any]:
    """The exact parameters of one capability, loaded just in time.

    Refuses an unregistered name the same way a call would, so an agent
    discovers the registry is closed while exploring rather than while acting.
    """
    try:
        check_permitted(name)
    except ToolRefused as exc:
        return {"error": "unregistered_tool", "detail": str(exc),
                "registered": sorted(TOOLS)}
    import inspect

    function = TOOLS[name]
    signature = inspect.signature(function)
    parameters = []
    for parameter in signature.parameters.values():
        entry: dict[str, Any] = {"name": parameter.name}
        if parameter.annotation is not inspect.Parameter.empty:
            entry["type"] = getattr(parameter.annotation, "__name__",
                                    str(parameter.annotation))
        entry["required"] = parameter.default is inspect.Parameter.empty
        if not entry["required"]:
            entry["default"] = parameter.default
        parameters.append(entry)
    out = {"name": name, "purpose": CARDS.get(name, {}).get("purpose", ""),
           "effect": EFFECTS.get(name, {}), "parameters": parameters,
           "doc": (function.__doc__ or "").strip()}
    if name == "search":
        out["params_schema"] = consult.SEARCH_PARAMS_SCHEMA
    # The permitted values, on the tool a caller was told to use. Omitting them
    # here while `search` carried them was how a cold agent guessed
    # `license_class="permissive"` and got a confident, empty answer.
    axes = consult.axis_vocabulary()
    for parameter in parameters:
        if parameter["name"] in axes:
            parameter["enum"] = list(axes[parameter["name"]])
            parameter["case_sensitive"] = True
    return out


# ------------------------------------------------------------------- server
def build_server(*, allow_writes: bool = True,
                 tier: str = "curate"):                    # pragma: no cover - needs SDK
    """Wire the tools onto FastMCP. Returns None when the SDK is absent.

    Every tool carries its MCP annotations so a client can reason about effect
    before calling, and every call still passes `check_permitted` - because the
    specification says annotations are hints and this system's own
    `CLOSED_ACTION_REGISTRY` says the registry is not permission.
    """
    try:
        from mcp.server.fastmcp import FastMCP
    except Exception:
        return None

    server = FastMCP(SERVER_NAME, instructions=SERVER_INSTRUCTIONS)
    surface = dict(TOOLS)
    surface["capabilities"] = tool_capabilities
    surface["capability_schema"] = tool_capability_schema

    granted = TIERS.get(tier, TIERS["curate"]) | {"capabilities",
                                                  "capability_schema"}
    for name, function in surface.items():
        # A tool outside the tier is not registered at all, rather than
        # registered and refused: an agent should not see a capability it can
        # never reach, and progressive disclosure is cheaper when the list is
        # already the truth.
        if name not in granted:
            continue
        if not allow_writes and name in WRITE_TOOLS:
            continue
        server.add_tool(_guarded(name, function, allow_writes, tier),
                        name=name,
                        annotations=EFFECTS.get(name))
    return server


def _guarded(name: str, function: Callable[..., Any], allow_writes: bool,
             tier: str = "curate"):
    """Enforcement at the boundary, not merely a declaration in a table."""
    import functools

    @functools.wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            check_permitted(name, allow_writes=allow_writes, tier=tier)
        except ToolRefused as exc:
            return {"error": "refused", "detail": str(exc)}
        return function(*args, **kwargs)

    return wrapper


def main(argv: list[str] | None = None) -> int:            # pragma: no cover - entry
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="MCP surface over the Resource Library")
    parser.add_argument("--list", action="store_true",
                        help="print the tool surface and exit")
    parser.add_argument("--read-only", action="store_true",
                        help="refuse record_application; serve reads only")
    parser.add_argument("--tier", default="curate", choices=sorted(TIERS),
                        help="how much of the surface to expose: consult "
                             "(read + application records), contribute (adds "
                             "briefs and staged proposals, cannot alter a "
                             "note), curate (adds promotion into the vault)")
    parser.add_argument("--http", action="store_true",
                        help="serve over loopback HTTP instead of stdio")
    parser.add_argument("--port", type=int, default=8321)
    parser.add_argument("--host", default="127.0.0.1",
                        help="ignored unless --http; anything but a loopback "
                             "address is refused")
    args = parser.parse_args(argv)

    if args.list:
        print(json.dumps({"server": SERVER_NAME,
                          "tier": args.tier,
                          "granted": sorted(TIERS[args.tier]),
                          "read_only": sorted(read_only_tools()),
                          "writes": sorted(WRITE_TOOLS),
                          "reaches_the_vault": sorted(VAULT_WRITE_TOOLS),
                          "effects": EFFECTS}, indent=2))
        return 0

    server = build_server(allow_writes=not args.read_only, tier=args.tier)
    if server is None:
        print("The MCP SDK is not installed; `pip install mcp` to serve. The "
              "tool functions in librarian.mcp_server remain importable and "
              "usable in-process.", file=sys.stderr)
        return 2

    if not args.http:
        server.run()                                       # stdio: a subprocess agent
        return 0

    # Loopback only. A catalogue of one person's research has no business on a
    # network interface, and the MCP guidance for local HTTP servers is
    # explicit: bind 127.0.0.1, validate Origin, and enable DNS-rebinding
    # protection. Refusing a non-loopback host is cheaper than explaining the
    # consequences of allowing one.
    if args.host not in ("127.0.0.1", "::1", "localhost"):
        print(f"refused: --host {args.host} is not a loopback address. This "
              f"server is not built to be reachable from a network.",
              file=sys.stderr)
        return 2
    settings = getattr(server, "settings", None)
    if settings is not None:
        for attribute, value in (("host", args.host), ("port", args.port)):
            if hasattr(settings, attribute):
                setattr(settings, attribute, value)
    print(f"serving on http://{args.host}:{args.port} (loopback only)",
          file=sys.stderr)
    server.run(transport="streamable-http")
    return 0

if __name__ == "__main__":                                 # pragma: no cover
    raise SystemExit(main())
