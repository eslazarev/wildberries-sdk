"""Render the agent-facing files served from the docs site root.

``llms.txt`` is the short index (the repository's own file, copied to the site
so ``<site>/llms.txt`` resolves, which is where the convention puts it).
``llms-full.txt`` is a digest of every operation: route, required parameters,
models and the exact method name in each of the five clients. It deliberately
leaves out the WB prose — that is 300k+ characters and lives on the site, one
page per operation, linked from every block.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from .render import operation_slug
from .specs import Operation

SITE_URL = "https://eslazarev.github.io/wildberries-sdk"
MISSING = "—"

HEADER = """# Wildberries SDK — operation digest

> Every Wildberries API operation this SDK exposes: HTTP route, required
> parameters, request and response models, and the exact method name in each of
> the five generated clients (Python, Node.js, Go, PHP, Rust).

Generated from `specs/*.yaml` and the published clients, refreshed whenever the
specs change. Full reference with runnable examples per language: {site}/
Short index: {site}/llms.txt
`{missing}` means the operation is not available in that client.
"""


def operation_url(op: Operation) -> str:
    return f"{SITE_URL}/reference/{op.module}/{operation_slug(op)}/"


def _required(op: Operation) -> List[str]:
    return [p.name for p in op.params if p.required and p.name]


def _signatures(op: Operation, names: Dict) -> List[Tuple[str, str]]:
    """``[(language label, call), ...]`` in the order the clients are listed."""
    python = names.get("python")
    rows = [("python", f"wildberries_sdk.{op.module}.DefaultApi.{python}"
             if python else MISSING)]
    for label, lang in (("node", "npm"), ("go", "go"), ("php", "php"), ("rust", "rust")):
        entry = names.get(lang)
        rows.append((label, _call(op, lang, entry) if entry else MISSING))
    return rows


def _call(op: Operation, lang: str, entry: Tuple[str, str]) -> str:
    method, token = entry
    if lang == "npm":
        return f"{token}.{method}"
    if lang == "go":
        return f"client.{token}.{method}"
    if lang == "php":
        return f"{token}::{method}"
    return f"wildberries_sdk_{op.module}::apis::{token}::{method}"


def render_llms_full(by_module: Dict[str, List[Tuple[Operation, Dict]]]) -> str:
    out = [HEADER.format(site=SITE_URL, missing=MISSING)]
    for module, entries in by_module.items():
        out.append(f"## {module} ({len(entries)} operations)\n")
        for op, names in entries:
            out.append(_block(op, names))
    return "\n".join(out).rstrip() + "\n"


def _block(op: Operation, names: Dict) -> str:
    title = op.summary or f"{op.verb} {op.path}"
    lines = [f"### {title}", f"route: {op.verb} {op.path}"]
    required = _required(op)
    if required:
        lines.append("required: " + ", ".join(required))
    if op.request_model:
        lines.append(f"body: {op.request_model}")
    if op.response_model:
        lines.append(f"returns: {op.response_model}")
    lines += [f"{label}: {call}" for label, call in _signatures(op, names)]
    lines.append(f"docs: {operation_url(op)}")
    return "\n".join(lines) + "\n"


def render_llms_index(repo_llms_txt: str) -> str:
    """The repository's ``llms.txt`` plus a pointer to the digest beside it."""
    body = repo_llms_txt.rstrip()
    return body + (
        "\n\n## Machine-readable\n\n"
        f"- [llms-full.txt]({SITE_URL}/llms-full.txt): every operation with its "
        "route, parameters and the method name in all five clients\n"
        f"- [sitemap.xml]({SITE_URL}/sitemap.xml): every reference page\n"
    )
