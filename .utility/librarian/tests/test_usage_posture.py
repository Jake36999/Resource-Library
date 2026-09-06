"""A licence class is a fact; what it costs you is a policy.

These lock in the 2026-09-04 decision that the catalogue's posture is
`private`, and — more importantly — that switching it back is one config key
rather than an archaeology exercise.
"""
from __future__ import annotations

import json
from pathlib import Path

from librarian import config as cfg


def test_the_answer_is_donor_reference_or_tool_not_a_class_name():
    """The class alone does not say what it stops you doing, which is the only
    thing anybody asks a licence."""
    for klass in ("Permissive", "Weak_Copyleft", "Copyleft",
                  "Source_Available", "Unknown"):
        uses = cfg.permitted_uses(klass, "private")
        assert set(uses) == {"donor", "reference", "tool"}, klass


def test_distributed_posture_still_restricts():
    assert cfg.permitted_uses("Copyleft", "distributed") == ("reference", "tool")
    assert cfg.permitted_uses("Unknown", "distributed") == ("reference",)
    assert cfg.permitted_uses("Permissive", "distributed") == (
        "donor", "reference", "tool")


def test_an_unrecognised_class_is_treated_as_unknown_not_as_permitted():
    """A typo in a taxonomy value must never widen what is allowed."""
    assert cfg.permitted_uses("Freeish", "distributed") == ("reference",)
    assert cfg.permitted_uses(None, "distributed") == ("reference",)


def test_a_missing_or_broken_config_degrades_to_private(tmp_path: Path):
    """Same posture as everything else here: report a default, never raise."""
    assert cfg.distribution_posture(tmp_path / "absent.json") == "private"
    broken = tmp_path / "broken.json"
    broken.write_text("{not json", encoding="utf-8")
    assert cfg.distribution_posture(broken) == "private"


def test_an_unrecognised_posture_falls_back_rather_than_inventing_one(tmp_path: Path):
    target = tmp_path / "odd.json"
    target.write_text(json.dumps({"usage": {"distribution_posture": "yolo"}}),
                      encoding="utf-8")
    assert cfg.distribution_posture(target) == "private"


def test_the_shipped_config_says_private():
    """If this fails somebody changed the posture. That is allowed - but it
    changes what every ranked answer means, so it should not happen quietly."""
    assert cfg.distribution_posture() == "private"


def test_every_result_carries_its_permitted_uses(vault):
    """Derived on read from a recorded fact plus a configured posture. Storing
    it would let the two drift."""
    from librarian import consult, index

    db = vault / "test_index.sqlite"
    index.build(vault, db)
    response = consult.find_donor("scheduler", {}, 5, db_path=db)
    assert response.results, "fixture vault should return something"
    for result in response.results:
        assert result.fields["permitted_uses"] == ["donor", "reference", "tool"]


# ------------------------------- LOCATE_DO_NOT_ADJUDICATE, the general case

def test_the_catalogue_role_defaults_to_the_one_that_withholds_least(tmp_path: Path):
    assert cfg.catalogue_role(tmp_path / "absent.json") == "reference"
    broken = tmp_path / "broken.json"
    broken.write_text("{not json", encoding="utf-8")
    assert cfg.catalogue_role(broken) == "reference"


def test_the_shipped_config_says_reference():
    assert cfg.catalogue_role() == "reference"


def test_no_ranking_signal_zeroes_a_source_under_the_reference_role():
    """`LOCATE_DO_NOT_ADJUDICATE`. A zero under a double-digit weight is not a
    low rank, it is invisibility - and it was being awarded three separate ways
    for properties that only matter if you assume the user meant to depend on
    the thing. Any new signal should be added here."""
    from scout.rank import adoption, reusability, vitality

    assert reusability(None, "private") > 0.0, "unlicensed is readable and runnable"
    assert vitality(None, archived=True, role="reference") > 0.0, "archived is settled"
    assert adoption(0, "reference") > 0.0, "unfound is what a discovery tool is for"


def test_a_stated_constraint_still_eliminates(vault):
    """The distinction the policy turns on: a constraint the *user* states is
    theirs and must eliminate. Only unstated preferences baked into a ranking
    are the system's to stop imposing."""
    from librarian import consult, index

    db = vault / "constraint_index.sqlite"
    index.build(vault, db)
    wide = consult.find_donor("scheduler", {}, 10, db_path=db)
    assert wide.results, "fixture vault should return something"
    assert {r.fields.get("license_class") for r in wide.results} == {"Permissive"}

    excluded = consult.find_donor("scheduler", {"license_class": ["Copyleft"]}, 10,
                                  db_path=db)
    found = {r.name for r in wide.results} & {r.name for r in excluded.results}
    assert not found, "a licence class the user asked for must eliminate everything else"
    assert excluded.filtered_out > 0
