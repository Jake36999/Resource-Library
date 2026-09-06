"""The queue carries the resumability guarantee, so interruption and lease
recovery are tested rather than assumed."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import pytest

from scout import db


@pytest.fixture()
def conn(tmp_path):
    path = tmp_path / "queue.sqlite"
    db.init(path)
    with db.connect(path) as connection:
        yield connection


def add(conn, url, **kw):
    return db.add_candidate(conn, url=url, **kw)


def test_duplicate_url_becomes_corroboration_not_a_second_row(conn):
    first, created_a = add(conn, "https://github.com/a/b")
    second, created_b = add(conn, "https://github.com/a/b")
    assert created_a is True and created_b is False
    assert first == second
    row = conn.execute("SELECT corroboration FROM scout_queue WHERE id=?", (first,)).fetchone()
    assert row["corroboration"] == 2, "rediscovery is evidence, not noise"


def test_url_normalisation_catches_trivial_variants(conn):
    add(conn, "https://github.com/a/b")
    for variant in ("http://github.com/a/b", "https://www.github.com/a/b",
                    "https://github.com/a/b/", "https://github.com/a/b.git"):
        _, created = add(conn, variant)
        assert created is False, f"{variant} should match the canonical URL"
    assert len(db.fetch_state(conn, "discovered")) == 1


def test_claim_takes_highest_score_first(conn):
    for name, score in (("low", 10.0), ("high", 90.0), ("mid", 50.0)):
        row_id, _ = add(conn, f"https://github.com/x/{name}")
        db.update(conn, row_id, state="queued", score=score, cohort_id="C1")
    claimed = db.claim_next(conn, "owner-1", 600, "C1")
    assert claimed["url"].endswith("high")
    assert claimed["state"] == "deep_dive"


def test_interruption_leaves_completed_work_and_resumes_at_next_best(conn):
    for name, score in (("a", 90.0), ("b", 80.0), ("c", 70.0)):
        row_id, _ = add(conn, f"https://github.com/x/{name}")
        db.update(conn, row_id, state="queued", score=score, cohort_id="C1")

    first = db.claim_next(conn, "run-1", 600, "C1")
    db.release(conn, first["id"], "catalogued")
    second = db.claim_next(conn, "run-1", 600, "C1")
    # Simulate a crash: the second item stays leased and unfinished.

    resumed = db.claim_next(conn, "run-2", 600, "C1")
    assert resumed["url"].endswith("c"), "a live lease must not be stolen"
    finished = conn.execute(
        "SELECT COUNT(*) n FROM scout_queue WHERE state='catalogued'").fetchone()
    assert finished["n"] == 1, "completed work survives the interruption"
    assert second["url"].endswith("b")


def test_expired_lease_is_reclaimable(conn):
    row_id, _ = add(conn, "https://github.com/x/stuck")
    db.update(conn, row_id, state="queued", score=50.0, cohort_id="C1")
    db.claim_next(conn, "dead-run", 600, "C1")
    stale = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(timespec="seconds")
    db.update(conn, row_id, lease_expires_at=stale)

    reclaimed = db.claim_next(conn, "new-run", 600, "C1")
    assert reclaimed is not None, "an abandoned lease must not deadlock the queue"
    assert reclaimed["lease_owner"] == "new-run"
    assert reclaimed["attempts"] == 2


def test_claim_returns_none_when_queue_drained(conn):
    assert db.claim_next(conn, "owner", 600, "C1") is None


def test_freeze_takes_top_n_and_leaves_the_rest(conn):
    for index in range(10):
        row_id, _ = add(conn, f"https://github.com/x/r{index}")
        db.update(conn, row_id, state="ranked", score=float(index))
    frozen = db.freeze_cohort(conn, "C1", 4)
    assert len(frozen) == 4
    assert [r["score"] for r in frozen] == [9.0, 8.0, 7.0, 6.0]
    assert len(db.fetch_state(conn, "ranked")) == 6, "the rest wait for the next cohort"


def test_signals_are_stored_and_replaceable(conn):
    row_id, _ = add(conn, "https://github.com/x/y")
    db.record_signals(conn, row_id, [
        {"signal": "gap_fit", "value": 1.0, "weight": 30.0, "detail": "empty topic"}])
    db.record_signals(conn, row_id, [
        {"signal": "gap_fit", "value": 0.5, "weight": 30.0, "detail": "half full"}])
    rows = db.signals_for(conn, row_id)
    assert len(rows) == 1 and rows[0]["value"] == 0.5


def test_counts_reports_every_state(conn):
    row_id, _ = add(conn, "https://github.com/x/y")
    db.update(conn, row_id, state="ranked")
    assert db.counts(conn) == {"ranked": 1}
