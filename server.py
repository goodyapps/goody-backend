"""
Goody Backend v2.0
- Amazon.de + Amazon.pl scraping (nemokama)
- CamelCamelCamel kainų istorija (nemokama)
- UPCitemdb barkodų atpažinimas (nemokama)
- Claude Haiku tik nuotraukoms + verdiktui (~$0.003/užklausa)
- Automatinis vertimas į reikalingą kalbą
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os, json, time, hashlib, re
import requests
from bs4 import BeautifulSoup
from functools import wraps
from dotenv import load_dotenv
import anthropic

load_dotenv()

app = Flask(__name__)
CORS(app)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
DAILY_FREE_LIMIT  = int(os.getenv("DAILY_FREE_LIMIT", "200"))
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "86400"))

cache = {}
rate_store = {}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

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

def lookup_barcode(barcode: str) -> dict:
    try:
        url = f"https://api.upcitemdb.com/prod/trial/lookup?upc={barcode}"
        resp = requests.get(url, headers={"Accept": "application/json"}, timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            items = data.get("items", [])
            if items:
                item = items[0]
                return {"product_name": item.get("title", ""), "brand": item.get("brand", ""), "found": True}
    except Exception as e:
        print(f"UPCitemdb error: {e}")
    return {"found": False, "product_name": ""}

def get_price_history(query: str) -> dict:
    try:
        search_url = f"https://camelcamelcamel.com/search?sq={query.replace(' ', '+')}"
        headers = {**HEADERS, "Accept-Language": "en-US,en;q=0.9"}
        resp = requests.get(search_url, headers=headers, timeout=10)
        if resp.status_code != 200:
            return {}
        soup = BeautifulSoup(resp.text, "html.parser")
        product_link = soup.select_one(".product_image a, .search_result a")
        if not product_link:
            return {}
        href = product_link.get("href", "")
        product_url = f"https://camelcamelcamel.com{href}" if href.startswith("/") else href
        prod_resp = requests.get(product_url, headers=headers, timeout=10)
        if prod_resp.status_code != 200:
            return {}
        prod_soup = BeautifulSoup(prod_resp.text, "html.parser")
        history = {}
        current_el = prod_soup.select_one(".current_price, .price")
        if current_el:
            m = re.search(r"[\d,]+\.?\d*", current_el.get_text().replace(",", ""))
            if m:
                history["current"] = float(m.group())
        high_el = prod_soup.select_one(".highest_price")
        if high_el:
            m = re.search(r"[\d,]+\.?\d*", high_el.get_text().replace(",", ""))
            if m:
                history["highest"] = float(m.group())
        low_el = prod_soup.select_one(".lowest_price")
        if low_el:
            m = re.search(r"[\d,]+\.?\d*", low_el.get_text().replace(",", ""))
            if m:
                history["lowest"] = float(m.group())
        return history
    except Exception as e:
        print(f"CamelCamelCamel error: {e}")
        return {}

def claude_analyze(query: str, results: list, price_history: dict = None) -> dict:
    if not ANTHROPIC_API_KEY:
        return {"verdict": "OK", "verdict_label": "Normal", "verdict_reason": "", "ai_summary": "", "alternative": "", "buy_recommendation": "", "price_forecast": ""}
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    prices_str = ", ".join([f"{r['shop']}: EUR{r['price']}" for r in results[:5] if r.get("price", 0) > 0])
    history_str = ""
    if price_history:
        if price_history.get("lowest"):
            history_str = f"Price history - Lowest: EUR{price_history.get('lowest')}, Highest: EUR{price_history.get('highest', 'N/A')}"
    prompt = f"""Product: "{query}"
Prices found: {prices_str or "none"}
{history_str}

