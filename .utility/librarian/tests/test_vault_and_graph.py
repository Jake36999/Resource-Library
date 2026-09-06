"""Parsing, access points, the graph, and the surfaces that expose them."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from librarian import access_points as access
from librarian import graph as graph_mod
from librarian import notes as notes_mod
from librarian import policy
from librarian.config import CatalogueConfig


# ------------------------------------------------------------------- parsing

def test_typed_links_keep_their_relation():
    links = notes_mod.extract_links("src", "- [implements_pattern:: [[Pattern - X]]]")
    assert links == [notes_mod.Link("src", "Pattern - X", "implements_pattern")]


def test_untyped_links_are_related_to():
    links = notes_mod.extract_links("src", "see [[Other Note]] for more")
    assert links[0].relation == "related_to"


def test_a_link_inside_backticks_is_syntax_not_an_edge():
    body = "On the child: `[listed_in:: [[parent note]]]`\n\nReal: [[Actual Note]]"
    targets = {link.dst for link in notes_mod.extract_links("src", body)}
    assert targets == {"Actual Note"}


def test_a_link_in_a_fenced_block_is_not_an_edge():
    body = "```\n[[Example Note]]\n```\n\n[[Real Note]]"
    targets = {link.dst for link in notes_mod.extract_links("src", body)}
    assert targets == {"Real Note"}


def test_malformed_frontmatter_is_reported_not_raised():
    frontmatter, body, error = notes_mod.parse_frontmatter(
        '---\nkey: "unclosed\n  nested: [\n---\n\n# Title\n')
    assert error, "a bad block must be reported so integrity can fail on it"
    assert "# Title" in body, "the body must still be readable"


def test_sections_split_on_headings():
    sections = notes_mod.split_sections("# T\n\n## Bottom Line\nOne.\n\n## Next\nTwo.")
    assert sections["Bottom Line"] == "One."
    assert sections["Next"] == "Two."


def test_dot_directories_are_never_indexed(tmp_path: Path):
    (tmp_path / ".pytest_cache").mkdir()
    (tmp_path / ".pytest_cache" / "README.md").write_text("junk", encoding="utf-8")
    (tmp_path / "note.md").write_text("# Note", encoding="utf-8")
    found = [p.name for p in notes_mod.iter_note_paths(tmp_path)]
    assert found == ["note.md"], \
        "a README dropped by a tool is not a note, and indexing it made the index " \
        "look permanently stale"


# ------------------------------------------------------------- access points

DOC = """
# Example

