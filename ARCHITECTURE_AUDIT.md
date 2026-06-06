# Goody Backend — Architektūros auditas
_Data: 2026-06-06 | Versija: server.py v7.55_

---

## 1. DUOMENŲ BAZĖ

**Yra. Supabase (PostgreSQL).**

Naudojamas `supabase` Python SDK (`supabase>=2.0.0`). Jokio SQLAlchemy, psycopg2, sqlite3 ar `.db` failų.

### Sukurta lentelė (`supabase_setup.sql`):

```sql
price_history (
  id           bigserial PRIMARY KEY,
  product_name text NOT NULL,
  shop         text NOT NULL,
  price        numeric(10,2) NOT NULL,
  currency     text DEFAULT 'EUR',
  checked_at   timestamptz DEFAULT now()
)
```

Indeksas: `(product_name, checked_at DESC)`. Row Level Security įjungtas — `anon` gali skaityti ir rašyti.

### Kaip naudojama:
- `save_prices_to_supabase()` — fire-and-forget per `threading.Thread` po kiekvienos paieškos
- `fetch_price_history_from_supabase()` — skaito paskutines 90 dienų, max 500 eilučių
- `_sb_load_search_counts()` — startuojant užkraunami populiarių paieškų skaičiai

**Nėra:** watchlist lentelės, vartotojų lentelės, notifikacijų lentelės.

---

## 2. ENDPOINT'AI

| Metodas | URL | Aprašas |
|---------|-----|---------|
| POST | `/api/search` | Pagrindinė paieška: scrape'ina visas parduotuves, grąžina kainas + AI analizę. Saugo į Supabase. |
| POST | `/api/search-stream` | SSE srautinė paieška — siunčia daliniai rezultatai iš kiekvienos parduotuvės atskirai, pabaigoje AI. |
| GET | `/api/price-history?q=...` | Kainų istorija iš Supabase — sugrupuota pagal dieną ir parduotuvę, skirta Chart.js grafiko frontend'e. |
| POST | `/api/watchlist-check` | Patikrina sąrašą produktų prieš Supabase istoriją (7 d. langas). Praneša jei kaina pasiekė target arba krito. |
| POST | `/api/classify` | Klasifikuoja produktą pagal pavadinimą (kategorija, rekomenduojamas minimalus kainų slenkstis). |
| POST | `/api/barcode` | Barkodo paieška — lookup pagal EAN/UPC. |
| POST | `/api/scan-image` | Nuotraukos analizė (Claude Vision) — identifikuoja produktą, tada ieško kainų. |
| GET | `/api/popular-searches` | Populiariausios paieškos (in-memory, užkrauta iš Supabase startuojant). |
| POST | `/api/track` | Click tracking — įrašo paspaudimą į parduotuvę (in-memory). |
| GET | `/api/click-stats` | Click statistika (reikia `DEBUG_API_KEY`). |
| GET | `/api/cache-stats` | Cache statistika, kaštų skaičiavimas (reikia `DEBUG_API_KEY`). |
| GET | `/api/debug-html` | Debuginimui — grąžina raw HTML iš parduotuvės (reikia `DEBUG_API_KEY`). |
| GET | `/api/health` | Serverio sveikata, versija, konfigūracijos statusas. |
| GET | `/api/rate-limit` | Rate limit statusas pagal IP. |

---

## 3. KAINŲ GAVIMAS

### Srautas:
```
Vartotojas → POST /api/search
  → normalize_query()
  → cache check (in-memory, TTL 30 min)
  → lygiagrečiai scrape'ina parduotuves:
      Varle.lt, Elesen.lt, Pigu.lt, Topocentras.lt, Amazon.DE, Amazon.PL
  → kiekvienai parduotuvei: fetch_url() → BeautifulSoup parse → extract_prices()
  → dedup + sort by price
  → analyze_deal_with_ai() → OpenAI arba Claude
  → threading.Thread → save_prices_to_supabase()
  → grąžina JSON
```

### Kaip `fetch_url()` gauna HTML:

1. **ScraperAPI** (pirmas) — `api.scraperapi.com`
   - LT parduotuvės: 1 kreditas (standard)
   - LT parduotuvės su JS: 5 kreditai (render=true)
   - Amazon: 25 kreditai (premium=true, render=true, anti-bot bypass)
2. **Zyte API** (fallback, tik LT parduotuvės) — `api.zyte.com/v1/extract` su `httpResponseBody`
3. **Direct HTTP** (paskutinis fallback) — tiesioginiai requests su lietuviškais headers

### AI analizė:
- `analyze_deal_with_ai()` → `openai_analyze()` arba `claude_analyze()`
- Naudojama TIK kai ≥2 parduotuvės ir kainų skirtumas ≥5%
- Kitais atvejais: `rule_based_ai_analyze()` (nemokama, rule-based logika)

---

## 4. PRIKLAUSOMYBĖS (`requirements.txt`)

| Paketas | Versija | Paskirtis |
|---------|---------|-----------|
| flask | 3.0.3 | Web framework |
| flask-cors | 4.0.1 | CORS middleware |
| python-dotenv | 1.0.1 | `.env` kintamųjų skaitymas |
| gunicorn | 21.2.0 | WSGI serveris (Render deploy) |
| anthropic | >=0.40.0 | Claude API (AI analizė + scan-image) |
| openai | >=1.0.0 | OpenAI GPT API (AI analizė) |
| requests | 2.31.0 | HTTP scraping, ScraperAPI, Zyte |
| beautifulsoup4 | 4.12.3 | HTML parsing (kainų ištraukimas) |
| lxml | 5.1.0 | BS4 greitesnis parser'is |
| supabase | >=2.0.0 | Supabase PostgreSQL SDK |
| urllib3 | >=2.0.0 | HTTP pool (requests dependency) |

