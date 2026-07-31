# wildberries-sdk (PHP)

Сгенерированные PHP-клиенты находятся в `clients/php/<module>`.

📖 **Документация:** <https://eslazarev.github.io/wildberries-sdk/> — справочник по всем операциям API с примерами вызова.

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

```bash
composer require eslazarev/wildberries-sdk
```

## Пример (communications)

```php
<?php

use GuzzleHttp\Client;
use Wildberries\Sdk\Communications\Api\DefaultApi;
use Wildberries\Sdk\Communications\Configuration;

$token = getenv("WB_API_TOKEN");

$config = Configuration::getDefaultConfiguration()
    ->setHost("https://feedbacks-api.wildberries.ru")
    ->setApiKey("Authorization", $token);

$api = new DefaultApi(new Client(), $config);
$response = $api->apiV1FeedbacksGet(true, 100, 0);

var_dump($response);
```

## Доступные клиенты

- `Wildberries\Sdk\General`
- `Wildberries\Sdk\Items`
- `Wildberries\Sdk\OrdersFbs`
- `Wildberries\Sdk\OrdersDbw`
- `Wildberries\Sdk\OrdersDbs`
- `Wildberries\Sdk\InStorePickup`
- `Wildberries\Sdk\OrdersFbw`
- `Wildberries\Sdk\Promotion`
- `Wildberries\Sdk\Communications`
- `Wildberries\Sdk\Tariffs`
- `Wildberries\Sdk\Analytics`
- `Wildberries\Sdk\Reports`
- `Wildberries\Sdk\Finances`
- `Wildberries\Sdk\Wbd`

<!-- PHP_METHODS_LIST_START -->
## Методы API

### general (`general`)
- `general.APIApi.getV2News` — `GET /api/communications/v2/news` — Получение новостей портала продавцов
- `general.DefaultApi.deleteV1User` — `DELETE /api/v1/user` — Удалить пользователя
- `general.DefaultApi.getV1Rating` — `GET /api/common/v1/rating` — Получить рейтинг продавца
- `general.DefaultApi.getV1SellerInfo` — `GET /api/v1/seller-info` — Получить информацию о продавце
- `general.DefaultApi.getV1Subscriptions` — `GET /api/common/v1/subscriptions` — Получить информацию о подписке Джем
- `general.DefaultApi.getV1TariffConstructorOptions` — `GET /api/common/v1/tariff-constructor/options` — Получить информацию об опциях Конструктора тарифов
- `general.DefaultApi.getV1Users` — `GET /api/v1/users` — Получить список активных или приглашённых пользователей продавца
- `general.DefaultApi.postV1Invite` — `POST /api/v1/invite` — Создать приглашение для нового пользователя
- `general.DefaultApi.putV1UsersAccess` — `PUT /api/v1/users/access` — Изменить права доступа пользователей
- `general.WBAPIApi.getPing` — `GET /ping` — Проверка подключения

