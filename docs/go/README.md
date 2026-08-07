# wildberries-sdk (Go)

Сгенерированные Go-клиенты находятся в `clients/go/<module>`.

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

Каждая спецификация — отдельный Go-модуль. Установите нужные модули:

```bash
go get github.com/eslazarev/wildberries-sdk/clients/go/finances
go get github.com/eslazarev/wildberries-sdk/clients/go/items
go get github.com/eslazarev/wildberries-sdk/clients/go/orders_fbs
# ... и т.д.
```

Доступные модули:
- `github.com/eslazarev/wildberries-sdk/clients/go/general`
- `github.com/eslazarev/wildberries-sdk/clients/go/items`
- `github.com/eslazarev/wildberries-sdk/clients/go/orders_fbs`
- `github.com/eslazarev/wildberries-sdk/clients/go/orders_dbw`
- `github.com/eslazarev/wildberries-sdk/clients/go/orders_dbs`
- `github.com/eslazarev/wildberries-sdk/clients/go/in_store_pickup`
- `github.com/eslazarev/wildberries-sdk/clients/go/orders_fbw`
- `github.com/eslazarev/wildberries-sdk/clients/go/promotion`
- `github.com/eslazarev/wildberries-sdk/clients/go/communications`
- `github.com/eslazarev/wildberries-sdk/clients/go/tariffs`
- `github.com/eslazarev/wildberries-sdk/clients/go/analytics`
- `github.com/eslazarev/wildberries-sdk/clients/go/reports`
- `github.com/eslazarev/wildberries-sdk/clients/go/finances`
- `github.com/eslazarev/wildberries-sdk/clients/go/wbd`

## Использование

Импортируйте модуль и используйте API:

<!-- GO_METHODS_LIST_START -->
## Методы API

### general (`general`)
- `general.DefaultApiService.DeleteV1User` — `DELETE /api/v1/user` — Удалить пользователя
- `general.DefaultApiService.GetV1Rating` — `GET /api/common/v1/rating` — Получить рейтинг продавца
- `general.DefaultApiService.GetV1SellerInfo` — `GET /api/v1/seller-info` — Получить информацию о продавце
- `general.DefaultApiService.GetV1Subscriptions` — `GET /api/common/v1/subscriptions` — Получить информацию о подписке Джем
- `general.DefaultApiService.GetV1TariffConstructorOptions` — `GET /api/common/v1/tariff-constructor/options` — Получить информацию об опциях Конструктора тарифов
- `general.DefaultApiService.GetV1Users` — `GET /api/v1/users` — Получить список активных или приглашённых пользователей продавца
- `general.DefaultApiService.PostV1Invite` — `POST /api/v1/invite` — Создать приглашение для нового пользователя
- `general.DefaultApiService.PutV1UsersAccess` — `PUT /api/v1/users/access` — Изменить права доступа пользователей
- `general.APIAPIService.GetV2News` — `GET /api/communications/v2/news` — Получение новостей портала продавцов
- `general.WBAPIAPIService.GetPing` — `GET /ping` — Проверка подключения

