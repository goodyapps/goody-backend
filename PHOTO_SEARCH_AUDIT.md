# Photo → Search Pipeline Quality Audit
**Date:** 2026-06-19  
**Audited by:** Claude Code (automated audit)  
**Scope:** `server.py` — `/api/identify-product` + `/api/scan-image` + `/api/search` pipeline

---

## Pipeline Overview

```
Photo → /api/identify-product → search_query → /api/search → results
   OR
Photo → /api/scan-image (identify + search in one call) → results
```

Two separate endpoint paths exist with **different query-building logic** — this is the most important structural finding (see §2).

---

## 1. IMAGE ANALYSIS

### Vision Prompt (exact, as sent to Claude Haiku and Gemini 2.0 Flash)

```
You are a product identification assistant for a price comparison app.
The image may be: a physical product label, product packaging, a photo of a shop shelf, OR a screenshot/photo of a webpage or price comparison site.
In ALL cases extract the product name and brand from any visible text.

Respond ONLY with valid JSON (no markdown, no explanation):
{"brand":"","product_name":"","model":"","key_specs":"","search_query":"","confidence":"high|medium|low","scanned_price":null}

- brand: manufacturer name (e.g. "Mobvoi", "Lenovo", "Apple", "LEGO", "Nutella")
- product_name: full product name in English — read it from ANY text visible in the image
- model: ONLY include model identifiers that are EXPLICITLY printed/shown as text in the image.
  Do NOT guess, infer, or invent model names. If not clearly visible, leave blank.
- key_specs: key differentiating specs if visible (e.g. "16GB 512GB", "750g", null)
- search_query: 2-4 word Amazon search query. Brand + confirmed model ONLY.
  If model is uncertain, use just brand + product category.
  NO storage sizes unless they ARE the model name.
- confidence: "high"=text clearly readable, "medium"=partially visible, "low"=mostly inferred
- scanned_price: numeric price in EUR if a price tag/label is visible, else null
IMPORTANT: Even if this is a screenshot of a webpage, still extract the product name.
NEVER invent product names or model suffixes not visible in the image.
```

### Parallel model strategy
- Gemini 2.0 Flash (free) + Claude Haiku run **simultaneously** via `ThreadPoolExecutor`
- Winner selected by `_score()`: `confidence_level (1-3) + 1 per non-empty field (brand, product_name, model, search_query)` → max score 7
- If both return empty `product_name` → OCR fallback: Gemini reads raw text, then Haiku parses it to JSON

### Assessment

| Aspect | Status | Notes |
|---|---|---|
| Confidence extraction | ✅ Working | `high/medium/low` parsed and used for model selection |
| `model=null` when not visible | ✅ Working | Prompt explicitly says "leave blank if not clearly visible" |
| Dual model fallback | ✅ Working | Gemini free → Haiku backup, best wins |
| OCR last-resort | ✅ Working | 3-stage: structured → structured → OCR→reparse |
| Image quality pre-check | ❌ Missing | No blur/dark/low-resolution detection before API call |
| Timeout handling | ⚠️ Partial | 25s total for each model — could be tight on slow connections |

**Risks:**
- **No image quality gate.** Blurry or dark photo is sent to AI, wastes ~€0.001 per call and returns `confidence: low`. A blur score (Laplacian variance) would reject clearly bad images before API call.
- **`search_query` can include full regional model code.** If AI reads "RB34C600ESA" from label, it outputs `search_query: "Samsung RB34C600ESA"` — shops may not find it (see §2).
- **No logging of `confidence: low` results.** Worth tracking to understand real-world accuracy.

**Priority fixes:**
- P2: Add image blur/size pre-check (e.g. reject if base64 < 5KB or Laplacian < threshold)
- P2: Log identify confidence distribution to Supabase for accuracy tracking

---

## 2. QUERY GENERATION

### Critical finding: TWO separate code paths

**Path A — identify-product + search (used by camera scan flow):**
```python
# /api/identify-product — uses AI-generated search_query directly:
search_query = vision.get("search_query")  # e.g. "Samsung RB34C600ESA"
# If empty, fallback: brand + product_name + key_specs
# If brand missing from query, prepend it
→ returned to frontend → frontend calls /api/search with this string
```

