"""Ranking is the component that decides where expensive effort goes, so its
behaviour is pinned by tests rather than trusted."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from scout.rank import (adoption, corroboration, depth, gap_fit, license_class,
                        license_from_text, spdx_is_unresolved,
                        reusability, score_candidate, vitality)
from scout.config import DEFAULT_WEIGHTS

NOW = datetime(2026, 9, 1, tzinfo=timezone.utc)


def days_ago(n: int) -> str:
    return (NOW - timedelta(days=n)).isoformat().replace("+00:00", "Z")


# ------------------------------------------------------------- components

def test_gap_fit_rewards_empty_topics():
    assert gap_fit(0) == 1.0
    assert gap_fit(5) == 0.5
    assert gap_fit(10) == 0.0
    assert gap_fit(99) == 0.0, "a saturated topic must stop attracting work"


def test_gap_fit_is_monotonic():
    values = [gap_fit(n) for n in range(0, 12)]
    assert values == sorted(values, reverse=True)


def test_corroboration_thresholds():
    assert corroboration(1) == 0.0, "a single sighting carries no consensus"
    assert corroboration(2) == 0.6
    assert corroboration(9) == 1.0


def test_vitality_prefers_recent_under_either_role():
    for role in ("reference", "integration"):
        assert vitality(days_ago(5), now=NOW, role=role) == 1.0
        assert (vitality(days_ago(5), now=NOW, role=role)
                > vitality(days_ago(200), now=NOW, role=role)
                > vitality(days_ago(1200), now=NOW, role=role)), role


def test_an_archived_repository_is_only_worthless_when_you_meant_to_depend_on_it():
    """Nine of the 2026-09-04 cohort are archived and several are among its
    most instructive entries. Archived means *settled*, which for something you
    intend to read is a virtue - it will not move under you."""
    assert vitality(days_ago(1), archived=True, now=NOW, role="integration") == 0.0
    assert vitality(days_ago(1), archived=True, now=NOW, role="reference") > 0.5


def test_a_reference_catalogue_never_zeroes_a_source_for_being_old():
    """Zero under a 15-point weight is not a low rank, it is invisibility."""
    assert vitality(days_ago(4000), now=NOW, role="reference") > 0.3
    assert vitality(None, now=NOW, role="reference") > 0.3
    assert vitality(days_ago(4000), now=NOW, role="integration") == 0.1


def test_vitality_handles_missing_and_malformed():
    assert vitality(None, now=NOW, role="integration") == 0.2
    assert vitality("not-a-date", now=NOW, role="integration") == 0.2
    assert (vitality("not-a-date", now=NOW, role="reference")
            == vitality(None, now=NOW, role="reference"))


def test_reusability_ordering_holds_under_both_postures():
    """Permissive is always preferred. How much that preference is worth is
    what the posture decides."""
    for posture in ("private", "distributed"):
        assert (reusability("MIT", posture) > reusability("MPL-2.0", posture)
                > reusability("GPL-3.0", posture)), posture


def test_an_unlicensed_source_is_disqualified_only_when_output_is_published():
    """The catalogue's own posture is `private`, and privately a repository
    with no licence can still be read, run and copied from - so scoring it zero
    asked the wrong question. Set `usage.distribution_posture` to
    `distributed` and the strict scale returns."""
    assert reusability("NOASSERTION", "distributed") == 0.0
    assert reusability(None, "distributed") == 0.0
    assert reusability("NOASSERTION", "private") > 0.8
    assert reusability(None, "private") > 0.8


def test_private_posture_keeps_licence_from_being_decisive():
    """A 15% spread can break a tie between equals and can never bury a better
    answer. That is the whole intent of the private scale."""
    spread = reusability("MIT", "private") - reusability("NOASSERTION", "private")
    assert spread < 0.2
    assert (reusability("MIT", "distributed")
            - reusability("NOASSERTION", "distributed")) == 1.0


def test_license_class_distinguishes_weak_copyleft():
    assert license_class("LGPL-2.1") == "Weak_Copyleft"
    assert license_class("GPL-2.0") == "Copyleft"
    assert license_class("Apache-2.0") == "Permissive"
    assert license_class("Other") == "Unknown"


def test_adoption_is_log_scaled_not_linear():
    small, large = adoption(500), adoption(200_000)
    assert small > 0
    # A 400x difference in stars must not translate to a 400x difference in
    # score, or niche-but-relevant resources are permanently buried.
    assert large / small < 3.0


def test_adoption_saturates_and_floors():
    assert adoption(0, "integration") == 0.0
    assert adoption(None, "integration") == 0.0
    for role in ("reference", "integration"):
        assert adoption(10_000_000, role) == 1.0


def test_obscurity_is_not_evidence_of_worthlessness_for_a_discovery_tool():
    """Six of the 2026-09-04 cohort have exactly zero stars, including a graded
    graph fixture set that is immediately reusable. A catalogue whose job is
    surfacing work nobody has found cannot treat *nobody found it* as a
    verdict."""
    assert adoption(0, "reference") > 0.3
    assert adoption(None, "reference") > 0.3
    assert adoption(50_000, "reference") > adoption(0, "reference")


def test_depth_accumulates_evidence():
    assert depth() == 0.0
    assert depth(has_docs=True) == 0.35
    assert depth(has_docs=True, has_papers=True, readme_bytes=9000) == 0.85
    assert depth(True, True, 20000, True) == 1.0


# -------------------------------------------------------------- composite

def base(**gh):
    payload = {"pushed_at": days_ago(10), "license_spdx": "MIT", "stars": 1000,
               "readme_bytes": 3000, "archived": False}
    payload.update(gh)
    return {"domain_key": "testing_verification", "corroboration": 1, "github": payload}


def test_score_is_bounded():
    score, _ = score_candidate(base(), DEFAULT_WEIGHTS, 0, NOW)
    assert 0 <= score <= 100


def test_perfect_candidate_approaches_ceiling():
    record = base(pushed_at=days_ago(1), license_spdx="MIT", stars=100_000,
                  readme_bytes=20000, has_docs=True, has_papers=True, has_spec=True)
    record["corroboration"] = 5
    score, _ = score_candidate(record, DEFAULT_WEIGHTS, 0, NOW)
    assert score > 90


def test_dead_unlicensed_candidate_scores_low():
    """Under `distributed` the missing licence alone is disqualifying. Under
    the catalogue's own `private` posture it is not, so the candidate must
    still be held down by the things that are actually wrong with it - four
    years stale, three stars, no readme, a saturated topic."""
    record = base(pushed_at=days_ago(1500), license_spdx="NOASSERTION", stars=3,
                  readme_bytes=0)
    healthy = base(pushed_at=days_ago(1), license_spdx="NOASSERTION",
                   stars=100_000, readme_bytes=20000, has_docs=True)
    strict, _ = score_candidate(record, DEFAULT_WEIGHTS, 10, NOW,
                                posture="distributed")
    assert strict < 10
    private, _ = score_candidate(record, DEFAULT_WEIGHTS, 10, NOW,
                                 posture="private")
    alive, _ = score_candidate(healthy, DEFAULT_WEIGHTS, 0, NOW,
                               posture="private")
    assert private < 30, "dead and obscure must still rank low"
    assert alive > private * 2, "the licence must not be what separates them"


def test_gap_fit_can_outweigh_popularity():
    """The design intent: a modest resource filling an empty topic should beat
    a popular one landing in a saturated topic."""
    niche, _ = score_candidate(base(stars=400), DEFAULT_WEIGHTS, 0, NOW)
    crowded, _ = score_candidate(base(stars=150_000), DEFAULT_WEIGHTS, 10, NOW)
    assert niche > crowded


def test_signals_sum_to_total():
    score, signals = score_candidate(base(), DEFAULT_WEIGHTS, 3, NOW)
    assert round(sum(s.points for s in signals), 3) == score


def test_every_signal_is_explained():
    _, signals = score_candidate(base(), DEFAULT_WEIGHTS, 3, NOW)
    assert len(signals) == 6
    assert all(s.detail for s in signals), "a rank you cannot explain cannot be tuned"


def test_weights_are_configurable():
    weights = dict(DEFAULT_WEIGHTS, adoption=0.0)
    plain, _ = score_candidate(base(stars=200_000), DEFAULT_WEIGHTS, 5, NOW)
    no_stars, _ = score_candidate(base(stars=200_000), weights, 5, NOW)
    assert no_stars < plain


def test_scoring_is_deterministic():
    a, _ = score_candidate(base(), DEFAULT_WEIGHTS, 4, NOW)
    b, _ = score_candidate(base(), DEFAULT_WEIGHTS, 4, NOW)
    assert a == b


def test_source_available_is_distinguished_from_unknown():
    """BUSL, FSL and similar are a known restrictive answer, not a missing one.
    GitHub reports them as NOASSERTION, which is why they need naming."""
    assert license_class("BUSL-1.1") == "Source_Available"
    assert license_class("FSL-1.1-Apache-2.0") == "Source_Available"
    assert license_class("Hippocratic-2.1") == "Source_Available"
    assert license_class("NOASSERTION") == "Unknown"


def test_source_available_ranks_below_copyleft_but_above_unknown():
    assert (reusability("GPL-3.0", "distributed") > reusability("BUSL-1.1", "distributed")
            > reusability("NOASSERTION", "distributed"))


def test_private_posture_puts_unknown_above_source_available():
    """Deliberately the reverse of the strict ordering, and not an oversight.
    A source-available licence states restrictions; an absent one states
    nothing. Privately neither binds, but only one of them has told you it
    intends to."""
    assert reusability("NOASSERTION", "private") > reusability("BUSL-1.1", "private")


# ------------------------------------------------- licence read from text
#
# `license_class` is the one field that eliminates in `find_donor`, and the
# GitHub API is unreliable about it: NOASSERTION for every composite LICENSE
# and every source-available licence, nothing at all when the licence is
# stated only in a readme. Three of the seventeen sources in the 2026-09
# cohort were wrong or absent from the API alone. Every case below is taken
# from a real repository read during that pass.

MIT_BODY = """MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction."""

LGPL_BODY = """                  GNU LESSER GENERAL PUBLIC LICENSE
                       Version 2.1, February 1999

 This library is free software; you can redistribute it and/or modify it
 under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation. It refers throughout to the GNU General
 Public License, which is a different licence."""

GPL3_BODY = """                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 The GNU General Public License is a free, copyleft license. If you want
 permissive terms, use the GNU Lesser General Public License instead. For
 network use, consider the GNU Affero General Public License."""

LIBCST_BODY = """All contributions towards LibCST are MIT licensed.

