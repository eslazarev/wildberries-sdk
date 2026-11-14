"""Every Wildberries API operation the installed wildberries-sdk can call.

The catalog is read from the SDK's own source, not from a copy of the specs:
each generated method carries its summary and description in the docstring,
and its ``_<name>_serialize`` twin holds the HTTP verb, the path, the hosts and
the wire name of every parameter. Reading the files instead of importing them
keeps startup instant — importing all modules takes seconds — and a module is
imported only when one of its operations is described or called.

Kept free of the ``mcp`` package and of Python 3.10 syntax, so the repository
test suite can check it on any interpreter.
"""
from __future__ import annotations

import importlib
import importlib.metadata
import importlib.util
import inspect
import os
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

SDK_PACKAGE = "wildberries_sdk"
SITE_URL = "https://eslazarev.github.io/wildberries-sdk/"

_DEF = re.compile(r"^    def (\w+)\(", re.M)
_CLASS = re.compile(r"^class (\w+)\b", re.M)
_DOCSTRING = re.compile(r'"""(.*?)"""', re.S)
_VERB = re.compile(r"method='([A-Z]+)'")
_PATH = re.compile(r"resource_path='([^']+)'")
_HOSTS = re.compile(r"_hosts = \[(.*?)\]", re.S)
_VERSION = re.compile(r'^__version__ = "([^"]+)"', re.M)
# How the generated client puts each argument on the wire.
_WIRE = (
    ("path", re.compile(r"_path_params\['([^']+)'\] = (\w+)")),
    ("query", re.compile(r"_query_params\.append\(\('([^']+)', (\w+)\)")),
    ("header", re.compile(r"_header_params\['([^']+)'\] = (\w+)\s*$", re.M)),
    ("form", re.compile(r"_form_params\.append\(\('([^']+)', (\w+)\)")),
    ("file", re.compile(r"_files\['([^']+)'\] = (\w+)")),
)
_BODY = re.compile(r"_body_params = (\w+)")
_SKIP_SUFFIXES = ("_with_http_info", "_without_preload_content")


@dataclass
class Param:
    name: str           # the Python keyword argument
    location: str       # path, query, header, form, file or body
    wire_name: str      # the name Wildberries' docs use, e.g. ``isAnswered``


@dataclass
class Operation:
    id: str             # ``<module>.<method>``, stable across releases
    module: str
    api_class: str
    method: str
    verb: str
    path: str
    summary: str
    description: str
    hosts: List[str] = field(default_factory=list)
    params: List[Param] = field(default_factory=list)

    @property
    def read_only(self) -> bool:
        return self.verb in ("GET", "HEAD", "OPTIONS")

    @property
    def docs_url(self) -> str:
        cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", self.path.strip("/"))
        cleaned = re.sub(r"_+", "_", cleaned).strip("_").lower()
        return f"{SITE_URL}reference/{self.module}/{self.verb.lower()}_{cleaned}/"

    def brief(self) -> Dict[str, Any]:
        return {"operation_id": self.id, "verb": self.verb, "path": self.path,
                "summary": self.summary, "module": self.module,
                "read_only": self.read_only}


def _plain(text: str) -> str:
    """Docstring text without HTML tags and runs of whitespace."""
    text = re.sub(r"<[^>]+>", " ", text.replace('\\"', '"'))
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n\s*", "\n\n", text)).strip()


def _fold(text: str) -> str:
    return text.lower().replace("ё", "е")


def _words(text: str) -> str:
    """Folded text as space-separated words, a space in front.

    Paths and method names split into words too, so ``" ping"`` occurs in
    ``/ping`` and ``get_ping`` but not in ``shipping``.
    """
    return " " + re.sub(r"[\W_]+", " ", _fold(text))


