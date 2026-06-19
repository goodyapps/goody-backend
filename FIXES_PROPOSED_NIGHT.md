# FIXES_PROPOSED_NIGHT.md
**Data:** 2026-06-19 (naktinis auditas)  
**Statusas:** Palieka rytinei peržiūrai — NEATLIKTA šioje šakoje  
**Vertinimas:** Kiekvienas fix'as su rizikos lygiu ir siūlomu veiksmų planu

---

## VIDUTINĖ RIZIKA — REKOMENDUOJAMA ATLIKTI

### M1 — Dependency upgrades (pip-audit 13 CVE)

**Problema:** 6 paketai su žinomais CVE.  
**Rizika atnaujinimo:** flask-cors 4→6 ir lxml 5→6 yra major bumps.

**Siūlomas planas:**
1. Sukurk šaką `deps-update`
2. Atnaujink `requirements.txt`:
   ```
   flask>=3.1.3          # minor bump, backward compatible
   flask-cors>=6.0.0     # TESTUOTI — major API changes
   gunicorn>=22.0.0      # HTTP smuggling fix, minor API changes
   requests>=2.33.0      # backward compatible
   python-dotenv>=1.2.2  # backward compatible
   lxml>=6.1.0           # TESTUOTI — major bump
   ```
3. Paleisk `python -m pip install -r requirements.txt` lokaliame venv
4. Paleisk visus testus (test_pipeline.py, test_buylink_fix.py, test_accessory_fix.py)
5. Jei testai žali → merge

**Kritinis patikrinimas po flask-cors 6.0.0:**
- CORS `origins="*"` sintaksė galėjo pasikeisti
- Patikrinti ar frontend gali siųsti POST į `/api/search`

**Estim. laikas:** 30-60 min  
**Rekomenduojama:** Taip — CVE-2024-1135 gunicorn HTTP smuggling yra realus pavojus

---

### M2 — CORS tightening (`ALLOWED_ORIGINS` → faktinis domenas)

**Problema:** CORS `"*"` numatytoji reikšmė leidžia bet kuriam saituui siųsti cross-origin užklausas.  
**Rizika:** Minimalus — nėra slapuko autentikacijos, bet galima piktnaudžiauti rate limit vartotojų naršyklėje.

**Veiksmas:**
1. Nustatyti Render env var: `ALLOWED_ORIGINS=https://goody-app.onrender.com` (arba faktinį frontend domeną)
2. Patikrinti ar frontend kvietimai veikia

**Estim. laikas:** 5 min  
**Rizika:** ŽEMA jei domenas žinomas. Jei nežinomas → frontend sulaužytas.

---

### M3 — Supabase kvietime timeout

**Problema:** `sb.table(...).execute()` neturi explicit timeout — gali pakibti neribotai jei Supabase serveris lėtas.

**Siūlomas pataisymas:**

```python
# Vietoj:
sb.table("price_history").insert(rows).execute()

# Naudoti su timeout (jei Supabase client palaiko):
import httpx
sb_with_timeout = _sb_create(SUPABASE_URL, SUPABASE_KEY, options={"timeout": 5})
```

Arba aprėpti su `concurrent.futures.wait(timeout=5)`:
```python
with ThreadPoolExecutor(max_workers=1) as ex:
    fut = ex.submit(lambda: sb.table(...).execute())
    try:
        fut.result(timeout=5)
    except Exception:
        pass
```

**Estim. laikas:** 30 min (reikia patikrinti Supabase Python SDK dokumentaciją)  
**Rekomenduojama:** Vidutinis prioritetas — Supabase yra stabili paslauga, bet timeout prideda saugiklį

---

### M4 — `post_process` unit testai

**Problema:** `post_process` yra kritinė funkcija (verdiktas, sutaupymas, is_cheapest) be testų.  
**Rizika:** Nepadengta — bug'ai gali praslysti į produkciją.

