# MORNING_BRIEF.md
**Data:** 2026-06-19 | **Naktinis darbas (~5 val)**  
**Paruošė:** Autonominis nakties agentas

---

## 1. ELESEN VERDIKTAS

**Bug:** "LEGO 76430 Hogwarts" rodė Nintendo Switch žaidimą €34.99 su "Buy now" nuoroda į žaidimą.

**Priežastis (Root cause):**
- Elesen naudoja **Nosto** JS paieškos platformą — statinis HTML yra tuščias, 0 produktų
- ScraperAPI `render_js=True` **kartais** suspėja sugauti Nosto AJAX rezultatus (~7s timeout), **kartais** ne
- Kai sugauna: Elesen Nosto grąžina Switch žaidimą su "76430" katalogo klaida pavadinime
- `is_relevant_result` praleido žaidimą — "76430" buvo ir query, ir title
- `is_relevant_result` netikrino **produkto tipo** — Nintendo Switch žaidimas praeina kai LEGO query

**Pataisymas (type-filter šaka):**
- Pridėtas `_PRODUCT_TYPE_SIGNALS` — gaming platform title + ne-žaidimo query → reject
- 30/30 testų PASS (test_type_filter.py)
- `or all_results` fallback (line 6267) apeina type-filter — dokumentuota ELESEN_ROOT_CAUSE.md

**Šaka:** `type-filter` — paruošta peržiūrai, ne merged

---

## 2. PENTEST TOP FINDINGS

**Šaka:** `security-night` | **Failas:** PENTEST_AUDIT.md

| Prioritetas | Radinys | Rizika | Statusas |
|---|---|---|---|
| P1 | VPN rotacija apeinant rate limit (scan-image, identify-product) | 🔴 AUKŠTA | Dokumentuota |
| P2 | Supabase RLS neįjungta (direct write galimas) | 🟡 VIDUTINĖ | Reikia Supabase dashboard |
| P3 | /api/track be rate_limit (stats manipulation) | 🟡 VIDUTINĖ | ✅ **PATAISYTA** |
| P4 | /api/popular-searches be rate_limit | 🟢 ŽEMA | ✅ **PATAISYTA** |
| P5 | DoS per 14MB nuotraukas (koordinuota ataka) | 🟡 VIDUTINĖ | Dokumentuota |
| P6 | Prompt injection per query (žema praktinė rizika) | 🟢 ŽEMA | Dokumentuota |

**Pataisymai šioje šakoje:** `@rate_limit` pridėtas `/api/track` ir `/api/popular-searches`.

**Pataisymų padariniai:** Minimalūs — `/api/track` kviečiamas 1x per "Buy now" paspaudimą; `/api/popular-searches` — 1x puslapio krovimui. Rate limit 20/min + 200/day per IP — neblokuos teisėtų.

---

## 3. TESTAI PARAŠYTI

**Šaka:** `night-tests` | **Failas:** test_night_coverage.py

**70/70 testų PASS.** `python test_night_coverage.py`

| Sritis | Testų sk. | Ką tikrina |
|---|---|---|
| `_UNIT_TOKEN_RE` regex | 26 | Fiziniai vienetai (g, ml, kg) atpažinti; modelio kodai nepažymėti |
| Unit filter (is_relevant_result) | 6 | Maisto/kosmetikos query su gramais/ml veikia be unit title |
| Model code matching | 8 | WH-1000XM5 hyphen norm, 76430 set number, 128GB |
| Accessory filter | 7 | "for X" patterns, charger/cable reject; user-requested accessory allow |
| Product-type signals | 10 | LEGO vs Nintendo Switch reject; game query allow; MacBook not blocked |
| Query normalization | 9 | "kur pirkti", "buy cheap", "pigiausias", "review" stripped |
| Short Amazon query | 4 | 76430 set number preserved, Samsung model code preserved |

---

## 4. P1_DIVERGENCE SANTRAUKA

**Šaka:** `security-night` | **Failas:** P1_DIVERGENCE.md

**identify-product vs scan-image skiriasi** 4 svarbiais aspektais:

