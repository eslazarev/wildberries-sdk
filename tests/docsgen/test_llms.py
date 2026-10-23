from collections import OrderedDict

from docsgen.llms import SITE_URL, operation_url, render_llms_full
from docsgen.specs import Operation, Param


def _op(**kw):
    base = dict(module="general", verb="GET", path="/api/v1/account/balance",
                summary="Получить баланс", description="Длинное описание из спеки WB.",
                params=[], request_model=None, response_model=None)
    base.update(kw)
    return Operation(**base)


def _names(python="get_api_v1_account_balance", npm=("getApiV1AccountBalance", "WBAPIApi"),
           go=("GetApiV1AccountBalance", "WBAPIApi"),
           php=("getApiV1AccountBalance", "Wildberries\\Sdk\\General\\Api\\WBAPIApi"),
           rust=("get_api_v1_account_balance", "default_api")):
    return {"python": python, "npm": npm, "go": go, "php": php, "rust": rust}


def _entries(*ops):
    return OrderedDict([("general", [(op, _names()) for op in ops])])


def test_header_points_at_the_site_and_the_short_index():
    text = render_llms_full(_entries(_op()))
    assert text.startswith("# ")
    assert SITE_URL in text
    assert "llms.txt" in text


def test_one_block_per_operation():
    text = render_llms_full(_entries(_op(), _op(path="/api/v1/other", summary="Другое")))
    assert text.count("\n### ") == 2


def test_block_carries_route_and_title():
    text = render_llms_full(_entries(_op()))
    assert "### Получить баланс" in text
    assert "route: GET /api/v1/account/balance" in text


def test_block_lists_every_client_method():
    text = render_llms_full(_entries(_op()))
    assert "python: wildberries_sdk.general.DefaultApi.get_api_v1_account_balance" in text
    assert "node: WBAPIApi.getApiV1AccountBalance" in text
    assert "go: client.WBAPIApi.GetApiV1AccountBalance" in text
    assert "php: Wildberries\\Sdk\\General\\Api\\WBAPIApi::getApiV1AccountBalance" in text
    assert "rust: wildberries_sdk_general::apis::default_api::get_api_v1_account_balance" in text


def test_missing_client_is_marked_not_guessed():
    entries = OrderedDict([("general", [(_op(), _names(go=None, python=None))])])
    text = render_llms_full(entries)
    assert "go: —" in text
    assert "python: —" in text


def test_block_links_to_the_operation_page():
    text = render_llms_full(_entries(_op()))
    assert ("docs: " + SITE_URL
            + "/reference/general/get_api_v1_account_balance/") in text


def test_required_params_and_models_are_listed():
    op = _op(params=[Param("nmID", "query", True, "integer", "ID"),
                     Param("locale", "query", False, "string", "язык")],
             request_model="BalanceRequest", response_model="BalanceResponse")
    text = render_llms_full(_entries(op))
    assert "required: nmID" in text
    assert "locale" not in text.split("required:")[1].splitlines()[0]
    assert "body: BalanceRequest" in text
    assert "returns: BalanceResponse" in text


def test_optional_lines_are_omitted_when_empty():
    text = render_llms_full(_entries(_op()))
    assert "required:" not in text
    assert "body:" not in text
    assert "returns:" not in text


def test_module_heading_counts_its_operations():
    text = render_llms_full(_entries(_op(), _op(path="/x", summary="X")))
    assert "## general (2 operations)" in text


def test_spec_prose_is_left_out():
    # The digest must stay context-sized; descriptions live on the site.
    text = render_llms_full(_entries(_op()))
    assert "Длинное описание" not in text


def test_render_is_deterministic():
    entries = _entries(_op())
    assert render_llms_full(entries) == render_llms_full(entries)


def test_operation_url_matches_the_site_layout():
    assert operation_url(_op()) == (
        SITE_URL + "/reference/general/get_api_v1_account_balance/")


def test_index_keeps_the_repository_file_and_adds_the_digest_link():
    from docsgen.llms import render_llms_index

    text = render_llms_index("# Wildberries SDK\n\n> summary\n")
    assert text.startswith("# Wildberries SDK")
    assert "> summary" in text
    assert f"{SITE_URL}/llms-full.txt" in text
