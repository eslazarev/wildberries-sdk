# wildberries-sdk (Rust)

Сгенерированные Rust-клиенты находятся в `clients/rust/<module>`.

📖 **Документация:** <https://eslazarev.github.io/wildberries-sdk/> — справочник по всем операциям API с примерами вызова.

[![Спроси DeepWiki об этом репо](https://deepwiki.com/badge.svg)](https://deepwiki.com/eslazarev/wildberries-sdk)

## Безопасность

SDK выпускается с security-first процессом:

- статический анализ кода CodeQL
- оценка по OpenSSF Scorecard
- сканирование секретов TruffleHog (verified-режим)
- аудит зависимостей Python (pip-audit)
- npm audit
- Composer audit
- Cargo audit
- проверка уязвимостей Go (govulncheck)
- в опубликованных пакетах нет захардкоженных API-токенов

[![CodeQL](https://github.com/eslazarev/wildberries-sdk/actions/workflows/codeql.yml/badge.svg)](https://github.com/eslazarev/wildberries-sdk/actions/workflows/codeql.yml)
[![Scorecard](https://github.com/eslazarev/wildberries-sdk/actions/workflows/scorecard.yml/badge.svg)](https://github.com/eslazarev/wildberries-sdk/actions/workflows/scorecard.yml)
[![Secrets](https://github.com/eslazarev/wildberries-sdk/actions/workflows/secrets.yml/badge.svg)](https://github.com/eslazarev/wildberries-sdk/actions/workflows/secrets.yml)
[![Dependency Audit](https://github.com/eslazarev/wildberries-sdk/actions/workflows/dependency-audit.yml/badge.svg)](https://github.com/eslazarev/wildberries-sdk/actions/workflows/dependency-audit.yml)

## Установка

Каждая спецификация - отдельный crate (например, `wildberries_sdk_general`).

```bash
cargo add wildberries_sdk_general
```

Если крейты недоступны в registry, используйте локальные зависимости:

```toml
[dependencies]
wildberries_sdk_general = { path = "clients/rust/general" }
```

## Использование

Каждая спецификация - отдельный crate. Добавьте нужный crate как локальную зависимость:

```toml
[dependencies]
wildberries_sdk_general = { path = "clients/rust/general" }
```

## Частота релизов

[на сайте документации](https://eslazarev.github.io/wildberries-sdk/releases/)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/eslazarev/wildberries-sdk/main/.github/images/release-cadence-ru-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/eslazarev/wildberries-sdk/main/.github/images/release-cadence-ru-light.svg">
  <img src="https://raw.githubusercontent.com/eslazarev/wildberries-sdk/main/.github/images/release-cadence-ru-light.svg" alt="Календарь релизов за последний год">
</picture>

<!-- RUST_METHODS_LIST_START -->
## Методы API

### general (`general`)
- `general::api_api::get_v2_news` — `GET /api/communications/v2/news` — Метод позволяет получать новости портала продавцов.
- `general::default_api::delete_v1_user` — `DELETE /api/v1/user` — Метод удаляет пользователя из [списка сотрудников продавца](https://dev.wildberries.ru/openapi/api-information#tag/sellerUserManagement/operation/getV1Users).
- `general::default_api::get_v1_rating` — `GET /api/common/v1/rating` — Метод возвращает пользовательский рейтинг продавца и количество отзывов.
- `general::default_api::get_v1_seller_info` — `GET /api/v1/seller-info` — Метод позволяет получать наименование продавца и ID его профиля.
- `general::default_api::get_v1_subscriptions` — `GET /api/common/v1/subscriptions` — Метод возвращает информацию о подписке [Джем](https://seller.wildberries.ru/monetization/jam): - Если продавец никогда не подключал подписку Джем, возвращается пустой ответ `200`.
- `general::default_api::get_v1_tariff_constructor_options` — `GET /api/common/v1/tariff-constructor/options` — Метод возвращает информацию обо всех опциях и пакетах опций, которые продавец подключил в [Конструкторе тарифов](https://seller.wildberries.ru/tariff-constructor).
- `general::default_api::get_v1_users` — `GET /api/v1/users` — Метод возвращает список активных или приглашённых пользователей профиля продавца.
- `general::default_api::post_v1_invite` — `POST /api/v1/invite` — Метод создаёт приглашение для нового пользователя с настройкой доступов к разделам профиля продавца.
- `general::default_api::put_v1_users_access` — `PUT /api/v1/users/access` — Метод меняет права доступа одному или нескольким пользователям.
- `general::wbapi_api::get_ping` — `GET /ping` — Метод проверяет: 1.

### items (`items`)
- `items::default_api::delete_v2_tag_id` — `DELETE /content/v2/tag/{id}` — Метод удаляет ярлык из [списка ярлыков](https://dev.wildberries.ru/openapi/item-management#tag/labels/operation/getV2Tags) продавца.
- `items::default_api::delete_v3_stocks_warehouse_id` — `DELETE /api/v3/stocks/{warehouseId}` — Метод удаляет запись об остатках товаров продавца из [списка остатков](https://dev.wildberries.ru/openapi/item-management#tag/sellerWarehousesInventory/operation/postV3StocksWarehouseId).
- `items::default_api::delete_v3_warehouses_warehouse_id` — `DELETE /api/v3/warehouses/{warehouseId}` — Метод удаляет [склад продавца](https://dev.wildberries.ru/openapi/item-management#tag/sellerWarehouses/operation/getV3Warehouses).
- `items::default_api::get_v1_brands` — `GET /api/content/v1/brands` — Метод возвращает список брендов по ID предмета.
- `items::default_api::get_v2_buffer_goods_task` — `GET /api/v2/buffer/goods/task` — Метод возвращает информацию о товарах и ошибках в товарах из загрузки в обработке.
- `items::default_api::get_v2_buffer_tasks` — `GET /api/v2/buffer/tasks` — Метод возвращает информацию про загрузку скидок в обработке.
- `items::default_api::get_v2_cards_limits` — `GET /content/v2/cards/limits` — Возвращает бесплатные и платные лимиты продавца на [создание карточек товаров](https://dev.wildberries.ru/openapi/item-management#tag/listingItems/operation/postV2CardsUpload).
- `items::default_api::get_v2_directory_colors` — `GET /content/v2/directory/colors` — Метод возвращает возможные значения [характеристики](https://dev.wildberries.ru/openapi/item-management#tag/categoriesSubcategoriesAndCharacteristics/operation/getV2ObjectCharcsSubjectId) предмета…
- `items::default_api::get_v2_directory_countries` — `GET /content/v2/directory/countries` — Метод возвращает возможные значения [характеристики](https://dev.wildberries.ru/openapi/item-management#tag/categoriesSubcategoriesAndCharacteristics/operation/getV2ObjectCharcsSubjectId) предмета…
- `items::default_api::get_v2_directory_kinds` — `GET /content/v2/directory/kinds` — Метод возвращает возможные значения [характеристики](https://dev.wildberries.ru/openapi/item-management#tag/categoriesSubcategoriesAndCharacteristics/operation/getV2ObjectCharcsSubjectId) предмета…
- `items::default_api::get_v2_directory_okpd` — `GET /api/content/v2/directory/okpd` — Метод возвращает список кодов ОКПД2 по ID [предмета](https://dev.wildberries.ru/openapi/work-with-products#tag/categoriesSubcategoriesAndCharacteristics/paths/~1content~1v2~1object~1all/get) и…
- `items::default_api::get_v2_directory_okpd_all` — `GET /api/content/v2/directory/okpd/all` — Метод возвращает справочный список всех кодов ОКПД2.
- `items::default_api::get_v2_directory_seasons` — `GET /content/v2/directory/seasons` — Метод возвращает возможные значения [характеристики](https://dev.wildberries.ru/openapi/item-management#tag/categoriesSubcategoriesAndCharacteristics/operation/getV2ObjectCharcsSubjectId) предмета…
- `items::default_api::get_v2_directory_tnved` — `GET /content/v2/directory/tnved` — Метод возвращает список кодов ТН ВЭД по ID [предмета](https://dev.wildberries.ru/openapi/item-management#tag/categoriesSubcategoriesAndCharacteristics/operation/getV2ObjectAll) и фрагменту кода ТН…
- `items::default_api::get_v2_directory_tnved_all` — `GET /api/content/v2/directory/tnved/all` — Метод возвращает справочный список всех кодов ТН ВЭД.
- `items::default_api::get_v2_directory_vat` — `GET /content/v2/directory/vat` — Метод возвращает возможные значения [характеристики](https://dev.wildberries.ru/openapi/item-management#tag/categoriesSubcategoriesAndCharacteristics/operation/getV2ObjectCharcsSubjectId) предмета…
- `items::default_api::get_v2_history_goods_task` — `GET /api/v2/history/goods/task` — Метод возвращает информацию о товарах и об ошибках в товарах в обработанной загрузке.
- `items::default_api::get_v2_history_tasks` — `GET /api/v2/history/tasks` — Метод возвращает информацию об обработанной загрузке цен и скидок.
- `items::default_api::get_v2_list_goods_filter` — `GET /api/v2/list/goods/filter` — Метод возвращает информацию о товарах: цены, валюту, общие скидки, [скидки WB Клуба](https://dev.wildberries.ru/openapi/item-management#tag/pricesAndDiscounts/operation/postV2UploadTaskClubDiscount)…
- `items::default_api::get_v2_list_goods_size_nm` — `GET /api/v2/list/goods/size/nm` — Метод возвращает информацию обо всех размерах одного товара: цены, валюту, общие скидки и скидки для…
- `items::default_api::get_v2_object_all` — `GET /content/v2/object/all` — Метод возвращает список названий [родительских категорий предметов](https://dev.wildberries.ru/openapi/item-management#tag/categoriesSubcategoriesAndCharacteristics/operation/getV2ObjectParentAll) и…
- `items::default_api::get_v2_object_charcs_subject_id` — `GET /content/v2/object/charcs/{subjectId}` — Метод возвращает параметры характеристик предмета: названия, типы данных, единицы измерения и так далее.
- `items::default_api::get_v2_object_parent_all` — `GET /content/v2/object/parent/all` — Метод возвращает названия и ID всех родительских категорий для [создания карточек товаров](https://dev.wildberries.ru/openapi/item-management#tag/listingItems): например, `Электроника`, `Бытовая…
- `items::default_api::get_v2_quarantine_goods` — `GET /api/v2/quarantine/goods` — Метод возвращает информацию о товарах в карантине.
- `items::default_api::get_v2_tags` — `GET /content/v2/tags` — Метод возвращает список и характеристики всех ярлыков продавца для группировки и фильтрации товаров.
- `items::default_api::get_v3_dbw_warehouses_warehouse_id_contacts` — `GET /api/v3/dbw/warehouses/{warehouseId}/contacts` — Метод возвращает список контактов, привязанных к [складу продавца](https://dev.wildberries.ru/openapi/item-management#tag/sellerWarehouses/operation/getV3Warehouses).
- `items::default_api::get_v3_offices` — `GET /api/v3/offices` — Метод возвращает список складов WB для привязки к складу продавца при его [создании](https://dev.wildberries.ru/openapi/item-management#tag/sellerWarehouses/operation/postV3Warehouses) или…
- `items::default_api::get_v3_warehouses` — `GET /api/v3/warehouses` — Метод возвращает список всех складов продавца.
- `items::default_api::patch_v2_tag_id` — `PATCH /content/v2/tag/{id}` — Метод заменяет данные ярлыка: имя и цвет.
- `items::default_api::post_v1_recommendations_list` — `POST /api/content/v1/recommendations/list` — Метод возвращает список [рекомендаций](https://seller.wildberries.ru/recommendations-v3) в карточках товаров.
- `items::default_api::post_v1_recommendations_set` — `POST /api/content/v1/recommendations/set` — Метод обновляет, добавляет или удаляет [рекомендации](https://seller.wildberries.ru/recommendations-v3) для товаров.
- `items::default_api::post_v1_upload_task_b2b_wholesale` — `POST /api/discounts-prices/v1/upload/task/b2b/wholesale` — Метод устанавливает [оптовые скидки для бизнеса](https://seller.wildberries.ru/instructions/ru/ru/material/how-to-enable-wholesale-discounts-for-business)
- `items::default_api::post_v2_barcodes` — `POST /content/v2/barcodes` — Метод генерирует массив уникальных баркодов для создания размера в [карточке товара](https://dev.wildberries.ru/openapi/item-management#tag/listingItems/operation/postV2CardsUpload).
- `items::default_api::post_v2_cards_delete_trash` — `POST /content/v2/cards/delete/trash` — Метод переносит [карточки товаров в корзину](https://dev.wildberries.ru/openapi/item-management#tag/listings/operation/postV2GetCardsTrash).
- `items::default_api::post_v2_cards_error_list` — `POST /content/v2/cards/error/list` — Метод возвращает список карточек товаров ([черновиков](https://seller.wildberries.ru/new-goods/error-cards)), при создании или редактировании которых произошли ошибки, с описанием этих ошибок.
- `items::default_api::post_v2_cards_move_nm` — `POST /content/v2/cards/moveNm` — Метод [объединяет и разъединяет](/knowledge-base/articles/019d49a4-1320-71bb-9dac-8ba07e7177ce/rabota-s-tovarami#obuedinenie-i-razuedinenie-kartochek-tovarov) карточки товаров.
- `items::default_api::post_v2_cards_recover` — `POST /content/v2/cards/recover` — Метод восстанавливает [карточки товаров из корзины](https://dev.wildberries.ru/openapi/item-management#tag/listings/operation/postV2GetCardsTrash).
- `items::default_api::post_v2_cards_update` — `POST /content/v2/cards/update` — Метод обновляет данные карточек товаров.
- `items::default_api::post_v2_cards_upload` — `POST /content/v2/cards/upload` — Метод создаёт карточки товаров c указанием описаний и характеристик товаров.
- `items::default_api::post_v2_cards_upload_add` — `POST /content/v2/cards/upload/add` — Метод создаёт карточки товаров, присоединяя их к существующим отдельным карточкам и группам…
- `items::default_api::post_v2_get_cards_list` — `POST /content/v2/get/cards/list` — Метод возвращает список созданных карточек товаров.
- `items::default_api::post_v2_get_cards_trash` — `POST /content/v2/get/cards/trash` — Метод возвращает список карточек товаров в корзине.
- `items::default_api::post_v2_list_goods_filter` — `POST /api/v2/list/goods/filter` — Метод возвращает информацию о товарах по их артикулам: цены, валюту, общие скидки…
- `items::default_api::post_v2_tag` — `POST /content/v2/tag` — Метод добавляет один ярлык продавца.
- `items::default_api::post_v2_tag_nomenclature_link` — `POST /content/v2/tag/nomenclature/link` — Метод добавляет или снимает ярлык с карточки товара.
- `items::default_api::post_v2_upload_task` — `POST /api/v2/upload/task` — Метод устанавливает цены и скидки для товаров.
- `items::default_api::post_v2_upload_task_club_discount` — `POST /api/v2/upload/task/club-discount` — Устанавливает скидки для товаров в рамках подписки [WB Клуб](https://seller.wildberries.ru/help-center/article/A-337).
- `items::default_api::post_v2_upload_task_size` — `POST /api/v2/upload/task/size` — Метод устанавливает цены отдельно для размеров товаров.
- `items::default_api::post_v3_media_file` — `POST /content/v3/media/file` — Метод загружает и добавляет один медиафайл к карточке товара.
- `items::default_api::post_v3_media_save` — `POST /content/v3/media/save` — Метод загружает набор медиафайлов в карточку товара через указание ссылок в запросе.
- `items::default_api::post_v3_stocks_warehouse_id` — `POST /api/v3/stocks/{warehouseId}` — Метод возвращает данные об остатках товаров на [складах продавца](https://dev.wildberries.ru/openapi/item-management#tag/sellerWarehouses).
- `items::default_api::post_v3_warehouses` — `POST /api/v3/warehouses` — Метод создаёт склад продавца для работы с [остатками товаров](https://dev.wildberries.ru/openapi/item-management#tag/sellerWarehousesInventory), кроме сверхгабаритных (СГТ), по модели…
- `items::default_api::put_v3_dbw_warehouses_warehouse_id_contacts` — `PUT /api/v3/dbw/warehouses/{warehouseId}/contacts` — Метод обновляет список контактов [склада продавца](https://dev.wildberries.ru/openapi/item-management#tag/sellerWarehouses/operation/getV3Warehouses).
- `items::default_api::put_v3_stocks_warehouse_id` — `PUT /api/v3/stocks/{warehouseId}` — Метод обновляет количество остатков товаров продавца [в списке](https://dev.wildberries.ru/openapi/item-management#tag/sellerWarehousesInventory/operation/postV3StocksWarehouseId).
- `items::default_api::put_v3_warehouses_warehouse_id` — `PUT /api/v3/warehouses/{warehouseId}` — Метод обновляет данные [склада продавца](https://dev.wildberries.ru/openapi/item-management#tag/sellerWarehouses/operation/getV3Warehouses), кроме складов для сверхгабаритных товаров (СГТ…

### orders_fbs (`orders_fbs`)
- `orders_fbs::default_api::get_v3_fbs_settings_autoreturns` — `GET /api/marketplace/v3/fbs/settings/autoreturns` — Метод возвращает информацию о настройках автовозврата, установленных продавцом.
- `orders_fbs::default_api::get_v3_fbs_settings_autoreturns_subcategories_restricted` — `GET /api/marketplace/v3/fbs/settings/autoreturns/subcategories/restricted` — Метод возвращает список ID предметов, товары которых не могут храниться на складах WB и будут возвращены в ПВЗ автоматически.
- `orders_fbs::default_api::patch_v3_fbs_settings_autoreturns` — `PATCH /api/marketplace/v3/fbs/settings/autoreturns` — Метод устанавливает настройки автовозврата продавца для малогабаритных товаров — `"cargoType":1`.
- `orders_fbs::default_api::patch_v3_fbs_settings_autoreturns_items` — `PATCH /api/marketplace/v3/fbs/settings/autoreturns/items` — Метод устанавливает настройки автовозврата малогабаритных товаров — `"cargoType":1`.
- `orders_fbs::default_api::post_v3_fbs_settings_autoreturns_items` — `POST /api/marketplace/v3/fbs/settings/autoreturns/items` — Метод возвращает настройки автовозврата товаров.
- `orders_fbs::fbs_api::delete_v3_orders_order_id_meta` — `DELETE /api/v3/orders/{orderId}/meta` — Метод удаляет значение [идентификаторов маркировки сборочного задания](https://dev.wildberries.ru/openapi/orders-fbs#tag/fbsLabelIdentifiers/operation/postV3OrdersMeta) для переданного ключа.
- `orders_fbs::fbs_api::delete_v3_passes_pass_id` — `DELETE /api/v3/passes/{passId}` — Метод удаляет пропуск продавца [из списка](https://dev.wildberries.ru/openapi/orders-fbs#tag/fbsPasses/operation/getV3Passes).
- `orders_fbs::fbs_api::delete_v3_supplies_supply_id` — `DELETE /api/v3/supplies/{supplyId}` — Метод удаляет [поставку](https://dev.wildberries.ru/openapi/orders-fbs#tag/fbsSupplies/operation/getV3SuppliesSupplyId), если она активна и за ней не закреплено ни одно…
- `orders_fbs::fbs_api::delete_v3_supplies_supply_id_trbx` — `DELETE /api/v3/supplies/{supplyId}/trbx` — Метод удаляет грузоместа из поставки.
- `orders_fbs::fbs_api::get_v3_fbs_dictionaries_countries_oksm` — `GET /api/marketplace/v3/fbs/dictionaries/countries/oksm` — Метод возвращает список стран ОКСМ — Общероссийского классификатора стран мира — с полными названиями и кодами.
- `orders_fbs::fbs_api::get_v3_fbs_orders_archive` — `GET /api/marketplace/v3/fbs/orders/archive` — Метод возвращает сборочные задания, созданные более 3 месяцев назад.
- `orders_fbs::fbs_api::get_v3_fbs_shipping_points` — `GET /api/marketplace/v3/fbs/shipping-points`
- `orders_fbs::fbs_api::get_v3_fbs_supplies_supply_id_shipping_points` — `GET /api/marketplace/v3/fbs/supplies/{supplyId}/shipping-points` — Метод возвращает доступные пункты отгрузки для указанной поставки.
- `orders_fbs::fbs_api::get_v3_fbs_supplies_supply_id_stickers_spot` — `GET /api/marketplace/v3/fbs/supplies/{supplyId}/stickers/spot` — Метод возвращает сформированный QR-код СПОТ для поставки в формате PNG, кодировка base64.
- `orders_fbs::fbs_api::get_v3_orders` — `GET /api/v3/orders` — Метод возвращает информацию о сборочных заданиях, созданных не более 3 месяцев назад, без их актуального…
- `orders_fbs::fbs_api::get_v3_orders_new` — `GET /api/v3/orders/new` — Метод возвращает список всех новых [сборочных заданий](https://dev.wildberries.ru/openapi/orders-fbs#tag/fbsAssemblyOrders/operation/getV3Orders), которые есть у продавца на момент запроса.
- `orders_fbs::fbs_api::get_v3_passes` — `GET /api/v3/passes` — Метод возвращает список всех [созданных](https://dev.wildberries.ru/openapi/orders-fbs#tag/fbsPasses/operation/postV3Passes) пропусков продавца.
- `orders_fbs::fbs_api::get_v3_passes_offices` — `GET /api/v3/passes/offices` — Метод возвращает список складов для привязки к [пропуску продавца](https://dev.wildberries.ru/openapi/orders-fbs#tag/fbsPasses/operation/getV3Passes).
- `orders_fbs::fbs_api::get_v3_supplies` — `GET /api/v3/supplies` — Метод возвращает список [поставок](https://dev.wildberries.ru/openapi/orders-fbs#tag/fbsSupplies/operation/getV3SuppliesSupplyId).
- `orders_fbs::fbs_api::get_v3_supplies_orders_reshipment` — `GET /api/v3/supplies/orders/reshipment` — Метод возвращает все [сборочные задания](https://dev.wildberries.ru/openapi/orders-fbs#tag/fbsAssemblyOrders/operation/getV3Orders), требующие повторной отгрузки.
- `orders_fbs::fbs_api::get_v3_supplies_supply_id` — `GET /api/v3/supplies/{supplyId}` — Метод возвращает подробную информацию о поставке.
- `orders_fbs::fbs_api::get_v3_supplies_supply_id_barcode` — `GET /api/v3/supplies/{supplyId}/barcode` — Метод возвращает QR-код [поставки](https://dev.wildberries.ru/openapi/orders-fbs#tag/fbsSupplies/operation/getV3SuppliesSupplyId) в форматах: - SVG - ZPLV (вертикальный) - ZPLH (горизонтальный) - PNG…
- `orders_fbs::fbs_api::get_v3_supplies_supply_id_order_ids` — `GET /api/marketplace/v3/supplies/{supplyId}/order-ids` — Метод возвращает список ID сборочных заданий, закреплённых за поставкой.
- `orders_fbs::fbs_api::get_v3_supplies_supply_id_trbx` — `GET /api/v3/supplies/{supplyId}/trbx` — Возвращает список грузомест поставки.
- `orders_fbs::fbs_api::patch_v3_fbs_supplies_shipping_method` — `PATCH /api/marketplace/v3/fbs/supplies/shipping-method` — Метод устанавливает способ доставки, дату и пункт отгрузки у поставок.
- `orders_fbs::fbs_api::patch_v3_fbs_supplies_supply_id_orders_transfer` — `PATCH /api/marketplace/v3/fbs/supplies/{supplyId}/orders/transfer` — Метод переводит сборочные задания из статуса `complete` — в доставке в статус `confirm` — на сборке.
- `orders_fbs::fbs_api::patch_v3_orders_order_id_cancel` — `PATCH /api/v3/orders/{orderId}/cancel` — Метод отменяет [сборочное задание](https://dev.wildberries.ru/openapi/orders-fbs#tag/fbsAssemblyOrders/operation/getV3Orders) и переводит в…
- `orders_fbs::fbs_api::patch_v3_supplies_supply_id_deliver` — `PATCH /api/v3/supplies/{supplyId}/deliver` — Метод закрывает [поставку](https://dev.wildberries.ru/openapi/orders-fbs#tag/fbsSupplies/operation/getV3SuppliesSupplyId) и переводит все…
- `orders_fbs::fbs_api::patch_v3_supplies_supply_id_orders` — `PATCH /api/marketplace/v3/supplies/{supplyId}/orders` — Метод добавляет до 100 [сборочных заданий](https://dev.wildberries.ru/openapi/orders-fbs#tag/fbsAssemblyOrders/operation/getV3Orders) к поставке и переводит их в…
- `orders_fbs::fbs_api::post_v3_fbs_supplies_spot_list` — `POST /api/marketplace/v3/fbs/supplies/spot/list` — Метод возвращает данные СПОТ для списка поставок.
- `orders_fbs::fbs_api::post_v3_orders_client` — `POST /api/v3/orders/client` — Метод позволяет получать информацию о покупателе по ID сборочного задания.
- `orders_fbs::fbs_api::post_v3_orders_meta` — `POST /api/marketplace/v3/orders/meta` — Метод возвращает идентификаторы маркировки [сборочных заданий](https://dev.wildberries.ru/openapi/orders-fbs#tag/fbsAssemblyOrders/operation/getV3Orders) и статусы их проверки.
- `orders_fbs::fbs_api::post_v3_orders_status` — `POST /api/v3/orders/status` — Метод возвращает статусы [сборочных заданий](https://dev.wildberries.ru/openapi/orders-fbs#tag/fbsAssemblyOrders/operation/getV3Orders) по их ID.
- `orders_fbs::fbs_api::post_v3_orders_status_history` — `POST /api/v3/orders/status/history` — Метод возвращает историю [статусов](https://dev.wildberries.ru/openapi/orders-fbs#tag/fbsAssemblyOrders/operation/postV3OrdersStatus) для…
- `orders_fbs::fbs_api::post_v3_orders_stickers` — `POST /api/v3/orders/stickers` — Метод возвращает список стикеров для [сборочных заданий](https://dev.wildberries.ru/openapi/orders-fbs#tag/fbsAssemblyOrders) в…
- `orders_fbs::fbs_api::post_v3_orders_stickers_cross_border` — `POST /api/v3/orders/stickers/cross-border` — Метод возвращает список стикеров [сборочных заданий](https://dev.wildberries.ru/openapi/orders-fbs#tag/fbsAssemblyOrders/operation/getV3Orders) трансграничных поставок в формате PDF.
- `orders_fbs::fbs_api::post_v3_passes` — `POST /api/v3/passes` — Метод создаёт [пропуск продавца](https://dev.wildberries.ru/openapi/orders-fbs#tag/fbsPasses/operation/getV3Passes) с привязкой к складу WB.
- `orders_fbs::fbs_api::post_v3_supplies` — `POST /api/v3/supplies` — Метод создаёт новую [поставку](https://dev.wildberries.ru/openapi/orders-fbs#tag/fbsSupplies/operation/getV3SuppliesSupplyId).
- `orders_fbs::fbs_api::post_v3_supplies_supply_id_trbx` — `POST /api/v3/supplies/{supplyId}/trbx` — Метод добавляет требуемое количество [грузомест](https://dev.wildberries.ru/openapi/orders-fbs#tag/fbsSupplies/operation/getV3SuppliesSupplyIdTrbx) в…
- `orders_fbs::fbs_api::post_v3_supplies_supply_id_trbx_stickers` — `POST /api/v3/supplies/{supplyId}/trbx/stickers` — Метод возвращает QR-стикеры в форматах: - SVG - ZPLV (вертикальный) - ZPLH (горизонтальный) - PNG Размер стикеров — 580x400 px.
- `orders_fbs::fbs_api::put_v3_fbs_supplies_supply_id_spot` — `PUT /api/marketplace/v3/fbs/supplies/{supplyId}/spot` — Метод добавляет данные СПОТ в поставку.
- `orders_fbs::fbs_api::put_v3_orders_order_id_meta_customs_declaration` — `PUT /api/marketplace/v3/orders/{orderId}/meta/customs-declaration` — Метод обновляет номер ДТ — декларации на товары — в [идентификаторах маркировки сборочного задания](https://dev.wildberries.ru/openapi/orders-fbs#tag/fbsLabelIdentifiers/operation/postV3OrdersMeta).
- `orders_fbs::fbs_api::put_v3_orders_order_id_meta_expiration` — `PUT /api/v3/orders/{orderId}/meta/expiration` — Метод закрепляет за [сборочным заданием](https://dev.wildberries.ru/openapi/orders-fbs#tag/fbsAssemblyOrders/operation/getV3Orders) срок годности товара.
- `orders_fbs::fbs_api::put_v3_orders_order_id_meta_gtin` — `PUT /api/v3/orders/{orderId}/meta/gtin` — Метод обновляет GTIN, уникальный ID товара в Беларуси, в…
- `orders_fbs::fbs_api::put_v3_orders_order_id_meta_imei` — `PUT /api/v3/orders/{orderId}/meta/imei` — Метод обновляет IMEI в [идентификаторах маркировки сборочного задания](https://dev.wildberries.ru/openapi/orders-fbs#tag/fbsLabelIdentifiers/operation/postV3OrdersMeta).
- `orders_fbs::fbs_api::put_v3_orders_order_id_meta_sgtin` — `PUT /api/v3/orders/{orderId}/meta/sgtin` — Метод обновляет код маркировки [Честного знака](https://честныйзнак.рф/) в идентификаторах маркировки…
- `orders_fbs::fbs_api::put_v3_orders_order_id_meta_uin` — `PUT /api/v3/orders/{orderId}/meta/uin` — Метод обновляет УИН, уникальный идентификационный номер, в…
- `orders_fbs::fbs_api::put_v3_passes_pass_id` — `PUT /api/v3/passes/{passId}` — Метод обновляет данные [пропуска продавца](https://dev.wildberries.ru/openapi/orders-fbs#tag/fbsPasses/operation/getV3Passes).

### orders_dbw (`orders_dbw`)
- `orders_dbw::dbw_api::get_v3_dbw_orders` — `GET /api/v3/dbw/orders` — Метод возвращает информацию о завершенных [сборочных заданиях](https://dev.wildberries.ru/openapi/orders-dbw#tag/dbwAssemblyOrders).
- `orders_dbw::dbw_api::get_v3_dbw_orders_new` — `GET /api/v3/dbw/orders/new` — Метод возвращает список всех новых [сборочных заданий](https://dev.wildberries.ru/openapi/orders-dbw#tag/dbwAssemblyOrders), которые есть у продавца на момент запроса.
- `orders_dbw::dbw_api::patch_v3_dbw_orders_order_id_cancel` — `PATCH /api/v3/dbw/orders/{orderId}/cancel` — Метод отменяет [сборочное задание](https://dev.wildberries.ru/openapi/orders-dbw#tag/dbwAssemblyOrders) и переводит в…
- `orders_dbw::dbw_api::patch_v3_dbw_orders_order_id_confirm` — `PATCH /api/v3/dbw/orders/{orderId}/confirm` — Метод переводит [сборочное задание](https://dev.wildberries.ru/openapi/orders-dbw#tag/dbwAssemblyOrders) в…
- `orders_dbw::dbw_api::post_v3_dbw_orders_client` — `POST /api/marketplace/v3/dbw/orders/client` — Метод возвращает информацию о покупателях по ID сборочных заданий.
- `orders_dbw::dbw_api::post_v3_dbw_orders_courier` — `POST /api/v3/dbw/orders/courier` — Метод возвращает контактные данные и номер автомобиля курьера по ID сборочного задания.
- `orders_dbw::dbw_api::post_v3_dbw_orders_delivery_date` — `POST /api/v3/dbw/orders/delivery-date` — Метод возвращает информацию о выбранных покупателем дате и времени доставки сборочных заданий.
- `orders_dbw::dbw_api::post_v3_dbw_orders_meta_delete` — `POST /api/marketplace/v3/dbw/orders/meta/delete` — Метод удаляет значение указанных [идентификаторов маркировки сборочного задания](https://dev.wildberries.ru/openapi/orders-dbw#tag/dbwLabelIdentifiers/operation/postV3DbwOrdersMetaDetails) для…
- `orders_dbw::dbw_api::post_v3_dbw_orders_meta_details` — `POST /api/marketplace/v3/dbw/orders/meta/details` — Метод возвращает идентификаторы маркировки [сборочных заданий](https://dev.wildberries.ru/openapi/orders-dbw#tag/dbwAssemblyOrders/operation/getV3DbwOrders) и статусы их проверки.
- `orders_dbw::dbw_api::post_v3_dbw_orders_meta_sgtin` — `POST /api/marketplace/v3/dbw/orders/meta/sgtin` — Метод обновляет код маркировки [Честного знака](https://честныйзнак.рф/) в…
- `orders_dbw::dbw_api::post_v3_dbw_orders_status` — `POST /api/v3/dbw/orders/status` — Метод возвращает статусы сборочных заданий по их ID.
- `orders_dbw::dbw_api::post_v3_dbw_orders_status_deliver` — `POST /api/marketplace/v3/dbw/orders/status/deliver` — Метод переводит [сборочные задания](https://dev.wildberries.ru/openapi/orders-dbw#tag/dbwAssemblyOrders/operation/getV3DbwOrders) из…
- `orders_dbw::dbw_api::post_v3_dbw_orders_stickers` — `POST /api/v3/dbw/orders/stickers` — Метод возвращает список стикеров для [сборочных заданий](https://dev.wildberries.ru/openapi/orders-dbw#tag/dbwAssemblyOrders/operation/getV3DbwOrdersNew) в…
- `orders_dbw::dbw_api::put_v3_dbw_orders_order_id_meta_gtin` — `PUT /api/v3/dbw/orders/{orderId}/meta/gtin` — Метод обновляет GTIN, уникальный ID товара в Беларуси, в…
- `orders_dbw::dbw_api::put_v3_dbw_orders_order_id_meta_imei` — `PUT /api/v3/dbw/orders/{orderId}/meta/imei` — Метод обновляет IMEI в [идентификаторах маркировки сборочного задания](https://dev.wildberries.ru/openapi/orders-dbw#tag/dbwLabelIdentifiers/operation/postV3DbwOrdersMetaDetails).
- `orders_dbw::dbw_api::put_v3_dbw_orders_order_id_meta_uin` — `PUT /api/v3/dbw/orders/{orderId}/meta/uin` — Метод обновляет УИН, уникальный идентификационный номер, в…

### dbs (`dbs`)
- `dbs::dbs_api::get_v3_dbs_orders` — `GET /api/v3/dbs/orders` — Метод возвращает информацию о завершенных [сборочных заданиях](https://dev.wildberries.ru/openapi/dbs#tag/dbsAssemblyOrders) после продажи или отмены заказа.
- `dbs::dbs_api::get_v3_dbs_orders_new` — `GET /api/v3/dbs/orders/new` — Метод возвращает список всех новых [сборочных заданий](https://dev.wildberries.ru/openapi/dbs#tag/dbsAssemblyOrders), которые есть у продавца на момент запроса.
- `dbs::dbs_api::post_v3_dbs_groups_info` — `POST /api/v3/dbs/groups/info` — Метод возвращает информацию о платной доставке сборочных заданий, которые поступили на один склад (`warehouseId`) в рамках одной транзакции покупателя (`orderUid`).
- `dbs::dbs_api::post_v3_dbs_orders_b2b_info` — `POST /api/marketplace/v3/dbs/orders/b2b/info` — Метод возвращает данные B2B-покупателей по ID сборочных заданий: - ИНН - КПП - Наименование организации
- `dbs::dbs_api::post_v3_dbs_orders_client` — `POST /api/v3/dbs/orders/client` — Метод возвращает информацию о покупателе по ID сборочных заданий.
- `dbs::dbs_api::post_v3_dbs_orders_delivery_date` — `POST /api/v3/dbs/orders/delivery-date` — Метод возвращает информацию о выбранных покупателем дате и времени доставки заказов.
- `dbs::dbs_api::post_v3_dbs_orders_final_price` — `POST /api/marketplace/v3/dbs/orders/final-price` — Метод возвращает: - цены продавца без учёта скидок - суммы к оплате покупателем с учетом всех скидок и кэшбека
- `dbs::dbs_api::post_v3_dbs_orders_meta_customs_declaration` — `POST /api/marketplace/v3/dbs/orders/meta/customs-declaration` — Метод обновляет номера ДТ — деклараций на товары — и коды стран происхождения товаров в…
- `dbs::dbs_api::post_v3_dbs_orders_meta_delete` — `POST /api/marketplace/v3/dbs/orders/meta/delete` — Метод удаляет значение указанных [идентификаторов маркировки сборочных заданий](https://dev.wildberries.ru/openapi/dbs#tag/dbsLabelIdentifiers/operation/postV3DbsOrdersMetaDetails).
- `dbs::dbs_api::post_v3_dbs_orders_meta_details` — `POST /api/marketplace/v3/dbs/orders/meta/details` — Метод возвращает идентификаторы маркировки [сборочных заданий](https://dev.wildberries.ru/openapi/dbs#tag/dbsAssemblyOrders) и статусы их проверки.
- `dbs::dbs_api::post_v3_dbs_orders_meta_gtin` — `POST /api/marketplace/v3/dbs/orders/meta/gtin` — Метод обновляет GTIN, уникальный ID товара в Беларуси, в…
- `dbs::dbs_api::post_v3_dbs_orders_meta_imei` — `POST /api/marketplace/v3/dbs/orders/meta/imei` — Метод обновляет IMEI в [идентификаторах маркировки сборочных заданий](https://dev.wildberries.ru/openapi/dbs#tag/dbsLabelIdentifiers/operation/postV3DbsOrdersMetaDetails).
- `dbs::dbs_api::post_v3_dbs_orders_meta_sgtin` — `POST /api/marketplace/v3/dbs/orders/meta/sgtin` — Метод обновляет код маркировки [Честного знака](https://честныйзнак.рф/) в…
- `dbs::dbs_api::post_v3_dbs_orders_meta_uin` — `POST /api/marketplace/v3/dbs/orders/meta/uin` — Метод обновляет УИН, уникальные идентификационные номера, в…
- `dbs::dbs_api::post_v3_dbs_orders_status_cancel` — `POST /api/marketplace/v3/dbs/orders/status/cancel` — Метод переводит [сборочные задания](https://dev.wildberries.ru/openapi/dbs#tag/dbsAssemblyOrders) из…
- `dbs::dbs_api::post_v3_dbs_orders_status_confirm` — `POST /api/marketplace/v3/dbs/orders/status/confirm` — Метод переводит [сборочные задания](https://dev.wildberries.ru/openapi/dbs#tag/dbsAssemblyOrders) из…
- `dbs::dbs_api::post_v3_dbs_orders_status_deliver` — `POST /api/marketplace/v3/dbs/orders/status/deliver` — Метод переводит [сборочные задания](https://dev.wildberries.ru/openapi/dbs#tag/dbsAssemblyOrders) из…
- `dbs::dbs_api::post_v3_dbs_orders_status_info` — `POST /api/marketplace/v3/dbs/orders/status/info` — Метод возвращает статусы [сборочных заданий](https://dev.wildberries.ru/openapi/dbs#tag/dbsAssemblyOrders) по их ID.
- `dbs::dbs_api::post_v3_dbs_orders_status_receive` — `POST /api/marketplace/v3/dbs/orders/status/receive` — Метод переводит [сборочные задания](https://dev.wildberries.ru/openapi/dbs#tag/dbsAssemblyOrders) из…
- `dbs::dbs_api::post_v3_dbs_orders_status_reject` — `POST /api/marketplace/v3/dbs/orders/status/reject` — Метод переводит [сборочные задания](https://dev.wildberries.ru/openapi/dbs#tag/dbsAssemblyOrders) из…
- `dbs::dbs_api::post_v3_dbs_orders_stickers` — `POST /api/marketplace/v3/dbs/orders/stickers` — Метод возвращает стикеры для сборочных заданий с доставкой в ПВЗ в [статусах](https://dev.wildberries.ru/openapi/dbs#tag/dbsAssemblyOrders/operation/postV3DbsOrdersStatusInfo): - `confirm` — на…

### in_store_pickup (`in_store_pickup`)
- `in_store_pickup::default_api::get_v3_click_collect_orders` — `GET /api/v3/click-collect/orders` — Метод возвращает информацию о завершённых сборочных заданиях после продажи или отмены заказа.
- `in_store_pickup::default_api::get_v3_click_collect_orders_new` — `GET /api/v3/click-collect/orders/new` — Метод возвращает список всех новых [сборочных заданий](https://dev.wildberries.ru/openapi/in-store-pickup#tag/inStorePickupAssemblyOrders), которые есть у продавца на момент запроса.
- `in_store_pickup::default_api::post_v3_click_collect_orders_client` — `POST /api/v3/click-collect/orders/client` — Метод возвращает информацию о покупателе по ID сборочного задания.
- `in_store_pickup::default_api::post_v3_click_collect_orders_client_identity` — `POST /api/v3/click-collect/orders/client/identity` — Метод сообщает, принадлежит ли проверяемый заказ покупателю или нет по переданному коду.
- `in_store_pickup::default_api::post_v3_click_collect_orders_final_price` — `POST /api/marketplace/v3/click-collect/orders/final-price` — Метод возвращает: - цены продавца без учёта скидок - суммы к оплате покупателем с учетом всех скидок и кэшбека
- `in_store_pickup::default_api::post_v3_click_collect_orders_meta_customs_declaration` — `POST /api/marketplace/v3/click-collect/orders/meta/customs-declaration` — Метод обновляет номера ДТ — деклараций на товары — и коды стран происхождения товаров в…
- `in_store_pickup::default_api::post_v3_click_collect_orders_meta_delete` — `POST /api/marketplace/v3/click-collect/orders/meta/delete` — Метод удаляет значения указанных…
- `in_store_pickup::default_api::post_v3_click_collect_orders_meta_details` — `POST /api/marketplace/v3/click-collect/orders/meta/details` — Метод возвращает идентификаторы маркировки [сборочных заданий ](https://dev.wildberries.ru/openapi/in-store-pickup#tag/inStorePickupAssemblyOrders) и статусы их проверки.
- `in_store_pickup::default_api::post_v3_click_collect_orders_meta_gtin` — `POST /api/marketplace/v3/click-collect/orders/meta/gtin` — Метод обновляет GTIN, уникальный ID товара в Беларуси, в…
- `in_store_pickup::default_api::post_v3_click_collect_orders_meta_imei` — `POST /api/marketplace/v3/click-collect/orders/meta/imei` — Метод обновляет IMEI в…
- `in_store_pickup::default_api::post_v3_click_collect_orders_meta_sgtin` — `POST /api/marketplace/v3/click-collect/orders/meta/sgtin` — Метод обновляет код маркировки [Честного знака](https://честныйзнак.рф/) в…
- `in_store_pickup::default_api::post_v3_click_collect_orders_meta_uin` — `POST /api/marketplace/v3/click-collect/orders/meta/uin` — Метод обновляет УИН, уникальные идентификационные номера, в…
- `in_store_pickup::default_api::post_v3_click_collect_orders_status_cancel` — `POST /api/marketplace/v3/click-collect/orders/status/cancel` — Переводит [сборочные задания](https://dev.wildberries.ru/openapi/in-store-pickup#tag/inStorePickupAssemblyOrders) из…
- `in_store_pickup::default_api::post_v3_click_collect_orders_status_confirm` — `POST /api/marketplace/v3/click-collect/orders/status/confirm` — Метод переводит [сборочные задания](https://dev.wildberries.ru/openapi/in-store-pickup#tag/inStorePickupAssemblyOrders) из…
- `in_store_pickup::default_api::post_v3_click_collect_orders_status_info` — `POST /api/marketplace/v3/click-collect/orders/status/info` — Метод возвращает статусы [сборочных заданий](https://dev.wildberries.ru/openapi/in-store-pickup#tag/inStorePickupAssemblyOrders) по их ID.
- `in_store_pickup::default_api::post_v3_click_collect_orders_status_prepare` — `POST /api/marketplace/v3/click-collect/orders/status/prepare` — Метод переводит [сборочные задания](https://dev.wildberries.ru/openapi/in-store-pickup#tag/inStorePickupAssemblyOrders) из…
- `in_store_pickup::default_api::post_v3_click_collect_orders_status_receive` — `POST /api/marketplace/v3/click-collect/orders/status/receive` — Метод переводит [сборочные задания](https://dev.wildberries.ru/openapi/in-store-pickup#tag/inStorePickupAssemblyOrders) из…
- `in_store_pickup::default_api::post_v3_click_collect_orders_status_reject` — `POST /api/marketplace/v3/click-collect/orders/status/reject` — Метод переводит [сборочные задания](https://dev.wildberries.ru/openapi/in-store-pickup#tag/inStorePickupAssemblyOrders) из…

### orders_fbw (`orders_fbw`)
- `orders_fbw::default_api::delete_v1_drafts_draft_id` — `DELETE /api/supplies/v1/drafts/{draftId}` — Метод удаляет черновик поставки по его ID.
- `orders_fbw::default_api::delete_v1_drafts_draft_id_items` — `DELETE /api/supplies/v1/drafts/{draftId}/items` — Метод удаляет товары из черновика поставки по списку баркодов.
- `orders_fbw::default_api::get_v1_drafts` — `GET /api/supplies/v1/drafts` — Метод возвращает список черновиков поставок.
- `orders_fbw::default_api::get_v1_drafts_draft_id_items` — `GET /api/supplies/v1/drafts/{draftId}/items` — Метод возвращает список товаров черновика.
- `orders_fbw::default_api::get_v1_supplies_id` — `GET /api/v1/supplies/{ID}` — Метод возвращает детали поставки по ID.
- `orders_fbw::default_api::get_v1_supplies_id_goods` — `GET /api/v1/supplies/{ID}/goods` — Метод возвращает информацию о товарах в поставке.
- `orders_fbw::default_api::get_v1_supplies_id_package` — `GET /api/v1/supplies/{ID}/package` — Метод возвращает информацию об упаковке поставки.
- `orders_fbw::default_api::get_v1_supplies_supply_id_discrepancies_quantity` — `GET /api/supplies/v1/discrepancies/{supplyId}` — Метод возвращает информацию о выявленных расхождениях между заявленным и фактическим количеством товара в поставке.
- `orders_fbw::default_api::get_v1_transit_tariffs` — `GET /api/v1/transit-tariffs` — Метод [временно отключён](/release-notes?id=570)
- `orders_fbw::default_api::get_v1_warehouses` — `GET /api/v1/warehouses` — Метод [временно отключён](/release-notes?id=570)
- `orders_fbw::default_api::post_v1_acceptance_options` — `POST /api/v1/acceptance/options` — Метод [временно отключён](/release-notes?id=570)
- `orders_fbw::default_api::post_v1_drafts` — `POST /api/supplies/v1/drafts` — Метод создаёт пустой черновик поставки.
- `orders_fbw::default_api::post_v1_drafts_draft_id_items` — `POST /api/supplies/v1/drafts/{draftId}/items` — Метод добавляет товары в черновик поставки.
- `orders_fbw::default_api::post_v1_supplies` — `POST /api/v1/supplies` — Метод возвращает список поставок, по умолчанию — последние 1000 поставок.

### promotion (`promotion`)
- `promotion::default_api::delete_v0_normquery_bids` — `DELETE /adv/v0/normquery/bids` — Метод удаляет ставки с поисковых кластеров.
- `promotion::default_api::get_v0_bids_recommendations` — `GET /api/advert/v0/bids/recommendations` — Метод возвращает рекомендуемые ставки для карточек товаров и поисковых кластеров кампании.
- `promotion::default_api::get_v0_daily_limits` — `GET /api/advert/v0/daily-limits` — Метод возвращает текущие настройки…
- `promotion::default_api::get_v0_delete` — `GET /adv/v0/delete` — Метод удаляет [кампании](https://dev.wildberries.ru/openapi/promotion#tag/campaigns/operation/getV2Adverts) в статусе `4` — готова к запуску.
- `promotion::default_api::get_v0_pause` — `GET /adv/v0/pause` — Метод ставит [кампании](https://dev.wildberries.ru/openapi/promotion#tag/campaigns/operation/getV2Adverts) в статусе `9` — активна — на паузу.
- `promotion::default_api::get_v0_start` — `GET /adv/v0/start` — Метод запускает [кампании](https://dev.wildberries.ru/openapi/promotion#tag/campaigns/operation/getV2Adverts) в статусах `4` — готово к запуску — или `11` — пауза.
- `promotion::default_api::get_v0_stop` — `GET /adv/v0/stop` — Метод завершает [кампании](https://dev.wildberries.ru/openapi/promotion#tag/campaigns/operation/getV2Adverts) в статусах: - `9` — активна - `11` — пауза
- `promotion::default_api::get_v1_advert` — `GET /adv/v1/advert` — Метод возвращает информацию о кампании [WB Медиа](https://cmp.wildberries.ru/cmpf/list).
- `promotion::default_api::get_v1_adverts` — `GET /adv/v1/adverts` — Метод возвращает список всех [медиакампаний](https://dev.wildberries.ru/openapi/promotion#tag/media/operation/getV1Advert) продавца по их типам и статусам.
- `promotion::default_api::get_v1_balance` — `GET /adv/v1/balance` — Метод возвращает информацию о: - счёте кабинета Продвижения WB.
- `promotion::default_api::get_v1_budget` — `GET /adv/v1/budget`
- `promotion::default_api::get_v1_calendar_promotions` — `GET /api/v1/calendar/promotions` — Метод возвращает список [акций](https://dev.wildberries.ru/openapi/promotion#tag/promoCalendar/operation/getV1CalendarPromotionsDetails) в WB с датами и временем проведения.
- `promotion::default_api::get_v1_calendar_promotions_details` — `GET /api/v1/calendar/promotions/details` — Метод возвращает подробную информацию об [акции](https://dev.wildberries.ru/openapi/promotion#tag/promoCalendar/operation/getV1CalendarPromotionsDetails) по ID.
- `promotion::default_api::get_v1_calendar_promotions_nomenclatures` — `GET /api/v1/calendar/promotions/nomenclatures` — Метод формирует список товаров, подходящих для участия в [акции](https://dev.wildberries.ru/openapi/promotion#tag/promoCalendar/operation/getV1CalendarPromotionsDetails).
- `promotion::default_api::get_v1_config` — `GET /api/advert/v1/config` — Метод возвращает валюту, код валюты [профиля продавца](https://cmp.wildberries.ru/campaigns/finances) и допустимые шаги ставок для метода…
- `promotion::default_api::get_v1_count` — `GET /adv/v1/count` — Метод возвращает количество [медиакампаний](https://dev.wildberries.ru/openapi/promotion#tag/media/operation/getV1Advert) продавца с группировкой по статусам.
- `promotion::default_api::get_v1_payments` — `GET /adv/v1/payments` — Метод возвращает историю пополнений счёта **WB Продвижение** за заданный период.
- `promotion::default_api::get_v1_promotion_count` — `GET /adv/v1/promotion/count` — Метод возвращает списки всех [рекламных кампаний](https://dev.wildberries.ru/openapi/promotion#tag/campaigns/operation/getV2Adverts) продавца с их ID.
- `promotion::default_api::get_v1_supplier_subjects` — `GET /adv/v1/supplier/subjects` — Метод возвращает список [предметов](https://dev.wildberries.ru/openapi/item-management#tag/categoriesSubcategoriesAndCharacteristics/operation/getV2ObjectAll), которые можно добавить в рекламную…
- `promotion::default_api::get_v1_upd` — `GET /adv/v1/upd` — Метод формирует список фактических затрат на рекламные кампании за заданный период.
- `promotion::default_api::get_v2_adverts` — `GET /api/advert/v2/adverts` — Метод возвращает информацию о рекламных кампаниях с единой или ручной ставкой по их статусам, типам оплаты и ID.
- `promotion::default_api::get_v3_fullstats` — `GET /adv/v3/fullstats` — Метод формирует статистику для кампаний независимо от типа.
- `promotion::default_api::patch_v0_auction_nms` — `PATCH /adv/v0/auction/nms` — Метод добавляет и удаляет карточки товаров в кампаниях.
- `promotion::default_api::patch_v1_bids` — `PATCH /api/advert/v1/bids` — Метод меняет ставки карточек товаров по артикулам WB в кампаниях: - с единой ставкой - с ручной ставкой - с моделью оплаты `cpc` — за клики Для кампаний в статусах `4`, `9` и `11`.
- `promotion::default_api::post_v0_normquery_bids` — `POST /adv/v0/normquery/bids` — Метод устанавливает ставки в рублях на поисковые кластеры.
- `promotion::default_api::post_v0_normquery_get_bids` — `POST /adv/v0/normquery/get-bids` — Метод возвращает список поисковых кластеров со ставками по: - ID кампаний - артикулам WB
- `promotion::default_api::post_v0_normquery_get_minus` — `POST /adv/v0/normquery/get-minus` — Метод возвращает список минус-фраз по: - ID кампаний - артикулам WB
- `promotion::default_api::post_v0_normquery_list` — `POST /adv/v0/normquery/list` — Метод возвращает списки активных и неактивных поисковых кластеров, по которым было не меньше 100 показов.
- `promotion::default_api::post_v0_normquery_set_minus` — `POST /adv/v0/normquery/set-minus` — Метод устанавливает и удаляет минус-фразы в кампаниях c единой и ручной ставкой.
- `promotion::default_api::post_v0_normquery_stats` — `POST /adv/v0/normquery/stats` — Метод формирует статистику по поисковым кластерам за указанный период.
- `promotion::default_api::post_v0_rename` — `POST /adv/v0/rename` — Метод меняет название [кампании](https://dev.wildberries.ru/openapi/promotion#tag/campaigns/operation/getV2Adverts).
- `promotion::default_api::post_v1_bids_min` — `POST /api/advert/v1/bids/min` — Метод возвращает минимальные ставки для карточек товаров в разменных единицах — 0,01 от базовой валюты [профиля продавца](https://cmp.wildberries.ru/campaigns/finances) — по типу оплаты и местам…
- `promotion::default_api::post_v1_budget_deposit` — `POST /adv/v1/budget/deposit` — Метод пополняет [бюджет](https://dev.wildberries.ru/openapi/promotion#tag/finances/operation/postV2Budget) кампании.
- `promotion::default_api::post_v1_calendar_promotions_upload` — `POST /api/v1/calendar/promotions/upload` — Метод создаёт задание на загрузку товара в [акцию](https://dev.wildberries.ru/openapi/promotion#tag/promoCalendar/operation/getV1CalendarPromotionsDetails).
- `promotion::default_api::post_v1_normquery_bids` — `POST /api/advert/v1/normquery/bids` — Метод устанавливает ставки на поисковые кластеры в валюте [профиля продавца](https://cmp.wildberries.ru/campaigns/finances).
- `promotion::default_api::post_v1_normquery_stats` — `POST /adv/v1/normquery/stats` — Метод формирует статистику по поисковым кластерам за указанный период с детализацией по дням.
- `promotion::default_api::post_v1_stats` — `POST /adv/v1/stats` — Метод формирует статистику кампаний сервиса [WB Медиа](https://cmp.wildberries.ru/cmpf/statistics).
- `promotion::default_api::post_v2_budget` — `POST /api/advert/v2/budget` — Метод возвращает информацию об остатках бюджетов [кампаний](https://dev.wildberries.ru/openapi/promotion#tag/campaigns/operation/getV2Adverts).
- `promotion::default_api::post_v2_seacat_save_ad` — `POST /adv/v2/seacat/save-ad` — Метод создаёт кампанию: - с ручной ставкой для продвижения товаров в поиске и/или рекомендациях - с единой ставкой для продвижения товаров одновременно в поиске и рекомендациях
- `promotion::default_api::post_v2_supplier_nms` — `POST /adv/v2/supplier/nms` — Метод возвращает список [карточек товаров](https://dev.wildberries.ru/openapi/item-management#tag/listings/operation/postV2GetCardsList), которые можно добавить в рекламную…
- `promotion::default_api::put_v0_auction_placements` — `PUT /adv/v0/auction/placements` — Метод меняет места размещения в кампаниях с ручной ставкой и моделью оплаты за показы — `cpm`.
- `promotion::default_api::put_v0_daily_limits` — `PUT /api/advert/v0/daily-limits` — Метод включает, выключает и обновляет дневной лимит кампаний.

### communications (`communications`)
- `communications::default_api::delete_v1_pins` — `DELETE /api/feedbacks/v1/pins` — Метод позволяет открепить отзывы в карточке товара или в группе…
- `communications::default_api::get_v1_claims` — `GET /api/v1/claims` — Метод возвращает заявки покупателей на возврат товаров за последние 14 дней.
- `communications::default_api::get_v1_feedback` — `GET /api/v1/feedback` — Метод возвращает данные [отзыва](https://dev.wildberries.ru/openapi/customer-communication#tag/feedbacks/operation/getV1Feedbacks) по его ID.
- `communications::default_api::get_v1_feedbacks` — `GET /api/v1/feedbacks` — Метод возвращает список отзывов по заданным фильтрам.
- `communications::default_api::get_v1_feedbacks_archive` — `GET /api/v1/feedbacks/archive` — Метод возвращает список архивных [отзывов](https://dev.wildberries.ru/openapi/customer-communication#tag/feedbacks/operation/getV1Feedbacks).
- `communications::default_api::get_v1_feedbacks_count` — `GET /api/v1/feedbacks/count` — Метод возвращает количество обработанных или необработанных [отзывов](https://dev.wildberries.ru/openapi/customer-communication#tag/feedbacks/operation/getV1Feedbacks) за заданный период.
- `communications::default_api::get_v1_feedbacks_count_unanswered` — `GET /api/v1/feedbacks/count-unanswered` — Метод возвращает: - количество необработанных [отзывов](https://dev.wildberries.ru/openapi/customer-communication#tag/feedbacks/operation/getV1Feedbacks) за сегодня и за всё время
- `communications::default_api::get_v1_new_feedbacks_questions` — `GET /api/v1/new-feedbacks-questions` — Метод проверяет наличие непросмотренных [вопросов](https://dev.wildberries.ru/openapi/customer-communication#tag/questions/operation/getV1Questions) и…
- `communications::default_api::get_v1_pins` — `GET /api/feedbacks/v1/pins` — Метод предоставляет список закреплённых и откреплённых отзывов.
- `communications::default_api::get_v1_pins_count` — `GET /api/feedbacks/v1/pins/count` — Метод возвращает количество закреплённых и откреплённых отзывов за заданный период.
- `communications::default_api::get_v1_pins_limits` — `GET /api/feedbacks/v1/pins/limits` — Метод возвращает лимиты закреплённых отзывов по тарифу и подписке.
- `communications::default_api::get_v1_question` — `GET /api/v1/question` — Метод возвращает данные [вопроса](https://dev.wildberries.ru/openapi/customer-communication#tag/questions/operation/getV1Questions) по его ID.
- `communications::default_api::get_v1_questions` — `GET /api/v1/questions` — Метод возвращает список вопросов по заданным фильтрам.
- `communications::default_api::get_v1_questions_count` — `GET /api/v1/questions/count` — Метод возвращает количество отвеченных или неотвеченных [вопросов](https://dev.wildberries.ru/openapi/customer-communication#tag/questions/operation/getV1Questions) за заданный период.
- `communications::default_api::get_v1_questions_count_unanswered` — `GET /api/v1/questions/count-unanswered` — Метод возвращает общее количество неотвеченных [вопросов](https://dev.wildberries.ru/openapi/customer-communication#tag/questions/operation/getV1Questions) и количество неотвеченных вопросов за…
- `communications::default_api::get_v1_seller_chats` — `GET /api/v1/seller/chats` — Метод возвращает список всех чатов продавца.
- `communications::default_api::get_v1_seller_download_id` — `GET /api/v1/seller/download/{id}` — Метод возвращает файл или изображение из сообщения по его ID.
- `communications::default_api::get_v1_seller_events` — `GET /api/v1/seller/events` — Метод возвращает список событий всех [чатов с покупателями](https://dev.wildberries.ru/openapi/customer-communication#tag/buyersChat/operation/getV1SellerChats).
- `communications::default_api::patch_v1_claim` — `PATCH /api/v1/claim` — Метод отправляет ответ на [заявку](https://dev.wildberries.ru/openapi/customer-communication#tag/buyersReturns/operation/getV1Claims) покупателя на возврат товаров.
- `communications::default_api::patch_v1_feedbacks_answer` — `PATCH /api/v1/feedbacks/answer` — Метод позволяет отредактировать уже отправленный [ответ на отзыв](https://dev.wildberries.ru/openapi/customer-communication#tag/feedbacks/operation/postV1FeedbacksAnswer) покупателя.
- `communications::default_api::patch_v1_questions` — `PATCH /api/v1/questions` — В зависимости от тела запроса, метод позволяет: - отметить [вопрос](https://dev.wildberries.ru/openapi/customer-communication#tag/questions/operation/getV1Questions) как просмотренный - отклонить…
- `communications::default_api::post_v1_feedbacks_answer` — `POST /api/v1/feedbacks/answer` — Метод позволяет ответить на [отзыв](https://dev.wildberries.ru/openapi/customer-communication#tag/feedbacks/operation/getV1Feedbacks) покупателя.
- `communications::default_api::post_v1_feedbacks_order_return` — `POST /api/v1/feedbacks/order/return` — Метод запрашивает возврат товара, по которому оставлен [отзыв](https://dev.wildberries.ru/openapi/customer-communication#tag/feedbacks/operation/getV1Feedbacks).
- `communications::default_api::post_v1_pins` — `POST /api/feedbacks/v1/pins` — Метод позволяет закрепить отзывы в карточке товара или в группе…
- `communications::default_api::post_v1_seller_message` — `POST /api/v1/seller/message` — Метод отправляет сообщения в [чат с покупателем](https://dev.wildberries.ru/openapi/customer-communication#tag/buyersChat/operation/getV1SellerChats).

### rates (`rates`)
- `rates::default_api::get_v1_acceptance_coefficients` — `GET /api/tariffs/v1/acceptance/coefficients` — Метод [временно отключён](/release-notes?id=570)
- `rates::default_api::get_v1_tariffs_box` — `GET /api/v1/tariffs/box` — Для остатков товаров, которые поставляются на склад в коробах, метод возвращает [тарифы](https://seller.wildberries.ru/dynamic-product-categories) на: - доставку со склада или пункта приёма до…
- `rates::default_api::get_v1_tariffs_commission` — `GET /api/v1/tariffs/commission` — Метод возвращает данные о [комиссии](https://seller.wildberries.ru/dynamic-product-categories/commission) WB по…
- `rates::default_api::get_v1_tariffs_pallet` — `GET /api/v1/tariffs/pallet` — Для товаров, которые поставляются на склад WB на монопаллетах, метод возвращает [стоимость](https://seller.wildberries.ru/dynamic-product-categories): - доставки со склада до покупателя - доставки от…
- `rates::default_api::get_v1_tariffs_return` — `GET /api/v1/tariffs/return` — Метод возвращает [тарифы](https://seller.wildberries.ru/dynamic-product-categories/return-cost): - на перевозку товаров со склада WB или из пункта приёма до продавца - на обратную перевозку…

### analytics (`analytics`)
- `analytics::csv_api::get_v2_nm_report_downloads` — `GET /api/v2/nm-report/downloads` — Метод возвращает список отчётов с расширенной аналитикой продавца.
- `analytics::csv_api::get_v2_nm_report_downloads_file_download_id` — `GET /api/v2/nm-report/downloads/file/{downloadId}` — Метод возвращает отчёт с расширенной аналитикой продавца по ID [задания на генерацию](https://dev.wildberries.ru/openapi/analytics#tag/sellerAnalyticsCsv/operation/postV2NmReportDownloads).
- `analytics::csv_api::post_v2_nm_report_downloads` — `POST /api/v2/nm-report/downloads` — Метод создаёт задание на генерацию отчёта с расширенной аналитикой продавца.
- `analytics::csv_api::post_v2_nm_report_downloads_retry` — `POST /api/v2/nm-report/downloads/retry` — Метод создает повторное [задание на генерацию](https://dev.wildberries.ru/openapi/analytics#tag/sellerAnalyticsCsv/operation/postV2NmReportDownloads) отчёта с расширенной аналитикой продавца.
- `analytics::default_api::post_v1_order_feed` — `POST /api/analytics/v1/order-feed` — Метод формирует набор данных о заказах и продажах.
- `analytics::default_api::post_v1_stocks_report_seller_warehouses` — `POST /api/analytics/v1/stocks-report/seller-warehouses` — Метод возвращает текущие остатки товаров на складах продавца.
- `analytics::default_api::post_v1_stocks_report_wb_warehouses` — `POST /api/analytics/v1/stocks-report/wb-warehouses` — Метод возвращает текущие остатки товаров на складах WB.
- `analytics::default_api::post_v2_item_rating` — `POST /api/analytics/v2/item-rating` — Метод формирует набор данных об оценках товаров.
- `analytics::default_api::post_v2_search_report_product_orders` — `POST /api/v2/search-report/product/orders` — Метод формирует данные для таблицы: - о заказах по каждому поисковому запросу для конкретного товара - о позициях товара в результатах поиска по каждому запросу Данные указаны в рамках периода для…
- `analytics::default_api::post_v2_search_report_product_search_texts` — `POST /api/v2/search-report/product/search-texts` — Метод формирует топ поисковых запросов по товару.
- `analytics::default_api::post_v2_search_report_report` — `POST /api/v2/search-report/report` — Метод формирует набор данных для основной страницы отчёта по поисковым запросам с: - общей информацией - позициями товаров - данными по видимости и переходам в карточку - данными для таблицы по…
- `analytics::default_api::post_v2_search_report_table_details` — `POST /api/v2/search-report/table/details` — Метод формирует дополнительные данные к [основному отчёту](https://dev.wildberries.ru/openapi/analytics#tag/searchQueriesForYourItems/operation/postV2SearchReportReport) с пагинацией по товарам в…
- `analytics::default_api::post_v2_search_report_table_groups` — `POST /api/v2/search-report/table/groups` — Метод формирует дополнительные данные к [основному отчёту](https://dev.wildberries.ru/openapi/analytics#tag/searchQueriesForYourItems/operation/postV2SearchReportReport) с пагинацией по группам.
- `analytics::default_api::post_v2_stocks_report_offices` — `POST /api/v2/stocks-report/offices` — Метод формирует набор данных об остатках по складам.
- `analytics::default_api::post_v2_stocks_report_products_groups` — `POST /api/v2/stocks-report/products/groups` — Метод формирует набор данных об остатках по группам товаров.
- `analytics::default_api::post_v2_stocks_report_products_products` — `POST /api/v2/stocks-report/products/products` — Метод формирует набор данных об остатках по товарам.
- `analytics::default_api::post_v2_stocks_report_products_sizes` — `POST /api/v2/stocks-report/products/sizes` — Метод формирует набор данных об остатках по размерам товара.
- `analytics::default_api::post_v3_sales_funnel_grouped_history` — `POST /api/analytics/v3/sales-funnel/grouped/history` — Метод возвращает статистику карточек товаров по дням или неделям.
- `analytics::default_api::post_v3_sales_funnel_products` — `POST /api/analytics/v3/sales-funnel/products` — Метод формирует отчёт о товарах, сравнивая ключевые показатели за текущий период с аналогичным прошлым.
- `analytics::default_api::post_v3_sales_funnel_products_history` — `POST /api/analytics/v3/sales-funnel/products/history` — Метод возвращает статистику карточек товаров по дням или неделям.

### reports (`reports`)
- `reports::c_api::post_v1_analytics_excise_report` — `POST /api/v1/analytics/excise-report` — Метод возвращает отчёт с [операциями по товарам с обязательной маркировкой](https://seller.wildberries.ru/analytics-reports/excise-report).
- `reports::default_api::get_v1_acceptance_report` — `GET /api/v1/acceptance_report` — Метод создаёт [задание на генерацию](https://dev.wildberries.ru/openapi/reports#tag/acceptanceExpenses/operation/getV1AcceptanceReportTasksTaskIdStatus) отчёта об…
- `reports::default_api::get_v1_acceptance_report_tasks_task_id_download` — `GET /api/v1/acceptance_report/tasks/{task_id}/download` — Метод возвращает отчёт об [операциях при приёмке](https://seller.wildberries.ru/analytics-reports/acceptance-report) по ID…
- `reports::default_api::get_v1_acceptance_report_tasks_task_id_status` — `GET /api/v1/acceptance_report/tasks/{task_id}/status` — Метод возвращает статус [задания на генерацию](https://dev.wildberries.ru/openapi/reports#tag/acceptanceExpenses/operation/getV1AcceptanceReport) отчёта об…
- `reports::default_api::get_v1_analytics_antifraud_details` — `GET /api/v1/analytics/antifraud-details` — Метод возвращает отчёт об удержаниях за самовыкупы.
- `reports::default_api::get_v1_analytics_banned_producs_blocked` — `GET /api/v1/analytics/banned-products/blocked` — Метод возвращает список [заблокированных карточек товаров продавца](https://seller.wildberries.ru/analytics-reports/banned-products) с причинами блокировки.
- `reports::default_api::get_v1_analytics_brand_share` — `GET /api/v1/analytics/brand-share` — Метод возвращает отчёт о [доле бренда продавца в продажах](https://seller.wildberries.ru/analytics-reports/brand-share).
- `reports::default_api::get_v1_analytics_brand_share_brands` — `GET /api/v1/analytics/brand-share/brands` — Метод возвращает список брендов продавца для отчёта о [доле бренда в продажах](https://seller.wildberries.ru/analytics-reports/brand-share).
- `reports::default_api::get_v1_analytics_brand_share_parent_subjects` — `GET /api/v1/analytics/brand-share/parent-subjects` — Метод возвращает родительские категории бренда продавца для отчёта о [доле бренда в продажах](https://seller.wildberries.ru/analytics-reports/brand-share).
- `reports::default_api::get_v1_analytics_goods_labeling` — `GET /api/v1/analytics/goods-labeling` — Метод возвращает отчёт о штрафах за отсутствие обязательной маркировки товаров.
- `reports::default_api::get_v1_analytics_goods_return` — `GET /api/v1/analytics/goods-return`
- `reports::default_api::get_v1_analytics_region_sale` — `GET /api/v1/analytics/region-sale`
- `reports::default_api::get_v1_deductions` — `GET /api/analytics/v1/deductions` — Метод возвращает отчёт об удержаниях за [подмены и неверные вложения](https://seller.wildberries.ru/analytics-reports/dimensions-penalties/retentions)
- `reports::default_api::get_v1_goods_return` — `GET /api/analytics/v1/item-returns` — Метод возвращает отчёт о [возвратах товаров продавцу](https://seller.wildberries.ru/return-transfer-reports).
- `reports::default_api::get_v1_measurement_penalties` — `GET /api/analytics/v1/measurement-penalties` — Метод возвращает отчёт об [удержаниях за занижение габаритов упаковки](https://seller.wildberries.ru/analytics-reports/dimensions-penalties)
- `reports::default_api::get_v1_paid_storage` — `GET /api/v1/paid_storage` — Метод создаёт [задание на генерацию](https://dev.wildberries.ru/openapi/reports#tag/paidStorage/operation/getV1PaidStorageTasksTaskIdStatus) отчёта о…
- `reports::default_api::get_v1_paid_storage_tasks_task_id_download` — `GET /api/v1/paid_storage/tasks/{task_id}/download` — Метод возвращает отчёт о [платном хранении](https://seller.wildberries.ru/analytics-reports/paid-storage/storage) по ID…
- `reports::default_api::get_v1_paid_storage_tasks_task_id_status` — `GET /api/v1/paid_storage/tasks/{task_id}/status` — Метод возвращает статус [задания на генерацию](https://dev.wildberries.ru/openapi/reports#tag/paidStorage/operation/getV1PaidStorage) отчёта о…
- `reports::default_api::get_v1_supplier_orders` — `GET /api/v1/supplier/orders` — Метод возвращает информацию о заказах.
- `reports::default_api::get_v1_supplier_sales` — `GET /api/v1/supplier/sales` — Метод возвращает информацию о продажах и возвратах.
- `reports::default_api::get_v1_warehouse_measurements` — `GET /api/analytics/v1/warehouse-measurements` — Метод возвращает отчёт о [замерах склада](https://seller.wildberries.ru/analytics-reports/dimensions-penalties/warehouse-measurements)
- `reports::default_api::get_v1_warehouse_remains` — `GET /api/v1/warehouse_remains` — Метод создаёт [задание на генерацию](https://dev.wildberries.ru/openapi/reports#tag/warehousesInventoryReport/operation/getV1WarehouseRemainsTasksTaskIdStatus) отчёта об…
- `reports::default_api::get_v1_warehouse_remains_tasks_task_id_download` — `GET /api/v1/warehouse_remains/tasks/{task_id}/download` — Метод возвращает отчёт об [остатках на складах WB](https://seller.wildberries.ru/analytics-reports/warehouse-remains) по ID…
- `reports::default_api::get_v1_warehouse_remains_tasks_task_id_status` — `GET /api/v1/warehouse_remains/tasks/{task_id}/status` — Метод возвращает статус [задания на генерацию](https://dev.wildberries.ru/openapi/reports#tag/warehousesInventoryReport/operation/getV1WarehouseRemains) отчёта об…

### finances (`finances`)
- `finances::default_api::get_v1_account_balance` — `GET /api/v1/account/balance` — Метод возвращает данные виджета баланса на [главной странице](https://seller.wildberries.ru) портала продавцов.
- `finances::default_api::get_v1_documents_categories` — `GET /api/v1/documents/categories` — Метод возвращает категории документов для получения [списка документов продавца](https://dev.wildberries.ru/openapi/documents-and-accounting#tag/documents/operation/getV1DocumentsList).
- `finances::default_api::get_v1_documents_download` — `GET /api/v1/documents/download` — Метод загружает один документ из [списка документов продавца](https://dev.wildberries.ru/openapi/documents-and-accounting#tag/documents/operation/getV1DocumentsList).
- `finances::default_api::get_v1_documents_list` — `GET /api/v1/documents/list` — Метод возвращает список документов продавца.
- `finances::default_api::post_v1_acquiring_detailed` — `POST /api/finance/v1/acquiring/detailed` — Метод возвращает детализации к [отчётам об издержках на приём платежей](https://seller.wildberries.ru/suppliers-mutual-settlements/reports-implementations/acquiring-reports) за указанный период.
- `finances::default_api::post_v1_acquiring_detailed_report_id` — `POST /api/finance/v1/acquiring/detailed/{reportId}` — Метод возвращает детализации к [отчётам об издержках на приём платежей](https://seller.wildberries.ru/suppliers-mutual-settlements/reports-implementations/acquiring-reports) по ID отчётов.
- `finances::default_api::post_v1_acquiring_list` — `POST /api/finance/v1/acquiring/list` — Метод возвращает список отчётов об издержках на приём платежей по формату [таблицы отчётов](https://seller.wildberries.ru/suppliers-mutual-settlements/reports-implementations/acquiring-reports).
- `finances::default_api::post_v1_documents_download_all` — `POST /api/v1/documents/download/all` — Метод загружает несколько документов из [списка документов продавца](https://dev.wildberries.ru/openapi/documents-and-accounting#tag/documents/operation/getV1DocumentsList).
- `finances::default_api::post_v1_sales_reports_detailed` — `POST /api/finance/v1/sales-reports/detailed` — Метод возвращает детализации к [отчётам реализации](https://seller.wildberries.ru/suppliers-mutual-settlements) за указанный период.
- `finances::default_api::post_v1_sales_reports_detailed_report_id` — `POST /api/finance/v1/sales-reports/detailed/{reportId}` — Метод возвращает детализации к [отчётам реализации](https://seller.wildberries.ru/suppliers-mutual-settlements) по ID отчётов.
- `finances::default_api::post_v1_sales_reports_list` — `POST /api/finance/v1/sales-reports/list` — Метод возвращает список отчётов релизации по формату [таблицы отчётов](https://seller.wildberries.ru/suppliers-mutual-settlements).
<!-- RUST_METHODS_LIST_END -->