| Aspektas | identify-product | scan-image |
|---|---|---|
| Modeliai | Gemini (free) + Haiku lygiagrečiai | Tik claude-haiku (env var) |
| Prompt | Lankstus (screenshotai ✓) | Griežtas (NEVER guess) |
| Query | `brand + product_name` (semantinis) | `brand + product_code` (tikslus) |
| Fallback | 3 pakopų (Gemini→Haiku→OCR) | Nėra (iš karto 422) |

**Divergencija LEGO kategorijoje: ~35%** — identify generuoja "LEGO Harry Potter Hogwarts" (semantinis), scan generuoja "LEGO 76430" (tikslus). is_relevant_result veikia geriau su kodo tipo query.

**Greitas fix (R1, žema rizika):** Kai identify-product gauna `model_code` iš AI → naudoti `brand + model_code` kaip search query (kaip scan-image). Šiuo metu AI-generated search_query dažnai ignoruoja kodą.

---

## 5. CODE HEALTH TOP ISSUES

**Šaka:** `security-night` | **Failas:** CODE_HEALTH.md

| # | Problema | Sunkumas | Quick fix? |
|---|---|---|---|
| 1 | `_scan_ph_exec` neuždarytas scan_image (~line 7183) | 🟡 Vidutinis | ✅ 1 eilutė |
| 2 | ~15 silent `except Exception: pass` DB/Supabase vietose | 🟡 Vidutinis | ~10 eilučių |
| 3 | `_fx_cache` thread race condition | 🟡 Vidutinis | 5 eilutės |
| 4 | `ACCESSORY_KEYWORDS` ir `_ACCESSORY_MATCH_WORDS` du sąrašai | 🟡 Vidutinis | Peržiūrai |
| 5 | `print()` vietoj `logging` (97+ vietos) | 🟢 Žemas | Didelis refactor |

---

## 6. REKOMENDUOJAMAS MERGE EILIŠKUMAS

```
1. security-night → main   (žema rizika: +@rate_limit 2 endpoints, 3 .md failai)
                            PRIEŠ: python test_pipeline.py
                            PRIEŠ: python test_night_coverage.py
                            PATIKRINTI: ar rate_limit neblokuoja normaliems

2. type-filter → main      (žema-vidutinė rizika: +_PRODUCT_TYPE_SIGNALS)
                            PRIEŠ: python test_type_filter.py (30/30)
                            RIZIKA: ar MacBook/Notebook false positives?
                            STEBĖTI: ar žaidimų query tinkamai veikia

3. night-tests → main      (zero rizika: tik testų failai)

NEMERGE'INTI be papildomos peržiūros:
- deps-update (gunicorn/requests update — deployment rizika)
```

---

## 7. ŠAKOS STATUSAS

| Šaka | Commits | Pushinta | Turinys |
|---|---|---|---|
| `security-night` | +4 naktį | ✅ | PENTEST_AUDIT.md, P1_DIVERGENCE.md, CODE_HEALTH.md, MORNING_BRIEF.md, @rate_limit fix |
| `type-filter` | +2 anksčiau | ✅ | _PRODUCT_TYPE_SIGNALS, ELESEN_ROOT_CAUSE.md, test_type_filter.py |
| `night-tests` | +1 naktį | ✅ | test_night_coverage.py (70 testų) |
| `main` | nepakeista naktį | ✅ | — |

---

## 8. KĄ DARYTI RYTĄ

**Privaloma prieš bet ką mergint:**
1. `python test_night_coverage.py` — turi būti 70/70 PASS
2. `python test_type_filter.py` — turi būti 30/30 PASS
3. Supabase dashboard: įjungti RLS ant `price_history` ir `searches` lentelių

**Rekomenduojama:**
4. Patikrinti ar Elesen `/rezultatus/LEGO%2076430%20Hogwarts` URL grąžina geresnį HTML
5. Render logs: ieškoti `[Elesen]` eilučių su ScraperAPI — kiek dažnai grąžina 0 vs produktus
6. Pataisyti `_scan_ph_exec` shutdown (CODE_HEALTH H4, 1 eilutė)

**Gali palaukti:**
- `print()` → `logging` migracija
- Scraperių unifikacija
- ACCESSORY sąrašų sujungimas
