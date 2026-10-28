import json
from pathlib import Path
from xml.etree import ElementTree

from docsgen.changelog import FEED_LIMIT, parse_entries, render_atom, to_data

ROOT = Path(__file__).resolve().parents[2]
ATOM = "{http://www.w3.org/2005/Atom}"
SITE = "https://eslazarev.github.io/wildberries-sdk/"

SAMPLE = """# Changelog

## Unreleased
### Changed (2026.10.21)
- Товары (Items): уточнена семантика `settings.sort`

### Changed (2026.10.22)
- Отчёты: лимит 1 запрос/мин & burst 10 для `GET /api/v1/x<y>`
- изменение без раздела
"""


def _real():
    return parse_entries((ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))


def test_committed_data_matches_the_changelog():
    committed = json.loads((ROOT / "data" / "changelog.json").read_text(encoding="utf-8"))
    assert committed == to_data(_real()), \
        "data/changelog.json is stale: run python scripts/generate-changelog-data.py"


def test_data_is_newest_first_and_split_into_sections():
    data = to_data(parse_entries(SAMPLE))
    assert [e["date"] for e in data["entries"]] == ["2026-10-22", "2026-10-21"]
    newest = data["entries"][0]
    assert newest["url"].endswith("CHANGELOG.md#changed-20261022")
    assert newest["changes"][0] == {
        "section": "Отчёты", "text": "лимит 1 запрос/мин & burst 10 для `GET /api/v1/x<y>`"}
    assert newest["changes"][1]["section"] == "Прочее"
    assert newest["sections"] == ["Отчёты", "Прочее"]


def test_feed_is_valid_atom_with_escaped_content():
    feed = ElementTree.fromstring(render_atom(to_data(parse_entries(SAMPLE)), SITE))
    entries = feed.findall(f"{ATOM}entry")
    assert len(entries) == 2
    first = entries[0]
    assert first.find(f"{ATOM}title").text == "WB API · 22 октября 2026: Отчёты, Прочее"
    assert first.find(f"{ATOM}link").get("href").endswith("#changed-20261022")
    content = first.find(f"{ATOM}content").text
    assert "<code>GET /api/v1/x&lt;y&gt;</code>" in content
    assert "&amp; burst" in content
    assert feed.find(f"{ATOM}updated").text == "2026-10-22T00:00:00Z"


def test_feed_of_the_real_changelog_is_capped_and_unique():
    feed = ElementTree.fromstring(render_atom(to_data(_real()), SITE))
    ids = [e.find(f"{ATOM}id").text for e in feed.findall(f"{ATOM}entry")]
    assert 0 < len(ids) <= FEED_LIMIT
    assert len(ids) == len(set(ids))
    assert feed.find(f"{ATOM}link[@rel='self']").get("href") == SITE + "changelog.xml"
