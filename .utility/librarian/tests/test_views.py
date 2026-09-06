"""Derived views. The property that matters is that they are *derived*:
regenerating from the notes must be reproducible, must not invent anything,
and must not rewrite what a person authored.
"""
from __future__ import annotations

import re
from pathlib import Path

from librarian import views


def _taxonomy(vault: Path) -> Path:
    return vault / "00-Indexes" / "Taxonomy Index.md"


def _topic(vault: Path) -> Path:
    return next((vault / "00-Indexes").glob("Topic - *.md"))


def test_regenerating_twice_changes_nothing(vault: Path):
    """Idempotence is what makes a view safe to run on a schedule."""
    views.run(vault, write=True)
    assert views.run(vault, write=False) == [], \
        "a second pass must find no drift, or the view is not a function of the notes"


def test_check_reports_drift_without_writing(vault: Path):
    views.run(vault, write=True)
    path = _topic(vault)
    damaged = re.sub(r"^resource_count:.*$", "resource_count: 999",
                     path.read_text(encoding="utf-8"), count=1, flags=re.M)
    path.write_text(damaged, encoding="utf-8")

    changes = views.run(vault, write=False)
    assert changes, "a deliberately wrong count must be detected"
    assert path.read_text(encoding="utf-8") == damaged, \
        "check mode must not write; it is the gate, not the fix"


def test_a_stale_count_is_corrected_from_the_notes(vault: Path):
    views.run(vault, write=True)
    path = _topic(vault)
    text = path.read_text(encoding="utf-8")
    truth = re.search(r"^resource_count:\s*(\d+)", text, re.M).group(1)
    path.write_text(re.sub(r"^resource_count:.*$", "resource_count: 41", text,
                           count=1, flags=re.M), encoding="utf-8")

    views.run(vault, write=True)
    fixed = re.search(r"^resource_count:\s*(\d+)",
                      path.read_text(encoding="utf-8"), re.M).group(1)
    assert fixed == truth, \
        "the notes are truth; a hand-typed count is the copy that can be wrong"


def test_membership_is_reconciled_without_reordering(vault: Path):
    """The view owns which resources a topic holds. It does not own the order,
    which is a presentation choice a person may have made."""
    existing = "- [[zebra]]\n- [[apple]]\n"
    out = views.reconcile_list(existing, ["apple", "zebra", "mango"])
    assert out.splitlines() == ["- [[zebra]]", "- [[apple]]", "- [[mango]]"], \
        "entries already present keep their order; newcomers are appended"


def test_membership_drops_what_no_longer_qualifies(vault: Path):
    out = views.reconcile_list("- [[gone]]\n- [[stays]]\n", ["stays"])
    assert out.splitlines() == ["- [[stays]]"]


def test_rows_outside_the_matrix_section_are_removed(vault: Path):
    """The 2026-09 hand-edit appended seventeen rows to the end of the file,
    which put them inside a later section where nothing could see them."""
    views.run(vault, write=True)
    path = _taxonomy(vault)
    stray = "\n| [[a stray row]] | Mixed | Data | Active | Unknown | Server | CLI | Local_First | CPU_Only | Uncertified |\n"
    path.write_text(path.read_text(encoding="utf-8") + stray, encoding="utf-8")

    views.run(vault, write=True)
    text = path.read_text(encoding="utf-8")
    assert "a stray row" not in text, \
        "a matrix row outside the matrix duplicates a resource and is invisible to the section"
    assert views.run(vault, write=False) == []


def test_the_view_never_invents_a_frontmatter_field(vault: Path):
    """Adding a field would be schema drift, which is not a view's business."""
    text = "---\ntype: \"topic_index\"\n---\n\n# x\n"
    assert views.set_frontmatter_scalar(text, "resource_count", 7) == text


def test_only_the_named_section_is_rewritten(vault: Path):
    text = ("# Note\n\n## Keep Me\nauthored prose\n\n"
            "## Approved Resources\n- [[old]]\n\n## Keep Me Too\nmore prose\n")
    out = views.replace_section(text, "Approved Resources", "- [[new]]")
    assert "authored prose" in out and "more prose" in out
    assert "- [[new]]" in out and "- [[old]]" not in out
