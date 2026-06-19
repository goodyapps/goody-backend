# ELESEN_MATCH_DEBUG.md
**Data:** 2026-06-19  
**Bug:** "LEGO 76430 Hogwarts" → Goody rodo Elesen.lt €34.99, bet "Buy now" atidaro Nintendo Switch žaidimą "LEGO Harry Potter 1-7" (barkodas 5051895411827)

---

## 1. Kaip Elesen scraper ištraukia produktą?

Elesen scraperį sudaro du keliai (`_scrape_elesen_from_html`, server.py:2497):

```
1. SPA kelias: _extract_spa_products() → _walk_for_products()
   → Ieško JSON struktūroje <script> žymėse (Next.js __NEXT_DATA__, window.__STATE__, ld+json)
   → Jei randa — grąžina iš karto, DOM kelias IGNORUOJAMAS

2. DOM kelias (fallback): BeautifulSoup article.product-card → .product-card__title + a[href]
   → Ima iki 8 pirmų produkto kortelių iš HTML
```

**Abu keliai ima PIRMUS tinkamus rezultatus iš Elesen paieškos — be papildomo ranking ar relevance patikrinimo.**

---

## 2. KRITINIS: Kodėl model/set kodas 76430 nevaliduojamas grąžintame rezultate?

### Teorinė `is_relevant_result` analizė

`is_relevant_result("LEGO 76430 Hogwarts", "LEGO Harry Potter 1-7 Nintendo Switch")` turėtų grąžinti `False`:

```
q = "lego 76430 hogwarts"
t = "lego harry potter 1-7 nintendo switch"

model_tokens = re.findall(r'\b[a-z]*\d+[a-z0-9-]*\b', q) → ["76430"]
(76430 nėra unit token: g/ml/kg/hz etc.)

_model_in_title("76430"):
  - "76430" in t?  → NO
  - t_nh = "legoharrypotter17nintendoswitch"
  - "76430" in t_nh? → NO
  → returns False

→ is_relevant_result grąžina False ✓ (turėtų filtruoti)
```

### Bet bug'as vis tiek atsiranda — kodėl?

**Hipotezė A (labiausiai tikėtina): Elesen SPA JSON turi "76430" produkto pavadinime**

Elesen kataloge Nintendo Switch LEGO Harry Potter žaidimas (barkodas 5051895411827) gali būti pažymėtas `"name": "LEGO Harry Potter 76430 Nintendo Switch"` arba `"label": "76430 LEGO Harry Potter"` — t.y. Elesen savo kataloge supainiojo rinkinį su žaidimu (klaidingai priskyrė set numerį žaidimui).

Tada:
- `is_relevant_result("LEGO 76430 Hogwarts", "LEGO Harry Potter 76430 Nintendo Switch")` → `True` (76430 yra abiejuose)
- Produkto URL eina į Harry Potter žaidimo puslapį
- Goody rodo pavadinimą su 76430 → atrodo "tinkamas", bet tai KLAIDINGAS produktas

**Hipotezė B (antra tikimybė): Klaidinga URL ir pavadinimo kombinacija**

