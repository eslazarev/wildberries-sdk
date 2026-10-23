"""Build minimal, deterministic call-example snippets per language.

Examples show client/config init plus a method call. Required query/path
parameters and the request body are shown as ``...`` placeholders — we never
fabricate field values, so the snippet stays correct as specs evolve.

Names come from the generated clients, never from the spec: the client renames
``isAnswered`` to ``is_answered`` in Python and calls the request body after its
model (``putV3StocksWarehouseIdRequest``), so a snippet written from the spec
would not run. ``names`` therefore carries ``python_params`` and the per-language
body parameter names alongside the method names.

For non-Python languages ``names[lang]`` is a ``(method_name, class_token)``
tuple (where class_token is the API class, Go client field, or Rust module),
or ``None`` when the operation is absent from that client.  For Python it
remains a plain string (or ``None``).
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from .naming import to_camel
from .specs import Operation

# (language id, tab label, fenced code lang)
LANGS: List[Tuple[str, str, str]] = [
    ("python", "Python", "python"),
    ("npm", "Node.js", "typescript"),
    ("go", "Go", "go"),
    ("php", "PHP", "php"),
    ("rust", "Rust", "rust"),
]

UNAVAILABLE = "// операция недоступна в этом клиенте"


def _host(op: Operation) -> Optional[str]:
    """The operation's production host. ``None`` when WB declares no server —
    better to leave the line out than to point the snippet at the wrong API."""
    return op.servers[0] if op.servers else None


def _python_args(op: Operation, names: Dict) -> List[str]:
    """The client's own required parameter names, plus the request body."""
    params = names.get("python_params") or []
    args = [name for name, required in params if required]
    body = names.get("python_body")
    if body and body not in args:
        args.append(body)
    return args


def _required_param_names(op: Operation) -> List[str]:
    return [p.name for p in op.params if p.required and p.name]


def _python(op: Operation, method: str, names: Dict) -> str:
    arglist = ", ".join(f"{name}=..." for name in _python_args(op, names))
    return (
        "import os\n"
        f"from wildberries_sdk import {op.module}\n\n"
        'token = os.getenv("WB_API_TOKEN")\n'
        f"api = {op.module}.DefaultApi(\n"
        f"    {op.module}.ApiClient({op.module}.Configuration(api_key={{\"HeaderApiKey\": token}}))\n"
        ")\n"
        f"result = api.{method}({arglist})\n"
        "print(result)"
    )


def _npm(op: Operation, method: str, class_token: str, names: Dict) -> str:
    fields = [f"{name}: ..." for name in _required_param_names(op)]
    body = names.get("npm_body")
    if body:
        fields.append(f"{body}: {{ ... }}")
    req = "{ " + ", ".join(fields) + " }" if fields else ""
    # The npm runtime defaults basePath to http://localhost, so the host has to
    # be set explicitly or the request never reaches Wildberries.
    host = _host(op)
    base_path = f"  basePath: '{host}',\n" if host else ""
    return (
        f"import {{ Configuration, {class_token} }} from 'wildberries-sdk';\n\n"
        f"const api = new {class_token}(new Configuration({{\n"
        f"{base_path}"
        f"  apiKey: process.env.WB_API_TOKEN,\n"
        f"}}));\n"
        f"const result = await api.{method}({req});\n"
        "console.log(result);"
    )


def _go(op: Operation, method: str, field_name: str, names: Dict) -> str:
    body = names.get("go_body")
    setter = f".{body}(...)" if body else ""
    return (
        "cfg := " + op.module + ".NewConfiguration()\n"
        'cfg.AddDefaultHeader("Authorization", os.Getenv("WB_API_TOKEN"))\n'
        "client := " + op.module + ".NewAPIClient(cfg)\n"
        f"result, _, err := client.{field_name}.{method}(context.Background())"
        f"{setter}.Execute()"
    )


def _php(op: Operation, method: str, full_class: str, names: Dict) -> str:
    args = ", ".join("..." for _ in _required_param_names(op)) or (
        "..." if op.request_model else ""
    )
    # Split "Namespace\Class" into namespace and class name for the setApiKey call.
    # The configuration class lives in the same vendor namespace root.
    ns_parts = full_class.rsplit("\\", 2)
    # ns_parts is e.g. ["Wildberries\Sdk\General", "Api", "WBAPIApi"] (after rsplit by \)
    # Actually full_class is like "Wildberries\Sdk\General\Api\WBAPIApi"
    # We need the root namespace prefix for Configuration: "Wildberries\Sdk\General"
    # Extract it by stripping the trailing "\Api\ClassName"
    ns_root = full_class.rsplit("\\Api\\", 1)[0] if "\\Api\\" in full_class else "WildberriesSdk"
    # Configuration defaults to http://localhost; the host is per operation.
    host = _host(op)
    set_host = f"\n    ->setHost('{host}')" if host else ""
    return (
        "<?php\n"
        f"$config = {ns_root}\\Configuration::getDefaultConfiguration()\n"
        f"    ->setApiKey('Authorization', getenv('WB_API_TOKEN')){set_host};\n"
        f"$api = new {full_class}(new GuzzleHttp\\Client(), $config);\n"
        f"$result = $api->{method}({args});"
    )


def _rust(op: Operation, method: str, mod_name: str, names: Dict) -> str:
    body = ", ..." if (op.request_model or _required_param_names(op)) else ""
    # Configuration::new() leaves base_path at http://localhost.
    host = _host(op)
    base_path = f"config.base_path = \"{host}\".to_owned();\n" if host else ""
    return (
        "use " + f"wildberries_sdk_{op.module}" + f"::apis::{{configuration::Configuration, configuration::ApiKey, {mod_name}}};\n\n"
        "let mut config = Configuration::new();\n"
        f"{base_path}"
        "config.api_key = Some(ApiKey { prefix: None, key: std::env::var(\"WB_API_TOKEN\").unwrap() });\n"
        f"let result = {mod_name}::{method}(&config{body}).await?;"
    )


_BUILDERS = {"python": _python, "npm": _npm, "go": _go, "php": _php, "rust": _rust}


def build_examples(op: Operation, names: Dict) -> List[Tuple[str, str, str]]:
    """Return ``[(tab_label, fenced_lang, code), ...]`` in fixed language order.

    ``names["python"]`` is a plain string (or None).
    ``names[lang]`` for npm/go/php/rust is a ``(method_name, class_token)`` tuple
    or None when the operation is absent from that client.
    """
    out: List[Tuple[str, str, str]] = []
    for lang_id, label, fence in LANGS:
        entry = names.get(lang_id)
        if lang_id == "python":
            code = _python(op, entry, names) if entry else UNAVAILABLE
        else:
            if entry is None:
                code = UNAVAILABLE
            else:
                method, class_token = entry
                code = _BUILDERS[lang_id](op, method, class_token, names)
        out.append((label, fence, code))
    return out
