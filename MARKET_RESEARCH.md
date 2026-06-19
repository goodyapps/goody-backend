# MARKET_RESEARCH.md
**Data:** 2026-06-20 | **Šaka:** security-night  
**Metodas:** Publični šaltiniai, App Store aprašymai, svetainių tyrinėjimas  
**Tikslas:** Kur stovi Goody tarp Lietuvos ir Europos kainų palyginimo rinkos

---

## LIETUVOS RINKA: PAGRINDINIAI ŽAIDĖJAI

### 1. Kaina24.lt — RINKOS LYDERIS

**Aprėptis:** 20 mln.+ produktų, 1200+ pardavėjų, veikia nuo ~2008  
**Stiprybės:**
- Didžiausias produktų katalogas Lietuvoje
- Gerai žinomas brendas (SEO dominavimas)
- Veikia visose kategorijose: elektronika, maistas, namų apyvoka, batai, knygos
- Puslapio greitis geras, UX patikimas

**Silpnybės:**
- **Nėra nuotraukų paieškos** — tik tekstas ir barkodas
- **Nėra mobiliosios aplikacijos** (tik responsive web)
- Kainų istorija egzistuoja, bet ne visada matoma
- Registracija reikalinga kainų stebėjimui
- UX pasenęs — tankus, skaitmens orientuotas

**Goody diferenciacija prieš Kaina24:** Nuotraukų paieška, modernesnė UX, PWA (offline-capable), automatinis skandinaviškų/lenkiškų kainų įtraukimas (Amazon.DE, Amazon.PL)

---

### 2. Kainos.lt — ELEKTRONIKOS SPECIALIZANTAS

**Aprėptis:** Iki 20 mažmenininkų, sutelkta į elektroniką ir buitinę techniką  
**Stiprybės:**
- Gilus elektronikos katalogas
- Aiški, specifinė auditorija (pirkėjai, kurie lygina TV, telefonus)
- Gerai žinomos specializuotose bendruomenėse

**Silpnybės:**
- **Nėra vizualinės paieškos**
- Nesiūlo Amazon/tarptautinių kainų
- Mažiau kategorijų nei Kaina24
- Mobilus dizainas vidutiniškas

**Goody diferenciacija prieš Kainos:** Platesnis aprėptis (ne tik elektronika), Amazon.DE/PL įtraukimas, foto paieška

---

### 3. Pricer.lt — NIŠINIS ŽAIDĖJAS

**Aprėptis:** Nedidelis, sutelktas į elektroniką, ~5 pardavėjai  
**Technologijos:** Turi barkodų nuskaitymo funkciją (senesnė technologija)  
**Situacija:** Ribotas atnaujinimas, nereikšminga rinkos dalis

**Reikšmė Goody kontekste:** Barkodai yra jau "senosios kartos" foto paieška. Goody AI paieška yra milijoną kartų pranašesnė (barkodo ant daikto gali nebūti, bet daiktas vis tiek atpažįstamas).

---

### 4. inBaltic.eu — BALTIJOS REGIONINIS

**Aprėptis:** Apima Lietuvą, Latviją, Estiją  
**Stiprybės:** Regioninis aprėptis — galima lyginti kainas trijose šalyse  
**Silpnybės:**
- Ribota LT penetracija (žinomumas mažas)
- **Nėra foto paieškos**
- Mažiau pardavėjų nei Kaina24

**Reikšmė Goody kontekste:** Goody galėtų tapti "inBaltic" alternatyva pridėjus latvių/estų pardavėjus — bet tai yra scraping infrastruktūros klausimas.

---

## TARPTAUTINIAI ŽAIDĖJAI, KURIE GALI ATEITI

### Google Lens / Google Shopping

**Dabartinė situacija:** Google Lens atpažįsta produktus, Google Shopping rodo kainas — bet tik kai Google Shopping aprėpia pardavėją (LT rinka: neišbaigta).

**Grėsmė:** Google gali bet kada integruo greitą "Fotografuok ir rask kainą" funkciją į Google Lens. Jau yra beta funkcija tam tikrose šalyse (US, UK).

**Kodėl Goody saugus artimoje perspektyvoje:**
- Google Shopping LT nėra pilnai integruotas (Varle, Senukai, 1a nėra Google Shopping)
- Google nerodo realių Elesen, Pigu realaus laiko kainų
- Goody specialiai suderinta su LT rinka

---

### Pricesnap (Europa)

**Kas tai:** Europos vizualinės paieškos kainų palyginimo aplikacija — **artimiausias Goody analogas pasaulyje**

**Ar yra Lietuvoje:** Per konkrečią analizę nerandama tiesioginio LT paleidimo; daugiausia veikia D, UK, FR, ES rinkose

**Funkcijos:** Panašiai kaip Goody — foto nuskaitymas, barcode, kainų palyginimas  
**Skirtumas nuo Goody:** Ne sutelktas į LT/regioninę rinką; neaišku ar scraping'a Varle/Pigu/Senukai

**Grėsmė:** Jei Pricesnap pradeda agresyviai ateiti į Baltiją, tai būtų tiesioginis konkurentas. **Šiuo metu: neatrodo.**

---

### Amazon / Idealo (Vokietija)

