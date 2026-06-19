# BUYLINK_DEBUG.md
**Data:** 2026-06-19  
**Simptomas:** "Buy now" atidaro (A) Elesen homepage, (B) Amazon.PL 76451 vietoj 76430  
**Scenarijus:** "LEGO 76430 Hogwarts" paieška → Elesen.lt €34.99 + Amazon.PL €64.79

---

## BUG A — Elesen.lt "Buy now" atidaro homepage

### Kodo kelias (URL ištraukimas)

`scrape_elesen()` kviečia `_scrape_elesen_from_html()` → pirma bando SPA kelią:

```python
# _scrape_elesen_from_html, eilutė 2497
spa = _extract_spa_products(html, query, "Elesen.lt", "🇱🇹", "https://www.elesen.lt", "elesen")
if spa:
    return spa  # ← jei SPA sėkmingas, DOM kelias NEPANAUDOJAMAS
```

SPA `_walk_for_products` URL ištraukimas (eilutės 1981–1988):
```python
slug = (node.get("url") or node.get("slug") or
        node.get("urlKey") or node.get("url_key") or
        node.get("link") or node.get("href") or
        node.get("productUrl") or node.get("product_url") or
        node.get("canonical") or node.get("pageUrl") or
        node.get("detailUrl") or node.get("productLink") or
        node.get("itemUrl") or node.get("path") or "")  # ← FALLBACK: tuščia eilutė

link = slug if slug.startswith("http") else f"{base_url.rstrip('/')}/{slug.lstrip('/')}"
```

### Klaidos kelias

Jei Elesen SPA JSON produktas grąžina `url: ""` (tuščia), `url: null`, arba URL laukas visai nėra JSON'e:

```python
slug = "" or "" or "" or ... = ""
# slug neprasideda "http"
link = f"https://www.elesen.lt/{''}" = "https://www.elesen.lt/"  # ← HOMEPAGE
```

Elesen talpina produktus per SPA (ateina JSON state), bet URL laukas gali būti:
- `null` — negrąžinamas JSON objekte
- `""` — tuščia eilutė (dažna Elesen `__NUXT_DATA__` struktūroje)
- Santykinė nuoroda kaip `"/lt/products/lego-76430"` — teisingai apdorojama
- Pilna nuoroda `"https://www.elesen.lt/lt/products/..."` — teisingai apdorojama

### DOM fallback (kai SPA nepavyksta)

```python
# eilutė 2547-2549
link_el = item.select_one("a[href]")
href = link_el["href"] if link_el else ""
link = href if href.startswith("http") else f"https://www.elesen.lt{href}"
```

Jei `link_el = None` (nėra `<a href>` elemente):
```python
href = ""
link = "https://www.elesen.lt"  # ← HOMEPAGE (be slash)
```

### Kodėl `slug = ""` sukuria homepage, o ne klaidą

```python
f"https://www.elesen.lt/{slug.lstrip('/')}"
```

Kai `slug = ""`: `"".lstrip("/") = ""` → `"https://www.elesen.lt/"` — tai VALIDUS URL (homepage), todėl nėra jokio išimties signalo.

### Patvirtinimas iš screenshot'o

Elesen atidaro `elesen.lt` pagrindinį puslapį su "VASAROS KAINOS" banneriu ir kategorijų meniu — tai 100% homepage, ne paieška, ne produktas.

---

## BUG B — Amazon.PL atidaro 76451 vietoj 76430

### Duomenys iš screenshot'ų

| Laukas | Rodytas Goody'je | Atidarytas Amazon.PL |
|---|---|---|
| Produktas | LEGO 76430 Hogwarts (iš paieškos konteksto) | LEGO 76451 Privet Drive: Wizyta ciotki Marge |
| Kaina | €64.79 | 275.99 PLN (= **€64.79** keitimo kursu ~4.26) |
| Rinkinys | 76430 (Hogwarts Owl Post) | 76451 (4 Privet Drive) |

**Kaina SUTAMPA** — €64.79 = 275.99 PLN. Tai reiškia: kaina IR URL abu ateina iš **to paties** 76451 produkto.

### Kodo kelias

```python
# eilutės 2728-2750 (scrape_amazon)
h2_el = item.select_one("h2")
name = h2_el.get("aria-label", "") or ""
if not name:
    span = h2_el.select_one("span")
    name = span.get_text(strip=True)
name = name[:100]
if not is_relevant_result(query, name):
    continue
```

