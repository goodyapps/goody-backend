# BUYLINK_FIX_CHECK.md
**Šaka:** `buylink-fix`  
**Data:** 2026-06-19  
**Tikrinimo tipas:** Logikos testai (be HTTP) + Layer 1 baseline + Layer 2 (prieš deploy)  
**Commits:** `50b3636` (initial), `asinfix` (B3 enhanced)

---

## VERDIKTAS: ŽALIA — saugu merginti

Logika veikia teisingai visais atvejais. Jokių regresijų. URL validacija atmeta homepage link'us. Sponsored+neteisingas modelio kodas atmetamas. Tikri produktai ir teisingi sponsored nepradingo.

**Išlyga:** Sponsored label CSS selektoriai (`s-sponsored-label-info-icon`, `puis-sponsored-label-text`) priklauso nuo Amazon HTML struktūros — jei Amazon pakeitė klasių pavadinimus, aptikimas gali veikti tik iš dalies. Fix suveiks pilnai po deploy kai bus matomi realūs Render logai.

---

## 1. Tiksliniai buylink-fix testai (test_buylink_fix.py)

**Rezultatas: 33/33 PASS**

### Fix A — Tuščio URL atmetimas (_walk_for_products, visos SPA parduotuvės)

| # | Scenarijus | Laukiamas | Gautas | Status |
|---|---|---|---|---|
| 1 | slug="" → SKIP | SKIP | SKIP | ✅ PASS |
| 2 | slug="" kitoje parduotuvėje (1a.lt) → SKIP | SKIP | SKIP | ✅ PASS |
| 3 | Santykinė nuoroda "/lt/products/lego-76430" → KEEP | KEEP | KEEP | ✅ PASS |
| 4 | Pilna nuoroda "https://www.elesen.lt/..." → KEEP | KEEP | KEEP | ✅ PASS |
| 5 | 1a.lt santykinė nuoroda → KEEP | KEEP | KEEP | ✅ PASS |
| 6 | 1a.lt tuščias slug → SKIP | SKIP | SKIP | ✅ PASS |
| 7 | slug="/" → resolves to homepage → SKIP | SKIP | SKIP | ✅ PASS |

**7/7 PASS.** Tuščias URL teisingai atmetamas visose SPA parduotuvėse.

### Fix A — Tuščio href atmetimas (_scrape_elesen_from_html DOM kelias)

| # | Scenarijus | Laukiamas | Gautas | Status |
|---|---|---|---|---|
| 1 | href="" → SKIP | SKIP | SKIP | ✅ PASS |
| 2 | href="/" → SKIP | SKIP | SKIP | ✅ PASS |
| 3 | href="#" → SKIP | SKIP | SKIP | ✅ PASS |
| 4 | href="/lt/products/lego-76430-hogwarts-peles-narvas" → KEEP | KEEP | KEEP | ✅ PASS |
| 5 | Pilna https://... nuoroda → KEEP | KEEP | KEEP | ✅ PASS |
| 6 | Santykinė "/lt/prekes/samsung" → KEEP | KEEP | KEEP | ✅ PASS |

**6/6 PASS.** Elesen DOM kelias teisingai atskiria productus nuo homepage.

### Fix B1/B2 — Sponsored + konkuruojantis modelio kodas (Amazon)

| # | Scenarijus | Laukiamas | Gautas | Status |
|---|---|---|---|---|
| 1 | Sponsored + 76430 (query) + 76451 (title) → SKIP | SKIP | SKIP | ✅ PASS |
| 2 | Sponsored + 76430 (query) + "432 pieces" (3 skaitmenys) → KEEP | KEEP | KEEP | ✅ PASS |
| 3 | ORGANIC (ne sponsored) + du kodai title → KEEP | KEEP | KEEP | ✅ PASS |
| 4 | Sponsored + TIKTAI 76430 title (teisingas prod.) → KEEP | KEEP | KEEP | ✅ PASS |
| 5 | Sponsored + query be numerinio kodo (iPhone 15 Pro Max) → KEEP | KEEP | KEEP | ✅ PASS |
| 6 | Sponsored + iPhone 15 128GB (128 = 3 skaitmenys, ne bare code) → KEEP | KEEP | KEEP | ✅ PASS |
| 7 | Sponsored + Samsung RB34C600ESA (alfanumerinis, ne bare digit) → KEEP | KEEP | KEEP | ✅ PASS |
| 8 | Sponsored + 9999 (query) + 8888 (title, 4 skaitmenys) → SKIP | SKIP | SKIP | ✅ PASS |

