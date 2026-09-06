"""Shallow clones, and their disposal.

The toolchain works on a local path, so cataloguing a source means fetching
it. The decision (spec 7.1) is: shallow clone, use it, delete it. A clone is
recoverable from origin at any time, so keeping sixty-four of them buys disk
cost and staleness for nothing.

`git` is a subprocess, so it is a registered action and its command line is
built here in code. No caller passes a string through - `NO_ARBITRARY_SHELL`
is not waived because git happens to be safe.
"""
from __future__ import annotations

import re
import os
import shutil
import stat
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from . import policy

# A repo_key is `owner/name`; a URL is https and github-shaped. Anything else
# is refused rather than passed to git and hoped about.
REPO_KEY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*/[A-Za-z0-9][A-Za-z0-9._-]*$")
SAFE_URL = re.compile(r"^https://[A-Za-z0-9.-]+/[A-Za-z0-9._/-]+?(?:\.git)?$")

CLONE_TIMEOUT_SECONDS = 300


class CloneRefused(RuntimeError):
    pass


@dataclass(frozen=True)
class Clone:
    path: Path
    url: str
    depth: int
    temporary: bool
    blobless: bool = False


def normalise_url(repo_key_or_url: str) -> str:
    """Accept a repo_key or an https URL; refuse anything else.

    Refusing early is what keeps a malformed catalogue entry from reaching a
    command line at all.
    """
    value = (repo_key_or_url or "").strip()
    if REPO_KEY.match(value):
        return f"https://github.com/{value}.git"
    if SAFE_URL.match(value):
        return value if value.endswith(".git") else value + ".git"
    raise CloneRefused(
        f"'{repo_key_or_url}' is neither an owner/name repo key nor an https URL. "
        f"Commands are built from validated values, never from free text.")


def git_available() -> tuple[bool, str]:
    if shutil.which("git") is None:
        return False, "git is not on PATH; cloning is unavailable"
    return True, "git available"


def shallow_clone(repo_key_or_url: str, dest: Path | None = None, *,
                  depth: int = 1, timeout: int = CLONE_TIMEOUT_SECONDS,
                  blobless: bool = False) -> Clone:
    """Depth-1, single-branch, no submodules, no credential prompt.

    `GIT_TERMINAL_PROMPT=0` matters: an unattended sweep must fail on a
    private repository rather than block forever waiting for a password.

    `blobless=True` adds `--filter=blob:none --no-checkout`, which fetches the
    commit and tree objects and **no file contents at all**. That is what makes
    surveying a hundred repositories affordable: the structure of
    `open-metadata/docs-v1-legacy` is 10,759 paths and 2.2 GB checked out, and
    a few hundred kilobytes as a tree. It also costs no REST quota, because it
    goes over the git protocol rather than the API.

    Use it whenever the question is *what is in here* rather than *what does
    this code say*. A blobless clone cannot be read from - `git show` will go
    back to the network for each blob - so anything that needs file contents
    wants the default.
    """
    policy.check_action("git_shallow_clone")
    ok, reason = git_available()
    if not ok:
        raise CloneRefused(reason)

    url = normalise_url(repo_key_or_url)
    temporary = dest is None
    target = Path(dest) if dest else Path(tempfile.mkdtemp(prefix="librarian-clone-"))
    if target.exists() and any(target.iterdir()):
        raise CloneRefused(f"{target} is not empty; refusing to clone over it")
    target.mkdir(parents=True, exist_ok=True)

    command = ["git", "clone", "--depth", str(max(1, depth)), "--single-branch",
               "--no-tags", "--recurse-submodules=no"]
    if blobless:
        command += ["--filter=blob:none", "--no-checkout"]
    command += [url, str(target)]
    completed = subprocess.run(
        command, capture_output=True, text=True, timeout=timeout,
        env=_clone_env())
    if completed.returncode != 0:
        discard(target)
        raise CloneRefused(
            f"git clone failed for {url} (exit {completed.returncode}): "
            f"{(completed.stderr or '').strip()[:300]}")
    return Clone(path=target, url=url, depth=depth, temporary=temporary,
                 blobless=blobless)



# Environment variables a credential could arrive through. Dropped rather than
# the environment being rebuilt from nothing - see `_clone_env`.
CREDENTIAL_MARKERS = ("TOKEN", "PASSWORD", "PASSWD", "SECRET", "CREDENTIAL",
                      "AUTH", "NETRC")


def _clone_env() -> dict[str, str]:
    """The environment a clone runs in: the OS's, minus anything credential-ish.

    This was previously built from nothing - `{GIT_TERMINAL_PROMPT, GIT_ASKPASS,
    PATH}` and no more - which is a reasonable instinct and was **broken on
    Windows**: without `SystemRoot`, `getaddrinfo()` cannot start its resolver
    thread, so every clone failed with `unable to access ... getaddrinfo()
    thread failed to start`. It failed at DNS, before any network policy could
    apply, which is why it looked like a connectivity problem rather than a bug.

    Nothing in the vault records a successful network clone, `workbenches/` is
    empty, and the intake pipeline has one recorded run. Those are consistent
    with this never having worked here.

    The hardening intent is kept and made explicit instead: start from the real
    environment, drop every variable whose name suggests a credential, drop
    every `GIT_*` override so a configured credential helper cannot be
    inherited, then set the three that must hold.
    """
    env = {k: v for k, v in os.environ.items()
           if not k.upper().startswith("GIT_")
           and not any(marker in k.upper() for marker in CREDENTIAL_MARKERS)}
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GIT_ASKPASS"] = "echo"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["PATH"] = _path_env()
    return env

def discard(path: Path) -> bool:
    """Remove a clone. Git packs are read-only on Windows, so force it.

    Returns whether the directory is gone. Teardown that silently fails is
    how a "nothing is kept" design ends up keeping everything.
    """
    policy.check_action("discard_clone")
    target = Path(path)
    if not target.exists():
        return True

    def on_error(func, name, _exc):                        # pragma: no cover - platform
        try:
            Path(name).chmod(stat.S_IWRITE)
            func(name)
        except Exception:
            pass

    shutil.rmtree(target, onerror=on_error)
    return not target.exists()


def _path_env() -> str:
    import os
    return os.environ.get("PATH", "")