```python
# eilutės 2798-2810
link_el = h2_el.parent if h2_el and h2_el.parent.name == "a" else item.select_one("a[href*='/dp/']")
href = link_el["href"] if link_el else ""
link = f"https://www.amazon.{domain}{href}" if href.startswith("/") else href
asin_m = re.search(r"/dp/([A-Z0-9]{10})", link)
asin = asin_m.group(1) if asin_m else ""
aff = f"https://www.amazon.{domain}/dp/{asin}?tag={aff_tag}" if asin else search_url
```

### Klaidos mechanizmas — Amazon Sponsored Keyword Stuffing

Amazon leidžia reklamos davėjams naudoti **keyword targeting** — t.y. parodyti savo reklamą kai kas nors ieško konkurento produkto. Amazon sponsored ads gali rodyti **bet kokį pavadinimą** kaip reklaminį tekstą (h2 aria-label), tačiau produktas, kaina ir ASIN lieka **reklamduotojo produkto** (76451).

Konkrečiai ši paieška:
```
Amazon.PL search: "LEGO 76430 Hogwarts"
→ Sponsored result (pirmas):
   h2.aria-label = "LEGO Harry Potter 76430 Hogwarts Owl Post..." (KEYWORD MATCH)
   price = 275.99 PLN (← tai yra 76451 kaina!)
   a[href*='/dp/'] = /dp/B0XXXXXXXXX (← tai yra 76451 ASIN!)
```

### Kodėl is_relevant_result NEPAGAVO

```python
is_relevant_result("LEGO 76430 Hogwarts", "LEGO Harry Potter 76430 Hogwarts Owl Post")
```
→ model_tokens = ["76430"]  
→ "76430" yra pavadinime (keyword-stuffed) → True → **PRALEISTA**

Ši klaida fundamentali: `is_relevant_result` tikrina PAVADINIMĄ, bet ne ASIN/URL. Kai pavadinimas surašytas siekiant raktinių žodžių atitikimo, filtras negali pagauti klaidingo produkto.

### Ar kaina ir URL gali ateiti iš SKIRTINGŲ produktų?

**Šiuo atveju: NE.** Kaina (275.99 PLN) ir URL (76451 ASIN) abu ateina iš TO PATIES `item` div — 76451 sponsored produkto. Problema yra pavadinimas (keyword-stuffed 76430), o ne kaina/URL neatitikimas.

**Teoriškai: TAIP, gali būti kaina ≠ URL.** Tai atsitiktų kai:
```python
link_el = h2_el.parent if h2_el.parent.name == "a" else item.select_one("a[href*='/dp/']")
```
Jei `item` div'e yra **keli /dp/ linkai** (pvz., varianto linkai, "similar items" sekcija), `select_one("a[href*='/dp/']")` paima PIRMĄ — kuris gali būti kitam produktui nei kaina. Bet **šiuo konkrečiu atveju kaina = URL** (abu 76451).

### Faktinis neigiamas poveikis

Goody rodo:
- **Elesen.lt €34.99** (BEST DEAL, SAVE €29.80 vs Amazon.PL)
- **Amazon.PL €64.79** (Good deal)

Abi kainos yra abejotinos — Elesen grąžino kažkokį €34.99 produktą (gal kitą LEGO ar paneigę), o Amazon grąžino 76451 su 76430 keyword title. Vartotojas mato "Hogwarts LEGO nuo €34.99" ir paspaudžia — atidaro Elesen homepage arba 76451 Privet Drive. Nei vienas nėra ieškomas 76430.

---

## ABIEJŲ BUG'Ų DIAGRAMA

```
Vartotojas ieško: "LEGO 76430 Hogwarts"
        │
        ├── Elesen.lt scraper
        │   └── SPA JSON: produktas su url="" arba url: null
        │       → slug = ""
        │       → link = "https://www.elesen.lt/"  ← HOMEPAGE BUG
        │
        └── Amazon.PL scraper
            └── Sponsored result: 76451, bet h2="...76430 Hogwarts..."
                → is_relevant_result: True (76430 pavadinime)
                → kaina: 275.99 PLN (76451)
                → URL: /dp/76451_ASIN
                → RODOMA: €64.79, pavadinimas rodo 76430
                → ATIDARO: 76451 Privet Drive ← WRONG PRODUCT BUG
```

---

## SIŪLOMI SPRENDIMAI

### Fix A: Elesen homepage (konservatyvus fix)

Validuoti URL prieš išsaugant — jei `slug` yra tuščias arba yra tik domenų root, atmesti rezultatą:

```python
# _walk_for_products, po slug ekstrakcijos:
if not slug or slug in ("/", ""):
    pass  # neįtraukti produkto be URL
else:
    link = slug if slug.startswith("http") else f"{base_url.rstrip('/')}/{slug.lstrip('/')}"
    # ... likęs kodas ...
```

