# Rust

One crate per API area:

```bash
cargo add wildberries_sdk_finances
```

```rust
use wildberries_sdk_finances::apis::configuration::{ApiKey, Configuration};
use wildberries_sdk_finances::apis::default_api;

let mut configuration = Configuration::new();
configuration.base_path = "https://finance-api.wildberries.ru".to_owned(); // required
configuration.api_key = Some(ApiKey {
    prefix: None,
    key: std::env::var("WB_API_TOKEN")?,
});

let balance = default_api::get_v1_account_balance(&configuration).await?;
```

The module path is on the digest's `rust:` line — `default_api` for most
operations, `wbapi_api` and friends for the rest.

## Host: you must set it

`Configuration::new()` leaves `base_path` at `http://localhost`, and the
generated functions interpolate it directly. Set it from the digest's `host:`
line (or `sandbox:`) before the first call.

## Errors

Functions return `Result<T, Error<SomeOperationError>>`. `Error::ResponseContent`
carries the status and body, so match on it for 429 and back off; the typed
`entity` holds WB's error model when it parsed.

## Async

The clients are `reqwest`-based and async — every call is `.await`, so the
caller needs a tokio runtime.
