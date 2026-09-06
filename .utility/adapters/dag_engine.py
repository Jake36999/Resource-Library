from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


def _configured_root() -> Path:
    """Read from `library_config.json`; absent on another machine.

    A path compiled into a module cannot be wrong on the machine that wrote it
    and cannot be right anywhere else. Absence degrades: the adapter reports the
    source as unavailable rather than raising.
    """
    import json

    config = Path(__file__).resolve().parent.parent / "library_config.json"
    try:
        doc = json.loads(config.read_text(encoding="utf-8"))
        return Path((doc.get("read_only_sources") or {}).get("dag_engine") or "")
    except Exception:
        return Path("")


READ_ONLY_ROOT = _configured_root()


@dataclass(frozen=True)
class ReadOnlySource:
    name: str
    root: Path

    def exists(self) -> bool:
        return self.root.exists()

    def is_ready(self) -> bool:
        return self.exists() and self.root.is_dir()

    def describe(self) -> dict[str, str]:
        return {
            "name": self.name,
            "root": str(self.root),
            "exists": str(self.exists()),
            "mode": "read-only",
        }


def get_source() -> ReadOnlySource:
    return ReadOnlySource(name="dag_engine", root=READ_ONLY_ROOT)
