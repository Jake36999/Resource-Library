"""A check that cannot name the note it failed on is one nobody can act on."""
from __future__ import annotations

from pathlib import Path

from librarian import integrity


def test_a_clean_vault_passes(vault: Path):
    violations = integrity.run_all(vault)
    errors = [v for v in violations if v.severity == integrity.ERROR]
    assert errors == [], f"the fixture vault should be clean: {errors}"
    assert integrity.exit_code(violations) == 0


def test_a_broken_link_fails_exactly_one_check_and_names_the_note(vault: Path):
    target = vault / "01-Resources" / "widget-scheduler.md"
    target.write_text(target.read_text(encoding="utf-8")
                      + "\n- [related_to:: [[No Such Note]]]\n", encoding="utf-8")

    violations = [v for v in integrity.run_all(vault) if v.severity == integrity.ERROR]
    assert len(violations) == 1, f"one defect, one violation: {violations}"
    only = violations[0]
    assert only.check == "wikilinks_resolve"
    assert only.note == "widget-scheduler"
    assert "No Such Note" in only.detail, "the message must name the broken link"


def test_duplicate_prose_across_resources_is_an_error(vault: Path):
    first = (vault / "01-Resources" / "widget-scheduler.md").read_text(encoding="utf-8")
    second = vault / "01-Resources" / "gadget-queue.md"
    body = second.read_text(encoding="utf-8")
    shared = "Runs dependent jobs on a schedule and recovers from partial failure."
    second.write_text(body.replace(
        "A durable message queue for local-first workloads.", shared), encoding="utf-8")

    violations = integrity.run_check("distinct_resource_prose", vault)
    names = {v.note for v in violations}
    assert names == {"widget-scheduler", "gadget-queue"}, \
        "both sides of a duplicate must be reported; either alone is not actionable"
    assert "Bottom Line" in violations[0].detail
    assert shared in first


def test_a_container_without_expansion_status_is_an_error(vault: Path):
    target = vault / "01-Resources" / "awesome-plumbing.md"
    target.write_text(target.read_text(encoding="utf-8").replace(
        'expansion_status: "pending"', ""), encoding="utf-8")
    violations = integrity.run_check("container_has_expansion_status", vault)
    assert [v.note for v in violations] == ["awesome-plumbing"]


def test_an_unknown_licence_class_is_an_error(vault: Path):
    target = vault / "01-Resources" / "gadget-queue.md"
    target.write_text(target.read_text(encoding="utf-8").replace(
        'license_class: "Copyleft"', 'license_class: "Freeish"'), encoding="utf-8")
    violations = integrity.run_check("license_class_known", vault)
    assert [v.note for v in violations] == ["gadget-queue"]
    assert "Source_Available" in violations[0].detail, \
        "the message should show the closed set it was checked against"


def test_an_invented_topic_key_is_an_error(vault: Path):
    target = vault / "03-Patterns" / "Pattern - Job Scheduling.md"
    target.write_text(target.read_text(encoding="utf-8").replace(
        'topic_keys: ["plumbing"]', 'topic_keys: ["plumbing", "invented_domain"]'),
        encoding="utf-8")
    violations = integrity.run_check("topic_keys_known", vault)
    assert [v.note for v in violations] == ["Pattern - Job Scheduling"]
    assert "invented_domain" in violations[0].detail


def test_an_application_record_missing_its_lesson_is_an_error(vault: Path):
    target = vault / "09-Applications" / "Application - Nightly Batch.md"
    text = target.read_text(encoding="utf-8")
    head, _, _ = text.partition("## What The Catalogue Should Learn")
    target.write_text(head, encoding="utf-8")
    violations = integrity.run_check("application_record_shape", vault)
    details = [v.detail for v in violations]
    assert any("What The Catalogue Should Learn" in d for d in details), \
        "that section is what turns a diary entry into a requirement"


def test_a_stale_taxonomy_matrix_is_a_warning_not_an_error(vault: Path):
    matrix = vault / "00-Indexes" / "Taxonomy Index.md"
    matrix.write_text(matrix.read_text(encoding="utf-8").replace(
        "| Python | Infrastructure | Production_Ready | Permissive |",
        "| Python | Infrastructure | Production_Ready | Copyleft |"), encoding="utf-8")
    violations = integrity.run_check("taxonomy_matrix_agrees", vault)
    assert violations, "a matrix that disagrees with the notes must be reported"
    assert all(v.severity == integrity.WARNING for v in violations), \
        "the note is truth and the matrix is generated, so this is stale, not wrong"
    assert violations[0].note == "widget-scheduler"


def test_templates_are_exempt_from_link_resolution(vault: Path, tmp_path: Path):
    template = vault / "09-Applications" / "_Template - Application Record.md"
    template.write_text('---\ntype: "application_record"\n---\n\n'
                        '# Template\n\n- [applied_resource:: [[]]]\n'
                        '- [related_topic:: [[Topic -]]]\n', encoding="utf-8")
    violations = [v for v in integrity.run_all(vault) if v.severity == integrity.ERROR]
    assert violations == [], \
        "a placeholder in a template is an instruction to the author, not a broken edge"


def test_run_check_rejects_an_unknown_name(vault: Path):
    import pytest
    with pytest.raises(KeyError) as caught:
        integrity.run_check("no_such_check", vault)
    assert "Known:" in str(caught.value)


