# INTENT INTEGRATION PATIKRA — PRIEŠ MERGE Į MAIN

**Šaka:** intent-integration  
**Data:** 2026-06-20  
**Verdiktas:** ✅ ŽALIA — saugu merge į main

---

## 1. TESTAI

Paleisti 4 testų rinkiniai šakoje `intent-integration`:

| Failas | Rezultatas | Pastaba |
|--------|-----------|---------|
| `test_core_functions.py` | **20/20 PASS** ✅ | normalize_query, deduplicate_by_shop, _short_amazon_query |
| `test_matching.py` | **Visi PASS** ✅ | is_relevant_result — 150+ atvejų, iš jų iPhone, Sony, Bosch, Dyson ir kt. |
| `test_price_validation.py` | **1 FAIL** ⚠️ | iPhone SE @219€ — **pre-existing klaidoje main** (ne mūsų pakeitimai) |
| `test_accessory_fix.py` | **1 FAIL** ⚠️ | compatible signal testas — **pre-existing klaidoje main** (ne mūsų pakeitimai) |

**Patvirtinimas:** abiejų nesėkmių tas pats rezultatas ant `main` šakos — mūsų kodo pakeitimai šių klaidų nesukūrė.

**Paveikti testai:** 0 — intent-integration nepablogino nei vieno testo.

---

## 2. FIRE-AND-FORGET — KRITIŠKAS PATIKRINIMAS

**Atsakymas: ✅ TAIP — logging yra visiškai non-blocking**

### Kodo kelias `search()`:
```python
threading.Thread(target=save_prices_to_supabase, ...).start()  # egzistavo anksčiau

_search_id = str(uuid.uuid4())
result["search_id"] = _search_id
log_intent_async(_build_intent_event(...), get_supabase())  # ← NAUJAS

ip = get_client_ip()
...
return resp  ← vartotojas gauna atsakymą ČIA, nepriklausomai nuo logging
```

### Kodo kelias `search_stream()`:
```python
threading.Thread(target=save_prices_to_supabase, ...).start()

_stream_id = str(uuid.uuid4())
result["search_id"] = _stream_id
log_intent_async(_build_intent_event(...), get_supabase())  # ← NAUJAS

yield _sse("complete", result)  ← SSE complete siunčiamas ČIA
```

### Apsaugos mechanizmai:
- `log_intent_async()` → `threading.Thread(..., daemon=True).start()` → iš karto grąžina kontrolę
- `_sb_log_intent()` turi `try/except Exception` — visos Supabase klaidos sugaunamos, tik `[intent_log] WARNING:` spausdinama
- Jei `sb_client is None` (Supabase nepasiekiamas) → funkcija iš karto grąžina `return`
- Vartotojo paieška **niekada nelaukia** intent logging rezultato

**Išvada:** Jei Supabase miega, lėtinas ar grąžina klaidą — vartotojas to nejaučia.

---

## 3. SCHEMA ATITIKIMAS

`intent_events` Supabase lentelė vs `_build_intent_event()` grąžinamas dict:

| Lentelės stulpelis | Tipas | _build_intent_event() | Statusas |
|-------------------|-------|----------------------|---------|
| id | UUID NOT NULL | `str(uuid.uuid4())` | ✅ |
| product_key | TEXT NOT NULL | `_make_product_key(...)` | ✅ |
| product_name | TEXT NOT NULL | `query.lower().strip()[:200]` | ✅ |
| product_type | TEXT | `result_data.get("product_type")` | ✅ |
| input_method | TEXT NOT NULL DEFAULT 'text' | `input_method or "text"` | ✅ |
| scan_confidence | TEXT | **nepateikiama** → NULL | ✅ nullable |
| language | TEXT NOT NULL DEFAULT 'lt' | `language or "lt"` | ✅ |
| hour_of_day | SMALLINT | `now.hour` | ✅ |
| day_of_week | SMALLINT | `now.weekday()` | ✅ |
| week_of_year | SMALLINT | `now.isocalendar()[1]` | ✅ |
| verdict | TEXT | `result_data.get("ai_verdict") or result_data.get("verdict")` | ✅ |
| price_min_eur | NUMERIC(10,2) | `round(float(...), 2)` arba None | ✅ |
| price_max_eur | NUMERIC(10,2) | `round(float(...), 2)` arba None | ✅ |
| shops_found | SMALLINT DEFAULT 0 | `len(results_list)` | ✅ |
| cheapest_shop | TEXT | `results_list[0].get("shop")` | ✅ |
| has_history | BOOLEAN DEFAULT FALSE | `bool(result_data.get("price_history"))` | ✅ |
| clicked_shop | TEXT DEFAULT NULL | `None` (užpildoma vėliau per /api/track) | ✅ |
| clicked_at | TIMESTAMPTZ DEFAULT NULL | `None` | ✅ |
| added_watchlist | BOOLEAN DEFAULT FALSE | `False` | ✅ |
| watchlist_target_eur | NUMERIC(10,2) DEFAULT NULL | `None` | ✅ |
| created_at | TIMESTAMPTZ DEFAULT NOW() | **nepateikiama** → Supabase užpildo automatiškai | ✅ |

