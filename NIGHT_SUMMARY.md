# NIGHT_SUMMARY.md
**Data:** 2026-06-19 (naktinis auditas)  
**Šaka:** night-hardening  
**Dirbta:** SECURITY_AUDIT + STABILITY_AUDIT + TEST_COVERAGE + žemos rizikos fix'ai

---

## TOP 5 SAUGUMO RADINIAI

| # | Radinys | Kritiškumas | Statusas |
|---|---|---|---|
| 1 | **`/api/debug-html` visiškai atviras kai DEBUG_API_KEY=""** — bet kas galėjo naudoti ScraperAPI kreditus | 🔴 AUKŠTAS | ✅ PATAISYTA |
| 2 | **15 dependency CVE (6 paketai)** — gunicorn HTTP smuggling, flask/requests/lxml/flask-cors pažeidžiamumai | 🟡 VIDUTINIS | ⏳ Peržiūrai |
| 3 | **Trūkstamas rate limit** prie `/api/price-history` ir `/api/watchlist-check` — galima Supabase DoS | 🟡 VIDUTINIS | ✅ PATAISYTA |
| 4 | **CORS `"*"` numatytoji reikšmė** — bet kuri svetainė gali siųsti cross-origin užklausas | 🟡 VIDUTINIS | ⏳ Peržiūrai |
| 5 | **SSRF: NĖRA** — fetch_url naudojamas tik su hardcoded shop URL, ne su vartotojo įvestimi | ✅ OK | — |

---

## TOP 5 STABILUMO RADINIAI

| # | Radinys | Kritiškumas | Statusas |
|---|---|---|---|
| 1 | **`global _amz_blocked_until` Python 3.12 SyntaxError** — neleidžia importuoti server.py lokaliame Python 3.12, blokuoja testus | 🔴 KRITINIS | ✅ PATAISYTA |
| 2 | **Supabase kvietimai be timeout** — `sb.table(...).execute()` gali pakibti neribotai | 🟡 VIDUTINIS | ⏳ Peržiūrai |
| 3 | **`_ph_exec` nebuvo `finally` bloke** — executor galėjo tekėti jei exception retry cascade metu | 🟡 VIDUTINIS | ✅ PATAISYTA |
| 4 | **Graceful degradation: GERAI** — visi ScraperAPI/Zyte/AI/Supabase fail'ai gaudomi, app tęsia veikimą | ✅ OK | — |
| 5 | **Self-ping keepalive: VEIKIA** — 13 min intervalu, 3 retry, daemon thread | ✅ OK | — |

---

## KĄ PATAISIAU ŠAKOJE (žema rizika, automatiškai)

### 1. `/api/debug-html` auth bypass [server.py]
```python
# PRIEŠ: jei DEBUG_API_KEY="" → endpoint atviras visiems
if DEBUG_API_KEY and request.args.get("key") != DEBUG_API_KEY:
    return 401

# PO: jei DEBUG_API_KEY="" → endpoint visada uždarytas
if not DEBUG_API_KEY or request.args.get("key") != DEBUG_API_KEY:
    return 401
```

### 2. Rate limiting pridėtas 2 endpointams [server.py]
```python
@app.route("/api/price-history", methods=["GET"])
@rate_limit  # ← pridėta
def price_history_endpoint():

@app.route("/api/watchlist-check", methods=["POST"])
@rate_limit  # ← pridėta
def watchlist_check():
```

### 3. `_ph_exec` executor finalizer [server.py]
```python
try:
    price_history = ph_fut.result(timeout=1)
except Exception:
    pass
finally:
    _ph_exec.shutdown(wait=False)  # ← perkeltas į finally
```

### 4. `global _amz_blocked_until` Python 3.12 fix [server.py]
```python
def scrape_amazon(...):
    global _amz_blocked_until  # ← perkeltas į funkcijos pradžią
    results = []
    if time.time() < _amz_blocked_until:
```

### 5. Naujas testų failas: `test_core_functions.py`
- 20 testų: `normalize_query` (8), `deduplicate_by_shop` (5), `_short_amazon_query` (7)
- **20/20 PASS**

### 6. Audito dokumentai
- `SECURITY_AUDIT.md` — pilnas saugumo auditas
- `STABILITY_AUDIT.md` — stabilumo auditas
- `TEST_COVERAGE.md` — testų dangos analizė
- `FIXES_PROPOSED_NIGHT.md` — vidutinės/aukštos rizikos siūlymai
- `NIGHT_SUMMARY.md` — šis dokumentas

---

## KĄ PALIKAU PERŽIŪRAI (vidutinė/aukšta rizika)

| Fix | Kodėl nedaryta | Prioritetas |
|---|---|---|
| gunicorn 21→22 (CVE-2024-1135 HTTP smuggling) | Major bump — gali keisti worker konfigūraciją | 🔴 AUKŠTAS |
| requests 2.31→2.33 (CVE) | Naudojamas visur — reikia smoke testų po upgrade | 🔴 AUKŠTAS |
| flask-cors 4→6 (CVE) | Major bump — CORS API galėjo pasikeisti | 🟡 VIDUTINIS |
| flask 3.0→3.1 (CVE) | Minor bump, bet reikia testuoti | 🟡 VIDUTINIS |
| CORS `"*"` → faktinis domenas | Nežinomas frontend domenas — sulaužytų app | 🟡 VIDUTINIS |
| Supabase timeout | Reikia SDK dokumentacijos patikrinimo | 🟡 VIDUTINIS |
| `post_process` unit testai | 2-3 val. darbas | 🟡 VIDUTINIS |

---

## REKOMENDUOJAMA RYTINĖ TVARKA

**Peržiūrėk šiandien (greitai):**

1. `git checkout night-hardening` → peržiūrėk diff
2. Jei žalia → `git merge night-hardening` → Render auto-deploy
3. Patikrink Render logus po deploy — ar matosi jokie `401 Unauthorized` (debug-html) iš legitimate naudotojų?

**Atskiroje šakoje (`deps-update`) — šiandien:**

4. `requests==2.31.0` → `requests>=2.33.0` — minimal CVE fix, safe
5. `gunicorn==21.2.0` → `gunicorn>=22.0.0` — HTTP smuggling fix
6. Paleisk `python test_pipeline.py` po upgrade

**Kitos dienos darbai:**

7. CORS tightening — sužinok frontend domeną, nustatyk `ALLOWED_ORIGINS`
8. `flask-cors 4→6` — testuoti atskiroje šakoje
9. `post_process` unit testai

---

## TESTŲ REZULTATAI (night-hardening šakoje)

```
test_buylink_fix.py    : 33/33 PASS
test_core_functions.py : 20/20 PASS (nauja)
test_accessory_fix.py  : 28/29 PASS (1 pre-existing)
test_pipeline.py Layer1: 198/200 (2 pre-existing)
```

Visos žemos rizikos kodo modifikacijos nepaveikė esamų testų.