[![build](https://img.shields.io/badge/x.svg)](https://travis-ci.org/x)

The API lives at https://api.example.org/v1/records and returns JSON.
It needs an API key. Anonymous use is capped at 60 requests per hour.

Bulk data: https://data.example.org/dump/all.parquet

Docs: https://docs.example.org/getting-started
"""


def test_only_addresses_are_extracted():
    points = access.extract(DOC, "example/example")
    urls = {p.url for p in points}
    assert "https://api.example.org/v1/records" in urls
    assert "https://data.example.org/dump/all.parquet" in urls
    assert not any("shields.io" in u or "travis" in u for u in urls), \
        "a badge is not an address"
    assert not any("docs.example.org" in u for u in urls), \
        "a documentation homepage is a link, not an access point"


def test_auth_and_rate_limit_are_read_from_the_same_paragraph():
    points = {p.url: p for p in access.extract(DOC, "example/example")}
    api = points["https://api.example.org/v1/records"]
    assert api.auth == "api_key"
    assert api.rate_limit == "60 per hour"

    bulk = points["https://data.example.org/dump/all.parquet"]
    assert bulk.rate_limit == "", \
        "a limit stated about another endpoint must not be attributed to this one"
    assert bulk.auth == "unknown", "unknown is a valid value; a guess is not"


def test_kinds_are_classified():
    kinds = {p.kind for p in access.extract(DOC, "example/example")}
    assert kinds == {"rest_api", "dataset_download"}


def test_storing_twice_preserves_verification_state(tmp_path: Path):
    db = tmp_path / "index.sqlite"
    points = access.extract(DOC, "example/example")
    access.store(points, db)
    access.verify(db, prober=lambda url, timeout: (True, "HEAD 200"))
    before = {r["id"]: (r["reachable"], r["verified_at"]) for r in access.all_points(db)}

    access.store(points, db)               # a re-scan of the same documentation
    after = {r["id"]: (r["reachable"], r["verified_at"]) for r in access.all_points(db)}
    assert before == after, \
        "re-extracting the same address is not evidence that it stopped working"


def test_an_unreachable_endpoint_is_flagged_not_dropped(tmp_path: Path):
    db = tmp_path / "index.sqlite"
    access.store(access.extract(DOC, "example/example"), db)
    report = access.verify(db, prober=lambda url, timeout: (False, "connection refused"))
    rows = access.all_points(db)
    assert report.unreachable == len(rows)
    assert len(rows) == 2, "the rows survive; only their reachable flag changes"
    assert all(r["reachable"] == 0 for r in rows)


def test_find_data_returns_access_points_with_their_verification_state(
        vault: Path, built: Path):
    from librarian import consult

    points = [access.AccessPoint(
        id=access.make_id("example/widget-scheduler", "https://api.example.org/v1/jobs"),
        source="example/widget-scheduler", kind="rest_api",
        url="https://api.example.org/v1/jobs", auth="api_key")]
    access.store(points, built)
    access.verify(built, prober=lambda url, timeout: (True, "HEAD 200"))

    response = consult.find_data("plumbing scheduler jobs", db_path=built)
    addresses = [r for r in response.results if r.kind == "access_point"]
    assert addresses, "a data question should surface the addresses that answer it"
    assert addresses[0].fields["verified_at"]
    assert "verified" in addresses[0].why


# --------------------------------------------------------------------- graph

def test_export_produces_a_graph_of_the_vault_only(built: Path, tmp_path: Path):
    out = graph_mod.export(built, tmp_path / "graphify-out" / "graph.json")
    document = json.loads(out.read_text(encoding="utf-8"))
    assert document["nodes"], "the vault is already a graph; export it, do not build one"
    assert all(node["_origin"] == "vault" for node in document["nodes"])
    assert all(link["confidence"] == "EXTRACTED" for link in document["links"]), \
        "a link written in a note is extracted, not inferred, and must say which"
    assert document["built_at_index"], \
        "a graph that cannot say what state it described is not evidence"


def test_export_drops_edges_to_notes_that_do_not_exist(built: Path, tmp_path: Path,
                                                       vault: Path):
    from librarian import index as index_mod

    target = vault / "01-Resources" / "widget-scheduler.md"
    target.write_text(target.read_text(encoding="utf-8")
                      + "\n- [related_to:: [[Ghost]]]\n", encoding="utf-8")
    index_mod.build(vault, built, rebuild=True)
    document = json.loads(graph_mod.export(built, tmp_path / "g" / "graph.json")
                          .read_text(encoding="utf-8"))
    ids = {node["id"] for node in document["nodes"]}
    assert all(link["target"] in ids for link in document["links"])


def test_centrality_excludes_hubs_and_glossary(built: Path):
    scores = graph_mod.centrality(built)
    assert "Taxonomy Index" not in scores, \
        "every resource links the hub, so counting it ranks the router top"
    assert not any(name.startswith("Glossary - ") for name in scores), \
        "glossary notes are referenced by construction, not by significance"


def test_centrality_ignores_filing_relations(built: Path):
    scores = graph_mod.centrality(built)
    assert "Topic - Plumbing" not in scores or scores["Topic - Plumbing"] < 1.0, \
        "parent_topic means 'filed under', not 'depends on'"


def test_graphify_absent_degrades_to_no_communities(built: Path, tmp_path: Path,
                                                    monkeypatch):
    import shutil
    monkeypatch.setattr(shutil, "which", lambda name: None)
    cfg = CatalogueConfig(graphify_bin=str(tmp_path / "no-such-binary"))
    stats = graph_mod.build(built, cfg, work_dir=tmp_path / "work")
    assert stats.backend == "none"
    assert stats.communities == 0
    assert "degrades" in stats.reason or "not found" in stats.reason
    assert stats.centrality_scored > 0, \
        "centrality is ours and must survive graphify being absent"


def test_communities_are_never_written_into_a_note(built: Path, vault: Path,
                                                   tmp_path: Path, monkeypatch):
    import shutil
    monkeypatch.setattr(shutil, "which", lambda name: None)
    before = {p: p.read_text(encoding="utf-8")
              for p in notes_mod.iter_note_paths(vault)}
    graph_mod.build(built, CatalogueConfig(graphify_bin=str(tmp_path / "none")),
                    work_dir=tmp_path / "work")
    after = {p: p.read_text(encoding="utf-8")
             for p in notes_mod.iter_note_paths(vault)}
    assert before == after, \
        "GRAPH_IS_DERIVED: a community assignment in frontmatter would be schema " \
        "drift, and would let the graph start authoring the taxonomy"


def test_disagreements_are_a_report_and_change_nothing(built: Path):
    report = graph_mod.disagreements(built)
    assert isinstance(report, list)
    for item in report:
        assert item.topic and item.members_in_topic >= 0


def test_measured_gap_fit_is_off_unless_asked(built: Path):
    assert graph_mod.measured_gap_fit(built, CatalogueConfig()) == {}, \
        "swapping a ranking signal's basis must be measured before it is trusted"


# -------------------------------------------------------------------- policy

def test_an_unregistered_action_is_refused_by_name():
    with pytest.raises(policy.PolicyError) as caught:
        policy.check_action("write_a_helper_script")
    assert caught.value.code == policy.CLOSED_ACTION_REGISTRY
    assert "write_a_helper_script" in caught.value.message
    assert "report the gap" in caught.value.message, \
        "a refusal must produce a decision point, not a dead end"


def test_the_registry_cannot_be_widened_at_runtime():
    assert isinstance(policy.REGISTERED_ACTIONS, frozenset)
    with pytest.raises(AttributeError):
        policy.REGISTERED_ACTIONS.add("anything")


def test_a_sweep_cannot_reach_a_workbench_action():
    with pytest.raises(policy.PolicyError) as caught:
        policy.check_sweep_action("workbench_open")
    assert caught.value.code == policy.EXECUTION_SANDBOX_ONLY


def test_evidence_required_accepts_an_explicit_unknown():
    policy.check_evidence("license_class", "Unknown", source=None)
    with pytest.raises(policy.PolicyError) as caught:
        policy.check_evidence("license_class", "Permissive", source=None)
    assert caught.value.code == policy.EVIDENCE_REQUIRED


def test_clone_refuses_anything_that_is_not_a_repo_key_or_https_url():
    from librarian import clone

    assert clone.normalise_url("owner/name") == "https://github.com/owner/name.git"
    for bad in ("; rm -rf /", "file:///etc/passwd", "--upload-pack=evil", ""):
        with pytest.raises(clone.CloneRefused):
            clone.normalise_url(bad)


# ----------------------------------------------------------------- mcp surface

def test_the_mcp_surface_exposes_exactly_one_write():
    from librarian import mcp_server

    assert mcp_server.WRITE_TOOLS == {"record_application"}
    assert "index_build" not in mcp_server.TOOLS
    assert not any(name.startswith("workbench") for name in mcp_server.TOOLS), \
        "an agent must have no reachable path to Mode D"
    assert set(mcp_server.TOOLS) - mcp_server.WRITE_TOOLS == mcp_server.read_only_tools()


def test_mcp_tools_return_the_response_envelope(built: Path, monkeypatch):
    from librarian import consult, mcp_server

    monkeypatch.setattr(consult, "orient",
                        lambda q, limit=10, **kw: consult.Response(intent="orient"))
    payload = mcp_server.tool_orient("anything")
    assert set(payload) >= {"intent", "results", "filtered_out", "tier_reached",
                            "next_step", "partial", "notes"}


def test_mcp_search_reports_invalid_params_with_the_schema(monkeypatch, vault: Path):
    from librarian import mcp_server

    payload = mcp_server.tool_search({"intent": "nonsense", "terms": ["x"]})
    assert payload["error"] == "invalid_params"
    assert payload["schema"]["$id"] == "catalogue/search_params/v1"


# ------------------------------------------------------------------- evalset

def test_the_eval_set_points_only_at_notes_that_exist():
    from librarian import evalset
    from librarian.config import VAULT_ROOT

    questions, k = evalset.load()
    assert len(questions) >= 20, "twenty questions with known answers is the contract"
    assert k == 5
    names = {p.stem for p in notes_mod.iter_note_paths(VAULT_ROOT)}
    missing = {expected for question in questions for expected in question.expects
               if expected not in names}
    assert not missing, \
        f"an eval question whose answer left the vault must be re-pointed: {missing}"


def test_community_assignments_are_reproducible(built: Path, tmp_path: Path):
    """Deleting the index and rebuilding must reproduce the same assignments.

    Clustering runs with `--no-label`, which skips graphify's LLM community
    naming. That is not a preference: a model in this path would make the
    derived store non-reproducible, and a derived store that cannot be
    reproduced is not disposable.
    """
    ok, _ = graph_mod.graphify_available()
    if not ok:
        pytest.skip("graphify is not installed on this host")

    graph_mod.build(built, work_dir=tmp_path / "one")
    first = graph_mod.communities(built)
    graph_mod.build(built, work_dir=tmp_path / "two")
    second = graph_mod.communities(built)
    assert first == second and first, \
        "the same graph must cluster the same way, or the index is not disposable"
