"""
Goody Backend v5.55 — translation coverage fix + new LT vocab + Amazon price fallback:
- _LT_CATEGORY_WORDS: added blenderis/fotoaparatas/garsiakalbis (were in dicts but not
  in the category-word trigger list → Amazon got untranslated LT queries → 0 results)
- New LT translation pairs: nešiojamas/belaidis/tosteris/grilis/kavos kapsulės + more
- Amazon scraper: .a-price-whole/.a-price-fraction fallback when .a-offscreen missing
- AI_MAX_TOKENS default: 200 → 150 (saves ~25% tokens; response fits comfortably in 150)
- v5.54: SSE price history parallel fetch, Amazon rating-based deal_score
- v5.53: validate_price floors (dishwasher/freezer/laptop/aircon), 90-day Supabase
"""

from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import os, json, time, hashlib, re, random
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
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

# Shared HTTP session with connection pooling — reuses TCP/TLS for same hosts.
# pool_connections=10 covers 4 shop domains + APIs; pool_maxsize=20 for parallel scrapes.
_http = requests.Session()
_http_retry = Retry(total=1, connect=1, backoff_factor=0.2, status_forcelist=[502, 503, 504])
_http.mount("https://", HTTPAdapter(pool_connections=10, pool_maxsize=20, max_retries=_http_retry))
_http.mount("http://",  HTTPAdapter(pool_connections=4,  pool_maxsize=8,  max_retries=_http_retry))

app = Flask(__name__)
_ALLOWED_ORIGINS = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "*").split(",") if o.strip()]
CORS(app, origins=_ALLOWED_ORIGINS if "*" not in _ALLOWED_ORIGINS else "*")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY    = os.getenv("OPENAI_API_KEY", "")
SUPABASE_URL      = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY      = os.getenv("SUPABASE_KEY", "")

SCRAPER_API_KEY   = os.getenv("SCRAPER_API_KEY", "")
ZYTE_API_KEY      = os.getenv("ZYTE_API_KEY", "")

AI_PROVIDER = os.getenv("AI_PROVIDER", "openai").lower()
AI_MODEL_OPENAI = os.getenv("AI_MODEL_OPENAI", "gpt-4o-mini")
AI_MODEL_CLAUDE = os.getenv("AI_MODEL_CLAUDE", "claude-haiku-4-5-20251001")
AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "150"))