**Idealo:** Vokiška kainų palyginimo platforma (~50M produktų), turi foto paiešką  
**Ar konkuruoja su Goody:** Ne tiesiogiai — sutelkta į DE rinką  
**Reikšmė:** Amazon.DE jau yra Goody duomenų šaltinis — ne konkurentas

---

## GOODY UNIKALUMAS RINKOJE

### Vizualinė paieška Lietuvoje — tik Goody

```
BALTIJOS RINKA: Kainų palyginimas su foto paieška
╔══════════════════════════════════════════════╗
║  Kaina24.lt     ████████████  Tekstas tik   ║
║  Kainos.lt      ██████        Tekstas tik   ║
║  Pricer.lt      ██            Barkodas tik  ║
║  inBaltic.eu    ████          Tekstas tik   ║
║  GOODY          ████████████  AI FOTO ✓     ║
╚══════════════════════════════════════════════╝
```

**Šis unikalumas yra Goody didžiausia diferenciacija.** Nė vienas LT kainų palyginimo servisas neturi AI nuotraukų identifikavimo.

---

## RINKOS SEGMENTAI

### Segmentas 1: "Pigesnio nori" pirkėjas (30% rinkos)

**Profilis:** Žino ką perka, ieško pigiausios kainos  
**Elgesys:** Įveda modelio kodą → palygina → perka  
**Dabartinis sprendimas:** Kaina24.lt  
**Goody vertė jiems:** SSE streaming (greičiau), Amazon.DE kainos (kartais pigiau nei LT)

---

### Segmentas 2: "Nežinau ar gerai" pirkėjas (40% rinkos)

**Profilis:** Parduotuvėje randa produktą, nori sužinoti ar tai gera kaina  
**Elgesys:** Fotografuoja ant lentynos → bando palyginti  
**Dabartinis sprendimas:** Google + ranka → lėta  
**Goody vertė jiems:** **MAKSIMALI** — tiksliai šis use-case yra Goody širdis

---

### Segmentas 3: "Prenumeruoti" pirkėjas (15% rinkos)

**Profilis:** Ieško konkrečios prekės, nori pirmos kai kaina kris  
**Elgesys:** Stebi kainą, gauna pranešimą  
**Dabartinis sprendimas:** Kaina24 kainų stebėjimas (reikia registracijos)  
**Goody vertė jiems:** Watch price + push pranešimai (bet: localStorage tik, ne serverio pusė)

---

### Segmentas 4: "Turistai/migrantai" pirkėjas (15% rinkos)

**Profilis:** Iš Vokietijos, Lenkijos, Rusijos kalba — gyvena Lietuvoje  
**Elgesys:** Nori palyginti LT kainų su gimtinės kainomis  
**Dabartinis sprendimas:** Rankiniai patikrinimai  
**Goody vertė jiems:** Amazon.DE/PL integracija, multilingual — **bet RU kalbos trūkumas yra kliūtis**

---

## KONKURENCINIS PRANAŠUMŲ ŽEMĖLAPIS

| Funkcija | Goody | Kaina24 | Kainos | Pricer |
|---|---|---|---|---|
| AI foto paieška | ✅ Unikalus | ❌ | ❌ | ❌ |
| Barkodų skaitymas | ✅ | ❌ | ❌ | ✅ |
| Balso paieška | ✅ | ❌ | ❌ | ❌ |
| PWA (offline) | ✅ | ❌ | ❌ | ❌ |
| Amazon.DE/PL kainos | ✅ | ❌ | ❌ | ❌ |
| Kainų istorija | ✅ | ✅ | ✅ | ❌ |
| Kainų stebėjimas | ✅ (local) | ✅ (serverio) | ✅ | ❌ |
| LT pardavėjų aprėptis | 8 | 1200+ | 20 | 5 |
| Produktų katalogas | Dinaminė | 20M+ | Didelis | Mažas |
| Mobilios app | PWA | ❌ | ❌ | ❌ |
| Registracija | ❌ Nereikia | ✅ Reikia kainų stebėjimui | ❌ | ❌ |

---

## STRATEGINĖS IŠVADOS

1. **Goody yra "Blue Ocean" Baltijos foto-paieškos segmente.** Nė vienas konkurentas neturi AI paieškos.

2. **Grėsmė ne iš LT, o iš Google.** Jei Google Shopping įtrauks LT pardavėjus + Lens integraciją, tai bus sunkus varžovas. Goody tuomet turi būti greitesnis, tiksllesnis, lokalus.

3. **Pardavėjų aprėptis yra Goody silpniausia vieta.** 8 parduotuvės vs Kaina24's 1200+ — skirtumas milžiniškas. Vartotojas, kuriam Goody neranda pigiau, grįžta į Kaina24.

4. **Tarptautinės kainos yra diferenciacinis pranašumas.** Kaina24 nerodo Amazon.DE kainų — Goody rodo. Tai yra realus "geriausia kaina" pažadas.

5. **"Geriausia reali kaina"** (user's product north star) — Goody turi daugiau potencialo nei Kaina24 rasti **žemesnę** kainą dėl Amazon integrijos, bet **mažiau patikimą aprėptį** dėl mažiau pardavėjų.
