# Changelog

## Unreleased
### Changed (2026.07.17)
- Promotion (Реклама): в ответе/схеме конфигурации кампаний добавлено обязательное поле `minTopUp` — минимальная сумма пополнения бюджета в minor units (0,01 от базовой валюты аккаунта продавца); обновлены описания ставок/шагов ставок с формулировкой «0,01 от базовой валюты» (ранее «от базовой единицы валюты»).
- Analytics (Оценка товара): добавлен новый endpoint `POST /api/analytics/v2/item-rating` (operationId `postV2ItemRating`) с расширенными ответами ошибок (`403`, `429`).
- Analytics (Оценка товара): `POST /api/analytics/v1/item-rating` помечен как `deprecated` и будет удалён 30 июля; сохранён как read-only.
- Analytics (Оценка товара): введены версии схем для v1 (`ItemRatingRequestV1`, `ItemRatingResponseV1`, `DistributionTableItemV1`), исправлено имя схемы периода `PastPeriodItemRating` (ранее `pastPeriodItemRating`).
- Analytics (Оценка товара): обновлён контракт v2 — новый `ItemRatingRequest` (обязательные `currentPeriod`, `orderBy`, `offset`; добавлены фильтры `subjectIds`, `brandNames`, `tagIds`, флаги `isNotIncludeNmsWithoutSales`, `onlyShadowedNms`, пагинация `limit` до 1000) и новый `ItemRatingResponse` (поле `items` вместо `cards`); `DistributionTableItem` расширен и теперь включает обязательные поля (в т.ч. `tagName`, `tagId`, `pinnedFeedback`, `isShadowed`) и детализированные метрики по отзывам/звёздам.
- Reports (Контент-аналитика): раздел/тег переименован с «Скрытые товары» на «Заблокированные карточки»; для отчёта по заблокированным карточкам обновлён `summary` на «Получить отчёт».
- Reports (Контент-аналитика): endpoint получения «Скрытые из каталога» помечен как `deprecated` и будет удалён 30 июля (описание заменено на уведомление об устаревании).

### Changed (2026.07.16)
- Товары (Items): обновлены ссылки в описаниях/параметрах/ошибках (knowledge-base, release-notes) с абсолютных `https://dev.wildberries.ru/...` на относительные пути (`/knowledge-base/...`, `/release-notes?...`); функциональных изменений эндпоинтов/полей/лимитов нет
- Заказы FBS: обновлены ссылки в описаниях (инструкция, проверка `isCancellable`, статусы маркировки) на относительные; контракт API без изменений
- Заказы DBW: уточнены ссылки в описании deprecated-метода получения идентификаторов маркировки (ссылка на release notes стала относительной); статус устаревания/дата удаления не изменены
- Заказы DBS: обновлены ссылки на раздел лимитов и release notes в описаниях (в т.ч. для deprecated-метода получения идентификаторов маркировки) на относительные; функциональных изменений нет
- Самовывоз (In-store pickup): обновлена ссылка в описании deprecated-метода получения идентификаторов маркировки (release notes → относительная); остальное без изменений
- Заказы FBW: обновлены ссылки в описаниях ошибок (business-solutions → относительная); без изменений API
- Продвижение (Promotion): обновлены ссылки в описаниях ошибок (business-solutions → относительная); без изменений API
- Общение с покупателями (Communications): обновлены ссылки в описаниях (в т.ч. про `imtId` и закрепление отзывов) на относительные; без изменений API
- Тарифы (Rates): обновлены ссылки в описаниях ошибок (business-solutions → относительная); без изменений API
- Аналитика (Analytics): обновлены ссылки в описаниях ошибок (business-solutions → относительная); без изменений API
- Отчёты (Reports): обновлена ссылка на инструкцию по сохранению отчёта в таблицы (на knowledge-base, относительная); без изменений API
- Финансы (Finances): удалён устаревший эндпоинт `GET /api/v5/supplier/reportDetailByPeriod` (Отчёт о продажах по реализации) вместе со схемой ответа `DetailReportItem` и связанными параметрами/описанием лимитов; обновлены ссылки в описаниях (Google Таблицы, business-solutions) на относительные
- Общее (General): обновлены ссылки в описаниях ошибок (business-solutions → относительная); без изменений структуры ошибок/полей

### Changed (2026.07.14)
- Promotion/Реклама: в ответах кампаний добавлено новое обязательное поле `restrictions` (объект «Ограничения кампании») с флагом `can_change_nms: boolean`, определяющим, можно ли изменять список товаров (НМ) в кампании.
- Promotion/Календарь промо: из описания `servers` для эндпоинтов `GET /api/v1/calendar/promotions`, `GET /api/v1/calendar/promotions/details`, `GET /api/v1/calendar/promotions/nomenclatures`, `POST /api/v1/calendar/promotions/upload` удалён sandbox-сервер `https://dp-calendar-api-sandbox.wildberries.ru` (остаётся только `https://dp-calendar-api.wildberries.ru`).

### Changed (2026.07.11)
- Promotion: изменён тип query-параметра `status` с `integer` на `string` (пример теперь `1,3,7`, что указывает на передачу списка статусов строкой).
- Promotion: в схеме `stats` удалено ограничение `maxItems: 100` (массив `stats` больше не ограничен 100 элементами на уровне спецификации).

### Changed (2026.07.10)
- Общие (API Information): добавлены `operationId` для методов `/ping` (`getPing`), `/api/communications/v2/news` (`getV2News`), `/api/v1/seller-info` (`getV1SellerInfo`), `/api/v1/rating` (`getV1Rating`, ранее `getCommonV1Rating`), `/api/v1/subscriptions` (`getV1Subscriptions`, ранее `getCommonV1Subscriptions`), `/api/v1/tariff-constructor/options` (`getV1TariffConstructorOptions`, ранее `getCommonV1TariffConstructorOptions`); добавлены `x-displayName` для тегов; обновлены ссылки на разделы `introduction/authorization/...` (без изменения контрактов/лимитов)
- Управление пользователями продавца: добавлены `operationId` для `/api/v1/invite` (`postV1Invite`), `/api/v1/users` (`getV1Users`), `/api/v1/users/access` (`putV1UsersAccess`), `/api/v1/user` (`deleteV1User`); обновлены внутренние ссылки на новые теги/operationId
- Товары / Контент: в описаниях лимитов убраны упоминания методов `POST /content/v2/cards/error/list` и `POST /content/v2/cards/delete/trash` из списка «исключений» для лимитов категории «Контент» (документационное изменение)
- Товары / Характеристики: лимиты переразмечены по типам токенов — для персонального/сервисного/базового с секретом: `100/мин` (интервал `600 мс`, всплеск `5`), для базового: `2/час` (интервал `30 мин`, всплеск `1`) вместо единого лимита `100/мин`
- Товары / Ярлыки: лимиты переразмечены по типам токенов аналогично (персональный/сервисный/базовый с секретом `100/мин`, базовый `2/час`) вместо единого лимита `100/мин`
- Товары / Медиафайлы: лимиты переразмечены по типам токенов (персональный/сервисный/базовый с секретом `100/мин`, базовый `2/час`) и выделены как лимиты методов «Медиафайлов» (ранее относились к общим лимитам «Контента» с перечнем исключений)
- Товары / Карточки: для метода переноса карточек в корзину (`POST /content/v2/cards/delete/trash`) изменён лимит с `3 запроса/мин` (интервал `20 сек`) на раздельные лимиты по типам токенов: персональный/сервисный/базовый с секретом `100/мин` (600 мс, всплеск 5), базовый `2/час` (30 мин, всплеск 1)
- Товары / Карточки: для методов «лимиты карточек» (`GET /content/v2/cards/limits`) и «несозданные карточки с ошибками» (`POST /content/v2/cards/error/list`) явно выделен отдельный лимит `10 запросов/мин` (интервал `6 сек`, всплеск `5`)
- Заказы DBS: поля `dDateFrom` и `dDateTo` в модели сборочного задания помечены как «Не используется» (примеры очищены)
- Поставки FBW: добавлены `operationId` для методов `/api/v1/acceptance/options` (`postV1AcceptanceOptions`), `/api/v1/warehouses` (`getV1Warehouses`), `/api/v1/transit/tariffs` (`getV1TransitTariffs`), `/api/v1/supplies` (`postV1Supplies`), `/api/v1/supplies/{id}` (`getV1SuppliesId`), `/api/v1/supplies/{id}/goods` (`getV1SuppliesIdGoods`), `/api/v1/supplies/{id}/package` (`getV1SuppliesIdPackage`); добавлены `x-displayName` для тегов; обновлены ссылки на новые теги/operationId
- Тарифы WB: добавлены `operationId` для `/api/v1/tariffs/commission` (`getV1TariffsCommission`), `/api/v1/acceptance/coefficients` (`getV1AcceptanceCoefficients`), `/api/v1/tariffs/box` (`getV1TariffsBox`), `/api/v1/tariffs/pallet` (`getV1TariffsPallet`), `/api/v1/tariffs/return` (`getV1TariffsReturn`); добавлены `x-displayName` для тегов; обновлены ссылки на новые теги/operationId
- Аналитика: переименованы `operationId` методов воронки продаж — `postSalesFunnelProducts`→`postV3SalesFunnelProducts`, `postSalesFunnelProductsHistory`→`postV3SalesFunnelProductsHistory`, `postSalesFunnelGroupedHistory`→`postV3SalesFunnelGroupedHistory`
- Отчёты: переименованы `operationId` — `getMeasurementPenalties`→`getV1MeasurementPenalties`, `getWarehouseMeasurements`→`getV1WarehouseMeasurements`, `getDeductions`→`getV1Deductions`
- Финансы: добавлены `operationId` для баланса и документов — `/api/v1/account/balance` (`getV1AccountBalance`), `/api/v1/documents/categories` (`getV1DocumentsCategories`), `/api/v1/documents/list` (`getV1DocumentsList`), `/api/v1/documents/download` (`getV1DocumentsDownload`), `/api/v1/documents/download/all` (`postV1DocumentsDownloadAll`); метод `/api/v5/supplier/reportDetailByPeriod` помечен как `deprecated` и будет удалён 15 июля
- Продвижение: изменён контракт запроса для удаления ставок по поисковым кластерам — вместо `V0SetNormQueryBidsRequest` используется `V0DeleteNormQueryBidsRequest` (в элементах `bids[]` удалено поле `bid`, обязательны `advert_id`, `nm_id`, `norm_query`); добавлены схемы `V0DeleteNormQueryBidsRequest`/`Item`
- Продвижение: в схему ошибки добавлено поле `type` (тип ошибки)
- Заказы DBW/DBS/Самовывоз: отмечены устаревшие методы (deprecation notice) с датами удаления — DBW/DBS: удаление 27 июля, Самовывоз: удаление 15 июля (без изменения эндпоинтов в диффе)
- Сквозное: массово обновлены ссылки на разделы лимитов/авторизации (`Vvedenie/Avtorizaciya/...` → `introduction/authorization/...`) и на теги финансовых отчётов (`Finansovye-otchyoty` → `financialReports`) — изменения в документации/навигации без изменения API-контрактов и фактических лимитов (кроме явно перечисленных выше)

### Changed (2026.07.09)
- Общие (Common/Users): для ряда методов добавлен ответ `403 Forbidden` (`/api/common/v1/balance`, `/api/common/v1/subscriptions`, `/api/common/v1/tariff-constructor/options`, `/api/common/v1/tariff-constructor/plan`, `/api/v1/users`, `/api/v1/users/access`, `/api/v1/user`) и введён общий формат ошибки `application/problem+json` (schema `components.responses.403` с полями `title/detail/code/requestId/origin/status/statusText/timestamp`).
- Товары (Items): для `403` в одном из методов заменён формат ответа с `application/json` + пример `Result403V3` на `application/problem+json` со схемой `Response403General`; удалён пример `components/examples/Result403V3`; добавлена схема `components/schemas/Response403General`; уточнено описание параметра `objectIDs` (“ID” вместо “id”).
- Заказы DBS (Orders DBS): для `/api/marketplace/v3/dbs/orders/status/deliver` переработан ответ `403` — вместо `$ref` на `AccessDenied` теперь описаны два формата: `application/json` (schema `Error`, пример `code: AccessDenied`) и `application/problem+json` (schema `Response403General`); в модели заказа сокращено описание поля ГТД до “Номер ДТ”; добавлена схема `components/schemas/Response403General`.
- Продвижение (Promotion / Календарь акций): переименованы/перепривязаны компоненты и ссылки для раздела календаря акций (tag в ссылках `Kalendar-akcij` → `promoCalendar`); параметр запроса переименован `limitPromotion` → `limitPromo`; переименованы компоненты: `PromotionsSuccessResponse`→`PromoSuccessResponse`, `PromotionsGetByIDSuccessResponse`→`PromosGetByIDSuccessResponse`, `ResponsePromotionsItemsLists`→`ResponsePromoItemsLists`, `PromotionsItemsList`→`PromoItemsList`, `PromotionsSupplierTaskRequest`→`PromoSupplierTaskRequest`; расширен формат ошибки `FullStatsError` — добавлено поле `errors[]` (с `detail` и `field`), обновлены `required` (убран обязательный `detail`, порядок/набор обязательных полей скорректирован), добавлен пример `MaxDateRangeError` (ограничение диапазона дат 31 день).
- Аналитика (Analytics): для методов `/api/v2/stocks-report/products` и `/api/v2/stocks-report/products/groups` добавлен альтернативный ответ `403` в формате `application/problem+json` со схемой `Response403General`; добавлена схема `components/schemas/Response403General`.
- Финансы (Finances): для методов финансовых отчётов и эквайринга добавлен ответ `403 Forbidden` (`/api/finance/v1/sales-reports/detailed/{reportId}`, `/api/finance/v1/sales-reports/detailed`, `/api/finance/v1/acquiring/detailed/{reportId}`, `/api/finance/v1/acquiring/detailed`, а также метод(ы) финансовых отчётов в начале файла); добавлен общий `components.responses.403` в формате `application/problem+json` (единая структура с `code/requestId/origin/...`).

### Changed (2026.07.04)
- Orders DBS: исправлены ссылки в описании идентификаторов маркировки `customsDeclaration` и `originCountryCode` на корректные пути `/v3/dbs/orders/meta/customs-declaration` (ранее частично указывался `/v3/dbs/meta/...`).
- Orders DBS: исправлена ошибка в описании удаления идентификаторов — вместо дублирования `customsDeclaration` теперь указан `originCountryCode` (уточнение: при удалении номера ДТ также удаляется `originCountryCode`).

- Продвижение: добавлен GET `/api/advert/v1/config` — получение валюты/кода валюты аккаунта продавца и шагов ставок `cpcStep`/`cpmStep`; лимит 1 запрос/мин (burst 10).
- Продвижение: добавлен POST `/api/advert/v1/normquery/bids` — установка ставок для поисковых кластеров в валюте аккаунта продавца (minor units, 0.01 базовой единицы); лимит 2 запроса/сек (burst 4) для personal/service; новые схемы `V1SetNormQueryBidsRequest/Response`.
- Продвижение: метод минимальных ставок для карточек товаров — ставки теперь описаны как «в разменных единицах 0,01 от базовой единицы валюты аккаунта», в ответе для каждой ставки добавлено обязательное поле `currency` (ISO 4217).
- Продвижение: в ряде ответов добавлено поле `currency` (ISO 4217) и обновлены описания денежных полей на «в валюте аккаунта продавца»: финансы кампаний (balance/net/bonus/total), история пополнений, статистика/поисковые кластеры, статистика кампаний.
- Продвижение: для `/adv/v0/normquery/bids` уточнено, что метод устанавливает ставки **в рублях**; в ответе по ставкам добавлены обязательные поля `bid_kopecks` (ставка в minor units) и `currency`.
- Продвижение: в запросе пополнения бюджета убрана `nullable: true` у `cashback_sum` и `cashback_percent`; обновлены примеры ошибок 400 — заменены частные кейсы на общий `MinimumDepositAmountError` с сообщением `minimum deposit amount is 1000`.

