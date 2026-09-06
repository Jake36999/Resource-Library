"""Declarative assertions over the vault, in the spirit of dbt tests.

Each check is a function from the vault root to a list of violations, so the
set is extended by adding a function to `CHECKS` and nothing else. A check
that cannot name the note it failed on is not a check anybody can act on, so
`Violation.note` is required.

Errors fail a run; warnings are reported and do not. The split matters: a
broken link is a defect, whereas a resource nobody links to yet is a fact
about a young catalogue.
"""
from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

from . import notes as notes_mod
from .config import (INDEX_FOLDER, INTERNAL_FOLDER, LICENSE_CLASSES, is_hub,
                     vault_root)
from .notes import DISTINCT_SECTIONS, Note

ERROR = "error"
WARNING = "warning"

# Layers whose links and fields are load-bearing. Templates are excluded on
# purpose: `[[Topic -]]` in a template is a placeholder for the author to
# fill, not a broken edge.
CONTENT_LAYERS = {"resource", "topic", "pattern", "glossary", "application",
                  "workflow", "paper", "review", "index", "document", "scouting"}

APPLICATION_REQUIRED_FIELDS = ("type", "project", "stage", "resources_used", "outcome")
APPLICATION_REQUIRED_SECTIONS = ("What Was Needed", "What Was Found And Taken",
                                 "What It Replaced", "What The Catalogue Should Learn")

DOMAIN_KEY = re.compile(r"\(`(?P<key>[a-z0-9_]+)`\)")
TOPIC_KEY = re.compile(r'^topic_key:\s*"?(?P<key>[a-z0-9_]+)"?', re.M)


@dataclass(frozen=True)
class Violation:
    """Contract per spec 9.3."""

    check: str
    note: str
    detail: str
    severity: str = ERROR


# ------------------------------------------------------------------- helpers

def _load(vault: Path) -> list[Note]:
    return notes_mod.load_vault(vault)


def _normalise(text: str) -> str:
    return " ".join(text.split()).strip().lower()


def known_topic_keys(vault: Path) -> set[str]:
    """The authoritative key register: the topic indexes plus the domain note.

    [[Scouting Domains]] says of itself that it is authoritative and that the
    scout may not invent a domain. This function is the only place that
    reads that authority, so widening it means editing Markdown.
    """
    keys: set[str] = set()
    index_dir = vault / INDEX_FOLDER
    if index_dir.exists():
        for path in index_dir.glob("Topic - *.md"):
            match = TOPIC_KEY.search(path.read_text(encoding="utf-8"))
            if match:
                keys.add(match.group("key"))
    # Found by name, not by folder. The register moved from `00-Indexes` to
    # `internal docs` on 2026-09-04, and a check that silently stops finding
    # its own authority is worse than one that fails loudly - an empty key set
    # makes every `topic_keys` value look invented.
    for folder in (INTERNAL_FOLDER, INDEX_FOLDER):
        register = vault / folder / "Scouting Domains.md"
        if register.exists():
            keys.update(m.group("key") for m in DOMAIN_KEY.finditer(
                register.read_text(encoding="utf-8")))
            break
    return keys


# -------------------------------------------------------------------- checks

def check_frontmatter_parses(vault: Path, loaded: list[Note] | None = None) -> list[Violation]:
    return [Violation("frontmatter_parses", note.name, note.parse_error)
            for note in (loaded or _load(vault)) if note.parse_error]


def check_wikilinks_resolve(vault: Path, loaded: list[Note] | None = None) -> list[Violation]:
    loaded = loaded or _load(vault)
    names = {note.name for note in loaded}
    out: list[Violation] = []
    for note in loaded:
        if note.layer not in CONTENT_LAYERS:
            continue
        for link in note.links():
            if link.dst not in names:
                out.append(Violation(
                    "wikilinks_resolve", note.name,
                    f"link [[{link.dst}]] ({link.relation}) resolves to no note"))
    return out


