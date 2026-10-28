"""GitHub shows README images through its camo proxy, and deepwiki.com answers
server-side fetches with a Vercel bot checkpoint instead of the SVG. Camo then
returns 502 and the README shows a broken-image icon. The badge is therefore
kept in the repository and must never be hot-linked again.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BADGE = ROOT / ".github" / "images" / "deepwiki-badge.svg"
READMES = [ROOT / "README.md",
           *sorted((ROOT / "docs" / "i18n").glob("README.*.md")),
           *sorted((ROOT / "docs").glob("*/README.md"))]


def test_no_readme_hotlinks_the_deepwiki_badge():
    offenders = [str(p.relative_to(ROOT)) for p in READMES
                 if "deepwiki.com/badge.svg" in p.read_text(encoding="utf-8")]
    assert not offenders, f"camo cannot fetch deepwiki.com: {offenders}"


def test_the_badge_lives_in_the_repository():
    assert BADGE.is_file(), "save https://deepwiki.com/badge.svg to .github/images/"
    head = BADGE.read_text(encoding="utf-8")[:200]
    # A Vercel checkpoint page saved by mistake is HTML, not an image.
    assert head.lstrip().startswith("<svg"), "deepwiki-badge.svg is not an SVG"


def test_every_readme_links_the_telegram_channel():
    missing = [str(p.relative_to(ROOT)) for p in READMES
               if "https://t.me/wildberries_api_radar" not in p.read_text(encoding="utf-8")]
    assert not missing, f"no Telegram channel link in {missing}"