**Path B — scan-image (legacy all-in-one endpoint):**
```python
# /api/scan-image — ignores AI's search_query, builds its own:
if product_code and brand:
    search_query = f"{brand} {product_code}"   # "Samsung RB34C600ESA"
elif product_code:
    search_query = f"{product_name} {product_code}"
else:
    search_query = product_name + (pieces info)
```

**These paths produce different queries for the same photo.** Path B always uses the raw `product_code` string; Path A trusts the AI to generate a good `search_query`.

### Model code normalization
- **Added 2026-06-19:** `_model_code_variants(query)` strips `/EF`-style suffix and trailing 2-3 uppercase letters from the last token when preceded by a digit:
  - `"Samsung RB34C600ESA/EF"` → `["...ESA/EF", "...ESA", "RB34C600"]`
  - `"Samsung RB34C600ESA"` → `["...ESA", "RB34C600"]`
- Progressive retry cascade fires **after** main search returns 0 results — so adds a full extra search round trip.

### Query length and marketing words
- `_short_amazon_query()` strips marketing filler (15 words) and caps at 3 words — used **inside Amazon scraper** as internal retry, not before first attempt.
- Elesen gets the full untruncated query regardless of length.
- AI-generated `search_query` is capped at "2-4 words" by prompt instruction — usually clean.

### Assessment

| Aspect | Status | Notes |
|---|---|---|
| AI query quality | ✅ Good | Prompt explicitly says "Brand + model ONLY, 2-4 words" |
| Model code normalization | ✅ Added | `_model_code_variants` handles `/EF` and regional letter suffixes |
| Progressive retry | ✅ Added | Fires post-search when 0 results |
| Path A vs Path B inconsistency | ⚠️ Risk | Different logic for same photo |
| Query too long / with filler | ⚠️ Partial | Only Amazon has internal truncation; Elesen gets full string |

**Risks:**
- **Path A trusts AI's `search_query` 100%.** If AI over-specifies (e.g., adds `"256GB"` to model code), it narrows results unnecessarily. The prompt says "NO storage sizes unless they ARE the model name" — but AI does not always comply.
- **Retry adds latency.** 0-result detection + retry adds 12-16s to an already-slow path. Better solution: try normalized query *in parallel* with full query on first attempt.
- **No test for `_model_code_variants`.** Regex `r'^(.*\d)([A-Z]{2,3})$'` won't match codes ending in digit+letter+digit (e.g., `WH-1000XM5` ends in `5` — correct, won't strip). But `RB34C600ESA` ends in `0` + `ESA` — ✅ correct.

**Priority fixes:**
- P1: Run normalized query **in parallel** with full query (not after 0 results) — adds ~0 latency when it works
- P1: Normalize `search_query` in Path A before sending to search: strip `/XX` suffix before first attempt
- P2: Test `_model_code_variants` with ≥10 real model codes

---

## 3. SCRAPE

### Active shops and timeouts

| Shop | Method | Timeout | Notes |
|---|---|---|---|
| **Elesen.lt** | Direct HTTP 2s → ScraperAPI render_js 7s | 9s total | LT proxy, JS-rendered |
| **Amazon.DE** | ScraperAPI premium render_js | 18s | Internal retry with `_short_amazon_query` |
| **Amazon.PL** | ScraperAPI premium render_js | 18s | Same as DE |

**Execution order in `/api/search`:**
1. Elesen starts immediately (parallel with translation)
2. Translation (LT→DE/PL) runs in parallel — static dict instant, Claude ~2s
3. Amazon.DE + Amazon.PL start after translation completes
4. LT shops collected with 11s timeout
5. Amazon collected with up to `22 - elapsed` seconds remaining

**Execution order in `/api/scan-image`:**
- All 3 shops start simultaneously with 10s total timeout — **Amazon gets same timeout as Elesen**, which is too tight for premium ScraperAPI (typically 10-20s)

### Graceful degradation
- Each shop runs in its own future; exceptions are caught per-shop
- If one shop errors, others continue — ✅ graceful
- If timeout fires, `as_completed` returns what's ready — ✅ partial results OK

### Amazon internal retry
```python
# scrape_amazon() — when 0 items found and not bot-blocked:
short_q = _short_amazon_query(query)  # strip filler, cap at 3 words
# Retries once with short_q if different from original
```

### Assessment