### items (`items`)
- `items.DefaultApi.apiContentV1BrandsGet` — `GET /api/content/v1/brands` — Бренды
- `items.DefaultApi.apiV2BufferGoodsTaskGet` — `GET /api/v2/buffer/goods/task` — Детализация необработанной загрузки
- `items.DefaultApi.apiV2BufferTasksGet` — `GET /api/v2/buffer/tasks` — Состояние необработанной загрузки
- `items.DefaultApi.apiV2HistoryGoodsTaskGet` — `GET /api/v2/history/goods/task` — Детализация обработанной загрузки
- `items.DefaultApi.apiV2HistoryTasksGet` — `GET /api/v2/history/tasks` — Состояние обработанной загрузки
- `items.DefaultApi.apiV2ListGoodsFilterGet` — `GET /api/v2/list/goods/filter` — Получить товары с ценами
- `items.DefaultApi.apiV2ListGoodsFilterPost` — `POST /api/v2/list/goods/filter` — Получить товары с ценами по артикулам
- `items.DefaultApi.apiV2ListGoodsSizeNmGet` — `GET /api/v2/list/goods/size/nm` — Получить размеры товара с ценами
- `items.DefaultApi.apiV2QuarantineGoodsGet` — `GET /api/v2/quarantine/goods` — Получить товары в карантине
- `items.DefaultApi.apiV2UploadTaskClubDiscountPost` — `POST /api/v2/upload/task/club-discount` — Установить скидки WB Клуба
- `items.DefaultApi.apiV2UploadTaskPost` — `POST /api/v2/upload/task` — Установить цены и скидки
- `items.DefaultApi.apiV2UploadTaskSizePost` — `POST /api/v2/upload/task/size` — Установить цены для размеров
- `items.DefaultApi.apiV3DbwWarehousesWarehouseIdContactsGet` — `GET /api/v3/dbw/warehouses/{warehouseId}/contacts` — Список контактов
- `items.DefaultApi.apiV3DbwWarehousesWarehouseIdContactsPut` — `PUT /api/v3/dbw/warehouses/{warehouseId}/contacts` — Обновить список контактов
- `items.DefaultApi.apiV3OfficesGet` — `GET /api/v3/offices` — Получить список складов WB
- `items.DefaultApi.apiV3StocksWarehouseIdDelete` — `DELETE /api/v3/stocks/{warehouseId}` — Удалить остатки товаров
- `items.DefaultApi.apiV3StocksWarehouseIdPost` — `POST /api/v3/stocks/{warehouseId}` — Получить остатки товаров
- `items.DefaultApi.apiV3StocksWarehouseIdPut` — `PUT /api/v3/stocks/{warehouseId}` — Обновить остатки товаров
- `items.DefaultApi.apiV3WarehousesGet` — `GET /api/v3/warehouses` — Получить список складов продавца
- `items.DefaultApi.apiV3WarehousesPost` — `POST /api/v3/warehouses` — Создать склад продавца
- `items.DefaultApi.apiV3WarehousesWarehouseIdDelete` — `DELETE /api/v3/warehouses/{warehouseId}` — Удалить склад продавца
- `items.DefaultApi.apiV3WarehousesWarehouseIdPut` — `PUT /api/v3/warehouses/{warehouseId}` — Обновить склад продавца
- `items.DefaultApi.contentV2BarcodesPost` — `POST /content/v2/barcodes` — Генерация баркодов
- `items.DefaultApi.contentV2CardsDeleteTrashPost` — `POST /content/v2/cards/delete/trash` — Перенос карточек товаров в корзину
- `items.DefaultApi.contentV2CardsErrorListPost` — `POST /content/v2/cards/error/list` — Список несозданных карточек товаров с ошибками
- `items.DefaultApi.contentV2CardsLimitsGet` — `GET /content/v2/cards/limits` — Лимиты карточек товаров
- `items.DefaultApi.contentV2CardsMoveNmPost` — `POST /content/v2/cards/moveNm` — Объединение и разъединение карточек товаров
- `items.DefaultApi.contentV2CardsRecoverPost` — `POST /content/v2/cards/recover` — Восстановление карточек товаров из корзины
- `items.DefaultApi.contentV2CardsUpdatePost` — `POST /content/v2/cards/update` — Редактирование карточек товаров
- `items.DefaultApi.contentV2CardsUploadAddPost` — `POST /content/v2/cards/upload/add` — Создание карточек товаров с присоединением
- `items.DefaultApi.contentV2CardsUploadPost` — `POST /content/v2/cards/upload` — Создание карточек товаров
- `items.DefaultApi.contentV2DirectoryColorsGet` — `GET /content/v2/directory/colors` — Цвет
- `items.DefaultApi.contentV2DirectoryCountriesGet` — `GET /content/v2/directory/countries` — Страна производства
- `items.DefaultApi.contentV2DirectoryKindsGet` — `GET /content/v2/directory/kinds` — Пол
- `items.DefaultApi.contentV2DirectorySeasonsGet` — `GET /content/v2/directory/seasons` — Сезон
- `items.DefaultApi.contentV2DirectoryTnvedGet` — `GET /content/v2/directory/tnved` — ТНВЭД-код
- `items.DefaultApi.contentV2DirectoryVatGet` — `GET /content/v2/directory/vat` — Ставка НДС
- `items.DefaultApi.contentV2GetCardsListPost` — `POST /content/v2/get/cards/list` — Список карточек товаров
- `items.DefaultApi.contentV2GetCardsTrashPost` — `POST /content/v2/get/cards/trash` — Список карточек товаров в корзине
- `items.DefaultApi.contentV2ObjectAllGet` — `GET /content/v2/object/all` — Список предметов
- `items.DefaultApi.contentV2ObjectCharcsSubjectIdGet` — `GET /content/v2/object/charcs/{subjectId}` — Характеристики предмета
- `items.DefaultApi.contentV2ObjectParentAllGet` — `GET /content/v2/object/parent/all` — Родительские категории товаров
- `items.DefaultApi.contentV2TagIdDelete` — `DELETE /content/v2/tag/{id}` — Удаление ярлыка
- `items.DefaultApi.contentV2TagIdPatch` — `PATCH /content/v2/tag/{id}` — Изменение ярлыка
- `items.DefaultApi.contentV2TagNomenclatureLinkPost` — `POST /content/v2/tag/nomenclature/link` — Управление ярлыками в карточке товара
- `items.DefaultApi.contentV2TagPost` — `POST /content/v2/tag` — Создание ярлыка
- `items.DefaultApi.contentV2TagsGet` — `GET /content/v2/tags` — Список ярлыков
- `items.DefaultApi.contentV3MediaFilePost` — `POST /content/v3/media/file` — Загрузить медиафайл
- `items.DefaultApi.contentV3MediaSavePost` — `POST /content/v3/media/save` — Загрузить медиафайлы по ссылкам
- `items.DefaultApi.postV1RecommendationsList` — `POST /api/content/v1/recommendations/list` — Список рекомендаций в карточках товаров
- `items.DefaultApi.postV1RecommendationsSet` — `POST /api/content/v1/recommendations/set` — Установить рекомендации для товаров
- `items.DefaultApi.postV1UploadTaskB2bWholesale` — `POST /api/discounts-prices/v1/upload/task/b2b/wholesale` — Установить оптовые скидки для B2B-продаж

