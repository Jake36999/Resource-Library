"""The services added on 2026-09-04, and the defects each was built against.

Every test here names a failure that was measured rather than imagined. Three
of them lock in *negative* results — things that were built, measured, found
worse, and turned off — because a rejected option nobody can re-run is folklore.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from librarian import coverage, duplicates, freshness, provenance, usesignal
from librarian import queryunderstanding as qu


# ------------------------------------------------------------------- freshness

def test_the_same_non_answer_spelled_twice_is_not_a_change():
    """`UNKNOWN -> NOASSERTION` was reported as a licence divergence on the
    first real run. Both mean *we could not tell*."""
    claim = {"repo_key": "a/b", "spdx": "UNKNOWN", "maturity_stage": "Active"}
    live = {"full_name": "a/b", "license": {"spdx_id": "NOASSERTION"}}
    assert [d for d in freshness.compare(claim, live)
            if d["kind"].startswith("licence")] == []


def test_a_licence_that_was_never_captured_is_not_a_licence_that_changed():
    """The distinction decides what anybody does about it, and the first real
    run found six of the second kind on the 2026-08-31 cohort."""
    claim = {"repo_key": "a/b", "spdx": "UNKNOWN", "maturity_stage": "Active"}
    live = {"full_name": "a/b", "license": {"spdx_id": "MIT"}}
    kinds = {d["kind"] for d in freshness.compare(claim, live)}
    assert "licence_undercaptured" in kinds
    assert "licence_changed" not in kinds

    relicensed = {"repo_key": "a/b", "spdx": "MIT", "maturity_stage": "Active"}
    live_gpl = {"full_name": "a/b", "license": {"spdx_id": "GPL-3.0"}}
    assert "licence_changed" in {d["kind"] for d in freshness.compare(relicensed, live_gpl)}


def test_an_archived_repository_the_note_calls_maintained_warns():
    claim = {"repo_key": "a/b", "spdx": "MIT", "maturity_stage": "Production_Ready"}
    live = {"full_name": "a/b", "archived": True, "license": {"spdx_id": "MIT"}}
    kinds = {d["kind"] for d in freshness.compare(claim, live)}
    assert "archived" in kinds and "archived" in freshness.WARNING_KINDS


def test_activity_and_popularity_are_recorded_without_warning():
    """A catalogue that shouts about star counts trains its reader to ignore it."""
    claim = {"repo_key": "a/b", "spdx": "MIT", "maturity_stage": "Active",
             "pushed_at": "2026-01-01T00:00:00Z", "stars": 100}
    live = {"full_name": "a/b", "license": {"spdx_id": "MIT"},
            "pushed_at": "2026-09-01T00:00:00Z", "stargazers_count": 400}
    kinds = {d["kind"] for d in freshness.compare(claim, live)}
    assert kinds == {"pushed", "stars"}
    assert not any(k in freshness.WARNING_KINDS for k in kinds)


def test_an_unreachable_repository_is_the_loudest_result():
    assert freshness.compare({"repo_key": "a/b"}, {})[0]["kind"] == "gone"


# ---------------------------------------------------------- query understanding

def test_the_segmenter_excludes_what_a_request_rules_out():
    query = ("A service reads a large configuration file and must reject a "
             "malformed one. The storage engine and the query layer are out of "
             "scope.")
    seg = qu.segment(query)
    assert {"storage", "engine", "layer"} <= set(seg.excluded)
    assert {"configuration", "malformed", "reject"} <= set(seg.ask)


def test_a_word_used_positively_is_never_excluded():
    """Without this, a scope clause mentioning `configuration` would delete it
    from a query that is *about* configuration."""
    query = ("Validate the configuration at startup. The configuration parsed "
             "cleanly is out of scope.")
    seg = qu.segment(query)
    assert "configuration" in seg.ask
    assert "configuration" not in seg.excluded


def test_a_short_query_is_left_entirely_alone():
    """The twenty eval questions contain no scope clauses. If segmentation
    moves them it is doing something other than what it claims."""
    seg = qu.segment("how is backpressure handled")
    assert seg.excluded == () and seg.context == ()


def test_the_segmenter_tokenises_exactly_as_the_search_does():
    """A private regex here produced `scope` while the search produced
    `scope.`, so the excluded term never matched the term being excluded."""
    from librarian.consult import terms_from

    text = "The query layer is out of scope."
    assert set(qu.segment(text).excluded) <= {t.lower() for t in terms_from(text)}


def test_segmentation_stays_off_because_it_was_measured_worse():
    """Both remedies were implemented and both lose: dropping excluded terms
    gives 5 misses against 4, weighting gives 7. The module is kept so a
    model-backed version can be compared on the same harness."""
    from librarian.config import CatalogueConfig

    cfg = CatalogueConfig.load()
    assert cfg.query_segmentation is False
    assert cfg.coverage_order == "bm25"


# -------------------------------------------------------------------- coverage

def test_a_question_from_outside_the_collection_is_refused(vault: Path):
    from librarian import consult, index

    db = vault / "cov.sqlite"
    index.build(vault, db)
    query = "best technique for laminating croissant dough overnight"
    response = consult.find_donor(query, {}, 5, db_path=db)
    verdict = coverage.assess(query, response, db_path=db)
    assert verdict.level == coverage.UNCOVERED
    assert not verdict.trustworthy


def test_thin_means_no_opinion_rather_than_probably_fine():
    """Five overlap-derived signals were measured and none separates a question
    the catalogue answers from one it merely has vocabulary for. `thin` is the
    honest verdict for everything in between and must not read as approval."""
    verdict = coverage.Verdict(coverage.THIN, 0.2, 3, ("a", "b"), ("a",), "x")
    assert verdict.trustworthy is False
    assert "leads, not answers" in verdict.sentence()


# ------------------------------------------------------------------ duplicates

def test_the_duplicate_floor_is_inside_the_observed_range():
    """The first version set the floor at 0.18 when the maximum similarity in
    the corpus was 0.144 - an unfireable check reporting "none found", which is
    worse than no check."""
    spread = duplicates.distribution()
    if not spread:
        pytest.skip("no corpus available")
    assert spread["max"] > duplicates.SEMANTIC_FLOOR, \
        "a floor above the maximum can never fire"
    assert duplicates.SEMANTIC_FLOOR > spread["median"]


def test_a_pair_is_ranked_on_the_signal_its_docstring_trusts():
    """A weighted sum was tried and was wrong on the arithmetic: semantic
    Jaccard tops out near 0.14 while structural runs to 1.0, so a composite
    that *said* semantic mattered most ranked by directory shape."""
    pair = duplicates.Pair("a", "b", structural=1.0, semantic=0.12,
                           declared=1.0, shared_signals=(), shared_terms=())
    assert pair.score == 0.12


def test_structure_alone_does_not_make_a_duplicate():
    """Every Python project has tests. Corroboration is required, not sufficient."""
    pair = duplicates.Pair("a", "b", structural=1.0, semantic=0.0,
                           declared=1.0, shared_signals=(), shared_terms=())
    assert pair.corroborated and pair.score == 0.0


# ------------------------------------------------------------------ use signal

def test_the_use_signal_refuses_to_rank_on_nothing(tmp_path: Path):
    """Fitting a ranking signal to an empty table produces a knob that looks
    principled and encodes nothing."""
    db = tmp_path / "components.sqlite"
    usesignal.record("a query", "some - note", "taken", db_path=db)
    state = usesignal.readiness(db)
    assert state.events == 1 and not state.ready
    assert "not enough to rank on" in state.sentence()


def test_taking_a_source_counts_for_more_than_opening_it(tmp_path: Path):
    db = tmp_path / "components.sqlite"
    usesignal.record("q", "n1", "taken", db_path=db)
    usesignal.record("q", "n2", "opened", db_path=db)
    usesignal.record("q", "n3", "irrelevant", db_path=db)
    scores = usesignal.weights(db)
    assert scores["n1"] > scores["n2"] > 0 > scores["n3"]


def test_an_unknown_verdict_is_refused(tmp_path: Path):
    with pytest.raises(ValueError):
        usesignal.record("q", "n", "brilliant", db_path=tmp_path / "c.sqlite")


# ------------------------------------------------------------------ provenance

def test_a_hedged_or_borrowed_number_is_unsupported_not_contradicted():
    """`Roughly 150 entries` counts README lines, and `904 schemas` is a fact
    about a different repository. Reporting either as a defect would teach
    authors to stop being specific."""
    assert provenance.UNSUPPORTED != provenance.CONTRADICTED


def test_the_claim_pattern_ignores_bare_numbers():
    """A number in prose is not a claim about a tree."""
    assert not provenance.CLAIM.search("supports Java 1 to 25")
    assert provenance.CLAIM.search("1,833 test paths")


def test_the_catalogue_can_account_for_its_own_structural_claims():
    """The whole point of applying the lineage topic to itself."""
    claims = provenance.check()
    if not claims:
        pytest.skip("no component store built")
    counts = provenance.summarise(claims)
    total = sum(counts.values())
    assert counts[provenance.SUPPORTED] / total > 0.9
    # Not zero. A contradiction appears whenever a surveyed repository changes
    # between the survey a note was written from and the current one - two
    # showed up in `llama_index` within two days of re-surveying it. That is
    # the check working. What must stay rare is the *rate*.
    assert counts[provenance.CONTRADICTED] / total < 0.05


# ------------------------------------------------------- component retrieval

def test_a_component_match_is_whole_segment_not_substring():
    """Shape 2, reintroduced and caught. The first version used `LIKE '%side%'`
    and returned `app/sidekiq` and `components/SideNav` for a query about
    ranking configurations *side by side*. This system already fixed that once
    for `interface_protocol: "REST"` matching *the rest of the system*, and
    `F:\Mark-XLVIII-main` documents fixing it independently in its own
    capability search - two systems, same defect, same remedy."""
    from librarian.consult import _matched_terms_bounded

    assert _matched_terms_bounded("sidekiq", ["side"]) == []
    assert _matched_terms_bounded("SideNav", ["side"]) == []
    assert _matched_terms_bounded("side by side", ["side"]) == ["side"]


def test_a_ubiquitous_directory_name_names_no_source():
    """`test` is a directory in nearly a third of surveyed repositories, so
    matching it picks out nothing. Same reasoning as `SELECTIVITY_CEILING`, one
    grain down."""
    from librarian import consult

    spread = consult.component_name_distribution()
    if not spread:
        pytest.skip("no component store")
    common = dict(spread["most_common"])
    assert common.get("tests", 0) > consult.COMPONENT_SELECTIVITY_CEILING or \
        common.get("docs", 0) > consult.COMPONENT_SELECTIVITY_CEILING, \
        "the ceiling must actually exclude something, or it is decoration"


def test_the_component_ceiling_ships_with_its_distribution():
    """`THRESHOLD_CARRIES_ITS_DISTRIBUTION`, the invariant added the same day."""
    from librarian import consult

    assert callable(consult.component_name_distribution)


def test_components_never_crowd_out_the_coarse_grain():
    """Components share the page budget rather than being appended past it -
    `limit=3` used to return four rows, which made the parameter meaningless.
    But the fine grain must never dominate: at a small limit it yields
    entirely, and it is capped at a quarter of the page above that."""
    from librarian import consult
    from librarian.config import CatalogueConfig
    from librarian.relevance import apply

    base = CatalogueConfig.load()
    cfg = apply(base, {"include_components": True})

    small = consult.find_donor("parse SQL keeping comments", {}, 3, cfg=cfg)
    assert len(small.results) <= 3, "limit must bound the whole response"
    assert not [r for r in small.results if r.kind == "component"],         "at a small limit the fine grain yields entirely"

    page = consult.find_donor("parse SQL keeping comments", {}, 12, cfg=cfg)
    assert len(page.results) <= 12
    components = [r for r in page.results if r.kind == "component"]
    assert len(components) <= consult.COMPONENT_LIMIT
    assert len(components) * 3 <= len(page.results),         "components must stay a minority of the page"


def test_a_component_result_is_traceable_to_a_survey():
    """A component exists only because a survey recorded that path at a known
    commit. That is what makes it data rather than a guess."""
    from librarian import consult

    results = consult.find_components(["ontologies", "peopleOntology"])
    for result in results:
        assert result.fields["repo_key"]
        assert "recorded by the survey of" in result.why


def test_the_separation_probe_is_rerunnable():
    """Stage 2 closed on a measurement with only five negative examples, which
    bounds the effect size rather than proving zero. The probe is kept so the
    answer can be re-derived when the scenario set gains negatives."""
    from librarian import coverage

    assert callable(coverage.separation_probe)
    assert set(coverage.SEPARATION_VARIANTS) == {"whole", "ask_only", "component"}
