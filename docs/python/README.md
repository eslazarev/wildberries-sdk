# Wildberries SDK for Python (wildberries-sdk)

<img src="https://raw.githubusercontent.com/eslazarev/wildberries-sdk/main/.github/images/using_wildberries_sdk_python.gif">

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
pip install wildberries-sdk
```

## Пример получения 100 неотвеченных отзывов (клиент - communications)

```python
import os
from wildberries_sdk import communications

token = os.getenv("WB_API_TOKEN")

api = communications.DefaultApi(
    communications.ApiClient(
        communications.Configuration(api_key={"HeaderApiKey": token})
    )
)
feedbacks = api.api_v1_feedbacks_get(is_answered=False, take=100, skip=0).data.feedbacks

print(feedbacks)
```

## Доступные клиенты

Импортируйте каждый клиент как `wildberries_sdk.<client>`:

- `wildberries_sdk.general`
- `wildberries_sdk.products`
- `wildberries_sdk.orders_fbs`
- `wildberries_sdk.orders_dbw`
- `wildberries_sdk.orders_dbs`
- `wildberries_sdk.in_store_pickup`
- `wildberries_sdk.orders_fbw`
- `wildberries_sdk.promotion`
- `wildberries_sdk.communications`
- `wildberries_sdk.tariffs`
- `wildberries_sdk.analytics`
- `wildberries_sdk.reports`
- `wildberries_sdk.finances`
- `wildberries_sdk.wbd`

<!-- PY_METHODS_LIST_START -->
## Методы API

### general (`general`)
- `general.DefaultApi.delete_v1_user` — `DELETE /api/v1/user` — Удалить пользователя
- `general.DefaultApi.get_ping` — `GET /ping` — Проверка подключения
- `general.DefaultApi.get_v1_rating` — `GET /api/common/v1/rating` — Получить рейтинг продавца
- `general.DefaultApi.get_v1_seller_info` — `GET /api/v1/seller-info` — Получить информацию о продавце
- `general.DefaultApi.get_v1_subscriptions` — `GET /api/common/v1/subscriptions` — Получить информацию о подписке Джем
- `general.DefaultApi.get_v1_tariff_constructor_options` — `GET /api/common/v1/tariff-constructor/options` — Получить информацию об опциях Конструктора тарифов
- `general.DefaultApi.get_v1_users` — `GET /api/v1/users` — Получить список активных или приглашённых пользователей продавца
- `general.DefaultApi.get_v2_news` — `GET /api/communications/v2/news` — Получение новостей портала продавцов
- `general.DefaultApi.post_v1_invite` — `POST /api/v1/invite` — Создать приглашение для нового пользователя
- `general.DefaultApi.put_v1_users_access` — `PUT /api/v1/users/access` — Изменить права доступа пользователей

### items (`items`)
- `items.DefaultApi.api_content_v1_brands_get` — `GET /api/content/v1/brands` — Бренды
- `items.DefaultApi.api_v2_buffer_goods_task_get` — `GET /api/v2/buffer/goods/task` — Детализация необработанной загрузки
- `items.DefaultApi.api_v2_buffer_tasks_get` — `GET /api/v2/buffer/tasks` — Состояние необработанной загрузки
- `items.DefaultApi.api_v2_history_goods_task_get` — `GET /api/v2/history/goods/task` — Детализация обработанной загрузки
- `items.DefaultApi.api_v2_history_tasks_get` — `GET /api/v2/history/tasks` — Состояние обработанной загрузки
- `items.DefaultApi.api_v2_list_goods_filter_get` — `GET /api/v2/list/goods/filter` — Получить товары с ценами
- `items.DefaultApi.api_v2_list_goods_filter_post` — `POST /api/v2/list/goods/filter` — Получить товары с ценами по артикулам
- `items.DefaultApi.api_v2_list_goods_size_nm_get` — `GET /api/v2/list/goods/size/nm` — Получить размеры товара с ценами
- `items.DefaultApi.api_v2_quarantine_goods_get` — `GET /api/v2/quarantine/goods` — Получить товары в карантине
- `items.DefaultApi.api_v2_upload_task_club_discount_post` — `POST /api/v2/upload/task/club-discount` — Установить скидки WB Клуба
- `items.DefaultApi.api_v2_upload_task_post` — `POST /api/v2/upload/task` — Установить цены и скидки
- `items.DefaultApi.api_v2_upload_task_size_post` — `POST /api/v2/upload/task/size` — Установить цены для размеров
- `items.DefaultApi.api_v3_dbw_warehouses_warehouse_id_contacts_get` — `GET /api/v3/dbw/warehouses/{warehouseId}/contacts` — Список контактов
- `items.DefaultApi.api_v3_dbw_warehouses_warehouse_id_contacts_put` — `PUT /api/v3/dbw/warehouses/{warehouseId}/contacts` — Обновить список контактов
- `items.DefaultApi.api_v3_offices_get` — `GET /api/v3/offices` — Получить список складов WB
- `items.DefaultApi.api_v3_stocks_warehouse_id_delete` — `DELETE /api/v3/stocks/{warehouseId}` — Удалить остатки товаров
- `items.DefaultApi.api_v3_stocks_warehouse_id_post` — `POST /api/v3/stocks/{warehouseId}` — Получить остатки товаров
- `items.DefaultApi.api_v3_stocks_warehouse_id_put` — `PUT /api/v3/stocks/{warehouseId}` — Обновить остатки товаров
- `items.DefaultApi.api_v3_warehouses_get` — `GET /api/v3/warehouses` — Получить список складов продавца
- `items.DefaultApi.api_v3_warehouses_post` — `POST /api/v3/warehouses` — Создать склад продавца
- `items.DefaultApi.api_v3_warehouses_warehouse_id_delete` — `DELETE /api/v3/warehouses/{warehouseId}` — Удалить склад продавца
- `items.DefaultApi.api_v3_warehouses_warehouse_id_put` — `PUT /api/v3/warehouses/{warehouseId}` — Обновить склад продавца
- `items.DefaultApi.content_v2_barcodes_post` — `POST /content/v2/barcodes` — Генерация баркодов
- `items.DefaultApi.content_v2_cards_delete_trash_post` — `POST /content/v2/cards/delete/trash` — Перенос карточек товаров в корзину
- `items.DefaultApi.content_v2_cards_error_list_post` — `POST /content/v2/cards/error/list` — Список несозданных карточек товаров с ошибками
- `items.DefaultApi.content_v2_cards_limits_get` — `GET /content/v2/cards/limits` — Лимиты карточек товаров
- `items.DefaultApi.content_v2_cards_move_nm_post` — `POST /content/v2/cards/moveNm` — Объединение и разъединение карточек товаров
- `items.DefaultApi.content_v2_cards_recover_post` — `POST /content/v2/cards/recover` — Восстановление карточек товаров из корзины
- `items.DefaultApi.content_v2_cards_update_post` — `POST /content/v2/cards/update` — Редактирование карточек товаров
- `items.DefaultApi.content_v2_cards_upload_add_post` — `POST /content/v2/cards/upload/add` — Создание карточек товаров с присоединением
- `items.DefaultApi.content_v2_cards_upload_post` — `POST /content/v2/cards/upload` — Создание карточек товаров
- `items.DefaultApi.content_v2_directory_colors_get` — `GET /content/v2/directory/colors` — Цвет
- `items.DefaultApi.content_v2_directory_countries_get` — `GET /content/v2/directory/countries` — Страна производства
- `items.DefaultApi.content_v2_directory_kinds_get` — `GET /content/v2/directory/kinds` — Пол
- `items.DefaultApi.content_v2_directory_seasons_get` — `GET /content/v2/directory/seasons` — Сезон
- `items.DefaultApi.content_v2_directory_tnved_get` — `GET /content/v2/directory/tnved` — ТНВЭД-код
- `items.DefaultApi.content_v2_directory_vat_get` — `GET /content/v2/directory/vat` — Ставка НДС
- `items.DefaultApi.content_v2_get_cards_list_post` — `POST /content/v2/get/cards/list` — Список карточек товаров
- `items.DefaultApi.content_v2_get_cards_trash_post` — `POST /content/v2/get/cards/trash` — Список карточек товаров в корзине
- `items.DefaultApi.content_v2_object_all_get` — `GET /content/v2/object/all` — Список предметов
- `items.DefaultApi.content_v2_object_charcs_subject_id_get` — `GET /content/v2/object/charcs/{subjectId}` — Характеристики предмета
- `items.DefaultApi.content_v2_object_parent_all_get` — `GET /content/v2/object/parent/all` — Родительские категории товаров
- `items.DefaultApi.content_v2_tag_id_delete` — `DELETE /content/v2/tag/{id}` — Удаление ярлыка
- `items.DefaultApi.content_v2_tag_id_patch` — `PATCH /content/v2/tag/{id}` — Изменение ярлыка
- `items.DefaultApi.content_v2_tag_nomenclature_link_post` — `POST /content/v2/tag/nomenclature/link` — Управление ярлыками в карточке товара
- `items.DefaultApi.content_v2_tag_post` — `POST /content/v2/tag` — Создание ярлыка
- `items.DefaultApi.content_v2_tags_get` — `GET /content/v2/tags` — Список ярлыков
- `items.DefaultApi.content_v3_media_file_post` — `POST /content/v3/media/file` — Загрузить медиафайл
- `items.DefaultApi.content_v3_media_save_post` — `POST /content/v3/media/save` — Загрузить медиафайлы по ссылкам
- `items.DefaultApi.post_v1_recommendations_list` — `POST /api/content/v1/recommendations/list` — Список рекомендаций в карточках товаров
- `items.DefaultApi.post_v1_recommendations_set` — `POST /api/content/v1/recommendations/set` — Установить рекомендации для товаров
- `items.DefaultApi.post_v1_upload_task_b2b_wholesale` — `POST /api/discounts-prices/v1/upload/task/b2b/wholesale` — Установить оптовые скидки для B2B-продаж

### orders_fbs (`orders_fbs`)
- `orders_fbs.DefaultApi.api_marketplace_v3_fbs_orders_archive_get` — `GET /api/marketplace/v3/fbs/orders/archive` — Получить список архивных сборочных заданий
- `orders_fbs.DefaultApi.api_marketplace_v3_orders_meta_post` — `POST /api/marketplace/v3/orders/meta` — Получить идентификаторы маркировки сборочных заданий
- `orders_fbs.DefaultApi.api_marketplace_v3_orders_order_id_meta_customs_declaration_put` — `PUT /api/marketplace/v3/orders/{orderId}/meta/customs-declaration` — Закрепить номер ДТ за сборочным заданием
- `orders_fbs.DefaultApi.api_marketplace_v3_supplies_supply_id_order_ids_get` — `GET /api/marketplace/v3/supplies/{supplyId}/order-ids` — Получить ID сборочных заданий поставки
- `orders_fbs.DefaultApi.api_marketplace_v3_supplies_supply_id_orders_patch` — `PATCH /api/marketplace/v3/supplies/{supplyId}/orders` — Добавить сборочные задания к поставке
- `orders_fbs.DefaultApi.api_v3_orders_client_post` — `POST /api/v3/orders/client` — Заказы с информацией по клиенту
- `orders_fbs.DefaultApi.api_v3_orders_get` — `GET /api/v3/orders` — Получить информацию о сборочных заданиях
- `orders_fbs.DefaultApi.api_v3_orders_new_get` — `GET /api/v3/orders/new` — Получить список новых сборочных заданий
- `orders_fbs.DefaultApi.api_v3_orders_order_id_cancel_patch` — `PATCH /api/v3/orders/{orderId}/cancel` — Отменить сборочное задание
- `orders_fbs.DefaultApi.api_v3_orders_order_id_meta_delete` — `DELETE /api/v3/orders/{orderId}/meta` — Удалить идентификаторы маркировки сборочного задания
- `orders_fbs.DefaultApi.api_v3_orders_order_id_meta_expiration_put` — `PUT /api/v3/orders/{orderId}/meta/expiration` — Закрепить за сборочным заданием срок годности товара
- `orders_fbs.DefaultApi.api_v3_orders_order_id_meta_gtin_put` — `PUT /api/v3/orders/{orderId}/meta/gtin` — Закрепить GTIN за сборочным заданием
- `orders_fbs.DefaultApi.api_v3_orders_order_id_meta_imei_put` — `PUT /api/v3/orders/{orderId}/meta/imei` — Закрепить IMEI за сборочным заданием
- `orders_fbs.DefaultApi.api_v3_orders_order_id_meta_sgtin_put` — `PUT /api/v3/orders/{orderId}/meta/sgtin` — Закрепить код маркировки Честного знака за сборочным заданием
- `orders_fbs.DefaultApi.api_v3_orders_order_id_meta_uin_put` — `PUT /api/v3/orders/{orderId}/meta/uin` — Закрепить УИН за сборочным заданием
- `orders_fbs.DefaultApi.api_v3_orders_status_history_post` — `POST /api/v3/orders/status/history` — История статусов для сборочных заданий трансграничных поставок
- `orders_fbs.DefaultApi.api_v3_orders_status_post` — `POST /api/v3/orders/status` — Получить статусы сборочных заданий
- `orders_fbs.DefaultApi.api_v3_orders_stickers_cross_border_post` — `POST /api/v3/orders/stickers/cross-border` — Получить стикеры сборочных заданий трансграничных поставок
- `orders_fbs.DefaultApi.api_v3_orders_stickers_post` — `POST /api/v3/orders/stickers` — Получить стикеры сборочных заданий
- `orders_fbs.DefaultApi.api_v3_passes_get` — `GET /api/v3/passes` — Получить список пропусков
- `orders_fbs.DefaultApi.api_v3_passes_offices_get` — `GET /api/v3/passes/offices` — Получить список складов, для которых требуется пропуск
- `orders_fbs.DefaultApi.api_v3_passes_pass_id_delete` — `DELETE /api/v3/passes/{passId}` — Удалить пропуск
- `orders_fbs.DefaultApi.api_v3_passes_pass_id_put` — `PUT /api/v3/passes/{passId}` — Обновить пропуск
- `orders_fbs.DefaultApi.api_v3_passes_post` — `POST /api/v3/passes` — Создать пропуск
- `orders_fbs.DefaultApi.api_v3_supplies_get` — `GET /api/v3/supplies` — Получить список поставок
- `orders_fbs.DefaultApi.api_v3_supplies_orders_reshipment_get` — `GET /api/v3/supplies/orders/reshipment` — Получить все сборочные задания для повторной отгрузки
- `orders_fbs.DefaultApi.api_v3_supplies_post` — `POST /api/v3/supplies` — Создать новую поставку
- `orders_fbs.DefaultApi.api_v3_supplies_supply_id_barcode_get` — `GET /api/v3/supplies/{supplyId}/barcode` — Получить QR-код поставки
- `orders_fbs.DefaultApi.api_v3_supplies_supply_id_delete` — `DELETE /api/v3/supplies/{supplyId}` — Удалить поставку
- `orders_fbs.DefaultApi.api_v3_supplies_supply_id_deliver_patch` — `PATCH /api/v3/supplies/{supplyId}/deliver` — Передать поставку в доставку
- `orders_fbs.DefaultApi.api_v3_supplies_supply_id_get` — `GET /api/v3/supplies/{supplyId}` — Получить информацию о поставке
- `orders_fbs.DefaultApi.api_v3_supplies_supply_id_trbx_delete` — `DELETE /api/v3/supplies/{supplyId}/trbx` — Удалить грузоместа из поставки
- `orders_fbs.DefaultApi.api_v3_supplies_supply_id_trbx_get` — `GET /api/v3/supplies/{supplyId}/trbx` — Получить список грузомест поставки
- `orders_fbs.DefaultApi.api_v3_supplies_supply_id_trbx_post` — `POST /api/v3/supplies/{supplyId}/trbx` — Добавить грузоместа к поставке
- `orders_fbs.DefaultApi.api_v3_supplies_supply_id_trbx_stickers_post` — `POST /api/v3/supplies/{supplyId}/trbx/stickers` — Получить стикеры грузомест поставки
- `orders_fbs.DefaultApi.get_marketplace_v3_fbs_settings_autoreturns` — `GET /api/marketplace/v3/fbs/settings/autoreturns` — Получить настройки автовозврата продавца
- `orders_fbs.DefaultApi.get_marketplace_v3_fbs_settings_autoreturns_subcategories_restricted` — `GET /api/marketplace/v3/fbs/settings/autoreturns/subcategories/restricted` — Получить предметы, которые не хранятся на складах WB
- `orders_fbs.DefaultApi.patch_marketplace_v3_fbs_settings_autoreturns` — `PATCH /api/marketplace/v3/fbs/settings/autoreturns` — Обновить настройки автовозврата продавца
- `orders_fbs.DefaultApi.patch_marketplace_v3_fbs_settings_autoreturns_items` — `PATCH /api/marketplace/v3/fbs/settings/autoreturns/items` — Обновить настройки автовозврата товаров
- `orders_fbs.DefaultApi.post_marketplace_v3_fbs_settings_autoreturns_items` — `POST /api/marketplace/v3/fbs/settings/autoreturns/items` — Получить настройки автовозврата товаров

### orders_dbw (`orders_dbw`)
- `orders_dbw.DefaultApi.get_v3_dbw_orders` — `GET /api/v3/dbw/orders` — Получить информацию о завершенных сборочных заданиях
- `orders_dbw.DefaultApi.get_v3_dbw_orders_new` — `GET /api/v3/dbw/orders/new` — Получить список новых сборочных заданий
- `orders_dbw.DefaultApi.patch_v3_dbw_orders_order_id_cancel` — `PATCH /api/v3/dbw/orders/{orderId}/cancel` — Отменить сборочное задание
- `orders_dbw.DefaultApi.patch_v3_dbw_orders_order_id_confirm` — `PATCH /api/v3/dbw/orders/{orderId}/confirm` — Перевести на сборку
- `orders_dbw.DefaultApi.post_v3_dbw_orders_client` — `POST /api/marketplace/v3/dbw/orders/client` — Информация о покупателе
- `orders_dbw.DefaultApi.post_v3_dbw_orders_courier` — `POST /api/v3/dbw/orders/courier` — Информация о курьере
- `orders_dbw.DefaultApi.post_v3_dbw_orders_delivery_date` — `POST /api/v3/dbw/orders/delivery-date` — Получить дату и время доставки
- `orders_dbw.DefaultApi.post_v3_dbw_orders_meta_delete` — `POST /api/marketplace/v3/dbw/orders/meta/delete` — Удалить идентификаторы маркировки сборочных заданий
- `orders_dbw.DefaultApi.post_v3_dbw_orders_meta_details` — `POST /api/marketplace/v3/dbw/orders/meta/details` — Получить идентификаторы маркировки сборочных заданий
- `orders_dbw.DefaultApi.post_v3_dbw_orders_meta_sgtin` — `POST /api/marketplace/v3/dbw/orders/meta/sgtin` — Закрепить коды маркировки Честного знака за сборочными заданиями
- `orders_dbw.DefaultApi.post_v3_dbw_orders_status` — `POST /api/v3/dbw/orders/status` — Получить статусы сборочных заданий
- `orders_dbw.DefaultApi.post_v3_dbw_orders_status_deliver` — `POST /api/marketplace/v3/dbw/orders/status/deliver` — Перевести сборочные задания в доставку
- `orders_dbw.DefaultApi.post_v3_dbw_orders_stickers` — `POST /api/v3/dbw/orders/stickers` — Получить стикеры сборочных заданий
- `orders_dbw.DefaultApi.put_v3_dbw_orders_order_id_meta_gtin` — `PUT /api/v3/dbw/orders/{orderId}/meta/gtin` — Закрепить GTIN за сборочным заданием
- `orders_dbw.DefaultApi.put_v3_dbw_orders_order_id_meta_imei` — `PUT /api/v3/dbw/orders/{orderId}/meta/imei` — Закрепить IMEI за сборочным заданием
- `orders_dbw.DefaultApi.put_v3_dbw_orders_order_id_meta_uin` — `PUT /api/v3/dbw/orders/{orderId}/meta/uin` — Закрепить УИН за сборочным заданием

### dbs (`dbs`)
- `dbs.DefaultApi.get_v3_dbs_orders` — `GET /api/v3/dbs/orders` — Получить информацию о завершенных сборочных заданиях
- `dbs.DefaultApi.get_v3_dbs_orders_new` — `GET /api/v3/dbs/orders/new` — Получить список новых сборочных заданий
- `dbs.DefaultApi.post_v3_dbs_groups_info` — `POST /api/v3/dbs/groups/info` — Получить информацию о платной доставке
- `dbs.DefaultApi.post_v3_dbs_orders_b2b_info` — `POST /api/marketplace/v3/dbs/orders/b2b/info` — Информация о покупателе B2B
- `dbs.DefaultApi.post_v3_dbs_orders_client` — `POST /api/v3/dbs/orders/client` — Информация о покупателе
- `dbs.DefaultApi.post_v3_dbs_orders_delivery_date` — `POST /api/v3/dbs/orders/delivery-date` — Получить дату и время доставки
- `dbs.DefaultApi.post_v3_dbs_orders_final_price` — `POST /api/marketplace/v3/dbs/orders/final-price` — Получить цены продавца и суммы к оплате
- `dbs.DefaultApi.post_v3_dbs_orders_meta_customs_declaration` — `POST /api/marketplace/v3/dbs/orders/meta/customs-declaration` — Закрепить номера ДТ за сборочными заданиями
- `dbs.DefaultApi.post_v3_dbs_orders_meta_delete` — `POST /api/marketplace/v3/dbs/orders/meta/delete` — Удалить идентификаторы маркировки сборочных заданий
- `dbs.DefaultApi.post_v3_dbs_orders_meta_details` — `POST /api/marketplace/v3/dbs/orders/meta/details` — Получить идентификаторы маркировки сборочных заданий
- `dbs.DefaultApi.post_v3_dbs_orders_meta_gtin` — `POST /api/marketplace/v3/dbs/orders/meta/gtin` — Закрепить GTIN за сборочными заданиями
- `dbs.DefaultApi.post_v3_dbs_orders_meta_imei` — `POST /api/marketplace/v3/dbs/orders/meta/imei` — Закрепить IMEI за сборочными заданиями
- `dbs.DefaultApi.post_v3_dbs_orders_meta_sgtin` — `POST /api/marketplace/v3/dbs/orders/meta/sgtin` — Закрепить коды маркировки Честного знака за сборочными заданиями
- `dbs.DefaultApi.post_v3_dbs_orders_meta_uin` — `POST /api/marketplace/v3/dbs/orders/meta/uin` — Закрепить УИН за сборочными заданиями
- `dbs.DefaultApi.post_v3_dbs_orders_status_cancel` — `POST /api/marketplace/v3/dbs/orders/status/cancel` — Отменить сборочные задания
- `dbs.DefaultApi.post_v3_dbs_orders_status_confirm` — `POST /api/marketplace/v3/dbs/orders/status/confirm` — Перевести сборочные задания на сборку
- `dbs.DefaultApi.post_v3_dbs_orders_status_deliver` — `POST /api/marketplace/v3/dbs/orders/status/deliver` — Перевести сборочные задания в доставку
- `dbs.DefaultApi.post_v3_dbs_orders_status_info` — `POST /api/marketplace/v3/dbs/orders/status/info` — Получить статусы сборочных заданий
- `dbs.DefaultApi.post_v3_dbs_orders_status_receive` — `POST /api/marketplace/v3/dbs/orders/status/receive` — Сообщить о получении заказов
- `dbs.DefaultApi.post_v3_dbs_orders_status_reject` — `POST /api/marketplace/v3/dbs/orders/status/reject` — Сообщить об отказе от заказов
- `dbs.DefaultApi.post_v3_dbs_orders_stickers` — `POST /api/marketplace/v3/dbs/orders/stickers` — Получить стикеры для сборочных заданий с доставкой в ПВЗ

### in_store_pickup (`in_store_pickup`)
- `in_store_pickup.DefaultApi.get_v3_click_collect_orders` — `GET /api/v3/click-collect/orders` — Получить информацию о завершённых сборочных заданиях
- `in_store_pickup.DefaultApi.get_v3_click_collect_orders_new` — `GET /api/v3/click-collect/orders/new` — Получить список новых сборочных заданий
- `in_store_pickup.DefaultApi.post_v3_click_collect_orders_client` — `POST /api/v3/click-collect/orders/client` — Информация о покупателе
- `in_store_pickup.DefaultApi.post_v3_click_collect_orders_client_identity` — `POST /api/v3/click-collect/orders/client/identity` — Проверить, что заказ принадлежит покупателю
- `in_store_pickup.DefaultApi.post_v3_click_collect_orders_final_price` — `POST /api/marketplace/v3/click-collect/orders/final-price` — Получить цены продавца и суммы к оплате
- `in_store_pickup.DefaultApi.post_v3_click_collect_orders_meta_customs_declaration` — `POST /api/marketplace/v3/click-collect/orders/meta/customs-declaration` — Закрепить номера ДТ за сборочными заданиями
- `in_store_pickup.DefaultApi.post_v3_click_collect_orders_meta_delete` — `POST /api/marketplace/v3/click-collect/orders/meta/delete` — Удалить идентификаторы маркировки сборочных заданий
- `in_store_pickup.DefaultApi.post_v3_click_collect_orders_meta_details` — `POST /api/marketplace/v3/click-collect/orders/meta/details` — Получить идентификаторы маркировки сборочных заданий
- `in_store_pickup.DefaultApi.post_v3_click_collect_orders_meta_gtin` — `POST /api/marketplace/v3/click-collect/orders/meta/gtin` — Закрепить GTIN за сборочными заданиями
- `in_store_pickup.DefaultApi.post_v3_click_collect_orders_meta_imei` — `POST /api/marketplace/v3/click-collect/orders/meta/imei` — Закрепить IMEI за сборочными заданиями
- `in_store_pickup.DefaultApi.post_v3_click_collect_orders_meta_sgtin` — `POST /api/marketplace/v3/click-collect/orders/meta/sgtin` — Закрепить коды маркировки Честного знака за сборочными заданиями
- `in_store_pickup.DefaultApi.post_v3_click_collect_orders_meta_uin` — `POST /api/marketplace/v3/click-collect/orders/meta/uin` — Закрепить УИН за сборочными заданиями
- `in_store_pickup.DefaultApi.post_v3_click_collect_orders_status_cancel` — `POST /api/marketplace/v3/click-collect/orders/status/cancel` — Отменить сборочные задания
- `in_store_pickup.DefaultApi.post_v3_click_collect_orders_status_confirm` — `POST /api/marketplace/v3/click-collect/orders/status/confirm` — Перевести сборочные задания на сборку
- `in_store_pickup.DefaultApi.post_v3_click_collect_orders_status_info` — `POST /api/marketplace/v3/click-collect/orders/status/info` — Получить статусы сборочных заданий
- `in_store_pickup.DefaultApi.post_v3_click_collect_orders_status_prepare` — `POST /api/marketplace/v3/click-collect/orders/status/prepare` — Сообщить, что сборочные задания готовы к выдаче
- `in_store_pickup.DefaultApi.post_v3_click_collect_orders_status_receive` — `POST /api/marketplace/v3/click-collect/orders/status/receive` — Сообщить, что заказы приняты покупателями
- `in_store_pickup.DefaultApi.post_v3_click_collect_orders_status_reject` — `POST /api/marketplace/v3/click-collect/orders/status/reject` — Сообщить об отказе от заказов

### orders_fbw (`orders_fbw`)
- `orders_fbw.DefaultApi.get_v1_supplies_id` — `GET /api/v1/supplies/{ID}` — Детали поставки
- `orders_fbw.DefaultApi.get_v1_supplies_id_goods` — `GET /api/v1/supplies/{ID}/goods` — Товары поставки
- `orders_fbw.DefaultApi.get_v1_supplies_id_package` — `GET /api/v1/supplies/{ID}/package` — Упаковка поставки
- `orders_fbw.DefaultApi.get_v1_transit_tariffs` — `GET /api/v1/transit-tariffs` — Транзитные направления
- `orders_fbw.DefaultApi.get_v1_warehouses` — `GET /api/v1/warehouses` — Список складов
- `orders_fbw.DefaultApi.post_v1_acceptance_options` — `POST /api/v1/acceptance/options` — Опции приёмки
- `orders_fbw.DefaultApi.post_v1_supplies` — `POST /api/v1/supplies` — Список поставок

### promotion (`promotion`)
- `promotion.DefaultApi.delete_v0_normquery_bids` — `DELETE /adv/v0/normquery/bids` — Удалить ставки поисковых кластеров
- `promotion.DefaultApi.get_v0_bids_recommendations` — `GET /api/advert/v0/bids/recommendations` — Рекомендуемые ставки для карточек товаров и поисковых кластеров
- `promotion.DefaultApi.get_v0_delete` — `GET /adv/v0/delete` — Удаление кампании
- `promotion.DefaultApi.get_v0_pause` — `GET /adv/v0/pause` — Пауза кампании
- `promotion.DefaultApi.get_v0_start` — `GET /adv/v0/start` — Запуск кампании
- `promotion.DefaultApi.get_v0_stop` — `GET /adv/v0/stop` — Завершение кампании
- `promotion.DefaultApi.get_v1_advert` — `GET /adv/v1/advert` — Информация о медиакампании
- `promotion.DefaultApi.get_v1_adverts` — `GET /adv/v1/adverts` — Список медиакампаний
- `promotion.DefaultApi.get_v1_balance` — `GET /adv/v1/balance` — Баланс
- `promotion.DefaultApi.get_v1_budget` — `GET /adv/v1/budget` — Бюджет кампании
- `promotion.DefaultApi.get_v1_calendar_promotions` — `GET /api/v1/calendar/promotions` — Список акций
- `promotion.DefaultApi.get_v1_calendar_promotions_details` — `GET /api/v1/calendar/promotions/details` — Детальная информация об акциях
- `promotion.DefaultApi.get_v1_calendar_promotions_nomenclatures` — `GET /api/v1/calendar/promotions/nomenclatures` — Список товаров для участия в акции
- `promotion.DefaultApi.get_v1_config` — `GET /api/advert/v1/config` — Конфигурационные значения продвижения
- `promotion.DefaultApi.get_v1_count` — `GET /adv/v1/count` — Количество медиакампаний
- `promotion.DefaultApi.get_v1_payments` — `GET /adv/v1/payments` — Получение истории пополнений счёта
- `promotion.DefaultApi.get_v1_promotion_count` — `GET /adv/v1/promotion/count` — Списки кампаний
- `promotion.DefaultApi.get_v1_supplier_subjects` — `GET /adv/v1/supplier/subjects` — Предметы для кампаний
- `promotion.DefaultApi.get_v1_upd` — `GET /adv/v1/upd` — Получение истории затрат
- `promotion.DefaultApi.get_v2_adverts` — `GET /api/advert/v2/adverts` — Информация о кампаниях
- `promotion.DefaultApi.get_v3_fullstats` — `GET /adv/v3/fullstats` — Статистика кампаний
- `promotion.DefaultApi.patch_v0_auction_nms` — `PATCH /adv/v0/auction/nms` — Изменение списка карточек товаров в кампаниях
- `promotion.DefaultApi.patch_v1_bids` — `PATCH /api/advert/v1/bids` — Изменение ставок в кампаниях
- `promotion.DefaultApi.post_v0_normquery_bids` — `POST /adv/v0/normquery/bids` — Установить ставки для поисковых кластеров
- `promotion.DefaultApi.post_v0_normquery_get_bids` — `POST /adv/v0/normquery/get-bids` — Список ставок поисковых кластеров
- `promotion.DefaultApi.post_v0_normquery_get_minus` — `POST /adv/v0/normquery/get-minus` — Список минус-фраз кампаний
- `promotion.DefaultApi.post_v0_normquery_list` — `POST /adv/v0/normquery/list` — Списки активных и неактивных поисковых кластеров
- `promotion.DefaultApi.post_v0_normquery_set_minus` — `POST /adv/v0/normquery/set-minus` — Установка и удаление минус-фраз
- `promotion.DefaultApi.post_v0_normquery_stats` — `POST /adv/v0/normquery/stats` — Статистика поисковых кластеров
- `promotion.DefaultApi.post_v0_rename` — `POST /adv/v0/rename` — Переименование кампании
- `promotion.DefaultApi.post_v1_bids_min` — `POST /api/advert/v1/bids/min` — Минимальные ставки для карточек товаров
- `promotion.DefaultApi.post_v1_budget_deposit` — `POST /adv/v1/budget/deposit` — Пополнение бюджета кампании
- `promotion.DefaultApi.post_v1_calendar_promotions_upload` — `POST /api/v1/calendar/promotions/upload` — Добавить товар в акцию
- `promotion.DefaultApi.post_v1_normquery_bids` — `POST /api/advert/v1/normquery/bids` — Установить ставки для поисковых кластеров в валюте аккаунта продавца
- `promotion.DefaultApi.post_v1_normquery_stats` — `POST /adv/v1/normquery/stats` — Статистика по поисковым кластерам с детализацией по дням
- `promotion.DefaultApi.post_v1_stats` — `POST /adv/v1/stats` — Статистика медиакампаний
- `promotion.DefaultApi.post_v2_seacat_save_ad` — `POST /adv/v2/seacat/save-ad` — Создать кампанию
- `promotion.DefaultApi.post_v2_supplier_nms` — `POST /adv/v2/supplier/nms` — Карточки товаров для кампаний
- `promotion.DefaultApi.put_v0_auction_placements` — `PUT /adv/v0/auction/placements` — Изменение мест размещения в кампаниях с ручной ставкой

### communications (`communications`)
- `communications.DefaultApi.delete_feedbacks_v1_pins` — `DELETE /api/feedbacks/v1/pins` — Открепить отзывы
- `communications.DefaultApi.get_feedbacks_v1_pins` — `GET /api/feedbacks/v1/pins` — Список закреплённых и откреплённых отзывов
- `communications.DefaultApi.get_feedbacks_v1_pins_count` — `GET /api/feedbacks/v1/pins/count` — Количество закреплённых и откреплённых отзывов
- `communications.DefaultApi.get_feedbacks_v1_pins_limits` — `GET /api/feedbacks/v1/pins/limits` — Лимиты закреплённых отзывов
- `communications.DefaultApi.get_v1_claims` — `GET /api/v1/claims` — Заявки покупателей на возврат
- `communications.DefaultApi.get_v1_feedback` — `GET /api/v1/feedback` — Получить отзыв по ID
- `communications.DefaultApi.get_v1_feedbacks` — `GET /api/v1/feedbacks` — Список отзывов
- `communications.DefaultApi.get_v1_feedbacks_archive` — `GET /api/v1/feedbacks/archive` — Список архивных отзывов
- `communications.DefaultApi.get_v1_feedbacks_count` — `GET /api/v1/feedbacks/count` — Количество отзывов
- `communications.DefaultApi.get_v1_feedbacks_count_unanswered` — `GET /api/v1/feedbacks/count-unanswered` — Необработанные отзывы
- `communications.DefaultApi.get_v1_new_feedbacks_questions` — `GET /api/v1/new-feedbacks-questions` — Непросмотренные отзывы и вопросы
- `communications.DefaultApi.get_v1_question` — `GET /api/v1/question` — Получить вопрос по ID
- `communications.DefaultApi.get_v1_questions` — `GET /api/v1/questions` — Список вопросов
- `communications.DefaultApi.get_v1_questions_count` — `GET /api/v1/questions/count` — Количество вопросов
- `communications.DefaultApi.get_v1_questions_count_unanswered` — `GET /api/v1/questions/count-unanswered` — Неотвеченные вопросы
- `communications.DefaultApi.get_v1_seller_chats` — `GET /api/v1/seller/chats` — Список чатов
- `communications.DefaultApi.get_v1_seller_download_id` — `GET /api/v1/seller/download/{id}` — Получить файл из сообщения
- `communications.DefaultApi.get_v1_seller_events` — `GET /api/v1/seller/events` — События чатов
- `communications.DefaultApi.patch_v1_claim` — `PATCH /api/v1/claim` — Ответ на заявку покупателя
- `communications.DefaultApi.patch_v1_feedbacks_answer` — `PATCH /api/v1/feedbacks/answer` — Отредактировать ответ на отзыв
- `communications.DefaultApi.patch_v1_questions` — `PATCH /api/v1/questions` — Работа с вопросами
- `communications.DefaultApi.post_feedbacks_v1_pins` — `POST /api/feedbacks/v1/pins` — Закрепить отзывы
- `communications.DefaultApi.post_v1_feedbacks_answer` — `POST /api/v1/feedbacks/answer` — Ответить на отзыв
- `communications.DefaultApi.post_v1_feedbacks_order_return` — `POST /api/v1/feedbacks/order/return` — Возврат товара по ID отзыва
- `communications.DefaultApi.post_v1_seller_message` — `POST /api/v1/seller/message` — Отправить сообщение

### rates (`rates`)
- `rates.DefaultApi.get_v1_acceptance_coefficients` — `GET /api/tariffs/v1/acceptance/coefficients` — Тарифы на поставку
- `rates.DefaultApi.get_v1_tariffs_box` — `GET /api/v1/tariffs/box` — Тарифы для коробов
- `rates.DefaultApi.get_v1_tariffs_commission` — `GET /api/v1/tariffs/commission` — Комиссия по категориям товаров
- `rates.DefaultApi.get_v1_tariffs_pallet` — `GET /api/v1/tariffs/pallet` — Тарифы для монопаллет
- `rates.DefaultApi.get_v1_tariffs_return` — `GET /api/v1/tariffs/return` — Тарифы на возврат

### analytics (`analytics`)
- `analytics.DefaultApi.get_v2_nm_report_downloads` — `GET /api/v2/nm-report/downloads` — Получить список отчётов
- `analytics.DefaultApi.get_v2_nm_report_downloads_file_download_id` — `GET /api/v2/nm-report/downloads/file/{downloadId}` — Получить отчёт
- `analytics.DefaultApi.post_v1_order_feed` — `POST /api/analytics/v1/order-feed` — Получить отчёт
- `analytics.DefaultApi.post_v1_stocks_report_wb_warehouses` — `POST /api/analytics/v1/stocks-report/wb-warehouses` — Остатки на складах WB
- `analytics.DefaultApi.post_v2_item_rating` — `POST /api/analytics/v2/item-rating` — Получить отчёт
- `analytics.DefaultApi.post_v2_nm_report_downloads` — `POST /api/v2/nm-report/downloads` — Создать отчёт
- `analytics.DefaultApi.post_v2_nm_report_downloads_retry` — `POST /api/v2/nm-report/downloads/retry` — Сгенерировать отчёт повторно
- `analytics.DefaultApi.post_v2_search_report_product_orders` — `POST /api/v2/search-report/product/orders` — Заказы и позиции по поисковым запросам товара
- `analytics.DefaultApi.post_v2_search_report_product_search_texts` — `POST /api/v2/search-report/product/search-texts` — Поисковые запросы по товару
- `analytics.DefaultApi.post_v2_search_report_report` — `POST /api/v2/search-report/report` — Основная страница
- `analytics.DefaultApi.post_v2_search_report_table_details` — `POST /api/v2/search-report/table/details` — Пагинация по товарам в группе
- `analytics.DefaultApi.post_v2_search_report_table_groups` — `POST /api/v2/search-report/table/groups` — Пагинация по группам
- `analytics.DefaultApi.post_v2_stocks_report_offices` — `POST /api/v2/stocks-report/offices` — Данные по складам
- `analytics.DefaultApi.post_v2_stocks_report_products_groups` — `POST /api/v2/stocks-report/products/groups` — Данные по группам
- `analytics.DefaultApi.post_v2_stocks_report_products_products` — `POST /api/v2/stocks-report/products/products` — Данные по товарам
- `analytics.DefaultApi.post_v2_stocks_report_products_sizes` — `POST /api/v2/stocks-report/products/sizes` — Данные по размерам
- `analytics.DefaultApi.post_v3_sales_funnel_grouped_history` — `POST /api/analytics/v3/sales-funnel/grouped/history` — Статистика групп карточек товаров по дням
- `analytics.DefaultApi.post_v3_sales_funnel_products` — `POST /api/analytics/v3/sales-funnel/products` — Статистика карточек товаров за период
- `analytics.DefaultApi.post_v3_sales_funnel_products_history` — `POST /api/analytics/v3/sales-funnel/products/history` — Статистика карточек товаров по дням

### reports (`reports`)
- `reports.DefaultApi.get_v1_acceptance_report` — `GET /api/v1/acceptance_report` — Создать отчёт
- `reports.DefaultApi.get_v1_acceptance_report_tasks_task_id_download` — `GET /api/v1/acceptance_report/tasks/{task_id}/download` — Получить отчёт
- `reports.DefaultApi.get_v1_acceptance_report_tasks_task_id_status` — `GET /api/v1/acceptance_report/tasks/{task_id}/status` — Проверить статус
- `reports.DefaultApi.get_v1_analytics_antifraud_details` — `GET /api/v1/analytics/antifraud-details` — Самовыкупы
- `reports.DefaultApi.get_v1_analytics_banned_producs_blocked` — `GET /api/v1/analytics/banned-products/blocked` — Получить отчёт
- `reports.DefaultApi.get_v1_analytics_brand_share` — `GET /api/v1/analytics/brand-share` — Получить отчёт
- `reports.DefaultApi.get_v1_analytics_brand_share_brands` — `GET /api/v1/analytics/brand-share/brands` — Бренды продавца
- `reports.DefaultApi.get_v1_analytics_brand_share_parent_subjects` — `GET /api/v1/analytics/brand-share/parent-subjects` — Родительские категории бренда
- `reports.DefaultApi.get_v1_analytics_goods_labeling` — `GET /api/v1/analytics/goods-labeling` — Маркировка товара
- `reports.DefaultApi.get_v1_analytics_goods_return` — `GET /api/v1/analytics/goods-return` — Получить отчёт
- `reports.DefaultApi.get_v1_analytics_region_sale` — `GET /api/v1/analytics/region-sale` — Получить отчёт
- `reports.DefaultApi.get_v1_deductions` — `GET /api/analytics/v1/deductions` — Подмены и неверные вложения
- `reports.DefaultApi.get_v1_measurement_penalties` — `GET /api/analytics/v1/measurement-penalties` — Удержания за занижение габаритов упаковки
- `reports.DefaultApi.get_v1_paid_storage` — `GET /api/v1/paid_storage` — Создать отчёт
- `reports.DefaultApi.get_v1_paid_storage_tasks_task_id_download` — `GET /api/v1/paid_storage/tasks/{task_id}/download` — Получить отчёт
- `reports.DefaultApi.get_v1_paid_storage_tasks_task_id_status` — `GET /api/v1/paid_storage/tasks/{task_id}/status` — Проверить статус
- `reports.DefaultApi.get_v1_supplier_orders` — `GET /api/v1/supplier/orders` — Заказы
- `reports.DefaultApi.get_v1_supplier_sales` — `GET /api/v1/supplier/sales` — Продажи
- `reports.DefaultApi.get_v1_warehouse_measurements` — `GET /api/analytics/v1/warehouse-measurements` — Замеры склада
- `reports.DefaultApi.get_v1_warehouse_remains` — `GET /api/v1/warehouse_remains` — Создать отчёт
- `reports.DefaultApi.get_v1_warehouse_remains_tasks_task_id_download` — `GET /api/v1/warehouse_remains/tasks/{task_id}/download` — Получить отчёт
- `reports.DefaultApi.get_v1_warehouse_remains_tasks_task_id_status` — `GET /api/v1/warehouse_remains/tasks/{task_id}/status` — Проверить статус
- `reports.DefaultApi.post_v1_analytics_excise_report` — `POST /api/v1/analytics/excise-report` — Получить отчёт

### finances (`finances`)
- `finances.DefaultApi.get_v1_account_balance` — `GET /api/v1/account/balance` — Получить баланс продавца
- `finances.DefaultApi.get_v1_documents_categories` — `GET /api/v1/documents/categories` — Категории документов
- `finances.DefaultApi.get_v1_documents_download` — `GET /api/v1/documents/download` — Получить документ
- `finances.DefaultApi.get_v1_documents_list` — `GET /api/v1/documents/list` — Список документов
- `finances.DefaultApi.post_v1_acquiring_detailed` — `POST /api/finance/v1/acquiring/detailed` — Детализации к отчётам об издержках на приём платежей за период
- `finances.DefaultApi.post_v1_acquiring_detailed_report_id` — `POST /api/finance/v1/acquiring/detailed/{reportId}` — Детализации к отчётам об издержках на приём платежей по ID отчётов
- `finances.DefaultApi.post_v1_acquiring_list` — `POST /api/finance/v1/acquiring/list` — Список отчётов об издержках на приём платежей
- `finances.DefaultApi.post_v1_documents_download_all` — `POST /api/v1/documents/download/all` — Получить документы
- `finances.DefaultApi.post_v1_sales_reports_detailed` — `POST /api/finance/v1/sales-reports/detailed` — Детализации к отчётам реализации за период
- `finances.DefaultApi.post_v1_sales_reports_detailed_report_id` — `POST /api/finance/v1/sales-reports/detailed/{reportId}` — Детализации к отчётам реализации по ID отчётов
- `finances.DefaultApi.post_v1_sales_reports_list` — `POST /api/finance/v1/sales-reports/list` — Список отчётов реализации
<!-- PY_METHODS_LIST_END -->
