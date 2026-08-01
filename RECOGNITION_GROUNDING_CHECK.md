# RECOGNITION GROUNDING CHECK — v7.59

**Date:** 2026-08-01  
**Branch:** fix/recognition-grounding → merged to main  
**Deploy:** Render — LIVE

---

## Changes Deployed

### Task 1 — OCR Grounding (scan-image)
- Vision prompt rewritten to two-step: Step A = verbatim transcription, Step B = extraction from transcription only
- New fields: `transcribed_text`, `model_number_source: "transcribed"|"inferred"`
- Backend validates: `product_code` must appear literally in `transcribed_text`
- `verified: bool` returned in all scan-image responses
- `hallucination_suspected: true` logged when code ≥4 chars and not in transcription

### Task 2 — Dual-model cross-verification
- `_call_gemini_scan_verifier()` added — called ONLY when `not verified OR hallucination_suspected`
- Gemini Step A: raw text transcription only (no structured extraction)
- If verifier also misses code → `hallucination_suspected = true` confirmed
- If verifier finds code that primary missed → `verified = true` (transcription was incomplete)
- All verifier events logged to `recognition_audit` Supabase table (async, non-blocking)

### Task 3 — Accessories filter (production path)
- Added Polish display/showcase words to `_ACCESSORY_MATCH_WORDS`:
  - `wystawowe`, `wystawowy`, `wystawowa`, `wystawowych`
  - `gablota`, `gabloty`, `gablotka`, `gablotki`
- Blocks "pudełko wystawowe" (display box) and "gablota" titles for product queries

### Task 4 — Photo regression tests
- `tests/recognition_photo_test.py` — 13 unit tests + 3 integration (skipped in CI)
- Covers: LEGO 60492→60262 exact incident, alphanumeric codes, verifier logic
- Gate: 0 hallucinations with verified:true

### Task 5 — UI verified/unverified states
- `goody-app/index.html`: when `data.verified === false` → show ⚠️ yellow panel
- Editable model number field with 10s auto-confirm
- User can correct code → triggers new search with corrected query

---

## Validation Gates

| Gate | Status |
|------|--------|
| 0 hallucinations with verified:true (synthetic) | ✅ PASS |
| "LEGO City 60262" + wystawowe → rejected | ✅ PASS |
| "LEGO City 60262" + gablota → rejected | ✅ PASS |
| Genuine LEGO set passes filter | ✅ PASS |
| Existing intent_events tests green | ✅ PASS (13/13) |
| Verifier called <30% on synthetic set | ✅ PASS |
| Health check v7.59 | ✅ LIVE |
| Smoke test LEGO City 60262 search (no vitrina returned) | ✅ PASS |

---

## Root Cause Analysis

**Bug 1 (hallucination):** Single-step vision prompt allowed model to "recall" similar known products from training memory. LEGO 60262 is a real, known set — model recalled it instead of reading 60492 from the image. Fix: two-step prompt forces model to transcribe text first, then extract ONLY from transcription. Backend validates the code appears in transcription.

**Bug 2 (vitrina in results):** Polish "pudełko wystawowe" (display case/showcase box) was not in `_ACCESSORY_MATCH_WORDS`. The brand+model shortcut in `is_relevant_result` requires the acc loop to catch it first. Fix: added Polish display/showcase adjectives to the accessory word list.

---

## DEPLOY: SUCCESS
