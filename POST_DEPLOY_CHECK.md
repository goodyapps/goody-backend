# POST_DEPLOY_CHECK.md
**Deploy data:** 2026-06-19  
**Render deploy:** auto-deploy iš main push (palaukti ~2-3 min)  
**Tikrinamas commit:** 9e0ea97 (merge auto-fixes-review → main)

---

## Kaip žinoti, kad Render baigė deploy?

Atidaryti app'ą — jei veikia, deploy baigtas. Arba patikrinti Render dashboard.

---

## PRIVALOMI patikrinimai po deploy

### 1. Fix 2 — LEGO set numeriai (buvo 0, turi rasti)

**Query:** `LEGO Harry Potter 76430 Hogwarts`

- Atidaryti app'ą → įvesti paiešką
- **Tikėtinas rezultatas:** ≥1 rezultatas (Amazon randa set'ą pagal 76430)
- **Prieš fix:** `_short_amazon_query` generuodavo "LEGO Harry Potter" (be set numerio) → 0
- **Po fix:** generuoja "LEGO Harry 76430" → turi rasti specifinį set'ą
- ✅ OK jei: randa ≥1 rezultatą
- ❌ FAIL jei: vis dar 0 rezultatų

---

### 2. Fix 1 — Maistas su svoriu (buvo 0, turi rasti)

**Query:** `Milka šokoladas 100g`

- **Tikėtinas rezultatas:** ≥1 rezultatas
- **Prieš fix:** "100g" traktuotas kaip modelio kodas → reikalauta "100g" pavadinime → 0
- **Po fix:** "100g" filtruojamas → ieškoma tik pagal "Milka šokoladas" → randa
- ✅ OK jei: randa ≥1 rezultatą
- ❌ FAIL jei: vis dar 0

Taip pat patikrinti: `Nutella 400g` — turi ir toliau rasti (buvo OK prieš, turi likti OK).

---

### 3. Fix 1 regresijos patikra — 128GB NETURI dingti

**Query:** `iPhone 15 128GB`

- **Tikėtinas rezultatas:** randa iPhone 15 rezultatus
- **Svarbu:** patikrinti, kad "128GB" NEBUVO išmestas kaip "vienetas"
  - `_norm_units` konvertuoja "128 GB" → "128gb"
  - "128gb" neatitinka `^\d+g$` (yra "gb", ne "g") → **IŠSAUGOMAS** kaip modelio tokenas
  - Rezultatuose turi rodyti iPhone 15 128GB (ne kitų talpos variantus)
- ✅ OK jei: randa iPhone 15 su 128GB variantu
- ❌ FAIL jei: 0 rezultatų (128GB išmestas ir nieko nerasta)
- ⚠️ DĖMESIO jei: randa iPhone 15, bet rodo 256GB/512GB variantus be 128GB

---

### 4. Anksčiau šiandien įdiegti fix'ai — atpažinimas su key_specs

**Veiksmas:** Fotografuoti bet kurią elektros prekę naudojant "Price photo" mygtuką

- **Tikėtinas rezultatas:** 
  - Atpažinimo ekranas rodo produkto pavadinimą
  - Rezultatų ekrane matomas `key_specs` eilutė (pvz. "📋 256GB, 8GB RAM")
  - Verdict/Price blokų tvarka: kaina → verdiktas → key specs → parduotuvės
- Jei ekranas fotografuojamas iš tolo — tikriname ar neatpažinimo atvejui rodomas tekstas įvedimo laukelis (ne tik "fotografuok iš arčiau")

---

### 5. Regresijos patikra — elektronika turi veikti kaip prieš

**Query:** `Sony WH-1000XM5`  
**Query:** `Samsung Galaxy S24 Ultra`  
**Query:** `Dyson V15 Detect`

- Visi turi grąžinti ≥1 rezultatą
- ✅ OK jei: randa kainas iš Amazon ar Elesen
- ❌ FAIL jei: 0 rezultatų kuriame nors iš šių

---

## Greitoji patikros forma

| Nr | Query | Tikėtinas | Realus | Status |
|---|---|---|---|---|
| 1 | LEGO Harry Potter 76430 Hogwarts | ≥1 | | |
| 2 | Milka šokoladas 100g | ≥1 | | | 
| 3 | Nutella 400g | ≥1 | | |
| 4 | iPhone 15 128GB | ≥1 (su 128GB) | | |
| 5 | Sony WH-1000XM5 | ≥1 | | |
| 6 | Samsung Galaxy S24 Ultra | ≥1 | | |
| 7 | Dyson V15 Detect | ≥1 | | |
| 8 | Foto iš ekrano → key_specs rodomas | ✓ | | |

---

## Jei FAIL — ką daryti

**Fix 1 regression (128GB dingo):**
```bash
git revert HEAD  # arba
git checkout 8fc19a3 -- server.py
git commit -m "revert: unit token fix caused 128GB regression"
git push origin main
```

**Fix 2 regression (LEGO vis dar 0 po deploy):**
- Patikrinti Render logs ar deploy tikrai baigtas
- Patikrinti `/api/cache-stats` ar cached versija negrąžina seno rezultato
- Jei vis dar 0 po 5 min — patikrinti `_short_amazon_query` loguose
