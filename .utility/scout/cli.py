"""Command line entry point.

    python -m scout status
    python -m scout discover [--tier2] [--per-query N]
    python -m scout expand
    python -m scout scout [--limit N] [--readme]
    python -m scout enrich [--limit N]
    python -m scout rank
    python -m scout freeze [--force]
    python -m scout dive [--limit N]
    python -m scout publish
    python -m scout cycle          # discover -> scout -> enrich -> rank -> freeze

Stages are separate commands on purpose. This host keeps one task model
resident, so the scout batch and the deep dive must be run as distinct
passes rather than interleaved.
"""
from __future__ import annotations

import argparse
import json
import sys

from .config import ScoutConfig
from . import db, discovery, evaluate, deep_dive, scout_pass
from .domains import rotation, resource_counts


def cmd_status(args, cfg: ScoutConfig) -> int:
    db.init()
    with db.connect() as conn:
        counts = db.counts(conn)
        cohort = db.active_cohort(conn)
        ranked = counts.get("ranked", 0)
        print("queue state:")
        for state in db.STATES:
            print(f"  {state:<12} {counts.get(state, 0)}")
        print(f"\nactive cohort: {cohort or 'none'}")
        print(f"cohort gate:   {ranked}/{cfg.cohort_size} ranked")
        if cohort:
            row = conn.execute(
                "SELECT COUNT(*) n FROM scout_queue WHERE cohort_id=? AND state='queued'",
                (cohort,)).fetchone()
            print(f"remaining in cohort: {row['n']}")
    print("\ntopic coverage (gap-fit input):")
    for key, count in sorted(resource_counts().items(), key=lambda kv: kv[1]):
        print(f"  {key:<32} {count}")
    return 0


def cmd_discover(args, cfg: ScoutConfig) -> int:
    db.init()
    domains = rotation(cfg, include_tier2=args.tier2)
    if not domains:
        print("no domains in rotation", file=sys.stderr)
        return 1
    totals = {"added": 0, "corroborated": 0}
    with db.connect() as conn:
        for domain in domains:
            try:
                result = discovery.discover_domain(conn, domain, cfg, args.per_query)
            except discovery.RateLimited as exc:
                print(f"stopped: {exc}", file=sys.stderr)
                break
            totals["added"] += result["added"]
            totals["corroborated"] += result["corroborated"]
            print(f"  {domain.key:<28} +{result['added']:<4} "
                  f"({result['corroborated']} already seen)")
    print(f"\ndiscovered {totals['added']} new, "
          f"{totals['corroborated']} corroborations")
    return 0


def cmd_expand(args, cfg: ScoutConfig) -> int:
    db.init()
    totals = {"added": 0, "corroborated": 0}
    with db.connect() as conn:
        for note, repo_key in discovery.container_notes():
            if not repo_key:
                continue
            readme = discovery.fetch_readme(repo_key, cfg)
            if not readme:
                print(f"  {note:<48} no README fetched")
                continue
            result = discovery.expand_container(conn, note, repo_key, cfg, readme)
            totals["added"] += result["added"]
            totals["corroborated"] += result["corroborated"]
            print(f"  {note:<48} +{result['added']} "
                  f"({result['corroborated']} already seen)")
    print(f"\nexpanded {totals['added']} new candidates")
    return 0


def cmd_scout(args, cfg: ScoutConfig) -> int:
    db.init()
    domains = rotation(cfg, include_tier2=True)
    with db.connect() as conn:
        result = scout_pass.run_batch(conn, cfg, domains, args.limit, args.readme)
    print(json.dumps(result, indent=2))
    return 0


def cmd_enrich(args, cfg: ScoutConfig) -> int:
    db.init()
    with db.connect() as conn:
        updated = evaluate.enrich_depth(conn, cfg, args.limit)
    print(f"depth probed for {updated} candidates")
    return 0


def cmd_rank(args, cfg: ScoutConfig) -> int:
    db.init()
    with db.connect() as conn:
        result = evaluate.run(conn, cfg)
    print(json.dumps(result, indent=2))
    return 0


def cmd_freeze(args, cfg: ScoutConfig) -> int:
    db.init()
    with db.connect() as conn:
        result = evaluate.freeze(conn, cfg, force=args.force)
    print(json.dumps(result, indent=2))
    if not result.get("frozen"):
        print(f"\nnot enough ranked items yet - use --force to freeze a short cohort")
    return 0


def cmd_dive(args, cfg: ScoutConfig) -> int:
    db.init()
    with db.connect() as conn:
        result = deep_dive.run(conn, cfg, limit=args.limit)
    print(json.dumps(result, indent=2))
    return 0


def cmd_publish(args, cfg: ScoutConfig) -> int:
    db.init()
    with db.connect() as conn:
        result = deep_dive.publish(conn, cfg)
    print(json.dumps(result, indent=2))
    print("\nnow run: python .utility\\build_solutions_library.py")
    return 0


def cmd_cycle(args, cfg: ScoutConfig) -> int:
    """Everything up to the cohort gate. Deliberately stops before the deep
    dive so the model swap is an explicit, separate step."""
    for step in (cmd_discover, cmd_expand, cmd_scout, cmd_enrich, cmd_rank, cmd_freeze):
        print(f"\n=== {step.__name__.replace('cmd_', '')} ===")
        code = step(args, cfg)
        if code != 0:
            return code
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="scout", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status")
    p = sub.add_parser("discover")
    p.add_argument("--tier2", action="store_true", help="include reserve domains")
    p.add_argument("--per-query", type=int, default=0, dest="per_query")
    sub.add_parser("expand")
    p = sub.add_parser("scout")
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--readme", action="store_true",
                   help="fetch README for each candidate (slower, better labels)")
    p = sub.add_parser("enrich")
    p.add_argument("--limit", type=int, default=50)
    sub.add_parser("rank")
    p = sub.add_parser("freeze")
    p.add_argument("--force", action="store_true")
    p = sub.add_parser("dive")
    p.add_argument("--limit", type=int, default=0)
    sub.add_parser("publish")
    p = sub.add_parser("cycle")
    p.add_argument("--tier2", action="store_true")
    p.add_argument("--per-query", type=int, default=0, dest="per_query")
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--readme", action="store_true")
    p.add_argument("--force", action="store_true")

    args = parser.parse_args(argv)
    for attr, default in (("per_query", 0), ("limit", 0), ("readme", False),
                          ("force", False), ("tier2", False)):
        if not hasattr(args, attr):
            setattr(args, attr, default)
    cfg = ScoutConfig.load()
    handlers = {
        "status": cmd_status, "discover": cmd_discover, "expand": cmd_expand,
        "scout": cmd_scout, "enrich": cmd_enrich, "rank": cmd_rank,
        "freeze": cmd_freeze, "dive": cmd_dive, "publish": cmd_publish,
        "cycle": cmd_cycle,
    }
    return handlers[args.command](args, cfg)


if __name__ == "__main__":
    raise SystemExit(main())
