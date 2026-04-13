"""
SmartShop Test Backend — Amazon.de Scraping
Skirta bug'ų išgaudymui prieš paleidžiant pilną versiją
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
DAILY_FREE_LIMIT  = int(os.getenv("DAILY_FREE_LIMIT", "100"))
CACHE_TTL_SECONDS = 3600

cache = {}
rate_store = {}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
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
            return jsonify({"error": "daily_limit", "message": "Limitas pasiektas.", "remaining": 0}), 429
        return f(*args, **kwargs)
    return decorated

# ── AMAZON.DE SCRAPING ─────────────────────────────
def scrape_amazon(query: str) -> list:
    results = []
    try:
        url = f"https://www.amazon.de/s?k={query.replace(' ', '+')}&language=lt"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        
        print(f"Amazon status: {resp.status_code}")
        
        if resp.status_code != 200:
            print(f"Amazon blocked: {resp.status_code}")
            return results

        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Amazon produktų kortelės
        items = soup.select('[data-component-type="s-search-result"]')
        print(f"Amazon items found: {len(items)}")

        for item in items[:6]:
            try:
                # Pavadinimas
                name_el = item.select_one("h2 a span, h2 span")
                name = name_el.get_text(strip=True) if name_el else ""
                if not name:
                    continue

                # Kaina
                price_whole = item.select_one(".a-price-whole")
                price_frac = item.select_one(".a-price-fraction")
                
                if not price_whole:
                    continue
                    
                price_text = price_whole.get_text(strip=True).replace(".", "").replace(",", "")
                frac_text = price_frac.get_text(strip=True) if price_frac else "00"
                
                try:
                    price = float(f"{price_text}.{frac_text}")
                except:
                    continue

                if price <= 0 or price > 50000:
                    continue

                # Nuoroda
                link_el = item.select_one("h2 a")
                link = ""
                if link_el:
                    href = link_el.get("href", "")
                    if href.startswith("/"):
                        link = "https://www.amazon.de" + href
                    else:
                        link = href

                # Reitingas
                rating_el = item.select_one(".a-icon-alt")
                rating = 0
                if rating_el:
                    rating_match = re.search(r"([\d,]+)", rating_el.get_text())
                    if rating_match:
                        try:
                            rating = float(rating_match.group(1).replace(",", "."))
                        except:
                            pass

                # Review count
                review_el = item.select_one('[aria-label*="Bewertung"], .a-size-base.s-underline-text')
                review_count = 0
                if review_el:
                    rev_match = re.search(r"[\d.,]+", review_el.get_text().replace(".", "").replace(",", ""))
                    if rev_match:
                        try:
                            review_count = int(rev_match.group())
                        except:
                            pass

                # Prime
                prime = bool(item.select_one(".a-icon-prime"))
                delivery = "Prime 1-2 d." if prime else "2-5 d."

                results.append({
                    "shop": "Amazon.de",
                    "flag": "🌍",
                    "url": link,
                    "affiliate_url": f"https://www.amazon.de/s?k={query.replace(' ', '+')}&tag=smartshop-21",
                    "price": price,
                    "currency": "EUR",
                    "in_stock": True,
                    "delivery": delivery,
                    "deal_score": 75,
                    "rating": rating,
                    "review_count": review_count,
                    "notes": "Prime" if prime else "",
                    "is_best_value": False,
                    "is_cheapest": False,
                    "is_top_rated": False,
                    "why_recommended": "",
                    "source": "amazon.de",
                    "product_title": name[:80]
                })

            except Exception as e:
                print(f"Item parse error: {e}")
                continue

    except Exception as e:
        print(f"Amazon scraping error: {e}")

    return results

def post_process(results: list, query: str) -> dict:
    results = [r for r in results if r.get("price", 0) > 0]
    
    if not results:
        return {
            "product_name": query,
            "product_emoji": "🔍",
            "ai_verdict": "WAIT",
            "verdict_label": "Nerasta",
            "verdict_reason": "Nepavyko rasti kainų.",
            "ai_summary": "Bandykite tikslesnį pavadinimą.",
            "buy_recommendation": "Patikslinkite paiešką.",
            "deal_score": 0,
            "price_min": 0, "price_max": 0, "price_avg": 0,
            "results": [],
            "debug": "No results found"
        }

    results.sort(key=lambda x: x.get("price", 0))
    prices = [r["price"] for r in results]
    price_min = min(prices)
    price_max = max(prices)
    price_avg = round(sum(prices) / len(prices))

    results[0]["is_cheapest"] = True

    rated = [r for r in results if r.get("rating", 0) > 0]
    if rated:
        max(rated, key=lambda r: r.get("rating", 0))["is_top_rated"] = True

    savings_pct = ((price_max - price_min) / price_max * 100) if price_max > 0 else 0

    if savings_pct > 15:
        verdict, verdict_label = "BUY", "Pirkti dabar"
        reason = f"Pigiausia kaina {price_min:.2f}€ — {savings_pct:.0f}% pigiau."
    else:
        verdict, verdict_label = "OK", "Normalu"
        reason = f"Kainos nuo {price_min:.2f}€ iki {price_max:.2f}€."

    return {
        "product_name": query,
        "product_emoji": "🛒",
        "ai_verdict": verdict,
        "verdict_label": verdict_label,
        "verdict_reason": reason,
        "ai_summary": f"Rastos {len(results)} kainos Amazon.de. Pigiausia: {price_min:.2f}€.",
        "buy_recommendation": f"Pigiausia: {price_min:.2f}€",
        "deal_score": min(100, int(savings_pct * 2 + 50)),
        "price_min": price_min,
        "price_max": price_max,
        "price_avg": price_avg,
        "results": results
    }

def analyze_image(image_b64: str) -> dict:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image_b64}},
                {"type": "text", "text": 'Return ONLY JSON no markdown: {"product_name":"exact brand and model in English","price_visible":0,"barcode":""}'}
            ]
        }]
    )
    text = "".join(b.text for b in response.content if hasattr(b, "text"))
    try:
        s = text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(s)
    except:
        return {"product_name": "", "price_visible": 0, "barcode": ""}

@app.route("/api/search", methods=["POST"])
@rate_limit
def search():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "Query required"}), 400

    cache_key = hashlib.md5(f"amz:{query}".encode()).hexdigest()
    cached = get_cache(cache_key)
    if cached:
        cached["_cached"] = True
        return jsonify(cached)

    results = scrape_amazon(query)
    result = post_process(results, query)
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
        vision = analyze_image(data["image"])
        product_name = vision.get("product_name", "").strip()
        price_visible = vision.get("price_visible", 0)

        if not product_name:
            return jsonify({"error": "product_not_recognized", "message": "Nepavyko atpažinti produkto"}), 400

        cache_key = hashlib.md5(f"amz_scan:{product_name}".encode()).hexdigest()
        cached = get_cache(cache_key)
        if cached:
            cached["_cached"] = True
            cached["scanned_product"] = product_name
            cached["store_price"] = price_visible
            return jsonify(cached)

        results = scrape_amazon(product_name)

        if isinstance(price_visible, (int, float)) and price_visible > 1:
            results.insert(0, {
                "shop": "📷 Nuskaitytas",
                "flag": "📷",
                "url": "",
                "affiliate_url": "",
                "price": price_visible,
                "currency": "EUR",
                "in_stock": True,
                "delivery": "Fizinė parduotuvė",
                "deal_score": 50,
                "rating": 0, "review_count": 0,
                "notes": "Kaina iš nuotraukos",
                "is_best_value": False, "is_cheapest": False, "is_top_rated": False,
                "why_recommended": "", "source": "scan"
            })

        result = post_process(results, product_name)
        result["scanned_product"] = product_name
        result["store_price"] = price_visible if isinstance(price_visible, (int, float)) and price_visible > 1 else 0
        set_cache(cache_key, result)

        ip = request.remote_addr or "unknown"
        used = rate_store.get(ip, {}).get("count", 1)
        result["_rate"] = {"used": used, "limit": DAILY_FREE_LIMIT, "remaining": max(0, DAILY_FREE_LIMIT - used)}
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "version": "4.0-amazon-test", "api_configured": bool(ANTHROPIC_API_KEY)})

@app.route("/api/rate-limit", methods=["GET"])
def rate_limit_status():
    ip = request.remote_addr or "unknown"
    today = time.strftime("%Y-%m-%d")
    used = rate_store.get(ip, {}).get("count", 0) if rate_store.get(ip, {}).get("date") == today else 0
    return jsonify({"used": used, "limit": DAILY_FREE_LIMIT, "remaining": max(0, DAILY_FREE_LIMIT - used)})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"SmartShop Amazon Test v4.0 on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
