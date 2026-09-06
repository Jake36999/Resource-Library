#!/usr/bin/env python3
"""Preflight check for the Resource Library build environment.

Run this on the machine that hosts Docker, LM Studio and the vault:

    python .utility\\preflight.py

It verifies every external dependency the design assumes, and reports what
is missing rather than failing on the first problem. Nothing is modified;
the only side effects are a pulled test image and a container that is
removed again.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
UTILITY = VAULT / ".utility"
LM_URL = "http://127.0.0.1:1234/v1"
SANDBOX_IMAGE = "python:3.12-slim"

PASS, WARN, FAIL = "PASS", "WARN", "FAIL"
results: list[tuple[str, str, str]] = []


def record(name: str, status: str, detail: str = "") -> None:
    results.append((name, status, detail))
    mark = {PASS: "  ok  ", WARN: " warn ", FAIL: " FAIL "}[status]
    print(f"[{mark}] {name}" + (f"\n         {detail}" if detail else ""))


def run(argv: list[str], timeout: int = 60) -> tuple[int, str]:
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr).strip()
    except FileNotFoundError:
        return 127, f"{argv[0]} not found on PATH"
    except subprocess.TimeoutExpired:
        return 124, f"timed out after {timeout}s"


# ---------------------------------------------------------------- docker

def check_docker() -> None:
    if not shutil.which("docker"):
        record("docker on PATH", FAIL, "install Docker Desktop, or add it to PATH")
        return
    code, out = run(["docker", "version", "--format", "{{.Server.Version}}"], 30)
    if code != 0:
        record("docker daemon", FAIL,
               "the CLI is present but the daemon did not answer. Is Docker Desktop running?\n"
               f"         {out[:200]}")
        return
    record("docker daemon", PASS, f"server {out.splitlines()[-1]}")

    # The sandbox needs to run with no network, capped resources, clean teardown.
    code, out = run(["docker", "run", "--rm", "--network", "none",
                     "--memory", "512m", "--cpus", "1", SANDBOX_IMAGE,
                     "python", "-c", "print('sandbox-ok')"], 300)
    if code != 0:
        record("sandbox container", FAIL,
               f"could not run {SANDBOX_IMAGE} with --network none --memory 512m\n"
               f"         {out[:300]}")
        return
    if "sandbox-ok" not in out:
        record("sandbox container", WARN, f"ran but produced unexpected output: {out[:150]}")
        return
    record("sandbox container", PASS, "runs with --network none, memory and cpu caps")

    # Isolation must actually hold: no egress when the network is off.
    code, out = run(["docker", "run", "--rm", "--network", "none", SANDBOX_IMAGE,
                     "python", "-c",
                     "import urllib.request as u;"
                     "u.urlopen('http://example.com', timeout=4);print('LEAK')"], 120)
    if "LEAK" in out:
        record("sandbox network isolation", FAIL,
               "the container reached the internet with --network none. Do not run "
               "untrusted code until this is understood.")
    else:
        record("sandbox network isolation", PASS, "no egress with --network none")


# ------------------------------------------------------------- lm studio

def check_lmstudio() -> None:
    try:
        with urllib.request.urlopen(f"{LM_URL}/models", timeout=10) as r:
            payload = json.loads(r.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        record("lm studio server", FAIL,
               f"no answer at {LM_URL} ({exc.reason}). The desktop app being open is not "
               "enough - start the local server (Developer -> Local Server, or `lms server start`).")
        return
    except Exception as exc:
        record("lm studio server", FAIL, f"{type(exc).__name__}: {exc}")
        return

    models = [m.get("id", "") for m in payload.get("data", []) if isinstance(m, dict)]
    if not models:
        record("lm studio server", WARN, "reachable but no models are loaded")
        return
    record("lm studio server", PASS, f"{len(models)} model(s): {', '.join(models[:4])}"
           + (" ..." if len(models) > 4 else ""))

    wanted = {"scout": "qwen/qwen3-4b-2507",
              "research": "qwen2.5-14b-deepresearch-i1",
              "embedding": "text-embedding-nomic-embed-text-v1.5@q4_k_m"}
    for role, model_id in wanted.items():
        present = any(model_id.split("@")[0] in m for m in models)
        record(f"model for {role}", PASS if present else WARN,
               model_id if present else f"{model_id} not listed - pin an available one in library_config.json")

    # Constrained decoding is the fix for the historical parse failures.
    body = {"model": models[0],
            "messages": [{"role": "user", "content": "Reply with JSON: {\"ok\": true}"}],
            "max_tokens": 64, "temperature": 0,
            "response_format": {"type": "json_object"}}
    req = urllib.request.Request(f"{LM_URL}/chat/completions",
                                 data=json.dumps(body).encode("utf-8"), method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            out = json.loads(r.read().decode("utf-8"))
        content = out["choices"][0]["message"]["content"]
        json.loads(content)
        record("structured output (json_object)", PASS, "model returned parseable JSON")
    except json.JSONDecodeError:
        record("structured output (json_object)", WARN,
               "the server accepted response_format but the reply was not valid JSON. "
               "parse_json_object's raw_decode fallback will cover this.")
    except Exception as exc:
        record("structured output (json_object)", WARN,
               f"could not confirm ({type(exc).__name__}). First call also pays model "
               "load time; the adapter allows 900s for it.")


# -------------------------------------------------------------- toolchain

def check_toolchain() -> None:
    root = Path("F:/Mark-XLVIII-main/ToolSet")
    if not root.exists():
        record("ToolSet root", FAIL, f"{root} not found - adjust the path in this script")
        return
    record("ToolSet root", PASS, str(root))
    needed = {
        "aletheia_toolchain/create_file_map_v3.py": "manifest scanner",
        "aletheia_toolchain/manifest_doctor.py": "manifest validator",
        "aletheia_toolchain/semantic_slicer_v7.0.py": "semantic slicer",
        "local_tool_assist_mcp/workflow.py": "guided investigation",
        "local_tool_assist_mcp/tool_registry.py": "closed action registry",
        "local_tool_assist_mcp/policy.py": "policy codes",
    }
    for rel, what in needed.items():
        p = root / rel
        record(f"toolchain: {Path(rel).name}", PASS if p.exists() else FAIL,
               what if p.exists() else f"missing at {p}")


# ------------------------------------------------------------------ vault

def check_vault() -> None:
    record("vault root", PASS if (VAULT / "00-Indexes").exists() else FAIL, str(VAULT))
    cfg = UTILITY / "library_config.json"
    if not cfg.exists():
        record("library_config.json", FAIL, f"missing at {cfg}")
        return
    try:
        conf = json.loads(cfg.read_text(encoding="utf-8"))
    except Exception as exc:
        record("library_config.json", FAIL, f"unparseable: {exc}")
        return
    for key in ("lmstudio", "github", "scout", "license_overrides"):
        record(f"config: {key}", PASS if key in conf else WARN,
               "present" if key in conf else "absent - defaults will be used")

    record("GITHUB_TOKEN", PASS if os.environ.get("GITHUB_TOKEN") else WARN,
           "set" if os.environ.get("GITHUB_TOKEN")
           else "unset - GitHub allows only 60 requests/hour without it")

    try:
        sys.path.insert(0, str(UTILITY))
        from scout.rank import license_class          # noqa: F401
        from scout.config import ScoutConfig
        ScoutConfig.load()
        record("scout package imports", PASS, "rank + config load cleanly")
    except Exception as exc:
        record("scout package imports", FAIL, f"{type(exc).__name__}: {exc}")


def main() -> int:
    print("Resource Library preflight\n" + "=" * 60)
    for section, fn in (("Docker", check_docker), ("LM Studio", check_lmstudio),
                        ("Toolchain", check_toolchain), ("Vault", check_vault)):
        print(f"\n-- {section} " + "-" * (57 - len(section)))
        try:
            fn()
        except Exception as exc:                       # a broken check must not hide the rest
            record(f"{section} (check crashed)", FAIL, f"{type(exc).__name__}: {exc}")

    fails = [r for r in results if r[1] == FAIL]
    warns = [r for r in results if r[1] == WARN]
    print("\n" + "=" * 60)
    print(f"{len(results)} checks · {len(results)-len(fails)-len(warns)} pass · "
          f"{len(warns)} warn · {len(fails)} fail")
    if fails:
        print("\nBlocking:")
        for name, _, detail in fails:
            print(f"  - {name}: {detail.splitlines()[0] if detail else ''}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