### orders_fbs (`orders_fbs`)
- `orders_fbs.DefaultApi.getV3SettingsAutoreturns` — `GET /api/marketplace/v3/fbs/settings/autoreturns` — Получить настройки автовозврата продавца
- `orders_fbs.DefaultApi.getV3SettingsAutoreturnsSubcategoriesRestricted` — `GET /api/marketplace/v3/fbs/settings/autoreturns/subcategories/restricted` — Получить предметы, которые не хранятся на складах WB
- `orders_fbs.DefaultApi.patchV3SettingsAutoreturns` — `PATCH /api/marketplace/v3/fbs/settings/autoreturns` — Обновить настройки автовозврата продавца
- `orders_fbs.DefaultApi.patchV3SettingsAutoreturnsItems` — `PATCH /api/marketplace/v3/fbs/settings/autoreturns/items` — Обновить настройки автовозврата товаров
- `orders_fbs.DefaultApi.postV3SettingsAutoreturnsItems` — `POST /api/marketplace/v3/fbs/settings/autoreturns/items` — Получить настройки автовозврата товаров
- `orders_fbs.FBSApi.apiMarketplaceV3FbsOrdersArchiveGet` — `GET /api/marketplace/v3/fbs/orders/archive` — Получить список архивных сборочных заданий
- `orders_fbs.FBSApi.apiMarketplaceV3OrdersMetaPost` — `POST /api/marketplace/v3/orders/meta` — Получить идентификаторы маркировки сборочных заданий
- `orders_fbs.FBSApi.apiMarketplaceV3OrdersOrderIdMetaCustomsDeclarationPut` — `PUT /api/marketplace/v3/orders/{orderId}/meta/customs-declaration` — Закрепить номер ДТ за сборочным заданием
- `orders_fbs.FBSApi.apiMarketplaceV3SuppliesSupplyIdOrderIdsGet` — `GET /api/marketplace/v3/supplies/{supplyId}/order-ids` — Получить ID сборочных заданий поставки
- `orders_fbs.FBSApi.apiMarketplaceV3SuppliesSupplyIdOrdersPatch` — `PATCH /api/marketplace/v3/supplies/{supplyId}/orders` — Добавить сборочные задания к поставке
- `orders_fbs.FBSApi.apiV3OrdersClientPost` — `POST /api/v3/orders/client` — Заказы с информацией по клиенту
- `orders_fbs.FBSApi.apiV3OrdersGet` — `GET /api/v3/orders` — Получить информацию о сборочных заданиях
- `orders_fbs.FBSApi.apiV3OrdersNewGet` — `GET /api/v3/orders/new` — Получить список новых сборочных заданий
- `orders_fbs.FBSApi.apiV3OrdersOrderIdCancelPatch` — `PATCH /api/v3/orders/{orderId}/cancel` — Отменить сборочное задание
- `orders_fbs.FBSApi.apiV3OrdersOrderIdMetaDelete` — `DELETE /api/v3/orders/{orderId}/meta` — Удалить идентификаторы маркировки сборочного задания
- `orders_fbs.FBSApi.apiV3OrdersOrderIdMetaExpirationPut` — `PUT /api/v3/orders/{orderId}/meta/expiration` — Закрепить за сборочным заданием срок годности товара
- `orders_fbs.FBSApi.apiV3OrdersOrderIdMetaGtinPut` — `PUT /api/v3/orders/{orderId}/meta/gtin` — Закрепить GTIN за сборочным заданием
- `orders_fbs.FBSApi.apiV3OrdersOrderIdMetaImeiPut` — `PUT /api/v3/orders/{orderId}/meta/imei` — Закрепить IMEI за сборочным заданием
- `orders_fbs.FBSApi.apiV3OrdersOrderIdMetaSgtinPut` — `PUT /api/v3/orders/{orderId}/meta/sgtin` — Закрепить код маркировки Честного знака за сборочным заданием
- `orders_fbs.FBSApi.apiV3OrdersOrderIdMetaUinPut` — `PUT /api/v3/orders/{orderId}/meta/uin` — Закрепить УИН за сборочным заданием
- `orders_fbs.FBSApi.apiV3OrdersStatusHistoryPost` — `POST /api/v3/orders/status/history` — История статусов для сборочных заданий трансграничных поставок
- `orders_fbs.FBSApi.apiV3OrdersStatusPost` — `POST /api/v3/orders/status` — Получить статусы сборочных заданий
- `orders_fbs.FBSApi.apiV3OrdersStickersCrossBorderPost` — `POST /api/v3/orders/stickers/cross-border` — Получить стикеры сборочных заданий трансграничных поставок
- `orders_fbs.FBSApi.apiV3OrdersStickersPost` — `POST /api/v3/orders/stickers` — Получить стикеры сборочных заданий
- `orders_fbs.FBSApi.apiV3PassesGet` — `GET /api/v3/passes` — Получить список пропусков
- `orders_fbs.FBSApi.apiV3PassesOfficesGet` — `GET /api/v3/passes/offices` — Получить список складов, для которых требуется пропуск
- `orders_fbs.FBSApi.apiV3PassesPassIdDelete` — `DELETE /api/v3/passes/{passId}` — Удалить пропуск
- `orders_fbs.FBSApi.apiV3PassesPassIdPut` — `PUT /api/v3/passes/{passId}` — Обновить пропуск
- `orders_fbs.FBSApi.apiV3PassesPost` — `POST /api/v3/passes` — Создать пропуск
- `orders_fbs.FBSApi.apiV3SuppliesGet` — `GET /api/v3/supplies` — Получить список поставок
- `orders_fbs.FBSApi.apiV3SuppliesOrdersReshipmentGet` — `GET /api/v3/supplies/orders/reshipment` — Получить все сборочные задания для повторной отгрузки
- `orders_fbs.FBSApi.apiV3SuppliesPost` — `POST /api/v3/supplies` — Создать новую поставку
- `orders_fbs.FBSApi.apiV3SuppliesSupplyIdBarcodeGet` — `GET /api/v3/supplies/{supplyId}/barcode` — Получить QR-код поставки
- `orders_fbs.FBSApi.apiV3SuppliesSupplyIdDelete` — `DELETE /api/v3/supplies/{supplyId}` — Удалить поставку
- `orders_fbs.FBSApi.apiV3SuppliesSupplyIdDeliverPatch` — `PATCH /api/v3/supplies/{supplyId}/deliver` — Передать поставку в доставку
- `orders_fbs.FBSApi.apiV3SuppliesSupplyIdGet` — `GET /api/v3/supplies/{supplyId}` — Получить информацию о поставке
- `orders_fbs.FBSApi.apiV3SuppliesSupplyIdTrbxDelete` — `DELETE /api/v3/supplies/{supplyId}/trbx` — Удалить грузоместа из поставки
- `orders_fbs.FBSApi.apiV3SuppliesSupplyIdTrbxGet` — `GET /api/v3/supplies/{supplyId}/trbx` — Получить список грузомест поставки
- `orders_fbs.FBSApi.apiV3SuppliesSupplyIdTrbxPost` — `POST /api/v3/supplies/{supplyId}/trbx` — Добавить грузоместа к поставке
- `orders_fbs.FBSApi.apiV3SuppliesSupplyIdTrbxStickersPost` — `POST /api/v3/supplies/{supplyId}/trbx/stickers` — Получить стикеры грузомест поставки

