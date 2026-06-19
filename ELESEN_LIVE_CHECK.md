# ELESEN_LIVE_CHECK.md
**Data:** 2026-06-19  
**Tikslas:** Nustatyti tikslią priežastį (A/B/C) — kodėl "LEGO 76430 Hogwarts" grąžina Nintendo žaidimą  
**Metodas:** Live HTTP diagnostika + HTML analizė

---

## IŠVADA PIRMA: Elesen HTML neturi produktų (JS-rendered puslapis)

Tiesioginė HTTP užklausa `https://www.elesen.lt/paieska?q=LEGO%2076430%20Hogwarts`:
- HTTP 200 OK, 165 929 simboliai
- **Nėra `__NEXT_DATA__`, `__NUXT_DATA__`, `product-card` klasių, produktų JSON**
- "76430" HTML'e randamas **tik** URL atspindžiuose (slapukų dialoge, paieškos inpute, GTM skripte)
- Google Tag Manager evento duomenys: `"items":[]` — **0 produktų**

```html
<!-- GTM: Elesen grąžino 0 produktų šiai paieškoje -->
{"events":[{"name":"view_item_list","params":{
    "items":[], "itemListName":"SearchList"
}}]}
```

**Kodėl:** Elesen naudoja **Nosto** paieškos platformą. Produktai kraujami per JavaScript AJAX kvietimus PO puslapio užkrovimo. Statinis HTML yra tuščias skeletas.

---

## IŠVADA ANTRA: `scrape_elesen` grąžina 0 rezultatų šiai paieškoje

```
[Elesen.lt] embedded JSON extraction: 0 results
[Elesen] 0 items
[Direct 200] https://www.elesen.lt/paieska?q=LEGO%2076430%20Hogwarts
[Elesen] failed 200
Oficialus scrape_elesen() rezultatas: 0 rezultatų
```

Tai galioja ir ScraperAPI render_js=True keliui (testavimo metu). ScraperAPI gali nepalaukti kol Nosto AJAX pakrauna produktus (7s timeout, Nosto kraujas async).

---

## VERDIKTAS: NĖRA A/B/C — tai CACHE bug

**Priežastis D (nenumatyta): Goody cache grąžino seną rezultatą iš kitos paieškos.**

### Kas nutiko (rekonstrukcija):

1. **Anksčiau** vartotojas (arba kitas) ieškojo "LEGO Harry Potter" arba panašiai → Elesen grąžino Nintendo Switch žaidimą → rezultatas įrašytas į Goody cache.

2. **Šiai paieška** "LEGO 76430 Hogwarts" → Elesen grąžina 0 rezultatų (Nosto AJAX, nepagauna).

3. **Bet!** Goody cache key yra `md5("v64:lego 76430 hogwarts:lt")` — **ne** tas pats kaip "LEGO Harry Potter". Tai **ne** klasikinis cache collision.

### Tikroji rekonstrukcija — ScraperAPI padavė rezultatus kitu laiku:

ScraperAPI `render_js=True` **KARTAIS** suspėja pagauti Nosto AJAX rezultatus (priklausomai nuo serverio greičio), **KARTAIS** nepagauna. Kai nepagauna — 0 rezultatų. Kai pagauna — grąžina ką Elesen davė.

Elesen paieška "LEGO 76430 Hogwarts" naudojant Nosto gali grąžinti:
- LEGO Hogwarts Castle 76430 (teisingas) 
- LEGO Harry Potter Switch žaidimą (neteisingas — Elesen Nosto susieja per "Harry Potter" semantiką)

Kai `scrape_elesen` pavyko (ScraperAPI suspėjo) — grąžino žaidimą + rinkinį. Goody pasiliko žaidimą.

---

## PATVIRTINTAS FAKTAS: Elesen URL struktūra skiriasi

HTML'e rastos kelios URL formos:
- `/paieska?q=...` — šiuo metu naudojama (teisingas endpoint) ✓
- `/rezultatus/LEGO 76430 Hogwarts` — kita forma, rodoma kaip "search history" šablonas
- `/en/search/LEGO+76430+Hogwarts` — angliška versija

Nosto paieška naudoja `/rezultatus/` ar `/search/` - gali grąžinti kitokius rezultatus nei `/paieska`. Tai verta patikrinti.

---

## KODĖL is_relevant_result LEIDO žaidimą (teorinis atvejis)

Jei Elesen Nosto grąžino žaidimą su pavadinimu:  
`"LEGO Harry Potter Kolekcinė Žaidimų Serija 1-7 Nintendo Switch"` (be "76430") →

```
is_relevant_result("LEGO 76430 Hogwarts", "LEGO Harry Potter ..."):
  model_tokens = ["76430"]
  "76430" NOT in title → return False  ✓ (turėtų filtruoti!)
```

**Tai turėtų filtruoti!** Bet jei Elesen Nosto grąžino su pavadinimu:  
`"LEGO Harry Potter 76430 Nintendo Switch"` (su "76430" katalogo klaidoje) →

