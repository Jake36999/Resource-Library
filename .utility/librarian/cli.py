"""One command per stage, deliberately.

The same reason the scout has separate commands: stages that must not
interleave should not be able to. `index` and `embed` are separate because
embedding needs a model resident and indexing does not; `graph` is separate
because it shells out; `workbench` is separate because a person opens one.

Every command prints something a person can act on and returns a meaningful
exit code, so any of them can be a build step.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import access_points as access_mod
from . import views as views_mod
from . import consult
from . import embed as embed_mod
from . import evalset
from . import graph as graph_mod
from . import components as components_mod
from . import coverage as coverage_mod
from . import duplicates as duplicates_mod
from . import provenance as provenance_mod
from . import usesignal as usesignal_mod
from . import freshness as freshness_mod
from . import relevance as relevance_mod
from . import scenariotest as scenario_mod
from . import index as index_mod
from . import integrity as integrity_mod
from . import toolchain as toolchain_mod
from .config import CatalogueConfig, index_db_path, vault_root


def _print_response(response: consult.Response, as_json: bool) -> None:
    if as_json:
        print(json.dumps(response.to_dict(), indent=2, ensure_ascii=False))
        return
    head = (f"intent: {response.intent}   tier reached: {response.tier_reached}"
            f"   eliminated by filters: {response.filtered_out}")
    if response.matched:
        head += f"   matched: {response.matched}"
    print(head)
    if not response.results:
        print("  (nothing matched)")
    for result in response.results:
        print(f"  [{result.kind}] {result.name}   {result.score:.3f}")
        print(f"      why: {result.why}")
    if response.components:
        print("\n  inside those sources:")
        for component in response.components:
            print(f"      {component.name}")
            print(f"          {component.why}")
    for advisory in response.advisories:
        print(f"\n  ! {advisory}")
    if response.facets:
        # The drop-downs, as text. A count is the size of the set that survives
        # choosing that value, because filters eliminate rather than re-rank -
        # so this shows the cost of a constraint before it is paid.
        print("\n  narrow by:")
        for axis, values in response.facets.items():
            shown = "   ".join(f"{v['value']} ({v['count']})" for v in values[:6])
            more = "   ..." if len(values) > 6 else ""
            print(f"      {axis:<20} {shown}{more}")
    print(f"\n  next: {response.next_step}")
    for note in response.notes:
        print(f"  note: {note}")


def cmd_status(args) -> int:
    counts = index_mod.counts()
    print(f"vault       {vault_root()}")
    print(f"index       {index_db_path()}")
    print(f"indexed at  {counts.pop('indexed_at')}")
    for table, count in counts.items():
        print(f"  {table:18} {count}")
    print(f"  {'index stale':18} {index_mod.is_stale()}")
    ok, reason = embed_mod.available()
    print(f"embeddings  {'yes' if ok else 'no'} - {reason}")
    ok, reason = toolchain_mod.toolchain_available()
    print(f"toolchain   {'yes' if ok else 'no'} - {reason}")
    ok, reason = graph_mod.graphify_available()
    print(f"graphify    {'yes' if ok else 'no'} - {reason}")
    return 0


def cmd_index(args) -> int:
    stats = index_mod.build(rebuild=args.rebuild)
    print(f"indexed {stats.notes} notes, {stats.chunks} chunks, {stats.links} links "
          f"in {stats.duration_s}s")
    for error in stats.errors[:20]:
        print(f"  error: {error}")
    return 1 if stats.errors else 0


def cmd_integrity(args) -> int:
    violations = (integrity_mod.run_check(args.check) if args.check
                  else integrity_mod.run_all())
    counts = integrity_mod.summarise(violations)
    for violation in violations:
        if violation.severity == integrity_mod.WARNING and args.errors_only:
            continue
        print(f"  {violation.severity:7} {violation.check:28} {violation.note}")
        print(f"          {violation.detail}")
    print(f"\n{counts.get('error', 0)} error(s), {counts.get('warning', 0)} warning(s) "
          f"over {len(integrity_mod.CHECKS)} checks")
    return integrity_mod.exit_code(violations)


def cmd_views(args) -> int:
    """Regenerate the derived views, or report their drift.

    `--check` writes nothing and exits non-zero when a view disagrees with the
    notes, so it can gate a build the way `integrity` does. Without it the
    views are brought into line and what changed is printed.
    """
    changes = views_mod.run(write=not args.check)
    for change in changes:
        print(f"  {change}")
    if not changes:
        print("derived views agree with the notes")
        return 0
    verb = "would rewrite" if args.check else "rewrote"
    print(f"\n{verb} {len(changes)} view(s)")
    return 1 if args.check else 0


def cmd_embed(args) -> int:
    try:
        stats = embed_mod.build(rebuild=args.rebuild)
    except embed_mod.EmbeddingsUnavailable as exc:
        print(f"embeddings unavailable: {exc}")
        return 2
    print(f"embedded {stats.embedded} chunk(s), skipped {stats.skipped} unchanged, "
          f"{stats.dims} dims, model {stats.model}")
    for error in stats.errors:
        print(f"  error: {error}")
    return 1 if stats.errors else 0


def cmd_graph(args) -> int:
    stats = graph_mod.build()
    print(f"graph: {stats.nodes} nodes, {stats.edges} edges, "
          f"{stats.communities} communities via {stats.backend}")
    if stats.reason:
        print(f"  {stats.reason}")
    print(f"  centrality scored for {stats.centrality_scored} notes "
          f"(hubs, index and glossary notes excluded)")
    report = graph_mod.disagreements()
    if report:
        print(f"\n{len(report)} community/topic disagreement(s) - a report, not a change:")
        for item in report:
            print(f"  community {item.community} mostly sits under {item.topic} "
                  f"({item.members_in_topic} in, {item.members_elsewhere} elsewhere)")
            if item.examples:
                print(f"    e.g. {', '.join(item.examples[:4])}")
    return 0
    entries = graph_mod.report()
    crossing = [e for e in entries if e.crosses_topics]
    print(f"  {len(entries)} community report(s); {len(crossing)} cross more than "
          f"one topic - `python -m librarian communities --crossing`")

def cmd_communities(args) -> int:
    """What the vault graph found, in prose. Reads; never clusters (R6)."""
    entries = graph_mod.reports()
    if not entries:
        print("no community reports; run `python -m librarian graph` first")
        return 0
    shown = [e for e in entries if e.crosses_topics] if args.crossing else entries
    for entry in shown:
        marker = "  [crosses topics]" if entry.crosses_topics else ""
        print(f"\ncommunity {entry.community} - {entry.size} notes{marker}")
        print(f"  {entry.summary}")
    print(f"\n{len(shown)} of {len(entries)} communities"
          f"{' that cross topics' if args.crossing else ''}")
    return 0


def cmd_access(args) -> int:
    if args.verify:
        report = access_mod.verify(limit=args.limit)
        print(f"checked {report.checked}: {report.reachable} reachable, "
              f"{report.unreachable} unreachable")
        for url, detail in report.failures:
            print(f"  unreachable (flagged, not dropped): {url} - {detail}")
        return 0
    result = access_mod.refresh()
    print(f"extracted {result['extracted']} access point(s), stored {result['stored']}")
    rows = access_mod.all_points()
    for row in rows[:args.limit or 20]:
        print(f"  {row['kind']:17} {row['source'][:28]:30} {row['url'][:60]}")
    if not rows:
        print("  none recorded yet - access points are extracted from a source's own "
              "documentation during scouting, so they arrive with the next intake run")
    return 0


def cmd_scenario(args) -> int:
    """The domain search test: can somebody mid-project find what they need?

    Randomly sampled unless a seed is given, so repeated runs explore the
    scenario corpus rather than tuning against a fixed six.
    """
    report = scenario_mod.run(sample=args.sample, seed=args.seed)
    print(scenario_mod.format_report(report))
    return 0 if report.useful_at_k >= args.threshold else 1


def cmd_provenance(args) -> int:
    """Structural numbers in notes, against the surveys they came from."""
    claims = provenance_mod.check()
    if not claims:
        print("no component store, or nothing surveyed; run "
              "`python -m librarian components build`")
        return 1
    print(provenance_mod.format_report(claims, show=args.show, limit=args.limit))
    return 0


def cmd_used(args) -> int:
    """Record what an answer turned out to be worth."""
    if args.status:
        state = usesignal_mod.readiness()
        top = sorted(usesignal_mod.weights().items(), key=lambda kv: -kv[1])
        print(usesignal_mod.format_status(state, top))
        return 0
    if not (args.query and args.note):
        print("give a query and a note, or --status")
        return 1
    usesignal_mod.record(args.query, args.note, args.verdict,
                         rank=args.rank, comment=args.comment)
    print(f"recorded: {args.verdict} - {args.note}")
    print(f"  {usesignal_mod.readiness().sentence()}")
    return 0


def cmd_duplicates(args) -> int:
    """Candidate duplicate pairs. Reports; merges nothing."""
    if args.distribution:
        for key, value in duplicates_mod.distribution().items():
            print(f"  {key:<16}{value}")
        return 0
    pairs = duplicates_mod.find(floor=args.floor)
    print(duplicates_mod.format_report(pairs[:args.limit]))
    return 0


def cmd_coverage(args) -> int:
    """Whether an answer is worth trusting, in absolute terms."""
    if args.calibrate:
        print(coverage_mod.format_calibration(coverage_mod.calibrate()))
        return 0
    if not args.question:
        print("give a question, or --calibrate")
        return 1
    response = consult.find_donor(args.question, {}, args.limit)
    verdict = coverage_mod.assess(args.question, response)
    print(f"{verdict.level.upper()}  {verdict.sentence()}")
    for result in response.results:
        print(f"  {result.score:.2f}  {result.name}")
        print(f"        {result.why}")
    return 0 if verdict.level != coverage_mod.UNCOVERED else 1


def cmd_freshness(args) -> int:
    """Re-check what the catalogue claims against what is true now.

    Writes readings into the data layer and edits nothing. `integrity` turns
    the readings that matter into warnings.
    """
    report = freshness_mod.run(stale_days=args.stale_days, limit=args.limit)
    print(freshness_mod.format_report(report))
    return 1 if (args.strict and report.warning) else 0


def cmd_components(args) -> int:
    """The data layer: what sources are made of, filtered without reading prose.

    `vocab` first if you do not know the collection - it answers *what are the
    axes here* without needing the schema or a guess.
    """
    if args.action == "build":
        report = components_mod.build()
        print(f"built from {', '.join(report.surveys)}")
        print(f"  {report.sources} sources, {report.directories} directories, "
              f"{report.extensions} extension rows, {report.signals} signals, "
              f"{report.paths} sample paths")
        if report.skipped:
            print(f"  skipped {len(report.skipped)}: {', '.join(report.skipped[:5])}")
        return 0
    if args.action == "vocab":
        print(components_mod.format_vocabulary(components_mod.vocabulary()))
        return 0
    if args.action == "status":
        state = components_mod.status()
        if not state["present"]:
            print(f"no component store at {state['path']}; run "
                  f"`python -m librarian components build`")
            return 1
        print(f"component store  {state['path']}")
        for table, n in state["counts"].items():
            print(f"  {table:<14}{n:>8}")
        return 0
    if args.action == "signal":
        if not args.value:
            print("give a signal name; `components vocab` lists them")
            return 1
        rows = components_mod.sources_with(args.value, minimum=args.min)
        if not rows:
            print(f"no source carries '{args.value}' at >= {args.min}")
            return 1
        print(f"{len(rows)} source(s) carrying '{args.value}':")
        for row in rows[:args.limit]:
            share = (f"{row['files']}/{row['file_count']}"
                     if row.get("file_count") else str(row["files"]))
            print(f"  {share:>14}  {row['repo_key']}")
        return 0
    if args.action == "profile":
        data = components_mod.profile(args.value or "")
        if not data:
            print(f"nothing recorded for '{args.value}'")
            return 1
        print(f"{data['repo_key']}  ({data['cohort']} cohort, "
              f"{data['file_count']} files, {data['language'] or 'unknown'})")
        print("  signals:    " + ", ".join(
            f"{s['signal']} {s['files']}" for s in data["signals"]) or "  (none)")
        print("  extensions: " + ", ".join(
            f"{e['extension']} {e['files']}" for e in data["extensions"][:12]))
        tops = [d for d in data["directories"] if d["parent"] is None][:12]
        print("  top level:  " + ", ".join(f"{d['name']} {d['files']}" for d in tops))
        if data["root_files"]:
            print("  root files: " + ", ".join(data["root_files"][:14]))
        return 0
    print(f"unknown action {args.action}")
    return 1


def cmd_relevance(args) -> int:
    """The relevance workbench: named ranking configurations, side by side.

    Every configuration runs against one index in one process, because both
    instruments read the vault and the vault contains this system's own index
    notes - so a number from a previous session is not comparable with one from
    this session, and a ranking change is indistinguishable from a documentation
    edit unless they are measured together.
    """
    only = [n.strip() for n in (args.only or "").split(",") if n.strip()]
    rows = relevance_mod.run(only=only or None, sample=args.scenarios)
    print(relevance_mod.format_report(rows))
    return 0


def cmd_eval(args) -> int:
    report = evalset.run()
    print(evalset.format_report(report))
    return 0 if report.hit_rate >= args.threshold else 1


def cmd_query(args) -> int:
    limit = args.limit
    if args.intent == "orient":
        response = consult.orient(args.query, limit)
    elif args.intent == "donor":
        constraints = {k: v for k, v in {
            "license_class": args.license_class,
            "deployment_target": args.deployment_target,
            "hardware_footprint": args.hardware_footprint,
            "max_age_days": args.max_age_days}.items() if v}
        response = consult.find_donor(args.query, constraints, limit)
    elif args.intent == "pattern":
        response = consult.find_pattern(args.query, limit)
    elif args.intent == "technique":
        response = consult.find_technique(args.query, args.source, limit)
    elif args.intent == "data":
        response = consult.find_data(args.query, None, limit)
    else:
        response = consult.find_precedent(args.query, limit)
    _print_response(response, args.json)
    return 0 if response.results else 1


def cmd_note(args) -> int:
    note = consult.get_note(args.name)
    if not note.get("found"):
        print(note.get("why", "not found"))
        return 1
    if args.json:
        print(json.dumps(note, indent=2, ensure_ascii=False))
    else:
        print(f"# {note['name']}  ({note['layer']} / {note['type']})")
        print(f"path: {note['path']}\n")
        print(note["body"][:4000])
    return 0


def cmd_workbench(args) -> int:
    """Mode D. Imported here, not at module scope, so the read and index
    commands carry no reference to the one subsystem that executes code."""
    from . import workbench as wb

    try:
        if args.action == "list":
            benches = wb.list_open()
            if not benches:
                print("no open workbenches")
            for bench in benches:
                mark = "documented" if bench.documented else "UNDOCUMENTED"
                print(f"  {bench.id:44} {bench.repo_key:28} {mark}")
            return 0

        if args.action == "open":
            bench = wb.open(args.target, depth=args.depth,
                            allow_no_container=args.no_container)
            print(f"opened {bench.id}")
            print(f"  source      {bench.path / 'source'}")
            print(f"  container   {bench.container or '(none)'}")
            print(f"  network     {bench.network}")
            for note in bench.notes:
                print(f"  note: {note}")
            print("\n  document it before closing; close refuses without a record")
            return 0

        if args.action == "status":
            bench = wb.status(args.target)
            print(json.dumps(bench.as_dict(), indent=2, default=str))
            return 0

        if args.action == "map":
            summary = wb.map_source(args.target, args.symbol)
            print(summary.prose())
            return 0

        if args.action == "document":
            record = json.loads(Path(args.record).read_text(encoding="utf-8"))
            path = wb.document(args.target, record, attested_by="user")
            print(f"record written: {path}")
            return 0

        if args.action == "close":
            result = wb.close(args.target, force=args.force, reason=args.reason)
            if result.refused:
                print(f"refused: {result.refused}\n  {result.detail}")
                return 1
            for item in result.persisted:
                print(f"  kept      {item}")
            for item in result.destroyed:
                print(f"  destroyed {item}")
            return 0
    except wb.WorkbenchRefused as exc:
        print(f"refused: {exc.code}\n  {exc.message}")
        return 1
    return 1


def cmd_serve(args) -> int:
    """The agent surface. Flags are forwarded rather than reimplemented, so the
    subcommand and `python -m librarian.mcp_server` cannot drift apart."""
    from . import mcp_server

    argv: list[str] = []
    if args.list:
        argv.append("--list")
    if args.read_only:
        argv.append("--read-only")
    argv += ["--tier", args.tier]
    if args.http:
        argv += ["--http", "--host", args.host, "--port", str(args.port)]
    return mcp_server.main(argv)


def cmd_brief(args) -> int:
    """Requests, from the human side. The same calls an agent makes over MCP."""
    from . import brief as brief_mod

    action = args.action
    if action == "list":
        found = brief_mod.all_briefs(args.status)
        if not found:
            print("no briefs" + (f" with status {args.status}" if args.status else ""))
            return 0
        for record in found:
            print(brief_mod.summarise(record))
            print()
        return 0

    if action == "open":
        constraints = {}
        for pair in args.constraint or []:
            axis, _, values = pair.partition("=")
            if not values:
                print(f"--constraint wants axis=value, got {pair!r}")
                return 2
            constraints.setdefault(axis.strip(), []).extend(
                v.strip() for v in values.split("|") if v.strip())
        try:
            record = brief_mod.open_brief(args.project, args.need,
                                          args.rules_out or [], constraints,
                                          created_by="user")
        except (ValueError, policy_error()) as exc:
            print(f"refused: {exc}")
            return 1
        print(brief_mod.summarise(record))
        return 0

    if action == "show":
        print(brief_mod.summarise(brief_mod.load(args.brief_id)))
        return 0

    if action == "close":
        try:
            record = brief_mod.close(args.brief_id, args.summary,
                                     discard_undisposed=args.discard)
        except policy_error() as exc:
            print(f"refused: {exc}")
            return 1
        print(brief_mod.summarise(record))
        return 0

    print(f"unknown action {action!r}")
    return 2


def cmd_staging(args) -> int:
    """The airlock: what agents proposed, and the one command that admits it."""
    from . import propose as propose_mod

    if args.action == "list":
        waiting = propose_mod.all_proposals(args.status)
        if not waiting:
            print("staging is empty")
            return 0
        for proposal in waiting:
            axes = ", ".join(f"{a}={v}" for a, v in sorted(proposal.axes.items()))
            print(f"{proposal.proposal_id}  [{proposal.status}]")
            print(f"  {proposal.repo_key}  {proposal.canonical_url}")
            print(f"  by {proposal.proposed_by}"
                  + (f" against {proposal.brief_id}" if proposal.brief_id else ""))
            if axes:
                print(f"  {axes}")
            print()
        return 0

    if args.action == "rederive":
        lister = None
        if args.deep:
            # `agent_surface` is a ladder of paths and a staged proposal keeps
            # none, so filling it needs the tree again. A blobless listing over
            # the git protocol costs no API budget.
            from scout.survey import list_tree

            def lister(key: str) -> list[str]:
                try:
                    return list_tree(key)
                except Exception as exc:              # noqa: BLE001
                    print(f"  {key}: no listing ({exc})")
                    return []

        touched = 0
        for proposal in propose_mod.all_proposals(propose_mod.STAGED):
            paths = lister(proposal.repo_key) if lister else None
            result = propose_mod.rederive(proposal, paths=paths)
            if result["changed"]:
                touched += 1
                print(f"{result['repo_key']}: {result['changed']}")
        print(f"{touched} proposal(s) updated; no model calls, no network")
        return 0

    if args.action == "show":
        proposal = propose_mod.load(args.proposal_id)
        print(propose_mod.render(proposal, {
            "Bottom Line": "<written at promotion>",
            "What It Solves": "<written at promotion>"}))
        return 0

    if args.action == "promote":
        result = propose_mod.promote(
            args.proposal_id, args.bottom_line, args.what_it_solves,
            primary_topic=args.topic, dry_run=args.dry_run)
        if result.get("status") == "rejected":
            print("rejected - the vault would not accept this note:")
            for violation in result["violations"]:
                print(f"  - {violation}")
            return 1
        if result.get("status") == "would_write":
            print(result["text"])
            return 0
        print(f"wrote {result['path']}")
        return 0

    print(f"unknown action {args.action!r}")
    return 2


def cmd_queue(args) -> int:
    """Sources someone is using that the catalogue does not hold."""
    from . import enrich

    if args.action == "list":
        entries = enrich.all_entries(args.status)
        if not entries:
            print("the queue is empty"
                  + (f" for status {args.status}" if args.status else ""))
            return 0
        # Most-sighted first: something three projects reached for
        # independently is worth charting before something nobody repeated.
        for entry in sorted(entries, key=lambda e: -e.sightings):
            print(enrich.summarise(entry))
            print()
        return 0

    if args.action == "add":
        try:
            result = enrich.log_use(args.repo, reported_by="user",
                                    project=args.project, why=args.why)
        except ValueError as exc:
            print(f"refused: {exc}")
            return 1
        print(f"{result['status']}: {result.get('note') or result.get('entry_id')}")
        if result.get("next"):
            print(f"  {result['next']}")
        return 0

    if args.action == "skip":
        try:
            entry = enrich.resolve(args.repo, enrich.SKIPPED,
                                   resolution=args.why)
        except (ValueError, policy_error()) as exc:
            print(f"refused: {exc}")
            return 1
        print(enrich.summarise(entry))
        return 0

    print(f"unknown action {args.action!r}")
    return 2


def cmd_populate(args) -> int:
    """Run the local-model library agent over a brief or the queue.

    Refuses rather than half-running when LM Studio is not reachable: a
    population pass that silently charts nothing looks exactly like a
    population pass that found nothing.
    """
    from . import populate
    from .localmodel import LocalModel, ModelUnavailable

    try:
        model = LocalModel.connect()
    except ModelUnavailable as exc:
        print(f"no local model: {exc}")
        return 2

    try:
        fetchers = populate.Fetchers.live()
    except ImportError as exc:
        print(f"the scouting pipeline is not importable: {exc}")
        return 2

    if args.what == "queue":
        def say(line: str) -> None:
            print(line, flush=True)

        log = populate.run_queue(model=model, fetchers=fetchers,
                                 limit=args.limit, agent=args.agent,
                                 progress=say)
    elif args.what == "brief":
        if not args.brief_id:
            print("populate brief needs a brief id")
            return 2
        log = populate.run_brief(args.brief_id, model=model, fetchers=fetchers,
                                 limit=args.limit, agent=args.agent)
    else:
        print(f"unknown target {args.what!r}")
        return 2

    for line in log.notes:
        print(f"  {line}")
    print(log.summary())
    print("nothing reached the vault; review with `librarian staging list`")
    return 0


def policy_error():
    from .policy import PolicyError

    return PolicyError


def webapp_default_port() -> int:
    """Read from the module rather than repeated here, so the help text and the
    server cannot disagree about where it listens."""
    from . import webapp

    return webapp.DEFAULT_PORT


def cmd_web(args) -> int:
    """The person surface. Same engine, rendered as a catalogue rather than a
    transcript, because narrowing by axis is a different act from asking."""
    from . import webapp

    return webapp.serve(host=args.host, port=args.port,
                        open_browser=not args.no_browser)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="librarian",
        description="Consult and maintain the Resource Library catalogue.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="what the index holds and what is reachable"
                   ).set_defaults(func=cmd_status)

    p = sub.add_parser("index", help="rebuild the derived store from the vault")
    p.add_argument("--rebuild", action="store_true",
                   help="drop derived rows first, including embeddings")
    p.set_defaults(func=cmd_index)

    p = sub.add_parser("integrity", help="run the vault assertions")
    p.add_argument("--check", help="run one named check")
    p.add_argument("--errors-only", action="store_true")
    p.set_defaults(func=cmd_integrity)

    p = sub.add_parser("views", help="regenerate the derived views from the notes")
    p.add_argument("--check", action="store_true",
                   help="report drift and exit non-zero; write nothing")
    p.set_defaults(func=cmd_views)

    p = sub.add_parser("embed", help="build chunk embeddings via LM Studio")
    p.add_argument("--rebuild", action="store_true")
    p.set_defaults(func=cmd_embed)

    sub.add_parser("graph", help="vault communities and filtered centrality"
                   ).set_defaults(func=cmd_graph)

    p = sub.add_parser("communities", help="what the vault graph found, in prose")
    p.add_argument("--crossing", action="store_true",
                   help="only communities that span more than one topic")
    p.set_defaults(func=cmd_communities)

    p = sub.add_parser("access", help="access points: extract, list, verify")
    p.add_argument("--verify", action="store_true", help="check reachability")
    p.add_argument("--limit", type=int, default=0)
    p.set_defaults(func=cmd_access)

    p = sub.add_parser("scenario",
                       help="domain search test: real components, described in their own terms")
    p.add_argument("--sample", type=int, default=scenario_mod.DEFAULT_SAMPLE,
                   help="how many scenarios to draw; 0 runs all of them")
    p.add_argument("--seed", type=int, default=None, help="reproduce a previous run")
    p.add_argument("--threshold", type=float, default=0.8,
                   help="minimum useful@5 before the command fails")
    p.set_defaults(func=cmd_scenario)

    p = sub.add_parser("provenance",
                       help="check the catalogue's own structural claims against the surveys")
    p.add_argument("--show", default=provenance_mod.CONTRADICTED,
                   choices=[provenance_mod.SUPPORTED, provenance_mod.UNSUPPORTED,
                            provenance_mod.CONTRADICTED])
    p.add_argument("--limit", type=int, default=25)
    p.set_defaults(func=cmd_provenance)

    p = sub.add_parser("used",
                       help="record what an answer was worth, so ranking can eventually learn")
    p.add_argument("query", nargs="?", default="")
    p.add_argument("note", nargs="?", default="")
    p.add_argument("--verdict", default="opened", choices=list(usesignal_mod.VERDICTS))
    p.add_argument("--rank", type=int, default=None)
    p.add_argument("--comment", default="")
    p.add_argument("--status", action="store_true",
                   help="how much signal has accumulated, and whether it is enough")
    p.set_defaults(func=cmd_used)

    p = sub.add_parser("duplicates",
                       help="candidate near-duplicate sources; reports, never merges")
    p.add_argument("--floor", type=float, default=duplicates_mod.SEMANTIC_FLOOR)
    p.add_argument("--limit", type=int, default=15)
    p.add_argument("--distribution", action="store_true",
                   help="the similarity spread, so a floor is derived not guessed")
    p.set_defaults(func=cmd_duplicates)

    p = sub.add_parser("coverage",
                       help="does the catalogue actually cover this question?")
    p.add_argument("question", nargs="?", default="")
    p.add_argument("--limit", type=int, default=5)
    p.add_argument("--calibrate", action="store_true",
                   help="fit the verdict against the scenario set and show the confusion table")
    p.set_defaults(func=cmd_coverage)

    p = sub.add_parser("freshness",
                       help="re-check recorded facts against upstream; reports, never edits")
    p.add_argument("--stale-days", type=float, default=7.0,
                   help="skip sources checked more recently than this")
    p.add_argument("--limit", type=int, default=None,
                   help="stop after this many checks; the API budget is the constraint")
    p.add_argument("--strict", action="store_true",
                   help="exit non-zero when a recorded claim is now wrong")
    p.set_defaults(func=cmd_freshness)

    p = sub.add_parser("components",
                       help="the data layer: filter sources by what they are made of")
    p.add_argument("action",
                   choices=["vocab", "signal", "profile", "build", "status"],
                   help="vocab lists the filterable axes; start there")
    p.add_argument("value", nargs="?", default="",
                   help="signal name, or repo_key for profile")
    p.add_argument("--min", type=int, default=1, help="minimum matching files")
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(func=cmd_components)

    p = sub.add_parser("relevance",
                       help="compare ranking configurations side by side on one index")
    p.add_argument("--only", default="",
                   help="comma-separated configuration names from rank_configs.json")
    p.add_argument("--scenarios", type=int, default=0,
                   help="scenarios per configuration; 0 runs all of them")
    p.set_defaults(func=cmd_relevance)

    p = sub.add_parser("eval", help="run the retrieval evaluation set")
    p.add_argument("--threshold", type=float, default=0.7,
                   help="minimum hit rate for exit code 0")
    p.set_defaults(func=cmd_eval)

    p = sub.add_parser("query", help="ask the catalogue")
    p.add_argument("intent", choices=["orient", "donor", "pattern", "technique",
                                      "data", "precedent"])
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--json", action="store_true")
    p.add_argument("--license-class", dest="license_class", default="")
    p.add_argument("--deployment-target", dest="deployment_target", default="")
    p.add_argument("--hardware-footprint", dest="hardware_footprint", default="")
    p.add_argument("--max-age-days", dest="max_age_days", type=int, default=0)
    p.add_argument("--source", default="")
    p.set_defaults(func=cmd_query)

    p = sub.add_parser("note", help="print one note")
    p.add_argument("name")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_note)

    p = sub.add_parser("workbench", help="Mode D: open a source, engage, document, close")
    p.add_argument("action", choices=["open", "status", "list", "map", "document",
                                      "close"])
    p.add_argument("target", nargs="?", default="",
                   help="repo_key for open; workbench id for the rest")
    p.add_argument("--depth", type=int, default=1)
    p.add_argument("--symbol", default="", help="closure target, for map")
    p.add_argument("--record", default="", help="JSON application record, for document")
    p.add_argument("--force", action="store_true",
                   help="close an abandoned engagement; requires --reason")
    p.add_argument("--reason", default="")
    p.add_argument("--no-container", dest="no_container", action="store_true",
                   help="read the clone without a sandbox; nothing may be executed")
    p.set_defaults(func=cmd_workbench)

    p = sub.add_parser("brief", help="research requests: open, list, show, close")
    p.add_argument("action", choices=["open", "list", "show", "close"])
    p.add_argument("brief_id", nargs="?", default="")
    p.add_argument("--project", default="", help="who is asking")
    p.add_argument("--need", default="", help="what they need, in their words")
    p.add_argument("--rules-out", action="append", dest="rules_out",
                   help="what a candidate must not assume; required, repeatable")
    p.add_argument("--constraint", action="append",
                   help="axis=Value or axis=Value|Value, repeatable")
    p.add_argument("--status", default="", help="filter: open, claimed, closed")
    p.add_argument("--summary", default="", help="required to close")
    p.add_argument("--discard", action="store_true",
                   help="close despite undecided candidates, on the record")
    p.set_defaults(func=cmd_brief)

    p = sub.add_parser("staging", help="the airlock: proposed notes awaiting review")
    p.add_argument("action",
                   choices=["list", "show", "promote", "rederive"])
    p.add_argument("proposal_id", nargs="?", default="")
    p.add_argument("--status", default="", help="filter: staged, promoted")
    p.add_argument("--bottom-line", dest="bottom_line", default="",
                   help="required to promote; the sentence a reader acts on")
    p.add_argument("--what-it-solves", dest="what_it_solves", default="",
                   help="required to promote")
    p.add_argument("--topic", default="", help="primary_topic for the note")
    p.add_argument("--dry-run", action="store_true",
                   help="render the note without writing it")
    p.add_argument("--deep", action="store_true",
                   help="re-list each repository so path-derived axes "
                        "(agent_surface) can be filled; no API budget")
    p.set_defaults(func=cmd_staging)

    p = sub.add_parser("queue", help="sources in use that are not catalogued yet")
    p.add_argument("action", choices=["list", "add", "skip"])
    p.add_argument("repo", nargs="?", default="",
                   help="owner/repo or a github URL; an entry id for skip")
    p.add_argument("--project", default="", help="which project is using it")
    p.add_argument("--why", default="", help="one sentence; required to skip")
    p.add_argument("--status", default="", help="filter: queued, claimed, skipped")
    p.set_defaults(func=cmd_queue)

    p = sub.add_parser("populate",
                       help="run the local-model library agent (LM Studio)")
    p.add_argument("what", choices=["brief", "queue"])
    p.add_argument("brief_id", nargs="?", default="")
    p.add_argument("--limit", type=int, default=8,
                   help="stop after this many proposals")
    p.add_argument("--agent", default="library-agent",
                   help="recorded as ingestion_agent on what it stages")
    p.set_defaults(func=cmd_populate)

    p = sub.add_parser("serve", help="the MCP surface, over stdio or loopback HTTP")
    p.add_argument("--list", action="store_true",
                   help="print the tool surface and its declared effects")
    p.add_argument("--read-only", action="store_true",
                   help="do not expose any write")
    p.add_argument("--tier", default="curate",
                   choices=["consult", "contribute", "curate"],
                   help="how much of the surface to expose; a library agent "
                        "wants contribute, which cannot alter a note")
    p.add_argument("--http", action="store_true",
                   help="serve over loopback HTTP instead of stdio")
    p.add_argument("--host", default="127.0.0.1",
                   help="loopback only; anything else is refused")
    p.add_argument("--port", type=int, default=8321)
    p.set_defaults(func=cmd_serve)

    p = sub.add_parser("web", help="the faceted search page, in a browser")
    p.add_argument("--host", default="127.0.0.1",
                   help="loopback only; anything else is refused")
    p.add_argument("--port", type=int, default=webapp_default_port())
    p.add_argument("--no-browser", action="store_true",
                   help="do not open a browser window")
    p.set_defaults(func=cmd_web)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":                                 # pragma: no cover
    raise SystemExit(main())
