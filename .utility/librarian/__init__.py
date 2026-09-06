"""The librarian: a queryable reference with a supervised intake.

Three subsystems, deliberately separate, per `00-Indexes/Design Specification.md`:

    index/graph     the derived store - disposable, rebuildable from Markdown
    consult         Mode C, the read surface - fast, stateless, one permitted write
    toolchain/      Modes A, B and D - slow, gated, calls the ToolSet rather
    workbench       than reimplementing it

Markdown is truth. Everything in `catalogue_index.sqlite` can be deleted and
rebuilt from the vault; if the index and a note disagree, the note wins.
"""
from __future__ import annotations

__all__ = [
    "config",
    "policy",
    "notes",
    "index",
    "integrity",
    "consult",
    "embed",
    "toolchain",
    "access_points",
    "graph",
    "workbench",
    "evalset",
]

__version__ = "1.0.0"
