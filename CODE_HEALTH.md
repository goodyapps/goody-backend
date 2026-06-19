# CODE_HEALTH.md
**Data:** 2026-06-19 | **Šaka:** security-night  
**Metodas:** Statinė kodo analizė — server.py (~7600 eilučių)

---

## APIBENDRINIMAS

| Kategorija | Radinių | Sunkumas |
|---|---|---|
| Silent exception handlers | 87 | 🟡 Vidutinis |
| Accessory list duplication | 1 | 🟡 Vidutinis |
| Logging (print vs logging) | 97+ | 🟢 Žemas |
| ThreadPoolExecutor cleanup | 2 | 🟡 Vidutinis |
| Version history komentaras | 1 | 🟢 Žemas |
| _fx_cache race condition | 1 | 🟡 Vidutinis |
| Scraper code duplication | 6 | 🟢 Žemas (known) |

---

## H1 — 87 SILENT EXCEPTION HANDLERS

**Mastai:** `grep "except Exception:" server.py | wc -l` = 87 vietų

**Problemos tipas:** Daugelis jų turi `pass` arba tuščią eilutę — klaida įvyksta, bet neinformuoja.

**Konkretūs pavyzdžiai — klaidos prarandamos tyliai:**

```python
# server.py:207 (bootstrap) — DB klaida prarandama tyliai
try:
    ...
except Exception:
    pass   # ← Supabase init klaida — niekada nematysime

# server.py:1314 — FX rate update klaida
try:
    rates = fetch_fx_rates()
except Exception:
    pass   # ← Valiutos kursų atnaujinimas nepavyko — nematyti

# server.py:1439 — Supabase upsert klaida
try:
    sb.table(...).upsert(...).execute()
except Exception:
    pass   # ← Kainų istorija nerašoma — nematyti
```

**Pataisymas (žema rizika):**
```python
# Vietoj:
except Exception:
    pass

# Naudoti:
except Exception as e:
    print(f"[modul] WARNING: {e}")
```

**Prioritetiniai** (paslėptos klaidos, paveikiančios veikimą):
- `_sb_upsert_search` (line ~1198) — search count neįrašomas
- `_sb_upsert_price` (line ~1226) — kainų istorija neįrašoma
- FX rate update — valiuta klaidi
- Supabase init (line ~207) — nežinome ar DB prisijungta

**Nevertingi** (scraper item failures): ~40 `except Exception as e: print(...)` — jau loguoja.

---

## H2 — ACCESSORY KEYWORD DUPLICATION

**Problem:** Dvi skirtingos accessory žodžių sąrašai tame pačiame faile:

```python
# line 254: ACCESSORY_KEYWORDS (list) — naudojama /api/classify endpoint
ACCESSORY_KEYWORDS = ["case", "cover", "protector", ...]  # 40+ žodžių

# line 454: _ACCESSORY_MATCH_WORDS (frozenset) — naudojama is_relevant_result()
_ACCESSORY_MATCH_WORDS = frozenset({'case', 'cover', 'sleeve', ...})  # 80+ žodžių
```

**Skirtumas:** `_ACCESSORY_MATCH_WORDS` turi daugiau žodžių (LT/DE/PL) ir naudoja `frozenset` (O(1) lookup). `ACCESSORY_KEYWORDS` yra senesnė sąrašo forma.

**Rizika:** Naujas žodis pridedamas į vieną sąrašą bet ne kitą → nenuoseklus elgesys `/api/classify` vs `is_relevant_result`.

**Pataisymas (vidutinė rizika — reikia peržiūros):**
```python
# Sujungti į vieną:
_ACCESSORY_MATCH_WORDS = frozenset({...})  # pilnas sąrašas
ACCESSORY_KEYWORDS = list(_ACCESSORY_MATCH_WORDS)  # /api/classify naudoja list

# Arba: palikti atskirai, bet pridėti komentarą kad sinchronizuoti reikia
```

---

## H3 — PRINT() VIETOJ LOGGING

