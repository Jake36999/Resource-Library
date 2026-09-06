"""Community reports - the one idea taken from graphrag.

A report is what lets the catalogue answer *what has this become*, which no
single note contains. The properties worth pinning are that it is derived and
disposable, that every clause traces to a link the index already holds, and
that it stays advisory: an observation written down may not reassign a topic.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from librarian import consult
from librarian import graph as graph_mod
from librarian import index as index_mod


def _assign(db: Path, groups: dict[int, list[str]]) -> None:
    """Stand in for graphify. The clustering is not what these tests are about,
    and requiring the binary would make them fail on a machine without it."""
    conn = index_mod.connect(db)
    try:
        index_mod.init(conn)
        conn.execute("DELETE FROM note_community")
        for community, members in groups.items():
            for rank, name in enumerate(members):
                conn.execute(
                    "INSERT OR REPLACE INTO note_community"
                    "(note, community, label, centrality) VALUES(?,?,?,?)",
                    (name, community, "", 1.0 - rank * 0.1))
        conn.commit()
    finally:
        conn.close()


def _names(db: Path, layer: str = "resource") -> list[str]:
    conn = index_mod.connect(db)
    try:
        return [r["name"] for r in conn.execute(
            "SELECT name FROM note WHERE layer = ? ORDER BY name", (layer,))]
    finally:
        conn.close()


def test_no_communities_means_no_reports_rather_than_an_error(built: Path):
    """R8. graphify absent degrades to nothing to summarise, never to a raise."""
    conn = index_mod.connect(built)
    try:
        conn.execute("DELETE FROM note_community")
        conn.commit()
    finally:
        conn.close()
    assert graph_mod.report(built) == []
    assert graph_mod.reports(built) == []


def test_a_report_summarises_from_facts_the_index_holds(built: Path):
    members = _names(built)
    _assign(built, {0: members})
    entries = graph_mod.report(built, min_members=1)
    assert entries, "a community with members must produce a report"

    entry = entries[0]
    assert entry.size == len(members)
    assert str(len(members)) in entry.summary
    assert entry.members[0] in entry.summary, \
        "the most connected member is named, so the summary can be checked"


def test_a_tiny_community_is_not_summarised(built: Path):
    """Below a handful of members a 'community' is an accident of layout, and a
    report on it would be noise wearing the same clothes as a finding."""
    members = _names(built)
    _assign(built, {0: members[:1]})
    assert graph_mod.report(built, min_members=3) == []


def test_a_report_says_when_a_community_only_restates_a_topic(built: Path):
    """The distinction that decides whether a report is worth reading."""
    conn = index_mod.connect(built)
    try:
        rows = conn.execute(
            "SELECT name, primary_topic FROM resource_facet "
            "WHERE primary_topic IS NOT NULL AND primary_topic != ''").fetchall()
    finally:
        conn.close()
    by_topic: dict[str, list[str]] = {}
    for row in rows:
        by_topic.setdefault(row["primary_topic"], []).append(row["name"])
    single = max(by_topic.values(), key=len)

    _assign(built, {0: single})
    entry = graph_mod.report(built, min_members=1)[0]
    assert not entry.crosses_topics
    assert "restates a topic" in entry.summary


def test_reports_are_derived_and_disposable(built: Path):
    """Deleting them loses nothing: `report()` rebuilds from the index, which
    rebuilds from the notes. Markdown stays truth."""
    members = _names(built)
    _assign(built, {0: members})
    first = graph_mod.report(built, min_members=1)

    conn = index_mod.connect(built)
    try:
        conn.execute("DELETE FROM community_report")
        conn.commit()
    finally:
        conn.close()
    assert graph_mod.reports(built) == []

    second = graph_mod.report(built, min_members=1)
    assert [e.summary for e in second] == [e.summary for e in first]


def test_nothing_is_written_to_a_note(built: Path, vault: Path):
    """R2. A community lives in the index and never in frontmatter."""
    members = _names(built)
    before = {p: p.read_text(encoding="utf-8")
              for p in (vault / "01-Resources").glob("*.md")}
    _assign(built, {0: members})
    graph_mod.report(built, min_members=1)
    after = {p: p.read_text(encoding="utf-8")
             for p in (vault / "01-Resources").glob("*.md")}
    assert before == after


def test_orient_offers_a_crossing_community_and_not_a_single_topic_one(built: Path):
    """`orient` asks what is here. A grouping nobody assigned belongs in that
    answer; one that mirrors a topic does not, because the topic index is the
    better answer for it."""
    conn = index_mod.connect(built)
    try:
        rows = conn.execute(
            "SELECT name, primary_topic FROM resource_facet").fetchall()
    finally:
        conn.close()
    topics = {r["primary_topic"] for r in rows if r["primary_topic"]}
    if len(topics) < 2:
        return                                  # fixture has nothing to cross

    crossing = [r["name"] for r in rows if r["primary_topic"]][:4]
    _assign(built, {0: crossing})
    graph_mod.report(built, min_members=1)

    response = consult.orient("plumbing scheduler queue", db_path=built)
    communities = [r for r in response.results if r.kind == "community"]
    for result in communities:
        assert len([t for t in result.fields["topics"] if t]) > 1, \
            "a community confined to one topic must not be offered"
        assert result.why, "every result explains itself, communities included"