### items (`items`)
- `items.DefaultApiService.ApiContentV1BrandsGet` — `GET /api/content/v1/brands` — Бренды
- `items.DefaultApiService.ApiV2BufferGoodsTaskGet` — `GET /api/v2/buffer/goods/task` — Детализация необработанной загрузки
- `items.DefaultApiService.ApiV2BufferTasksGet` — `GET /api/v2/buffer/tasks` — Состояние необработанной загрузки
- `items.DefaultApiService.ApiV2HistoryGoodsTaskGet` — `GET /api/v2/history/goods/task` — Детализация обработанной загрузки
- `items.DefaultApiService.ApiV2HistoryTasksGet` — `GET /api/v2/history/tasks` — Состояние обработанной загрузки
- `items.DefaultApiService.ApiV2ListGoodsFilterGet` — `GET /api/v2/list/goods/filter` — Получить товары с ценами
- `items.DefaultApiService.ApiV2ListGoodsFilterPost` — `POST /api/v2/list/goods/filter` — Получить товары с ценами по артикулам
- `items.DefaultApiService.ApiV2ListGoodsSizeNmGet` — `GET /api/v2/list/goods/size/nm` — Получить размеры товара с ценами
- `items.DefaultApiService.ApiV2QuarantineGoodsGet` — `GET /api/v2/quarantine/goods` — Получить товары в карантине
- `items.DefaultApiService.ApiV2UploadTaskClubDiscountPost` — `POST /api/v2/upload/task/club-discount` — Установить скидки WB Клуба
- `items.DefaultApiService.ApiV2UploadTaskPost` — `POST /api/v2/upload/task` — Установить цены и скидки
- `items.DefaultApiService.ApiV2UploadTaskSizePost` — `POST /api/v2/upload/task/size` — Установить цены для размеров
- `items.DefaultApiService.ApiV3DbwWarehousesWarehouseIdContactsGet` — `GET /api/v3/dbw/warehouses/{warehouseId}/contacts` — Список контактов
- `items.DefaultApiService.ApiV3DbwWarehousesWarehouseIdContactsPut` — `PUT /api/v3/dbw/warehouses/{warehouseId}/contacts` — Обновить список контактов
- `items.DefaultApiService.ApiV3OfficesGet` — `GET /api/v3/offices` — Получить список складов WB
- `items.DefaultApiService.ApiV3StocksWarehouseIdDelete` — `DELETE /api/v3/stocks/{warehouseId}` — Удалить остатки товаров
- `items.DefaultApiService.ApiV3StocksWarehouseIdPost` — `POST /api/v3/stocks/{warehouseId}` — Получить остатки товаров
- `items.DefaultApiService.ApiV3StocksWarehouseIdPut` — `PUT /api/v3/stocks/{warehouseId}` — Обновить остатки товаров
- `items.DefaultApiService.ApiV3WarehousesGet` — `GET /api/v3/warehouses` — Получить список складов продавца
- `items.DefaultApiService.ApiV3WarehousesPost` — `POST /api/v3/warehouses` — Создать склад продавца
- `items.DefaultApiService.ApiV3WarehousesWarehouseIdDelete` — `DELETE /api/v3/warehouses/{warehouseId}` — Удалить склад продавца
- `items.DefaultApiService.ApiV3WarehousesWarehouseIdPut` — `PUT /api/v3/warehouses/{warehouseId}` — Обновить склад продавца
- `items.DefaultApiService.ContentV2BarcodesPost` — `POST /content/v2/barcodes` — Генерация баркодов
- `items.DefaultApiService.ContentV2CardsDeleteTrashPost` — `POST /content/v2/cards/delete/trash` — Перенос карточек товаров в корзину
- `items.DefaultApiService.ContentV2CardsErrorListPost` — `POST /content/v2/cards/error/list` — Список несозданных карточек товаров с ошибками
- `items.DefaultApiService.ContentV2CardsLimitsGet` — `GET /content/v2/cards/limits` — Лимиты карточек товаров
- `items.DefaultApiService.ContentV2CardsMoveNmPost` — `POST /content/v2/cards/moveNm` — Объединение и разъединение карточек товаров
- `items.DefaultApiService.ContentV2CardsRecoverPost` — `POST /content/v2/cards/recover` — Восстановление карточек товаров из корзины
- `items.DefaultApiService.ContentV2CardsUpdatePost` — `POST /content/v2/cards/update` — Редактирование карточек товаров
- `items.DefaultApiService.ContentV2CardsUploadAddPost` — `POST /content/v2/cards/upload/add` — Создание карточек товаров с присоединением
- `items.DefaultApiService.ContentV2CardsUploadPost` — `POST /content/v2/cards/upload` — Создание карточек товаров
- `items.DefaultApiService.ContentV2DirectoryColorsGet` — `GET /content/v2/directory/colors` — Цвет
- `items.DefaultApiService.ContentV2DirectoryCountriesGet` — `GET /content/v2/directory/countries` — Страна производства
- `items.DefaultApiService.ContentV2DirectoryKindsGet` — `GET /content/v2/directory/kinds` — Пол
- `items.DefaultApiService.ContentV2DirectorySeasonsGet` — `GET /content/v2/directory/seasons` — Сезон
- `items.DefaultApiService.ContentV2DirectoryTnvedGet` — `GET /content/v2/directory/tnved` — ТНВЭД-код
- `items.DefaultApiService.ContentV2DirectoryVatGet` — `GET /content/v2/directory/vat` — Ставка НДС
- `items.DefaultApiService.ContentV2GetCardsListPost` — `POST /content/v2/get/cards/list` — Список карточек товаров
- `items.DefaultApiService.ContentV2GetCardsTrashPost` — `POST /content/v2/get/cards/trash` — Список карточек товаров в корзине
- `items.DefaultApiService.ContentV2ObjectAllGet` — `GET /content/v2/object/all` — Список предметов
- `items.DefaultApiService.ContentV2ObjectCharcsSubjectIdGet` — `GET /content/v2/object/charcs/{subjectId}` — Характеристики предмета
- `items.DefaultApiService.ContentV2ObjectParentAllGet` — `GET /content/v2/object/parent/all` — Родительские категории товаров
- `items.DefaultApiService.ContentV2TagIdDelete` — `DELETE /content/v2/tag/{id}` — Удаление ярлыка
- `items.DefaultApiService.ContentV2TagIdPatch` — `PATCH /content/v2/tag/{id}` — Изменение ярлыка
- `items.DefaultApiService.ContentV2TagNomenclatureLinkPost` — `POST /content/v2/tag/nomenclature/link` — Управление ярлыками в карточке товара
- `items.DefaultApiService.ContentV2TagPost` — `POST /content/v2/tag` — Создание ярлыка
- `items.DefaultApiService.ContentV2TagsGet` — `GET /content/v2/tags` — Список ярлыков
- `items.DefaultApiService.ContentV3MediaFilePost` — `POST /content/v3/media/file` — Загрузить медиафайл
- `items.DefaultApiService.ContentV3MediaSavePost` — `POST /content/v3/media/save` — Загрузить медиафайлы по ссылкам
- `items.DefaultApiService.PostV1RecommendationsList` — `POST /api/content/v1/recommendations/list` — Список рекомендаций в карточках товаров
- `items.DefaultApiService.PostV1RecommendationsSet` — `POST /api/content/v1/recommendations/set` — Установить рекомендации для товаров
- `items.DefaultApiService.PostV1UploadTaskB2bWholesale` — `POST /api/discounts-prices/v1/upload/task/b2b/wholesale` — Установить оптовые скидки для B2B-продаж