Respond ONLY with JSON:
{{"verdict":"BUY|WAIT|SKIP|OK","verdict_label":"Buy now|Wait|Avoid|Normal","verdict_reason":"1 sentence why","ai_summary":"2 sentences analysis","alternative":"cheaper alternative product name if overpriced, empty string if ok","buy_recommendation":"specific advice","price_forecast":"will price drop soon? yes/no/maybe + brief reason"}}"""
    try:
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        text = "".join(b.text for b in resp.content if hasattr(b, "text"))
        text = text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Claude analyze error: {e}")
        return {"verdict": "OK", "verdict_label": "Normal", "verdict_reason": "", "ai_summary": "", "alternative": "", "buy_recommendation": "", "price_forecast": ""}

def claude_translate(query: str, target_lang: str = "en") -> str:
    if not ANTHROPIC_API_KEY:
        return query
    common_english = ["iphone", "samsung", "sony", "apple", "lg", "xiaomi", "dyson", "amazon", "macbook", "ipad"]
    if any(w in query.lower() for w in common_english) and target_lang == "en":
        return query
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    lang_names = {"en": "English", "de": "German", "pl": "Polish", "lt": "Lithuanian"}
    lang_name = lang_names.get(target_lang, "English")
    try:
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=60,
            messages=[{"role": "user", "content": f'Translate this product name to {lang_name} for e-commerce search. Return ONLY the translated name: "{query}"'}]
        )
        result = "".join(b.text for b in resp.content if hasattr(b, "text")).strip().strip('"')
        return result if result else query
    except:
        return query

def scrape_amazon(query: str, domain: str = "de", lang: str = "de") -> list:
    results = []
    try:
        url = f"https://www.amazon.{domain}/s?k={query.replace(' ', '+')}"
        headers = {**HEADERS, "Accept-Language": f"{lang}-{domain.upper()},{lang};q=0.9,en;q=0.8"}
        resp = requests.get(url, headers=headers, timeout=15)
        print(f"Amazon.{domain} status: {resp.status_code} for '{query}'")
        if resp.status_code != 200:
            return results
        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.select('[data-component-type="s-search-result"]')
        print(f"Amazon.{domain} items: {len(items)}")
        shop_name = f"Amazon.{domain}"
        flag = "🌍" if domain == "de" else "🇵🇱"
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
                price_text = price_whole.get_text(strip=True).replace(".", "").replace(",", "").replace("\xa0", "")
                price_text = re.sub(r"[^\d]", "", price_text)
                frac_text = price_frac.get_text(strip=True) if price_frac else "00"
                frac_text = re.sub(r"[^\d]", "", frac_text)[:2] or "00"
                if not price_text:
                    continue
                try:
                    price = float(f"{price_text}.{frac_text}")
                except:
                    continue
                if price <= 0 or price > 100000:
                    continue
                link_el = item.select_one("h2 a")
                link = ""
                if link_el:
                    href = link_el.get("href", "")
                    link = f"https://www.amazon.{domain}{href}" if href.startswith("/") else href
                asin_match = re.search(r"/dp/([A-Z0-9]{10})", link)
                asin = asin_match.group(1) if asin_match else ""
                affiliate_url = f"https://www.amazon.{domain}/dp/{asin}?tag=goody-21" if asin else f"https://www.amazon.{domain}/s?k={query.replace(' ', '+')}"
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
                    m = re.search(r"[\d]+", review_el.get_text().replace(".", "").replace(",", ""))
                    if m:
                        try:
                            review_count = int(m.group())
                        except:
                            pass
                prime = bool(item.select_one(".a-icon-prime"))
                delivery = "Prime · Tomorrow" if prime else "2-5 days"
                results.append({
                    "shop": shop_name, "flag": flag, "url": link, "affiliate_url": affiliate_url,
                    "price": price, "currency": "EUR", "in_stock": True, "delivery": delivery,
                    "deal_score": 75, "rating": rating, "review_count": review_count,
                    "notes": "Prime" if prime else "", "is_best_value": False, "is_cheapest": False,
                    "is_top_rated": False, "why_recommended": "", "source": f"amazon.{domain}",
                    "product_title": name[:80]
                })
            except Exception as e:
                print(f"Item parse error: {e}")
                continue
    except Exception as e:
        print(f"Amazon.{domain} error: {e}")
    return results

def post_process(results: list, query: str, ai_data: dict = None, price_history: dict = None) -> dict:
    results = [r for r in results if r.get("price", 0) > 0]
    if not results:
        return {
            "product_name": query, "product_emoji": "🔍", "ai_verdict": "WAIT",
            "verdict_label": "Not found", "verdict_reason": "No prices found.",
            "ai_summary": "Try a more specific product name.", "buy_recommendation": "Refine your search.",
            "alternative": "", "price_forecast": "", "deal_score": 0,
            "price_min": 0, "price_max": 0, "price_avg": 0, "price_history": price_history or {}, "results": []
        }
    results.sort(key=lambda x: x.get("price", 0))
    prices = [r["price"] for r in results]
    price_min = min(prices)
    price_max = max(prices)
    price_avg = round(sum(prices) / len(prices), 2)
    results[0]["is_cheapest"] = True
    rated = [r for r in results if r.get("rating", 0) > 0]
    if rated:
        max(rated, key=lambda r: r.get("rating", 0))["is_top_rated"] = True
    best_idx = max(range(len(results)), key=lambda i: results[i].get("deal_score", 0))
    results[best_idx]["is_best_value"] = True
    verdict = "OK"
    verdict_label = "Normal"
    verdict_reason = f"Prices from EUR{price_min:.2f} to EUR{price_max:.2f}."
    ai_summary = f"Found {len(results)} prices. Cheapest: EUR{price_min:.2f}."
    alternative = ""
    buy_recommendation = f"Best price: EUR{price_min:.2f}"
    price_forecast = ""
    if ai_data:
        verdict = ai_data.get("verdict", verdict)
        verdict_label = ai_data.get("verdict_label", verdict_label)
        verdict_reason = ai_data.get("verdict_reason", verdict_reason)
        ai_summary = ai_data.get("ai_summary", ai_summary)
        alternative = ai_data.get("alternative", "")
        buy_recommendation = ai_data.get("buy_recommendation", buy_recommendation)
        price_forecast = ai_data.get("price_forecast", "")
    savings_pct = ((price_max - price_min) / price_max * 100) if price_max > 0 else 0
    deal_score = min(100, int(savings_pct * 2 + 50))
    return {
        "product_name": query, "product_emoji": "🛒", "ai_verdict": verdict,
        "verdict_label": verdict_label, "verdict_reason": verdict_reason,
        "ai_summary": ai_summary, "buy_recommendation": buy_recommendation,
        "alternative": alternative, "price_forecast": price_forecast,
        "deal_score": deal_score, "price_min": price_min, "price_max": price_max,
        "price_avg": price_avg, "price_history": price_history or {}, "results": results
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
    cache_key = hashlib.md5(f"v2:{query}".encode()).hexdigest()
    cached = get_cache(cache_key)
    if cached:
        cached["_cached"] = True
        return jsonify(cached)
    query_en = claude_translate(query, "en")
    query_de = claude_translate(query, "de")
    query_pl = claude_translate(query, "pl")
    print(f"Query: {query} -> EN: {query_en}, DE: {query_de}, PL: {query_pl}")
    results_de = scrape_amazon(query_de, "de", "de")
    results_pl = scrape_amazon(query_pl, "pl", "pl")
    all_results = results_de + results_pl
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
        b64 = data["image"]
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        vision_prompt = """Analyze this image carefully.

