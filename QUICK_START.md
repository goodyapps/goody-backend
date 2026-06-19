# QUICK_START.md
**Pirmos 30 minučių — žingsnis po žingsnio**  
**Tikslas:** Nuo "ką nors dariau per naktį" iki "žinau ką darysiu šiandien" per 30 min

---

## MINUTĖ 1-2: Vienas failo atidarymas

Atsidaryk šį failą:
```
C:\Users\giedrius.simonaviciu\projektai\goody-backend\ACTION_PLAN.md
```
Paskaityk tik sekciją "MERGE EILIŠKUMAS" apačioje. Tiek užtenka pradėti.

---

## MINUTĖ 3-5: Patikrink ar Elesen šiandien rodo klaidingą produktą

Šis testas parodo ar elesen-fix reikalingas:

```powershell
# PowerShell:
$body = '{"query": "LEGO 76430 Hogwarts", "language": "lt"}'
$r = Invoke-RestMethod -Uri "https://goody-app.onrender.com/api/search" `
     -Method POST -ContentType "application/json" -Body $body
$r.results | Select-Object shop, product_title, price | Format-Table
```

**Interpretacija:**
- Jei `product_title` turi "Nintendo Switch" arba "žaidimas" → **elesen-fix reikalingas** (ir/arba type-filter)
- Jei visi rezultatai yra LEGO rinkiniai → Elesen šiandien veikia teisingai
- Jei Elesen nerodomas (`shop` nėra "elesen") → ScraperAPI šiandien nesugebėjo Nosto AJAX pagauti

---

## MINUTĖ 6-12: Supabase RLS (be kodo)

**Render deploy NEPALEISTAS — tik Supabase dashboard.**

1. Eik į Supabase projektą → Table Editor
2. Lentelė `price_history` → RLS piktograma → Enable Row Level Security
3. Lentelė `searches` → tas pats
4. Politika: tik `service_role` gali rašyti (anoniminiai neturi prieigos)

Jei nežinai kaip: peržiūrėk PENTEST_AUDIT.md sekcija P2.

---

## MINUTĖ 13-18: Pirmas merge — security-night (žema rizika)

```powershell
cd C:\Users\giedrius.simonaviciu\projektai\goody-backend

# Patikrink testus
$env:PYTHONIOENCODING="utf-8"
python test_night_coverage.py

# Jei 70/70 PASS:
git checkout main
git merge security-night
git push origin main

# Stebėk Render deploy ~2 min
# Render logs: ar /api/track ir /api/popular-searches rodo rate_limit log'us
```

**Jei testai FAIL:** Nestumk. Peržiūrėk test_night_coverage.py — gali būti environment problema (SUPABASE_URL env var).

---

## MINUTĖ 19-25: Antras merge — night-tests (nulinė rizika)

```powershell
# Dar main šakoje:
git merge night-tests
git push origin main
# Jokio papildomo tikrinimo nereikia — tik testų failas
```

---

## MINUTĖ 26-30: Sprendimas dėl type-filter

```powershell
# Paleisk testus:
python test_type_filter.py
python test_pipeline.py
```

**Jei abu PASS:**
- Peržiūrėk BRANCHES_STATUS.md sekcija `type-filter` — ar esi pasiruošęs merginti?
- Merge = Render deploy = reali rizika. Jei nori palaukti rytojaus → tai yra geras sprendimas.
- Jei mergini dabar: `git merge type-filter; git push origin main` → stebėk 10 min

**Jei FAIL:** Nestumk. Peržiūrėk kokis testas fail'ina.

---

## PO 30 MIN: Atviri klausimai

Paskaityk ACTION_PLAN.md sekciją "KLAUSIMAI, KURIE REIKIA TAVĘS":
1. elesen-fix (S2): pirmiausia reikia tavo sprendimo
2. S5 (identify R1): ar norima šią savaitę?
3. Supabase RLS: ar padaryta?

---

## JEIGU KAS SULAUŽYTA PO MERGE

```powershell
# Greitai atšaukti paskutinį merge:
git checkout main
git revert -m 1 HEAD
git push origin main
# Render auto-deploy atstatymo versiją
```

---

## VISŲ NAKTIES DOKUMENTŲ SĄRAŠAS

| Dokumentas | Skaityti kada | Laikas |
|---|---|---|
| **QUICK_START.md** | Dabar (tu čia) | 5 min |
| **ACTION_PLAN.md** | Po šio | 10 min |
| **BRANCHES_STATUS.md** | Prieš kiekvieną merge | 3 min |
| MORNING_BRIEF.md | Pilka nakties santrauka | 10 min |
| PENTEST_AUDIT.md | Kai sprendžia K1, K2 | 5 min |
| P1_DIVERGENCE.md | Kai darys S5 (identify R1) | 15 min |
| ELESEN_ROOT_CAUSE.md | Kai sprendžia S2 (elesen-fix) | 10 min |
| CODE_HEALTH.md | Kai eis prie V3 (thread fix) | 5 min |
| EXPLORATION_BRIEF.md | Produkto planavimui | 5 min |
| FEATURE_IDEAS.md | Funkcijų prioritetams | 10 min |
| PRODUCT_GAPS.md | Prieš bet kokią naują funkciją | 10 min |

---

## ŠAKOS IŠ ŽVILGSNIO

```
✅ MERGED (ignoruoti):  night-hardening, accessory-fix, buylink-fix, auto-fixes-review
⏳ LAUKIA (tavo rankose):
   security-night  → ŽEMA RIZIKA  → merge pirmą
   night-tests     → NULĖ RIZIKA  → merge antrą
   type-filter     → VIDUT. RIZIKA → merge trečią (po testų)
   elesen-fix      → SPRENDIMAS   → tavo pasirinkimas
```
