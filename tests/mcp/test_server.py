"""The MCP tools themselves: needs the `mcp` package (Python 3.10+).

Nothing here reaches Wildberries: the SDK's HTTP layer is replaced, so what the
server would send is checked without a token or network.
"""
import importlib
import json
import sys
from pathlib import Path
from urllib.parse import quote

import pytest

pytest.importorskip("mcp")

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from mcp.server.mcpserver.exceptions import ToolError  # noqa: E402

from wildberries_mcp import server  # noqa: E402


class _Response:
    status, reason, headers = 200, "OK", {"X-Ratelimit-Remaining": "9"}
    data = b'{"ok": true}'


@pytest.fixture
def sent(monkeypatch):
    monkeypatch.setenv("WB_API_TOKEN", "test-token")
    requests = []
    for module in server.catalog().modules:
        rest = importlib.import_module(f"wildberries_sdk.{module}.rest")

        def request(self, method, url, headers=None, body=None, post_params=None,
                    _request_timeout=None, _rest=rest):
            requests.append({"method": method, "url": url, "body": body,
                             "auth": (headers or {}).get("Authorization")})
            return _rest.RESTResponse(_Response())

        monkeypatch.setattr(rest.RESTClientObject, "request", request)
    return requests


def _op(predicate):
    return next(op for op in server.catalog().operations if predicate(op))


def test_every_operation_can_be_described():
    for op in server.catalog().operations:
        described = server.describe(op)
        assert described["host"] and described["docs_url"]
        json.dumps(described, ensure_ascii=False)


def _sample(annotation):
    """A value the SDK accepts for a parameter, whatever its type."""
    from pydantic import TypeAdapter
    uuid = "0f6d4b52-5a7b-4f2c-9a51-1c2f3e4d5a6b"
    for candidate in (1, "2026-01-01", True, "x", uuid, [1], ["x"], [uuid]):
        try:
            TypeAdapter(annotation).validate_python(candidate)
            return candidate
        except Exception:
            continue
    return None


def test_query_parameters_accept_the_names_from_wildberries_docs(sent):
    def renamed(op):
        return [p for p in op.params if p.location == "query" and p.wire_name != p.name]

    op = _op(lambda o: o.read_only and renamed(o))
    param = renamed(op)[0]
    signature = {name: (annotation, req) for name, annotation, req in server.signature_params(op)}
    arguments = {name: _sample(annotation) for name, (annotation, req) in signature.items() if req}
    arguments.pop(param.name, None)
    arguments[param.wire_name] = _sample(signature[param.name][0])
    server.call(op, arguments)
    assert f"{quote(param.wire_name)}=" in sent[-1]["url"]


def test_body_goes_out_as_given_even_with_fields_the_specs_lack(sent):
    op = _op(lambda o: not o.read_only and any(p.location == "body" for p in o.params)
             and not any(p.location == "path" for p in o.params))
    body = next(p.name for p in op.params if p.location == "body")
    payload = {"brandNewField": True, "items": [{"nmID": 1}]}
    result = server.call(op, {body: payload})
    assert sent[-1]["body"] == payload
    assert sent[-1]["method"] == op.verb
    assert sent[-1]["url"].startswith(op.hosts[0] + op.path)
    assert sent[-1]["auth"] == "test-token"
    assert result == {"status": 200, "body": {"ok": True},
                      "rate_limit": {"X-Ratelimit-Remaining": "9"}}


def test_missing_token_is_explained(monkeypatch):
    monkeypatch.delenv("WB_API_TOKEN", raising=False)
    with pytest.raises(ValueError, match="WB_API_TOKEN"):
        server.call(_op(lambda o: o.read_only), {})


def test_unknown_parameter_lists_the_real_ones(sent):
    op = _op(lambda o: o.read_only and o.params)
    with pytest.raises(ValueError, match="has no parameter 'bogus'"):
        server.call(op, {"bogus": 1})


@pytest.mark.anyio
async def test_reads_and_writes_go_through_their_own_tools(sent):
    read = _op(lambda o: o.read_only)
    write = _op(lambda o: not o.read_only)
    with pytest.raises(ToolError, match="call_read_operation"):
        await server.call_write_operation(read.id)
    with pytest.raises(ToolError, match="call_write_operation"):
        await server.call_read_operation(write.id)


@pytest.mark.anyio
async def test_tool_annotations_mark_writes_destructive():
    tools = {t.name: t for t in await server.server.list_tools()}
    assert set(tools) == {"search_operations", "describe_operation",
                          "call_read_operation", "call_write_operation"}
    assert tools["call_write_operation"].annotations.destructive_hint is True
    for name in ("search_operations", "describe_operation", "call_read_operation"):
        assert tools[name].annotations.read_only_hint is True


@pytest.fixture
def anyio_backend():
    return "asyncio"
