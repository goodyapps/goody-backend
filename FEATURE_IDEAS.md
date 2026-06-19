# FEATURE_IDEAS.md
**Data:** 2026-06-20 | **Šaka:** security-night  
**Kontekstas:** Remiantis kodo analize + rinkos tyrimu + user produkto vizija "it must be the best app who offers real price"  
**Prioritetai:** A = didelė vertė / mažas darbas, B = didelė vertė / didelis darbas, C = mažas darbas / menka vertė

---

## A KLASĖ: DIDELĖ VERTĖ / MAŽAS DARBAS

### A1 — "Kaina prieš metus" badge

**Idėja:** Prie kiekvieno rezultato, kur yra kainų istorija, rodyti `"▼ X% pigesnis nei prieš 6 mėn."` arba `"▲ Pabrangs: geriausia dabar pirkti"` badge'ą.

**Kodėl veikia:** Kodas jau turi `get_price_history()` ir `renderPriceHistory()`. Reikia tik pridėti badge kalkuliavimo logiką prie `renderResults()` — duomenys jau yra.

**Vartotojo vertė:** Aiški, konkreti priežastis pirkti DABAR. Tai yra "geriausia reali kaina" pažado įgyvendinimas.

**Darbo apimtis:** ~30 eilučių frontend (badge render + % kalkuliacija)

---

### A2 — Scan patarimas prieš kamerą

**Idėja:** Prieš atidarant kamerą, rodyti 2s "tooltip" su: "Fotografuok etiketę/barcode. Geresnis apšvietimas = tikslesnis atpažinimas."

**Kodėl veikia:** Dabar vartotojas sužino apie blogą nuotrauką TIK po identify klaidos (~30s vėliau). Proaktyvus patarimas sumažins failed scans kiekį.

**Darbo apimtis:** ~15 eilučių — paprastas toast/overlay prieš `openCam()` iškvietimą.

---

### A3 — "Geriausia kaina Lietuvoje" patvirtinimas

**Idėja:** Jei mažiausia kaina yra žymiai mažesnė nei kitos (>15% skirtumas), rodyti: `✓ Geriausias pasiūlymas Lietuvoje šiandien`.

**Kodėl veikia:** Išplečia dabar esantį "Verdict" bar logiką. Verdict bar jau skaičiuoja pigiausią kainą — reikia tik pridėti "Geriausia Lietuvoje" tekstą kai Amazon.DE nėra pigiausias, o LT parduotuvė yra žymiai žemesnė.

**Darbo apimtis:** ~10 eilučių

---

### A4 — Rate limit: pasiūlyti watchlist prieš einant

**Idėja:** Kai vartotojas pasiekia rate limitą, vietoj "Grįžk rytoj" rodyti: "Išsaugok šiandienius radinius — stebėk kainą ir gaukite pranešimą kai ji kris."

**Kodėl veikia:** Rate limit šiuo metu yra dead-end. Watchlist konversija čia galėtų būti didelė — vartotojas yra aktyvus, tik be daugiau paieškų.

**Darbo apimtis:** ~20 eilučių — modifikuotas rate limit ekranas + deeplink į watchlist

---

### A5 — "Ar nupirkai?" quick poll

**Idėja:** Kai `visibilitychange` event fiksuoja grįžimą iš parduotuvės (jau implementuota!), papildomai klausti: `"Ar nupirkai? [✓ Taip] [✗ Ne]"` — mikro-apklausa.

**Kodėl veikia:** Šiuo metu back banner tik sako "Grįžti į Goody". Conversion data būtų vertingas (kurios parduotuvės konvertuoja geriau) + vartotojas jaučia, kad app domisi juo.

**Duomenų nauda:** Galima matyti kurio pardavėjo "Buy now" paspaudimas dažniau baigiasi pirkimu.

**Darbo apimtis:** ~25 eilučių + 1 naujas `/api/log-purchase` endpoint

---

## B KLASĖ: DIDELĖ VERTĖ / DIDELIS DARBAS

### B1 — Watchlist serverio pusėje (ne localStorage)

**Dabartinė situacija:** Watchlist saugoma `localStorage` — dingsta pakeitus naršyklę, išvalžius datos, arba naujame telefone.

**Idėja:** Watchlist saugoti serveryje — tiesiog IP + query + target_price. Nereikia vartotojo paskyros — IP-based (kaip rate limit).

**Kodėl svarbu:** "Stebi kainą" yra viena iš pagrindinių retention funkcijų. Jei ji dingsta — vartotojas ir grįžti nemotyvuotas.

**Rizika:** IP gali keistis (mobilusis). Sprendimas: local + server sync — abu. localStorage lieka kaip pirminė kopija.

**Darbo apimtis:** ~100 eilučių + Supabase lentelė + CORS update

---

### B2 — Push pranešimai kainų kritimui