def check_distinct_resource_prose(vault: Path, loaded: list[Note] | None = None) -> list[Violation]:
    """No two resources share a `Bottom Line` or `What It Solves` block.

    This is the check that caught the original defect - 41 notes filled from
    a topic template, each describing its neighbour as well as itself.
    """
    loaded = loaded or _load(vault)
    out: list[Violation] = []
    for section in DISTINCT_SECTIONS:
        buckets: dict[str, list[str]] = defaultdict(list)
        for note in loaded:
            if note.layer != "resource":
                continue
            text = _normalise(note.section(section))
            if text:
                buckets[text].append(note.name)
        for text, owners in buckets.items():
            if len(owners) > 1:
                for name in sorted(owners):
                    others = ", ".join(sorted(set(owners) - {name}))
                    out.append(Violation(
                        "distinct_resource_prose", name,
                        f"'{section}' is identical to: {others}"))
    return out


def check_resource_has_url_and_licence(vault: Path, loaded: list[Note] | None = None) -> list[Violation]:
    out: list[Violation] = []
    for note in (loaded or _load(vault)):
        if note.layer not in {"resource", "review"} or is_hub(note.type):
            continue
        if not note.string("canonical_url"):
            out.append(Violation("resource_has_url_and_licence", note.name,
                                 "no canonical_url"))
        if not note.string("license_class"):
            out.append(Violation("resource_has_url_and_licence", note.name,
                                 "no license_class"))
    return out


def check_license_class_known(vault: Path, loaded: list[Note] | None = None) -> list[Violation]:
    """The licence enum is closed (spec 4.3).

    `Source_Available` means readable but restricted; `Unknown` means
    undetermined. Collapsing the two would let a restricted licence be
    recommended as merely unresearched.
    """
    out: list[Violation] = []
    for note in (loaded or _load(vault)):
        value = note.string("license_class")
        if value and value not in LICENSE_CLASSES:
            out.append(Violation("license_class_known", note.name,
                                 f"license_class '{value}' is not one of "
                                 f"{', '.join(LICENSE_CLASSES)}"))
    return out


def check_container_has_expansion_status(vault: Path, loaded: list[Note] | None = None) -> list[Violation]:
    out: list[Violation] = []
    for note in (loaded or _load(vault)):
        if note.is_container() and not note.string("expansion_status"):
            out.append(Violation("container_has_expansion_status", note.name,
                                 "container: true with no expansion_status "
                                 "(pending | partial | complete | declined)"))
    return out


def check_topic_keys_known(vault: Path, loaded: list[Note] | None = None) -> list[Violation]:
    known = known_topic_keys(vault)
    out: list[Violation] = []
    if not known:                                          # pragma: no cover
        return [Violation("topic_keys_known", "Scouting Domains",
                          "no topic or domain keys found; the register is missing")]
    for note in (loaded or _load(vault)):
        if note.layer == "template":
            continue
        values = note.get("topic_keys") or []
        if isinstance(values, str):
            values = [values]
        for key in values:
            if str(key) not in known:
                out.append(Violation("topic_keys_known", note.name,
                                     f"topic_key '{key}' is in no topic index and "
                                     f"not in [[Scouting Domains]]"))
    return out


def check_application_record_shape(vault: Path, loaded: list[Note] | None = None) -> list[Violation]:
    """The frontmatter and body contract for `09-Applications/` (spec 10.4).

    `What The Catalogue Should Learn` is the section that turns a diary entry
    into a requirement, so its absence is an error rather than a warning.
    """
    out: list[Violation] = []
    for note in (loaded or _load(vault)):
        if note.layer != "application" or note.type != "application_record":
            continue
        for field in APPLICATION_REQUIRED_FIELDS:
            if field not in note.frontmatter:
                out.append(Violation("application_record_shape", note.name,
                                     f"missing required frontmatter '{field}'"))
        for section in APPLICATION_REQUIRED_SECTIONS:
            if not note.section(section):
                out.append(Violation("application_record_shape", note.name,
                                     f"missing required section '## {section}'"))
        attested = note.string("attested_by")
        if attested and attested not in {"user", "agent"}:
            out.append(Violation("application_record_shape", note.name,
                                 f"attested_by '{attested}' must be user or agent"))
    return out