### orders_dbw (`orders_dbw`)
- `orders_dbw.DBWApi.getV3DbwOrders` — `GET /api/v3/dbw/orders` — Получить информацию о завершенных сборочных заданиях
- `orders_dbw.DBWApi.getV3DbwOrdersNew` — `GET /api/v3/dbw/orders/new` — Получить список новых сборочных заданий
- `orders_dbw.DBWApi.getV3DbwOrdersOrderIdMeta` — `GET /api/v3/dbw/orders/{orderId}/meta` — Получить идентификаторы маркировки сборочного задания
- `orders_dbw.DBWApi.patchV3DbwOrdersOrderIdCancel` — `PATCH /api/v3/dbw/orders/{orderId}/cancel` — Отменить сборочное задание
- `orders_dbw.DBWApi.patchV3DbwOrdersOrderIdConfirm` — `PATCH /api/v3/dbw/orders/{orderId}/confirm` — Перевести на сборку
- `orders_dbw.DBWApi.postV3DbwOrdersClient` — `POST /api/marketplace/v3/dbw/orders/client` — Информация о покупателе
- `orders_dbw.DBWApi.postV3DbwOrdersCourier` — `POST /api/v3/dbw/orders/courier` — Информация о курьере
- `orders_dbw.DBWApi.postV3DbwOrdersDeliveryDate` — `POST /api/v3/dbw/orders/delivery-date` — Получить дату и время доставки
- `orders_dbw.DBWApi.postV3DbwOrdersMetaDelete` — `POST /api/marketplace/v3/dbw/orders/meta/delete` — Удалить идентификаторы маркировки сборочных заданий
- `orders_dbw.DBWApi.postV3DbwOrdersMetaDetails` — `POST /api/marketplace/v3/dbw/orders/meta/details` — Получить идентификаторы маркировки сборочных заданий
- `orders_dbw.DBWApi.postV3DbwOrdersMetaSgtin` — `POST /api/marketplace/v3/dbw/orders/meta/sgtin` — Закрепить коды маркировки Честного знака за сборочными заданиями
- `orders_dbw.DBWApi.postV3DbwOrdersStatus` — `POST /api/v3/dbw/orders/status` — Получить статусы сборочных заданий
- `orders_dbw.DBWApi.postV3DbwOrdersStatusDeliver` — `POST /api/marketplace/v3/dbw/orders/status/deliver` — Перевести сборочные задания в доставку
- `orders_dbw.DBWApi.postV3DbwOrdersStickers` — `POST /api/v3/dbw/orders/stickers` — Получить стикеры сборочных заданий
- `orders_dbw.DBWApi.putV3DbwOrdersOrderIdMetaGtin` — `PUT /api/v3/dbw/orders/{orderId}/meta/gtin` — Закрепить GTIN за сборочным заданием
- `orders_dbw.DBWApi.putV3DbwOrdersOrderIdMetaImei` — `PUT /api/v3/dbw/orders/{orderId}/meta/imei` — Закрепить IMEI за сборочным заданием
- `orders_dbw.DBWApi.putV3DbwOrdersOrderIdMetaUin` — `PUT /api/v3/dbw/orders/{orderId}/meta/uin` — Закрепить УИН за сборочным заданием

### orders_dbs (`orders_dbs`)
- `orders_dbs.DBSApi.getV3DbsOrders` — `GET /api/v3/dbs/orders` — Получить информацию о завершенных сборочных заданиях
- `orders_dbs.DBSApi.getV3DbsOrdersNew` — `GET /api/v3/dbs/orders/new` — Получить список новых сборочных заданий
- `orders_dbs.DBSApi.postV3DbsGroupsInfo` — `POST /api/v3/dbs/groups/info` — Получить информацию о платной доставке
- `orders_dbs.DBSApi.postV3DbsOrdersB2bInfo` — `POST /api/marketplace/v3/dbs/orders/b2b/info` — Информация о покупателе B2B
- `orders_dbs.DBSApi.postV3DbsOrdersClient` — `POST /api/v3/dbs/orders/client` — Информация о покупателе
- `orders_dbs.DBSApi.postV3DbsOrdersDeliveryDate` — `POST /api/v3/dbs/orders/delivery-date` — Получить дату и время доставки
- `orders_dbs.DBSApi.postV3DbsOrdersMetaCustomsDeclaration` — `POST /api/marketplace/v3/dbs/orders/meta/customs-declaration` — Закрепить номера ДТ за сборочными заданиями
- `orders_dbs.DBSApi.postV3DbsOrdersMetaDelete` — `POST /api/marketplace/v3/dbs/orders/meta/delete` — Удалить идентификаторы маркировки сборочных заданий
- `orders_dbs.DBSApi.postV3DbsOrdersMetaDetails` — `POST /api/marketplace/v3/dbs/orders/meta/details` — Получить идентификаторы маркировки сборочных заданий
- `orders_dbs.DBSApi.postV3DbsOrdersMetaGtin` — `POST /api/marketplace/v3/dbs/orders/meta/gtin` — Закрепить GTIN за сборочными заданиями
- `orders_dbs.DBSApi.postV3DbsOrdersMetaImei` — `POST /api/marketplace/v3/dbs/orders/meta/imei` — Закрепить IMEI за сборочными заданиями
- `orders_dbs.DBSApi.postV3DbsOrdersMetaInfo` — `POST /api/marketplace/v3/dbs/orders/meta/info` — Получить идентификаторы маркировки сборочных заданий
- `orders_dbs.DBSApi.postV3DbsOrdersMetaSgtin` — `POST /api/marketplace/v3/dbs/orders/meta/sgtin` — Закрепить коды маркировки Честного знака за сборочными заданиями
- `orders_dbs.DBSApi.postV3DbsOrdersMetaUin` — `POST /api/marketplace/v3/dbs/orders/meta/uin` — Закрепить УИН за сборочными заданиями
- `orders_dbs.DBSApi.postV3DbsOrdersStatusCancel` — `POST /api/marketplace/v3/dbs/orders/status/cancel` — Отменить сборочные задания
- `orders_dbs.DBSApi.postV3DbsOrdersStatusConfirm` — `POST /api/marketplace/v3/dbs/orders/status/confirm` — Перевести сборочные задания на сборку
- `orders_dbs.DBSApi.postV3DbsOrdersStatusDeliver` — `POST /api/marketplace/v3/dbs/orders/status/deliver` — Перевести сборочные задания в доставку
- `orders_dbs.DBSApi.postV3DbsOrdersStatusInfo` — `POST /api/marketplace/v3/dbs/orders/status/info` — Получить статусы сборочных заданий
- `orders_dbs.DBSApi.postV3DbsOrdersStatusReceive` — `POST /api/marketplace/v3/dbs/orders/status/receive` — Сообщить о получении заказов
- `orders_dbs.DBSApi.postV3DbsOrdersStatusReject` — `POST /api/marketplace/v3/dbs/orders/status/reject` — Сообщить об отказе от заказов
- `orders_dbs.DBSApi.postV3DbsOrdersStickers` — `POST /api/marketplace/v3/dbs/orders/stickers` — Получить стикеры для сборочных заданий с доставкой в ПВЗ

