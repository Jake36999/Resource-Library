"""The domain register is authoritative Markdown, so parsing it must be exact
and must not silently drop a domain the user has added."""
from __future__ import annotations

import pytest

from scout.domains import parse
from scout.discovery import repo_key_from_url

SAMPLE = """
# Scouting Domains

## Proposed Domains

### Tier 1 - Enter Rotation Now

**ML Training & MLOps** (`ml_training_mlops`)
Training frameworks and experiment tracking.
Seed queries: `open source experiment tracking mlops`, `fine-tuning framework LLM`

**Signal, Audio & Speech** (`signal_audio_speech`)
DSP and speech.
Seed queries: `open source speech recognition offline`

### Tier 2 - Reserve

**Robotics & Embedded** (`robotics_embedded`)
ROS and firmware.
Seed queries: `ROS2 package`, `motion planning library`
"""


def test_parses_every_domain():
    domains = parse(SAMPLE)
    assert [d.key for d in domains] == [
        "ml_training_mlops", "signal_audio_speech", "robotics_embedded"]


def test_assigns_tiers_from_section_headings():
    tiers = {d.key: d.tier for d in parse(SAMPLE)}
    assert tiers["ml_training_mlops"] == 1
    assert tiers["signal_audio_speech"] == 1
    assert tiers["robotics_embedded"] == 2


def test_extracts_seed_queries():
    domains = {d.key: d for d in parse(SAMPLE)}
    assert domains["ml_training_mlops"].seed_queries == (
        "open source experiment tracking mlops", "fine-tuning framework LLM")
    assert len(domains["signal_audio_speech"].seed_queries) == 1


def test_description_excludes_the_seed_line():
    domains = {d.key: d for d in parse(SAMPLE)}
    assert "Seed queries" not in domains["robotics_embedded"].description
    assert "ROS and firmware" in domains["robotics_embedded"].description


def test_empty_register_yields_no_domains():
    assert parse("# Nothing here\n") == []


# ------------------------------------------------------------- url parsing

@pytest.mark.parametrize("url,expected", [
    ("https://github.com/owner/repo", "owner/repo"),
    ("https://github.com/owner/repo.git", "owner/repo"),
    ("http://www.github.com/Owner/Repo-Name", "Owner/Repo-Name"),
    ("https://github.com/owner/repo/tree/main/docs", "owner/repo"),
])
def test_repo_key_extraction(url, expected):
    assert repo_key_from_url(url) == expected


@pytest.mark.parametrize("url", [
    "https://example.com/owner/repo",
    "https://github.com/topics/python",
    "https://github.com/sponsors/someone",
    "",
])
def test_non_repository_urls_are_rejected(url):
    assert repo_key_from_url(url) is None
