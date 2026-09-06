"""The vault graph - permitted use 1 of graphify, and no others.

Community detection over **the catalogue's own note link graph**. The vault is
already a graph: typed edges (`implements_pattern`, `mentions_term`,
`parent_topic`, `related_to`, `applied_resource`, `listed_in`) across every
layer, all of them written in the notes. Nothing is fetched and nothing is
inferred; this module exports what the index already holds, asks graphify to
cluster it, and reads the assignments back.

The rulings in spec 4B.3 are enforced here rather than merely cited, because
this is the component most likely to expand past its remit - a graph tool
invites you to graph everything, and graphing everything rebuilds the
component library the design rejected:

    R1  no graph of a catalogued *source* is ever built or stored here
    R2  communities live in the index, never in note frontmatter
    R3  a community is an observation; disagreements produce a report, not a change
    R4  hubs, index notes and glossary notes are excluded from centrality
    R5  graphify runs as a registered action with a bounded timeout
    R6  never on the read path
    R8  absent graphify degrades to no communities, never to an error
    R9  edge confidence is carried through
    R10 the graph records what state it described
"""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from . import index as index_mod
from . import policy
from .config import CatalogueConfig, is_hub

# Layers excluded from centrality outright. Every resource note carries
# `taxonomy_hub:: [[Taxonomy Index]]` and `mentions_term:: [[Glossary - X]]`,
# so in-degree without this exclusion ranks the router and the dictionary
# above everything they route to - the vault's version of the MARK graph's
# `Any`, `Path` and `_cfg()` problem.
# `topic` is here even though topic indexes are legitimate retrieval answers.
# Being a good answer to "where does this live" and being structurally central
# are different claims, and every note in a topic points at its index.
CENTRALITY_EXCLUDED_LAYERS = frozenset({"glossary", "index", "template", "topic"})

# Relations that mean "this is filed here", not "this is about that".
# Included in the graph, excluded from centrality for the same reason.
STRUCTURAL_RELATIONS = frozenset({"taxonomy_hub", "application_hub", "paper_hub",
                                  "listed_in", "parent_topic"})


@dataclass(frozen=True)
class GraphStats:
    nodes: int = 0
    edges: int = 0
    communities: int = 0
    centrality_scored: int = 0
    backend: str = "none"          # graphify | none
    reason: str = ""
    built_at_index: str = ""       # R10: what state the graph described
    graph_path: str = ""


@dataclass(frozen=True)
class Disagreement:
    """A community and a topic that do not agree. Reported, never applied."""

    community: int
    topic: str
    members_in_topic: int
    members_elsewhere: int
    examples: tuple[str, ...] = ()


# ------------------------------------------------------------------- export

def export(db_path: Path | None = None, out_path: Path | None = None) -> Path:
    """Write the vault's link graph as node-link JSON.

    Node shape follows what graphify already emits and consumes (External
    Dependencies Reference 2A.2), so the same tool reads it without a
    translation layer.
    """
    conn = index_mod.connect(db_path)
    try:
        index_mod.init(conn)
        note_rows = conn.execute(
            "SELECT name, layer, type, path FROM note ORDER BY name").fetchall()
        known = {row["name"] for row in note_rows}
        nodes = [{
            "id": _slug(row["name"]),
            "label": row["name"],
            "norm_label": row["name"],
            "file_type": "document",
            "source_file": row["path"],
            "source_location": "L1",
            "_origin": "vault",
            "layer": row["layer"],
            "note_type": row["type"] or "",
        } for row in note_rows]

        links = []
        for row in conn.execute(
                "SELECT src, dst, relation FROM link ORDER BY src, dst, relation"):
            if row["dst"] not in known:
                continue                       # a broken link is integrity's problem
            links.append({
                "source": _slug(row["src"]),
                "target": _slug(row["dst"]),
                "relation": row["relation"] or "related_to",
                # R9: vault edges are written in the notes, so they are
                # extracted rather than inferred, and say so.
                "confidence": "EXTRACTED",
                "confidence_score": 1.0,
                "weight": 1.0,
                "_origin": "vault",
            })

        stamp = index_mod.get_stamp(conn, "indexed_at", "")
        document = {
            "directed": True, "multigraph": False, "graph": {}, "hyperedges": [],
            "built_at_commit": "", "built_at_index": stamp,
            "nodes": nodes, "links": links,
        }
    finally:
        conn.close()

    target = Path(out_path) if out_path else Path(tempfile.mkdtemp(
        prefix="librarian-graph-")) / "graphify-out" / "graph.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
    return target


