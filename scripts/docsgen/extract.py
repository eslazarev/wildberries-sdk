"""Extract real method names from the generated clients.

The Python client is the *anchor*: its ``_<name>_serialize`` blocks contain the
HTTP method and resource path, giving an exact ``(VERB, path) -> snake_name`` map
with no guessing. The other languages expose only method names, which we collect
into sets for verification against case-transformed candidates.

openapi-generator splits operations across multiple API-class files by OpenAPI tag,
so the extractors here scan ALL of a module's API-class files and return a
``method_name_lower -> (real_name, class_token)`` dict so callers can emit the
correct class/service/module in examples.
"""
from __future__ import annotations

import glob
import os
import re
from typing import Dict, Optional, Set, Tuple


def _read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def python_anchor(module: str, clients_dir: str = "clients") -> Dict[Tuple[str, str], str]:
    """Return ``{(VERB, path): snake_method_name}`` from the Python client."""
    api_dir = os.path.join(clients_dir, "python", module, "api")
    result: Dict[Tuple[str, str], str] = {}
    for fp in sorted(glob.glob(os.path.join(api_dir, "*.py"))):
        if os.path.basename(fp) in ("__init__.py", "api.py"):
            continue
        lines = _read(fp).splitlines()
        defs = [
            (m.group(1), i)
            for i, line in enumerate(lines)
            if (m := re.match(r"^    def (\w+)\(", line))
        ]
        blocks = []
        for j, (name, start) in enumerate(defs):
            end = defs[j + 1][1] if j + 1 < len(defs) else len(lines)
            blocks.append((name, lines[start:end]))

        serialize: Dict[str, Tuple[str, str]] = {}
        for name, block in blocks:
            if not (name.startswith("_") and name.endswith("_serialize")):
                continue
            base = name[1:-len("_serialize")]
            method = path = None
            for line in block:
                if method is None:
                    mm = re.search(r"method='([^']+)'", line)
                    if mm:
                        method = mm.group(1)
                if path is None:
                    mp = re.search(r"resource_path='([^']+)'", line)
                    if mp:
                        path = mp.group(1)
                if method and path:
                    break
            if method and path:
                serialize[base] = (method.upper(), path)

        for name, block in blocks:
            if name.startswith("_") or name == "__init__":
                continue
            if name.endswith(("_with_http_info", "_without_preload_content")):
                continue
            if name in serialize:
                result[serialize[name]] = name
    return result


# openapi-generator splits operations across multiple API classes by OpenAPI
# tag (e.g. DefaultApi.ts + APIApi.ts + WBAPIApi.ts). Every extractor below must
# scan ALL of a module's API-class files, not just the ``Default`` one, or
# tagged operations are missed and falsely reported as unavailable.

# PHP class methods that are framework boilerplate, not API operations.
_PHP_BOILERPLATE = {"__construct", "getConfig", "getHostIndex", "setHostIndex"}


def npm_names(module: str, clients_dir: str = "clients") -> Set[str]:
    apis_dir = os.path.join(clients_dir, "npm", module, "src", "apis")
    out: Set[str] = set()
    for fp in glob.glob(os.path.join(apis_dir, "*.ts")):
        if os.path.basename(fp) == "index.ts":
            continue
        out.update(m.group(1) for m in re.finditer(r"async (\w+)Raw\(", _read(fp)))
    return out


def go_names(module: str, clients_dir: str = "clients") -> Set[str]:
    module_dir = os.path.join(clients_dir, "go", module)
    out: Set[str] = set()
    for fp in glob.glob(os.path.join(module_dir, "api_*.go")):
        out.update(m.group(1) for m in re.finditer(r"\)\s+([A-Z]\w+)Execute\(", _read(fp)))
    return out


def php_names(module: str, clients_dir: str = "clients") -> Set[str]:
    api_dir = os.path.join(clients_dir, "php", module, "lib", "Api")
    out: Set[str] = set()
    for fp in glob.glob(os.path.join(api_dir, "*.php")):
        for m in re.finditer(r"public function (\w+)\(", _read(fp)):
            name = m.group(1)
            if name.endswith(("WithHttpInfo", "Async", "Request")) or name in _PHP_BOILERPLATE:
                continue
            out.add(name)
    return out


def rust_names(module: str, clients_dir: str = "clients") -> Set[str]:
    apis_dir = os.path.join(clients_dir, "rust", module, "src", "apis")
    out: Set[str] = set()
    for fp in glob.glob(os.path.join(apis_dir, "*.rs")):
        if os.path.basename(fp) in ("configuration.rs", "mod.rs"):
            continue
        out.update(m.group(1) for m in re.finditer(r"^pub async fn (\w+)\(", _read(fp), re.M))
    return out


def name_sets(module: str, clients_dir: str = "clients") -> Dict[str, Set[str]]:
    """All four verification sets keyed by language id."""
    return {
        "npm": npm_names(module, clients_dir),
        "go": go_names(module, clients_dir),
        "php": php_names(module, clients_dir),
        "rust": rust_names(module, clients_dir),
    }


