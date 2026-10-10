"""Build the literate-nav SUMMARY.md tree."""
from __future__ import annotations

from typing import Dict, List

from .render import operation_slug
from .specs import Operation


def build_summary(by_module: Dict[str, List[Operation]]) -> str:
    lines = [
        "* [Wildberries SDK](index.md)",
        "* [Начало работы](getting-started.md)",
        "* [Частота релизов](releases.md)",
        "* Справочник API",
    ]
    for module in by_module:
        lines.append(f"    * [{module}](reference/{module}/index.md)")
        for op in by_module[module]:
            title = op.summary or f"{op.verb} {op.path}"
            slug = operation_slug(op)
            lines.append(f"        * [{title}](reference/{module}/{slug}.md)")
    return "\n".join(lines) + "\n"
