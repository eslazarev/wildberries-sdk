---
name: wildberries-sdk
description: Call the Wildberries (WB, Вайлдберриз) seller API from Python, Node.js, Go, PHP or Rust with the generated wildberries-sdk clients — finding the right operation, module, token category and host instead of guessing method names or hand-rolling HTTP. Use this for any task touching the Wildberries marketplace API: product cards and characteristics (карточки товаров), stocks and prices (остатки, цены, скидки), FBS/FBW/DBS and in-store-pickup orders (сборочные задания, поставки, ярлыки), promotions and ads (реклама, кампании, ставки), buyer feedback and questions (отзывы, вопросы, чат с покупателем), tariffs, analytics, reports, finances and documents (финансы, отчёты, документы). Trigger it even when the user never names the SDK and just says something like "вытащи неотвеченные отзывы с ВБ", "обнови остатки на маркетплейсе" or "pull yesterday's WB orders into a CSV".
---

# Wildberries SDK

The Wildberries seller API is ~350 operations spread across a dozen hosts, each
guarded by a different token category. The `wildberries-sdk` clients generate a
typed method for every one of those operations in five languages, from the
official OpenAPI specs, republished within a day of any spec change.

Working with it well is mostly about two things: finding the right operation,
and getting auth right. Guessing method names does not work — they are
generated from the HTTP route, not from the human name of the action.

## 1. Find the operation first

Never invent a method name. Search the digest of all operations, which lists
each one with its route, required parameters and the exact method name in all
five clients:

```bash
python scripts/find_operation.py "остатки"            # search by meaning, RU or EN
python scripts/find_operation.py "/api/v3/orders"     # or by route
python scripts/find_operation.py "отзыв" --lang python
```

The script reads <https://eslazarev.github.io/wildberries-sdk/llms-full.txt>
and caches it for a day. Each hit looks like this:

```
### Обновить остатки товаров
route: PUT /api/v3/stocks/{warehouseId}
host: https://marketplace-api.wildberries.ru
sandbox: https://marketplace-api-sandbox.wildberries.ru
required: warehouseId
body: object — python put_v3_stocks_warehouse_id_request, node putV3StocksWarehouseIdRequest, go .PutV3StocksWarehouseIdRequest()
python: wildberries_sdk.items.DefaultApi.put_v3_stocks_warehouse_id(warehouse_id, put_v3_stocks_warehouse_id_request)
node: DefaultApi.putV3StocksWarehouseId
go: client.DefaultApi.PutV3StocksWarehouseId
php: Wildberries\Sdk\Items\Api\DefaultApi::putV3StocksWarehouseId
rust: wildberries_sdk_items::apis::default_api::put_v3_stocks_warehouse_id
docs: https://eslazarev.github.io/wildberries-sdk/reference/items/put_api_v3_stocks_warehouseid/
```

The `docs:` page carries the full WB description, every parameter, and a
runnable example in each language. Open it whenever the one-line summary is not
enough — in particular, it is where WB states **which token category** the
method needs.

If the search returns nothing, widen it (a single Russian stem like `постав`
beats a whole phrase), or browse the module list in `references/modules.md`.

## 2. Pick the module, then install only it

The API is split into modules that mirror the specs: `items`, `orders_fbs`,
`orders_fbw`, `orders_dbw`, `orders_dbs`, `dbs`, `in_store_pickup`,
`promotion`, `communications`, `rates`, `analytics`, `reports`, `finances`,
`general`, `wbd`. The operation's `python:` line names its module.

`references/modules.md` says what lives in each one and which WB host it talks
to. Install per language:

| Language | Install | Import |
| --- | --- | --- |
| Python | `pip install wildberries-sdk` | `from wildberries_sdk import finances` |
| Node.js | `npm install wildberries-sdk` | `import { DefaultApi } from 'wildberries-sdk'` |
| Go | `go get github.com/eslazarev/wildberries-sdk/clients/go/finances` | one module per area |
| PHP | `composer require eslazarev/wildberries-sdk` | `Wildberries\Sdk\Finances\...` |
| Rust | `cargo add wildberries_sdk_finances` | one crate per area |

Python and Node ship every module in one package; Go and Rust publish one
module or crate per area, so install the one the operation belongs to.