```
is_relevant_result("LEGO 76430 Hogwarts", "LEGO Harry Potter 76430 Nintendo Switch"):
  model_tokens = ["76430"]
  "76430" IN title → _model_in_title = True
  brands_in_q = ["lego"] → lego in title → True
  → return True  ✗ (PRALEIDŽIA žaidimą!)
```

Tai **Priežastis A** — bet nepatikrinama be ScraperAPI rendered HTML.

---

## KAS TIKSLIAI NUTINKA (žingsnis po žingsnio):

```
Vartotojas: ieško "LEGO 76430 Hogwarts"
    ↓
scrape_elesen("LEGO 76430 Hogwarts")
    ↓ Direct HTTP → 200 OK, bet HTML tuščias (Nosto AJAX neįkrautas)
    ↓ scrape: 0 rezultatų
    ↓ ScraperAPI render_js=True → kartais pagauna Nosto rezultatus, kartais ne
    ↓ [kai pagauna] Elesen Nosto grąžina: Switch žaidimas €34.99 (Elesen katalogo klaida)
    ↓ is_relevant_result("LEGO 76430 Hogwarts", "LEGO Harry Potter 76430 Nintendo Switch")
       → jei "76430" žaidimo pavadinime: True (praleidžia)
       → jei "76430" nėra: False (filtruoja, 0 rezultatų)
    ↓ [0 rezultatų] → retry cascade: _model_code_variants → ["LEGO 76430 Hogwarts"] (tik vienas)
    ↓ Elesen vėl 0 → galutinai 0 Elesen rezultatų arba žaidimas
    ↓ [jei žaidimas liko] → Goody rodo žaidimą €34.99 kaip Best Deal
    ↓ Vartotojas paspaudžia "Buy now" → Elesen žaidimo puslapis
```

---

## ELESEN NOSTO ENDPOINT ATRADIMAS

Elesen naudoja `/rezultatus/` URL formą search history šablonuose. Verta patikrinti:
```
https://www.elesen.lt/rezultatus/LEGO%2076430%20Hogwarts
```
Gali grąžinti kitokį HTML su faktiniais produktais.

---

## PASIŪLYMAS: Kaip pataisyti (NEATLIKTA)

### Trumpalaikis fix — produkto tipo filtras:

Po `is_relevant_result`, jei query turi LEGO set numerį (4-6 skaitmenų), papildomai tikrinti:

```python
# Jei produkto pavadinime YRA žaidimų konsolės žymė → atmesti
_GAME_KEYWORDS = {"nintendo switch", "ps4", "ps5", "xbox", "pc game", "steam", 
                  "playstation", "žaidimas nintendo", "game for nintendo"}
if any(kw in name.lower() for kw in _GAME_KEYWORDS):
    if not any(kw in query.lower() for kw in _GAME_KEYWORDS):
        skip  # Ieškoma rinkinio, grąžinamas žaidimas
```

**Efektas:** Atmeta Nintendo Switch, PS4, PS5 žaidimus kai query jų nepieško.  
**Rizika:** ŽEMA — šie žodžiai labai specifiniai produkto tipui.

### Papildomas fix — Elesen URL atnaujinimas:

Patikrinti ar `https://www.elesen.lt/rezultatus/{query}` grąžina geresnę HTML struktūrą nei `/paieska?q=`.

### Ilgalaikis fix:

Elesen scraper reikia atnaujinti pagal jų naują Nosto-based frontend. Gal reikia tiesiogiai kviesti Nosto API (jei viešas endpoint yra).

---

## TESTAVIMO REKOMENDACIJA

Norint 100% patvirtinti priežastį A, reikia:
1. ScraperAPI rendered HTML "LEGO 76430 Hogwarts" query → patikrinti ar Elesen Nosto grąžina žaidimą su "76430" pavadinime
2. Arba: Render logai iš momento kai vartotojas matė klaidingą rezultatą — ieškoti `[Elesen]` eilučių

---

## SANTRAUKA

| Klausimas | Atsakymas |
|---|---|
| Ar Elesen statinis HTML turi produktų? | **NE** — Nosto AJAX |
| Ar `scrape_elesen` veikia dabar? | **Ne patikimai** — 0 rezultatų per direktą, ScraperAPI nepastovus |
| Priežastis A (76430 pavadinime)? | **Tikėtina**, nepatvirtinta be ScraperAPI rendered HTML |
| Priežastis B (Fix A1 numetė)? | **Neatitinka** — jei scrape grąžina 0, nėra ką numesti |
| Priežastis C (all_results fallback)? | **Galima** — jei ScraperAPI grąžino žaidimą ir is_relevant_result leido |
| Pagrindinis sistemos bug? | **`is_relevant_result` neleidžia filtruoti pagal produkto tipą** |
| Siūlomas fix? | Konsolės žaidimų raktažodžių filtras + Elesen Nosto endpoint patikra |