**Mastai:** 97+ `print(f"[...")` eilučių serveryje.

**Problema:** 
- Render logai rodo viską — sunku filtruoti pagal level (WARNING vs INFO vs DEBUG)
- Jei `sys.stdout` perdengiamas (pvz., testavime) — viskas prarandama
- Nėra timestamp informacijos (Render prideda patį, bet ne modulis)

**Dabartinė situacija:** Gerai sustruktūruoti logai su `[ModuleName]` prefix — tai jau geriau nei daugelyje projektų. Gunicorn prideda timestamp.

**Rekomendacija (žema rizika):**
```python
import logging
log = logging.getLogger("goody")

# Vietoj:
print(f"[Elesen] 0 results")

# Naudoti:
log.info("[Elesen] 0 results")
log.warning("[scan_image] image_too_large: %s chars", len(image_b64))
```

**Prioritetas: ŽEMAS** — dabartinė sistema veikia, migracija didelė, rizikingas darbas.

---

## H4 — THREADPOOLEXECUTOR BEZ `with` KONTEKSTO

**Problem 1 — scan_image (line 7109-7114):**
```python
_scan_ph_exec = ThreadPoolExecutor(max_workers=1)  # ← be `with`
scan_ph_fut = _scan_ph_exec.submit(get_price_history, search_query)
scan_executor = ThreadPoolExecutor(max_workers=10)  # ← be `with`
try:
    ...
finally:
    scan_executor.shutdown(wait=False)  # ← tik scan_executor
    # _scan_ph_exec NIEKADA neuždaromas!
```

**Poveikis:** `_scan_ph_exec` thread pool nenaikinama po kiekvieno scan-image kvietimo. 
- `wait=False` reiškia threads gali tęsti veiklą fone
- Po >1000 kvietimų: thread leak, gali pritrūkti resursų

**Pataisymas (žema rizika):**
```python
# Pakeisti _scan_ph_exec su:
with ThreadPoolExecutor(max_workers=1) as _scan_ph_exec:
    scan_ph_fut = _scan_ph_exec.submit(get_price_history, search_query)
    # ... rest of code

# Arba pridėti į finally:
finally:
    scan_executor.shutdown(wait=False)
    _scan_ph_exec.shutdown(wait=False)  # ← PRIDĖTA
```

**Problem 2 — search() endpoint (line ~6210):**
```python
with ThreadPoolExecutor(max_workers=12) as executor:  # ← ✓ naudoja `with`
```
Čia gerai — naudoja konteksto tvarkyklę.

**search_stream — ✓ GERAI:**
```python
finally:
    stream_executor.shutdown(wait=False)
    _ph_exec.shutdown(wait=False)  # runs even on GeneratorExit
```

---

## H5 — _FX_CACHE THREAD RACE CONDITION

**Kodas (~line 711):**
```python
_fx_cache = {"ts": 0, "rates": {"PLN": 0.233, "GBP": 1.17}}

def get_fx_rate(currency):
    if time.time() - _fx_cache["ts"] < 3600:  # 1h cache
        return _fx_cache["rates"].get(currency, 1.0)
    # Fetch new rates
    ...
    _fx_cache["ts"] = time.time()      # ← ne-atominis
    _fx_cache["rates"] = new_rates     # ← ne-atominis
```

**Problema:** Du request'ai vienu metu → abu mato "cache expired" → abu siunčia HTTP request FX rate API. Lenktyniavimas dėl cache atnaujinimo.

**Praktinis poveikis:** ŽEMAS — FX API kviečiamas max 2x per valandą per thread (gunicorn 4 threads). FX rate fetch yra greita (< 1s). Jei nepavyksta → default rates naudojami.

**Pataisymas (žema rizika):**
```python
import threading
_fx_lock = threading.Lock()

def get_fx_rate(currency):
    with _fx_lock:
        if time.time() - _fx_cache["ts"] < 3600:
            return _fx_cache["rates"].get(currency, 1.0)
    # fetch outside lock
    ...
    with _fx_lock:
        _fx_cache.update({"ts": time.time(), "rates": new_rates})
```

