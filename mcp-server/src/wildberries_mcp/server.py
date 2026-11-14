"""MCP server for the Wildberries seller API, built on wildberries-sdk.

Four tools instead of one per operation: a few hundred tool schemas would fill
an agent's context before it did anything, and many clients cap the number of
tools. The agent finds an operation, reads its parameters, then calls it:

    search_operations -> describe_operation -> call_read_operation
                                             -> call_write_operation

Reads and writes are separate tools so that clients can tell them apart by
their annotations: a write is marked destructive, and clients that honour the
annotations ask before running it.

Environment: WB_API_TOKEN (the seller's API token), WB_MCP_MAX_RESPONSE_CHARS.
"""
from __future__ import annotations

import inspect
import json
import os
import re
from contextlib import contextmanager
from typing import Any, Iterator, get_args

import anyio
import urllib3
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import BaseModel, TypeAdapter, ValidationError

from . import __version__
from .catalog import Catalog, Operation, load_method, signature_params

MAX_RESPONSE_CHARS = int(os.environ.get("WB_MCP_MAX_RESPONSE_CHARS", "60000"))
MAX_SCHEMA_CHARS = 40000
REQUEST_TIMEOUT = 120

INSTRUCTIONS = """\
Wildberries seller API (marketplace wildberries.ru) through wildberries-sdk.

Workflow: search_operations finds an operation by words in Russian or English,
a path or a method name; describe_operation lists its parameters and request
body schema; call_read_operation (GET) or call_write_operation (POST, PUT,
PATCH, DELETE) runs it with the seller's token. Some reports and lists are
POST operations and go through call_write_operation too.

Wildberries limits request rates per seller and token category; a 429 response
means wait and retry, its headers say how long. Operation descriptions state the
limits. Reference with examples: https://eslazarev.github.io/wildberries-sdk/
"""

server = MCPServer(
    name="wildberries",
    title="Wildberries API",
    instructions=INSTRUCTIONS,
    website_url="https://eslazarev.github.io/wildberries-sdk/",
    version=__version__,
)

_catalog: Catalog | None = None


@contextmanager
def _agent_errors() -> Iterator[None]:
    """Let the agent read why a call failed: MCP hides other exceptions' text."""
    try:
        yield
    except (ValueError, KeyError) as exc:
        raise ToolError(exc.args[0] if exc.args else repr(exc)) from None
    except urllib3.exceptions.HTTPError as exc:
        raise ToolError(f"Network error reaching Wildberries: {exc}") from None


def catalog() -> Catalog:
    global _catalog
    if _catalog is None:
        _catalog = Catalog.from_sdk()
    return _catalog


def _snake(name: str) -> str:
    return re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", name).lower()


def _unwrap_one_of(annotation: Any) -> Any:
    """The union a generated ``oneOf`` wrapper stands for, else the annotation.

    openapi-generator models ``oneOf`` as a class with an ``actual_instance``
    field; its own JSON Schema lists internal validator fields, not the shapes
    Wildberries accepts.
    """
    for candidate in (annotation, *get_args(annotation)):
        for inner in (candidate, *get_args(candidate)):
            if isinstance(inner, type) and issubclass(inner, BaseModel) \
                    and "actual_instance" in inner.model_fields:
                return inner.model_fields["actual_instance"].annotation
    return annotation


def _schema(annotation: Any) -> dict:
    try:
        return TypeAdapter(_unwrap_one_of(annotation)).json_schema(by_alias=True)
    except Exception:  # an annotation pydantic cannot express as JSON Schema
        return {"description": str(annotation)}


def describe(op: Operation) -> dict[str, Any]:
    wire = {p.name: p for p in op.params}
    params = []
    for name, annotation, required in signature_params(op):
        location = wire[name].location if name in wire else "query"
        entry: dict[str, Any] = {"name": name, "in": location, "required": required}
        if name in wire and wire[name].wire_name != name and location != "body":
            entry["wire_name"] = wire[name].wire_name
        schema = _schema(annotation)
        text = json.dumps(schema, ensure_ascii=False)
        if len(text) > MAX_SCHEMA_CHARS:
            schema = {"note": f"schema truncated ({len(text)} chars); see docs_url",
                      "title": schema.get("title"),
                      "properties": sorted((schema.get("properties") or {}).keys())}
        entry["schema"] = schema
        if location == "file":
            entry["note"] = "file uploads are not supported through MCP"
        params.append(entry)
    return {
        **op.brief(),
        "description": op.description,
        # An operation without servers of its own goes to its module's host.
        "host": op.hosts[0] if op.hosts else load_method(op)[0].Configuration().host,
        "parameters": params,
        "docs_url": op.docs_url,
        "call_with": "call_read_operation" if op.read_only else "call_write_operation",
    }


