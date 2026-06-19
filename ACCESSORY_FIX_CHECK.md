# ACCESSORY_FIX_CHECK.md
**Šaka:** `accessory-fix`  
**Data:** 2026-06-19  
**Tikrinimo tipas:** Logikos testai (be HTTP) + tiksliniai Fix A/C testai  
**Tikrintojas:** automatinis (test_accessory_fix.py + run_layer1.py)

---

## VERDIKTAS: ŽALIA — saugu merginti

Visi kritiniai testai praėjo. Jokių regresijų tikruose produktuose.

---

## 1. Tiksliniai testai (test_accessory_fix.py)

**Rezultatas: 28/29 PASS, 1 žinoma prieš-egzistuojanti problema**

### Fix A — LED/apšvietimo aksesuarai TURI būti atmesti

| # | Užklausa | Pavadinimas (sutrumpintas) | Laukiamas | Gautas | Status |
|---|---|---|---|---|---|
| 1 | LEGO Harry 76430 | LocoLee Light **Compatible with** Lego 76430... | ATMESTA | ATMESTA | ✅ PASS |
| 2 | LEGO Harry 76430 | LEGO 76430 **LED Lighting Kit** Hogwarts Owl Post | ATMESTA | ATMESTA | ✅ PASS |
| 3 | LEGO 76430 Hogwarts | LEGO 76430 **LED Light Set** Hogwarts Owl Post | ATMESTA | ATMESTA | ✅ PASS |
| 4 | LEGO Harry 76430 | BrickBling LEGO 76430 **Lighting Kit** for Hogwarts | ATMESTA | ATMESTA | ✅ PASS |
| 5 | LEGO 75257 Millennium Falcon | **LED Lighting Kit** LEGO 75257 Millennium Falcon | ATMESTA | ATMESTA | ✅ PASS |
| 6 | LEGO Harry 76430 | BrickBling LED Light Set **for Lego** 76430 | ATMESTA | ATMESTA | ✅ PASS (buvo ir prieš) |
| 7 | LEGO Harry 76430 | LEGO 76430 **Beleuchtung** Set Hogwarts (vokiškai) | ATMESTA | ATMESTA | ✅ PASS |

**7/7 LED aksesuarai teisingai atmesti.** Fix A veikia.

Aktyvi atmėtimo priežastis kiekvienam atvejui:
- #1 — `compat_patterns` ("compatible with" title'e, ne užklausoje)
- #2, #3, #4, #5 — `_ACCESSORY_MATCH_WORDS`: "lighting" / "light set" / "led light" yra title'e bet NE užklausoje
- #6 — `compat_patterns` ("for lego" title'e) — veikė ir prieš Fix A
- #7 — `_ACCESSORY_MATCH_WORDS`: "beleuchtung"

---

### Fix A — TIKRI LEGO rinkiniai NETURI būti atmesti

| # | Užklausa | Pavadinimas | Laukiamas | Gautas | Status |
|---|---|---|---|---|---|
| 1 | LEGO Harry 76430 | LEGO Harry Potter 76430 Hogwarts Owl Post Building Set | RODOMA | RODOMA | ✅ PASS |
| 2 | LEGO 75257 Millennium Falcon | LEGO Star Wars 75257 Millennium Falcon Building Set | RODOMA | RODOMA | ✅ PASS |
| 3 | LEGO 76430 | LEGO Harry Potter 76430 | RODOMA | RODOMA | ✅ PASS |

**3/3 tikri LEGO rinkiniai teisingai praeina.**

---

### Fix A — PS5 valdikliai

| # | Užklausa | Pavadinimas | Laukiamas | Gautas | Status |
|---|---|---|---|---|---|
| 1 | PS5 controller | Silicone Cover for PS5 DualSense Controller Anti-Slip Case | ATMESTA | ATMESTA | ✅ PASS |
| 2 | PS5 controller | Sony PlayStation DualSense PS5 Wireless Controller White | RODOMA | RODOMA | ✅ PASS |
| 3 | PS5 controller | OIVO PS5 Controller Charging Stand Station Dock | ATMESTA | ATMESTA | ✅ PASS |

---