**Siūlomas veiksmas:** Parašyti `test_post_process.py` su 15-20 unit testais:
- Pigiausias rezultatas → is_cheapest=True
- Verdikto apskaičiavimas su keliais rezultatais
- Suspicious price → is_suspicious žymėjimas
- Fix C (accessory reject) vis dar veikia su realiu post_process (ne inlined versija)

**Estim. laikas:** 2-3 val.

---

## AUKŠTA RIZIKA — ATIDŽIAI PERŽIŪRĖTI

### H1 — `requests==2.31.0` → `requests>=2.33.0`

Techniškai backward compatible, bet requests naudojamas visur. Jei kažkas pasikeitė HTTP sesijos elgesyje, gali sulaužyti scraping.

**Rekomenduojama:** Testuoti lokaliame venv prieš deploy.

---

### H2 — `gunicorn==21.2.0` → `gunicorn>=22.0.0`

CVE-2024-1135 — HTTP request smuggling. Gunicorn 22 pataisė šią problemą.

**Rizika:** gunicorn 22 gali turėti skirtingą worker konfigūraciją. Render naudoja gunicorn nuo `Procfile` arba `gunicorn server:app` komandos — patikrinti ar `--workers 1 --threads 2` vis dar veikia.

**Rekomenduojama:** Atnaujinti — HTTP smuggling yra rimtas saugumo pavojus.

---

### H3 — `lxml==5.1.0` → `lxml>=6.1.0`

lxml naudojamas kaip BeautifulSoup parser'is:
```python
soup = BeautifulSoup(resp.text, "html.parser")  # naudoja html.parser, ne lxml
```

Patikrinti: ar kažkur naudojamas `"lxml"` parser argumentas — jei taip, lxml 6.x gali turėti skirtingą elgesį.

```bash
grep -n '"lxml"' server.py
```

Jei naudojamas tik `html.parser` → lxml upgrade yra saugus (lxml naudojamas tik kaip fallback).

---

## ŽEMOS RIZIKOS — REKOMENDUOJAMA PADARYTI

### L1 — `ALLOWED_ORIGINS` env var dokumentavimas

Pridėti į Render environment variables dokumentaciją (arba CLAUDE.md):
```
ALLOWED_ORIGINS=https://jūsų-frontend.onrender.com
RENDER_EXTERNAL_URL=https://goody-backend.onrender.com
DEBUG_API_KEY=<strong-random-key>
MINUTE_LIMIT=20
```

---

### L2 — `_model_code_variants` testai

Parašyti 10 unit testų modelio kodo variantų generatoriui:
- `"Samsung RB34C600ESA"` → `["Samsung RB34C600ESA", "Samsung RB34C600", "Samsung RB346"]`
- `"LEGO 76430"` → modelio kodas nekeičiamas

---

### L3 — Health endpoint versija

```python
return jsonify({
    "status": "ok",
    "version": "7.55",  # ← pasenusi versija, reikia atnaujinti
    ...
})
```

Versija turėtų atspindėti realią server.py versiją (dokstringe matosi `v7.56`).

---

## PRIORITETŲ SUVESTINĖ

| Fix | Prioritetas | Estim. laikas | Rizika |
|---|---|---|---|
| gunicorn upgrade (CVE-2024-1135) | 🔴 AUKŠTAS | 15 min | Vidutinė |
| requests upgrade (CVE) | 🔴 AUKŠTAS | 15 min | Žema |
| flask/dotenv/lxml upgrade | 🟡 VIDUTINIS | 30 min | Žema-Vidutinė |
| flask-cors upgrade 4→6 | 🟡 VIDUTINIS | 30 min | Vidutinė |
| CORS tightening | 🟡 VIDUTINIS | 5 min | Žema |
| Supabase timeout | 🟡 VIDUTINIS | 30 min | Žema |
| post_process testai | 🟡 VIDUTINIS | 2-3 val | — |
| _model_code_variants testai | 🟢 ŽEMAS | 30 min | — |
| Health version update | 🟢 ŽEMAS | 5 min | — |