### Changed (2026.07.03)
- Заказы DBS / Идентификаторы маркировки DBS: добавлен новый тип идентификатора `originCountryCode` (числовой код страны происхождения по ОКСМ) в `meta` и в перечисление ключей
- Заказы DBS / Идентификаторы маркировки DBS: исправлена ссылка для `customsDeclaration` (путь без `/orders/`: `/api/marketplace/v3/dbs/meta/customs-declaration`)
- Заказы DBS / Идентификаторы маркировки DBS: метод закрепления ДТ расширен — теперь обновляет **номер ДТ + originCountryCode**, разрешён для статусов сборочного задания `confirm` и `deliver` (ранее только `deliver`)
- Заказы DBS / Идентификаторы маркировки DBS: в запросе закрепления ДТ добавлено обязательное поле `originCountryCode` (maxLength: 3), требуется только для B2B-заказов (`"isB2b": true`); добавлены ошибки `OrderNotB2B`, `InvalidOriginCountryCode`, в схеме ошибок добавлен код `400`
- Заказы DBS / Идентификаторы маркировки DBS: изменён ответ метода закрепления ДТ — вместо `204` теперь `200` с телом `api.StatusSetResponses`; удалён пример ошибки `IncorrectParameter`
- Самовывоз (Click&Collect) / Идентификаторы маркировки: добавлен новый endpoint `POST /api/marketplace/v3/click-collect/orders/meta/customs-declaration` для закрепления **номера ДТ + originCountryCode** (batch до 1000), ответ `200` с `api.CustomsDeclarationSetResponse`
- Самовывоз (Click&Collect) / Идентификаторы маркировки: для нового метода закрепления ДТ введены ограничения — только B2B (`options.isB2b=true`) и статусы `confirm` или `prepare`; у одного задания только один ДТ
- Самовывоз (Click&Collect) / Идентификаторы маркировки: расширены правила удаления — добавлен тип `customsDeclaration`; при удалении `customsDeclaration` также удаляется `originCountryCode`
- Самовывоз (Click&Collect): в схемы заказов добавлено поле `options.isB2b` (признак B2B-продажи)
- Самовывоз (Click&Collect) / Идентификаторы маркировки: добавлены схемы/ошибки для batch-ответов по ДТ (`api.StatusSetCustomsDeclarationResponse`, `api.BatchCustomsDeclarationErrorResponse`) с деталями `OrderNotB2B`, `InvalidOriginCountryCode` и кодами `400/404/409/422`

### Changed (2026.07.02)
- Товары (Контент): добавлена информация о возможности тестирования методов в песочнице (/sandbox) и о наличии специальных sandbox-методов для управления карточками товаров
- Товары (Контент): уточнено поведение параметра `locale` — в песочнице не используется, данные песочницы возвращаются только на русском языке (обновлено в нескольких методах)
- Товары (Контент): обновлены ссылки/теги в описаниях лимитов и исключений (переезд ссылок на `listingItems`, `listings`, `recommendations` вместо старых `Sozdanie-kartochek-tovarov`, `Kartochki-tovarov`, `promotion/Rekomendacii`) — изменения документационные, без изменения путей API
- Товары (Контент): для `POST /content/v2/cards/upload` и `POST /content/v2/cards/upload/add` добавлено уточнение — в песочнице карточка создаётся сразу, без асинхронного ожидания
- Товары (Склады продавца): исправлены ссылки в описаниях методов контактов склада (убран ошибочный префикс `/openapi/openapi/...`)

- Заказы FBS: добавлена информация о тестировании методов в песочнице (/sandbox) и о специальных sandbox-методах для эмуляции действий пользователя
- Заказы FBS: для `POST /api/v3/orders/status/history` добавлены `servers` для Prod и Sandbox; в описании указано, что в песочнице метод всегда возвращает `200`
- Заказы FBS: для метода получения стикеров трансграничных поставок добавлено примечание — в песочнице всегда возвращается `200`
- Заказы FBS: массово исправлены ссылки в описаниях (убран `/openapi/openapi/...`, актуализированы относительные ссылки), без изменения контрактов/эндпоинтов

- Заказы DBW: исправлены ссылки в описаниях методов (убран `/openapi/openapi/...`), без изменения контрактов/эндпоинтов

- Заказы DBS: добавлена информация о тестировании методов в песочнице (/sandbox) и о специальных sandbox-методах для эмуляции действий пользователя
- Заказы DBS: исправлены ссылки на методы для `customsDeclaration` (номер ДТ) — корректный путь включает `/dbs/orders/meta/customs-declaration`
- Заказы DBS: в описании закрепления номера ДТ обновлена ссылка на метод статуса — вместо `/api/v3/dbs/orders/status/post` указано `/api/marketplace/v3/dbs/orders/status/info/post` (документационное уточнение)

- Самовывоз (In-store pickup): добавлена информация о тестировании методов в песочнице (/sandbox) и о специальных sandbox-методах для эмуляции действий пользователя

- Поставки FBW: добавлено примечание о сценарии песочницы — карточки создавать в песочнице Контента, затем использовать баркоды в песочнице Поставок

- Продвижение: добавлена информация о тестировании методов в песочнице (/sandbox) и о специальных sandbox-методах для управления тестовым балансом
- Продвижение: уточнены ограничения статистики в песочнице — доступна за последние 30 дней, генерируется только для кампаний в статусе `9`, тип `8`, 9 раз в сутки
- Продвижение (Календарь акций): для `/api/v1/calendar/promotions`, `/details`, `/nomenclatures`, `/upload` добавлены `servers` для Sandbox (`https://dp-calendar-api-sandbox.wildberries.ru`) помимо Prod

- Коммуникации (Вопросы/Отзывы/Чаты/Возвраты): добавлена информация о тестировании методов в песочнице (/sandbox) и о специальных sandbox-методах для управления тестовыми вопросами и отзывами

- Отчёты: для отчётов заказов и продаж/возвратов добавлено ограничение песочницы — диапазон `dateFrom`/`dateTo` можно задавать только за последние 4 месяца от текущей даты

### Changed (2026.07.01)
- Finances: в модели ответа добавлено новое обязательное поле `b2bCustomerTin` (string) — ИНН B2B‑покупателя (пример: `010101010101`)
- Finances: в схеме (snake_case) добавлено поле `b2b_customer_tin` (string) — ИНН B2B‑покупателя (пример: `010101010101`)

### Changed (2026.06.27)
- Тарифы на поставку: добавлен GET `/api/tariffs/v1/acceptance/coefficients` (common-api) — получение коэффициентов/тарифов приёмки по складам на ближайшие 14 дней; новый query-параметр `warehouseIDs` (CSV), добавлены ответы `403`/`404`, изменён формат ошибки `400` на `application/json` с моделью `models.ErrorModel`; лимиты снижены до 6 запросов/мин (интервал 10 сек, всплеск 6) для персонального/сервисного/базового с секретом; для метода явно задана `HeaderApiKey` security
- Тарифы на остаток: эндпоинты `/api/v1/tariffs/box` и `/api/v1/tariffs/pallet` сохранены, но обновлены описания/примеры ошибок `400` (для `/box` теперь `detail: Invalid date param`)
- Тарифы на остаток / Стоимость возврата продавцу: в моделях `models.WarehousesBoxRates`, `models.WarehousesPalletRates`, `models.WarehousesReturnRates` добавлено поле `currency` (string, валюта тарифов, пример `RUB`)

### Changed (2026.06.26)
- Управление пользователями продавца: в перечень кодов прав доступа (enum `code`) добавлены `brandzone` (Бренд‑зона. Публикация изменений) и `brandzoneSubscribe` (управление подпиской бренд‑зоны); обновлены примеры ответов со включением новых прав
- Товары (Контент) / Рекомендации: добавлен новый раздел «Рекомендации» и новые методы `POST /api/content/v1/recommendations/list` (получение списка рекомендаций в карточках) и `POST /api/content/v1/recommendations/set` (установка/обновление/удаление рекомендаций); токены: personal/service; лимит: 100 запросов/мин (интервал 600 мс, всплеск 5); добавлены схемы `GetRecomReq/GetRecomRes/SetRecomReq/SetRecomRes` и ответы ошибок `400`, `208`
- Продвижение: удалён раздел «Рекомендации» и эндпоинты `POST /api/content/v1/recommendations/list` и `POST /api/content/v1/recommendations/set` (перенесены в спецификацию «Товары/Контент»); удалены связанные схемы (`GetRecom*`, `SetRecom*`, `response400*`, `response208*`)
- Заказы DBS: для метода получения стикеров для сборочных заданий с доставкой в ПВЗ добавлен тип токена `base-with-secret` (базовый с секретом) в `x-token-types`
- Аналитика / История остатков: для `POST /api/v1/stocks/report/wbWarehouses` добавлен тип токена `base-with-secret` (базовый с секретом) в `x-token-types`
- Отчёты (Statistics): удалён устаревший метод `GET /api/v1/supplier/stocks` (ранее deprecated) и схема ответа `StocksItem` из components
- Финансы: изменений в контракте/лимитах нет (только переразметка описаний по типам токенов)

### Changed (2026.06.25)
- Информация о продавце: добавлен GET `/api/common/v1/tariff-constructor/options` (common-api.wildberries.ru) для получения подключённых опций и пакетов Конструктора тарифов; доступ по сервисному токену, query-параметр `locale` (`ru|en`, default `ru`)
- Информация о продавце: введён лимит для GET `/api/common/v1/tariff-constructor/options` — 1 запрос/мин на аккаунт (интервал 1 мин, всплеск до 10)
- Информация о продавце: добавлены схемы ответа/ошибок для нового метода — `PlanBuilderOptionsInfo` (поля `activeOptionCount`, `activePackageCount`, `totalCommissionRate`, массивы `packages`/`options`), `PlanBuilderPackage`, `PlanBuilderOption`, `PlanBuilderOptionShort`, `PlanBuilderPromotion`, `PlanBuilderErrors`; добавлены примеры ответов 200/400/404 (в т.ч. коды `INVALID_LOCALE`, `OPTIONS_NOT_AVAILABLE`)

### Changed (2026.06.24)
- Товары/Остатки: для ответа `406 Not Acceptable` при обновлении остатков заменён `$ref` на `#/components/responses/StatusNotAcceptable` на инлайн-описание с `schema: #/components/schemas/UpdateBlocked` и примерами `StatusNotAcceptable` + новый `WarehouseStocksUpdateBlock`.
- Товары/Остатки: добавлена схема ошибки `UpdateBlocked` (поля `code`, `message`, `data`) для случаев блокировки обновления остатков.
- Товары/Остатки: удалён компонент `components.responses.StatusNotAcceptable` (его структура перенесена в `components.schemas.UpdateBlocked` + `components.examples`).
- Товары/Остатки: добавлен пример ошибки `WarehouseStocksUpdateBlock` (работы на складе; обновление остатков временно невозможно, повторить позже); пример `StatusNotAcceptable` перенесён/оформлен как `components.examples.StatusNotAcceptable`.

### Changed (2026.06.23)
- Общие/Права доступа: удалены коды прав `wbPoint` (WB Point) и `feedbacksQuestions` (вопросы+отзывы/жалобы на отзывы) из перечня доступных разрешений и обязательных значений (enum) в компонентах спецификации.

### Changed (2026.06.20)
- Communications: удалено поле `date` из объекта `attachments.goodCard` (в т.ч. из схемы «Информация о заказе»); поле было помечено как `deprecated` и планировалось к отключению 16 июня.

### Changed (2026.06.19)
- Товары (Content API): для всех методов раздела добавлен Sandbox-сервер `https://content-api-sandbox.wildberries.ru` (помимо Prod `https://content-api.wildberries.ru`) в `servers` у эндпоинтов `/content/v2/*` и `/content/v3/media/*`.
- Цены и скидки (Discounts & Prices API): для всех методов раздела добавлен Sandbox-сервер `https://discounts-prices-api-sandbox.wildberries.ru` (помимо Prod `https://discounts-prices-api.wildberries.ru`) в `servers` у эндпоинтов `/api/v2/*`.
- Marketplace (остатки/склады/офисы): добавлен Sandbox-сервер `https://marketplace-api-sandbox.wildberries.ru` (помимо Prod) в `servers` для `/api/v3/stocks/{warehouseId}`, `/api/v3/offices`, `/api/v3/warehouses`, `/api/v3/warehouses/{warehouseId}`.
- Заказы FBS (Marketplace): добавлен Sandbox-сервер `https://marketplace-api-sandbox.wildberries.ru` (помимо Prod) в `servers` для всех эндпоинтов раздела (`/api/v3/passes*`, `/api/v3/orders*`, `/api/v3/supplies*`, `/api/marketplace/v3/*`).
- Заказы FBS (Marketplace): уточнено описание поля `scanDate` в схеме поставки — теперь «Дата сканирования поставки или первого заказа (RFC3339)» (ранее только «Дата скана поставки»).
- Заказы DBS (Marketplace): добавлен Sandbox-сервер `https://marketplace-api-sandbox.wildberries.ru` (помимо Prod) в `servers` для всех эндпоинтов `/api/v3/dbs/*` и `/api/marketplace/v3/dbs/*`.
- Самовывоз из магазина (Click&Collect, Marketplace): добавлен блок `servers` с Prod/Sandbox (`https://marketplace-api.wildberries.ru`, `https://marketplace-api-sandbox.wildberries.ru`) для всех эндпоинтов раздела `/api/v3/click-collect/*` и `/api/marketplace/v3/click-collect/*`.
- Заказы FBW (Supplies API): добавлен Sandbox-сервер `https://supplies-api-sandbox.wildberries.ru` (помимо Prod `https://supplies-api.wildberries.ru`) в `servers` для `/api/v1/acceptance/options` и `/api/v1/warehouses`.
- Продвижение (Advert API): добавлен Sandbox-сервер `https://advert-api-sandbox.wildberries.ru` (помимо Prod `https://advert-api.wildberries.ru`) в `servers` для всех эндпоинтов раздела `/adv/*`.
- Коммуникации (вопросы/отзывы, Feedbacks API): добавлен Sandbox-сервер `https://feedbacks-api-sandbox.wildberries.ru` (помимо Prod `https://feedbacks-api.wildberries.ru`) в `servers` для всех эндпоинтов `/api/v1/*` раздела.
- Отчёты (Statistics API): добавлен Sandbox-сервер `https://statistics-api-sandbox.wildberries.ru` (помимо Prod `https://statistics-api.wildberries.ru`) в `servers` для `/api/v1/supplier/stocks`, `/api/v1/supplier/orders`, `/api/v1/supplier/sales`.
- Финансы (Statistics API): для deprecated-эндпоинта `/api/v5/supplier/reportDetailByPeriod` добавлен Sandbox-сервер `https://statistics-api-sandbox.wildberries.ru` (помимо Prod) в `servers` (статус `deprecated: true` без изменений).

### Changed (2026.06.18)
- Карточки товаров: из описаний методов получения списка карточек товаров и списка карточек товаров в корзине удалено примечание о доступности только по токену с категорией «Контент» или «Продвижение» (изменение документации по авторизации, без изменения эндпоинтов).
- Orders FBS: добавлено новое поле `isPickupPointShipmentAllowed` (boolean, non-null) в моделях/ответах заказов — признак, можно ли отгрузить заказ на ПВЗ (`true`/`false`).
- Orders FBS: обновлены описания, связанные с проверкой маркировки — термин «валидация» заменён на «проверка», а также добавлены ссылки на KB для статусов/требований по маркировке (`decision`, `requiredMeta`, `optionalMeta`, `meta.status`).

### Changed (2026.06.17)
- Работа с товарами: спецификация переименована из `02-products.yaml` в `02-items.yaml`; соответственно клиентские модули `products` переименованы в `items` (пакеты `wildberries-sdk-products` → `wildberries-sdk-items`). Содержимое API не изменилось — это переименование вслед за источником Wildberries.

