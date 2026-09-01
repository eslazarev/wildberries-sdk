# wildberries-sdk (npm)

Единый npm-пакет с клиентами Wildberries по всем спецификациям.

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
[![Socket Badge](https://badge.socket.dev/npm/package/wildberries-sdk/latest)](https://socket.dev/npm/package/wildberries-sdk)

## Установка

```bash
npm install wildberries-sdk
```

## Пример (communications)

```ts
import { Configuration, DefaultApi } from "wildberries-sdk/communications";

async function main() {
  const config = new Configuration({
    basePath: "https://feedbacks-api.wildberries.ru",
    apiKey: "YOUR_TOKEN",
  });

  const api = new DefaultApi(config);
  const response = await api.apiV1FeedbacksGet({
    isAnswered: true,
    take: 100,
    skip: 0,
  });

  console.log(response);
}

main().catch(console.error);
```

<!-- NPM_METHODS_LIST_START -->
## Методы API

### general (`general`)
- `general.APIApi.getV2News` — Получение новостей портала продавцов
- `general.DefaultApi.deleteV1User` — Удалить пользователя
- `general.DefaultApi.getV1Rating` — Получить рейтинг продавца
- `general.DefaultApi.getV1SellerInfo` — Получить информацию о продавце
- `general.DefaultApi.getV1Subscriptions` — Получить информацию о подписке Джем
- `general.DefaultApi.getV1TariffConstructorOptions` — Получить информацию об опциях Конструктора тарифов
- `general.DefaultApi.getV1Users` — Получить список активных или приглашённых пользователей продавца
- `general.DefaultApi.postV1Invite` — Создать приглашение для нового пользователя
- `general.DefaultApi.putV1UsersAccess` — Изменить права доступа пользователей
- `general.WBAPIApi.getPing` — Проверка подключения

### items (`items`)
- `items.DefaultApi.apiContentV1BrandsGet` — Бренды
- `items.DefaultApi.apiV2BufferGoodsTaskGet` — Детализация необработанной загрузки
- `items.DefaultApi.apiV2BufferTasksGet` — Состояние необработанной загрузки
- `items.DefaultApi.apiV2HistoryGoodsTaskGet` — Детализация обработанной загрузки
- `items.DefaultApi.apiV2HistoryTasksGet` — Состояние обработанной загрузки
- `items.DefaultApi.apiV2ListGoodsFilterGet` — Получить товары с ценами
- `items.DefaultApi.apiV2ListGoodsFilterPost` — Получить товары с ценами по артикулам
- `items.DefaultApi.apiV2ListGoodsSizeNmGet` — Получить размеры товара с ценами
- `items.DefaultApi.apiV2QuarantineGoodsGet` — Получить товары в карантине
- `items.DefaultApi.apiV2UploadTaskClubDiscountPost` — Установить скидки WB Клуба
- `items.DefaultApi.apiV2UploadTaskPost` — Установить цены и скидки
- `items.DefaultApi.apiV2UploadTaskSizePost` — Установить цены для размеров
- `items.DefaultApi.apiV3DbwWarehousesWarehouseIdContactsGet` — Список контактов
- `items.DefaultApi.apiV3DbwWarehousesWarehouseIdContactsPut` — Обновить список контактов
- `items.DefaultApi.apiV3OfficesGet` — Получить список складов WB
- `items.DefaultApi.apiV3StocksWarehouseIdDelete` — Удалить остатки товаров
- `items.DefaultApi.apiV3StocksWarehouseIdPost` — Получить остатки товаров
- `items.DefaultApi.apiV3StocksWarehouseIdPut` — Обновить остатки товаров
- `items.DefaultApi.apiV3WarehousesGet` — Получить список складов продавца
- `items.DefaultApi.apiV3WarehousesPost` — Создать склад продавца
- `items.DefaultApi.apiV3WarehousesWarehouseIdDelete` — Удалить склад продавца
- `items.DefaultApi.apiV3WarehousesWarehouseIdPut` — Обновить склад продавца
- `items.DefaultApi.contentV2BarcodesPost` — Генерация баркодов
- `items.DefaultApi.contentV2CardsDeleteTrashPost` — Перенос карточек товаров в корзину
- `items.DefaultApi.contentV2CardsErrorListPost` — Список несозданных карточек товаров с ошибками
- `items.DefaultApi.contentV2CardsLimitsGet` — Лимиты карточек товаров
- `items.DefaultApi.contentV2CardsMoveNmPost` — Объединение и разъединение карточек товаров
- `items.DefaultApi.contentV2CardsRecoverPost` — Восстановление карточек товаров из корзины
- `items.DefaultApi.contentV2CardsUpdatePost` — Редактирование карточек товаров
- `items.DefaultApi.contentV2CardsUploadAddPost` — Создание карточек товаров с присоединением
- `items.DefaultApi.contentV2CardsUploadPost` — Создание карточек товаров
- `items.DefaultApi.contentV2DirectoryColorsGet` — Цвет
- `items.DefaultApi.contentV2DirectoryCountriesGet` — Страна производства
- `items.DefaultApi.contentV2DirectoryKindsGet` — Пол
- `items.DefaultApi.contentV2DirectorySeasonsGet` — Сезон
- `items.DefaultApi.contentV2DirectoryTnvedGet` — ТНВЭД-код
- `items.DefaultApi.contentV2DirectoryVatGet` — Ставка НДС
- `items.DefaultApi.contentV2GetCardsListPost` — Список карточек товаров
- `items.DefaultApi.contentV2GetCardsTrashPost` — Список карточек товаров в корзине
- `items.DefaultApi.contentV2ObjectAllGet` — Список предметов
- `items.DefaultApi.contentV2ObjectCharcsSubjectIdGet` — Характеристики предмета
- `items.DefaultApi.contentV2ObjectParentAllGet` — Родительские категории товаров
- `items.DefaultApi.contentV2TagIdDelete` — Удаление ярлыка
- `items.DefaultApi.contentV2TagIdPatch` — Изменение ярлыка
- `items.DefaultApi.contentV2TagNomenclatureLinkPost` — Управление ярлыками в карточке товара
- `items.DefaultApi.contentV2TagPost` — Создание ярлыка
- `items.DefaultApi.contentV2TagsGet` — Список ярлыков
- `items.DefaultApi.contentV3MediaFilePost` — Загрузить медиафайл
- `items.DefaultApi.contentV3MediaSavePost` — Загрузить медиафайлы по ссылкам
- `items.DefaultApi.postV1RecommendationsList` — Список рекомендаций в карточках товаров
- `items.DefaultApi.postV1RecommendationsSet` — Установить рекомендации для товаров
- `items.DefaultApi.postV1UploadTaskB2bWholesale` — Установить оптовые скидки для B2B-продаж

### orders_fbs (`orders_fbs`)
- `orders_fbs.DefaultApi.getMarketplaceV3FbsSettingsAutoreturns` — Получить настройки автовозврата продавца
- `orders_fbs.DefaultApi.getMarketplaceV3FbsSettingsAutoreturnsSubcategoriesRestricted` — Получить предметы, которые не хранятся на складах WB
- `orders_fbs.DefaultApi.patchMarketplaceV3FbsSettingsAutoreturns` — Обновить настройки автовозврата продавца
- `orders_fbs.DefaultApi.patchMarketplaceV3FbsSettingsAutoreturnsItems` — Обновить настройки автовозврата товаров
- `orders_fbs.DefaultApi.postMarketplaceV3FbsSettingsAutoreturnsItems` — Получить настройки автовозврата товаров
- `orders_fbs.FBSApi.apiMarketplaceV3FbsOrdersArchiveGet` — Получить список архивных сборочных заданий
- `orders_fbs.FBSApi.apiMarketplaceV3OrdersMetaPost` — Получить идентификаторы маркировки сборочных заданий
- `orders_fbs.FBSApi.apiMarketplaceV3OrdersOrderIdMetaCustomsDeclarationPut` — Закрепить номер ДТ за сборочным заданием
- `orders_fbs.FBSApi.apiMarketplaceV3SuppliesSupplyIdOrderIdsGet` — Получить ID сборочных заданий поставки
- `orders_fbs.FBSApi.apiMarketplaceV3SuppliesSupplyIdOrdersPatch` — Добавить сборочные задания к поставке
- `orders_fbs.FBSApi.apiV3OrdersClientPost` — Заказы с информацией по клиенту
- `orders_fbs.FBSApi.apiV3OrdersGet` — Получить информацию о сборочных заданиях
- `orders_fbs.FBSApi.apiV3OrdersNewGet` — Получить список новых сборочных заданий
- `orders_fbs.FBSApi.apiV3OrdersOrderIdCancelPatch` — Отменить сборочное задание
- `orders_fbs.FBSApi.apiV3OrdersOrderIdMetaDelete` — Удалить идентификаторы маркировки сборочного задания
- `orders_fbs.FBSApi.apiV3OrdersOrderIdMetaExpirationPut` — Закрепить за сборочным заданием срок годности товара
- `orders_fbs.FBSApi.apiV3OrdersOrderIdMetaGtinPut` — Закрепить GTIN за сборочным заданием
- `orders_fbs.FBSApi.apiV3OrdersOrderIdMetaImeiPut` — Закрепить IMEI за сборочным заданием
- `orders_fbs.FBSApi.apiV3OrdersOrderIdMetaSgtinPut` — Закрепить код маркировки Честного знака за сборочным заданием
- `orders_fbs.FBSApi.apiV3OrdersOrderIdMetaUinPut` — Закрепить УИН за сборочным заданием
- `orders_fbs.FBSApi.apiV3OrdersStatusHistoryPost` — История статусов для сборочных заданий трансграничных поставок
- `orders_fbs.FBSApi.apiV3OrdersStatusPost` — Получить статусы сборочных заданий
- `orders_fbs.FBSApi.apiV3OrdersStickersCrossBorderPost` — Получить стикеры сборочных заданий трансграничных поставок
- `orders_fbs.FBSApi.apiV3OrdersStickersPost` — Получить стикеры сборочных заданий
- `orders_fbs.FBSApi.apiV3PassesGet` — Получить список пропусков
- `orders_fbs.FBSApi.apiV3PassesOfficesGet` — Получить список складов, для которых требуется пропуск
- `orders_fbs.FBSApi.apiV3PassesPassIdDelete` — Удалить пропуск
- `orders_fbs.FBSApi.apiV3PassesPassIdPut` — Обновить пропуск
- `orders_fbs.FBSApi.apiV3PassesPost` — Создать пропуск
- `orders_fbs.FBSApi.apiV3SuppliesGet` — Получить список поставок
- `orders_fbs.FBSApi.apiV3SuppliesOrdersReshipmentGet` — Получить все сборочные задания для повторной отгрузки
- `orders_fbs.FBSApi.apiV3SuppliesPost` — Создать новую поставку
- `orders_fbs.FBSApi.apiV3SuppliesSupplyIdBarcodeGet` — Получить QR-код поставки
- `orders_fbs.FBSApi.apiV3SuppliesSupplyIdDelete` — Удалить поставку
- `orders_fbs.FBSApi.apiV3SuppliesSupplyIdDeliverPatch` — Передать поставку в доставку
- `orders_fbs.FBSApi.apiV3SuppliesSupplyIdGet` — Получить информацию о поставке
- `orders_fbs.FBSApi.apiV3SuppliesSupplyIdTrbxDelete` — Удалить грузоместа из поставки
- `orders_fbs.FBSApi.apiV3SuppliesSupplyIdTrbxGet` — Получить список грузомест поставки
- `orders_fbs.FBSApi.apiV3SuppliesSupplyIdTrbxPost` — Добавить грузоместа к поставке
- `orders_fbs.FBSApi.apiV3SuppliesSupplyIdTrbxStickersPost` — Получить стикеры грузомест поставки
- `orders_fbs.FBSApi.getV3FbsShippingPoints` — Получить список пунктов отгрузки поставок
- `orders_fbs.FBSApi.patchV3FbsSuppliesShippingMethod` — Установить параметры отгрузки поставок
- `orders_fbs.FBSApi.patchV3FbsSuppliesWaybill` — Установить ID ЭТрН поставок

### orders_dbw (`orders_dbw`)
- `orders_dbw.DBWApi.getV3DbwOrders` — Получить информацию о завершенных сборочных заданиях
- `orders_dbw.DBWApi.getV3DbwOrdersNew` — Получить список новых сборочных заданий
- `orders_dbw.DBWApi.patchV3DbwOrdersOrderIdCancel` — Отменить сборочное задание
- `orders_dbw.DBWApi.patchV3DbwOrdersOrderIdConfirm` — Перевести на сборку
- `orders_dbw.DBWApi.postV3DbwOrdersClient` — Информация о покупателе
- `orders_dbw.DBWApi.postV3DbwOrdersCourier` — Информация о курьере
- `orders_dbw.DBWApi.postV3DbwOrdersDeliveryDate` — Получить дату и время доставки
- `orders_dbw.DBWApi.postV3DbwOrdersMetaDelete` — Удалить идентификаторы маркировки сборочных заданий
- `orders_dbw.DBWApi.postV3DbwOrdersMetaDetails` — Получить идентификаторы маркировки сборочных заданий
- `orders_dbw.DBWApi.postV3DbwOrdersMetaSgtin` — Закрепить коды маркировки Честного знака за сборочными заданиями
- `orders_dbw.DBWApi.postV3DbwOrdersStatus` — Получить статусы сборочных заданий
- `orders_dbw.DBWApi.postV3DbwOrdersStatusDeliver` — Перевести сборочные задания в доставку
- `orders_dbw.DBWApi.postV3DbwOrdersStickers` — Получить стикеры сборочных заданий
- `orders_dbw.DBWApi.putV3DbwOrdersOrderIdMetaGtin` — Закрепить GTIN за сборочным заданием
- `orders_dbw.DBWApi.putV3DbwOrdersOrderIdMetaImei` — Закрепить IMEI за сборочным заданием
- `orders_dbw.DBWApi.putV3DbwOrdersOrderIdMetaUin` — Закрепить УИН за сборочным заданием

### dbs (`dbs`)
- `dbs.DBSApi.getV3DbsOrders` — Получить информацию о завершенных сборочных заданиях
- `dbs.DBSApi.getV3DbsOrdersNew` — Получить список новых сборочных заданий
- `dbs.DBSApi.postV3DbsGroupsInfo` — Получить информацию о платной доставке
- `dbs.DBSApi.postV3DbsOrdersB2bInfo` — Информация о покупателе B2B
- `dbs.DBSApi.postV3DbsOrdersClient` — Информация о покупателе
- `dbs.DBSApi.postV3DbsOrdersDeliveryDate` — Получить дату и время доставки
- `dbs.DBSApi.postV3DbsOrdersFinalPrice` — Получить цены продавца и суммы к оплате
- `dbs.DBSApi.postV3DbsOrdersMetaCustomsDeclaration` — Закрепить номера ДТ за сборочными заданиями
- `dbs.DBSApi.postV3DbsOrdersMetaDelete` — Удалить идентификаторы маркировки сборочных заданий
- `dbs.DBSApi.postV3DbsOrdersMetaDetails` — Получить идентификаторы маркировки сборочных заданий
- `dbs.DBSApi.postV3DbsOrdersMetaGtin` — Закрепить GTIN за сборочными заданиями
- `dbs.DBSApi.postV3DbsOrdersMetaImei` — Закрепить IMEI за сборочными заданиями
- `dbs.DBSApi.postV3DbsOrdersMetaSgtin` — Закрепить коды маркировки Честного знака за сборочными заданиями
- `dbs.DBSApi.postV3DbsOrdersMetaUin` — Закрепить УИН за сборочными заданиями
- `dbs.DBSApi.postV3DbsOrdersStatusCancel` — Отменить сборочные задания
- `dbs.DBSApi.postV3DbsOrdersStatusConfirm` — Перевести сборочные задания на сборку
- `dbs.DBSApi.postV3DbsOrdersStatusDeliver` — Перевести сборочные задания в доставку
- `dbs.DBSApi.postV3DbsOrdersStatusInfo` — Получить статусы сборочных заданий
- `dbs.DBSApi.postV3DbsOrdersStatusReceive` — Сообщить о получении заказов
- `dbs.DBSApi.postV3DbsOrdersStatusReject` — Сообщить об отказе от заказов
- `dbs.DBSApi.postV3DbsOrdersStickers` — Получить стикеры для сборочных заданий с доставкой в ПВЗ

### in_store_pickup (`in_store_pickup`)
- `in_store_pickup.DefaultApi.getV3ClickCollectOrders` — Получить информацию о завершённых сборочных заданиях
- `in_store_pickup.DefaultApi.getV3ClickCollectOrdersNew` — Получить список новых сборочных заданий
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersClient` — Информация о покупателе
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersClientIdentity` — Проверить, что заказ принадлежит покупателю
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersFinalPrice` — Получить цены продавца и суммы к оплате
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersMetaCustomsDeclaration` — Закрепить номера ДТ за сборочными заданиями
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersMetaDelete` — Удалить идентификаторы маркировки сборочных заданий
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersMetaDetails` — Получить идентификаторы маркировки сборочных заданий
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersMetaGtin` — Закрепить GTIN за сборочными заданиями
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersMetaImei` — Закрепить IMEI за сборочными заданиями
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersMetaSgtin` — Закрепить коды маркировки Честного знака за сборочными заданиями
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersMetaUin` — Закрепить УИН за сборочными заданиями
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersStatusCancel` — Отменить сборочные задания
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersStatusConfirm` — Перевести сборочные задания на сборку
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersStatusInfo` — Получить статусы сборочных заданий
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersStatusPrepare` — Сообщить, что сборочные задания готовы к выдаче
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersStatusReceive` — Сообщить, что заказы приняты покупателями
- `in_store_pickup.DefaultApi.postV3ClickCollectOrdersStatusReject` — Сообщить об отказе от заказов

### orders_fbw (`orders_fbw`)
- `orders_fbw.DefaultApi.getV1SuppliesId` — Детали поставки
- `orders_fbw.DefaultApi.getV1SuppliesIdGoods` — Товары поставки
- `orders_fbw.DefaultApi.getV1SuppliesIdPackage` — Упаковка поставки
- `orders_fbw.DefaultApi.getV1TransitTariffs` — Транзитные направления
- `orders_fbw.DefaultApi.getV1Warehouses` — Список складов
- `orders_fbw.DefaultApi.postV1AcceptanceOptions` — Опции приёмки
- `orders_fbw.DefaultApi.postV1Supplies` — Список поставок

### promotion (`promotion`)
- `promotion.DefaultApi.deleteV0NormqueryBids` — Удалить ставки поисковых кластеров
- `promotion.DefaultApi.getV0BidsRecommendations` — Рекомендуемые ставки для карточек товаров и поисковых кластеров
- `promotion.DefaultApi.getV0Delete` — Удаление кампании
- `promotion.DefaultApi.getV0Pause` — Пауза кампании
- `promotion.DefaultApi.getV0Start` — Запуск кампании
- `promotion.DefaultApi.getV0Stop` — Завершение кампании
- `promotion.DefaultApi.getV1Advert` — Информация о медиакампании
- `promotion.DefaultApi.getV1Adverts` — Список медиакампаний
- `promotion.DefaultApi.getV1Balance` — Баланс
- `promotion.DefaultApi.getV1Budget` — Бюджет кампании
- `promotion.DefaultApi.getV1CalendarPromotions` — Список акций
- `promotion.DefaultApi.getV1CalendarPromotionsDetails` — Детальная информация об акциях
- `promotion.DefaultApi.getV1CalendarPromotionsNomenclatures` — Список товаров для участия в акции
- `promotion.DefaultApi.getV1Config` — Конфигурационные значения продвижения
- `promotion.DefaultApi.getV1Count` — Количество медиакампаний
- `promotion.DefaultApi.getV1Payments` — Получение истории пополнений счёта
- `promotion.DefaultApi.getV1PromotionCount` — Списки кампаний
- `promotion.DefaultApi.getV1SupplierSubjects` — Предметы для кампаний
- `promotion.DefaultApi.getV1Upd` — Получение истории затрат
- `promotion.DefaultApi.getV2Adverts` — Информация о кампаниях
- `promotion.DefaultApi.getV3Fullstats` — Статистика кампаний
- `promotion.DefaultApi.patchV0AuctionNms` — Изменение списка карточек товаров в кампаниях
- `promotion.DefaultApi.patchV1Bids` — Изменение ставок в кампаниях
- `promotion.DefaultApi.postV0NormqueryBids` — Установить ставки для поисковых кластеров
- `promotion.DefaultApi.postV0NormqueryGetBids` — Список ставок поисковых кластеров
- `promotion.DefaultApi.postV0NormqueryGetMinus` — Список минус-фраз кампаний
- `promotion.DefaultApi.postV0NormqueryList` — Списки активных и неактивных поисковых кластеров
- `promotion.DefaultApi.postV0NormquerySetMinus` — Установка и удаление минус-фраз
- `promotion.DefaultApi.postV0NormqueryStats` — Статистика поисковых кластеров
- `promotion.DefaultApi.postV0Rename` — Переименование кампании
- `promotion.DefaultApi.postV1BidsMin` — Минимальные ставки для карточек товаров
- `promotion.DefaultApi.postV1BudgetDeposit` — Пополнение бюджета кампании
- `promotion.DefaultApi.postV1CalendarPromotionsUpload` — Добавить товар в акцию
- `promotion.DefaultApi.postV1NormqueryBids` — Установить ставки для поисковых кластеров в валюте аккаунта продавца
- `promotion.DefaultApi.postV1NormqueryStats` — Статистика по поисковым кластерам с детализацией по дням
- `promotion.DefaultApi.postV1Stats` — Статистика медиакампаний
- `promotion.DefaultApi.postV2SeacatSaveAd` — Создать кампанию
- `promotion.DefaultApi.postV2SupplierNms` — Карточки товаров для кампаний
- `promotion.DefaultApi.putV0AuctionPlacements` — Изменение мест размещения в кампаниях с ручной ставкой

### communications (`communications`)
- `communications.DefaultApi.deleteFeedbacksV1Pins` — Открепить отзывы
- `communications.DefaultApi.getFeedbacksV1Pins` — Список закреплённых и откреплённых отзывов
- `communications.DefaultApi.getFeedbacksV1PinsCount` — Количество закреплённых и откреплённых отзывов
- `communications.DefaultApi.getFeedbacksV1PinsLimits` — Лимиты закреплённых отзывов
- `communications.DefaultApi.getV1Claims` — Заявки покупателей на возврат
- `communications.DefaultApi.getV1Feedback` — Получить отзыв по ID
- `communications.DefaultApi.getV1Feedbacks` — Список отзывов
- `communications.DefaultApi.getV1FeedbacksArchive` — Список архивных отзывов
- `communications.DefaultApi.getV1FeedbacksCount` — Количество отзывов
- `communications.DefaultApi.getV1FeedbacksCountUnanswered` — Необработанные отзывы
- `communications.DefaultApi.getV1NewFeedbacksQuestions` — Непросмотренные отзывы и вопросы
- `communications.DefaultApi.getV1Question` — Получить вопрос по ID
- `communications.DefaultApi.getV1Questions` — Список вопросов
- `communications.DefaultApi.getV1QuestionsCount` — Количество вопросов
- `communications.DefaultApi.getV1QuestionsCountUnanswered` — Неотвеченные вопросы
- `communications.DefaultApi.getV1SellerChats` — Список чатов
- `communications.DefaultApi.getV1SellerDownloadId` — Получить файл из сообщения
- `communications.DefaultApi.getV1SellerEvents` — События чатов
- `communications.DefaultApi.patchV1Claim` — Ответ на заявку покупателя
- `communications.DefaultApi.patchV1FeedbacksAnswer` — Отредактировать ответ на отзыв
- `communications.DefaultApi.patchV1Questions` — Работа с вопросами
- `communications.DefaultApi.postFeedbacksV1Pins` — Закрепить отзывы
- `communications.DefaultApi.postV1FeedbacksAnswer` — Ответить на отзыв
- `communications.DefaultApi.postV1FeedbacksOrderReturn` — Возврат товара по ID отзыва
- `communications.DefaultApi.postV1SellerMessage` — Отправить сообщение

### rates (`rates`)
- `rates.DefaultApi.getV1AcceptanceCoefficients` — Тарифы на поставку
- `rates.DefaultApi.getV1TariffsBox` — Тарифы для коробов
- `rates.DefaultApi.getV1TariffsCommission` — Комиссия по категориям товаров
- `rates.DefaultApi.getV1TariffsPallet` — Тарифы для монопаллет
- `rates.DefaultApi.getV1TariffsReturn` — Тарифы на возврат

### analytics (`analytics`)
- `analytics.CSVApi.getV2NmReportDownloads` — Получить список отчётов
- `analytics.CSVApi.getV2NmReportDownloadsFileDownloadId` — Получить отчёт
- `analytics.CSVApi.postV2NmReportDownloads` — Создать отчёт
- `analytics.CSVApi.postV2NmReportDownloadsRetry` — Сгенерировать отчёт повторно
- `analytics.DefaultApi.postAnalyticsV1StocksReportSellerWarehouses` — Остатки на складах продавца
- `analytics.DefaultApi.postV1OrderFeed` — Получить отчёт
- `analytics.DefaultApi.postV1StocksReportWbWarehouses` — Остатки на складах WB
- `analytics.DefaultApi.postV2ItemRating` — Получить отчёт
- `analytics.DefaultApi.postV2SearchReportProductOrders` — Заказы и позиции по поисковым запросам товара
- `analytics.DefaultApi.postV2SearchReportProductSearchTexts` — Поисковые запросы по товару
- `analytics.DefaultApi.postV2SearchReportReport` — Основная страница
- `analytics.DefaultApi.postV2SearchReportTableDetails` — Пагинация по товарам в группе
- `analytics.DefaultApi.postV2SearchReportTableGroups` — Пагинация по группам
- `analytics.DefaultApi.postV2StocksReportOffices` — Данные по складам
- `analytics.DefaultApi.postV2StocksReportProductsGroups` — Данные по группам
- `analytics.DefaultApi.postV2StocksReportProductsProducts` — Данные по товарам
- `analytics.DefaultApi.postV2StocksReportProductsSizes` — Данные по размерам
- `analytics.DefaultApi.postV3SalesFunnelGroupedHistory` — Статистика групп карточек товаров по дням
- `analytics.DefaultApi.postV3SalesFunnelProducts` — Статистика карточек товаров за период
- `analytics.DefaultApi.postV3SalesFunnelProductsHistory` — Статистика карточек товаров по дням

### reports (`reports`)
- `reports.CApi.postV1AnalyticsExciseReport` — Получить отчёт
- `reports.DefaultApi.getV1AcceptanceReport` — Создать отчёт
- `reports.DefaultApi.getV1AcceptanceReportTasksTaskIdDownload` — Получить отчёт
- `reports.DefaultApi.getV1AcceptanceReportTasksTaskIdStatus` — Проверить статус
- `reports.DefaultApi.getV1AnalyticsAntifraudDetails` — Самовыкупы
- `reports.DefaultApi.getV1AnalyticsBannedProducsBlocked` — Получить отчёт
- `reports.DefaultApi.getV1AnalyticsBrandShare` — Получить отчёт
- `reports.DefaultApi.getV1AnalyticsBrandShareBrands` — Бренды продавца
- `reports.DefaultApi.getV1AnalyticsBrandShareParentSubjects` — Родительские категории бренда
- `reports.DefaultApi.getV1AnalyticsGoodsLabeling` — Маркировка товара
- `reports.DefaultApi.getV1AnalyticsGoodsReturn` — Получить отчёт
- `reports.DefaultApi.getV1AnalyticsRegionSale` — Получить отчёт
- `reports.DefaultApi.getV1Deductions` — Подмены и неверные вложения
- `reports.DefaultApi.getV1MeasurementPenalties` — Удержания за занижение габаритов упаковки
- `reports.DefaultApi.getV1PaidStorage` — Создать отчёт
- `reports.DefaultApi.getV1PaidStorageTasksTaskIdDownload` — Получить отчёт
- `reports.DefaultApi.getV1PaidStorageTasksTaskIdStatus` — Проверить статус
- `reports.DefaultApi.getV1SupplierOrders` — Заказы
- `reports.DefaultApi.getV1SupplierSales` — Продажи
- `reports.DefaultApi.getV1WarehouseMeasurements` — Замеры склада
- `reports.DefaultApi.getV1WarehouseRemains` — Создать отчёт
- `reports.DefaultApi.getV1WarehouseRemainsTasksTaskIdDownload` — Получить отчёт
- `reports.DefaultApi.getV1WarehouseRemainsTasksTaskIdStatus` — Проверить статус

### finances (`finances`)
- `finances.DefaultApi.getV1AccountBalance` — Получить баланс продавца
- `finances.DefaultApi.getV1DocumentsCategories` — Категории документов
- `finances.DefaultApi.getV1DocumentsDownload` — Получить документ
- `finances.DefaultApi.getV1DocumentsList` — Список документов
- `finances.DefaultApi.postV1AcquiringDetailed` — Детализации к отчётам об издержках на приём платежей за период
- `finances.DefaultApi.postV1AcquiringDetailedReportId` — Детализации к отчётам об издержках на приём платежей по ID отчётов
- `finances.DefaultApi.postV1AcquiringList` — Список отчётов об издержках на приём платежей
- `finances.DefaultApi.postV1DocumentsDownloadAll` — Получить документы
- `finances.DefaultApi.postV1SalesReportsDetailed` — Детализации к отчётам реализации за период
- `finances.DefaultApi.postV1SalesReportsDetailedReportId` — Детализации к отчётам реализации по ID отчётов
- `finances.DefaultApi.postV1SalesReportsList` — Список отчётов реализации
<!-- NPM_METHODS_LIST_END -->
