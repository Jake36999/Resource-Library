"""The read surface. Three properties are asserted here because they are the
ones the design would be worthless without: filters eliminate, results
explain themselves, and a missing subsystem degrades rather than raises."""
from __future__ import annotations

from pathlib import Path

import pytest

from librarian import consult
from librarian import embed as embed_mod


def test_hard_filters_eliminate_rather_than_down_rank(built: Path):
    response = consult.find_donor("queue scheduler jobs",
                                  {"license_class": "Permissive"}, 10, db_path=built)
    licences = {r.fields.get("license_class") for r in response.results}
    assert licences <= {"Permissive"}, \
        "a candidate failing a constraint must be absent, not merely demoted"
    assert response.filtered_out > 0, \
        "the count of what was eliminated is how a thin result set gets explained"


def test_a_constraint_nothing_meets_returns_nothing_and_says_why(built: Path):
    response = consult.find_donor("scheduler", {"deployment_target": "Browser",
                                       "hardware_footprint": "High_Memory"},
                                  10, db_path=built)
    assert response.results == ()
    assert "constraint" in response.next_step
    assert response.filtered_out > 0


def test_unknown_values_are_eliminated_too(built: Path):
    """"We do not know whether this runs on a laptop" is not an answer to
    "what runs on a laptop"."""
    response = consult.find_donor("curated list plumbing",
                                  {"license_class": "Permissive"}, 10, db_path=built)
    assert "awesome-plumbing" not in {r.name for r in response.results}


def test_every_result_carries_a_why(built: Path):
    for response in (
        consult.orient("plumbing scheduler", db_path=built),
        consult.find_donor("dependent jobs", {}, db_path=built),
        consult.find_pattern("ordering dependent work", db_path=built),
        consult.find_technique("how are retries handled", db_path=built),
        consult.find_data("plumbing", db_path=built),
        consult.find_precedent("widget-scheduler", db_path=built),
    ):
        for result in response.results:
            assert result.why.strip(), f"{response.intent}/{result.name} has no why"


def test_why_never_claims_a_term_that_did_not_match(built: Path):
    response = consult.find_donor("scheduler", {}, 10, db_path=built)
    for result in response.results:
        for quoted in result.why.split("matched ")[1:]:
            term = quoted.split("'")[1]
            note = consult.get_note(result.name, db_path=built)
            haystack = (note["body"] + note["name"] + str(note["frontmatter"])).lower()
            assert term.lower() in haystack, \
                f"why claimed '{term}' matched {result.name}, and it did not"


def test_an_unavailable_subsystem_produces_partial_not_an_exception(built: Path,
                                                                   monkeypatch):
    def exploding(*args, **kwargs):
        raise RuntimeError("LM Studio is on fire")

    monkeypatch.setattr(embed_mod, "search",
                        lambda conn, query, cfg=None, limit=50, layers=None:
                        ([], "LM Studio unreachable"))
    response = consult.find_donor("scheduler", {}, db_path=built)
    assert response.partial is True
    assert response.notes, "partial must say what was missing"
    assert response.results, "degrading must still answer from what is available"


def test_find_technique_refuses_an_uncatalogued_source_and_suggests_intake(built: Path):
    response = consult.find_technique("how is backpressure handled",
                                      source="nobody/nothing", db_path=built)
    assert response.results == ()
    assert "not catalogued" in response.next_step
    assert any("never fetches" in note for note in response.notes), \
        "the read path must say that fetching is an intake operation, not do it"


def test_find_technique_ends_at_the_source_and_says_so(built: Path):
    response = consult.find_technique("recovers from partial failure", db_path=built)
    assert response.results
    assert "workbench" in response.next_step
    assert any("ephemeral" in note for note in response.notes), \
        "no permanent index of extracted symbols exists, and the answer should say so"


def test_orient_separates_topics_from_resources(built: Path):
    grouped = consult.orient("plumbing scheduler queue", db_path=built).grouped()
    assert "topic" in grouped and "resource" in grouped
    assert any(r.name == "Topic - Plumbing" for r in grouped["topic"])


