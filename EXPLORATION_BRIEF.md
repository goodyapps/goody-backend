# EXPLORATION_BRIEF.md
**Data:** 2026-06-20 | **Šaka:** security-night  
**Užduotis:** Produkto/UX tyrinėjimas — vykdyta autonomiškai per naktį  
**Vizija:** "it must be the best app who offers real price"

---

## 5 SVARBIAUSI RADINIAI

### 1. Goody yra UNIKALUS — nei vienas LT konkurentas neturi AI foto paieškos

Kaina24, Kainos, Pricer, inBaltic — niekas. Foto paieška yra Goody vienintelė ir nepakartojama diferenciacija Baltijos rinkoje. Google Lens+Shopping yra potenciali ateities grėsmė, bet dabar LT rinkoje — nėra.

**Ką tai reiškia:** Goody neturi tiesioginio konkurrento pagrindiniame use case ("fotografuok produktą parduotuvėje → rask pigiau"). Tai yra Blue Ocean. Šią poziciją reikia įtvirtinti greičiau nei ji atsiranda.

---

### 2. "Geriausia reali kaina" pažadas turi KRITINĘ SPRAGĄ — pardavėjų aprėptis

Goody: 8 parduotuvės. Kaina24: 1200+. Vartotojas, kuris lygina abu, visada ras kažką, ko Goody neranda. Tai yra sisteminis, ne techninis klausimas — kiekvienas naujas scraperis yra savaitinis darbas.

**Ką tai reiškia:** Arba komunikuoti aiškiai ("tikriname geriausias 6 LT parduotuves + Amazon Europoje"), arba Amazon.DE/PL integracija turi būti pagrindinė vertės propozicija — tarptautinės kainos, kurių Kaina24 nerodo.

---

### 3. Scan patirtis yra gera, bet PERNELYG LĖTA kritiniam momentui

Nuotrauka → pirmos kainos: iki **40 sekundžių** blogiausiu atveju (30s identify + 10s pirma parduotuvė). SSE streaming labai pagerina suvokiamą greitį — bet vartotojas, stovas parduotuvėje su telefonu, netrpėliauja 40s.

**Ką tai reiškia:** Identify-product greitis yra bottleneck. Gemini (gratis) kartais lėtas. Jei Gemini grąžina per ~5s, o Haiku per ~3s — abu veikia lygiagrečiai — blogiausias atvejis yra Gemini timeout (10s) + Haiku kaip fallback = ~13s identify. Tai priimtina. Bet 30s timeout yra per didelis be progreso indikatoriaus.

---

### 4. Rusų kalba yra neišbaigta — ir tai yra prarastas segmentas

LANGS["ru"] neegzistuoja. Lietuvoje yra ~150,000 rusiškai kalbančių. Turistai iš Vokietijos / Lenkijos kalbantys rusiškai. Tai nišinis segmentas, bet tiksliai tas segmentas, kuris naudoja "parduotuvėje nufotografuok" use case.

**Ką tai reiškia:** ~200 eilučių frontend vertimų = pilnas RU palaikymas. Žema kaina, aiški auditorija.

---

### 5. Watchlist ir kainų istorija yra silpniausios retention funkcijos

Watchlist: dingsta keičiant naršyklę/telefoną (localStorage only). Kainų istorija: dažnai tuščia naujiems produktams. Push pranešimų nėra. Tai reiškia, kad po pirmojo apsilankymo **nėra mechanizmo grąžinti vartotoją**.

**Ką tai reiškia:** Goody šiuo metu yra vienkartinė priemonė, ne įprotis. "Patikrinkite dabar" veikia, bet "grįžk rytoj kai kaina kris" — neveikia.

---

## PRADINĖ REKOMENDACIJA

Vartotojas pasakė: **"it must be the best app who offers real price."**

Šiuo metu Goody yra **geriausias** pagal vieną dimensiją (foto paieška), bet **ne geriausias** pagal kitą (aprėptis, pristatymo kaina, kainų istorija).

**Siūlomas prioritetas artimiausioms savaitėms:**

```
SAVAITĖ 1: Stabilizuoti core pažadą
├── Fix: identify-product → naudoti brand+model_code kai AI randa kodą (R1)
│         → mažina LEGO tipo divergenciją ~35%→~10%
├── UX: Scan patarimas prieš kamerą (A2 iš FEATURE_IDEAS)
│         → mažina failed scans, geresnė pirmoji patirtis
└── Data: Aiški komunikacija "tikriname 8 parduotuves" vietoj "geriausia kaina"

SAVAITĖ 2-3: Pridėti vieną retention spąstą
├── Push pranešimai (B2) — didžiausias retention ROI
│   arba
└── Watchlist serverio pusėje (B1) — žema rizika

SAVAITĖ 4: Naujų vartotojų segmentas
└── Rusų kalba (B3) — 150k potencialių LT vartotojų
```

---

## DOKUMENTAI ŠIOJE SERIJOJE

| Dokumentas | Turinys |
|---|---|
| [UX_EXPLORATION.md](UX_EXPLORATION.md) | 9 trintys vartotojo kelyje, onboarding analizė, UX balai |
| [MARKET_RESEARCH.md](MARKET_RESEARCH.md) | Kaina24/Kainos/Pricer/inBaltic/Pricesnap palyginimas, konkurencinis žemėlapis |
| [FEATURE_IDEAS.md](FEATURE_IDEAS.md) | A/B/C kategorijų idėjos su darbo apimtimis |
| [PRODUCT_GAPS.md](PRODUCT_GAPS.md) | 8 vietos kur "geriausia reali kaina" pažadas sulaužomas |
| **[EXPLORATION_BRIEF.md](EXPLORATION_BRIEF.md)** | **Šis dokumentas — 5 svarbiausi radiniai + rekomendacija** |

---

*Tyrinėjimas atliktas autonomiškai per naktį. Jokio kodo nekeis — tik analizė ir dokumentacija.*
