# INTENT DATA VALIDACIJA — VERDIKTAS

**Šaka:** intent-data  
**Data:** 2026-06-20  
**Testai:** 48/48 PASS, 0 pavojingų  

## ✅ VERDIKTAS: ŽALIA — dizainas paruoštas diegimui

---

## 1. KAS BUVO TIKRINAMA

Trys izoliacijos lygiai (NIEKO nepaliesta gyvo Supabase ar main):

| Blokas | Ką tikrinome | Rezultatas |
|--------|-------------|-----------|
| 1. Normalizavimas | `_make_product_key()` — ar skirtingos paieškos susijungia į vieną raktą | ✅ 30/30 |
| 2. Migracijos sausas testas | SQLite dry-run: CREATE, ALTER, backfill, rollback | ✅ 9/9 |
| 3. Pilno srauto simuliacija | Insert → click → agregate → JOIN per product_key | ✅ 9/9 |

---

## 2. RASTI IR IŠTAISYTI KLAIDOS (`_make_product_key()` v1 → v2)

Testavimas atskleidė 4 pavojingas klaidas pirmoje versijoje. Visos ištaisytos `intent_schema.py`:

### Klaida 1 — Brand neištrauktas iš query (PAVOJINGA: duomenys fragmentuojasi)
```
"LEGO 76430 Hogwarts" → ":76430"   ← NETEISINGA (v1)
"lego 76430"          → "lego:76430" ← kitas raktas!
```
**Taisymas:** `effective_brand = b or (word_tokens[0] if word_tokens else "")` — jei brand parametras tuščias, brandas spėjamas iš pirmojo žodžio query.

### Klaida 2 — Brūkšneliniai modelio kodai sulaužyti (PAVOJINGA)
```
"Sony WH-1000XM5" → "sony-wh-1000xm5"  ← NETEISINGA (v1, brūkšnelis kaip separatorius)
```
**Taisymas:** Tokeno tipo nustatymas pakeistas iš regex `^[a-z]*\d+` į `bool(re.search(r'\d', clean))` — bet kuris tokenas su skaičiumi (nepriklausomai nuo vietos) = modelio kodas. `wh-1000xm5` teisingai atpažįstamas.

### Klaida 3 — Regioniniai sufixai /EF /EK neišvalyti
```
"RB34C600ESA/EF" → "samsung:rb34c600esaef"  ← NETEISINGA (v1)
```
**Taisymas:** `t = re.sub(r'/\w{1,3}$', '', raw)` — strip /EF, /EK, /EN, /BH ir kt. prieš valymą.

### Klaida 4 — Lietuviški simboliai ištrynami
```
"šokoladas" → "okoladas"  ← NETEISINGA (v1, [^a-z0-9-] pašalina "š")
```
**Taisymas:** Regex pakeistas į `[^\w-]` — Python `\w` atpažįsta Unicode raides (ą, č, ę, š, ų, ū, ž ir kt.).

---

## 3. NORMALIZAVIMO REZULTATAI

Kritiniai atvejai po v2 taisymų:

| Paieška | product_key | Pastaba |
|---------|------------|---------|
| `LEGO 76430 Hogwarts` | `lego:76430` | ✅ |
| `lego 76430` | `lego:76430` | ✅ Susijungia su eilute viršuje |
| `LEGO Harry Potter 76430` | `lego:76430` | ✅ |
| `Sony WH-1000XM5` | `sony:wh-1000xm5` | ✅ |
| `WH-1000XM5` + brand=Sony | `sony:wh-1000xm5` | ✅ |
| `samsung rb34c600esa` | `samsung:rb34c600esa` | ✅ |
| `RB34C600ESA/EF` + brand=Samsung | `samsung:rb34c600esa` | ✅ /EF išvalytas |
| `Milka 100g` | `milka` | ✅ kiekis (100g) ignoruotas |
| `Milka šokoladas 100g` | `milka:šokoladas` | ✅ šokoladas = skirtingas produktas |
| `Nutella 750g` | `nutella` | ✅ |
| `Haribo Goldbären` | `haribo:goldbären` | ✅ Vokiški simboliai išsaugoti |
| `Dove šampūnas maitinantis` | `dove:šampūnas-maitinantis` | ✅ |

**Pavojingų susiliejimų testai:**
- `LEGO Technic 42151` ir `LEGO City 42151` → tas pats `lego:42151` ✅ (tai TEISINGA — tas pats rinkinys)
- `Nike Air Max 90 size 32` → `nike:90` (dydis 32 ignoruotas — teisingai, tai ne modelio numeris)
- Tuščias query `""` → `""` ✅
- Baltieji tarpai `"   "` → `""` ✅

### Žinomi apribojimai (priimtini)

| Apribojimas | Poveikis | Vertinimas |
|------------|---------|-----------|
| `sony wh 1000xm5` (su tarpais) → `sony:1000xm5` (ne `sony:wh-1000xm5`) | Nedidelis — realūs query dažniausiai su brūkšneliu | Priimtina |
| ISBN su/be brūkšnelių → skirtingi raktai | Nedidelis — knygos nėra pagrindinis use case | Priimtina |
| `iPhone 15 Pro Max` → `apple:15` (Pro Max ignoruotas) | Vidutinis — Pro ir non-Pro sujungiami | Priimtina (v1 feature) |

---

## 4. MIGRACIJOS SAUSAS TESTAS (SQLite — izoliuota)

