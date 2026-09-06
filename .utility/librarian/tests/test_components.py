"""The data layer holds facts, and the facts must survive two survey formats.

The defect these were written against was silent: the 2026-09-03 survey stores
a *truncated* path sample under `tests` and the real count under a companion
key `tests__count`, so taking the sample's length recorded ten tests for a
repository with 847 - for 64 of the 113 sources, with nothing to notice.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from librarian import components


OLD_FORMAT = {
    "widget - scheduler": {
        "repo": "widget/scheduler",
        "note": "widget - scheduler",
        "files": 900,
        "top": ["src (500)", "test (390)", "(root) (10)"],
        "second": {"src": ["core (300)", "cli (200)"]},
        "extensions": [".py (700)", ".md (12)"],
        "root_files": ["README.md", "LICENSE"],
        "signals": {
            "tests": ["test/a.py", "test/b.py"],
            "tests__count": ["847"],
            "grammars": ["src/core/grammar.lark"],
            "grammars__count": ["1"],
        },
    }
}

NEW_FORMAT = {
    "gadget/queue": {
        "repo": "gadget/queue",
        "meta": {"full_name": "gadget/queue", "language": "Rust", "spdx": "MIT",
                 "stars": 42, "archived": True, "pushed": "2025-01-02T00:00:00Z"},
        "files": 120,
        "top": ["src (100)", "(root) (20)"],
        "second": {},
        "extensions": [".rs (100)"],
        "root_files": ["Cargo.toml"],
        "signals": {"tests": {"n": 55, "sample": ["src/lib_test.rs"]}},
    }
}


@pytest.fixture()
def built(tmp_path: Path) -> Path:
    surveys = tmp_path / "surveys"
    surveys.mkdir()
    (surveys / "2026-09-03-cohort.json").write_text(
        json.dumps(OLD_FORMAT), encoding="utf-8")
    (surveys / "2026-09-04-cohort.json").write_text(
        json.dumps(NEW_FORMAT), encoding="utf-8")
    db = tmp_path / "components.sqlite"
    components.build(surveys, db)
    return db


def test_a_truncated_sample_does_not_become_the_count(built: Path):
    """The whole reason this module reads a companion key."""
    rows = {r["repo_key"]: r for r in components.sources_with("tests", db_path=built)}
    assert rows["widget/scheduler"]["files"] == 847, \
        "the sample holds two paths; the count is 847 and lives beside it"
    assert rows["gadget/queue"]["files"] == 55


def test_the_count_companion_is_not_itself_a_signal(built: Path):
    vocab = components.vocabulary(db_path=built)
    names = {name for name, _ in vocab["signals"]}
    assert "tests" in names
    assert not any(n.endswith("__count") for n in names), \
        "`tests__count` is how a count was stored, not a kind of material"


def test_both_survey_formats_land_in_one_shape(built: Path):
    old = components.profile("widget/scheduler", db_path=built)
    new = components.profile("gadget/queue", db_path=built)
    assert old["file_count"] == 900 and new["file_count"] == 120
    assert old["note"] == "widget - scheduler"
    assert new["language"] == "Rust" and new["archived"] == 1
    assert {d["name"] for d in old["directories"] if d["parent"] == "src"} == {"core", "cli"}


def test_a_sample_path_is_never_mistaken_for_a_complete_list(built: Path):
    """`signal_path` is a sample by construction. Counting its rows and
    reporting that as the total is the same defect in a different place."""
    conn = components.connect(built)
    try:
        sampled = conn.execute(
            "SELECT COUNT(*) FROM signal_path WHERE repo_key='widget/scheduler' "
            "AND signal='tests'").fetchone()[0]
        recorded = conn.execute(
            "SELECT files FROM signal WHERE repo_key='widget/scheduler' "
            "AND signal='tests'").fetchone()[0]
    finally:
        conn.close()
    assert sampled == 2 and recorded == 847


def test_the_store_is_disposable(built: Path):
    """Same bargain as `catalogue_index.sqlite`: delete it, rebuild it, lose
    nothing. The surveys are the durable artefact."""
    before = components.profile("widget/scheduler", db_path=built)
    built.unlink()
    components.build(built.parent / "surveys", built)
    assert components.profile("widget/scheduler", db_path=built) == before


def test_the_surveys_are_never_rewritten(built: Path):
    """Two incompatible formats are absorbed on read. A record that gets
    normalised in place stops being a record of what was fetched."""
    raw = json.loads((built.parent / "surveys" / "2026-09-03-cohort.json")
                     .read_text(encoding="utf-8"))
    assert raw == OLD_FORMAT


def test_vocabulary_answers_what_can_be_filtered_without_the_schema(built: Path):
    """The first call an unfamiliar agent should be able to make."""
    vocab = components.vocabulary(db_path=built)
    assert set(vocab) == {"signals", "extensions", "languages", "cohorts"}
    assert dict(vocab["cohorts"]) == {"2026-09-03": 1, "2026-09-04": 1}


def test_an_unknown_source_returns_nothing_rather_than_raising(built: Path):
    assert components.profile("nobody/here", db_path=built) == {}
    assert components.sources_with("no_such_signal", db_path=built) == []


def test_status_reports_absence_instead_of_failing(tmp_path: Path):
    state = components.status(tmp_path / "missing.sqlite")
    assert state["present"] is False and "missing.sqlite" in state["path"]
