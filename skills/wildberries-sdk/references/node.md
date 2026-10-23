# Node.js / TypeScript

```bash
npm install wildberries-sdk
```

```ts
import { Configuration, DefaultApi } from 'wildberries-sdk';

const api = new DefaultApi(new Configuration({
  basePath: 'https://finance-api.wildberries.ru',   // required — see below
  apiKey: process.env.WB_API_TOKEN!,
}));

const balance = await api.getV1AccountBalance();
```

## Host: you must set it

The generated runtime defaults `basePath` to `http://localhost`, and unlike the
Python and Go clients it does not know the per-operation host. Always pass
`basePath` from the digest's `host:` line for that operation (or its `sandbox:`
line), otherwise the request silently goes nowhere.

Operations in one module can live on different hosts — `communications` spans
feedbacks, chat and returns — so build one client per host, not one per module.

## Errors

Rejected requests throw `ResponseError` with the original `response`:

```ts
import { ResponseError } from 'wildberries-sdk';

try {
  await api.getV1AccountBalance();
} catch (err) {
  if (err instanceof ResponseError && err.response.status === 429) {
    // back off
  }
  throw err;
}
```

## Shapes

Methods are camelCase (`getV1Feedbacks`), take a single object argument when
they have parameters, and return parsed JSON typed by the generated models.
The `…Raw` variant of each method returns the `Response` when the headers
matter.

## Request body parameter

Everything goes in one object argument, and the body key is named after the
model rather than `body`: `{ warehouseId, putV3StocksWarehouseIdRequest: {...} }`
for an inline body, `{ salesReportListReq: {...} }` when the digest names a
model. WB does not validate field names on several write methods — it answers
`204` and changes nothing — so a wrong key fails silently.