PRODUCT: What exact product? Brand + model number in English.
PRICE: Look everywhere for price tag/label/sticker - even if far from product.
  - Price might be on shelf label, hanging tag, separate sticker
  - Look for any numbers with currency symbols
  - If you see a price tag anywhere in image, report it
BARCODE: Any barcode or QR code?

Return ONLY valid JSON (no markdown):
{"product_name":"exact brand and model in English","price_visible":0,"barcode":"","context":"brief description"}

Rules: price_visible = exact number if clearly a price, 0 if none found."""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": b64}},
                {"type": "text", "text": vision_prompt}
            ]}]
        )
        text = "".join(b.text for b in response.content if hasattr(b, "text"))
        text = text.strip().replace("```json", "").replace("```", "").strip()
        try:
            vision = json.loads(text)
        except:
            vision = {"product_name": "", "price_visible": 0, "barcode": ""}

        product_name = vision.get("product_name", "").strip()
        price_visible = vision.get("price_visible", 0)
        barcode = vision.get("barcode", "")

        if isinstance(price_visible, (int, float)) and price_visible <= 1:
            price_visible = 0

        if barcode and not product_name:
            upc_data = lookup_barcode(barcode)
            if upc_data.get("found"):
                product_name = upc_data["product_name"]

        if not product_name:
            return jsonify({"error": "product_not_recognized", "message": "Could not identify product. Try a clearer photo."}), 400

        cache_key = hashlib.md5(f"scan_v2:{product_name}".encode()).hexdigest()
        cached = get_cache(cache_key)
        if cached:
            cached["_cached"] = True
            cached["scanned_product"] = product_name
            cached["store_price"] = price_visible
            return jsonify(cached)

        query_de = claude_translate(product_name, "de")
        query_pl = claude_translate(product_name, "pl")
        results_de = scrape_amazon(query_de, "de", "de")
        results_pl = scrape_amazon(query_pl, "pl", "pl")
        all_results = results_de + results_pl

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
def barcode_lookup_route(barcode):
    cache_key = f"upc:{barcode}"
    cached = get_cache(cache_key)
    if cached:
        return jsonify(cached)
    result = lookup_barcode(barcode)
    if result.get("found"):
        set_cache(cache_key, result)
    return jsonify(result)

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "version": "2.0-goody", "features": ["amazon.de", "amazon.pl", "camelcamelcamel", "upcitemdb", "claude-haiku"], "api_configured": bool(ANTHROPIC_API_KEY), "cache_entries": len(cache)})

@app.route("/api/rate-limit", methods=["GET"])
def rate_limit_status():
    ip = request.remote_addr or "unknown"
    today = time.strftime("%Y-%m-%d")
    used = rate_store.get(ip, {}).get("count", 0) if rate_store.get(ip, {}).get("date") == today else 0
    return jsonify({"used": used, "limit": DAILY_FREE_LIMIT, "remaining": max(0, DAILY_FREE_LIMIT - used)})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"Goody API v2.0 on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