Arba DOM kelyje (_scrape_elesen_from_html):
```python
link_el = item.select_one("a[href]")
href = link_el["href"] if link_el else ""
if not href or href in ("/", "#", "javascript:void(0)"):
    continue  # Praleisti produktus be URL
link = href if href.startswith("http") else f"https://www.elesen.lt{href}"
```

**Rizika: žema.** Produktai be URL nebūtų rodomi — tai GERIAU nei rodyti su homepage link'u.

---

### Fix B: Amazon wrong product (sudėtingesnė)

Problema fundamentali: Amazon sponsored ads title ≠ actual product. Kelios galimybės:

**Variantas B1 (paprasta, dalinė apsauga):** Ištraukti set numerį iš URL/ASIN ir palyginti su query:

```python
# Po link ekstrakcijos:
# Patikrinti: ar URL yra Amazon produkto URL su /dp/?
# Elgsenos patvirtinimas: jei galima išgauti ASIN, patikrinti ar ASIN parduotuvėje
# Tai reikalauja papildomo request → per brangu
```

**Variantas B2 (geriausia praktika):** Ištraukti `data-asin` atributą iš `item` ir patikrinti ar jis sutampa su anksčiau pamatytu:

```python
# Amazon search item struktūra:
# <div data-asin="B0XXXXXXXXX" data-component-type="s-search-result">
asin_from_div = item.get("data-asin", "")
# Jei asin_from_div ir asin_from_link nesutampa → potenciali klaida
```

**Variantas B3 (prieinamas):** Iš URL ištraukti ASIN ir vizualiai patikrinti ar set numeris nėra įtrauktas į ASIN. Bet ASIN yra opaque (ne readable) — neveiks.

**Variantas B4 (pagrindinis):** Patikrinti ar kaina neatsiranda iš `post_process` Fix C (suspicious price). 76451 = €64.79 vs Elesen = €34.99 — mediana ≈ €64.79 (2 elementai). Elesen €34.99 < 40% mediainos → suspicious. Fix C jau sugaudo tai → **jau padeda**, bet ne visai sprendžia.

**Efektyviausias trumpalaikis Fix B:** Neleisti h2.aria-label būti iš skirtingo `data-asin` nei item container:

```python
# Papildomas validavimas:
item_asin = item.get("data-asin", "")
url_asin = asin_m.group(1) if asin_m else ""
if item_asin and url_asin and item_asin != url_asin:
    # URL ASIN nesutampa su item ASIN — potenciali reklaminė klaida
    # Naudoti item_asin vietoj url_asin
    url = f"https://www.amazon.{domain}/dp/{item_asin}"
    aff = f"https://www.amazon.{domain}/dp/{item_asin}?tag={aff_tag}" if aff_tag else url
```

Tai NEAPSAUGO nuo keyword-stuffed title, bet užtikrina, kad URL ir kaina bent jau iš to paties `item` ASIN.

---

## ATSAKYMAI Į SPECIFINIUS KLAUSIMUS

| Klausimas | Atsakymas |
|---|---|
| 1. Ką scraper grąžina kaip "url" Elesen'ui? | SPA: grąžina `slug = ""` → homepage. DOM: `href = ""` → homepage |
| 2. Ar Elesen ištraukiamas produkto href? | Dažnai NE — SPA JSON produktai neturi pilno URL lauko |
| 3. Kaip validuojama 76430 vs 76451? | NETEISINGAI — tikrinamas tik title, ne ASIN/URL |
| 4. Ar imamas pirmas paieškos rezultatas? | Taip — pirmasis praeiną is_relevant_result |
| 5. Ar kaina ir URL iš to paties produkto? | Šiuo atveju TAIP (abu 76451). Title yra keyword-stuffed (rodo 76430) |
| 6. Ar kaina/URL VISADA iš to paties? | Teoriškai NE (keli /dp/ linkai item'e galimi). Šiuo atveju taip |
| 7. Ryšys su identify vs scan keliu? | Nėra — abu bug'ai yra scraping logikoje, nepriklausomai nuo užklausos kilmės |

---

## PRIORITETAI

| Bug | Rimtumas | Fix sudėtingumas | Siūloma |
|---|---|---|---|
| A: Elesen homepage | AUKŠTAS — naudotojas negali pirkti | ŽEMAS — 3 kodo eilutės | Diegti iš karto |
| B: Amazon wrong product | AUKŠTAS — klaidinga kainų lyginimas | VIDUTINIS — reikia ASIN validacijos | Diegti su B4 variantu |

Rimčiausias scenarijus: **kaina iš vieno produkto + URL į kitą** teoriškai galimas bet ŠIUO ATVEJU nepasitvirtino. Tačiau B4 ASIN validacija uždaro šią spragą visam laikui.
