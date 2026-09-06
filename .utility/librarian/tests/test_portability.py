"""The tool must be able to operate a vault that is not the one it lives in.

Before 2026-09-05 it could not, and it failed in the worst possible way: the
override was **half-wired**. Fifteen call sites asked `vault_root()` and
respected `CATALOGUE_VAULT`; seventeen used a module constant computed at import
from the package's own location and silently did not — including the one that
decided where the databases lived. Pointing the tool at another vault read the
index from one place and wrote it to another.

These tests exist because that is not a bug you notice. Nothing raises, nothing
warns, and the answers are merely wrong.
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest


MINIMAL_NOTE = """---
uuid: "11111111-1111-5111-8111-111111111111"
canonical_url: "https://github.com/acme/widget"
repo_key: "acme/widget"
type: "developer_tool"
primary_topic: "Plumbing"
status: "published"
license: "MIT"
ecosystem: "Python"
domain_primary: "Infrastructure"
maturity_stage: "Active"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "CLI"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
github_stars: 5
github_pushed_at: "2026-01-01T00:00:00Z"
---
# acme - widget

## Bottom Line
A widget that reticulates splines on a schedule.

## What It Solves
- Reticulate splines without a person watching.

## Architecture & Mechanics
- A loop and a queue.

## Taxonomy
- Ecosystem: Python

## Integration & Use Cases
- Reticulate your splines.

## Semantic Links
- [parent_topic:: [[Topic - Plumbing]]]

## Evidence
- Source URL: https://github.com/acme/widget

## GitHub Snapshot

- Stars: 5
"""

MINIMAL_TOPIC = """---
topic_key: "plumbing"
type: "topic_index"
status: "active"
inclusion_criteria: "Anything that moves fluid."
resource_count: 1
review_count: 0
---
# Topic - Plumbing

## Inclusion Criteria
Anything that moves fluid.

## Canonical Vocabulary
- pipe

## Why This Topic Exists
Because fluid moves.

## Mechanics
- Pipes.

## Typical Use Cases
- Moving fluid.

## Approved Resources
- [[acme - widget]]

## Review Queue
- None yet.

## Related Patterns
- None yet.

## Related Glossary
- None yet.

## Related Topics
- None yet.
"""


@pytest.fixture()
def elsewhere(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A vault that is not the one this package lives inside."""
    vault = tmp_path / "another-vault"
    (vault / "01-Resources").mkdir(parents=True)
    (vault / "00-Indexes").mkdir(parents=True)
    (vault / "01-Resources" / "acme - widget.md").write_text(
        MINIMAL_NOTE, encoding="utf-8")
    (vault / "00-Indexes" / "Topic - Plumbing.md").write_text(
        MINIMAL_TOPIC, encoding="utf-8")
    monkeypatch.setenv("CATALOGUE_VAULT", str(vault))
    monkeypatch.delenv("CATALOGUE_INDEX_DB", raising=False)
    monkeypatch.delenv("CATALOGUE_DATA", raising=False)
    return vault


def test_every_path_follows_the_override(elsewhere: Path):
    """The specific failure: `DATA_ROOT` was frozen at import, so databases
    landed in the package's own vault whatever `CATALOGUE_VAULT` said."""
    from librarian import config

    assert config.vault_root() == elsewhere
    assert config.data_root() == elsewhere / ".Data"
    assert config.database_dir() == elsewhere / ".Data" / "Databases"
    assert config.index_db_path().parent == elsewhere / ".Data" / "Databases"
    assert config.component_db_path().parent == elsewhere / ".Data" / "Databases"
    assert config.survey_dir() == elsewhere / ".Data" / "surveys"


def test_the_scout_resolves_the_same_vault(elsewhere: Path):
    """Two packages, one contract. `scout` keeps no import-time dependency on
    `librarian`, so the environment variable is what they share."""
    from scout import config as scout_config
    from scout import survey

    assert scout_config.vault_root() == elsewhere
    assert survey.survey_dir() == elsewhere / ".Data" / "surveys"


def test_the_read_path_runs_end_to_end_somewhere_else(elsewhere: Path):
    from librarian import consult, index, notes

    loaded = notes.load_vault(elsewhere)
    assert {n.name for n in loaded} == {"acme - widget", "Topic - Plumbing"}

    db = elsewhere / ".Data" / "Databases" / "catalogue_index.sqlite"
    index.build(elsewhere, db)
    response = consult.find_donor("reticulate splines", {}, 5, db_path=db)
    assert [r.name for r in response.results if r.kind == "resource"] == ["acme - widget"]


def test_nothing_is_written_back_into_the_package_vault(elsewhere: Path):
    """The half-wired failure mode, asserted directly: a run against another
    vault must not touch this one."""
    from librarian import config, index

    package_vault = config.VAULT_ROOT
    index.build(elsewhere, config.index_db_path())
    written = config.index_db_path()
    assert written.exists()
    assert elsewhere in written.parents
    assert package_vault not in written.parents


def test_an_empty_directory_reports_what_is_missing(tmp_path: Path,
                                                    monkeypatch: pytest.MonkeyPatch):
    """`librarian init` does not exist yet, so an empty vault must at least
    degrade rather than raise - the posture everything else here takes."""
    from librarian import index, notes

    empty = tmp_path / "empty-vault"
    empty.mkdir()
    monkeypatch.setenv("CATALOGUE_VAULT", str(empty))
    assert notes.load_vault(empty) == []
    db = empty / ".Data" / "Databases" / "catalogue_index.sqlite"
    stats = index.build(empty, db)
    assert db.exists(), "an empty vault still produces a valid, empty index"
    assert stats.notes == 0


def test_no_absolute_machine_path_survives_in_package_defaults():
    """Machine paths belong in `library_config.json`, never in a dataclass
    default that ships to another machine."""
    from librarian.config import CatalogueConfig

    defaults = CatalogueConfig()
    assert defaults.graphify_bin == ""
    assert defaults.toolchain_candidates == ()
    assert defaults.toolchain_root == ""
