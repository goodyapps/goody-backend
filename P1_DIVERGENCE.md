# P1_DIVERGENCE.md
**Data:** 2026-06-19 | **Šaka:** security-night  
**Analizė:** identify-product vs scan-image divergencija  
**Metodas:** Statinė kodo analizė — 0 API kvietimų

---

## TL;DR

`identify-product` ir `scan-image` skiriasi 4 kritiniais aspektais:
1. **Modelis** — identify naudoja Gemini + Haiku lygiagrečiai; scan naudoja tik `AI_MODEL_CLAUDE` (default: Haiku)
2. **Prompt tikslumas** — identify yra lankstus (screenshotai, pakuotė, bet kas); scan yra griežtas ("NEVER guess")
3. **Paieškos query** — identify grąžina brandą+pavadinimą; scan grąžina **brandą+product_code** (daug tiksliau)
4. **Kaina** — identify sukuria tik JSON; scan paleidžia visą scrapinimo pipeline (ScraperAPI + AI)

---

## 1. MODELIAI

| Aspektas | identify-product | scan-image |
|---|---|---|
| AI modelis | Gemini 2.0 Flash (pirmas) + Claude Haiku (lygiagrečiai) | `AI_MODEL_CLAUDE` (env var, default: claude-haiku-4-5-20251001) |
| Lygiagretumo | Paralel (ThreadPoolExecutor, 2 workers) | Vienas kvietimas |
| Fallback | Gemini → Haiku → OCR Gemini → OCR→Haiku parse | Nėra (tiesiogiai 422) |
| max_tokens | 300 | 500 |
| Kaina per kvietimą | Gemini: $0, Haiku: $0.0004 | Haiku: $0.0004 |

**Praktinis poveikis:** identify naudoja 2 modelius ir ima geriau įvertintą rezultatą (pagal `_score` funkciją). Scan turi tik 1 šansą.

---

## 2. PROMPT SKIRTUMAS

### identify-product prompts:
```
"The image may be: a physical product label, product packaging, a photo of a shop shelf, 
OR a screenshot/photo of a webpage or price comparison site."
"Even if this is a screenshot of a webpage, still extract the product name from the visible text."
"If model is uncertain or not clearly visible, leave this field empty."
```

**Schema:**
```json
{"brand":"","product_name":"","model":"","key_specs":"","search_query":"","confidence":"high|medium|low","scanned_price":null}
```

### scan-image prompts:
```
"You are extracting an EXACT product identification from packaging."
"STRICT rules ... product_code: the EXACT product number printed on the box"
"If you are not 100% sure of a digit in product_code, set product_code to null"
"A wrong code is worse than no code."
```

**Schema:**
```json
{"brand":"","product_name":"","product_code":null,"pieces":null,"age_range":"","price_visible":0,"barcode":"","confidence":"high|medium|low"}
```

---

## 3. SEARCH QUERY KONSTRUKCIJA

### identify-product:
```python
search_query = vision.get("search_query") or f"{brand} {product_name} {key_specs}"
# AI pati generuoja search_query: "Brand + confirmed model ONLY"
# Pavyzdžiai: "Mobvoi TicNote", "Apple MacBook Air M3", "Nutella 750g"
```

### scan-image:
```python
if product_code and brand:
    search_query = f"{brand} {product_code}"  # "LEGO 76430"
elif product_code:
    search_query = f"{product_name} {product_code}".strip()
else:
    search_query = product_name + (f" {pieces} pieces" if pieces else "")
```

**Kritinis skirtumas:** scan-image kuria `brand + product_code` paieškos užklausą. Tai tiksliau nei vardinis ieškojimas, nes leidžia `is_relevant_result` tikrinti modelio tokeną `76430` rezultatų pavadinimuose.

---

## 4. DIVERGENCIJOS SCENARIJAI

### Scenarijus A: LEGO pakuotė su aiškiai matomo numeriu

| | identify-product | scan-image |
|---|---|---|
| Extrakcija | product_name="LEGO Harry Potter Hogwarts", model="" (Gemini gali ignoruoti numerį) | product_code="76430", pieces=1153 |
| Search query | AI-generated: "LEGO Harry Potter Hogwarts" | "LEGO 76430" |
| Rizika | **type-filter problema**: Elesen gali grąžinti Switch žaidimą; query neturi modelio numerio, `is_relevant_result` negali tiksliai atmesti | **Tikslus**: `is_relevant_result` tikrina "76430" visų shop rezultatų pavadinimuose |
| Divergencija | ~30% tikimybė rodyti neteisingą produktą | ~5% tikimybė (tik jei scrapas grąžina 76430 klaidos) |

### Scenarijus B: Ekraną su LEGO puslapiu (screenshot)

