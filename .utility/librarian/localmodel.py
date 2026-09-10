"""Local models, given one small job at a time.

## The rule this module exists to enforce

> **Open analysis, strict return.**

A scouting prompt must not tell the model what the catalogue hopes to hear.
*"Is this a good donor for a CSI pipeline?"* gets agreement, because a small
model asked a leading question agrees. *"What is this, and what is it made of?"*
gets a description, and a description can be wrong in ways that are visible.

So the instruction is open-ended and the **return is closed**: an enumeration,
a bounded list, a fixed set of keys, validated on arrival and refused if it does
not conform. That is `OPEN_ANALYSIS_STRICT_RETURN`, and it is the whole reason a
7B model can be trusted with the data layer while being kept away from the
information layer.

## One task, one chunk, no pipeline

Nothing here tells a model about briefs, staging, promotion or the catalogue's
purpose. Each call states a single job, hands over a single chunk, and names
the shape of the answer. A model that does not know it is part of a pipeline
cannot try to be helpful about the pipeline — which is the failure mode that
produces confident nonsense in the fields nobody checks.

That also means every call is independent: no history, no accumulated context,
and a failure in one costs one retry rather than a run.

## Profiles

Different jobs want different settings, and `temperature` is the important one.
Choosing from a closed enumeration is not a creative act and runs at 0. Writing
bullets from a file listing runs slightly above it, because 0 makes small models
repeat one phrase. Nothing here runs at the adapter's default.

Model *selection* is a hint rather than a pin: `model_hint` matches loaded
models by substring, and falls back to whatever is loaded. A profile that
demanded a model nobody has would stop the run, and stopping the run is worse
than running on the model that is there and saying which one it was.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Callable

MAX_REPAIR_ATTEMPTS = 1

# Never a chat model, whatever it sorts as. LM Studio reports `state: None` and
# `type: None` for every model on this install, so the adapter's "prefer a
# loaded chat model" scoring degenerates to alphabetical order - which picked a
# DAG model and sat for eleven minutes JIT-loading it. Exclusion by name is
# crude and is the only signal actually available.
NOT_CHAT = ("embed", "embedding", "rerank", "-vl", "vision", "ocr", "tts",
            "text_to_speech", "text-to-speech", "speech", "whisper", "clip",
            "diffusion", "sd-", "flux", "dag-")

# Task roles, in preference order, matched as substrings against loaded model
# ids. A role is a hint about *size and job*, not a pin: choosing from a
# four-value enumeration wants the smallest instruct model that can read, and
# writing bullets wants a little more. Override per task in
# `library_config.json` under `lmstudio.models`.
ROLE_PREFERENCE: dict[str, tuple[str, ...]] = {
    # short, deterministic, closed-vocabulary answers
    "fast": ("qwen3-4b", "qwen2.5-3b", "llama-3.2-3b", "phi-4-mini",
             "gemma-3-4b", "mistral-7b", "qwen3-8b"),
    # a few sentences of description from documentation
    "standard": ("qwen3-8b", "qwen3.5-9b", "mistral-7b", "gemma-4",
                 "qwen2.5-14b", "qwen3-4b"),
}


class ModelRefused(RuntimeError):
    """The model did not return the shape the task requires.

    Raised rather than returned as a partial, because a half-filled record is
    the thing that reaches the catalogue looking finished.
    """


class ModelUnavailable(RuntimeError):
    """No local model could be reached. Every caller degrades rather than dies."""


@dataclass(frozen=True)
class Profile:
    """How one task is run. Everything tunable about a call lives here."""

    task: str
    purpose: str
    schema: dict[str, Any]
    temperature: float = 0.0
    max_tokens: int = 512
    # Substring matched against the ids LM Studio reports. A hint, never a pin.
    model_hint: str = ""
    # Which preference list to walk when no explicit hint is configured.
    role: str = "fast"
    # How much of a chunk this task may see. Small on purpose: a task that
    # needs the whole repository is not decomposed enough.
    chunk_chars: int = 6000

    def clip(self, text: str) -> str:
        text = (text or "").strip()
        if len(text) <= self.chunk_chars:
            return text
        # Cut at a line boundary so the model never sees half a token of code.
        head = text[: self.chunk_chars]
        cut = head.rfind("\n")
        return (head[:cut] if cut > self.chunk_chars // 2 else head) + \
            "\n[... truncated ...]"


# --------------------------------------------------------------- the client

class LocalModel:
    """A thin, testable wrapper. The adapter does the transport."""

    def __init__(self, chat: Callable[..., str] | None = None,
                 models: list[str] | None = None,
                 configured: dict[str, str] | None = None):
        self._chat = chat
        self._models = models or []
        self._configured = {k: v for k, v in (configured or {}).items() if v}
        self.calls: list[dict[str, Any]] = []

    # -- construction ------------------------------------------------------

    @classmethod
    def connect(cls, base_url: str = "") -> "LocalModel":
        """Reach LM Studio through the existing adapter.

        Raises `ModelUnavailable` with the adapter's own reason, which already
        distinguishes *the server is not running* from *the app is open but the
        local server was never started* — a distinction that costs an hour the
        first time nobody makes it.
        """
        try:
            from adapters.lmstudio import LMStudioClient, LMStudioSettings
        except ImportError as exc:                          # pragma: no cover
            raise ModelUnavailable(f"cannot import the LM Studio adapter: {exc}")

        settings = LMStudioSettings.from_config(_adapter_config())
        if base_url:
            settings = LMStudioSettings(**{**settings.__dict__,
                                           "base_url": base_url})
        client = LMStudioClient(settings)
        available, reason = client.availability()
        if not available:
            raise ModelUnavailable(reason)

        ids = [str(m.get("id") or "") for m in client.list_models()]
        return cls(chat=client.chat, models=[i for i in ids if i],
                   configured=dict(settings.stage_models))

    # -- the one call ------------------------------------------------------

    def run(self, profile: Profile, chunk: str, *,
            question: str = "") -> dict[str, Any]:
        """One task, one chunk, validated on return.

        On a malformed answer the validation error is handed back once and the
        task retried. A second failure refuses: a model that cannot produce
        four enum values after being told exactly what is wrong is not going to
        on the third attempt, and pretending otherwise burns an overnight run.
        """
        if self._chat is None:
            raise ModelUnavailable("no local model is connected")

        system = _system_prompt(profile)
        user = _user_prompt(profile, chunk, question)
        messages = [{"role": "system", "content": system},
                    {"role": "user", "content": user}]

        problems = ""
        for attempt in range(MAX_REPAIR_ATTEMPTS + 1):
            if problems:
                messages = messages[:2] + [{
                    "role": "user",
                    "content": (f"That did not match the required shape: "
                                f"{problems}\nReturn only the JSON object, "
                                f"corrected.")}]
            raw = self._chat(
                profile.task, messages,
                model=self.pick(profile), temperature=profile.temperature,
                max_tokens=profile.max_tokens, json_schema=profile.schema)
            self.calls.append({"task": profile.task, "attempt": attempt})
            parsed, problems = _parse(raw, profile.schema)
            if not problems:
                return parsed

        raise ModelRefused(
            f"{profile.task}: the model did not return the required shape after "
            f"{MAX_REPAIR_ATTEMPTS + 1} attempts ({problems}). Nothing was "
            f"recorded; a partial record is worse than a missing one.")

    def pick(self, profile: Profile) -> str | None:
        """Choose a model for this task, in three descending steps.

        1. an explicit id configured for the task in `library_config.json`;
        2. the profile's own hint, or its role's preference list;
        3. the first loaded model that is not obviously not a chat model.

        Step three exists because the adapter's own fallback is alphabetical
        when LM Studio reports no load state, and alphabetical picked a DAG
        model that took eleven minutes to load and never answered.
        """
        if not self._models:
            return None

        configured = self._configured.get(profile.task)
        if configured:
            return configured

        chat = [m for m in self._models if not self._excluded(m)]
        for hint in ([profile.model_hint] if profile.model_hint
                     else ROLE_PREFERENCE.get(profile.role, ())):
            for model_id in chat:
                if hint.lower() in model_id.lower():
                    return model_id
        return chat[0] if chat else None

    @staticmethod
    def _excluded(model_id: str) -> bool:
        low = model_id.lower()
        return any(token in low for token in NOT_CHAT)


def _adapter_config() -> dict[str, Any]:
    from .config import UTILITY_ROOT

    path = UTILITY_ROOT / "library_config.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


# ------------------------------------------------------------- the prompts

def _system_prompt(profile: Profile) -> str:
    """Deliberately short, and deliberately silent about the wider system.

    Three things only: the job, the evidence rule, and the shape. Anything
    about *why* the catalogue wants this invites the model to be helpful about
    the catalogue, and a model being helpful about something it cannot see is
    how a guess arrives wearing the clothes of a fact.
    """
    return (
        f"You describe software from evidence. Your task: {profile.purpose}\n\n"
        "Rules:\n"
        "- Use only what is in the text you are given. You have no other "
        "knowledge of this project.\n"
        "- If the text does not say, choose the least committed option the "
        "schema allows, or leave the field empty. Do not infer.\n"
        "- Do not judge whether the project is good, popular or worth using.\n"
        "- Reply with one JSON object matching the schema. No prose, no "
        "explanation, no markdown fence."
    )


def _user_prompt(profile: Profile, chunk: str, question: str) -> str:
    ask = question or "Describe what this is, from the evidence below."
    return f"{ask}\n\n---\n{profile.clip(chunk)}\n---"


# ------------------------------------------------------------ the contract

FENCE = re.compile(r"^\s*```(?:json)?\s*|\s*```\s*$", re.I)


def _parse(raw: str, schema: dict[str, Any]) -> tuple[dict[str, Any], str]:
    """Parse and check. Returns `(value, problems)`; problems empty means good.

    The schema is checked here as well as being sent for constrained decoding,
    because `response_format` is dropped on a retry when a build rejects it —
    so trusting the sampler alone would mean the one path that most needs
    checking is the one path with none.
    """
    text = FENCE.sub("", (raw or "").strip())
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        return {}, "no JSON object in the reply"
    try:
        value = json.loads(text[start:end + 1])
    except json.JSONDecodeError as exc:
        return {}, f"invalid JSON ({exc})"
    if not isinstance(value, dict):
        return {}, "the reply was not a JSON object"

    problems = _check(value, schema)
    return (value, "; ".join(problems)) if problems else (value, "")


def _check(value: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    properties = schema.get("properties", {})
    for name in schema.get("required", []):
        if name not in value:
            problems.append(f"missing '{name}'")

    for name, rule in properties.items():
        if name not in value:
            continue
        problems += _check_one(name, value[name], rule)
    return problems


def _check_one(name: str, item: Any, rule: dict[str, Any]) -> list[str]:
    kind = rule.get("type")
    if kind == "string":
        if not isinstance(item, str):
            return [f"'{name}' must be a string"]
        if rule.get("enum") and item not in rule["enum"]:
            return [f"'{name}' must be one of {rule['enum']}, not {item!r}"]
        if rule.get("maxLength") and len(item) > rule["maxLength"]:
            return [f"'{name}' is longer than {rule['maxLength']} characters"]
    elif kind == "array":
        if not isinstance(item, list):
            return [f"'{name}' must be an array"]
        if rule.get("maxItems") and len(item) > rule["maxItems"]:
            return [f"'{name}' has more than {rule['maxItems']} items"]
        problems = []
        for element in item:
            problems += _check_one(f"{name}[]", element, rule.get("items", {}))
        return problems
    elif kind == "boolean" and not isinstance(item, bool):
        return [f"'{name}' must be true or false"]
    elif kind == "integer" and not isinstance(item, int):
        return [f"'{name}' must be an integer"]
    return []


# --------------------------------------------------------------- reporting

@dataclass
class RunLog:
    """What a population run did, kept so an unattended job is auditable.

    Counting refusals separately from errors matters: a refusal means the model
    would not produce the shape, which is a model or prompt problem; an error
    means the network or the API failed, which is not.
    """

    considered: int = 0
    screened_out: int = 0
    proposed: int = 0
    refused: int = 0
    errors: int = 0
    notes: list[str] = field(default_factory=list)

    def say(self, line: str) -> None:
        self.notes.append(line)

    def summary(self) -> str:
        return (f"considered {self.considered}, screened out {self.screened_out}, "
                f"proposed {self.proposed}, model refusals {self.refused}, "
                f"errors {self.errors}")
