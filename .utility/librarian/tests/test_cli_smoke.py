"""The entry point must at least import and describe itself.

Written after `cli.py` was left syntactically broken while **292 tests
passed** - because nothing in the suite imported it. A test suite that is
green while the command a person types is unparseable is measuring the wrong
thing, and the cheapest fix is to import every module that ships.
"""
from __future__ import annotations

import importlib
import pkgutil

import pytest


def test_every_shipped_module_imports():
    """Catches a syntax error anywhere in the package, including the parts no
    other test happens to touch."""
    import librarian

    failures = []
    for module in pkgutil.iter_modules(librarian.__path__):
        # `__main__` runs the CLI on import - that is what `python -m` needs -
        # so importing it here would execute against pytest's own argv.
        if module.name in {"tests", "__main__"}:
            continue
        try:
            importlib.import_module(f"librarian.{module.name}")
        except Exception as exc:                    # noqa: BLE001 - reporting
            failures.append(f"librarian.{module.name}: {exc}")
    assert not failures, "modules that do not import: " + "; ".join(failures)


def test_the_parser_builds_and_every_subcommand_is_reachable():
    from librarian import cli

    parser = cli.build_parser()
    action = next(a for a in parser._actions if a.dest == "command")
    names = set(action.choices)
    assert {"query", "index", "integrity", "serve", "web", "coverage",
            "components", "freshness", "relevance", "provenance",
            "duplicates", "brief", "staging"} <= names
    for name in names:
        assert action.choices[name] is not None


def test_help_does_not_raise(capsys: pytest.CaptureFixture[str]):
    from librarian import cli

    with pytest.raises(SystemExit) as caught:
        cli.build_parser().parse_args(["--help"])
    assert caught.value.code == 0
    assert "librarian" in capsys.readouterr().out
