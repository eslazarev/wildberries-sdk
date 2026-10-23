#!/usr/bin/env python3
"""Search every Wildberries SDK operation by meaning, route or method name.

Reads the operation digest published with the docs site and prints the matching
blocks: route, required parameters, the method name in all five clients and a
link to the full reference page.

    python find_operation.py "остатки"
    python find_operation.py "/api/v3/orders" --lang go
    python find_operation.py отзыв --limit 5

The digest is cached for a day under ~/.cache/wildberries-sdk/. Standard
library only, so it runs anywhere Python does.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
import urllib.request

DIGEST_URL = "https://eslazarev.github.io/wildberries-sdk/llms-full.txt"
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "wildberries-sdk")
CACHE_FILE = os.path.join(CACHE_DIR, "llms-full.txt")
MAX_AGE_SECONDS = 24 * 60 * 60
LANGS = ("python", "node", "go", "php", "rust")


def _read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def load_digest(source: str | None, refresh: bool) -> str:
    """The published digest, or the best local copy when the site is unreachable."""
    if source:
        return _read(source)

    fresh = (os.path.isfile(CACHE_FILE)
             and time.time() - os.path.getmtime(CACHE_FILE) < MAX_AGE_SECONDS)
    if fresh and not refresh:
        return _read(CACHE_FILE)

    try:
        with urllib.request.urlopen(DIGEST_URL, timeout=30) as response:
            text = response.read().decode("utf-8")
    except Exception:
        # Offline, behind a proxy, or run from a checkout before the site is
        # deployed: a local digest beats refusing to answer.
        for candidate in (os.environ.get("WB_SDK_DIGEST"),
                          os.path.join("website", "docs", "llms-full.txt"),
                          CACHE_FILE):
            if candidate and os.path.isfile(candidate):
                return _read(candidate)
        raise

    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as fh:
        fh.write(text)
    return text


def split_blocks(digest: str):
    """``[(module, block_text), ...]`` — one entry per operation."""
    blocks = []
    module = ""
    current: list[str] = []
    for line in digest.splitlines():
        if line.startswith("## "):
            if current:
                blocks.append((module, "\n".join(current).strip()))
                current = []
            module = line[3:].split(" (")[0].strip()
        elif line.startswith("### "):
            if current:
                blocks.append((module, "\n".join(current).strip()))
            current = [line]
        elif current:
            current.append(line)
    if current:
        blocks.append((module, "\n".join(current).strip()))
    return blocks


def matches(block: str, terms: list[str]) -> bool:
    haystack = block.lower()
    return all(term.lower() in haystack for term in terms)


def render(module: str, block: str, lang: str | None) -> str:
    if not lang:
        return f"[{module}]\n{block}"
    keep = []
    for line in block.splitlines():
        head = line.split(":", 1)[0]
        if head in LANGS and head != lang:
            continue
        keep.append(line)
    return f"[{module}]\n" + "\n".join(keep)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("terms", nargs="+",
                        help="words, a route fragment or a method name; all must match")
    parser.add_argument("--lang", choices=LANGS, help="print only this client's method")
    parser.add_argument("--limit", type=int, default=20, help="max results (default 20)")
    parser.add_argument("--source", help="read a local digest instead of the site")
    parser.add_argument("--refresh", action="store_true", help="ignore the cached copy")
    args = parser.parse_args()

    try:
        digest = load_digest(args.source, args.refresh)
    except Exception as exc:
        print(f"Could not read the operation digest: {exc}\n"
              f"Browse {DIGEST_URL} or the docs site instead.", file=sys.stderr)
        return 2

    hits = [(module, block) for module, block in split_blocks(digest)
            if matches(block, args.terms)]
    if not hits:
        print(f"Nothing matched {' '.join(args.terms)!r}. Try a shorter stem "
              f"(\"постав\" rather than \"создать поставку\") or search by route.",
              file=sys.stderr)
        return 1

    for module, block in hits[:args.limit]:
        print(render(module, block, args.lang))
        print()
    if len(hits) > args.limit:
        print(f"... {len(hits) - args.limit} more matches; narrow the search "
              f"or raise --limit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
