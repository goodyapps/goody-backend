"""
Goody Backend v5.5 — Fixes:
- Amazon: ScraperAPI render=true + country_code
- Elesen: per platus selector pataisytas (dedup fix)
- Amazon.pl: verčiama į lenkiškai (ne angliškai)
- ThreadPoolExecutor: max_workers=8
- Deduplication: viena parduotuvė = vienas geriausias rezultatas
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os, json, time, hashlib, re, random
import requests
from bs4 import BeautifulSoup
from functools import wraps
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
import anthropic

load_dotenv()

app = Flask(__name__)
CORS(app)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
SCRAPER_API_KEY   = os.getenv("SCRAPER_API_KEY", "")
ZYTE_API_KEY      = os.getenv("ZYTE_API_KEY", "")
DAILY_FREE_LIMIT  = int(os.getenv("DAILY_FREE_LIMIT", "200"))
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "3600"))

cache = {}
rate_store = {}
_fx_cache = {"ts": 0, "rates": {"PLN": 0.233, "GBP": 1.17}}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
]

def get_headers(lang="lt"):
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": f"{lang},en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
    }

def fetch_url(url: str, lang: str = "lt", timeout: int = 10):
    """Fetch URL — Zyte API pirma, tada ScraperAPI, tada tiesiogiai."""
    # 1. Zyte API
    if ZYTE_API_KEY:
        try:
            resp = requests.post(
                "https://api.zyte.com/v1/extract",
                auth=(ZYTE_API_KEY, ""),
                json={"url": url, "httpResponseBody": True},
                timeout=15,
            )
            if resp.status_code == 200:
                import base64
                body = base64.b64decode(resp.json()["httpResponseBody"])
                class FakeResp:
                    status_code = 200
                    def __init__(self, content):
                        self.content = content
                        self.text = content.decode("utf-8", errors="replace")
                print(f"[Zyte OK] {url[:70]}")
                return FakeResp(body)
            print(f"[Zyte {resp.status_code}] fallback")
        except Exception as e:
            print(f"[Zyte err] {e}")

    # 2. ScraperAPI fallback
    # FIX: render=true būtina Amazon, country_code padeda teisingam regionui
    if SCRAPER_API_KEY:
        try:
            is_amazon = "amazon." in url
            country = "de" if "amazon.de" in url else ("pl" if "amazon.pl" in url else "")
            scraper_url = (
                f"http://api.scraperapi.com"
                f"?api_key={SCRAPER_API_KEY}"
                f"&url={requests.utils.quote(url, safe='')}"
                f"&render={'true' if is_amazon else 'false'}"
                + (f"&country_code={country}" if country else "")
            )
            resp = requests.get(scraper_url, timeout=15)
            if resp.status_code == 200:
                print(f"[ScraperAPI OK] {url[:70]}")
                return resp
            print(f"[ScraperAPI {resp.status_code}] fallback → direct")
        except Exception as e:
            print(f"[ScraperAPI err] {e}")

    # 3. Tiesiogiai
    try:
        time.sleep(random.uniform(0.3, 0.9))
        resp = requests.get(url, headers=get_headers(lang), timeout=timeout, allow_redirects=True)
        print(f"[Direct {resp.status_code}] {url[:70]}")
        return resp
    except Exception as e:
        print(f"[Direct err] {e}")
        return None

def get_cache(key):
    if key in cache:
        e = cache[key]
        if time.time() - e["ts"] < CACHE_TTL_SECONDS:
            return e["data"]
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
    except Exception as e:
        print(f"[FX err] {e}")
    return _fx_cache["rates"]

def to_eur(price: float, currency: str) -> float:
    if currency == "EUR":
        return round(price, 2)
    rates = get_fx_rates()
    return round(price * rates.get(currency, 1.0), 2)

def parse_price(text: str) -> float:
    if not text:
        return 0.0
    text = text.replace("\xa0", " ").replace("€", "").replace("Eur", "").replace("EUR", "").strip()
    if "," in text and "." in text:
        text = text.replace(",", "")
    elif "," in text:
        text = text.replace(",", ".")
    m = re.search(r"\d+\.?\d*", text)
    if m:
        try:
            val = float(m.group())
            if 0 < val < 100000:
                return val
        except:
            pass
    return 0.0

def deduplicate_by_shop(results: list) -> list:
    """FIX: Viena parduotuvė = vienas pigiausias rezultatas."""
    best = {}
    for r in results:
        shop = r.get("shop", "")
        price = r.get("price", 999999)
        if shop not in best or price < best[shop].get("price", 999999):
            best[shop] = r
    return list(best.values())

# ── VARLE.LT ──
def scrape_varle(query: str) -> list:
    results = []
    try:
        url = f"https://varle.lt/search/?q={requests.utils.quote(query)}"
        resp = fetch_url(url, "lt")
        if not resp or resp.status_code != 200:
            print(f"[Varle] failed {resp.status_code if resp else 'no response'}")
            return results
        soup = BeautifulSoup(resp.text, "html.parser")
        items = (
            soup.select(".product-list-item") or
            soup.select("[data-product-id]") or
            soup.select(".product-card") or
            soup.select("article.product") or
            soup.select(".search-result-item")
        )
        print(f"[Varle] {len(items)} items")
        for item in items[:6]:
            try:
                price_el = (
                    item.select_one(".price-box__price") or
                    item.select_one("[class*='price-box']") or
                    item.select_one("[class*='product-price']") or
                    item.select_one(".price")
                )
                if not price_el:
                    continue
                price = parse_price(price_el.get_text())
                if not price:
                    continue
                name_el = (
                    item.select_one(".product-list-item__title") or
                    item.select_one("[class*='product-title']") or
                    item.select_one("[class*='product-name']") or
                    item.select_one("h2") or item.select_one("h3")
                )
                name = name_el.get_text(strip=True)[:100] if name_el else query
                link_el = item.select_one("a[href]")
                href = link_el["href"] if link_el else ""
                link = href if href.startswith("http") else f"https://varle.lt{href}"
                results.append(_make_result("Varle.lt", "🇱🇹", link, price, name, "varle"))
            except Exception as e:
                print(f"[Varle item] {e}")
    except Exception as e:
        print(f"[Varle] {e}")
    return results

# ── PIGU.LT ──
def scrape_pigu(query: str) -> list:
    results = []
    try:
        url = f"https://pigu.lt/lt/search?query={requests.utils.quote(query)}"
        resp = fetch_url(url, "lt")
        if not resp or resp.status_code != 200:
            print(f"[Pigu] failed")
            return results
        soup = BeautifulSoup(resp.text, "html.parser")
        items = (
            soup.select(".product-box") or
            soup.select("[class*='product-item']") or
            soup.select("[class*='ProductCard']") or
            soup.select(".catalog-product")
        )
        print(f"[Pigu] {len(items)} items")
        for item in items[:6]:
            try:
                price_el = (
                    item.select_one("[class*='price-main']") or
                    item.select_one("[class*='ProductPrice']") or
                    item.select_one("[class*='price']")
                )
                if not price_el:
                    continue
                price = parse_price(price_el.get_text())
                if not price:
                    continue
                name_el = (
                    item.select_one("[class*='product-name']") or
                    item.select_one("[class*='ProductName']") or
                    item.select_one("h2") or item.select_one("h3") or
                    item.select_one("a[title]")
                )
                name = (name_el.get("title") or name_el.get_text(strip=True))[:100] if name_el else query
                link_el = item.select_one("a[href]")
                href = link_el["href"] if link_el else ""
                link = href if href.startswith("http") else f"https://pigu.lt{href}"
                results.append(_make_result("Pigu.lt", "🇱🇹", link, price, name, "pigu"))
            except Exception as e:
                print(f"[Pigu item] {e}")
    except Exception as e:
        print(f"[Pigu] {e}")
    return results

# ── SENUKAI.LT ──
def scrape_senukai(query: str) -> list:
    results = []
    try:
        url = f"https://www.senukai.lt/paieska?q={requests.utils.quote(query)}"
        resp = fetch_url(url, "lt")
        if not resp or resp.status_code != 200:
            print(f"[Senukai] failed")
            return results
        soup = BeautifulSoup(resp.text, "html.parser")
        items = (
            soup.select(".product-item") or
            soup.select("[class*='product-card']") or
            soup.select(".grid-item") or
            soup.select("[data-sku]")
        )
        print(f"[Senukai] {len(items)} items")
        for item in items[:6]:
            try:
                price_el = (
                    item.select_one(".price-value") or
                    item.select_one("[class*='price']") or
                    item.select_one(".product-price")
                )
                if not price_el:
                    continue
                price = parse_price(price_el.get_text())
                if not price:
                    continue
                name_el = (
                    item.select_one(".product-name") or
                    item.select_one("[class*='name']") or
                    item.select_one("h2") or item.select_one("h3")
                )
                name = name_el.get_text(strip=True)[:100] if name_el else query
                link_el = item.select_one("a[href]")
                href = link_el["href"] if link_el else ""
                link = href if href.startswith("http") else f"https://www.senukai.lt{href}"
                results.append(_make_result("Senukai.lt", "🇱🇹", link, price, name, "senukai"))
            except Exception as e:
                print(f"[Senukai item] {e}")
    except Exception as e:
        print(f"[Senukai] {e}")
    return results

# ── TOPOCENTRAS.LT ──
def scrape_topo(query: str) -> list:
    results = []
    try:
        url = f"https://www.topocentras.lt/search?q={requests.utils.quote(query)}"
        resp = fetch_url(url, "lt")
        if not resp or resp.status_code != 200:
            print(f"[Topo] failed")
            return results
        soup = BeautifulSoup(resp.text, "html.parser")
        items = (
            soup.select(".product-item") or
            soup.select("[class*='ProductCard']") or
            soup.select("[class*='product-list-item']") or
            soup.select(".catalog-grid__item")
        )
        print(f"[Topo] {len(items)} items")
        for item in items[:6]:
            try:
                price_el = (
                    item.select_one(".price__value") or
                    item.select_one("[class*='price']") or
                    item.select_one(".product-price")
                )
                if not price_el:
                    continue
                price = parse_price(price_el.get_text())
                if not price:
                    continue
                name_el = (
                    item.select_one(".product-name") or
                    item.select_one("[class*='title']") or
                    item.select_one("h2") or item.select_one("h3")
                )
                name = name_el.get_text(strip=True)[:100] if name_el else query
                link_el = item.select_one("a[href]")
                href = link_el["href"] if link_el else ""
                link = href if href.startswith("http") else f"https://www.topocentras.lt{href}"
                results.append(_make_result("Topo centras", "🇱🇹", link, price, name, "topo"))
            except Exception as e:
                print(f"[Topo item] {e}")
    except Exception as e:
        print(f"[Topo] {e}")
    return results

# ── ELESEN.LT ──
def scrape_elesen(query: str) -> list:
    results = []
    try:
        url = f"https://www.elesen.lt/paieska?q={requests.utils.quote(query)}"
        resp = fetch_url(url, "lt")
        if not resp or resp.status_code != 200:
            print(f"[Elesen] failed")
            return results
        soup = BeautifulSoup(resp.text, "html.parser")

        # FIX: Buvo "[class*='product']" — per platus, paima ir parent ir children
        # Dabar naudojame tikslesnius selektorius
        items = (
            soup.select(".product-item") or
            soup.select("[class*='product-card']") or
            soup.select("[class*='product-list-item']") or
            soup.select("[class*='catalog-item']") or
            soup.select(".item-box")
        )
        print(f"[Elesen] {len(items)} items")

        for item in items[:6]:
            try:
                price_el = item.select_one("[class*='price']") or item.select_one(".price")
                if not price_el:
                    continue
                price = parse_price(price_el.get_text())
                if not price:
                    continue
                name_el = item.select_one("[class*='name']") or item.select_one("h2") or item.select_one("h3")
                name = name_el.get_text(strip=True)[:100] if name_el else query
                link_el = item.select_one("a[href]")
                href = link_el["href"] if link_el else ""
                link = href if href.startswith("http") else f"https://www.elesen.lt{href}"
                results.append(_make_result("Elesen.lt", "🇱🇹", link, price, name, "elesen"))
            except Exception as e:
                print(f"[Elesen item] {e}")
    except Exception as e:
        print(f"[Elesen] {e}")
    return results

# ── 1A.LT ──
def scrape_1a(query: str) -> list:
    results = []
    try:
        url = f"https://www.1a.lt/search?q={requests.utils.quote(query)}"
        resp = fetch_url(url, "lt")
        if not resp or resp.status_code != 200:
            print(f"[1a] failed")
            return results
        soup = BeautifulSoup(resp.text, "html.parser")
        items = (
            soup.select(".product-item") or
            soup.select("[class*='product-card']") or
            soup.select("[class*='ProductItem']") or
            soup.select(".item-product")
        )
        print(f"[1a] {len(items)} items")
        for item in items[:6]:
            try:
                price_el = item.select_one("[class*='price']") or item.select_one(".price")
                if not price_el:
                    continue
                price = parse_price(price_el.get_text())
                if not price:
                    continue
                name_el = item.select_one("[class*='name']") or item.select_one("h2") or item.select_one("h3")
                name = name_el.get_text(strip=True)[:100] if name_el else query
                link_el = item.select_one("a[href]")
                href = link_el["href"] if link_el else ""
                link = href if href.startswith("http") else f"https://www.1a.lt{href}"
                results.append(_make_result("1a.lt", "🇱🇹", link, price, name, "1a"))
            except Exception as e:
                print(f"[1a item] {e}")
    except Exception as e:
        print(f"[1a] {e}")
    return results

# ── AMAZON ──
def scrape_amazon(query: str, domain: str = "de") -> list:
    results = []
    currency = "PLN" if domain == "pl" else "EUR"
    lang = "pl" if domain == "pl" else "de"
    try:
        url = f"https://www.amazon.{domain}/s?k={requests.utils.quote(query)}&ref=sr_pg_1"
        resp = fetch_url(url, lang)
        if not resp or resp.status_code != 200:
            print(f"[Amazon.{domain}] failed status={resp.status_code if resp else 'none'}")
            return results

        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.select('[data-component-type="s-search-result"]')
        print(f"[Amazon.{domain}] {len(items)} items")

        if len(items) == 0:
            # Debug: ar Amazon grąžino CAPTCHA?
            if "captcha" in resp.text.lower() or "robot" in resp.text.lower():
                print(f"[Amazon.{domain}] CAPTCHA detected!")
            else:
                print(f"[Amazon.{domain}] No items found, HTML length: {len(resp.text)}")

        for item in items[:5]:
            try:
                name_el = item.select_one("h2 a span")
                name = name_el.get_text(strip=True) if name_el else ""
                if not name:
                    continue

                raw = 0.0
                price_el = item.select_one(".a-price .a-offscreen")
                if price_el:
                    raw = parse_price(price_el.get_text())
                if not raw:
                    whole = item.select_one(".a-price-whole")
                    frac = item.select_one(".a-price-fraction")
                    if whole:
                        whole_txt = re.sub(r"[^\d]", "", whole.get_text())
                        frac_txt = re.sub(r"[^\d]", "", frac.get_text() if frac else "00")[:2] or "00"
                        if whole_txt:
                            try:
                                raw = float(f"{whole_txt}.{frac_txt}")
                            except:
                                pass
                if not raw:
                    for sel in [".a-color-price", ".s-price-instructions-style"]:
                        pel = item.select_one(sel)
                        if pel:
                            raw = parse_price(pel.get_text())
                            if raw:
                                break
                if not raw or raw > 100000:
                    continue
                price = to_eur(raw, currency)

                link_el = item.select_one("h2 a")
                href = link_el["href"] if link_el else ""
                link = f"https://www.amazon.{domain}{href}" if href.startswith("/") else href

                asin_m = re.search(r"/dp/([A-Z0-9]{10})", link)
                asin = asin_m.group(1) if asin_m else ""
                aff = (f"https://www.amazon.{domain}/dp/{asin}?tag=goody-21"
                       if asin else f"https://www.amazon.{domain}/s?k={requests.utils.quote(query)}")

                rating = 0
                rating_el = item.select_one(".a-icon-alt")
                if rating_el:
                    m = re.search(r"([\d,]+)", rating_el.get_text())
                    if m:
                        try:
                            rating = float(m.group(1).replace(",", "."))
                        except:
                            pass

                review_count = 0
                rev_el = item.select_one(".a-size-base.s-underline-text")
                if rev_el:
                    m = re.search(r"\d+", rev_el.get_text().replace(".", "").replace(",", ""))
                    if m:
                        try:
                            review_count = int(m.group())
                        except:
                            pass

                prime = bool(item.select_one(".a-icon-prime"))
                orig_note = f"{raw:.0f} {currency}" if currency != "EUR" else ""

                results.append({
                    "shop": f"Amazon.{domain.upper()}",
                    "flag": "🌍" if domain == "de" else "🇵🇱",
                    "url": link, "affiliate_url": aff,
                    "price": price, "currency": "EUR",
                    "original_price": raw if currency != "EUR" else None,
                    "original_currency": currency if currency != "EUR" else None,
                    "in_stock": True,
                    "delivery": "Prime · Tomorrow" if prime else "2-5 d.",
                    "deal_score": 75, "rating": rating, "review_count": review_count,
                    "notes": " · ".join(filter(None, ["Prime" if prime else "", orig_note])),
                    "is_best_value": False, "is_cheapest": False, "is_top_rated": False,
                    "why_recommended": "", "source": f"amazon.{domain}",
                    "product_title": name[:80]
                })
            except Exception as e:
                print(f"[Amazon.{domain} item] {e}")
    except Exception as e:
        print(f"[Amazon.{domain}] {e}")
    return results

def _make_result(shop, flag, link, price, name, source):
    return {
        "shop": shop, "flag": flag,
        "url": link, "affiliate_url": link,
        "price": price, "currency": "EUR", "in_stock": True,
        "delivery": "1-3 d.", "deal_score": 70, "rating": 0,
        "review_count": 0, "notes": "",
        "is_best_value": False, "is_cheapest": False, "is_top_rated": False,
        "why_recommended": "", "source": source, "product_title": name
    }

# ── CLAUDE ──
def claude_translate(query: str, target_lang: str = "en") -> str:
    if not ANTHROPIC_API_KEY:
        return query
    common = ["iphone", "samsung", "sony", "apple", "lg", "xiaomi", "dyson", "macbook", "huawei", "lenovo"]
    if any(w in query.lower() for w in common) and target_lang == "en":
        return query
    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        lang_names = {"en": "English", "de": "German", "pl": "Polish", "lt": "Lithuanian"}
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=60,
            messages=[{"role": "user", "content": f'Translate to {lang_names.get(target_lang, "English")} for e-commerce search. Return ONLY the product name: "{query}"'}]
        )
        result = "".join(b.text for b in resp.content if hasattr(b, "text")).strip().strip('"')
        return result if result else query
    except:
        return query

def claude_analyze(query: str, results: list, price_history: dict = None) -> dict:
    empty = {"verdict": "OK", "verdict_label": "Normal", "verdict_reason": "",
             "ai_summary": "", "alternative": "", "buy_recommendation": "", "price_forecast": ""}
    if not ANTHROPIC_API_KEY or not results:
        return empty
    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        prices_str = ", ".join([f"{r['shop']}: €{r['price']:.2f}" for r in results[:8] if r.get("price", 0) > 0])
        history_str = ""
        if price_history:
            parts = []
            if price_history.get("lowest"):
                parts.append(f"Lowest ever: €{price_history['lowest']}")
            if price_history.get("highest"):
                parts.append(f"Highest ever: €{price_history['highest']}")
            history_str = ", ".join(parts)

        prompt = f"""Product: "{query}"
