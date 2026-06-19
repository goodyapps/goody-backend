# PRODUCT_GAPS.md
**Data:** 2026-06-20 | **Šaka:** security-night  
**Tikslas:** Atviras ir griežtas produkto silpnybių įvertinimas — kur "geriausia reali kaina" pažadas sulaužomas

---

## ĮSPĖJIMAS: ŠIS DOKUMENTAS YRA KRITINIS

Tai nėra lista "ką pataisyti". Tai yra atviras atsakymas: **kur Goody nepateisina savo pažado "it must be the best app who offers real price"?**

---

## G1 — PARDAVĖJŲ APRĖPTIS: KRITINĖ SPRAGA (DIDELĖ)

**Pažadas:** "Geriausia kaina"  
**Realybė:** 8 parduotuvės. Kaina24.lt — 1200+.

**Konkreti situacija:**
- Vartotojas ieško "Samsung Galaxy S24" → Goody rodo Varle, Pigu, Elesen, Amazon.DE, Amazon.PL kainas
- Kaina24 rodo dar 15+ LT pardavėjų (Tele2, Bitė, Mobilly, Kilobaitas, RD.lt, Skytech, DataLink...)
- Goody galėtų rodyti €649, Kaina24 vartotojas randa €599 iš pardavėjo, kuris Goody neparodytas

**Poveikis:** Vartotojas, kuris lyginamai naudoja abu, visada ras geresnę kainą Kaina24 (dėl aprėpties pločio). Goody "geriausia kaina" gali būti visiškai klaidinga.

**Kaip dabar kovoja:** Amazon.DE/PL integracija randa tarptautinę kainą, kuri kartais mažesnė nei bet kuri LT parduotuvė. Tai GALI kompensuoti.

**Sprendimas (ilgalaikis):** Affiliate API integracija su daugiau pardavėjų. Arba: **nustatyti lūkesčius** — "Tikriname geriausias 6 LT parduotuvės + Amazon Europoje".

---

## G2 — KAINŲ ISTORIJA: DAŽNAI TUŠČIA (DIDELĖ)

**Pažadas:** "Stebėk kainų istoriją"  
**Realybė:** Kainų istorija kaupiama tik tada, kai kažkas jau ieškojo to produkto Goody. Naujam vartotojui — tuščia.

**Konkreti situacija:**
- Naujas vartotojas ieško "LG OLED 65C3" → pirmą kartą → kainų istorija = "Duomenys renkami..."
- Kaina24 turi kainų istoriją šiam TV nuo 2022m. (ilga istorija).

**Poveikis:** "Ar tai gera kaina?" klausimas be atsakymo. Vartotojas negali apsispręsti.

**Kodas:** `get_price_history()` rašo į Supabase, bet tik kai tas query jau buvo ieškomas. Bootstrap laikotarpis yra ilgas.

**Sprendimas:** Pre-populate populiariausių produktų kainų istorija. Arba: partnerystė su Kaina24 duomenimis (nerealiu trumpuoju laikotarpiu).

---

## G3 — WATCHLIST: NEVEIKIA KITAME TELEFONE (VIDUTINĖ)

**Pažadas:** "Stebėk kainą, gauk pranešimą"  
**Realybė:** Watchlist saugoma localStorage — išnyksta kai:
- Vartotojas atidaro Goody naujame telefone / kompiuteryje
- Naršyklė išvalo localStorage (iOS Safari agresyviai tai daro)
- Vartotojas atsidaro incognito

**Poveikis:** Retention funkcija, kuri "pamiršta" vartotoją. Tai sumažina pasitikėjimą — "Goody pamiršo mano sąrašą".

**Kodas:** `localStorage.setItem("goody_watchlist_v2", ...)` — pilnai kliento pusėje.

---

## G4 — PAIEŠKOS TIKSLUMAS: LEGO PROBLEMA (VIDUTINĖ)

**Pažadas:** "Rask tikslią kainą"  
**Realybė:** identify-product generuoja semantinę query ("LEGO Harry Potter Hogwarts") vietoj kodo query ("LEGO 76430") → P1_DIVERGENCE.md dokumentuoja ~35% divergenciją LEGO kategorijoje.

