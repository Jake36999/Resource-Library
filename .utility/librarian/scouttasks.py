"""The decomposed jobs a local model is given, one at a time.

Every task here is small enough that a 7B model can do it reliably, and none of
them knows about any other. A task receives a chunk and returns a shape. It is
never told what the catalogue is for, which brief it is serving, or what will
happen to its answer — because a model that knows it is filling in a form tries
to fill in the form, and the fields nobody checks are where that shows.

## Why one axis per call

Ten enumerations in one reply is where small models fail: they drift to the
first plausible value, repeat a value across axes, or invent a compromise.
Asked *"which of these four words describes how mature this is"* with the four
words in front of them, they are reliable.

Ten calls per candidate is slower and free. An overnight local run has time.

## Why the screen comes first

`screen` is the cheapest call and the one that saves the rest. It reads the
brief's disqualifiers — the assumptions a candidate must not make — against the
README, and returns `keep`, `reject` or `unclear`. `unclear` is a real answer:
forcing a binary out of a model that cannot tell is how RuView gets charted
positively.
"""
from __future__ import annotations

from typing import Any

from .localmodel import Profile

MAX_BULLETS = 6
BULLET_CHARS = 160


def _bullets(name: str, max_items: int = MAX_BULLETS) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            name: {"type": "array", "maxItems": max_items,
                   "items": {"type": "string", "maxLength": BULLET_CHARS}},
        },
        "required": [name],
    }


# ------------------------------------------------------------ 1. the screen

SCREEN = Profile(
    task="screen",
    purpose=("decide whether a project contradicts any of the stated "
             "constraints"),
    temperature=0.0,
    max_tokens=300,
    chunk_chars=5000,
    schema={
        "type": "object",
        "properties": {
            "verdict": {"type": "string", "enum": ["keep", "reject", "unclear"]},
            "reason": {"type": "string", "maxLength": 300},
            "contradicts": {"type": "array", "maxItems": 5,
                            "items": {"type": "string", "maxLength": 200}},
        },
        "required": ["verdict", "reason"],
    },
)


def screen_question(need: str, disqualifiers: list[str]) -> str:
    """The one prompt that is allowed to know what was asked for.

    Even here the framing is negative: the model is asked what the text
    *contradicts*, not whether the project is suitable. Asked for suitability a
    small model says yes; asked for a contradiction it has to point at a
    sentence.
    """
    rules = "\n".join(f"- {d}" for d in disqualifiers)
    return (
        "Someone is looking for software that meets this description:\n"
        f"  {need}\n\n"
        "It must not do any of the following:\n"
        f"{rules}\n\n"
        "Read the project text below. Does anything in it contradict one of "
        "those constraints?\n"
        "- 'reject' only if the text states something that contradicts one, and "
        "quote it in `contradicts`.\n"
        "- 'unclear' if the text does not say either way. This is a normal "
        "answer; most texts will not say.\n"
        "- 'keep' if the text positively shows it does not contradict them.\n"
        "Do not judge quality, popularity or whether it is a good idea."
    )


# ------------------------------------------------------- 2. the axis picker

def axis_profile(axis: str, values: list[str]) -> Profile:
    """One enumeration, in front of the model, with nothing else to decide."""
    return Profile(
        task=f"axis:{axis}",
        purpose=f"choose the single value of '{axis}' that the evidence supports",
        temperature=0.0,
        max_tokens=200,
        chunk_chars=5000,
        schema={
            "type": "object",
            "properties": {
                "value": {"type": "string", "enum": sorted(values)},
                "evidence": {"type": "string", "maxLength": 200},
                "confident": {"type": "boolean"},
            },
            "required": ["value", "confident"],
        },
    )


AXIS_QUESTIONS: dict[str, str] = {
    "ecosystem": "Which language or platform is most of this project written "
                 "in or built for?",
    "domain_primary": "What subject area is this project about?",
    "maturity_stage": "What state is this project in? "
                      "'Reference' means it is documentation or a list rather "
                      "than running code. 'Abandoned' means the text or dates "
                      "say it is no longer maintained.",
    "license_class": "What kind of licence does the text say this is under? "
                     "Choose 'Unknown' if it does not say.",
    "deployment_target": "Where does this run? 'Local_Only' means on one "
                         "machine, 'Server' means it is hosted for others, "
                         "'Browser' means in a web page, 'Desktop' means an "
                         "installed application.",
    "interface_protocol": "How does a person or program mainly interact with "
                          "it?",
    "data_locality": "Where does its data live? 'Local_First' means on the "
                     "machine that runs it, 'Distributed' means across nodes "
                     "or services, 'Stateless' means it keeps none.",
    "hardware_footprint": "What does it need to run? Choose 'Low_VRAM' only if "
                          "the text mentions a GPU.",
    "security_compliance": "Is this project about security, or does it handle "
                           "security-sensitive material? 'Security_Adjacent' "
                           "if yes, 'Uncertified' otherwise. This is not a "
                           "judgement about whether it is secure.",
    "agent_surface": "Can a program call this? 'Callable' means a documented "
                     "API or library, 'Procedural' means a command line, "
                     "'Documented' means only prose, 'None' means neither.",
}