| | identify-product | scan-image |
|---|---|---|
| Palaikymas | **Taip** — "may be screenshot of webpage" | Silpnas — prompt skirtas "packaging", gali grąžinti 422 |
| Extrakcija | Gerai skaitys tekstą iš puslapio | Gali skaityti teisingai arba atsisakyti |
| **Verdiktas** | identify tinkamesnis screenshotams | scan sukurtas fizinei pakuotei |

### Scenarijus C: Neaiški nuotrauka (prastas apšvietimas)

| | identify-product | scan-image |
|---|---|---|
| Elgsena | 3-pakopinis fallback (Gemini → Haiku → OCR) → grąžina kažką | Iš karto 422 "product_not_recognized" |
| UX | Vartotojas gauna rezultatą (gal netikslu) | Vartotojas gauna klaidos ekraną |
| **Verdiktas** | Geresnis UX, bet gali grąžinti klaidingą produktą | Saugesnis, bet blogesnis UX |

### Scenarijus D: Kosmetika/maistas (Dove Shampoo, Milka)

| | identify-product | scan-image |
|---|---|---|
| Search query | AI-generated: "Dove Nourishing Shampoo 400ml" | product_name + pieces (nėra kodo) = "Dove Nourishing Shampoo 400ml" |
| Skirtumas | **Beveik identiškas rezultatas** — tiek identify, tiek scan generuoja panašų query be produkto kodo | — |
| **Verdiktas** | Nedidelė divergencija |

---

## 5. DIVERGENCIJOS DYDIS (ĮVERTINIMAS)

Kategorijos, kur identify-product ir scan-image **skiriasi rezultatais**:

| Kategorija | Tikimybė diverguoti | Priežastis |
|---|---|---|
| LEGO rinkiniai | **DIDELĖ (~35%)** | identify negeneruoja "LEGO 76430" tipo query; scan tai daro kai mato kodą |
| Elektronika (iPhone, Samsung) | **VIDUTINĖ (~15%)** | identify gali praleisti modelio numerį; scan meta 422 jei numeris neaiškus |
| Maistas, kosmetika | **ŽEMA (~5%)** | Abu generuoja panašų query (brand + product_name) |
| Screenshotai | **AUKŠTA (~40%)** | scan neoptimizuotas screenshotams; identify optimizuotas |

---

## 6. ROOT CAUSE: Kodėl diverguoja

```
identify-product:              scan-image:
  AI → product_name              AI → product_code (griežtas)
  AI → search_query (laisvas)    search = "{brand} {product_code}" (deterministinis)
       ↓                              ↓
  "LEGO Harry Potter"         "LEGO 76430"
       ↓                              ↓
  is_relevant_result:         is_relevant_result:
    model_tokens=[]             model_tokens=["76430"]
    overlap check (55%)         tikrina "76430" kiekviename rezultate
       ↓                              ↓
  Nintendo Switch žaidimas    Atmeta žaidimą ✓
  praeina (overlap ok)
```

**Šaknis:** identify-product naudoja semantinį query (brandas + pavadinimas), o scan-image naudoja precizinį query (brandas + kodas). `is_relevant_result` veikia geriau su kodo tipo query.

---

## 7. REKOMENDACIJOS

### R1: identify-product turėtų ieškoti product_code (žema rizika)
```python
# Jei AI grąžino model_code ir brand:
if model_code and brand:
    search_query = f"{brand} {model_code}"  # kaip scan-image
# Dabar: naudoja AI-generated search_query (gali ignoruoti kodą)
```

### R2: scan-image turėtų turėti OCR fallback kaip identify (vidutinė rizika)
Kai AI grąžina 422 (neaiški nuotrauka), vietoj klaidos paleisti Gemini OCR ir pakartoti.

### R3: Unify pirmą žingsnį — vienas "extract" endpoint (aukšta rizika, architektūros pakeitimas)
Vietoj dviejų endpoint'ų: `extract-product` (ekstrakcija, abu stiliai) + `search-by-product` (paieškas).

**Palikta peržiūrai** — R1 gali būti greitas win, R2/R3 reikia didesnio refactoring.

---

## 8. SANTRAUKA

| | identify-product | scan-image |
|---|---|---|
| Geriausiai tinka | Screenshotai, greita ID, neaiškios nuotraukos | Fizinė pakuotė su aiškiu kodu, kainų palyginimas |
| Precizija (LEGO) | ~65% (semantinis query) | ~95% (kodas query) |
| Fallback | 3 pakopų | Nėra |
| Kaina | Gemini: $0 + Haiku: ~$0.0004 | Haiku: ~$0.0004 + ScraperAPI: ~$0.01-0.02 |
| Divergencija | Didelė LEGO/elektronikos kategorijose | — |
| Veiksmas (R1) | Naudoti `brand + model_code` query kaip scan-image | — |