### orders_fbs (`orders_fbs`)
- `orders_fbs.DefaultApiService.GetMarketplaceV3FbsSettingsAutoreturns` — `GET /api/marketplace/v3/fbs/settings/autoreturns` — Получить настройки автовозврата продавца
- `orders_fbs.DefaultApiService.GetMarketplaceV3FbsSettingsAutoreturnsSubcategoriesRestricted` — `GET /api/marketplace/v3/fbs/settings/autoreturns/subcategories/restricted` — Получить предметы, которые не хранятся на складах WB
- `orders_fbs.DefaultApiService.PatchMarketplaceV3FbsSettingsAutoreturns` — `PATCH /api/marketplace/v3/fbs/settings/autoreturns` — Обновить настройки автовозврата продавца
- `orders_fbs.DefaultApiService.PatchMarketplaceV3FbsSettingsAutoreturnsItems` — `PATCH /api/marketplace/v3/fbs/settings/autoreturns/items` — Обновить настройки автовозврата товаров
- `orders_fbs.DefaultApiService.PostMarketplaceV3FbsSettingsAutoreturnsItems` — `POST /api/marketplace/v3/fbs/settings/autoreturns/items` — Получить настройки автовозврата товаров
- `orders_fbs.FBSAPIService.ApiMarketplaceV3FbsOrdersArchiveGet` — `GET /api/marketplace/v3/fbs/orders/archive` — Получить список архивных сборочных заданий
- `orders_fbs.FBSAPIService.ApiMarketplaceV3OrdersMetaPost` — `POST /api/marketplace/v3/orders/meta` — Получить идентификаторы маркировки сборочных заданий
- `orders_fbs.FBSAPIService.ApiMarketplaceV3OrdersOrderIdMetaCustomsDeclarationPut` — `PUT /api/marketplace/v3/orders/{orderId}/meta/customs-declaration` — Закрепить номер ДТ за сборочным заданием
- `orders_fbs.FBSAPIService.ApiMarketplaceV3SuppliesSupplyIdOrderIdsGet` — `GET /api/marketplace/v3/supplies/{supplyId}/order-ids` — Получить ID сборочных заданий поставки
- `orders_fbs.FBSAPIService.ApiMarketplaceV3SuppliesSupplyIdOrdersPatch` — `PATCH /api/marketplace/v3/supplies/{supplyId}/orders` — Добавить сборочные задания к поставке
- `orders_fbs.FBSAPIService.ApiV3OrdersClientPost` — `POST /api/v3/orders/client` — Заказы с информацией по клиенту
- `orders_fbs.FBSAPIService.ApiV3OrdersGet` — `GET /api/v3/orders` — Получить информацию о сборочных заданиях
- `orders_fbs.FBSAPIService.ApiV3OrdersNewGet` — `GET /api/v3/orders/new` — Получить список новых сборочных заданий
- `orders_fbs.FBSAPIService.ApiV3OrdersOrderIdCancelPatch` — `PATCH /api/v3/orders/{orderId}/cancel` — Отменить сборочное задание
- `orders_fbs.FBSAPIService.ApiV3OrdersOrderIdMetaDelete` — `DELETE /api/v3/orders/{orderId}/meta` — Удалить идентификаторы маркировки сборочного задания
- `orders_fbs.FBSAPIService.ApiV3OrdersOrderIdMetaExpirationPut` — `PUT /api/v3/orders/{orderId}/meta/expiration` — Закрепить за сборочным заданием срок годности товара
- `orders_fbs.FBSAPIService.ApiV3OrdersOrderIdMetaGtinPut` — `PUT /api/v3/orders/{orderId}/meta/gtin` — Закрепить GTIN за сборочным заданием
- `orders_fbs.FBSAPIService.ApiV3OrdersOrderIdMetaImeiPut` — `PUT /api/v3/orders/{orderId}/meta/imei` — Закрепить IMEI за сборочным заданием
- `orders_fbs.FBSAPIService.ApiV3OrdersOrderIdMetaSgtinPut` — `PUT /api/v3/orders/{orderId}/meta/sgtin` — Закрепить код маркировки Честного знака за сборочным заданием
- `orders_fbs.FBSAPIService.ApiV3OrdersOrderIdMetaUinPut` — `PUT /api/v3/orders/{orderId}/meta/uin` — Закрепить УИН за сборочным заданием
- `orders_fbs.FBSAPIService.ApiV3OrdersStatusHistoryPost` — `POST /api/v3/orders/status/history` — История статусов для сборочных заданий трансграничных поставок
- `orders_fbs.FBSAPIService.ApiV3OrdersStatusPost` — `POST /api/v3/orders/status` — Получить статусы сборочных заданий
- `orders_fbs.FBSAPIService.ApiV3OrdersStickersCrossBorderPost` — `POST /api/v3/orders/stickers/cross-border` — Получить стикеры сборочных заданий трансграничных поставок
- `orders_fbs.FBSAPIService.ApiV3OrdersStickersPost` — `POST /api/v3/orders/stickers` — Получить стикеры сборочных заданий
- `orders_fbs.FBSAPIService.ApiV3PassesGet` — `GET /api/v3/passes` — Получить список пропусков
- `orders_fbs.FBSAPIService.ApiV3PassesOfficesGet` — `GET /api/v3/passes/offices` — Получить список складов, для которых требуется пропуск
- `orders_fbs.FBSAPIService.ApiV3PassesPassIdDelete` — `DELETE /api/v3/passes/{passId}` — Удалить пропуск
- `orders_fbs.FBSAPIService.ApiV3PassesPassIdPut` — `PUT /api/v3/passes/{passId}` — Обновить пропуск
- `orders_fbs.FBSAPIService.ApiV3PassesPost` — `POST /api/v3/passes` — Создать пропуск
- `orders_fbs.FBSAPIService.ApiV3SuppliesGet` — `GET /api/v3/supplies` — Получить список поставок
- `orders_fbs.FBSAPIService.ApiV3SuppliesOrdersReshipmentGet` — `GET /api/v3/supplies/orders/reshipment` — Получить все сборочные задания для повторной отгрузки
- `orders_fbs.FBSAPIService.ApiV3SuppliesPost` — `POST /api/v3/supplies` — Создать новую поставку
- `orders_fbs.FBSAPIService.ApiV3SuppliesSupplyIdBarcodeGet` — `GET /api/v3/supplies/{supplyId}/barcode` — Получить QR-код поставки
- `orders_fbs.FBSAPIService.ApiV3SuppliesSupplyIdDelete` — `DELETE /api/v3/supplies/{supplyId}` — Удалить поставку
- `orders_fbs.FBSAPIService.ApiV3SuppliesSupplyIdDeliverPatch` — `PATCH /api/v3/supplies/{supplyId}/deliver` — Передать поставку в доставку
- `orders_fbs.FBSAPIService.ApiV3SuppliesSupplyIdGet` — `GET /api/v3/supplies/{supplyId}` — Получить информацию о поставке
- `orders_fbs.FBSAPIService.ApiV3SuppliesSupplyIdTrbxDelete` — `DELETE /api/v3/supplies/{supplyId}/trbx` — Удалить грузоместа из поставки
- `orders_fbs.FBSAPIService.ApiV3SuppliesSupplyIdTrbxGet` — `GET /api/v3/supplies/{supplyId}/trbx` — Получить список грузомест поставки
- `orders_fbs.FBSAPIService.ApiV3SuppliesSupplyIdTrbxPost` — `POST /api/v3/supplies/{supplyId}/trbx` — Добавить грузоместа к поставке
- `orders_fbs.FBSAPIService.ApiV3SuppliesSupplyIdTrbxStickersPost` — `POST /api/v3/supplies/{supplyId}/trbx/stickers` — Получить стикеры грузомест поставки

