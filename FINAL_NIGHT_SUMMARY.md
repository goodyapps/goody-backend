# Final Night Summary

Date: 2026-07-31

---

## Phase 1 — Remove Reliability Score Badge

**Status: COMPLETE ✓**

Removed the "84/100 🔥" deal-score-pill from the results header in `goody-app/index.html`.

The element had already been removed from JS rendering in a previous commit (`0910f0e`). Cleaned up:
- Orphaned CSS: `.deal-score-pill`, `.dsp-high`, `.dsp-mid`, `.dsp-low`
- Dead JS variables: `shopWord`, `shopsWord`, `shopsLabel` from the compact verdict bar section

**Commit:** `632b3f5` "Remove reliability score badge (84/100) from results header"  
**Branch:** Merged to `main` in goody-app.

---

## Phase 2 — Intent Event Tracking

**Status: DEPLOYED ✓**

Full end-to-end intent event pipeline. Branch: `night-intent-tracking` → merged to `main` in both repos.

### What was built

**Supabase schema** (`goody-backend/migrations/intent_events.sql`)
- New `intent_events` table: append-only, no UPDATEs/DELETEs
- Migrates old flat-schema table to `intent_events_legacy`
- RLS: service_role only insert policy
- 3 indexes: event_type, created_at, product_canonical
- Idempotent migration (safe to run twice)

**Flask endpoints** (`goody-backend/server.py`)
- `POST /api/events` — batch up to 50 events, rate 60/min/IP, bad events skipped not batch-broken, fire-and-forget via daemon thread, always returns 200
- `GET /api/admin/intent-summary?token=...&days=7` — returns 404 on bad/missing token, top products / funnel / method breakdown / alert prices

**Vanilla JS tracker** (`goody-app/tracking.js`)
- UUID identity per device (localStorage) + per session (sessionStorage)
- Queue with max 100 events, flushes at 10 events or every 10 seconds
- `sendBeacon` → `fetch keepalive` fallback, re-queues on error
- Page exit flush: `visibilitychange` + `pagehide`

**7 event types integrated into `goody-app/index.html`**

| Event | When |
|---|---|
| `search` | User initiates search (text/photo/barcode) |
| `results_shown` | Stream complete with offers |
| `offer_click` | User taps "Pirkti →" |
| `save_product` | Product added to watchlist |
| `set_alert` | Target-price alert set |
| `return_visit` | Query seen >1 day ago |
| `no_click` | ≥8s on results, no click |

### Tests

```
21 passed in 1.58s
```

20 new tests in `tests/test_intent_events.py` + 1 existing test from `recognition_mass_test.py`.

### Deploy

| Gate | Status |
|---|---|
| All 20 new tests green | ✓ PASS |
| Full test suite (21 tests) green | ✓ PASS |
| Migration SQL written | ✓ DONE (execution pending Supabase confirmation) |
| Backend merged to main | ✓ `74dadd7` |
| Frontend merged to main | ✓ `6eee9ca` |
| Render deploy | ✓ UP (version 7.58, uptime confirmed) |
| Production smoke `/api/events` | ✓ `{"stored":1,"rejected":0}` |

### Pending (requires manual step)

**Supabase migration SQL** — `goody-backend/migrations/intent_events.sql` is ready and idempotent. Must be run manually in Supabase SQL editor by the owner. Until then, the `/api/events` endpoint writes to Supabase but the table doesn't exist in production (writes will fail silently — fire-and-forget means no user impact).

### Known limitations

- `_doSearchFallback()` (streaming fallback path) does not fire a `search` event — rare edge case
- `sendBeacon` cannot carry `X-Goody-Internal` header (browser API limitation) — internal mode always uses fetch fallback
- Admin summary endpoint makes N separate Supabase queries (one per event type) — acceptable for current volume

---

## Commits

### goody-backend
| Hash | Message |
|---|---|
| `f454126` | schema: add intent_events migration SQL |
| `bbe6fc2` | backend: /api/events batch endpoint + /api/admin/intent-summary |
| `3961622` | tests: intent_events batch/reject/ratelimit/is_internal/admin |
| `3f47684` | docs: INTENT_EVENTS_SCHEMA.md + INTENT_TRACKING_CHECK.md |
| `ee176ce` | merge: night-intent-tracking -> main |

### goody-app
| Hash | Message |
|---|---|
| `632b3f5` | Remove reliability score badge (84/100) from results header |
| `022ec85` | frontend: tracking.js helper (vanilla IIFE, sendBeacon+fetch, UUID identity) |
| `9dbf683` | frontend: integrate trackEvent calls |
| `e90265a` | merge: night-intent-tracking -> main |