def _slug(name: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in name).strip("_").lower()


# ------------------------------------------------------------------ graphify

def graphify_available(cfg: CatalogueConfig | None = None) -> tuple[bool, str]:
    cfg = cfg or CatalogueConfig.load()
    if not cfg.graph_enabled:
        return False, "graph disabled in library_config.json"
    binary = _binary(cfg)
    if binary is None:
        return False, (f"graphify not found at {cfg.graphify_bin} or on PATH; "
                       f"the vault graph degrades to no communities")
    if cfg.graphify_bin and binary != cfg.graphify_bin:
        # Say when a different binary is being used than the one configured.
        # A green status line for the wrong executable is worse than a red one.
        return True, (f"graphify at {binary} (configured path {cfg.graphify_bin} "
                      f"was not present; using the one on PATH)")
    return True, f"graphify available at {binary}"


def _binary(cfg: CatalogueConfig) -> str | None:
    candidate = Path(cfg.graphify_bin)
    if candidate.exists():
        return str(candidate)
    found = shutil.which("graphify")
    return found


def _cluster(graph_path: Path, cfg: CatalogueConfig) -> tuple[bool, str]:
    """Run `graphify cluster-only`, as a registered action with a timeout.

    `--no-label` is not optional: community naming calls a model, and this
    path must stay deterministic so that deleting the index and rebuilding
    reproduces the same assignments.
    """
    policy.check_action("graphify_build")
    binary = _binary(cfg)
    if binary is None:
        return False, "graphify unavailable"
    workspace = graph_path.parent.parent
    command = [binary, "cluster-only", str(workspace),
               "--graph", str(graph_path), "--no-label", "--no-viz"]
    try:
        completed = subprocess.run(command, capture_output=True, text=True,
                                   timeout=cfg.graphify_timeout_seconds)
    except subprocess.TimeoutExpired:
        return False, (f"graphify timed out after {cfg.graphify_timeout_seconds}s; "
                       f"falling back to no communities")
    except Exception as exc:                                # pragma: no cover
        return False, f"graphify failed to start: {exc}"
    if completed.returncode != 0:
        return False, f"graphify exit {completed.returncode}: " \
                      f"{(completed.stderr or completed.stdout or '')[-300:]}"
    return True, (completed.stdout or "").strip().splitlines()[-1] if completed.stdout \
        else "clustered"


# -------------------------------------------------------------------- build

def build(db_path: Path | None = None, cfg: CatalogueConfig | None = None, *,
          work_dir: Path | None = None, keep_graph: bool = False) -> GraphStats:
    """Export, cluster, ingest. Degrades to centrality-only without graphify.

    Only ever called on the vault. There is no parameter for a repository
    path and there must not be one: `NO_PERSISTENT_SOURCE_GRAPH` means a
    graph of a catalogued source lives and dies inside a workbench.
    """
    cfg = cfg or CatalogueConfig.load()
    workspace = Path(work_dir) if work_dir else Path(
        tempfile.mkdtemp(prefix="librarian-graph-"))
    graph_path = workspace / "graphify-out" / "graph.json"
    export(db_path, graph_path)

    document = json.loads(graph_path.read_text(encoding="utf-8"))
    nodes, edges = len(document["nodes"]), len(document["links"])
    stamp = document.get("built_at_index", "")

    ok, reason = graphify_available(cfg)
    backend, assignments = "none", {}
    if ok:
        clustered, detail = _cluster(graph_path, cfg)
        if clustered:
            backend = "graphify"
            document = json.loads(graph_path.read_text(encoding="utf-8"))
            assignments = {node["label"]: (node.get("community"),
                                           node.get("community_name") or "")
                           for node in document["nodes"]
                           if node.get("community") is not None}
            reason = detail
        else:
            reason = detail
    scores = centrality(db_path, cfg)
    written = _store(db_path, assignments, scores)

    if not keep_graph and work_dir is None:
        shutil.rmtree(workspace, ignore_errors=True)

    return GraphStats(
        nodes=nodes, edges=edges,
        communities=len({c for c, _ in assignments.values()}),
        centrality_scored=written, backend=backend, reason=reason,
        built_at_index=stamp,
        graph_path=str(graph_path) if keep_graph or work_dir else "")


