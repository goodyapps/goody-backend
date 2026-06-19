# BRANCHES_STATUS.md
**Sukurta:** 2026-06-20 | **Dabartinė šaka:** security-night  
**main HEAD:** `54415ae` (Live Elesen diagnostic)

---

## ŠAKŲ ŽEMĖLAPIS

```
main (54415ae)
├── security-night  [+5 commits] ← LAUKIA MERGE
│   ├── PENTEST_AUDIT.md + @rate_limit ant /api/track, /api/popular-searches
│   ├── P1_DIVERGENCE.md, CODE_HEALTH.md, MORNING_BRIEF.md (dokumentai)
│   └── UX/Market/Feature/Product dokumentai (šios nakties)
│
├── type-filter     [+2 commits] ← LAUKIA MERGE
│   ├── _PRODUCT_TYPE_SIGNALS (gaming platform + LT/PL knygų signalas)
│   ├── is_relevant_result() pataisymas (+6 eilutės)
│   ├── ELESEN_ROOT_CAUSE.md
│   └── test_type_filter.py (30 testų)
│
├── night-tests     [+1 commit] ← LAUKIA MERGE
│   └── test_night_coverage.py (70 testų)
│
├── elesen-fix      [+1 commit] ← NAUJA (šios nakties), LAUKIA SPRENDIMO
│   └── or all_results → or [] (2 eilutės: search + search_stream)
│
├── night-hardening [0 naujų] ← MERGED INTO main (c92cb4f)
├── accessory-fix   [0 naujų] ← MERGED INTO main (e0f5ae5)
├── buylink-fix     [0 naujų] ← MERGED INTO main (8bd06fc)
└── auto-fixes-review [0 naujų] ← MERGED INTO main
```

---

## DETALUS ŠAKŲ STATUSAS

### `security-night` — SAUGU MERGINTI

| Aspektas | Statusas |
|---|---|
| Server.py pakeitimai | +2 eilutės (@rate_limit ant 2 endpoint'ų) |
| Testai | `python test_night_coverage.py` — 70/70 PASS (patvirtinta) |
| Konfliktai su main | Nėra — pakeitimai lines 7300 ir 7312 (endpoint dekoratoriai) |
| Konfliktai su type-filter | Nėra — type-filter keičia lines 581-651 (is_relevant_result) |
| .md failai | +9 naujų dokumentų (nefunkciniai) |
| **Verdiktas** | 🟢 **ŽEMA RIZIKA — SAUGU** |

**Merge komandos:**
```bash
python test_night_coverage.py  # turi būti 70/70
git checkout main
git merge security-night
git push origin main
```

---

### `type-filter` — SAUGU (su testu)

| Aspektas | Statusas |
|---|---|
| Server.py pakeitimai | +25 eilutės (_PRODUCT_TYPE_SIGNALS + is_relevant_result papildymas) |
| Testai | `python test_type_filter.py` — 30/30 PASS (patvirtinta) |
| Konfliktai su main | Nėra — pakeitimai lines 581-651 |
| Konfliktai su security-night | Nėra — skirtingos kodo dalys |
| Known risk | MacBook/Notebook false positives jau patikrinti — nepaveikia |
| **Verdiktas** | 🟡 **ŽEMA-VIDUTINĖ RIZIKA — SAUGU po testo** |

**Merge komandos:**
```bash
python test_type_filter.py     # turi būti 30/30
python test_pipeline.py        # turi būti ≥490/500
git checkout main
git merge type-filter
git push origin main
```

**Po deploy stebėk:**
- Render logs: ar matosi `[is_relevant_result]` su type-filter reject
- Rankinis testas: "LEGO 76430 Hogwarts" → ar rodo LEGO rinkinį (ne Switch žaidimą)?

---

### `night-tests` — NULINĖ RIZIKA

| Aspektas | Statusas |
|---|---|
| Server.py pakeitimai | Nėra |
| Turinys | Tik `test_night_coverage.py` (naujas failas) |
| Konfliktai | Nėra su niekuo |
| **Verdiktas** | 🟢 **NULINĖ RIZIKA — SAUGU BET KADA** |

```bash
git checkout main
git merge night-tests
git push origin main
```

---

### `elesen-fix` — LAUKIA PRODUKTO SPRENDIMO

| Aspektas | Statusas |
|---|---|
| Server.py pakeitimai | 2 eilutės: `or all_results` → pašalinta (search + search_stream) |
| Testai | Neparašyta specialaus testo (reikia live testo) |
| Konfliktai su main | Nėra |
| Konfliktai su type-filter | Nėra |
| Konfliktai su security-night | Nėra |
| **Verdiktas** | 🔴 **REIKIA SPRENDIMO prieš merge** |

**Sprendimas:** Ar geriau rodyti 0 rezultatų (tiksliai) ar klaidingą produktą (kažkas nors)?
- **Jei "0 geriau"** → merge po type-filter
- **Jei "kažkas geriau"** → palik šakoje, naudoti tik type-filter

**Patikrinimas prieš merge:**
```bash
# Live testas ryte:
# 1. Rasti LEGO 76430 Hogwarts Render logus — ar Elesen grąžina rezultatus?
# 2. Jei TAIP ir rodo žaidimą → elesen-fix reikalingas
# 3. Jei TAIP ir rodo rinkinį → type-filter pakankamas

# Arba greitas API testas:
curl -X POST https://goody-app.onrender.com/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "LEGO 76430 Hogwarts", "language": "lt"}'
# Tikrink ar Elesen rezultatuose yra Nintendo Switch žaidimas
```

---

### SENOS ŠAKOS — galima ignoruoti / ištrinti

| Šaka | Statusas | Saugu trinti? |
|---|---|---|
| `night-hardening` | Merged į main (c92cb4f) | ✅ Taip |
| `accessory-fix` | Merged į main (e0f5ae5) | ✅ Taip |
| `buylink-fix` | Merged į main (8bd06fc) | ✅ Taip |
| `auto-fixes-review` | Merged į main | ✅ Taip |
| `feat/cache-stats-v521` | Nėra naujų commits vs main | Patikrink pirma |
| `feat/cost-opt-v518` | Nėra naujų commits vs main | Patikrink pirma |
| `feat/price-validation-v520` | Nėra naujų commits vs main | Patikrink pirma |
| `feat/progressive-stream-v519` | Nėra naujų commits vs main | Patikrink pirma |
| `feat/speed-v517` | Nėra naujų commits vs main | Patikrink pirma |

---

## KONFLIKTŲ ANALIZĖ

### type-filter + security-night (jei merginami abu)

| Failas | type-filter eilutės | security-night eilutės | Konfliktas? |
|---|---|---|---|
| server.py | 581-651 | 7300, 7312 | ❌ NĖRA |
| ELESEN_ROOT_CAUSE.md | Egzistuoja šakoje | Nėra šakoje | ❌ NĖRA |

**Saugu abu merginti paeiliui — jokių konfliktų.**

### elesen-fix + type-filter

| Failas | elesen-fix eilutės | type-filter eilutės | Konfliktas? |
|---|---|---|---|
| server.py | 6268, 6513 | 581-651 | ❌ NĖRA |

**Saugu merginti paeiliui.**

---

## REKOMENDUOJAMA MERGE TVARKA

```
1. security-night  (žema rizika, @rate_limit dokumentai)
2. night-tests     (nulinė rizika, tik testai)  
3. type-filter     (žema-vidutinė, po testų)
4. elesen-fix      (tik po sprendimo + type-filter)
```

Kiekvienas merge = Render auto-deploy = ~2 min deployment laikas. Tarp kiekvieno merge palaikyk ~5 min stebėjimui.
