from __future__ import annotations

from dataclasses import dataclass, field
import json
import os
import urllib.error
import urllib.request
from typing import Any


DEFAULT_BASE_URL = "http://127.0.0.1:1234/v1"


@dataclass(frozen=True)
class LMStudioSettings:
    enabled: bool = True
    base_url: str = DEFAULT_BASE_URL
    api_token: str | None = None
    stage_models: dict[str, str] = field(default_factory=dict)
    # A local model has to be loaded into VRAM before it emits its first token.
    # With JIT loading that alone can exceed a 45s budget, which is why every
    # historical failure in logs/lmstudio_errors.log is a timeout.
    timeout_seconds: int = 300
    # The first call of a run pays the model-load cost; later calls do not.
    warmup_timeout_seconds: int = 900
    # Reachability probe must fail fast rather than inherit the long budget.
    probe_timeout_seconds: int = 10
    temperature: float = 0.2
    max_tokens: int = 4096
    json_mode: bool = True
    max_input_chars: int = 16000
    max_output_chars: int = 16000

    @classmethod
    def from_config(cls, config: dict[str, Any] | None) -> "LMStudioSettings":
        config = config or {}
        section = config.get("lmstudio", {}) if isinstance(config, dict) else {}
        env_enabled = os.environ.get("LM_STUDIO_ENABLED")
        enabled = section.get("enabled", True)
        if env_enabled is not None:
            enabled = env_enabled.strip().lower() not in {"0", "false", "no", "off"}
        return cls(
            enabled=bool(enabled),
            base_url=os.environ.get("LM_STUDIO_BASE_URL", section.get("base_url", DEFAULT_BASE_URL)),
            api_token=os.environ.get("LM_STUDIO_API_TOKEN", section.get("api_token")),
            stage_models=dict(section.get("models", {})),
            timeout_seconds=int(section.get("timeout_seconds", 300)),
            warmup_timeout_seconds=int(section.get("warmup_timeout_seconds", 900)),
            probe_timeout_seconds=int(section.get("probe_timeout_seconds", 10)),
            temperature=float(section.get("temperature", 0.2)),
            max_tokens=int(section.get("max_tokens", 4096)),
            json_mode=bool(section.get("json_mode", True)),
            max_input_chars=int(section.get("max_input_chars", 16000)),
            max_output_chars=int(section.get("max_output_chars", 16000)),
        )


class LMStudioClient:
    def __init__(self, settings: LMStudioSettings):
        self.settings = settings
        self._models_cache: list[dict[str, Any]] | None = None
        self._warmed_up = False

    def _request_json(
        self,
        method: str,
        path: str,
        body: dict[str, Any] | None = None,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        url = f"{self.settings.base_url.rstrip('/')}/{path.lstrip('/')}"
        payload = None if body is None else json.dumps(body).encode("utf-8")
        request = urllib.request.Request(url, data=payload, method=method.upper())
        request.add_header("Content-Type", "application/json")
        if self.settings.api_token:
            request.add_header("Authorization", f"Bearer {self.settings.api_token}")
        effective_timeout = self.settings.timeout_seconds if timeout is None else timeout
        with urllib.request.urlopen(request, timeout=effective_timeout) as response:
            raw = response.read().decode("utf-8")
        return json.loads(raw) if raw else {}

    def is_available(self) -> bool:
        return self.availability()[0]

    def availability(self) -> tuple[bool, str]:
        """Reachability plus a human-readable reason, so a down server is
        distinguishable from a running server with no chat model loaded."""
        try:
            models = self.list_models()
        except Exception as exc:
            return False, (
                f"cannot reach LM Studio at {self.settings.base_url} ({exc}). "
                "The desktop app being open is not sufficient - the local "
                "server must be started (Developer -> Local Server, or "
                "`lms server start`)."
            )
        if not models:
            return False, "LM Studio is reachable but reports no models."
        return True, f"LM Studio reachable with {len(models)} model(s)."

    def list_models(self) -> list[dict[str, Any]]:
        if self._models_cache is not None:
            return self._models_cache
        payload = self._request_json("GET", "/models", timeout=self.settings.probe_timeout_seconds)
        models = payload.get("data", [])
        if not isinstance(models, list):
            models = []
        self._models_cache = [item for item in models if isinstance(item, dict)]
        return self._models_cache

    def choose_model(self, stage: str, preferred: str | None = None) -> str | None:
        if preferred:
            return preferred
        stage_model = self.settings.stage_models.get(stage)
        if stage_model:
            return stage_model
        models = self.list_models()
        if not models:
            return None

        def score(model: dict[str, Any]) -> tuple[int, str]:
            model_id = str(model.get("id") or model.get("name") or model.get("model") or "")
            lower = model_id.lower()
            model_type = str(model.get("type") or "").lower()
            is_embedding = "embed" in lower or model_type == "embeddings"
            is_visual = any(token in lower for token in ["vision", "vl", "image"])
            is_loaded = str(model.get("state", "")).lower() == "loaded"
            return (
                0 if is_loaded and not is_embedding and not is_visual else 1 if not is_embedding and not is_visual else 2,
                model_id,
            )

        selected = sorted(models, key=score)[0]
        return str(selected.get("id") or selected.get("name") or selected.get("model") or "").strip() or None

    def chat(
        self,
        stage: str,
        messages: list[dict[str, str]],
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        json_mode: bool | None = None,
        json_schema: dict[str, Any] | None = None,
    ) -> str:
        model_name = self.choose_model(stage, model)
        if not model_name:
            raise RuntimeError("LM Studio is available but no chat-capable model could be selected.")
        payload = {
            "model": model_name,
            "messages": messages,
            "temperature": self.settings.temperature if temperature is None else temperature,
            "max_tokens": self.settings.max_tokens if max_tokens is None else max_tokens,
        }
        # Constrained decoding is the durable fix for "Extra data: line N" -
        # the model cannot append commentary after the object because the
        # sampler will not let it. A schema constrains shape as well as syntax.
        want_json = self.settings.json_mode if json_mode is None else json_mode
        if json_schema:
            payload["response_format"] = {
                "type": "json_schema",
                "json_schema": {"name": stage, "strict": True, "schema": json_schema},
            }
        elif want_json:
            payload["response_format"] = {"type": "json_object"}
        # The first request of a run absorbs model loading; give it room.
        timeout = self.settings.timeout_seconds
        if not self._warmed_up:
            timeout = max(timeout, self.settings.warmup_timeout_seconds)
        try:
            response = self._request_json("POST", "/chat/completions", payload, timeout=timeout)
        except Exception:
            # Some builds reject response_format for models without a grammar
            # backend. Retry once unconstrained rather than losing the stage.
            if "response_format" not in payload:
                raise
            payload.pop("response_format")
            response = self._request_json("POST", "/chat/completions", payload, timeout=timeout)
        self._warmed_up = True
        choices = response.get("choices", [])
        if not choices:
            raise RuntimeError("LM Studio returned no choices.")
        message = choices[0].get("message", {})
        content = message.get("content")
        if not isinstance(content, str):
            raise RuntimeError("LM Studio returned a non-text chat response.")
        return content
