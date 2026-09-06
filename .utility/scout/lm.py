"""Model access.

Local work goes to LM Studio through the existing adapter, which already
handles model loading budgets, constrained JSON output and reachability
reporting. Escalation to a hosted model is opt-in, keyed from the
environment only, and never writes a credential anywhere.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path
from typing import Any

from .config import UTILITY_ROOT, ScoutConfig, escalation_key

if str(UTILITY_ROOT) not in sys.path:
    sys.path.insert(0, str(UTILITY_ROOT))


class LMUnavailable(RuntimeError):
    pass


def client_for(model: str = ""):
    """An LM Studio client with the pipeline's model pinned, if configured."""
    try:
        from adapters.lmstudio import LMStudioClient, LMStudioSettings
    except ImportError as exc:  # pragma: no cover - depends on vault layout
        raise LMUnavailable(f"cannot import the LM Studio adapter: {exc}")

    config_path = UTILITY_ROOT / "library_config.json"
    raw: dict[str, Any] = {}
    if config_path.exists():
        try:
            raw = json.loads(config_path.read_text(encoding="utf-8"))
        except Exception:
            raw = {}
    settings = LMStudioSettings.from_config(raw)
    client = LMStudioClient(settings)
    available, reason = client.availability()
    if not available:
        raise LMUnavailable(reason)
    if model:
        client._pinned_model = model  # noqa: SLF001 - honoured via choose_model below
        original = client.choose_model
        client.choose_model = lambda stage, preferred=None: model or original(stage, preferred)
    return client


# ------------------------------------------------------- hosted escalation

def escalate(cfg: ScoutConfig, system: str, user: str,
             max_tokens: int = 4000) -> str:
    """Send one request to a hosted model.

    Only called when the local model's confidence is low, the item is in the
    top decile of its cohort, or the item is a paper - cases where a wrong
    entry costs more than the API call.
    """
    provider = (cfg.escalation_provider or "none").lower()
    if provider == "none":
        raise LMUnavailable("escalation is disabled (scout.escalation_provider)")
    key = escalation_key(provider)
    if not key:
        env = "OPENAI_API_KEY" if provider == "openai" else "ANTHROPIC_API_KEY"
        raise LMUnavailable(f"{env} is not set in the environment")

    if provider == "openai":
        url = "https://api.openai.com/v1/chat/completions"
        body = {
            "model": cfg.escalation_model or "gpt-4o-mini",
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": user}],
            "max_tokens": max_tokens,
            "response_format": {"type": "json_object"},
        }
        headers = {"Authorization": f"Bearer {key}",
                   "Content-Type": "application/json"}
        payload = _post(url, body, headers)
        return payload["choices"][0]["message"]["content"]

    url = "https://api.anthropic.com/v1/messages"
    body = {
        "model": cfg.escalation_model or "claude-sonnet-4-5",
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    headers = {"x-api-key": key, "anthropic-version": "2023-06-01",
               "Content-Type": "application/json"}
    payload = _post(url, body, headers)
    parts = payload.get("content") or []
    return "".join(p.get("text", "") for p in parts if isinstance(p, dict))


def _post(url: str, body: dict[str, Any], headers: dict[str, str],
          timeout: int = 180) -> dict[str, Any]:
    request = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"), method="POST")
    for name, value in headers.items():
        request.add_header(name, value)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))
