# Wildberries SDK clients for Python, Node.js, Go, PHP and Rust, continuously kept in sync with the official OpenAPI specs.

🌐 [Русский](../../README.md) · **English** · [简体中文](README.zh-CN.md) · [Türkçe](README.tr.md) · [Қазақша](README.kk.md) · [Oʻzbekcha](README.uz.md)

📖 **Documentation:** <https://eslazarev.github.io/wildberries-sdk/> — reference for all Wildberries API operations with examples in Python, Node.js, Go, PHP and Rust.

![using_sdk.gif](../../.github/images/using_wildberries_sdk_python.gif)

| Language | Version | Downloads | README | Registry |
| --- | --- | --- | --- | --- |
| Python | [![PyPI](https://img.shields.io/pypi/v/wildberries-sdk.svg)](https://pypi.org/project/wildberries-sdk/) | [![PyPI Downloads](https://static.pepy.tech/badge/wildberries-sdk)](https://pepy.tech/project/wildberries-sdk) | [docs/python/README.md](../python/README.md) | [pypi.org](https://pypi.org/project/wildberries-sdk/) |
| Node.js | [![npm](https://img.shields.io/npm/v/wildberries-sdk.svg)](https://www.npmjs.com/package/wildberries-sdk) | [![NPM Downloads](https://img.shields.io/npm/dt/wildberries-sdk.svg)](https://www.npmjs.com/package/wildberries-sdk) | [docs/npm/README.md](../npm/README.md) | [npmjs.com](https://www.npmjs.com/package/wildberries-sdk) |
| PHP | [![Packagist](https://img.shields.io/packagist/v/eslazarev/wildberries-sdk.svg)](https://packagist.org/packages/eslazarev/wildberries-sdk) | [![Packagist Downloads](https://img.shields.io/packagist/dt/eslazarev/wildberries-sdk.svg)](https://packagist.org/packages/eslazarev/wildberries-sdk) | [docs/php/README.md](../php/README.md) | [packagist.org](https://packagist.org/packages/eslazarev/wildberries-sdk) |
| Go | [![Go](https://img.shields.io/github/v/tag/eslazarev/wildberries-sdk?label=go)](https://github.com/eslazarev/wildberries-sdk/tags) | — | [docs/go/README.md](../go/README.md) | [pkg.go.dev](https://pkg.go.dev/github.com/eslazarev/wildberries-sdk/clients/go/finances) |
| Rust | [![Rust](https://img.shields.io/github/v/tag/eslazarev/wildberries-sdk?label=rust)](https://github.com/eslazarev/wildberries-sdk/tags) | — | [docs/rust/README.md](../rust/README.md) | [crates.io](https://crates.io/crates/wildberries_sdk_finances) |

## Security

This SDK is built with a security-first release process:

- CodeQL static analysis
- OpenSSF Scorecard
- TruffleHog verified secret scanning
- Python dependency audit (pip-audit)
- npm audit
- Composer audit
- Cargo audit
- Go vulnerability scanning (govulncheck)
- No hardcoded API tokens in the published packages

[![CodeQL](https://github.com/eslazarev/wildberries-sdk/actions/workflows/codeql.yml/badge.svg)](https://github.com/eslazarev/wildberries-sdk/actions/workflows/codeql.yml)
[![Scorecard](https://github.com/eslazarev/wildberries-sdk/actions/workflows/scorecard.yml/badge.svg)](https://github.com/eslazarev/wildberries-sdk/actions/workflows/scorecard.yml)
[![Secrets](https://github.com/eslazarev/wildberries-sdk/actions/workflows/secrets.yml/badge.svg)](https://github.com/eslazarev/wildberries-sdk/actions/workflows/secrets.yml)
[![Dependency Audit](https://github.com/eslazarev/wildberries-sdk/actions/workflows/dependency-audit.yml/badge.svg)](https://github.com/eslazarev/wildberries-sdk/actions/workflows/dependency-audit.yml)


All Wildberries API operations available today are supported, grouped by spec module.

## Why these generated clients

- **Full request/response typing.** Each client uses the language's native type system: pydantic in Python, TypeScript interfaces in Node.js, Go structs, typed PHP classes, serde structs in Rust. Field typos and wrong types are caught at compile/lint time.
- **IDE autocomplete out of the box.** Method names, parameters, model fields and enum values are highlighted and suggested — no need to read the Wildberries documentation while writing code.
- **Descriptions and docstrings from the specs.** Wildberries field- and method-level comments are carried over into the generated code and surface as IDE hover tooltips.
- **Client-side validation.** Required fields and types are checked before the request leaves your process. In Python, pydantic additionally validates formats, enums and min/max constraints; in Go, TypeScript, PHP and Rust the check is limited to required fields and types.
- **One contract across languages.** Operation IDs, model fields and endpoints are identical in Python, Node.js, Go, PHP and Rust — migrating between stacks does not require rewriting business logic.
- **No drift from the upstream specs.** When Wildberries updates the API, the SDK gets the new methods and models in a same-day PR — no need to manually diff the spec.
- **Batteries-included transport layer.** Authentication, headers, base URLs, JSON serialization and HTTP error handling are implemented once in the shared `api_client` / `runtime` / `client` module and reused by every method.

### Clients are kept up to date by GitHub Actions whenever specs change.

Why this matters: see the spec change history in [CHANGELOG.md](../../CHANGELOG.md). Changes happen often — multiple times per week.

## All currently published Wildberries specs are covered

- General — [`specs/01-general.yaml`](../../specs/01-general.yaml)
- Products — [`specs/02-items.yaml`](../../specs/02-items.yaml)
- FBS orders — [`specs/03-orders-fbs.yaml`](../../specs/03-orders-fbs.yaml)
- DBW orders — [`specs/04-orders-dbw.yaml`](../../specs/04-orders-dbw.yaml)
- DBS orders — [`specs/05-orders-dbs.yaml`](../../specs/05-orders-dbs.yaml)
- In-store pickup orders — [`specs/06-in-store-pickup.yaml`](../../specs/06-in-store-pickup.yaml)
- FBW supplies — [`specs/07-orders-fbw.yaml`](../../specs/07-orders-fbw.yaml)
- Marketing and promotion — [`specs/08-promotion.yaml`](../../specs/08-promotion.yaml)
- Buyer communications — [`specs/09-communications.yaml`](../../specs/09-communications.yaml)
- Tariffs — [`specs/10-tariffs.yaml`](../../specs/10-tariffs.yaml)
- Analytics — [`specs/11-analytics.yaml`](../../specs/11-analytics.yaml)
- Reports — [`specs/12-reports.yaml`](../../specs/12-reports.yaml)
- Finances and accounting — [`specs/13-finances.yaml`](../../specs/13-finances.yaml)
- Wildberries Digital — [`specs/14-wbd.yaml`](../../specs/14-wbd.yaml)

The full per-method listing (descriptions are taken verbatim from Wildberries OpenAPI specs in Russian) is in the [main Russian README](../../README.md#в-данный-момент-представлены-все-доступные-спецификации).
