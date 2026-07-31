# Intent Events — Schema & Payload Reference

## Table: `intent_events`

Append-only event log. No UPDATEs or DELETEs from application code.

| Column | Type | Notes |
|---|---|---|
| `id` | bigint identity | Auto PK |
| `event_type` | text | One of the types below |
| `anonymous_user_id` | uuid | From `localStorage('goody_uid')` — not personal data |
| `session_id` | uuid | From `sessionStorage('goody_sid')` — new each tab/session |
| `product_canonical` | text | Normalised product key (brand:model or query slug), null for non-product events |
| `payload` | jsonb | Type-specific fields (see below) |
| `is_internal` | boolean | True when request carries `X-Goody-Internal` header with valid token |
| `created_at` | timestamptz | Server-side UTC timestamp |

## Event Types & Payload Schemas

### `search`
Fired when a search is initiated.
```json
{
  "query_raw": "Samsung Galaxy S24",
  "method": "text",
  "language": "lt"
}
```
- `method`: `"text"` | `"photo"` | `"barcode"`

### `results_shown`
Fired when all scrapers have responded or timed out (complete, non-partial).
```json
{
  "offers_count": 4,
  "min_price": 849.00,
  "max_price": 999.00,
  "price_spread_pct": 15,
  "stores_responded": ["Amazon.DE", "Varle.lt"],
  "stores_failed": [],
  "search_duration_ms": 3200
}
```

### `offer_click`
Fired when the user taps "Pirkti →" or "Peržiūrėti →".
```json
{
  "store": "Amazon.DE",
  "price": 849.00,
  "position_in_list": 0,
  "is_cheapest": true,
  "sort_mode": "cheapest"
}
```

### `save_product`
Fired when the user adds a product to the watchlist.
```json
{
  "source_screen": "results"
}
```

### `set_alert`
Fired when the user sets a target-price alert (toggleWatch with a target).
```json
{
  "target_price": 800.00,
  "current_min_price": 849.00
}
```

### `return_visit`
Fired when the user opens a product they already searched for (>1 day ago).
```json
{
  "days_since_last_seen": 3
}
```

### `no_click`
Fired when the results screen was shown but no offer was clicked within ≥8 seconds.
```json
{
  "offers_count": 4,
  "min_price": 849.00,
  "seconds_on_screen": 12
}
```

## Internal Mode

Set `localStorage.setItem('goody_internal', '1')` in the browser console to tag
all your events with `is_internal=true`. Internal events are excluded from all
admin analytics queries.

## Admin Summary Endpoint

`GET /api/admin/intent-summary?token=<ADMIN_SUMMARY_TOKEN>&days=7`

Returns: top products, funnel conversion, no-click products, method breakdown, alert prices.
