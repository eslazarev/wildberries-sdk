# Wildberries SDK

Сгенерированные SDK-клиенты для API Wildberries на **Python, Node.js, Go, PHP и Rust**,
постоянно синхронизируемые с официальными OpenAPI-спецификациями.

<a href="https://deepwiki.com/eslazarev/wildberries-sdk" target="_blank" rel="noopener"><img src="https://deepwiki.com/badge.svg" alt="Спроси DeepWiki об этом репо"></a>

📡 Изменения API — в Telegram-канале [@wildberries_api_radar](https://t.me/wildberries_api_radar): пост о каждом обновлении спецификаций Wildberries. Для RSS-ридеров есть [Atom-лента](changelog.xml).

Этот сайт — справочник по **всем операциям API**. Для каждой операции указаны HTTP-метод
и путь, параметры, модели запроса и ответа, а также пример вызова на всех пяти языках.

- [Начало работы](getting-started.md) — установка клиента для вашего языка.
- **Справочник API** — операции, сгруппированные по модулям спецификаций (меню слева).

## Для ИИ-агентов

Навык для Claude Code ставится одной командой:

```
/plugin install wildberries-sdk --marketplace eslazarev/wildberries-sdk
```

После установки агент сам находит нужную операцию, подбирает модуль, категорию токена
и хост и пишет вызов, который действительно работает — вместо того чтобы угадывать
имена методов.

Агентам без Claude Code пригодится машиночитаемый перечень операций:
[llms.txt](llms.txt) — краткий индекс сайта, [llms-full.txt](llms-full.txt) — полный
дайджест с маршрутом, хостом, песочницей, обязательными параметрами и именем метода
в каждом из пяти клиентов. В репозитории для них же лежит
[AGENTS.md](https://github.com/eslazarev/wildberries-sdk/blob/main/AGENTS.md).

Исходный код и пакеты: [github.com/eslazarev/wildberries-sdk](https://github.com/eslazarev/wildberries-sdk).
