"""The adapter must work with the ToolSet absent, and must not collapse the
two ways an investigation can be stopped into one generic error."""
from __future__ import annotations

from pathlib import Path

from librarian import intake as intake_mod
from librarian import toolchain
from librarian.config import CatalogueConfig


def absent_config(tmp_path: Path) -> CatalogueConfig:
    return CatalogueConfig(toolchain_root=str(tmp_path / "nope"),
                           toolchain_candidates=(str(tmp_path / "also-nope"),))


def test_toolchain_absent_is_reported_not_raised(tmp_path: Path, monkeypatch):
    monkeypatch.delenv("TOOLSET_ROOT", raising=False)
    ok, reason = toolchain.toolchain_available(absent_config(tmp_path))
    assert ok is False
    assert "Tried:" in reason, "the message must say where it looked"


def test_investigate_with_the_toolchain_absent_returns_an_error_result(
        tmp_path: Path, monkeypatch):
    monkeypatch.delenv("TOOLSET_ROOT", raising=False)
    result = toolchain.investigate(tmp_path, "objective", cfg=absent_config(tmp_path))
    assert result.status == "error"
    assert result.blocked_by is None, \
        "a missing ToolSet is not a manifest block or a refused approval"


def test_manifest_block_and_policy_block_are_distinct(tmp_path: Path):
    blocked = toolchain.normalise({
        "status": "blocked", "session_id": "s1",
        "events": [{"event": "MANIFEST_BLOCK", "status": "BLOCK"}]})
    refused = toolchain.normalise({
        "status": "review_required", "session_id": "s2",
        "events": [{"event": "REVIEW_REQUIRED"}],
        "policy": {"code": "REVIEW_APPROVAL_REQUIRED"}})
    unapproved = toolchain.normalise({
        "status": "review_required", "session_id": "s3",
        "events": [{"event": "REVIEW_REQUIRED", "reason": "allow_slice is false"}]})

    assert blocked.blocked_by == toolchain.MANIFEST_BLOCK
    assert refused.blocked_by == toolchain.POLICY_BLOCK
    assert unapproved.blocked_by is None, \
        "a decision nobody made is not a decision that was refused"
    assert refused.policy["code"] == "REVIEW_APPROVAL_REQUIRED"


def test_a_complete_run_reports_its_report(tmp_path: Path):
    result = toolchain.normalise({
        "status": "complete", "session_id": "s4",
        "events": [{"event": "SLICE_COMPLETE"}, {"event": "ARCHIVED"}],
        "artifacts": {"final_markdown": str(tmp_path / "report.md")}})
    assert result.status == "complete"
    assert result.report_path == tmp_path / "report.md"
    assert result.event_names() == ["SLICE_COMPLETE", "ARCHIVED"]


def test_investigate_passes_the_safe_profile_and_never_dev_mode(tmp_path: Path):
    seen = {}

    def runner(**kwargs):
        seen.update(kwargs)
        return {"status": "complete", "session_id": "s", "events": [], "artifacts": {}}

    toolchain.investigate(tmp_path, "objective", allow_slice=True, runner=runner)
    assert seen["profile"] == "safe"
    assert seen["allow_slice"] is True
    import os
    assert os.environ.get("LTA_DEV_MODE") is None, \
        "the intake must never set the escape hatch"


def test_read_slice_summarises_without_retaining(tmp_path: Path):
    import json
    path = tmp_path / "semantic_slice.json"
    path.write_text(json.dumps({
        "built_at_commit": "abc",
        "slices": [{"name": "run", "kind": "function", "path": "app/cli.py",
                    "docstring": "Entry point."},
                   {"name": "Widget", "kind": "class", "path": "app/core.py"}]}),
        encoding="utf-8")
    summary = toolchain.read_slice(path)
    assert summary["available"] is True
    assert summary["symbol_count"] == 2
    assert "app/cli.py" in summary["modules"]


def test_read_slice_reports_an_unreadable_file(tmp_path: Path):
    path = tmp_path / "broken.json"
    path.write_text("{not json", encoding="utf-8")
    assert toolchain.read_slice(path)["available"] is False


# --------------------------------------------------------------- intake wiring

class FakeClone:
    def __init__(self, path: Path):
        self.path = path


def test_investigate_source_summarises_a_slice_and_keeps_no_clone(tmp_path: Path):
    import json
    holder: dict[str, Path] = {}

    def cloner(key, dest, depth=1):
        Path(dest).mkdir(parents=True, exist_ok=True)
        (Path(dest) / "main.py").write_text("print(1)", encoding="utf-8")
        holder["workspace"] = Path(dest).parent
        return FakeClone(Path(dest))

    slice_path = tmp_path / "semantic_slice.json"
    slice_path.write_text(json.dumps({"slices": [
        {"name": "main", "kind": "function", "path": "main.py"}]}), encoding="utf-8")

    def investigator(repo_path, objective, **kwargs):
        return toolchain.InvestigationResult(
            status="complete", session_id="s", events=({"event": "SLICE_COMPLETE"},),
            slice_path=slice_path)

    evidence = intake_mod.investigate_source("owner/repo", "catalogue it",
                                             investigator=investigator, cloner=cloner)
    assert evidence.available is True
    assert evidence.symbol_count == 1
    assert evidence.slice_retained is False, \
        "a slice is a component of a source, not a source; it is not kept"
    assert not holder["workspace"].exists(), "the clone must be gone"


def test_investigate_source_degrades_when_the_clone_fails(tmp_path: Path):
    def cloner(key, dest, depth=1):
        raise RuntimeError("no such repository")

    evidence = intake_mod.investigate_source(
        "owner/repo", "catalogue it", cloner=cloner,
        investigator=lambda *a, **k: toolchain.InvestigationResult(status="complete"))
    assert evidence.available is False
    assert evidence.status == "clone_failed"
    assert "no such repository" in evidence.reason


def test_investigate_source_carries_a_block_through(tmp_path: Path):
    def cloner(key, dest, depth=1):
        Path(dest).mkdir(parents=True, exist_ok=True)
        return FakeClone(Path(dest))

    def investigator(repo_path, objective, **kwargs):
        return toolchain.InvestigationResult(
            status="blocked", blocked_by=toolchain.MANIFEST_BLOCK,
            detail="doctor said BLOCK", events=({"event": "MANIFEST_BLOCK"},))

    evidence = intake_mod.investigate_source("owner/repo", "x",
                                             investigator=investigator, cloner=cloner)
    assert evidence.available is False
    assert evidence.blocked_by == toolchain.MANIFEST_BLOCK


def test_evidence_block_is_labelled_untrusted():
    evidence = intake_mod.SourceEvidence(True, "owner/repo", "complete",
                                         symbol_count=3, modules=("a.py",))
    text = intake_mod.evidence_block(evidence)
    assert "untrusted" in text
    assert "discarded" in text


def test_evidence_block_says_so_when_unavailable():
    evidence = intake_mod.SourceEvidence(False, "owner/repo", "clone_failed", "boom")
    text = intake_mod.evidence_block(evidence)
    assert "do not infer structure" in text, \
        "absent evidence must forbid invention, not merely be silent"