# ---------------------------------------------------------------------------
# Method → class-token maps
# Each function returns ``{method_name_lower: (real_method_name, class_token)}``
# so callers can resolve both the real name and the class/service/module to use
# in generated examples.
# ---------------------------------------------------------------------------

def _go_field_from_service(service_type: str) -> str:
    """Convert a Go service type name to its APIClient field name.

    ``DefaultApiService`` → ``DefaultApi``
    ``WBAPIAPIService``   → ``WBAPIAPI``
    ``CSVAPIService``     → ``CSVAPI``
    """
    if service_type.endswith("Service"):
        return service_type[: -len("Service")]
    return service_type


def npm_class_map(module: str, clients_dir: str = "clients") -> Dict[str, Tuple[str, str]]:
    """Return ``{method_lower: (real_name, ClassName)}`` for all npm API classes."""
    apis_dir = os.path.join(clients_dir, "npm", module, "src", "apis")
    out: Dict[str, Tuple[str, str]] = {}
    for fp in sorted(glob.glob(os.path.join(apis_dir, "*.ts"))):
        basename = os.path.basename(fp)
        if basename == "index.ts":
            continue
        class_name = basename[: -len(".ts")]  # e.g. "WBAPIApi"
        for m in re.finditer(r"async (\w+)Raw\(", _read(fp)):
            name = m.group(1)
            out[name.lower()] = (name, class_name)
    return out


def go_class_map(module: str, clients_dir: str = "clients") -> Dict[str, Tuple[str, str]]:
    """Return ``{method_lower: (real_name, field_name)}`` for all go API files."""
    module_dir = os.path.join(clients_dir, "go", module)
    out: Dict[str, Tuple[str, str]] = {}
    for fp in sorted(glob.glob(os.path.join(module_dir, "api_*.go"))):
        content = _read(fp)
        # Determine the service type declared in this file.
        svc_m = re.search(r"^type (\w+Service) service", content, re.M)
        if not svc_m:
            continue
        field_name = _go_field_from_service(svc_m.group(1))
        # Each Execute() helper's outer receiver method is named <Method>Execute.
        for m in re.finditer(r"\)\s+([A-Z]\w+)Execute\(", content):
            name = m.group(1)
            out[name.lower()] = (name, field_name)
    return out


def php_class_map(module: str, clients_dir: str = "clients") -> Dict[str, Tuple[str, str]]:
    """Return ``{method_lower: (real_name, 'Namespace\\\\Class')}`` for all PHP API classes."""
    api_dir = os.path.join(clients_dir, "php", module, "lib", "Api")
    out: Dict[str, Tuple[str, str]] = {}
    for fp in sorted(glob.glob(os.path.join(api_dir, "*.php"))):
        content = _read(fp)
        class_name = os.path.basename(fp)[: -len(".php")]  # e.g. "WBAPIApi"
        ns_m = re.search(r"^namespace ([^;]+);", content, re.M)
        namespace = ns_m.group(1) if ns_m else "WildberriesSdk\\Api"
        full_class = f"{namespace}\\{class_name}"
        for m in re.finditer(r"public function (\w+)\(", content):
            name = m.group(1)
            if name.endswith(("WithHttpInfo", "Async", "Request")) or name in _PHP_BOILERPLATE:
                continue
            out[name.lower()] = (name, full_class)
    return out


def rust_class_map(module: str, clients_dir: str = "clients") -> Dict[str, Tuple[str, str]]:
    """Return ``{method_lower: (real_name, mod_name)}`` for all rust API modules."""
    apis_dir = os.path.join(clients_dir, "rust", module, "src", "apis")
    out: Dict[str, Tuple[str, str]] = {}
    for fp in sorted(glob.glob(os.path.join(apis_dir, "*.rs"))):
        basename = os.path.basename(fp)
        if basename in ("configuration.rs", "mod.rs"):
            continue
        mod_name = basename[: -len(".rs")]  # e.g. "wbapi_api"
        for m in re.finditer(r"^pub async fn (\w+)\(", _read(fp), re.M):
            name = m.group(1)
            out[name.lower()] = (name, mod_name)
    return out


def class_maps(module: str, clients_dir: str = "clients") -> Dict[str, Dict[str, Tuple[str, str]]]:
    """Return method→(real_name, class_token) maps for all four languages."""
    return {
        "npm": npm_class_map(module, clients_dir),
        "go": go_class_map(module, clients_dir),
        "php": php_class_map(module, clients_dir),
        "rust": rust_class_map(module, clients_dir),
    }


# --- request-body parameter names ------------------------------------------
#
# The body parameter is not called "body": openapi-generator names it after the
# model, and for an inline body it invents a model from the operation id. A
# guessed key is the worst kind of wrong here — several WB write methods accept
# unknown field names, answer 204 and change nothing — so read the real name
# out of each client instead of deriving it.

