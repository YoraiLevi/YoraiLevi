"""Contracts for README card markdown generation."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load_readme_gen():
    path = Path("README.md.py")
    spec = importlib.util.spec_from_file_location("readme_md_py", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def readme_gen(language_colors):
    # language_colors patches svg before/while this module imports svg
    return _load_readme_gen()


def test_repolike_card_uses_argument_html_url(readme_gen, sample_repo, language_colors):
    """Must read html_url from the argument — not a leaked outer `repo` name."""
    sample_repo = {
        **sample_repo,
        "html_url": "https://github.com/YoraiLevi/argument-url-only",
    }
    # Deliberately bind a different `repo` in this frame; buggy code used to
    # pick up the caller's loop variable via LEGB and would fail NameError
    # here (no outer repo) or link the wrong repo if one leaked.
    _dark, _dn, _light, _ln, md = readme_gen.repolike_card(sample_repo, "t0")
    assert 'href="https://github.com/YoraiLevi/argument-url-only"' in md
    assert "example-repo" in _dark  # name still from argument payload


def test_srcset_paths_have_no_trailing_slash(readme_gen, sample_repo, language_colors):
    *_rest, md = readme_gen.repolike_card(sample_repo, "t1")
    assert 'srcset="./assets/card-dark-t1.svg"' in md
    assert 'srcset="./assets/card-light-t1.svg"' in md
    assert 'srcset="./assets/card-dark-t1.svg/"' not in md
    assert 'srcset="./assets/card-light-t1.svg/"' not in md


def test_readme_committed_srcset_has_no_trailing_slash():
    text = Path("README.md").read_text(encoding="utf-8")
    assert 'srcset="./assets/' in text
    assert ".svg/" not in text