## 3. Auth: the token comes from the caller

Every method authenticates with a seller API token sent in the `Authorization`
header. Read it from the environment (`WB_API_TOKEN` is the convention in the
SDK's own examples) or from whatever secret store the project already uses, and
never hardcode it or echo it back to the user — it grants full access to a
seller's account.

```python
import os
from wildberries_sdk import finances

api = finances.DefaultApi(
    finances.ApiClient(
        finances.Configuration(api_key={"HeaderApiKey": os.environ["WB_API_TOKEN"]})
    )
)
balance = api.get_v1_account_balance()
```

The other four languages differ only in syntax — see `references/<language>.md`
for the exact client construction, error type and async story.

WB issues tokens **per category** (Контент, Маркетплейс, Статистика,
Продвижение, Вопросы и отзывы, Цены и скидки, Аналитика, Поставки, Финансы,
Возвраты…), plus a distinction between a personal and a service token. A token
from the wrong category returns 401 or 403 no matter how correct the call is,
so when a request is rejected, check the category on the operation's `docs:`
page before debugging the code.

## 4. The host is per operation, and three clients need it spelled out

WB spreads its API over a dozen domains — `content-api`, `marketplace-api`,
`advert-api`, `finance-api` and so on — and the host belongs to the operation,
not to the module. The digest's `host:` line gives it.

| Client | Host |
| --- | --- |
| Python | compiled into each method; leave it alone |
| Go | resolved from the generated `OperationServers` map; leave it alone |
| Node.js | **must be set** — the runtime defaults to `http://localhost` |
| PHP | **must be set** via `setHost()` — same default |
| Rust | **must be set** via `configuration.base_path` — same default |

For Node, PHP and Rust, a call written without the base URL does not fail
loudly with "wrong host" — it tries localhost and dies with a connection
error, which reads like a network problem and sends people debugging the wrong
thing. Set it from the `host:` line every time.

Because the host follows the operation rather than the module, one module can
span several services: `communications` covers feedbacks, buyer chat and
returns on three different domains. Build one client per host.

Where the digest shows a `sandbox:` line, that environment exists. Use it
whenever a task would otherwise write real data — creating orders, changing
prices, answering buyers — and the user has not explicitly said to act on
production. In Python pass `_host_index=1`; elsewhere point the base URL at the
sandbox host.

## 5. Naming: parameters and the request body

Do not derive these from the spec — the digest carries the real ones, read out
of the published clients.

The `python:` line ends with the call signature, in the client's own spelling:
the spec's `isAnswered` is `is_answered` there, and passing the spec's name
raises `TypeError`.

The `body:` line names the body parameter per language, because it is never
called `body`: the generator names it after the model, inventing one from the
operation id when WB declares the body inline. Node and Go take it as
`putV3StocksWarehouseIdRequest` and `.PutV3StocksWarehouseIdRequest(...)`
respectively; PHP and Rust take it positionally.

Passing the payload under a guessed key is quietly dangerous on WB: several
write methods do not validate field names and answer `204` while changing
nothing. If a write "succeeds" and nothing moved, suspect the key before the
logic, and read the state back to confirm.

## 6. Writing code that survives the next release

- **The clients are generated.** Never patch anything under a client's package
  to work around a bug; the next spec change overwrites it. Report the problem
  against the spec instead.
- **Operations appear and disappear weekly.** Pin a version in production code,
  and re-run the search rather than trusting a method name from memory.
- **Rate limits are per seller profile and per method group.** WB answers 429
  with a retry window; back off and retry rather than tightening a loop.
- **Pagination is explicit.** Most list methods take `limit`/`skip` or a cursor
  in the request body — the operation page shows which, and the digest's
  `required:` line shows what must be passed.
- **Responses are typed models**, not dicts. Reach into attributes
  (`result.data.feedbacks`), and let the IDE or compiler catch field renames.

## Reference files

Read these when the task needs them, not upfront:

- `references/modules.md` — what each of the 15 modules covers and its WB host
- `references/python.md`, `references/node.md`, `references/go.md`,
  `references/php.md`, `references/rust.md` — client construction, errors,
  pagination and sandbox switching in that language
- The docs site <https://eslazarev.github.io/wildberries-sdk/> — the full
  reference, one page per operation