def check_resource_has_parent_topic(vault: Path, loaded: list[Note] | None = None) -> list[Violation]:
    out: list[Violation] = []
    for note in (loaded or _load(vault)):
        if note.layer != "resource":
            continue
        if not any(link.relation == "parent_topic" for link in note.links()):
            out.append(Violation("resource_has_parent_topic", note.name,
                                 "no parent_topic link; it is unreachable by browsing",
                                 WARNING))
    return out


MATRIX_ROW = re.compile(r"^\|\s*\[\[(?P<note>[^\]]+)\]\]\s*\|(?P<rest>.*)\|\s*$", re.M)
MATRIX_COLUMNS = ("ecosystem", "domain_primary", "maturity_stage", "license_class",
                  "deployment_target", "interface_protocol", "data_locality",
                  "hardware_footprint", "security_compliance", "agent_surface")


def check_taxonomy_matrix_agrees(vault: Path, loaded: list[Note] | None = None) -> list[Violation]:
    """The generated matrix must agree with the notes it was generated from.

    A warning, not an error, because the note is truth and the matrix is
    derived: a disagreement means the matrix is stale and a build run will fix
    it. It matters because the matrix is what a person reads while the
    frontmatter is what `find_donor` filters on, and a licence that reads
    Permissive in the table but Unknown in the field is a resource the
    constraint path will silently refuse to offer.
    """
    matrix = vault / INDEX_FOLDER / "Taxonomy Index.md"
    if not matrix.exists():
        return []
    by_name = {note.name: note for note in (loaded or _load(vault))}
    out: list[Violation] = []
    for row in MATRIX_ROW.finditer(matrix.read_text(encoding="utf-8")):
        note = by_name.get(row.group("note").strip())
        if note is None or note.layer != "resource":
            continue
        cells = [cell.strip() for cell in row.group("rest").split("|")]
        for column, cell in zip(MATRIX_COLUMNS, cells):
            declared = note.string(column)
            if cell and declared and cell != declared:
                out.append(Violation(
                    "taxonomy_matrix_agrees", note.name,
                    f"{column}: matrix says '{cell}', frontmatter says '{declared}'. "
                    f"The note is truth; regenerate the matrix.", WARNING))
    return out


def check_orphan_notes(vault: Path, loaded: list[Note] | None = None) -> list[Violation]:
    """Nothing links here. A fact about a young catalogue, not a defect."""
    loaded = loaded or _load(vault)
    inbound: set[str] = set()
    for note in loaded:
        for link in note.links():
            inbound.add(link.dst)
    out: list[Violation] = []
    for note in loaded:
        if note.layer in {"resource", "pattern", "application", "workflow", "paper"} \
                and note.name not in inbound:
            out.append(Violation("orphan_notes", note.name,
                                 f"no note links to this {note.layer}", WARNING))
    return out


def check_derived_views_current(vault: Path, loaded: list[Note] | None = None) -> list[Violation]:
    """The derived views should say what the notes say.

    A warning, not an error, because the fix is a command rather than a
    correction: `python -m librarian views`. It matters because
    `scout.rank.gap_fit` reads `resource_count` and carries the largest
    ranking weight, so a stale count mis-ranks every candidate for that topic -
    quietly, and in a direction nobody would think to check.
    """
    from . import views as views_mod
    try:
        changes = views_mod.run(vault, write=False)
    except Exception as exc:                              # pragma: no cover
        return [Violation("derived_views_current", "Taxonomy Index",
                          f"could not compute the derived views: {exc}", WARNING)]
    return [Violation("derived_views_current", change.note,
                      f"{change.view} disagrees with the notes ({change.detail}); "
                      f"run `python -m librarian views`", WARNING)
            for change in changes]