def _arguments(op: Operation, arguments: dict[str, Any]) -> dict[str, Any]:
    """Map the agent's arguments onto the SDK's keyword arguments.

    Wildberries' own docs say ``isAnswered``; the SDK says ``is_answered``.
    Either is accepted, so an agent working from the official docs still works.
    Path, query and header values are checked against the SDK's types. The body
    is sent as given: the generated models would silently drop a field the
    specs do not list yet and empty out a ``oneOf`` body altogether.
    """
    signature = {name: (annotation, required)
                 for name, annotation, required in signature_params(op)}
    by_wire = {p.wire_name: p.name for p in op.params}
    body = {p.name for p in op.params if p.location == "body"}
    out: dict[str, Any] = {}
    for key, value in (arguments or {}).items():
        name = key if key in signature else by_wire.get(key) or _snake(key)
        if name not in signature:
            raise ValueError(f"{op.id} has no parameter {key!r}; it takes: "
                             f"{', '.join(sorted(signature)) or 'no parameters'}")
        if name not in body and value is not None:
            try:
                value = TypeAdapter(signature[name][0]).validate_python(value)
            except ValidationError as exc:
                raise ValueError(f"{op.id}: invalid {name!r}: "
                                 f"{exc.errors()[0].get('msg', exc)}") from None
        out[name] = value
    missing = [name for name, (_a, required) in signature.items()
               if required and out.get(name) is None]
    if missing:
        raise ValueError(f"{op.id}: missing required {', '.join(missing)}; "
                         "describe_operation lists them.")
    return out


def _decode(raw: bytes) -> Any:
    text = raw.decode("utf-8", errors="replace")
    try:
        return json.loads(text) if text else None
    except ValueError:
        return text


def _clip(value: Any) -> tuple[Any, bool]:
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    if len(text) <= MAX_RESPONSE_CHARS:
        return value, False
    return text[:MAX_RESPONSE_CHARS], True


def call(op: Operation, arguments: dict[str, Any]) -> dict[str, Any]:
    token = os.environ.get("WB_API_TOKEN", "").strip()
    if not token:
        raise ValueError("WB_API_TOKEN is not set: add it to the env of this MCP "
                         "server in the client's configuration.")
    module, api_class = load_method(op)
    kwargs = _arguments(op, arguments)
    api = api_class(module.ApiClient(module.Configuration(api_key={"HeaderApiKey": token})))
    # The SDK's own request builder: host, path, query encoding, headers and
    # auth, without the public method's model validation of the body.
    serialize = getattr(api, f"_{op.method}_serialize")
    params = {name: None for name in inspect.signature(serialize).parameters}
    params.update(kwargs, _request_auth=None, _content_type=None, _headers=None, _host_index=0)
    response = api.api_client.call_api(*serialize(**params), _request_timeout=REQUEST_TIMEOUT)
    response.read()
    body, truncated = _clip(_decode(response.data))
    result: dict[str, Any] = {"status": response.status, "body": body}
    limits = {k: v for k, v in response.getheaders().items()
              if k.lower().startswith(("x-ratelimit", "retry-after"))}
    if limits:
        result["rate_limit"] = limits
    if truncated:
        result["truncated"] = (f"response cut at {MAX_RESPONSE_CHARS} characters; "
                               "narrow it with the operation's paging or filter parameters")
    return result


@server.tool(annotations=ToolAnnotations(title="Search Wildberries API operations",
                                         readOnlyHint=True, openWorldHint=False))
def search_operations(query: str, module: str | None = None, limit: int = 15) -> dict[str, Any]:
    """Find Wildberries API operations by words (Russian or English), a path or a method name.

    Examples: "неотвеченные отзывы", "остатки на складах", "/api/v3/orders/new".
    Optionally narrow to one module; an empty query lists the module's operations.
    """
    cat = catalog()
    if module and module not in cat.modules:
        raise ToolError(f"Unknown module {module!r}; modules: {', '.join(cat.modules)}")
    found = cat.search(query, module=module, limit=min(max(limit, 1), 100))
    return {"operations": [op.brief() for op in found], "modules": cat.modules}


@server.tool(annotations=ToolAnnotations(title="Describe a Wildberries API operation",
                                         readOnlyHint=True, openWorldHint=False))
def describe_operation(operation_id: str) -> dict[str, Any]:
    """Parameters, request body JSON Schema, host, rate limits and docs link of one operation."""
    with _agent_errors():
        return describe(catalog().get(operation_id))


@server.tool(annotations=ToolAnnotations(title="Call a read-only Wildberries API operation",
                                         readOnlyHint=True, openWorldHint=True))
async def call_read_operation(operation_id: str,
                              arguments: dict[str, Any] | None = None) -> dict[str, Any]:
    """Run a GET operation with the seller's token and return the HTTP status and JSON body.

    `arguments` maps parameter names (as describe_operation lists them, or as
    Wildberries' docs spell them) to values.
    """
    with _agent_errors():
        op = catalog().get(operation_id)
        if not op.read_only:
            raise ValueError(f"{op.id} is {op.verb}: run it with call_write_operation.")
        return await anyio.to_thread.run_sync(call, op, arguments or {})


@server.tool(annotations=ToolAnnotations(title="Call a Wildberries API operation that may change data",
                                         readOnlyHint=False, destructiveHint=True,
                                         idempotentHint=False, openWorldHint=True))
async def call_write_operation(operation_id: str,
                               arguments: dict[str, Any] | None = None) -> dict[str, Any]:
    """Run a POST, PUT, PATCH or DELETE operation with the seller's token.

    These can change the seller's account: prices, stocks, cards, campaigns,
    replies to buyers. Some report and list operations are POST as well. The
    request body goes in `arguments` under the body parameter's name, as JSON
    keyed the way Wildberries' docs spell the fields.
    """
    with _agent_errors():
        op = catalog().get(operation_id)
        if op.read_only:
            raise ValueError(f"{op.id} is {op.verb}: run it with call_read_operation.")
        return await anyio.to_thread.run_sync(call, op, arguments or {})


def main() -> None:
    server.run()


if __name__ == "__main__":
    main()
