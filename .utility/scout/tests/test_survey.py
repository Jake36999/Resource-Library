"""The surveyor, promoted from a scratchpad on 2026-09-04.

Everything here runs offline. The network half is one shared function
(`discovery.fetch_repo`) and one shared clone; the part worth testing is the
classification, which is pure.
"""
from __future__ import annotations

from scout import survey


def test_a_path_can_be_two_kinds_of_material_at_once():
    """`tests/fixtures/x.json` genuinely is both, and counting it under each is
    the intended behaviour rather than double counting."""
    signals = survey.classify(["tests/fixtures/x.json"])
    assert signals["tests"]["n"] == 1
    assert signals["fixtures"]["n"] == 1


def test_the_count_and_the_sample_are_stored_separately():
    """The 2026-09-03 survey stored only a truncated sample, and its length was
    later mistaken for the count - ten tests recorded for a repository with
    847. Storing both removes the ambiguity rather than documenting it."""
    paths = [f"test/case_{i}.py" for i in range(40)]
    signals = survey.classify(paths)
    assert signals["tests"]["n"] == 40
    assert len(signals["tests"]["sample"]) == survey.SAMPLE_PATHS


def test_shape_reports_structure_without_a_network():
    paths = ["src/main.py", "src/core/a.py", "src/core/b.py", "docs/guide.md",
             "README.md", "Dockerfile"]
    shape = survey.shape(paths)
    assert shape["files"] == 6
    assert "src (3)" in shape["top"]
    assert shape["second"]["src"] == ["core (2)"]
    assert "README.md" in shape["root_files"] and "Dockerfile" in shape["root_files"]
    assert ".py (3)" in shape["extensions"]


def test_an_empty_repository_does_not_raise():
    shape = survey.shape([])
    assert shape["files"] == 0 and shape["signals"] == {}


def test_the_signal_table_is_the_one_the_data_layer_reads():
    """`components.py` classifies nothing itself; it reads what a survey wrote.
    If these drift, the data layer silently stops matching the surveyor."""
    from librarian.components import SCHEMA

    assert "signal" in SCHEMA
    assert set(survey.SIGNALS) >= {"tests", "fixtures", "grammars", "schemas",
                                   "docs", "examples", "agent_instructions"}