### Changed (2026.06.16)
- Orders FBS: уточнено описание статуса валидации маркировки `sgtinWithdrawn` — теперь «Выбыл. Проверка не пройдена» (вместо «Списан. Проверка не пройдена»)
- Самовывоз (Click&Collect) / Идентификаторы маркировки: добавлен новый метод `POST /api/marketplace/v3/click-collect/orders/meta/details` для получения идентификаторов маркировки сборочных заданий со статусами их проверки; ответ — `api.OrdersMetaDetailsResponse`
- Самовывоз (Click&Collect) / Идентификаторы маркировки: метод `POST /api/marketplace/v3/click-collect/orders/meta/info` помечен как `deprecated` и будет удалён 15 июля; добавлено явное предупреждение в описании
- Самовывоз (Click&Collect) / Идентификаторы маркировки: обновлены ссылки в описаниях методов удаления/закрепления маркировок (sgtin/uin/imei/gtin) на новый endpoint `/meta/details` вместо `/meta/info`
- Самовывоз (Click&Collect) / Идентификаторы маркировки: для нового метода получения деталей добавано описание лимитов — 150 запросов/мин на аккаунт (интервал 400 мс, всплеск 20), запросы с 4XX считаются как 10
- Самовывоз (Click&Collect) / Схемы: добавлены `api.MetaDetailsResponse`, `api.OrdersMetaDetailsResponse` и `MetaDetailsErrors` (детализация ошибок валидации по ключам `imei/uin/sgtin/gtin/expiration/customsDeclaration` с полями `key`, `value`, `decision`)

### Changed (2026.06.12)
- Orders FBS: в описаниях/ошибках по УИН заменена формулировка «спецификация с договором на поставку» на «спецификация с договором на доставку» (в т.ч. для `uinNotFound` и рекомендаций по повторному добавлению УИН).
- Orders DBW: удалён устаревший endpoint `PATCH /api/v3/dbw/orders/{orderId}/assemble` (перевод в доставку; ранее помечен deprecated и планировался к удалению 5 июня).
- Orders DBW: удалены устаревшие методы работы с маркировкой — `DELETE /api/marketplace/v3/dbw/orders/meta` (удаление идентификаторов по `key`) и `PUT /api/v3/dbw/orders/{orderId}/meta/sgtin` (привязка SGTIN; ранее deprecated, удаление 5 июня).
- Orders DBW: для batch-ошибок изменена схема `api.BatchError.detail`: было `object` (пример `{}`), стало `string`, `nullable: true` (пример `null`); обновлены примеры ответов (detail теперь `null`).
- Orders DBW: в одном из методов с `400`-ответом расширена схема ошибки до `allOf: [Error, api.BatchError]` и добавлен пример `UploadDataLimit` (превышен лимит загрузки).
- Orders DBW: для списка `orders` добавлено ограничение `maxItems: 1000` (лимит количества ID заказов в запросе).
- In-store pickup: `api.OrderClientInfo` — перенесены/уточнены примеры на уровне полей (`phone`, `firstName`, `orderID`, `phoneCode`), удалён общий `example`; также убрана точка в конце описания `phone`.
- In-store pickup: `api.OrderClientInfoResp` — удалены поля `supplierStatus` и `wbStatus` и соответствующий пример ответа.

### Changed (2026.06.11)
- Products / Цены и скидки: обновлено описание лимитов запросов — вместо единого лимита добавлена разбивка по типам (Персональный/Сервисный/Базовый с секретом: 6 сек, 10 запросов, интервал 600 мс, всплеск 5; Базовый: 1 ч, 4 запроса, интервал 15 мин, всплеск 1) для методов категории.
- Orders DBS: уточнено описание метода «Получить дату и время доставки» — теперь речь о доставке заказов (вместо «сборочных заданий»).
- Orders DBS: расширена модель данных доставки — поле `dDate` уточнено как «дата доставки, указанная покупателем» (обновлён пример), добавлены новые nullable-поля `dDateFrom` и `dDateTo` для интервала доставки, если он указан покупателем.

### Changed (2026.06.10)
- Products: исправлены ссылки в описаниях методов «Список контактов» и «Обновить список контактов» для складов продавца (обновлён путь документации на `/openapi/openapi/work-with-products#...`).
- Orders FBS: переименован tag для «идентификаторов маркировки» с `fbs-label-identifiers` на `fbsLabelIdentifiers` (обновлены все ссылки на раздел/методы маркировки).
- Orders FBS: массово обновлены ссылки в описаниях методов (пропуска/сборочные задания/поставки/стикеры/статусы) на новый базовый путь документации `/openapi/openapi/...`.
- Orders DBW: переименован tag для «метаданных/идентификаторов маркировки» с `dbw-label-identifiers` на `dbwLabelIdentifiers` (обновлены все ссылки).
- Orders DBW: исправлена ссылка в таблице статусов для перевода в `complete` — endpoint изменён с `/status/assemble` на `/status/deliver` (в документации).
- Orders DBW: обновлены ссылки в описаниях методов на новый базовый путь документации `/openapi/openapi/...`.
- Orders DBS: переименован tag для «идентификаторов маркировки» с `dbs-label-identifiers` на `dbsLabelIdentifiers` (обновлены все ссылки, включая тексты ошибок/requiredMeta).
- In-store pickup (Самовывоз): переименован tag для «идентификаторов маркировки» с `in-store-pickup-label-identifiers` на `inStorePickupLabelIdentifiers` (обновлены все ссылки в методах удаления/закрепления).

### Changed (2026.06.06)
- Общие: обновлены описания авторизации для методов «Получить информацию о продавце» и «Получить информацию о подписке Джем» — изменена ссылка на раздел про категории токенов (без изменения эндпоинтов/схем).

### Changed (2026.06.05)
- Общие: для `/api/common/v1/supplier-rating` и `/api/common/v1/subscriptions` добавлен новый вариант ответа `402` (Payment Required) помимо `401/429`.
- Товары (Контент/карточки): в описания лимитов/исключений для методов контента добавлены ссылки на новые методы рекомендаций (`postV1RecommendationsList`, `postV1RecommendationsSet`).
- Товары (Контент/медиа): переименованы компоненты ответов `208 Already Reported` — `Responses208` → `Response208`, `Responses208V3` → `Response208V3`; обновлены `$ref` в соответствующих методах. В `Response208V3` изменены описания полей `title` и `detail` с «ошибки» на «ответа».
- Заказы FBS: для ряда методов добавлен ответ `402` (Payment Required) в дополнение к существующим `401/403/404/429`.
- Заказы DBW: для методов добавлен ответ `402` (Payment Required) в дополнение к существующим `401/403/429`.
- Заказы DBS: для методов добавлен ответ `402` (Payment Required) в дополнение к существующим `401/403/404/429`.
- Самовывоз из магазина: для методов добавлен ответ `402` (Payment Required) в дополнение к существующим `401/403/429`.
- Продвижение/Маркетинг: добавлен новый раздел (tag) **«Рекомендации»**.
- Продвижение/Рекомендации: добавлены новые endpoints контента:
  - `POST https://content-api.wildberries.ru/api/content/v1/recommendations/list` — получение списка рекомендаций в карточках товаров (read-only), токены: personal/service, лимит 100 req/min (600 мс, burst 5); схемы `GetRecomReq/GetRecomRes`, ошибки `response400GetRecom`.
  - `POST https://content-api.wildberries.ru/api/content/v1/recommendations/set` — установка/обновление/удаление рекомендаций, токены: personal/service, лимит 100 req/min (600 мс, burst 5); ответы `200/208/400`, схемы `SetRecomReq/SetRecomRes`, ошибки `response208SetRecom/response400SetRecom`.
- Коммуникации: для методов (pins/claims/chats) добавлен ответ `402` (Payment Required) в дополнение к существующим `401/403/429`.
- Тарифы: для методов добавлен ответ `402` (Payment Required) в дополнение к существующим `401/403/404`.
- Аналитика: для методов добавлен ответ `402` (Payment Required) в дополнение к существующим `401/403`.
- Отчёты: для методов добавлен ответ `402` (Payment Required) в дополнение к существующим `401/403`.
- Финансы: для методов финансовых отчётов/документов добавлен ответ `402` (Payment Required) в дополнение к существующим `401/429`.

### Changed (2026.06.04)
- Products: в описаниях лимитов запросов уточнено правило тарификации — любой запрос с ответом `4XX` теперь учитывается как 10 запросов (ранее только `409`).
- Orders FBS: в описаниях лимитов запросов уточнено правило тарификации — любой запрос с ответом `4XX` теперь учитывается как 10 запросов (ранее только `409`), включая метод с лимитом 1 запрос/10 минут.
- Orders FBS: удалена устаревшая схема `Meta` (помечалась deprecated, планировалось отключение 30 апреля) и поле `meta` из `v3.GetMetaMultiResponse` — используйте `metaDetails`.
- Orders FBS: расширены и уточнены статусы проверки маркировки в `MetaDetails.status`: добавлены ошибки для `sgtin` (`sgtinNoGS`, `sgtinHasInvalidSymbols`, `sgtinHasNonLatinSymbols`, `sgtinInvalidPattern`), обновлены формулировки `pending/required`, переработано описание допустимости перевода поставки в доставку; добавлены/уточнены статусы (`imeiMaySell`, `imeiSoldB2B`, `sgtinIntroduced`, `sgtinSoldB2B`, `sgtinWithdrawn`, `sgtinDisaggregation`).
- Orders DBW: в описаниях лимитов запросов уточнено правило тарификации — любой запрос с ответом `4XX` теперь учитывается как 10 запросов (ранее только `409`).
- Orders DBS: в описаниях лимитов запросов уточнено правило тарификации — любой запрос с ответом `4XX` теперь учитывается как 10 запросов (ранее только `409`); также обновлены ссылки на раздел лимитов на `https://dev.wildberries.ru/docs/...`.
- In-store pickup: в описаниях лимитов запросов уточнено правило тарификации — любой запрос с ответом `4XX` теперь учитывается как 10 запросов (ранее только `409`); в ряде методов таблица лимитов заменена на плейсхолдер `<no value>`.
- Promotion: в теле запроса для создания/обновления кампании поле `name` стало обязательным (`required`).

### Changed (2026.06.03)
- Communications: во всех методах раздела заменена схема ошибок `responsefeedbackErr` → `responseFeedbackQuestionErr` (переименование/унификация модели ответа об ошибке)
- Communications: для PATCH-операции по вопросам добавлен ответ `422 Unprocessable Entity` («Ошибка обработки параметров запроса») с примером `ResponsePatchQuestion`
- Communications: для получения архивных отзывов добавлен ответ `422 Unprocessable Entity` («Ошибка обработки параметров запроса») с примером `ResponseGetFeedbackArchive`
- Communications: добавлены новые examples в components: `ResponseGetFeedbackArchive`, `ResponsePatchQuestion`
- Communications: поле `date` в одной из схем помечено как `deprecated: true` и добавлено описание о плановом отключении 16 июня (release-notes id=534)

### Changed (2026.05.30)
- Общая информация: изменена разметка описания (обёртка в `<div class="api-block">`, переразметка списков) — функциональных изменений API нет
- Товары (Products): изменена разметка описания (добавлен `<div class="api-block">`, блок ссылки на инструкцию вынесен отдельно) — функциональных изменений API нет
- Заказы FBS: изменена разметка описания (добавлен `<div class="api-block">`) — функциональных изменений API нет
- Заказы DBW: в описании раздела переименовано «идентификаторы маркировки» → «метаданные» для сборочных заданий (ссылка на тот же tag `dbw-label-identifiers`), добавлен `<div class="api-block">` — изменений эндпоинтов не показано
- Заказы DBS: изменена разметка описания (добавлен `<div class="api-block">`) — функциональных изменений API нет
- Заказы Самовывоз: изменена разметка описания (добавлен `<div class="api-block">`) — функциональных изменений API нет
- Заказы FBW: изменена разметка описания (добавлен `<div class="api-block">`) — функциональных изменений API нет
- Продвижение (Promotion): в одном из ответов поле/схема массива «Карточки товаров для кампаний» помечено как `nullable: true` (теперь может быть `null` вместо массива); также изменена разметка описания (добавлен `<div class="api-block">`)
- Общение с покупателями (Communications): изменена разметка описания (добавлен `<div class="api-block">`, блок ссылки на инструкцию вынесен отдельно) — функциональных изменений API нет
- Тарифы (Tariffs): изменена разметка описания (добавлен `<div class="api-block">`) — функциональных изменений API нет
- Аналитика (Analytics): изменена разметка описания (добавлен `<div class="api-block">`) — функциональных изменений API нет
- Отчёты (Reports): изменена разметка описания (добавлен `<div class="api-block">`) — функциональных изменений API нет
- Финансы (Finances): изменена разметка описания (добавлен `<div class="api-block">`) — функциональных изменений API нет

### Changed (2026.05.29)
- Products / Цены и скидки: добавлен POST `/api/discounts-prices/v1/upload/task/b2b/wholesale` для установки оптовых скидок B2B (personal/service token), асинхронная загрузка с ответами `200` (SuccessTaskResponseV3) и `208` (Responses208V3), лимит категории «Цены и скидки» — 10 запросов/6 сек (интервал 600 мс, всплеск 5)
- Products / Цены и скидки: расширены модели данных — добавлены `B2BWholesale`, `WholesaleDiscountThresholdReq/Res`, `B2BWholesaleTaskRequest`; в ответах товаров добавлено поле `wholesaleDiscountThreshold` (многоуровневые оптовые скидки для B2B)
- Products / Цены и скидки: обновлены описания методов истории задач `/api/v2/history/tasks` и детализации `/api/v2/history/goods/task`, а также методов получения цен (по одному артикулу и по списку) — теперь явно включают оптовые скидки B2B
- Products / Цены и скидки: поле `price` в схеме размера товара сделано `nullable: true`
- Products / Цены и скидки: введён новый формат ошибок V3 — `ResponseErrorV3`, новые примеры `UploadLimitExceededV3`, `InvalidDataFormatV3`, `InvalidItemNoV3`, `Result208V3`, `Result403V3`, а также примеры валидации уровней/значений скидок; обновлён текст `UnexpectedResult` (категория поддержки «Интеграции по API»)
- Products / Цены и скидки: уточнён лимит размера загрузки — пример `UploadLimitExceeded` теперь указывает максимум 1 000 items (вместо 10 000)
- Orders FBS: раздел «Метаданные FBS» переименован в «Идентификаторы маркировки FBS» (обновлены теги/описания/тексты ошибок и лимитов; функционально методы те же)
- Orders DBW: раздел «Метаданные DBW» переименован в «Идентификаторы маркировки DBW» (обновлены теги/описания/лимиты и тексты ошибок); deprecated-методы получения/удаления для одного задания остаются deprecated, но переименованы в терминах «идентификаторов маркировки»
- Orders DBS: раздел «Метаданные DBS» переименован в «Идентификаторы маркировки DBS» (обновлены теги/описания/лимиты и тексты ошибок; deprecated-метод получения метаданных также переименован терминологически)
- In-store pickup: раздел «Метаданные Самовывоз» переименован в «Идентификаторы маркировки Самовывоз» (обновлены теги/описания/лимиты и параметры удаления)
- Promotion: поле `nm_settings` помечено как `nullable: true` в ответе кампании
- Promotion: у поля `payment_type` убран `enum` (значения `cpm/cpc` остаются только в описании, без формального ограничения схемой)

### Changed (2026.05.28)
- Сборочные задания DBW: изменён summary метода «Дата и время доставки» → «Получить дату и время доставки» (без изменений контракта/параметров).
- Orders DBS: изменён summary метода «Дата и время доставки» → «Получить дату и время доставки» (без изменений контракта/параметров).

### Changed (2026.05.27)
- Orders FBS / Метаданные FBS: в описаниях и параметрах метаданных `customsDeclaration` термин «номер ГТД» заменён на «номер ДТ» (декларация на товары); обновлены summary/description, описание поля и текст ошибки `409`.
- Orders FBS / Метаданные FBS: уточнено правило — у сборочного задания может быть только один номер ДТ; ДТ обязательно для товаров, произведённых вне ЕАЭС; добавление по-прежнему доступно только в статусах `confirm` или `complete`.
- Orders DBS / Метаданные DBS: в описаниях и параметрах метаданных `customsDeclaration` термин «номер ГТД» заменён на «номер ДТ»; обновлены summary/description и описание поля.
- Orders DBS / Метаданные DBS: правило «один номер на сборочное задание» актуализировано для ДТ; ограничение по статусу без изменений — добавление только для заданий в статусе `deliver`.

