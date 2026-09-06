

# ------------------------------------------------- the environment a clone runs in

def test_the_clone_environment_keeps_what_the_os_needs():
    """A real bug, found 2026-09-04. The environment was built from nothing -
    `{GIT_TERMINAL_PROMPT, GIT_ASKPASS, PATH}` - which on Windows drops
    `SystemRoot` and breaks DNS: every clone failed at `getaddrinfo() thread
    failed to start`, before any network was touched. It looked like
    connectivity and it was a missing variable."""
    import os

    from librarian import clone

    env = clone._clone_env()
    for needed in ("PATH",):
        assert needed in env
    for name in os.environ:
        if name.upper() in {"SYSTEMROOT", "WINDIR", "COMSPEC", "TEMP", "TMP"}:
            assert name in env, f"{name} is required by the OS and must survive"


def test_the_clone_environment_still_drops_credentials():
    """The hardening intent that motivated the empty environment is kept, and
    made explicit rather than achieved by omission."""
    import os

    from librarian import clone

    os.environ["MY_GITHUB_TOKEN"] = "secret"
    os.environ["GIT_CREDENTIAL_HELPER"] = "store"
    try:
        env = clone._clone_env()
        assert "MY_GITHUB_TOKEN" not in env
        assert "GIT_CREDENTIAL_HELPER" not in env, \
            "an inherited credential helper would defeat GIT_TERMINAL_PROMPT=0"
        assert env["GIT_TERMINAL_PROMPT"] == "0"
        assert env["GIT_ASKPASS"] == "echo"
    finally:
        os.environ.pop("MY_GITHUB_TOKEN", None)
        os.environ.pop("GIT_CREDENTIAL_HELPER", None)
