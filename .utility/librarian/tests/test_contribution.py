"""The contribution path: brief, propose, decide, close, promote.

Written because four agents in four projects are about to be pointed at this
vault and told to log what they find. Every test below is a refusal that has to
hold when the thing being refused is unattended and in a hurry.

The refusals are the interesting assertions. A test that a valid proposal works
proves the happy path; a test that an invalid one is *stopped by name* is what
makes it safe to hand the surface to something that has never read the design
specification.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from librarian import brief as brief_mod
from librarian import mcp_server as mcp
from librarian import policy
from librarian import propose as propose_mod


AXES = {"license_class": "Permissive", "domain_primary": "Infrastructure",
        "ecosystem": "Python", "maturity_stage": "Production_Ready",
        "deployment_target": "Server", "interface_protocol": "CLI",
        "data_locality": "Local_First", "hardware_footprint": "CPU_Only",
        "security_compliance": "Uncertified", "agent_surface": "Procedural"}

EVIDENCE = {"survey": "2026-09-09-cohort.json", "file_count": 120,
            "fetched_at": "2026-09-09T10:00:00Z", "source": "github api"}

EVIDENCE_SECTIONS = {
    "What Is Inside": "- 120 files.",
    "Architecture & Mechanics": "- A queue with a retry table.",
    "Integration & Use Cases": "- Runs beside an existing worker.",
}


@pytest.fixture()
def catalogue(vault: Path, tmp_path: Path, monkeypatch) -> Path:
    """Point every path helper at a throwaway vault.

    The whole module resolves paths through `config`, never at import, so
    redirecting the environment is enough - which is the portability property
    `test_portability` already pins.
    """
    monkeypatch.setenv("CATALOGUE_VAULT", str(vault))
    monkeypatch.setenv("CATALOGUE_DATA", str(tmp_path / "data"))
    # The real content model, not a hand-written stand-in. These tests assert
    # that an axis value outside its enumeration is refused; asserting that
    # against a copy of the enumeration would only prove the copy exists.
    model = Path(__file__).resolve().parents[3] / "internal docs" / "Note Content Model.md"
    if model.exists():
        target = vault / "internal docs" / model.name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(model.read_text(encoding="utf-8"), encoding="utf-8")
    return vault


def open_one(**overrides):
    payload = {
        "project": "network_management",
        "need": "a sensing model that consumes raw Intel 5300 CSI",
        "disqualifiers": ["must not assume ESP32 CSI shape"],
        "constraints": {"license_class": ["Permissive"]},
        "assess_coverage": False,
    }
    payload.update(overrides)
    return brief_mod.open_brief(**payload)


# ------------------------------------------------------------------- briefs

def test_a_brief_without_disqualifiers_is_refused(catalogue):
    """The RuView case. A topic list finds the right area and the wrong answer,
    because the fact that disqualifies a candidate is a fact about the asker."""
    with pytest.raises(policy.PolicyError) as caught:
        open_one(disqualifiers=[])
    assert caught.value.code == policy.BRIEF_REQUIRED
    assert "topic list" in caught.value.message


def test_whitespace_is_not_a_disqualifier(catalogue):
    with pytest.raises(policy.PolicyError):
        open_one(disqualifiers=["   ", ""])


def test_an_unknown_axis_value_is_refused_rather_than_matching_nothing(catalogue):
    """A constraint outside its enumeration silently matches nothing, and a
    brief nobody can satisfy reads exactly like a brief nobody has done yet."""
    with pytest.raises(ValueError) as caught:
        open_one(constraints={"license_class": ["permissive"]})
    assert "Permissive" in str(caught.value)


def test_an_unknown_axis_is_refused_and_lists_the_real_ones(catalogue):
    with pytest.raises(ValueError) as caught:
        open_one(constraints={"licence": ["Permissive"]})
    assert "license_class" in str(caught.value)


def test_a_brief_records_who_asked_and_what_is_ruled_out(catalogue):
    record = open_one()
    assert record.status == brief_mod.OPEN
    assert record.disqualifiers == ("must not assume ESP32 CSI shape",)
    assert brief_mod.load(record.brief_id).need == record.need


def test_claiming_twice_by_different_agents_is_refused(catalogue):
    record = brief_mod.claim(open_one().brief_id, "agent-a")
    with pytest.raises(policy.PolicyError):
        brief_mod.claim(record.brief_id, "agent-b")
    # the same agent re-claiming is not an error; it is a resumed session
    brief_mod.claim(record.brief_id, "agent-a")


def test_opening_a_brief_reports_what_is_already_catalogued(catalogue, built,
                                                            monkeypatch):
    """The cheapest possible answer to a research request is *we already have
    this*. It is worth nothing if the call that produces it can break quietly -
    which it did: a wrong attribute name was swallowed into `verdict: unknown`
    and reported as though coverage had merely been inconclusive.
    """
    monkeypatch.setenv("CATALOGUE_INDEX_DB", str(built))
    record = brief_mod.open_brief(
        "network_management", "a scheduler that resumes after a failed task",
        ["must not require a hosted control plane"])
    assert record.coverage["verdict"] in {"covered", "thin", "uncovered"},         record.coverage
    assert "widget-scheduler" in record.coverage["already_catalogued"]


# ------------------------------------------------------------- dispositions

def test_a_rejection_without_a_reason_is_refused(catalogue):
    """The reason is the negative result. `RuView's sense model assumes ESP32
    input shape` is worth more to the next search than most positive entries,
    and it exists only if something insists on it here."""
    record = open_one()
    brief_mod.add_candidate(record.brief_id, "ruview/ruview")
    with pytest.raises(policy.PolicyError) as caught:
        brief_mod.decide(record.brief_id, "ruview/ruview", brief_mod.REJECTED)
    assert caught.value.code == policy.DISPOSITION_REQUIRED


def test_deciding_on_something_never_added_is_refused(catalogue):
    record = open_one()
    with pytest.raises(ValueError):
        brief_mod.decide(record.brief_id, "never/seen", brief_mod.REJECTED,
                         reason="x")


def test_closing_refuses_while_a_candidate_is_undecided(catalogue):
    record = open_one()
    brief_mod.add_candidate(record.brief_id, "someone/unlooked-at")
    with pytest.raises(policy.PolicyError) as caught:
        brief_mod.close(record.brief_id, "done")
    assert caught.value.code == policy.DISPOSITION_REQUIRED
    assert "someone/unlooked-at" in caught.value.message


def test_closing_needs_a_summary(catalogue):
    with pytest.raises(policy.PolicyError):
        brief_mod.close(open_one().brief_id, "   ")


def test_discarding_is_allowed_but_never_silent(catalogue):
    """The escape hatch leaves a trace. Dropping a candidate is a decision and
    the brief still shows what was seen and let go."""
    record = open_one()
    brief_mod.add_candidate(record.brief_id, "someone/unlooked-at")
    closed = brief_mod.close(record.brief_id, "out of budget",
                             discard_undisposed=True,
                             discard_reason="ran out of session budget")
    assert closed.status == brief_mod.CLOSED
    dropped = closed.candidates[0]
    assert dropped.disposition == brief_mod.DISCARDED
    assert dropped.reason == "ran out of session budget"
    assert not closed.undisposed


def test_a_closed_brief_takes_no_further_work(catalogue):
    record = open_one()
    brief_mod.close(record.brief_id, "nothing found")
    with pytest.raises(policy.PolicyError):
        brief_mod.add_candidate(record.brief_id, "late/arrival")


# ------------------------------------------------------------------ propose

def test_a_proposal_without_evidence_is_refused(catalogue):
    """`EVIDENCE_REQUIRED` enforced rather than asserted. A field nobody
    fetched is a guess, and a guess is what this catalogue exists not to hold."""
    with pytest.raises(policy.PolicyError) as caught:
        propose_mod.propose("acme/thing", "https://github.com/acme/thing",
                            AXES, {})
    assert caught.value.code == policy.EVIDENCE_REQUIRED


def test_a_bare_fetched_at_is_not_evidence(catalogue):
    with pytest.raises(policy.PolicyError):
        propose_mod.propose("acme/thing", "https://github.com/acme/thing",
                            AXES, {"fetched_at": "2026-09-09T10:00:00Z"})


def test_an_axis_value_outside_the_enumeration_is_refused_by_name(catalogue):
    with pytest.raises(policy.PolicyError) as caught:
        propose_mod.propose("acme/thing", "https://github.com/acme/thing",
                            {**AXES, "license_class": "Copyfree"}, EVIDENCE)
    assert caught.value.code == policy.NO_SCHEMA_DRIFT
    assert "Permissive" in caught.value.message


def test_a_machine_may_not_write_the_interpretation(catalogue):
    """The one rule that keeps a thousand notes readable. A local model fills
    enumerations well and writes plausible mush, and mush passes every
    structural check there is."""
    with pytest.raises(policy.PolicyError) as caught:
        propose_mod.propose("acme/thing", "https://github.com/acme/thing",
                            AXES, EVIDENCE,
                            sections={"Bottom Line": "A great tool."})
    assert caught.value.code == policy.INTERPRETATION_IS_NOT_MACHINE_WORK


def test_a_source_already_catalogued_is_refused_with_the_note_that_has_it(catalogue):
    with pytest.raises(policy.PolicyError) as caught:
        propose_mod.propose("example/widget-scheduler",
                            "https://github.com/example/widget-scheduler",
                            AXES, EVIDENCE)
    assert caught.value.code == policy.STAGING_BEFORE_VAULT
    assert "widget-scheduler" in caught.value.message


def test_proposing_writes_to_staging_and_never_to_the_vault(catalogue):
    before = {p.name for p in (catalogue / "01-Resources").glob("*.md")}
    proposal = propose_mod.propose("acme/thing", "https://github.com/acme/thing",
                                   AXES, EVIDENCE, sections=EVIDENCE_SECTIONS)
    after = {p.name for p in (catalogue / "01-Resources").glob("*.md")}
    assert before == after, "propose must not touch the vault"
    assert proposal.path().exists()
    assert json.loads(proposal.path().read_text(encoding="utf-8"))["status"] == "staged"


def test_readiness_says_what_promotion_would_refuse_later(catalogue):
    """A proposal that sits in staging looking finished and can never be
    promoted is worse than a refused one."""
    thin = propose_mod.propose("acme/thin", "https://github.com/acme/thin",
                               AXES, EVIDENCE)
    verdict = propose_mod.readiness(thin)
    assert verdict["ready"] is False
    assert any("Architecture & Mechanics" in p for p in verdict["blocked_on"])

    # It catches missing frontmatter as well as missing sections, which is the
    # more useful half: `github_stars` and `github_pushed_at` are required, and
    # an agent that did not fetch them can be told so while it is still holding
    # the connection rather than at promotion a day later.
    assert any("github_stars" in p for p in verdict["blocked_on"])

    full = propose_mod.propose("acme/full", "https://github.com/acme/full",
                               AXES, EVIDENCE, sections=EVIDENCE_SECTIONS,
                               metadata={"primary_topic": "Plumbing",
                                         "license": "MIT", "github_stars": 10,
                                         "github_pushed_at": "2026-08-01T00:00:00Z"})
    assert propose_mod.readiness(full)["ready"] is True,         propose_mod.readiness(full)["blocked_on"]


def test_a_proposal_against_a_brief_disposes_of_itself(catalogue):
    record = open_one()
    proposal = propose_mod.propose("acme/thing", "https://github.com/acme/thing",
                                   AXES, EVIDENCE, brief_id=record.brief_id,
                                   sections=EVIDENCE_SECTIONS)
    reloaded = brief_mod.load(record.brief_id)
    assert not reloaded.undisposed
    assert reloaded.candidates[0].proposal_id == proposal.proposal_id


# ------------------------------------------------------------------ promote

def _staged(**overrides):
    payload = {"repo_key": "acme/thing",
               "canonical_url": "https://github.com/acme/thing",
               "axes": AXES, "evidence": EVIDENCE,
               "sections": EVIDENCE_SECTIONS,
               "metadata": {"primary_topic": "Plumbing", "license": "MIT",
                            "github_stars": 10,
                            "github_pushed_at": "2026-08-01T00:00:00Z"}}
    payload.update(overrides)
    return propose_mod.propose(**payload)


def test_promotion_without_interpretation_is_refused(catalogue):
    proposal = _staged()
    with pytest.raises(policy.PolicyError) as caught:
        propose_mod.promote(proposal.proposal_id, "", "something")
    assert caught.value.code == policy.INTERPRETATION_IS_NOT_MACHINE_WORK


def test_promotion_writes_a_note_the_vault_accepts(catalogue):
    from librarian import integrity, notes

    proposal = _staged()
    result = propose_mod.promote(
        proposal.proposal_id,
        "Runs dependent jobs and resumes rather than restarting.",
        "- Re-running a whole batch after one task fails.",
        primary_topic="Plumbing")
    assert result["status"] == "written", result

    path = Path(result["path"])
    assert path.parent.name == "01-Resources"
    note = notes.load_note(path, catalogue)
    errors = [v for check in (integrity.check_frontmatter_complete,
                              integrity.check_sections_complete,
                              integrity.check_axis_values_known)
              for v in check(catalogue, [note])
              if v.severity != integrity.WARNING]
    assert not errors, errors


def test_a_note_the_vault_would_reject_is_reported_not_written(catalogue):
    """The airlock refuses exactly what `librarian integrity` would, because it
    calls the same three checks rather than a second copy of the rules."""
    proposal = _staged(sections={"What Is Inside": "- some files."})
    result = propose_mod.promote(proposal.proposal_id, "A thing.", "- A need.",
                                 primary_topic="Plumbing")
    assert result["status"] == "rejected"
    assert any("Architecture & Mechanics" in v for v in result["violations"])
    assert not (catalogue / "01-Resources" / "acme - thing.md").exists()


def test_promoting_twice_is_refused(catalogue):
    proposal = _staged()
    propose_mod.promote(proposal.proposal_id, "A thing.", "- A need.",
                        primary_topic="Plumbing")
    with pytest.raises(policy.PolicyError) as caught:
        propose_mod.promote(proposal.proposal_id, "A thing.", "- A need.",
                            primary_topic="Plumbing")
    assert caught.value.code == policy.STAGING_BEFORE_VAULT


def test_dry_run_renders_without_writing(catalogue):
    proposal = _staged()
    result = propose_mod.promote(proposal.proposal_id, "A thing.", "- A need.",
                                 primary_topic="Plumbing", dry_run=True)
    assert result["status"] == "would_write"
    assert "## Bottom Line" in result["text"]
    assert not (catalogue / "01-Resources" / "acme - thing.md").exists()


# -------------------------------------------------------------- the tiers

def test_the_three_tiers_are_nested_and_named(catalogue):
    assert mcp.TIERS["consult"] < mcp.TIERS["contribute"] < mcp.TIERS["curate"]
    assert mcp.TIERS["curate"] == frozenset(mcp.TOOLS)


def test_a_contribute_agent_cannot_reach_the_vault(catalogue):
    """The property that replaces "exactly one tool writes", which stopped
    being true the moment outside agents were allowed to contribute.

    A library agent may fill staging all day. The reachable damage is a
    directory of JSON.
    """
    reachable = mcp.TIERS["contribute"] & mcp.VAULT_WRITE_TOOLS
    assert reachable == {"record_application"}, (
        "the only vault write a contribute agent holds should be the append to "
        "09-Applications; promotion belongs to curate")
    assert "promote_proposal" not in mcp.TIERS["contribute"]


def test_promotion_is_refused_below_its_tier_and_says_where_it_lives(catalogue):
    with pytest.raises(mcp.ToolRefused) as caught:
        mcp.check_permitted("promote_proposal", tier="contribute")
    message = str(caught.value)
    assert "tier_refused" in message
    assert "curate" in message, "a refusal must say where the capability lives"


def test_an_unknown_tier_is_refused_rather_than_defaulting_open(catalogue):
    with pytest.raises(mcp.ToolRefused) as caught:
        mcp.check_permitted("find_donor", tier="admin")
    assert "unknown_tier" in str(caught.value)


def test_reads_in_the_contribute_tier_are_not_marked_as_writes(catalogue):
    """Tier membership and effect are different questions. Deriving one from
    the other marked `list_briefs` a write and hid it from a read-only server."""
    for name in ("list_briefs", "list_proposals"):
        assert name in mcp.TIERS["contribute"]
        assert name not in mcp.WRITE_TOOLS
        assert mcp.EFFECTS[name]["readOnlyHint"] is True


def test_every_contribution_tool_declares_an_effect_and_a_card(catalogue):
    for name in mcp.CONTRIBUTE_TOOLS | mcp.CURATE_TOOLS:
        assert name in mcp.EFFECTS, f"{name} has no declared effect"
        assert name in mcp.CARDS, f"{name} has no capability card"


def test_the_tool_surface_refuses_the_same_things_the_module_does(catalogue):
    """The MCP wrapper must not soften a refusal into an empty result."""
    refused = mcp.tool_open_brief("p", "n", [])
    assert refused["error"] == "rejected"
    assert policy.BRIEF_REQUIRED in refused["detail"]

    staged = mcp.tool_propose_resource("acme/thing",
                                       "https://github.com/acme/thing",
                                       AXES, {})
    assert staged["error"] == "rejected"
    assert policy.EVIDENCE_REQUIRED in staged["detail"]


def test_the_propose_tool_reports_readiness_with_the_proposal(catalogue):
    result = mcp.tool_propose_resource("acme/thing",
                                       "https://github.com/acme/thing",
                                       AXES, EVIDENCE)
    assert result["ready"] is False
    assert result["blocked_on"]
