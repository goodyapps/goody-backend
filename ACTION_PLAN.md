# ACTION_PLAN.md
**Sukurta:** 2026-06-20 (naktinis apibendrinimas)  
**Šaltiniai:** MORNING_BRIEF, PENTEST_AUDIT, P1_DIVERGENCE, CODE_HEALTH, ELESEN_ROOT_CAUSE, UX_EXPLORATION, MARKET_RESEARCH, FEATURE_IDEAS, PRODUCT_GAPS, TEST_RESULTS  
**Principas:** NIEKO į main be šio plano sekimo

---

## KRITINIS — daryk pirmą (saugumas + gyva app'a)

### K1 — Supabase RLS: tiesioginis rašymas į DB be autentikacijos
**Šaka:** main (Supabase dashboard — ne kodo pakeitimas)  
**Rizika:** 🔴 AUKŠTA — bet ne kodo pakeitimas  
**Laikas:** 5 min  
**Sprendimas:** Render → Supabase dashboard → Tables → `price_history` + `searches` → RLS Enable → politika: `service_role` tik  
**Autonomiškai:** Taip (jei turi Supabase prieigą)  
**Patikrinimas:** Bandyk tiesiogiai POST `https://[projektas].supabase.co/rest/v1/price_history` be rakto → turi gauti 401

---

### K2 — DEBUG_API_KEY nenustatytas Render
**Šaka:** Render env vars  
**Rizika:** 🟡 VIDUTINĖ — `/api/debug-html` endpoint'as grąžina 401 be rakto (gerai saugumui), bet negalima naudoti diagnostikai  
**Laikas:** 2 min  
**Sprendimas:** Render dashboard → Environment → `DEBUG_API_KEY=<stiprus raktas>` (pvz. iš PowerShell: `[System.Web.Security.Membership]::GeneratePassword(32,8)`)  
**Autonomiškai:** Taip

---

## SVARBUS — Elesen tikslumas + šakų merge

### S1 — type-filter merge į main (LEGO žaidimo klaida)
**Šaka:** `type-filter` → `main`  
**Rizika:** 🟡 ŽEMA-VIDUTINĖ — 25 eilutės server.py (_PRODUCT_TYPE_SIGNALS + is_relevant_result)  
**Laikas:** 10 min  
**Ką daryti:**
```
1. git checkout main
2. python test_type_filter.py   → turi būti 30/30 PASS
3. python test_pipeline.py      → turi būti ≥ 490/500 (Layer 1)
4. Jei abu PASS → git merge type-filter
5. git push origin main
6. Stebėk Render logs 10 min po deploy
```
**Autonomiškai:** NE — prašo merge į main (Render auto-deploy paleistas!)  
**Stebėk:** Ar LEGO 76430 Hogwarts rodo rinkinį, ne žaidimą. Ar MacBook nerodo false reject.

---

### S2 — elesen-fix peržiūra (ar keisti `or all_results` → `or []`)
**Šaka:** `elesen-fix` (NAUJA, paruošta per naktį)  
**Rizika:** 🔴 VIDUTINĖ-AUKŠTA — Pakeitus, vartotojai matys 0 rezultatų vietoj klaidingo produkto  
**Laikas:** 20 min peržiūros + testo  
**Ką daryti:**
1. Perklausyk: ar geriau rodyti **klaidingą** produktą ar **0 rezultatų**? Tai produkto sprendimas.
2. Jei "geriau 0 nei klaidinga" → `git merge elesen-fix` TIKTAI PO type-filter merge
3. Jei "geriau kažkas nei nieko" → palik `elesen-fix` šakoje, nemerge'ink

**Patikrinimas prieš merge:**
```bash
# Ryte: Render logai → ieškoti:
grep "\[Elesen\]" render_logs.txt
# Turi matyti arba "N results" (Nosto pavyko) arba "0 results" / klaida

# Arba vienas live testas:
# POST /api/search {"query": "LEGO 76430 Hogwarts"} → ar rodo Switch žaidimą?
# Jei TAIP → type-filter nepadeda (scenario C) → elesen-fix reikia
# Jei NE → type-filter pakankamas
```
**Autonomiškai:** NE — produkto sprendimas

---

### S3 — security-night merge į main (@rate_limit fix + docs)
**Šaka:** `security-night` → `main`  
**Rizika:** 🟢 ŽEMA — Tik 2 eilutės server.py (@rate_limit dekoratoriai) + .md failai (nefunkciniai)  
**Laikas:** 5 min  
**Ką daryti:**
```
1. python test_night_coverage.py  → turi būti 70/70 PASS
2. git checkout main
3. git merge security-night
4. git push origin main
```
**Autonomiškai:** NE — Render auto-deploy  
**Pastaba:** Merge PRIEŠ arba PO type-filter — nėra konflikto (skirtingos failo dalys)

