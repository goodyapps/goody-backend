# STABILITY_AUDIT.md
**Data:** 2026-06-19 (naktinis auditas)  
**Šaka:** night-hardening  
**Aplinka:** Render free tier, 512MB RAM

---

## APIBENDRINIMAS

| Kategorija | Statusas |
|---|---|
| Graceful degradation (ScraperAPI / Zyte / Gemini / Supabase) | ✅ GERAI |
| Timeout'ai visuose HTTP kvietime | ✅ GERAI (su viena išlyga) |
| Self-ping keepalive | ✅ VEIKIA |
| ThreadPoolExecutor valdymas | ✅ GERAI (su vienu pataisytu bug'u) |
| In-memory cache valdymas | ✅ GERAI (500 entry cap) |
| Supabase klientas be timeout | ⚠️ VIDUTINIS |
| Parallel retry cascade memory | ⚠️ STEBĖTI |
| `_amz_blocked_until` global bug (Python 3.12) | ❌ KRITINIS | **PATAISYTA** |

---

## ST1 — Graceful Degradation ✅ GERAI

### ScraperAPI nukrenta

```python
try:
    resp = _http.get(scraper_url, timeout=scraper_timeout)
    if resp.status_code == 200:
        return resp
    print(f"[ScraperAPI {resp.status_code}] -> Zyte fallback")
except Exception as e:
    print(f"[ScraperAPI err] {e} -> Zyte fallback")
```

→ Automatiškai krenta į Zyte fallback, tada į direct. **Nėra crash.**

### Zyte nukrenta

```python
try:
    resp = _http.post("https://api.zyte.com/v1/extract", ...)
    ...
except Exception as e:
    print(f"[Zyte err] {e} -> direct")
```

→ Krenta į direct HTTP. **Nėra crash.**

### Gemini / Claude / OpenAI nukrenta

AI funkcijos (`analyze_deal_with_ai`, `validate_results_with_ai`, `claude_translate`) — visos turi try/except ir grąžina tuščias reikšmes:

```python
except Exception as e:
    print(f"[AI analyze] {e}")
    return {"verdict": "", ...}
```

→ App rodo rezultatus BEZ AI komentaro. **Nėra crash, vartotojas gauna kainas.**

### Supabase nukrenta

```python
def save_prices_to_supabase(product_name, results):
    sb = get_supabase()
    if not sb:
        return
    try:
        sb.table("price_history").insert(rows).execute()
    except Exception as e:
        print(f"[Supabase save] {e}")
```

→ Kaina neišsaugoma, bet paieška veikia. **Nėra crash.**

---

## ST2 — Timeout'ai ✅ GERAI (su viena išlyga)

### Padengti timeout'ai

| Kvietimas | Timeout | Vertinimas |
|---|---|---|
| ScraperAPI | `scraper_timeout` param (5-35s) | ✅ |
| Zyte | `timeout=6` | ✅ |
| Direct HTTP | `timeout=SHOP_TIMEOUT` (default 5s) | ✅ |
| FX rates | `timeout=5` | ✅ |
| Barcode (UPCItemDB / OpenFoodFacts) | `timeout=5` | ✅ |
| ThreadPoolExecutor as_completed | `timeout=11-22s` | ✅ |
| Translation | `timeout=4` | ✅ |
| Price history future | `timeout=1` | ✅ |

### Supabase — BEZ explicit timeout ⚠️

```python
sb.table("price_history").insert(rows).execute()
sb.table("searches").select(...).execute()
```

Supabase Python client nenaudoja explicit timeout — jei Supabase serveris pakymba, kvietimas gali pakibti neribotai.

**Rizika:** VIDUTINĖ — jei Supabase pakymba, `save_prices_to_supabase` ir `fetch_price_history_from_supabase` gali pakibti. `save_prices` yra fire-and-forget, bet `fetch_price_history` blokuoja price_history thread.

**Pataisymas (neatliktas — reikia Supabase client dokumentacijos):** Naudoti `postgrest_client.timeout` arba išoriniuose kvietime aprėpti `concurrent.futures.wait(timeout=...)`.

---

## ST3 — `_amz_blocked_until` Python 3.12 SyntaxError ❌ KRITINIS — **PATAISYTA**

### Problema

```python
# PRIEŠ (klaidingas):
def scrape_amazon(...):
    results = []
    if time.time() < _amz_blocked_until:  # ← naudoja prieš global deklaraciją
        ...
    if _bot_blocked:
        global _amz_blocked_until         # ← Python 3.12: SyntaxError čia
        _amz_blocked_until = ...
```

Python 3.12 griežtina `global` deklaracijas — jei kintamasis naudojamas funkcijoje prieš `global` deklaraciją, tai `SyntaxError`. Senesnėse versijose (3.10, 3.11) tai veikia su įspėjimu.

**Pasekmė:** Render naudoja Python 3.11 (todėl veikia), bet lokaliame Python 3.12 import'as krenta — neleidžia paleisti testų.

### Pataisymas (šioje šakoje)

```python
# PO (pataisyta):
def scrape_amazon(...):
    global _amz_blocked_until  # ← perkelta į funkcijos pradžią
    results = []
    if time.time() < _amz_blocked_until:
        ...
    if _bot_blocked:
        _amz_blocked_until = ...  # ← dublikatas pašalintas
```

---

## ST4 — ThreadPoolExecutor valdymas ✅ GERAI

### Pagrindinis executor

```python
executor = ThreadPoolExecutor(max_workers=10)
try:
    ...
finally:
    executor.shutdown(wait=False)
```

✅ `finally` bloke — shutdown vyksta net jei exception.

### Price history executor (`_ph_exec`) — **PATAISYTA**

```python
# PRIEŠ:
_ph_exec = ThreadPoolExecutor(max_workers=1)
ph_fut = _ph_exec.submit(get_price_history, query)
# ... ~100 eilučių kodo ...
try:
    price_history = ph_fut.result(timeout=1)
except Exception:
    pass
_ph_exec.shutdown(wait=False)  # ← galėjo neįvykti jei exception
```

Jei exception tarp `submit` ir `shutdown` — executor neuždarytas iki GC.

```python
# PO (pataisyta):
try:
    price_history = ph_fut.result(timeout=1)
except Exception:
    pass
finally:
    _ph_exec.shutdown(wait=False)  # ← vyksta visada
```

### Retry cascade executor

```python
_re = ThreadPoolExecutor(max_workers=4)
try:
    ...
finally:
    _re.shutdown(wait=False)
```

✅ Teisingai valdomas.

---

## ST5 — Render 512MB RAM — Memory Risks ✅ STEBĖTI

### In-memory cache

```python
_CACHE_MAX = int(os.getenv("CACHE_MAX_ENTRIES", "500"))
```

Kiekvienas cache entry ≈ vidutiniškai ~5-50KB (JSON rezultatai). 500 × 50KB = 25MB. **Priimtina.**

### BeautifulSoup parsavimas

Amazon HTML ≈ 500KB-2MB. 10 lygiagrečių scraping threads × 2MB = 20MB peak. **Priimtina 512MB kontekste.**

### scan-image

Priima base64 images iki ~14MB. Vienas kvietimas max ~14MB RAM per apdorojimą. Rate limited per @rate_limit. **Priimtina.**

### Rizikos scenarijus

Jei 20 req/min visi yra scan-image su 14MB nuotraukomis: 20 × 14MB = 280MB. Tai GALI sukurti RAM slėgį kartu su kitais procesais. Bet tai ekstremali situacija.

**Rekomenduojama stebėti:** Render dashboard memory usage po aktyvaus naudojimo.

---

## ST6 — Self-ping Keepalive ✅ VEIKIA

```python
def _keepalive_worker():
    render_url = os.getenv("RENDER_EXTERNAL_URL", "").rstrip("/")
    if not render_url:
        return  # ← silent exit if not configured
    time.sleep(60)
    while True:
        for attempt in range(3):
            try:
                r = _http.get(f"{render_url}/api/health", timeout=10)
                print(f"[KeepAlive] ping {r.status_code}")
                break
            except Exception as e:
                print(f"[KeepAlive] attempt {attempt+1}/3 failed: {e}")
                if attempt < 2:
                    time.sleep(30)
        time.sleep(13 * 60)

threading.Thread(target=_keepalive_worker, daemon=True).start()
```

✅ Ping kas 13 min (Render timeout = 15 min)  
✅ 3 retry su 30s pause  
✅ daemon=True — neblokuoja shutdown  
⚠️ Jei `RENDER_EXTERNAL_URL` nenustatytas → keepalive neveikia. Reikia patikrinti Render env vars.

---

## ST7 — Unhandled Exceptions patikrinimas ✅ GERAI

Visi išoriniai kvietimai turi try/except. Pagrindiniai endpointai:
- `/api/search`: threadpool try/finally + kiekvienas shop try/except
- `/api/search-stream`: generate() try/except + finally cleanup
- `/api/scan-image`: try/except su specific error messages
- Supabase calls: try/except visur

Flask errorhandler užfiksuoja 500:
```python
@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "internal_error"}), 500
```

---

## Žemos rizikos pataisymų suvestinė (šioje šakoje)

| Fix | Statusas |
|---|---|
| `global _amz_blocked_until` — perkeltas į funkcijos pradžią (Python 3.12 fix) | ✅ PATAISYTA |
| `_ph_exec.shutdown` perkeltas į `finally` bloką | ✅ PATAISYTA |
