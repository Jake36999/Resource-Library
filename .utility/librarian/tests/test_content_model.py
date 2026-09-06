"""The note schema, and the checks that read it.

[[Note Content Model]] is a Markdown note rather than a JSON file because
`NO_SCHEMA_DRIFT` says note shape changes only by editing its authoritative
Markdown. These tests pin the two properties that makes the arrangement worth
having: the model parses into rules, and a note that breaks a rule fails a
named check rather than passing quietly.
"""
from __future__ import annotations

import re
import textwrap
from pathlib import Path

import pytest

from librarian import content_model as model_mod
from librarian import integrity as integrity_mod


MODEL = """
    ---
    type: "content_model"
    ---

    # Note Content Model

    ## Shapes

    | Shape | Identified by |
    | --- | --- |
    | resource | layer `resource` or `review`, and a `canonical_url` |

    ## Frontmatter — resource

    | Field | Requirement |
    | --- | --- |
    | canonical_url | required |
    | license_class | required |
    | ecosystem | required |
    | sensitivity | optional |

    ## Sections — resource

    | Order | Section | Requirement |
    | --- | --- | --- |
    | 1 | Bottom Line | required |
    | 2 | What It Solves | required |
    | 3 | Reading Notes | optional |
    | 4 | Semantic Links | required |

    ## Axis Values

    | Axis | Permitted values |
    | --- | --- |
    | ecosystem | Python, Mixed |
    | license_class | Permissive, Unknown |
    """


@pytest.fixture()
def modelled(vault: Path) -> Path:
    (vault / "internal docs" / "Note Content Model.md").write_text(
        textwrap.dedent(MODEL).lstrip(), encoding="utf-8")
    return vault


def test_the_model_parses_into_rules(modelled: Path):
    model = model_mod.load(modelled)
    assert model.error is None
    shape = model.shapes["resource"]
    assert shape.required_fields == ("canonical_url", "license_class", "ecosystem")
    assert shape.optional_fields == ("sensitivity",)
    assert shape.required_sections == ("Bottom Line", "What It Solves", "Semantic Links")
    assert shape.optional_sections == ("Reading Notes",)
    assert model.axis_values["ecosystem"] == frozenset({"Python", "Mixed"})


def test_optional_sections_keep_their_declared_position(modelled: Path):
    """`Reading Notes` sits third in the model, between two required sections.

    Concatenating required and optional would put it last and the ordering check
    would then demand the wrong order of every note that has one.
    """
    order = model_mod.load(modelled).section_order["resource"]
    assert order == ("Bottom Line", "What It Solves", "Reading Notes", "Semantic Links")


def test_a_note_of_no_declared_shape_is_not_validated(modelled: Path):
    """Hub and index notes are written for people. Constraining their prose
    would buy nothing, so they match no shape and are skipped."""
    model = model_mod.load(modelled)

    class FakeNote:
        type = "taxonomy_hub"
        layer = "index"
        def string(self, key): return ""

    assert model.shape_of(FakeNote()) is None


def test_a_missing_required_field_is_an_error(modelled: Path):
    target = next((modelled / "01-Resources").glob("*.md"))
    text = target.read_text(encoding="utf-8")
    target.write_text(re.sub(r"^license_class:.*$", "", text, count=1, flags=re.M),
                      encoding="utf-8")

    hits = [v for v in integrity_mod.run_check("frontmatter_complete", modelled)
            if v.note == target.stem]
    assert hits, "a field the system reads must not go missing quietly"
    assert "license_class" in hits[0].detail
    assert hits[0].severity == integrity_mod.ERROR


def test_a_missing_required_section_is_an_error(modelled: Path):
    target = next((modelled / "01-Resources").glob("*.md"))
    text = target.read_text(encoding="utf-8")
    target.write_text(text.replace("## Bottom Line", "## Bottum Line", 1), encoding="utf-8")

    hits = [v for v in integrity_mod.run_check("sections_complete", modelled)
            if v.note == target.stem and v.severity == integrity_mod.ERROR]
    assert hits and "Bottom Line" in hits[0].detail


def test_an_unknown_axis_value_is_an_error_not_a_new_category(modelled: Path):
    """`find_donor` eliminates on these fields, so a typo does not degrade a
    ranking - it removes the resource from every constrained answer, silently."""
    target = next((modelled / "01-Resources").glob("*.md"))
    text = target.read_text(encoding="utf-8")
    target.write_text(re.sub(r'^ecosystem:.*$', 'ecosystem: "Pythonn"', text,
                             count=1, flags=re.M), encoding="utf-8")

    hits = [v for v in integrity_mod.run_check("axis_values_known", modelled)
            if v.note == target.stem]
    assert hits and "Pythonn" in hits[0].detail
    assert hits[0].severity == integrity_mod.ERROR


def test_an_unreadable_model_fails_once_not_everywhere(modelled: Path):
    """A broken schema must read as one failure. Reporting every note as
    malformed would bury the one thing that is actually wrong."""
    path = modelled / "internal docs" / "Note Content Model.md"
    path.write_text(path.read_text(encoding="utf-8").replace("## Shapes", "## Shpes", 1),
                    encoding="utf-8")

    assert integrity_mod.run_check("content_model_parses", modelled), \
        "an unparseable schema is an error in its own right"
    assert integrity_mod.run_check("frontmatter_complete", modelled) == [], \
        "the checks that depend on the model must stand down, not fire on everything"
    assert integrity_mod.run_check("axis_values_known", modelled) == []


def test_an_absent_model_is_reported_rather_than_raised(vault: Path):
    """The vault must stay checkable while the schema is being written."""
    model = model_mod.load(vault)
    assert model.error and "missing" in model.error
    assert integrity_mod.run_check("frontmatter_complete", vault) == []


def test_the_model_is_still_found_if_it_moves_back(modelled: Path):
    """The schema note moved from `00-Indexes` to `internal docs` on
    2026-09-04. Both are checked, because a model that cannot be found degrades
    every shape check to a warning - and a silent degradation caused by a
    folder rename is the kind of loss nobody notices until a malformed note
    ships."""
    moved = modelled / "internal docs" / "Note Content Model.md"
    text = moved.read_text(encoding="utf-8")
    moved.unlink()
    legacy = modelled / "00-Indexes" / "Note Content Model.md"
    legacy.parent.mkdir(parents=True, exist_ok=True)
    legacy.write_text(text, encoding="utf-8")

    model = model_mod.load(modelled)
    assert model.error is None and model.shapes, \
        "the fallback exists so a folder move cannot silently disable shape checks"
