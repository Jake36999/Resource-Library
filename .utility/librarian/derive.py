"""Axis values that are facts, derived rather than inferred.

## Why this module exists

The first live run of the scouting tasks got four of ten axes wrong, and the
wrong ones were not the hard ones. A model was asked what licence
`sql-parser-cst` is under, with `declared licence: GPL-3.0` sitting in the text
above the question, and answered `Unknown`. It was asked what ecosystem, with
`main language: TypeScript` in front of it, and answered `Python`.

That is not a prompt problem and a bigger model would only hide it. **A field
that can be read off fetched metadata must never be put to a model at all** —
asking is strictly worse than reading, because it converts a fact into a guess
and the guess is indistinguishable from the fact downstream.

`EVIDENCE_REQUIRED` already says this: a factual field comes from a fetched
source. The scouting pipeline had the sources and asked anyway.

## What is left for the model

The five axes below are genuinely interpretive — no metadata field answers
them, and reading the documentation is the only way. Those go to the model,
one at a time, and an unconfident answer is dropped rather than recorded.

| Derived here | From |
| --- | --- |
| `license_class` | the declared SPDX identifier |
| `ecosystem` | the repository's main language, then its file extensions |
| `maturity_stage` | the archived flag and the age of the last push |
| `hardware_footprint` | whether the evidence mentions a GPU at all |

| Left to the model | Why |
| --- | --- |
| `domain_primary` | what a project is *about* is not in its metadata |
| `deployment_target` | a language does not say where it runs |
| `interface_protocol` | needs the documentation |
| `data_locality` | needs the documentation |
| `agent_surface` | needs the documentation |
| `security_compliance` | needs the documentation |
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any, Iterable

# Axes this module answers. Everything else is the model's job, and the split
# is asserted by a test rather than described here and hoped for.
DERIVED_AXES = ("license_class", "ecosystem", "maturity_stage",
                "hardware_footprint", "security_compliance",
                "agent_surface")

# Axes whose definition *is* a set of paths. When there is no listing to read,
# these are left empty rather than put to a model: a model reading a README
# cannot know whether `.claude/skills/` exists, so an answer would be noise
# wearing the clothes of a finding.
PATH_DEFINED = ("agent_surface",)

# A language name to the ecosystem enumeration. Still deliberately incomplete:
# an unmapped language returns nothing and the axis is left for a person, which
# is the honest outcome for a taxonomy with no value for it. Six languages were
# added to the enumeration on 2026-09-09 because the first intake outside the
# original cohort left this axis empty on nearly every source; Ruby, PHP,
# Kotlin, Swift and Haskell still have no home.
LANGUAGE_ECOSYSTEM = {
    "python": "Python",
    "go": "Go",
    "rust": "Rust",
    "typescript": "TypeScript",
    "javascript": "JavaScript",
    "java": "Java",
    "c#": "CSharp", "csharp": "CSharp",
    "c++": "CPlusPlus", "cpp": "CPlusPlus",
    "shell": "Shell", "powershell": "Shell", "batchfile": "Shell",
    "css": "Web_CSS", "scss": "Web_CSS", "less": "Web_CSS",
    "markdown": "Markdown", "mdx": "Markdown", "text": "Markdown",
    "hcl": "Infrastructure_Automation", "dockerfile": "Infrastructure_Automation",
    "jinja": "Infrastructure_Automation", "puppet": "Infrastructure_Automation",
    "openscad": "CAD_Modeling",
}

EXTENSION_ECOSYSTEM = {
    ".py": "Python", ".go": "Go", ".rs": "Rust",
    ".ts": "TypeScript", ".tsx": "TypeScript",
    ".js": "JavaScript", ".jsx": "JavaScript", ".mjs": "JavaScript",
    ".java": "Java", ".cs": "CSharp",
    ".cpp": "CPlusPlus", ".cc": "CPlusPlus", ".cxx": "CPlusPlus",
    ".hpp": "CPlusPlus", ".sh": "Shell", ".ps1": "Shell",
    ".css": "Web_CSS", ".scss": "Web_CSS", ".md": "Markdown",
    ".tf": "Infrastructure_Automation", ".scad": "CAD_Modeling",
}

# Mentioned anywhere in the evidence, these mean the project expects a GPU.
GPU = re.compile(r"\b(cuda|gpu|vram|nvidia|rocm|tensorrt|bitsandbytes|"
                 r"torch\.cuda|accelerat\w*\s+gpu)\b", re.I)

STALE_DAYS = 730          # two years without a push, and it is not Active
ABANDONED_MARKERS = re.compile(
    r"\b(no longer maintained|unmaintained|deprecated|archived|"
    r"this project is dead|not actively developed|read.only)\b", re.I)


def derive_axes(meta: dict[str, Any], survey: dict[str, Any],
                evidence_text: str = "", *,
                licence_text: str = "",
                paths: Iterable[str] = (),
                repo_key: str = "",
                permitted: dict[str, frozenset[str]] | None = None
                ) -> dict[str, str]:
    """Everything that can be read rather than guessed.

    Returns only what the evidence actually supports. A missing axis is left
    missing so `readiness` reports it and a person fills it — which is a better
    outcome than a plausible value nobody can tell is wrong.
    """
    out: dict[str, str] = {}

    licence = _license_class(meta, licence_text, evidence_text)
    if licence:
        out["license_class"] = licence

    ecosystem = _ecosystem(meta, survey)
    if ecosystem:
        out["ecosystem"] = ecosystem

    maturity = _maturity(meta, evidence_text)
    if maturity:
        out["maturity_stage"] = maturity

    footprint = _footprint(evidence_text)
    if footprint:
        out["hardware_footprint"] = footprint

    out["security_compliance"] = _security(evidence_text)

    # A ladder of paths, so it is read rather than asked. Only computed when
    # there is a listing to read: without one this would return `None` for
    # every source, which is a claim rather than an absence.
    listing = list(paths or survey.get("paths") or ())
    if listing:
        out["agent_surface"] = agent_surface(
            listing,
            # Passed explicitly rather than dug out of the metadata: a staged
            # proposal's metadata carries `github_*` fields and no repo key, so
            # the name rule could never fire on a re-derivation.
            repo_key=repo_key or str(meta.get("repo_key")
                                     or meta.get("full_name") or ""),
            description=str(meta.get("description") or ""),
            topics=meta.get("topics") or ())

    if permitted:
        out = {axis: value for axis, value in out.items()
               if axis not in permitted or value in permitted[axis]}
    return out


def _license_class(meta: dict[str, Any], licence_text: str = "",
                   readme: str = "") -> str:
    """The SPDX identifier if there is one, else the LICENSE file itself.

    GitHub reports no usable licence for a great many repositories that plainly
    have one - a composite LICENSE, an uncommon licence, a file its classifier
    did not recognise. Stopping at the API field left `license_class` empty on
    most of a real batch, and that field is what `find_donor` eliminates on: an
    empty one removes the source from every constrained answer, silently.

    Reuses `scout.rank` for both readings rather than growing a second mapping.
    The GPL family is the hard case and the reason those functions are not
    substring matching.
    """
    try:
        from scout.rank import (license_class, license_from_text,
                                spdx_is_unresolved)
    except ImportError:                                     # pragma: no cover
        return ""

    spdx = (meta.get("license_spdx") or meta.get("spdx")
            or meta.get("github_license_spdx") or "")
    if spdx and not spdx_is_unresolved(spdx):
        return license_class(spdx)
    if not licence_text and not readme:
        return ""
    reading = license_from_text(licence_text, readme if not licence_text else "")
    return reading.license_class or ""


EXT_COUNT = re.compile(r"^\s*(\.[A-Za-z0-9_+-]+)\s*\((\d+)\)\s*$")


def extension_counts(survey: dict[str, Any]) -> dict[str, int]:
    """Extension counts, whatever shape the survey stored them in.

    `scout.survey.shape` writes `[".py (150)", ".md (30)"]`; a hand-built
    fixture writes `{".py": 150}`. Both callers below tested for a mapping and
    silently did nothing on the real form, so neither the ecosystem fallback
    nor the prose rule ever fired against a live survey.
    """
    raw = survey.get("extensions")
    if isinstance(raw, dict):
        return {str(k).lower(): _int(v) for k, v in raw.items()}
    out: dict[str, int] = {}
    for item in raw or ():
        match = EXT_COUNT.match(str(item))
        if match:
            out[match.group(1).lower()] = int(match.group(2))
        elif str(item).startswith("."):
            out[str(item).lower()] = 1
    return out


def _ecosystem(meta: dict[str, Any], survey: dict[str, Any]) -> str:
    language = str(meta.get("language") or meta.get("github_language") or "").lower()
    if language in LANGUAGE_ECOSYSTEM:
        return LANGUAGE_ECOSYSTEM[language]

    extensions = extension_counts(survey)
    if extensions:
        ranked = sorted(extensions.items(), key=lambda kv: -kv[1])
        # Only the dominant extension counts. Walking down the list until
        # something maps reported `Markdown` for a repository that is 250 `.ts`
        # files and 30 `.md` ones - `.ts` has no value in this enumeration, so
        # the loop fell through to the readme files. An unmapped leader means
        # the taxonomy has no home for this language, and saying nothing is the
        # honest answer.
        top_name, top_count = ranked[0]
        mapped = EXTENSION_ECOSYSTEM.get(str(top_name).lower())
        if mapped:
            return mapped
    # A language with no home in the enumeration - Ruby, Kotlin, Swift - is
    # left for a person rather than forced into `Mixed`, which would say
    # something false about a single-language repository.
    return ""


def _maturity(meta: dict[str, Any], evidence_text: str) -> str:
    if meta.get("archived") or ABANDONED_MARKERS.search(evidence_text or ""):
        return "Abandoned"
    pushed = str(meta.get("pushed_at") or meta.get("github_pushed_at") or "")
    age = _age_days(pushed)
    if age is None:
        return ""
    if age > STALE_DAYS:
        return "Abandoned"
    # `Production_Ready` and `Reference` are judgements about what a repository
    # *is*, which metadata cannot settle. Recency only rules out abandonment.
    return "Active"


def _footprint(evidence_text: str) -> str:
    """Only the negative case is safe to derive.

    Text mentioning CUDA might still run on a CPU; text mentioning nothing of
    the sort is not a GPU project. So absence gives `CPU_Only` and presence
    gives nothing, leaving the harder call to a reader.
    """
    if not evidence_text:
        return ""
    return "" if GPU.search(evidence_text) else "CPU_Only"


# The enumeration is two values and one of them is the default. `Uncertified`
# does not mean "we checked and it failed" - it means no certification is
# claimed, which is true of essentially everything here. So the only question
# worth asking is whether this is security material at all, and that is a
# keyword question rather than a judgement about how secure anything is.
SECURITY = re.compile(
    r"\b(exploit\w*|payload|penetration test\w*|pentest\w*|red team|malware|"
    r"vulnerabilit\w+|CVE-\d|shellcode|backdoor|c2 framework|"
    r"command and control|antivirus evasion|reverse shell|"
    r"privilege escalation|siem|intrusion detection|firewall|forensic\w*|"
    r"cryptograph\w+|authentication|authorisation|authorization|"
    r"secrets? management|threat (?:model|intel)\w*)\b", re.I)


def _security(evidence_text: str) -> str:
    """Security material, or not. Never a claim about how secure something is."""
    return ("Security_Adjacent" if SECURITY.search(evidence_text or "")
            else "Uncertified")


def _age_days(timestamp: str) -> int | None:
    if not timestamp:
        return None
    text = timestamp.strip().replace("Z", "+00:00")
    try:
        when = datetime.fromisoformat(text)
    except ValueError:
        return None
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - when).days


def _int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


# ------------------------------------------------------------- grounding

WORD = re.compile(r"[A-Za-z][A-Za-z0-9_.+-]{2,}")
COMMON = frozenset("""
the and for with that this from into your you are was were has have had not
but can will would should could may might must all any some each other than
then them they their there these those when where which while who whom whose
its it's use uses used using run runs running make makes made take takes
produce produces output outputs input inputs data file files code project
library tool support supports requires required work works
""".split())


def grounded(bullets: list[str], source: str, *,
             min_hits: int = 1) -> tuple[list[str], list[str]]:
    """Drop bullets whose distinctive words do not appear in the evidence.

    The live run produced *"Uses tree-sitter for parsing"* for a repository
    whose documentation never mentions tree-sitter. That is the failure this
    whole design is arranged against, and it landed in a section a machine is
    allowed to write — so allowing it requires checking it.

    Crude on purpose: it asks only whether the bullet's uncommon words occur in
    the text the model was given. It cannot catch a wrong claim built from
    right words, and it reliably catches an invented name, which is the shape
    the hallucinations actually take.
    """
    haystack = (source or "").lower()
    kept, dropped = [], []
    for bullet in bullets or []:
        text = str(bullet).strip()
        if not text:
            continue
        distinctive = [w.lower() for w in WORD.findall(text)
                       if w.lower() not in COMMON]
        if not distinctive:
            kept.append(text)
            continue
        hits = sum(1 for w in distinctive if w in haystack)
        (kept if hits >= min(min_hits, len(distinctive)) and
         hits >= len(distinctive) * 0.5 else dropped).append(text)
    return kept, dropped


# ===========================================================================
# agent_surface — a ladder of paths, not a judgement
# ===========================================================================
#
# [[Note Content Model]] defines this axis explicitly: `None`; `Documented`
# (an `AGENTS.md`, `CLAUDE.md`, `.cursor/` or equivalent); `Procedural`
# (executable skills under `.claude/skills/`, `.agents/skills/`,
# `.opencode/skills/`); `Callable` (the source *is* an agent-invocable
# interface, usually an MCP server). *A source is recorded at the highest rung
# it reaches.*
#
# That is a file listing question. Putting it to a model was the same error as
# putting the licence to one - the answer is in evidence we already hold, and
# asking converts it into a guess. Measured against the 130 hand-charted
# sources, mere presence of an `agent_instructions` path predicts
# `agent_surface != None` at 0.985.

SKILL_DIR = re.compile(
    r"(?:^|/)(?:\.claude|\.agents|\.opencode|\.cursor|\.gemini)?/?skills/"
    r"[^/]+/(?:SKILL\.md|skill\.md)", re.I)

INSTRUCTION_FILE = re.compile(
    r"(?:^|/)(?:AGENTS?\.md|CLAUDE\.md|GEMINI\.md|CONVENTIONS\.md|"
    r"\.cursorrules|copilot-instructions\.md)$", re.I)

INSTRUCTION_DIR = re.compile(
    r"(?:^|/)\.(?:claude|cursor|agents|opencode|gemini|aider)/", re.I)

# An MCP server is the usual way a repository *is* an agent-invocable
# interface. A manifest or a package directory is strong; a passing mention in
# a workflow file or a test fixture is not, which is why this does not simply
# match "mcp" anywhere in a path.
MCP_STRONG = re.compile(
    r"(?:^|/)(?:\.mcp\.json|mcp\.json|mcp_config\.json|"
    r"\.well-known/mcp\.json)$|"
    r"(?:^|/)(?:_mcp|mcp_server|mcpb)(?:/|$)|"
    r"(?:^|/)mcp/(?:__init__\.py|server\.py|index\.ts|main\.py)$", re.I)


def agent_surface(paths: Iterable[str], *, repo_key: str = "",
                  description: str = "", topics: Iterable[str] = ()) -> str:
    """The highest rung the evidence reaches. `None` when it reaches none.

    Deliberately returns `None` rather than "" for an absent surface: `None`
    is a permitted value on this axis and means *we looked and there is no
    agent surface*, which is a finding. An empty string would mean *nobody
    looked*, and 78% of the corpus genuinely has no surface.
    """
    listing = [str(p) for p in (paths or ()) if p]

    declared = f"{description} {' '.join(str(t) for t in topics or ())}"
    # A repository *named* mcp is one, and the name is evidence. `semgrep/mcp`
    # was charted `Callable` and derived `None`, because its MCP-ness is in the
    # name rather than in any of the ten sampled paths.
    named = bool(re.search(r"(?:^|[/_-])mcp(?:[/_-]|$)", repo_key or "", re.I))
    if (named
            or any(MCP_STRONG.search(p) for p in listing)
            or re.search(r"\bmcp\b.{0,40}\bserver\b"
                         r"|\bserver\b.{0,40}\bmcp\b"
                         r"|model context protocol", declared, re.I)):
        return "Callable"
    if any(SKILL_DIR.search(p) for p in listing):
        return "Procedural"
    if any(INSTRUCTION_FILE.search(p) or INSTRUCTION_DIR.search(p)
           for p in listing):
        return "Documented"
    return "None"


# ===========================================================================
# interface_protocol — read the manifest, do not guess the shape
# ===========================================================================
#
# File shape cannot separate these. Measured over the hand-charted corpus,
# `CLI` (n=36), `Python_SDK` (n=37) and `REST` (n=16) are all dominated by
# `.py` and carry identical root files - readme, licence, gitignore,
# contributing. Only `Markdown` stands out, by having almost no code.
#
# What *does* separate them is the manifest: a declared console entry point is
# a command line, a web framework dependency is an HTTP interface, and a
# package with neither is a library. Those files are small and free to fetch
# from `raw.githubusercontent.com`, so this reads them.

CONSOLE_ENTRY = re.compile(
    r"\[project\.scripts\]|\[tool\.poetry\.scripts\]|console_scripts|"
    r"entry_points\s*=|\[\[bin\]\]|^\s*\"bin\"\s*:|^\s*bin\s*:", re.M)

REST_FRAMEWORK = re.compile(
    r"\b(fastapi|flask|django|starlette|sanic|tornado|bottle|falcon|"
    r"express|koa|nestjs|hapi|axum|actix-web|warp|rocket|gin-gonic|"
    r"fiber|spring-boot|uvicorn|gunicorn|hypercorn)\b", re.I)

WEB_FRAMEWORK = re.compile(
    r"\b(react|vue|svelte|angular|next|nuxt|astro|solid-js|preact|"
    r"tailwindcss|vite|webpack)\b", re.I)

GUI_FRAMEWORK = re.compile(
    r"\b(electron|tauri|pyqt5|pyqt6|pyside\d?|tkinter|wxpython|kivy|"
    r"dear-?imgui|gtk|javafx|swing)\b", re.I)

# Manifest files worth fetching, in the order they are tried.
MANIFESTS = ("pyproject.toml", "setup.py", "setup.cfg", "package.json",
             "Cargo.toml", "go.mod", "composer.json", "Gemfile")


def interface_protocol(manifest_text: str, survey: dict[str, Any] | None = None,
                       *, paths: Iterable[str] = ()) -> str:
    """MEASURED AND REJECTED. Not wired into `derive_axes`, on purpose.

    Kept the way `rank_configs.json` keeps `coverage-idf`: so the rejection
    stays reproducible and a future attempt has a number to beat.

    Manifest-based derivation was measured against 45 hand-charted sources and
    answered 22 of them at **0.409 accuracy**. The error is a category
    mistake, not a tuning problem: *a dependency list is not an interface
    declaration*. A library that depends on `fastapi` for its own test server
    was read as a REST service three times; `CLI` was read as `REST` twice and
    as `Python_SDK` twice.

    The prose branch alone was swept across seven thresholds and **precision
    never exceeded 0.80** while recall fell from 0.46 to 0.29. For an axis that
    `find_donor` eliminates on, one wrong value in five is worse than an empty
    one - it removes the source from answers it belongs in and adds it to ones
    it does not.

    What would beat it is reading the *declaration* rather than the dependency
    list: the `[project.scripts]` table on its own, a `package.json` `bin`
    field on its own, or the usage section of a README. That is a different
    piece of work.

    Original docstring follows.

    What a caller mainly talks to. "" when the evidence does not say.

    Order matters and is not arbitrary. A repository that declares both a
    console script and a web framework is usually a server with a launcher
    command, so `REST` is tested first. A GUI toolkit outranks both because
    nothing ships Qt by accident.
    """
    text = manifest_text or ""
    survey = survey or {}

    if GUI_FRAMEWORK.search(text):
        return "GUI"
    if REST_FRAMEWORK.search(text):
        return "REST"
    if CONSOLE_ENTRY.search(text):
        return "CLI"
    if WEB_FRAMEWORK.search(text):
        return "Web_UI"

    # No manifest, or one that says nothing. Fall back to the single case the
    # file shape does separate: a repository that is essentially prose.
    if _is_prose(survey, paths):
        return "Markdown"
    if text and re.search(r"\[project\]|\[tool\.poetry\]|setuptools|"
                          r"^\s*\"main\"\s*:", text, re.M):
        # A declared package with no entry point and no framework is something
        # you import.
        return "Python_SDK"
    return ""


def _is_prose(survey: dict[str, Any], paths: Iterable[str] = ()) -> bool:
    """Is this repository mostly words rather than code?

    Measured: 14 of the 24 `Markdown` sources have `.md` as their dominant
    extension, and no other value on this axis does. The threshold asks for a
    clear majority rather than a plurality, because a code project with a big
    docs tree should not be filed as prose.
    """
    counts = extension_counts(survey)
    if counts:
        total = sum(counts.values())
        prose = sum(v for k, v in counts.items()
                    if k in (".md", ".mdx", ".rst", ".txt", ".adoc"))
        if total and prose / total >= 0.6:
            return True
    listing = [str(p).lower() for p in (paths or ())]
    if listing:
        prose = sum(1 for p in listing
                    if p.endswith((".md", ".mdx", ".rst", ".txt", ".adoc")))
        return prose / len(listing) >= 0.6
    return False
