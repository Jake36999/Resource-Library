"""The queue: the cheapest contribution on the surface.

The design claim is that logging a source costs an agent nothing, so these
tests are mostly about *not refusing* things a busy agent will actually send —
a URL, a duplicate, a name it half-remembers — while still refusing what cannot
be fetched later.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from librarian import consult, enrich, policy


@pytest.fixture()
def catalogue(vault: Path, tmp_path: Path, monkeypatch) -> Path:
    monkeypatch.setenv("CATALOGUE_VAULT", str(vault))
    monkeypatch.setenv("CATALOGUE_DATA", str(tmp_path / "data"))
    return vault


# ------------------------------------------------------------- what it takes

@pytest.mark.parametrize("given", [
    "acme/queue",
    "https://github.com/acme/queue",
    "https://github.com/acme/queue/",
    "http://github.com/acme/queue.git",
    "github.com/acme/queue/tree/main/src",
])
def test_it_accepts_what_an_agent_actually_has_to_hand(given):
    """A project agent mid-task has a URL in its context, not a canonical key.
    Refusing it would mean stopping to transform one, and the whole design of
    this path is that logging costs nothing."""
    assert enrich.normalise(given) == "acme/queue"


@pytest.mark.parametrize("given", ["", "queue", "some notes about a queue",
                                   "https://example.com/thing"])
def test_it_refuses_what_could_never_be_fetched(given):
    """Queueing something nobody can act on is worse than not queueing."""
    assert enrich.normalise(given) == ""


def test_a_junk_key_is_refused_with_the_reason(catalogue):
    with pytest.raises(ValueError) as caught:
        enrich.log_use("just some words", reported_by="agent")
    assert "owner/repo" in str(caught.value)


# ------------------------------------------------------------ the three answers

def test_something_already_catalogued_answers_with_the_note(catalogue):
    """The cheapest possible answer to any research request: we have this."""
    result = enrich.log_use("example/widget-scheduler", reported_by="agent")
    assert result["status"] == enrich.CATALOGUED
    assert result["note"] == "widget-scheduler"
    assert not enrich.all_entries(), "nothing to queue; it is already here"


def test_something_new_is_queued_and_claims_nothing(catalogue):
    result = enrich.log_use("acme/queue", reported_by="agent",
                            project="network_management", why="retry semantics")
    assert result["status"] == enrich.QUEUED
    entry = enrich.load(result["entry_id"])
    assert entry.why == "retry semantics"
    assert entry.status == enrich.QUEUED


def test_logging_twice_counts_a_sighting_rather_than_duplicating(catalogue):
    """Something three projects reached for independently should be charted
    before something nobody repeated."""
    enrich.log_use("acme/queue", reported_by="agent-a", project="one")
    again = enrich.log_use("acme/queue", reported_by="agent-b", project="two")
    assert again["status"] == "seen_again"
    assert again["sightings"] == 2
    assert len(enrich.all_entries()) == 1


def test_the_first_why_is_kept_when_a_later_sighting_has_none(catalogue):
    enrich.log_use("acme/queue", reported_by="a", why="retry semantics")
    enrich.log_use("acme/queue", reported_by="b")
    assert enrich.find("acme/queue").why == "retry semantics"


# ------------------------------------------------------------- the lifecycle

def test_skipping_needs_a_reason(catalogue):
    """Same rule as a rejected candidate: it is what stops the next pass
    fetching this again."""
    result = enrich.log_use("acme/queue", reported_by="agent")
    with pytest.raises(policy.PolicyError) as caught:
        enrich.resolve(result["entry_id"], enrich.SKIPPED)
    assert caught.value.code == policy.DISPOSITION_REQUIRED

    entry = enrich.resolve(result["entry_id"], enrich.SKIPPED,
                           resolution="archived since 2019")
    assert entry.resolution == "archived since 2019"


def test_a_resolved_entry_cannot_be_reclaimed(catalogue):
    result = enrich.log_use("acme/queue", reported_by="agent")
    enrich.resolve(result["entry_id"], enrich.SKIPPED, resolution="no")
    with pytest.raises(policy.PolicyError):
        enrich.claim(result["entry_id"], "library-agent")


# ------------------------------------------- the connection to applications

def test_an_application_record_queues_the_sources_it_names(catalogue):
    """The moment a source proved useful enough to write a record about is the
    moment it is worth charting, and the agent has already typed the name."""
    result = consult.record_application({
        "project": "network_management", "stage": "delivery",
        "outcome": "the retry loop stopped losing jobs",
        "resources_used": ["acme/queue", "example/widget-scheduler"],
        "sections": {
            "What Was Needed": "a queue that resumes after a failure",
            "What Was Found And Taken": "acme/queue's retry table",
            "What It Replaced": "a shell loop",
            "What The Catalogue Should Learn": "retry semantics beat features",
        }}, vault=catalogue)

    queued = [q["repo_key"] for q in result["queued_for_enrichment"]]
    assert queued == ["acme/queue"], \
        "the uncatalogued one is queued; the catalogued one is not"
    assert enrich.find("acme/queue").project == "network_management"


def test_a_note_named_by_title_is_not_mistaken_for_a_repository(catalogue):
    """Application records name resources by note title. A title is not a repo
    key, and treating one as a failure would make every record noisy."""
    result = consult.record_application({
        "project": "x", "stage": "delivery", "outcome": "worked",
        "resources_used": ["widget-scheduler"],
        "sections": {"What Was Needed": "a", "What Was Found And Taken": "b",
                     "What It Replaced": "c",
                     "What The Catalogue Should Learn": "d"}},
        vault=catalogue)
    assert result["queued_for_enrichment"] == []


def test_recording_an_application_still_succeeds_if_queueing_fails(catalogue,
                                                                  monkeypatch):
    """The record is the authoritative write. A queue that cannot be reached
    must not lose it."""
    def boom(*args, **kwargs):
        raise RuntimeError("disk full")

    monkeypatch.setattr(enrich, "queue_unknown", boom)
    result = consult.record_application({
        "project": "y", "stage": "delivery", "outcome": "worked",
        "resources_used": ["acme/queue"],
        "sections": {"What Was Needed": "a", "What Was Found And Taken": "b",
                     "What It Replaced": "c",
                     "What The Catalogue Should Learn": "d"}},
        vault=catalogue)
    assert Path(result["path"]).exists()
    assert result["queued_for_enrichment"] == []
