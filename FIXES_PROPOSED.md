# FIXES_PROPOSED.md
**Branch:** `auto-fixes-review`  
**Date:** 2026-06-19  
**Status:** Both fixes implemented and committed on this branch. Not merged to main.

---

## Summary

| Fix | Status | Risk | Impact | Categories affected |
|---|---|---|---|---|
| Fix 1: Unit-token false negatives | IMPLEMENTED | LOW | HIGH | food, cosmetics, baby |
| Fix 2: LEGO set number preservation | IMPLEMENTED | LOW | MEDIUM | toys/LEGO |

Live test baseline (before fixes): 12/20 queries returned results.  
Expected after fixes: ~14-15/20 (Milka 100g + LEGO Harry Potter 76430 restored).

---

## Fix 1 — Unit-token false negatives in `is_relevant_result` and `post_process`

**Commit:** `fix: unit-token false negatives in is_relevant_result and post_process`

### Root cause

```python
# BEFORE (buggy):
model_tokens = re.findall(r'\b[a-z]*\d+[a-z0-9-]*\b', q)
# "100g", "400ml", "250ml", "800g" all match this pattern
# -> requires them to appear in product title
# -> Amazon titles often omit exact unit -> 0 relevant results
# -> post_process: model tokens present + 0 results -> returns empty []
```

**Live test confirmation:** "Milka 100g" -> 0 results in production.

### The fix

New constant `_UNIT_TOKEN_RE = re.compile(r'^\d+(?:g|ml|l|kg|mg|oz|cl|dl|mm|cm|m|w|v|hz|rpm|pcs|st|stk|er|x)$')` applied in three places:

1. `is_relevant_result()` model_tokens: filter out unit tokens
2. `is_relevant_result()` q_words overlap: exclude unit tokens from overlap denominator
3. `post_process()` empty-results guard: same filter

### Verified safe for:
- `Sony WH-1000XM5` -> "1000xm5" has no unit suffix -> still model token (correct)
- `Samsung RB34C600ESA` -> "rb34c600esa" has no unit suffix -> still model token (correct)
- `Milka 100g` -> "100g" filtered -> brand/name overlap only -> matches ✓
- `Milka 100g` vs `Ritter Sport 100g` -> "milka" absent in title -> rejected ✓

### Edge cases not fixed:
- `Nike Air Max 270 42` — shoe size "42" has no unit suffix, still treated as model token
- `Adidas Ultraboost 22` — year "22" has no unit suffix, still treated as model token (intentional)

---

## Fix 2 — `_short_amazon_query` drops LEGO set numbers

**Commit:** included in same server.py file change

### Root cause

`_short_amazon_query` truncates to 3 words, dropping 4-6 digit set numbers that are the most
specific part of LEGO queries.

`"LEGO Harry Potter 76430 Hogwarts"` -> `"LEGO Harry Potter"` (76430 dropped)

**Live test confirmation:** "LEGO Harry Potter 76430" -> 0 results in production.

### The fix

Priority list: collect all standalone 4-6 digit tokens before truncating. After truncation,
inject any dropped priority tokens by replacing the last slot.

`"LEGO Harry Potter 76430 Hogwarts"` -> `"LEGO Harry 76430"` (set number preserved)

### Verified behaviors:
- `"LEGO Technic 42170"` -> unchanged (already 3 words) ✓
- `"LEGO Harry Potter 76430 Hogwarts"` -> `"LEGO Harry 76430"` ✓
- `"Philips Airfryer XXL HD9860"` -> `"Philips Airfryer XXL"` (no standalone digits) ✓

---

## Fixes NOT implemented

### Supabase soft cache (P2 from SCRAPE_USAGE.md)
Requires schema change to store full result objects.

### LT food vocabulary additions
`_LT_CATEGORY_WORDS` already has cosmetics/clothing terms added in v7.47-7.49.
Food terms (sokoladas, pienas) are low priority since users search in English/German.

### Shoe-size as model token
`Nike Air Max 270 42` — "42" is correctly treated as a specific model variant.
User recommendation: search without shoe size.

---

## How to merge

```bash
git checkout main
git merge auto-fixes-review
git push origin main
```

Commit hash for Fix 1+2: `f277060`
