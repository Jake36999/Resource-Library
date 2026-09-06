"""Parse [[Note Content Model]], which is the note schema.

The schema is a Markdown note rather than a JSON file, and that is the point.
`NO_SCHEMA_DRIFT` says note shape changes only by editing its authoritative
Markdown; putting the schema in `.utility/` would have made a Python package the
authority over the vault it describes.

This module only reads. It has no opinion about what the schema *should* say -
when the model and the vault disagree, `integrity.py` reports it and a person
decides which one was wrong.

Nothing here fails hard on a malformed model: a missing table yields an empty
rule set, and `integrity` reports the model as unparseable rather than raising.
A schema that cannot be read must not take the whole check suite down with it.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .config import INDEX_FOLDER, INTERNAL_FOLDER, vault_root

MODEL_NOTE = "Note Content Model"

REQUIRED = "required"
OPTIONAL = "optional"

# `| a | b |` -> ["a", "b"]. Separator rows (`| --- | --- |`) are dropped by the
# callers, which is cheaper than a second pattern.
ROW = re.compile(r"^\|(?P<cells>.+)\|\s*$", re.M)


@dataclass(frozen=True)
class Shape:
    """One validated note kind."""
    name: str
    required_fields: tuple[str, ...] = ()
    optional_fields: tuple[str, ...] = ()
    required_sections: tuple[str, ...] = ()
    optional_sections: tuple[str, ...] = ()
    # every section in the order the model declares them, required and optional
    # together - concatenating the two lists would put an optional section that
    # belongs in the middle at the end, and the ordering check reads this.
    ordered_sections: tuple[str, ...] = ()

    @property
    def known_fields(self) -> frozenset[str]:
        return frozenset(self.required_fields) | frozenset(self.optional_fields)


@dataclass(frozen=True)
class ContentModel:
    shapes: dict[str, Shape] = field(default_factory=dict)
    axis_values: dict[str, frozenset[str]] = field(default_factory=dict)
    section_order: dict[str, tuple[str, ...]] = field(default_factory=dict)
    error: str | None = None
    # Absent and broken are different failures. A vault that never adopted the
    # schema is not in violation of it - it degrades to no shape checks, the
    # way an absent graphify degrades to no communities. A model that exists
    # and does not parse is somebody's mistake, and that is an error.
    missing: bool = False

    def shape_of(self, note) -> str | None:
        """Which shape a note is validated against, or None to skip it.

        Keyed on `type` and folder, never on filename - a hub note living in the
        pattern folder is not a pattern.
        """
        note_type = (note.type or "").strip()
        for shape, expected in (("topic", "topic_index"), ("pattern", "pattern"),
                                ("glossary", "glossary_term"),
                                ("application", "application_record")):
            if note_type == expected:
                return shape if shape in self.shapes else None
        if note.layer in {"resource", "review"} and note.string("canonical_url"):
            return "resource" if "resource" in self.shapes else None
        return None


def _cells(line: str) -> list[str]:
    match = ROW.match(line)
    if not match:
        return []
    return [cell.strip() for cell in match.group("cells").split("|")]


def _table_after(text: str, heading: str) -> list[list[str]]:
    """Body rows of the first table under `## heading`, header and rule dropped."""
    match = re.search(rf"^##\s+{re.escape(heading)}\s*$", text, re.M)
    if not match:
        return []
    rest = text[match.end():]
    nxt = re.search(r"^##\s+", rest, re.M)
    block = rest[:nxt.start()] if nxt else rest
    rows = [_cells(line) for line in block.splitlines() if line.strip().startswith("|")]
    rows = [r for r in rows if r and not all(set(c) <= set("- :") for c in r)]
    return rows[1:] if rows else []          # drop the header row


def _requirement_split(rows: list[list[str]], name_at: int, req_at: int
                       ) -> tuple[tuple[str, ...], tuple[str, ...]]:
    required, optional = [], []
    for row in rows:
        if len(row) <= max(name_at, req_at):
            continue
        name, requirement = row[name_at], row[req_at].lower()
        if requirement.startswith(REQUIRED):
            required.append(name)
        elif requirement.startswith(OPTIONAL):
            optional.append(name)
    return tuple(required), tuple(optional)


def _locate(vault: Path) -> Path:
    """Where the content model lives.

    It moved from `00-Indexes` to `internal docs` on 2026-09-04. Both are
    checked because the note is the schema: failing to find it degrades the
    whole shape check to a warning, and a silent degradation caused by a folder
    rename is exactly the kind of quiet loss that is worth two `exists()` calls.
    """
    for folder in (INTERNAL_FOLDER, INDEX_FOLDER):
        candidate = vault / folder / f"{MODEL_NOTE}.md"
        if candidate.exists():
            return candidate
    return vault / INTERNAL_FOLDER / f"{MODEL_NOTE}.md"


def load(vault: Path | None = None) -> ContentModel:
    path = _locate(Path(vault or vault_root()))
    if not path.exists():
        return ContentModel(
            error=f"{MODEL_NOTE} is missing; note shape is unvalidated",
            missing=True)
    text = path.read_text(encoding="utf-8")

    shapes: dict[str, Shape] = {}
    declared = [row[0] for row in _table_after(text, "Shapes") if row]
    for name in declared:
        req_f, opt_f = _requirement_split(
            _table_after(text, f"Frontmatter — {name}"), 0, 1)
        # section tables carry an order column, so the name is the second cell
        section_rows = _table_after(text, f"Sections — {name}")
        req_s, opt_s = _requirement_split(section_rows, 1, 2)
        ordered = tuple(row[1] for row in section_rows if len(row) > 1)
        shapes[name] = Shape(name, req_f, opt_f, req_s, opt_s, ordered)

    axis_values: dict[str, frozenset[str]] = {}
    for row in _table_after(text, "Axis Values"):
        if len(row) < 2:
            continue
        values = {v.strip() for v in row[1].split(",") if v.strip()}
        if values:
            axis_values[row[0]] = frozenset(values)

    if not shapes:
        return ContentModel(error=f"{MODEL_NOTE} declares no shapes; "
                                  f"the Shapes table did not parse")
    return ContentModel(shapes=shapes, axis_values=axis_values,
                        section_order={s.name: s.ordered_sections
                                       for s in shapes.values()})
