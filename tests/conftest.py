"""Shared fixtures for profile-card generation tests."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def sample_repo():
    return {
        "name": "example-repo",
        "html_url": "https://github.com/YoraiLevi/example-repo",
        "description": "Reliable state detection & driving of agents <v2>",
        "language": "Python",
        "archived": False,
        "stargazers_count": 3,
        "forks_count": 1,
    }


@pytest.fixture
def language_colors(monkeypatch):
    """Avoid depending on live network fetch inside svg import side effects."""
    import svg

    colors = {"Python": "#3572A5", "Markdown": "#083fa1"}
    monkeypatch.setattr(svg, "github_languageColors_json", colors)
    return colors
