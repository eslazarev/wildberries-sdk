# wildberries-mcp — MCP-сервер для API продавца Wildberries

<!-- mcp-name: io.github.eslazarev/wildberries-mcp -->

[![PyPI](https://img.shields.io/pypi/v/wildberries-mcp.svg)](https://pypi.org/project/wildberries-mcp/)
[![Python](https://img.shields.io/pypi/pyversions/wildberries-mcp.svg)](https://pypi.org/project/wildberries-mcp/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/eslazarev/wildberries-sdk/blob/main/LICENSE)

`wildberries-mcp` подключает ИИ-агента — Claude, Cursor, VS Code, Codex и любой другой
MCP-клиент — ко всему API продавца Wildberries: товарам и ценам, остаткам, заказам FBS,
DBS и DBW, поставкам FBW, рекламе, отзывам и вопросам, аналитике, отчётам и финансам.

Сервер работает поверх [wildberries-sdk](https://pypi.org/project/wildberries-sdk/) и
выходит вместе с ним. Wildberries меняет спецификации API несколько раз в неделю; после
каждого изменения выходит новая версия SDK и сервера, и новые операции сразу доступны
агенту.

📖 Справочник операций: <https://eslazarev.github.io/wildberries-sdk/> ·
📡 Изменения API: [@wildberries_api_radar](https://t.me/wildberries_api_radar) ·
💻 Исходный код: [GitHub](https://github.com/eslazarev/wildberries-sdk/tree/main/mcp-server)

## Что можно попросить у агента

- «Сколько у меня необработанных отзывов? Покажи последние пять с оценкой ниже четырёх»
- «Какие товары заканчиваются на складах WB?»
- «Выгрузи отчёт о продажах за прошлую неделю и посчитай выручку по артикулам»
- «Какие рекламные кампании сейчас активны и сколько на них потрачено?»
- «Покажи новые сборочные задания FBS»
- «Ответь на свежие вопросы покупателей» — изменяющая операция, клиент спросит подтверждение

Агент сам находит нужную операцию, читает её параметры и вызывает её. Знать пути API и
названия методов не нужно.

## Быстрый старт

1. Установите [uv](https://docs.astral.sh/uv/getting-started/installation/). Он сам скачает
   сервер и Python 3.10+, ставить их вручную не нужно.
2. Создайте токен API в личном кабинете продавца Wildberries. У токена должен быть доступ к
   тем категориям (контент, аналитика, вопросы и отзывы и т. д.), с которыми будет работать
   агент.
3. Подключите сервер к клиенту — команды ниже. Сервер читает токен из переменной
   `WB_API_TOKEN`.
4. Перезапустите клиент или начните новую сессию и спросите агента о своём магазине.

## Подключение к клиентам

### Claude Code

```bash
claude mcp add wildberries --env WB_API_TOKEN=<токен> -- uvx wildberries-mcp
```

С флагом `-s user` сервер будет доступен во всех проектах. Проверка: `claude mcp list`
должен показать `wildberries: uvx wildberries-mcp - ✔ Connected`.

### Claude Desktop, Cursor, Windsurf, Gemini CLI

Все четыре используют один формат. Добавьте сервер в раздел `mcpServers` файла
конфигурации клиента — Claude Desktop: Settings → Developer → Edit Config; Cursor:
`~/.cursor/mcp.json`; Windsurf: `~/.codeium/windsurf/mcp_config.json`; Gemini CLI:
`~/.gemini/settings.json`.

```json
{
  "mcpServers": {
    "wildberries": {
      "command": "uvx",
      "args": ["wildberries-mcp"],
      "env": { "WB_API_TOKEN": "<токен>" }
    }
  }
}
```

### VS Code

Файл `.vscode/mcp.json` в проекте (или команда **MCP: Add Server**):

```json
{
  "servers": {
    "wildberries": {
      "type": "stdio",
      "command": "uvx",
      "args": ["wildberries-mcp"],
      "env": { "WB_API_TOKEN": "<токен>" }
    }
  }
}
```

### Codex CLI

В `~/.codex/config.toml`:

```toml
[mcp_servers.wildberries]
command = "uvx"
args = ["wildberries-mcp"]
env = { WB_API_TOKEN = "<токен>" }
```

### Без uv

```bash
pip install wildberries-mcp      # Python 3.10+
```

В конфигурации клиента укажите команду `wildberries-mcp` без аргументов (или
`python -m wildberries_mcp`) — вместо `uvx` и `["wildberries-mcp"]`.

## Как это устроено

В API Wildberries около трёхсот операций. Если сделать по инструменту на каждую, их схемы
займут контекст агента ещё до первого вопроса, а многие клиенты ограничивают число
инструментов. Поэтому инструментов четыре, и агент работает с ними по шагам:

```
search_operations → describe_operation → call_read_operation   (GET)
                                       → call_write_operation  (POST, PUT, PATCH, DELETE)
```

**1. Поиск.** Агент ищет операцию словами — по-русски или по-английски, — по пути или
по имени метода. Русские слова находятся в любой форме («отзывов» → «Отзывы»), а
распространённые слова связаны с английскими путями: «остатки» находит `/stocks`,
«отзывы» — `/feedbacks`.

```json
search_operations({"query": "неотвеченные отзывы", "limit": 2})

{"operations": [
  {"operation_id": "communications.get_v1_feedbacks_count_unanswered",
   "verb": "GET", "path": "/api/v1/feedbacks/count-unanswered",
   "summary": "Необработанные отзывы", "module": "communications", "read_only": true},
  {"operation_id": "communications.get_v1_feedbacks",
   "verb": "GET", "path": "/api/v1/feedbacks",
   "summary": "Список отзывов", "module": "communications", "read_only": true}
 ],
 "modules": ["analytics", "communications", "..."]}
```

**2. Описание.** Агент получает описание операции из документации Wildberries (вместе с
лимитами запросов), хост, параметры с JSON Schema и ссылку на страницу справочника.

```json
describe_operation({"operation_id": "communications.get_v1_feedbacks"})

{"operation_id": "communications.get_v1_feedbacks", "verb": "GET",
 "path": "/api/v1/feedbacks", "host": "https://feedbacks-api.wildberries.ru",
 "description": "Метод возвращает список отзывов по заданным фильтрам…",
 "parameters": [
   {"name": "is_answered", "in": "query", "required": true, "wire_name": "isAnswered",
    "schema": {"type": "boolean", "description": "Вернуть только обработанные отзывы…"}},
   {"name": "take", "in": "query", "required": true,
    "schema": {"type": "integer", "description": "Количество отзывов (max. 5 000)"}},
   …
 ],
 "docs_url": "https://eslazarev.github.io/wildberries-sdk/reference/communications/get_api_v1_feedbacks/",
 "call_with": "call_read_operation"}
```

**3. Вызов.** Агент передаёт аргументы и получает HTTP-статус и тело ответа Wildberries.

```json
call_read_operation({"operation_id": "communications.get_v1_feedbacks",
                     "arguments": {"isAnswered": false, "take": 5, "skip": 0}})

{"status": 200,
 "body": {"data": {"countUnanswered": 3, "feedbacks": […]}, "error": false},
 "rate_limit": {"X-Ratelimit-Remaining": "2"}}
```

Параметры можно называть так, как в документации Wildberries (`isAnswered`, `nmId`), или
так, как в SDK (`is_answered`, `nm_id`). Значения пути, query и заголовков проверяются по
типам SDK до отправки: агент получает понятную ошибку вместо ответа `400`. Тело запроса
уходит в Wildberries как есть — поле, которого ещё нет в спецификации, не потеряется.

## Инструменты

| Инструмент | Аргументы | Что делает |
| --- | --- | --- |
| `search_operations` | `query`, `module` (необязательно), `limit` (по умолчанию 15, до 100) | ищет операции; пустой `query` с `module` выводит все операции раздела |
| `describe_operation` | `operation_id` | описание, хост, параметры, JSON Schema тела запроса, ссылка на справочник |
| `call_read_operation` | `operation_id`, `arguments` | выполняет GET-операцию |
| `call_write_operation` | `operation_id`, `arguments` | выполняет POST, PUT, PATCH и DELETE |

Каждый инструмент отказывается выполнять операцию не своего типа: GET не пройдёт через
`call_write_operation`, а POST — через `call_read_operation`.

## Разделы API

| `module` | Раздел документации Wildberries |
| --- | --- |
| `general` | Общее: проверка подключения, информация о продавце, рейтинг, новости и уведомления, пользователи кабинета |
| `items` | Работа с товарами: карточки, цены и скидки, остатки, склады продавца |
| `orders_fbs` | Заказы FBS: сборочные задания, поставки, пропуска |
| `orders_dbw` | Заказы DBW |
| `dbs` | DBS — доставка силами продавца |
| `in_store_pickup` | Самовывоз |
| `orders_fbw` | Поставки FBW: черновики и поставки, склады, опции приёмки |
| `promotion` | Маркетинг и продвижение: рекламные кампании, ставки, бюджеты, акции |
| `communications` | Общение с покупателями: отзывы, вопросы, чаты, заявки на возврат |
| `rates` | Тарифы: комиссии по категориям, тарифы для коробов и монопаллет, на поставку и возврат |
| `analytics` | Аналитика и данные: воронка продаж, поисковые запросы, остатки на складах |
| `reports` | Отчёты: продажи, заказы, удержания, самовыкупы, маркировка, замеры склада |
| `finances` | Документы и бухгалтерия: баланс, отчёты реализации, документы |

Полный список операций с параметрами и примерами — в
[справочнике](https://eslazarev.github.io/wildberries-sdk/).

## Чтение и изменение данных

Меньше половины операций — GET, они только читают данные. Остальные идут через
`call_write_operation`: они меняют цены и скидки, остатки, карточки товаров, рекламные
кампании и бюджеты, статусы заказов, публикуют ответы покупателям. У этого инструмента
стоят аннотации MCP `destructiveHint` и `idempotentHint: false`: клиенты, которые их
учитывают, спрашивают подтверждение перед каждым вызовом. Читайте, что агент собирается отправить, прежде чем соглашаться.

Часть отчётов и списков в API Wildberries тоже сделана через POST — например, отчёты об
остатках и воронка продаж. Они проходят через `call_write_operation`, хотя ничего не
меняют, поэтому клиент спросит подтверждение и для них.

## Лимиты запросов

Wildberries ограничивает частоту запросов отдельно для каждой категории методов; лимиты
каждой операции перечислены в её описании, которое агент получает из
`describe_operation`. Вместе с ответом сервер передаёт агенту заголовки `X-Ratelimit-*` и
`Retry-After`, если Wildberries их прислал. После ответа `429` агент видит, сколько
ждать, и может повторить запрос.

## Настройки

| Переменная | По умолчанию | Назначение |
| --- | --- | --- |
| `WB_API_TOKEN` | — | токен API продавца; без него поиск и описание работают, а вызовы — нет |
| `WB_MCP_MAX_RESPONSE_CHARS` | `60000` | ответ длиннее обрезается, и агент получает подсказку сузить запрос фильтрами и пагинацией |

## Частые проблемы

| Что видит агент | Причина и что делать |
| --- | --- |
| `WB_API_TOKEN is not set` | переменная не попала в окружение сервера: проверьте блок `env` в конфигурации клиента и перезапустите клиент |
| `401` и `token is expired` | срок токена истёк — создайте новый в личном кабинете и замените его в конфигурации |
| `401` на одних разделах при `200` на других | у токена нет доступа к категории этой операции — выпустите токен с нужными категориями |
| `429 Too Many Requests` | превышен лимит категории; подождите столько, сколько указано в заголовках ответа |
| `Network error reaching Wildberries … Failed to resolve` | DNS-сервер сети не знает хост Wildberries (так бывает с роутерами); проверьте `nslookup <хост>` или смените DNS |
| `response cut at … characters` | ответ слишком большой — попросите агента взять меньше записей за раз или увеличьте `WB_MCP_MAX_RESPONSE_CHARS` |
| `file uploads are not supported through MCP` | файлы через сервер не передаются — загрузку медиафайла карточки и отправку файла в чат делайте через SDK напрямую |
| сервер не появляется в клиенте | убедитесь, что `uvx` есть в `PATH` того окружения, из которого клиент запускает серверы; при необходимости укажите полный путь к `uvx` |

## Версии

Версия сервера совпадает с версией `wildberries-sdk`, и каждый выпуск зависит ровно от
своей версии SDK. `uvx wildberries-mcp` берёт последнюю версию; чтобы зафиксировать
конкретную, укажите `uvx wildberries-mcp==<версия>`. Что изменилось в API — в
[CHANGELOG](https://github.com/eslazarev/wildberries-sdk/blob/main/CHANGELOG.md) и в
Telegram-канале [@wildberries_api_radar](https://t.me/wildberries_api_radar).

Ошибки и предложения — в [issues](https://github.com/eslazarev/wildberries-sdk/issues).

## In English

`wildberries-mcp` is an MCP server that gives AI agents (Claude, Cursor, VS Code, Codex
and other MCP clients) access to every operation of the Wildberries seller API through
[wildberries-sdk](https://pypi.org/project/wildberries-sdk/). It exposes four tools —
`search_operations`, `describe_operation`, `call_read_operation` and
`call_write_operation` — instead of one tool per operation, so a few hundred schemas do
not fill the agent's context. Write operations are annotated as destructive, and clients
that honour MCP annotations ask before running them. The server is released together
with the SDK, so new operations reach the agent as soon as Wildberries publishes them.

```bash
claude mcp add wildberries --env WB_API_TOKEN=<token> -- uvx wildberries-mcp
```

The server reads the seller's API token from `WB_API_TOKEN`. Operation summaries are in
Russian; search accepts Russian and English words, paths and method names. Reference:
<https://eslazarev.github.io/wildberries-sdk/>.

## Лицензия

MIT
