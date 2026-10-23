from docsgen.specs import Operation, Param
from docsgen.examples import build_examples


def _op():
    return Operation(
        module="finances", verb="POST",
        path="/api/finance/v1/sales-reports/list",
        summary="Список отчётов реализации", description="",
        params=[], request_model="SalesReportListReq", response_model="SalesReportListRes[]",
    )


# For non-Python languages names are (real_method_name, class_token) tuples.
def _names_with_default_api():
    return {
        "python": "post_v1_sales_reports_list",
        "rust": ("post_v1_sales_reports_list", "default_api"),
        "npm": ("postV1SalesReportsList", "DefaultApi"),
        "php": ("postV1SalesReportsList", "Wildberries\\Sdk\\Finances\\Api\\DefaultApi"),
        "go": ("PostV1SalesReportsList", "DefaultApi"),
    }


def test_build_examples_returns_all_five_languages_in_order():
    examples = build_examples(_op(), _names_with_default_api())
    assert [label for label, _lang, _code in examples] == \
        ["Python", "Node.js", "Go", "PHP", "Rust"]


def test_python_example_uses_module_and_method():
    names = {"python": "post_v1_sales_reports_list", "rust": None,
             "npm": None, "php": None, "go": None}
    examples = dict((label, code) for label, _lang, code in build_examples(_op(), names))
    py = examples["Python"]
    assert "from wildberries_sdk import finances" in py
    assert "api.post_v1_sales_reports_list(" in py


def test_unavailable_language_renders_notice():
    names = {"python": "post_v1_sales_reports_list", "rust": None,
             "npm": None, "php": None, "go": None}
    examples = dict((label, code) for label, _lang, code in build_examples(_op(), names))
    assert examples["Go"] == "// операция недоступна в этом клиенте"


def test_npm_uses_correct_class_token():
    """npm example must import and instantiate the class the method actually lives in."""
    names = {
        "python": "ping_get",
        "npm": ("pingGet", "WBAPIApi"),
        "go": ("PingGet", "WBAPIAPI"),
        "php": ("pingGet", "Wildberries\\Sdk\\General\\Api\\WBAPIApi"),
        "rust": ("ping_get", "wbapi_api"),
    }
    op = Operation(
        module="general", verb="GET", path="/ping",
        summary="Ping", description="",
        params=[], request_model=None, response_model=None,
    )
    examples = dict((label, code) for label, _lang, code in build_examples(op, names))
    assert "WBAPIApi" in examples["Node.js"]
    assert "DefaultApi" not in examples["Node.js"]
    assert "WBAPIAPI" in examples["Go"]
    assert "DefaultApi" not in examples["Go"]
    assert "WBAPIApi" in examples["PHP"]
    assert "DefaultApi" not in examples["PHP"]
    assert "wbapi_api" in examples["Rust"]
    assert "default_api" not in examples["Rust"]


# --- names come from the clients, not the specs ----------------------------

def _stocks_op(servers=("https://marketplace-api.wildberries.ru",)):
    return Operation(
        module="items", verb="PUT", path="/api/v3/stocks/{warehouseId}",
        summary="Обновить остатки", description="",
        params=[Param("warehouseId", "path", True, "integer", "ID склада")],
        request_model="object", response_model=None, servers=list(servers),
    )


def _stocks_names():
    return {
        "python": "put_v3_stocks_warehouse_id",
        "python_params": [("warehouse_id", True),
                          ("put_v3_stocks_warehouse_id_request", False)],
        "python_body": "put_v3_stocks_warehouse_id_request",
        "npm": ("putV3StocksWarehouseId", "DefaultApi"),
        "npm_body": "putV3StocksWarehouseIdRequest",
        "go": ("PutV3StocksWarehouseId", "DefaultApi"),
        "go_body": "PutV3StocksWarehouseIdRequest",
        "php": ("putV3StocksWarehouseId", "Wildberries\\Sdk\\Items\\Api\\DefaultApi"),
        "rust": ("put_v3_stocks_warehouse_id", "default_api"),
    }


def _examples(op=None, names=None):
    op = op or _stocks_op()
    names = names or _stocks_names()
    return {label: code for label, _lang, code in build_examples(op, names)}


def test_python_uses_the_clients_parameter_spelling_not_the_specs():
    py = _examples()["Python"]
    # The spec calls it warehouseId; the generated client takes warehouse_id.
    assert "warehouse_id=..." in py
    assert "warehouseId=" not in py


def test_python_names_the_request_body_after_its_model():
    assert "put_v3_stocks_warehouse_id_request=..." in _examples()["Python"]


def test_node_sets_the_base_path_because_the_runtime_defaults_to_localhost():
    node = _examples()["Node.js"]
    assert "basePath: 'https://marketplace-api.wildberries.ru'" in node


def test_node_names_the_request_body_key():
    assert "putV3StocksWarehouseIdRequest: { ... }" in _examples()["Node.js"]


def test_php_sets_the_host():
    assert "->setHost('https://marketplace-api.wildberries.ru')" in _examples()["PHP"]


def test_rust_sets_the_base_path():
    assert 'config.base_path = "https://marketplace-api.wildberries.ru".to_owned();' \
        in _examples()["Rust"]


def test_go_chains_the_body_builder():
    assert ".PutV3StocksWarehouseIdRequest(...)" in _examples()["Go"]


def test_go_needs_no_base_path_because_the_client_resolves_it():
    go = _examples()["Go"]
    assert "wildberries.ru" not in go


def test_host_line_is_omitted_when_the_spec_declares_no_server():
    examples = _examples(op=_stocks_op(servers=()))
    assert "basePath" not in examples["Node.js"]
    assert "setHost" not in examples["PHP"]
    assert "base_path" not in examples["Rust"]