| Aspect | Status | Notes |
|---|---|---|
| Parallel execution | ✅ Good | All shops parallel |
| Shop failure isolation | ✅ Good | Per-shop try/except |
| Amazon timeout in `/api/scan-image` | ❌ Too short | 10s total = Amazon almost always times out |
| Amazon timeout in `/api/search` | ✅ Good | Up to 22s available |
| Amazon bot detection | ✅ Detected | CAPTCHA logged, no wasted retry |
| Elesen timeout | ✅ OK | 2s direct + 7s ScraperAPI = 9s |

**Risks:**
- **`/api/scan-image` gives Amazon only 10s** — ScraperAPI premium regularly takes 10-20s. Amazon results almost certainly time out on every scan-image request. This means scan-image effectively only uses Elesen.
- **Only 1 LT shop (Elesen).** For categories like large appliances, Elesen inventory is thin. Varle/Senukai/Pigu scrapers still exist but are not called.

**Priority fixes:**
- P0: Increase `scan-image` timeout from 10s to at least 18s (matching Amazon's own timeout)
- P1: For large appliance queries (šaldytuvas, skalbyklė, etc.), add Varle.lt to retry executor — scraper exists, just not called

---

## 4. VALIDATION

### Stage 1 — `is_relevant_result(query, title)` (rule-based, free)
- Checks model number match with compact variants (hyphen removal, suffix stripping)
- Checks accessory word blocklist (150+ words in LT/EN/DE/PL: "case", "dėklas", "filter", "dirželis", etc.)
- For model-specific queries, hides results where model doesn't match at all
- Short queries (<2 words, no model number) use brand-only check

### Stage 2 — `validate_price(price, query)` (rule-based, free)
- Category-specific price floors: MacBook ≥€500, iPhone ≥€400, fridge ≥€30, washing machine ≥€50, etc.
- Global ceiling ≥€50,000
- Returns 0.0 for rejected prices (removed from results)

### Stage 3 — `validate_results_with_ai(query, results)` (Claude Haiku, paid)
- **Triggers only when max/min price ratio ≥ 2x** (recently lowered from 3x)
- Sends up to 8 results to Claude Haiku with instruction: "dramatically cheaper = accessory"
- Falls back to full result list if AI call fails or removes everything

### Stage 4 — `code_match` flag (scan endpoints only)
- If a `product_code` was extracted (e.g., "RB34C600ESA"), each result gets `code_match: bool`
- Results without code match get `match_warning` label
- **Does NOT hide results** — just warns; relevant for UX not filtering

### Assessment

| Aspect | Status | Notes |
|---|---|---|
| Accessory word blocklist | ✅ Comprehensive | 150+ words, multi-language |
| Price floor per category | ✅ Good | Covers major categories |
| AI accessory filter | ✅ Working | Triggers at 2x spread |
| Model code presence check | ✅ Working | `code_match` flag per result |
| Strict model match for code queries | ✅ Working | `post_process` returns [] if model-specific and no match |
| Validation when 1 result only | ⚠️ Gap | `validate_results_with_ai` skips if ≤1 result |

**Risks:**
- **`validate_results_with_ai` needs ≥2 results to trigger.** If only 1 result found (e.g., after retry), accessories can slip through even at 2x price.
- **`is_relevant_result` doesn't handle Samsung fridge codes well.** `RB34C600` in a result title matches `RB34C600ESA` query — ✅ BUT `RB34C600ESA/EF` in title vs `RB34C600` query also needs to match. Current digit-substring logic: `code_digits in title_digits` should handle this.
- **No test for `validate_results_with_ai`.** Hard to unit-test (requires API), but the trigger logic (`max/min < 2`) could be tested.

**Priority fixes:**
- P2: Single-result case: run simpler rule-based accessory check even when AI skips (check if price is below category floor)
- P2: Add integration test fixture for `validate_results_with_ai` trigger condition

---

## 5. ZERO RESULTS HANDLING

### Backend (added 2026-06-19)
```
Original query → 0 results
→ _model_code_variants() generates [stripped_suffix, stripped_regional_code]
→ Full re-search for each variant (Elesen + Amazon.DE + Amazon.PL, 16s)
→ First successful variant → results returned, query updated to shorter version
→ Still 0 → response includes tried_query field
```

### Frontend
- If `d.search_suggestion` returned → auto-retry with 1.2s delay (existing mechanism)
- If no suggestion → show no-results screen with `d.tried_query` in editable input
- User can edit the query and hit "Redaguoti ir ieškoti"
- Amazon.de deep-link with tried_query for manual fallback

### Assessment

| Aspect | Status | Notes |
|---|---|---|
| Progressive retry | ✅ Added | 2-level cascade (strip /XX, strip regional letters) |
| Editable retry query | ✅ Added | Frontend shows tried_query in input |
| Retry latency | ⚠️ High | Each retry = 16s extra wait |
| Third-level fallback | ❌ Missing | No "brand + category" fallback (e.g., "Samsung šaldytuvas") |

**Risks:**
- **Retry adds 16s.** Users wait 25-30s total for a 0-result scan. Would be better to run normalized variants in parallel on first attempt.
- **No category-level fallback.** If "Samsung RB34C600" also returns 0, there's no automatic "Samsung šaldytuvas" attempt.

---

## TEST COVERAGE

| Component | Test file | Coverage |
|---|---|---|
| `is_relevant_result()` | `test_matching.py` | ✅ Excellent (20 scenarios, 60+ test cases) |
| `validate_price()` + `parse_price()` | `test_price_validation.py` | ✅ Good (30+ cases, all categories) |
| Vision/identify pipeline | — | ❌ **Zero tests** |
| Query generation logic | — | ❌ **Zero tests** |
| `_model_code_variants()` | — | ❌ **Zero tests** |
| `scrape_elesen()` / `scrape_amazon()` | — | ❌ **Zero tests** (requires live API) |
| `validate_results_with_ai()` | — | ❌ **Zero tests** |
| Zero-results retry cascade | — | ❌ **Zero tests** |
| `/api/identify-product` endpoint | — | ❌ **Zero tests** |
| `/api/scan-image` endpoint | — | ❌ **Zero tests** |

**Test coverage for the photo→search pipeline = 0%.**  
Only the downstream filtering functions are tested. The entire chain from photo to query is untested.

---

## TOP 3 FIXES TO IMPROVE HIT RATE

### #1 — P0: Fix Amazon timeout in `/api/scan-image`
**Current:** All 3 shops get 10s total. Amazon premium ScraperAPI needs 10-20s. Amazon almost always times out in scan-image.  
**Fix:** Increase `scan-image` timeout from `timeout=10` to `timeout=20`. One line change.  
**Expected impact:** Amazon results appear in scan-image for the first time. Estimated +30-40% hit rate for scan-image path.

### #2 — P1: Normalize query BEFORE first attempt (not after 0 results)
**Current:** Original query tried first → 0 results → 16s retry with normalized query.  
**Fix:** Extract `_model_code_variants(search_query)` at query-build time; run ALL variants in the first parallel search batch. First variant to return results wins.  
**Example:** Send `"Samsung RB34C600ESA"` AND `"Samsung RB34C600"` to shops simultaneously. Total latency unchanged.  
**Expected impact:** Eliminates the 16s retry penalty. Model-code queries go from 0 results to finding products without extra wait.

### #3 — P1: Add test for `_model_code_variants` + query generation
**Current:** Zero tests for query generation code.  
**Fix:** Add `test_query_generation.py` with ≥15 cases: regional suffix stripping, /XX suffix stripping, AI query passthrough, brand prepend logic.  
**Why it matters:** The regex `r'^(.*\d)([A-Z]{2,3})$'` is the core of hit-rate improvement. Without tests, regressions are invisible.

---

## SUMMARY TABLE

| Pipeline Stage | Status | Biggest Risk | Priority Fix |
|---|---|---|---|
| Image analysis | 🟡 Good with gaps | No quality pre-check | P2: blur detection |
| Query generation | 🟡 Recently improved | Retry adds 16s latency | P1: parallel first-attempt |
| Scrape | 🔴 **Amazon scan-image broken** | 10s timeout too short | P0: increase to 20s |
| Validation | 🟢 Good | Single-result accessory gap | P2: rule fallback |
| Zero results | 🟡 Recently improved | No category fallback | P1: parallel first-attempt |
| Test coverage | 🔴 **0% for photo pipeline** | Silent regressions | P1: add query tests |