def _store(db_path: Path | None, assignments: dict[str, tuple[int, str]],
           scores: dict[str, float]) -> int:
    """R2: the index, and only the index. Nothing is written to a note."""
    conn = index_mod.connect(db_path)
    try:
        index_mod.init(conn)
        conn.execute("DELETE FROM note_community")
        names = set(assignments) | set(scores)
        written = 0
        for name in sorted(names):
            community, label = assignments.get(name, (-1, ""))
            conn.execute(
                "INSERT OR REPLACE INTO note_community(note, community, label, "
                "centrality) VALUES(?,?,?,?)",
                (name, community if community is not None else -1, label,
                 scores.get(name)))
            written += 1
        index_mod.stamp(conn, "graph_built_at", index_mod.now_iso())
        conn.commit()
        return written
    finally:
        conn.close()


# --------------------------------------------------------------- centrality

def centrality(db_path: Path | None = None,
               cfg: CatalogueConfig | None = None) -> dict[str, float]:
    """Filtered, log-dampened in-degree.

    R4 requires exclusion rather than down-weighting, so hubs, index notes and
    glossary notes are removed from the graph *before* anything is counted,
    and structural edges ("filed under") do not count as significance.
    """
    import math

    cfg = cfg or CatalogueConfig.load()
    excluded = set(cfg.centrality_exclude)
    conn = index_mod.connect(db_path)
    try:
        index_mod.init(conn)
        layers = {row["name"]: (row["layer"], row["type"] or "")
                  for row in conn.execute("SELECT name, layer, type FROM note")}
        counts: dict[str, int] = {}
        for row in conn.execute("SELECT src, dst, relation FROM link"):
            dst = row["dst"]
            if dst in excluded or dst not in layers:
                continue
            layer, note_type = layers[dst]
            if layer in CENTRALITY_EXCLUDED_LAYERS or is_hub(note_type):
                continue
            if row["relation"] in STRUCTURAL_RELATIONS:
                continue
            counts[dst] = counts.get(dst, 0) + 1
    finally:
        conn.close()

    if not counts:
        return {}
    # Log-dampened, exactly as star counts already are: a note with fifty
    # inbound links is not fifty times more central than one with one.
    top = math.log1p(max(counts.values())) or 1.0
    return {name: round(math.log1p(value) / top, 4) for name, value in counts.items()}


def communities(db_path: Path | None = None) -> dict[str, int]:
    conn = index_mod.connect(db_path)
    try:
        index_mod.init(conn)
        return {row["note"]: row["community"] for row in conn.execute(
            "SELECT note, community FROM note_community WHERE community >= 0")}
    finally:
        conn.close()


# ----------------------------------------------------------------- advisory

# ------------------------------------------------------- community reports

# What a community report is *for*: the catalogue can already say what is where
# and which of those is worth reading. It cannot say what it has become. A
# question like "what does this vault actually cover in retrieval" has no answer
# in any single note, so it has to be precomputed at the level of the cluster -
# which is the one idea worth taking from microsoft/graphrag, whose
# `summarize_communities` writes exactly this artefact and whose `global_search`
# then map-reduces over it.
#
# Two differences from graphrag, both deliberate:
#
#   No model.  graphrag prompts an LLM per community. This assembles the summary
#              from what the members demonstrably share - their topics, patterns,
#              glossary terms, licence classes and most central members. Every
#              clause traces to a link that exists in a note. LM Studio is not
#              reachable on this host, but that is not the reason: a summary
#              nobody can trace is a summary nobody can check, and the same
#              `why`-carrying discipline the read path already enforces applies
#              here.
#
#   Advisory.  R3. A report is an observation written down. It may not create,
#              rename or reassign a topic, and it lives in the disposable index.

REPORT_MIN_MEMBERS = 3          # below this a "community" is an accident of layout
REPORT_TOP_MEMBERS = 8


@dataclass(frozen=True)
class CommunityReport:
    community: int
    label: str
    size: int
    topics: dict[str, int]
    members: tuple[str, ...]
    summary: str

    @property
    def crosses_topics(self) -> bool:
        """The finding worth having. A community confined to one topic mostly
        restates the topic; one spanning several is a grouping nobody assigned."""
        return len([t for t in self.topics if t]) > 1