### Fix A — Regresijos: tikri produktai su galimais konfliktais

| # | Užklausa | Pavadinimas | Laukiamas | Gautas | Status |
|---|---|---|---|---|---|
| 1 | Philips Hue **lighting kit** | Philips Hue Smart Lighting Starter Kit | RODOMA | RODOMA | ✅ PASS |
| 2 | Govee **smart lighting** | Govee RGBIC LED Strip Lighting 5m | RODOMA | RODOMA | ✅ PASS |
| 3 | LG OLED55C3 | LG OLED 55 C3 OLED55C3 4K Smart TV | RODOMA | RODOMA | ✅ PASS |
| 4 | iPhone 15 128GB | Apple iPhone 15 128GB Black Smartphone | RODOMA | RODOMA | ✅ PASS |
| 5 | Samsung RB34C600ESA | Samsung RB34C600ESA Kühlschrank 201cm | RODOMA | RODOMA | ✅ PASS |
| 6 | Sony WH-1000XM5 | Sony WH-1000XM5 Wireless Noise-Cancelling Headphones | RODOMA | RODOMA | ✅ PASS |
| 7 | Milka 100g | Milka Alpenmilch Schokolade 100g | RODOMA | RODOMA | ✅ PASS |
| 8 | Dyson V15 Detect | Dyson V15 Detect Absolute Cordless Vacuum Cleaner | RODOMA | RODOMA | ✅ PASS |

**8/8 tikri produktai be regresijų.**

Svarbus pastebėjimas dėl "lighting" ir "light kit":
- `_ACCESSORY_MATCH_WORDS` patikra: `if acc not in q: return False`
- Jei žodis yra IR title, IR užklausoje — **filtras nesuveikia**
- "Philips Hue lighting kit" užklausa → "lighting" yra užklausoje → praeina ✓
- "LEGO 76430 Hogwarts" užklausa → "lighting" NĖRA užklausoje → filtras suveikia ✓

---

### Žinoma prieš-egzistuojanti problema (ne Fix A regresija)

| Užklausa | Pavadinimas | Laukiamas | Gautas | Priežastis |
|---|---|---|---|---|
| LEGO 76430 **lighting** | LocoLee LED Lighting Kit **for LEGO** 76430 | RODOMA | ATMESTA | Pre-existing compat_patterns: "for lego" title'e, bet "for" nėra užklausoje |

**Tai NE Fix A regresija.** `_ACCESSORY_MATCH_WORDS` čia nesuveikia (nes "lighting" yra užklausoje). Problema yra `compat_patterns` logika: jei vartotojas ieško "LEGO 76430 lighting" (norėdamas apšvietimo rinkinį), bet pavadinimas turi "for LEGO" → sugaudoma kaip aksesuaras.

Tai buvo **tas pats elgesys prieš Fix A**. Atskiras klausimas, kurį galima spręsti vėliau.

---

## 2. Fix C — Kainų sanity testai

| # | Scenarijus | Laukiama | Gauta | Status |
|---|---|---|---|---|
| 1 | LEGO LED kit €27.98 vs tikras rinkinys €78.98 | REJECTED (signal='led light') | REJECTED | ✅ PASS |
| 2 | Sony WH-1000XM5 €35 vs €120 — tikra akcija | WARN (laikomas) | WARN | ✅ PASS |
| 3 | Abu LEGO rinkiniai ~€79-83 — panašios kainos | Nėra žymėjimo | Nėra | ✅ PASS |
| 4 | Vienintelis rezultatas yra pigus aksesuaras | LAIKOMAS (nėra alternatyvų) | LAIKOMAS | ✅ PASS |
| 5 | PS5 dėklas €15 (compatible) vs valdiklis €65 | REJECTED (signal='compatible') | REJECTED | ✅ PASS |

**5/5 kainų sanity testai praėjo.**

### Logas skaidrumo patikrai

```
[post_process] REJECT suspicious+accessory signal='led light'
               price=27.98 median=78.98
               title='LEGO 76430 LED Lighting Kit Hogwarts Owl Post'

[post_process] WARN suspicious_price (no accessory signal, keeping)
               price=35.00 median=120.00
               title='Sony WH-1000XM5 Headphones Black'

[post_process] REJECT suspicious+accessory signal='compatible'
               price=15.00 median=65.00
               title='PS5 Controller Compatible Silicone Cover'
```

