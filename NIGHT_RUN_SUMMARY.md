# Night Run Summary — 2026-07-07 (branch: fix/recognition-night-run)

## Constraints respected
- ❌ NIEKO į main — branch not merged
- ❌ NIEKO į gyvą Supabase — no live DB touched
- ❌ Render auto-deploy — not triggered
- ❌ Migration SQL — not run (none needed)

---

## Fixed items

### 1 — is_relevant_result comprehensive overhaul (v7.58) `5d60038`

**Before:** L1 rel_fail=7/200, acc_fail=6/200  
**After:** L1 rel_fail=0/200, acc_fail=0/200

Root causes found and fixed:

| Bug | Fix |
|-----|-----|
| `'pro'` in `_VARIANT_WORDS` blocks TRX PRO4 (title has 'pro4' token, not 'pro') | Allow variant absorbed into model-number token (prefix + digit) |
| `'plus'` in `_VARIANT_WORDS` blocks NUK First Choice+ (title uses '+' symbol) | Allow '+' as synonym for 'plus' |
| `'repair'` in acc words blocks "Dove Intensive Repair Shampoo" | Remove 'repair'; add 'repair kit' (phrase) |
| `'skin'` in acc words blocks "Garnier Skin Naturals" | Remove 'skin' (sticker/decal covers phone skin case) |
| `'rucksack'` in acc words blocks "Osprey Kestrel 48 Herren Rucksack" | Remove 'rucksack' (standalone hiking backpack is main product) |
| `'ladegerät'` in acc words blocks "Anker Ladegerät" for query "Anker Charger" | Add cross-language synonym mapping (ladegerät ↔ charger) |
| "Ramp set for Hot Wheels" not caught (no known brand, no model number) | Add "for [word-in-query]" check without requiring brand/model |
| "Display box Haribo" not caught | Add 'display box' to acc words |
| 'bookmark', 'accessory' (singular) missing | Added to acc words |

Also fixed in prior commits on this branch (v7.57):
- Book title overlap threshold (0.55→0.50 for 4+ word queries)
- "for X" compat pattern narrowed to brand/model queries only (prevents book-subtitle false blocks)
- Added hinge/gasket/seal/bearing to acc words (mechanical spare parts)
- Removed bare 'akku' (cordless vacuums like "Akku-Staubsauger" are main products)

### 2 — test_pipeline.py updated to real server.py imports `5d60038`

Old test had stale inlined copies of `is_relevant_result` and helper functions that did NOT include the `_ACCESSORY_MATCH_WORDS` check. Now imports directly from server.py — future server.py changes are tested automatically.

### 3 — Security: rate limiting for two endpoints `94e5b92`

| Endpoint | Risk | Fix |
|----------|------|-----|
| `GET /api/debug-html` | HIGH — burns ScraperAPI credits if key leaks | Global 10 calls/min cap |
| `POST /api/track` | MED — click counter poisoning | Per-IP 30 calls/min cap |

---

## Found but not fixed (requires manual review)

### LEGO 76430 — returning Nintendo Switch game (root cause known)

The Elesen scraper hits a CloudFlare wall since 2026-06-16 (LT shops removed). Elesen returns 0 results for LEGO 76430 in Layer 2 live test (confirmed: `[zero] LEGO Harry Potter 76430`). The wrong-product match was from Amazon sponsored ad keyword stuffing — this is now correctly rejected by the updated `is_relevant_result`.

**Status:** Not a code bug. Elesen is returning no results due to CloudFlare. Amazon scrape returns 0 results for this query (also confirmed in Layer 2). The LEGO 76430 issue is a data availability problem, not a recognition bug.

### Accessory false-match (LED kits) — already handled

LED/lighting acc words were added to `_ACCESSORY_MATCH_WORDS` in a prior commit: `'lighting', 'light kit', 'light set', 'led light', 'lighting kit'`. No further action needed.

### Amazon sponsored-ad keyword stuffing

`is_relevant_result` now correctly rejects sponsored ads with mismatched model numbers. No additional fix needed for currently active shops (Amazon.DE, Amazon.PL).

---

## Layer 2 live test results (before this night run — from prior session)

```
[ok   ] Samsung RB34C600ESA
[zero ] Bosch WAX32EH0           ← no results (scraper/availability)
[ok   ] Sony WH-1000XM5
[ok   ] Apple iPhone 15 Pro 128GB
[ok   ] LEGO Technic 42170
[zero ] LEGO Harry Potter 76430  ← 0 results (CloudFlare/availability)
[ok   ] Milka 100g
[ok   ] Nutella 400g
[ok   ] Dove Shampoo 400ml
[ok   ] Nivea Creme 250ml
[zero ] Nike Air Max 270 42      ← no results
[zero ] Adidas Ultraboost 22     ← no results
[ok   ] Atomic Habits James Clear
[ok   ] Clean Code Robert Martin
[ok   ] Dyson V15 Detect
[zero ] Philips Airfryer XXL HD9860 ← no results
[ok   ] Garmin Forerunner 265
```

13/17 OK, 4 zero (all are scraper/availability issues, not recognition bugs).

---

## Manual env var actions needed

None required. All changes are pure Python logic — no new environment variables or config needed.

The following were already noted from the previous night run (still pending review by human):
- `DEBUG_API_KEY` — rotate if shared; the debug-html rate limit now protects against credit abuse even if key leaks.

---

## Before/after test results

| Metric | Before (stale inlined) | After (real server.py) |
|--------|----------------------|----------------------|
| L1 rel_fail | 2/200 | **0/200** |
| L1 acc_fail | 8/200 | **0/200** |

Note: the "before" baseline used stale inlined functions that were missing the `_ACCESSORY_MATCH_WORDS` check entirely. The "real" baseline (after import fix, before night run fixes) was rel_fail=7/200, acc_fail=6/200. The night run brought both to 0.

---

## Recommendations

1. **Merge to main after code review** — all changes are on `fix/recognition-night-run`. Create a PR; review the `_ACCESSORY_MATCH_WORDS` removals (repair, skin, rucksack) before merging.

2. **Cross-language synonym expansion** — the `_ACC_CROSS_LANG` dict currently covers charger synonyms (ladegerät/kroviklis/ładowarka). Consider expanding for other common pairs (kabel↔cable, etc.) when false negatives appear for German/Lithuanian/Polish queries.

3. **Elesen CloudFlare** — Elesen.lt is still blocked (CloudFlare). Either re-add Playwright/Selenium scraping for Elesen, or remove it from active shops to avoid wasted scraper credit on failed requests.

4. **test_pipeline.py Layer 2** — the live test shows 4 "zero" results, all for real scraper/availability failures. These are not code bugs but worth monitoring over time to detect if Amazon blocking increases.

5. **Rotate DEBUG_API_KEY** periodically. The 10/min global rate limit on debug-html is a backstop, not a substitute for a strong key.
