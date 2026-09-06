"""Mode D. The three properties that make it safe are asserted, not assumed:
a sweep cannot open one, close refuses without a record, and teardown happens
even when the engagement went wrong."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from librarian import policy
from librarian import workbench as wb


class Ran:
    """A container runtime that always succeeds, and remembers the command."""

    def __init__(self):
        self.commands: list[list[str]] = []

    def __call__(self, args, timeout=0):
        self.commands.append(list(args))
        return type("R", (), {"returncode": 0, "stdout": "container-id", "stderr": ""})()


@pytest.fixture(autouse=True)
def isolated_root(tmp_path, monkeypatch):
    monkeypatch.setenv("LIBRARIAN_WORKBENCH_ROOT", str(tmp_path / "workbenches"))
    monkeypatch.delenv(wb.MODE_ENV, raising=False)


def fake_clone(key, dest, depth=1):
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "main.py").write_text("print(1)", encoding="utf-8")
    return type("C", (), {"path": dest})()


def test_a_sweep_cannot_open_a_workbench(monkeypatch):
    monkeypatch.setenv(wb.MODE_ENV, "sweep")
    with pytest.raises(wb.WorkbenchRefused) as caught:
        wb.open("owner/repo", cloner=fake_clone, runner=Ran())
    assert caught.value.code == policy.EXECUTION_SANDBOX_ONLY
    assert "unattended" in caught.value.message


def test_the_sweep_path_does_not_import_the_workbench():
    """Enforced in code, not by convention (spec 9.5).

    The runtime guard above is the second line of defence; this is the first.
    """
    import scout.cli
    import scout.deep_dive
    import scout.scout_pass
    for module in (scout.cli, scout.deep_dive, scout.scout_pass):
        source = Path(module.__file__).read_text(encoding="utf-8")
        assert "workbench" not in source, \
            f"{module.__name__} must have no path to Mode D"


def test_open_builds_an_isolated_container(monkeypatch):
    runner = Ran()
    bench = wb.open("owner/repo", cloner=fake_clone, runner=runner)
    command = " ".join(runner.commands[0])
    assert "--network none" in command, "egress is off by default"
    assert "--memory" in command and "--cpus" in command, "resource caps are required"
    assert "--user 1000:1000" in command, "non-root inside the container"
    assert "-e " not in command and "--env" not in command, \
        "the sandbox never inherits the token set"
    mounts = [c for c in runner.commands[0] if ":/work" in c]
    assert len(mounts) == 1 and str(bench.path) in mounts[0], \
        "the workbench directory is the only host path visible"


def test_close_refuses_without_a_record_and_changes_nothing(monkeypatch):
    bench = wb.open("owner/repo", cloner=fake_clone, runner=Ran())
    result = wb.close(bench.id, runner=Ran())
    assert result.refused == policy.DOCUMENT_BEFORE_DESTROY
    assert result.destroyed == ()
    assert (bench.path / "source" / "main.py").exists(), \
        "a refused close must leave the engagement exactly as it was"


def test_close_after_documenting_destroys_everything(vault: Path, built: Path):
    bench = wb.open("owner/repo", cloner=fake_clone, runner=Ran())
    wb.document(bench.id, {
        "project": "Workbench Test", "stage": "evaluation",
        "outcome": "learned something",
        "sections": {"What Was Needed": "a", "What Was Found And Taken": "b",
                     "What It Replaced": "c",
                     "What The Catalogue Should Learn": "d"}},
        vault=vault, db_path=built)

    result = wb.close(bench.id, runner=Ran())
    assert result.refused is None
    assert any("clone" in item for item in result.destroyed)
    assert any(str(vault) in item for item in result.persisted), \
        "the record survives; everything else does not"
    assert not bench.path.exists()


def test_teardown_happens_even_when_the_engagement_errored(monkeypatch):
    bench = wb.open("owner/repo", cloner=fake_clone, runner=Ran())
    (bench.path / "source" / "broken").mkdir()
    (bench.path / "source" / "broken" / "half-written.bin").write_bytes(b"\x00" * 32)

    result = wb.close(bench.id, force=True, reason="engagement failed", runner=Ran())
    assert result.refused is None
    assert not bench.path.exists(), \
        "a sandbox left behind is a sandbox that stopped being ephemeral"


def test_a_forced_close_must_say_why():
    bench = wb.open("owner/repo", cloner=fake_clone, runner=Ran())
    result = wb.close(bench.id, force=True, runner=Ran())
    assert result.refused == "FORCE_REQUIRES_REASON"


def test_a_forced_close_is_logged(monkeypatch, tmp_path):
    from librarian import config as config_mod
    monkeypatch.setattr(config_mod, "LOG_DIR", tmp_path / "logs")
    monkeypatch.setattr(wb, "_log_force", wb._log_force)
    bench = wb.open("owner/repo", cloner=fake_clone, runner=Ran())
    wb.close(bench.id, force=True, reason="abandoned", runner=Ran())
    log = (tmp_path / "logs" / "workbench_force_close.log")
    assert log.exists() and "abandoned" in log.read_text(encoding="utf-8")


def test_open_refuses_without_a_sandbox_unless_asked(monkeypatch):
    class Failed:
        def __call__(self, args, timeout=0):
            return type("R", (), {"returncode": 1, "stdout": "",
                                  "stderr": "docker daemon not running"})()

    with pytest.raises(wb.WorkbenchRefused) as caught:
        wb.open("owner/repo", cloner=fake_clone, runner=Failed())
    assert caught.value.code == policy.EXECUTION_SANDBOX_ONLY

    bench = wb.open("owner/repo", cloner=fake_clone, runner=Failed(),
                    allow_no_container=True)
    assert bench.container == ""
    assert any("do not execute" in note for note in bench.notes), \
        "an engagement that ran outside a container is a different fact and must say so"


# ------------------------------------------------------------------- closure

def graph_document(tmp_path: Path, *, with_dynamic: bool) -> Path:
    nodes = [
        {"id": "sched", "label": "scheduler", "source_file": "app/scheduler.py",
         "file_type": "code"},
        {"id": "queue", "label": "queue", "source_file": "app/queue.py",
         "file_type": "code"},
        {"id": "util", "label": "util", "source_file": "app/util.py",
         "file_type": "code"},
        {"id": "plugin", "label": "plugin_lookup", "source_file": "app/plugins.py",
         "file_type": "code"},
    ]
    links = [
        {"source": "sched", "target": "queue", "relation": "imports",
         "confidence": "EXTRACTED"},
        {"source": "queue", "target": "util", "relation": "calls",
         "confidence": "EXTRACTED"},
    ]
    if with_dynamic:
        links.append({"source": "sched", "target": "plugin",
                      "relation": "indirect_call", "confidence": "INFERRED"})
    path = tmp_path / "graph.json"
    path.write_text(json.dumps({"directed": True, "nodes": nodes, "links": links}),
                    encoding="utf-8")
    return path


def test_closure_follows_imports_and_calls(tmp_path: Path):
    summary = wb.closure_from_graph(graph_document(tmp_path, with_dynamic=False),
                                    "scheduler")
    assert set(summary.files) == {"app/scheduler.py", "app/queue.py", "app/util.py"}
    assert summary.confidence == 1.0
    assert "3 file(s)" in summary.prose()


def test_unresolved_dynamic_imports_lower_confidence_rather_than_vanish(tmp_path: Path):
    clean = wb.closure_from_graph(graph_document(tmp_path, with_dynamic=False),
                                  "scheduler")
    dynamic = wb.closure_from_graph(graph_document(tmp_path, with_dynamic=True),
                                    "scheduler")
    assert dynamic.unresolved, "an unfollowable edge must be recorded, not dropped"
    assert dynamic.confidence < clean.confidence
    assert "floor, not a total" in dynamic.prose(), \
        "the prose must admit the approximation rather than imply completeness"


def test_closure_prose_is_what_persists(tmp_path: Path):
    summary = wb.closure_from_graph(graph_document(tmp_path, with_dynamic=False),
                                    "scheduler")
    prose = summary.prose()
    assert isinstance(prose, str) and "scheduler" in prose
    assert "app/scheduler.py" not in prose, \
        "the note gets a descriptor, not a file listing that ages independently"
