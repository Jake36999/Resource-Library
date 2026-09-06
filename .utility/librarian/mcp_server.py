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

from . import consult
from . import index as index_mod
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
}

WRITE_TOOLS = frozenset({"record_application"})


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


def check_permitted(name: str, *, allow_writes: bool = True) -> None:
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
def build_server(*, allow_writes: bool = True):            # pragma: no cover - needs SDK
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

    for name, function in surface.items():
        if not allow_writes and name in WRITE_TOOLS:
            continue
        server.add_tool(_guarded(name, function, allow_writes),
                        name=name,
                        annotations=EFFECTS.get(name))
    return server


def _guarded(name: str, function: Callable[..., Any], allow_writes: bool):
    """Enforcement at the boundary, not merely a declaration in a table."""
    import functools

    @functools.wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            check_permitted(name, allow_writes=allow_writes)
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
    parser.add_argument("--http", action="store_true",
                        help="serve over loopback HTTP instead of stdio")
    parser.add_argument("--port", type=int, default=8321)
    parser.add_argument("--host", default="127.0.0.1",
                        help="ignored unless --http; anything but a loopback "
                             "address is refused")
    args = parser.parse_args(argv)

    if args.list:
        print(json.dumps({"server": SERVER_NAME,
                          "read_only": sorted(read_only_tools()),
                          "writes": sorted(WRITE_TOOLS),
                          "effects": EFFECTS}, indent=2))
        return 0

    server = build_server(allow_writes=not args.read_only)
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
