# FIXES_PROPOSED.md
**Branch:** `auto-fixes-review`  **Date:** 2026-06-19

## Summary
- **7** good titles rejected by `is_relevant_result` (false negatives)
- **4** unit-token false negatives (food/cosmetics: 100g/400ml treated as model code)
- **6** accessory titles NOT filtered (false positives — minor)
- **91** queries truncated by `_short_amazon_query` (potential LEGO set-number loss)

---

## Fix 1 — Unit-token false negatives in `is_relevant_result`
**Risk: LOW** | **Impact: HIGH** | **Categories affected: food, cosmetics, baby**

### Root cause
```python
model_tokens = re.findall(r'\b[a-z]*\d+[a-z0-9-]*\b', q)
# '100g', '400ml', '800g', '250ml' all match this regex
# -> requires them to appear in product title
# -> Amazon titles rarely include exact weight string -> 0 relevant results
```

### Fix
Before extracting model_tokens, strip known unit suffixes from query tokens:
```python
_UNIT_SUFFIXES = re.compile(r'^\d+(?:g|ml|l|kg|mg|oz|cl|mm|cm|m|w|v|hz|rpm|pcs|st|stk)$')
model_tokens = [t for t in re.findall(r'\b[a-z]*\d+[a-z0-9-]*\b', q)
                if not _UNIT_SUFFIXES.match(t)]
```
Also in `post_process`: same filter before the `elif re.findall(...)` check.

---

## Fix 2 — `_short_amazon_query` drops LEGO set numbers
**Risk: LOW** | **Impact: MEDIUM** | **Categories affected: LEGO/toys**

### Root cause
`_short_amazon_query` caps at 3 words. For 'LEGO Harry Potter 76430 Hogwarts' -> 'LEGO Harry Potter' (set number 76430 dropped — most specific part).

### Fix
Detect 4-6 digit standalone numbers (LEGO set numbers) and always keep them:
```python
def _short_amazon_query(q: str) -> str:
    words = q.split()
    if len(words) <= 3:
        return q
    # Always preserve 4-6 digit tokens (LEGO set numbers, product IDs)
    priority = [w for w in words if re.match(r'^\d{4,6}$', w)]
    kept = [w for w in words if w.lower() not in _AMZ_FILLER]
    if kept and len(kept) < len(words):
        result = kept[:3]
        # If priority tokens were dropped, replace last slot
        for p in priority:
            if p not in result:
                result = result[:2] + [p]
        return ' '.join(result)
    return ' '.join(words[:3])
```

---

## Fix 3 — LT food/cosmetics vocabulary gap in `_is_lt_query`
**Risk: LOW** | **Impact: MEDIUM** | **Categories affected: food, cosmetics, clothing**

### Root cause
`_LT_CATEGORY_WORDS` covers appliances/electronics well but lacks: food terms (šokoladas, pienas, jogurtas), cosmetics (kremas, šampūnas, parfumas), clothing (avalynė, apranga, drabužiai), books (knyga).
Result: Lithuanian food/cosmetics queries are NOT translated -> Amazon receives Lithuanian query -> 0 results.

### Fix
Add to `_LT_CATEGORY_WORDS`:
```python
# Food
"šokoladas","sokoladas","pienas","jogurtas","suris","duona",
"maistas","maisto","gėrimas","gerimas","arbata","kava",
# Cosmetics
"kremas","šampūnas","sampunas","dezodorantas","parfumas","kvepalai",
"makiažas","makiazas","kosmetika","losjonas",
# Clothing
"avalynė","avalyne","batai","batas","apranga","drabužiai",
"drabuziai","striukė","striuke","kelnės","kelnes","marškiniai",
# Books
"knyga","knygos","vadovėlis","vadovelis",
```
Also add to `_LT_DE` / `_LT_PL` translation maps for the key terms.

---

## Fix 4 — `post_process` compounds unit-token bug
**Risk: LOW** | **Impact: HIGH** | **Linked to Fix 1**

### Root cause
When query contains digit-tokens AND no relevant results found, `post_process` returns `[]` instead of closest match. With unit tokens treated as model codes (Fix 1's bug), this means food/cosmetics queries always return empty instead of closest match.

### Fix
Apply the same `_UNIT_SUFFIXES` filter in `post_process` before the `elif` check. This is automatically fixed once Fix 1 is applied (same regex).

---

## Implementation order
1. Fix 1 + Fix 4 together (same change, highest impact)
2. Fix 2 (independent, low risk)
3. Fix 3 (additive, no risk)

## Files changed
- `server.py` — `is_relevant_result()`, `post_process()`, `_short_amazon_query()`, `_LT_CATEGORY_WORDS`, `_LT_DE`

