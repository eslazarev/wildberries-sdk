# Python, Node.js, Go, PHP және Rust үшін Wildberries SDK клиенттері — ресми OpenAPI спецификацияларымен үнемі синхрондалған.

🌐 [Русский](../../README.md) · [English](README.en.md) · [简体中文](README.zh-CN.md) · [Türkçe](README.tr.md) · **Қазақша** · [Oʻzbekcha](README.uz.md)

📖 **Құжаттама:** <https://eslazarev.github.io/wildberries-sdk/> — барлық Wildberries API операциялары бойынша Python, Node.js, Go, PHP және Rust мысалдарымен анықтамалық.

![using_sdk.gif](../../.github/images/using_wildberries_sdk_python.gif)

| Тіл | Нұсқасы | Жүктеулер | README | Реестр |
| --- | --- | --- | --- | --- |
| Python | [![PyPI](https://img.shields.io/pypi/v/wildberries-sdk.svg)](https://pypi.org/project/wildberries-sdk/) | [![PyPI Downloads](https://static.pepy.tech/badge/wildberries-sdk)](https://pepy.tech/project/wildberries-sdk) | [docs/python/README.md](../python/README.md) | [pypi.org](https://pypi.org/project/wildberries-sdk/) |
| Node.js | [![npm](https://img.shields.io/npm/v/wildberries-sdk.svg)](https://www.npmjs.com/package/wildberries-sdk) | [![NPM Downloads](https://img.shields.io/npm/dt/wildberries-sdk.svg)](https://www.npmjs.com/package/wildberries-sdk) | [docs/npm/README.md](../npm/README.md) | [npmjs.com](https://www.npmjs.com/package/wildberries-sdk) |
| PHP | [![Packagist](https://img.shields.io/packagist/v/eslazarev/wildberries-sdk.svg)](https://packagist.org/packages/eslazarev/wildberries-sdk) | [![Packagist Downloads](https://img.shields.io/packagist/dt/eslazarev/wildberries-sdk.svg)](https://packagist.org/packages/eslazarev/wildberries-sdk) | [docs/php/README.md](../php/README.md) | [packagist.org](https://packagist.org/packages/eslazarev/wildberries-sdk) |
| Go | [![Go](https://img.shields.io/github/v/tag/eslazarev/wildberries-sdk?label=go)](https://github.com/eslazarev/wildberries-sdk/tags) | — | [docs/go/README.md](../go/README.md) | [pkg.go.dev](https://pkg.go.dev/github.com/eslazarev/wildberries-sdk/clients/go/finances) |
| Rust | [![Rust](https://img.shields.io/github/v/tag/eslazarev/wildberries-sdk?label=rust)](https://github.com/eslazarev/wildberries-sdk/tags) | — | [docs/rust/README.md](../rust/README.md) | [crates.io](https://crates.io/crates/wildberries_sdk_finances) |

## Қауіпсіздік

Бұл SDK қауіпсіздік басымдықты шығарылым процесімен жасалған:

- CodeQL статикалық код талдауы
- OpenSSF Scorecard бағалауы
- TruffleHog расталған құпиялар сканерленуі
- Python тәуелділіктер аудиті (pip-audit)
- npm audit
- Composer audit
- Cargo audit
- Go осалдықтарын тексеру (govulncheck)
- Жарияланған пакеттерде қатты кодталған API токендері жоқ

[![CodeQL](https://github.com/eslazarev/wildberries-sdk/actions/workflows/codeql.yml/badge.svg)](https://github.com/eslazarev/wildberries-sdk/actions/workflows/codeql.yml)
[![Scorecard](https://github.com/eslazarev/wildberries-sdk/actions/workflows/scorecard.yml/badge.svg)](https://github.com/eslazarev/wildberries-sdk/actions/workflows/scorecard.yml)
[![Secrets](https://github.com/eslazarev/wildberries-sdk/actions/workflows/secrets.yml/badge.svg)](https://github.com/eslazarev/wildberries-sdk/actions/workflows/secrets.yml)
[![Dependency Audit](https://github.com/eslazarev/wildberries-sdk/actions/workflows/dependency-audit.yml/badge.svg)](https://github.com/eslazarev/wildberries-sdk/actions/workflows/dependency-audit.yml)


Бүгінгі күні қолжетімді барлық Wildberries API командалары спецификация модульдері бойынша топтастырылып ұсынылған.

## Автоматты түрде құрастырылған клиенттердің артықшылықтары

- **Сұраныс/жауаптың толық типтелуі.** Әр тілдегі клиент өзінің табиғи типтер жүйесін пайдаланады: Python-да pydantic, Node.js-те TypeScript интерфейстері, Go-да struct, PHP-де типтелген кластар, Rust-та serde құрылымдары. Өріс атауларындағы қателер мен қате типтер компиляция/линт кезеңінде ұсталады.
- **IDE-да автотолықтыру дайын.** Метод атаулары, параметрлер, модель өрістері мен enum мәндері белгіленіп, ұсынылады — Wildberries құжаттамасын оқудың қажеті жоқ.
- **Спецификациядан сипаттамалар мен docstring-тер.** Wildberries-тің YAML-дағы өріс/метод түсініктемелері кодқа көшіріледі және IDE-да hover-да көрінеді.
- **Клиент жағында тексеру.** Міндетті өрістер мен типтер сұраныс жіберілмей тұрып тексеріледі (Python pydantic форматтарды, enum-дарды және min/max шектеулерін де тексереді; Go/TypeScript/PHP/Rust-та тексеру міндетті өрістер мен типтермен шектеледі).
- **Барлық тілдер үшін бірдей контракт.** Операция ID-лері, модель өрістері және эндпоинттер Python, Node.js, Go, PHP және Rust-та бірдей — стектер арасында көшу кезінде бизнес-логиканы қайта жазудың қажеті жоқ.
- **Спецификациялармен ауытқу жоқ.** Wildberries API-ді жаңартқанда, SDK сол күні жаңа методтар мен модельдерді PR арқылы алады — спецификацияны қолмен diff жасаудың керегі жоқ.
- **Дайын transport-қабат.** Аутентификация, тақырыптар, базалық URL-дер, JSON сериализациясы, HTTP қателерін өңдеу — ортақ `api_client` / `runtime` / `client` модулінде бір рет іске асырылған және барлық методтармен қолданылады.

### Спецификация өзгерген кезде клиенттер GitHub Actions арқылы автоматты түрде өзекті күйде сақталады.

Бұл неліктен маңызды — спецификация өзгерістерінің тарихын қараңыз: [CHANGELOG.md](../../CHANGELOG.md). Әдетте аптасына бірнеше рет өзгереді.

## Жарияланған Wildberries спецификацияларының барлығы қамтылған

- Жалпы — [`specs/01-general.yaml`](../../specs/01-general.yaml)
- Тауарлармен жұмыс — [`specs/02-items.yaml`](../../specs/02-items.yaml)
- FBS тапсырыстары — [`specs/03-orders-fbs.yaml`](../../specs/03-orders-fbs.yaml)
- DBW тапсырыстары — [`specs/04-orders-dbw.yaml`](../../specs/04-orders-dbw.yaml)
- DBS тапсырыстары — [`specs/05-orders-dbs.yaml`](../../specs/05-orders-dbs.yaml)
- Дүкеннен алу — [`specs/06-in-store-pickup.yaml`](../../specs/06-in-store-pickup.yaml)
- FBW жеткізілімдері — [`specs/07-orders-fbw.yaml`](../../specs/07-orders-fbw.yaml)
- Маркетинг және жарнама — [`specs/08-promotion.yaml`](../../specs/08-promotion.yaml)
- Сатып алушылармен байланыс — [`specs/09-communications.yaml`](../../specs/09-communications.yaml)
- Тарифтер — [`specs/10-tariffs.yaml`](../../specs/10-tariffs.yaml)
- Аналитика — [`specs/11-analytics.yaml`](../../specs/11-analytics.yaml)
- Есептер — [`specs/12-reports.yaml`](../../specs/12-reports.yaml)
- Қаржы және бухгалтерия — [`specs/13-finances.yaml`](../../specs/13-finances.yaml)
- Wildberries Цифрлық — [`specs/14-wbd.yaml`](../../specs/14-wbd.yaml)

Әр методтың толық тізімі (сипаттамалар Wildberries OpenAPI спецификацияларынан орыс тілінде алынған) [негізгі README](../../README.md#в-данный-момент-представлены-все-доступные-спецификации)-да.