### in_store_pickup (`in_store_pickup`)
- `in_store_pickup.DefaultApi.getV3ClickCollectOrders` — `GET /api/v3/click-collect/orders` — Получить информацию о завершённых сборочных заданиях
- `in_store_pickup.DefaultApi.getV3ClickCollectOrdersNew` — `GET /api/v3/click-collect/orders/new` — Получить список новых сборочных заданий
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersClient` — `POST /api/v3/click-collect/orders/client` — Информация о покупателе
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersClientIdentity` — `POST /api/v3/click-collect/orders/client/identity` — Проверить, что заказ принадлежит покупателю
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersMetaCustomsDeclaration` — `POST /api/marketplace/v3/click-collect/orders/meta/customs-declaration` — Закрепить номера ДТ за сборочными заданиями
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersMetaDelete` — `POST /api/marketplace/v3/click-collect/orders/meta/delete` — Удалить идентификаторы маркировки сборочных заданий
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersMetaDetails` — `POST /api/marketplace/v3/click-collect/orders/meta/details` — Получить идентификаторы маркировки сборочных заданий
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersMetaGtin` — `POST /api/marketplace/v3/click-collect/orders/meta/gtin` — Закрепить GTIN за сборочными заданиями
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersMetaImei` — `POST /api/marketplace/v3/click-collect/orders/meta/imei` — Закрепить IMEI за сборочными заданиями
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersMetaInfo` — `POST /api/marketplace/v3/click-collect/orders/meta/info` — Получить идентификаторы маркировки сборочных заданий
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersMetaSgtin` — `POST /api/marketplace/v3/click-collect/orders/meta/sgtin` — Закрепить коды маркировки Честного знака за сборочными заданиями
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersMetaUin` — `POST /api/marketplace/v3/click-collect/orders/meta/uin` — Закрепить УИН за сборочными заданиями
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersStatusCancel` — `POST /api/marketplace/v3/click-collect/orders/status/cancel` — Отменить сборочные задания
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersStatusConfirm` — `POST /api/marketplace/v3/click-collect/orders/status/confirm` — Перевести сборочные задания на сборку
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersStatusInfo` — `POST /api/marketplace/v3/click-collect/orders/status/info` — Получить статусы сборочных заданий
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersStatusPrepare` — `POST /api/marketplace/v3/click-collect/orders/status/prepare` — Сообщить, что сборочные задания готовы к выдаче
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersStatusReceive` — `POST /api/marketplace/v3/click-collect/orders/status/receive` — Сообщить, что заказы приняты покупателями
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersStatusReject` — `POST /api/marketplace/v3/click-collect/orders/status/reject` — Сообщить об отказе от заказов

### orders_fbw (`orders_fbw`)
- `orders_fbw.DefaultApi.getV1SuppliesId` — `GET /api/v1/supplies/{ID}` — Детали поставки
- `orders_fbw.DefaultApi.getV1SuppliesIdGoods` — `GET /api/v1/supplies/{ID}/goods` — Товары поставки
- `orders_fbw.DefaultApi.getV1SuppliesIdPackage` — `GET /api/v1/supplies/{ID}/package` — Упаковка поставки
- `orders_fbw.DefaultApi.getV1TransitTariffs` — `GET /api/v1/transit-tariffs` — Транзитные направления
- `orders_fbw.DefaultApi.getV1Warehouses` — `GET /api/v1/warehouses` — Список складов
- `orders_fbw.DefaultApi.postV1AcceptanceOptions` — `POST /api/v1/acceptance/options` — Опции приёмки
- `orders_fbw.DefaultApi.postV1Supplies` — `POST /api/v1/supplies` — Список поставок