---

### S4 — night-tests merge į main (tik testų failas)
**Šaka:** `night-tests` → `main`  
**Rizika:** 🟢 NULINĖ — tik `test_night_coverage.py` (naujas failas)  
**Laikas:** 2 min  
**Autonomiškai:** NE — Render auto-deploy (bet deploy nekeičia veikimo — testas nėra routes)

---

### S5 — identify-product → naudoti brand+model_code query (R1 fix)
**Šaka:** Nauja šaka nuo main (dar nepadaryta)  
**Rizika:** 🟡 VIDUTINĖ — Keičia identify-product query generavimą  
**Laikas:** 30 min  
**Ką daryti:**  
P1_DIVERGENCE.md Rekomendacija R1:
```python
# server.py: identify_product() funkcijoje
# Po AI response parsing:
model_code = vision.get("model") or vision.get("key_specs_first_code")
if model_code and brand:
    search_query = f"{brand} {model_code}"  # kaip scan-image
else:
    search_query = vision.get("search_query") or f"{brand} {product_name}"
```
**Efektas:** ~35% LEGO divergencija sumažėja iki ~10%  
**Autonomiškai:** Gali būti padaryta — bet reikia peržiūros prieš merge

---

## VERTINGAS — Produkto gerinimas

### V1 — Rusų kalba: pilnas LANGS.ru palaikymas
**Šaka:** Nauja (dar nepadaryta)  
**Rizika:** 🟢 ŽEMA — tik vertimų eilutės, nekeičia logikos  
**Laikas:** 3-4 val (manualus vertimas)  
**Detales:** FEATURE_IDEAS.md B3

---

### V2 — "Kaina prieš X mėn" badge prie rezultatų
**Šaka:** Nauja frontend šaka  
**Rizika:** 🟢 ŽEMA — tik renderResults() modifikacija  
**Laikas:** 1-2 val  
**Detales:** FEATURE_IDEAS.md A1

---

### V3 — _scan_ph_exec.shutdown() thread leak fix
**Šaka:** Atskira šaka (1 eilutė)  
**Rizika:** 🟢 ŽEMA  
**Laikas:** 5 min  
**Kodas:**
```python
# server.py ~7183 (finally block scan_image):
finally:
    scan_executor.shutdown(wait=False)
    _scan_ph_exec.shutdown(wait=False)  # ← PRIDĖTI
```

---

### V4 — Push pranešimai kainų kritimui
**Šaka:** Nauja (didelis darbas)  
**Rizika:** 🟡 VIDUTINĖ — Service Worker + VAPID  
**Laikas:** 2-3 dienos  
**Detales:** FEATURE_IDEAS.md B2

---

## NICE-TO-HAVE — Palaukti

| # | Darbas | Kodėl palaukti |
|---|---|---|
| N1 | Watchlist serverio pusėje | Reikia auth sprendimo pirma |
| N2 | Scraper unifikacija | Didelis refactor, menka nauda |
| N3 | print() → logging | Didelis refactor, veikia ir dabar |
| N4 | ACCESSORY_KEYWORDS deduplication | Menkas poveikis |
| N5 | Latvių/estų parduotuvės | Scraping infrastruktūra |
| N6 | _fx_cache thread lock | Praktinis poveikis labai mažas |

---

## MERGE EILIŠKUMAS (rekomenduojama)

```
ETAPAS 1 — Saugumas (ne Render deploy):
  → Supabase RLS (K1) — Supabase dashboard tik
  → Render DEBUG_API_KEY (K2) — env var tik

ETAPAS 2 — Kodo fix'ai (kiekvienas = Render deploy):
  → security-night → main  (S3, žema rizika, +@rate_limit)
  → night-tests → main     (S4, nulinė rizika, tik testai)
  → type-filter → main     (S1, vidutinė rizika, +type signals)
  → elesen-fix → main      (S2, tik po S1, tik jei produkto sprendimas "geriau 0")

ETAPAS 3 — Produkto gerinimas:
  → R1 fix (S5) → nauja šaka → main
  → V2 badge → main
  → V3 thread fix → main
  → V1 rusų kalba → main (ilgas, bet žema rizika)
```

---

## KLAUSIMAI, KURIE REIKIA TAVĘS

1. **elesen-fix (S2):** Ar geriau rodyti 0 rezultatų ar klaidingą produktą?
2. **S5 (identify R1):** Ar norima keisti identify-product query logiką šią savaitę?
3. **Pardavėjų aprėptis (PRODUCT_GAPS G1):** Koks planas plėsti nuo 8 parduotuvių? Affiliate API ar scraping?
4. **ALLOWED_ORIGINS (K2 susijęs):** Nustatyti CORS domain ribojimą (`ALLOWED_ORIGINS` env var)
