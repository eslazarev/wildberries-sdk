"""Render Markdown pages for operations and module indexes."""
from __future__ import annotations

import json
import re
from typing import Dict, List, Optional

from .examples import build_examples
from .specs import Operation

# WB specs cross-reference the developer portal with site-absolute links
# (``/openapi/...``) that we don't host — they 404 on our site. Point them at
# the real portal instead, opening in a new tab so we don't navigate users away.
# Covers HTML ``href="/openapi/..."`` and Markdown ``[text](/openapi/...)`` forms;
# the Markdown form becomes an HTML anchor since Markdown can't carry ``target``.
WB_PORTAL = "https://dev.wildberries.ru"
_NEW_TAB = 'target="_blank" rel="noopener"'


def _rewrite_wb_links(text: str) -> str:
    if not text:
        return text
    text = re.sub(
        r"\[([^\]]+)\]\(/openapi/([^)]+)\)",
        rf'<a href="{WB_PORTAL}/openapi/\2" {_NEW_TAB}>\1</a>',
        text,
    )
    text = re.sub(
        r'href="/openapi/([^"]*)"',
        rf'href="{WB_PORTAL}/openapi/\1" {_NEW_TAB}',
        text,
    )
    return text


def _enable_markdown_in_divs(text: str) -> str:
    """WB descriptions wrap content (incl. Markdown tables) in styling ``<div>``s.
    Python-Markdown skips Markdown inside raw block HTML unless the element opts in
    via ``markdown="1"`` (requires the ``md_in_html`` extension)."""
    if not text:
        return text
    return re.sub(
        r'<div class="(description_[^"]*)">',
        r'<div markdown="1" class="\1">',
        text,
    )


def operation_slug(op: Operation) -> str:
    """Stable filename stem, e.g. ``GET /api/v1/account/balance`` -> ``get_api_v1_account_balance``."""
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", op.path.strip("/"))
    cleaned = re.sub(r"_+", "_", cleaned).strip("_").lower()
    return f"{op.verb.lower()}_{cleaned}"


def _indent(code: str, spaces: int = 4) -> str:
    pad = " " * spaces
    return "\n".join(pad + line if line else "" for line in code.splitlines())


def _params_table(op: Operation) -> str:
    if not op.params:
        return ""
    rows = ["## Параметры", "",
            "| Имя | Расположение | Тип | Обязательный | Описание |",
            "| --- | --- | --- | --- | --- |"]
    for p in op.params:
        req = "да" if p.required else "нет"
        desc = _rewrite_wb_links(p.description).replace("\n", " ").replace("|", "\\|")
        rows.append(f"| {p.name} | {p.location} | {p.type} | {req} | {desc} |")
    return "\n".join(rows) + "\n"


def page_description(op: Operation) -> str:
    """The page's own meta description: search snippets and link previews."""
    endpoint = f"{op.verb} {op.path}"
    lead = f"{op.summary} ({endpoint})" if op.summary else endpoint
    return f"{lead}: пример вызова API Wildberries на Python, Node.js, Go, PHP и Rust."


def render_operation(op: Operation, names: Dict[str, Optional[str]]) -> str:
    title = op.summary or f"{op.verb} {op.path}"
    # A JSON string is a valid YAML double-quoted scalar, so this escapes any
    # quote or colon a summary may hold.
    parts: List[str] = ["---", f"description: {json.dumps(page_description(op), ensure_ascii=False)}",
                        "---", "", f"# {title}", "", f"`{op.verb} {op.path}`", ""]
    if op.description:
        parts += [_enable_markdown_in_divs(_rewrite_wb_links(op.description)), ""]
    table = _params_table(op)
    if table:
        parts += [table]
    if op.request_model:
        parts += [f"**Тело запроса:** `{op.request_model}`", ""]
    if op.response_model:
        parts += [f"**Ответ:** `{op.response_model}`", ""]
    parts += ["## Примеры вызова", ""]
    for label, fence, code in build_examples(op, names):
        parts.append(f'=== "{label}"')
        parts.append("")
        parts.append(f"    ```{fence}")
        parts.append(_indent(code))
        parts.append("    ```")
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def render_module_index(module: str, ops: List[Operation]) -> str:
    parts = [f"# {module}", "",
             f"Операции модуля `{module}` ({len(ops)}).", ""]
    for op in ops:
        title = op.summary or f"{op.verb} {op.path}"
        parts.append(f"- [{title}]({operation_slug(op)}.md) — `{op.verb} {op.path}`")
    return "\n".join(parts) + "\n"
