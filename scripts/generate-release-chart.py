#!/usr/bin/env python3
"""Refresh the release cadence data file and the static README charts.

Reads the repository's ``v*`` tags and writes:

  data/releases.json                              consumed by the docs site build
  .github/images/release-cadence-<lang>-<theme>.svg   embedded in the READMEs

One picture per README language and per colour scheme, so a translated README
shows a chart in its own language.

Run from anywhere:  python scripts/generate-release-chart.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from docsgen.release_render import LOCALES, render_svg  # noqa: E402
from docsgen.releases import build_stats, read_tags  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(ROOT, "data", "releases.json")
IMAGES_DIR = os.path.join(ROOT, ".github", "images")


def main() -> int:
    releases = read_tags(ROOT)
    if not releases:
        print("No v* tags found. Is this a shallow clone without tags?",
              file=sys.stderr)
        return 1

    stats = build_stats(releases)

    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as fh:
        json.dump(stats.to_dict(), fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")

    os.makedirs(IMAGES_DIR, exist_ok=True)
    written = 0
    for lang in LOCALES:
        for theme in ("dark", "light"):
            target = os.path.join(IMAGES_DIR, f"release-cadence-{lang}-{theme}.svg")
            with open(target, "w", encoding="utf-8") as fh:
                fh.write(render_svg(stats, theme=theme, lang=lang))
            written += 1

    print(f"Release chart: {stats.total} releases in the window, "
          f"{stats.window_start} to {stats.window_end}, {written} images.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