# Summaries are Russian, paths English, and a seller may call a thing by
# another name than Wildberries does. A query word that starts with a key also
# matches the key's alternatives, each at the start of a word.
_SYNONYMS: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    ("отзыв", ("feedback",)),
    ("вопрос", ("question",)),
    ("неотвеч", ("unanswered", "необработ")),
    ("необработ", ("unanswered", "неотвеч")),
    ("остат", ("stock",)),
    ("склад", ("warehouse",)),
    ("заказ", ("order",)),
    ("сборочн", ("order",)),
    ("поставк", ("suppl",)),
    ("поставок", ("suppl",)),
    ("карточ", ("card",)),
    ("товар", ("goods", "product")),
    ("кампан", ("advert", "campaign")),
    ("реклам", ("advert", "promotion")),
    ("баланс", ("balance",)),
    ("продаж", ("sale",)),
    ("возврат", ("return",)),
    ("отчет", ("report",)),
    ("тариф", ("tariff",)),
    ("новост", ("news",)),
    ("скидк", ("discount",)),
    ("штрихкод", ("barcode",)),
    ("баркод", ("barcode",)),
    ("документ", ("document",)),
    ("приемк", ("acceptance",)),
    ("хранен", ("storage",)),
    ("штраф", ("penalt",)),
    ("подключ", ("ping",)),
    ("чат", ("chat",)),
)


def _stem(word: str) -> str:
    # Russian inflects at the end: «отзывов» and «отзывы» share «отзы».
    return word if len(word) <= 4 else word[:max(4, len(word) - 2)]


def _alternatives(word: str) -> List[str]:
    alts = [_stem(word)]
    for key, extra in _SYNONYMS:
        if word.startswith(key):
            alts.extend(extra)
    return alts


def _split_docstring(doc: str) -> Tuple[str, str]:
    body = doc.split("\n        :param", 1)[0].split("\n        :return", 1)[0]
    summary, _, description = body.strip().partition("\n")
    return summary.strip(), _plain(description)


def _parse_file(module: str, source: str) -> List[Operation]:
    classes = [(m.start(), m.group(1)) for m in _CLASS.finditer(source)]
    defs = [(m.start(), m.group(1)) for m in _DEF.finditer(source)]
    blocks: Dict[str, Tuple[str, str]] = {}
    for i, (start, name) in enumerate(defs):
        end = defs[i + 1][0] if i + 1 < len(defs) else len(source)
        owner = [cls for pos, cls in classes if pos < start]
        blocks[name] = (owner[-1] if owner else "", source[start:end])

    ops: List[Operation] = []
    for name, (api_class, block) in blocks.items():
        if name.startswith("_") or name.endswith(_SKIP_SUFFIXES):
            continue
        serialize = blocks.get(f"_{name}_serialize", ("", ""))[1]
        verb, path = _VERB.search(serialize), _PATH.search(serialize)
        if not (verb and path):
            continue
        doc = _DOCSTRING.search(block)
        summary, description = _split_docstring(doc.group(1) if doc else "")
        hosts_block = _HOSTS.search(serialize)
        hosts = re.findall(r"'([^']+)'", hosts_block.group(1)) if hosts_block else []
        params = [Param(py, location, wire)
                  for location, pattern in _WIRE
                  for wire, py in pattern.findall(serialize)]
        body = _BODY.search(serialize)
        if body:
            params.append(Param(body.group(1), "body", body.group(1)))
        ops.append(Operation(
            id=f"{module}.{name}", module=module, api_class=api_class, method=name,
            verb=verb.group(1), path=path.group(1), summary=summary or path.group(1),
            description=description, hosts=hosts, params=params,
        ))
    return ops


def sdk_dir() -> str:
    spec = importlib.util.find_spec(SDK_PACKAGE)
    if spec is None or not spec.submodule_search_locations:
        raise RuntimeError("wildberries-sdk is not installed")
    return list(spec.submodule_search_locations)[0]


def _module_version(path: str) -> Optional[str]:
    try:
        with open(os.path.join(path, "__init__.py"), encoding="utf-8") as fh:
            match = _VERSION.search(fh.read())
    except OSError:
        return None
    return match.group(1) if match else None