### orders_dbw (`orders_dbw`)
- `orders_dbw.DBWAPIService.GetV3DbwOrders` — `GET /api/v3/dbw/orders` — Получить информацию о завершенных сборочных заданиях
- `orders_dbw.DBWAPIService.GetV3DbwOrdersNew` — `GET /api/v3/dbw/orders/new` — Получить список новых сборочных заданий
- `orders_dbw.DBWAPIService.PatchV3DbwOrdersOrderIdCancel` — `PATCH /api/v3/dbw/orders/{orderId}/cancel` — Отменить сборочное задание
- `orders_dbw.DBWAPIService.PatchV3DbwOrdersOrderIdConfirm` — `PATCH /api/v3/dbw/orders/{orderId}/confirm` — Перевести на сборку
- `orders_dbw.DBWAPIService.PostV3DbwOrdersClient` — `POST /api/marketplace/v3/dbw/orders/client` — Информация о покупателе
- `orders_dbw.DBWAPIService.PostV3DbwOrdersCourier` — `POST /api/v3/dbw/orders/courier` — Информация о курьере
- `orders_dbw.DBWAPIService.PostV3DbwOrdersDeliveryDate` — `POST /api/v3/dbw/orders/delivery-date` — Получить дату и время доставки
- `orders_dbw.DBWAPIService.PostV3DbwOrdersMetaDelete` — `POST /api/marketplace/v3/dbw/orders/meta/delete` — Удалить идентификаторы маркировки сборочных заданий
- `orders_dbw.DBWAPIService.PostV3DbwOrdersMetaDetails` — `POST /api/marketplace/v3/dbw/orders/meta/details` — Получить идентификаторы маркировки сборочных заданий
- `orders_dbw.DBWAPIService.PostV3DbwOrdersMetaSgtin` — `POST /api/marketplace/v3/dbw/orders/meta/sgtin` — Закрепить коды маркировки Честного знака за сборочными заданиями
- `orders_dbw.DBWAPIService.PostV3DbwOrdersStatus` — `POST /api/v3/dbw/orders/status` — Получить статусы сборочных заданий
- `orders_dbw.DBWAPIService.PostV3DbwOrdersStatusDeliver` — `POST /api/marketplace/v3/dbw/orders/status/deliver` — Перевести сборочные задания в доставку
- `orders_dbw.DBWAPIService.PostV3DbwOrdersStickers` — `POST /api/v3/dbw/orders/stickers` — Получить стикеры сборочных заданий
- `orders_dbw.DBWAPIService.PutV3DbwOrdersOrderIdMetaGtin` — `PUT /api/v3/dbw/orders/{orderId}/meta/gtin` — Закрепить GTIN за сборочным заданием
- `orders_dbw.DBWAPIService.PutV3DbwOrdersOrderIdMetaImei` — `PUT /api/v3/dbw/orders/{orderId}/meta/imei` — Закрепить IMEI за сборочным заданием
- `orders_dbw.DBWAPIService.PutV3DbwOrdersOrderIdMetaUin` — `PUT /api/v3/dbw/orders/{orderId}/meta/uin` — Закрепить УИН за сборочным заданием

### orders_dbs (`orders_dbs`)
- `orders_dbs.DBSAPIService.GetV3DbsOrders` — `GET /api/v3/dbs/orders` — Получить информацию о завершенных сборочных заданиях
- `orders_dbs.DBSAPIService.GetV3DbsOrdersNew` — `GET /api/v3/dbs/orders/new` — Получить список новых сборочных заданий
- `orders_dbs.DBSAPIService.PostV3DbsGroupsInfo` — `POST /api/v3/dbs/groups/info` — Получить информацию о платной доставке
- `orders_dbs.DBSAPIService.PostV3DbsOrdersB2bInfo` — `POST /api/marketplace/v3/dbs/orders/b2b/info` — Информация о покупателе B2B
- `orders_dbs.DBSAPIService.PostV3DbsOrdersClient` — `POST /api/v3/dbs/orders/client` — Информация о покупателе
- `orders_dbs.DBSAPIService.PostV3DbsOrdersDeliveryDate` — `POST /api/v3/dbs/orders/delivery-date` — Получить дату и время доставки
- `orders_dbs.DBSAPIService.PostV3DbsOrdersMetaCustomsDeclaration` — `POST /api/marketplace/v3/dbs/orders/meta/customs-declaration` — Закрепить номера ДТ за сборочными заданиями
- `orders_dbs.DBSAPIService.PostV3DbsOrdersMetaDelete` — `POST /api/marketplace/v3/dbs/orders/meta/delete` — Удалить идентификаторы маркировки сборочных заданий
- `orders_dbs.DBSAPIService.PostV3DbsOrdersMetaDetails` — `POST /api/marketplace/v3/dbs/orders/meta/details` — Получить идентификаторы маркировки сборочных заданий
- `orders_dbs.DBSAPIService.PostV3DbsOrdersMetaGtin` — `POST /api/marketplace/v3/dbs/orders/meta/gtin` — Закрепить GTIN за сборочными заданиями
- `orders_dbs.DBSAPIService.PostV3DbsOrdersMetaImei` — `POST /api/marketplace/v3/dbs/orders/meta/imei` — Закрепить IMEI за сборочными заданиями
- `orders_dbs.DBSAPIService.PostV3DbsOrdersMetaSgtin` — `POST /api/marketplace/v3/dbs/orders/meta/sgtin` — Закрепить коды маркировки Честного знака за сборочными заданиями
- `orders_dbs.DBSAPIService.PostV3DbsOrdersMetaUin` — `POST /api/marketplace/v3/dbs/orders/meta/uin` — Закрепить УИН за сборочными заданиями
- `orders_dbs.DBSAPIService.PostV3DbsOrdersStatusCancel` — `POST /api/marketplace/v3/dbs/orders/status/cancel` — Отменить сборочные задания
- `orders_dbs.DBSAPIService.PostV3DbsOrdersStatusConfirm` — `POST /api/marketplace/v3/dbs/orders/status/confirm` — Перевести сборочные задания на сборку
- `orders_dbs.DBSAPIService.PostV3DbsOrdersStatusDeliver` — `POST /api/marketplace/v3/dbs/orders/status/deliver` — Перевести сборочные задания в доставку
- `orders_dbs.DBSAPIService.PostV3DbsOrdersStatusInfo` — `POST /api/marketplace/v3/dbs/orders/status/info` — Получить статусы сборочных заданий
- `orders_dbs.DBSAPIService.PostV3DbsOrdersStatusReceive` — `POST /api/marketplace/v3/dbs/orders/status/receive` — Сообщить о получении заказов
- `orders_dbs.DBSAPIService.PostV3DbsOrdersStatusReject` — `POST /api/marketplace/v3/dbs/orders/status/reject` — Сообщить об отказе от заказов
- `orders_dbs.DBSAPIService.PostV3DbsOrdersStickers` — `POST /api/marketplace/v3/dbs/orders/stickers` — Получить стикеры для сборочных заданий с доставкой в ПВЗ

