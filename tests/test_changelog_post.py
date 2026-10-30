from pathlib import Path

from changelog_post import MAX_MESSAGE, compose, fallback_body, new_entries, valid_body
from docsgen.changelog import github_slug, parse_entries

ROOT = Path(__file__).resolve().parent.parent

BEFORE = """# Changelog

## Unreleased
### Changed (2026.10.21)
- Товары (Items): уточнена семантика `settings.sort`
"""

AFTER = """# Changelog

## Unreleased
### Changed (2026.10.22)
- Общее: удалены sandbox-серверы для **Статистики**
- Отчёты: лимит 1 запрос/мин & burst 10 для `GET /api/v1/x<y>`

### Changed (2026.10.21)
- Товары (Items): уточнена семантика `settings.sort`
"""


def test_only_entries_added_by_the_push_are_new():
    fresh = new_entries(BEFORE, AFTER)
    assert [e.heading for e in fresh] == ["Changed (2026.10.22)"]
    assert len(fresh[0].bullets) == 2


def test_nothing_new_means_no_post():
    assert new_entries(AFTER, AFTER) == []


def test_anchor_matches_github_heading_ids():
    assert github_slug("Changed (2026.10.22)") == "changed-20261022"
    twice = "### Changed (2026.10.22)\n- a\n### Changed (2026.10.22)\n- b\n"
    assert [e.anchor for e in parse_entries(twice)] == [
        "changed-20261022", "changed-20261022-1"]


def test_every_real_changelog_entry_parses():
    entries = parse_entries((ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))
    assert entries, "no dated entries found in CHANGELOG.md"
    assert all(e.bullets and e.anchor.startswith("changed-") for e in entries)


def test_fallback_escapes_and_keeps_markup_telegram_accepts():
    body = fallback_body(new_entries(BEFORE, AFTER)[0])
    assert "&amp; burst" in body
    assert "<code>GET /api/v1/x&lt;y&gt;</code>" in body
    assert "<b>Статистики</b>" in body
    assert valid_body(body)


def test_fallback_of_every_real_entry_fits_a_message():
    for entry in parse_entries((ROOT / "CHANGELOG.md").read_text(encoding="utf-8")):
        text = compose(entry, fallback_body(entry), ["wb"])
        assert len(text) <= MAX_MESSAGE, entry.heading


def test_model_markup_outside_telegram_html_is_rejected():
    assert valid_body("🧪 <b>Ок</b>\n<blockquote expandable>• <code>/x</code></blockquote>")
    assert not valid_body("<h2>Заголовок</h2>")
    assert not valid_body('<a href="https://example.com">ссылка</a>')
    assert not valid_body("<b>незакрытый")
    assert not valid_body("лимит 1 & 2")
    assert not valid_body("")


def test_post_links_to_the_entry_anchor():
    entry = new_entries(BEFORE, AFTER)[0]
    text = compose(entry, "тело", ["лимиты"])
    assert text.startswith("📡 <b>WB API · 22 октября 2026</b>")
    assert "CHANGELOG.md#changed-20261022" in text
    assert text.endswith("#лимиты")
