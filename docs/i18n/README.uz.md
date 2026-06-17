# Python, Node.js, Go, PHP va Rust uchun Wildberries SDK mijozlari — rasmiy OpenAPI spetsifikatsiyalari bilan doimiy sinxronlashtirilgan.

🌐 [Русский](../../README.md) · [English](README.en.md) · [简体中文](README.zh-CN.md) · [Türkçe](README.tr.md) · [Қазақша](README.kk.md) · **Oʻzbekcha**

📖 **Hujjatlar:** <https://eslazarev.github.io/wildberries-sdk/> — barcha Wildberries API operatsiyalari uchun Python, Node.js, Go, PHP va Rust misollari bilan ma'lumotnoma.

![using_sdk.gif](../../.github/images/using_wildberries_sdk_python.gif)

| Til | Versiya | Yuklab olishlar | README | Reestr |
| --- | --- | --- | --- | --- |
| Python | [![PyPI](https://img.shields.io/pypi/v/wildberries-sdk.svg)](https://pypi.org/project/wildberries-sdk/) | [![PyPI Downloads](https://static.pepy.tech/badge/wildberries-sdk)](https://pepy.tech/project/wildberries-sdk) | [docs/python/README.md](../python/README.md) | [pypi.org](https://pypi.org/project/wildberries-sdk/) |
| Node.js | [![npm](https://img.shields.io/npm/v/wildberries-sdk.svg)](https://www.npmjs.com/package/wildberries-sdk) | [![NPM Downloads](https://img.shields.io/npm/dt/wildberries-sdk.svg)](https://www.npmjs.com/package/wildberries-sdk) | [docs/npm/README.md](../npm/README.md) | [npmjs.com](https://www.npmjs.com/package/wildberries-sdk) |
| PHP | [![Packagist](https://img.shields.io/packagist/v/eslazarev/wildberries-sdk.svg)](https://packagist.org/packages/eslazarev/wildberries-sdk) | [![Packagist Downloads](https://img.shields.io/packagist/dt/eslazarev/wildberries-sdk.svg)](https://packagist.org/packages/eslazarev/wildberries-sdk) | [docs/php/README.md](../php/README.md) | [packagist.org](https://packagist.org/packages/eslazarev/wildberries-sdk) |
| Go | [![Go](https://img.shields.io/github/v/tag/eslazarev/wildberries-sdk?label=go)](https://github.com/eslazarev/wildberries-sdk/tags) | — | [docs/go/README.md](../go/README.md) | [pkg.go.dev](https://pkg.go.dev/github.com/eslazarev/wildberries-sdk/clients/go/finances) |
| Rust | [![Rust](https://img.shields.io/github/v/tag/eslazarev/wildberries-sdk?label=rust)](https://github.com/eslazarev/wildberries-sdk/tags) | — | [docs/rust/README.md](../rust/README.md) | [crates.io](https://crates.io/crates/wildberries_sdk_finances) |

## Xavfsizlik

Ushbu SDK xavfsizlik birinchi oʻrinda boʻlgan reliz jarayoni bilan chiqariladi:

- CodeQL statik kod tahlili
- OpenSSF Scorecard bahosi
- TruffleHog tasdiqlangan sirlarni skanerlash
- Python bogʻliqliklarini tekshirish (pip-audit)
- npm audit
- Composer audit
- Cargo audit
- Go zaifliklarini tekshirish (govulncheck)
- Eʼlon qilingan paketlarda qattiq kodlangan API tokenlari yoʻq

[![CodeQL](https://github.com/eslazarev/wildberries-sdk/actions/workflows/codeql.yml/badge.svg)](https://github.com/eslazarev/wildberries-sdk/actions/workflows/codeql.yml)
[![Scorecard](https://github.com/eslazarev/wildberries-sdk/actions/workflows/scorecard.yml/badge.svg)](https://github.com/eslazarev/wildberries-sdk/actions/workflows/scorecard.yml)
[![Secrets](https://github.com/eslazarev/wildberries-sdk/actions/workflows/secrets.yml/badge.svg)](https://github.com/eslazarev/wildberries-sdk/actions/workflows/secrets.yml)
[![Dependency Audit](https://github.com/eslazarev/wildberries-sdk/actions/workflows/dependency-audit.yml/badge.svg)](https://github.com/eslazarev/wildberries-sdk/actions/workflows/dependency-audit.yml)


Wildberries API ning bugun mavjud boʻlgan barcha buyruqlari spetsifikatsiya modullari boʻyicha guruhlangan holda qoʻllab-quvvatlanadi.

## Avtomatik yaratiladigan mijozlarning afzalliklari

- **Soʻrov/javobning toʻliq tiplanishi.** Har bir tildagi mijoz oʻzining mahalliy tiplar tizimidan foydalanadi: Python’da pydantic, Node.js’da TypeScript interfeyslari, Go’da struct, PHP’da tiplangan klasslar, Rust’da serde tuzilmalari. Maydon nomidagi xatolar va notoʻgʻri tiplar kompilyatsiya/lint bosqichida aniqlanadi.
- **IDE-da avtotoʻldirish darhol ishlaydi.** Metod nomlari, parametrlar, model maydonlari va enum qiymatlari belgilanadi va tavsiya etiladi — Wildberries hujjatlarini oʻqishga hojat yoʻq.
- **Spetsifikatsiyalardan tavsiflar va docstring’lar.** Wildberries’ning YAML’dagi maydon/metod izohlari yaratilgan kodga koʻchiriladi va IDE’da hover orqali koʻrinadi.
- **Mijoz tomonida tekshirish.** Majburiy maydonlar va tiplar soʻrov yuborilishidan oldin tekshiriladi (Python pydantic formatlarni, enum’larni va min/max cheklovlarini ham tekshiradi; Go/TypeScript/PHP/Rust’da tekshirish majburiy maydonlar va tiplar bilan cheklanadi).
- **Barcha tillar uchun yagona kontrakt.** Operatsiya ID’lari, model maydonlari va endpoint’lar Python, Node.js, Go, PHP va Rust’da bir xil — stack’lar oʻrtasida koʻchish biznes-mantiqni qayta yozishni talab qilmaydi.
- **Spetsifikatsiyalardan ogʻishlik yoʻq.** Wildberries API’ni yangilaganda SDK oʻsha kuni yangi metod va modellarga ega PR oladi — spec diff’ni qoʻlda hisoblashning hojati yoʻq.
- **Tayyor transport qatlami.** Autentifikatsiya, sarlavhalar, asosiy URL’lar, JSON serializatsiyasi va HTTP xatoliklarini boshqarish umumiy `api_client` / `runtime` / `client` modulida bir marta amalga oshirilgan va barcha metodlar tomonidan qayta ishlatiladi.

### Spetsifikatsiya oʻzgarganda mijozlar GitHub Actions tomonidan avtomatik tarzda yangilanib turiladi.

Bu nima uchun muhim — spetsifikatsiya oʻzgarishlari tarixini koʻring: [CHANGELOG.md](../../CHANGELOG.md). Odatda haftada bir necha marta oʻzgaradi.

## Eʼlon qilingan barcha Wildberries spetsifikatsiyalari qamrab olingan

- Umumiy — [`specs/01-general.yaml`](../../specs/01-general.yaml)
- Tovarlar bilan ishlash — [`specs/02-items.yaml`](../../specs/02-items.yaml)
- FBS buyurtmalari — [`specs/03-orders-fbs.yaml`](../../specs/03-orders-fbs.yaml)
- DBW buyurtmalari — [`specs/04-orders-dbw.yaml`](../../specs/04-orders-dbw.yaml)
- DBS buyurtmalari — [`specs/05-orders-dbs.yaml`](../../specs/05-orders-dbs.yaml)
- Doʻkondan olib ketish — [`specs/06-in-store-pickup.yaml`](../../specs/06-in-store-pickup.yaml)
- FBW yetkazib berishlari — [`specs/07-orders-fbw.yaml`](../../specs/07-orders-fbw.yaml)
- Marketing va reklama — [`specs/08-promotion.yaml`](../../specs/08-promotion.yaml)
- Xaridorlar bilan muloqot — [`specs/09-communications.yaml`](../../specs/09-communications.yaml)
- Tariflar — [`specs/10-tariffs.yaml`](../../specs/10-tariffs.yaml)
- Tahlil — [`specs/11-analytics.yaml`](../../specs/11-analytics.yaml)
- Hisobotlar — [`specs/12-reports.yaml`](../../specs/12-reports.yaml)
- Moliya va buxgalteriya — [`specs/13-finances.yaml`](../../specs/13-finances.yaml)
- Wildberries Raqamli — [`specs/14-wbd.yaml`](../../specs/14-wbd.yaml)

Har bir metodning toʻliq roʻyxati (tavsiflar Wildberries OpenAPI spetsifikatsiyalaridan rus tilida olingan) [asosiy README](../../README.md#в-данный-момент-представлены-все-доступные-спецификации)’da.
