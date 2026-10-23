# PHP

```bash
composer require eslazarev/wildberries-sdk
```

```php
<?php
use Wildberries\Sdk\Finances\Api\DefaultApi;
use Wildberries\Sdk\Finances\Configuration;

$config = Configuration::getDefaultConfiguration()
    ->setApiKey('Authorization', getenv('WB_API_TOKEN'))
    ->setHost('https://finance-api.wildberries.ru');   // required — see below

$api = new DefaultApi(new GuzzleHttp\Client(), $config);
$balance = $api->getV1AccountBalance();
```

The fully qualified class is on the digest's `php:` line.

## Host: you must set it

`Configuration` defaults to `http://localhost`. The real host only appears in
the method's docblock, so take it from the digest's `host:` line and call
`setHost()`. Build a separate `Configuration` per host when a task spans
services.

## Errors

`ApiException` carries `getCode()` (the HTTP status) and
`getResponseBody()`. Treat 429 as a rate limit and back off; 401 and 403 point
at the token category rather than the code.

## Shapes

Methods are camelCase and return generated model objects with getters
(`$balance->getData()->getCurrent()`). Each method has a `…WithHttpInfo`
variant when the status code or headers are needed.
