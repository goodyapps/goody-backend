"""
Goody Backend v5.10 — All Lithuanian shops + relevance filtering:
- All 8 shops now active: Varle, Pigu, 1a, Senukai, Topo, Elesen, Amazon.DE, Amazon.PL
- Product relevance filter: accessories and wrong models filtered from results
- Fixed AI model: gpt-4o-mini (was gpt-5.4-mini which does not exist)
- Supabase price history (v5.9) retained
- AI_PROVIDER=openai | claude | none
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os, json, time, hashlib, re, random
import requests
from bs4 import BeautifulSoup
from functools import wraps
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from dotenv import load_dotenv
import anthropic

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

try:
    from supabase import create_client as _sb_create
except Exception:
    _sb_create = None


load_dotenv()

app = Flask(__name__)
CORS(app)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY    = os.getenv("OPENAI_API_KEY", "")
SUPABASE_URL      = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY      = os.getenv("SUPABASE_KEY", "")

SCRAPER_API_KEY   = os.getenv("SCRAPER_API_KEY", "")
ZYTE_API_KEY      = os.getenv("ZYTE_API_KEY", "")

AI_PROVIDER = os.getenv("AI_PROVIDER", "openai").lower()
AI_MODEL_OPENAI = os.getenv("AI_MODEL_OPENAI", "gpt-4o-mini")
AI_MODEL_CLAUDE = os.getenv("AI_MODEL_CLAUDE", "claude-haiku-4-5-20251001")
AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "300"))

DAILY_FREE_LIMIT  = int(os.getenv("DAILY_FREE_LIMIT", "200"))
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "3600"))

# ── PRODUCT CLASSIFICATION KEYWORDS ──
ACCESSORY_KEYWORDS = [
    # English
    "case", "cover", "protector", "screen protector", "tempered glass",
    "cable", "charger", "adapter", "holder", "strap", "stand",
    "shell", "bumper", "sleeve", "pouch", "wallet case",
    "screen film", "glass film",
    # Lithuanian
    "dėklas", "etui", "plėvelė", "apsauginis stiklas", "kabelis",
    "kroviklis", "įkroviklis", "adapteris", "laikiklis", "dirželis",
    # German
    "hülle", "schutzglas", "schutzhülle", "ladekabel", "aufladekabel",
    # Polish
    "kabel", "ładowarka", "etui", "szkło",
]

MAIN_PRODUCT_KEYWORDS = [
    "iphone", "samsung galaxy", "macbook", "laptop", "notebook",
    "television", " tv ", "headphones", "earbuds", "airpods",
    "playstation", "xbox", "nintendo switch", "tablet", "ipad",
    "smartwatch", "camera", "monitor", "speaker", "soundbar",
    "refrigerator", "washing machine", "vacuum", "dyson",
]

# ── PRODUCT RELEVANCE MATCHING ──
_STOP_WORDS = {
    'the', 'a', 'an', 'for', 'with', 'and', 'or', 'in', 'of', 'to', 'on', 'at', 'by', 'is',
    'do', 'dla', 'mit', 'und', 'fur', 'von', 'zu', 'na', 'ze', 'po',
    'ne', 'su', 'be', 'ir', 'ar', 'tai', 'das', 'der', 'die', 'den',
}
_KNOWN_BRANDS = {
    'samsung', 'apple', 'sony', 'lg', 'xiaomi', 'huawei', 'lenovo', 'asus', 'acer',
    'hp', 'dell', 'microsoft', 'google', 'motorola', 'oneplus', 'realme', 'oppo',
    'dyson', 'philips', 'bosch', 'siemens', 'canon', 'nikon', 'bose', 'jbl', 'anker',
    'logitech', 'razer', 'corsair', 'kingston', 'seagate', 'wd', 'sandisk', 'intel',
    'amd', 'nvidia', 'panasonic', 'hitachi', 'toshiba', 'sharp', 'hisense', 'tcl',
}
_ACCESSORY_MATCH_WORDS = frozenset({
    'case', 'cover', 'sleeve', 'bumper', 'wallet', 'skin', 'sticker', 'decal',
    'holder', 'stand', 'mount', 'cradle', 'dock', 'bracket', 'grip',
    'charger', 'cable', 'adapter', 'hub', 'extender', 'splitter', 'dongle',
    'screen protector', 'tempered glass', 'film', 'foil',
    'replacement', 'spare', 'repair', 'filter', 'bag', 'brush', 'attachment',
    'earpad', 'eartip', 'ear tip', 'cushion', 'pad',
    'stylus', 'remote', 'controller',
    'dėklas', 'maišelis', 'rankinė', 'stovas', 'laikiklis',
    'kroviklis', 'kabelis', 'plėvelė', 'stikliukas', 'apsauga',
    'etui', 'obudowa', 'pokrowiec', 'ładowarka', 'kabel', 'szkło', 'folia',
    'uchwyt', 'podstawka', 'naklejka', 'ochraniacz', 'filtr',
    'hülle', 'tasche', 'schutzhülle', 'ladegerät', 'halterung', 'schutzglas',
    'ersatz', 'zubehör',
})
_VARIANT_WORDS = frozenset({
    'pro', 'max', 'ultra', 'plus', 'lite', 'mini', 'fe', 'edge',
    'note', 'fold', 'flip', 'air', 'neo', 'active', 'sport',
})


def _norm_units(text):
    return re.sub(
        r'(\d+)\s+(gb|tb|mb|mp|mah|hz|mhz|ghz)\b',
        lambda m: m.group(1) + m.group(2),
        text.lower()
    )


def is_relevant_result(query: str, product_title: str) -> bool:
    if not product_title or not query:
        return True
    q = _norm_units(query)
    t = _norm_units(product_title)
    for acc in _ACCESSORY_MATCH_WORDS:
        if acc in t and acc not in q:
            return False
    for brand in [b for b in _KNOWN_BRANDS if b in q]:
        if brand not in t:
            return False
    q_tok = set(re.findall(r'[a-z0-9]+', q))
    t_tok = set(re.findall(r'[a-z0-9]+', t))
    for variant in _VARIANT_WORDS:
        if variant in q_tok and variant not in t_tok:
            return False
    model_tokens = re.findall(r'\b[a-z]*\d+[a-z0-9-]*\b', q)
    if model_tokens:
        if not all(m in t for m in model_tokens):
            return False
    q_words = [w for w in re.findall(r'[a-z0-9]{2,}', q) if w not in _STOP_WORDS]
    t_words = set(re.findall(r'[a-z0-9]{2,}', t))
    if not q_words:
        return True
    overlap = sum(1 for w in q_words if w in t_words)
    ratio = overlap / len(q_words)
    if len(q_words) <= 2:
        return ratio >= 1.0
    return ratio >= 0.55


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


# ── FREE BARCODE LOOKUP ──
def lookup_barcode_free(barcode: str) -> str:
    """Looks up product name from EAN/UPC barcode using free APIs. Returns empty string if not found."""
    barcode = barcode.strip()
    if not re.match(r'^\d{8,14}$', barcode):
        return ""

    # Open Food Facts (works best for food/grocery products)
    try:
        resp = requests.get(
            f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json",
            timeout=5,
            headers={"User-Agent": "GoodyApp/1.0 (price comparison)"},
        )
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == 1:
                p = data.get("product", {})
                name = (
                    p.get("product_name_en")
                    or p.get("product_name")
                    or p.get("generic_name")
                    or ""
                ).strip()
                if name:
                    brand = p.get("brands", "").split(",")[0].strip()
                    return f"{brand} {name}".strip() if brand and brand.lower() not in name.lower() else name
    except Exception as e:
        print(f"[OpenFoodFacts] {e}")

    # Open Product Data (UPCItemDB trial — free, limited)
    try:
        resp = requests.get(
            f"https://api.upcitemdb.com/prod/trial/lookup?upc={barcode}",
            timeout=5,
            headers={"User-Agent": "GoodyApp/1.0"},
        )
        if resp.status_code == 200:
            items = resp.json().get("items", [])
            if items:
                return items[0].get("title", "").strip()
    except Exception as e:
        print(f"[UPCItemDB] {e}")

    return ""


# ── CHEAP PRODUCT TYPE CLASSIFICATION ──
def classify_product_cheap(product_name: str, price: float = 0.0) -> str:
    """Returns 'MAIN' or 'ACCESSORY'. Uses free heuristics first, GPT-4o-mini only as last resort."""
    name_lower = product_name.lower()

    # Step 1: keyword match (free)
    if any(kw in name_lower for kw in ACCESSORY_KEYWORDS):
        return "ACCESSORY"
    if any(kw in name_lower for kw in MAIN_PRODUCT_KEYWORDS):
        return "MAIN"

    # Step 2: price range (free)
    if 0 < price < 30:
        return "ACCESSORY"
    if price > 150:
        return "MAIN"

    # Step 3: GPT-4o-mini text-only (< $0.0001 per call)
    if OPENAI_API_KEY and OpenAI:
        try:
            client = OpenAI(api_key=OPENAI_API_KEY)
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": f'Is "{product_name}" a main product or accessory? Reply: MAIN or ACCESSORY'
                }],
                max_tokens=5,
                temperature=0,
            )
            answer = resp.choices[0].message.content.strip().upper()
            if "ACCESSORY" in answer:
                return "ACCESSORY"
        except Exception as e:
            print(f"[classify] {e}")

    return "MAIN"


# ── SUPABASE PRICE HISTORY ──
_sb_client = None

def get_supabase():
    global _sb_client
    if _sb_client is None and SUPABASE_URL and SUPABASE_KEY and _sb_create:
        try:
            _sb_client = _sb_create(SUPABASE_URL, SUPABASE_KEY)
        except Exception as e:
            print(f"[Supabase init] {e}")
    return _sb_client


def save_prices_to_supabase(product_name: str, results: list):
    """Fire-and-forget: saves current search prices to Supabase. Non-blocking."""
    sb = get_supabase()
    if not sb:
        return
    try:
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        rows = [
            {
                "product_name": product_name.lower().strip(),
                "shop": r.get("shop", ""),
                "price": r.get("price", 0),
                "currency": r.get("currency", "EUR"),
                "checked_at": now,
            }
            for r in results
            if r.get("price", 0) > 0 and not (
                r.get("source") == "scan" or "scanned" in r.get("shop", "").lower()
            )
        ]
        if rows:
            sb.table("price_history").insert(rows).execute()
            print(f"[Supabase] saved {len(rows)} rows for '{product_name}'")
    except Exception as e:
        print(f"[Supabase save] {e}")


def fetch_price_history_from_supabase(product_name: str) -> list:
    """Returns last 90 days of price rows for a product."""
    sb = get_supabase()
    if not sb:
        return []
    try:
        resp = (
            sb.table("price_history")
            .select("shop, price, currency, checked_at")
            .eq("product_name", product_name.lower().strip())
            .order("checked_at", desc=False)
            .limit(500)
            .execute()
        )
        return resp.data or []
    except Exception as e:
        print(f"[Supabase history] {e}")
        return []


def fetch_url(url: str, lang: str = "lt", timeout: int = 10, scraper_timeout: int = 15):
    """Fetch URL — Zyte API pirma, tada ScraperAPI, tada tiesiogiai."""
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
                + ("&premium=true" if is_amazon else "")
            )
            resp = requests.get(scraper_url, timeout=scraper_timeout)
            if resp.status_code == 200:
                print(f"[ScraperAPI OK] {url[:70]}")
                return resp

            print(f"[ScraperAPI {resp.status_code}] fallback → direct")
        except Exception as e:
            print(f"[ScraperAPI err] {e}")

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
            reset_time = time.strftime("%Y-%m-%dT00:00:00Z", time.gmtime(
                time.mktime(time.strptime(time.strftime("%Y-%m-%d"), "%Y-%m-%d")) + 86400
            ))
            return jsonify({
                "error": "daily_limit",
                "message": f"Pasiektas dienos paieškų limitas ({DAILY_FREE_LIMIT}). Limitas atsinaujins rytoj.",
                "remaining": 0,
                "resets_at": reset_time
            }), 429

        return f(*args, **kwargs)

    return decorated


def get_fx_rates() -> dict:
    if time.time() - _fx_cache["ts"] < 21600:
        return _fx_cache["rates"]

    try:
        resp = requests.get("https://api.exchangerate-api.com/v4/latest/EUR", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            _fx_cache["rates"] = {
                k: round(1 / v, 6)
                for k, v in data.get("rates", {}).items()
                if v > 0
            }
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

    text = (text.replace("\xa0", " ").replace("€", "").replace("Eur", "").replace("EUR", "")
                .replace("zł", "").replace("zl", "").replace("PLN", "").replace(" ", "").strip())

    if "," in text and "." in text:
        if text.rfind(".") < text.rfind(","):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    elif "," in text:
        text = text.replace(",", ".")

    m = re.search(r"\d+\.?\d*", text)

    if m:
        try:
            val = float(m.group())
            if 0 < val < 100000:
                return val
        except Exception:
            pass

    return 0.0


def deduplicate_by_shop(results: list) -> list:
    """Viena parduotuvė = vienas pigiausias rezultatas."""
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
                    item.select_one("h2") or
                    item.select_one("h3")
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
            print("[Pigu] failed")
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
                    item.select_one("h2") or
                    item.select_one("h3") or
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
            print("[Senukai] failed")
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
                    item.select_one("h2") or
                    item.select_one("h3")
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
            print("[Topo] failed")
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
                    item.select_one("h2") or
                    item.select_one("h3")
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
            print("[Elesen] failed")
            return results

        soup = BeautifulSoup(resp.text, "html.parser")

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

                price_text = price_el.get_text()
                price = parse_price(price_text)

                if not price:
                    continue

                # Elesen rodo kainas centais be dešimtainio skyriklio (pvz. "28999" = 289.99€)
                clean = price_text.replace("\xa0", " ").replace("€", "").replace("Eur", "").strip()
                if "," not in clean and "." not in clean and price == int(price):
                    price = round(price / 100, 2)

                name_el = (
                    item.select_one("[class*='name']") or
                    item.select_one("h2") or
                    item.select_one("h3")
                )


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
            print("[1a] failed")
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

                name_el = (
                    item.select_one("[class*='name']") or
                    item.select_one("h2") or
                    item.select_one("h3")
                )

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
        url = f"https://www.amazon.{domain}/s?k={requests.utils.quote(query)}"
        resp = fetch_url(url, lang, scraper_timeout=35)

        if not resp or resp.status_code != 200:
            print(f"[Amazon.{domain}] failed status={resp.status_code if resp else 'none'}")
            return results

        soup = BeautifulSoup(resp.text, "html.parser")

        items = (
            soup.select('[data-component-type="s-search-result"]') or
            soup.select('div[data-asin][data-index]') or
            soup.select('div[data-asin]:not([data-asin=""])')
        )

        print(f"[Amazon.{domain}] {len(items)} items (html_len={len(resp.text)})")

        if len(items) == 0:
            if "captcha" in resp.text.lower() or "robot" in resp.text.lower():
                print(f"[Amazon.{domain}] CAPTCHA detected!")
            else:
                snippet = resp.text[5000:6000] if len(resp.text) > 5000 else resp.text
                print(f"[Amazon.{domain}] No items. Body snippet: {snippet[:300]}")

        for item in items[:5]:
            try:
                h2_el = item.select_one("h2")
                name = ""

                if h2_el:
                    name = h2_el.get("aria-label", "") or ""

                    if not name:
                        span = h2_el.select_one("span")
                        name = span.get_text(strip=True) if span else h2_el.get_text(strip=True)

                if not name:
                    continue

                name = name[:100]

                raw = 0.0
                price_el = item.select_one(".a-price .a-offscreen")

                if price_el:
                    raw = parse_price(price_el.get_text())

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

                link_el = h2_el.parent if h2_el and h2_el.parent.name == "a" else item.select_one("a[href*='/dp/']")
                href = link_el["href"] if link_el else ""
                link = f"https://www.amazon.{domain}{href}" if href.startswith("/") else href

                asin_m = re.search(r"/dp/([A-Z0-9]{10})", link)
                asin = asin_m.group(1) if asin_m else ""

                aff = (
                    f"https://www.amazon.{domain}/dp/{asin}?tag=goody-21"
                    if asin
                    else f"https://www.amazon.{domain}/s?k={requests.utils.quote(query)}"
                )

                rating = 0
                rating_el = item.select_one(".a-icon-alt")

                if rating_el:
                    m = re.search(r"([\d,]+)", rating_el.get_text())

                    if m:
                        try:
                            rating = float(m.group(1).replace(",", "."))
                        except Exception:
                            pass

                review_count = 0
                rev_el = item.select_one(".a-size-base.s-underline-text")

                if rev_el:
                    m = re.search(r"\d+", rev_el.get_text().replace(".", "").replace(",", ""))

                    if m:
                        try:
                            review_count = int(m.group())
                        except Exception:
                            pass

                prime = bool(item.select_one(".a-icon-prime"))
                orig_note = f"{raw:.0f} {currency}" if currency != "EUR" else ""

                results.append({
                    "shop": f"Amazon.{domain.upper()}",
                    "flag": "🌍" if domain == "de" else "🇵🇱",
                    "url": link,
                    "affiliate_url": aff,
                    "price": price,
                    "currency": "EUR",
                    "original_price": raw if currency != "EUR" else None,
                    "original_currency": currency if currency != "EUR" else None,
                    "in_stock": True,
                    "delivery": "Prime · Tomorrow" if prime else "2-5 d.",
                    "deal_score": 75,
                    "rating": rating,
                    "review_count": review_count,
                    "notes": " · ".join(filter(None, ["Prime" if prime else "", orig_note])),
                    "is_best_value": False,
                    "is_cheapest": False,
                    "is_top_rated": False,
                    "why_recommended": "",
                    "source": f"amazon.{domain}",
                    "product_title": name[:80]
                })
            except Exception as e:
                print(f"[Amazon.{domain} item] {e}")

    except Exception as e:
        print(f"[Amazon.{domain}] {e}")

    return results


def _make_result(shop, flag, link, price, name, source):
    return {
        "shop": shop,
        "flag": flag,
        "url": link,
        "affiliate_url": link,
        "price": price,
        "currency": "EUR",
        "in_stock": True,
        "delivery": "1-3 d.",
        "deal_score": 70,
        "rating": 0,
        "review_count": 0,
        "notes": "",
        "is_best_value": False,
        "is_cheapest": False,
        "is_top_rated": False,
        "why_recommended": "",
        "source": source,
        "product_title": name
    }


# ── CLAUDE TRANSLATION / VISION ──
def claude_translate(query: str, target_lang: str = "en") -> str:
    if not ANTHROPIC_API_KEY:
        return query

    common = [
        "iphone", "samsung", "sony", "apple", "lg",
        "xiaomi", "dyson", "macbook", "huawei", "lenovo"
    ]

    if any(w in query.lower() for w in common) and target_lang == "en":
        return query

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        lang_names = {
            "en": "English",
            "de": "German",
            "pl": "Polish",
            "lt": "Lithuanian"
        }

        resp = client.messages.create(
            model=AI_MODEL_CLAUDE,
            max_tokens=60,
            messages=[
                {
                    "role": "user",
                    "content": f'Translate to {lang_names.get(target_lang, "English")} for e-commerce search. Return ONLY the product name: "{query}"'
                }
            ]
        )

        result = "".join(
            b.text for b in resp.content if hasattr(b, "text")
        ).strip().strip('"')

        return result if result else query

    except Exception:
        return query


# ── AI ANALYSIS ENGINE ──
def empty_ai():
    return {
        "verdict": "OK",
        "verdict_label": "Normal",
        "verdict_reason": "",
        "ai_summary": "",
        "alternative": "",
        "buy_recommendation": "",
        "price_forecast": ""
    }


def rule_based_ai_analyze(query: str, results: list, price_history: dict = None) -> dict:
    if not results:
        return {
            "verdict": "WAIT",
            "verdict_label": "Not found",
            "verdict_reason": "No prices found.",
            "ai_summary": "Try a more specific product name.",
            "alternative": "",
            "buy_recommendation": "Refine your search.",
            "price_forecast": ""
        }

    prices = [r.get("price", 0) for r in results if r.get("price", 0) > 0]

    if not prices:
        return empty_ai()

    price_min = min(prices)
    price_max = max(prices)
    price_avg = round(sum(prices) / len(prices), 2)
    spread_pct = ((price_max - price_min) / price_max * 100) if price_max else 0

    if len(prices) == 1:
        verdict = "OK"
        label = "Normal"
        reason = "Only one valid price was found, so comparison confidence is limited."
    elif spread_pct >= 20:
        verdict = "BUY"
        label = "Buy now"
        reason = f"The cheapest offer is about {spread_pct:.0f}% below the highest found price."
    elif price_min > price_avg * 0.97:
        verdict = "WAIT"
        label = "Wait"
        reason = "The best price is close to the current market average."
    else:
        verdict = "OK"
        label = "Normal"
        reason = "The current price looks reasonable, but not exceptional."

    return {
        "verdict": verdict,
        "verdict_label": label,
        "verdict_reason": reason,
        "ai_summary": f"Goody found {len(prices)} valid price point(s). Lowest price: €{price_min:.2f}, average: €{price_avg:.2f}.",
        "alternative": "",
        "buy_recommendation": f"Best found price is €{price_min:.2f}. Compare delivery and seller reliability before buying.",
        "price_forecast": "No strong price history signal available."
    }


def build_ai_prompt(query: str, results: list, price_history: dict = None) -> str:
    clean_results = []

    for r in results[:8]:
        if r.get("price", 0) > 0:
            clean_results.append({
                "shop": r.get("shop", ""),
                "price": r.get("price", 0),
                "rating": r.get("rating", 0),
                "delivery": r.get("delivery", ""),
                "title": r.get("product_title", r.get("name", ""))[:120]
            })

    prices = [r["price"] for r in clean_results if r.get("price", 0) > 0]

    payload = {
        "query": query,
        "results": clean_results,
        "price_stats": {
            "min": min(prices) if prices else 0,
            "max": max(prices) if prices else 0,
            "avg": round(sum(prices) / len(prices), 2) if prices else 0,
            "count": len(prices)
        },
        "price_history": price_history or {}
    }

    return f"""
