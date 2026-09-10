"""The local-model layer: strict returns, decomposed tasks, offline runs.

No test here reaches LM Studio or GitHub. The model is a scripted fake and the
fetchers are injected, following the `FakeLM` pattern the scout tests already
use — which is what makes it possible to assert *what happens when the model
misbehaves*, the case that matters most and is the hardest to provoke against a
real one.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from librarian import brief as brief_mod
from librarian import content_model, enrich, populate, propose as propose_mod
from librarian import scouttasks
from librarian.localmodel import (LocalModel, ModelRefused, Profile, RunLog,
                                  _parse)


# --------------------------------------------------------------- the contract

SHAPE = {
    "type": "object",
    "properties": {
        "value": {"type": "string", "enum": ["a", "b"]},
        "bullets": {"type": "array", "maxItems": 2,
                    "items": {"type": "string", "maxLength": 10}},
        "confident": {"type": "boolean"},
    },
    "required": ["value"],
}


def test_a_fenced_reply_is_still_parsed():
    """Small models fence their JSON however the schema is declared."""
    value, problems = _parse('```json\n{"value": "a"}\n```', SHAPE)
    assert not problems and value == {"value": "a"}


def test_prose_around_the_object_is_tolerated_but_a_missing_object_is_not():
    value, problems = _parse('Sure! {"value": "b"} Hope that helps.', SHAPE)
    assert not problems and value["value"] == "b"

    _, problems = _parse("I cannot answer that.", SHAPE)
    assert "no JSON object" in problems


def test_a_value_outside_the_enumeration_is_a_problem_not_a_result():
    """The whole point of `OPEN_ANALYSIS_STRICT_RETURN`. The model may consider
    anything; it may only *return* a value the caller declared."""
    _, problems = _parse('{"value": "maybe"}', SHAPE)
    assert "must be one of" in problems


def test_the_declared_limits_are_enforced_not_merely_sent():
    """`response_format` is dropped on retry when a build rejects it, so the
    one path that most needs checking would otherwise have none."""
    _, problems = _parse('{"value": "a", "bullets": ["x", "y", "z"]}', SHAPE)
    assert "more than 2 items" in problems

    _, problems = _parse('{"value": "a", "bullets": ["far too long to fit"]}', SHAPE)
    assert "longer than 10" in problems

    _, problems = _parse('{"value": "a", "confident": "yes"}', SHAPE)
    assert "must be true or false" in problems


def test_a_missing_required_key_is_named():
    _, problems = _parse('{"confident": true}', SHAPE)
    assert "missing 'value'" in problems


# ------------------------------------------------------------------ the run

class Scripted:
    """A model that returns whatever the script says, in order."""

    def __init__(self, *replies: str):
        self.replies = list(replies)
        self.seen: list[list[dict[str, str]]] = []

    def __call__(self, stage, messages, **kwargs):
        self.seen.append(messages)
        return self.replies.pop(0) if self.replies else "{}"


PROFILE = Profile(task="t", purpose="pick a letter", schema=SHAPE)


def test_a_good_reply_comes_back_parsed():
    model = LocalModel(chat=Scripted('{"value": "a"}'))
    assert model.run(PROFILE, "some evidence")["value"] == "a"


def test_a_bad_reply_is_retried_once_with_the_reason():
    """The repair turn hands the validation error back. A model told exactly
    what is wrong usually fixes it; one that does not, will not."""
    chat = Scripted('{"value": "nonsense"}', '{"value": "b"}')
    model = LocalModel(chat=chat)
    assert model.run(PROFILE, "evidence")["value"] == "b"

    repair = chat.seen[1][-1]["content"]
    assert "did not match" in repair and "must be one of" in repair


def test_two_bad_replies_refuse_rather_than_returning_a_partial():
    """A half-filled record is the thing that reaches the catalogue looking
    finished."""
    model = LocalModel(chat=Scripted('{"value": "x"}', '{"value": "y"}'))
    with pytest.raises(ModelRefused) as caught:
        model.run(PROFILE, "evidence")
    assert "did not return the required shape" in str(caught.value)


def test_the_prompt_never_mentions_the_catalogue_or_the_pipeline():
    """A model that knows it is filling in a form tries to fill in the form.

    Nothing in a task prompt may reference briefs, staging, promotion or what
    the catalogue is for - the fields nobody checks are where that shows.
    """
    chat = Scripted('{"value": "a"}')
    LocalModel(chat=chat).run(PROFILE, "evidence")
    text = " ".join(m["content"] for m in chat.seen[0]).lower()
    for word in ("catalogue", "brief", "staging", "promote", "vault",
                 "obsidian", "note"):
        assert word not in text, f"the task prompt leaks '{word}'"


def test_the_prompt_forbids_judging_the_project():
    chat = Scripted('{"value": "a"}')
    LocalModel(chat=chat).run(PROFILE, "evidence")
    system = chat.seen[0][0]["content"].lower()
    assert "do not judge" in system
    assert "use only what is in the text" in system


def test_a_chunk_is_clipped_at_a_line_boundary():
    profile = Profile(task="t", purpose="p", schema=SHAPE, chunk_chars=40)
    clipped = profile.clip("\n".join(f"line {i} of text" for i in range(20)))
    assert "truncated" in clipped
    assert len(clipped) < 200
    assert not clipped.split("[...")[0].endswith("lin")


def test_classification_runs_at_zero_temperature():
    """Choosing from a closed enumeration is not a creative act."""
    profile = scouttasks.axis_profile("license_class", ["Permissive", "Unknown"])
    assert profile.temperature == 0.0
    assert scouttasks.SCREEN.temperature == 0.0
    # Description sits just above zero: at 0 a small model repeats one phrase.
    assert 0 < scouttasks.MECHANICS.temperature < 0.5


def test_the_model_hint_is_a_hint_and_never_a_pin():
    """A profile that demanded a model nobody has would stop the run, which is
    worse than running on what is loaded and recording which it was."""
    model = LocalModel(chat=Scripted(), models=["qwen3-8b", "nomic-embed"])
    assert model.pick(Profile("t", "p", SHAPE, model_hint="qwen")) == "qwen3-8b"
    # An unmatched hint falls through to whatever chat model is loaded rather
    # than returning nothing and letting the adapter sort alphabetically.
    assert model.pick(Profile("t", "p", SHAPE, model_hint="llama")) == "qwen3-8b"


def test_a_model_that_is_obviously_not_a_chat_model_is_never_chosen():
    """LM Studio reports `state: None` for every model on this install, so the
    adapter's "prefer a loaded chat model" scoring degenerates to alphabetical
    order. It picked `dag-llama3` and sat for eleven minutes loading it."""
    model = LocalModel(chat=Scripted(),
                       models=["dag-llama3", "nomic-embed-text",
                               "unlimited-ocr", "qwen/qwen3-vl-4b",
                               "orpeus_text_to_speech", "qwen/qwen3-4b"])
    assert model.pick(Profile("t", "p", SHAPE)) == "qwen/qwen3-4b"


def test_a_role_walks_its_preference_list():
    """Choosing from a four-value enumeration wants the smallest instruct model
    that can read; writing bullets wants a little more."""
    models = ["qwen/qwen3-8b", "qwen/qwen3-4b"]
    model = LocalModel(chat=Scripted(), models=models)
    assert model.pick(Profile("t", "p", SHAPE, role="fast")) == "qwen/qwen3-4b"
    assert model.pick(Profile("t", "p", SHAPE, role="standard")) == "qwen/qwen3-8b"


def test_an_explicit_configuration_beats_every_heuristic():
    """`library_config.json` pins a model per task so a run is reproducible."""
    model = LocalModel(chat=Scripted(), models=["qwen/qwen3-4b", "big-model"],
                       configured={"screen": "big-model"})
    assert model.pick(Profile("screen", "p", SHAPE)) == "big-model"
    assert model.pick(Profile("other", "p", SHAPE)) == "qwen/qwen3-4b"


# ------------------------------------------------------------- the questions

def test_the_screen_asks_for_a_contradiction_not_for_approval():
    """Asked whether something is suitable a small model says yes. Asked what
    the text contradicts, it has to point at a sentence."""
    question = scouttasks.screen_question("a CSI model", ["must not assume ESP32"])
    assert "contradict" in question
    assert "must not assume ESP32" in question
    assert "unclear" in question, "abstaining must be offered as normal"


def test_unclear_is_a_permitted_verdict():
    """Forcing a binary out of a model that cannot tell is how a source gets
    charted positively when the evidence never said."""
    assert "unclear" in scouttasks.SCREEN.schema["properties"]["verdict"]["enum"]


def test_every_axis_the_vault_declares_has_a_question():
    model = content_model.load()
    if not model.axis_values:
        pytest.skip("this vault declares no axes")
    missing = set(model.axis_values) - set(scouttasks.AXIS_QUESTIONS)
    assert not missing, f"axes with no plain-language question: {sorted(missing)}"


def test_a_survey_is_rendered_as_shape_not_as_paths():
    """A model given four thousand paths describes the first twenty."""
    chunk = scouttasks.survey_chunk({
        "file_count": 210,
        "directories": {"src": 100, "tests": 60, "docs": 50},
        "extensions": {".py": 150, ".md": 40},
        "root_files": ["README.md", "pyproject.toml"]})
    assert "210" in chunk and "src: 100" in chunk and ".py: 150" in chunk
    assert len(chunk) < 1000


# ------------------------------------------------------------- grounding

def test_an_invented_name_is_dropped():
    """The live run produced 'Uses tree-sitter for parsing' for a project whose
    documentation never mentions tree-sitter — in a section a machine is
    allowed to write. Allowing that section requires checking it."""
    from librarian.derive import grounded

    source = ("A SQL parser that produces a Concrete Syntax Tree preserving "
              "comments and whitespace. Written in TypeScript.")
    kept, dropped = grounded([
        "Produces a Concrete Syntax Tree",
        "Preserves comments and whitespace",
        "Uses tree-sitter for parsing",
    ], source)
    assert "Uses tree-sitter for parsing" in dropped
    assert len(kept) == 2


def test_grounding_keeps_paraphrase_and_drops_fabrication():
    from librarian.derive import grounded

    source = "Reads jobs from disk, retries failed ones, and exposes a CLI."
    kept, dropped = grounded(["Retries failed jobs", "Exposes a CLI",
                              "Integrates with Kubernetes and Prometheus"],
                             source)
    assert len(kept) == 2 and len(dropped) == 1


def test_grounding_does_not_drop_a_bullet_of_common_words():
    from librarian.derive import grounded

    kept, dropped = grounded(["It can be used with the data"], "anything")
    assert kept and not dropped


# --------------------------------------------------------------- derivation

def test_a_declared_licence_is_classified_not_guessed():
    from librarian.derive import derive_axes

    assert derive_axes({"license_spdx": "GPL-3.0"}, {})["license_class"] == "Copyleft"
    assert derive_axes({"license_spdx": "MIT"}, {})["license_class"] == "Permissive"
    assert "license_class" not in derive_axes({}, {})


def test_an_unmapped_language_is_left_for_a_person():
    """Ruby has no value in this vault's enumeration. Forcing it into `Mixed`
    would say something false about a single-language repository.

    This test named TypeScript until 2026-09-09, when six languages were added
    to the enumeration precisely because leaving them unmapped emptied the axis
    on nearly every source of a real intake. The property is unchanged; the
    example had to move because the taxonomy did.
    """
    from librarian.derive import derive_axes

    assert "ecosystem" not in derive_axes({"language": "Ruby"}, {})
    assert derive_axes({"language": "Go"}, {})["ecosystem"] == "Go"


def test_the_languages_added_on_2026_09_09_all_derive():
    """Added to the enumeration deliberately; a mapping that did not follow
    would leave the axis exactly as empty as before."""
    from librarian import content_model
    from librarian.derive import derive_axes

    permitted = content_model.load().axis_values
    if "ecosystem" not in permitted:
        pytest.skip("this vault declares no ecosystem enumeration")
    for language, expected in (("Rust", "Rust"), ("TypeScript", "TypeScript"),
                               ("JavaScript", "JavaScript"), ("Java", "Java"),
                               ("C#", "CSharp"), ("C++", "CPlusPlus")):
        got = derive_axes({"language": language}, {}, "x",
                          permitted=permitted).get("ecosystem")
        assert got == expected, f"{language} derived {got!r}"


def test_no_permitted_value_carries_punctuation_the_tokenizer_eats():
    """`C#` and `C++` both reduce to the single token `c` under FTS5's
    `porter unicode61`, so a search for one matches the other and every stray
    `c` besides. Measured before the values were chosen, and pinned here so the
    next addition does not quietly reintroduce it."""
    from librarian import content_model

    values = content_model.load().axis_values.get("ecosystem", ())
    bad = [v for v in values if not v.replace("_", "").isalnum()]
    assert not bad, f"unsearchable enum values: {bad}"


def test_the_extension_histogram_is_the_fallback_for_ecosystem():
    from librarian.derive import derive_axes

    axes = derive_axes({}, {"extensions": {".md": 5, ".py": 200}})
    assert axes["ecosystem"] == "Python"


def test_archived_and_stale_both_read_as_abandoned():
    from librarian.derive import derive_axes

    assert derive_axes({"archived": True}, {})["maturity_stage"] == "Abandoned"
    assert derive_axes({"pushed_at": "2019-01-01T00:00:00Z"},
                       {})["maturity_stage"] == "Abandoned"
    assert derive_axes({"pushed_at": "2026-08-30T00:00:00Z"},
                       {})["maturity_stage"] == "Active"


def test_only_the_negative_gpu_case_is_derived():
    """Text mentioning CUDA might still run on a CPU; text mentioning nothing
    of the sort is not a GPU project."""
    from librarian.derive import derive_axes

    assert derive_axes({}, {}, "a pure python parser")["hardware_footprint"] == "CPU_Only"
    assert "hardware_footprint" not in derive_axes({}, {}, "requires CUDA 12")


def test_a_derived_value_outside_the_enumeration_is_dropped():
    """`NO_SCHEMA_DRIFT` applies to derivation too, not only to the model."""
    from librarian.derive import derive_axes

    axes = derive_axes({"license_spdx": "MIT"}, {},
                       permitted={"license_class": frozenset({"Copyleft"})})
    assert "license_class" not in axes


def test_the_licence_file_is_read_when_the_api_will_not_say():
    """GitHub reports no usable licence for a great many repositories that
    plainly have one. Stopping at the API field left `license_class` empty on
    most of a real batch — and that field is what `find_donor` eliminates on,
    so an empty one removes the source from every constrained answer."""
    from librarian.derive import derive_axes

    mit = ("MIT License\n\nPermission is hereby granted, free of charge, to "
           "any person obtaining a copy of this software")
    assert derive_axes({}, {}, "x", licence_text=mit)["license_class"] == "Permissive"

    # a declared SPDX still wins: it is the stronger evidence
    assert derive_axes({"license_spdx": "GPL-3.0"}, {}, "x",
                       licence_text=mit)["license_class"] == "Copyleft"


def test_unknown_is_recorded_once_we_have_actually_looked():
    """`EVIDENCE_REQUIRED` says Unknown is a valid value. Having read the
    LICENSE and the readme and found nothing is a finding, not a gap."""
    from librarian.derive import derive_axes

    assert derive_axes({}, {}, "a parser with no licence statement"
                       )["license_class"] == "Unknown"


def test_security_compliance_asks_what_the_material_is_not_how_safe_it_is():
    """The enumeration is two values and one is the default. `Uncertified`
    does not mean we checked and it failed."""
    from librarian.derive import derive_axes

    assert derive_axes({}, {}, "a framework for penetration testing and "
                       "payload generation")["security_compliance"] == "Security_Adjacent"
    assert derive_axes({}, {}, "a markdown table formatter"
                       )["security_compliance"] == "Uncertified"


def test_every_derived_axis_is_declared_in_DERIVED_AXES():
    """The split between derived and asked is asserted, not described. An axis
    derived here but absent from the tuple would be asked *and* derived, and
    the model's answer would silently win or lose depending on dict order."""
    from librarian import derive

    produced = set(derive.derive_axes(
        {"license_spdx": "MIT", "language": "Go", "pushed_at": "2026-08-01T00:00:00Z"},
        {}, "a plain tool"))
    assert produced <= set(derive.DERIVED_AXES), produced - set(derive.DERIVED_AXES)


