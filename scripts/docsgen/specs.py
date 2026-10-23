"""Load Wildberries OpenAPI specs into a flat list of operations."""
from __future__ import annotations

import glob
import os
from dataclasses import dataclass, field
from typing import List, Optional

import yaml

VERBS = {"get", "post", "put", "delete", "patch", "head", "options"}


@dataclass
class Param:
    name: str
    location: str
    required: bool
    type: str
    description: str


@dataclass
class Operation:
    module: str
    verb: str           # upper-case, e.g. "GET"
    path: str
    summary: str
    description: str
    params: List[Param] = field(default_factory=list)
    request_model: Optional[str] = None
    response_model: Optional[str] = None
    # WB hosts the areas of its API on separate domains and declares them per
    # path item: production first, sandbox (where it exists) second.
    servers: List[str] = field(default_factory=list)


def module_from_filename(filename: str) -> str:
    """``specs/13-finances.yaml`` -> ``finances`` (matches clients/<lang>/<module>)."""
    base = os.path.basename(filename)
    if base.endswith(".yaml"):
        base = base[:-5]
    base = base.split("-", 1)[1] if "-" in base else base
    return base.replace("-", "_")


def _ref_name(schema) -> Optional[str]:
    if not isinstance(schema, dict):
        return None
    if "$ref" in schema:
        return schema["$ref"].split("/")[-1]
    if schema.get("type") == "array":
        inner = _ref_name(schema.get("items") or {})
        return f"{inner}[]" if inner else "array"
    return schema.get("type")


def _server_urls(servers) -> List[str]:
    if not isinstance(servers, list):
        return []
    return [s["url"] for s in servers
            if isinstance(s, dict) and isinstance(s.get("url"), str) and s["url"]]


def _resolve_ref(doc: dict, node) -> dict:
    """Follow a local ``$ref`` chain inside the same document.

    WB declares shared parameters once under ``components/parameters`` and
    references them from the operations. Unresolved, they arrive nameless and
    render as empty rows in the parameter table.
    """
    for _ in range(10):
        if not isinstance(node, dict) or "$ref" not in node:
            break
        ref = node["$ref"]
        if not isinstance(ref, str) or not ref.startswith("#/"):
            return {}
        target = doc
        for part in ref[2:].split("/"):
            part = part.replace("~1", "/").replace("~0", "~")
            if not isinstance(target, dict) or part not in target:
                return {}
            target = target[part]
        node = target
    return node if isinstance(node, dict) else {}


def _json_schema(container) -> Optional[dict]:
    if not isinstance(container, dict):
        return None
    return (container.get("content", {}) or {}).get("application/json", {}).get("schema")


def load_operations(specs_dir: str = "specs") -> List[Operation]:
    ops: List[Operation] = []
    for filename in sorted(glob.glob(os.path.join(specs_dir, "*.yaml"))):
        with open(filename, "r", encoding="utf-8") as fh:
            doc = yaml.safe_load(fh) or {}
        module = module_from_filename(filename)
        root_servers = _server_urls(doc.get("servers"))
        for path, item in (doc.get("paths") or {}).items():
            if not isinstance(item, dict):
                continue
            path_servers = _server_urls(item.get("servers")) or root_servers
            for verb, op in item.items():
                if verb not in VERBS or not isinstance(op, dict):
                    continue
                params = []
                for raw in (op.get("parameters") or []):
                    p = _resolve_ref(doc, raw)
                    if not p.get("name"):
                        continue
                    params.append(Param(
                        name=p.get("name", ""),
                        location=p.get("in", ""),
                        required=bool(p.get("required")),
                        type=(p.get("schema") or {}).get("type", ""),
                        description=(p.get("description") or "").strip(),
                    ))
                request_model = _ref_name(_json_schema(op.get("requestBody") or {}))
                response_model = None
                for code in ("200", "201"):
                    resp = (op.get("responses") or {}).get(code) or {}
                    schema = _json_schema(resp)
                    if schema:
                        response_model = _ref_name(schema)
                        break
                ops.append(Operation(
                    module=module,
                    verb=verb.upper(),
                    path=path,
                    summary=(op.get("summary") or "").strip(),
                    description=(op.get("description") or "").strip(),
                    params=params,
                    request_model=request_model,
                    response_model=response_model,
                    servers=_server_urls(op.get("servers")) or path_servers,
                ))
    return ops