---

## H6 — 130 EILUČIŲ VERSION HISTORY FAILO VIRŠUJE

**Problema:** `server.py` prasideda 130 eilučių su:
```python
"""
- v7.55 — scan-image: extract exact product_code...
- v7.54 — ...
- v7.53 — ...
...
- v6.01 — ...
"""
```

**Poveikis:** Kodas skaitymas sunkesnis — reikia slinkti žemyn prieš matant pirmus realius kodo sakinius. Visa ši informacija yra git historijoje.

**Rekomendacija:** Perkelti į `CHANGELOG.md` ir palikti tik 5-10 paskutinių versijų komentarą kode.

**Prioritetas: ŽEMAS** — nefunkcinis pakeitimas, visada galima vėliau.

---

## H7 — 6 IDENTIŠKAI STRUKTŪRUOTI SCRAPERS

**Scraper funkcijos su panašia struktūra:**
- `_scrape_varle_from_html` (line 2253)
- `_scrape_pigu_from_html` (line 2322)
- `_scrape_lupa_items` (line 2376) — naudoja ir Senukai, ir 1a
- `_scrape_topo_from_html` (line 2436)
- `_scrape_elesen_from_html` (line 2497)
- `_scrape_amazon_*` (kelios funkcijos)

**Bendra struktūra:**
```python
def _scrape_X_from_html(html, query):
    soup = BeautifulSoup(html)
    items = soup.select("[selector1]") or soup.select("[selector2]")
    for item in items[:8]:
        try:
            price = parse_price(item.select_one("[price-sel]"))
            if not price: continue
            name = item.select_one("[name-sel]").get_text()
            if not is_relevant_result(query, name): continue
            link = item.select_one("a")["href"]
            results.append(_make_result(...))
        except Exception:
            pass
    return results
```

**Kodas nėra blogas** — shop-specific selectors reikalauja atskirų funkcijų. Unifikacija su callback-based abstraction padidintų kompleksiškumą neduodant aiškios naudos.

**Rekomendacija:** Palikti kaip yra — abstrakcijai ne laikas.

---

## PRIORITETŲ LENTELĖ

| # | Problema | Sunkumas | Veikimo poveikis | Darbas |
|---|---|---|---|---|
| 1 | _scan_ph_exec neuždarytas | 🟡 Vidutinis | Thread leak per laiką | 2 eilutės |
| 2 | Silent DB/Supabase exceptions | 🟡 Vidutinis | Klaidos prarandamos | ~10 vietų |
| 3 | _fx_cache race condition | 🟡 Vidutinis | Minimalus praktiškai | 5 eilutės |
| 4 | ACCESSORY_KEYWORDS duplikacija | 🟡 Vidutinis | Nenuoseklumas | Peržiūrai |
| 5 | print() vietoj logging | 🟢 Žemas | Nefunkcinis | Didelis refactor |
| 6 | Version history komentaras | 🟢 Žemas | Nefunkcinis | Vienkartinis |
| 7 | Scraper code duplication | 🟢 Žemas | Nefunkcinis | Didelis refactor |

---

## TRUMPALAIKIAI FIX'AI (gali būti atlikti be rizikos)

### Fix 1: _scan_ph_exec neuždarytas
```python
# server.py ~7183 (scan_image finally block)
finally:
    scan_executor.shutdown(wait=False)
    _scan_ph_exec.shutdown(wait=False)  # ← PRIDĖTI ŠIĄ EILUTĘ
```

### Fix 2: Silent Supabase upsert exceptions
```python
# Visose _sb_upsert_* funkcijose:
except Exception as e:
    print(f"[Supabase] WARNING upsert failed: {e}")  # vietoj pass
```

**Šie fix'ai palikti peržiūrai rytą** — žema rizika, bet reikia tikslių eilučių numerių prieš keičiant.