### in_store_pickup (`in_store_pickup`)
- `in_store_pickup.DefaultApiService.GetV3ClickCollectOrders` — `GET /api/v3/click-collect/orders` — Получить информацию о завершённых сборочных заданиях
- `in_store_pickup.DefaultApiService.GetV3ClickCollectOrdersNew` — `GET /api/v3/click-collect/orders/new` — Получить список новых сборочных заданий
- `in_store_pickup.DefaultApiService.PostV3ClickCollectOrdersClient` — `POST /api/v3/click-collect/orders/client` — Информация о покупателе
- `in_store_pickup.DefaultApiService.PostV3ClickCollectOrdersClientIdentity` — `POST /api/v3/click-collect/orders/client/identity` — Проверить, что заказ принадлежит покупателю
- `in_store_pickup.DefaultApiService.PostV3ClickCollectOrdersMetaCustomsDeclaration` — `POST /api/marketplace/v3/click-collect/orders/meta/customs-declaration` — Закрепить номера ДТ за сборочными заданиями
- `in_store_pickup.DefaultApiService.PostV3ClickCollectOrdersMetaDelete` — `POST /api/marketplace/v3/click-collect/orders/meta/delete` — Удалить идентификаторы маркировки сборочных заданий
- `in_store_pickup.DefaultApiService.PostV3ClickCollectOrdersMetaDetails` — `POST /api/marketplace/v3/click-collect/orders/meta/details` — Получить идентификаторы маркировки сборочных заданий
- `in_store_pickup.DefaultApiService.PostV3ClickCollectOrdersMetaGtin` — `POST /api/marketplace/v3/click-collect/orders/meta/gtin` — Закрепить GTIN за сборочными заданиями
- `in_store_pickup.DefaultApiService.PostV3ClickCollectOrdersMetaImei` — `POST /api/marketplace/v3/click-collect/orders/meta/imei` — Закрепить IMEI за сборочными заданиями
- `in_store_pickup.DefaultApiService.PostV3ClickCollectOrdersMetaSgtin` — `POST /api/marketplace/v3/click-collect/orders/meta/sgtin` — Закрепить коды маркировки Честного знака за сборочными заданиями
- `in_store_pickup.DefaultApiService.PostV3ClickCollectOrdersMetaUin` — `POST /api/marketplace/v3/click-collect/orders/meta/uin` — Закрепить УИН за сборочными заданиями
- `in_store_pickup.DefaultApiService.PostV3ClickCollectOrdersStatusCancel` — `POST /api/marketplace/v3/click-collect/orders/status/cancel` — Отменить сборочные задания
- `in_store_pickup.DefaultApiService.PostV3ClickCollectOrdersStatusConfirm` — `POST /api/marketplace/v3/click-collect/orders/status/confirm` — Перевести сборочные задания на сборку
- `in_store_pickup.DefaultApiService.PostV3ClickCollectOrdersStatusInfo` — `POST /api/marketplace/v3/click-collect/orders/status/info` — Получить статусы сборочных заданий
- `in_store_pickup.DefaultApiService.PostV3ClickCollectOrdersStatusPrepare` — `POST /api/marketplace/v3/click-collect/orders/status/prepare` — Сообщить, что сборочные задания готовы к выдаче
- `in_store_pickup.DefaultApiService.PostV3ClickCollectOrdersStatusReceive` — `POST /api/marketplace/v3/click-collect/orders/status/receive` — Сообщить, что заказы приняты покупателями
- `in_store_pickup.DefaultApiService.PostV3ClickCollectOrdersStatusReject` — `POST /api/marketplace/v3/click-collect/orders/status/reject` — Сообщить об отказе от заказов

### orders_fbw (`orders_fbw`)
- `orders_fbw.DefaultApiService.GetV1SuppliesId` — `GET /api/v1/supplies/{ID}` — Детали поставки
- `orders_fbw.DefaultApiService.GetV1SuppliesIdGoods` — `GET /api/v1/supplies/{ID}/goods` — Товары поставки
- `orders_fbw.DefaultApiService.GetV1SuppliesIdPackage` — `GET /api/v1/supplies/{ID}/package` — Упаковка поставки
- `orders_fbw.DefaultApiService.GetV1TransitTariffs` — `GET /api/v1/transit-tariffs` — Транзитные направления
- `orders_fbw.DefaultApiService.GetV1Warehouses` — `GET /api/v1/warehouses` — Список складов
- `orders_fbw.DefaultApiService.PostV1AcceptanceOptions` — `POST /api/v1/acceptance/options` — Опции приёмки
- `orders_fbw.DefaultApiService.PostV1Supplies` — `POST /api/v1/supplies` — Список поставок