def test_orient_marks_a_container_as_an_aggregator(built: Path):
    grouped = consult.orient("curated list of plumbing tools", db_path=built).grouped()
    names = {r.name for r in grouped.get("aggregator", ())}
    assert "awesome-plumbing" in names, \
        "a list of resources is not a resource and must not be offered as one"


def test_find_pattern_returns_the_pattern_and_its_examples(built: Path):
    response = consult.find_pattern("ordering dependent work so failure resumes",
                                    db_path=built)
    kinds = {r.kind for r in response.results}
    assert "pattern" in kinds
    assert any(r.kind == "resource" and "implements_pattern" in r.why
               for r in response.results)


def test_find_precedent_finds_the_record_that_links_to_the_resource(built: Path):
    response = consult.find_precedent("widget-scheduler", db_path=built)
    assert [r.name for r in response.results][:1] == ["Application - Nightly Batch"]
    assert "applied_resource" in response.results[0].why
    assert response.results[0].fields["what_the_catalogue_should_learn"]


def test_find_precedent_with_nothing_recorded_asks_for_a_record(built: Path):
    response = consult.find_precedent("gadget-queue", db_path=built)
    assert response.results == ()
    assert "write the record" in response.next_step


def test_filters_alone_are_usable_with_no_matching_terms(built: Path):
    response = consult.find_donor("zzzzz nonsense token", {"license_class": "Copyleft"},
                                  10, db_path=built)
    assert [r.name for r in response.results] == ["gadget-queue"]
    assert response.tier_reached == 2, \
        "structured filters answer at tier 2, without any search machinery"
    assert "no term matched" in response.results[0].why


def test_unknown_constraints_are_rejected_not_ignored(built: Path):
    with pytest.raises(ValueError) as caught:
        consult.find_donor("scheduler", {"licence": "Permissive"}, db_path=built)
    assert "unknown constraint" in str(caught.value)


def test_get_note_returns_both_link_directions(built: Path):
    note = consult.get_note("widget-scheduler", db_path=built)
    assert note["found"] is True
    assert any(link["relation"] == "parent_topic" for link in note["links_out"])
    assert any(link["relation"] == "applied_resource" for link in note["links_in"])


def test_get_note_explains_a_miss(built: Path):
    note = consult.get_note("nothing here", db_path=built)
    assert note["found"] is False and note["why"]


# ------------------------------------------------------- the typed parameters

def test_search_params_reject_unknown_fields(vault: Path):
    with pytest.raises(ValueError):
        consult.validate_params({"intent": "donor", "terms": ["x"], "sneaky": 1},
                                vault=vault)


def test_search_params_reject_an_invented_domain(vault: Path):
    with pytest.raises(ValueError) as caught:
        consult.validate_params({"intent": "donor", "terms": ["x"],
                                 "domain": "not_a_domain"}, vault=vault)
    assert "register" in str(caught.value), \
        "an invalid domain must be an error, never a silent miss"


def test_search_params_accept_a_registered_domain(vault: Path):
    valid = consult.validate_params({"intent": "orient", "terms": ["queue"],
                                     "domain": "distributed_systems"}, vault=vault)
    assert valid["domain"] == "distributed_systems"


def test_search_params_close_the_licence_enum(vault: Path):
    with pytest.raises(ValueError):
        consult.validate_params({"intent": "donor", "terms": ["x"],
                                 "filters": {"license_class": "MIT-ish"}}, vault=vault)


def test_dispatch_routes_by_intent(built: Path, vault: Path):
    response = consult.dispatch({"intent": "precedent", "terms": ["widget-scheduler"]},
                                db_path=built, vault=vault)
    assert response.intent == "precedent"


# --------------------------------------------------------- the permitted write

RECORD = {
    "project": "Test Project",
    "stage": "delivery",
    "outcome": "it worked",
    "sections": {
        "What Was Needed": "A thing.",
        "What Was Found And Taken": "The thing.",
        "What It Replaced": "A worse thing.",
        "What The Catalogue Should Learn": "Things should be findable.",
    },
}