# ------------------------------------------------- agent_surface, a path ladder

def test_the_agent_surface_ladder_reads_paths_not_prose():
    """[[Note Content Model]] defines this axis as a ladder of paths, and says
    a source is recorded at the highest rung it reaches. Putting it to a model
    was the same error as putting the licence to one."""
    from librarian.derive import agent_surface

    assert agent_surface(["src/main.py", "README.md"]) == "None"
    assert agent_surface(["AGENTS.md", "src/main.py"]) == "Documented"
    assert agent_surface([".claude/settings.json"]) == "Documented"
    assert agent_surface([".agents/skills/audit/SKILL.md"]) == "Procedural"
    assert agent_surface([".mcp.json"]) == "Callable"


def test_the_highest_rung_wins():
    from librarian.derive import agent_surface

    both = [".agents/skills/audit/SKILL.md", "AGENTS.md"]
    assert agent_surface(both) == "Procedural"
    assert agent_surface(both + ["pkg/_mcp/server.py"]) == "Callable"


def test_a_repository_named_mcp_is_callable():
    """`semgrep/mcp` was charted `Callable` and derived `None`, because its
    MCP-ness is in the name rather than in any of the ten sampled paths. The
    name is evidence."""
    from librarian.derive import agent_surface

    assert agent_surface(["README.md"], repo_key="semgrep/mcp") == "Callable"
    assert agent_surface(["README.md"], repo_key="wshobson/maverick-mcp") == "Callable"
    assert agent_surface(["README.md"], repo_key="acme/mcphersons") == "None"


