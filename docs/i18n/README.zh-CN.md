# Wildberries SDK 客户端 — Python、Node.js、Go、PHP、Rust，与官方 OpenAPI 规范持续保持同步。

🌐 [Русский](../../README.md) · [English](README.en.md) · **简体中文** · [Türkçe](README.tr.md) · [Қазақша](README.kk.md) · [Oʻzbekcha](README.uz.md)

📖 **文档：** <https://eslazarev.github.io/wildberries-sdk/> — 涵盖所有 Wildberries API 操作的参考手册，附 Python、Node.js、Go、PHP 和 Rust 示例。

![using_sdk.gif](../../.github/images/using_wildberries_sdk_python.gif)

| 语言 | 版本 | 下载量 | README | 注册表 |
| --- | --- | --- | --- | --- |
| Python | [![PyPI](https://img.shields.io/pypi/v/wildberries-sdk.svg)](https://pypi.org/project/wildberries-sdk/) | [![PyPI Downloads](https://static.pepy.tech/badge/wildberries-sdk)](https://pepy.tech/project/wildberries-sdk) | [docs/python/README.md](../python/README.md) | [pypi.org](https://pypi.org/project/wildberries-sdk/) |
| Node.js | [![npm](https://img.shields.io/npm/v/wildberries-sdk.svg)](https://www.npmjs.com/package/wildberries-sdk) | [![NPM Downloads](https://img.shields.io/npm/dt/wildberries-sdk.svg)](https://www.npmjs.com/package/wildberries-sdk) | [docs/npm/README.md](../npm/README.md) | [npmjs.com](https://www.npmjs.com/package/wildberries-sdk) |
| PHP | [![Packagist](https://img.shields.io/packagist/v/eslazarev/wildberries-sdk.svg)](https://packagist.org/packages/eslazarev/wildberries-sdk) | [![Packagist Downloads](https://img.shields.io/packagist/dt/eslazarev/wildberries-sdk.svg)](https://packagist.org/packages/eslazarev/wildberries-sdk) | [docs/php/README.md](../php/README.md) | [packagist.org](https://packagist.org/packages/eslazarev/wildberries-sdk) |
| Go | [![Go](https://img.shields.io/github/v/tag/eslazarev/wildberries-sdk?label=go)](https://github.com/eslazarev/wildberries-sdk/tags) | — | [docs/go/README.md](../go/README.md) | [pkg.go.dev](https://pkg.go.dev/github.com/eslazarev/wildberries-sdk/clients/go/finances) |
| Rust | [![Rust](https://img.shields.io/github/v/tag/eslazarev/wildberries-sdk?label=rust)](https://github.com/eslazarev/wildberries-sdk/tags) | — | [docs/rust/README.md](../rust/README.md) | [crates.io](https://crates.io/crates/wildberries_sdk_finances) |

## 安全

本 SDK 采用安全优先的发布流程：

- CodeQL 静态代码分析
- OpenSSF Scorecard 评分
- TruffleHog 已验证密钥扫描
- Python 依赖审计 (pip-audit)
- npm audit
- Composer audit
- Cargo audit
- Go 漏洞扫描 (govulncheck)
- 发布的包中不包含硬编码的 API 令牌

[![CodeQL](https://github.com/eslazarev/wildberries-sdk/actions/workflows/codeql.yml/badge.svg)](https://github.com/eslazarev/wildberries-sdk/actions/workflows/codeql.yml)
[![Scorecard](https://github.com/eslazarev/wildberries-sdk/actions/workflows/scorecard.yml/badge.svg)](https://github.com/eslazarev/wildberries-sdk/actions/workflows/scorecard.yml)
[![Secrets](https://github.com/eslazarev/wildberries-sdk/actions/workflows/secrets.yml/badge.svg)](https://github.com/eslazarev/wildberries-sdk/actions/workflows/secrets.yml)
[![Dependency Audit](https://github.com/eslazarev/wildberries-sdk/actions/workflows/dependency-audit.yml/badge.svg)](https://github.com/eslazarev/wildberries-sdk/actions/workflows/dependency-audit.yml)


本仓库覆盖目前公开的全部 Wildberries API 命令,按规范模块组织。

## 为什么使用自动生成的客户端

- **完整的请求/响应类型。** 每种语言客户端使用其原生类型系统:Python 的 pydantic、Node.js 的 TypeScript 接口、Go 的 struct、PHP 的强类型类、Rust 的 serde 结构体。字段拼写错误和类型错误在编译/lint 阶段就会暴露。
- **IDE 自动补全开箱即用。** 方法名、参数、模型字段和枚举值都会被高亮和提示,无需查阅 Wildberries 文档。
- **规范中的描述和 docstring 自动同步。** Wildberries 在 YAML 中对字段和方法的中文/俄文说明被搬入生成的代码,在 IDE 中悬停可见。
- **客户端校验。** 必填字段和类型在请求发出前就会被检查(Python 的 pydantic 还会校验格式、枚举和 min/max 约束;Go、TypeScript、PHP、Rust 仅校验必填字段和类型)。
- **跨语言统一契约。** 操作 ID、模型字段和端点在 Python、Node.js、Go、PHP 和 Rust 之间完全一致 — 跨技术栈迁移不需要改写业务逻辑。
- **永远不偏离官方规范。** Wildberries 一旦更新 API,SDK 会在当天通过 PR 拿到新的方法和模型 — 无需手动 diff 规范。
- **开箱即用的传输层。** 认证、HTTP 头、base URL、JSON 序列化和 HTTP 错误处理在共享的 `api_client` / `runtime` / `client` 模块中实现一次,所有方法复用。

### 客户端通过 GitHub Actions 在规范变更时自动保持最新。

为什么这点重要 — 看规范变更历史:[CHANGELOG.md](../../CHANGELOG.md)。一周通常会有多次变更。

## 目前覆盖的全部 Wildberries 规范

- 通用 — [`specs/01-general.yaml`](../../specs/01-general.yaml)
- 商品管理 — [`specs/02-items.yaml`](../../specs/02-items.yaml)
- FBS 订单 — [`specs/03-orders-fbs.yaml`](../../specs/03-orders-fbs.yaml)
- DBW 订单 — [`specs/04-orders-dbw.yaml`](../../specs/04-orders-dbw.yaml)
- DBS 订单 — [`specs/05-orders-dbs.yaml`](../../specs/05-orders-dbs.yaml)
- 自提订单 — [`specs/06-in-store-pickup.yaml`](../../specs/06-in-store-pickup.yaml)
- FBW 入库 — [`specs/07-orders-fbw.yaml`](../../specs/07-orders-fbw.yaml)
- 营销和推广 — [`specs/08-promotion.yaml`](../../specs/08-promotion.yaml)
- 买家沟通 — [`specs/09-communications.yaml`](../../specs/09-communications.yaml)
- 资费 — [`specs/10-tariffs.yaml`](../../specs/10-tariffs.yaml)
- 分析 — [`specs/11-analytics.yaml`](../../specs/11-analytics.yaml)
- 报表 — [`specs/12-reports.yaml`](../../specs/12-reports.yaml)
- 财务和会计 — [`specs/13-finances.yaml`](../../specs/13-finances.yaml)
- Wildberries Digital — [`specs/14-wbd.yaml`](../../specs/14-wbd.yaml)

完整的方法清单(描述直接来自 Wildberries OpenAPI 规范的俄文原文)在 [主 README](../../README.md#в-данный-момент-представлены-все-доступные-спецификации) 中。
