# SECURITY_AUDIT.md
**Data:** 2026-06-19 (naktinis auditas)  
**Šaka:** night-hardening  
**Auditorius:** automatinis (server.py 7058 eilučių, git log 363 commit'ų)

---

## APIBENDRINIMAS

| Kategorija | Kritiškumas | Statusas |
|---|---|---|
| Hardcoded secrets | ✅ NĖRA | OK |
| SSRF rizika | ✅ ŽEMA | OK — tik whitelist URL |
| `/api/debug-html` auth bypass | ❌ AUKŠTAS | **PATAISYTA šioje šakoje** |
| Trūkstamas rate limit (2 endpoint) | ⚠️ VIDUTINIS | **PATAISYTA šioje šakoje** |
| CORS `"*"` numatytoji reikšmė | ⚠️ VIDUTINIS | Palieka peržiūrai |
| Dependency CVEs (15 pažeidžiamumų) | ⚠️ VIDUTINIS | Palieka peržiūrai |
| `.env` failas | ✅ OK | .gitignore'd, ne git istorijoje |
| Rate limiting bendroje logikoje | ✅ OK | 20 req/min + 200/day per IP |

---

## S1 — `/api/debug-html` visiškai atviras kai `DEBUG_API_KEY=""` ❌ AUKŠTAS

### Problema

```python
# PRIEŠ (pažeidžiamas):
if DEBUG_API_KEY and request.args.get("key") != DEBUG_API_KEY:
    return jsonify({"error": "unauthorized"}), 401
```

Kai `DEBUG_API_KEY = ""` (numatytoji reikšmė, env var neįrašytas):
- `bool("") = False` → `if False and ...: return 401` → sąlyga NIEKADA nevykdoma
- Endpoint prieinamas visiems be autentikacijos

**Pasekmės:** `/api/debug-html` atlieka realius scraping kvietimus per ScraperAPI (~5-25 kreditai/kvietimas). Piktybinis vartotojas gali išnaudoti visus ScraperAPI kreditus.

### Pataisymas (šioje šakoje)

```python
# PO (pataisyta):
if not DEBUG_API_KEY or request.args.get("key") != DEBUG_API_KEY:
    return jsonify({"error": "unauthorized"}), 401
```

Kai `DEBUG_API_KEY = ""` → `not "" = True` → visada grąžina 401. Endpoint veikia tik kai env var nustatytas.

**Poveikis:** Minimalus — debug endpoint negali būti naudojamas prod be rakto. Jei DEBUG_API_KEY niekad nebuvo naudojamas → nėra poveikio.

---

## S2 — Trūkstamas rate limit: `/api/price-history`, `/api/watchlist-check` ⚠️ VIDUTINIS

### Problema

Šie endpointai neturėjo `@rate_limit` dekoratoriaus:
- `/api/price-history` (GET) — klausia Supabase
- `/api/watchlist-check` (POST) — klausia Supabase iki 20 kartų per kvietimą

Kažkas galėjo spam'inti šiuos endpointus ir išeikvoti Supabase row reads / connection pool.

### Pataisymas (šioje šakoje)

Pridėtas `@rate_limit` prie abiejų endpointų — dabar naudoja tą patį 20 req/min + 200/day limitą.

---

## S3 — CORS `"*"` numatytoji reikšmė ⚠️ VIDUTINIS

### Problema

```python
_ALLOWED_ORIGINS = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "*").split(",") if o.strip()]
CORS(app, origins=_ALLOWED_ORIGINS if "*" not in _ALLOWED_ORIGINS else "*")
```

Jei `ALLOWED_ORIGINS` env var nenustatytas → CORS `origins="*"` → bet kuri svetainė gali siųsti cross-origin užklausas.

**Praktinis poveikis:** Kadangi nėra slapuko autentikacijos (tik rate limiting pagal IP), piktybinis saitas galėtų naudoti vartotojo naršyklę kaip tarpinę stotį scan-image kvietimams (išnaudoti jų rate limit).

**Realus pavojus:** ŽEMAS-VIDUTINIS — naudotojai naudoja pačios Goody vartotojo sąsajos, ne trečiųjų šalių saitus.

### Rekomenduojamas pataisymas (NEATLIKTAS — vidutinė rizika)

Render dashboard → Environment Variables → `ALLOWED_ORIGINS=https://goody-app.onrender.com` (arba faktinis frontend domenas).

**Pastaba:** CORS konfigūracijos keitimas gali sulaužyti frontend jei domenas neteisingai nurodytas. Todėl palikta peržiūrai.

---

## S4 — Dependency pažeidžiamumai (pip-audit) ⚠️ VIDUTINIS/AUKŠTAS

### Rasti CVEs

```
flask         3.0.3   CVE-2026-27205  Fix: 3.1.3
flask-cors    4.0.1   PYSEC-2024-71   Fix: 4.0.2
flask-cors    4.0.1   PYSEC-2024-260  Fix: 4.0.2
flask-cors    4.0.1   CVE-2024-6844   Fix: 6.0.0
flask-cors    4.0.1   CVE-2024-6866   Fix: 6.0.0
flask-cors    4.0.1   CVE-2024-6839   Fix: 6.0.0
python-dotenv 1.0.1   CVE-2026-28684  Fix: 1.2.2
gunicorn      21.2.0  CVE-2024-1135   Fix: 22.0.0
gunicorn      21.2.0  CVE-2024-6827   Fix: 22.0.0
requests      2.31.0  CVE-2024-35195  Fix: 2.32.0
requests      2.31.0  CVE-2024-47081  Fix: 2.32.4
requests      2.31.0  CVE-2026-25645  Fix: 2.33.0
lxml          5.1.0   PYSEC-2026-87   Fix: 6.1.0
```

**Iš viso: 13 CVE, 6 paketai.**

### Rizikos vertinimas

| Paketas | Dabartinis | Siūlomas | Pakeitimo rizika | Prioritetas |
|---|---|---|---|---|
| flask-cors | 4.0.1 | 6.0.0 | AUKŠTA (major bump, API gali skirtis) | VIDUTINIS — pataisyti atskiroje šakoje, testuoti |
| gunicorn | 21.2.0 | 22.0.0 | VIDUTINĖ (major bump) | AUKŠTAS — HTTP request smuggling CVE-2024-1135 |
| requests | 2.31.0 | 2.33.0 | ŽEMA (minor bumps, backward compatible) | AUKŠTAS — aktyvi naudojama biblioteka |
| flask | 3.0.3 | 3.1.3 | ŽEMA (minor bump) | VIDUTINIS |
| python-dotenv | 1.0.1 | 1.2.2 | ŽEMA | ŽEMAS |
| lxml | 5.1.0 | 6.1.0 | AUKŠTA (major bump) | VIDUTINIS |

### Rekomenduojamas veiksmas

Pataisyti requirements.txt atskiroje šakoje (ne night-hardening), testuoti prieš deployant:
1. `requests>=2.33.0` — backward compatible, didelė naudojama biblioteka
2. `gunicorn>=22.0.0` — HTTP smuggling fix
3. `flask>=3.1.3` — minor bump
4. `flask-cors>=6.0.0` — testuoti ar CORS veikia su nauju API
5. `lxml>=6.1.0` — testuoti BeautifulSoup parsavimą

---

## S5 — `.env` failas (TIRIAMA) ✅ OK

### Patikrinimas

```
git ls-files .env  → (tuščias — ne git istorijoje)
.gitignore         → .env ✓ (teisingai ignoruojamas)
git log --all -- .env → (jokie commit'ai)
```

**Rasta `.env` turinyje:**
```
SUPABASE_URL=https://irgmwoopbetvmpjthftp.supabase.co
SUPABASE_KEY=sb_publishable_aYQk4qMrl_eWoM9Oqt1JIQ_Tb22yKBz
```

**Vertinimas:** `sb_publishable_` prefiksas reiškia viešą raktas (analogiškas Supabase anon key). Nėra service_role rakto. Supabase URL yra projekto ID — jis žinomas, bet nėra paslaptis. **Rizika: ŽEMA.** Jokie realūs raktai (ANTHROPIC, OPENAI, SCRAPER_API, ZYTE) `.env` faile nėra.

---

## S6 — Hardcoded paslaptys kode ✅ NĖRA

```python
# Visos paslaptys per env variables:
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY    = os.getenv("OPENAI_API_KEY", "")
SCRAPER_API_KEY   = os.getenv("SCRAPER_API_KEY", "")
ZYTE_API_KEY      = os.getenv("ZYTE_API_KEY", "")
SUPABASE_URL      = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY      = os.getenv("SUPABASE_KEY", "")
```

**Vienintelė hardcoded reikšmė:** `AMAZON_AFFILIATE_TAG = os.getenv("AMAZON_AFFILIATE_TAG", "goody-21")`  
Tai nėra paslaptis — affiliate tag'ai yra viešai matomi URL parametrais.

---

## S7 — SSRF rizika ✅ ŽEMA

### Tikrinimas

`fetch_url(url, ...)` naudojamas tik su hardcoded shop URL:
```python
f"https://varle.lt/search/?q={requests.utils.quote(query)}"
f"https://pigu.lt/lt/search?searchPhrase={requests.utils.quote(query)}"
f"https://www.amazon.{domain}/s?k={requests.utils.quote(query)}"
# ... ir t.t.
```

`/api/debug-html` endpoint'as naudoja whitelist:
```python
urls = {
    "varle": f"https://varle.lt/search/?q=...",
    "pigu": f"https://pigu.lt/...",
    # ... tik žinomi shops
}
url = urls.get(shop, urls["varle"])  # default į varle.lt
```

**Vartotojas NEGALI nurodyti URL** — tik query string tekstą (normalus URL encode'inamas). **SSRF rizika: NĖRA.**

---

## Žemos rizikos pataisymų suvestinė (šioje šakoje)

| Fix | Rizika | Statusas |
|---|---|---|
| debug-html auth bypass → `if not DEBUG_API_KEY or ...` | ŽEMA | ✅ PATAISYTA |
| `@rate_limit` prie `/api/price-history` | ŽEMA | ✅ PATAISYTA |
| `@rate_limit` prie `/api/watchlist-check` | ŽEMA | ✅ PATAISYTA |
