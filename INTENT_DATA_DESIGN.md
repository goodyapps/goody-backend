# INTENT_DATA_DESIGN.md
**Data:** 2026-06-20 | **Šaka:** intent-data  
**Statusas:** DIZAINO DOKUMENTAS — PERŽIŪRAI, nekeičiamas gyvas kodas  
**Strateginis tikslas:** Pirkimo ketinimo duomenų grandinė — Goody ilgalaikis moat

---

## SITUACIJOS ANALIZĖ: KO ŠIUO METU KAUPIAME

### Supabase lentelės (esamos)

#### `searches` — populiarios paieškos (labai ribota)
```
query TEXT PRIMARY KEY   ← lowercase paieškos žodžiai
count INTEGER            ← kiek kartų ieškota
last_seen TIMESTAMPTZ    ← paskutinis kartas
```
**Problema:** Tik žodžių dažnumas. Nėra: koks buvo verdiktas, kaip ieškota, ar pirkta.

#### `price_history` — kainų istorija
```
product_name TEXT        ← nestandartizuotas (kiekviena paieška = atskiras product)
shop TEXT
price NUMERIC
currency TEXT
checked_at TIMESTAMPTZ
```
**Problema kritinė:** `product_name` yra raw query string. "LEGO 76430 Hogwarts", "lego 76430", "76430 hogwarts castle" — tai 3 SKIRTINGI produktai DB. Duomenys **fragmentuojasi** ir tampa neparenkami.

### In-memory (prarandama prie restart)
- `_click_counts[shop]` — paspaudimai per parduotuvę (tik skaičiai, ne produktai)
- `_search_counts[query]` — paieškų dažnumas (sinchronizuojama į `searches`)

### NIEKUR netransformuojama:
- Kaip ieškota (foto / barkodas / tekstas / balsas)
- Koks verdiktas gautas (BUY / WAIT / OK)
- Kokia geriausia kaina rasta ir kiek parduotuvių
- Ar vartotojas paspaudė "Buy Now" ir kurią parduotuvę
- Ar išsaugojo watchlist
- Laiko kontekstas (valanda, savaitės diena)
- Produkto kategorija (MAIN / FOOD / BOOK / ACCESSORY)

---

## PRODUKTO RAKTAS: KRITINĖ INFRASTRUKTŪRA

Prieš bet kokią schemą — reikia išspręsti **produkto rakto problemą**. Be jo visi ketinimo duomenys fragmentuojasi.

### Problema
```
Vartotojas A ieško: "LEGO 76430 Hogwarts"        → product_name = "lego 76430 hogwarts"
Vartotojas B ieško: "lego 76430"                  → product_name = "lego 76430"  
Vartotojas C ieško: "LEGO Hogwarts Castle 76430"  → product_name = "lego hogwarts castle 76430"
```
Supabase mato 3 skirtingus produktus. Kainų istorija nesikaupia. Paieškų statistika nesijungia.

### Sprendimas: `product_key` normalizavimas

```python
def _make_product_key(query: str, brand: str = "", model_code: str = "") -> str:
    """
    Normalizuotas produkto raktas duomenų sujungimui.
    Prioritetas: brand:model_code > brand:normalized_name > normalized_name
    
    Pavyzdžiai:
      "LEGO 76430 Hogwarts"          → "lego:76430"
      "Sony WH-1000XM5"              → "sony:wh-1000xm5"
      "Nutella 750g"                 → "nutella:750g"  (750g = kiekybinis, ne modelis)
      "Samsung Galaxy S24 Ultra"     → "samsung:galaxy-s24-ultra"
      "Nike Air Max 90"              → "nike:air-max-90"
    """
    b = re.sub(r'[^\w]', '', brand.lower()).strip() if brand else ""
    
    # Jei model_code aiškiai gautas iš AI (scan arba identify)
    if model_code:
        mc = re.sub(r'[^a-z0-9]', '-', model_code.lower()).strip('-')
        return f"{b}:{mc}" if b else f":{mc}"
    
    # Bandyti ištraukti iš query
    q = query.lower().strip()
    # Pašalinti fillerius
    q = re.sub(r'\b(buy|cheap|best|review|kur|pirkti|pigiausias|where|kaufen)\b', '', q)
    tokens = q.split()
    
    # Model token: alfanumerinis su skaičiumi (ne grynai skaičius, ne matavimo vienetas)
    model_tokens = []
    for t in tokens:
        if re.match(r'^[a-z]*\d+[a-z0-9-]*$', t) and not _UNIT_TOKEN_RE.match(t):
            model_tokens.append(t)
    
    if b and model_tokens:
        return f"{b}:{model_tokens[0]}"  # pirmas modelio tokenas
    elif model_tokens:
        return f":{model_tokens[0]}"
    else:
        # Vardinis produktas (maistas, kosmetika): pirmieji 3 reikšmingi žodžiai
        significant = [t for t in tokens if len(t) > 2 and t not in ('for', 'and', 'the', 'ir', 'und')]
        return ' '.join(significant[:3])
```

