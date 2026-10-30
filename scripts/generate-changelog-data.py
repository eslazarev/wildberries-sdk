#!/usr/bin/env python3
"""Refresh data/changelog.json from CHANGELOG.md.

One object per dated entry, newest first: date, GitHub anchor and link, and
every change split into its API section and text. The Atom feed on the docs
site is built from CHANGELOG.md directly, the same way.

Run from anywhere:  python scripts/generate-changelog-data.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from docsgen.changelog import parse_entries, to_data  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHANGELOG = os.path.join(ROOT, "CHANGELOG.md")
DATA_FILE = os.path.join(ROOT, "data", "changelog.json")


def main() -> int:
    with open(CHANGELOG, encoding="utf-8") as fh:
        entries = parse_entries(fh.read())
    if not entries:
        print("No dated entries in CHANGELOG.md.", file=sys.stderr)
        return 1

    data = to_data(entries)
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    changes = sum(len(e["changes"]) for e in data["entries"])
    print(f"Changelog data: {len(entries)} entries, {changes} changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
