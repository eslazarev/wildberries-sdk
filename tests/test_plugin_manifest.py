"""The plugin manifests duplicate a few fields, so they can drift apart.

``marketplace.json`` advertises the plugin to anyone running
``/plugin install wildberries-sdk --marketplace eslazarev/wildberries-sdk``;
``plugin.json`` is what Claude Code reads once it is installed. If the two
disagree on the name or version, ``claude plugin tag`` refuses to cut a
release — and the skill the marketplace promises has to actually be there.
"""
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_DIR = ROOT / ".claude-plugin"


def _load(name):
    return json.loads((MANIFEST_DIR / name).read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def plugin():
    return _load("plugin.json")


@pytest.fixture(scope="module")
def entry():
    """The marketplace's own listing for this repository's plugin."""
    market = _load("marketplace.json")
    by_name = {p["name"]: p for p in market["plugins"]}
    assert market["name"] in by_name, "the marketplace does not list its own plugin"
    return by_name[market["name"]]


@pytest.mark.parametrize("field", ["name", "version", "license"])
def test_marketplace_entry_agrees_with_the_plugin_manifest(plugin, entry, field):
    assert entry[field] == plugin[field]


def test_plugin_source_points_at_the_repository_root(entry):
    assert entry["source"] == "./"


def test_every_skill_the_plugin_ships_is_discoverable(plugin):
    """Claude Code loads skills from <plugin root>/skills/<name>/SKILL.md."""
    skills = sorted(p.name for p in (ROOT / "skills").iterdir() if p.is_dir())
    assert skills, "the plugin advertises skills but ships none"
    for name in skills:
        skill = ROOT / "skills" / name / "SKILL.md"
        assert skill.is_file(), f"{name} has no SKILL.md"
        # The frontmatter name is the handle the catalogue and /plugin show.
        assert f"\nname: {name}\n" in skill.read_text(encoding="utf-8")[:400]


def test_the_install_line_is_in_every_readme(plugin):
    """A plugin nobody can find installed is a plugin nobody installs."""
    command = f"/plugin install {plugin['name']} --marketplace eslazarev/wildberries-sdk"
    readmes = [ROOT / "README.md"] + sorted((ROOT / "docs" / "i18n").glob("README.*.md"))
    for readme in readmes:
        assert command in readme.read_text(encoding="utf-8"), \
            f"{readme.relative_to(ROOT)} does not say how to install the plugin"
