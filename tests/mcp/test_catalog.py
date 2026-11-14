"""The MCP catalog against the specs: every operation, found and described right.

No operation count or name is frozen here: both come from specs/ and src/ at run
time, so the tests keep holding after the next spec update.
"""
from pathlib import Path

import pytest

from docsgen.render import operation_slug
from docsgen.specs import load_operations
from wildberries_mcp.catalog import Catalog, current_modules

ROOT = Path(__file__).resolve().parents[2]
SDK = ROOT / "src" / "wildberries_sdk"


@pytest.fixture(scope="module")
def catalog():
    return Catalog.from_sdk(str(SDK))


@pytest.fixture(scope="module")
def spec_ops():
    return load_operations(str(ROOT / "specs"))


def test_catalog_holds_exactly_the_operations_of_current_modules(catalog, spec_ops):
    modules = set(current_modules(str(SDK)))
    expected = {(op.module, op.verb, op.path) for op in spec_ops if op.module in modules}
    assert {(op.module, op.verb, op.path) for op in catalog.operations} == expected


def test_retired_modules_are_left_out(catalog):
    versions = {}
    for init in SDK.glob("*/__init__.py"):
        for line in init.read_text(encoding="utf-8").splitlines():
            if line.startswith("__version__ ="):
                versions[init.parent.name] = line.split('"')[1]
    stale = {m for m, v in versions.items() if v != max(versions.values(), key=lambda s: tuple(map(int, s.split("."))))}
    assert stale, "expected at least one retired module still in src/"
    assert not stale & set(catalog.modules)


def test_ids_are_unique_and_operations_complete(catalog):
    assert len(catalog.by_id) == len(catalog.operations)
    for op in catalog.operations:
        assert op.id == f"{op.module}.{op.method}"
        assert op.summary and op.api_class
        assert op.verb in {"GET", "POST", "PUT", "PATCH", "DELETE"}


def test_parameters_keep_the_wire_names_from_the_specs(catalog, spec_ops):
    by_key = {(op.module, op.verb, op.path): op for op in catalog.operations}
    for spec_op in spec_ops:
        op = by_key.get((spec_op.module, spec_op.verb, spec_op.path))
        if op is None:
            continue
        wire = {p.wire_name for p in op.params if p.location in ("path", "query")}
        spec = {p.name for p in spec_op.params if p.location in ("path", "query")}
        assert spec <= wire, op.id


def test_docs_url_points_at_the_reference_page(catalog, spec_ops):
    for spec_op in spec_ops[:50]:
        found = [op for op in catalog.operations
                 if (op.module, op.verb, op.path) == (spec_op.module, spec_op.verb, spec_op.path)]
        for op in found:
            assert op.docs_url.endswith(f"/reference/{op.module}/{operation_slug(spec_op)}/")


def test_search_finds_an_operation_by_its_own_summary_path_and_method(catalog):
    for op in catalog.operations[::25]:
        for query in (op.summary, op.path, op.method):
            assert op in catalog.search(query, limit=10), (query, op.id)


def test_search_matches_russian_word_forms(catalog):
    op = next(o for o in catalog.operations if "отзыв" in o.summary.lower())
    module_ops = catalog.search("отзывов", module=op.module, limit=50)
    assert any("отзыв" in o.summary.lower() for o in module_ops)
    assert all(o.module == op.module for o in module_ops)


def _op(method, path, summary, description="", module="m"):
    from wildberries_mcp.catalog import Operation
    return Operation(id=f"{module}.{method}", module=module, api_class="DefaultApi",
                     method=method, verb="GET", path=path, summary=summary,
                     description=description)


def test_search_matches_words_not_letters_inside_them():
    ping = _op("get_ping", "/ping", "Проверка подключения")
    shipping = _op("get_v3_shipping_points", "/api/v3/shipping-points",
                   "Пункты отгрузки", "Shipping points of a supply")
    found = Catalog([shipping, ping]).search("ping")
    assert found == [ping]


def test_search_bridges_russian_words_and_english_paths():
    feedbacks = _op("get_v1_feedbacks_count_unanswered", "/api/v1/feedbacks/count-unanswered",
                    "Необработанные отзывы")
    questions = _op("get_v1_questions_count_unanswered", "/api/v1/questions/count-unanswered",
                    "Неотвеченные вопросы")
    stocks = _op("post_v3_stocks", "/api/v3/stocks/{warehouseId}", "Получить список товаров")
    catalog = Catalog([questions, feedbacks, stocks])
    assert catalog.search("неотвеченные отзывы")[0] is feedbacks
    assert catalog.search("остатки на складе")[0] is stocks


def test_search_by_part_of_a_path():
    deep = _op("get_v3_orders_new", "/api/v3/orders/new", "Новые сборочные задания")
    other = _op("get_v3_orders", "/api/v3/orders", "Сборочные задания")
    assert Catalog([other, deep]).search("/api/v3/orders/new")[0] is deep
    assert {op.id for op in Catalog([other, deep]).search("/api/v3/orders")} == {deep.id, other.id}