Some Python files have been derived from the standard library and are
therefore PSF licensed. Modifications on these files are dual licensed.
Some Python files have been taken from dataclasses and are therefore Apache
licensed.

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software."""


def test_a_licence_body_resolves_to_one_identifier():
    reading = license_from_text(MIT_BODY)
    assert reading.names == ("MIT",)
    assert reading.license_class == "Permissive"
    assert not reading.composite and not reading.review_required


def test_gpl_family_cross_references_are_not_separate_licences():
    """Every GPL-family text names its siblings, so substring matching alone
    reports three licences for a file that grants one. The discriminator is
    position: a licence document opens with its own title."""
    assert license_from_text(LGPL_BODY).names == ("LGPL-2.1",), \
        "LGPL-2.1 refers to the GPL throughout; that is a reference, not a grant"
    assert license_from_text(GPL3_BODY).names == ("GPL-3.0",), \
        "GPL-3.0 names the LGPL and the AGPL in its own closing sections"


def test_lgpl_is_weak_copyleft_not_copyleft():
    """The distinction `find_donor` filters on. Reading semgrep's LICENSE as
    Copyleft would have removed it from every weak-copyleft-tolerant query."""
    assert license_from_text(LGPL_BODY).license_class == "Weak_Copyleft"


def test_a_composite_licence_reports_all_of_them_and_asks_for_review():
    """The correct answer for a composite is a person reading it. A confident
    single answer would be the plausible guess `EVIDENCE_REQUIRED` forbids."""
    reading = license_from_text(LIBCST_BODY)
    assert set(reading.names) == {"MIT", "PSF-2.0", "Apache-2.0"}
    assert reading.composite and reading.review_required
    assert reading.license_class == "Permissive", \
        "all three are permissive, so the most restrictive class is still Permissive"


def test_a_composite_takes_the_most_restrictive_class_present():
    mixed = GPL3_BODY + "\n\nPortions are MIT licensed."
    reading = license_from_text(mixed)
    assert "MIT" in reading.names and "GPL-3.0" in reading.names
    assert reading.license_class == "Copyleft", \
        "the most restrictive licence present governs what a reuser may do"
    assert reading.review_required


def test_a_readme_licence_is_read_but_never_trusted_outright():
    """`syntax-tree/mdast` ships no LICENSE file and states CC-BY-4.0 in one
    line of its readme. Recording that as Unknown loses a written answer;
    recording it as settled overstates a prose mention."""
    readme = "# mdast\n\n## License\n\n[CC-BY-4.0][license] (c) Titus Wormer\n"
    reading = license_from_text("", readme)
    assert reading.names == ("CC-BY-4.0",)
    assert reading.license_class == "Permissive"
    assert reading.review_required, "prose is weaker evidence than a LICENSE file"
    assert "readme" in reading.evidence


def test_no_licence_anywhere_is_unknown_and_flagged():
    """Three sources in the 2026-09 cohort had no licence at all. That is a
    finding, not a gap: `Unknown` is excluded from every constrained query."""
    reading = license_from_text("", "# a readme with nothing to say")
    assert reading.names == ()
    assert reading.license_class == "Unknown"
    assert reading.review_required


def test_unresolved_spdx_values_are_recognised_as_questions():
    """NOASSERTION means "we could not tell", not "there is no licence" - the
    difference between spending a request and recording a finding."""
    assert spdx_is_unresolved("NOASSERTION")
    assert spdx_is_unresolved("Other")
    assert spdx_is_unresolved("")
    assert not spdx_is_unresolved("MIT")


def test_a_reading_never_invents_a_single_identifier():
    reading = license_from_text(LIBCST_BODY)
    assert " AND " in reading.spdx, \
        "a composite must report every licence found, not choose one"


OSQUERY_LICENSE = """# License