def _model(vault: Path):
    from . import content_model as model_mod
    return model_mod.load(vault)


def check_content_model_parses(vault: Path, loaded: list[Note] | None = None) -> list[Violation]:
    """[[Note Content Model]] is the schema; an unreadable schema is an error.

    Reported separately from the checks that use it so that a broken model reads
    as one failure rather than as several hundred notes suddenly being wrong.
    """
    model = _model(vault)
    if not model.error:
        return []
    # A vault with no model degrades to no shape checks and says so; one whose
    # model will not parse has a defect somebody introduced.
    severity = WARNING if model.missing else ERROR
    return [Violation("content_model_parses", "Note Content Model",
                      model.error, severity)]


def check_frontmatter_complete(vault: Path, loaded: list[Note] | None = None) -> list[Violation]:
    """Every field the model marks required, present on every note of that shape.

    A field is required when something in the system reads it - a promoted
    column, a hard filter, a ranking input - so a missing one is not untidiness.
    `license_class` absent means the note is excluded from every constrained
    query, silently.
    """
    model = _model(vault)
    if model.error:
        return []
    out: list[Violation] = []
    for note in (loaded or _load(vault)):
        shape_name = model.shape_of(note)
        if not shape_name:
            continue
        shape = model.shapes[shape_name]
        for field_name in shape.required_fields:
            if field_name not in note.frontmatter:
                out.append(Violation("frontmatter_complete", note.name,
                                     f"{shape_name} note is missing required "
                                     f"frontmatter '{field_name}'"))
    return out


def check_sections_complete(vault: Path, loaded: list[Note] | None = None) -> list[Violation]:
    """Every section the model marks required, present, in the declared order.

    Order is a warning rather than an error: a note with its sections shuffled
    is readable and complete, and the cost of the disagreement is that a reader
    scanning for `Bottom Line` first has to hunt. A *missing* required section
    is an error, because something that reads the note will find nothing there.
    """
    model = _model(vault)
    if model.error:
        return []
    out: list[Violation] = []
    for note in (loaded or _load(vault)):
        shape_name = model.shape_of(note)
        if not shape_name:
            continue
        shape = model.shapes[shape_name]
        headings = re.findall(r"^##\s+(.+?)\s*$", note.body, re.M)
        present = set(headings)
        for section in shape.required_sections:
            if section not in present:
                out.append(Violation("sections_complete", note.name,
                                     f"{shape_name} note is missing required "
                                     f"section '## {section}'"))
        declared = [h for h in model.section_order.get(shape_name, ()) if h in present]
        actual = [h for h in headings if h in set(declared)]
        if actual != declared:
            out.append(Violation("sections_complete", note.name,
                                 f"sections are out of the order "
                                 f"[[Note Content Model]] declares: expected "
                                 f"{' -> '.join(declared)}", WARNING))
    return out


def check_axis_values_known(vault: Path, loaded: list[Note] | None = None) -> list[Violation]:
    """The nine taxonomy axes are closed enumerations.

    A value outside the model is an error rather than a new category. Several of
    these fields are what `find_donor` eliminates on, so a typo does not produce
    a slightly worse ranking - it removes the resource from every constrained
    answer, and nothing anywhere says so.
    """
    model = _model(vault)
    if model.error or not model.axis_values:
        return []
    out: list[Violation] = []
    for note in (loaded or _load(vault)):
        if model.shape_of(note) != "resource":
            continue
        for axis, permitted in model.axis_values.items():
            value = note.string(axis)
            if value and value not in permitted:
                out.append(Violation("axis_values_known", note.name,
                                     f"{axis} is '{value}', which "
                                     f"[[Note Content Model]] does not permit; "
                                     f"add it there deliberately or fix the note"))
    return out