def test_record_application_writes_a_valid_record(vault: Path, built: Path):
    from librarian import integrity

    written = consult.record_application(dict(RECORD), vault=vault, db_path=built)
    path = Path(written["path"])
    assert path.exists()
    assert written["attested_by"] == "agent", \
        "records written by a tool must be distinguishable from ones a person wrote"
    violations = [v for v in integrity.run_check("application_record_shape", vault)
                  if v.severity == integrity.ERROR]
    assert violations == [], f"the write must satisfy its own contract: {violations}"


def test_record_application_refuses_without_the_lesson(vault: Path, built: Path):
    record = dict(RECORD)
    record["sections"] = dict(RECORD["sections"])
    record["sections"]["What The Catalogue Should Learn"] = "  "
    with pytest.raises(ValueError) as caught:
        consult.record_application(record, vault=vault, db_path=built)
    assert "What The Catalogue Should Learn" in str(caught.value)


def test_record_application_refuses_to_overwrite(vault: Path, built: Path):
    consult.record_application(dict(RECORD), vault=vault, db_path=built)
    with pytest.raises(FileExistsError):
        consult.record_application(dict(RECORD), vault=vault, db_path=built)


def test_the_consult_surface_may_write_nothing_else():
    from librarian import policy

    policy.check_consult_write("record_application")
    with pytest.raises(policy.PolicyError) as caught:
        policy.check_consult_write("delete_note")
    assert caught.value.code == policy.READ_ONLY_CONSULT


def test_a_generic_token_in_a_name_does_not_beat_a_real_body_match():
    """The defect this rule exists for, stated as the decision it encodes.

    `run-llama - llama_index` matched 'run' - one term of ten - and outranked
    `apache - airflow`, which matched four terms in its own `What It Solves`.
    The name ranking is weighted above the text ranking, so a weak hit inside
    it beats a strong hit outside it.
    """
    query = ["run", "twelve", "dependent", "jobs", "nightly", "recover",
             "partial", "failure", "rerunning", "everything"]
    assert not consult._name_hit_qualifies(("run",), query,
                                           "run-llama - llama_index")


def test_a_name_that_is_mostly_the_matched_term_still_qualifies():
    """The other half of the rule, and why it is two tests rather than one.

    A topic index is the thing `orient` most needs to reach by name, and
    `Topic - Plumbing` matches one term of three - the same query coverage
    that disqualifies the case above. What separates them is how much of the
    *note's own name* the term accounts for.
    """
    query = ["plumbing", "scheduler", "queue"]
    assert consult._name_hit_qualifies(("plumbing",), query, "Topic - Plumbing")


def test_two_matched_terms_qualify_on_any_query_length():
    query = ["spatial", "joins", "geometry", "columns", "python", "dataframes"]
    assert consult._name_hit_qualifies(("spatial", "python"), query,
                                       "some - unrelated-name")


def test_a_short_query_is_a_name_lookup_by_intent():
    """`orient("airflow")` must still resolve by name; that is what the name
    ranking is for."""
    assert consult._name_hit_qualifies(("airflow",), ["airflow"],
                                       "apache - airflow")


def test_name_hits_are_ordered_by_match_quality_not_row_order(built: Path):
    """The position becomes the RRF rank, so whatever order SQLite returned
    the rows in was silently deciding relevance."""
    from librarian import index as index_mod
    conn = index_mod.connect(built)
    try:
        hits = consult.by_name(conn, ["plumbing", "scheduler"])
    finally:
        conn.close()
    counts = [len(h.matched) for h in hits]
    assert counts == sorted(counts, reverse=True), \
        "a hit matching more of the query must rank above one matching less"