**Dabartinė situacija:** Kainų stebėjimas yra — bet pranešimų nėra. Vartotojas turi pats grįžti ir patikrinti.

**Idėja:** Web Push API — paslauga siunčia pranešimą kai stebimo produkto kaina krinta žemiau nustatytos.

**Kodėl svarbu:** Tai yra skirtumas tarp "geros aplikacijos" ir "aplikacijos kuri dirba tau". Kai kaina kris, vartotojas gauna pranešimą — ir grįžta į Goody. Retention loop.

**Reikalavimas:** Service Worker + Push API + serverio VAPID raktai + background job kainų tikrinimui

**Darbo apimtis:** ~300 eilučių (didelis) + Render cron job + VAPID setup

---

### B3 — Rusų kalbos pilnas palaikymas

**Dabartinė situacija:** LANGS objekte nėra `ru` — rusiškai kalbantys gauna anglišką fallback.

**Idėja:** Pridėti pilną `LANGS.ru` objektą (~150 vertimų + OB_STEPS ru versija).

**Kodėl svarbu:** Lietuva turi ~5-7% rusiškai kalbančių gyventojų. Migranto UX (foto parduotuvėje → palyginti kainas) — tai tiksli Goody auditorija. Rusiškai kalbantys turistai iš Vokietijos/Lenkijos dar daugiau.

**Darbo apimtis:** ~200 eilučių frontend (vertimai) + naršyklės auto-detect `ru` support

---

### B4 — Latvių/estų pardavėjų integravimas

**Idėja:** Pridėti bent 1-2 pagrindinius LV/EE pardavėjus (pvz., 220.lv, Euronics.ee).

**Kodėl svarbu:** inBaltic.eu turi tokią funkciją — Goody galėtų pranokti juos su foto paieška + Baltijos kainomis viename ekrane.

**Rizika:** Kiekvieno naujo scraper kūrimas yra 2-4 dienų darbas + ScraperAPI papildomi kreditai.

**Darbo apimtis:** Didelis — scraper + HTML analizė + relevance tuning

---

### B5 — "Ar tai gera kaina?" AI verdiktas

**Idėja:** Po rezultatų rodymo, jei yra kainų istorija, AI generuoja 1 sakinio verdiktą: "Šio produkto vidutinė kaina yra €XX, šiandien €YY — tai X% žemiau vidurkio."

**Kodėl veikia:** Vartotojas negali pats interpretuoti kainų grafiko greitai. Vienas aiškus sakinys ("PIRK DABAR" vs "PALAUKTI") yra "geriausia reali kaina" pažadas tekstiniame pavidale.

**Darbo apimtis:** ~50 eilučių frontend + backend verdikto kalkuliacija (nereikia AI, tik matematika)

---

## C KLASĖ: MAŽAS DARBAS / MENKA VERTĖ (skirti vėlai)

### C1 — Produktų palyginimas šalia šalia

**Idėja:** Galimybė pažymėti 2-3 produktus ir matyti juos šalia šalia su kainomis.

**Kodėl žema prioritetas:** Goody vartotojai dažnai ieško 1 produkto kainos, ne lygina produktus tarpusavyje. Šis use-case labiau tinka Kainos.lt / review svetainėms.

---

### C2 — Kategorijų paieška naršymui

**Idėja:** Paspaudus kategoriją (Elektronika → Telefonai) rodyti populiarius produktus toje kategorijoje.

**Kodėl žema prioritetas:** Reikalauja didelės DB su kuratoriais produktų. Goody stiprybė yra reaktyvi paieška, ne naršymas.

---

### C3 — Referral programa

**Idėja:** "Pasiūlyk draugui" funkcija su unikaliu nuoroda.

**Kodėl žema prioritetas:** Be serverio-side vartotojų paskyrų — sunku sekti. Be aiškios naudos pateikti (ką draugas gauna?).

---

## PRIORITETŲ SANTRAUKA

| Prioritetas | Idėja | Poveikis | Darbas |
|---|---|---|---|
| 🥇 1 | A1: Kaina prieš metus badge | Conversion ↑ | Mažas |
| 🥇 2 | A3: Geriausia kaina LT badge | Pasitikėjimas ↑ | Mažas |
| 🥇 3 | A5: "Ar nupirkai?" poll | Data + UX ↑ | Mažas |
| 🥈 4 | B2: Push pranešimai | Retention ↑↑ | Didelis |
| 🥈 5 | B5: AI verdiktas "pirk/lauk" | Conversion ↑↑ | Vidutinis |
| 🥉 6 | B1: Watchlist serverio pusėje | Retention ↑ | Vidutinis |
| 🥉 7 | B3: Rusų kalba | Nauji vartotojai | Vidutinis |
| 📌 | A2: Scan patarimas | Scan kokybė ↑ | Labai mažas |
| 📌 | A4: Rate limit → Watchlist | Dead-end → CTA | Mažas |
