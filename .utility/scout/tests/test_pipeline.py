"""End-to-end wiring check.

Runs discovery through publish with the network and the model replaced by
fakes, so the pipeline's control flow is verified without needing LM Studio
running or a GitHub token present.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest

from scout import db, deep_dive, evaluate, scout_pass
from scout.config import ScoutConfig
from scout.domains import Domain

NOW = datetime(2026, 9, 1, tzinfo=timezone.utc)

DOMAINS = [
    Domain("testing_verification", "Testing & Verification", 1, "Property testing.",
           ("property based testing library",)),
    Domain("crypto_identity", "Crypto & Identity", 1, "Cryptography.",
           ("cryptography library audited",)),
]


class FakeLM:
    """Stands in for LM Studio. Records what it was asked."""

    def __init__(self, payloads):
        self.payloads = list(payloads)
        self.calls = []

    def chat(self, stage, messages, **kwargs):
        self.calls.append((stage, kwargs.get("json_schema") is not None))
        if not self.payloads:
            raise RuntimeError("no more fake responses")
        return json.dumps(self.payloads.pop(0))


@pytest.fixture()
def conn(tmp_path):
    path = tmp_path / "q.sqlite"
    db.init(path)
    with db.connect(path) as connection:
        yield connection


@pytest.fixture()
def cfg():
    return ScoutConfig(cohort_size=2, max_attempts=2, escalation_provider="none")


def seed(conn, url, stars=1000, spdx="MIT", pushed="2026-08-20T00:00:00Z"):
    row_id, _ = db.add_candidate(conn, url=url, title=url.split("github.com/")[-1],
                                 repo_key=url.split("github.com/")[-1],
                                 discovery_query="q", discovery_backend="github_search",
                                 domain_key="testing_verification")
    db.update(conn, row_id, github_json=json.dumps({
        "stars": stars, "license_spdx": spdx, "pushed_at": pushed,
        "archived": False, "readme_bytes": 5000, "has_docs": True,
        "description": "a thing", "topics": ["testing"], "language": "Python"}))
    return row_id


def test_scout_pass_labels_and_advances(conn, cfg, monkeypatch):
    seed(conn, "https://github.com/a/one")
    seed(conn, "https://github.com/a/two")
    fake = FakeLM([
        {"archetype": "library", "domain_key": "testing_verification",
         "tags": ["Testing", " Fuzzing "], "one_line": "A testing library.",
         "sensitivity": "normal", "confidence": 0.8},
        {"archetype": "tool", "domain_key": "crypto_identity",
         "tags": ["crypto"], "one_line": "A crypto tool.",
         "sensitivity": "review_required", "confidence": 0.6},
    ])
    monkeypatch.setattr(scout_pass, "client_for", lambda model="": fake)

    result = scout_pass.run_batch(conn, cfg, DOMAINS)
    assert result["scouted"] == 1
    assert result["deferred"] == 1, "dual-use material is diverted, never ranked"
    assert all(schema for _, schema in fake.calls), "scout must use constrained JSON"

    rows = {r["repo_key"]: r for r in conn.execute("SELECT * FROM scout_queue")}
    assert json.loads(rows["a/one"]["tags"]) == ["testing", "fuzzing"]


def test_scout_rejects_invented_domain_keys(conn, cfg, monkeypatch):
    seed(conn, "https://github.com/a/one")
    fake = FakeLM([{"archetype": "library", "domain_key": "a_domain_i_made_up",
                    "tags": ["x"], "one_line": "Thing.", "sensitivity": "normal",
                    "confidence": 0.9}])
    monkeypatch.setattr(scout_pass, "client_for", lambda model="": fake)
    scout_pass.run_batch(conn, cfg, DOMAINS)
    row = conn.execute("SELECT domain_key FROM scout_queue").fetchone()
    assert row["domain_key"] == "unmatched", "the scout cannot expand the taxonomy"


def test_scout_failure_retries_then_rejects(conn, cfg, monkeypatch):
    seed(conn, "https://github.com/a/one")

    class Broken:
        def chat(self, *a, **k):
            raise RuntimeError("model exploded")

    monkeypatch.setattr(scout_pass, "client_for", lambda model="": Broken())
    scout_pass.run_batch(conn, cfg, DOMAINS)
    assert conn.execute("SELECT state FROM scout_queue").fetchone()["state"] == "discovered"
    scout_pass.run_batch(conn, cfg, DOMAINS)
    assert conn.execute("SELECT state FROM scout_queue").fetchone()["state"] == "rejected"


def test_full_cycle_to_cohort_and_dive(conn, cfg, monkeypatch, tmp_path):
    vault = tmp_path / "vault"
    (vault / "00-Indexes").mkdir(parents=True)
    (vault / "01-Resources").mkdir()
    (vault / "00-Indexes" / "Topic - Testing.md").write_text(
        '---\ntopic_key: "testing_verification"\nresource_count: 0\n---\n', encoding="utf-8")

    good = seed(conn, "https://github.com/a/good", stars=5000)
    weak = seed(conn, "https://github.com/a/weak", stars=2, spdx="NOASSERTION",
                pushed="2019-01-01T00:00:00Z")
    for row_id in (good, weak):
        db.update(conn, row_id, state="scouted", archetype="library",
                  one_line="x", scout_confidence=0.9, tags="[]")

    ranked = evaluate.run(conn, cfg, vault_root=vault, now=NOW)
    assert ranked["ranked"] == 2

    frozen = evaluate.freeze(conn, cfg, vault_root=vault)
    assert frozen["frozen"] is True and frozen["size"] == 2
    note = vault / "07-Scouting" / f"Scout Cohort {frozen['cohort_id']}.md"
    assert note.exists(), "the cohort must be visible before expensive work starts"
    body = note.read_text(encoding="utf-8")
    assert body.index("a/good") < body.index("a/weak"), "note lists best first"

    fake = FakeLM([
        {"bottom_line": "Good thing.", "solves": ["s"], "mechanics": ["m"],
         "use_cases": ["u"], "confidence": 0.9},
        {"bottom_line": "Weak thing.", "solves": ["s"], "mechanics": ["m"],
         "use_cases": ["u"], "confidence": 0.4},
    ])
    monkeypatch.setattr(deep_dive, "client_for", lambda model="": fake)
    monkeypatch.setattr("scout.discovery.fetch_readme", lambda key, cfg: "readme text")
    monkeypatch.setattr(deep_dive, "DOSSIER_DIR", tmp_path / "dossiers")

    result = deep_dive.run(conn, cfg, vault_root=vault)
    assert result["catalogued"] == 2 and result["failed"] == 0

    rows = list(conn.execute("SELECT repo_key, dossier_path FROM scout_queue "
                             "WHERE state='catalogued'"))
    assert len(rows) == 2 and all(r["dossier_path"] for r in rows)


def test_deep_dive_consumes_in_descending_rank(conn, cfg, monkeypatch, tmp_path):
    order = []
    for name, score in (("low", 10.0), ("top", 99.0), ("mid", 55.0)):
        row_id, _ = db.add_candidate(conn, url=f"https://github.com/x/{name}",
                                     repo_key=f"x/{name}")
        db.update(conn, row_id, state="queued", score=score, cohort_id="C1",
                  github_json="{}")

    class Recorder:
        def chat(self, stage, messages, **kwargs):
            payload = json.loads(messages[1]["content"].split("\n", 1)[1])
            order.append(payload["repo_key"])
            return json.dumps({"bottom_line": "b", "solves": ["s"],
                               "mechanics": ["m"], "use_cases": ["u"],
                               "confidence": 0.9})

    monkeypatch.setattr(deep_dive, "client_for", lambda model="": Recorder())
    monkeypatch.setattr("scout.discovery.fetch_readme", lambda key, cfg: "")
    monkeypatch.setattr(deep_dive, "DOSSIER_DIR", tmp_path / "dossiers")

    deep_dive.run(conn, cfg)
    assert order == ["x/top", "x/mid", "x/low"], \
        "highest value must be finished first so interruption is survivable"


def test_publish_feeds_the_existing_build_inputs(conn, cfg, monkeypatch, tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "repositories to chart.md").write_text("- [ ] https://github.com/old/one.git\n",
                                                    encoding="utf-8")
    staging = tmp_path / "staging"
    dossiers = tmp_path / "dossiers"
    dossiers.mkdir()
    monkeypatch.setattr(deep_dive, "STAGING_DIR", staging)

    row_id, _ = db.add_candidate(conn, url="https://github.com/new/two",
                                 repo_key="new/two")
    path = dossiers / "new__two.json"
    path.write_text(json.dumps({
        "repo_key": "new/two", "url": "https://github.com/new/two",
        "github": {"stars": 42, "license_spdx": "MIT", "full_name": "new/two"},
        "review": {}}), encoding="utf-8")
    db.update(conn, row_id, state="catalogued", dossier_path=str(path))

    result = deep_dive.publish(conn, cfg, vault_root=vault)
    assert result == {"published": 1, "seeded": 1}

    cache = json.loads((staging / "github_repo_metadata.json").read_text(encoding="utf-8"))
    assert cache["new/two"]["stars"] == 42, "metadata lands in the cache the build reads"
    seed_text = (vault / "repositories to chart.md").read_text(encoding="utf-8")
    assert "new/two" in seed_text and "old/one" in seed_text


def test_a_renamed_repository_is_detected_and_the_old_key_kept():
    """Two of the seventeen sources in the 2026-09 cohort had been renamed, and
    in both cases the repository's own README still pointed at the old path.
    `db.url_hash()` keys on the URL string, so a rename produces a duplicate
    candidate at one path and a dying canonical URL at the other.

    The old key is kept rather than discarded: it belongs in `aliases`, because
    every inbound link ever written still uses it.
    """
    from scout import discovery
    from scout.config import ScoutConfig

    original = discovery._request
    discovery._request = lambda url, cfg: {"full_name": "HCAI-Lab-GT/capabilibara"}
    try:
        moved = discovery.resolve_repo_key("eilab-gt/capabilibara", ScoutConfig())
        assert moved["repo_key"] == "HCAI-Lab-GT/capabilibara"
        assert moved["canonical_url"].endswith("HCAI-Lab-GT/capabilibara")
        assert moved["moved_from"] == "eilab-gt/capabilibara"

        assert discovery.resolve_repo_key("HCAI-Lab-GT/capabilibara",
                                          ScoutConfig()) is None,             "a repository that has not moved must cost no bookkeeping"
        assert discovery.resolve_repo_key("hcai-lab-gt/CAPABILIBARA",
                                          ScoutConfig()) is None,             "GitHub paths are case-insensitive; a case difference is not a move"
    finally:
        discovery._request = original