**8/8 PASS.** Ypač svarbūs:
- **#1**: LEGO 76430 → 76451 bug atvejis → **ATMETAMAS** ✅
- **#3**: Organinis (ne sponsored) su dviem kodais → **IŠSAUGOMAS** ✅
- **#4**: Teisingas sponsored (tik 76430 title) → **IŠSAUGOMAS** ✅
- **#6, #7**: iPhone 128GB ir Samsung alphanumeric → **IŠSAUGOMI** ✅

### Fix B3 — ASIN suderinamumo korekcija

| # | Scenarijus | Laukiamas | Gautas | Status |
|---|---|---|---|---|
| 1 | item_asin == url_asin → jokios korekcijos | "B0ABCDE1234" | "B0ABCDE1234" | ✅ PASS |
| 2 | item_asin ≠ url_asin → koreguoja į item_asin | "B0ABCDE1234" | "B0ABCDE1234" | ✅ PASS |
| 3 | item_asin tuščias → paliekami url_asin | "B0ABCDE1234" | "B0ABCDE1234" | ✅ PASS |
| 4 | url_asin tuščias, item_asin yra → **rekonstruoja URL** | "B0ABCDE1234" | "B0ABCDE1234" | ✅ PASS |

**4/4 PASS.** Pastaba: #4 — papildomas patobulinimas: jei link ekstrakcija nepavyko, bet `data-asin` yra → URL rekonstruojamas iš item ASIN (vietoj skip). Tai pagerina atsparumą.

### Regresijos patikra — ankstesni fix'ai

| # | Scenarijus | Laukiamas | Gautas | Status |
|---|---|---|---|---|
| 1 | LED kit rejected (accessory-fix) | FALSE | FALSE | ✅ PASS |
| 2 | LED light set rejected | FALSE | FALSE | ✅ PASS |
| 3 | TIKRAS LEGO 76430 praeina | TRUE | TRUE | ✅ PASS |
| 4 | iPhone 15 128GB praeina | TRUE | TRUE | ✅ PASS |
| 5 | Samsung RB34C600ESA praeina | TRUE | TRUE | ✅ PASS |
| 6 | Sony WH-1000XM5 praeina | TRUE | TRUE | ✅ PASS |
| 7 | PS5 controller praeina | TRUE | TRUE | ✅ PASS |
| 8 | Dyson V15 Detect praeina | TRUE | TRUE | ✅ PASS |

**8/8 PASS.** Jokių regresijų tarp tikrų produktų.

---

## 2. Layer 1 baseline (test_pipeline.py, is_relevant_result logika)

Šie testai naudoja **inlined** seną kodo versiją — tikrina bazinę is_relevant_result logiką, kuri buylink-fix NEKEIČIA.

| Kategorija | rel_pass | acc_pass | unit_bug | short_q_trunc |
|---|---|---|---|---|
| appliances | 20/20 | 18/20 | 0 | 0 |
| electronics | 20/20 | 18/20 | 0 | 10 |
| lego | 20/20 | 16/20 | 0 | 6 |
| food | 20/20 | 20/20 | 0 | 6 |
| cosmetics | 20/20 | 20/20 | 0 | 15 |
| clothing | 20/20 | 20/20 | 0 | 12 |
| books | 18/20 | 20/20 | 0 | 14 |
| household | 20/20 | 20/20 | 0 | 13 |
| sports | 20/20 | 20/20 | 0 | 4 |
| baby | 20/20 | 20/20 | 0 | 11 |
| **TOTAL** | **198/200** | **192/200** | **0** | **91** |