**Konkreti situacija:**
- Vartotojas fotografuoja LEGO 76430 Hogwarts pakuotę
- Goody rodo... "Hogwarts board game" arba "Harry Potter puzzle" (skirtingas produktas)
- Vartotojas perka neteisingą produktą arba praranda pasitikėjimą

**Kodas:** `identify-product` grąžina `search_query = vision.get("search_query")` — AI-generated, dažnai be modelio numerio. Fix: R1 iš P1_DIVERGENCE.md.

---

## G5 — BALSO PAIEŠKA: TRINANT 30% VARTOTOJŲ (MAŽESNĖ)

**Pažadas:** "Ieškok balsu"  
**Realybė:** Tik Chrome. iOS Safari vartotojai (didelė dalis mobiliojo srauto) gauna klaidos toast'ą.

**Poveikis:** Balso paieška yra reklamuota funkcija — kai neveikia 30% telefonų, tai yra pažado neįvykdymas.

---

## G6 — RUSŲ KALBA: PUSIAU IMPLEMENTUOTA (MAŽESNĖ)

**Pažadas:** Implicitas — app rodo `ru` kaip kalbos pasirinktį kai kuriose vietose  
**Realybė:** `LANGS["ru"]` neegzistuoja → fallback į `LANGS["en"]`. Rusiškai kalbantis vartotojas mato maišytą LT/EN UX.

**Poveikis:** Nors mažesnė nišė, bet tai yra konkretus, matomas nesubalansuotas UX.

---

## G7 — KAINŲ TIKSLUMAS: BEZ PRISTATYMO (VIDUTINĖ)

**Pažadas:** "Geriausia reali kaina"  
**Realybė:** Rodomos produkto kainos BEZ pristatymo mokesčio.

**Konkreti situacija:**
- Varle rodo €49.99, Pigu rodo €47.99 → Goody sako "Pigu pigiausias"
- Bet Pigu pristatymas €4.99, Varle pristatymas €0 (>€30 pirkiniams)
- **Reali kaina:** Varle = €49.99, Pigu = €52.98 → Varle yra pigesnis

**Kodas:** `_make_result()` grąžina tik `price` — be `shipping`. Scraperiai nescrapina shipping kainų (sudėtinga — priklauso nuo pirkinio dydžio, vietos).

**Poveikis:** "Geriausia reali kaina" pažadas yra techniškai klaidingas jei kainoje nėra pristatymo.

---

## G8 — POPULIARŪS PRODUKTAI: NĖRA KONTEKSTO (MAŽESNĖ)

**Pažadas:** Implicit — "Goody žino geriausias kainas"  
**Realybė:** "Populiarios paieškos" chips yra sutrumpinti ir be konteksto (be kainos, be kategorijos).

**Konkreti situacija:** Vartotojas mato chip "iPhone 15 Pro" — paspaudžia → gauna paieškos rezultatą. Bet nežino iš anksto ar kaina šiandien yra gera ar bloga.

---

## SILPNYBIŲ PRIORITETŲ ŽEMĖLAPIS

```
          POVEIKIS PAŽADUI
KRITINIS  │ G1: Pardavėjų aprėptis ◄── didžiausia problema
          │ G2: Kainų istorija tuščia
          │
VIDUTINIS │ G3: Watchlist išnyksta    G4: Tikslumas LEGO
          │ G7: Pristatymas neįskaitytas
          │
MAŽESNIS  │ G5: Balso Chrome only    G6: RU kalba pusiau
          │ G8: Populiarios paieškos be konteksto
          │
          └────────────────────────────────────────
               MAŽAS DARBAS    DIDELIS DARBAS
```

---

## PAGRINDINĖ IŠVADA

**"It must be the best app who offers real price"** — šiuo metu Goody yra **geriausias** pagal:
- Vizualinę paiešką (unikalus LT rinkoje)
- Amazon.DE/PL kainų integraciją
- Paieškos greitį (SSE streaming)

Bet yra **rizikingas** dėl:
- Pardavėjų aprėpties (G1) — vartotojas gali rasti geresnę kainą Kaina24
- Kainų istorijos (G2) — naujiems produktams neturi duomenų
- Pristatymo neįskaitymo (G7) — "reali kaina" nėra pilnai reali

**Šie trys punktai yra pirmiausia, prieš pridedant naujų funkcijų.**