You are Goody's AI Shopping Coach.

You DO NOT search the web.
You DO NOT browse.
You DO NOT call external URLs.
You DO NOT invent prices, shops, stock status or discounts.
You ONLY analyze the structured data provided by Goody.

Data:
{json.dumps(payload, ensure_ascii=False)}

Return ONLY valid JSON, no markdown:
{{
  "verdict": "BUY|WAIT|SKIP|OK",
  "verdict_label": "Buy now|Wait|Avoid|Normal",
  "verdict_reason": "one short sentence",
  "ai_summary": "1-2 short sentences explaining the deal",
  "alternative": "short alternative suggestion if overpriced, otherwise empty string",
  "buy_recommendation": "specific buying advice in 1-2 sentences",
  "price_forecast": "short price outlook based only on available data"
}}
""".strip()


def openai_analyze(query: str, results: list, price_history: dict = None) -> dict:
    if not OPENAI_API_KEY or OpenAI is None or not results:
        return rule_based_ai_analyze(query, results, price_history)

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        prompt = build_ai_prompt(query, results, price_history)

        resp = client.chat.completions.create(
            model=AI_MODEL_OPENAI,
            messages=[
                {
                    "role": "system",
                    "content": "You are Goody's AI deal analyst. Return strict JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=AI_MAX_TOKENS,
            response_format={"type": "json_object"}
        )

        text = resp.choices[0].message.content.strip()
        return json.loads(text)

    except Exception as e:
        print(f"[OpenAI analyze] {e}")
        return rule_based_ai_analyze(query, results, price_history)


def claude_analyze(query: str, results: list, price_history: dict = None) -> dict:
    if not ANTHROPIC_API_KEY or not results:
        return rule_based_ai_analyze(query, results, price_history)

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        prompt = build_ai_prompt(query, results, price_history)

        resp = client.messages.create(
            model=AI_MODEL_CLAUDE,
            max_tokens=AI_MAX_TOKENS,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        text = "".join(
            b.text for b in resp.content if hasattr(b, "text")
        ).strip()

        text = text.replace("```json", "").replace("```", "").strip()

        return json.loads(text)

    except Exception as e:
        print(f"[Claude analyze] {e}")
        return rule_based_ai_analyze(query, results, price_history)


def analyze_deal_with_ai(query: str, results: list, price_history: dict = None) -> dict:
    """
    Claude:
    - coding / architecture externally
    - translation
    - image scan
    - optional fallback runtime AI

    OpenAI:
    - main runtime analysis
    - structured JSON
    - AI Shopping Coach
    - deal scoring explanation
    """

    if AI_PROVIDER == "openai":
        return openai_analyze(query, results, price_history)

    if AI_PROVIDER == "claude":
        return claude_analyze(query, results, price_history)

    return rule_based_ai_analyze(query, results, price_history)


def get_price_history(query: str) -> dict:
    try:
        resp = fetch_url(
            f"https://camelcamelcamel.com/search?sq={requests.utils.quote(query)}",
            "en"
        )

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
    results = deduplicate_by_shop(results)
    results = [r for r in results if r.get("price", 0) > 0]
    filtered = [r for r in results if is_relevant_result(query, r.get("product_title", ""))]
    if filtered:
        results = filtered

    if not results:
        return {
            "product_name": query,
            "ai_verdict": "WAIT",
            "verdict_label": "Not found",
            "verdict_reason": "No prices found.",
            "ai_summary": "Try a more specific product name.",
            "buy_recommendation": "Refine your search.",
            "alternative": "",
            "price_forecast": "",
            "deal_score": 0,
            "price_min": 0,
            "price_max": 0,
            "price_avg": 0,
            "price_history": price_history or {},
            "results": []
        }

    results.sort(key=lambda x: x.get("price", 999999))

    prices = [r["price"] for r in results]
    price_min, price_max = min(prices), max(prices)
    price_avg = round(sum(prices) / len(prices), 2)

    results[0]["is_cheapest"] = True

    rated = [r for r in results if r.get("rating", 0) > 0]

    if rated:
        max(rated, key=lambda r: r.get("rating", 0))["is_top_rated"] = True

    results[
        max(
            range(len(results)),
            key=lambda i: results[i].get("deal_score", 0)
        )
    ]["is_best_value"] = True

    ai = ai_data or {}
    savings_pct = ((price_max - price_min) / price_max * 100) if price_max > 0 else 0
    deal_score = min(100, int(savings_pct * 1.5 + 50))

    return {
        "product_name": query,
        "ai_verdict": ai.get("verdict", "OK"),
        "verdict_label": ai.get("verdict_label", "Normal"),
        "verdict_reason": ai.get("verdict_reason", ""),
        "ai_summary": ai.get("ai_summary", ""),
        "buy_recommendation": ai.get(
            "buy_recommendation",
            f"Best price found: €{price_min:.2f}"
        ),
        "alternative": ai.get("alternative", ""),
        "price_forecast": ai.get("price_forecast", ""),
        "deal_score": deal_score,
        "price_min": price_min,
        "price_max": price_max,
        "price_avg": price_avg,
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

    # Barcode detection — free lookup before any AI
    original_query = query
    if re.match(r'^\d{8,14}$', query):
        product_from_barcode = lookup_barcode_free(query)
        if product_from_barcode:
            print(f"[Barcode] {query} → {product_from_barcode}")
            query = product_from_barcode

    cache_key = hashlib.md5(f"v59:{query.lower()}".encode()).hexdigest()
    cached = get_cache(cache_key)

    if cached:
        cached["_cached"] = True
        return jsonify(cached)

    try:
        query_de = claude_translate(query, "de")
    except Exception:
        query_de = query

    try:
        query_pl = claude_translate(query, "pl")
    except Exception:
        query_pl = query

    print(f"\n=== SEARCH: '{original_query}' → resolved:'{query}' DE:'{query_de}' PL:'{query_pl}' ===")

    all_results = []

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {
            executor.submit(scrape_varle,   query):          "Varle",
            executor.submit(scrape_pigu,    query):          "Pigu",
            executor.submit(scrape_1a,      query):          "1a",
            executor.submit(scrape_senukai, query):          "Senukai",
            executor.submit(scrape_topo,    query):          "Topo",
            executor.submit(scrape_elesen,  query):          "Elesen",
            executor.submit(scrape_amazon,  query_de, "de"): "Amazon.DE",
            executor.submit(scrape_amazon,  query_pl, "pl"): "Amazon.PL",
        }

        for f in as_completed(futures, timeout=45):
            name = futures[f]

            try:
                res = f.result(timeout=5)
                print(f"  [{name}] returned {len(res)} results")
                all_results.extend(res)
            except Exception as e:
                print(f"  [{name}] error: {e}")

    print(f"=== TOTAL: {len(all_results)} results before dedup/filter ===\n")

    price_history = {}

    try:
        with ThreadPoolExecutor(max_workers=1) as phex:
            phf = phex.submit(get_price_history, query)
            price_history = phf.result(timeout=8)
    except Exception:
        pass

    ai_data = analyze_deal_with_ai(query, all_results, price_history)
    result = post_process(all_results, query, ai_data, price_history)

    price_for_classify = result.get("price_min", 0)
    result["product_type"] = classify_product_cheap(query, price_for_classify)

    set_cache(cache_key, result)

    threading.Thread(target=save_prices_to_supabase, args=(query, all_results), daemon=True).start()

    ip = request.remote_addr or "unknown"
    used = rate_store.get(ip, {}).get("count", 1)

    result["_rate"] = {
        "used": used,
        "limit": DAILY_FREE_LIMIT,
        "remaining": max(0, DAILY_FREE_LIMIT - used)
    }

    return jsonify(result)


@app.route("/api/price-history", methods=["GET"])
def price_history_endpoint():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"error": "q required"}), 400

    if not (SUPABASE_URL and SUPABASE_KEY):
        return jsonify({"error": "Supabase not configured", "history": []}), 200

    rows = fetch_price_history_from_supabase(q)

    # Group by date and shop for frontend charting
    by_date: dict = {}
    shops: set = set()
    for row in rows:
        ts = row.get("checked_at", "")
        day = ts[:10] if ts else ""
        shop = row.get("shop", "")
        price = float(row.get("price", 0))
        if day and shop and price > 0:
            shops.add(shop)
            by_date.setdefault(day, {})[shop] = min(
                by_date[day].get(shop, price), price
            )

    sorted_days = sorted(by_date.keys())
    shop_list = sorted(shops)

    datasets = []
    for shop in shop_list:
        datasets.append({
            "shop": shop,
            "prices": [by_date[day].get(shop) for day in sorted_days],
        })

    return jsonify({
        "product_name": q,
        "labels": sorted_days,
        "datasets": datasets,
        "raw": rows[-100:],
    })


@app.route("/api/classify", methods=["POST"])
def classify_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400
    product_name = (data.get("product_name") or data.get("query") or "").strip()
    if not product_name:
        return jsonify({"error": "product_name required"}), 400
    price = float(data.get("price") or 0)
    product_type = classify_product_cheap(product_name, price)
    return jsonify({"product_name": product_name, "product_type": product_type})


@app.route("/api/barcode", methods=["POST"])
def barcode_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400
    barcode = (data.get("barcode") or "").strip()
    if not barcode:
        return jsonify({"error": "barcode required"}), 400
    product_name = lookup_barcode_free(barcode)
    if product_name:
        return jsonify({"barcode": barcode, "product_name": product_name, "source": "open_food_facts"})
    return jsonify({"barcode": barcode, "product_name": "", "source": "not_found"}), 404


@app.route("/api/scan-image", methods=["POST"])
@rate_limit
def scan_image():
    data = request.get_json()

    if not data or "image" not in data:
        return jsonify({"error": "No image"}), 400

    if not ANTHROPIC_API_KEY:
        return jsonify({
            "error": "scan_unavailable",
            "message": "Nuotraukų nuskaitymas neprieinamas. Prašome susisiekti su palaikymu."
        }), 503

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        response = client.messages.create(
            model=AI_MODEL_CLAUDE,
            max_tokens=256,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": data["image"]
                            }
                        },
                        {
                            "type": "text",
                            "text": """Analyze this image. Find the product and any visible price.