_PY_SCALARS = ("StrictStr", "StrictInt", "StrictBool", "StrictFloat", "StrictBytes")
_TS_SCALARS = {"number", "string", "boolean", "Date"}
_GO_SCALARS = {"string", "int32", "int64", "float32", "float64", "bool", "time.Time"}


def _python_signatures(module: str, clients_dir: str) -> Dict[str, list]:
    """``{method: [(param, annotation, required), ...]}`` from the Python client."""
    api_dir = os.path.join(clients_dir, "python", module, "api")
    out: Dict[str, list] = {}
    for fp in sorted(glob.glob(os.path.join(api_dir, "*.py"))):
        for m in re.finditer(r"^    def (\w+)\(\s*\n((?:        .*\n)+?)    \)",
                             _read(fp), re.M):
            method, block = m.group(1), m.group(2)
            if method in out:
                continue
            params = []
            for name, annotation, default in re.findall(
                    r"^        (\w+)\s*:\s*(.+?)(\s*=\s*\S+)?,?\s*$", block, re.M):
                if name.startswith("_"):
                    continue
                params.append((name, annotation.strip().rstrip(","), not default))
            out[method] = params
    return out


def python_params(module: str, clients_dir: str = "clients") -> Dict[str, list]:
    """``{method: [(param_name, required), ...]}`` — the client's own spelling.

    The spec calls a parameter ``isAnswered``; the generated client calls it
    ``is_answered``. Examples must use the client's name or they raise TypeError.
    """
    return {
        method: [(name, required) for name, _annotation, required in params]
        for method, params in _python_signatures(module, clients_dir).items()
    }


def python_body_params(module: str, clients_dir: str = "clients") -> Dict[str, str]:
    """Return ``{method_name: body_parameter_name}`` from the Python client."""
    out: Dict[str, str] = {}
    for method, params in _python_signatures(module, clients_dir).items():
        for name, annotation, _required in params:
            core = annotation.replace("Annotated[", "").replace("Optional[", "")
            core = core.split(",")[0].strip().rstrip("]")
            if core.startswith(_PY_SCALARS):
                continue
            if name in ("body", "request_body") or core.startswith(("List[", "Dict[", "object")) \
                    or re.match(r"^[A-Z]", core):
                out[method] = name
                break
    return out


def npm_body_params(module: str, clients_dir: str = "clients") -> Dict[str, str]:
    """Return ``{method_lower: body_property_name}`` from the npm client."""
    apis_dir = os.path.join(clients_dir, "npm", module, "src", "apis")
    out: Dict[str, str] = {}
    for fp in sorted(glob.glob(os.path.join(apis_dir, "*.ts"))):
        content = _read(fp)
        interfaces = {
            m.group(1): m.group(2)
            for m in re.finditer(r"export interface (\w+) \{\n(.*?)\n\}", content, re.S)
        }
        for m in re.finditer(r"async (\w+)\(requestParameters: (\w+)", content):
            method, iface = m.group(1), m.group(2)
            props = re.findall(r"^    (\w+)\??: ([^;]+);", interfaces.get(iface, ""), re.M)
            body = _last_non_scalar(props, _TS_SCALARS, ("body", "requestBody"))
            if body:
                out[method.lower()] = body
    return out


def go_body_params(module: str, clients_dir: str = "clients") -> Dict[str, str]:
    """Return ``{method_lower: BuilderMethodName}`` for the Go body setters."""
    module_dir = os.path.join(clients_dir, "go", module)
    out: Dict[str, str] = {}
    for fp in sorted(glob.glob(os.path.join(module_dir, "api_*.go"))):
        for m in re.finditer(
                r"func \(r Api(\w+)Request\) (\w+)\(\w+ ([^)]+)\) Api\w+Request", _read(fp)):
            method, setter, go_type = m.group(1), m.group(2), m.group(3)
            if _scalar_go(go_type) and setter.lower() not in ("body", "requestbody"):
                continue
            out[method.lower()] = setter
    return out


def _last_non_scalar(props, scalars, body_names):
    """The property holding the request body: named outright, else the last
    one whose type is not a plain scalar."""
    chosen = None
    for name, type_ in props:
        if name in body_names:
            return name
        base = type_.replace("Array<", "").replace(">", "").split("|")[0].strip()
        if base not in scalars:
            chosen = name
    return chosen


def _scalar_go(go_type: str) -> bool:
    base = go_type.lstrip("*[]").strip()
    return base in _GO_SCALARS


def body_params(module: str, clients_dir: str = "clients") -> Dict[str, Dict[str, str]]:
    """Body parameter names per language, keyed as the class maps are."""
    return {
        "python": python_body_params(module, clients_dir),
        "npm": npm_body_params(module, clients_dir),
        "go": go_body_params(module, clients_dir),
    }