### promotion (`promotion`)
- `promotion.DefaultApiService.AdvV0AuctionNmsPatch` — `PATCH /adv/v0/auction/nms` — Изменение списка карточек товаров в кампаниях
- `promotion.DefaultApiService.AdvV0AuctionPlacementsPut` — `PUT /adv/v0/auction/placements` — Изменение мест размещения в кампаниях с ручной ставкой
- `promotion.DefaultApiService.AdvV0DeleteGet` — `GET /adv/v0/delete` — Удаление кампании
- `promotion.DefaultApiService.AdvV0NormqueryBidsDelete` — `DELETE /adv/v0/normquery/bids` — Удалить ставки поисковых кластеров
- `promotion.DefaultApiService.AdvV0NormqueryBidsPost` — `POST /adv/v0/normquery/bids` — Установить ставки для поисковых кластеров
- `promotion.DefaultApiService.AdvV0NormqueryGetBidsPost` — `POST /adv/v0/normquery/get-bids` — Список ставок поисковых кластеров
- `promotion.DefaultApiService.AdvV0NormqueryGetMinusPost` — `POST /adv/v0/normquery/get-minus` — Список минус-фраз кампаний
- `promotion.DefaultApiService.AdvV0NormqueryListPost` — `POST /adv/v0/normquery/list` — Списки активных и неактивных поисковых кластеров
- `promotion.DefaultApiService.AdvV0NormquerySetMinusPost` — `POST /adv/v0/normquery/set-minus` — Установка и удаление минус-фраз
- `promotion.DefaultApiService.AdvV0NormqueryStatsPost` — `POST /adv/v0/normquery/stats` — Статистика поисковых кластеров
- `promotion.DefaultApiService.AdvV0PauseGet` — `GET /adv/v0/pause` — Пауза кампании
- `promotion.DefaultApiService.AdvV0RenamePost` — `POST /adv/v0/rename` — Переименование кампании
- `promotion.DefaultApiService.AdvV0StartGet` — `GET /adv/v0/start` — Запуск кампании
- `promotion.DefaultApiService.AdvV0StopGet` — `GET /adv/v0/stop` — Завершение кампании
- `promotion.DefaultApiService.AdvV1AdvertGet` — `GET /adv/v1/advert` — Информация о медиакампании
- `promotion.DefaultApiService.AdvV1AdvertsGet` — `GET /adv/v1/adverts` — Список медиакампаний
- `promotion.DefaultApiService.AdvV1BalanceGet` — `GET /adv/v1/balance` — Баланс
- `promotion.DefaultApiService.AdvV1BudgetDepositPost` — `POST /adv/v1/budget/deposit` — Пополнение бюджета кампании
- `promotion.DefaultApiService.AdvV1BudgetGet` — `GET /adv/v1/budget` — Бюджет кампании
- `promotion.DefaultApiService.AdvV1CountGet` — `GET /adv/v1/count` — Количество медиакампаний
- `promotion.DefaultApiService.AdvV1NormqueryStatsPost` — `POST /adv/v1/normquery/stats` — Статистика по поисковым кластерам с детализацией по дням
- `promotion.DefaultApiService.AdvV1PaymentsGet` — `GET /adv/v1/payments` — Получение истории пополнений счёта
- `promotion.DefaultApiService.AdvV1PromotionCountGet` — `GET /adv/v1/promotion/count` — Списки кампаний
- `promotion.DefaultApiService.AdvV1StatsPost` — `POST /adv/v1/stats` — Статистика медиакампаний
- `promotion.DefaultApiService.AdvV1SupplierSubjectsGet` — `GET /adv/v1/supplier/subjects` — Предметы для кампаний
- `promotion.DefaultApiService.AdvV1UpdGet` — `GET /adv/v1/upd` — Получение истории затрат
- `promotion.DefaultApiService.AdvV2SeacatSaveAdPost` — `POST /adv/v2/seacat/save-ad` — Создать кампанию
- `promotion.DefaultApiService.AdvV2SupplierNmsPost` — `POST /adv/v2/supplier/nms` — Карточки товаров для кампаний
- `promotion.DefaultApiService.AdvV3FullstatsGet` — `GET /adv/v3/fullstats` — Статистика кампаний
- `promotion.DefaultApiService.ApiAdvertV0BidsRecommendationsGet` — `GET /api/advert/v0/bids/recommendations` — Рекомендуемые ставки для карточек товаров и поисковых кластеров
- `promotion.DefaultApiService.ApiAdvertV1BidsMinPost` — `POST /api/advert/v1/bids/min` — Минимальные ставки для карточек товаров
- `promotion.DefaultApiService.ApiAdvertV1BidsPatch` — `PATCH /api/advert/v1/bids` — Изменение ставок в кампаниях
- `promotion.DefaultApiService.ApiAdvertV2AdvertsGet` — `GET /api/advert/v2/adverts` — Информация о кампаниях
- `promotion.DefaultApiService.ApiV1CalendarPromotionsDetailsGet` — `GET /api/v1/calendar/promotions/details` — Детальная информация об акциях
- `promotion.DefaultApiService.ApiV1CalendarPromotionsGet` — `GET /api/v1/calendar/promotions` — Список акций
- `promotion.DefaultApiService.ApiV1CalendarPromotionsNomenclaturesGet` — `GET /api/v1/calendar/promotions/nomenclatures` — Список товаров для участия в акции
- `promotion.DefaultApiService.ApiV1CalendarPromotionsUploadPost` — `POST /api/v1/calendar/promotions/upload` — Добавить товар в акцию
- `promotion.DefaultApiService.GetV1Config` — `GET /api/advert/v1/config` — Конфигурационные значения продвижения
- `promotion.DefaultApiService.PostV1NormqueryBids` — `POST /api/advert/v1/normquery/bids` — Установить ставки для поисковых кластеров в валюте аккаунта продавца

