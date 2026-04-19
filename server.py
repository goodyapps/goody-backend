"""
Goody Backend v5.0
- Varle.lt, Pigu.lt, Senukai.lt, Topo centras, Elesen.lt, 1a.lt
- Amazon.de + Amazon.pl (PLN->EUR auto konvertavimas)
- ScraperAPI (Cloudflare bypass) + rotating headers fallback
- CamelCamelCamel kainų istorija + UPCitemdb barkodai
- Valiutų kursai realiu laiku
- Claude Haiku verdiktas + vertimas + alternatyva
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os, json, time, hashlib, re, random
import requests
from bs4 import BeautifulSoup
from functools import wraps
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
from dotenv import load_dotenv
import anthropic

load_dotenv()

app = Flask(__name__)
CORS(app)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
SCRAPER_API_KEY   = os.getenv("SCRAPER_API_KEY", "")
DAILY_FREE_LIMIT  = int(os.getenv("DAILY_FREE_LIMIT", "200"))
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "86400"))

cache = {}
rate_store = {}
_fx_cache = {"ts": 0, "rates": {"PLN": 0.233, "GBP": 1.17, "CZK": 0.041, "SEK": 0.088}}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

def get_headers(lang="lt"):
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": f"{lang},en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }

def fetch_url(url: str, lang: str = "lt"):
    if SCRAPER_API_KEY:
        try:
            scraper_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={requests.utils.quote(url, safe='')}&render=false"
            resp = requests.get(scraper_url, timeout=20)
            if resp.status_code == 200:
                print(f"ScraperAPI OK: {url[:60]}")
                return resp
            print(f"ScraperAPI {resp.status_code}, fallback to direct")
        except Exception as e:
            print(f"ScraperAPI error: {e}")
    try:
        time.sleep(random.uniform(0.2, 0.7))
        resp = requests.get(url, headers=get_headers(lang), timeout=12)
        print(f"Direct {resp.status_code}: {url[:60]}")
        return resp
    except Exception as e:
        print(f"Direct error: {e}")
        return None

def get_cache(key):
    if key in cache:
        entry = cache[key]
        if time.time() - entry["ts"] < CACHE_TTL_SECONDS:
            return entry["data"]
        del cache[key]
    return None

def set_cache(key, data):
    cache[key] = {"data": data, "ts": time.time()}

def rate_limit(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        ip = request.remote_addr or "unknown"
        today = time.strftime("%Y-%m-%d")
        if ip not in rate_store or rate_store[ip]["date"] != today:
            rate_store[ip] = {"date": today, "count": 0}
        rate_store[ip]["count"] += 1
        if rate_store[ip]["count"] > DAILY_FREE_LIMIT:
            return jsonify({"error": "daily_limit", "message": "Daily limit reached.", "remaining": 0}), 429
        return f(*args, **kwargs)
    return decorated

def get_fx_rates() -> dict:
    if time.time() - _fx_cache["ts"] < 21600:
        return _fx_cache["rates"]
    try:
        resp = requests.get("https://api.exchangerate-api.com/v4/latest/EUR", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            _fx_cache["rates"] = {k: round(1/v, 6) for k, v in data.get("rates", {}).items() if v > 0}
            _fx_cache["ts"] = time.time()
            print(f"FX updated: 1 PLN = {_fx_cache['rates'].get('PLN', '?')} EUR")
    except Exception as e:
        print(f"FX error: {e}")
    return _fx_cache["rates"]

def to_eur(price: float, currency: str) -> float:
    if currency == "EUR":
        return round(price, 2)
    rates = get_fx_rates()
    rate = rates.get(currency, 1.0)
    return round(price * rate, 2)

def lookup_barcode(barcode: str) -> dict:
    try:
        resp = requests.get(f"https://api.upcitemdb.com/prod/trial/lookup?upc={barcode}",
                           headers={"Accept": "application/json"}, timeout=8)
        if resp.status_code == 200:
            items = resp.json().get("items", [])
            if items:
                return {"product_name": items[0].get("title", ""), "found": True}
    except Exception as e:
        print(f"UPCitemdb error: {e}")
    return {"found": False, "product_name": ""}

def get_price_history(query: str) -> dict:
    try:
        resp = fetch_url(f"https://camelcamelcamel.com/search?sq={query.replace(' ', '+')}", "en")
        if not resp or resp.status_code != 200:
            return {}
        soup = BeautifulSoup(resp.text, "html.parser")
        link = soup.select_one(".product_image a, .search_result a")
        if not link:
            return {}
        href = link.get("href", "")
        prod_url = f"https://camelcamelcamel.com{href}" if href.startswith("/") else href
        resp2 = fetch_url(prod_url, "en")
        if not resp2 or resp2.status_code != 200:
            return {}
        soup2 = BeautifulSoup(resp2.text, "html.parser")
        history = {}
        for key, sel in [("current", ".current_price"), ("highest", ".highest_price"), ("lowest", ".lowest_price")]:
            el = soup2.select_one(sel)
            if el:
                m = re.search(r"[\d]+\.?\d*", el.get_text().replace(",", ""))
                if m:
                    history[key] = float(m.group())
        return history
    except Exception as e:
        print(f"CCC error: {e}")
        return {}

def scrape_amazon(query: str, domain: str = "de", lang: str = "de") -> list:
    results = []
    orig_currency = "PLN" if domain == "pl" else "EUR"
    try:
        url = f"https://www.amazon.{domain}/s?k={query.replace(' ', '+')}"
        resp = fetch_url(url, lang)
        if not resp or resp.status_code != 200:
            return results

        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.select('[data-component-type="s-search-result"]')
        print(f"Amazon.{domain}: {len(items)} items for '{query}'")

        for item in items[:5]:
            try:
                name_el = item.select_one("h2 a span, h2 span")
                name = name_el.get_text(strip=True) if name_el else ""
                if not name:
                    continue

                price_whole = item.select_one(".a-price-whole")
                price_frac = item.select_one(".a-price-fraction")
                if not price_whole:
                    continue

                price_text = re.sub(r"[^\d]", "", price_whole.get_text().replace("\xa0", ""))
                frac_text = re.sub(r"[^\d]", "", price_frac.get_text() if price_frac else "00")[:2] or "00"
                if not price_text:
                    continue

                raw_price = float(f"{price_text}.{frac_text}")
                if raw_price <= 0 or raw_price > 100000:
                    continue

                price_eur = to_eur(raw_price, orig_currency)

                link_el = item.select_one("h2 a")
                link = ""
                if link_el:
                    href = link_el.get("href", "")
                    link = f"https://www.amazon.{domain}{href}" if href.startswith("/") else href

                asin_match = re.search(r"/dp/([A-Z0-9]{10})", link)
                asin = asin_match.group(1) if asin_match else ""
                affiliate_url = (f"https://www.amazon.{domain}/dp/{asin}?tag=goody-21" if asin
                                else f"https://www.amazon.{domain}/s?k={query.replace(' ', '+')}")

                rating_el = item.select_one(".a-icon-alt")
                rating = 0
                if rating_el:
                    m = re.search(r"([\d,]+)", rating_el.get_text())
                    if m:
                        try:
                            rating = float(m.group(1).replace(",", "."))
                        except:
                            pass

                review_el = item.select_one(".a-size-base.s-underline-text")
                review_count = 0
                if review_el:
                    m = re.search(r"\d+", review_el.get_text().replace(".", "").replace(",", ""))
                    if m:
                        try:
                            review_count = int(m.group())
                        except:
                            pass

                prime = bool(item.select_one(".a-icon-prime"))
                orig_note = f"{raw_price:.0f} {orig_currency}" if orig_currency != "EUR" else ""
                notes = " · ".join(filter(None, ["Prime" if prime else "", orig_note]))

                results.append({
                    "shop": f"Amazon.{domain}",
                    "flag": "🌍" if domain == "de" else "🇵🇱",
                    "url": link, "affiliate_url": affiliate_url,
                    "price": price_eur, "currency": "EUR",
                    "original_price": raw_price if orig_currency != "EUR" else None,
                    "original_currency": orig_currency if orig_currency != "EUR" else None,
                    "in_stock": True,
                    "delivery": "Prime · Tomorrow" if prime else "2-5 days",
                    "deal_score": 75, "rating": rating, "review_count": review_count,
                    "notes": notes,
                    "is_best_value": False, "is_cheapest": False, "is_top_rated": False,
                    "why_recommended": "", "source": f"amazon.{domain}",
                    "product_title": name[:80]
                })
            except Exception as e:
                print(f"Amazon item error: {e}")
    except Exception as e:
        print(f"Amazon.{domain} error: {e}")
    return results

SHOPS_CONFIG = [
    {
        "id": "varle", "name": "Varle.lt", "flag": "🇱🇹",
        "search_url": "https://varle.lt/search/?q={query}",
        "item_sel": ".product-list-item, [class*='product-card'], .product-item",
        "price_sel": ".price-box, [class*='price'], .price",
        "name_sel": "h2, h3, [class*='product-name']",
        "link_sel": "a[href]",
    },
    {
        "id": "pigu", "name": "Pigu.lt", "flag": "🇱🇹",
        "search_url": "https://pigu.lt/lt/search?query={query}",
        "item_sel": ".product-box, [class*='product-item'], [class*='product-card']",
        "price_sel": "[class*='price'], .price",
        "name_sel": "[class*='product-name'], h2, h3",
        "link_sel": "a[href]",
    },
    {
        "id": "senukai", "name": "Senukai.lt", "flag": "🇱🇹",
        "search_url": "https://www.senukai.lt/paieska?q={query}",
        "item_sel": ".product-item, [class*='product-card']",
        "price_sel": "[class*='price'], .price",
        "name_sel": "[class*='name'], h2, h3",
        "link_sel": "a[href]",
    },
    {
        "id": "topocentras", "name": "Topo centras", "flag": "🇱🇹",
        "search_url": "https://www.topocentras.lt/search?q={query}",
        "item_sel": ".product-item, [class*='product']",
        "price_sel": "[class*='price'], .price",
        "name_sel": "[class*='name'], h2, h3",
        "link_sel": "a[href]",
    },
    {
        "id": "elesen", "name": "Elesen.lt", "flag": "🇱🇹",
        "search_url": "https://www.elesen.lt/paieska?q={query}",
        "item_sel": ".product-item, [class*='product']",
        "price_sel": "[class*='price'], .price",
        "name_sel": "[class*='name'], h2, h3",
        "link_sel": "a[href]",
    },
    {
        "id": "1a", "name": "1a.lt", "flag": "🇱🇹",
        "search_url": "https://www.1a.lt/search?q={query}",
        "item_sel": ".product-item, [class*='product-card']",
        "price_sel": "[class*='price'], .price",
        "name_sel": "[class*='name'], h2, h3",
        "link_sel": "a[href]",
    },
]

def scrape_shop(shop: dict, query: str) -> list:
    results = []
    try:
        url = shop["search_url"].replace("{query}", query.replace(" ", "+"))
        resp = fetch_url(url, "lt")
        if not resp or resp.status_code != 200:
            print(f"{shop['name']} failed")
            return results

        soup = BeautifulSoup(resp.text, "html.parser")
        items = []
        for sel in shop["item_sel"].split(", "):
            items = soup.select(sel.strip())
            if items:
                break

        print(f"{shop['name']}: {len(items)} items")

        for item in items[:5]:
            try:
                price_el = None
                for sel in shop["price_sel"].split(", "):
                    price_el = item.select_one(sel.strip())
                    if price_el:
                        break
                if not price_el:
                    continue

                price_text = re.sub(r"[^\d,.]", "", price_el.get_text().replace("\xa0", "").replace(" ", ""))
                price_text = price_text.replace(",", ".")
                m = re.search(r"\d+\.?\d*", price_text)
                if not m:
                    continue
                price = float(m.group())
                if price <= 0 or price > 100000:
                    continue

                link_el = item.select_one(shop["link_sel"])
                link = ""
                if link_el:
                    href = link_el.get("href", "")
                    if href.startswith("http"):
                        link = href
                    elif href.startswith("/"):
                        base = "/".join(url.split("/")[:3])
                        link = base + href

                name_el = None
                for sel in shop["name_sel"].split(", "):
                    name_el = item.select_one(sel.strip())
                    if name_el:
                        break
                name = name_el.get_text(strip=True)[:80] if name_el else query

                results.append({
                    "shop": shop["name"], "flag": shop["flag"],
                    "url": link, "affiliate_url": link,
                    "price": price, "currency": "EUR", "in_stock": True,
                    "delivery": "1-3 d.", "deal_score": 72, "rating": 0,
                    "review_count": 0, "notes": "",
                    "is_best_value": False, "is_cheapest": False,
                    "is_top_rated": False, "why_recommended": "",
                    "source": shop["id"], "product_title": name
                })
            except Exception as e:
                print(f"{shop['name']} item error: {e}")
    except Exception as e:
        print(f"{shop['name']} error: {e}")
    return results

def claude_translate(query: str, target_lang: str = "en") -> str:
    if not ANTHROPIC_API_KEY:
        return query
    common_en = ["iphone", "samsung", "sony", "apple", "lg", "xiaomi", "dyson", "macbook", "ipad", "huawei", "lenovo"]
    if any(w in query.lower() for w in common_en) and target_lang == "en":
        return query
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    lang_names = {"en": "English", "de": "German", "pl": "Polish", "lt": "Lithuanian"}
    try:
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=60,
            messages=[{"role": "user", "content": f'Translate to {lang_names.get(target_lang, "English")} for e-commerce search. Return ONLY the translated product name: "{query}"'}]
        )
        result = "".join(b.text for b in resp.content if hasattr(b, "text")).strip().strip('"')
        return result if result else query
    except:
        return query

def claude_analyze(query: str, results: list, price_history: dict = None) -> dict:
    empty = {"verdict": "OK", "verdict_label": "Normal", "verdict_reason": "", "ai_summary": "", "alternative": "", "buy_recommendation": "", "price_forecast": ""}
    if not ANTHROPIC_API_KEY:
        return empty
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    prices_str = ", ".join([f"{r['shop']}: €{r['price']:.2f}" for r in results[:6] if r.get("price", 0) > 0])
    history_str = ""
    if price_history:
        parts = []
        if price_history.get("lowest"):
            parts.append(f"Lowest ever: €{price_history['lowest']}")
        if price_history.get("highest"):
            parts.append(f"Highest ever: €{price_history['highest']}")
        history_str = ", ".join(parts)
    prompt = f"""Product: "{query}"
