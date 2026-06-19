# Scrape Usage Diagnostic
**Date:** 2026-06-19  
**Source:** `server.py` code audit — no runtime data, static analysis only

---

## 1. Fallback Chain Logic

All scraping goes through `fetch_url()`. The chain per request:

```
fetch_url(url, render_js=False)
  → ScraperAPI (1 credit)         ← primary
  → Zyte httpResponseBody          ← fallback (NOT for Amazon)
  → Direct HTTP                    ← last resort

fetch_url(url, render_js=True)
  → ScraperAPI + render=true (5 credits)     ← primary
  → Zyte httpResponseBody                     ← fallback (NOT for Amazon)
  → Direct HTTP                               ← last resort

fetch_url(amazon_url, render_js=True)        ← Amazon path
  → ScraperAPI + render=true + premium=true (25 credits)   ← primary
  [Zyte is SKIPPED — `if ZYTE_API_KEY and not is_amazon`]
  → Direct HTTP                               ← last resort
```

**Trigger conditions for fallback:**
- ScraperAPI fails → HTTP status ≠ 200, or exception (timeout, connection error)
- Zyte fails → HTTP status ≠ 200, or exception
- Each fallback is automatic and silent — no circuit breaker

### Per-shop actual chain used

| Shop | Direct first? | ScraperAPI tier | Zyte fallback? |
|---|---|---|---|
| **Elesen.lt** | ✅ 2s direct attempt | render_js=True (5 cr) | ✅ Yes |
| **Amazon.DE** | ❌ No | render_js + premium (25 cr) | ❌ **Skipped** |
| **Amazon.PL** | ❌ No | render_js + premium (25 cr) | ❌ **Skipped** |
| Varle.lt (inactive) | ✅ 2s direct | render_js=True (5 cr) | ✅ Yes |

---

## 2. Zyte: Primary or Fallback?

**Zyte is always fallback — never primary.** It fires only when ScraperAPI returns non-200 or throws.

**Critical finding: Zyte is explicitly SKIPPED for Amazon** (`if ZYTE_API_KEY and not is_amazon`).

The `cache_stats()` endpoint has a **stale cost comment**:
```python
# Amazon: 2 × $0.0075 Zyte browserHtml  = $0.01500   ← WRONG, Amazon never uses Zyte
# LT shops: 6 × $0.00049 ScraperAPI = $0.00294       ← WRONG shop count, only 1 active (Elesen)
```
This cost model is outdated and misleading — do not rely on it.

**When Zyte fires in practice:**
- Render's US IP gets Cloudflare-blocked on LT shops (elesen.lt, varle.lt, etc.)
- ScraperAPI fails/is rate-limited → all LT shop requests fall through to Zyte
- Each Zyte `httpResponseBody` call = 1 Zyte credit

---

## 3. Credit Waste from Retries

This is the most likely explanation for high Zyte/ScraperAPI usage.

### Amazon internal retry (always active)

```python
# scrape_amazon() — when 0 items parsed and not bot-blocked:
short_q = _short_amazon_query(query)  # strip filler, cap 3 words
if short_q != query:
    retry_resp = fetch_url(retry_url, lang, render_js=True, scraper_timeout=18)
    # ↑ Another 25 ScraperAPI premium credits
```

**2 Amazon domains × 25 premium credits × potentially 2 attempts (original + short_q retry) = up to 100 premium credits per search.**

### `_model_code_variants` outer retry (added 2026-06-19)

```python
# When all_results == 0 after main search:
for _vq in _model_code_variants(query)[1:]:   # up to 2 variants
    _re.submit(scrape_amazon, _vq_de, "de")   # → 25 premium credits each
    _re.submit(scrape_amazon, _vq_pl, "pl")   # → 25 premium credits each
```

**Worst case for 0-result query with 2 model variants:**
```
Main search:
  Amazon.DE primary:    25 cr
  Amazon.DE short_q:    25 cr (internal retry)
  Amazon.PL primary:    25 cr
  Amazon.PL short_q:    25 cr (internal retry)
  = 100 premium cr

Outer retry variant 1:
  Amazon.DE primary:    25 cr
  Amazon.DE short_q:    25 cr
  Amazon.PL primary:    25 cr
  Amazon.PL short_q:    25 cr
  = 100 premium cr

Outer retry variant 2 (if variant 1 also 0):
  = 100 more premium cr

Total worst case: 300 premium ScraperAPI credits for ONE failed scan
```