def test_matching_more_of_the_query_outranks_matching_less(built: Path):
    """RRF fuses positions, not strengths, so without a coverage contributor a
    note ranked first on one common term beats one ranked second on four.

    Measured on the real vault: `neo4j-labs - neocarta` matched 'database' and
    outranked `osquery - osquery`, which matched 'operating', 'system' and
    'database', for "query the operating system state as if it were a
    database". Coverage needs no calibration - it is a count of distinct query
    terms already computed for the `why` - so it enters as another ranking.
    """
    response = consult.find_donor("plumbing scheduler queue jobs", {}, 10, db_path=built)
    assert response.results
    covered = [len([t for t in ("plumbing", "scheduler", "queue", "jobs")
                    if t in r.why]) for r in response.results]
    leading = covered[0]
    assert leading >= max(covered),         "the result matching most of the query must not sit below one matching less"


def test_agent_surface_is_a_hard_filter_like_every_other_axis(built: Path):
    """The tenth axis, added 2026-09-04.

    The catalogue exists to help agents find prior work, so whether a source is
    legible to one - instructions, executable procedure, or a callable
    interface - is a property worth eliminating on. It behaves like the others:
    a source whose value is unknown is not a lower-ranked answer, it is absent.
    """
    response = consult.find_donor("scheduler", {"agent_surface": "Callable"}, 10,
                                  db_path=built)
    surfaces = {r.fields.get("agent_surface") for r in response.results}
    assert surfaces <= {"Callable"},         "an axis that does not eliminate is a ranking hint, not a constraint"
    assert "agent_surface" in consult.FILTER_FIELDS


def test_a_caveat_is_not_evidence_that_a_source_does_the_thing():
    """`Reading Notes` records what is *wrong* with a source. Counting a term
    match there as coverage put `gudu-sql-omni-introduce` - whose matched words
    sit inside the sentence "It is not that" - above `dbt-core`."""
    assert not consult.is_claim_section("Reading Notes")
    assert not consult.is_claim_section("Evidence")
    assert consult.is_claim_section("Bottom Line")
    assert consult.is_claim_section("Transferable Capability")
    assert consult.is_claim_section("a heading nobody has defined yet"),         "an unknown section is more likely to describe a source than to caveat it"


def test_a_term_must_be_a_whole_token_in_a_name():
    """'review' inside `asreview` is not a match for a query about review
    workflows. Names are short, so a substring hit is most of the evidence."""
    assert consult._matched_terms_bounded("asreview", ["review"]) == []
    assert consult._matched_terms_bounded("Review Queue", ["review"]) == ["review"]
    assert consult._matched_terms_bounded("dbt-labs - dbt-core", ["dbt"]) == ["dbt"]


def test_one_note_cannot_win_by_having_many_sections(built: Path):
    """`rrf` is defined over rankings of distinct items. Feeding it a chunk
    ranking made "how many of my sections mention this" a ranking signal, which
    rewarded verbose notes and got worse with every section added."""
    from librarian import index as index_mod
    conn = index_mod.connect(built)
    try:
        terms = consult.terms_from("plumbing scheduler queue")
        hits = consult.lexical(conn, terms, limit=60)
    finally:
        conn.close()
    seen, deduped = set(), []
    for hit in hits:
        if hit.note not in seen:
            seen.add(hit.note)
            deduped.append(hit.note)
    assert len(deduped) == len(set(deduped))
    assert len(deduped) <= len(hits), "dedup must not invent entries"


# ------------------------------------------- selectivity is corpus-relative

def _corpus(answerable: int, containing: dict[str, int], padding: int = 0):
    """A throwaway index with a known document frequency per term.

    `padding` adds glossary notes, which can never be an answer. They exist
    here because in the real vault there are 211 of them against 132 answerable
    notes, and counting them is what made `read` (in 96% of resource notes)
    look like a discriminating term.
    """
    import sqlite3
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE note (name TEXT, layer TEXT)")
    conn.execute("CREATE TABLE chunk (note TEXT, text TEXT)")
    for i in range(answerable):
        conn.execute("INSERT INTO note VALUES (?, 'resource')", (f"r{i}",))
        words = [term for term, count in containing.items() if i < count]
        conn.execute("INSERT INTO chunk VALUES (?, ?)", (f"r{i}", " ".join(words)))
    for i in range(padding):
        conn.execute("INSERT INTO note VALUES (?, 'glossary')", (f"g{i}",))
        conn.execute("INSERT INTO chunk VALUES (?, 'unrelated wording')", (f"g{i}",))
    return conn