### Changed (2026.05.26)
- Orders FBS: обновлено описание поля `sgtins` (массив кодов маркировки) — добавлен пример, уточнено что поддерживаются полный и короткий форматы кодов Честного знака, и что GS-разделитель нужно передавать как Unicode-экранирование `\u001D`.
- Communications: уточнено описание поля `rid/srid` — обновлены ссылки на источники `srid`, добавлены ссылки на новые методы детализаций финансовых отчётов (реализация и эквайринг: по ID отчётов и за период).
- Analytics: обновлены ссылки в описаниях отчётов — вместо прямой ссылки на `reportDetailByPeriod` теперь ссылка на раздел «Финансовые отчёты» (детализации к отчётам реализации).
- Reports: обновлены ссылки в описаниях методов заказов/продаж — вместо прямой ссылки на `reportDetailByPeriod` теперь ссылка на раздел «Финансовые отчёты» (детализации к отчётам реализации).

### Changed (2026.05.22)
- Общие: у поля `inviteUrl` убран формат `uri` (теперь просто `string`), валидация URL на уровне схемы ослаблена.
- Заказы DBS: обновлены ссылки в описании лимитов запросов на абсолютные (`https://dev.wildberries.ru/docs/...`) вместо относительных; сами лимиты/эндпоинты не изменены.
- Отчёты: в примере `photoUrls` домен `wildberries.ru` заменён на шаблон `{{ .baseDomain }}` (URL теперь параметризован по базовому домену).

### Changed (2026.05.21)
- Promotion: для метода получения данных по медиакампании добавлен ответ `400 Bad Request` (`text/plain`) с примерами ошибок `InvalidRcIdAdv`, `IncorrectName`, `IncorrectSupplierIdAdv`.
- Analytics: добавлен новый раздел/тег **«Оценка товара»**.
- Analytics: добавлен новый endpoint `POST /api/analytics/v1/item-rating` (read-only) для формирования отчёта по оценкам товаров (обновление данных 1 раз в час); лимит — **3 запроса/мин** (интервал 20 сек, всплеск 3).
- Analytics: для `POST /api/analytics/v1/item-rating` добавлены схемы `ItemRatingRequest`/`ItemRatingResponse` и связанные типы (периоды `currentPeriod`/`pastPeriod`, фильтры `nmIds`/`subjectIds`/`brandNames`/`tagIds` до 50, пагинация `limit` до 1000 и `offset`, сортировка `orderBy.field` по `feedbackRating|feedbackCount|fiveStar|...|disqualified` и `mode asc|desc`).
- Analytics: уточнены формулировки в описаниях percentile-метрик в CSV/схемах — заменено «карточек конкурентов» на «карточек других продавцов».

### Changed (2026.05.20)
- Общие: добавлен новый тип токена «Базовый с секретом» в таблицы лимитов (1 мин: 1 запрос; всплеск 10) для общих методов
- Товары: расширен фильтр `withPhoto` (enum: добавлены `-1` и `2`), изменена семантика значений и пример запроса (`withPhoto` по умолчанию/в примере теперь `-1`); добавлены лимиты для токена «Базовый с секретом» во множестве методов (в т.ч. «Цены и скидки»/карантин: 6 сек — 10 запросов, интервал 600 мс, всплеск 5)
- Заказы DBW: добавлены лимиты для токена «Базовый с секретом» (1 мин — 300 запросов, интервал 200 мс, всплеск 20; 409 считается за 10)
- Заказы DBS: добавлены лимиты для токена «Базовый с секретом» (1 мин — 500 запросов, интервал 120 мс, всплеск 20; 409 считается за 10); уточнён блок описания доступных токенов (текст/ссылка)
- Самовывоз (Click&Collect): удалены устаревшие endpoints сборочных заданий `/api/v3/click-collect/orders/{orderId}/confirm|prepare|receive|reject|cancel` и `/api/v3/click-collect/orders/status`, а также устаревшие методы метаданных `/api/v3/click-collect/orders/{orderId}/meta` (GET/DELETE) и `/api/v3/click-collect/orders/{orderId}/meta/{sgtin|uin|imei|gtin}` (PUT); актуальные методы закрепления метаданных стандартизированы на `/api/marketplace/v3/click-collect/orders/meta/{sgtin|uin|imei|gtin}` (POST) с ответом `200` и схемами `api.Orders*SetRequest`/`api.MetaSetResponses`; унифицирован лимит для закрепления метаданных: 1 мин — 20 запросов, интервал 3 сек, всплеск 500; удалены связанные схемы/примеры ошибок (`api.*Request`, `api.baseMeta`, `api.OrderStatuses`, `StatusMismatch`, `FailedToUpdateMeta` и др.)
- Заказы FBW: добавлены лимиты для токена «Базовый с секретом» во всех методах раздела (значения совпадают с персональным/сервисным в таблицах)
- Продвижение: добавлены лимиты для токена «Базовый с секретом» во всех методах раздела; исправлен пример `RespStatCampaignNotFound` — теперь массив объектов вместо одиночного объекта
- Коммуникации: добавлены лимиты для токена «Базовый с секретом» во всех методах раздела
- Тарифы: добавлены лимиты для токена «Базовый с секретом» (в т.ч. тарифы для коробов/монопаллет/возвратов: 1 мин — 60 запросов, интервал 1 сек, всплеск 5; и др.)
- Аналитика: добавлены лимиты для токена «Базовый с секретом» во всех методах раздела; уточнён блок описания доступных токенов для отчёта остатков на складах WB (текст/ссылка)
- Отчёты: добавлены лимиты для токена «Базовый с секретом» во всех методах раздела
- Финансы: добавлены лимиты для токена «Базовый с секретом» во всех методах раздела; уточнены блоки описания доступных токенов для методов отчётов реализации/эквайринга (текст/ссылка)

### Changed (2026.05.16)
- Products: изменён текст ошибки в примере для валидации поля «WB Club Discount» — вместо шаблонных значений `{{.WbClubMinDiscount}}/{{.WbClubMaxDiscount}}` теперь выводится `<no value>` для обеих границ.
- Orders DBS: в ответе `DbsOnlyClientInfoResp` поле `orders` помечено как `nullable: true` (теперь может быть `null`).
- Orders FBW: поле `supplierAssignName` помечено как `nullable: true` (теперь может быть `null`).
- Самовывоз (Click&Collect): обновлено описание лимитов запросов для методов смены статусов/получения статусов — убрано уточнение «для методов сборочных заданий Самовывоз» и удалено правило «запрос с кодом ответа 409 учитывается как 10 запросов» (численные лимиты 1 rps, burst 10 сохранены).
- Самовывоз (Click&Collect): в описаниях ответов `409` для методов добавления маркировки исправлена формулировка — удалена точка в конце («Ошибка добавления маркировки»).
- Promotion: для метода получения статистики добавлен новый вариант ответа/схема `StatCampaignNotFound` (поля `advert_id`, `error`) и пример `RespStatCampaignNotFound` для случая «кампания не найдена».

### Changed (2026.05.15)
- Products: уточнено описание поля `isVariable` (добавлена ссылка на KB; изменена формулировка про отличия вариантов по характеристике)
- Products: в примерах для фильтра `withPhoto` изменено значение по умолчанию с `-1` на `0`
- Products: параметр `filter.withPhoto` теперь ограничен `enum: [0, 1, -1]`; обновлена семантика значений с 3 июня (переопределены значения `0` и `-1`), `default` остаётся `0`
- Products: поле `sizeID` помечено как `nullable: true`
- Products: поля `newPrice` и `newDiscount` помечены как `nullable: true`
- Products: в схеме истории загрузки добавлено `nullable: true` для `uploadID` и `historyGoods`
- Promotion: объект `adverts` помечен как `nullable: true`

### Changed (2026.05.13)
- Общие: расширен список кодов разделов/доступов (enum `code`) — добавлены `brandsFlow` (Мои бренды), `copyrightComplaints` (Обращения правообладателей), `pretrialClaims` (Досудебные претензии), `sellersChat` (Чат с покупателями); обновлены примеры пользователей/ролей с этими новыми кодами.
- Заказы DBW: для одного из эндпоинтов добавлен новый возможный ответ `402` (подключена общая схема ответа `#/components/responses/402`).

### Changed (2026.05.09)
- Orders FBS: параметр `key` для удаления метаданных ограничен `enum` значениями `imei|uin|gtin|sgtin|customsDeclaration` (вместо текстового перечисления в описании); уточнено описание поля `ddate` — «планируемая дата доставки заказа покупателю» (для СГТ, `cargoType: 2`).
- Orders DBW: поле `key` (удаление метаданных) теперь строго ограничено `enum` `imei|uin|gtin|sgtin`; в описаниях `rid` обновлены ссылки на финансовые отчёты — вместо «Отчет о продажах по реализации» добавлены новые операции детализаций (реализация/эквайринг) по ID отчётов и за период.
- Orders DBS: поле `key` (удаление метаданных) теперь имеет `enum` `imei|uin|gtin|sgtin|customsDeclaration`; у поля `rid` убраны явные `type: string` и `nullable: false` (осталось только описание/пример), а также обновлены ссылки на финансовые отчёты аналогично (детализации реализация/эквайринг по ID и за период).
- In-store pickup: поле `key` (удаление метаданных) теперь строго ограничено `enum` `imei|uin|gtin|sgtin`; в описаниях `rid` обновлены ссылки на финансовые отчёты — добавлены операции детализаций (реализация/эквайринг) по ID и за период вместо старой ссылки на отчёт по реализации.
- Orders FBW: для ответа `400` изменён `Content-Type` с `application/json` на `text/plain; charset=utf-8` при сохранении схемы `models.ErrorModel`.

### Changed (2026.05.08)
- Products: добавлен новый пример ошибки `SKUUploadDisabled` (code: `SKUUploadDisabled`) — загрузка остатков по ключу `sku` запрещена, требуется использовать `chrtId`; этот пример подключён в ответы 400 для нескольких методов (в т.ч. как `SKUUploadDisabled` и как `IncorrectSkuParameter`, ссылающийся на тот же пример).
- Orders FBS: уточнено ограничение метода получения информации о сборочных заданиях — возвращаются только задания, созданные не более 3 месяцев назад; для более старых данных необходимо использовать метод получения списка архивных заказов `/api/marketplace/v3/fbs/orders/archive` (GET).

### Changed (2026.05.07)
- Orders FBS: в ответ метода POST `/api/v3/orders/status` добавлено поле `isCancellable` (boolean, not nullable) — признак доступности отмены сборочного задания
- Orders FBS: уточнено описание PATCH `/api/v3/orders/{orderId}/cancel` — отмена возможна только до передачи задания Wildberries; рекомендовано предварительно проверять `isCancellable` через POST `/api/v3/orders/status`

### Changed (2026.05.06)
- Orders DBW: добавлен batch-эндпоинт перевода в доставку `POST /api/marketplace/v3/dbw/orders/status/deliver` (из `confirm` в `complete`) с телом `api.OrdersRequestV2(ordersIds[])` и ответом `200 api.StatusSetResponses` (постатусно: `isError`, `errors`, `metaDetails`); обновлена ссылка для статуса `complete` на новый метод
- Orders DBW: `PATCH /api/v3/dbw/orders/{orderId}/assemble` помечен как `deprecated` и будет удалён 5 июня (старый одиночный перевод в доставку, ответ `204`)
- Orders DBW / Метаданные: добавлен batch-эндпоинт удаления метаданных `POST /api/marketplace/v3/dbw/orders/meta/delete` с телом `api.OrdersMetaDleteRequestV2(key, ordersIds[])` и ответом `200 api.MetaDeleteResponses` (постатусно по orderId)
- Orders DBW / Метаданные: добавлен batch-эндпоинт закрепления маркировок `POST /api/marketplace/v3/dbw/orders/meta/sgtin` (несколько заказов, `api.OrdersSGTINsSetRequest`) с ответом `200 api.StatusSetResponses`; лимит для метода изменён до 300/мин (200 мс, всплеск 20) вместо 1000/мин (60 мс)
- Orders DBW / Метаданные: `DELETE /api/v3/dbw/orders/{orderId}/meta` помечен как `deprecated` и будет удалён 5 июня (удаление метаданных по `key` в query)
- Orders DBW / Метаданные: `PUT /api/v3/dbw/orders/{orderId}/meta/sgtin` помечен как `deprecated` и будет удалён 5 июня; уточнены ограничения для `sgtins[]` (16–135 символов на код)
- Orders DBW: добавлены схемы для batch-операций и ошибок: `api.StatusSetResponses`, `api.BatchErrorResponse` (в т.ч. `MetaValidationFail` с `metaDetails.decision`), `api.MetaDeleteResponses`, `api.OrdersSGTINsSetRequest`, `api.OrdersMetaDleteRequestV2`; `api.OrdersRequestV2` перенесена/актуализирована (max 1000 id)
- Orders DBS: для ответа перевода в доставку заменена схема `api.StatusSetResponses` → `api.StatusSetDeliverResponses` (добавлена детализация `MetaValidationFail` с `metaDetails`); добавлены схемы `api.StatusSetDeliverResponses`, `api.BatchErrorDeliverResponse`
- Orders DBS / Метаданные: в описаниях заменено “код маркировки Честного знака” → “код маркировки”; уточнение: если `meta` пустой, метаданных нет и добавить нельзя (ранее упоминался `metaDetails`); удалён ответ `409` “Ошибка обновления метаданных” для одного из методов метаданных
- Analytics: обновлено описание rate limit — добавлено разбиение по типам токена (Персональный/Сервисный: 3/мин; Базовый: 2/час)
- Finances: обновлено описание rate limit — добавлено разбиение по типам токена (Персональный/Сервисный: 1/мин; Базовый: 2/24ч)

### Changed (2026.05.05)
- Products: в модели характеристики добавлено поле `existNamedField: boolean` — указывает, как передавать характеристику в запросах создания/создания с присоединением/редактирования карточек (`true` — отдельным параметром запроса, `false` — внутри массива `characteristics`); обновлён пример ответа (добавлено `existNamedField: true`).
- Orders FBS: уточнена логика выборки сборочных заданий по периоду — в ответ попадают задания, **созданные** в указанном интервале `dateFrom`–`dateTo` (макс. 30 дней).
- Orders FBS: параметры `dateFrom` и `dateTo` уточнены по часовому поясу — Unix timestamp в UTC (для `dateFrom` также сохранено значение по умолчанию «30 дней до запроса»).
- Orders FBS: поле `createdAt` (RFC3339) уточнено — время в UTC.

### Changed (2026.05.04)
- Orders DBS / Метаданные DBS: во всех методах работы с метаданными сборочных заданий обновлены ссылки в описаниях с `/v3/dbs/orders/meta/info` на `/v3/dbs/orders/meta/details` (удаление метаданных, закрепление кодов маркировки «Честный знак», УИН, IMEI, GTIN, номера ГТД); функциональные изменения эндпоинтов/полей и лимитов в диффе не зафиксированы.