**At ScraperAPI pricing: 300 premium credits ≈ $0.09 per failed scan.** If 100 users/day hit 0-result queries: ~$9/day in failed scans alone.

### Scan-image double cost

`/api/scan-image` runs its own full parallel search (not cached by the same key as `/api/search`). If the same product is scanned and then also searched manually, **both searches hit ScraperAPI separately** — the scan_v66 cache key is different from the v64 search key.

---

## 4. Credit/Usage Tracking

### What exists

- `cache_stats()` at `/api/cache-stats` (debug key required):
  - Cache hit/miss count
  - Estimated cost based on `cost_per_miss × misses` — but formula uses **wrong shop count and wrong Zyte model**
  - Top 5 most-searched queries
  - Live cache sample (20 entries)

- Per-request logs to stdout: `[ScraperAPI OK]`, `[Zyte OK]`, `[Direct 200]`

### What does NOT exist

| Missing tracking | Impact |
|---|---|
| No ScraperAPI credit balance polling | Cannot alert before credits run out |
| No per-API call counter (ScraperAPI vs Zyte vs Direct) | Cannot see which API is actually being used |
| No retry event counter | Cannot see how often double/triple Amazon calls happen |
| No Zyte credit balance check | Cannot alert before Zyte runs out |
| No daily cost accumulator | Cost estimate resets on every Render restart |
| No alert threshold | No notification when spending spikes |

---

## 5. Cache

| Property | Value |
|---|---|
| Type | In-memory dict (`cache = {}`) |
| Max entries | 500 (configurable via `CACHE_MAX_ENTRIES` env var) |
| Eviction | LRU — oldest 10% evicted when full |
| TTL — regular | 30 min (`CACHE_TTL_SECONDS`, default 1800s) |
| TTL — popular (≥5 searches) | 2 hours (`POPULAR_CACHE_TTL`, default 7200s) |
| Persistence | ❌ None — lost on every Render restart/deploy |
| 0-result caching | ❌ Skipped — `set_cache` bails if no results |
| `/api/scan-image` vs `/api/search` | ❌ **Different cache keys** — same product scanned and searched costs 2× |
| Translation cache | ✅ In-memory, same process, evicts at 1000 entries |

**Consequence of no persistence:** Every Render cold start (deploy, scale-to-zero, crash) resets the cache. Popular products during early traffic → all fresh scrapes → sudden credit spike after each deploy.

---

## Top Recommendations to Reduce Scrape Costs

### #1 — Cap Amazon retry to 1 level (saves up to 50 credits/search)
The outer `_model_code_variants` retry calls `scrape_amazon` which internally may also retry with `_short_amazon_query`. This double-retry is unintended and expensive. **Options:**
- Pass a `_no_internal_retry=True` flag to `scrape_amazon` when calling from the outer retry
- Or: make outer retry use `_short_amazon_query(query)` directly instead of full `scrape_amazon`

**Saves:** 25-50 premium credits per 0-result scan. **Priority: P1**

### #2 — Unified cache key for scan + search (saves 50% of Amazon calls)
`scan_v66:{query}:{code}:{lang}` ≠ `v64:{query}:{lang}`. If a user scans a product and then searches the same query within 30 min, they pay twice. **Fix:** after scan-image identifies the product, use the same cache key as `/api/search` would — or check the v64 cache before running scan shops.

**Saves:** ~50% of Amazon premium credits for users who scan then compare. **Priority: P1**

### #3 — Add credit counter + alert
Add a simple in-memory counter: `_scraper_calls = {"scraperapi_premium": 0, "scraperapi_render": 0, "zyte": 0}`. Increment in `fetch_url()`. Expose in `cache_stats()`. Set a daily threshold and log a warning when exceeded.

**Saves:** Not direct savings, but prevents surprise billing. **Priority: P2**

### #4 — Persist cache to Supabase for popular queries
The `save_prices_to_supabase` function already stores results. Add a `get_price_history`-style lookup that returns last-hour results as a "soft cache" — if Supabase has results from the last 30 min for this query, skip scraping. This survives Render restarts.

**Saves:** Eliminates cold-start credit spikes after deploys. **Priority: P2**

### #5 — Circuit breaker for Amazon when bot-blocked
When Amazon returns CAPTCHA (`_bot_blocked = True`), the scraper logs it and skips the internal retry. But the outer `_model_code_variants` retry still attempts Amazon again (doesn't know it was blocked). **Fix:** set a short-lived `_amz_blocked` flag so outer retries skip Amazon when blocked.

**Saves:** 50-100 credits per blocked session. **Priority: P2**
