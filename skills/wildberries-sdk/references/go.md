# Go

One module per API area:

```bash
go get github.com/eslazarev/wildberries-sdk/clients/go/finances
```

```go
import (
    "context"
    "os"

    finances "github.com/eslazarev/wildberries-sdk/clients/go/finances"
)

client := finances.NewAPIClient(finances.NewConfiguration())

ctx := context.WithValue(context.Background(), finances.ContextAPIKeys,
    map[string]finances.APIKey{"HeaderApiKey": {Key: os.Getenv("WB_API_TOKEN")}})

balance, resp, err := client.DefaultApi.GetV1AccountBalance(ctx).Execute()
```

The service field matches the digest's `go:` line — usually `DefaultApi`,
sometimes `WBAPIAPI` or `APIAPI`.

## Host

Already handled: the generated `OperationServers` map pins each operation to
its WB host. Leave `cfg.Servers` alone. For the sandbox, pass an operation
server index:

```go
ctx = context.WithValue(ctx, finances.ContextOperationServerIndices,
    map[string]int{"DefaultApiService.GetV1AccountBalance": 1})
```

## Errors

`err` is a `*GenericOpenAPIError`; `resp` is the raw `*http.Response`, so check
`resp.StatusCode` for 429 and back off. `err.Body()` returns WB's payload,
which usually explains a 400 better than the typed model does.

## Builder calls

Parameters are chained before `Execute()`:

```go
feedbacks, _, err := client.DefaultApi.GetV1Feedbacks(ctx).
    IsAnswered(false).Take(100).Skip(0).Execute()
```

## Request body parameter

A builder method named after the model:
`.PutV3StocksWarehouseIdRequest(body)` for an inline body,
`.SalesReportListReq(body)` when the digest names a model, then `.Execute()`.
