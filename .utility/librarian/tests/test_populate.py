"""The unattended runner, driven offline.

A population pass is the one part of this system that runs with nobody
watching, so the interesting assertions are about what it does when things go
wrong: a repository that will not clone, a model that will not answer, a
candidate that is already charted. None of those may end the run, and none of
them may produce a silent gap.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from librarian import brief as brief_mod
from librarian import content_model, derive, enrich, populate
from librarian import propose as propose_mod
from librarian.localmodel import LocalModel, ModelUnavailable


META = {"description": "A durable queue that resumes after a failed task.",
        "language": "Python", "stars": 412, "pushed_at": "2026-08-30T00:00:00Z",
        "license_spdx": "MIT", "html_url": "https://github.com/acme/queue"}

README = ("# queue\n\nA durable message queue. Reads jobs from disk, retries "
          "failed ones, and exposes a CLI. Runs on a single machine.")

SURVEY = {"file_count": 210, "directories": {"src": 100, "tests": 60},
          # The shape a live survey writes: a list of "ext (n)" strings, and a
          # complete path listing.
          "extensions": [".py (150)", ".md (30)"],
          "paths": ["src/queue.py", "tests/test_queue.py", "README.md"],
          "survey_file": "2026-09-09-test.json"}


@pytest.fixture()
def catalogue(vault: Path, tmp_path: Path, monkeypatch) -> Path:
    monkeypatch.setenv("CATALOGUE_VAULT", str(vault))
    monkeypatch.setenv("CATALOGUE_DATA", str(tmp_path / "data"))
    model = Path(__file__).resolve().parents[3] / "internal docs" / "Note Content Model.md"
    if model.exists():
        target = vault / "internal docs" / model.name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(model.read_text(encoding="utf-8"), encoding="utf-8")
    return vault


class Answering:
    """A model that answers each task plausibly, keyed by the task name.

    Deliberately not a single canned reply: the runner makes fourteen calls per
    candidate and a fake that ignores which one it is answering would let a
    wiring mistake pass.
    """

    def __init__(self, screen: str = "keep", **overrides):
        self.screen = screen
        self.overrides = overrides
        self.tasks: list[str] = []

    def __call__(self, stage, messages, **kwargs):
        self.tasks.append(stage)
        if stage in self.overrides:
            return self.overrides[stage]
        if stage == "screen":
            return json.dumps({"verdict": self.screen,
                               "reason": "the text says nothing either way",
                               "contradicts": []})
        if stage == "queries":
            return json.dumps({"queries": ["durable queue", "job retry"]})
        if stage == "topic":
            return json.dumps({"topic": "Plumbing", "confident": True})
        if stage.startswith("axis:"):
            axis = stage.split(":", 1)[1]
            schema = kwargs.get("json_schema") or {}
            values = schema.get("properties", {}).get("value", {}).get("enum", [])
            return json.dumps({"value": values[0] if values else "",
                               "confident": True, "evidence": "the readme"})
        return json.dumps({"bullets": ["- 210 files under src/", "retries jobs"]})


def fetchers(**overrides) -> populate.Fetchers:
    base = {"search": lambda q: [{"repo_key": "acme/queue"}],
            "repo": lambda k: dict(META),
            "readme": lambda k: README,
            "survey": lambda k: dict(SURVEY)}
    base.update(overrides)
    return populate.Fetchers(**base)


def a_brief() -> brief_mod.Brief:
    return brief_mod.open_brief(
        "network_management", "a queue that resumes after a failed task",
        ["must not require a hosted control plane"], assess_coverage=False)


# ------------------------------------------------------------- one candidate

def test_a_candidate_becomes_a_staged_proposal_and_nothing_else(catalogue):
    model = LocalModel(chat=Answering())
    before = {p.name for p in (catalogue / "01-Resources").glob("*.md")}

    outcome = populate.chart_one("acme/queue", model, fetchers(), vault=catalogue)

    assert outcome["outcome"] == "proposed", outcome
    assert {p.name for p in (catalogue / "01-Resources").glob("*.md")} == before, \
        "an unattended run must not reach the vault"
    proposal = propose_mod.load(outcome["proposal_id"])
    assert proposal.proposed_by == "library-agent"
    assert proposal.evidence["file_count"] == 210


def test_the_machine_fills_data_and_leaves_the_interpretation_empty(catalogue):
    model = LocalModel(chat=Answering())
    outcome = populate.chart_one("acme/queue", model, fetchers(), vault=catalogue)
    proposal = propose_mod.load(outcome["proposal_id"])

    assert set(proposal.sections) <= set(propose_mod.EVIDENCE_SECTIONS)
    assert "Bottom Line" not in proposal.sections
    assert "What It Solves" not in proposal.sections
    assert proposal.axes, "the axes are the data layer and must be filled"


def test_a_fact_is_never_put_to_the_model(catalogue):
    """The finding that reshaped this pipeline.

    Asked for a licence with `declared licence: GPL-3.0` in the text above the
    question, a live 4B model answered `Unknown`. Asked for the ecosystem with
    `main language: TypeScript` in front of it, it answered `Python`. A bigger
    model would have hidden that rather than fixed it: asking is strictly worse
    than reading, because it turns a fact into a guess that reads the same
    downstream.
    """
    chat = Answering()
    populate.chart_one("acme/queue", LocalModel(chat=chat), fetchers(),
                       vault=catalogue)
    asked = {t.split(":", 1)[1] for t in chat.tasks if t.startswith("axis:")}
    leaked = asked & set(derive.DERIVED_AXES)
    assert not leaked, f"readable from evidence and guessed anyway: {leaked}"


def test_a_path_defined_axis_is_never_put_to_a_model(catalogue):
    """`agent_surface` is a ladder of paths. A model reading a README cannot
    know whether `.claude/skills/` exists, so with no listing the axis is left
    empty rather than answered - an answer would be noise wearing the clothes
    of a finding."""
    chat = Answering()
    survey_without_paths = {k: v for k, v in SURVEY.items() if k != "paths"}
    populate.chart_one("acme/queue", LocalModel(chat=chat),
                       fetchers(survey=lambda k: dict(survey_without_paths)),
                       vault=catalogue)
    asked = {t.split(":", 1)[1] for t in chat.tasks if t.startswith("axis:")}
    assert "agent_surface" not in asked


def test_each_remaining_axis_is_asked_once_and_alone(catalogue):
    """Ten enumerations in one reply is where small models drift."""
    chat = Answering()
    populate.chart_one("acme/queue", LocalModel(chat=chat), fetchers(),
                       vault=catalogue)
    axis_calls = [t for t in chat.tasks if t.startswith("axis:")]
    declared = set(content_model.load(catalogue).axis_values)
    assert set(a.split(":", 1)[1] for a in axis_calls) == (
        declared - set(derive.DERIVED_AXES) - set(derive.PATH_DEFINED))
    assert len(set(axis_calls)) == len(axis_calls), "each axis asked once"


def test_the_derived_values_are_the_ones_that_land(catalogue):
    outcome = populate.chart_one("acme/queue", LocalModel(chat=Answering()),
                                 fetchers(), vault=catalogue)
    axes = propose_mod.load(outcome["proposal_id"]).axes
    # MIT from the SPDX field, Python from the language, Active from the push
    # date, CPU_Only because nothing in the evidence mentions a GPU.
    assert axes["license_class"] == "Permissive"
    assert axes["ecosystem"] == "Python"
    assert axes["maturity_stage"] == "Active"
    assert axes["hardware_footprint"] == "CPU_Only"


def test_an_unconfident_answer_is_dropped_rather_than_recorded(catalogue):
    """The schema asks for `confident` so it can be honoured. Taking the value
    anyway would make the flag decoration."""
    hedging = Answering()
    hedging.overrides = {f"axis:{a}": json.dumps(
        {"value": v, "confident": False})
        for a, v in (("domain_primary", "Data"),
                     ("deployment_target", "Server"))}
    outcome = populate.chart_one("acme/queue", LocalModel(chat=hedging),
                                 fetchers(), vault=catalogue)
    axes = propose_mod.load(outcome["proposal_id"]).axes
    assert "domain_primary" not in axes
    assert "deployment_target" not in axes


def test_the_screen_runs_before_the_expensive_calls(catalogue):
    """One small call that removes most candidates. Doing fourteen first and
    screening after would work and would waste a night."""
    chat = Answering(screen="reject")
    outcome = populate.chart_one("acme/queue", LocalModel(chat=chat),
                                 fetchers(), brief=a_brief(), vault=catalogue)
    assert outcome["outcome"] == "screened_out"
    assert chat.tasks == ["screen"], f"work done after a reject: {chat.tasks}"


def test_an_unclear_screen_does_not_reject(catalogue):
    """Most texts will not say either way; treating silence as a reject would
    discard almost everything."""
    outcome = populate.chart_one("acme/queue",
                                 LocalModel(chat=Answering(screen="unclear")),
                                 fetchers(), brief=a_brief(), vault=catalogue)
    assert outcome["outcome"] == "proposed"


def test_something_already_catalogued_is_skipped_and_names_the_note(catalogue):
    outcome = populate.chart_one("example/widget-scheduler",
                                 LocalModel(chat=Answering()), fetchers(),
                                 vault=catalogue)
    assert outcome["outcome"] == "already_catalogued"
    assert outcome["note"] == "widget-scheduler"


def test_a_repository_that_will_not_clone_is_still_charted(catalogue):
    """The note carries less evidence and says so, rather than being lost."""
    def boom(key):
        raise RuntimeError("clone refused")

    log = populate.RunLog()
    outcome = populate.chart_one("acme/queue", LocalModel(chat=Answering()),
                                 fetchers(survey=boom), vault=catalogue, log=log)
    assert outcome["outcome"] == "proposed"
    proposal = propose_mod.load(outcome["proposal_id"])
    assert proposal.evidence["source"] == "github api"
    assert any("no file listing" in n for n in log.notes)


def test_a_repository_that_will_not_fetch_is_an_error_not_a_crash(catalogue):
    def boom(key):
        raise RuntimeError("404")

    log = populate.RunLog()
    outcome = populate.chart_one("acme/gone", LocalModel(chat=Answering()),
                                 fetchers(repo=boom), vault=catalogue, log=log)
    assert outcome["outcome"] == "error"
    assert log.errors == 1


def test_a_model_that_will_not_answer_refuses_that_candidate_only(catalogue):
    log = populate.RunLog()
    outcome = populate.chart_one(
        "acme/queue", LocalModel(chat=Answering(screen='{"nonsense": 1}')),
        fetchers(), brief=a_brief(), vault=catalogue, log=log)
    assert outcome["outcome"] == "refused"
    assert log.refused == 1


# ----------------------------------------------------------------- the runs

def test_a_brief_run_disposes_of_everything_it_saw(catalogue):
    """So a person can close the brief afterwards: the negative results are
    already written, in the model's own words about what the text contradicted.
    """
    record = a_brief()
    log = populate.run_brief(record.brief_id, model=LocalModel(chat=Answering()),
                             fetchers=fetchers(), limit=5, vault=catalogue)
    assert log.proposed == 1

    reloaded = brief_mod.load(record.brief_id)
    assert not reloaded.undisposed, "closing must be possible without more work"
    closed = brief_mod.close(record.brief_id, "one candidate staged")
    assert closed.status == brief_mod.CLOSED


def test_a_rejected_candidate_carries_the_reason_onto_the_brief(catalogue):
    record = a_brief()
    populate.run_brief(record.brief_id,
                       model=LocalModel(chat=Answering(screen="reject")),
                       fetchers=fetchers(), vault=catalogue)
    candidate = brief_mod.load(record.brief_id).candidates[0]
    assert candidate.disposition == brief_mod.REJECTED
    assert candidate.reason, "a rejection with no reason is the lost negative"


def test_the_run_stops_at_the_limit(catalogue):
    many = [{"repo_key": f"acme/thing-{i}"} for i in range(6)]
    record = a_brief()
    log = populate.run_brief(record.brief_id, model=LocalModel(chat=Answering()),
                             fetchers=fetchers(search=lambda q: many),
                             limit=2, vault=catalogue)
    assert log.proposed == 2


def test_the_queue_run_charts_what_someone_reported_using(catalogue):
    enrich.log_use("https://github.com/acme/queue", reported_by="agent",
                   project="network_management", why="used for retries")
    log = populate.run_queue(model=LocalModel(chat=Answering()),
                             fetchers=fetchers(), vault=catalogue)
    assert log.proposed == 1
    entry = enrich.all_entries()[0]
    assert entry.status == enrich.PROPOSED
    assert entry.proposal_id


def test_the_queue_run_needs_no_screen(catalogue):
    """Nobody is asking whether these fit a brief; they are already in use,
    which is the strongest signal the catalogue ever gets."""
    chat = Answering()
    enrich.log_use("acme/queue", reported_by="agent")
    populate.run_queue(model=LocalModel(chat=chat), fetchers=fetchers(),
                       vault=catalogue)
    assert "screen" not in chat.tasks


def test_search_queries_degrade_to_the_need_itself(catalogue):
    """A poor query beats no run."""
    model = LocalModel(chat=Answering(queries="not json at all"))
    assert populate.search_queries("a durable queue", model) == ["a durable queue"]


def test_a_run_log_separates_refusals_from_errors():
    """Three different problems with three different fixes."""
    log = populate.RunLog(considered=5, screened_out=2, proposed=1, refused=1,
                          errors=1)
    text = log.summary()
    assert "model refusals 1" in text and "errors 1" in text


# ------------------------------------------------------------- re-derivation

EVIDENCE = {"survey": "2026-09-09-test.json", "file_count": 120,
            "fetched_at": "2026-09-09T10:00:00Z", "source": "github api"}

def test_a_taxonomy_change_can_be_replayed_over_staging(catalogue):
    """Six languages were added to `ecosystem` on 2026-09-09, and forty
    proposals staged that morning had the axis empty - not for want of
    evidence, but because the enumeration had nowhere to put it.

    Re-derivation costs no model call and no network: it re-reads the metadata
    already on the proposal.
    """
    proposal = propose_mod.propose(
        "acme/rusty", "https://github.com/acme/rusty",
        {"domain_primary": "Infrastructure"}, dict(EVIDENCE),
        metadata={"github_language": "Rust",
                  "github_pushed_at": "2026-08-01T00:00:00Z"})
    assert "ecosystem" not in proposal.axes

    result = propose_mod.rederive(proposal, catalogue)
    assert result["changed"]["ecosystem"] == "Rust"
    assert propose_mod.load(proposal.proposal_id).axes["ecosystem"] == "Rust"


def test_re_derivation_leaves_alone_what_it_cannot_recompute(catalogue):
    """`hardware_footprint` and `security_compliance` need the full evidence
    text, which a proposal does not keep. Recomputing them from nothing would
    return a default that overwrote a better answer."""
    proposal = propose_mod.propose(
        "acme/keepme", "https://github.com/acme/keepme",
        {"hardware_footprint": "Low_VRAM", "security_compliance": "Security_Adjacent"},
        dict(EVIDENCE), metadata={"github_language": "Go"})

    propose_mod.rederive(proposal, catalogue)
    after = propose_mod.load(proposal.proposal_id).axes
    assert after["hardware_footprint"] == "Low_VRAM"
    assert after["security_compliance"] == "Security_Adjacent"
    assert after["ecosystem"] == "Go"


def test_re_derivation_is_idempotent(catalogue):
    proposal = propose_mod.propose(
        "acme/again", "https://github.com/acme/again", {}, dict(EVIDENCE),
        metadata={"github_language": "Java"})
    assert propose_mod.rederive(proposal, catalogue)["changed"]
    assert not propose_mod.rederive(
        propose_mod.load(proposal.proposal_id), catalogue)["changed"]
