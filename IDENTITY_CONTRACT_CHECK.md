# IDENTITY CONTRACT CHECK — v7.62

**Date:** 2026-08-01
**Branch:** fix/identity-contract → merge to main
**Incident:** #2 (2026-08-01) — recognition of LEGO City 60492 worked correctly, but the
search query dropped the model code and Amazon.pl's wrong-product substitute (LEGO Technic
42198) was shown instead of an honest "not found".

---

## Root cause

The screenshots/flow in this incident go through `runIdentify()` → `POST /api/identify-product`
→ confirm panel (`ccf-edit` "Ieškoti pagal" field) → `confirmSearch()` → `doSearch()`. This is a
**different, always-live** endpoint from `scan_image()`/`vision_only` (which the previous
session's v7.60/7.61 latency work touched — that code path is not wired into the current UI;
`runScan()` is never called from any button). All grounding/latency work done there did not
affect this incident.

`identify_product()` used the AI's own `search_query` field directly ("AI understands products
better than manual construction"). When the AI's `search_query` omitted the model number
(e.g. produced "LEGO City Passenger Jet" instead of "LEGO City Passenger Jet 60492"), the code
was silently dropped from the query before it ever reached the scraper/validator layer — so
`is_relevant_result()`'s existing strict model-code check (which already normalizes
spaces/hyphens and rejects fuzzy digit matches) had nothing to check against, and any
brand-matching result — including a wrong set — passed through.

---

## Changes deployed

### Task 1 — Query formation: model_code never dropped
- `identify_product()` (server.py): when `model_code` is present, the query is rebuilt as
  `"{brand-prefixed name} {model_code}"` regardless of what the AI put in its own
  `search_query`. Brand is prefixed only if not already present in the name (no duplication).
- Response now includes a `product_identity: {brand, model_code, name}` object.
- Verified other entry points already preserve the code and need no change:
  - **Barcode**: the scanned EAN/code IS the query string — nothing to drop.
  - **Text search**: whatever the user typed is sent verbatim.
  - **Saved products / alerts**: replay the exact string from a previous (now identity-safe) search.
  - **`scan_image()`** (dead code, unused by current UI): already built `"{brand} {code}"` correctly.

### Task 2 — Result validator: 3-level identity check
Investigation showed `is_relevant_result()` **already implements** all 3 levels — Level A
(model code, hyphen/space-normalized, no fuzzy matching), Level B (brand match; "for X" /
"compatible with X" / "skirta X" phrasing treated as accessory not brand match), Level C
(name-token-overlap similarity for no-code products) — the incident was never a validator gap,
it was Task 1's query-formation bug feeding the validator an empty slot to check against.

What was genuinely missing — added now:
- `_normalize_identity_code()`: shared space/hyphen-stripped, uppercased comparison helper.
- `_classify_rejection_reason()`: post-hoc reason classifier (`code_mismatch` /
  `brand_mismatch` / `accessory` / `low_similarity`) mirroring `is_relevant_result`'s own check
  order (brand → code → accessory) — used for logging only, does not alter the accept/reject
  decision, so the existing (heavily fixture-tested) matching behavior is untouched.
- `post_process()` now tags every rejected result with `rejected_reason` and returns
  `valid_offers` / `rejected_offers` counts in the API response.

### Task 3 — Honest "not found" UI
Investigation showed this was **already correctly implemented**:
- `post_process()` already returns `results: []` (not a wrong-product substitute) when a
  model-specific query has zero relevant matches — see the existing comment
  "model-specific query: no exact match → show nothing rather than wrong product".
- Frontend's `renderResults()` no-results branch already shows an honest "Nieko nerasta" state
  with an editable retry field — matches the requested UX.
- No "similar products" backfill section was added (task explicitly marked it optional/low
  priority — skipped to avoid scope creep).
- `results_shown` intent event payload now includes `valid_offers` / `rejected_offers` (client
  event, `payload` is a JSONB column — no schema migration needed).

### Task 4 — Regression tests
`tests/test_identity_contract.py` — 30 fixture-based tests, no live API calls:
- `TestQueryFormation` (7): verifies model_code survives query building across every entry
  point, including the exact Incident #2 shape.
- `TestCodeNormalization` (4): "6 0492"/"60-492" equal "60492"; 60492 ≠ 42198 ≠ 60462.
- `TestLevelA_ModelCode` (7), `TestLevelB_Brand` (3), `TestLevelC_NameSimilarity` (3): the
  3-level validator contract.
- `TestRejectionReasonClassification` (3): reason codes match actual rejection cause.
- `TestIncidentScenarios` (3) — the two incident pairs run through the real `post_process()`:
  - Incident pair 1: Technic 42198 + 60262 vitrina fixture → both rejected → honest "not found".
  - Incident pair 2: same query, genuine 60492 listing present among the same noise → only it passes.
  - No-code product (Sony WH-1000XM5): case accessory rejected, real headphones pass.

`tests/test_pipeline.py` does not exist in this repo — `test_identity_contract.py` is the
integration point instead (collected by pytest alongside the other `tests/*.py` files).

---

## Validation gates

| Gate | Result |
|------|--------|
| New identity tests green | ✅ 30/30 |
| `recognition_photo_test.py` + `test_intent_events.py` green (no regressions) | ✅ 33/33 |
| `recognition_mass_test.py` (500-item harness) — no NEW failures | ✅ Same 8 pre-existing failures with and without this change (verified via `git stash` A/B) — unrelated to identity contract (GoPro/Nikon/Insta360 battery, Colgate toothbrush/mouthwash, Rode deadcat, iPad mini case — all pre-existing accessory-filter gaps, out of scope) |
| Photo hallucination gate (0 hallucinations, `verified: true`) | ✅ unaffected — no changes to OCR grounding logic |
| Latency not degraded | ✅ `_classify_rejection_reason()` runs only on already-rejected items, pure in-memory string ops, zero new API/network calls |

---

## Smoke test plan (max 3 live queries)

1. `LEGO 60492` — result must be either a genuine 60492 listing or honest "not found"; never
   a different model.
2. `iPhone 16 Pro` — phones only, no cases.
3. One ordinary query — confirm nothing broke.

## DEPLOY: PENDING