def _set_surface(path: Path, value: str) -> None:
    text = path.read_text(encoding="utf-8")
    if "agent_surface" in text:
        import re
        text = re.sub(r'^agent_surface:.*$', f'agent_surface: "{value}"', text,
                      count=1, flags=re.M)
    else:
        # before the *closing* delimiter; replacing the first "---" would put
        # the field above the frontmatter block, where nothing reads it
        text = text.replace("\n---", f'\nagent_surface: "{value}"\n---', 1)
    path.write_text(text, encoding="utf-8")


def test_a_recorded_property_with_no_prose_behind_it_is_flagged(vault: Path):
    """The failure this catches was measured, not imagined.

    Several sources ship an agent-facing surface. It was recorded in
    frontmatter and inventoried in `What Is Inside`, and no query for that
    capability could reach any of them - because retrieval scores what a note
    *claims*, and the fact had only been written where it could be read.
    """
    target = next((vault / "01-Resources").glob("*.md"))
    _set_surface(target, "Callable")

    flagged = [v for v in integrity.run_check("recorded_property_is_findable", vault)
               if v.note == target.stem]
    assert flagged, "a substantive surface with no claim behind it must be reported"
    assert flagged[0].severity == integrity.WARNING, \
        "the fix is writing, so this warns rather than failing a run"


def test_saying_it_in_a_claim_section_clears_the_warning(vault: Path):
    target = next((vault / "01-Resources").glob("*.md"))
    _set_surface(target, "Callable")
    text = target.read_text(encoding="utf-8")
    target.write_text(
        text.replace("## Bottom Line\n",
                     "## Bottom Line\nReachable as a callable interface for an agent.\n", 1),
        encoding="utf-8")

    assert [v for v in integrity.run_check("recorded_property_is_findable", vault)
            if v.note == target.stem] == [], \
        "the check is satisfied by prose, which is the whole point of it"


def test_a_bare_instruction_file_is_not_asked_to_justify_itself(vault: Path):
    """`Documented` means the repository carries an AGENTS.md - a fact worth
    recording and not a capability worth claiming. Demanding prose for it would
    manufacture filler, which is the failure the standard's own
    'never a slot to fill' rule guards against."""
    target = next((vault / "01-Resources").glob("*.md"))
    _set_surface(target, "Documented")
    assert [v for v in integrity.run_check("recorded_property_is_findable", vault)
            if v.note == target.stem] == []


def test_a_topic_missing_from_the_route_map_is_a_warning(vault: Path):
    """`views.master_view` corrects the counts in the route map and never its
    membership, because which topics appear is a curation decision. So a new
    topic silently never appears - which happened on 2026-09-04, with
    `topic_count: 15` above a list of fourteen and every check passing."""
    master = vault / "00-Indexes" / "Master Index.md"
    master.parent.mkdir(parents=True, exist_ok=True)
    master.write_text("---\ntype: \"master_index\"\nstatus: \"active\"\n---\n\n"
                      "# Master Index\n\n## Route Map\n- (nothing yet)\n",
                      encoding="utf-8")
    violations = integrity.run_check("every_topic_is_routable", vault)
    assert violations, "an unlisted topic index is unreachable by browsing"
    assert all(v.severity == integrity.WARNING for v in violations), \
        "the fix is a routing decision, so it must not fail a run"
    assert "Topic - Plumbing" in {v.note for v in violations}


def test_a_listed_topic_raises_nothing(vault: Path):
    master = vault / "00-Indexes" / "Master Index.md"
    master.parent.mkdir(parents=True, exist_ok=True)
    master.write_text("---\ntype: \"master_index\"\nstatus: \"active\"\n---\n\n"
                      "# Master Index\n\n## Route Map\n- [[Topic - Plumbing]]\n",
                      encoding="utf-8")
    assert integrity.run_check("every_topic_is_routable", vault) == []


def test_a_check_with_no_firing_test_is_reported(vault: Path):
    """`FAILURE_MUST_BE_LOUD`. A check nobody has seen fail cannot be
    distinguished from a check that detects nothing - which is exactly what the
    duplicate floor above its own maximum was."""
    violations = integrity.run_check("every_check_can_fail", vault)
    assert all(v.severity == integrity.WARNING for v in violations), \
        "the fix is writing a test, so nobody should be blocked from a run"
    reported = {v.note for v in violations}
    assert "every_check_can_fail" not in reported, \
        "the check must not report itself; this test is its demonstration"


def test_a_threshold_without_its_distribution_is_reported(vault: Path, monkeypatch):
    """`THRESHOLD_CARRIES_ITS_DISTRIBUTION` was declared on 2026-09-04 and seven
    of eleven thresholds violated it two days later. A rule with no check is a
    preference."""
    from librarian import duplicates

    assert integrity.run_check("thresholds_carry_their_distribution", vault) == [], \
        "every corpus-relative threshold should currently carry its re-derivation"

    monkeypatch.delattr(duplicates, "distribution")
    violations = integrity.run_check("thresholds_carry_their_distribution", vault)
    assert any("SEMANTIC_FLOOR" in v.detail for v in violations), \
        "removing the re-derivation must be reported"
