"""Invariants for SVG card generation — well-formed XML and escaped text."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

import svg


def test_description_ampersand_is_xml_escaped(sample_repo, language_colors):
    out = svg.populate_svg_template(sample_repo, dark_mode=True)
    assert "&amp;" in out
    # Bare ampersand before "driving" must not remain
    assert "detection & driving" not in out
    assert "detection &amp; driving" in out
    ET.fromstring(out)


def test_description_angle_brackets_are_xml_escaped(sample_repo, language_colors):
    out = svg.populate_svg_template(sample_repo, dark_mode=True)
    assert "&lt;v2&gt;" in out
    assert "<v2>" not in out
    ET.fromstring(out)


def test_light_and_dark_cards_are_well_formed(sample_repo, language_colors):
    dark = svg.populate_svg_template(sample_repo, dark_mode=True)
    light = svg.populate_svg_template(sample_repo, dark_mode=False)
    ET.fromstring(dark)
    ET.fromstring(light)


def test_empty_description_is_well_formed(language_colors):
    repo = {
        "name": "no-desc",
        "description": None,
        "language": "Python",
        "archived": False,
        "stargazers_count": 0,
        "forks_count": 0,
    }
    out = svg.populate_svg_template(repo, dark_mode=True)
    ET.fromstring(out)


def test_checked_in_assets_are_well_formed_xml():
    assets = Path("assets")
    svgs = sorted(assets.glob("*.svg"))
    assert svgs, "expected generated card SVGs under assets/"
    for path in svgs:
        ET.parse(path)