### communications (`communications`)
- `communications.DefaultApiService.DeleteFeedbacksV1Pins` — `DELETE /api/feedbacks/v1/pins` — Открепить отзывы
- `communications.DefaultApiService.GetFeedbacksV1Pins` — `GET /api/feedbacks/v1/pins` — Список закреплённых и откреплённых отзывов
- `communications.DefaultApiService.GetFeedbacksV1PinsCount` — `GET /api/feedbacks/v1/pins/count` — Количество закреплённых и откреплённых отзывов
- `communications.DefaultApiService.GetFeedbacksV1PinsLimits` — `GET /api/feedbacks/v1/pins/limits` — Лимиты закреплённых отзывов
- `communications.DefaultApiService.GetV1Claims` — `GET /api/v1/claims` — Заявки покупателей на возврат
- `communications.DefaultApiService.GetV1Feedback` — `GET /api/v1/feedback` — Получить отзыв по ID
- `communications.DefaultApiService.GetV1Feedbacks` — `GET /api/v1/feedbacks` — Список отзывов
- `communications.DefaultApiService.GetV1FeedbacksArchive` — `GET /api/v1/feedbacks/archive` — Список архивных отзывов
- `communications.DefaultApiService.GetV1FeedbacksCount` — `GET /api/v1/feedbacks/count` — Количество отзывов
- `communications.DefaultApiService.GetV1FeedbacksCountUnanswered` — `GET /api/v1/feedbacks/count-unanswered` — Необработанные отзывы
- `communications.DefaultApiService.GetV1NewFeedbacksQuestions` — `GET /api/v1/new-feedbacks-questions` — Непросмотренные отзывы и вопросы
- `communications.DefaultApiService.GetV1Question` — `GET /api/v1/question` — Получить вопрос по ID
- `communications.DefaultApiService.GetV1Questions` — `GET /api/v1/questions` — Список вопросов
- `communications.DefaultApiService.GetV1QuestionsCount` — `GET /api/v1/questions/count` — Количество вопросов
- `communications.DefaultApiService.GetV1QuestionsCountUnanswered` — `GET /api/v1/questions/count-unanswered` — Неотвеченные вопросы
- `communications.DefaultApiService.GetV1SellerChats` — `GET /api/v1/seller/chats` — Список чатов
- `communications.DefaultApiService.GetV1SellerDownloadId` — `GET /api/v1/seller/download/{id}` — Получить файл из сообщения
- `communications.DefaultApiService.GetV1SellerEvents` — `GET /api/v1/seller/events` — События чатов
- `communications.DefaultApiService.PatchV1Claim` — `PATCH /api/v1/claim` — Ответ на заявку покупателя
- `communications.DefaultApiService.PatchV1FeedbacksAnswer` — `PATCH /api/v1/feedbacks/answer` — Отредактировать ответ на отзыв
- `communications.DefaultApiService.PatchV1Questions` — `PATCH /api/v1/questions` — Работа с вопросами
- `communications.DefaultApiService.PostFeedbacksV1Pins` — `POST /api/feedbacks/v1/pins` — Закрепить отзывы
- `communications.DefaultApiService.PostV1FeedbacksAnswer` — `POST /api/v1/feedbacks/answer` — Ответить на отзыв
- `communications.DefaultApiService.PostV1FeedbacksOrderReturn` — `POST /api/v1/feedbacks/order/return` — Возврат товара по ID отзыва
- `communications.DefaultApiService.PostV1SellerMessage` — `POST /api/v1/seller/message` — Отправить сообщение

### rates (`rates`)
- `rates.DefaultApiService.GetV1AcceptanceCoefficients` — `GET /api/tariffs/v1/acceptance/coefficients` — Тарифы на поставку
- `rates.DefaultApiService.GetV1TariffsBox` — `GET /api/v1/tariffs/box` — Тарифы для коробов
- `rates.DefaultApiService.GetV1TariffsCommission` — `GET /api/v1/tariffs/commission` — Комиссия по категориям товаров
- `rates.DefaultApiService.GetV1TariffsPallet` — `GET /api/v1/tariffs/pallet` — Тарифы для монопаллет
- `rates.DefaultApiService.GetV1TariffsReturn` — `GET /api/v1/tariffs/return` — Тарифы на возврат

### analytics (`analytics`)
- `analytics.DefaultApiService.PostV1ItemRating` — `POST /api/analytics/v1/item-rating` — Получить отчёт
- `analytics.DefaultApiService.PostV1OrderFeed` — `POST /api/analytics/v1/order-feed` — Получить отчёт
- `analytics.DefaultApiService.PostV1StocksReportWbWarehouses` — `POST /api/analytics/v1/stocks-report/wb-warehouses` — Остатки на складах WB
- `analytics.DefaultApiService.PostV2ItemRating` — `POST /api/analytics/v2/item-rating` — Получить отчёт
- `analytics.DefaultApiService.PostV2SearchReportProductOrders` — `POST /api/v2/search-report/product/orders` — Заказы и позиции по поисковым запросам товара
- `analytics.DefaultApiService.PostV2SearchReportProductSearchTexts` — `POST /api/v2/search-report/product/search-texts` — Поисковые запросы по товару
- `analytics.DefaultApiService.PostV2SearchReportReport` — `POST /api/v2/search-report/report` — Основная страница
- `analytics.DefaultApiService.PostV2SearchReportTableDetails` — `POST /api/v2/search-report/table/details` — Пагинация по товарам в группе
- `analytics.DefaultApiService.PostV2SearchReportTableGroups` — `POST /api/v2/search-report/table/groups` — Пагинация по группам
- `analytics.DefaultApiService.PostV2StocksReportOffices` — `POST /api/v2/stocks-report/offices` — Данные по складам
- `analytics.DefaultApiService.PostV2StocksReportProductsGroups` — `POST /api/v2/stocks-report/products/groups` — Данные по группам
- `analytics.DefaultApiService.PostV2StocksReportProductsProducts` — `POST /api/v2/stocks-report/products/products` — Данные по товарам
- `analytics.DefaultApiService.PostV2StocksReportProductsSizes` — `POST /api/v2/stocks-report/products/sizes` — Данные по размерам
- `analytics.DefaultApiService.PostV3SalesFunnelGroupedHistory` — `POST /api/analytics/v3/sales-funnel/grouped/history` — Статистика групп карточек товаров по дням
- `analytics.DefaultApiService.PostV3SalesFunnelProducts` — `POST /api/analytics/v3/sales-funnel/products` — Статистика карточек товаров за период
- `analytics.DefaultApiService.PostV3SalesFunnelProductsHistory` — `POST /api/analytics/v3/sales-funnel/products/history` — Статистика карточек товаров по дням
- `analytics.CSVAPIService.GetV2NmReportDownloads` — `GET /api/v2/nm-report/downloads` — Получить список отчётов
- `analytics.CSVAPIService.GetV2NmReportDownloadsFileDownloadId` — `GET /api/v2/nm-report/downloads/file/{downloadId}` — Получить отчёт
- `analytics.CSVAPIService.PostV2NmReportDownloads` — `POST /api/v2/nm-report/downloads` — Создать отчёт
- `analytics.CSVAPIService.PostV2NmReportDownloadsRetry` — `POST /api/v2/nm-report/downloads/retry` — Сгенерировать отчёт повторно