**Poveikis:** Visi 3 LEGO 76430 paieškos → `lego:76430`. Kainų istorija susijungia. Statistika skaičiuojama teisingai.

---

## KETINIMO GRANDINĖS SCHEMA

```
[KETINIMAS]          [SPRENDIMAS]         [VEIKSMAS]           [REZULTATAS]
Fotografuoja    →    Gauna verdiktą  →    Spaudžia "Buy" →     (Gali grįžti)
  arba                BUY / WAIT / OK        arba                  po kainos
tekstas ieško        + kainos info           watchlist →           kritimo
  arba                                       + išeina              SEKA
barkodas                                      į parduotuvę

↓ search intent      ↓ search decision       ↓ track_click        ↓ watchlist_hit
```

Visa grandinė susieta per `search_id` (UUID, vienam paieškos aktui).

---

## NAUJA SUPABASE SCHEMA

### Lentelė 1: `intent_events` — pagrindinis ketinimo žurnalas

```sql
CREATE TABLE intent_events (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- PRODUKTO IDENTIFIKACIJA
    product_key     TEXT NOT NULL,          -- 'lego:76430', 'sony:wh-1000xm5'
    product_name    TEXT NOT NULL,          -- 'lego 76430 hogwarts' (raw, lowercase)
    product_type    TEXT,                   -- MAIN, ACCESSORY, BOOK, FOOD, COSMETICS
    
    -- KETINIMO SIGNALAS
    input_method    TEXT NOT NULL,          -- 'text', 'photo', 'barcode', 'voice'
    scan_confidence TEXT,                   -- 'high', 'medium', 'low' (tik photo/barcode)
    language        TEXT NOT NULL,          -- 'lt', 'de', 'pl', 'en', 'ru'
    
    -- LAIKO KONTEKSTAS (anonimizuotas — nėra tikslios datos)
    hour_of_day     SMALLINT,               -- 0–23
    day_of_week     SMALLINT,               -- 0=Pirmadienis, 6=Sekmadienis
    week_of_year    SMALLINT,               -- 1–53 (sezoniškumui)
    
    -- SPRENDIMO SIGNALAS
    verdict         TEXT,                   -- 'BUY', 'WAIT', 'OK', 'NOT_FOUND'
    price_min_eur   NUMERIC(10,2),          -- žemiausia kaina EUR
    price_max_eur   NUMERIC(10,2),          -- aukščiausia kaina EUR
    shops_found     SMALLINT,               -- kiek parduotuvių grąžino rezultatą
    cheapest_shop   TEXT,                   -- kuri parduotuvė pigiausia
    has_history     BOOLEAN DEFAULT FALSE,  -- ar buvo kainų istorijos duomenų
    
    -- VEIKSMO SIGNALAS (papildoma prie click)
    clicked_shop    TEXT,                   -- kuria parduotuve paspaudė (nullable)
    clicked_at      TIMESTAMPTZ,
    added_watchlist BOOLEAN DEFAULT FALSE,
    watchlist_target_eur NUMERIC(10,2),     -- tikslinė kaina (nullable)
    
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Indeksai greičiui
CREATE INDEX idx_intent_product_key    ON intent_events(product_key, created_at DESC);
CREATE INDEX idx_intent_created        ON intent_events(created_at DESC);
CREATE INDEX idx_intent_verdict        ON intent_events(verdict, product_type);
CREATE INDEX idx_intent_input_method   ON intent_events(input_method, created_at DESC);
```

**Saugumas:** Nėra IP, nėra user_id, nėra jokio asmeninio identifikatoriaus. Kiekvienas eilutė = anoniminė sesija.

---

### Lentelė 2: `price_history` — IŠPLĖSTA (ne pakeista)

Esama `price_history` lentelė paliekama tokia pati. Pridedamas tik `product_key` stulpelis:

```sql
-- MIGRACIJA (žr. migration.sql): tik kolona, nekeičia struktūros
ALTER TABLE price_history 
    ADD COLUMN IF NOT EXISTS product_key TEXT;

-- Backfill: laikinas product_key = product_name (bus tiksliau kai pradės siųsti iš serverio)
UPDATE price_history 
    SET product_key = LOWER(TRIM(product_name))
    WHERE product_key IS NULL;

-- Indeksas naujam stulpeliui
CREATE INDEX IF NOT EXISTS idx_price_history_product_key 
    ON price_history(product_key, checked_at DESC);
```

**Efektas:** `fetch_price_history_from_supabase()` gali ieškoti pagal `product_key` vietoj `product_name`, susijungiant skirtingas to paties produkto paieškas.

---

### Lentelė 3: `watchlist_server` — serverio pusės watchlist (naujas)

```sql
CREATE TABLE watchlist_server (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_key     TEXT NOT NULL,
    product_name    TEXT NOT NULL,
    original_price_eur  NUMERIC(10,2),
    target_price_eur    NUMERIC(10,2),
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    hit_at          TIMESTAMPTZ,    -- kada kaina pasiekė tikslą
    hit_price_eur   NUMERIC(10,2),  -- faktinė kaina kai pasiekė tikslą
    notified        BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_watchlist_product_key ON watchlist_server(product_key);
CREATE INDEX idx_watchlist_active ON watchlist_server(hit_at) WHERE hit_at IS NULL;
```

**Pastaba:** Šis lentelė pasiūlyta ateičiai — push pranešimų infrastruktūrai. Šiuo metu watchlist yra localStorage ir tuo palikti.

---

## GDPR IR PRIVATUMAS

### Kas yra ANONIMINIS (saugus be papildomų priemonių)

| Duomenys | Teisinis pagrindas | Pastaba |
|---|---|---|
| `product_key` | Teisėtas interesas | Produktas, ne asmuo |
| `verdict`, `price_*` | Teisėtas interesas | Agreguota kainodara |
| `input_method` | Teisėtas interesas | Techninis metodas |
| `hour_of_day`, `day_of_week` | Teisėtas interesas | Bendras laikas, ne tikslus timestamp |
| `language` | Teisėtas interesas | Kalba, ne tautybė |
| `shops_found`, `cheapest_shop` | Teisėtas interesas | Rinkos info |

### Kas NEGALIMA saugoti be sutikimo

| Duomenys | Priežastis | Sprendimas |
|---|---|---|
| IP adresas | Asmeninis duomuo (GDPR 4(1)) | NIEKADA nesaugoti šioje lentelėje |
| User ID / Cookie | Stebėjimas | Nėra — be registracijos |
| Tikslus timestamp (sekundė) | Gali identifikuoti | Tik valanda/diena — ne tikslus laikas |
| Nuotraukos | Gali būti asmens duomenys | NIEKADA nesaugoti, tik apdoroti |

### Privacy by Design principai implementuoti

1. **Duomenų minimizavimas:** Saugoma tik tai, kas reikalinga verdikto gerinimui
2. **Anonimizavimas pagal dizainą:** Nėra jungties su konkrečiu asmeniu
3. **Laiko anonimiškumas:** `hour_of_day` + `day_of_week` vietoj `created_at` tikslaus laiko
4. **Automatinis senų duomenų šalinimas:** Rekomenduojama RLS politika: duomenys > 2 metų → archyvuoti

### Privatumo politikos kalba

```
Goody renka anoniminius produktų paieškos duomenis (produkto pavadinimas, kaina, 
paieškos metodas, valandos intervalas) statistiniais tikslais ir paslaugos gerinimui.
Asmeniniai duomenys (vardas, el. paštas, IP) nerinkimi ir nesaugomi.
Teisinis pagrindas: Reglamento (ES) 2016/679 6 str. 1 d. f p. (teisėtas interesas).
```

---

## KAIP SUKAUPTI DUOMENYS MAITINA VERDIKTĄ

### Šiandien (rule-based)
```
Vartotojas ieško "Sony WH-1000XM5"
Verdiktas: "Kaina €249. 3 parduotuvės. PIRKTI"
```

### Su 1 mėn. intent_events + price_history
```
Verdiktas: "Kaina €249 — tai 8% mažiau nei vidutiniškai per 30 dienų (vidutinė €271).
Rekomenduojame pirkti."
```

### Su 3 mėn. duomenimis + `day_of_week`
```
Verdiktas: "Kaina €249. PASTEBĖJOME: penktadieniais ši prekė vidutiniškai 11% pigesnė.
Šiandien trečiadienis — jei gali palaukti iki penktadienio, galimas sutaupymas ~€27."
```