def _member_facts(conn, names: Iterable[str]) -> dict[str, Any]:
    """Everything a report may assert, read from the index and nowhere else."""
    names = list(names)
    if not names:
        return {}
    marks = ",".join("?" for _ in names)
    rows = conn.execute(
        f"SELECT n.name, n.layer, f.primary_topic, f.license_class, f.maturity_stage "
        f"FROM note n LEFT JOIN resource_facet f ON f.name = n.name "
        f"WHERE n.name IN ({marks})", names).fetchall()
    links = conn.execute(
        f"SELECT dst, relation, COUNT(*) AS n FROM link "
        f"WHERE src IN ({marks}) AND relation IN "
        f"('implements_pattern','mentions_term') GROUP BY dst, relation "
        f"ORDER BY n DESC", names).fetchall()
    return {"rows": rows, "links": links}


def _phrase(counter: list[tuple[str, int]], limit: int = 3) -> str:
    return ", ".join(name for name, _ in counter[:limit])


def _summarise(community: int, label: str, members: list[str],
               facts: dict[str, Any]) -> tuple[str, dict[str, int]]:
    """Assemble the prose. Every clause is a fact from the index."""
    from collections import Counter

    rows = facts.get("rows", [])
    layers = Counter(r["layer"] for r in rows)
    topics = Counter(r["primary_topic"] for r in rows if r["primary_topic"])
    licences = Counter(r["license_class"] for r in rows if r["license_class"])
    maturity = Counter(r["maturity_stage"] for r in rows if r["maturity_stage"])

    patterns = [(r["dst"].replace("Pattern - ", ""), r["n"])
                for r in facts.get("links", []) if r["relation"] == "implements_pattern"]
    terms = [(r["dst"].replace("Glossary - ", ""), r["n"])
             for r in facts.get("links", []) if r["relation"] == "mentions_term"]

    resources = layers.get("resource", 0) + layers.get("review", 0)
    parts: list[str] = []

    shape = ", ".join(f"{count} {layer}" for layer, count in layers.most_common())
    parts.append(f"{len(members)} notes ({shape}).")

    if topics:
        if len(topics) == 1:
            only, _ = topics.most_common(1)[0]
            parts.append(f"All of its resources sit under {only}, so this community "
                         f"largely restates a topic rather than finding one.")
        else:
            spread = "; ".join(f"{name} ({n})" for name, n in topics.most_common(4))
            parts.append(f"Its resources span {len(topics)} topics — {spread} — "
                         f"a grouping nobody assigned.")

    if patterns:
        parts.append(f"What binds it: {_phrase(patterns)}.")
    if terms:
        parts.append(f"Recurring vocabulary: {_phrase(terms, 4)}.")

    if resources and licences:
        unknown = licences.get("Unknown", 0)
        restrictive = sum(licences.get(k, 0) for k in
                          ("Copyleft", "Weak_Copyleft", "Source_Available"))
        if unknown:
            parts.append(f"{unknown} of {resources} resources here "
                         f"{'has' if unknown == 1 else 'have'} no usable licence, so "
                         f"a constrained query cannot offer "
                         f"{'it' if unknown == 1 else 'them'}.")
        if restrictive:
            parts.append(f"{restrictive} "
                         f"{'carries' if restrictive == 1 else 'carry'} a copyleft or "
                         f"source-available licence.")
    if maturity.get("Abandoned"):
        count = maturity["Abandoned"]
        parts.append(f"{count} {'is' if count == 1 else 'are'} recorded as abandoned.")

    if members:
        parts.append(f"Most connected: {', '.join(members[:3])}.")

    return " ".join(parts), dict(topics)


def report(db_path: Path | None = None, *,
           min_members: int = REPORT_MIN_MEMBERS) -> list[CommunityReport]:
    """Write a summary of every community into the index. R8: no communities,
    no reports, and that is a degraded result rather than an error."""
    conn = index_mod.connect(db_path)
    try:
        index_mod.init(conn)
        grouped: dict[int, list[str]] = {}
        labels: dict[int, str] = {}
        for row in conn.execute(
                "SELECT note, community, label, centrality FROM note_community "
                "WHERE community >= 0 ORDER BY community, "
                "COALESCE(centrality, 0) DESC, note"):
            grouped.setdefault(row["community"], []).append(row["note"])
            if row["label"]:
                labels.setdefault(row["community"], row["label"])

        conn.execute("DELETE FROM community_report")
        built = index_mod.now_iso()
        out: list[CommunityReport] = []
        for community, members in sorted(grouped.items()):
            if len(members) < min_members:
                continue
            facts = _member_facts(conn, members)
            summary, topics = _summarise(community, labels.get(community, ""),
                                         members, facts)
            entry = CommunityReport(community, labels.get(community, ""),
                                    len(members), topics,
                                    tuple(members[:REPORT_TOP_MEMBERS]), summary)
            conn.execute(
                "INSERT OR REPLACE INTO community_report"
                "(community, label, size, topics, summary, members, built_at) "
                "VALUES(?,?,?,?,?,?,?)",
                (entry.community, entry.label, entry.size, json.dumps(entry.topics),
                 entry.summary, json.dumps(list(entry.members)), built))
            out.append(entry)
        conn.commit()
        return out
    finally:
        conn.close()


