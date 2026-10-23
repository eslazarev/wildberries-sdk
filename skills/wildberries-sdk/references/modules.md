# Modules

One module per Wildberries spec area. The digest's `python:` line names the
module an operation belongs to; this table is for the other direction — you
know what the user wants, you need the module.

Operation counts move every week, so treat them as a sense of size, not a
contract. Hosts are what the clients actually call; the dominant one is listed
first and the digest's `host:` line is authoritative per operation.

| Module | Ops | What lives here | Main hosts |
| --- | --- | --- | --- |
| `items` | ~55 | Product cards, characteristics, media, categories, barcodes, prices and discounts, warehouse stocks | content-api, discounts-prices-api, marketplace-api |
| `orders_fbs` | ~48 | FBS orders: assembly tasks, supplies, labels, statuses, cancellations (продажа со склада продавца) | marketplace-api |
| `promotion` | ~42 | Advertising campaigns, bids, budgets, statistics, media campaigns, promo calendar | advert-api, advert-media-api, dp-calendar-api |
| `communications` | ~25 | Buyer feedback and questions, chat with the buyer, returns handling | feedbacks-api, buyer-chat-api, returns-api |
| `reports` | ~24 | Sales, stock and detail reports, paid storage and acceptance | seller-analytics-api, statistics-api |
| `wbd` | ~22 | Wildberries Digital — digital goods | devapi-digital |
| `dbs` | ~21 | DBS orders: delivery by the seller | marketplace-api |
| `orders_dbs` | ~20 | The older DBS order surface, kept while WB migrates | marketplace-api |
| `analytics` | ~20 | Seller analytics: funnels, search reports, brand share, hidden products | seller-analytics-api |
| `in_store_pickup` | ~18 | Orders picked up in the seller's own store | marketplace-api |
| `orders_dbw` | ~16 | DBW orders: delivery by Wildberries from the seller's warehouse | marketplace-api |
| `orders_fbw` | ~14 | FBW supplies into WB warehouses: coefficients, slots, acceptance | supplies-api |
| `finances` | ~11 | Balance, financial reports, accounting documents | finance-api, documents-api |
| `general` | ~10 | Ping, seller info, users and access, news, subscriptions | common-api, user-management-api |
| `rates` | ~5 | Logistics, storage and commission tariffs | common-api |

## Choosing between the order modules

WB splits orders by fulfilment scheme, and the names are easy to confuse:

- **FBS** (`orders_fbs`) — goods sit in the seller's warehouse, WB delivers.
  The busiest module: assembly tasks, supplies, stickers, статусы.
- **FBW** (`orders_fbw`) — goods are shipped into a WB warehouse first. This
  module is about supplies and acceptance slots, not individual orders.
- **DBS** (`dbs`, and the legacy `orders_dbs`) — the seller delivers to the
  buyer. Prefer `dbs` for new code.
- **DBW** (`orders_dbw`) — WB delivers from the seller's warehouse under a
  separate contract.
- **In-store pickup** (`in_store_pickup`) — the buyer collects from the
  seller's own point.

If the user just says "заказы" without a scheme, ask which one they sell
under rather than guessing — the endpoints are not interchangeable.

## Install names

| Module | Python / Node | Go | Rust |
| --- | --- | --- | --- |
| any | `wildberries-sdk` (all modules in one package) | `github.com/eslazarev/wildberries-sdk/clients/go/<module>` | `wildberries_sdk_<module>` |

PHP ships every module in `eslazarev/wildberries-sdk` under
`Wildberries\Sdk\<Module>\`.