### reports (`reports`)
- `reports.DefaultApiService.GetV1AcceptanceReport` — `GET /api/v1/acceptance_report` — Создать отчёт
- `reports.DefaultApiService.GetV1AcceptanceReportTasksTaskIdDownload` — `GET /api/v1/acceptance_report/tasks/{task_id}/download` — Получить отчёт
- `reports.DefaultApiService.GetV1AcceptanceReportTasksTaskIdStatus` — `GET /api/v1/acceptance_report/tasks/{task_id}/status` — Проверить статус
- `reports.DefaultApiService.GetV1AnalyticsAntifraudDetails` — `GET /api/v1/analytics/antifraud-details` — Самовыкупы
- `reports.DefaultApiService.GetV1AnalyticsBannedProducsBlocked` — `GET /api/v1/analytics/banned-products/blocked` — Получить отчёт
- `reports.DefaultApiService.GetV1AnalyticsBannedProductsShadowed` — `GET /api/v1/analytics/banned-products/shadowed` — Скрытые из каталога
- `reports.DefaultApiService.GetV1AnalyticsBrandShare` — `GET /api/v1/analytics/brand-share` — Получить отчёт
- `reports.DefaultApiService.GetV1AnalyticsBrandShareBrands` — `GET /api/v1/analytics/brand-share/brands` — Бренды продавца
- `reports.DefaultApiService.GetV1AnalyticsBrandShareParentSubjects` — `GET /api/v1/analytics/brand-share/parent-subjects` — Родительские категории бренда
- `reports.DefaultApiService.GetV1AnalyticsGoodsLabeling` — `GET /api/v1/analytics/goods-labeling` — Маркировка товара
- `reports.DefaultApiService.GetV1AnalyticsGoodsReturn` — `GET /api/v1/analytics/goods-return` — Получить отчёт
- `reports.DefaultApiService.GetV1AnalyticsRegionSale` — `GET /api/v1/analytics/region-sale` — Получить отчёт
- `reports.DefaultApiService.GetV1Deductions` — `GET /api/analytics/v1/deductions` — Подмены и неверные вложения
- `reports.DefaultApiService.GetV1MeasurementPenalties` — `GET /api/analytics/v1/measurement-penalties` — Удержания за занижение габаритов упаковки
- `reports.DefaultApiService.GetV1PaidStorage` — `GET /api/v1/paid_storage` — Создать отчёт
- `reports.DefaultApiService.GetV1PaidStorageTasksTaskIdDownload` — `GET /api/v1/paid_storage/tasks/{task_id}/download` — Получить отчёт
- `reports.DefaultApiService.GetV1PaidStorageTasksTaskIdStatus` — `GET /api/v1/paid_storage/tasks/{task_id}/status` — Проверить статус
- `reports.DefaultApiService.GetV1SupplierOrders` — `GET /api/v1/supplier/orders` — Заказы
- `reports.DefaultApiService.GetV1SupplierSales` — `GET /api/v1/supplier/sales` — Продажи
- `reports.DefaultApiService.GetV1WarehouseMeasurements` — `GET /api/analytics/v1/warehouse-measurements` — Замеры склада
- `reports.DefaultApiService.GetV1WarehouseRemains` — `GET /api/v1/warehouse_remains` — Создать отчёт
- `reports.DefaultApiService.GetV1WarehouseRemainsTasksTaskIdDownload` — `GET /api/v1/warehouse_remains/tasks/{task_id}/download` — Получить отчёт
- `reports.DefaultApiService.GetV1WarehouseRemainsTasksTaskIdStatus` — `GET /api/v1/warehouse_remains/tasks/{task_id}/status` — Проверить статус
- `reports.CAPIService.PostV1AnalyticsExciseReport` — `POST /api/v1/analytics/excise-report` — Получить отчёт

### finances (`finances`)
- `finances.DefaultApiService.GetV1AccountBalance` — `GET /api/v1/account/balance` — Получить баланс продавца
- `finances.DefaultApiService.GetV1DocumentsCategories` — `GET /api/v1/documents/categories` — Категории документов
- `finances.DefaultApiService.GetV1DocumentsDownload` — `GET /api/v1/documents/download` — Получить документ
- `finances.DefaultApiService.GetV1DocumentsList` — `GET /api/v1/documents/list` — Список документов
- `finances.DefaultApiService.PostV1AcquiringDetailed` — `POST /api/finance/v1/acquiring/detailed` — Детализации к отчётам об издержках на приём платежей за период
- `finances.DefaultApiService.PostV1AcquiringDetailedReportId` — `POST /api/finance/v1/acquiring/detailed/{reportId}` — Детализации к отчётам об издержках на приём платежей по ID отчётов
- `finances.DefaultApiService.PostV1AcquiringList` — `POST /api/finance/v1/acquiring/list` — Список отчётов об издержках на приём платежей
- `finances.DefaultApiService.PostV1DocumentsDownloadAll` — `POST /api/v1/documents/download/all` — Получить документы
- `finances.DefaultApiService.PostV1SalesReportsDetailed` — `POST /api/finance/v1/sales-reports/detailed` — Детализации к отчётам реализации за период
- `finances.DefaultApiService.PostV1SalesReportsDetailedReportId` — `POST /api/finance/v1/sales-reports/detailed/{reportId}` — Детализации к отчётам реализации по ID отчётов
- `finances.DefaultApiService.PostV1SalesReportsList` — `POST /api/finance/v1/sales-reports/list` — Список отчётов реализации
<!-- GO_METHODS_LIST_END -->
