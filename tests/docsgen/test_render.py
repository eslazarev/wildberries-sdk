from docsgen.specs import Operation, Param
from docsgen.render import operation_slug, render_operation, render_module_index
from docsgen.nav import build_summary


def _op():
    return Operation(
        module="finances", verb="GET", path="/api/v1/account/balance",
        summary="Получить баланс продавца", description="Возвращает баланс.",
        params=[Param("locale", "query", False, "string", "Язык ответа")],
        request_model=None, response_model="ApiV1AccountBalanceGet200Response",
    )


def test_operation_slug_from_verb_and_path():
    assert operation_slug(_op()) == "get_api_v1_account_balance"


def test_render_operation_contains_core_sections():
    # For non-Python languages names are (real_method_name, class_token) tuples.
    names = {
        "python": "api_v1_account_balance_get",
        "rust": ("api_v1_account_balance_get", "default_api"),
        "npm": ("apiV1AccountBalanceGet", "DefaultApi"),
        "php": ("apiV1AccountBalanceGet", "Wildberries\\Sdk\\Finances\\Api\\DefaultApi"),
        "go": ("ApiV1AccountBalanceGet", "DefaultApi"),
    }
    md = render_operation(_op(), names)
    assert md.startswith("# Получить баланс продавца")
    assert "`GET /api/v1/account/balance`" in md
    assert "Возвращает баланс." in md
    assert "| locale | query |" in md
    assert '=== "Python"' in md
    assert '=== "Rust"' in md
    assert "ApiV1AccountBalanceGet200Response" in md


def test_render_module_index_lists_operations():
    md = render_module_index("finances", [_op()])
    assert md.startswith("# finances")
    assert "Получить баланс продавца" in md
    assert "get_api_v1_account_balance.md" in md


def test_build_summary_structure():
    op = Operation(
        module="finances", verb="GET", path="/api/v1/account/balance",
        summary="Получить баланс продавца", description="",
        params=[], request_model=None, response_model=None,
    )
    summary = build_summary({"finances": [op]})
    assert "* [Wildberries SDK](index.md)" in summary
    assert "* [Начало работы](getting-started.md)" in summary
    assert "* Справочник API" in summary
    assert "* [finances](reference/finances/index.md)" in summary
    assert "* [Получить баланс продавца](reference/finances/get_api_v1_account_balance.md)" \
        in summary


def test_summary_links_to_deepwiki_above_the_reference():
    from docsgen.nav import DEEPWIKI_URL

    summary = build_summary({})
    assert f"* [Спросить DeepWiki]({DEEPWIKI_URL})" in summary
    lines = summary.splitlines()
    assert lines.index(f"* [Спросить DeepWiki]({DEEPWIKI_URL})") < lines.index("* Справочник API")