**Identiškai kaip prieš buylink-fix.** Jokių regresijų.

- 2 rel failures — knygų kategorija, pre-existing, nėra ryšio su šiais pakeitimais
- URL/sponsored logika is_relevant_result NEKEIČIA → Layer 1 neturėjo ir negali keistis

---

## 3. Layer 2 live HTTP (goody-backend.onrender.com — PRODUCTION, ne buylink-fix)

**Svarbu: Layer 2 tikrina PRODUCTION serverį (main branch), o ne buylink-fix. Rezultatai atspindi PRE-deploy būklę.**

```
Summary: L1 rel_fail=2/500  L2 ok=14/20 zero=6/20
```

| Testas | Rezultatas | Pastabos |
|---|---|---|
| Samsung RB34C600ESA | 0 | Pre-existing (specifinis modelis, retas) |
| Bosch WAX32EH0 | 0 | Pre-existing |
| Sony WH-1000XM5 | 3 ok | |
| Apple iPhone 15 Pro 128GB | 1 ok | |
| LEGO Technic 42170 | 1 ok | |
| **LEGO Harry Potter 76430** | **0** | Pre-existing — arba Elesen grąžina su tuščiu URL (kurį buylink-fix atmestų), arba nėra paieškos rezultatų. Po deploy galėtų keistis. |
| Milka 100g | 1 ok | |
| Nutella 400g | 1 ok | |
| Dove Shampoo 400ml | 2 ok | |
| Nivea Creme 250ml | 2 ok | |
| Nike Air Max 270 42 | 0 | Pre-existing |
| Adidas Ultraboost 22 | 0 | Pre-existing |
| Atomic Habits James Clear | 1 ok | |
| Clean Code Robert Martin | 1 ok | |
| Dyson V15 Detect | 2 ok | |
| Philips Airfryer XXL HD9860 | 0 | Pre-existing |
| Garmin Forerunner 265 | 2 ok | |
| Polar Vantage V3 | 2 ok | |
| Pampers Premium Care Newborn | 1 ok | |
| Aptamil Profutura 1 800g | 1 ok | |

**L2 = 14/20 — identiškai kaip accessory-fix merge'o bazinis rezultatas.**

