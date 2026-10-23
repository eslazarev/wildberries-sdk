"""Turn a WB description into a one-line summary for a README bullet.

The Rust client carries the whole WB description in a single ``///`` doc
comment — HTML wrappers, limit tables and site-absolute links included. Printed
as-is it gives a README full of ``](/openapi/...)`` links that 404 anywhere
outside the Wildberries portal. This trims that text down to the one sentence a
method list needs, with the surviving links pointing at the real portal.
"""
from __future__ import annotations

import re

WB_PORTAL = "https://dev.wildberries.ru"
LIMIT = 200

_MD_LINK = re.compile(r"\]\(/openapi/")
_HREF = re.compile(r'href="/openapi/')
_TAG = re.compile(r"<[^>]+>")
# WB prefixes many descriptions with a styled box ("available with a Personal
# token", request limits). It renders as a badge on the site and as noise in a
# one-line bullet.
_BADGE = re.compile(r'<div class="description_[^"]*">.*?</div>', re.S)
_SENTENCE_END = re.compile(r"[.!?](?=\s|$)")
# A markdown table starts at the first cell divider; nothing after it belongs
# in a one-line summary.
_TABLE = re.compile(r"\s*\|.*$", re.S)


def clean_summary(text: str, limit: int = LIMIT) -> str:
    if not text:
        return ""
    text = text.replace('\\"', '"')
    text = _MD_LINK.sub(f"]({WB_PORTAL}/openapi/", text)
    text = _HREF.sub(f'href="{WB_PORTAL}/openapi/', text)
    without_badges = _BADGE.sub(" ", text)
    if without_badges.strip(" <>/div"):
        text = without_badges
    text = _TAG.sub(" ", text)
    text = _TABLE.sub("", text)
    text = " ".join(text.split())
    if not text:
        return ""
    return _shorten(text, limit)


def _shorten(text: str, limit: int) -> str:
    first = _SENTENCE_END.search(text)
    if first and first.end() <= limit:
        return text[:first.end()].strip()
    if len(text) <= limit:
        return text
    return _cut(text, limit) + "…"


def _cut(text: str, limit: int) -> str:
    """Cut at a word boundary, never inside a ``[text](url)`` link."""
    cut = text[:limit]
    opened = cut.rfind("[")
    if opened != -1 and cut.count("[", opened) > cut.count(")", opened):
        cut = cut[:opened]
    elif " " in cut:
        cut = cut[:cut.rfind(" ")]
    return cut.rstrip(" ,;:—-")