Elesen paieška gali grąžinti du produktus po €34.99:
1. LEGO Hogwarts Castle 76430 (teisingas) — be URL (slug tuščias JSON'e)
2. LEGO Harry Potter Switch (neteisinas) — su URL

Fix A1 (`_walk_for_products` empty-URL skip) išfiltruoja #1, bet #2 praleidžia.
Galutinis rezultatas: Goody rodo #2 su taisyklingu pavadinimu (gautu iš kito JSON lauko), bet su #2 URL.

**Hipotezė C (mažiausia tikimybė): `or all_results` fallback**

server.py:6267-6268:
```python
_relevant_for_ai = [r for r in all_results if r.get("price", 0) > 0
                    and is_relevant_result(query, r.get("product_title", ""))] or all_results
```

Jei `is_relevant_result` atmeta VISUS scraping rezultatus → `_relevant_for_ai = []` → fallback į `all_results` (visi rezultatai nepriklausomai nuo relevance). Jei šis scenarijus: 76430 Hogwarts Castle scrape nepavyko, bet Harry Potter žaidimas grąžintas → paskutinis atlieka fallback į `all_results`.

---

## 3. Ar yra produkto TIPO patikra?

**NĖRA.** Goody neatskiria:
- LEGO statybinių rinkinių (set) nuo LEGO vaizdo žaidimų
- Fizinių rinkinių nuo Nintendo Switch/PS4/PC žaidimų su LEGO licencija
- Žaislų nuo kompiuterinių žaidimų su tuo pačiu pavadinimu

`is_relevant_result` tikrina tik žodžių/brand/model kodo sutapimą — ne produkto tipą ar kategoriją.

Papildomas kontekstas: "Hogwarts" → "Harry Potter" asociacija semantiškai teisinga, todėl tiek LEGO 76430 Hogwarts Castle (rinkinys), tiek LEGO Harry Potter (žaidimas) atrodo susijęs su paieška.

---

## 4. Ar nuotrauka, kaina ir URL iš TO PATIES produkto?

Abi verčia iš `_walk_for_products` ar DOM scrapingo `_make_result`:

```python
results.append(_make_result("Elesen.lt", "🇱🇹", link, price, name, "elesen", img_url))
```

`link`, `price`, `name`, `img_url` — visi iš TO PATIES `item` (DOM) arba TO PATIES `node` (SPA JSON dict). **Teoriškai negalima situacija kur URL ir pavadinimas iš skirtingų šaltinių.**

Išimtis: Jei Elesen SPA JSON dict turi `name="LEGO Harry Potter 76430"` IR `url="/switch-game"` IR `image=<pilies-nuotrauka>` — visi trys iš to paties neteisingo dict objekto. Tada Goody galėtų rodyti PILIES NUOTRAUKĄ (iš img lauko) su ŽAIDIMO URL — jei Elesen savo JSON suklydo su nuotrauka.

---

## 5. Ar šis atvejis pasikartoja kitose parduotuvėse?

**Taip — ta pati rizika egzistuoja bet kuriai parduotuvei.** Priežastys:

- Varle.lt, 1a.lt, Pigu.lt — visos naudoja tą pačią `is_relevant_result` + `_walk_for_products`
- Visos grąžina paieškos rezultatus pagal savo algoritmus — galima gauti semantiškai susijusį, bet ne tiksliai atitinkantį produktą
- Ypač rizikinga kai: vienas prekių ženklas (LEGO) turi IR fizinius rinkinius IR vaizdo žaidimus IR knygų serijas — visi su panašiais pavadinimais

**Amazon specifika:** Amazon sponsored fix (Fix B) tikrina konkuruojančius SET KODUS (76430 vs 76451), bet NEŽIŪRI produkto tipo (žaidimas vs rinkinys).

---

## 6. Kodėl ankstesnis buylink fix nepagavo?

Fix B (sponsored+competing-model) tikrina:
```python
_q_codes = set(re.findall(r'\b\d{4,6}\b', query))  # {"76430"}
_t_codes = set(re.findall(r'\b\d{4,6}\b', name))   # {"76430"} jei title="LEGO Harry Potter 76430"
_competing = _t_codes - _q_codes                    # {} tuščia!
if _competing and any(len(c) == len(next(iter(_q_codes))) for c in _competing):
    continue  # skip
```

Jei produkto pavadinimas turi TĄ PATĮ kodą (76430) — `_competing` bus tuščia → neišfiltruojama.

Šis atvejis yra SKIRTINGAS nuo sponsored bug:
- Sponsored bug: teisingas kodas paieškoje (76430), klaidingas kodas produkto pavadime (76451)  
- Šis bug: teisingas kodas paieškoje (76430), **TAS PATS kodas** produkto pavadime, bet **klaidingas produkto tipas** (žaidimas ≠ rinkinys)

---

## APIBENDRINIMAS

### Root cause (labiausiai tikėtina)

Elesen katalogas turi klaidingai pažymėtą produktą: Nintendo Switch LEGO Harry Potter žaidimas (5051895411827) yra asocijuotas su LEGO set kodu "76430" Elesen vidinėje sistemoje. Tai atrodo kaip Elesen duomenų kokybės problema — jie galėjo klaidingai susieti žaidimą su LEGO rinkiniu (abu su "Harry Potter" ir "LEGO" vardais).

### Alternatyva

Fix A1 (empty-URL skip) pašalino tikrą Hogwarts Castle 76430 (nes jo slug JSON'e buvo tuščias), ir liko tik Harry Potter žaidimas kaip vienintelis Elesen rezultatas.

### Sisteminė problema

`is_relevant_result` validuoja **žodžių/kodo buvimą pavadinime**, bet ne **produkto tipo atitikimą**. Kai parduotuvė grąžina klaidingai katalogizuotą produktą su teisingais raktažodžiais — filtras praeina.

---

## PASIŪLYMAS — kaip spręsti (NEATLIKTA)

### Trumpalaikis (žema rizika)

**Post-scraping set kodo validacija** — po `is_relevant_result` patikros, jei query turi grynai skaitinį 4-6 skaitmenų kodą (LEGO set numeris, modelio kodas), patikrinti ar grąžinto produkto pavadinimas TIK TAME KODE atitinka — arba produkto URL turi tą kodą:

```python
# Pseudokodas — NEIMPLEMENTUOTA
_set_codes = re.findall(r'\b\d{4,6}\b', query)
if _set_codes:
    for code in _set_codes:
        if code not in product_title and code not in product_url:
            skip  # kodo nėra nei pavadinime, nei URL — klaidingas produktas
```

**Trūkumas:** Kai Elesen klaidingai etiketina produktą su 76430 pavadinime — šis fix nepadėtų. Bet padėtų hipotezei B (tuščias URL skip + Harry Potter grąžinamas be kodo pavadinime).

### Ilgalaikis (vidutinė rizika)

**Produkto tipo klasifikacija** — jei query nustatomas kaip "LEGO rinkinys" (skaitinis kodas + "lego"), produkto tipas tikrinamas prieš pridedant:
- Jei pavadinime yra "Nintendo Switch", "PS4", "PS5", "Xbox", "PC" → atmesti (tai žaidimas, ne rinkinys)
- Jei pavadinime yra "knygų serija", "filmas" → atmesti

**Trūkumas:** Sunku implementuoti universaliai — reikia kiekvienos kategorijos specifikos.

### Momentinis sprendimas (nulinis kodas)

Stebėti Render logus — ar matosi `[Elesen] skip empty-URL` kai ieškoma "LEGO 76430 Hogwarts". Jei taip — Fix A1 išfiltruoja teisingą produktą ir lieka tik klaidingas. Sprendimas: **leisti rezultatams be URL patekti į sąrašą be buy-link** (rodyti kainą be mygtuko), užuot visiškai atmetant.

---

## SEKANTYS ŽINGSNIAI

1. **Patikrinti Render logus** po "LEGO 76430 Hogwarts" paieškos — ieškoti `[Elesen.lt] skip empty-URL` pranešimų
2. **Patikrinti Elesen tiesiai**: `https://www.elesen.lt/paieska?q=LEGO%2076430%20Hogwarts` — kokius rezultatus grąžina?
3. Pagal tai nuspręsti: ar tai Elesen duomenų klaida, ar kodo klaida