By contributing to osquery you agree that your contributions will be licensed
under the terms of both the LICENSE-Apache-2.0 and the LICENSE-GPL-2.0 files.

If you are using osquery you are free to choose one of the provided licenses.

SPDX-License-Identifier: Apache-2.0 OR GPL-2.0-only
"""


def test_an_spdx_expression_outranks_reading_the_prose():
    """The machine-readable answer the convention exists to provide. Guessing
    at wording while an SPDX expression sits in the same file is indefensible."""
    reading = license_from_text(OSQUERY_LICENSE)
    assert reading.names == ("Apache-2.0", "GPL-2.0")
    assert "SPDX-License-Identifier" in reading.evidence


def test_an_or_expression_is_a_choice_and_takes_the_least_restrictive():
    """`Apache-2.0 OR GPL-2.0-only` lets the reuser pick, so the permissive
    option is what they may rely on. Reading it as Copyleft would remove a
    permissively usable project from every permissive-only query - which is
    what osquery would have suffered."""
    reading = license_from_text(OSQUERY_LICENSE)
    assert reading.license_class == "Permissive"
    assert " OR " in reading.spdx
    assert reading.review_required, "a dual licence is still a decision for a person"


def test_an_and_expression_binds_all_of_it():
    reading = license_from_text("SPDX-License-Identifier: MIT AND GPL-3.0-only")
    assert reading.license_class == "Copyleft"
    assert " AND " in reading.spdx


AGPL_WITH_A_BUNDLED_BSD = """GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

Portions of this distribution are BSD-3-Clause licensed.
"""


def test_gpl_version_boilerplate_is_not_a_licence_choice():
    """The defect this pins actually shipped, and got as far as the backfill.

    "either version 3 of the License, or (at your option) any later version"
    is GPL and AGPL boilerplate present in every copy of those licences, and it
    offers a choice between *versions of one licence* - not between licences.
    Reading it as a choice took the least restrictive name in the list, and
    reported ckan (AGPL-3.0) and wazuh (GPL-2.0) as Permissive: a copyleft
    project offered as an answer to a permissive-only query, which is the one
    direction of error this field must never make.

    A choice is now inferred only from an explicit SPDX `OR` expression.
    """
    reading = license_from_text(AGPL_WITH_A_BUNDLED_BSD)
    assert set(reading.names) == {"AGPL-3.0", "BSD-3-Clause"}
    assert reading.license_class == "Copyleft",         "a composite read from prose is a conjunction; the strictest licence governs"
    assert " AND " in reading.spdx
