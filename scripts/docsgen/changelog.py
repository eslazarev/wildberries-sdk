"""CHANGELOG.md as data: dated entries, the JSON file and the Atom feed.

CHANGELOG.md stays the source the update-specs pipeline writes. Everything here
is read from it, so the channel posts, data/changelog.json and the feed on the
docs site always tell the same story.
"""
from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from xml.sax.saxutils import escape

REPO_URL = "https://github.com/eslazarev/wildberries-sdk"
CHANGELOG_URL = f"{REPO_URL}/blob/main/CHANGELOG.md"
FEED_FILE = "changelog.xml"
FEED_LIMIT = 50

ENTRY_HEADING = re.compile(r"^### Changed \((\d{4})\.(\d{2})\.(\d{2})\)\s*$")
MONTHS = ("января", "февраля", "марта", "апреля", "мая", "июня", "июля",
          "августа", "сентября", "октября", "ноября", "декабря")
OTHER_SECTION = "Прочее"


@dataclass
class Entry:
    heading: str
    date: tuple[int, int, int]
    bullets: list[str] = field(default_factory=list)
    anchor: str = ""

    @property
    def text(self) -> str:
        return "\n".join(self.bullets)

    @property
    def iso_date(self) -> str:
        return "%04d-%02d-%02d" % self.date

    @property
    def url(self) -> str:
        return f"{CHANGELOG_URL}#{self.anchor}"


def github_slug(heading: str) -> str:
    """The id GitHub gives a Markdown heading, before de-duplication."""
    slug = heading.strip().lower()
    slug = re.sub(r"[^\w\- ]", "", slug)
    return slug.replace(" ", "-")


def parse_entries(markdown: str) -> list[Entry]:
    """Every dated entry in CHANGELOG order, with its GitHub anchor."""
    entries: list[Entry] = []
    seen: dict[str, int] = {}
    current: Entry | None = None
    for line in markdown.splitlines():
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
            slug = github_slug(heading)
            count = seen.get(slug, 0)
            seen[slug] = count + 1
            anchor = slug if count == 0 else f"{slug}-{count}"
            match = ENTRY_HEADING.match(line)
            current = None
            if match:
                y, m, d = (int(g) for g in match.groups())
                current = Entry(heading=heading, date=(y, m, d), anchor=anchor)
                entries.append(current)
            continue
        if current is not None and line.startswith("- "):
            current.bullets.append(line[2:].strip())
    return [e for e in entries if e.bullets]


def split_section(bullet: str) -> tuple[str, str]:
    """``"Продвижение: удалены …"`` -> ``("Продвижение", "удалены …")``."""
    section, sep, rest = bullet.partition(": ")
    if not sep or len(section) > 40:
        return OTHER_SECTION, bullet
    return section, rest


def sections(entry: Entry) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    for bullet in entry.bullets:
        section, text = split_section(bullet)
        grouped.setdefault(section, []).append(text)
    return grouped


def human_date(date: tuple[int, int, int]) -> str:
    return f"{date[2]} {MONTHS[date[1] - 1]}"


def inline_markdown(text: str) -> str:
    """Escape a CHANGELOG bullet and keep its `code` and **bold** as HTML."""
    out = html.escape(text, quote=False)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", out)


def to_data(entries: list[Entry]) -> dict:
    """The data/changelog.json document, newest entry first."""
    ordered = sorted(entries, key=lambda e: e.date, reverse=True)
    return {
        "source": "CHANGELOG.md",
        "entries": [
            {
                "date": e.iso_date,
                "anchor": e.anchor,
                "url": e.url,
                "sections": list(sections(e)),
                "changes": [dict(zip(("section", "text"), split_section(b)))
                            for b in e.bullets],
            }
            for e in ordered
        ],
    }


def render_atom(data: dict, site_url: str, limit: int = FEED_LIMIT) -> str:
    """An Atom feed of the newest entries of a ``to_data`` document."""
    site_url = site_url.rstrip("/") + "/"
    entries = data["entries"][:limit]
    updated = f"{entries[0]['date']}T00:00:00Z" if entries else "1970-01-01T00:00:00Z"
    out = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="ru">',
        "  <title>Изменения API Wildberries</title>",
        "  <subtitle>Что поменялось в OpenAPI-спецификациях Wildberries: "
        "новые методы, лимиты, удаления.</subtitle>",
        f"  <id>{escape(site_url + FEED_FILE)}</id>",
        f'  <link rel="self" type="application/atom+xml" href="{escape(site_url + FEED_FILE)}"/>',
        f'  <link rel="alternate" type="text/html" href="{escape(CHANGELOG_URL)}"/>',
        f"  <updated>{updated}</updated>",
        "  <author><name>wildberries-sdk</name></author>",
    ]
    for entry in entries:
        y, m, d = (int(p) for p in entry["date"].split("-"))
        title = f"WB API · {human_date((y, m, d))} {y}"
        if entry["sections"]:
            title += ": " + ", ".join(entry["sections"])
        grouped: dict[str, list[str]] = {}
        for change in entry["changes"]:
            grouped.setdefault(change["section"], []).append(change["text"])
        body = "".join(
            f"<h3>{html.escape(section)}</h3><ul>"
            + "".join(f"<li>{inline_markdown(t)}</li>" for t in texts)
            + "</ul>"
            for section, texts in grouped.items()
        )
        out += [
            "  <entry>",
            f"    <title>{escape(title)}</title>",
            f"    <id>{escape(entry['url'])}</id>",
            f'    <link rel="alternate" type="text/html" href="{escape(entry["url"])}"/>',
            f"    <updated>{entry['date']}T00:00:00Z</updated>",
            f'    <content type="html">{escape(body)}</content>',
            "  </entry>",
        ]
    out.append("</feed>")
    return "\n".join(out) + "\n"