def reports(db_path: Path | None = None) -> list[CommunityReport]:
    """Read back what `report()` stored. Cheap enough for the read path -
    it is a table scan of at most a few dozen rows, not a graphify call (R6)."""
    conn = index_mod.connect(db_path)
    try:
        index_mod.init(conn)
        rows = conn.execute(
            "SELECT * FROM community_report ORDER BY size DESC").fetchall()
    finally:
        conn.close()
    return [CommunityReport(r["community"], r["label"] or "", r["size"],
                            json.loads(r["topics"] or "{}"),
                            tuple(json.loads(r["members"] or "[]")),
                            r["summary"])
            for r in rows]


def disagreements(db_path: Path | None = None, *, min_members: int = 3
                  ) -> list[Disagreement]:
    """Where communities and topics disagree - a report for a person.

    R3: a community is an observation, not a category. This function returns
    findings and changes nothing; [[Scouting Domains]] and the topic indexes
    remain the sole authority over what a topic is.
    """
    conn = index_mod.connect(db_path)
    try:
        index_mod.init(conn)
        rows = conn.execute(
            "SELECT nc.note AS note, nc.community AS community, l.dst AS topic "
            "FROM note_community nc "
            "LEFT JOIN link l ON l.src = nc.note AND l.relation = 'parent_topic' "
            "WHERE nc.community >= 0").fetchall()
    finally:
        conn.close()

    by_community: dict[int, list[tuple[str, str]]] = {}
    for row in rows:
        by_community.setdefault(row["community"], []).append(
            (row["note"], row["topic"] or ""))

    out: list[Disagreement] = []
    for community, members in by_community.items():
        topics = [topic for _, topic in members if topic]
        if len(members) < min_members or not topics:
            continue
        dominant = max(set(topics), key=topics.count)
        inside = topics.count(dominant)
        outside = len(topics) - inside
        if outside and outside >= inside / 2:
            examples = tuple(note for note, topic in members
                             if topic and topic != dominant)[:5]
            out.append(Disagreement(community, dominant, inside, outside, examples))
    return sorted(out, key=lambda d: -d.members_elsewhere)


def measured_gap_fit(db_path: Path | None = None,
                     cfg: CatalogueConfig | None = None) -> dict[str, float]:
    """Community size as an alternative basis for the gap-fit signal.

    Behind `measured_gap_fit` in config and off by default. Swapping a ranking
    signal's basis is exactly the change that must be measured against the
    eval set before it is trusted, so this returns numbers for comparison and
    wires into nothing (spec 4B.4).
    """
    cfg = cfg or CatalogueConfig.load()
    if not cfg.measured_gap_fit:
        return {}
    assignments = communities(db_path)
    if not assignments:
        return {}
    conn = index_mod.connect(db_path)
    try:
        topic_of = {row["src"]: row["dst"] for row in conn.execute(
            "SELECT src, dst FROM link WHERE relation = 'parent_topic'")}
        keys = {row["name"]: json.loads(row["frontmatter"]).get("topic_key")
                for row in conn.execute(
                    "SELECT name, frontmatter FROM note WHERE layer = 'topic'")}
    finally:
        conn.close()

    sizes: dict[str, int] = {}
    for note, _ in assignments.items():
        topic = topic_of.get(note)
        key = keys.get(topic) if topic else None
        if key:
            sizes[key] = sizes.get(key, 0) + 1
    if not sizes:
        return {}
    largest = max(sizes.values()) or 1
    # Thin topics score high, exactly as the declared-count version does.
    return {key: round(1.0 - (size / largest), 4) for key, size in sizes.items()}
