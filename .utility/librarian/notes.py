"""Reading the vault.

Markdown is truth, so this module is the only place that decides what a note
*is*. Everything downstream - the index, integrity checks, retrieval, the
graph - works from the `Note` objects produced here, which means there is one
parser to keep correct rather than five that drift.

The frontmatter parser prefers PyYAML and falls back to a scanner for the
subset this vault actually uses. The fallback exists so a missing optional
dependency degrades rather than stopping the index.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

from .config import LAYER_FOLDERS, SKIP_DIRS

try:                                               # pragma: no cover - env dependent
    import yaml
except Exception:                                  # pragma: no cover
    yaml = None

FRONTMATTER = re.compile(r"\A---\r?\n(?P<body>.*?)\r?\n---\r?\n?", re.S)

# [relation:: [[Target]]] - the vault's typed edges, e.g.
# [implements_pattern:: [[Pattern - Agent Orchestration]]]
# The value alternates whole wikilinks with plain text, so the closing `]` of
# the field is not confused with the `]]` of the link it contains.
INLINE_FIELD = re.compile(
    r"\[(?P<relation>[a-z_][a-z0-9_]*)::\s*(?P<value>(?:\[\[[^\[\]]+\]\]|[^\[\]])*)\]"
)
WIKILINK = re.compile(r"\[\[(?P<target>[^\[\]|#]+)(?:#[^\[\]|]*)?(?:\|[^\[\]]*)?\]\]")
HEADING = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<title>.+?)\s*$", re.M)

# Sections that hold links, provenance rows or metadata tables rather than
# prose. They are excluded from chunking because a full-text index over them
# can only ever produce spurious matches: `## Semantic Links` is a block of
# wikilinks, `## Evidence Anchors` restates frontmatter, `## GitHub Snapshot`
# is a field dump. Before this exclusion they were 17% of the chunk corpus and
# were demonstrably ranking notes above the correct answer on a shared token.
#
# The information in them is not lost. Links are already first-class in the
# `link` table and drive graph traversal; frontmatter is searched directly by
# `consult.by_name`; note names are matched there too. Only the duplicate
# full-text copy goes away.
NON_PROSE_HEADINGS = frozenset({
    "semantic links",
    "evidence",
    "evidence anchors",
    "github snapshot",
    "related",
    "related glossary",
    "related topics",
    "related patterns",
    "related terms",
    "example repositories",
    "approved resources",
    "aliases",
})


def is_prose_heading(heading: str) -> bool:
    """False for link, provenance and metadata blocks. Used by chunking."""
    return heading.strip().lower() not in NON_PROSE_HEADINGS

# Sections whose text must be distinct across resources. The original defect
# this catalogue was rewritten to fix was 41 notes sharing these blocks.
DISTINCT_SECTIONS = ("Bottom Line", "What It Solves")

_QUOTES = "\"'"


@dataclass(frozen=True)
class Link:
    src: str
    dst: str
    relation: str


@dataclass(frozen=True)
class Chunk:
    """Contract per spec 9.1."""

    note: str
    layer: str
    ordinal: int
    heading: str
    text: str


@dataclass
class Note:
    name: str
    path: Path
    layer: str
    type: str
    frontmatter: dict[str, Any]
    body: str
    mtime: float
    parse_error: str = ""
    _sections: dict[str, str] | None = field(default=None, repr=False, compare=False)

    # ------------------------------------------------------------- accessors

    @property
    def sections(self) -> dict[str, str]:
        """`## Heading` -> text beneath it, for the duplicate-prose checks."""
        if self._sections is None:
            self._sections = split_sections(self.body)
        return self._sections

    def section(self, title: str) -> str:
        return self.sections.get(title, "")

    def get(self, key: str, default: Any = None) -> Any:
        return self.frontmatter.get(key, default)

    def string(self, key: str) -> str:
        value = self.frontmatter.get(key)
        if value is None:
            return ""
        if isinstance(value, (list, tuple)):
            return ", ".join(str(v) for v in value)
        return str(value)

    def links(self) -> list[Link]:
        return extract_links(self.name, self.body)

    def is_container(self) -> bool:
        return bool(self.frontmatter.get("container"))


# ------------------------------------------------------------------ parsing

def parse_frontmatter(text: str) -> tuple[dict[str, Any], str, str]:
    """Return (frontmatter, body, error).

    A malformed block is reported, not raised: one bad note must not stop an
    index build, and `integrity.py` is where a parse failure becomes an error
    somebody has to act on.
    """
    match = FRONTMATTER.match(text)
    if not match:
        return {}, text, ""
    raw = match.group("body")
    body = text[match.end():]
    if yaml is not None:
        try:
            loaded = yaml.safe_load(raw)
            if loaded is None:
                return {}, body, ""
            if not isinstance(loaded, dict):
                return {}, body, "frontmatter is not a mapping"
            return loaded, body, ""
        except Exception as exc:
            return _scan_frontmatter(raw), body, "YAML parse failed: %s" % exc
    return _scan_frontmatter(raw), body, ""


def _scan_frontmatter(raw: str) -> dict[str, Any]:
    """Fallback for `key: value`, `key: "value"`, `key: [a, b]`, `key: 12`."""
    out: dict[str, Any] = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line or line[:1] in {" ", "\t", "-"}:
            continue
        key, _, value = line.partition(":")
        out[key.strip()] = _scalar(value.strip())
    return out


def _scalar(value: str) -> Any:
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_scalar(part.strip()) for part in _split_list(inner)]
    if len(value) >= 2 and value[0] == value[-1] and value[0] in _QUOTES:
        return value[1:-1]
    low = value.lower()
    if low in {"true", "false"}:
        return low == "true"
    if low in {"null", "~", ""}:
        return None
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def _split_list(inner: str) -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    quote = ""
    for ch in inner:
        if quote:
            if ch == quote:
                quote = ""
            buf.append(ch)
        elif ch in _QUOTES:
            quote = ch
            buf.append(ch)
        elif ch == ",":
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if buf:
        parts.append("".join(buf))
    return [p for p in parts if p.strip()]


def split_sections(body: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    matches = list(HEADING.finditer(body))
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        title = match.group("title").strip()
        sections.setdefault(title, body[start:end].strip())
    return sections


FENCED_CODE = re.compile(r"```.*?```|~~~.*?~~~", re.S)
INLINE_CODE = re.compile(r"`[^`\n]*`")


def strip_code(body: str) -> str:
    """Blank out code spans, preserving offsets.

    A wikilink inside backticks is documentation of the link syntax, not an
    edge - `[listed_in:: [[parent note]]]` in a schema note names a shape, not
    a note. Blanking rather than deleting keeps every span valid for callers
    that also work on offsets.
    """
    def blank(match: re.Match) -> str:
        return "".join(" " if ch != "\n" else "\n" for ch in match.group(0))

    return INLINE_CODE.sub(blank, FENCED_CODE.sub(blank, body))


def extract_links(src: str, body: str) -> list[Link]:
    """Typed edges first, untyped wikilinks second.

    A target reached through `[relation:: [[X]]]` keeps its relation; anything
    else is `related_to`, which is honest about knowing only that a connection
    exists.
    """
    body = strip_code(body)
    seen: set[tuple[str, str, str]] = set()
    out: list[Link] = []
    typed_spans: list[tuple[int, int]] = []
    for match in INLINE_FIELD.finditer(body):
        relation = match.group("relation")
        typed_spans.append(match.span())
        for link in WIKILINK.finditer(match.group("value")):
            key = (src, link.group("target").strip(), relation)
            if key not in seen:
                seen.add(key)
                out.append(Link(*key))
    for match in WIKILINK.finditer(body):
        if any(start <= match.start() < end for start, end in typed_spans):
            continue
        key = (src, match.group("target").strip(), "related_to")
        if key not in seen:
            seen.add(key)
            out.append(Link(*key))
    return out


def layer_for(path: Path, vault_root: Path, frontmatter: dict[str, Any]) -> str:
    """Folder first, frontmatter `type` as a refinement.

    The folder is the one thing every note agrees on; `type` disambiguates
    within a folder (a template is not a record, a hub is not a topic).
    """
    try:
        relative = path.relative_to(vault_root)
    except ValueError:
        relative = path
    top = relative.parts[0] if len(relative.parts) > 1 else ""
    layer = LAYER_FOLDERS.get(top, "other")
    declared = str(frontmatter.get("type") or "")
    if path.name.startswith("_Template") or declared.startswith("_template"):
        return "template"
    if layer in ("index", "internal"):
        if declared == "topic_index":
            return "topic"
        if declared in {"design_spec", "implementation_brief", "reference", "roadmap",
                        "assessment", "domain_register", "research", "schema_extension"}:
            return "document"
    return layer


def iter_note_paths(vault_root: Path) -> Iterator[Path]:
    for path in sorted(vault_root.rglob("*.md")):
        parts = path.relative_to(vault_root).parts[:-1]
        if set(parts) & SKIP_DIRS:
            continue
        # Any dot-directory: .obsidian, .git, .pytest_cache and whatever tool
        # leaves one next. A README dropped by a test runner is not a note,
        # and indexing it made the index look permanently stale.
        if any(part.startswith(".") for part in parts):
            continue
        if path.name.startswith("."):
            continue
        yield path


def load_note(path: Path, vault_root: Path) -> Note:
    text = path.read_text(encoding="utf-8", errors="replace")
    frontmatter, body, error = parse_frontmatter(text)
    return Note(
        name=path.stem,
        path=path,
        layer=layer_for(path, vault_root, frontmatter),
        type=str(frontmatter.get("type") or ""),
        frontmatter=frontmatter,
        body=body,
        mtime=path.stat().st_mtime,
        parse_error=error,
    )


def load_vault(vault_root: Path) -> list[Note]:
    return [load_note(path, vault_root) for path in iter_note_paths(vault_root)]


# ----------------------------------------------------------------- chunking

def chunk_note(note: Note, target_chars: int = 1200, min_chars: int = 80) -> list[Chunk]:
    """One chunk per section, split on paragraph boundaries when oversized.

    Sections are the natural unit here because the vault's notes are written
    to a fixed set of headings: `Bottom Line` and `What It Solves` are the
    blocks a retrieval hit should point at, and keeping them whole means a
    match can be explained by naming the heading it came from.

    Link, provenance and metadata sections are skipped entirely - see
    `NON_PROSE_HEADINGS`. A chunk nobody could usefully match is not a neutral
    cost; it is a competitor for the ranking slot the right answer needs.
    """
    chunks: list[Chunk] = []
    ordinal = 0
    for heading, text in _iter_sections(note.body):
        if not is_prose_heading(heading):
            continue
        for piece in _split_text(text, target_chars):
            piece = piece.strip()
            if not piece:
                continue
            if len(piece) < min_chars and chunks and heading == chunks[-1].heading:
                continue
            chunks.append(Chunk(note=note.name, layer=note.layer, ordinal=ordinal,
                                heading=heading, text=piece))
            ordinal += 1
    if not chunks and note.body.strip():
        chunks.append(Chunk(note=note.name, layer=note.layer, ordinal=0,
                            heading="", text=note.body.strip()[:target_chars]))
    return chunks


def _iter_sections(body: str) -> Iterator[tuple[str, str]]:
    matches = list(HEADING.finditer(body))
    if not matches:
        yield "", body
        return
    preamble = body[:matches[0].start()].strip()
    if preamble:
        yield "", preamble
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        yield match.group("title").strip(), body[start:end]


def _split_text(text: str, target: int) -> list[str]:
    text = text.strip()
    if len(text) <= target:
        return [text] if text else []
    pieces: list[str] = []
    current: list[str] = []
    size = 0
    for para in re.split(r"\n\s*\n", text):
        para = para.strip()
        if not para:
            continue
        if size + len(para) > target and current:
            pieces.append("\n\n".join(current))
            current, size = [], 0
        current.append(para)
        size += len(para)
    if current:
        pieces.append("\n\n".join(current))
    return pieces
