# wildberries-mcp — MCP-сервер для API Wildberries

<!-- mcp-name: io.github.eslazarev/wildberries-mcp -->

MCP-сервер даёт ИИ-агенту (Claude, Cursor, VS Code и другим MCP-клиентам) доступ ко
всем операциям API продавца Wildberries. Работает поверх
[wildberries-sdk](https://pypi.org/project/wildberries-sdk/) и выходит вместе с ним:
когда Wildberries меняет спецификацию, новая операция появляется и в сервере.

📖 Справочник операций: <https://eslazarev.github.io/wildberries-sdk/> ·
📡 Изменения API: [@wildberries_api_radar](https://t.me/wildberries_api_radar)

## Подключение

Нужен [uv](https://docs.astral.sh/uv/) — он сам скачает сервер и Python 3.10+.
`WB_API_TOKEN` — токен API из личного кабинета продавца.

**Claude Code**

```bash
claude mcp add wildberries --env WB_API_TOKEN=<токен> -- uvx wildberries-mcp
```

**Claude Desktop, Cursor, VS Code и другие** — в конфигурации MCP-серверов клиента:

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

## Инструменты

Вместо сотен инструментов — по одному на операцию — сервер даёт четыре. Агент находит
нужную операцию, читает её параметры и вызывает:

| Инструмент | Что делает |
| --- | --- |
| `search_operations` | ищет операции по словам на русском или английском, по пути или имени метода: «неотвеченные отзывы», `/api/v3/orders/new` |
| `describe_operation` | параметры, JSON Schema тела запроса, хост, лимиты и ссылку на справочник |
| `call_read_operation` | выполняет GET-операцию |
| `call_write_operation` | выполняет POST, PUT, PATCH и DELETE |

Изменяющие операции — цены, остатки, карточки, кампании, ответы покупателям —
вызываются отдельным инструментом с пометкой `destructiveHint`. Клиенты, которые
учитывают аннотации MCP, спрашивают подтверждение перед таким вызовом. Часть отчётов и списков у Wildberries тоже
POST, поэтому они проходят через тот же инструмент.

Параметры можно называть так, как в документации Wildberries (`isAnswered`), или так,
как в SDK (`is_answered`). Тело запроса уходит в Wildberries как есть.

## Настройки

| Переменная | По умолчанию | Назначение |
| --- | --- | --- |
| `WB_API_TOKEN` | — | токен API продавца, нужен для вызова операций |
| `WB_MCP_MAX_RESPONSE_CHARS` | `60000` | длиннее ответ обрезается; сузьте его фильтрами и пагинацией |

Wildberries ограничивает частоту запросов. Вместе с ответом сервер передаёт агенту
заголовки `X-Ratelimit-*`, если Wildberries их прислал: после `429` по ним видно,
сколько ждать.