def check_recorded_property_is_findable(vault: Path, loaded: list[Note] | None = None) -> list[Violation]:
    """A property recorded in frontmatter should be sayable in the prose too.

    The scenario test found sources whose agent-facing surface was recorded in
    `agent_surface` and inventoried in `What Is Inside`, and which could still
    not be retrieved by anyone asking for that capability - because no *claim*
    section said it. The fact was written where it could be read, not where it
    could be found.

    A warning rather than an error: the fix is writing, and a note can be
    correct and still thin. But an axis value with no prose behind it is a fact
    the catalogue holds and cannot surface, which is the failure mode the whole
    system exists to avoid.
    """
    out: list[Violation] = []
    for note in (loaded or _load(vault)):
        if note.layer not in {"resource", "review"} or not note.string("canonical_url"):
            continue
        # Only the substantive rungs. `Documented` means the repository carries
        # an AGENTS.md or similar - a fact worth recording and not a capability
        # worth claiming, so requiring prose for it would manufacture filler.
        surface = note.string("agent_surface")
        if surface not in ("Procedural", "Callable"):
            continue
        claims = " ".join(
            (note.section(name) or "")
            for name in ("Bottom Line", "What It Solves", "Architecture & Mechanics",
                         "Transferable Capability", "Integration & Use Cases")).lower()
        if not any(word in claims for word in ("agent", "skill", "mcp", "procedure")):
            out.append(Violation(
                "recorded_property_is_findable", note.name,
                f"agent_surface is '{surface}' but no claim section says so; the "
                f"property is recorded and unfindable", WARNING))
    return out



def check_every_topic_is_routable(vault: Path,
                                  loaded: list[Note] | None = None) -> list[Violation]:
    """A topic index that the route map does not list is unreachable by browsing.

    `views.master_view` deliberately corrects the `(n approved)` figures and
    `topic_count` but never the membership, because which topics appear and in
    what order is a routing decision a person made. The consequence is that a
    *new* topic silently never appears: on 2026-09-04 the frontmatter said
    fifteen topics and the map listed fourteen, and every existing check
    passed, because the only thing being compared was the count.

    A warning rather than an error - the fix is a curation decision, not a data
    defect, and nobody should be blocked from a run by it.
    """
    master = vault / INDEX_FOLDER / "Master Index.md"
    if not master.exists():
        return []
    text = master.read_text(encoding="utf-8")
    notes = loaded if loaded is not None else notes_mod.load_vault(vault)
    out: list[Violation] = []
    for note in notes:
        if note.type != "topic_index":
            continue
        if f"[[{note.name}]]" not in text:
            out.append(Violation(
                "every_topic_is_routable", note.name,
                "topic index is not listed in the Master Index route map, so it "
                "cannot be reached by browsing; add it deliberately - `views` "
                "will not, because membership is a curation decision",
                WARNING))
    return out


def check_recorded_claims_are_current(vault: Path,
                                      loaded: list[Note] | None = None) -> list[Violation]:
    """A note's recorded facts against the last freshness reading.

    Warns rather than errors, and the reason is the whole design: the note is
    the authority (`MARKDOWN_IS_TRUTH`), the reading is data, and deciding that
    a note should change is a judgement a person makes. This check tells them
    there is a decision to make; it does not make it.

    Silent when no reading exists, because "nobody has looked" is not a defect
    in the note - it is a reason to run `librarian freshness`.
    """
    from . import freshness as freshness_mod

    out: list[Violation] = []
    for row in freshness_mod.divergences():
        actionable = [d for d in row["divergence"]
                      if d["kind"] in freshness_mod.WARNING_KINDS]
        if not actionable:
            continue
        for item in actionable:
            out.append(Violation(
                "recorded_claims_are_current", row["note"] or row["repo_key"],
                f"{item['kind']}: recorded {item['was']!r}, upstream is "
                f"{item['now']!r} as of {row['checked_at'][:10]} - {item['detail']}",
                WARNING))
    return out