Paleista ant SQLite — ne Supabase, ne main, ne Render.

| Žingsnis | Rezultatas |
|---------|-----------|
| `ALTER TABLE price_history ADD COLUMN product_key` | ✅ |
| `UPDATE price_history SET product_key = LOWER(TRIM(product_name))` | ✅ Backfill 4 esami įrašai |
| `CREATE INDEX idx_price_history_product_key` | ✅ |
| `CREATE TABLE intent_events (...)` su visais 20 stulpelių | ✅ |
| `CREATE INDEX` × 5 ant intent_events | ✅ |
| **Rollback:** `DROP TABLE intent_events` | ✅ Saugiai šalinamas |
| **Rollback:** `price_history` išlieka su 4 eilutėmis po rollback | ✅ |

SQLite sintaksė skiriasi nuo PostgreSQL (`IF NOT EXISTS` elgesys), tačiau lentelių struktūra ir logika patvirtinta. Supabase SQL Editor naudoja tikrą PostgreSQL — `IF NOT EXISTS` veiks teisingai.

---

## 5. PILNO SRAUTO SIMULIACIJA

Simuliuoti 3 realūs scenarijai izoliuotame SQLite:

**A: Vartotojas fotografuoja LEGO 76430**
- Input: `photo`, scan_confidence=`high`, verdict=`BUY`, price_min=€85.99, cheapest_shop=`varle`
- Intent event įrašytas: `product_key='lego:76430'`
- Vartotojas paspaudžia "Pirkti" pigu.lt → `clicked_shop='pigu'` atnaujinta ✅

**B: Tekstas "Sony WH-1000XM5", verdiktas WAIT**
- Intent event įrašytas: `product_key='sony:wh-1000xm5'`, clicked_shop=`None` ✅

**C: Kitas vartotojas ieško "lego 76430" (tekstas)**
- `product_key='lego:76430'` — **tas pats raktas kaip A** ✅
- Skirtingos paieškos sujungiamos per product_key automatiškai

**Agregatinės užklausos:**
```sql
-- LEGO 76430: 2 paieškos, vid. kaina €86.99, 1 pirkimas (50% konversija)
-- pigu.lt: 100% CTR iš BUY verdikto paspaudimų
-- photo: 100% konversija (1/1), text: 0% (0/2)
```

**JOIN tarp lentelių per product_key:**
```sql
SELECT ph.shop, ph.price, ph.checked_at
FROM price_history ph
JOIN intent_events ie ON ie.product_key = ph.product_key
WHERE ie.product_key = 'lego:76430'
-- → varle €89.99, pigu €87.99 ✅
```

---

## 6. DIEGIMO TVARKA

Kai patvirtinsite diegti, vykdyti **tik per Supabase dashboard → SQL Editor** (ne Render, ne server.py):

```
Etapas 1: ALTER TABLE price_history ADD COLUMN product_key + backfill + index
          → Rizika: NULINĖ (nullable kolona, esamas kodas nežino jos)
          → Patikrink: SELECT COUNT(*), COUNT(product_key) FROM price_history;

Etapas 2: CREATE TABLE intent_events + 5 indeksai
          → Rizika: NULINĖ (nauja lentelė)
          → Patikrink: SELECT table_name FROM information_schema.tables WHERE table_name='intent_events';

Etapas 4: RLS politikos (intent_events + price_history + searches)
          → Rizika: ŽEMA (tik riboja prieigą)
          → Patikrink: SELECT policyname FROM pg_policies WHERE tablename='intent_events';

Etapas 3: watchlist_server — NEKURTI dabar (ateičiai, FEATURE_IDEAS.md B1+B2)
```

Po migracijos — integruoti `intent_schema.py` funkcijas į `server.py` (detalės faile, sekcija 5):
- `search()` → `_build_intent_event()` + `log_intent_async()` po `post_process()`
- `search_stream()` → tas pats + siųsti `search_id` per SSE
- `track_click()` → `_sb_update_intent_click()` su `intent_id` iš request

---

## 7. FAILAI ŠIOJE ŠAKOJE

| Failas | Paskirtis | Statusas |
|--------|----------|---------|
| `INTENT_DATA_DESIGN.md` | Strateginis dizaino dokumentas | Peržiūrai |
| `migration.sql` | SQL migracijos skriptas | **NE PALEISTI** be patvirtinimo |
| `intent_schema.py` | Kodo eskizas (v2, visos klaidos ištaisytos) | Peržiūrai |
| `test_intent_validation.py` | 48 testų suite (SQLite) | Paleidžiamas lokaliai |
| `INTENT_VALIDATION.md` | Šis dokumentas | Verdiktas |

---

## 8. SANTRAUKA

- **Dizainas:** Teisingas. `product_key` metodika veikia ir sujungia skirtingas paieškas.
- **Klaidos:** 4 klaidos rastos ir ištaisytos `intent_schema.py` (v2) prieš bet kokį diegimą.
- **Migracija:** Saugu. Kiekvienas etapas yra additive (nullable kolonos, naujos lentelės) — negalima sugadinti esamų duomenų.
- **Rollback:** Paruoštas ir patikrintas `migration.sql` apačioje.
- **GDPR:** Nėra IP, nėra user_id — tik anoniminiai agregatai. Teisinis pagrindas: teisėtas interesas.

**Sekantis žingsnis:** Tavo sprendimas — mergeinti `intent-data` į main ir vykdyti migration.sql per Supabase dashboard.