def test_a_passing_mention_of_mcp_is_not_an_mcp_server():
    """Matching `mcp` anywhere in a path would call every repository with a
    test fixture or a CI job an agent-invocable interface."""
    from librarian.derive import agent_surface

    assert agent_surface([".github/workflows/pr-tests-mcp.yml"]) == "None"
    assert agent_surface(["docs/mcp-notes.md"]) == "None"


def test_agent_surface_is_omitted_when_there_is_no_listing_to_read():
    """`None` is a permitted value meaning *we looked and there is none*.
    Returning it with no paths would be a claim rather than an absence."""
    from librarian.derive import derive_axes

    assert "agent_surface" not in derive_axes({}, {}, "x")
    assert derive_axes({}, {}, "x", paths=["src/a.py"])["agent_surface"] == "None"


def test_the_extension_histogram_is_read_in_the_shape_the_survey_writes():
    """`scout.survey.shape` writes `['.py (150)']`, not a mapping. Both the
    ecosystem fallback and the prose rule tested `isinstance(dict)` and so did
    nothing at all against a live survey - a silent no-op."""
    from librarian.derive import derive_axes, extension_counts

    assert extension_counts({"extensions": [".py (150)", ".md (30)"]}) == \
        {".py": 150, ".md": 30}
    assert extension_counts({"extensions": {".py": 150}}) == {".py": 150}
    assert derive_axes({}, {"extensions": [".rs (600)", ".md (30)"]},
                       "x")["ecosystem"] == "Rust"


def test_interface_protocol_is_not_in_the_derived_set():
    """Measured and rejected: 0.409 accuracy on the 22 of 45 hand-charted
    sources it would answer, and the prose branch never exceeded 0.80
    precision across a seven-point threshold sweep. For an axis `find_donor`
    eliminates on, one wrong value in five is worse than an empty one.

    Pinned so a future attempt has to be wired in deliberately rather than
    drifting back."""
    from librarian import derive

    assert "interface_protocol" not in derive.DERIVED_AXES
    produced = derive.derive_axes(
        {"license_spdx": "MIT", "language": "Go"}, {"extensions": [".md (99)"]},
        "docs", paths=["README.md"])
    assert "interface_protocol" not in produced