def current_modules(root: Optional[str] = None) -> List[str]:
    """Modules regenerated in this release.

    A module whose spec Wildberries retired stays in the package at the version
    it was last generated with; its paths are gone from the API, so leave it out.
    """
    root = root or sdk_dir()
    versions = {}
    for name in sorted(os.listdir(root)):
        version = _module_version(os.path.join(root, name))
        if version and os.path.isdir(os.path.join(root, name, "api")):
            versions[name] = version
    if not versions:
        return []
    try:
        release = importlib.metadata.version("wildberries-sdk")
    except importlib.metadata.PackageNotFoundError:
        release = None
    if release not in versions.values():
        release = max(versions.values(), key=lambda v: tuple(int(p) for p in re.findall(r"\d+", v)))
    return [name for name, version in versions.items() if version == release]


class Catalog:
    def __init__(self, operations: List[Operation]):
        self.operations = operations
        self.by_id = {op.id: op for op in operations}

    @classmethod
    def from_sdk(cls, root: Optional[str] = None) -> "Catalog":
        root = root or sdk_dir()
        ops: List[Operation] = []
        for module in current_modules(root):
            api_dir = os.path.join(root, module, "api")
            for name in sorted(os.listdir(api_dir)):
                if not name.endswith(".py") or name == "__init__.py":
                    continue
                with open(os.path.join(api_dir, name), encoding="utf-8") as fh:
                    ops.extend(_parse_file(module, fh.read()))
        return cls(ops)

    @property
    def modules(self) -> List[str]:
        return sorted({op.module for op in self.operations})

    def get(self, operation_id: str) -> Operation:
        op = self.by_id.get(operation_id.strip())
        if op is None:
            raise KeyError(f"Unknown operation_id {operation_id!r}; "
                           "find one with search_operations.")
        return op

    def search(self, query: str, module: Optional[str] = None,
               limit: int = 15) -> List[Operation]:
        """Operations ranked by how well their text matches every query word.

        Each query word matches the start of a word, by its stem — «отзывов»
        finds «Отзывы» — or by a synonym, so «отзывы» also finds
        ``/api/v1/feedbacks``. Paths and method names count as much as
        summaries, which lets a query be ``/api/v3/orders/new`` or
        ``get_v1_feedbacks``.
        """
        query = query.strip()
        terms = [[" " + alt for alt in _alternatives(w)]
                 for w in re.findall(r"\w+", _fold(query).replace("_", " ")) if len(w) > 2]
        scored = []
        for op in self.operations:
            if module and op.module != module:
                continue
            heads = _words(f"{op.summary} {op.path} {op.method}")
            body = _words(f"{op.module} {op.description}")
            score = in_heads = in_body = 0
            for alts in terms:
                head_hits = max(heads.count(a) for a in alts)
                body_hits = max(body.count(a) for a in alts)
                # Being in the summary or path matters more than how often.
                score += 10 * bool(head_hits) + 3 * min(head_hits, 3) + min(body_hits, 3)
                in_heads += bool(head_hits)
                in_body += bool(head_hits or body_hits)
            if terms and in_heads == len(terms):
                score += 10 * len(terms)
            elif in_body < len(terms):
                score //= 4
            if query in (op.path, op.method, op.id):
                score += 1000
            elif "/" in query and query in op.path:
                score += 500
            if score or not terms:
                scored.append((score, op))
        scored.sort(key=lambda pair: (-pair[0], pair[1].id))
        return [op for _, op in scored[:max(1, limit)]]


def load_method(op: Operation):
    """Import the operation's module and return its unbound API method."""
    module = importlib.import_module(f"{SDK_PACKAGE}.{op.module}")
    api_class = getattr(module, op.api_class)
    return module, api_class


def signature_params(op: Operation) -> List[Tuple[str, Any, bool]]:
    """``[(name, annotation, required)]`` of the SDK method, private ones dropped."""
    _module, api_class = load_method(op)
    method = getattr(api_class, op.method)
    hints = getattr(method, "__annotations__", {})
    out = []
    for name, p in inspect.signature(method).parameters.items():
        if name == "self" or name.startswith("_"):
            continue
        out.append((name, hints.get(name, p.annotation), p.default is inspect.Parameter.empty))
    return out