DAILY_FREE_LIMIT    = int(os.getenv("DAILY_FREE_LIMIT", "200"))
CACHE_TTL_SECONDS   = int(os.getenv("CACHE_TTL_SECONDS", "1800"))   # 30 min default
POPULAR_CACHE_TTL   = int(os.getenv("POPULAR_CACHE_TTL", "7200"))   # 2 h for popular
POPULAR_THRESHOLD   = int(os.getenv("POPULAR_THRESHOLD", "5"))       # min searches to be "popular"
SHOP_TIMEOUT        = int(os.getenv("SHOP_TIMEOUT", "5"))            # seconds per shop
DEBUG_API_KEY       = os.getenv("DEBUG_API_KEY", "")
VARLE_AFFILIATE_TAG   = os.getenv("VARLE_AFFILIATE_TAG", "")          # e.g. "goody" → ?ref=goody
AMAZON_AFFILIATE_TAG  = os.getenv("AMAZON_AFFILIATE_TAG", "goody-21") # Amazon Associates tag

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
    # Lithuanian appliances/electronics
    "skustuvas", "skalbyklė", "skalbimo", "šaldytuvas", "dulkių",
    "televizorius", "ausinės", "garsiakalbis", "fotoaparatas",
    # German appliances
    "rasierer", "waschmaschine", "kühlschrank", "staubsauger",
    # Polish appliances
    "golarka", "pralka", "lodówka", "odkurzacz",
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
    'tefal', 'braun', 'kenwood', 'delonghi', 'rowenta', 'karcher', 'electrolux',
}
_ACCESSORY_MATCH_WORDS = frozenset({
    'case', 'cover', 'sleeve', 'bumper', 'wallet', 'skin', 'sticker', 'decal',
    'holder', 'stand', 'mount', 'cradle', 'dock', 'bracket', 'grip',
    'charger', 'cable', 'adapter', 'hub', 'extender', 'splitter', 'dongle',
    'screen protector', 'tempered glass', 'film', 'foil',
    'replacement', 'spare', 'repair', 'filter', 'bag', 'brush', 'attachment',
    'earpad', 'eartip', 'ear tip', 'cushion', 'pad',
    'stylus', 'remote', 'controller', 'headset',
    'watch band', 'sport band', 'fitness band', 'wristband',
    'dėklas', 'maišelis', 'rankinė', 'stovas', 'laikiklis',
    'kroviklis', 'kabelis', 'plėvelė', 'stikliukas', 'apsauga',
    'etui', 'obudowa', 'pokrowiec', 'ładowarka', 'kabel', 'szkło', 'folia',
    'uchwyt', 'podstawka', 'naklejka', 'ochraniacz', 'filtr',
    'hülle', 'tasche', 'schutzhülle', 'ladegerät', 'halterung', 'schutzglas',
    'ersatz', 'zubehör',
    # LT plural accessory forms
    'maišeliai', 'filtrai', 'filtras', 'priedai', 'priedas', 'laikiklis',
    # Multi-word accessory phrases
    'cleaning kit', 'cleaning brush', 'carry bag', 'carry case', 'screen film',
    'wall mount', 'power bank', 'spare part',
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
        if acc not in t:
            continue
        # For ASCII single words, require whole-word match (e.g. "kabel" must not match "kabellose")
        if acc.isascii() and ' ' not in acc:
            if not re.search(r'(?<![a-z0-9])' + re.escape(acc) + r'(?![a-z0-9])', t):
                continue
        if acc not in q:
            return False
    # Brand matching normalises spaces so "delonghi" matches "De Longhi" in titles
    q_ns = q.replace(" ", "")
    t_ns = t.replace(" ", "")
    brands_in_q = [b for b in _KNOWN_BRANDS if b.replace(" ", "") in q_ns]
    for brand in brands_in_q:
        if brand.replace(" ", "") not in t_ns:
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
        if brands_in_q:
            # Brand confirmed + all model tokens confirmed -> definite match
            return True
    # If query has non-ASCII chars (Lithuanian/Polish) brand+model checks are
    # sufficient — category words won't appear in foreign-language product titles.
    if any(ord(c) > 127 for c in query):
        return True
    # For "Brand + category" queries with no model number, brand match is sufficient.
    # Allow up to 2 non-brand words (handles "DeLonghi kavos aparatas" and similar
    # Lithuanian queries where category words have no EN/DE equivalent in titles).
    if brands_in_q and not model_tokens:
        q_words_non_brand = [w for w in re.findall(r'[a-z0-9]{2,}', q)
                             if w not in _STOP_WORDS and w not in brands_in_q]
        if len(q_words_non_brand) <= 2:
            return True
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
_search_counts: dict = {}
_cache_hits: int = 0
_cache_misses: int = 0
_server_start: float = time.time()

_CATEGORY_ICON_MAP = [
    (["iphone", "samsung galaxy", "xiaomi", "oneplus", "pixel", "telefon", "smartphone",
      "galaxy s", "galaxy a", "redmi", "poco"], "📱"),
    (["macbook", "laptop", "notebook", "thinkpad", "dell xps", "asus", "surface pro",
      "chromebook"], "💻"),
    (["ipad", "galaxy tab", "tablet"], "📱"),
    (["oled", "qled", " tv ", " tv", "tv ", "television", "televizorius", "monitor",
      "ekranas", "screen", "55\"", "65\"", "43\""], "📺"),
    (["headphone", "earphone", "ausines", "airpods", "wh-1000", "bose qc", "jabra",
      "earbuds", "earphone"], "🎧"),
    (["playstation", "xbox", "nintendo", "lego", "gamepad", "rtx 4", "rtx 3",
      "geforce", "gaming"], "🎮"),
    (["camera", "nikon", "canon", "sony zv", "fotoaparatas", "mirrorless", "dslr"], "📷"),
    (["dulkiu siurblys", "vacuum", "dyson v", "roomba", "miele"], "🧹"),
    (["skalbykle", "washing machine", "indaplove", "dishwasher", "bosch wan",
      "samsung ww"], "🫧"),
    (["keptuve", "virdulys", "kettle", "blender", "mikser", "multicooker",
      "air fryer", "kavos aparatas", "nespresso"], "🍳"),
    (["lego", "zaislai", "pampers", "chicco", "fisher-price", "baby"], "🧸"),
    (["ssd", "nvme", "hdd", "ram ddr", "corsair", "kingston fury",
      "procesorius", "cpu", "ryzen", "core i"], "🖥️"),
    (["spausdintuvas", "printer", "scanner", "hp laserjet", "epson"], "🖨️"),
    (["philips shav", "braun series", "gillette", "skustuvas", "epilator"], "🪒"),
]


def get_category_icon(query: str, product_type: str = "MAIN") -> str:
    q = query.lower()
    for keywords, icon in _CATEGORY_ICON_MAP:
        if any(kw in q for kw in keywords):
            return icon
    return "🛍️" if product_type == "ACCESSORY" else "🛒"


def normalize_query(query: str) -> str:
    """Normalize a search query so minor variations hit the same cache entry.
    - Lowercases
    - Collapses whitespace
    - Removes common noise words that don't affect product identity
    - Keeps product-specific content intact
    """
    q = query.strip()
    # Collapse internal whitespace
    q = re.sub(r'\s+', ' ', q)
    # Remove trailing punctuation
    q = q.rstrip('.,;:!?')
    return q


def suggest_simpler_query(query: str) -> str:
    words = query.strip().split()
    if len(words) <= 2:
        return ""
    # Keep 3 tokens for long queries (more specific suggestion)
    return " ".join(words[:3]) if len(words) >= 5 else " ".join(words[:2])


def track_search(query: str):
    key = re.sub(r'\s+', ' ', query.lower().strip())
    if key and len(key) >= 2:
        _search_counts[key] = _search_counts.get(key, 0) + 1

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
        resp = _http.get(
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
        resp = _http.get(
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
    """Returns last 90 days of price rows for a product, most recent first."""
    sb = get_supabase()
    if not sb:
        return []
    try:
        cutoff = time.strftime("%Y-%m-%dT%H:%M:%SZ",
                               time.gmtime(time.time() - 90 * 86400))
        resp = (
            sb.table("price_history")
            .select("shop, price, currency, checked_at")
            .eq("product_name", product_name.lower().strip())
            .gte("checked_at", cutoff)
            .order("checked_at", desc=False)
            .limit(500)
            .execute()
        )
        return resp.data or []
    except Exception as e:
        print(f"[Supabase history] {e}")
        return []


def fetch_url(url: str, lang: str = "lt", timeout: int = SHOP_TIMEOUT,
              scraper_timeout: int = 5, render_js: bool = False):
    """
    render_js=False: ScraperAPI (1 credit) -> Zyte httpResponseBody -> direct.
    render_js=True:  ScraperAPI render (5 credits) -> Zyte httpResponseBody -> direct.
    Amazon additionally uses premium=true (25 credits) for anti-bot bypass.
    Zyte browserHtml intentionally not used (requires paid plan upgrade).
    """
    is_amazon = "amazon." in url
    use_render = render_js or is_amazon

    if SCRAPER_API_KEY:
        try:
            country = "de" if "amazon.de" in url else ("pl" if "amazon.pl" in url else ("lt" if any(s in url for s in ["varle.lt","pigu.lt","1a.lt","senukai.lt","topocentras.lt","elesen.lt"]) else ""))
            scraper_url = (
                f"https://api.scraperapi.com"
                f"?api_key={SCRAPER_API_KEY}"
                f"&url={requests.utils.quote(url, safe='')}"
                f"&render={'true' if use_render else 'false'}"
                + (f"&country_code={country}" if country else "")
                + ("&premium=true" if is_amazon else "")
            )
            resp = _http.get(scraper_url, timeout=scraper_timeout)
            if resp.status_code == 200:
                print(f"[ScraperAPI OK] {url[:70]}")
                return resp

            print(f"[ScraperAPI {resp.status_code}] -> Zyte fallback")
        except Exception as e:
            print(f"[ScraperAPI err] {e} -> Zyte fallback")

    if ZYTE_API_KEY and not is_amazon:
        # Zyte httpResponseBody: cheap fallback for LT shops (free plan supports this)
        try:
            import base64
            resp = _http.post(
                "https://api.zyte.com/v1/extract",
                auth=(ZYTE_API_KEY, ""),
                json={"url": url, "httpResponseBody": True},
                timeout=6,
            )
            if resp.status_code == 200:
                body = base64.b64decode(resp.json()["httpResponseBody"])

                class _ZyteResp:
                    status_code = 200

                    def __init__(self, content):
                        self.content = content
                        self.text = content.decode("utf-8", errors="replace")

                print(f"[Zyte OK] {url[:70]}")
                return _ZyteResp(body)
            print(f"[Zyte {resp.status_code}] -> direct")
        except Exception as e:
            print(f"[Zyte err] {e} -> direct")

    try:
        resp = _http.get(url, headers=get_headers(lang), timeout=timeout, allow_redirects=True)
        print(f"[Direct {resp.status_code}] {url[:70]}")
        return resp
    except Exception as e:
        print(f"[Direct err] {e}")
        return None


def get_cache_ttl(query: str) -> int:
    """Popular searches (searched 5+ times) get 1-hour TTL; others get 30 min."""
    key = re.sub(r'\s+', ' ', query.lower().strip())
    if _search_counts.get(key, 0) >= POPULAR_THRESHOLD:
        return POPULAR_CACHE_TTL
    return CACHE_TTL_SECONDS


def get_cache(key):
    global _cache_hits, _cache_misses
    if key in cache:
        e = cache[key]
        ttl = e.get("ttl", CACHE_TTL_SECONDS)
        if time.time() - e["ts"] < ttl:
            _cache_hits += 1
            return e["data"]
        del cache[key]
    _cache_misses += 1
    return None


_CACHE_MAX = int(os.getenv("CACHE_MAX_ENTRIES", "500"))


def set_cache(key, data, ttl: int = None):
    # Don't cache empty results — let the next request try again
    if not data.get("results") and data.get("price_min", 0) == 0:
        return
    if ttl is None:
        ttl = CACHE_TTL_SECONDS
    if len(cache) >= _CACHE_MAX:
        sorted_keys = sorted(cache, key=lambda k: cache[k]["ts"])
        for k in sorted_keys[: max(1, _CACHE_MAX // 10)]:
            cache.pop(k, None)
    cache[key] = {"data": data, "ts": time.time(), "ttl": ttl}


def get_client_ip() -> str:
    """Return the real client IP, honouring Render's X-Forwarded-For proxy header."""
    xff = request.headers.get("X-Forwarded-For", "")
    if xff:
        return xff.split(",")[0].strip()
    return request.remote_addr or "unknown"


def rate_limit(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        ip = get_client_ip()
        today = time.strftime("%Y-%m-%d")

        # Purge yesterday's entries ~1% of requests to keep memory bounded
        if random.random() < 0.01:
            stale = [k for k, v in list(rate_store.items()) if v.get("date") != today]
            for k in stale:
                rate_store.pop(k, None)

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
        resp = _http.get("https://api.exchangerate-api.com/v4/latest/EUR", timeout=5)
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


_TV_WORDS   = ["tv ", " tv", "televizorius", "television", "oled", "qled", "naled", "mini led", "smarttv"]
_MACBOOK_W  = ["macbook"]
_IPHONE_W   = ["iphone"]
_GALAXY_W   = ["samsung galaxy s", "samsung galaxy a", "samsung galaxy z", "pixel 8", "pixel 9"]
_WASHING_W  = ["skalbyklė", "skalbykle", "washing machine", "waschmaschine", "pralka",
               "indaplovė", "indaplove", "dishwasher", "spülmaschine", "zmywarka"]
_FRIDGE_W   = ["šaldytuvas", "saldytuvas", "refrigerator", "kühlschrank", "lodówka",
               "šaldiklis", "saldiklis", "gefrierschrank", "zamrażarka"]
_LAPTOP_W   = ["laptop", "notebook", "thinkpad", "ideapad", "vivobook", "zenbook",
               "dell xps", "surface pro", "chromebook", "kompiuteris"]
_AIRCON_W   = ["oro kondicionierius", "kondicionierius", "klimaanlage", "klimatyzator", "air conditioner"]
_TV_SIZE_RE = re.compile(r"\b(43|50|55|65|75|85)\b")


def validate_price(price: float, query: str) -> float:
    """Return price if sane for this query, else 0.0 (so scrapers can do `if not price: continue`)."""
    if price <= 0:
        return 0.0
    if price > 50_000:
        return 0.0

    q = query.lower()

    # Big TV (43–85") cannot cost < €100 — likely scraping a cable/accessory price
    has_tv   = any(w in q for w in _TV_WORDS) or "televizorius" in q
    has_size = bool(_TV_SIZE_RE.search(q))
    if has_tv and has_size and price < 100:
        return 0.0
    if has_tv and price < 50:      # no-size TV floor raised: rejects centai misidentifications
        return 0.0

    # MacBook: entry model ≥ €700 new; refurb ≥ €200
    if any(w in q for w in _MACBOOK_W) and price < 200:
        return 0.0

    # iPhone: oldest supported model ≥ €50
    if any(w in q for w in _IPHONE_W) and price < 50:
        return 0.0

    # Samsung Galaxy S/A/Z, Pixel phones: clearly a phone search, not an accessory
    if any(w in q for w in _GALAXY_W) and price < 50:
        return 0.0

    # Washing machine / dishwasher: always > €100
    if any(w in q for w in _WASHING_W) and price < 100:
        return 0.0

    # Fridge / freezer: always > €100
    if any(w in q for w in _FRIDGE_W) and price < 100:
        return 0.0

    # Laptop (non-MacBook): > €80
    if any(w in q for w in _LAPTOP_W) and price < 80:
        return 0.0

    # Air conditioner: > €150
    if any(w in q for w in _AIRCON_W) and price < 150:
        return 0.0

    # Global floor: anything below €0.50 is a parse artefact
    if price < 0.50:
        return 0.0

    return price


def deduplicate_by_shop(results: list) -> list:
    """Viena parduotuvė = vienas pigiausias rezultatas."""
    best = {}

    for r in results:
        shop = r.get("shop", "")
        price = r.get("price", 999999)

        if shop not in best or price < best[shop].get("price", 999999):
            best[shop] = r

    return list(best.values())


# ── GENERIC SPA JSON EXTRACTOR ──
def _walk_for_products(node, query, shop, flag, base_url, src_key, out, depth=0):
    """Recursively search JSON tree for product-like objects."""
    if depth > 10 or len(out) >= 8:
        return
    if isinstance(node, dict):
        name = (node.get("name") or node.get("title") or node.get("productName")
                or node.get("fullName") or node.get("Product_name") or "")
        price_val = None
        for pf in ("price", "finalPrice", "priceWithVat", "currentPrice",
                   "salePrice", "regularPrice", "Price", "priceValue"):
            if pf in node:
                price_val = node[pf]; break
        if price_val is None and isinstance(node.get("prices"), dict):
            price_val = node["prices"].get("final") or node["prices"].get("regular")

        if name and price_val is not None:
            try:
                p = float(str(price_val).replace(",", "."))
                vp = validate_price(p, query)
                if vp:
                    slug = (node.get("url") or node.get("slug") or
                            node.get("urlKey") or node.get("link") or "")
                    link = slug if slug.startswith("http") else f"{base_url.rstrip('/')}/{slug.lstrip('/')}"
                    out.append(_make_result(shop, flag, link, vp, str(name)[:100], src_key))
            except (ValueError, TypeError):
                pass
        for v in node.values():
            _walk_for_products(v, query, shop, flag, base_url, src_key, out, depth + 1)
    elif isinstance(node, list):
        for item in node[:40]:
            _walk_for_products(item, query, shop, flag, base_url, src_key, out, depth + 1)


def _extract_spa_products(html: str, query: str, shop: str, flag: str,
                           base_url: str, src_key: str) -> list:
    """
    Try to pull product data from SPA HTML without JS execution:
    1. __NEXT_DATA__ (Next.js)
    2. window.__*STATE*__ inline scripts
    3. <script type="application/ld+json"> product listings
    4. JSON arrays inside <script> matching product patterns
    """
    out = []
    soup = BeautifulSoup(html, "html.parser")

    # 1. Next.js
    nd = soup.find("script", {"id": "__NEXT_DATA__"})
    if nd:
        try:
            _walk_for_products(json.loads(nd.string or "{}"),
                               query, shop, flag, base_url, src_key, out)
            if out:
                print(f"[{shop}] {len(out)} via __NEXT_DATA__")
                return out
        except Exception:
            pass

    # 2. window.* state patterns in inline scripts
    for scr in soup.find_all("script", src=False):
        txt = scr.string or ""
        if len(txt) < 50:
            continue
        for pat in [
            r'window\.__(?:INITIAL|PRELOADED|NUXT|APP|REACT_QUERY|REDUX)_?STATE__\s*=\s*(\{.+?\})\s*;',
            r'window\.(?:state|store|appState|pageData|__data)\s*=\s*(\{.+?\})\s*;',
            r'"products"\s*:\s*(\[.+?\])',
            r'"items"\s*:\s*(\[.+?\])',
            r'"results"\s*:\s*(\[.+?\])',
            r'"hits"\s*:\s*(\[.+?\])',
        ]:
            m = re.search(pat, txt, re.DOTALL)
            if not m:
                continue
            try:
                raw = m.group(1)
                if len(raw) > 500_000:
                    continue
                data = json.loads(raw)
                node = data if isinstance(data, dict) else {"items": data}
                _walk_for_products(node, query, shop, flag, base_url, src_key, out)
                if out:
                    print(f"[{shop}] {len(out)} via window state pattern")
                    return out
            except Exception:
                continue

    # 3. ld+json (structured data — often has offers)
    for scr in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(scr.string or "{}")
            _walk_for_products(data, query, shop, flag, base_url, src_key, out)
            if out:
                print(f"[{shop}] {len(out)} via ld+json")
                return out
        except Exception:
            pass

    print(f"[{shop}] embedded JSON extraction: {len(out)} results")
    return out


# ── VARLE.LT ──
def _varle_from_next_data(html: str, query: str) -> list:
    """Extract Varle products from __NEXT_DATA__ JSON (Next.js SSR payload)."""
    results = []
    try:
        m = re.search(r'<script[^>]+id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
        if not m:
            return results
        data = json.loads(m.group(1))

        # Walk the JSON tree looking for product-like dicts (have name + price fields)
        def walk(node, depth=0):
            if depth > 12 or len(results) >= 8:
                return
            if isinstance(node, dict):
                name_val = node.get("name") or node.get("title") or node.get("productName") or node.get("fullName")
                # Look for price in various common field names
                price_val = None
                for pf in ("price", "finalPrice", "priceWithVat", "currentPrice", "salePrice", "regularPrice"):
                    if pf in node:
                        price_val = node[pf]
                        break
                # Some shops nest price under "prices" dict
                if price_val is None and isinstance(node.get("prices"), dict):
                    price_val = node["prices"].get("final") or node["prices"].get("regular")
                if price_val is None and isinstance(node.get("priceFormatted"), str):
                    price_val = parse_price(node["priceFormatted"])

                if name_val and price_val is not None:
                    try:
                        p = float(price_val)
                        vp = validate_price(p, query)
                        if vp:
                            slug = node.get("url") or node.get("slug") or node.get("urlKey") or ""
                            link = slug if slug.startswith("http") else f"https://varle.lt/{slug.lstrip('/')}"
                            results.append(_make_result("Varle.lt", "🇱🇹", link, vp, str(name_val)[:100], "varle"))
                    except (ValueError, TypeError):
                        pass
                for v in node.values():
                    walk(v, depth + 1)
            elif isinstance(node, list):
                for item in node[:30]:
                    walk(item, depth + 1)

        walk(data)
        print(f"[Varle __NEXT_DATA__] {len(results)} products")
    except Exception as e:
        print(f"[Varle NEXT_DATA err] {e}")
    return results


def scrape_varle(query: str) -> list:
    results = []

    try:
        url = f"https://varle.lt/search/?q={requests.utils.quote(query)}"
        # Varle's ld+json is server-rendered; try direct first (2s max so ScraperAPI fallback
        # still completes within the 11s pool timeout: 2s direct + 7s scraper = 9s total)
        try:
            resp = _http.get(url, headers=get_headers("lt"), timeout=2, allow_redirects=True)
            if resp.status_code != 200:
                resp = None
        except Exception:
            resp = None
        if not resp:
            resp = fetch_url(url, "lt", render_js=False, scraper_timeout=7)

        if not resp or resp.status_code != 200:
            print(f"[Varle] failed {resp.status_code if resp else 'no response'}")
            return results

        # Strategy 1: parse __NEXT_DATA__ JSON (prices fully populated in SSR payload)
        results = _varle_from_next_data(resp.text, query)
        if results:
            return results

        # Strategy 2: ld+json (Varle embeds Product + Offers with prices in schema.org script)
        results = _extract_spa_products(resp.text, query, "Varle.lt", "🇱🇹",
                                        "https://varle.lt", "varle")
        if results:
            return results

        # Strategy 3: DOM fallback (prices may be empty without JS)
        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.select(".GRID_ITEM")
        print(f"[Varle DOM] {len(items)} items")

        for item in items[:8]:
            try:
                price_el = item.select_one(".price-tag") or item.select_one(".price-value")
                if not price_el:
                    continue
                price = validate_price(parse_price(price_el.get_text()), query)
                if not price:
                    continue
                title_anchor = item.select_one(".product-title a")
                name = title_anchor.get_text(strip=True)[:100] if title_anchor else query
                href = title_anchor["href"] if title_anchor and title_anchor.get("href") else ""
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
        # Pigu uses AJAX — try ld+json/window state extraction (fast, no render needed)
        resp = fetch_url(url, "lt", render_js=False, scraper_timeout=6)
        if not resp or resp.status_code != 200:
            print(f"[Pigu] failed {resp.status_code if resp else 'no resp'}")
            return results
        results = _extract_spa_products(resp.text, query, "Pigu.lt", "🇱🇹",
                                        "https://pigu.lt", "pigu")
    except Exception as e:
        print(f"[Pigu] {e}")
    return results


# ── SENUKAI.LT ──
def _scrape_lupa_items(soup, shop, flag, base_url, src_key, query):
    """Scrape LupaSearch-rendered product items from a BeautifulSoup tree."""
    items = (
        soup.select(".lupa-search-results-element") or
        soup.select(".lupa-product-item") or
        soup.select("[class*='lupa-search-result']") or
        soup.select("[class*='lupa-product']")
    )
    results = []
    for item in items[:6]:
        try:
            price_el = (
                item.select_one("[class*='lupa-price']") or
                item.select_one("[class*='price']")
            )
            if not price_el:
                continue
            price = validate_price(parse_price(price_el.get_text()), query)
            if not price:
                continue
            name_el = (
                item.select_one("[class*='lupa-product-title']") or
                item.select_one("[class*='lupa-product-name']") or
                item.select_one("[class*='name']") or
                item.select_one("h2") or item.select_one("h3")
            )
            name = name_el.get_text(strip=True)[:100] if name_el else query
            link_el = item.select_one("a[href]")
            href = link_el["href"] if link_el else ""
            link = href if href.startswith("http") else f"{base_url.rstrip('/')}{href}"
            results.append(_make_result(shop, flag, link, price, name, src_key))
        except Exception as e:
            print(f"[{shop} item] {e}")
    return results


def scrape_senukai(query: str) -> list:
    results = []
    try:
        url = f"https://www.senukai.lt/paieska?q={requests.utils.quote(query)}"
        resp = fetch_url(url, "lt", render_js=True, scraper_timeout=8)
        if not resp or resp.status_code != 200:
            print(f"[Senukai] failed {resp.status_code if resp else 'no resp'}")
            return results
        soup = BeautifulSoup(resp.text, "html.parser")
        results = _scrape_lupa_items(soup, "Senukai.lt", "🇱🇹",
                                     "https://www.senukai.lt", "senukai", query)
        print(f"[Senukai] {len(results)} results")
    except Exception as e:
        print(f"[Senukai] {e}")
    return results


# ── TOPOCENTRAS.LT ──
def scrape_topo(query: str) -> list:
    results = []
    try:
        url = f"https://www.topocentras.lt/search?q={requests.utils.quote(query)}"
        # Topo is a pure JS SPA — try embedded JSON extraction first (fast)
        resp = fetch_url(url, "lt", render_js=False, scraper_timeout=6)
        if not resp or resp.status_code != 200:
            print(f"[Topo] failed {resp.status_code if resp else 'no resp'}")
            return results
        results = _extract_spa_products(resp.text, query, "Topo centras", "🇱🇹",
                                        "https://www.topocentras.lt", "topo")
    except Exception as e:
        print(f"[Topo] {e}")
    return results


# ── ELESEN.LT ──
def scrape_elesen(query: str) -> list:
    results = []

    try:
        url = f"https://www.elesen.lt/paieska?q={requests.utils.quote(query)}"
        # Try direct first (2s, free) before falling back to ScraperAPI (costs credits)
        try:
            resp = _http.get(url, headers=get_headers("lt"), timeout=2, allow_redirects=True)
            if resp.status_code != 200:
                resp = None
        except Exception:
            resp = None
        if not resp:
            resp = fetch_url(url, "lt", render_js=False, scraper_timeout=7)

        if not resp or resp.status_code != 200:
            print("[Elesen] failed")
            return results

        soup = BeautifulSoup(resp.text, "html.parser")

        # Elesen uses article.product-card for each product card
        items = (
            soup.select("article.product-card") or
            soup.select(".product-card.vertical") or
            soup.select(".product-card") or
            soup.select("[class*='product-item']") or
            soup.select("[class*='catalog-item']") or
            soup.select(".item-box") or
            soup.select("[data-product-id]")
        )
        # Fall back to SPA JSON extraction if DOM scraping found nothing
        if not items:
            spa = _extract_spa_products(resp.text, query, "Elesen.lt", "🇱🇹",
                                        "https://www.elesen.lt", "elesen")
            if spa:
                print(f"[Elesen] {len(spa)} via SPA JSON fallback")
                return spa

        print(f"[Elesen] {len(items)} items")

        for item in items[:8]:
            try:
                price_el = (
                    item.select_one(".price") or
                    item.select_one("[class*='price']")
                )

                if not price_el:
                    continue

                price_text = price_el.get_text()
                raw_price = parse_price(price_text)
                if not raw_price:
                    continue

                # Elesen mixes euros and centai:
                #   "Kaina:3999 €"                → 3999 centai = €39.99 (integer-only values < 50000)
                #   "Kaina su nuolaida6999 €85.99" → 6999 centai = €69.99
                #   "Kaina su nuolaida1349 €1599 €"→ 1349 euros  (MacBook — raw passes validate)
                # Rule: if raw integer ≥ 100 AND raw/100 passes validate but raw doesn't → use centai.
                #       if both pass → centai only if < €5000 (common appliance range).
                #       if raw already passes and centai doesn't → keep raw (expensive product like MacBook).
                if raw_price >= 100 and raw_price == int(raw_price):
                    centai = round(raw_price / 100, 2)
                    p_eur = validate_price(raw_price, query)
                    p_cnt = validate_price(centai, query)
                    if p_cnt and not p_eur:
                        raw_price = centai          # centai is the only valid interpretation
                    elif p_cnt and p_eur and raw_price < 50000:
                        # Both valid: prefer centai for typical appliance prices (< €500)
                        # but keep euro if centai is implausibly cheap (< €5)
                        if centai >= 5:
                            raw_price = centai

                price = validate_price(raw_price, query)
                if not price:
                    continue

                name_el = (
                    item.select_one(".product-card__title") or
                    item.select_one(".product_name") or
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
        # 1a.lt uses LupaSearch (JS-rendered) — go straight to render_js
        resp = fetch_url(url, "lt", render_js=True, scraper_timeout=8)
        if not resp or resp.status_code != 200:
            print(f"[1a] failed {resp.status_code if resp else 'no resp'}")
            return results
        soup = BeautifulSoup(resp.text, "html.parser")
        results = _scrape_lupa_items(soup, "1a.lt", "🇱🇹", "https://www.1a.lt", "1a", query)
        print(f"[1a] {len(results)} results")
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
        resp = fetch_url(url, lang, render_js=True, scraper_timeout=8)

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

                if not raw:
                    whole_el = item.select_one(".a-price-whole")
                    if whole_el:
                        whole_txt = re.sub(r'[^\d]', '', whole_el.get_text())
                        frac_el = item.select_one(".a-price-fraction")
                        frac_txt = re.sub(r'[^\d]', '', frac_el.get_text()) if frac_el else "00"
                        if whole_txt:
                            try:
                                raw = float(f"{whole_txt}.{frac_txt[:2] or '00'}")
                            except Exception:
                                pass

                if not raw:
                    continue

                price = validate_price(to_eur(raw, currency), query)
                if not price:
                    continue

                link_el = h2_el.parent if h2_el and h2_el.parent.name == "a" else item.select_one("a[href*='/dp/']")
                href = link_el["href"] if link_el else ""
                link = f"https://www.amazon.{domain}{href}" if href.startswith("/") else href

                asin_m = re.search(r"/dp/([A-Z0-9]{10})", link)
                asin = asin_m.group(1) if asin_m else ""

                aff_tag = AMAZON_AFFILIATE_TAG
                aff = (
                    f"https://www.amazon.{domain}/dp/{asin}?tag={aff_tag}"
                    if asin and aff_tag
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

                # Build deal_score from objective signals instead of flat 75
                am_score = 65
                if rating >= 4.5:
                    am_score += 10
                elif rating >= 4.0:
                    am_score += 5
                if review_count >= 100:
                    am_score += 8
                elif review_count >= 10:
                    am_score += 3
                if prime:
                    am_score += 5

                results.append({
                    "shop": f"Amazon.{domain.upper()}",
                    "flag": "🇩🇪" if domain == "de" else "🇵🇱",
                    "url": link,
                    "affiliate_url": aff,
                    "price": price,
                    "currency": "EUR",
                    "original_price": raw if currency != "EUR" else None,
                    "original_currency": currency if currency != "EUR" else None,
                    "in_stock": True,
                    "delivery": "Prime · Tomorrow" if prime else "2-5 d.",
                    "deal_score": min(90, am_score),
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


def _varle_affiliate_url(product_url: str) -> str:
    if not VARLE_AFFILIATE_TAG or not product_url.startswith("http"):
        return product_url
    sep = "&" if "?" in product_url else "?"
    return f"{product_url}{sep}ref={requests.utils.quote(VARLE_AFFILIATE_TAG)}"


def _make_result(shop, flag, link, price, name, source):
    aff_link = _varle_affiliate_url(link) if source == "varle" else link
    return {
        "shop": shop,
        "flag": flag,
        "url": link,
        "affiliate_url": aff_link,
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


# ── TRANSLATION ──
_translate_cache: dict = {}

# Lithuanian category words that trigger translation for Amazon DE/PL search
_LT_CATEGORY_WORDS = [
    "ausines", "ausinės", "ausinis", "siurblys", "siurblio", "dulkių",
    "skalbyklė", "skalbyklės", "skustuvas", "skustuvo", "telefonas",
    "televizorius", "televizoriaus", "kompiuteris", "planšetė", "kamera",
    "virdulys", "keptuvė", "puodas", "šaldytuvas", "mikrobangų",
    "kavos", "žaislas", "žaislo", "laidynas", "džiovintuvas",
    "spausdintuvas", "monitorius", "klaviatūra", "pelė",
    "skalbimo", "džiovyklė", "šaldiklis", "orkaitė", "mikseris",
    "plaukų", "skutimosi", "indaplovė",
    # Extended appliances
    "kondicionierius", "ventiliatorius", "šildytuvas",
    "dantų", "epilatorius", "masažuoklis", "svarstyklės",
    "čiužinys", "lemputė", "lemputės", "žoliapjovė", "viryklė",
    "kaitlentė", "gaubtas",
    # In dicts but missing from trigger list — would cause untranslated Amazon queries:
    "blenderis", "fotoaparatas", "garsiakalbis",
    # New product categories (with and without diacritics)
    "nešiojamas", "nesiojamas", "belaidis", "belaidė", "belaidės",
    "belaide", "belaides", "tosteris", "grilis", "kapsulės", "kapsules",
    # Genitive/accusative forms in dict phrases but not trigger list
    "kondicionieriaus", "robotas", "kraujo",
]

# Static word-for-word replacement — avoids Claude API for common LT product searches.
# Words are sorted longest-first so "dulkių siurblys" matches before "siurblys".
_LT_DE: list[tuple[str, str]] = sorted([
    ("dulkių siurblys", "Staubsauger"), ("dulkių siurblio", "Staubsauger"),
    ("skalbimo mašina", "Waschmaschine"), ("skalbyklė", "Waschmaschine"),
    ("skalbyklės", "Waschmaschine"), ("skalbimo", "Wasch"),
    ("džiovyklė", "Wäschetrockner"), ("indaplovė", "Spülmaschine"),
    ("šaldytuvas", "Kühlschrank"), ("šaldiklis", "Gefrierschrank"),
    ("orkaitė", "Backofen"), ("mikrobangų", "Mikrowellen"),
    ("kavos aparatas", "Kaffeemaschine"), ("kavos", "Kaffee"),
    ("virdulys", "Wasserkocher"), ("keptuvė", "Bratpfanne"),
    ("puodas", "Kochtopf"), ("kaitlentė", "Kochfeld"),
    ("mikseris", "Mixer"), ("blenderis", "Mixer"),
    ("ausinės", "Kopfhörer"), ("ausines", "Kopfhörer"), ("ausinis", "Kopfhörer"),
    ("siurblys", "Staubsauger"), ("siurblio", "Staubsauger"),
    ("skustuvas", "Rasierer"), ("skustuvo", "Rasierer"),
    ("plaukų džiovintuvas", "Haartrockner"), ("džiovintuvas", "Haartrockner"),
    ("laidynas", "Bügeleisen"), ("plaukų", "Haar"),
    ("televizorius", "Fernseher"), ("televizoriaus", "Fernseher"),
    ("telefonas", "Smartphone"), ("kompiuteris", "Computer"),
    ("planšetė", "Tablet"), ("kamera", "Kamera"),
    ("fotoaparatas", "Kamera"), ("spausdintuvas", "Drucker"),
    ("monitorius", "Monitor"), ("klaviatūra", "Tastatur"),
    ("pelė", "Maus"), ("garsiakalbis", "Lautsprecher"),
    ("žaislas", "Spielzeug"), ("žaislo", "Spielzeug"),
    ("skutimosi", "Rasier"),
    # Extended categories
    ("oro kondicionierius", "Klimaanlage"), ("oro kondicionieriaus", "Klimaanlage"),
    ("ventiliatorius", "Ventilator"), ("šildytuvas", "Heizgerät"),
    ("elektrinė dantų šepetėlė", "elektrische Zahnbürste"),
    ("dantų šepetėlis", "Zahnbürste"), ("dantų šepetėlį", "Zahnbürste"),
    ("epilatorius", "Epilator"), ("masažuoklis", "Massagegerät"),
    ("svarstyklės", "Körperwaage"), ("svarstyklių", "Körperwaage"),
    ("kraujo spaudimas", "Blutdruckmessgerät"),
    ("čiužinys", "Matratze"), ("čiužinio", "Matratze"),
    ("lemputė", "LED Glühbirne"), ("lemputės", "LED Glühbirne"),
    ("žoliapjovė", "Rasenmäher"), ("robotas dulkių", "Saugroboter"),
    ("robotas siurblys", "Saugroboter"), ("rankinis siurblys", "Handstaubsauger"),
    ("viryklė", "Herd"), ("indų", "Spülmaschine"),
    ("gaubtas", "Dunstabzugshaube"),
    # New entries (with and without diacritics for keyboard compatibility)
    ("nešiojamas kompiuteris", "Laptop"), ("nesiojamas kompiuteris", "Laptop"),
    ("nešiojamas", "Laptop"), ("nesiojamas", "Laptop"),
    ("belaidės ausinės", "kabellose Kopfhörer"), ("belaides ausines", "kabellose Kopfhörer"),
    ("belaidis", "kabellos"), ("belaidė", "kabellos"), ("belaidės", "kabellos"),
    ("belaide", "kabellos"), ("belaides", "kabellos"),
    ("tosteris", "Toaster"), ("grilis", "Grill"),
    ("kavos kapsulės", "Kaffeekapseln"), ("kavos kapsules", "Kaffeekapseln"),
    ("kapsulės", "Kapseln"), ("kapsules", "Kapseln"),
], key=lambda t: -len(t[0]))

_LT_PL: list[tuple[str, str]] = sorted([
    ("dulkių siurblys", "odkurzacz"), ("dulkių siurblio", "odkurzacz"),
    ("skalbimo mašina", "pralka"), ("skalbyklė", "pralka"),
    ("skalbyklės", "pralka"), ("skalbimo", "pranie"),
    ("džiovyklė", "suszarka do ubrań"), ("indaplovė", "zmywarka"),
    ("šaldytuvas", "lodówka"), ("šaldiklis", "zamrażarka"),
    ("orkaitė", "piekarnik"), ("mikrobangų", "mikrofalówka"),
    ("kavos aparatas", "ekspres do kawy"), ("kavos", "kawa"),
    ("virdulys", "czajnik"), ("keptuvė", "patelnia"),
    ("puodas", "garnek"), ("kaitlentė", "płyta grzejna"),
    ("mikseris", "mikser"), ("blenderis", "blender"),
    ("ausinės", "słuchawki"), ("ausines", "słuchawki"), ("ausinis", "słuchawki"),
    ("siurblys", "odkurzacz"), ("siurblio", "odkurzacz"),
    ("skustuvas", "golarka"), ("skustuvo", "golarka"),
    ("plaukų džiovintuvas", "suszarka do włosów"), ("džiovintuvas", "suszarka"),
    ("laidynas", "żelazko"), ("plaukų", "włosy"),
    ("televizorius", "telewizor"), ("televizoriaus", "telewizor"),
    ("telefonas", "smartfon"), ("kompiuteris", "komputer"),
    ("planšetė", "tablet"), ("kamera", "kamera"),
    ("fotoaparatas", "aparat fotograficzny"), ("spausdintuvas", "drukarka"),
    ("monitorius", "monitor"), ("klaviatūra", "klawiatura"),
    ("pelė", "mysz"), ("garsiakalbis", "głośnik"),
    ("žaislas", "zabawka"), ("žaislo", "zabawka"),
    ("skutimosi", "do golenia"),
    # Extended categories
    ("oro kondicionierius", "klimatyzator"), ("oro kondicionieriaus", "klimatyzator"),
    ("ventiliatorius", "wentylator"), ("šildytuvas", "grzejnik"),
    ("elektrinė dantų šepetėlė", "elektryczna szczoteczka do zębów"),
    ("dantų šepetėlis", "szczoteczka do zębów"), ("dantų šepetėlį", "szczoteczka"),
    ("epilatorius", "epilator"), ("masažuoklis", "masażer"),
    ("svarstyklės", "waga łazienkowa"), ("svarstyklių", "waga"),
    ("kraujo spaudimas", "ciśnieniomierz"),
    ("čiužinys", "materac"), ("čiužinio", "materac"),
    ("lemputė", "żarówka LED"), ("lemputės", "żarówka"),
    ("žoliapjovė", "kosiarka"), ("robotas dulkių", "robot sprzątający"),
    ("robotas siurblys", "robot odkurzający"), ("rankinis siurblys", "odkurzacz ręczny"),
    ("viryklė", "kuchenka"), ("indų", "zmywarka"),
    ("gaubtas", "okap kuchenny"),
    # New entries (with and without diacritics for keyboard compatibility)
    ("nešiojamas kompiuteris", "laptop"), ("nesiojamas kompiuteris", "laptop"),
    ("nešiojamas", "laptop"), ("nesiojamas", "laptop"),
    ("belaidės ausinės", "słuchawki bezprzewodowe"), ("belaides ausines", "słuchawki bezprzewodowe"),
    ("belaidis", "bezprzewodowy"), ("belaidė", "bezprzewodowa"), ("belaidės", "bezprzewodowe"),
    ("belaide", "bezprzewodowa"), ("belaides", "bezprzewodowe"),
    ("tosteris", "toster"), ("grilis", "grill"),
    ("kavos kapsulės", "kapsułki do kawy"), ("kavos kapsules", "kapsułki do kawy"),
    ("kapsulės", "kapsułki"), ("kapsules", "kapsułki"),
], key=lambda t: -len(t[0]))


def _static_translate(query: str, target_lang: str) -> str:
    """Replace LT category words with target-language equivalents. Free and instant."""
    mapping = _LT_DE if target_lang == "de" else _LT_PL
    result = query
    q_low = query.lower()
    for lt_word, target_word in mapping:
        if lt_word in q_low:
            # Case-insensitive replacement preserving surrounding text
            result = re.sub(re.escape(lt_word), target_word, result, flags=re.IGNORECASE)
            q_low = result.lower()
    return result


def claude_translate(query: str, target_lang: str = "en") -> str:
    cache_key = f"{query.lower()}:{target_lang}"
    if cache_key in _translate_cache:
        return _translate_cache[cache_key]

    q_lower = query.lower()

    # Fast path: no Lithuanian words → brand/model works in any language
    if not any(w in q_lower for w in _LT_CATEGORY_WORDS):
        _translate_cache[cache_key] = query
        return query

    # Try static dictionary first (free, instant, covers ~95% of LT queries)
    static_result = _static_translate(query, target_lang)
    if static_result.lower() != query.lower():
        # Static translation succeeded — cache and return immediately
        _translate_cache[cache_key] = static_result
        print(f"  [translate_static] '{query}' → '{static_result}' ({target_lang})")
        return static_result

    # Last resort: Claude for unusual/unknown LT phrases
    if not ANTHROPIC_API_KEY:
        return query

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        lang_names = {"en": "English", "de": "German", "pl": "Polish", "lt": "Lithuanian"}
        resp = client.messages.create(
            model=AI_MODEL_CLAUDE,
            max_tokens=40,
            messages=[{
                "role": "user",
                "content": f'Translate to {lang_names.get(target_lang, "English")} for product search. Return ONLY the translated product name, no explanation: "{query}"'
            }]
        )
        result = "".join(b.text for b in resp.content if hasattr(b, "text")).strip().strip('"')
        result = result if result else query
        _translate_cache[cache_key] = result
        return result
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
    prices = [r.get("price", 0) for r in results if r.get("price", 0) > 0]
    p_min = min(prices) if prices else 0
    p_max = max(prices) if prices else 0

    shops_summary = "; ".join(
        f"{r.get('shop','')} €{r.get('price',0):.2f}"
        + (f" ★{r.get('rating')}" if r.get("rating") else "")
        for r in sorted(results, key=lambda x: x.get("price", 999999))[:4]
        if r.get("price", 0) > 0
    )

    hist = price_history or {}
    hist_line = ""
    if hist.get("lowest") and hist.get("count", 0) >= 2:
        hist_line = f" History: low €{hist['lowest']}, high €{hist.get('highest','?')} ({hist['count']} samples)."

    return f"""Goody price comparison coach. Analyze and return JSON only.
Product: {query}
Shops: {shops_summary}
Price range: €{p_min:.2f}–€{p_max:.2f} ({len(prices)} shops).{hist_line}

Rules: only use provided data. Be concise. Write in the language of the product query (LT/DE/PL/EN).

Return ONLY valid JSON:
{{"verdict":"BUY|WAIT|OK","verdict_label":"1-3 words","verdict_reason":"one sentence","ai_summary":"1-2 sentences","alternative":"cheaper alternative if overpriced else empty","buy_recommendation":"1-2 sentences of specific advice","price_forecast":"one sentence or empty"}}"""


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
    # Rule-based (free) when too few shops; paid AI when 2+ shops with meaningful spread
    if not results:
        return rule_based_ai_analyze(query, results, price_history)

    prices = [r.get("price", 0) for r in results if r.get("price", 0) > 0]
    if len(prices) < 2:   # need at least 2 shops to compare
        return rule_based_ai_analyze(query, results, price_history)

    price_max = max(prices)
    spread_pct = ((price_max - min(prices)) / price_max * 100) if price_max else 0
    if spread_pct < 5:    # prices are within 5% — not interesting enough for AI
        return rule_based_ai_analyze(query, results, price_history)

    if AI_PROVIDER == "openai":
        return openai_analyze(query, results, price_history)

    if AI_PROVIDER == "claude":
        return claude_analyze(query, results, price_history)

    return rule_based_ai_analyze(query, results, price_history)


def get_price_history(query: str) -> dict:
    """Returns price history from Supabase only. Instant and uses our own accumulated data."""
    try:
        rows = fetch_price_history_from_supabase(query)
        if not rows:
            return {}
        prices = [float(r.get("price", 0)) for r in rows if float(r.get("price", 0)) > 0]
        if not prices:
            return {}
        return {
            "lowest": round(min(prices), 2),
            "highest": round(max(prices), 2),
            "avg": round(sum(prices) / len(prices), 2),
            "count": len(prices),
            "source": "goody_history",
        }
    except Exception as e:
        print(f"[price_history] {e}")
        return {}


def post_process(results: list, query: str, ai_data: dict = None, price_history: dict = None) -> dict:
    results = deduplicate_by_shop(results)
    results = [r for r in results if r.get("price", 0) > 0]
    filtered = [r for r in results if is_relevant_result(query, r.get("product_title", ""))]
    if filtered:
        results = filtered

    if not results:
        suggestion = suggest_simpler_query(query)
        return {
            "product_name": query,
            "ai_verdict": "WAIT",
            "verdict_label": "Nerasta",
            "verdict_reason": "Produktas nerastas nė vienoje parduotuvėje.",
            "ai_summary": "Pabandykite tikslesnį pavadinimą arba trumpesnę užklausą.",
            "buy_recommendation": f'Pabandykite: "{suggestion}"' if suggestion else "Pabandykite kitą paieškos terminą.",
            "alternative": suggestion,
            "price_forecast": "",
            "deal_score": 0,
            "price_min": 0,
            "price_max": 0,
            "price_avg": 0,
            "price_history": price_history or {},
            "search_suggestion": suggestion,
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
    base_score = min(100, int(savings_pct * 1.5 + 50))

    # Adjust with price history: reward below-avg current prices, penalise above-avg
    hist = price_history or {}
    hist_avg = hist.get("avg", 0)
    hist_bonus = 0
    if hist_avg and hist.get("count", 0) >= 2 and price_min > 0:
        ratio = price_min / hist_avg
        if ratio < 0.90:    # ≥10% below historical avg → bonus
            hist_bonus = min(15, int((1 - ratio) * 100))
        elif ratio > 1.10:  # ≥10% above historical avg → mild penalty
            hist_bonus = -8

    deal_score = max(10, min(100, base_score + hist_bonus))

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
    t0 = time.time()
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data"}), 400

    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "query_required", "message": "Įveskite produkto pavadinimą."}), 400
    if len(query) < 2:
        return jsonify({"error": "query_too_short", "message": "Paieška per trumpa — įveskite bent 2 simbolius."}), 400
    if len(query) > 200:
        query = query[:200]

    # Normalize and barcode-resolve before cache lookup
    query = normalize_query(query)
    original_query = query
    if re.match(r'^\d{8,14}$', query):
        product_from_barcode = lookup_barcode_free(query)
        if product_from_barcode:
            print(f"[Barcode] {query} -> {product_from_barcode}")
            query = product_from_barcode

    cache_key = hashlib.md5(f"v60:{query.lower()}".encode()).hexdigest()
    etag = f'"{cache_key}"'
    cached = get_cache(cache_key)

    if cached:
        if request.headers.get("If-None-Match") == etag:
            return "", 304
        cached["_cached"] = True
        resp = jsonify(cached)
        resp.headers["ETag"] = etag
        resp.headers["Cache-Control"] = "private, max-age=900"
        return resp

    print(f"\n=== SEARCH: '{original_query}' -> resolved:'{query}' ===")
    t0_search = time.time()

    all_results = []

    # Price history runs in its own background executor so the main shop executor
    # doesn't block on it when it shuts down (executor.shutdown waits for all futures).
    _ph_exec = ThreadPoolExecutor(max_workers=1)
    ph_fut   = _ph_exec.submit(get_price_history, query)

    # For LT queries, pre-translate in parallel (2-3s) so Amazon gets the right query
    # from the start and no retry is needed. For English queries this returns instantly.
    q_lower = query.lower()
    is_lt_query = any(w in q_lower for w in _LT_CATEGORY_WORDS)
    query_de = query
    query_pl = query
    if is_lt_query:
        try:
            with ThreadPoolExecutor(max_workers=2) as _pre:
                _f_de = _pre.submit(claude_translate, query, "de")
                _f_pl = _pre.submit(claude_translate, query, "pl")
                query_de = _f_de.result(timeout=4) or query
                query_pl = _f_pl.result(timeout=4) or query
        except Exception:
            pass
    print(f"  [Translate] DE:'{query_de}' PL:'{query_pl}'")

    # Use explicit executor (not `with`) so shutdown(wait=False) doesn't block on slow futures.
    executor = ThreadPoolExecutor(max_workers=6)
    try:
        lt_futures = {
            executor.submit(scrape_varle,  query): "Varle",
            executor.submit(scrape_elesen, query): "Elesen",
        }

        # Amazon uses pre-translated query — no retry phase needed
        amz_futures = {
            executor.submit(scrape_amazon, query_de, "de"): "Amazon.DE",
            executor.submit(scrape_amazon, query_pl, "pl"): "Amazon.PL",
        }

        all_shop_futures = {**lt_futures, **amz_futures}

        try:
            for f in as_completed(all_shop_futures, timeout=9):
                name = all_shop_futures[f]
                try:
                    res = f.result(timeout=1)
                    print(f"  [{name}] {len(res)} results @ {round(time.time()-t0_search,1)}s")
                    all_results.extend(res)
                except Exception as e:
                    print(f"  [{name}] error: {e}")
        except Exception as e:
            print(f"[shops timeout] {e}")
    finally:
        executor.shutdown(wait=False)  # Don't block on slow futures still running in background

    _t_after_pool = time.time()
    print(f"=== TOTAL: {len(all_results)} results before dedup/filter @ {_t_after_pool-t0_search:.1f}s ===\n")

    # Collect price history (was running in background since t=0, should be ready)
    price_history = {}
    try:
        price_history = ph_fut.result(timeout=1)
    except Exception:
        pass
    _ph_exec.shutdown(wait=False)  # don't block if still running
    _t_after_ph = time.time()

    # Deduplicate before AI so it sees 1 price per shop, not raw multi-item list
    deduped_for_ai = deduplicate_by_shop(all_results)
    ai_data = analyze_deal_with_ai(query, deduped_for_ai, price_history)
    _t_after_ai = time.time()
    result = post_process(all_results, query, ai_data, price_history)
    _t_after_pp = time.time()

    price_for_classify = result.get("price_min", 0)
    product_type = classify_product_cheap(query, price_for_classify)
    _t_after_classify = time.time()
    result["product_type"] = product_type
    result["category_icon"] = get_category_icon(query, product_type)
    result["search_time_ms"] = int((time.time() - t0) * 1000)

    if request.headers.get("X-Debug-Key") == DEBUG_API_KEY and DEBUG_API_KEY:
        result["_timing"] = {
            "pool_s":     round(_t_after_pool     - t0_search, 2),
            "ph_s":       round(_t_after_ph       - _t_after_pool, 2),
            "ai_s":       round(_t_after_ai       - _t_after_ph, 2),
            "pp_s":       round(_t_after_pp       - _t_after_ai, 2),
            "classify_s": round(_t_after_classify - _t_after_pp, 2),
        }

    track_search(query)
    set_cache(cache_key, result, ttl=get_cache_ttl(query))
    threading.Thread(target=save_prices_to_supabase, args=(query, all_results), daemon=True).start()

    ip = get_client_ip()
    used = rate_store.get(ip, {}).get("count", 1)

    result["_rate"] = {
        "used": used,
        "limit": DAILY_FREE_LIMIT,
        "remaining": max(0, DAILY_FREE_LIMIT - used)
    }

    resp = jsonify(result)
    resp.headers["ETag"] = etag
    resp.headers["Cache-Control"] = "private, max-age=900"
    return resp


# ── SSE STREAMING SEARCH ──
@app.route("/api/search-stream", methods=["POST"])
@rate_limit
def search_stream():
    """SSE endpoint — sends partial results as each shop responds, then the final AI result."""
    t0 = time.time()
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400

    query = normalize_query(data.get("query", "").strip())
    if not query:
        return jsonify({"error": "query_required", "message": "Įveskite produkto pavadinimą."}), 400
    if len(query) < 2:
        return jsonify({"error": "query_too_short", "message": "Paieška per trumpa."}), 400
    if len(query) > 200:
        query = query[:200]

    original_query = query
    if re.match(r'^\d{8,14}$', query):
        product_from_barcode = lookup_barcode_free(query)
        if product_from_barcode:
            query = product_from_barcode

    # Capture rate info before entering the generator (request context won't be in the thread)
    ip = get_client_ip()
    used = rate_store.get(ip, {}).get("count", 1)
    rate_info = {"used": used, "limit": DAILY_FREE_LIMIT, "remaining": max(0, DAILY_FREE_LIMIT - used)}

    cache_key = hashlib.md5(f"v60:{query.lower()}".encode()).hexdigest()

    # Freeze query strings for generator closure
    _query = query
    _original = original_query

    def _sse(event_type: str, payload: dict) -> str:
        return f"data: {json.dumps({'type': event_type, 'payload': payload}, ensure_ascii=False)}\n\n"

    def generate():
        # ── Cache hit ──
        cached = get_cache(cache_key)
        if cached:
            cached = dict(cached)
            cached["_cached"] = True
            cached["_rate"] = rate_info
            yield _sse("complete", cached)
            return

        print(f"\n=== STREAM: '{_original}' -> '{_query}' ===")
        t_start = time.time()

        all_results = []
        shops_done = 0
        SHOPS_TOTAL = 4  # Active shops: Varle, Elesen, Amazon.DE, Amazon.PL

        def _send_partial():
            p = post_process(list(all_results), _query, None, {})
            p["_partial"] = True
            p["_shops_done"] = shops_done
            p["_shops_total"] = SHOPS_TOTAL
            p["_rate"] = rate_info
            return _sse("partial", p)

        # Price history fetches in parallel with translation + shops (starts at t=0)
        _ph_exec = ThreadPoolExecutor(max_workers=1)
        ph_fut = _ph_exec.submit(get_price_history, _query)

        try:
            # Pre-translate for LT queries
            q_lower = _query.lower()
            _is_lt = any(w in q_lower for w in _LT_CATEGORY_WORDS)
            q_de = _query
            q_pl = _query
            if _is_lt:
                try:
                    with ThreadPoolExecutor(max_workers=2) as _pre:
                        _f_de = _pre.submit(claude_translate, _query, "de")
                        _f_pl = _pre.submit(claude_translate, _query, "pl")
                        q_de = _f_de.result(timeout=4) or _query
                        q_pl = _f_pl.result(timeout=4) or _query
                except Exception:
                    pass
            print(f"  [Stream translate] DE:'{q_de}' PL:'{q_pl}'")

            stream_executor = ThreadPoolExecutor(max_workers=4)
            try:
                all_shop_futures = {
                    stream_executor.submit(scrape_varle,  _query):    "Varle",
                    stream_executor.submit(scrape_elesen, _query):    "Elesen",
                    stream_executor.submit(scrape_amazon, q_de, "de"): "Amazon.DE",
                    stream_executor.submit(scrape_amazon, q_pl, "pl"): "Amazon.PL",
                }

                try:
                    for f in as_completed(all_shop_futures, timeout=10):
                        name = all_shop_futures[f]
                        try:
                            res = f.result(timeout=1)
                            t_shop = round(time.time() - t_start, 1)
                            print(f"  [{name}] {len(res)} results @ {t_shop}s")
                            shops_done += 1
                            all_results.extend(res)
                            if any(r.get("price", 0) > 0 for r in res):
                                yield _send_partial()
                        except Exception as e:
                            print(f"  [{name}] error: {e}")
                            shops_done += 1
                except Exception as e:
                    print(f"[stream shops timeout] {e}")
            finally:
                stream_executor.shutdown(wait=False)

        except Exception as e:
            print(f"[stream executor] {e}")

        print(f"=== STREAM TOTAL: {len(all_results)} before dedup ===")

        # Collect price history (was running in background since t=0)
        price_history = {}
        try:
            price_history = ph_fut.result(timeout=1)
        except Exception:
            pass
        _ph_exec.shutdown(wait=False)

        # ── AI + final result ──
        try:
            deduped_for_ai = deduplicate_by_shop(all_results)
            ai_data = analyze_deal_with_ai(_query, deduped_for_ai, price_history)
            result = post_process(all_results, _query, ai_data, price_history)

            price_for_classify = result.get("price_min", 0)
            product_type = classify_product_cheap(_query, price_for_classify)
            result["product_type"] = product_type
            result["category_icon"] = get_category_icon(_query, product_type)
            result["search_time_ms"] = int((time.time() - t0) * 1000)
            result["_rate"] = rate_info

            track_search(_query)
            set_cache(cache_key, result, ttl=get_cache_ttl(_query))
            threading.Thread(target=save_prices_to_supabase, args=(_query, all_results), daemon=True).start()

            yield _sse("complete", result)

        except Exception as e:
            print(f"[stream final] {e}")
            yield _sse("error", {"message": "Įvyko klaida apdorojant rezultatus."})

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@app.route("/api/price-history", methods=["GET"])
def price_history_endpoint():
    q = request.args.get("q", "").strip()[:200]
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
@rate_limit
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
@rate_limit
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
    return jsonify({
        "barcode": barcode,
        "product_name": "",
        "source": "not_found",
        "message": "Barkodas neatpažintas. Pabandykite įvesti produkto pavadinimą rankiniu būdu arba nufotografuokite produktą."
    }), 404


@app.route("/api/scan-image", methods=["POST"])
@rate_limit
def scan_image():
    t0 = time.time()
    data = request.get_json()

    if not data or "image" not in data:
        return jsonify({"error": "No image"}), 400

    image_b64 = data.get("image", "")
    if len(image_b64) >= 14_000_000:  # ~10 MB binary
        return jsonify({"error": "image_too_large", "message": "Nuotrauka per didelė. Maksimalus dydis 10 MB."}), 413

    if not ANTHROPIC_API_KEY:
        return jsonify({
            "error": "scan_unavailable",
            "message": "Nuotraukų nuskaitymas neprieinamas. Prašome susisiekti su palaikymu."
        }), 503

    import base64 as _b64
    def _detect_media_type(b64: str) -> str:
        try:
            header = _b64.b64decode(b64[:32] + "==")[:8]
            if header[:4] == b'\x89PNG':
                return "image/png"
            if header[:3] in (b'GIF',):
                return "image/gif"
            if header[:4] == b'RIFF' or b'WEBP' in header:
                return "image/webp"
        except Exception:
            pass
        return "image/jpeg"

    media_type = _detect_media_type(image_b64)

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
                                "media_type": media_type,
                                "data": image_b64
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
        barcode_from_image = vision.get("barcode", "").strip()

        # If AI found a barcode in the image, try free barcode lookup for a better name
        if barcode_from_image and re.match(r'^\d{8,14}$', barcode_from_image):
            bc_name = lookup_barcode_free(barcode_from_image)
            if bc_name:
                product_name = bc_name
                confidence = "high"

        if isinstance(price_visible, (int, float)) and price_visible <= 1:
            price_visible = 0

        if not product_name or (confidence == "low" and len(product_name) < 4):
            return jsonify({
                "error": "product_not_recognized",
                "message": "Produktas neatpažintas. Pabandykite nufotografuoti arčiau, su geresniu apšvietimu arba įveskite pavadinimą rankiniu būdu.",
                "confidence": confidence
            }), 422

        cache_key = hashlib.md5(f"scan_v60:{product_name.lower()}".encode()).hexdigest()
        cached = get_cache(cache_key)

        if cached:
            cached["_cached"] = True
            cached["scanned_product"] = product_name
            cached["store_price"] = price_visible
            return jsonify(cached)

        query_de = product_name
        query_pl = product_name
        try:
            with ThreadPoolExecutor(max_workers=2) as _pre:
                _f_de = _pre.submit(claude_translate, product_name, "de")
                _f_pl = _pre.submit(claude_translate, product_name, "pl")
                query_de = _f_de.result(timeout=4) or product_name
                query_pl = _f_pl.result(timeout=4) or product_name
        except Exception:
            pass

        # Price history fetches in parallel with shops (starts immediately)
        _scan_ph_exec = ThreadPoolExecutor(max_workers=1)
        scan_ph_fut = _scan_ph_exec.submit(get_price_history, product_name)

        all_results = []
        scan_executor = ThreadPoolExecutor(max_workers=4)
        try:
            futures = {
                scan_executor.submit(scrape_varle,   product_name):    "Varle",
                scan_executor.submit(scrape_elesen,  product_name):    "Elesen",
                scan_executor.submit(scrape_amazon,  query_de, "de"):  "Amazon.DE",
                scan_executor.submit(scrape_amazon,  query_pl, "pl"):  "Amazon.PL",
            }
            try:
                for f in as_completed(futures, timeout=10):
                    try:
                        all_results.extend(f.result(timeout=1))
                    except Exception as e:
                        print(f"[Scan parallel] {e}")
            except Exception as e:
                print(f"[Scan timeout] {e}")
        finally:
            scan_executor.shutdown(wait=False)

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

        # Collect price history (was running in parallel since shop start)
        price_history = {}
        try:
            price_history = scan_ph_fut.result(timeout=1)
        except Exception:
            pass
        _scan_ph_exec.shutdown(wait=False)

        deduped_for_scan_ai = deduplicate_by_shop(all_results)
        ai_data = analyze_deal_with_ai(product_name, deduped_for_scan_ai, price_history)
        result = post_process(all_results, product_name, ai_data, price_history)

        result["scanned_product"] = product_name
        result["scan_confidence"] = confidence
        result["store_price"] = (
            price_visible
            if isinstance(price_visible, (int, float)) and price_visible > 1
            else 0
        )
        price_for_scan_classify = price_visible if isinstance(price_visible, (int, float)) and price_visible > 1 else result.get("price_min", 0)
        scan_product_type = classify_product_cheap(product_name, price_for_scan_classify)
        result["product_type"] = scan_product_type
        result["category_icon"] = get_category_icon(product_name, scan_product_type)
        result["search_time_ms"] = int((time.time() - t0) * 1000)

        set_cache(cache_key, result)

        track_search(product_name)
        threading.Thread(target=save_prices_to_supabase, args=(product_name, all_results), daemon=True).start()

        _ip = get_client_ip()
        used = rate_store.get(_ip, {}).get("count", 1)

        result["_rate"] = {
            "used": used,
            "limit": DAILY_FREE_LIMIT,
            "remaining": max(0, DAILY_FREE_LIMIT - used)
        }

        return jsonify(result)

    except Exception as e:
        print(f"[scan_image] {e}")
        return jsonify({"error": "scan_failed", "message": "Nuotraukos apdorojimas nepavyko."}), 500


@app.route("/api/popular-searches", methods=["GET"])
def popular_searches():
    limit = min(int(request.args.get("limit", 10)), 20)
    sorted_q = sorted(_search_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
    return jsonify({
        "searches": [{"query": q, "count": c} for q, c in sorted_q],
        "total_unique": len(_search_counts)
    })


@app.route("/api/cache-stats", methods=["GET"])
def cache_stats():
    total = _cache_hits + _cache_misses
    hit_rate = round(_cache_hits / total * 100, 1) if total else 0.0
    uptime_h = round((time.time() - _server_start) / 3600, 1)

    # Cost per uncached search (v5.20 routing):
    # LT shops: 6 × $0.00049 ScraperAPI = $0.00294
    # Amazon: 2 × $0.0075 Zyte browserHtml  = $0.01500
    # OpenAI (10% chance): $0.000019
    cost_per_miss = 0.00294 + 0.01500 + 0.000019
    cost_per_hit  = 0.0

    saved = round(_cache_hits * cost_per_miss, 4)
    spent = round(_cache_misses * cost_per_miss, 4)

    top5 = sorted(_search_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    popular_cached = [
        {"query": q, "count": c, "cached": any(
            v.get("data", {}) for v in cache.values()
        )}
        for q, c in top5
    ]

    # Current live cache entries with TTL remaining
    now = time.time()
    live_entries = []
    for k, v in list(cache.items())[:20]:
        age = now - v["ts"]
        ttl = v.get("ttl", CACHE_TTL_SECONDS)
        remaining = max(0, ttl - age)
        q = v.get("data", {}).get("query", "?")
        live_entries.append({
            "query": q,
            "age_s": round(age),
            "ttl_s": ttl,
            "expires_in_s": round(remaining),
            "popular": ttl >= POPULAR_CACHE_TTL,
        })
    live_entries.sort(key=lambda x: x["expires_in_s"], reverse=True)

    return jsonify({
        "uptime_hours": uptime_h,
        "cache": {
            "entries": len(cache),
            "max_entries": _CACHE_MAX,
            "hits": _cache_hits,
            "misses": _cache_misses,
            "hit_rate_pct": hit_rate,
            "ttl_regular_min": CACHE_TTL_SECONDS // 60,
            "ttl_popular_min": POPULAR_CACHE_TTL // 60,
            "popular_threshold": POPULAR_THRESHOLD,
        },
        "cost": {
            "per_cache_hit_usd": cost_per_hit,
            "per_cache_miss_usd": round(cost_per_miss, 5),
            "total_saved_usd": saved,
            "total_spent_usd": spent,
            "session_total_usd": round(saved + spent, 4),
        },
        "top_searches": popular_cached,
        "live_cache_sample": live_entries[:10],
    })


@app.route("/api/debug-html", methods=["GET"])
def debug_html():
    if DEBUG_API_KEY and request.args.get("key") != DEBUG_API_KEY:
        return jsonify({"error": "unauthorized"}), 401
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

    # __NEXT_DATA__ presence check
    next_data_script = soup.find("script", {"id": "__NEXT_DATA__"})
    next_data_keys = []
    next_data_sample = ""
    if next_data_script:
        try:
            nd = json.loads(next_data_script.string or "{}")
            def _collect_keys(obj, depth=0, prefix=""):
                keys = []
                if depth > 4: return keys
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        full = f"{prefix}.{k}" if prefix else k
                        keys.append(full)
                        keys += _collect_keys(v, depth+1, full)
                elif isinstance(obj, list) and obj:
                    keys += _collect_keys(obj[0], depth+1, f"{prefix}[0]")
                return keys
            next_data_keys = _collect_keys(nd)[:60]
            next_data_sample = json.dumps(nd, ensure_ascii=False)[:2000]
        except Exception as nd_err:
            next_data_sample = str(nd_err)

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
        "next_data_present": bool(next_data_script),
        "next_data_keys": next_data_keys,
        "next_data_sample": next_data_sample,
    })


@app.route("/api/health", methods=["GET"])
def health():
    uptime_s = int(time.time() - _server_start)
    hit_rate = (
        round(_cache_hits / (_cache_hits + _cache_misses) * 100, 1)
        if (_cache_hits + _cache_misses) > 0 else 0
    )
    return jsonify({
        "status": "ok",
        "version": "5.55",
        "uptime_s": uptime_s,
        "shops": ["Varle.lt", "Elesen.lt", "Amazon.DE", "Amazon.PL"],
        "ai": {
            "provider": AI_PROVIDER,
            "model": AI_MODEL_CLAUDE if AI_PROVIDER == "claude" else AI_MODEL_OPENAI,
            "configured": bool(ANTHROPIC_API_KEY or OPENAI_API_KEY),
        },
        "cache": {
            "entries": len(cache),
            "hit_rate_pct": hit_rate,
            "hits": _cache_hits,
            "misses": _cache_misses,
        },
        "supabase": bool(SUPABASE_URL and SUPABASE_KEY),
        "scraper_api": bool(SCRAPER_API_KEY),
        "zyte": bool(ZYTE_API_KEY),
    })


@app.route("/api/rate-limit", methods=["GET"])
def rate_limit_status():
    ip = get_client_ip()
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


# ── KEEP-ALIVE (Render free tier sleeps after 15 min) ──
def _keepalive_worker():
    """Ping /api/health every 13 min to prevent Render free-tier sleep (timeout = 15 min)."""
    render_url = os.getenv("RENDER_EXTERNAL_URL", "").rstrip("/")
    if not render_url:
        return
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


if __name__ == "__main__":
    import time as _t
    _server_start = _t.time()

    port = int(os.getenv("PORT", 5000))

    print("\n🟢 Goody API v5.55")
    print(f"📊 Supabase: {'✅ configured' if SUPABASE_URL else '⚠️ not set'}")
    print("📦 Active shops: Varle + Elesen + Amazon.DE + Amazon.PL")
    print(f"🔑 ScraperAPI: {'✅ configured' if SCRAPER_API_KEY else '⚠️ not set'}")
    print(f"🔑 Zyte: {'✅ configured' if ZYTE_API_KEY else '⚠️ not set'}")
    print(f"🤖 Anthropic: {'✅ configured' if ANTHROPIC_API_KEY else '❌ missing'}")
    print(f"🤖 OpenAI: {'✅ configured' if OPENAI_API_KEY else '❌ missing'}")
    print(f"🧠 AI provider: {AI_PROVIDER}")
    print(f"🧠 OpenAI model: {AI_MODEL_OPENAI}")

    app.run(host="0.0.0.0", port=port, debug=False)
