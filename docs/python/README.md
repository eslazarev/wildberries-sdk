# wildberries-sdk (Python)

## Установка

```bash
pip install wildberries-sdk
```

## Пример (communications)

```python
import os

from wildberries_sdk import communications

token = os.getenv("WB_API_TOKEN")

config = communications.Configuration(host="https://feedbacks-api.wildberries.ru")
config.api_key["HeaderApiKey"] = token

client = communications.ApiClient(configuration=config)
api = communications.DefaultApi(api_client=client)

response = api.api_v1_feedbacks_get(
    is_answered=True,
    take=100,
    skip=0,
)

print(response)
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