def check_application_links_a_resource(vault: Path,
                                       loaded: list[Note] | None = None) -> list[Violation]:
    """An application record that names its sources in prose is connected to nothing.

    `consult._proven_use_bonus` reads `application_count`, which `index.py`
    computes from `applied_resource` links. On 2026-09-04 that count was zero
    for all 130 resources and the bonus had never fired - not because either was
    broken, but because all four records list `resources_used` as descriptions
    ("agent harness implementations") rather than links.

    A fully built feedback path receiving nothing looks exactly like no feedback
    path, which is why this warns rather than staying silent.
    """
    notes = loaded if loaded is not None else notes_mod.load_vault(vault)
    out: list[Violation] = []
    for note in notes:
        if note.layer != "application" or note.name.startswith("_Template"):
            continue
        # A hub routes to records; it is not one. `is_hub` is the existing
        # authority on that distinction and is reused rather than re-listed.
        if is_hub(note.type):
            continue
        linked = [l for l in note.links() if l.relation == "applied_resource"]
        if not linked:
            out.append(Violation(
                "application_links_a_resource", note.name,
                "no `applied_resource` link, so this record contributes nothing "
                "to `application_count` and the proven-use bonus cannot see it; "
                "name the resource notes rather than describing them",
                WARNING))
    return out


def check_structural_claims_match_surveys(vault: Path,
                                          loaded: list[Note] | None = None) -> list[Violation]:
    """A number a note states about a tree, against the survey it came from.

    Only *contradicted* claims are reported: a corresponding quantity exists in
    the data layer and differs. `unsupported` is left alone, because a number
    with no matching row is usually counting something the signal table does
    not model - README entries, a fact about a different repository - and a
    false accusation here would teach authors to stop being specific, which is
    the opposite of what [[Source Documentation Standard]] wants.
    """
    from . import provenance as provenance_mod

    out: list[Violation] = []
    for claim in provenance_mod.check(vault):
        if claim.status != provenance_mod.CONTRADICTED:
            continue
        out.append(Violation(
            "structural_claims_match_surveys", claim.note,
            f"note says {claim.number} {claim.unit}; the survey records "
            f"{claim.nearest} - one of them is wrong",
            WARNING))
    return out


def check_thresholds_carry_their_distribution(vault: Path,
                                              loaded: list[Note] | None = None) -> list[Violation]:
    """`THRESHOLD_CARRIES_ITS_DISTRIBUTION`, enforced instead of asserted.

    A constant compared against corpus statistics is fitted to a corpus, and
    corpora move: `SELECTIVITY_CEILING` was correct at 81 resources and wrong at
    128, and `SEMANTIC_FLOOR` was set above the highest similarity that existed.
    Both were found by accident.

    The invariant was written down on 2026-09-04 and seven of eleven thresholds
    violated it two days later, which is what a rule with no check is worth.
    This does not judge the *value* - only that the function which would let
    somebody re-derive it exists and is named in the module.
    """
    import importlib
    import re

    # module -> the re-derivation each threshold must be able to point at
    REQUIRED = {
        "consult": {"SELECTIVITY_CEILING": "selectivity_distribution",
                    "COMPONENT_SELECTIVITY_CEILING": "component_name_distribution"},
        "duplicates": {"SEMANTIC_FLOOR": "distribution"},
        "coverage": {"STRONG_ACCOUNT": "calibrate", "THIN_ACCOUNT": "calibrate"},
    }
    out: list[Violation] = []
    for module_name, pairs in REQUIRED.items():
        try:
            module = importlib.import_module(f"librarian.{module_name}")
        except Exception as exc:                     # pragma: no cover - import guard
            out.append(Violation("thresholds_carry_their_distribution", module_name,
                                 f"could not import: {exc}", WARNING))
            continue
        for constant, function in pairs.items():
            if not hasattr(module, constant):
                continue
            if not callable(getattr(module, function, None)):
                out.append(Violation(
                    "thresholds_carry_their_distribution", module_name,
                    f"{constant} is a corpus-relative threshold and "
                    f"{function}() does not exist - nobody can re-derive it "
                    f"when the corpus moves, which is how it goes stale "
                    f"unnoticed", WARNING))
    return out


