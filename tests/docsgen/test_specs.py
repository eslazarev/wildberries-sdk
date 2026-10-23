import glob

from docsgen.specs import load_operations, module_from_filename

SPECS = "specs"


def test_module_from_filename():
    assert module_from_filename("specs/13-finances.yaml") == "finances"
    assert module_from_filename("specs/06-in-store-pickup.yaml") == "in_store_pickup"


def test_every_spec_file_contributes_operations():
    # Wildberries adds and removes operations weekly, so a frozen total only
    # ages. What must hold is that no spec file silently stops parsing.
    expected = {module_from_filename(path) for path in glob.glob(f"{SPECS}/*.yaml")}
    assert {op.module for op in load_operations(SPECS)} == expected


def test_operations_are_unique_and_well_formed():
    ops = load_operations(SPECS)
    assert ops
    keys = [(op.module, op.verb, op.path) for op in ops]
    assert len(keys) == len(set(keys))
    assert all(op.verb.isupper() for op in ops)
    assert all(op.path.startswith("/") for op in ops)


def test_load_operations_finds_known_finances_op():
    fin = [o for o in load_operations(SPECS) if o.module == "finances"]
    assert fin

    balance = next(o for o in fin if o.path == "/api/v1/account/balance")
    assert balance.verb == "GET"
    assert balance.summary == "Получить баланс продавца"

    sales = next(o for o in fin if o.path == "/api/finance/v1/sales-reports/list")
    assert sales.verb == "POST"
    assert sales.request_model == "SalesReportListReq"


def test_parameters_carry_their_location_and_requiredness():
    params = [p for op in load_operations(SPECS) for p in op.params]
    assert params
    assert {p.location for p in params} <= {"query", "path", "header", "cookie"}
    assert all(isinstance(p.required, bool) for p in params)


def test_parameters_declared_by_reference_are_resolved():
    # specs/02-items.yaml writes this one as {"$ref": "#/components/parameters/uploadID"}.
    op = next(o for o in load_operations(SPECS)
              if o.module == "items" and o.path == "/api/v2/history/tasks")
    upload = next(p for p in op.params if p.name == "uploadID")
    assert upload.location == "query"
    assert upload.required is True
    assert upload.type == "integer"
    assert upload.description


def test_operations_carry_the_wb_host_from_the_spec():
    # specs put the servers on the path item: production first, sandbox second.
    ops = load_operations(SPECS)
    balance = next(o for o in ops if o.module == "finances"
                   and o.path == "/api/v1/account/balance")
    assert balance.servers == ["https://finance-api.wildberries.ru"]

    cards = next(o for o in ops if o.module == "items"
                 and o.path == "/content/v2/object/parent/all")
    assert cards.servers[0] == "https://content-api.wildberries.ru"
    assert "sandbox" in cards.servers[1]


def test_every_operation_knows_where_to_send_the_request():
    ops = load_operations(SPECS)
    hostless = [f"{o.module} {o.verb} {o.path}" for o in ops if not o.servers]
    assert not hostless, hostless[:5]