### promotion (`promotion`)
- `promotion.DefaultApi.advV0AuctionNmsPatch` — `PATCH /adv/v0/auction/nms` — Изменение списка карточек товаров в кампаниях
- `promotion.DefaultApi.advV0AuctionPlacementsPut` — `PUT /adv/v0/auction/placements` — Изменение мест размещения в кампаниях с ручной ставкой
- `promotion.DefaultApi.advV0DeleteGet` — `GET /adv/v0/delete` — Удаление кампании
- `promotion.DefaultApi.advV0NormqueryBidsDelete` — `DELETE /adv/v0/normquery/bids` — Удалить ставки поисковых кластеров
- `promotion.DefaultApi.advV0NormqueryBidsPost` — `POST /adv/v0/normquery/bids` — Установить ставки для поисковых кластеров
- `promotion.DefaultApi.advV0NormqueryGetBidsPost` — `POST /adv/v0/normquery/get-bids` — Список ставок поисковых кластеров
- `promotion.DefaultApi.advV0NormqueryGetMinusPost` — `POST /adv/v0/normquery/get-minus` — Список минус-фраз кампаний
- `promotion.DefaultApi.advV0NormqueryListPost` — `POST /adv/v0/normquery/list` — Списки активных и неактивных поисковых кластеров
- `promotion.DefaultApi.advV0NormquerySetMinusPost` — `POST /adv/v0/normquery/set-minus` — Установка и удаление минус-фраз
- `promotion.DefaultApi.advV0NormqueryStatsPost` — `POST /adv/v0/normquery/stats` — Статистика поисковых кластеров
- `promotion.DefaultApi.advV0PauseGet` — `GET /adv/v0/pause` — Пауза кампании
- `promotion.DefaultApi.advV0RenamePost` — `POST /adv/v0/rename` — Переименование кампании
- `promotion.DefaultApi.advV0StartGet` — `GET /adv/v0/start` — Запуск кампании
- `promotion.DefaultApi.advV0StopGet` — `GET /adv/v0/stop` — Завершение кампании
- `promotion.DefaultApi.advV1AdvertGet` — `GET /adv/v1/advert` — Информация о медиакампании
- `promotion.DefaultApi.advV1AdvertsGet` — `GET /adv/v1/adverts` — Список медиакампаний
- `promotion.DefaultApi.advV1BalanceGet` — `GET /adv/v1/balance` — Баланс
- `promotion.DefaultApi.advV1BudgetDepositPost` — `POST /adv/v1/budget/deposit` — Пополнение бюджета кампании
- `promotion.DefaultApi.advV1BudgetGet` — `GET /adv/v1/budget` — Бюджет кампании
- `promotion.DefaultApi.advV1CountGet` — `GET /adv/v1/count` — Количество медиакампаний
- `promotion.DefaultApi.advV1NormqueryStatsPost` — `POST /adv/v1/normquery/stats` — Статистика по поисковым кластерам с детализацией по дням
- `promotion.DefaultApi.advV1PaymentsGet` — `GET /adv/v1/payments` — Получение истории пополнений счёта
- `promotion.DefaultApi.advV1PromotionCountGet` — `GET /adv/v1/promotion/count` — Списки кампаний
- `promotion.DefaultApi.advV1StatsPost` — `POST /adv/v1/stats` — Статистика медиакампаний
- `promotion.DefaultApi.advV1SupplierSubjectsGet` — `GET /adv/v1/supplier/subjects` — Предметы для кампаний
- `promotion.DefaultApi.advV1UpdGet` — `GET /adv/v1/upd` — Получение истории затрат
- `promotion.DefaultApi.advV2SeacatSaveAdPost` — `POST /adv/v2/seacat/save-ad` — Создать кампанию
- `promotion.DefaultApi.advV2SupplierNmsPost` — `POST /adv/v2/supplier/nms` — Карточки товаров для кампаний
- `promotion.DefaultApi.advV3FullstatsGet` — `GET /adv/v3/fullstats` — Статистика кампаний
- `promotion.DefaultApi.apiAdvertV0BidsRecommendationsGet` — `GET /api/advert/v0/bids/recommendations` — Рекомендуемые ставки для карточек товаров и поисковых кластеров
- `promotion.DefaultApi.apiAdvertV1BidsMinPost` — `POST /api/advert/v1/bids/min` — Минимальные ставки для карточек товаров
- `promotion.DefaultApi.apiAdvertV1BidsPatch` — `PATCH /api/advert/v1/bids` — Изменение ставок в кампаниях
- `promotion.DefaultApi.apiAdvertV2AdvertsGet` — `GET /api/advert/v2/adverts` — Информация о кампаниях
- `promotion.DefaultApi.apiV1CalendarPromotionsDetailsGet` — `GET /api/v1/calendar/promotions/details` — Детальная информация об акциях
- `promotion.DefaultApi.apiV1CalendarPromotionsGet` — `GET /api/v1/calendar/promotions` — Список акций
- `promotion.DefaultApi.apiV1CalendarPromotionsNomenclaturesGet` — `GET /api/v1/calendar/promotions/nomenclatures` — Список товаров для участия в акции
- `promotion.DefaultApi.apiV1CalendarPromotionsUploadPost` — `POST /api/v1/calendar/promotions/upload` — Добавить товар в акцию
- `promotion.DefaultApi.getV1Config` — `GET /api/advert/v1/config` — Конфигурационные значения продвижения
- `promotion.DefaultApi.postV1NormqueryBids` — `POST /api/advert/v1/normquery/bids` — Установить ставки для поисковых кластеров в валюте аккаунта продавца