def check_every_check_can_fail(vault: Path,
                               loaded: list[Note] | None = None) -> list[Violation]:
    """A check nobody has seen fail is not evidence that nothing is wrong.

    The duplicate detector reported "none found" from a floor above the highest
    similarity in the corpus; the difference between *clean* and *inert* was
    invisible. Every check here should have a test that makes it fire, and this
    reports the ones that do not.

    A warning, not an error: the fix is writing a test, and nobody should be
    blocked from a run by it.
    """
    import re

    tests_dir = Path(__file__).resolve().parent / "tests"
    if not tests_dir.exists():
        return []
    exercised: set[str] = set()
    for path in tests_dir.glob("test_*.py"):
        text = path.read_text(encoding="utf-8", errors="replace")
        exercised.update(re.findall(r"run_check\(\s*[\"']([a-z_]+)[\"']", text))
    return [
        Violation("every_check_can_fail", name,
                  "no test calls `run_check` on this check, so it has only ever "
                  "been observed passing - which cannot be distinguished from "
                  "it being unable to detect anything",
                  WARNING)
        for name in sorted(set(CHECKS) - exercised - {"every_check_can_fail"})
    ]

CHECKS: dict[str, Callable[[Path], list[Violation]]] = {
    "recorded_property_is_findable": check_recorded_property_is_findable,
    "content_model_parses": check_content_model_parses,
    "frontmatter_complete": check_frontmatter_complete,
    "sections_complete": check_sections_complete,
    "axis_values_known": check_axis_values_known,
    "derived_views_current": check_derived_views_current,
    "frontmatter_parses": check_frontmatter_parses,
    "wikilinks_resolve": check_wikilinks_resolve,
    "distinct_resource_prose": check_distinct_resource_prose,
    "resource_has_url_and_licence": check_resource_has_url_and_licence,
    "license_class_known": check_license_class_known,
    "container_has_expansion_status": check_container_has_expansion_status,
    "topic_keys_known": check_topic_keys_known,
    "application_record_shape": check_application_record_shape,
    "taxonomy_matrix_agrees": check_taxonomy_matrix_agrees,
    "resource_has_parent_topic": check_resource_has_parent_topic,
    "orphan_notes": check_orphan_notes,
    "every_topic_is_routable": check_every_topic_is_routable,
    "recorded_claims_are_current": check_recorded_claims_are_current,
    "application_links_a_resource": check_application_links_a_resource,
    "structural_claims_match_surveys": check_structural_claims_match_surveys,
    "thresholds_carry_their_distribution": check_thresholds_carry_their_distribution,
    "every_check_can_fail": check_every_check_can_fail,
}


# --------------------------------------------------------------------- entry

def run_all(vault: Path | None = None) -> list[Violation]:
    root = Path(vault) if vault else vault_root()
    loaded = _load(root)
    out: list[Violation] = []
    for name, check in CHECKS.items():
        out.extend(check(root, loaded))
    return sorted(out, key=lambda v: (v.severity != ERROR, v.check, v.note))


def run_check(name: str, vault: Path | None = None) -> list[Violation]:
    if name not in CHECKS:
        raise KeyError(f"no such check '{name}'. Known: {', '.join(sorted(CHECKS))}")
    root = Path(vault) if vault else vault_root()
    return CHECKS[name](root, _load(root))


def summarise(violations: Iterable[Violation]) -> dict[str, int]:
    counts = {ERROR: 0, WARNING: 0}
    for violation in violations:
        counts[violation.severity] = counts.get(violation.severity, 0) + 1
    return counts


def exit_code(violations: Iterable[Violation]) -> int:
    """Non-zero on any error. Warnings do not fail a run."""
    return 1 if any(v.severity == ERROR for v in violations) else 0
