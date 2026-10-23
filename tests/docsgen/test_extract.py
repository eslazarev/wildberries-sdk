"""The generator renames methods whenever openapi-generator's naming changes.

These tests therefore never spell a method name out: they look it up the way
``build-docs-site.py`` does and assert the invariants that must survive a
rename — every operation resolves, and an operation belonging to a non-default
API class keeps that class.
"""
import pytest

from docsgen.extract import (
    python_anchor, npm_names, go_names, php_names, rust_names,
    npm_class_map, go_class_map, php_class_map, rust_class_map, class_maps,
)
from docsgen.naming import to_camel, to_pascal

CLIENTS = "clients"
PING = ("GET", "/ping")                       # lives in WBAPIApi, not DefaultApi
BALANCE = ("GET", "/api/v1/account/balance")  # a plain DefaultApi operation


def _snake(module, verb_path):
    anchor = python_anchor(module, CLIENTS)
    assert verb_path in anchor, f"{verb_path} is missing from the {module} python client"
    return anchor[verb_path]


def _key(lang, snake):
    """The class-map key build-docs-site.py looks an operation up by."""
    if lang == "rust":
        return snake.lower()
    if lang == "go":
        return to_pascal(snake).lower()
    return to_camel(snake).lower()


def test_python_anchor_maps_verb_path_to_a_real_method():
    anchor = python_anchor("finances", CLIENTS)
    assert anchor
    assert all(name.isidentifier() for name in anchor.values())
    assert "account_balance" in _snake("finances", BALANCE)
    assert "sales_reports_list" in _snake("finances", ("POST", "/api/finance/v1/sales-reports/list"))


def test_every_language_exposes_the_same_operation():
    snake = _snake("finances", BALANCE)
    lowered = {
        "npm": {n.lower() for n in npm_names("finances", CLIENTS)},
        "go": {n.lower() for n in go_names("finances", CLIENTS)},
        "php": {n.lower() for n in php_names("finances", CLIENTS)},
        "rust": {n.lower() for n in rust_names("finances", CLIENTS)},
    }
    # Acronym casing differs per generator, so compare case-insensitively.
    assert to_camel(snake).lower() in lowered["npm"]
    assert to_pascal(snake).lower() in lowered["go"]
    assert to_camel(snake).lower() in lowered["php"]
    assert snake.lower() in lowered["rust"]


def test_php_names_exclude_helper_suffixes():
    names = php_names("finances", CLIENTS)
    assert not any(n.endswith(("WithHttpInfo", "Async", "Request")) for n in names)


def test_missing_module_returns_empty_set():
    assert npm_names("does_not_exist", CLIENTS) == set()


@pytest.mark.parametrize("lang,class_map,expected", [
    ("npm", npm_class_map, "WBAPIApi"),
    ("go", go_class_map, "WBAPIAPI"),
    ("php", php_class_map, "WBAPIApi"),
    ("rust", rust_class_map, "wbapi_api"),
])
def test_ping_keeps_its_own_api_class(lang, class_map, expected):
    snake = _snake("general", PING)
    cmap = class_map("general", CLIENTS)
    key = _key(lang, snake)
    assert key in cmap, f"{key} missing from the {lang} class map"
    _real_name, token = cmap[key]
    assert expected.lower() in token.lower()
    assert "defaultapi" not in token.lower().replace("_", "")


def test_default_api_operations_stay_on_default_api():
    snake = _snake("finances", BALANCE)
    cmaps = class_maps("finances", CLIENTS)
    _npm_real, npm_class = cmaps["npm"][_key("npm", snake)]
    assert npm_class == "DefaultApi"
    _go_real, go_field = cmaps["go"][_key("go", snake)]
    assert go_field == "DefaultApi"


def test_class_maps_cover_every_python_operation():
    """Whatever the generator renames, no operation may fall out of a client."""
    anchor = python_anchor("finances", CLIENTS)
    cmaps = class_maps("finances", CLIENTS)
    for snake in anchor.values():
        for lang in ("npm", "go", "php", "rust"):
            assert _key(lang, snake) in cmaps[lang], f"{snake} missing in {lang}"