Prices found: {prices_str or "none"}
{f"Price history: {history_str}" if history_str else ""}

Return ONLY valid JSON:
{{"verdict":"BUY|WAIT|SKIP|OK","verdict_label":"Buy now|Wait|Avoid|Normal","verdict_reason":"1 sentence why","ai_summary":"2 sentences analysis","alternative":"cheaper alternative product name if overpriced, empty string if good deal","buy_recommendation":"specific buying advice","price_forecast":"will price drop soon? yes/no/maybe + brief reason"}}"""
    try:
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        text = "".join(b.text for b in resp.content if hasattr(b, "text")).strip().replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Claude analyze error: {e}")
        return empty

def post_process(results: list, query: str, ai_data: dict = None, price_history: dict = None) -> dict:
    results = [r for r in results if r.get("price", 0) > 0]
    if not results:
        return {
            "product_name": query, "product_emoji": "🔍", "ai_verdict": "WAIT",
            "verdict_label": "Not found", "verdict_reason": "No prices found.",
            "ai_summary": "Try a more specific product name or model number.",
            "buy_recommendation": "Refine your search.", "alternative": "",
            "price_forecast": "", "deal_score": 0,
            "price_min": 0, "price_max": 0, "price_avg": 0,
            "price_history": price_history or {}, "results": []
        }
    results.sort(key=lambda x: x.get("price", 0))
    prices = [r["price"] for r in results]
    price_min, price_max = min(prices), max(prices)
    price_avg = round(sum(prices) / len(prices), 2)
    results[0]["is_cheapest"] = True
    rated = [r for r in results if r.get("rating", 0) > 0]
    if rated:
        max(rated, key=lambda r: r.get("rating", 0))["is_top_rated"] = True
    results[max(range(len(results)), key=lambda i: results[i].get("deal_score", 0))]["is_best_value"] = True
    ai = ai_data or {}
    savings_pct = ((price_max - price_min) / price_max * 100) if price_max > 0 else 0
    return {
        "product_name": query, "product_emoji": "🛒",
        "ai_verdict": ai.get("verdict", "OK"),
        "verdict_label": ai.get("verdict_label", "Normal"),
        "verdict_reason": ai.get("verdict_reason", ""),
        "ai_summary": ai.get("ai_summary", ""),
        "buy_recommendation": ai.get("buy_recommendation", f"Best price: €{price_min:.2f}"),
        "alternative": ai.get("alternative", ""),
        "price_forecast": ai.get("price_forecast", ""),
        "deal_score": min(100, int(savings_pct * 2 + 50)),
        "price_min": price_min, "price_max": price_max, "price_avg": price_avg,
        "price_history": price_history or {}, "results": results
    }

@app.route("/api/search", methods=["POST"])
@rate_limit
def search():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "Query required"}), 400

    cache_key = hashlib.md5(f"v5:{query}".encode()).hexdigest()
    cached = get_cache(cache_key)
    if cached:
        cached["_cached"] = True
        return jsonify(cached)

    query_en = claude_translate(query, "en")
    query_de = claude_translate(query, "de")
    query_pl = claude_translate(query, "pl")
    print(f"Query: '{query}' -> EN:'{query_en}' DE:'{query_de}' PL:'{query_pl}'")

    # ── PARALLEL SCRAPING — visos parduotuvės vienu metu ──
    all_results = []
    tasks = []
    for shop in SHOPS_CONFIG:
        tasks.append(("shop", shop, query))

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {}
        for task in tasks:
            if task[0] == "shop":
                f = executor.submit(scrape_shop, task[1], task[2])
            futures[f] = task[0]

        for f in as_completed(futures, timeout=25):
            try:
                all_results.extend(f.result(timeout=5))
            except Exception as e:
                print(f"Parallel task error: {e}")

    price_history = get_price_history(query_en) if all_results else {}
    ai_data = claude_analyze(query_en, all_results, price_history)
    result = post_process(all_results, query, ai_data, price_history)
    set_cache(cache_key, result)

    ip = request.remote_addr or "unknown"
    used = rate_store.get(ip, {}).get("count", 1)
    result["_rate"] = {"used": used, "limit": DAILY_FREE_LIMIT, "remaining": max(0, DAILY_FREE_LIMIT - used)}
    return jsonify(result)

@app.route("/api/scan-image", methods=["POST"])
@rate_limit
def scan_image():
    data = request.get_json()
    if not data or "image" not in data:
        return jsonify({"error": "No image"}), 400
    if not ANTHROPIC_API_KEY:
        return jsonify({"error": "API key missing"}), 500
    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        # ŽINGSNIS 1: Vizualus atpažinimas su web_search tool
        response = client.messages.create(
            model="claude-sonnet-4-20250514", max_tokens=1024,
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=[{"role": "user", "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": data["image"]}},
                {"type": "text", "text": """You are a product recognition expert for a Lithuanian price comparison app. Analyze this image and identify the product.