**Schema atitikimas: 100%.** Visi NOT NULL laukai užpildyti. `scan_confidence` yra nullable — tai žinomas apribojimas (šiuo metu visada NULL, bus naudojamas kai foto paieška grąžins confidence).

---

## 4. PRODUCT_KEY NORMALIZAVIMAS (v2)

`_make_product_key()` versija, integruota į `server.py`, yra **identiškas v2 kodas**, kuris praėjo 48/48 testų (test_intent_validation.py). Patikrintos ištaisytos klaidos:

| Klaida | v1 | v2 (integruota) |
|--------|-----|-----------------|
| Brand neištrauktas iš query | `"LEGO 76430"` → `":76430"` | `"lego:76430"` ✅ |
| Brūkšneliniai kodai sulaužyti | `"sony-wh-1000xm5"` | `"sony:wh-1000xm5"` ✅ |
| /EF sufixas neišvalytas | `"rb34c600esaef"` | `"rb34c600esa"` ✅ |
| Lietuviški simboliai ištrynami | `"okoladas"` | `"šokoladas"` ✅ |

`_UNIT_TOKEN_RE` paimama iš `server.py` (apibrėžta line 580) — nėra duplikacijos.

---

## 5. RESURSŲ NAUDOJIMAS

| Resursas | Poveikis |
|---------|---------|
| ScraperAPI kreditai | **0** — intent logging neskrapa |
| Anthropic/OpenAI tokenai | **0** — nėra AI kvietimų |
| Supabase kvietimai | **+1 INSERT** per paiešką (analogiškai save_prices_to_supabase) |
| Paieškos laikas (vartotojui) | **0 ms papildoma** — daemon thread, nelaukia |
| Serverio thread'ai | +1 trumpalaikis daemon thread per paiešką (tos pačios praktikos kaip ir anksčiau) |

**Išvada:** Resursų kaina minimali ir identiška jau egzistuojančiam `save_prices_to_supabase` pattern'ui.

---

## 6. FRONTEND PAKEITIMAI

`index.html` pakeitimai:

1. `let _currentSearchId = null;` — globalus kintamasis intent ID saugojimui
2. SSE `complete` handler: `_currentSearchId = msg.payload.search_id || null;` — išsaugo ID iš serverio atsakymo
3. `trackClick()`: siunčia `intent_id: _currentSearchId` su `/api/track` — susieja paspaudimą su paieška

**Rizika:** Jei `search_id` nėra payload'e (cache hit atveju), `_currentSearchId` = `null` → `/api/track` siunčia `intent_id: null` → backend sąlyga `if intent_id and shop:` neįvykdoma → jokio Supabase kvietimo. ✅ Saugu.

---

## 7. PAKEITIMŲ APIMTIS

Paveikti failai:
- `server.py`: +120 eilučių (import uuid/datetime, 6 helper funkcijos, 3 integracijų vietos)
- `index.html` (goody-app): +3 eilutės

Nepaveikti failai:
- Visi kiti `.py` failai
- Visos esamų funkcijų signatūros
- Visi API endpoint'ai (tik papildyta `/api/track`)

---

## VERDIKTAS

| Kriterijus | Rezultatas |
|-----------|-----------|
| Testai nesulaužyti | ✅ 0 naujų klaidų |
| Fire-and-forget | ✅ Patvirtinta kodu |
| Schema atitikimas | ✅ 100% |
| product_key v2 | ✅ 48/48 PASS |
| Resursai | ✅ Minimali kaina |

**✅ ŽALIA — saugu merge į main ir deploy per Render.**