Prices across shops: {prices_str or "none found"}
{f"Price history: {history_str}" if history_str else ""}

Return ONLY valid JSON (no markdown):
{{"verdict":"BUY|WAIT|SKIP|OK","verdict_label":"Buy now|Wait|Avoid|Normal","verdict_reason":"1 sentence why","ai_summary":"2 sentences analysis","alternative":"cheaper alternative if overpriced, else empty","buy_recommendation":"specific buying advice in 1-2 sentences","price_forecast":"will price drop soon? yes/no/maybe + brief reason"}}"""

        resp = client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        text = "".join(b.text for b in resp.content if hasattr(b, "text")).strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"[Claude analyze] {e}")
        return empty

def get_price_history(query: str) -> dict:
    try:
        resp = fetch_url(f"https://camelcamelcamel.com/search?sq={requests.utils.quote(query)}", "en")
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
        for key, sel in [("lowest", ".lowest_price"), ("highest", ".highest_price")]:
            el = soup2.select_one(sel)
            if el:
                m = re.search(r"[\d]+\.?\d*", el.get_text().replace(",", ""))
                if m:
                    history[key] = float(m.group())
        return history
    except Exception as e:
        print(f"[CamelCamel] {e}")
        return {}

def post_process(results: list, query: str, ai_data: dict = None, price_history: dict = None) -> dict:
    # FIX: Deduplication prieš viską
    results = deduplicate_by_shop(results)
    results = [r for r in results if r.get("price", 0) > 0]

    if not results:
        return {
            "product_name": query, "ai_verdict": "WAIT",
            "verdict_label": "Not found", "verdict_reason": "No prices found.",
            "ai_summary": "Try a more specific product name.",
            "buy_recommendation": "Refine your search.", "alternative": "",
            "price_forecast": "", "deal_score": 0,
            "price_min": 0, "price_max": 0, "price_avg": 0,
            "price_history": price_history or {}, "results": []
        }

    results.sort(key=lambda x: x.get("price", 999999))
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
    deal_score = min(100, int(savings_pct * 1.5 + 50))

    return {
        "product_name": query,
        "ai_verdict": ai.get("verdict", "OK"),
        "verdict_label": ai.get("verdict_label", "Normal"),
        "verdict_reason": ai.get("verdict_reason", ""),
        "ai_summary": ai.get("ai_summary", ""),
        "buy_recommendation": ai.get("buy_recommendation", f"Best price found: €{price_min:.2f}"),
        "alternative": ai.get("alternative", ""),
        "price_forecast": ai.get("price_forecast", ""),
        "deal_score": deal_score,
        "price_min": price_min, "price_max": price_max, "price_avg": price_avg,
        "price_history": price_history or {},
        "results": results
    }

# ── ROUTES ──

@app.route("/api/search", methods=["POST"])
@rate_limit
def search():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "Query required"}), 400

    cache_key = hashlib.md5(f"v55:{query.lower()}".encode()).hexdigest()
    cached = get_cache(cache_key)
    if cached:
        cached["_cached"] = True
        return jsonify(cached)

    try:
        query_de = claude_translate(query, "de")
    except Exception:
        query_de = query

    print(f"\n=== SEARCH: '{query}' → DE:'{query_de}' ===")

    all_results = []

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {
            executor.submit(scrape_elesen,  query):         "Elesen",
            executor.submit(scrape_amazon,  query_de, "de"): "Amazon.DE",
        }

        for f in as_completed(futures, timeout=25):
            name = futures[f]
            try:
                res = f.result(timeout=5)
                print(f"  [{name}] returned {len(res)} results")
                all_results.extend(res)
            except Exception as e:
                print(f"  [{name}] error: {e}")

    print(f"=== TOTAL: {len(all_results)} results before dedup/filter ===\n")

    # Strict 8s cap — fetch_url chain (Zyte+ScraperAPI+direct) was up to 180s here
    price_history = {}
    try:
        with ThreadPoolExecutor(max_workers=1) as phex:
            phf = phex.submit(get_price_history, query_en)
            price_history = phf.result(timeout=8)
    except Exception:
        pass

    ai_data = claude_analyze(query, all_results, price_history)
    result = post_process(all_results, query, ai_data, price_history)
    set_cache(cache_key, result)

    ip = request.remote_addr or "unknown"
    used = rate_store.get(ip, {}).get("count", 1)
    result["_rate"] = {
        "used": used,
        "limit": DAILY_FREE_LIMIT,
        "remaining": max(0, DAILY_FREE_LIMIT - used)
    }
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

        response = client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=256,
            messages=[{"role": "user", "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": data["image"]}},
                {"type": "text", "text": """Analyze this image. Find the product and any visible price.

