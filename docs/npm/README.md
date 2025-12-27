# wildberries-sdk (npm)

Единый npm-пакет с клиентами Wildberries по всем спецификациям.

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