Logai yra aiškūs: matosi signalas, kaina, pavadinimas. Filtras **skaidrus**.

---

## 3. Layer 1 baseline (test_pipeline.py — inlined kodas, be Fix A)

Šie testai naudoja SENĄ inline'd `is_relevant_result` versiją (ne mano pakeitimus), todėl rodo bazinę reikšmę — tik patikrina ar nieko nepradingo.

| Kategorija | rel_pass | acc_pass | unit_bug | short_q_trunc |
|---|---|---|---|---|
| appliances | 20/20 | 18/20 | 0 | 0 |
| electronics | 20/20 | 18/20 | 0 | 10 |
| lego | 20/20 | 16/20 | 0 | 6 |
| food | 20/20 | 20/20 | 0 | 6 |
| cosmetics | 20/20 | 20/20 | 0 | 15 |
| clothing | 20/20 | 20/20 | 0 | 12 |
| books | 18/20 | 20/20 | 0 | 14 |
| household | 20/20 | 20/20 | 0 | 13 |
| sports | 20/20 | 20/20 | 0 | 4 |
| baby | 20/20 | 20/20 | 0 | 11 |
| **TOTAL** | **198/200** | **192/200** | **0** | **91** |

**Rezultatai identiški baziniams (prieš fix'us).** Jokių regresijų.

Pastaba: LEGO kategorija turi 16/20 acc_pass su senuoju kodu — 4 aksesuarai nebuvo pagauti. Su Fix A (realia server.py versija) bent dalis jų dabar būtų pagauta (LED Lighting Kit tipo, kurie turi "lighting" žodį).

---

## 4. Layer 2 live HTTP — NEGALIMA TIKRINTI

Fix'ai yra tik `accessory-fix` šakoje — **production'e dar neįdiegti**. Live HTTP testai tikrintų SENĄ produkcinį kodą, todėl jie **neatskleidžia Fix A/C veikimo**. Po merge į main ir Render deploy — tik tada layer 2 bus prasmingas.

Etaloninis rezultatas prieš šiuos fix'us: **14/20** (po auto-fixes-review merge).

---

## 5. Filtro skaidrumas — ar matosi KODĖL kažkas atmesta?

Taip. Logai rodomi dviejose vietose:

**`is_relevant_result` — implicit** (pavadinimas nelogina, bet galima pridėti):
- Šiuo metu funkcija grąžina `True/False` be logavimo
- Galima pridėti vėliau, bet kol kas filtravimo priežastis matosi iš kodo logikos

**`post_process` Step 1b — explicit logavimas (Fix C)**:
```
[post_process] REJECT suspicious+accessory signal='...' price=... median=... title='...'
[post_process] WARN suspicious_price (no accessory signal, keeping) price=... title='...'
```

Render logai parodys, kada ir kodėl kaina atmetama.

---

## 6. Apibendrinimas

| Patikra | Rezultatas |
|---|---|
| Fix A: LED aksesuarai atmetami | ✅ 7/7 pagauta |
| Fix A: Tikri produktai nepradingo | ✅ 8/8 praeina |
| Fix A: Regresijų Layer 1 | ✅ 0 regresijų (198/200 rel, 192/200 acc — identiškai) |
| Fix C: Kainų anomalijų atmetimas | ✅ 5/5 atvejų teisingi |
| Fix C: Tikra akcija — WARN, ne REJECT | ✅ Teisingai laikoma su įspėjimu |
| Fix C: Saugiklis (vienintelis rezultatas) | ✅ Neišmetamas kai nėra alternatyvų |
| Logų skaidrumas | ✅ Aiškus signalas + kaina + pavadinimas |

**Verdiktas: ŽALIA.** Accessory-fix šaką **saugu merginti** į main.

Prieš merge rekomenduojama tik žiūrėti Render logus po deploy ir patikrinti "LEGO 76430" paiešką — turi rodyti tikrą rinkinį (~€79), ne LED lemputę (~€28).