Respond ONLY with JSON (no markdown):
{"product_name":"BRAND MODEL in English","price_visible":0,"barcode":"","confidence":"high/medium/low"}

Rules:
- product_name: brand + model in English (e.g. "Apple iPhone 16 Pro", "Sony WH-1000XM5")
- price_visible: numeric price in EUR if visible, else 0
- confidence: high=exact model, medium=brand+category, low=category only"""}
            ]}]
        )

        raw_text = ""
        for block in response.content:
            if hasattr(block, "text"):
                raw_text += block.text

        text = raw_text.strip().replace("```json", "").replace("```", "").strip()
        json_m = re.search(r'\{[^{}]*"product_name"[^{}]*\}', text, re.DOTALL)
        if json_m:
            text = json_m.group(0)

        try:
            vision = json.loads(text)
        except:
            name_m = re.search(r'"product_name"\s*:\s*"([^"]+)"', raw_text)
            vision = {
                "product_name": name_m.group(1) if name_m else "",
                "price_visible": 0, "barcode": "", "confidence": "low"
            }

        product_name = vision.get("product_name", "").strip()
        price_visible = vision.get("price_visible", 0)
        confidence = vision.get("confidence", "medium")

        if isinstance(price_visible, (int, float)) and price_visible <= 1:
            price_visible = 0

        if not product_name or (confidence == "low" and len(product_name) < 4):
            return jsonify({
                "error": "product_not_recognized",
                "message": "Produktas neatpažintas. Pabandykite aiškesnę nuotrauką."
            }), 400

        cache_key = hashlib.md5(f"scan_v55:{product_name.lower()}".encode()).hexdigest()
        cached = get_cache(cache_key)
        if cached:
            cached["_cached"] = True
            cached["scanned_product"] = product_name
            cached["store_price"] = price_visible
            return jsonify(cached)

        try:
            query_de = claude_translate(product_name, "de")
        except Exception:
            query_de = product_name

        all_results = []

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {
                executor.submit(scrape_elesen,  product_name):    "Elesen",
                executor.submit(scrape_amazon,  query_de, "de"):  "Amazon.DE",
            }
            for f in as_completed(futures, timeout=25):
                try:
                    all_results.extend(f.result(timeout=5))
                except Exception as e:
                    print(f"[Scan parallel] {e}")

        if isinstance(price_visible, (int, float)) and price_visible > 1:
            all_results.insert(0, {
                "shop": "Scanned price", "flag": "📷", "url": "", "affiliate_url": "",
                "price": price_visible, "currency": "EUR", "in_stock": True,
                "delivery": "In store", "deal_score": 50, "rating": 0,
                "review_count": 0, "notes": "Price from your photo",
                "is_best_value": False, "is_cheapest": False, "is_top_rated": False,
                "why_recommended": "", "source": "scan", "product_title": product_name
            })

        price_history = {}
        try:
            with ThreadPoolExecutor(max_workers=1) as phex:
                phf = phex.submit(get_price_history, product_name)
                price_history = phf.result(timeout=8)
        except Exception:
            pass

        ai_data = claude_analyze(product_name, all_results, price_history)
        result = post_process(all_results, product_name, ai_data, price_history)
        result["scanned_product"] = product_name
        result["store_price"] = price_visible if isinstance(price_visible, (int, float)) and price_visible > 1 else 0
        set_cache(cache_key, result)

        ip = request.remote_addr or "unknown"
        used = rate_store.get(ip, {}).get("count", 1)
        result["_rate"] = {
            "used": used, "limit": DAILY_FREE_LIMIT,
            "remaining": max(0, DAILY_FREE_LIMIT - used)
        }
        return jsonify(result)

    except Exception as e:
        print(f"[scan_image] {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/debug-html", methods=["GET"])
def debug_html():
    """Parodo tikrą HTML iš parduotuvės — debugging tikslais."""
    shop = request.args.get("shop", "varle")
    query = request.args.get("q", "Samsung Galaxy S24")
    urls = {
        "varle":   f"https://varle.lt/search/?q={requests.utils.quote(query)}",
        "pigu":    f"https://pigu.lt/lt/search?query={requests.utils.quote(query)}",
        "1a":      f"https://www.1a.lt/search?q={requests.utils.quote(query)}",
        "senukai": f"https://www.senukai.lt/paieska?q={requests.utils.quote(query)}",
        "topo":    f"https://www.topocentras.lt/search?q={requests.utils.quote(query)}",
        "elesen":  f"https://www.elesen.lt/paieska?q={requests.utils.quote(query)}",
        "amazon":  f"https://www.amazon.de/s?k={requests.utils.quote(query)}",
    }
    url = urls.get(shop, urls["varle"])
    resp = fetch_url(url, "lt")
    if not resp:
        return jsonify({"error": "fetch failed"}), 500
    soup = BeautifulSoup(resp.text, "html.parser")
    classes = set()
    for el in soup.find_all(class_=True):
        for c in el.get("class", []):
            classes.add(c)
    prices_found = []
    for el in soup.find_all(string=re.compile(r'\d+[.,]\d+')):
        txt = el.strip()
        if any(c in txt for c in ['€', 'Eur', 'EUR']) or (re.search(r'\d{2,}[.,]\d{2}', txt)):
            prices_found.append(txt[:50])
    return jsonify({
        "url": url,
        "status": resp.status_code,
        "html_snippet": resp.text[:5000],
        "all_classes": sorted(list(classes))[:100],
        "prices_found": prices_found[:20],
    })

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok", "version": "5.5-goody",
        "shops": ["Elesen.lt", "Amazon.DE"],
        "scraper_api": bool(SCRAPER_API_KEY),
        "anthropic_configured": bool(ANTHROPIC_API_KEY),
        "cache_entries": len(cache)
    })

@app.route("/api/rate-limit", methods=["GET"])
def rate_limit_status():
    ip = request.remote_addr or "unknown"
    today = time.strftime("%Y-%m-%d")
    used = rate_store.get(ip, {}).get("count", 0) if rate_store.get(ip, {}).get("date") == today else 0
    return jsonify({
        "used": used,
        "limit": DAILY_FREE_LIMIT,
        "remaining": max(0, DAILY_FREE_LIMIT - used)
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"\n🟢 Goody API v5.5")
    print(f"📦 Shops: Elesen.lt + Amazon.DE")
    print(f"🔑 ScraperAPI: {'✅ configured' if SCRAPER_API_KEY else '⚠️  not set (direct mode)'}")
    print(f"🤖 Anthropic: {'✅ configured' if ANTHROPIC_API_KEY else '❌ missing'}")
    app.run(host="0.0.0.0", port=port, debug=False)