Respond ONLY with JSON (no markdown):
{"product_name":"BRAND MODEL in English","price_visible":0,"barcode":"","confidence":"high/medium/low"}

Rules:
- product_name: brand + model in English (e.g. "Apple iPhone 16 Pro", "Sony WH-1000XM5")
- price_visible: numeric price in EUR if visible, else 0
- confidence: high=exact model, medium=brand+category, low=category only"""
                        }
                    ]
                }
            ]
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
        except Exception:
            name_m = re.search(r'"product_name"\s*:\s*"([^"]+)"', raw_text)
            vision = {
                "product_name": name_m.group(1) if name_m else "",
                "price_visible": 0,
                "barcode": "",
                "confidence": "low"
            }

        product_name = vision.get("product_name", "").strip()
        price_visible = vision.get("price_visible", 0)
        confidence = vision.get("confidence", "medium")

        if isinstance(price_visible, (int, float)) and price_visible <= 1:
            price_visible = 0

        if not product_name or (confidence == "low" and len(product_name) < 4):
            return jsonify({
                "error": "product_not_recognized",
                "message": "Produktas neatpažintas. Pabandykite nufotografuoti arčiau, su geresniu apšvietimu arba įveskite pavadinimą rankiniu būdu.",
                "confidence": confidence
            }), 422

        cache_key = hashlib.md5(f"scan_v59:{product_name.lower()}".encode()).hexdigest()
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

        try:
            query_pl = claude_translate(product_name, "pl")
        except Exception:
            query_pl = product_name

        all_results = []

        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {
                executor.submit(scrape_varle,   product_name):    "Varle",
                executor.submit(scrape_pigu,    product_name):    "Pigu",
                executor.submit(scrape_1a,      product_name):    "1a",
                executor.submit(scrape_senukai, product_name):    "Senukai",
                executor.submit(scrape_topo,    product_name):    "Topo",
                executor.submit(scrape_elesen,  product_name):    "Elesen",
                executor.submit(scrape_amazon,  query_de, "de"):  "Amazon.DE",
                executor.submit(scrape_amazon,  query_pl, "pl"):  "Amazon.PL",
            }

            for f in as_completed(futures, timeout=45):
                try:
                    all_results.extend(f.result(timeout=5))
                except Exception as e:
                    print(f"[Scan parallel] {e}")

        if isinstance(price_visible, (int, float)) and price_visible > 1:
            all_results.insert(0, {
                "shop": "Scanned price",
                "flag": "📷",
                "url": "",
                "affiliate_url": "",
                "price": price_visible,
                "currency": "EUR",
                "in_stock": True,
                "delivery": "In store",
                "deal_score": 50,
                "rating": 0,
                "review_count": 0,
                "notes": "Price from your photo",
                "is_best_value": False,
                "is_cheapest": False,
                "is_top_rated": False,
                "why_recommended": "",
                "source": "scan",
                "product_title": product_name
            })

        price_history = {}

        try:
            with ThreadPoolExecutor(max_workers=1) as phex:
                phf = phex.submit(get_price_history, product_name)
                price_history = phf.result(timeout=8)
        except Exception:
            pass

        ai_data = analyze_deal_with_ai(product_name, all_results, price_history)
        result = post_process(all_results, product_name, ai_data, price_history)

        result["scanned_product"] = product_name
        result["store_price"] = (
            price_visible
            if isinstance(price_visible, (int, float)) and price_visible > 1
            else 0
        )
        result["product_type"] = classify_product_cheap(
            product_name,
            price_visible if isinstance(price_visible, (int, float)) and price_visible > 1 else result.get("price_min", 0)
        )

        set_cache(cache_key, result)

        ip = request.remote_addr or "unknown"
        used = rate_store.get(ip, {}).get("count", 1)

        result["_rate"] = {
            "used": used,
            "limit": DAILY_FREE_LIMIT,
            "remaining": max(0, DAILY_FREE_LIMIT - used)
        }

        return jsonify(result)

    except Exception as e:
        print(f"[scan_image] {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/debug-html", methods=["GET"])
def debug_html():
    shop = request.args.get("shop", "varle")
    query = request.args.get("q", "Samsung Galaxy S24")

    urls = {
        "varle": f"https://varle.lt/search/?q={requests.utils.quote(query)}",
        "pigu": f"https://pigu.lt/lt/search?query={requests.utils.quote(query)}",
        "1a": f"https://www.1a.lt/search?q={requests.utils.quote(query)}",
        "senukai": f"https://www.senukai.lt/paieska?q={requests.utils.quote(query)}",
        "topo":      f"https://www.topocentras.lt/search?q={requests.utils.quote(query)}",
        "elesen":    f"https://www.elesen.lt/paieska?q={requests.utils.quote(query)}",
        "amazon":    f"https://www.amazon.de/s?k={requests.utils.quote(query)}",
        "amazon.pl": f"https://www.amazon.pl/s?k={requests.utils.quote(query)}",
    }

    url = urls.get(shop, urls["varle"])

    is_amazon = shop in ("amazon", "amazon.pl")
    debug_lang = "pl" if shop == "amazon.pl" else ("de" if shop == "amazon" else "lt")
    debug_scraper_timeout = 35 if is_amazon else 15


    resp = fetch_url(url, debug_lang, scraper_timeout=debug_scraper_timeout)

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

        if any(c in txt for c in ["€", "Eur", "EUR"]) or re.search(r'\d{2,}[.,]\d{2}', txt):
            prices_found.append(txt[:50])

    data_asin_els = soup.find_all(attrs={"data-asin": True})
    data_asin_nonempty = [e for e in data_asin_els if e.get("data-asin")]
    comp_type_els = soup.find_all(attrs={"data-component-type": "s-search-result"})

    return jsonify({
        "url": url,
        "status": resp.status_code,
        "html_len": len(resp.text),
        "data_asin_count": len(data_asin_nonempty),
        "data_component_type_count": len(comp_type_els),
        "html_head": resp.text[:3000],
        "html_body": resp.text[5000:9000],
        "all_classes": sorted(list(classes))[:150],
        "prices_found": prices_found[:20],
    })


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "version": "5.10-all-shops",
        "supabase_configured": bool(SUPABASE_URL and SUPABASE_KEY),
        "shops": ["Varle.lt", "Pigu.lt", "1a.lt", "Senukai.lt", "Topo centras", "Elesen.lt", "Amazon.DE", "Amazon.PL"],
        "scraper_api": bool(SCRAPER_API_KEY),
        "zyte_configured": bool(ZYTE_API_KEY),
        "anthropic_configured": bool(ANTHROPIC_API_KEY),
        "openai_configured": bool(OPENAI_API_KEY),
        "ai_provider": AI_PROVIDER,
        "ai_model_openai": AI_MODEL_OPENAI,
        "ai_model_claude": AI_MODEL_CLAUDE,
        "cache_entries": len(cache)
    })


@app.route("/api/rate-limit", methods=["GET"])
def rate_limit_status():
    ip = request.remote_addr or "unknown"
    today = time.strftime("%Y-%m-%d")

    used = (
        rate_store.get(ip, {}).get("count", 0)
        if rate_store.get(ip, {}).get("date") == today
        else 0
    )

    return jsonify({
        "used": used,
        "limit": DAILY_FREE_LIMIT,
        "remaining": max(0, DAILY_FREE_LIMIT - used)
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))

    print("\n🟢 Goody API v5.10")
    print(f"📊 Supabase: {'✅ configured' if SUPABASE_URL else '⚠️ not set'}")
    print("📦 Shops: Varle + Pigu + 1a + Senukai + Topo + Elesen + Amazon.DE + Amazon.PL")
    print(f"🔑 ScraperAPI: {'✅ configured' if SCRAPER_API_KEY else '⚠️ not set'}")
    print(f"🔑 Zyte: {'✅ configured' if ZYTE_API_KEY else '⚠️ not set'}")
    print(f"🤖 Anthropic: {'✅ configured' if ANTHROPIC_API_KEY else '❌ missing'}")
    print(f"🤖 OpenAI: {'✅ configured' if OPENAI_API_KEY else '❌ missing'}")
    print(f"🧠 AI provider: {AI_PROVIDER}")
    print(f"🧠 OpenAI model: {AI_MODEL_OPENAI}")

    app.run(host="0.0.0.0", port=port, debug=False)