### Changed (2026.05.01)
- Products: уточнены описания полей, связанных с маркировкой — `isKiz`, `needKiz`, `kizMarked` и подтверждение нанесения кода теперь явно относятся к коду маркировки [Честного знака](https://честныйзнак.рф/); без изменения схем/типов
- Products: переработаны описания параметров сортировки `ascending` (для `updatedAt` и `trashedAt`) и фильтра `allowedCategoriesOnly` (форматирование/семантика без изменения поведения)

- Orders FBS: в методах метаданных `sgtin` и в PUT закрепления маркировки обновлены summary/description — терминология приведена к «код маркировки Честного знака»; в схеме запроса `sgtins[]` уточнено описание элемента (ссылка на ЧЗ), убрано дублирование ограничений из описания массива (ограничения по длине остаются в описании элемента)
- Orders FBS / Поставки: термин «короба» заменён на «грузоместа» в методах `.../trbx` (получение списка, добавление, удаление, получение стикеров) и в описаниях полей (`trbxIds`, `id` в `Trbx`); эндпоинты не менялись
- Orders FBS: добавлено поле `recommendedWhId` (int64) в модели поставки — «ID рекомендуемого склада для приёмки поставки для Москвы и МО», `0` если не определён

- Orders DBW: в методах метаданных `sgtin` и в PUT закрепления маркировки обновлены summary/description — терминология приведена к «код маркировки Честного знака»; в схеме запроса `sgtins[]` уточнено описание элемента (ссылка на ЧЗ), убрано дублирование ограничений из описания массива

- Orders DBS: в методах метаданных `sgtin` и массового закрепления маркировок обновлены тексты/summary — терминология приведена к «код маркировки Честного знака»
- Orders DBS: исправлено описание: при пустой структуре метаданных теперь указано `metaDetails` вместо `meta` (уточнение документации)

- In-store pickup: в методе массового закрепления `sgtin` обновлены summary/description — терминология приведена к «коды маркировки Честного знака»

- Orders FBW: поле `needKiz` — уточнено описание, что речь о «коде маркировки Честного знака» (без изменения схемы)

- Finances: поля `kiz` и описание «Код маркировки» уточнены как «Код маркировки [Честного знака](https://честныйзнак.рф/)» (без изменения схем/типов)

### Changed (2026.04.30)
- Основные отчёты: обновлено описание лимитов запросов для методов раздела — вместо единого лимита «1 запрос/мин (всплеск 1)» введены типы лимитов (Персональный/Сервисный/Базовый) с разными периодами и всплесками; для части методов всплеск увеличен до 10 запросов, базовый лимит изменён на 1 запрос/3 ч или 1 запрос/2 ч (в зависимости от метода).

### Changed (2026.04.29)
- Orders FBS: добавлен GET `/api/marketplace/v3/fbs/orders/archive` для получения списка архивных сборочных заданий (старше 3 месяцев) с пагинацией `year`+`month`+`next`+`limit` (limit 100–1000) и лимитом 300 req/min (200 мс, burst 20); добавлены схемы ответа `v3.ArchiveOrders`/`v3.ArchiveOrder` и новый формат ошибок `v3.APIErrorV2` (в т.ч. ответы `401-2`, `429-2`).
- Orders DBW: добавлен batch-метод POST `/api/marketplace/v3/dbw/orders/meta/details` (тело `api.OrdersRequestV2.ordersIds` до 1000) для получения метаданных сборочных заданий и статусов их валидации; новый ответ `api.OrdersMetaDetailsResponse`, ошибки `api.BatchError`; лимит 300 req/min (200 мс, burst 20).
- Orders DBW: GET `/api/v3/dbw/orders/{orderId}/meta` помечен как `deprecated` и будет удалён 27 июля (замена — новый batch endpoint).
- Orders DBS: endpoint переименован/заменён с POST `/api/marketplace/v3/dbs/orders/meta/info` на POST `/api/marketplace/v3/dbs/orders/meta/details` с поддержкой статусов валидации; добавлены `api.OrdersRequestV2` и `api.OrdersMetaDetailsResponse`, ошибки `api.BatchError`.
- Orders DBS: POST `/api/marketplace/v3/dbs/orders/meta/info` помечен как `deprecated` и будет удалён 27 июля; для нового `/meta/details` обновлён лимит до 300 req/min (200 мс, burst 20) вместо 150 req/min (400 мс), правило «409 считается как 10 запросов» сохранено.

### Changed (2026.04.28)
- Products: в модели характеристик добавлено новое булево поле `isVariable` (признак меняющейся характеристики для различий вариантов товара); обновлён пример ответа с `isVariable: true`.
- Orders FBS: исправлена опечатка в перечислении ключей обязательной маркировки — `сustomsDeclaration` → `customsDeclaration`.
- Orders DBS: удалены устаревшие методы v3 `/api/v3/dbs/orders/status`, `/api/v3/dbs/orders/{orderId}/cancel|confirm|deliver|receive|reject`, а также `/api/v3/dbs/orders/{orderId}/meta` (GET/DELETE) и `/api/v3/dbs/orders/{orderId}/meta/{sgtin|uin|imei|gtin}` (PUT); удалены связанные компоненты (`Order`, `OrderDBS`, `Code`, `Meta`, примеры `InvalidWBCode`, `SGTINIsNotFilled`).
- Orders DBS: актуализированы batch-методы метаданных в `/api/marketplace/v3/dbs/orders/meta/*` (info/delete/sgtin/uin/imei/gtin/customs-declaration) — унифицированы схемы запросов/ответов (для `meta/info` используется `api.OrdersRequestV2` → `api.OrdersMetaResponse`, для set-методов — `api.*SetRequest` → `api.StatusSetResponses`), и обновлены лимиты: для получения/удаления метаданных — 150 req/min (интервал 400 ms, burst 20), для закрепления `sgtin` явно добавлены типы лимитов (персональный/сервисный/базовый).

### Changed (2026.04.25)
- Orders FBS: Терминология кроссбордера заменена на «трансграничные поставки» (в т.ч. для статуса `cancel_carrier`/`canceled_by_carrier`, методов стикеров и истории статусов, а также ограничения «только для Турции»).
- Orders FBS: Обновлены описания поля `crossBorderType` в схемах — `0` теперь «внутренняя поставка», `1` — «трансграничная поставка» (enum без изменений).
- Orders FBS: Уточнено правило добавления в пустую поставку — можно добавлять сборочные задания «трансграничных или внутренних поставок»; тип поставки определяется первым добавленным заказом по `crossBorderType`.
- Orders DBS: Изменена логика отмены — метод отмены переводит в `cancel` только из статусов `new` и `confirm`; отмена из `deliver` больше не допускается (явно указано).
- Promotion: Обновлено описание лимитов запросов — вместо единого лимита добавлены типы лимитов `Персональный` и `Сервисный` (с прежними значениями) и введён `Базовый` лимит (почасовые ограничения) для множества методов (кампании/создание/управление/финансы/статистика/рекомендованные ставки и др.).

### Changed (2026.04.23)
- Products: в примерах ошибок заменён шаблонный домен `openapi.{{ .baseDomain }}` на фиксированный `openapi.wildberries.ru` (поле `detail`)
- Products: для массива `chrtIds` добавлено ограничение `maxItems: 1000`
- Promotion: в примере ответа заменён шаблонный домен `www.{{ .baseDomain }}` на `www.wildberries.ru` (поле `url`)
- Reports: в примере ответа заменён шаблонный домен `static-basket-03.{{ .baseDomain }}` на `static-basket-03.wildberries.ru` (элементы `photoUrls`)
- Orders DBW: правка документации/форматирования описания поля `contacts` (без изменения схемы)

### Changed (2026.04.22)
- Products: в ответах методов с характеристиками добавлено поле `hasFilter: boolean` (признак ключевой/фильтруемой характеристики для покупателей)
- Products / Цены и скидки: обновлено описание лимитов — вместо единого лимита добавлены типы лимитов (Персональный/Сервисный: 10 запросов за 6 сек, Базовый: 4 запроса за 1 ч); применено ко всем методам категории, включая «Получить товары в карантине»
- Orders DBS: для устаревших методов добавлено описание лимитов запросов для «сборочных заданий DBS» (Персональный/Сервисный: 100/мин, Базовый: 50/ч; запрос с HTTP 409 считается за 10)
- Orders DBS: для устаревших методов добавлено описание лимитов запросов для «закрепления метаданных DBS» (Персональный/Сервисный: 300/мин или 1000/мин в зависимости от метода, Базовый: 10/ч; запрос с HTTP 409 считается за 10)
- Самовывоз (In-store pickup): для устаревших методов добавлено описание лимитов запросов для «сборочных заданий Самовывоз» (Персональный/Сервисный: 100/мин; Базовый: 10/ч или 50/ч в зависимости от метода; запрос с HTTP 409 считается за 10)
- Orders FBW: обновлены лимиты запросов — добавлены типы лимитов (Персональный/Сервисный сохраняют прежние значения; добавлен Базовый: 2 запроса/ч для большинства методов)
- Promotion / Календарь акций: обновлены лимиты запросов — добавлены типы лимитов (Персональный/Сервисный: 10 запросов за 6 сек; Базовый: 1 запрос/ч)
- Communications / Вопросы и отзывы: обновлены лимиты запросов — добавлены типы лимитов (Персональный/Сервисный: 3 запроса/сек; Базовый: 5 запросов/ч)
- Communications / Чат с покупателями: обновлены лимиты запросов — добавлены типы лимитов (Персональный/Сервисный: 10 запросов/10 сек; Базовый: 1 запрос/ч)
- Tariffs: обновлены лимиты запросов — добавлены типы лимитов (Персональный/Сервисный сохраняют прежние значения; добавлен Базовый: 5 запросов/ч или 1 запрос/ч в зависимости от метода)
- Analytics: обновлены лимиты запросов — добавлены типы лимитов (Персональный/Сервисный: 3 запроса/мин; Базовый: 2 запроса/ч или 1 запрос/ч в зависимости от метода)
- Reports: обновлены лимиты запросов — добавлены типы лимитов (Персональный/Сервисный сохраняют прежние значения; добавлены/уточнены Базовые лимиты: 4 запроса/ч, 2 запроса/ч или 1 запрос/ч; для одного метода Базовый: 1 запрос/3 ч)
- Finances / Финансовые отчёты: для устаревшего метода обновлены лимиты запросов — добавлены типы лимитов (Персональный/Сервисный: 1 запрос/мин с всплеском 10; Базовый: 2 запроса/24 ч)

### Changed (2026.04.21)
- Введение: обновлено описание лимитов запросов — вместо одной строки добавлена типизация лимитов (Персональный/Сервисный/Базовый); для базового лимита добавлены новые окна 1 ч (1 запрос/1 ч, всплеск 1) и 24 ч (1 запрос/24 ч, всплеск 1) для соответствующих методов.
- Товары: обновлены лимиты запросов — добавлены типы лимитов (Персональный/Сервисный/Базовый); для базового лимита введено ограничение 1 запрос/час (всплеск 1) для методов раздела «Категории, предметы и характеристики».
- Продвижение: обновлены лимиты запросов — добавлены типы лимитов (Персональный/Сервисный/Базовый); для базового лимита введены ограничения 5 запросов/час (интервал 12 мин, всплеск 1) для методов управления кампаниями и 1 запрос/час для части методов (в т.ч. финансовых/прочих в этом файле).
- Коммуникации: обновлены лимиты запросов — добавлены типы лимитов (Персональный/Сервисный/Базовый); для базового лимита введено ограничение 10 запросов/час (интервал 6 мин, всплеск 1) для соответствующего метода.
- Аналитика: уточнено требование к генерации отчётов — каждый новый отчёт должен иметь уникальный `ID` (предупреждение о возможных ошибках при повторном использовании).
- Аналитика: изменены ограничения по `limit` для топа поисковых запросов — максимум 100 теперь указан для тарифов «Джема» **Продвинутый** и **Премиальный** (вместо только «Продвинутый»); аналогичное уточнение в описании массива поисковых запросов в схемах.
- Аналитика: уточнено описание метода «Заказы и позиции по поисковым запросам товара» — данные сгруппированы по дням, максимальный период 7 дней; добавлено ограничение: отчёт можно получить максимум за последние 365 дней.
- Отчёты: обновлены лимиты запросов — добавлены типы лимитов (Персональный/Сервисный/Базовый); для базового лимита введены новые ограничения 6 ч (1 запрос/6 ч), 1 ч (1 запрос/1 ч) для ряда методов.
- Финансы: обновлены лимиты запросов — добавлены типы лимитов (Персональный/Сервисный/Базовый); для базового лимита введено ограничение 1 запрос/24 ч (всплеск 1) для методов баланса/справочников/операций, где ранее были минутные/секундные окна.

### Changed (2026.04.18)
- Продукты (карточки товаров): обновлено описание лимитов запросов — вместо одной строки добавлены типы лимитов (Персональный/Сервисный: 3 запроса/мин, интервал 20 сек, всплеск 5; добавлен Базовый: 2 запроса/ч, интервал 30 мин, всплеск 1).
- Продукты (карточки товаров): обновлено описание лимитов запросов для второго метода — Персональный/Сервисный: 10 запросов/мин, интервал 6 сек, всплеск 5; добавлен Базовый: 1 запрос/2 ч, интервал 2 ч, всплеск 1.

- Заказы FBS: уточнены условия передачи поставки в доставку — теперь требуется, чтобы обязательная маркировка была указана для всех сборочных заданий и вся маркировка прошла валидацию; добавлено примечание про обязательный УИН и необходимость заранее загрузить спецификацию с договором (обработка статусов УИН в ГИИС ДМДК ~30 минут).
- Заказы FBS (метаданные/маркировка): нормализованы значения типа маркировки в описаниях статусов (IMEI/UIN/SGTIN/GTIN/Expiration/Customs declaration → `imei`/`uin`/`sgtin`/`gtin`/`expiration`/`customsDeclaration`; также `сustomsDeclaration` исправлено на `customsDeclaration` в одном месте).
- Заказы FBS (метаданные/маркировка): расширено описание ошибки `uinNotFound` — ссылка на ГИИС ДМДК и рекомендации (проверка УИН в спецификации, перезагрузка через удаление/добавление, корректность/статус «в обороте»); уточнено написание «Честном знаке» в `sgtinNotFound`.

- Заказы DBW: обновлено описание лимитов запросов для методов управления сборочными заданиями — добавлены типы лимитов (Персональный/Сервисный: 300 запросов/мин, интервал 200 мс, всплеск 20; добавлен Базовый: 10 запросов/ч, интервал 6 мин, всплеск 1).

- Заказы DBS: обновлено описание лимитов запросов для методов закрепления метаданных — добавлены типы лимитов (Персональный/Сервисный: 500 запросов/мин, интервал 120 мс, всплеск 20; добавлен Базовый: 10 запросов/ч, интервал 6 мин, всплеск 1).

- Самовывоз (in-store pickup): обновлено описание лимитов запросов для методов закрепления метаданных — добавлены типы лимитов (Персональный/Сервисный: 300 запросов/мин, интервал 200 мс, всплеск 20; добавлен Базовый: 10 запросов/ч, интервал 6 мин, всплеск 1).
- Самовывоз (in-store pickup): обновлено описание лимитов запросов для второго метода закрепления метаданных — добавлены типы лимитов (Персональный/Сервисный: 1000 запросов/мин, интервал 60 мс, всплеск 20; добавлен Базовый: 10 запросов/ч, интервал 6 мин, всплеск 1).

- Заказы FBW: обновлено описание лимитов запросов для 2 методов — добавлены типы лимитов (Персональный/Сервисный: 6 запросов/мин, интервал 10 сек, всплеск 6/10; добавлен Базовый: 1 запрос/12 ч, интервал 12 ч, всплеск 1).

- Продвижение (кампании/медиа/статистика): во всех затронутых методах обновлено описание лимитов запросов — добавлены типы лимитов (Персональный/Сервисный сохраняют прежние значения), добавлен Базовый с ограничениями 1–5 запросов/ч (в зависимости от метода; для части методов 2 запроса/ч с интервалом 30 мин, для медиа/статистики — 1 запрос/ч, для одного медиа-метода — 5 запросов/ч с интервалом 12 мин).

- Коммуникации: обновлено описание лимитов запросов для 2 методов — добавлены типы лимитов (Персональный/Сервисный: 20 запросов/мин, интервал 3 сек, всплеск 10; добавлен Базовый: 1 запрос/ч, интервал 1 ч, всплеск 1).

- Тарифы: обновлено описание лимитов запросов для методов тарифов (короба, монопаллеты, возврат) — добавлены типы лимитов (Персональный/Сервисный: 60 запросов/мин, интервал 1 сек, всплеск 5; добавлен Базовый: 1 запрос/ч, интервал 1 ч, всплеск 1).

- Аналитика: обновлено описание лимитов запросов для множества методов — добавлены типы лимитов (Персональный/Сервисный: 3 запроса/мин, интервал 20 сек, всплеск 3), добавлен Базовый (обычно 1 запрос/ч; для части методов 2 запроса/ч с интервалом 30 мин).

- Отчёты: обновлено описание лимитов запросов — добавлены типы лимитов (Персональный/Сервисный: 10 запросов/5 ч, интервал 30 мин, всплеск 10; добавлен Базовый: 2 запроса/24 ч, интервал 12 ч, всплеск 1).
- Отчёты: обновлено описание лимитов запросов для второго метода — добавлены типы лимитов (Персональный/Сервисный: 1 запрос/мин; добавлен Базовый: 4 запроса/ч, интервал 15 мин, всплеск 1).

### Changed (2026.04.17)
- Общие: в примере `inviteUrl` заменён шаблонный домен `seller.{{ .baseDomain }}` на фиксированный `seller.wildberries.ru`
- Общие / Products / Orders FBS / Orders DBW / Orders DBS / In-store pickup / Orders FBW / Promotion / Communications / Tariffs / Analytics / Reports / Finances: обновлено описание и пример для ошибки `402 Payment required` — теперь указано, что ошибка возвращается только сервисам из «Каталога решений для бизнеса», и изменён текст `detail` + ссылка на пополнение баланса на `https://dev.wildberries.ru/company`
- Orders DBW: в описании лимитов для DBW уточнены формулировки («методы DBW», «управление сборочными заданиями»)
- Orders DBW: удалено примечание о тарификации ответа `409` как 10 запросов в блоке лимитов для методов сборочных заданий
- Orders DBW: переименован блок лимитов для метаданных с «закрепления метаданных модели DBW» на «закрепления метаданных DBW» (без изменения численных лимитов)
- In-store pickup: для устаревших методов закрепления метаданных добавлены блоки rate limit (в т.ч. правило: ответ `409` считается как 10 запросов); указаны лимиты 300/мин (200 мс, всплеск 20) и 1000/мин (60 мс, всплеск 20) соответственно

### Changed (2026.04.16)
- Orders FBS: уточнено описание статуса `ready_for_pickup` — теперь «заказ прибыл на ПВЗ» (ранее «сборочное задание прибыло на ПВЗ»).
- Orders DBS: уточнено описание статуса `ready_for_pickup` — теперь «заказ прибыл на ПВЗ» (ранее «сборочное задание прибыло на ПВЗ»).
- Самовывоз (Click&Collect): в методе получения статусов сборочных заданий уточнено описание `wbStatus=ready_for_pickup` — теперь «заказ готов к выдаче» (ранее «сборочное задание готово к выдаче»).

- Finances / Финансовые отчёты: добавлен POST `https://finance-api.wildberries.ru/api/finance/v1/sales-reports/list` — список отчётов реализации за период (доступно с 01.01.2025), поддержка токенов `personal`/`service`, лимит 1 запрос/мин.
- Finances / Финансовые отчёты: добавлен POST `https://finance-api.wildberries.ru/api/finance/v1/sales-reports/detailed/{reportId}` — детализация отчёта реализации по `reportId` (BigInt/int64), токены `personal`/`service`, лимит 1 запрос/мин; пагинация через `rrdId`, выбор полей через `fields`.
- Finances / Финансовые отчёты: добавлен POST `https://finance-api.wildberries.ru/api/finance/v1/sales-reports/detailed` — детализация отчётов реализации за период (доступно с 29.01.2024), лимит 1 запрос/мин; параметры `dateFrom/dateTo`, `period (daily|weekly)`, `rrdId`, `limit`, `fields`.
- Finances / Финансовые отчёты: добавлены отчёты по эквайрингу:
  - POST `/api/finance/v1/acquiring/list` — список отчётов об издержках на приём платежей, токены `personal`/`service`, лимит 1 запрос/мин.
  - POST `/api/finance/v1/acquiring/detailed/{reportId}` — детализация по ID отчёта, токены `personal`/`service`, лимит 1 запрос/мин; `rrdId/limit/fields`.
  - POST `/api/finance/v1/acquiring/detailed` — детализация за период, токены `personal`/`service`, лимит 1 запрос/мин; `dateFrom/dateTo`, `rrdId/limit/fields`.
- Finances / Deprecations: GET `https://statistics-api.wildberries.ru/api/v5/supplier/reportDetailByPeriod` помечен как `deprecated` и будет удалён 15 июля; для ошибок `400` теперь используется общий ответ `response400FinancialReports`.
- Finances / Ошибки: унифицирован формат `400` для фин. отчётов — `Content-Type: application/problem+json`, поле `request_id` переименовано в `requestId`, обновлены примеры и `origin` (`open-api-finreports`).
- Finances / Схемы: обновлены описания полей эквайринга (`acquiring_fee`, `acquiring_percent`, `payment_processing`) на формулировки «компенсация платёжных услуг/комиссия за интеграцию платёжных сервисов».
- Finances / Схемы: изменена семантика `reportType` — удалено значение `4`, обновлены описания типов (1 — основной, 2 — по выкупам, 3 — по выкупам для Грузии).

### Changed (2026.04.15)
- Products: обновлены ссылки в описаниях/документации (инструкция «Работа с товарами» и якоря про объединение/разъединение карточек по `imtID`), без изменений эндпоинтов, схем, полей и лимитов
- Orders FBS: обновлена ссылка на инструкцию (перенос с `news/127` в knowledge-base), без изменений API
- Orders DBW: обновлена ссылка на инструкцию (перенос с `news/241` в knowledge-base), без изменений API
- Communications (Общение с покупателями): обновлена ссылка на инструкцию (перенос с `news/278` в knowledge-base) и ссылки в описаниях полей/параметров `imtId` и логики закрепления отзывов для объединённых карточек, без изменений эндпоинтов, схем, полей и лимитов

### Changed (2026.04.13)
- Общие: в примере ответа для инвайта изменён `inviteUrl` на шаблонный домен `https://seller.{{ .baseDomain }}/...` вместо `https://seller.wildberries.ru/...`; в примере ошибки 402 обновлён URL пополнения баланса на `https://dev.{{ .baseDomain }}/company`
- Товары (Products): в примерах ошибок обновлён `detail` со ссылкой на документацию на `https://openapi.{{ .baseDomain }}/content/api/ru/` вместо `https://openapi.wildberries.ru/...`; в примере ошибки 402 обновлён URL пополнения баланса на `https://dev.{{ .baseDomain }}/company`
- Заказы FBS: в примере ошибки 402 обновлён URL пополнения баланса на `https://dev.{{ .baseDomain }}/company`
- Заказы DBW: в примере ошибки 402 обновлён URL пополнения баланса на `https://dev.{{ .baseDomain }}/company`
- Заказы DBS: в примере ошибки 402 обновлён URL пополнения баланса на `https://dev.{{ .baseDomain }}/company`
- Самовывоз (In-store pickup): в примере ошибки 402 обновлён URL пополнения баланса на `https://dev.{{ .baseDomain }}/company`
- Заказы FBW: в примере ошибки 402 обновлён URL пополнения баланса на `https://dev.{{ .baseDomain }}/company`
- Продвижение (Promotion): в примере объекта акции/рекламы обновлено поле `url` на `https://www.{{ .baseDomain }}/promotions/...` вместо `https://www.wildberries.ru/...`; в примере ошибки 402 обновлён URL пополнения баланса на `https://dev.{{ .baseDomain }}/company`
- Коммуникации (Communications): в примере ошибки 402 обновлён URL пополнения баланса на `https://dev.{{ .baseDomain }}/company`
- Тарифы (Tariffs): в примере ошибки 402 обновлён URL пополнения баланса на `https://dev.{{ .baseDomain }}/company`
- Аналитика (Analytics): в примере ошибки 402 обновлён URL пополнения баланса на `https://dev.{{ .baseDomain }}/company`
- Отчёты (Reports): в примере ошибки 402 обновлён URL пополнения баланса на `https://dev.{{ .baseDomain }}/company`; в примере данных отчёта обновлены `photoUrls` на `https://static-basket-03.{{ .baseDomain }}/...` вместо `https://static-basket-03.wildberries.ru/...`
- Финансы (Finances): в примере ошибки 402 обновлён URL пополнения баланса на `https://dev.{{ .baseDomain }}/company`

### Changed (2026.04.10)
- Products: добавлено поле `kizMarked` (boolean, default `false`, non-nullable) — подтверждение продавца, что обязательный код маркировки «Честный знак» нанесён на товар; добавлено в модели/примеры карточек и вариантов (в т.ч. в запросах на создание/обновление), при этом обязательность маркировки определяется по `needKiz` (если `needKiz=true` и `kizMarked=false`, карточка не пройдёт модерацию).
- Products: уточнено описание поля `needKiz` (форматирование/перечень значений без изменения типа: boolean).

### Changed (2026.04.09)
- Orders FBS: поля `partA` и `partB` в ответе со стикерами изменены с `integer` на `string` (примеры теперь строковые), уточнены описания («…для печати подписи»).
- Orders FBS: в ответ со стикерами добавлены поля `partA`, `partB`, `barcode` (закодированное значение стикера) и обновлён пример ответа (в т.ч. для статуса `awaitingTrackNumber` добавлены пустые значения).
- Orders DBW: обновлены описания полей `partA`/`partB` («…для печати подписи»), изменён пример значения `partB` с `'9753'` на `'97523'`.

### Changed (2026.04.08)
- Finances: в схему ответа добавлены поля `article_substitution` (ID подменного артикула), `sale_price_affiliated_discount_prc` (скидка по подменному артикулу, %), `agency_vat` (удержание агентского НДС, %; только для продавцов из Кыргызстана; возвращается при наличии значения), `sale_price_wholesale_discount_prc` (оптовая скидка для бизнеса, %)

### Changed (2026.04.07)
- Products: в ответе для пакетов ошибок (PublicErrorsOutput) добавлено поле `updatedAt` (string, date-time) — дата/время создания или редактирования пакета; обновлены примеры (в т.ч. `cursor.updatedAt` и `subjects[].updatedAt`).
- Products: для операций изменения цен/скидок добавлен новый ответ `409 Conflict` — ошибка конвертации/смены валюты (`ResponseError`, пример `Result409`: “You can't change prices and discounts while switching to another currency”).

### Changed (2026.04.03)
- Информация о продавце: добавлен GET `/api/common/v1/rating` (feedbacks-api) — получение рейтинга продавца и количества отзывов; доступ только по сервисному токену категории «Вопросы и отзывы»; лимит 1 запрос/мин (всплеск 1)
- Информация о продавце: добавлен GET `/api/common/v1/subscriptions` (common-api) — информация о подписке «Джем» (state/activationSource/level/since/till), при отсутствии подписки возможен пустой ответ `200`; доступ по сервисному токену; лимит 1 запрос/мин (всплеск 10)
- Информация о продавце: обновлено описание/summary метода получения информации о продавце — теперь явно указано, что можно использовать токен любой категории (убрано ограничение про «Тестовый контур»)

- Orders FBS: добавлен статус `cancel_carrier` (отменено перевозчиком) и `wbStatus` `canceled_by_carrier` — только для кроссбордера
- Orders FBS: ужесточены условия для PATCH `/api/v3/supplies/{supplyId}/deliver` — в поставке не должно быть сборочных заданий с отсутствующей обязательной маркировкой или с маркировкой, не прошедшей валидацию
- Orders FBS: для PATCH `/api/v3/supplies/{supplyId}/deliver` изменён формат ошибки `409` — вместо `Error` используется `409SupplyDeliverError`; заменён пример `UinIsNotFilled` на `MetaValidationFail` с деталями по заказам/метаданным
- Orders FBS: добавлена схема `MetaDetails` и поле `metaDetails` (массив) в ответах по метаданным сборочных заданий; поле `meta` помечено как `deprecated`, схема `Meta` помечена как устаревшая и будет отключена 30 апреля

- Продвижение: методы статистики поисковых кластеров теперь поддерживают кампании с моделями оплаты `cpm` и `cpc` (ранее только `cpm`)
- Продвижение: в моделях статистики поисковых кластеров поля `views`, `ctr`, `cpm` сделаны `nullable`; для кампаний `cpc` эти значения возвращаются `null` (обновлены описания)

### Changed (2026.03.27)
- General: в перечисление прав доступа (components.schemas.*.permissions[].code) добавлены новые коды `oldAnalyticsReports` (Отчёты) и `marketplace` (Свой склад); они также появились в примерах ответов для списков пользователей/ролей с `disabled: false`.

### Changed (2026.03.25)
- Orders FBS: в ответе метода получения PDF-стикеров сборочных заданий кроссбордера добавлено поле `status` (enum: `awaitingTrackNumber`, `ready`) — статус генерации стикера; обновлено описание с рекомендацией повторять запрос до `ready`.
- Orders FBS: изменена схема элемента `stickers`: поле `file` (base64 PDF) перемещено ниже (после `parcelId`), добавлен пример ответа, где при `awaitingTrackNumber` поля `parcelId`/`file` могут быть пустыми.

### Changed (2026.03.24)
- Аналитика / История остатков: добавлен новый read-only endpoint `POST /api/analytics/v1/stocks-report/wb-warehouses` (токены: personal, service) для получения текущих остатков по складам WB; обновление данных раз в 30 минут; лимит 3 запроса/мин (интервал 20 сек, всплеск 1 запрос).
- Аналитика / История остатков: добавлены схемы `InventoryRequest` (фильтры `nmIds` до 1000, опционально `chrtIds`, пагинация `limit` до 250000 и `offset`) и `InventoryWbResponse` (поля по размеру и складу: `nmId`, `chrtId`, `warehouseId`, `warehouseName`, `regionName`, `quantity`, `inWayToClient`, `inWayFromClient`).
- Отчёты / Склады: метод «Склады» помечен как `deprecated: true`; в описании указано, что будет удалён 23 июня (ссылка на release notes).

### Changed (2026.03.21)
- Общие: в ответе с данными продавца добавлено поле `tin` (string) — ИНН
- Товары (Контент / Карточки товаров): добавлены новые методы `POST /content/v2/cards/delete/trash` (перенос карточек в корзину) и `POST /content/v2/cards/recover` (восстановление карточек из корзины)
- Товары (Контент / Карточки товаров): поле `updatedAt` в выдаче списка карточек помечено как `nullable: true` (может быть `null`)
- Товары (Контент): обновлено описание лимитов для части методов карточек — убран список «исключений» из общего лимита (теперь формулировка «лимит на один аккаунт продавца» без перечисления исключений)
- Товары (Контент / Медиафайлы): в описании лимитов для загрузки медиа добавлены в список исключений новые методы корзины (`/content/v2/cards/delete/trash`, `/content/v2/cards/recover`)
- Продвижение: метод «Изменение ставок в кампаниях» расширен — теперь явно поддерживает кампании с моделью оплаты `cpc` (за клики) помимо единой/ручной ставки
- Продвижение: метод «Установка и удаление минус-фраз» — изменено описание применимости: теперь для кампаний с единой и ручной ставкой (вместо ограничения на ручную ставку и `cpm`)
- Коммуникации: в примерах `photoLinks` изменены расширения ссылок изображений с `.jpg` на `.webp`
- Коммуникации: удалено поле `clientID` (ранее `deprecated`) из схем/примеров сообщений чата с покупателем
- Коммуникации: удалено поле `statusID` (ранее `deprecated`) из схемы товара в коммуникациях
- Тарифы: уточнены описания — тарифы для коробов совпадают с тарифами для «Суперсейфа», для монопаллет — с тарифами для «Поштучных паллет» (лимиты без изменений: 60/мин)

### Changed (2026.03.19)
- Products: добавлены примеры ошибок 400 для операций с объединёнными карточками — `MissingRequiredCharacteristics` (не заполнены обязательные характеристики) и `NonUniqueCharacteristicsInOneGroup*` (неуникальные характеристики в группе) для методов создания/добавления характеристик
- Orders FBS: переименовано поле опций заказа `isB2b` → `isB2B` (breaking change в схемах)
- Orders DBW: добавлен новый endpoint `POST /api/marketplace/v3/dbw/orders/client` для получения информации о покупателе по ID сборочных заданий; введены схемы ответа `ClientInfoResp`/`ClientInfo` (поля: `replacementPhone`, `phone`, `phoneCode`, `additionalPhones`, `additionalPhoneCodes`, `firstName`, `fullName`, `orderId`); уточнено описание поля ошибки `Error.data`
- Orders DBS: в описаниях лимитов удалено правило «ответ 409 считается как 10 запросов»; расширена модель ошибки — `detail` дополнено значением `ImeiIsNotFilled`, описание `code` уточнено (404/409)
- Orders FBW: добавлено поле `isBoxOnPallet` (boolean) для поставок типа «Поштучная палета», возвращается только при `boxTypeID=2`; расширены/уточнены описания `boxTypeID` и опций доступных типов поставки по складам (добавлен флаг `isBoxOnPallet`)
- Promotion (Маркетинг/Реклама): добавлен endpoint `GET /api/advert/v0/bids/recommendations` (только для кампаний `cpm`) для получения рекомендуемых ставок по карточке (`base`) и поисковым кластерам (`normQueries`); лимит 5 запросов/мин; добавлены схемы `V0BidsRecommendationsResponse` и связанные; добавлены примеры ошибок 400 `IncorrectTypeAdv`, `IncorrectUsingMethods`; в ответах `V0GetNormQueryMinusResponseItem` и `V0GetNormQueryMinusResponse` сняты требования `required` (поля `advert_id`, `nm_id`, `items` больше не обязательны)
- Communications: в модели чата уточнено поле `addTime` (Unix Timestamp в мс, «дата и время создания чата») и добавлено новое поле `sign` (подпись чата)
- Reports: удалён (ранее deprecated) endpoint `GET /api/v1/supplier/incomes` «Поставки» и схема `IncomesItem`; переименован раздел/теги «Платная приёмка» → «Операции при приёмке» (эндпоинты `/api/v1/acceptance_report*` без изменения путей, обновлены ссылки/описания)

### Changed (2026.03.11)
- Orders FBS: уточнены правила добавления коробов в поставку — только в открытую; лимит по количеству коробов: не больше количества товаров в поставке + 1.
- Orders DBW: метод получения стикеров сборочных заданий — расширены допустимые статусы заказов для получения стикеров: `confirm` (на сборке) и `complete` (в доставке) вместо только `confirm`; ограничение «максимум 100 стикеров за запрос» сохранено и вынесено в описание; формулировки по форматам стикеров уточнены («доступные форматы»).

### Changed (2026.03.06)
- Общие: уточнено описание поля `detail` в ошибке (Payment Required) — теперь явно указывает на недостаток средств на балансе сервиса из Каталога бизнес‑решений; правки описания query-параметра `fromDate` (без изменения контракта)
- Товары: в ответах/моделях остатков изменена семантика массива — теперь «массив ID размеров (chrtId) и их остатков» вместо «баркодов и остатков»; удалены deprecated-поля/параметры, связанные с баркодами: `sku` (в элементах массива) и `skus` (массив баркодов) — ранее помечались как отключаемые 9 февраля; в компонентной модели добавлено поле `chrtId` (ID размера товара) рядом с `sku` и `amount`; уточнено описание `detail` для Payment Required
- Заказы FBS: уточнено описание `detail` для ошибки Payment Required (недостаточно средств на балансе сервиса)
- Заказы DBW: в ответе со стикером поле `file` больше не имеет `format: byte` (остается `string` с base64); пример `phone` приведён к строке (в кавычках); уточнено описание `detail` для Payment Required
- Заказы DBS: в ответе со стикером поле `file` больше не имеет `format: byte` (остается `string` с base64); изменён пример ошибки `SGTINIsNotFilled` — `code` теперь строковый (`SGTINIsNotFilled`), `message` пустая строка (вместо `code: 409`, `message: SGTINIsNotFilled`); уточнено описание `detail` для Payment Required
- Заказы FBW: удалена модель `models.AcceptanceCoefficient` и связанные примеры/ответы (`ResponseCoefficients`, `Response400CoefficientsNew`) — из спецификации исключено описание структуры коэффициентов приёмки; уточнено описание `detail` для Payment Required
- Продвижение: для query-параметра `status` убран фиксированный `enum` (остался `string`, пример `-1,4,8`); параметр `promotionIDs` изменён с `string` на `array<integer>`; уточнено описание `detail` для Payment Required
- Коммуникации: уточнено описание `detail` для ошибки Payment Required
- Тарифы: уточнено описание `detail` для ошибки Payment Required
- Аналитика: уточнено описание `detail` для ошибки Payment Required
- Отчёты: правки описаний query-параметров (перенос `description` на уровень параметра) без изменения контракта; уточнено описание `detail` для Payment Required
- Финансы: правки описаний query-параметров (перенос `description` на уровень параметра) без изменения контракта; уточнено описание `detail` для Payment Required
- WBD: поле `path` (список `id`) — заменено `x-nullable: true` на стандартное `nullable: true` (контракт по nullable сохранён)

### Changed (2026.03.05)
- Управление пользователями продавца: для методов `/api/v1/invite` (POST), `/api/v1/users` (GET), `/api/v1/users` (PUT), `/api/v1/users` (DELETE) явно задан тип токена `x-token-types: [personal]` и обновлено описание авторизации (методы доступны только по персональному токену)
- Общие изменения: добавлен новый тип ошибки `402 Payment Required` (components/responses/402, `application/problem+json` с полями `title`, `detail`); `402` добавлен в ответы ряда методов (в т.ч. в 01-general.yaml)
- Products: для множества методов добавлен ответ `402 Payment Required` (ссылка на `#/components/responses/402`), добавлено описание/схема ошибки `402` в components
- Orders FBS: для всех основных методов добавлен ответ `402 Payment Required`, добавлено описание/схема ошибки `402` в components
- Orders DBW: для всех основных методов добавлен ответ `402 Payment Required`, добавлено описание/схема ошибки `402` в components
- Orders DBS: добавлен ответ `402 Payment Required` для методов; для метода получения стикеров для сборочных заданий с доставкой в ПВЗ добавлен `x-token-types: [personal, service]` и обновлён блок описания авторизации (без изменения доступных типов токенов)
- In-store pickup: для методов добавлен ответ `402 Payment Required`, добавлено описание/схема ошибки `402` в components
- Orders FBW: для методов добавлен ответ `402 Payment Required`, добавлено описание/схема ошибки `402` в components
- Promotion: для методов календаря промо добавлен ответ `402 Payment Required`, добавлено описание/схема ошибки `402` в components
- Communications: для методов добавлен ответ `402 Payment Required`; для `/api/v1/seller/download/{id}` дополнительно явно добавлены ответы `401/402/429` (ранее отсутствовали в описании); добавлено описание/схема ошибки `402` в components
- Tariffs: для методов добавлен ответ `402 Payment Required`, добавлено описание/схема ошибки `402` в components
- Analytics: для методов добавлен ответ `402 Payment Required`, добавлено описание/схема ошибки `402` в components; обновлены примеры данных в одном из CSV-ответов (изменены значения в строках примера)
- Reports: для методов добавлен ответ `402 Payment Required`, добавлено описание/схема ошибки `402` в components
- Finances: для методов добавлен ответ `402 Payment Required`, добавлено описание/схема ошибки `402` в components

### Changed (2026.03.03)
- Orders FBS: в схему поставки добавлено поле `isB2b: boolean|null` — признак B2B-продажи (`true/false/null`, где `null` означает отсутствие признака, т.к. сборочные задания не добавлены к поставке).
- Orders DBS: изменён формат ответа для метода обновления статуса/данных (ранее `$ref api.StatusSetResponses`) — теперь явно описан объект с `requestId` и массивом `results[]` (элементы: `orderId`, `isError`, `errors[] {code, detail}`).
- Orders DBS: добавлен новый тип ошибки `SGTINIsNotFilled` (HTTP 409) и пример ответа; ошибка возвращается, если обязательный код маркировки SGTIN не указан.
- Orders DBS: обновлена документация метода закрепления кодов маркировки — уточнено, что статус должен быть `confirm` («на сборке»).
- Orders DBS: унифицированы значения `errors.detail` — вместо `not found/status conflict` теперь `NotFound/StatusMismatch` (обновлены описание и пример).
- Orders DBS: уточнено описание поля `orderId` в результатах обновления — «с успешно обновлёнными данными» вместо «метаданными».

### Changed (2026.02.27)
- Communications / Возвраты покупателями: в ответе по заявкам добавлены поля `origin_id_info` (nullable, результат сверки IMEI для возврата через ПВЗ WB; применимо к Apple/«Смартфоны» subjectId=515 при цене от 40000 с учётом скидки) и `delivery_dt` (дата/время получения заказа покупателем)
- Reports: для ряда отчётных методов добавлен ответ `204 No Content` с описанием «Нет данных» (когда по запросу отсутствуют данные)

### Changed (2026.02.22)
- Orders DBS: для метода получения стикеров сборочных заданий с доставкой в ПВЗ добавлено явное требование авторизации — использовать персональный и сервисный токены категории «Маркетплейс» (обновлено описание, без изменений в контракте/параметрах).

### Changed (2026.02.20)
- Products: ужесточены лимиты запросов для двух методов раздела — с 100 запросов/мин (интервал 600 мс) до 3 запросов/мин (интервал 20 сек), всплеск без изменений (5 запросов)
- Orders DBS: добавлен новый endpoint `POST /api/marketplace/v3/dbs/orders/stickers` для получения PDF-стикеров (только `type=pdf`, `width=58`, `height=40`; до 100 `orderId` в запросе) для сборочных заданий с доставкой в ПВЗ в статусах `confirm` и `deliver`; ответ содержит `stickers[]` с `orderId`, `partA`, `partB`, `barcode`, `file` (base64)
- Orders DBS: расширен enum `deliveryType` — добавлено значение `dbsPickupPoint` (доставка силами продавца в ПВЗ)
- Orders DBS: уточнено поле `address` в моделях заказов — при доставке в ПВЗ возвращается адрес ПВЗ
- Orders DBS: добавлены поля, специфичные для ПВЗ: `wbStickerId` (ID стикера, только для заказов в ПВЗ) и `scanPrice` (цена приёмки в ПВЗ, в копейках, nullable; только для заказов в ПВЗ)
- Analytics: в CSV-аналитике добавлен новый тип отчёта `STOCK_HISTORY_DAILY_CSV` (схема запроса `InventoryHistoryReportReq`, пример ответа `InventoryHistoryReportRes`) для отчёта по истории остатков по дням
- Analytics: переименована/уточнена модель запроса для `STOCK_HISTORY_REPORT_CSV`: `StocksReportReq` → `InventoryMetricsReportReq`, описание изменено с «истории остатков» на «статистике остатков»; обновлены соответствующие примеры ответа (`StocksReportRes` → `InventoryMetricsReportRes`)
- Analytics: заменён компонент периода `PeriodSt` → `PeriodInv` во всех связанных схемах фильтров остатков
- Analytics: обновлены тексты документации/ограничений: отчёты за период до года привязаны к типам `DETAIL_HISTORY_REPORT` и `GROUPED_HISTORY_REPORT` и доступны только по подписке «Джем»; отчёты по остаткам без подписки — типы `STOCK_HISTORY_REPORT_CSV` и `STOCK_HISTORY_DAILY_CSV`
- Analytics: параметр `skipDeletedNm` переописан как «Скрыть удалённые товары» (вместо «карточки товаров»/«nmID»); уточнены описания `stockType` (приведение к нижнему регистру в тексте) и пример сообщения о старте генерации отчёта (было `Created`, стало «Началось формирование файла/отчета»)

### Changed (2026.02.19)
- Products: в ответах ошибок для метода управления остатками/складом удалены примеры `SubjectDBSRestriction` и `SubjectFBSRestriction`; добавлены новые примеры ошибок `ProductPropertyConflict` (оптовый товар доступен только по схеме DBS) и `DeliveryTypeRestriction` (категория недоступна для выбранного типа доставки, возвращает `data` со `sku/chrtId/amount`).
- Orders FBW (Поставки): удалён (ранее `deprecated`) endpoint `GET /api/v1/acceptance/coefficients` на домене `supplies-api.wildberries.ru` (коэффициенты приёмки; в описании был указан перенос в Tariffs API).

### Changed (2026.02.18)
- Сборочные задания Самовывоз: добавлены batch-эндпоинты смены статуса (POST) с телом `api.OrdersRequestV2(ordersIds[])` и ответом `api.StatusSetResponses`: `/api/marketplace/v3/click-collect/orders/status/confirm` (new→confirm), `/status/prepare` (confirm→prepare), `/status/receive` (prepare→receive), `/status/reject` (prepare→reject), `/status/cancel` (new|confirm|prepare→cancel); лимит для этих методов изменён на 1 запрос/сек (burst 10), при 409 запрос считается за 10
- Сборочные задания Самовывоз: добавлен новый метод получения статусов по списку ID — `POST /api/marketplace/v3/click-collect/orders/status/info` (request `api.OrdersRequestV2`, response `api.OrderStatusesV2`); лимит 1 запрос/сек (burst 10), 409=10 запросов
- Сборочные задания Самовывоз: помечены как устаревшие и запланированы к удалению 19 мая старые single-order методы (PATCH): `/api/v3/click-collect/orders/{orderId}/confirm`, `/prepare`, `/receive`, `/reject`, а также `POST /api/v3/click-collect/orders/status`
- Метаданные Самовывоз: добавлены batch-эндпоинты (POST) — `/api/marketplace/v3/click-collect/orders/meta/info` (получение метаданных, response `api.OrdersMetaResponse`) и `/meta/delete` (удаление метаданных по `key` для списка `ordersIds`, request `api.OrdersMetaDeleteRequest`, response `api.OrdersResponses`); общий лимит для получения/удаления метаданных: 150 запросов/мин (интервал 400 мс, burst 20), 409=10 запросов
- Метаданные Самовывоз: добавлены batch-эндпоинты закрепления метаданных (POST) — `/meta/sgtin` (`api.OrdersSGTINsSetRequest`), `/meta/uin` (`api.OrdersUINSetRequest`), `/meta/imei` (`api.OrdersIMEISetRequest`), `/meta/gtin` (`api.OrdersGTINSetRequest`), ответы `api.MetaSetResponses`; лимит для закрепления метаданных: 20 запросов/мин (интервал 3 сек, burst 500), 409=10 запросов
- Метаданные Самовывоз: помечены как устаревшие и запланированы к удалению 19 мая старые single-order методы: `GET /api/v3/click-collect/orders/{orderId}/meta`, `DELETE /api/v3/click-collect/orders/{orderId}/meta`, `PATCH /api/v3/click-collect/orders/{orderId}/meta/sgtins`, `/meta/uin`, `/meta/imei`, `/meta/gtin`
- Схемы/контракты: добавлены новые модели для batch-операций и ошибок (`api.OrdersRequestV2`, `api.StatusSetResponses`, `api.OrderStatusesV2`, `api.OrdersMetaResponse`, `api.OrdersMetaDeleteRequest`, `api.MetaSetResponses`, `api.BatchError*`, `api.*ErrorResponse`) и новые ответы `IncorrectRequest` и `AccessDeniedBatch` (для batch-методов)
- Схемы/примеры: обновлены примеры `api.GTINRequest`, `api.IMEIRequest`, `api.UINRequest` — значения больше не массивы, а строки (`gtin`, `imei`, `uin`)

### Changed (2026.02.17)
- Самовывоз: в методе обновления IMEI для сборочного задания уточнено ограничение по статусам — теперь IMEI можно добавлять только для заданий в статусе `confirm` (ранее `confirm` и `prepare`) при доставке силами WB
- Самовывоз: описание поля `availableMeta` упрощено — удалено примечание про обязательность IMEI для предмета «Смартфоны» (`subjectId: 515`) и ссылки на связанные методы/разделы

- Коммуникации (Отзывы): в ответах/моделях отзыва добавлено новое поле `orderStatus` со значениями `buyout` / `rejected` / `returned` / `notSpecified`
- Коммуникации (Отзывы): в схеме отзыва скорректирован порядок/расположение полей — `text` и `userName` переразмещены (семантика сохранена: `text` — текст отзыва, `userName` — имя автора, `nullable: false`)
- Коммуникации (Отзывы): обновлены описания перечислений и булевых полей (типографика в `matchingSize`, `isAbleSupplierFeedbackValuation`) без изменения значений/типов

### Changed (2026.02.14)
- Самовывоз: в методе закрепления IMEI за сборочным заданием расширены допустимые статусы задания для добавления IMEI — теперь `confirm` и `prepare` (было только `confirm`); уточнено, что для предмета «Смартфоны» (`subjectId: 515`) указание IMEI обязательно (добавлено в описание списка доступных метаданных).
- Продвижение: для методов получения списков активных/неактивных поисковых кластеров и статистики по кластерам с детализацией по дням добавлены лимиты запросов (соответственно 5 rps, интервал 200 мс, всплеск 10; и 10 rpm, интервал 6 сек, всплеск 20).
- Аналитика: для отчётов «Воронка продаж» и связанных отчётов/таблиц (в т.ч. по поисковым запросам и остаткам) добавлено уточнение, что данные обновляются 1 раз в час; дополнено описание задержек появления данных и правила атрибуции выкупов/отмен/возвратов к дате заказа, с рекомендацией сверять финальные итоги через financial reports.
- Аналитика: в CSV-описании и моделях данных переопределена семантика `cancelCount`/`cancelSum` — теперь это «отменили и вернули» (включая динамики и блок `wbClub.*`); обновлены соответствующие описания в перечислениях полей сортировки/выбора метрик.
- Аналитика: уточнено описание поля `balanceSum` — «сумма остатков на складах на текущий день, шт.» (ранее без привязки ко дню и единицам).

### Changed (2026.02.13)
- Продвижение → Поисковые кластеры: добавлен POST `/adv/v0/normquery/list` — получение списков активных и неактивных поисковых кластеров (только кластеры с ≥100 показов); запрос `items[]` (max 100) с `advertId`, `nmId`, ответ `normQueries.active[]`/`normQueries.excluded[]` (оба nullable).
- Продвижение → Статистика: добавлен POST `/adv/v1/normquery/stats` — статистика по поисковым кластерам за период с детализацией по дням; запрос `from`, `to` (date) + `items[]` (max 100) с `advertId`, `nmId`, ответ `dailyStats[]` с `date` и метриками (`views`, `clicks`, `atbs`, `orders`, `ctr`, `cpc`, `cpm`, `avgPos`, `shks`, `spend`, `normQuery`).
- Продвижение → Статистика поисковых кластеров (существующий метод): уточнено описание — «метод формирует статистику…» вместо «возвращает статистику…».
- Продвижение → Статистика: в схеме статистики по поисковым кластерам добавлены поля `shks` (кол-во заказанных товаров, шт.) и `spend` (затраты на продвижение в кластере).

### Changed (2026.02.12)
- Orders FBS: поле `scanPrice` (number, uint32) помечено как `nullable: true` — теперь может возвращаться `null` до фактической приёмки заказа.

### Changed (2026.02.11)
- Продвижение / Кампании: удалены устаревшие методы получения информации о кампаниях `/adv/v1/promotion/adverts` (POST) и `/adv/v0/auction/adverts` (GET) (ранее помечены deprecated)
- Продвижение / Создание кампаний: удалён устаревший конфиг-метод `/adv/v0/config` (GET)
- Продвижение / Создание кампаний: метод минимальных ставок перенесён и актуализирован — вместо `/adv/v0/bids/min` теперь `/api/advert/v1/bids/min` (POST); уточнено, что значения ставок в копейках; добавлены лимиты: 20 запросов/мин (интервал 3 сек, всплеск 5)
- Продвижение / Управление кампаниями: удалён устаревший метод изменения ставок `/adv/v0/bids` (PATCH)
- Продвижение / Управление кампаниями: удалён устаревший `/adv/v0/auction/bids` (PATCH); актуальный метод — `/api/advert/v1/bids` (PATCH) без deprecated, изменено поле ставки `bid` → `bid_kopecks` (в запросе и ответе), добавлено описание placement (`combined` для unified; `search`/`recommendations` для manual) и лимит: 5 запросов/сек (200 мс, всплеск 5)
- Продвижение / Управление кампаниями: метод изменения списка товаров `/adv/v0/auction/nms` (PATCH) переведён из тега «Параметры кампаний» в «Управление кампаниями» (без изменения пути/логики)
- Продвижение / Параметры кампаний: полностью удалён раздел/тег «Параметры кампаний» и связанные устаревшие методы (фиксированные фразы, минус-фразы, управление nm для unified): `/adv/v1/search/set-plus` (GET/POST), `/adv/v1/search/set-excluded` (POST), `/adv/v1/auto/set-excluded` (POST), `/adv/v1/auto/getnmtoadd` (GET), `/adv/v1/auto/updatenm` (POST)
- Продвижение / Статистика: удалён deprecated-метод `/adv/v2/fullstats` (POST); актуальный `/adv/v3/fullstats` (GET) с лимитом 3 запроса/мин (интервал 20 сек, всплеск 1)
- Продвижение / Статистика: удалены устаревшие методы статистики по фразам/кластерам и ключевым словам: `/adv/v2/auto/stat-words` (GET), `/adv/v1/stat/words` (GET), `/adv/v0/stats/keywords` (GET)
- Продвижение / Схемы: удалены неиспользуемые схемы/примеры, связанные с удалёнными v0/v1 методами (в т.ч. `GetAuctionAdverts`, `V0GetConfigCategoriesResponse`, `V0AdvertMultibid*`, `ResponseInfoAdvertType8` и примеры ошибок для удалённых эндпоинтов)

### Changed (2026.02.07)
- Аналитика
  - Схема `ProductOrdersTextRes`: удалено поле `currency` (и исключено из `required`), теперь валюта не возвращается на уровне объекта ответа
  - CSV-ответы отчётов: в примерах добавлен/восстановлен столбец `Currency` (значение `RUB`) в строках `SalesFunnel*`, `SearchReport*` — ранее встречались строки без валюты

- Отчёты (Основные отчёты)
  - Обновлено описание метода получения заказов: вместо ссылки на метод «Продажи» указано получение продаж через «детализации к отчётам реализации» (`/api/v5/supplier/reportDetailByPeriod`)
  - В описание отчёта добавлено уточнение: в ответах могут отсутствовать заказы без подтверждённой оплаты (отложенные платежи/рассрочка) даже при наличии этих заказов в детализациях к отчётам реализации

### Changed (2026.02.06)
- Аналитика: во все CSV-отчёты добавлено поле валюты — в «Воронке продаж» добавлена колонка `currency`, в отчёте по поиску по артикулам WB добавлена колонка `Currency`, в отчёте по текстам поисковых запросов добавлена колонка `Currency`, в отчёте по истории остатков добавлена колонка `Currency` (обновлены примеры CSV).
- Аналитика: в ответы табличных методов добавлено обязательное поле `currency` (schema `Currency`, пример `RUB`): `TableResponse` (required), `TableDetailsResponse` (required), `TableProductResponse` (required), `ProductSearchTextsResponse` (required), `ProductOrdersTextResponse` (required), `TableGroupsResponse` (required), `TableSizeResponse` (required), `TableShippingOfficeResponse` (required), а также в `ProductHistoryResponse` и `GroupedHistoryResponse` (required на уровне элемента массива).

### Changed (2026.02.04)
- Orders DBS: сокращены единицы времени в таблице rate-лимитов (`1 минута` → `1 мин`, `200 миллисекунд` → `200 мс`).

### Changed (2026.01.31)
- Сборочные задания DBS: добавлен новый readonly-метод `POST /api/marketplace/v3/dbs/orders/b2b/info` для получения B2B-данных покупателя по ID сборочных заданий (ИНН, КПП, наименование организации); лимит: 300 запросов/мин, интервал 200 мс, всплеск 20
- Сборочные задания DBS: изменён путь метода закрепления ГТД — `POST /api/marketplace/v3/dbs/meta/customs-declaration` → `POST /api/marketplace/v3/dbs/orders/meta/customs-declaration` (старый путь фактически удалён/заменён)
- Сборочные задания DBS: для метода ГТД обновлено описание допустимого статуса сборочного задания: `delivery` → `deliver`
- Сборочные задания DBS: для методов закрепления метаданных (в т.ч. ГТД) обновлены лимиты — было 20 запросов/мин (интервал 3 сек, всплеск 500), стало 500 запросов/мин (интервал 120 мс, всплеск 20)
- Сборочные задания DBS: добавлены схемы ответов для B2B-информации `api.B2bClientInfoResponses`, `api.B2bClientInfoResponse`, `api.B2bClientInfo` (batch-результаты по `orderId` с `isError`, `errors` и `data`)

### Changed (2026.01.30)
- Orders FBS: Уточнена логика добавления сборочных заданий в пустую поставку — допускаются задания любого типа (кроссбордер/не кроссбордер), тип поставки фиксируется по первому добавленному заданию (`crossBorderType`), далее можно добавлять только задания того же типа.
- Orders FBS: Добавлено поле `crossBorderType` (int32, enum `0|1`) для сущностей сборочного задания (не nullable) — признак кроссбордера.
- Orders FBS: Добавлено поле `crossBorderType` (int32, enum `0|1`, nullable) для сущности поставки — тип поставки (возможен `null`, если тип отсутствует).
- Communications: Для query-параметров фильтрации по наличию ответа/обработанности добавлены явные значения по умолчанию `default: true` (ранее только в описании).
- Communications: В примере ответа удалено поле `size` из объекта товара.
- Communications: Уточнены часовые пояса для полей дат `dt` и `dt_update` — теперь явно указано `UTC+3`.
- Communications: Для параметров пагинации `limit` и `offset` добавлены явные `default` (50 и 0 соответственно); описание больше не содержит текст “по умолчанию …”.
- Reports: Уточнено ожидаемое максимальное количество строк в выгрузке при `flag=0` — “примерно 80000” вместо “примерно 100000”.
- Finances: Расширен enum `report_type`: добавлены значения `3` и `4` (отчёты для уведомления о выкупе для Грузии); обновлено описание типов отчёта.

### Changed (2026.01.29)
- Все API: сокращены единицы измерения времени в таблицах rate-лимитов (минута → мин, секунда → сек, миллисекунд → мс) — изменения без влияния на функциональность

### Changed (2026.01.28)
- Products: в примерах запросов для выгрузки карточек (/content/v2/get/cards/list) и карточек из корзины (/content/v2/get/cards/trash) добавлена поддержка сортировки `"sort":{"ascending":true}` для инкрементальной выгрузки (получение только новых/обновлённых или недавно перемещённых в корзину по сохранённому `cursor.updatedAt|trashedAt` + `cursor.nmID`)
- Products: ужесточён rate limit для одного из методов (таблица лимитов в описании): было 50 запросов/мин (интервал 1200 мс), стало 10 запросов/мин (интервал 6 секунд), всплеск без изменений (2); запрос с HTTP 409 по-прежнему считается как 10 запросов
- Products: изменены примеры текстов ошибок в схемах ответов (например, `Response403`/`responseContentError`): `errorText`/`additionalErrors` теперь на английском (“Access denied”, “Error text”) вместо русского
- Orders FBS: в ответе со стикерами изменён тип полей `partA` и `partB` со `string` на `integer` (примеры значений также переведены в числовой формат)
- Communications: поле `statusID` помечено как `deprecated` и будет отключено 10 февраля (ссылка на release notes id=469)
- Reports: удалён (фактически выведен из спецификации) deprecated endpoint `GET /api/v1/analytics/warehouse-measurements` (отчёты “Занижение габаритов упаковки”)
- Reports: в моделях возвратов убран формат `date-time` у полей `completedDt`, `expiredDt`, `readyToReturnDt` (остались строками без явного формата)

### Changed (2026.01.27)
- Общие: для ответов с ошибками 401 (Не авторизован) и 429 (Слишком много запросов) изменён `Content-Type` с `application/json` на `application/problem+json`.
- Products: для ответов с ошибками 401 и 429 изменён `Content-Type` с `application/json` на `application/problem+json`.
- Orders DBW: для ответов с ошибками 401 и 429 изменён `Content-Type` с `application/json` на `application/problem+json`.
- Orders DBS: для ответов с ошибками 401 и 429 изменён `Content-Type` с `application/json` на `application/problem+json`.
- In-store pickup: для ответов с ошибками 401 и 429 изменён `Content-Type` с `application/json` на `application/problem+json`.
- Orders FBW: для ответов с ошибками 401 и 429 изменён `Content-Type` с `application/json` на `application/problem+json`.
- Promotion: для ответов с ошибками 401 и 429 изменён `Content-Type` с `application/json` на `application/problem+json`.
- Communications: для ответов с ошибками 401 и 429 изменён `Content-Type` с `application/json` на `application/problem+json`.
- Tariffs: для ответов с ошибками 401 и 429 изменён `Content-Type` с `application/json` на `application/problem+json`.
- Analytics: для ответов с ошибками 401 и 429 изменён `Content-Type` с `application/json` на `application/problem+json`.
- Reports: для ответов с ошибками 401 и 429 изменён `Content-Type` с `application/json` на `application/problem+json`.
- Finances: для ответов с ошибками 401 и 429 изменён `Content-Type` с `application/json` на `application/problem+json`.

### Changed (2026.01.24)
- Products: уточнено описание `charcType=4` в методе «Характеристики предмета» — теперь явно указано, что число может быть целым или с десятичной дробью
- Products: обновлены ссылки в описании поля «Значения характеристики» (в нескольких местах) — вместо упоминания «Характеристики предмета» текстом добавлена явная ссылка на `GET /content/v2/object/charcs/{subjectId}`
- Products: правки форматирования/типографики в описаниях (`"charcType":1/4` — добавлены пробелы вокруг тире); функциональных изменений API нет

### Changed (2026.01.22)
- Поставки FBS: удалён устаревший endpoint `GET /api/v3/supplies/{supplyId}/orders` (получение сборочных заданий в поставке)
- Поставки FBS: удалена схема `SupplyOrder`, использовавшаяся в ответе `GET /api/v3/supplies/{supplyId}/orders`
- Отчёты (Отчёты об удержаниях): удалён устаревший endpoint `GET /api/v1/analytics/incorrect-attachments` (подмена товара); вместе с ним удалён response `SuccessIncorrectProductsResponse` и пример ошибки `IncorrectDateFrom`
- Отчёты (Отчёты об удержаниях): удалён устаревший endpoint `GET /api/v1/analytics/characteristics-change` (смена характеристик); вместе с ним удалён response `SuccessCharacteristicsTaskResponse`

### Changed (2026.01.21)
- Products: поле `x-category` изменено с массива на строку для эндпоинтов получения карточек и списка карточек в корзине.
- Orders DBS: обновлены rate limits для эндпоинта передачи данных СГ.
- Finances: добавлены поля `uuid_promocode` (ID промокода) и `sale_price_promocode_discount_prc` (скидка за промокод, %).

### Changed (2026.01.20)
- Orders DBS: значительно снижены rate limits для эндпоинтов передачи/удаления статусов и метаданных (с 100 req/min до 1 req/sec); уменьшены лимиты для эндпоинтов получения статусов и метаданных (с 1000 до 500 req/min, с 300 до 150 req/min).
- Communications: поле `clientID` помечено как deprecated и будет отключено 2 февраля.

### Changed (2026.01.17)
- Products/Orders DBW/DBS: исправлено написание «Доступ запрещён» в описаниях ошибок и `AccessDenied`.
- Orders FBS: обновлены ссылки на раздел сборочных заданий и метаданные.
- In-store pickup: актуализирована ссылка на список новых сборочных заданий в описании метаданных.
- Analytics: обновлена ссылка на отчёты по поисковым запросам.

### Changed (2026.01.16)
- Orders FBS: добавлен `customsDeclaration` (номер ГТД) в метаданные, расширены допустимые ключи и добавлен новый endpoint `/api/marketplace/v3/orders/{orderId}/meta/customs-declaration`.
- Communications: в методе подсчета отзывов/вопросов убрано обещание возвращать среднюю оценку.

### Changed (2026.01.15)
- Orders DBS: эндпоинты статусов и метаданных перенесены на `/api/marketplace/v3/...` и работают пачками через `api.OrdersRequestV2`; ответы и ошибки переведены на батч-форматы (`api.OrderStatusesV2`, `api.StatusSetResponses`, `api.BatchError`).
- Reports: уточнены описания отчетов по складам/заказам/продажам (задержки обновления, предварительный характер данных, возможное отсутствие неоплаченных заказов); `priceWithDisc` теперь включает скидку WB Клуба.

### Changed (2026.01.14)
- Finances: добавлены поля скидки лояльности продавца `loyalty_id` и `loyalty_discount`.
- Products: для создания/редактирования карточек и габаритов добавлено предупреждение о синхронизации до 30 минут, когда нельзя менять остатки и цены.