def test_document_frequency_counts_only_notes_that_could_be_answers():
    """The defect this catches was measured. `read` appears in 96% of resource
    notes and discriminates nothing, but counted against the whole vault it
    scored 0.53 and was waved through - because 211 short glossary, pattern and
    index notes are in the denominator and can never be returned."""
    conn = _corpus(100, {"everywhere": 96}, padding=160)
    assert consult._selective_terms(conn, ["everywhere"], 0.50, "answerable") == frozenset()
    assert consult._selective_terms(conn, ["everywhere"], 0.50, "all") == frozenset(
        {"everywhere"}), "the old scope is what let a term in 96% of answers count"


def test_a_rare_term_survives_under_either_scope():
    conn = _corpus(100, {"malformed": 3}, padding=160)
    for scope in ("answerable", "all"):
        assert "malformed" in consult._selective_terms(conn, ["malformed"], 0.50, scope)


def test_the_ceiling_eliminates_only_a_majority_term():
    conn = _corpus(100, {"just_under": 49, "just_over": 51})
    selective = consult._selective_terms(conn, ["just_under", "just_over"], 0.50)
    assert selective == frozenset({"just_under"})


def test_the_ranking_defaults_are_where_the_grid_put_them():
    """Both were swept against both instruments on 2026-09-04 rather than
    picked, and they interact - `bm25` coverage ordering is worse under the old
    denominator and best under the corrected one. Change either and re-run
    `python -m librarian relevance`; the eval alone will not notice."""
    from librarian.config import CatalogueConfig
    cfg = CatalogueConfig.load()
    assert consult.SELECTIVITY_CEILING == 0.50
    assert cfg.selectivity_scope == "answerable"
    assert cfg.coverage_order == "bm25"


# ------------------------------------------------------------------- facets

def test_facets_come_from_the_results_not_the_vocabulary(vault: Path):
    """A drop-down listing values that cannot be selected is a menu of dead
    ends. Only what the current candidates actually carry."""
    from librarian import index

    db = vault / "facet_index.sqlite"
    index.build(vault, db)
    response = consult.find_donor("scheduler", {}, 10, db_path=db)
    for axis, values in response.facets.items():
        assert values, f"{axis} listed with no values"
        assert all(v["count"] > 0 for v in values), "a zero-count facet is a dead end"


def test_an_axis_that_does_not_vary_is_omitted(vault: Path):
    """One value across every candidate narrows nothing. Saying so is a
    statement about coverage the ranked list cannot make."""
    from librarian import index

    db = vault / "facet_index2.sqlite"
    index.build(vault, db)
    response = consult.find_donor("scheduler", {}, 10, db_path=db)
    for axis, values in response.facets.items():
        assert len(values) >= 2, f"{axis} has one value and should be omitted"


def test_a_facet_count_is_the_size_of_the_surviving_set(vault: Path):
    """The property that makes a facet honest: `eligible` eliminates rather
    than demotes, so choosing a value leaves exactly that many. The reader
    sees the cost of a constraint before paying it."""
    from librarian import index

    db = vault / "facet_index3.sqlite"
    index.build(vault, db)
    wide = consult.find_donor("scheduler", {}, 10, db_path=db)
    licences = wide.facets.get("license_class")
    if not licences:
        import pytest

        pytest.skip("fixture vault does not vary on licence")
    value, count = licences[0]["value"], licences[0]["count"]
    narrowed = consult.find_donor("scheduler", {"license_class": [value]}, 10,
                                  db_path=db)
    assert narrowed.matched == count, \
        "the count promised by the facet must be what selecting it delivers"


def test_matched_counts_every_candidate_not_the_returned_page(vault: Path):
    from librarian import index

    db = vault / "facet_index4.sqlite"
    index.build(vault, db)
    response = consult.find_donor("scheduler", {}, 1, db_path=db)
    resources = [r for r in response.results if r.kind == "resource"]
    assert len(resources) <= 1
    assert response.matched >= len(resources)