### communications (`communications`)
- `communications.DefaultApi.apiFeedbacksV1PinsCountGet` — `GET /api/feedbacks/v1/pins/count` — Количество закреплённых и откреплённых отзывов
- `communications.DefaultApi.apiFeedbacksV1PinsDelete` — `DELETE /api/feedbacks/v1/pins` — Открепить отзывы
- `communications.DefaultApi.apiFeedbacksV1PinsGet` — `GET /api/feedbacks/v1/pins` — Список закреплённых и откреплённых отзывов
- `communications.DefaultApi.apiFeedbacksV1PinsLimitsGet` — `GET /api/feedbacks/v1/pins/limits` — Лимиты закреплённых отзывов
- `communications.DefaultApi.apiFeedbacksV1PinsPost` — `POST /api/feedbacks/v1/pins` — Закрепить отзывы
- `communications.DefaultApi.apiV1ClaimPatch` — `PATCH /api/v1/claim` — Ответ на заявку покупателя
- `communications.DefaultApi.apiV1ClaimsGet` — `GET /api/v1/claims` — Заявки покупателей на возврат
- `communications.DefaultApi.apiV1FeedbackGet` — `GET /api/v1/feedback` — Получить отзыв по ID
- `communications.DefaultApi.apiV1FeedbacksAnswerPatch` — `PATCH /api/v1/feedbacks/answer` — Отредактировать ответ на отзыв
- `communications.DefaultApi.apiV1FeedbacksAnswerPost` — `POST /api/v1/feedbacks/answer` — Ответить на отзыв
- `communications.DefaultApi.apiV1FeedbacksArchiveGet` — `GET /api/v1/feedbacks/archive` — Список архивных отзывов
- `communications.DefaultApi.apiV1FeedbacksCountGet` — `GET /api/v1/feedbacks/count` — Количество отзывов
- `communications.DefaultApi.apiV1FeedbacksCountUnansweredGet` — `GET /api/v1/feedbacks/count-unanswered` — Необработанные отзывы
- `communications.DefaultApi.apiV1FeedbacksGet` — `GET /api/v1/feedbacks` — Список отзывов
- `communications.DefaultApi.apiV1FeedbacksOrderReturnPost` — `POST /api/v1/feedbacks/order/return` — Возврат товара по ID отзыва
- `communications.DefaultApi.apiV1NewFeedbacksQuestionsGet` — `GET /api/v1/new-feedbacks-questions` — Непросмотренные отзывы и вопросы
- `communications.DefaultApi.apiV1QuestionGet` — `GET /api/v1/question` — Получить вопрос по ID
- `communications.DefaultApi.apiV1QuestionsCountGet` — `GET /api/v1/questions/count` — Количество вопросов
- `communications.DefaultApi.apiV1QuestionsCountUnansweredGet` — `GET /api/v1/questions/count-unanswered` — Неотвеченные вопросы
- `communications.DefaultApi.apiV1QuestionsGet` — `GET /api/v1/questions` — Список вопросов
- `communications.DefaultApi.apiV1QuestionsPatch` — `PATCH /api/v1/questions` — Работа с вопросами
- `communications.DefaultApi.apiV1SellerChatsGet` — `GET /api/v1/seller/chats` — Список чатов
- `communications.DefaultApi.apiV1SellerDownloadIdGet` — `GET /api/v1/seller/download/{id}` — Получить файл из сообщения
- `communications.DefaultApi.apiV1SellerEventsGet` — `GET /api/v1/seller/events` — События чатов
- `communications.DefaultApi.apiV1SellerMessagePost` — `POST /api/v1/seller/message` — Отправить сообщение

### rates (`rates`)
- `rates.DefaultApi.getV1AcceptanceCoefficients` — `GET /api/tariffs/v1/acceptance/coefficients` — Тарифы на поставку
- `rates.DefaultApi.getV1TariffsBox` — `GET /api/v1/tariffs/box` — Тарифы для коробов
- `rates.DefaultApi.getV1TariffsCommission` — `GET /api/v1/tariffs/commission` — Комиссия по категориям товаров
- `rates.DefaultApi.getV1TariffsPallet` — `GET /api/v1/tariffs/pallet` — Тарифы для монопаллет
- `rates.DefaultApi.getV1TariffsReturn` — `GET /api/v1/tariffs/return` — Тарифы на возврат

### analytics (`analytics`)
- `analytics.CSVApi.apiV2NmReportDownloadsFileDownloadIdGet` — `GET /api/v2/nm-report/downloads/file/{downloadId}` — Получить отчёт
- `analytics.CSVApi.apiV2NmReportDownloadsGet` — `GET /api/v2/nm-report/downloads` — Получить список отчётов
- `analytics.CSVApi.apiV2NmReportDownloadsPost` — `POST /api/v2/nm-report/downloads` — Создать отчёт
- `analytics.CSVApi.apiV2NmReportDownloadsRetryPost` — `POST /api/v2/nm-report/downloads/retry` — Сгенерировать отчёт повторно
- `analytics.DefaultApi.apiV2SearchReportProductOrdersPost` — `POST /api/v2/search-report/product/orders` — Заказы и позиции по поисковым запросам товара
- `analytics.DefaultApi.apiV2SearchReportProductSearchTextsPost` — `POST /api/v2/search-report/product/search-texts` — Поисковые запросы по товару
- `analytics.DefaultApi.apiV2SearchReportReportPost` — `POST /api/v2/search-report/report` — Основная страница
- `analytics.DefaultApi.apiV2SearchReportTableDetailsPost` — `POST /api/v2/search-report/table/details` — Пагинация по товарам в группе
- `analytics.DefaultApi.apiV2SearchReportTableGroupsPost` — `POST /api/v2/search-report/table/groups` — Пагинация по группам
- `analytics.DefaultApi.apiV2StocksReportOfficesPost` — `POST /api/v2/stocks-report/offices` — Данные по складам
- `analytics.DefaultApi.apiV2StocksReportProductsGroupsPost` — `POST /api/v2/stocks-report/products/groups` — Данные по группам
- `analytics.DefaultApi.apiV2StocksReportProductsProductsPost` — `POST /api/v2/stocks-report/products/products` — Данные по товарам
- `analytics.DefaultApi.apiV2StocksReportProductsSizesPost` — `POST /api/v2/stocks-report/products/sizes` — Данные по размерам
- `analytics.DefaultApi.postV1ItemRating` — `POST /api/analytics/v1/item-rating` — Получить отчёт
- `analytics.DefaultApi.postV1StocksReportWbWarehouses` — `POST /api/analytics/v1/stocks-report/wb-warehouses` — Остатки на складах WB
- `analytics.DefaultApi.postV2ItemRating` — `POST /api/analytics/v2/item-rating` — Получить отчёт
- `analytics.DefaultApi.postV3SalesFunnelGroupedHistory` — `POST /api/analytics/v3/sales-funnel/grouped/history` — Статистика групп карточек товаров по дням
- `analytics.DefaultApi.postV3SalesFunnelProducts` — `POST /api/analytics/v3/sales-funnel/products` — Статистика карточек товаров за период
- `analytics.DefaultApi.postV3SalesFunnelProductsHistory` — `POST /api/analytics/v3/sales-funnel/products/history` — Статистика карточек товаров по дням

