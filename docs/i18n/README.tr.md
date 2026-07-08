# Python, Node.js, Go, PHP ve Rust için Wildberries SDK istemcileri — resmi OpenAPI spesifikasyonlarıyla sürekli senkronize.

🌐 [Русский](../../README.md) · [English](README.en.md) · [简体中文](README.zh-CN.md) · **Türkçe** · [Қазақша](README.kk.md) · [Oʻzbekcha](README.uz.md)

📖 **Dokümantasyon:** <https://eslazarev.github.io/wildberries-sdk/> — tüm Wildberries API işlemleri için Python, Node.js, Go, PHP ve Rust örnekleriyle başvuru kılavuzu.

![using_sdk.gif](../../.github/images/using_wildberries_sdk_python.gif)

| Dil | Sürüm | İndirme | README | Paket Deposu |
| --- | --- | --- | --- | --- |
| Python | [![PyPI](https://img.shields.io/pypi/v/wildberries-sdk.svg)](https://pypi.org/project/wildberries-sdk/) | [![PyPI Downloads](https://static.pepy.tech/badge/wildberries-sdk)](https://pepy.tech/project/wildberries-sdk) | [docs/python/README.md](../python/README.md) | [pypi.org](https://pypi.org/project/wildberries-sdk/) |
| Node.js | [![npm](https://img.shields.io/npm/v/wildberries-sdk.svg)](https://www.npmjs.com/package/wildberries-sdk) | [![NPM Downloads](https://img.shields.io/npm/dt/wildberries-sdk.svg)](https://www.npmjs.com/package/wildberries-sdk) | [docs/npm/README.md](../npm/README.md) | [npmjs.com](https://www.npmjs.com/package/wildberries-sdk) |
| PHP | [![Packagist](https://img.shields.io/packagist/v/eslazarev/wildberries-sdk.svg)](https://packagist.org/packages/eslazarev/wildberries-sdk) | [![Packagist Downloads](https://img.shields.io/packagist/dt/eslazarev/wildberries-sdk.svg)](https://packagist.org/packages/eslazarev/wildberries-sdk) | [docs/php/README.md](../php/README.md) | [packagist.org](https://packagist.org/packages/eslazarev/wildberries-sdk) |
| Go | [![Go](https://img.shields.io/github/v/tag/eslazarev/wildberries-sdk?label=go)](https://github.com/eslazarev/wildberries-sdk/tags) | — | [docs/go/README.md](../go/README.md) | [pkg.go.dev](https://pkg.go.dev/github.com/eslazarev/wildberries-sdk/clients/go/finances) |
| Rust | [![Rust](https://img.shields.io/github/v/tag/eslazarev/wildberries-sdk?label=rust)](https://github.com/eslazarev/wildberries-sdk/tags) | — | [docs/rust/README.md](../rust/README.md) | [crates.io](https://crates.io/crates/wildberries_sdk_finances) |

## Güvenlik

Bu SDK güvenlik öncelikli bir sürüm süreciyle yayınlanır:

- CodeQL statik kod analizi
- OpenSSF Scorecard değerlendirmesi
- TruffleHog ile doğrulanmış sır taraması
- Python bağımlılık denetimi (pip-audit)
- npm audit
- Composer audit
- Cargo audit
- Go güvenlik açığı taraması (govulncheck)
- Yayınlanan paketlerde sabit kodlanmış API tokenları yok

[![CodeQL](https://github.com/eslazarev/wildberries-sdk/actions/workflows/codeql.yml/badge.svg)](https://github.com/eslazarev/wildberries-sdk/actions/workflows/codeql.yml)
[![Scorecard](https://github.com/eslazarev/wildberries-sdk/actions/workflows/scorecard.yml/badge.svg)](https://github.com/eslazarev/wildberries-sdk/actions/workflows/scorecard.yml)
[![Secrets](https://github.com/eslazarev/wildberries-sdk/actions/workflows/secrets.yml/badge.svg)](https://github.com/eslazarev/wildberries-sdk/actions/workflows/secrets.yml)
[![Dependency Audit](https://github.com/eslazarev/wildberries-sdk/actions/workflows/dependency-audit.yml/badge.svg)](https://github.com/eslazarev/wildberries-sdk/actions/workflows/dependency-audit.yml)


Bugün mevcut olan tüm Wildberries API komutları, spesifikasyon modüllerine göre gruplanmış olarak desteklenir.

## Otomatik üretilen istemcilerin avantajları

- **Tam istek/yanıt tiplemesi.** Her dilin istemcisi kendi yerel tip sistemini kullanır: Python'da pydantic, Node.js'de TypeScript arayüzleri, Go'da struct'lar, PHP'de tipli sınıflar, Rust'ta serde struct'ları. Alan adı yazım hataları ve yanlış tipler derleme/lint sırasında yakalanır.
- **IDE otomatik tamamlama hazır.** Metod adları, parametreler, model alanları ve enum değerleri vurgulanır ve önerilir — Wildberries dokümantasyonunu okumaya gerek kalmadan.
- **Spesifikasyondan açıklamalar ve docstring'ler.** Wildberries'in YAML'daki alan ve metod yorumları üretilen koda taşınır ve IDE'de hover ile görünür.
- **İstemci tarafı doğrulama.** Zorunlu alanlar ve tipler istek gönderilmeden önce kontrol edilir (Python pydantic ayrıca format, enum ve min/max kısıtlarını da doğrular; Go/TypeScript/PHP/Rust'ta kontrol zorunlu alan ve tip seviyesinde kalır).
- **Tüm dillerde tek bir kontrat.** İşlem ID'leri, model alanları ve uç noktalar Python, Node.js, Go, PHP ve Rust'ta aynıdır — yığınlar arası geçişte iş mantığını yeniden yazmaya gerek yoktur.
- **Spesifikasyondan sapma yoktur.** Wildberries API'yi güncellediğinde, SDK aynı gün içinde yeni metod ve modelleri içeren bir PR alır — spec diff'i manuel hesaplamak gerekmez.
- **Hazır transport katmanı.** Kimlik doğrulama, başlıklar, base URL'ler, JSON serileştirme ve HTTP hata yönetimi paylaşılan `api_client` / `runtime` / `client` modülünde bir kez uygulanır ve tüm metodlar tarafından yeniden kullanılır.

### İstemciler, spesifikasyon değiştiğinde GitHub Actions tarafından otomatik güncellenir.

Bu neden önemli — spesifikasyon değişiklik geçmişine bakın: [CHANGELOG.md](../../CHANGELOG.md). Genellikle haftada birkaç kez değişir.

## Yayınlanan tüm Wildberries spesifikasyonları kapsanır

- Genel — [`specs/01-general.yaml`](../../specs/01-general.yaml)
- Ürünler — [`specs/02-items.yaml`](../../specs/02-items.yaml)
- FBS siparişleri — [`specs/03-orders-fbs.yaml`](../../specs/03-orders-fbs.yaml)
- DBW siparişleri — [`specs/04-orders-dbw.yaml`](../../specs/04-orders-dbw.yaml)
- DBS siparişleri — [`specs/05-orders-dbs.yaml`](../../specs/05-orders-dbs.yaml)
- Mağazada teslim alma — [`specs/06-in-store-pickup.yaml`](../../specs/06-in-store-pickup.yaml)
- FBW tedarikleri — [`specs/07-orders-fbw.yaml`](../../specs/07-orders-fbw.yaml)
- Pazarlama ve kampanya — [`specs/08-promotion.yaml`](../../specs/08-promotion.yaml)
- Müşteri iletişimi — [`specs/09-communications.yaml`](../../specs/09-communications.yaml)
- Tarifeler — [`specs/10-rates.yaml`](../../specs/10-rates.yaml)
- Analitik — [`specs/11-analytics.yaml`](../../specs/11-analytics.yaml)
- Raporlar — [`specs/12-reports.yaml`](../../specs/12-reports.yaml)
- Finans ve muhasebe — [`specs/13-finances.yaml`](../../specs/13-finances.yaml)
- Wildberries Dijital — [`specs/14-wbd.yaml`](../../specs/14-wbd.yaml)

Her metodun tam listesi (açıklamalar Wildberries OpenAPI spesifikasyonlarındaki Rusça orijinal metinden alınmıştır) [ana README](../../README.md#в-данный-момент-представлены-все-доступные-спецификации)'de bulunur.
