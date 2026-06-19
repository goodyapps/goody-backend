# TEST_COVERAGE.md
**Data:** 2026-06-19 (naktinis auditas)  
**Šaka:** night-hardening

---

## Dabariniai testų failai

| Failas | Aprėptis | Testų skaičius |
|---|---|---|
| `test_pipeline.py` | `is_relevant_result` (Layer 1, 500 atvejų) + live HTTP (Layer 2, 20) | 520 |
| `test_accessory_fix.py` | Fix A/C (LED aksesuarų filtras, kainų sanity) | 29 |
| `test_buylink_fix.py` | Fix A (URL validacija) + Fix B (sponsored detection, ASIN) | 33 |
| `test_price_validation.py` | `validate_price` + `parse_price` | ~40 |
| `test_matching.py` | `is_relevant_result` papildomai (importuoja iš server.py) | ~60 |
| **`test_core_functions.py`** | `normalize_query`, `deduplicate_by_shop`, `_short_amazon_query` | **20 (nauja)** |

**Iš viso:** ~702 testai

---

## Padengtos funkcijos ✅

| Funkcija | Testų failas |
|---|---|
| `is_relevant_result` | test_pipeline.py, test_matching.py, test_accessory_fix.py |
| `validate_price` / `parse_price` | test_price_validation.py |
| `post_process` Fix C (accessory reject) | test_accessory_fix.py |
| `_walk_for_products` URL validation | test_buylink_fix.py |
| `_scrape_elesen_from_html` URL validation | test_buylink_fix.py |
| Sponsored detection + ASIN mismatch | test_buylink_fix.py |
| `normalize_query` | **test_core_functions.py (nauja)** |
| `deduplicate_by_shop` | **test_core_functions.py (nauja)** |
| `_short_amazon_query` | **test_core_functions.py (nauja)** |

---

## NETESTUOTOS kritinės funkcijos ⚠️

### 1. `post_process` pagrindinė logika

`post_process` yra viena svarbiausių funkcijų — sprendžia verdiktą, skaičiuoja sutaupymą, nustato "Best Deal". **Nėra jokių testų** išskyrus Fix C dalį (accessory reject).

**Nepadengta:**
- Verdikto skaičiavimas (Best Deal, Good Deal)
- Sutaupymo procentas
- `is_cheapest`, `is_best_value`, `is_top_rated` žymėjimai
- `is_suspicious` logika (mažiausia kaina < 40% mediainos)

### 2. `_walk_for_products` SPA JSON ėjimas

Testai turi URL validacijos logiką (test_buylink_fix.py), bet ne patį SPA walkery.

**Nepadengta:**
- JSON rekursija gyliui iki 12
- Kainų parsavimas iš įvairių laukų
- Img / rating ekstrakcija iš SPA JSON

### 3. `_static_translate` / `claude_translate`

Vertimo logika visiškai netestuota.

**Nepadengta:**
- LT → DE vertimas statiniame žodyne (5000+ atvejų)
- Fallback į Claude API kai žodynas nepavyksta
- Kokybė: ar vertimas semantiškai teisingas

### 4. `validate_results_with_ai`

AI validacijos wrapper — testuoti sunku (reikia API key), bet galima testuoti su mock.

### 5. Barcode lookup

`resolve_query` + `scrape_barcode` — naudoja OpenFoodFacts ir UPCItemDB. Nėra testų.

### 6. `_model_code_variants` (retry cascade)

Funkcija generuoja modelio kodo variantus: "RB34C600ESA" → "RB34C600". Nėra testų.

### 7. `get_category_icon` / `classify_product_cheap`

Kategorijos atpažinimas ir ikonos parinkimas. Nėra testų.

---

## Nauja: `test_core_functions.py` (šioje šakoje)

Padengtos 3 funkcijos kurios anksčiau nebuvo testuotos:

### `normalize_query` — 8 testai

- `"kur pirkti iPhone 16"` → `"iPhone 16"` ✅
- `"buy cheap Samsung Galaxy S24"` → `"Samsung Galaxy S24"` ✅
- `"Sony WH-1000XM5"` → `"Sony WH-1000XM5"` (nepakeistas) ✅
- `"pigiausias iPhone 15 128GB"` → `"iPhone 15 128GB"` ✅
- Whitespace trim ✅
- Review noise strip ✅
- Empty string → empty ✅
- Pure noise → original išsaugomas ✅

### `deduplicate_by_shop` — 5 testai

- 3 Amazon.DE įrašai → 1 (pigiausias €79.99) ✅
- 2 Elesen.lt → 1 (pigiausias €85.00) ✅
- Vienas rezultatas → nepakeistas ✅
- Tuščias sąrašas → tuščias ✅

### `_short_amazon_query` — 7 testai

- Modelio kodas (76430) išsaugomas ✅
- Brand (LEGO) išsaugomas ✅
- iPhone 15 128GB → 15 ir 128 išsaugomi ✅
- Samsung RB34C600ESA — brand + modelis ✅
- Dyson V15 — brand + model ✅

---

## Rekomenduojami ateities testai (neatlikti šioje šakoje)

### A. `post_process` unit testai (AUKŠTAS prioritetas)

```python
# Pseudokodas:
results = [
    {"shop": "Amazon.DE", "price": 79.99, "product_title": "Sony WH-1000XM5"},
    {"shop": "Elesen.lt",  "price": 89.99, "product_title": "Sony WH-1000XM5"},
]
output = post_process(results, "Sony WH-1000XM5", ai_data={}, price_history={})
assert output["results"][0]["is_cheapest"] == True
assert output["price_min"] == 79.99
assert "%" in output.get("savings_pct", "")
```

### B. `_model_code_variants` testai (VIDUTINIS prioritetas)

```python
assert "RB34C600" in _model_code_variants("Samsung RB34C600ESA")
assert "76430" in _model_code_variants("LEGO 76430")
```

### C. `_walk_for_products` testai su synthetic JSON (VIDUTINIS)

Sukurti sintetinį SPA JSON ir tikrinti ar produktai teisingai ištraukiami.

---

## Testų paleidimas (visi iš karto)

```bash
python test_buylink_fix.py && python test_core_functions.py && python test_accessory_fix.py
```

Layer 1 (lėčiau, importuoja server.py):
```bash
python test_pipeline.py
python test_price_validation.py
python test_matching.py
```