## YOUR TASK:

**STEP 1 — Read ALL text in the image:**
- Brand names, model numbers on packaging, labels, screens, tags
- Lithuanian product labels (translate to English):
  * "Belaidės ausinės" → wireless headphones
  * "Dulkių siurblys" → vacuum cleaner
  * "Nešiojamas kompiuteris" → laptop
  * "Išmanusis telefonas" → smartphone
  * "Oro valytuvas" → air purifier
  * "Kavos aparatas" → coffee machine
  * "Skalbimo mašina" → washing machine
  * "Šaldytuvas" → refrigerator
  * "Mikrobangų krosnelė" → microwave
  * "Robotas dulkių siurblys" → robot vacuum
  * "Laidynė" → iron
  * "Plaukų džiovintuvas" → hair dryer
  * "Elektrinė dantų šepetėlė" → electric toothbrush
- Model numbers: SM-S928B, iPhone 16, V15 Detect, WH-1000XM5, etc.
- Store shelf label text (Varle.lt, Pigu.lt, Senukai.lt, Topo centras)

**STEP 2 — Visual recognition:**
- Identify product by shape, design, color even without readable text
- If you see a partial brand name or logo, identify it

**STEP 3 — If unsure, use web_search:**
- Search for the model number or partial name you found
- Search for the product description in Lithuanian if you read it
- Example: search "SM-S928B" or "Dyson V15 Detect specifications"

