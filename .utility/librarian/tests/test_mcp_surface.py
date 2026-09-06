"""The agent surface: what it exposes, what it refuses, and how it says so.

Written against Stage 3a. The server itself predates this and worked; what it
lacked was everything that makes it usable by an agent that has never seen the
project — a cheap way to choose a tool, a schema loaded when it is needed, and
a refusal that names the rule rather than raising a stack trace.
"""
from __future__ import annotations

import pytest

from librarian import mcp_server as mcp


# --------------------------------------------------------------- the registry

def test_the_registry_is_closed_and_says_so_by_name():
    """`CLOSED_ACTION_REGISTRY` enforced at the boundary. An agent that needs
    something absent must report being blocked, not improvise."""
    with pytest.raises(mcp.ToolRefused) as caught:
        mcp.check_permitted("delete_the_vault")
    message = str(caught.value)
    assert "unregistered_tool" in message
    assert "delete_the_vault" in message
    assert "Registered:" in message, "a refusal must say what is available"


def test_a_read_only_server_refuses_the_write_and_names_the_flag():
    with pytest.raises(mcp.ToolRefused) as caught:
        mcp.check_permitted("record_application", allow_writes=False)
    assert "read_only_server" in str(caught.value)
    assert "--read-only" in str(caught.value), "say how to undo the refusal"

    mcp.check_permitted("record_application", allow_writes=True)


def test_exactly_one_tool_writes():
    """The property the whole surface rests on: safe to expose because the
    reachable mutation is one append."""
    assert mcp.WRITE_TOOLS == {"record_application"}
    assert mcp.read_only_tools() == frozenset(mcp.TOOLS) - mcp.WRITE_TOOLS
    assert len(mcp.read_only_tools()) == 9


# ------------------------------------------------------------------- effects

def test_every_tool_declares_its_effect():
    for name in mcp.TOOLS:
        assert name in mcp.EFFECTS, f"{name} has no declared effect"
        effect = mcp.EFFECTS[name]
        assert set(effect) == {"readOnlyHint", "destructiveHint",
                               "idempotentHint", "openWorldHint"}


def test_the_declared_effects_agree_with_the_registry():
    """A table that drifts from the code it describes is worse than no table."""
    for name in mcp.read_only_tools():
        assert mcp.EFFECTS[name]["readOnlyHint"] is True, name
    for name in mcp.WRITE_TOOLS:
        assert mcp.EFFECTS[name]["readOnlyHint"] is False, name


def test_the_write_is_not_idempotent_and_not_destructive():
    """Two identical calls are two records - which is why
    `consult.record_application` refuses a duplicate rather than overwriting."""
    effect = mcp.EFFECTS["record_application"]
    assert effect["idempotentHint"] is False
    assert effect["destructiveHint"] is False


def test_enforcement_does_not_read_the_annotation_table():
    """The MCP specification says annotations are hints, not security
    guarantees; `F:/Mark-XLVIII-main`'s handbook says *registry metadata is not
    permission*. So corrupting the description must not widen what is allowed."""
    original = dict(mcp.EFFECTS["record_application"])
    mcp.EFFECTS["record_application"] = {"readOnlyHint": True,
                                         "destructiveHint": False,
                                         "idempotentHint": True,
                                         "openWorldHint": False}
    try:
        with pytest.raises(mcp.ToolRefused):
            mcp.check_permitted("record_application", allow_writes=False)
    finally:
        mcp.EFFECTS["record_application"] = original


# ------------------------------------------------------- progressive disclosure

def test_the_first_call_is_cheap_and_names_the_second():
    """Ten tools with nine filter axes is too much schema to put in front of an
    agent that has not decided what it is doing."""
    cards = mcp.tool_capabilities()
    assert {c["name"] for c in cards["reads"]} == set(mcp.read_only_tools())
    assert {c["name"] for c in cards["writes"]} == set(mcp.WRITE_TOOLS)
    for card in cards["reads"] + cards["writes"]:
        assert card["purpose"], f"{card['name']} has no purpose"
        assert card["effect"], f"{card['name']} has no declared effect"
        assert "parameters" not in card, "a card must not carry a schema"
    assert "capability_schema" in cards["next"]


def test_a_schema_arrives_only_when_asked_for():
    schema = mcp.tool_capability_schema("find_donor")
    names = [p["name"] for p in schema["parameters"]]
    assert names[0] == "need"
    assert {"license_class", "deployment_target", "hardware_footprint"} <= set(names)
    assert schema["effect"]["readOnlyHint"] is True
    assert schema["doc"]


def test_the_typed_query_carries_its_json_schema():
    schema = mcp.tool_capability_schema("search")
    assert "params_schema" in schema, \
        "`search` takes one opaque object, so its schema is the only guide"


def test_asking_for_an_unregistered_schema_refuses_rather_than_guessing():
    """An agent should discover the registry is closed while exploring, not
    while acting."""
    out = mcp.tool_capability_schema("exfiltrate")
    assert out["error"] == "unregistered_tool"
    assert sorted(mcp.TOOLS) == out["registered"]


def test_a_card_exists_for_every_registered_tool():
    missing = set(mcp.TOOLS) - set(mcp.CARDS)
    assert not missing, f"undocumented in the L0 listing: {sorted(missing)}"


# ----------------------------------------------------------------- transports

def test_a_non_loopback_host_is_refused():
    """A catalogue of one person's research has no business on a network
    interface. The MCP guidance for local HTTP is bind 127.0.0.1 and validate
    Origin; refusing outright is cheaper than explaining the consequences."""
    assert mcp.main(["--http", "--host", "0.0.0.0"]) == 2
    assert mcp.main(["--http", "--host", "10.0.0.5"]) == 2


def test_the_surface_listing_needs_no_sdk_and_no_vault():
    """`--list` is how an operator checks what would be exposed before
    exposing it."""
    assert mcp.main(["--list"]) == 0