### reports (`reports`)
- `reports.CApi.apiV1AnalyticsExciseReportPost` — `POST /api/v1/analytics/excise-report` — Получить отчёт
- `reports.DefaultApi.apiV1AcceptanceReportGet` — `GET /api/v1/acceptance_report` — Создать отчёт
- `reports.DefaultApi.apiV1AcceptanceReportTasksTaskIdDownloadGet` — `GET /api/v1/acceptance_report/tasks/{task_id}/download` — Получить отчёт
- `reports.DefaultApi.apiV1AcceptanceReportTasksTaskIdStatusGet` — `GET /api/v1/acceptance_report/tasks/{task_id}/status` — Проверить статус
- `reports.DefaultApi.apiV1AnalyticsAntifraudDetailsGet` — `GET /api/v1/analytics/antifraud-details` — Самовыкупы
- `reports.DefaultApi.apiV1AnalyticsBannedProductsBlockedGet` — `GET /api/v1/analytics/banned-products/blocked` — Получить отчёт
- `reports.DefaultApi.apiV1AnalyticsBannedProductsShadowedGet` — `GET /api/v1/analytics/banned-products/shadowed` — Скрытые из каталога
- `reports.DefaultApi.apiV1AnalyticsBrandShareBrandsGet` — `GET /api/v1/analytics/brand-share/brands` — Бренды продавца
- `reports.DefaultApi.apiV1AnalyticsBrandShareGet` — `GET /api/v1/analytics/brand-share` — Получить отчёт
- `reports.DefaultApi.apiV1AnalyticsBrandShareParentSubjectsGet` — `GET /api/v1/analytics/brand-share/parent-subjects` — Родительские категории бренда
- `reports.DefaultApi.apiV1AnalyticsGoodsLabelingGet` — `GET /api/v1/analytics/goods-labeling` — Маркировка товара
- `reports.DefaultApi.apiV1AnalyticsGoodsReturnGet` — `GET /api/v1/analytics/goods-return` — Получить отчёт
- `reports.DefaultApi.apiV1AnalyticsRegionSaleGet` — `GET /api/v1/analytics/region-sale` — Получить отчёт
- `reports.DefaultApi.apiV1PaidStorageGet` — `GET /api/v1/paid_storage` — Создать отчёт
- `reports.DefaultApi.apiV1PaidStorageTasksTaskIdDownloadGet` — `GET /api/v1/paid_storage/tasks/{task_id}/download` — Получить отчёт
- `reports.DefaultApi.apiV1PaidStorageTasksTaskIdStatusGet` — `GET /api/v1/paid_storage/tasks/{task_id}/status` — Проверить статус
- `reports.DefaultApi.apiV1SupplierOrdersGet` — `GET /api/v1/supplier/orders` — Заказы
- `reports.DefaultApi.apiV1SupplierSalesGet` — `GET /api/v1/supplier/sales` — Продажи
- `reports.DefaultApi.apiV1WarehouseRemainsGet` — `GET /api/v1/warehouse_remains` — Создать отчёт
- `reports.DefaultApi.apiV1WarehouseRemainsTasksTaskIdDownloadGet` — `GET /api/v1/warehouse_remains/tasks/{task_id}/download` — Получить отчёт
- `reports.DefaultApi.apiV1WarehouseRemainsTasksTaskIdStatusGet` — `GET /api/v1/warehouse_remains/tasks/{task_id}/status` — Проверить статус
- `reports.DefaultApi.getV1Deductions` — `GET /api/analytics/v1/deductions` — Подмены и неверные вложения
- `reports.DefaultApi.getV1MeasurementPenalties` — `GET /api/analytics/v1/measurement-penalties` — Удержания за занижение габаритов упаковки
- `reports.DefaultApi.getV1WarehouseMeasurements` — `GET /api/analytics/v1/warehouse-measurements` — Замеры склада

### finances (`finances`)
- `finances.DefaultApi.getV1AccountBalance` — `GET /api/v1/account/balance` — Получить баланс продавца
- `finances.DefaultApi.getV1DocumentsCategories` — `GET /api/v1/documents/categories` — Категории документов
- `finances.DefaultApi.getV1DocumentsDownload` — `GET /api/v1/documents/download` — Получить документ
- `finances.DefaultApi.getV1DocumentsList` — `GET /api/v1/documents/list` — Список документов
- `finances.DefaultApi.postV1AcquiringDetailed` — `POST /api/finance/v1/acquiring/detailed` — Детализации к отчётам об издержках на приём платежей за период
- `finances.DefaultApi.postV1AcquiringDetailedReportId` — `POST /api/finance/v1/acquiring/detailed/{reportId}` — Детализации к отчётам об издержках на приём платежей по ID отчётов
- `finances.DefaultApi.postV1AcquiringList` — `POST /api/finance/v1/acquiring/list` — Список отчётов об издержках на приём платежей
- `finances.DefaultApi.postV1DocumentsDownloadAll` — `POST /api/v1/documents/download/all` — Получить документы
- `finances.DefaultApi.postV1SalesReportsDetailed` — `POST /api/finance/v1/sales-reports/detailed` — Детализации к отчётам реализации за период
- `finances.DefaultApi.postV1SalesReportsDetailedReportId` — `POST /api/finance/v1/sales-reports/detailed/{reportId}` — Детализации к отчётам реализации по ID отчётов
- `finances.DefaultApi.postV1SalesReportsList` — `POST /api/finance/v1/sales-reports/list` — Список отчётов реализации
<!-- PHP_METHODS_LIST_END -->