### Su 1 metų duomenimis + `week_of_year`
```
Verdiktas: "Kaina €249. KAINŲ ISTORIJA rodo: lapkritį-gruodį (Black Friday/Kalėdos)
šis produktas vidutiniškai nukrenta iki €185-€210. Šiuo metu istoriškai aukšta kaina.
Rekomenduojame PALAUKTI jei neskubu."
```

### Su verdict + click koreliacija
```
Analizė (vidinė): Kai verdiktas "BUY" + cheapest_shop = Amazon.DE:
  → 78% vartotojų spaudžia ant Amazon.DE
  → 12% spaudžia ant Varle (geresnis delivery?)
  → 10% nepasirenka nė vieno
Išvada: verdiktas "BUY" yra patikimas konversijos šaltinis.
```

### Su scan_confidence analize
```
Analizė (vidinė): scan_confidence="low" paieškos:
  → 60% baigiasi NOT_FOUND
  → 25% baigiasi WAIT (produktas rastas bet kaina aukšta)
  → 15% baigiasi paspaudimu
Išvada: žemos kokybės nuotraukos reikia aktyvesnio guidance UI.
```

---

## KODO ARCHITEKTŪRA: KĄ REIKIA KEISTI

### Server pusė: 3 naujos funkcijos

```python
# 1. Normalizuotas produkto raktas
def _make_product_key(query, brand="", model_code="") -> str:
    # (žr. intent_schema.py — pilnas implementavimas)

# 2. Asinchroninis ketinimo evento įrašymas
def _sb_log_intent(event: dict):
    """Fire-and-forget: log intent event to Supabase. Non-blocking."""
    sb = get_supabase()
    if not sb: return
    try:
        sb.table("intent_events").insert(event).execute()
    except Exception as e:
        print(f"[intent_log] {e}")

# 3. Paieškos rezultato prijungimas prie intent evento
def _build_intent_event(query, input_method, language, result_data, search_id) -> dict:
    now = datetime.utcnow()
    return {
        "id": search_id,
        "product_key": _make_product_key(query),
        "product_name": query.lower().strip()[:200],
        "product_type": result_data.get("product_type"),
        "input_method": input_method,
        "language": language,
        "hour_of_day": now.hour,
        "day_of_week": now.weekday(),  # 0=Mon
        "week_of_year": now.isocalendar()[1],
        "verdict": result_data.get("ai_verdict"),
        "price_min_eur": result_data.get("price_min"),
        "price_max_eur": result_data.get("price_max"),
        "shops_found": len(result_data.get("results", [])),
        "cheapest_shop": (result_data.get("results") or [{}])[0].get("shop"),
        "has_history": bool(result_data.get("price_history")),
    }
```

### Kur įterpti server.py

```
search() funkcija (~line 6277):
  PRIDĖTI po post_process():
    _search_id = str(uuid.uuid4())
    event = _build_intent_event(query, data.get("input_method","text"), language, result, _search_id)
    threading.Thread(target=_sb_log_intent, args=(event,), daemon=True).start()

search_stream() funkcija (~line 6517):
  PRIDĖTI po result = post_process():
    event = _build_intent_event(_query, data.get("input_method","text"), _lang, result, str(uuid.uuid4()))
    threading.Thread(target=_sb_log_intent, args=(event,), daemon=True).start()

track_click() funkcija (line 7317):
  PRIDĖTI: intent_event_id = data.get("intent_id") 
  Jei turime intent_id → UPDATE intent_events SET clicked_shop=shop, clicked_at=now() WHERE id=intent_id
```

### Frontend: minimalūs pakeitimai

```javascript
// doSearch() — siųsti input_method kaip papildomą lauką
const body = { query: q, language: curLang, input_method: "text" };  // "photo"|"barcode"|"voice"

// runIdentify() → confirmSearch() → search su method="photo"
// scanBarcode() → search su method="barcode"
// voiceSearch() → search su method="voice"

// track() — siųsti intent_id (susieti paspaudimą su paieška)
function track(shop, q, intentId) {
    fetch("/api/track", { method:"POST", 
        body: JSON.stringify({ shop, q, intent_id: intentId }) });
}
```

---

## DUOMENŲ PANAUDOJIMO GALIMYBĖS (ateičiai)

### 1. Dinaminis verdiktas iš istorijos

