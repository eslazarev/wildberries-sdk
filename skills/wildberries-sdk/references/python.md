# Python

```bash
pip install wildberries-sdk
```

Every module ships in the one package; import the one the operation belongs to.

```python
import os
from wildberries_sdk import finances

config = finances.Configuration(api_key={"HeaderApiKey": os.environ["WB_API_TOKEN"]})
api = finances.DefaultApi(finances.ApiClient(config))

balance = api.get_v1_account_balance()
print(balance.data.current)
```

`DefaultApi` holds most operations; a few live in another class (`WBAPIApi`,
`APIApi`). The digest's `python:` line names the class for the operation.

## Host

Nothing to configure: the production host is compiled into each method. Pass
`_host_index=1` to reach the sandbox where the digest shows a `sandbox:` line —
the index is positional, so `1` is always the sandbox and `0` production.

```python
api.get_v1_feedbacks(is_answered=False, take=100, skip=0, _host_index=1)
```

## Errors

```python
from wildberries_sdk.finances.exceptions import ApiException

try:
    api.get_v1_account_balance()
except ApiException as exc:
    # exc.status is the HTTP code, exc.body the raw WB payload
    if exc.status == 429:
        ...  # back off; WB limits are per seller profile
    raise
```

401 and 403 almost always mean the token is from the wrong category, not that
the code is wrong.

## Parameters and responses

Query parameters are snake_case keyword arguments (`is_answered`, `take`,
`skip`); a request body is a typed model or a dict. Responses are pydantic
models, so reach into attributes rather than subscripting.

To see a response as plain data: `result.to_dict()`.

## Request body parameter

Named after the model, never `body`. `body: SalesReportListReq` in the digest
means the keyword is `sales_report_list_req`; `body: object` means WB declared
it inline and the generator named it after the operation, e.g.
`put_v3_stocks_warehouse_id_request`.
