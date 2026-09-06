"""Stage 1 - discovery. Deterministic: no model runs here.

Candidates come from GitHub search against the domain register's seed
queries, and from expanding aggregator repositories already in the catalogue.
Container expansion is the densest available vein and costs nothing but
parsing - an awesome list already curated by a human is a stronger starting
signal than a raw search hit.
"""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Iterable

from .config import LOG_DIR, ScoutConfig, vault_root as _vault_root, github_token
from . import db
from .domains import Domain

GITHUB_URL = re.compile(r"https?://(?:www\.)?github\.com/([A-Za-z0-9._-]+)/([A-Za-z0-9._-]+)")
MD_LINK = re.compile(r"\[([^\]]{1,120})\]\((https?://[^\s)]+)\)")


class RateLimited(RuntimeError):
    """Raised when GitHub refuses further requests for now."""


def _request(url: str, cfg: ScoutConfig) -> Any:
    request = urllib.request.Request(url, method="GET")
    request.add_header("User-Agent", cfg.user_agent)
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")
    token = github_token()
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(request, timeout=cfg.request_timeout) as response:
            return json.loads(response.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as exc:
        if exc.code in (403, 429):
            raise RateLimited(f"GitHub rate limit hit ({exc.code}). "
                              "Set GITHUB_TOKEN to raise 60/hr to 5000/hr.") from exc
        raise


def repo_key_from_url(url: str) -> str | None:
    match = GITHUB_URL.search(url or "")
    if not match:
        return None
    owner, repo = match.group(1), match.group(2)
    if repo.endswith(".git"):
        repo = repo[:-4]
    # /owner/repo/tree/... and non-repository paths are not resources
    if owner.lower() in {"orgs", "sponsors", "topics", "collections", "features"}:
        return None
    return f"{owner}/{repo}"


def github_payload(item: dict[str, Any]) -> dict[str, Any]:
    licence = item.get("license") or {}
    return {
        "full_name": item.get("full_name") or "",
        "description": item.get("description") or "",
        "language": item.get("language") or "",
        "license_spdx": licence.get("spdx_id") or "UNKNOWN",
        "license_name": licence.get("name") or "Unknown",
        "default_branch": item.get("default_branch") or "main",
        "topics": item.get("topics") or [],
        "homepage": item.get("homepage") or "",
        "archived": bool(item.get("archived")),
        "disabled": bool(item.get("disabled")),
        "stars": int(item.get("stargazers_count") or 0),
        "watchers": int(item.get("watchers_count") or 0),
        "pushed_at": item.get("pushed_at") or "",
        "updated_at": item.get("updated_at") or "",
        "size_kb": int(item.get("size") or 0),
    }


def search_github(query: str, cfg: ScoutConfig, per_page: int = 15) -> list[dict[str, Any]]:
    url = (f"{cfg.github_api_base}/search/repositories?q="
           f"{urllib.parse.quote(query)}&sort=stars&order=desc&per_page={int(per_page)}")
    payload = _request(url, cfg)
    return list(payload.get("items") or [])


def probe_depth(repo_key: str, cfg: ScoutConfig) -> dict[str, Any]:
    """One request for the repository root listing, to tell whether a deep
    dive will find prose. Failure degrades to zero rather than blocking."""
    result = {"has_docs": False, "has_papers": False, "has_spec": False, "readme_bytes": 0}
    try:
        entries = _request(f"{cfg.github_api_base}/repos/{repo_key}/contents", cfg)
    except Exception:
        return result
    if not isinstance(entries, list):
        return result
    for entry in entries:
        name = str(entry.get("name") or "").lower()
        kind = entry.get("type")
        if kind == "dir" and name in {"docs", "doc", "documentation"}:
            result["has_docs"] = True
        elif kind == "dir" and name in {"papers", "paper", "publications", "research"}:
            result["has_papers"] = True
        elif kind == "file" and name.startswith("readme"):
            result["readme_bytes"] = int(entry.get("size") or 0)
        elif kind == "file" and ("spec" in name or name.endswith(".proto")):
            result["has_spec"] = True
    return result


def fetch_repo(repo_key: str, cfg: ScoutConfig) -> dict[str, Any]:
    """GitHub's own record for one repository, or `{}` if it is not reachable.

    The shared entry point for anything that needs repository metadata, so
    token handling and rate-limit behaviour live in one place. `RateLimited`
    propagates deliberately: a caller surveying a hundred repositories needs to
    stop rather than record a hundred empty results.
    """
    try:
        payload = _request(f"{cfg.github_api_base}/repos/{repo_key}", cfg)
    except RateLimited:
        raise
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def resolve_repo_key(repo_key: str, cfg: ScoutConfig) -> dict[str, Any] | None:
    """The repository's current path, when it differs from the one we asked for.

    Returns None when nothing moved, so a caller can skip the bookkeeping
    entirely. The old key is returned as well, because it belongs in `aliases`
    rather than being discarded - somebody's bookmark, and every inbound link
    ever written, still uses it.
    """
    try:
        payload = _request(f"{cfg.github_api_base}/repos/{repo_key}", cfg)
    except RateLimited:
        raise
    except Exception:
        return None
    current = str(payload.get("full_name") or "").strip()
    if not current or current.lower() == (repo_key or "").strip().lower():
        return None
    return {
        "repo_key": current,
        "canonical_url": f"https://github.com/{current}",
        "moved_from": repo_key,
        "moved_detected_at": db.now_iso(),
    }


def discover_domain(conn, domain: Domain, cfg: ScoutConfig,
                    per_query: int | None = None) -> dict[str, int]:
    """Run one domain's seed queries and file the results."""
    added = seen = 0
    limit = per_query or cfg.discovery_per_query
    for query in domain.seed_queries:
        try:
            items = search_github(query, cfg, limit)
        except RateLimited:
            raise
        except Exception as exc:
            _log({"stage": "discovery", "domain": domain.key,
                  "query": query, "error": str(exc)})
            continue
        for item in items:
            url = item.get("html_url") or ""
            if not url:
                continue
            row_id, created = db.add_candidate(
                conn, url=url, title=item.get("full_name") or "",
                description=item.get("description") or "",
                repo_key=item.get("full_name"), discovery_query=query,
                discovery_backend="github_search", domain_key=domain.key)
            if created:
                db.update(conn, row_id, github_json=json.dumps(github_payload(item)))
                added += 1
            else:
                seen += 1
        time.sleep(2)  # search API is 30/min authenticated, 10/min anonymous
    return {"added": added, "corroborated": seen}


def container_notes(vault_root: Path | None = None) -> list[tuple[str, str]]:
    """Catalogued aggregators awaiting expansion: (note name, repo_key)."""
    root = vault_root or _vault_root()
    out: list[tuple[str, str]] = []
    for folder in ("01-Resources", "04-Reviews"):
        directory = root / folder
        if not directory.exists():
            continue
        for path in directory.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            head = text.split("\n---\n", 1)[0]
            if "container: true" not in head:
                continue
            if re.search(r'^expansion_status:\s*"complete"', head, re.M):
                continue
            key = re.search(r'^repo_key:\s*"([^"]+)"', head, re.M)
            out.append((path.stem, key.group(1) if key else ""))
    return out


def expand_container(conn, note_name: str, repo_key: str, cfg: ScoutConfig,
                     readme_text: str) -> dict[str, int]:
    """Parse an aggregator's README into candidates.

    Each row's own annotation becomes the candidate description - the curator
    already wrote it, and it is better evidence than anything a model would
    invent from the link alone.
    """
    added = seen = 0
    for label, url in MD_LINK.findall(readme_text):
        key = repo_key_from_url(url)
        if not key or key == repo_key:
            continue
        row_id, created = db.add_candidate(
            conn, url=f"https://github.com/{key}", title=key,
            description=label.strip(), repo_key=key,
            discovery_query=f"container:{note_name}",
            discovery_backend="container_expansion", domain_key="")
        if created:
            added += 1
        else:
            seen += 1
    return {"added": added, "corroborated": seen}


def fetch_readme(repo_key: str, cfg: ScoutConfig) -> str:
    try:
        payload = _request(f"{cfg.github_api_base}/repos/{repo_key}/readme", cfg)
    except Exception:
        return ""
    import base64
    content = payload.get("content") or ""
    if payload.get("encoding") == "base64":
        try:
            return base64.b64decode(content).decode("utf-8", errors="replace")
        except Exception:
            return ""
    return content


def fetch_license_text(repo_key: str, cfg: ScoutConfig) -> str:
    """The repository's LICENSE file, decoded. Empty string when there is none.

    Separate from the repo metadata because it costs an extra request and is
    only worth spending when the API's `spdx_id` came back unresolved.
    """
    try:
        payload = _request(f"{cfg.github_api_base}/repos/{repo_key}/license", cfg)
    except RateLimited:
        raise
    except Exception:
        return ""
    import base64
    content = payload.get("content") or ""
    if payload.get("encoding") == "base64":
        try:
            return base64.b64decode(content).decode("utf-8", errors="replace")
        except Exception:
            return ""
    return content


def resolve_license(repo_key: str, spdx: str | None,
                    cfg: ScoutConfig) -> dict[str, Any] | None:
    """Read the LICENSE when the API would not say. Returns None when the API
    already gave a usable answer, so callers can skip the request entirely.

    The GitHub API reports NOASSERTION for every composite LICENSE and for
    every source-available licence, which means "unresolved" and "unlicensed"
    arrive looking identical. They are not: one needs a request, the other is
    a finding.
    """
    from .rank import license_from_text, spdx_is_unresolved
    if not spdx_is_unresolved(spdx):
        return None
    text = fetch_license_text(repo_key, cfg)
    # A repository with no LICENSE file may still state its licence in the
    # readme, and one that does should not be recorded as Unknown. The reading
    # is marked for review either way, because prose is weaker than a file.
    readme = fetch_readme(repo_key, cfg) if not text else ""
    reading = license_from_text(text, readme)
    return {
        "license_spdx": reading.spdx,
        "license_class": reading.license_class,
        "license_composite": reading.composite,
        "license_review_required": reading.review_required,
        "license_evidence": reading.evidence,
        "license_source": ("LICENSE file" if text else
                           "readme" if readme else "no licence text"),
    }


def _log(entry: dict[str, Any]) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    entry.setdefault("created_at", db.now_iso())
    with (LOG_DIR / "scout_discovery.log").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