Pastaba dėl LEGO 76430: 0 resultado produkciojoje galėtų reikšti, kad Elesen grąžina produktus su tuščiais URL (homepage link'ai), o aksesuarų fix atmeta LED kit'ą. Panašu kad produkcioje Elesen šiai paieška negrąžina validžių URL. Po buylink-fix deploy: Elesen homepage link'ai bus atmetami (kaip ir turėtų), todėl rezultatas bus "0 arba real product" — bet ne "homepage link".

---

## 4. Tikrinimas: ar buy-link logika veikia (prieš deploy)

Kadangi buylink-fix šaka nėra produkcioje, tiesioginio URL testavimo atlikti negalima. Vietoj to — logikos patikrinimas:

### Bug A pataisymas (Elesen homepage)

**Kaip veikia po fix:**
```python
# _walk_for_products (SPA kelias)
if not slug or link.rstrip("/") == base_url.rstrip("/"):
    print(f"[{shop}] skip empty-URL: name='...' slug='...'")
    # → produktas NEĮTRAUKIAMAS
```
```python
# _scrape_elesen_from_html (DOM kelias)
if not href or href in ("/", "#") or link.rstrip("/") == "https://www.elesen.lt":
    print(f"[Elesen item] skip empty-URL href='...' name='...'")
    continue  # → produktas PRALEISTAS
```

Logika testuose: **7/7 + 6/6 PASS.** Produkcioje Render logai rodys `skip empty-URL` kai Elesen grąžina tuščią href.

### Bug B pataisymas (Amazon 76451 vietoj 76430)

**Kaip veikia po fix:**
```python
# Jei Amazon sponsored 76451 ads rodomas 76430 paieškoje:
# Sponsored label → _is_sponsored = True
# Query: "76430" (5 skaitmenys)
# Title: "LEGO Harry Potter 76430 Hogwarts 76451 Privet Drive"
# → _competing = {"76451"} (5 skaitmenys, tas pats ilgis)
# → SKIP: "[Amazon.pl] skip sponsored+competing-model q={'76430'} title={'76430','76451'}"
```

Logika testuose: **8/8 PASS.**

**Riziką kelianti situacija (sponsor label CSS):** Jei Amazon atnaujino sponsored label HTML struktūrą (kitos klasės), `_is_sponsored = False` — tada fix nesuveikia. Bet tai tik silence failure (76451 išliks, bet nebus klaidingai atmetama), ne false positive.

**ASIN konsistencija:**
```python
if item_asin and asin and item_asin != asin:
    # Koreguoja URL į teisingą produktą
elif item_asin and not asin:
    # Rekonstruoja URL kai link extraction nepavyko
```

Logika testuose: **4/4 PASS.**

---

## 5. Logų skaidrumas

Po deploy Render logai rodys:

| Situacija | Logas |
|---|---|
| Elesen produktas su tuščiu URL | `[Elesen.lt] skip empty-URL: name='...' slug=''` |
| Elesen DOM kelias, tuščias href | `[Elesen item] skip empty-URL href='' name='...'` |
| Amazon sponsored + neteisingas modelis | `[Amazon.pl] skip sponsored+competing-model q={'76430'} title={'76430','76451'} name='...'` |
| Amazon ASIN neatitikimas | `[Amazon.pl] ASIN mismatch item=B0XXX link=B0YYY -> correcting name='...'` |
| Amazon jokio URL | `[Amazon.pl] skip no-URL name='...'` |

---

## 6. Pakeitimų suvestinė

| Fix | Failas | Eilutės | Aprašymas |
|---|---|---|---|
| A1 | server.py | ~2032 | `_walk_for_products`: slug tuščias arba homepage → skip |
| A2 | server.py | ~2552 | `_scrape_elesen_from_html`: href tuščias → continue |
| B1 | server.py | ~2735 | `scrape_amazon`: `item_asin = item.get("data-asin")` |
| B2 | server.py | ~2761 | Sponsored label aptikimas (3 CSS selektoriai) |
| B2 | server.py | ~2766 | Sponsored + konkuruojantis kodas → skip |
| B3 | server.py | ~2830 | ASIN mismatch → corrects to item_asin |
| B3+ | server.py | ~2834 | URL tuščias bet item_asin yra → rekonstruoja |
| B4 | server.py | ~2836 | Jokio URL/ASIN po korekcijos → skip |

**Bendri pakeitimai:** 38 papildomos eilutės, 1 pakeista eilutė.

---

## 7. Apibendrinimas

| Patikra | Rezultatas |
|---|---|
| Fix A: Tuščias slug/href → skip | ✅ 13/13 |
| Fix B1: Sponsored label aptikimas | ✅ Logika teisinga (CSS selektoriai) |
| Fix B2: Sponsored + neteisingas kodas → skip | ✅ 8/8 |
| Fix B3: ASIN mismatch → correction | ✅ 4/4 |
| Tikri produktai nepradingo | ✅ 8/8 |
| Teisingi sponsored nepradingo | ✅ Testas #4 (KEEP kai tik query kodas title) |
| Layer 1 regresija | ✅ 0 regresijų (198/200 identiškai) |
| Accessory fix vis dar veikia | ✅ LED kit atmestas |
| Layer 2 baseline | ✅ 14/20 (identiškai) |

**Verdiktas: ŽALIA.** Buylink-fix saugu merginti į main.

Po merge ir Render deploy, patikrinti Render logus:
- Ar matosi `skip empty-URL` kai ieškoma per Elesen
- Ar matosi `skip sponsored+competing-model` jei Amazon grąžina keyword-stuffed ad'ą
- "LEGO 76430" buy-now → turi atidaryti konretų produkto URL (ne homepage)