```sql
-- "Ar ši kaina žema pagal istoriją?"
SELECT 
    AVG(price_min_eur) as avg_price,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price_min_eur) as p25_price,
    COUNT(*) as sample_size
FROM intent_events
WHERE product_key = 'sony:wh-1000xm5'
  AND created_at > NOW() - INTERVAL '90 days'
  AND verdict != 'NOT_FOUND';
```

### 2. Savaitės dienos kainų tendencija

```sql
-- "Kokia diena pigiausia šiai kategorijai?"
SELECT 
    day_of_week,
    AVG(price_min_eur) as avg_min_price,
    COUNT(*) as n
FROM intent_events
WHERE product_type = 'ELECTRONICS'
  AND verdict != 'NOT_FOUND'
  AND created_at > NOW() - INTERVAL '180 days'
GROUP BY day_of_week
ORDER BY avg_min_price;
```

### 3. Populiarūs produktai su kainos kontekstu

```sql
-- "Populiariausios paieškos su dabartine kainos situacija"
SELECT 
    product_key,
    product_name,
    COUNT(*) as searches,
    AVG(price_min_eur) as avg_price,
    MAX(CASE WHEN created_at > NOW() - INTERVAL '7 days' THEN price_min_eur END) as recent_price
FROM intent_events
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY product_key, product_name
ORDER BY searches DESC
LIMIT 20;
```

### 4. Konversijų analizė

```sql
-- "Kuris shopas konvertuoja geriausiai?"
SELECT 
    cheapest_shop,
    COUNT(*) as impressions,
    SUM(CASE WHEN clicked_shop IS NOT NULL THEN 1 ELSE 0 END) as clicks,
    ROUND(100.0 * SUM(CASE WHEN clicked_shop = cheapest_shop THEN 1 ELSE 0 END) / COUNT(*), 1) as ctr_pct
FROM intent_events
WHERE verdict = 'BUY'
  AND created_at > NOW() - INTERVAL '30 days'
GROUP BY cheapest_shop
ORDER BY impressions DESC;
```

---

## MIGRACIJOS PLANAS

Visas SQL — žr. `migration.sql` šioje šakoje.

### Žingsnis 1 (Nekeičia veikimo — saugu bet kada)
```
Supabase dashboard → SQL Editor:
  ALTER TABLE price_history ADD COLUMN IF NOT EXISTS product_key TEXT;
  CREATE INDEX ...
  UPDATE price_history SET product_key = LOWER(TRIM(product_name)) WHERE product_key IS NULL;
```

### Žingsnis 2 (Nauja lentelė — saugu, nekeičia esamos)
```
CREATE TABLE intent_events (...);
CREATE INDEX ...
```

### Žingsnis 3 (Serverio kodas — atskiroje šakoje, po peržiūros)
```
Pridėti _make_product_key(), _sb_log_intent(), _build_intent_event()
Pridėti šaukimus search() ir search_stream()
Pridėti intent_id sekimą track_click()
```

### Žingsnis 4 (Frontend — minimalus)
```
Pridėti input_method lauką doSearch(), runIdentify() etc.
Siųsti intent_id su /api/track
```

### Žingsnis 5 (Po 1 mėn. duomenų — verdikto pagerinimas)
```
Naudoti intent_events statistiką rule_based_ai_analyze() papildymui
```

**Kiekvienas žingsnis nepriklausomas. Galima stabtelėti po bet kurio.**

---

## APIBENDRINIMAS: MOAT LOGIKA

```
Šiandien:        Goody rodo kainas iš 8 parduotuvių.
                 Bet kurį konkurentą galima pakartotas per 3 mėn.

Po 6 mėn.:       Goody žino, kad Sony WH-1000XM5 vidutiniškai 12% pigesnė
                 penktadieniais. Konkurentas turi pradėti nuo nulio.

Po 2 metų:       Goody žino, kad lapkritį ausinės krenta vidutiniškai 23%.
                 Goody žino, kuris shopas konvertuoja geriausiai kokiai kategorijai.
                 Goody žino, kad „foto" paieška baigiasi pirkimu 2.3× dažniau nei tekstas.
                 Konkurentas turi 2 metų duomenų deficitą.

Tai yra nekopijuojamas turtas.
```

---

## FAILAI ŠIOJE ŠAKOJE

| Failas | Turinys |
|---|---|
| **INTENT_DATA_DESIGN.md** | Šis dokumentas — pilnas dizainas |
| **migration.sql** | SQL lentelių kūrimas ir migracija (NE paleisti be peržiūros) |
| **intent_schema.py** | Python kodo eskizas (NE integruotas į server.py) |