def axis_question(axis: str) -> str:
    ask = AXIS_QUESTIONS.get(axis, f"Which value of '{axis}' does the evidence support?")
    return (f"{ask}\n\nChoose exactly one value from the list in the schema. "
            f"Set `confident` to false if the text does not really say, and "
            f"quote what you used in `evidence`.")


# ---------------------------------------------------- 3. the two descriptions

INSIDE = Profile(
    task="inside",
    role="standard",
    purpose="say what a repository is made of, from its file listing",
    temperature=0.15,
    max_tokens=600,
    chunk_chars=7000,
    schema=_bullets("bullets"),
)

INSIDE_QUESTION = (
    "Below is a summary of a repository's directories, file extensions and "
    "counts. Write up to six short bullets saying what it is made of.\n"
    "- Every bullet must cite a directory, an extension or a count that "
    "appears below.\n"
    "- Do not say what the project is for; only what is in it.\n"
    "- Do not speculate about code you cannot see."
)

MECHANICS = Profile(
    task="mechanics",
    role="standard",
    purpose="say how a project works, from its own documentation",
    temperature=0.15,
    max_tokens=700,
    chunk_chars=8000,
    schema=_bullets("bullets"),
)

MECHANICS_QUESTION = (
    "Below is a project's own documentation. Write up to six short bullets "
    "describing how it works: what it takes in, what it does, what it "
    "produces, and anything it explicitly requires.\n"
    "- Only state what the text states.\n"
    "- Prefer a specific mechanism over a general claim: 'parses with "
    "tree-sitter' rather than 'uses advanced parsing'.\n"
    "- Leave out marketing sentences, badges and comparisons to other "
    "projects."
)

USES = Profile(
    task="uses",
    role="standard",
    purpose="say where a project is meant to be used, from its documentation",
    temperature=0.15,
    max_tokens=600,
    chunk_chars=8000,
    schema=_bullets("bullets", max_items=4),
)

USES_QUESTION = (
    "Below is a project's own documentation. Write up to four short bullets "
    "describing the situations it says it is for.\n"
    "- Only situations the text names. If it names none, return an empty list.\n"
    "- Do not invent use cases that sound plausible."
)


# ----------------------------------------------------------- 4. the queries

QUERIES = Profile(
    task="queries",
    role="standard",
    purpose="turn a description of a need into search terms",
    temperature=0.3,
    max_tokens=400,
    chunk_chars=2000,
    schema={
        "type": "object",
        "properties": {
            "queries": {"type": "array", "maxItems": 6,
                        "items": {"type": "string", "maxLength": 80}},
        },
        "required": ["queries"],
    },
)

QUERIES_QUESTION = (
    "Below is a description of something someone needs. Write up to six short "
    "search queries that would find open-source projects matching it.\n"
    "- Use the words the field itself uses, not the words in the description.\n"
    "- Vary them: a specific technical term, a general one, a synonym.\n"
    "- Two to five words each. No punctuation, no boolean operators."
)


# ------------------------------------------------------------ 5. the topic

def topic_profile(topics: list[str]) -> Profile:
    return Profile(
        task="topic",
        purpose="file a project under one of an existing set of subject headings",
        temperature=0.0,
        max_tokens=200,
        chunk_chars=4000,
        schema={
            "type": "object",
            "properties": {
                "topic": {"type": "string", "enum": sorted(topics)},
                "confident": {"type": "boolean"},
            },
            "required": ["topic", "confident"],
        },
    )


TOPIC_QUESTION = (
    "Which of the subject headings in the schema does this project belong "
    "under? Choose the closest one even if none is a good fit, and set "
    "`confident` to false when none is."
)


def survey_chunk(survey: dict[str, Any], limit: int = 25) -> str:
    """A file listing rendered small enough to be one chunk.

    Directories and extensions with counts, not paths. A model given four
    thousand paths describes the first twenty; given the shape, it describes
    the repository.
    """
    lines = []
    counts = survey.get("file_count") or survey.get("files")
    if counts:
        lines.append(f"total files: {counts}")
    for key, label in (("directories", "top-level directories"),
                       ("extensions", "file extensions"),
                       ("signals", "material kinds")):
        rows = survey.get(key) or {}
        if isinstance(rows, dict):
            pairs = sorted(rows.items(), key=lambda kv: -_as_int(kv[1]))[:limit]
        elif isinstance(rows, list):
            pairs = [(str(r), "") for r in rows[:limit]]
        else:
            continue
        if pairs:
            lines.append("")
            lines.append(f"{label}:")
            lines += [f"  {name}: {count}" if count != "" else f"  {name}"
                      for name, count in pairs]
    roots = survey.get("root_files") or []
    if roots:
        lines += ["", "files at the root:", "  " + ", ".join(map(str, roots[:30]))]
    return "\n".join(lines) or "no file listing was captured"


def _as_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0