---

## 5. SCHEDULER / CRON

**Nėra jokio išorinio scheduler'io (APScheduler, Celery, cron).** Veikia du background thread'ai:

| Thread | Kas daro | Periodiškumas |
|--------|----------|---------------|
| `_keepalive_worker` | Pingina `GET /api/health` kad Render free-tier neužmigtų | Kas 13 min |
| `_sb_load_search_counts` | Vienkartinis — užkrauna populiarias paieškas iš Supabase | Tik startuojant |

`save_prices_to_supabase()` kviečiamas per `threading.Thread` po kiekvienos paieškos — tai **ne scheduler**, o fire-and-forget reaktyvus įrašas.

**Išvada:** kainos į DB patenka TIK kai realus vartotojas ieško. Nėra automatinio naktinio kainų tikrinimo.

---

## 6. ENV KINTAMIEJI

| Kintamasis | Default | Paskirtis |
|------------|---------|-----------|
| `ANTHROPIC_API_KEY` | — | Claude API raktas |
| `OPENAI_API_KEY` | — | OpenAI API raktas |
| `SUPABASE_URL` | — | Supabase projekto URL |
| `SUPABASE_KEY` | — | Supabase anon/service key |
| `SCRAPER_API_KEY` | — | ScraperAPI raktas (HTML scraping) |
| `ZYTE_API_KEY` | — | Zyte API raktas (fallback scraping) |
| `AI_PROVIDER` | `"openai"` | `"openai"` arba `"claude"` |
| `AI_MODEL_OPENAI` | `"gpt-4o-mini"` | OpenAI modelis |
| `AI_MODEL_CLAUDE` | `"claude-haiku-4-5-20251001"` | Claude modelis |
| `AI_MAX_TOKENS` | `150` | Max tokenų AI atsakymui |
| `ALLOWED_ORIGINS` | `"*"` | CORS leistini origins |
| `DAILY_FREE_LIMIT` | `200` | Max paieškų per dieną per IP |
| `MINUTE_LIMIT` | `20` | Max paieškų per minutę per IP |
| `CACHE_TTL_SECONDS` | `1800` | Cache gyvavimo laikas (30 min) |
| `POPULAR_CACHE_TTL` | `7200` | Populiarių paieškų cache (2 val) |
| `POPULAR_THRESHOLD` | `5` | Min paieškų skaičius "populiari" statusui |
| `CACHE_MAX_ENTRIES` | `500` | Max cache įrašų kiekis |
| `SHOP_TIMEOUT` | `5` | HTTP timeout sekundėmis per parduotuvę |
| `DEBUG_API_KEY` | — | Raktas debug endpoint'ams |
| `VARLE_AFFILIATE_TAG` | — | Varle affiliate ref parametras |
| `AMAZON_AFFILIATE_TAG` | `"goody-21"` | Amazon Associates tag |
| `RENDER_EXTERNAL_URL` | — | Render deploy URL (keepalive pingui) |
| `PORT` | `5000` | HTTP port |

---

## 7. DEPLOY

| Failas | Turinys |
|--------|---------|
| `Procfile` | `web: gunicorn server:app --workers 1 --worker-class gthread --threads 4 --timeout 120 --keep-alive 5 --log-level info` |
| `render.yaml` | **Nėra** |
| `runtime.txt` | **Nėra** |

Deploy'inama į Render — GitHub auto-deploy (push į `main` → Render perkrauna). Python versija nenurodytas (Render aptinka automatiškai).

---

## 8. KO TRŪKSTA — kainų stebėjimo sistema su istorija

### Kas jau veikia ✅
- `price_history` lentelė Supabase su indeksu
- `save_prices_to_supabase()` — įrašo kainas po kiekvienos paieškos
- `GET /api/price-history` — grąžina duomenis Chart.js grafiko
- `POST /api/watchlist-check` — patikrina watchlist prieš istoriją

### Ko trūksta ❌

**1. Periodinis automatinis kainų tikrinimas**
Dabar kainos registruojamos tik kai kas nors ieško. Jei produkto niekas neiešką savaitę — kainų istorija neaugą. Reikia:
- `APScheduler` arba Render Cron Job (arba GitHub Actions cron)
- Kasdien / kas 6h perscanuoti populiarius produktus arba watchlist'o produktus

**2. Watchlist saugojimas serverio pusėje**
Dabar watchlist gyvena tik `localStorage` — jei vartotojas išvalo naršyklę, watchlist dingsta. Supabase reikia lentelės:
```sql
watchlist (id, user_identifier text, product_name text, target_price numeric, created_at)
```

**3. Notifikacijos (email / push)**
`/api/watchlist-check` grąžina alerts JSON'ą, bet jis kviečiamas iš frontend'o tik kai vartotojas atsidaro app'ą. Reikia:
- Email siuntimo (Resend / SendGrid) kai kaina krenta
- Arba Web Push notifikacijos (Service Worker + VAPID)

**4. Vartotojų identifikacija**
Nėra autentifikacijos — watchlist'as neturi `user_id`. Reikia arba:
- Supabase Auth (pilna auth sistema)
- Arba paprastesnio sprendimo: unikalus `device_id` (UUID generuojamas frontend'e, saugomas `localStorage`)

**5. Kainų deduplication istorijoje**
Šiandien tą patį produktą ieško 50 žmonių → 50 identišku įrašų tuo pačiu metu. Reikia `ON CONFLICT DO NOTHING` arba `UPSERT` pagal `(product_name, shop, DATE(checked_at))`.
