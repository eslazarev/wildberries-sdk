#!/usr/bin/env python3
"""Generate the MkDocs reference site from specs + generated clients.

Writes Markdown into website/docs/reference/<module>/ and website/docs/SUMMARY.md.
Run from the repo root:  python scripts/build-docs-site.py
"""
from __future__ import annotations

import os
import shutil
import sys
from collections import OrderedDict

from docsgen.extract import class_maps, python_anchor
from docsgen.naming import to_camel, to_pascal
from docsgen.nav import build_summary
from docsgen.release_render import render_page as render_release_page
from docsgen.releases import load_stats
from docsgen.render import operation_slug, render_module_index, render_operation
from docsgen.specs import load_operations

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPECS_DIR = os.path.join(ROOT, "specs")
CLIENTS_DIR = os.path.join(ROOT, "clients")
DOCS_DIR = os.path.join(ROOT, "website", "docs")
REFERENCE_DIR = os.path.join(DOCS_DIR, "reference")
RELEASES_DATA = os.path.join(ROOT, "data", "releases.json")


def resolve_names(snake, cmaps):
    """Map snake anchor name -> per-language (method_name, class_token) pairs.

    Returns a dict keyed by language id, values are ``(method, class_token)``
    tuples for non-Python languages and just the snake name for Python.
    When snake is None (operation absent from Python client) all langs are None.
    When a language doesn't have the method it maps to None.
    """
    resolved = {"python": snake, "rust": None, "npm": None, "php": None, "go": None}
    if snake is None:
        return resolved
    pascal = to_pascal(snake)
    camel = to_camel(snake)
    candidates = {"rust": snake, "npm": camel, "php": camel, "go": pascal}
    for lang in ("rust", "npm", "php", "go"):
        # Match case-insensitively and emit the client's REAL method name, so
        # acronym casing (e.g. ``ID``/``IDs`` vs ``Id``/``Ids``) never produces a
        # false "unavailable".
        entry = cmaps[lang].get(candidates[lang].lower())
        resolved[lang] = entry  # (real_name, class_token) or None
    return resolved


def main():
    ops = load_operations(SPECS_DIR)

    by_module = OrderedDict()
    for op in ops:
        by_module.setdefault(op.module, []).append(op)

    if os.path.isdir(REFERENCE_DIR):
        shutil.rmtree(REFERENCE_DIR)
    os.makedirs(REFERENCE_DIR, exist_ok=True)

    no_example = 0
    for module, module_ops in list(by_module.items()):
        anchor = python_anchor(module, CLIENTS_DIR)
        if not anchor:
            print(f"WARNING: no python client for module {module}; skipping", file=sys.stderr)
            del by_module[module]
            continue
        cmaps = class_maps(module, CLIENTS_DIR)
        module_dir = os.path.join(REFERENCE_DIR, module)
        os.makedirs(module_dir, exist_ok=True)

        for op in module_ops:
            snake = anchor.get((op.verb, op.path))
            if snake is None:
                no_example += 1
            names = resolve_names(snake, cmaps)
            page = render_operation(op, names)
            with open(os.path.join(module_dir, f"{operation_slug(op)}.md"), "w",
                      encoding="utf-8") as fh:
                fh.write(page)

        index = render_module_index(module, module_ops)
        with open(os.path.join(module_dir, "index.md"), "w", encoding="utf-8") as fh:
            fh.write(index)

    stats = load_stats(RELEASES_DATA, ROOT)
    with open(os.path.join(DOCS_DIR, "releases.md"), "w", encoding="utf-8") as fh:
        fh.write(render_release_page(stats))

    with open(os.path.join(DOCS_DIR, "SUMMARY.md"), "w", encoding="utf-8") as fh:
        fh.write(build_summary(by_module))

    total = sum(len(v) for v in by_module.values())
    print(f"Generated {total} operations across {len(by_module)} modules "
          f"({no_example} without any client example).")
    print(f"Release chart: {stats.total} releases in the rolling window.")


if __name__ == "__main__":
    main()