**STEP 4 — Price detection:**
- Find ANY price in the image: shelf labels, stickers, tags, displays
- Lithuanian formats: 299,99 € / 299.99 € / 299 € / 299-
- Convert to decimal: 299.99

**STEP 5 — Barcode:**
- EAN-13, EAN-8 or QR code if visible

After your analysis, respond with ONLY this JSON (no markdown, no extra text):
{"product_name":"BRAND MODEL in English","price_visible":0,"barcode":"","context":"what you see","confidence":"high/medium/low"}

CRITICAL RULES:
- product_name must be brand + model in English
- Use web_search if you need to identify a model number or partial name
- If you can identify category but not exact model, return e.g. "Bosch cordless drill" or "Samsung robot vacuum"
- confidence: high=exact model known, medium=brand+category known, low=only category known
- NEVER return empty product_name — always return your best identification"""}
            ]}]
        )

        # Surinkti tekstą iš visų response blokų (įskaitant po web_search)
        raw_text = ""
        for block in response.content:
            if hasattr(block, "text"):
                raw_text += block.text
        # Ieškoti JSON iš raw_text
        text = raw_text.strip().replace("```json", "").replace("```", "").strip()
        # Ištraukti JSON jei yra papildomo teksto
        json_match = re.search(r'\{[^{}]*"product_name"[^{}]*\}', text, re.DOTALL)
        if json_match:
            text = json_match.group(0)
        try:
            vision = json.loads(text)
        except:
            # Bandyti ištraukti product_name iš teksto
            name_match = re.search(r'"product_name"\s*:\s*"([^"]+)"', raw_text)
            vision = {
                "product_name": name_match.group(1) if name_match else "",
                "price_visible": 0,
                "barcode": "",
                "confidence": "low"
            }

        product_name = vision.get("product_name", "").strip()
        price_visible = vision.get("price_visible", 0)
        barcode = vision.get("barcode", "")
        confidence = vision.get("confidence", "medium")

        if isinstance(price_visible, (int, float)) and price_visible <= 1:
            price_visible = 0

        # Jei barkodas rastas — bandyti UPCitemdb
        if barcode and not product_name:
            upc = lookup_barcode(barcode)
            if upc.get("found"):
                product_name = upc["product_name"]

        # Jei produktas vis dar neatpažintas ir confidence žemas
        if not product_name or (confidence == "low" and len(product_name) < 4):
            return jsonify({"error": "product_not_recognized", "message": "Produktas neatpažintas. Pabandykite aiškesnę nuotrauką arba artimiau priartinkite prie produkto/etiketės."}), 400

        cache_key = hashlib.md5(f"scan_v5:{product_name}".encode()).hexdigest()
        cached = get_cache(cache_key)
        if cached:
            cached["_cached"] = True
            cached["scanned_product"] = product_name
            cached["store_price"] = price_visible
            return jsonify(cached)

        query_de = claude_translate(product_name, "de")
        query_pl = claude_translate(product_name, "pl")

        all_results = []
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(scrape_shop, shop, product_name): shop["name"] for shop in SHOPS_CONFIG}
            for f in as_completed(futures, timeout=25):
                try:
                    all_results.extend(f.result(timeout=5))
                except Exception as e:
                    print(f"Scan parallel error: {e}")

        if isinstance(price_visible, (int, float)) and price_visible > 1:
            all_results.insert(0, {
                "shop": "Scanned price", "flag": "📷", "url": "", "affiliate_url": "",
                "price": price_visible, "currency": "EUR", "in_stock": True,
                "delivery": "In store", "deal_score": 50, "rating": 0, "review_count": 0,
                "notes": "Price from your photo", "is_best_value": False, "is_cheapest": False,
                "is_top_rated": False, "why_recommended": "", "source": "scan"
            })

        price_history = get_price_history(product_name) if all_results else {}
        ai_data = claude_analyze(product_name, all_results, price_history)
        result = post_process(all_results, product_name, ai_data, price_history)
        result["scanned_product"] = product_name
        result["store_price"] = price_visible if isinstance(price_visible, (int, float)) and price_visible > 1 else 0
        set_cache(cache_key, result)

        ip = request.remote_addr or "unknown"
        used = rate_store.get(ip, {}).get("count", 1)
        result["_rate"] = {"used": used, "limit": DAILY_FREE_LIMIT, "remaining": max(0, DAILY_FREE_LIMIT - used)}
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/barcode/<barcode>", methods=["GET"])
def barcode_route(barcode):
    cached = get_cache(f"upc:{barcode}")
    if cached:
        return jsonify(cached)
    result = lookup_barcode(barcode)
    if result.get("found"):
        set_cache(f"upc:{barcode}", result)
    return jsonify(result)

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok", "version": "5.0-goody",
        "shops": [s["name"] for s in SHOPS_CONFIG] + ["Amazon.de", "Amazon.pl"],
        "scraper_api": bool(SCRAPER_API_KEY),
        "api_configured": bool(ANTHROPIC_API_KEY),
        "cache_entries": len(cache)
    })

@app.route("/api/rate-limit", methods=["GET"])
def rate_limit_status():
    ip = request.remote_addr or "unknown"
    today = time.strftime("%Y-%m-%d")
    used = rate_store.get(ip, {}).get("count", 0) if rate_store.get(ip, {}).get("date") == today else 0
    return jsonify({"used": used, "limit": DAILY_FREE_LIMIT, "remaining": max(0, DAILY_FREE_LIMIT - used)})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"Goody API v5.0")
    print(f"Shops: {', '.join(s['name'] for s in SHOPS_CONFIG)} + Amazon.de + Amazon.pl")
    print(f"ScraperAPI: {'configured' if SCRAPER_API_KEY else 'not set (direct mode)'}")
    app.run(host="0.0.0.0", port=port, debug=True)
