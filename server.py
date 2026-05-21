"""
Goody Backend v6.87 — _CATEGORY_ICON_MAP: +neff🍳/asko🫧/bauknecht🫧/severin🍳/bomann🍳; _ROBOT_VAC_W: +dreame/ecovacs/eufy; _NOISE_WORDS: +pigiausia/best deal/kur pigiausia:
- v6.86 — _ACCESSORY_MATCH_WORDS: +staubsaugerbeutel/ersatzbeutel/tonerkassette:
- v6.85 — _ACCESSORY_MATCH_WORDS: +ersatzbürste/seitenbürste/cartridge/refill/druckerpatrone (robot vacuum/printer accessories):
- v6.84 — _KNOWN_BRANDS: remove duplicate ariston/smeg entries:
- v6.83 — _VARIANT_WORDS: +slim/boost/titan (model suffix variants):
- v6.82 — _NOISE_WORDS: +lietuva/vokietija/lenkija/deutschland/polska (cache hit boost):
- v6.81 — _KNOWN_BRANDS +gigabyte/msi/fritzbox; _CATEGORY_ICON_MAP +gigabyte/msi🎮/fritzbox🌐:
- v6.80 — _LT_DE/PL: +colių→Zoll/cali (inch) TV size translation:
- v6.79 — _LT_DE/PL: +kavos malūnėlis/automatinis kavos aparatas translations:
- v6.78 — _CATEGORY_ICON_MAP: +dreame/ecovacs/eufy🤖; _ACCESSORY_MAP: +audio-technica🎧:
- v6.77 — _LT_DE/PL: +virtuvinis kombainas/akumuliatorinis; _ACCESSORY: +toner/wandhalterung/dėklai; _KNOWN_BRANDS: +audio-technica:
- v6.76 — _CATEGORY_ICON_MAP: +air purifier💨/health🩺/scale⚖️/brands (yamaha/daikin/vaillant/tp-link/moulinex/beurer):
- v6.75 — _KNOWN_BRANDS: +daikin/vaillant/levoit/beurer/moulinex/krups/yamaha+:
- v6.74 — _LT_DE/PL: +vandens/vaizdo/veiksmo/sniego/šilumos standalone fallbacks:
- v6.73 — _ACCESSORY_MATCH_WORDS: +worek pyłowy/akcesoria (PL dust bag/accessories):
- v6.72 — _ACCESSORY_MATCH_WORDS: +ohrpolster/tragetasche/ersatzohrpolster:
- v6.71 — _ACCESSORY_MATCH_WORDS: +ersatzfilter/milchaufschäumer/luftfilter:
- v6.70 — _LT_DE/PL: +dujų→Gas/gazowy (gas stove/boiler); icon: +gasherd🍳:
- v6.69 — _CATEGORY_ICON_MAP: +heat pump🌬️/steam cleaner🫧/boiler🚿:
- v6.68 — _LT_DE/PL: +šilumos siurblys→Wärmepumpe/pompa ciepła; trigger: +šilumos:
- v6.67 — _NOISE_WORDS: +išpardavimas/promocja/wyprzedaż/recenzja/gdzie kupić/preisvergleich:
- v6.66 — validate_price: +pressure washer €20/lawn mower €30 floors (centai fix):
- v6.65 — _CATEGORY_ICON_MAP: +kärcher (umlaut) to power tools🔨:
- v6.64 — _LT_DE/PL: +sniego valytuvas→Schneefräse/odśnieżarka; trigger: +sniego:
- v6.63 — _LT_DE/PL: +vejapjovė→Rasenmäher/kosiarka; +kompresorius→Kompressor/kompresor:
- v6.62 — _ACCESSORY_MATCH_WORDS: +battery pack/replacement battery/akkupack/netzteil:
- v6.61 — _NOISE_WORDS: +kainos/apžvalga/pigiausias/pirkti/internetu/kur nusipirkti (cache hit boost):
- v6.60 — validate_price: _VACUUM_W +siurblys/dulkiu siurblys; _SPEAKER_W +sonos/harman kardon €50 floor:
- v6.59 — validate_price: +fernseher/telewizor to _TV_WORDS (translated Amazon TV floor fix):
- v6.58 — validate_price: +vacuum €15/smartwatch €20 floors (centai fix for Dyson/Garmin):
- v6.57 — _LT_DE/PL: +boileris/plovykla→Hochdruckreiniger; icon: +karcher/stihl🔨 sonos/harman kardon🔊:
- v6.56 — _KNOWN_BRANDS: +sonos/harman kardon/stihl/husqvarna/worx/metabo/parkside/greenworks/ilife/cecotec/blaupunkt:
- v6.55 — _LT_DE/PL: +garų siurblys→Dampfsauger/odkurzacz parowy, +garų valytuvas→Dampfreiniger/myjka parowa:
- v6.54 — _ACCESSORY_MATCH_WORDS: +systainer (Festool carry case); 97 tests:
- v6.53 — validate_price: +robot vacuum €50/gaming console €100 price floors:
- v6.52 — _NOISE_WORDS: +discount/sale/angebote/oferta/rabat/akcija/nuolaida (cache hit boost):
- v6.51 — _ACCESSORY_MATCH_WORDS: +strap/dirželis/armband/pasek (watch strap gaps):
- v6.50 — _KNOWN_BRANDS: +epson/dreame/ecovacs/eufy/milwaukee/ryobi/festool/einhell/weber/instant/vitamix:
- v6.49 — _NOISE_WORDS: +kaip nusipirkti/kur rasti/palyginti/compare/vergleichen (cache hit boost):
- v6.48 — _LT_CATEGORY_WORDS/DE/PL: +žaislai (toy plural) translation miss fix:
- v6.47 — _KNOWN_BRANDS: +poco/redmi/nothing; icon map: +nothing phone:
- v6.46 — _LT_CATEGORY_WORDS: remove duplicate viryklė; cache_stats: "query"→"product_name":
- v6.45 — _LT_CATEGORY_WORDS: +genitive triggers (svarstyklių/čiužinio/kietojo/indų):
- v6.44 — scan-image AI prompt: +barcode instruction, +key specs in product_name:
- v6.43 — icon: robot kuchenny/küchenmaschine/thermomix → 🍳 (not 🤖 robot vacuum):
- v6.43 — Elesen centai fix: skip conversion when price text has decimal separator:
- v6.41 — +šepetėlis trigger/translation (toothbrush LT→DE/PL); version strings:
- v6.40 — icon +bohrmaschine/wiertarka/perforatorius to 🔨 power tools:
- v6.39 — _varle_from_next_data: comma-decimal price fix; list[:40] (was :30):
- v6.38 — icon 🪒 +oral-b/toothbrush/zahnbürste/šepetėlis/szczoteczka:
- v6.37 — icon fix: monitor→🖥️ (was 📺); +display/monitorius/bildschirm to monitor entry:
- v6.36 — accessory filter: 'remote' → 'remote control' (prevents false-hide of presentation remotes):
- v6.35 — render_js 6s (fits 8s stream timeout); +brands honor/vivo/fujifilm/oral-b; _walk depth 12; SPA keys expanded:
- v6.34 — LT shops: direct(2s) → render_js=True(7s), within 9s pool timeout:
- v6.33 — LT shop render_js fallback helpers (_scrape_*_from_html refactor):
- v6.32 — icon fixes: nesiojamas→nesiojamas kompiuteris💻; lempute💡; robotinis🤖:
- v6.31 — phone📱 brands (motorola/honor/realme/oppo/vivo); ps5/ps4🎮; fix aparat→aparat foto📷:
- v6.30 — icon keyword fixes: bügeleisen👕 umlaut; sviestuvai/prozektorius💡 norm:
- v6.29 — ☕coffee/kettle split from 🍳; 🤖robot vacuum; 🛴scooter split; DE/PL icon gaps:
- v6.28 — TV📺/vacuum🧹/washing🫧 DE+PL icon keywords; fridge cleanup:
- v6.27 — fridge❄️/AC🌬️ split; projector📽️; juicer🥤 backend icons:
- v6.26 — alarm/lamp backend icons; vaizdo/veiksmo LT triggers; scan executor cleanup:
- v6.25 — _ph_exec.shutdown in finally (GeneratorExit cleanup fix):
- v6.24 — žadintuvas→Wecker/budzik; lempa→Lampe/lampa; router/mic/keyboard icons:
- v6.23 — mikrofonas→Mikrofon/mikrofon; maršrutizatorius→Router; išmanioji→Smart:
- v6.16 — garų→Dampf/parowy standalone; nešiojamas+product translation fixes:
- v6.15 — nešiojamas+product fixes: kondicionierius/siurblys/pjūklas no longer→Laptop:
- v6.14 — relevance filter in Elesen/Pigu/Topo DOM scrapers (was only in SPA/Amazon):
- v6.13 — standalone fallback translations: kondicionierius/valytuvas/robotas/kampinis:
- v6.12 — _varle_from_next_data: early relevance filter (matches _walk_for_products):
- v6.11 — _CATEGORY_ICON_MAP: speaker🔊, mouse🖱️, iron👕 icons:
- v6.10 — diskas→Festplatte, lygintuvas→Bügeleisen, nešiojamas garsiakalbis fix:
- v6.9 — _LT_PL storage/keyboard translations: kietasis diskas, atmintinė, mechaninė:
- v6.8 — LT translations: garsinė/kolonėlė→Lautsprecher, kampinis šlifuoklis/suktukas:
- v6.7 — MAIN_PRODUCT_KEYWORDS +power tools (LT/DE/PL); classify correctly < €150:
- v6.6 — Power tool translations: šlifuoklis/suktukas→Schleifer/Schrauber (DE/PL):
- v6.5 — _KNOWN_BRANDS: +15 EU appliance brands (AEG, Zanussi, Liebherr, Beko, Gorenje etc.):
- v6.4 — Early relevance filter in scrape_amazon: accessories skipped before price parse:
- v6.3 — Fix startup version string; frontend _getIcon power-tool/treadmill icons:
- v6.2 — Early relevance filter in _walk_for_products: irrelevant SPA items skipped before filling 8-slot cap:
- v5.96 — Amazon scraper: scan up to 8 items (was 5) for better relevance filtering:
- v5.95 — fix get_category_icon: normalize LT diacritics; add siurblys/ausinukai/gruzdintuve icons:
- v5.94 — fix LT trigger words: gruzdintuvė, plakiklis, garso, namų, kino, vandens, robotinis:
- v5.93 — LT translation dict: robot vacuum, soundbar, video camera, air fryer:
- v5.92 — user-agent refresh (Chrome 136) + startup version fix:
- v5.91 — streaming _trans_pool cleanup on client disconnect (try/finally):
- v5.90 — health endpoint version + shops list corrected:
- Relevance filter now runs BEFORE dedup (keeps cheapest relevant result per shop)
- Barcode results cached in-memory permanently (barcodes don't change)
- SPA extractor: +Nuxt2 window.__NUXT__, +productList/searchResults, +more price/URL fields
- /api/watchlist-check: Supabase-based price check for watchlist items (no ScraperAPI)
- Popular searches persisted to Supabase searches table (survives restarts)
- v5.67 — query normalization:
- normalize_query strips shopping-intent noise words (buy, kur pirkti, cheap, review, etc.)
  in LT/DE/PL/EN so "kur pirkti iPhone 16" hits same cache as "iPhone 16"
- v5.66 — AI and deal_score improvements:
- build_ai_prompt: includes spread %, at-historical-low signal, 5 shops (was 4)
- deal_score: extra +10 bonus when current price is at 30d historical low
- v5.65 — search quality:
- Cache version bumped to v64 (invalidates stale pre-Pigu/Topo results)
- v5.64 — diacritics-insensitive LT query detection via _is_lt_query
- v5.63 — translation improvements:
- _static_translate: diacritics-insensitive matching (ą→a, č→c, etc.) — no-accent queries now work
- Added 20+ new LT product categories: smartwatch, earbuds, juicer, hair straightener, food processor,
  humidifier, thermometer, game console, treadmill, bread maker, player, charger, projector
- v5.62 — scraper improvements:
- Pigu.lt: corrected search URL (searchPhrase param), direct-first + DOM fallback
- Topo: direct-first + DOM fallback
- v5.60: added Pigu + Topo to all 3 search endpoints, 6 shops total
- v5.59 — UX improvements:
- barcode lookup concurrent (4s timeout vs 10s sequential)
- /api/popular-searches public (was always returning 401 to frontend)
- 500/404 error handlers added
- v5.58: security + rate limiting hardening:
- get_client_ip: rightmost XFF IP (Render-safe, blocks spoofing)
- per-minute rate limit: 20 req/min per IP (burst protection)
- v5.57: affiliate click tracking:
- /api/track POST: logs shop + query on each buy-button click (fire-and-forget)
- /api/click-stats GET: returns click counts per shop
- v5.56: speed + accuracy improvements:
- LT shops (Varle/Elesen) now start immediately in parallel with translation; Amazon
  added after translation completes → saves 1-3s when static dict misses and Claude API
  is called (applies to both /api/search and /api/search-stream)
- v5.55: translation coverage fix, new LT vocab, Amazon price whole+fraction fallback
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
    "kavos", "virdulys", "keptuvė", "mikseris", "blenderis",
    "džiovintuvas", "laidynas", "orkaitė", "indaplovė",
    "kondicionierius", "šildytuvas", "projektorius",
    "dviratis", "paspirtukas", "bėgimo", "laikrodis",
    # Lithuanian power tools
    "grąžtas", "pjūklas", "perforatorius", "šlifuoklis", "suktukas",
    # German appliances
    "rasierer", "waschmaschine", "kühlschrank", "staubsauger",
    "kaffeemaschine", "wasserkocher", "projektor", "laufband",
    "bohrmaschine", "schleifer", "winkelschleifer", "akkuschrauber",
    # Polish appliances
    "golarka", "pralka", "lodówka", "odkurzacz",
    "ekspres", "czajnik", "rower", "hulajnoga",
    "wiertarka", "szlifierka", "wkrętarka",
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
    'garmin', 'fitbit', 'fossil', 'jabra', 'sennheiser', 'miele', 'whirlpool',
    'nespresso', 'irobot', 'roomba', 'makita', 'dewalt', 'lego', 'shure',
    # European appliance brands common in LT market
    'aeg', 'zanussi', 'liebherr', 'gorenje', 'indesit', 'beko', 'candy', 'haier',
    'ninja', 'kitchenaid', 'smeg', 'melitta', 'sage', 'russell', 'breville',
    'grundig', 'ariston', 'hotpoint', 'bauknecht', 'constructa',
    # Sports / wearables / cameras
    'polar', 'suunto', 'gopro', 'dji', 'nokia', 'roborock', 'beats', 'marshall',
    # Phone brands in icon map but missing from brand matching
    'honor', 'vivo', 'poco', 'redmi', 'nothing',
    # Camera brands
    'fujifilm', 'olympus', 'leica',
    # Personal care
    'oral-b',
    # Printers
    'epson',
    # Robot vacuum brands popular in EU
    'dreame', 'ecovacs', 'eufy',
    # Power tools
    'milwaukee', 'ryobi', 'festool', 'einhell',
    'stihl', 'husqvarna', 'worx', 'metabo', 'parkside', 'greenworks',
    # Other EU-market brands
    'weber', 'instant', 'vitamix',
    # Smart speakers / audio
    'sonos', 'harman kardon',
    # Budget/mid-range brands in EU market
    'ilife', 'cecotec', 'blaupunkt',
    # HVAC / heating brands (popular in LT for heat pumps, boilers)
    'daikin', 'vaillant', 'viessmann', 'mitsubishi electric', 'gree', 'baxi',
    # ariston already in set above
    # Air quality / purifiers (popular EU market)
    'levoit', 'blueair', 'coway', 'winix', 'xiaomi air',
    # Health / medical devices
    'beurer', 'omron', 'medisana', 'withings',
    # Kitchen appliances (popular in LT)
    'moulinex', 'krups', 'severin', 'cuisinart', 'bomann',
    # Home appliances (premium/built-in)
    'neff', 'asko',  # smeg already in set above
    # Audio / home cinema
    'yamaha', 'denon', 'pioneer', 'onkyo', 'marantz', 'audio-technica',
    # Networking / smart home
    'ubiquiti', 'zyxel', 'netgear', 'tp-link', 'fritzbox', 'avm',
    # GPU / PC component brands
    'gigabyte', 'msi', 'zotac', 'sapphire',
}
_ACCESSORY_MATCH_WORDS = frozenset({
    'case', 'cover', 'sleeve', 'bumper', 'wallet', 'skin', 'sticker', 'decal',
    'holder', 'stand', 'mount', 'cradle', 'dock', 'bracket', 'grip',
    'charger', 'cable', 'adapter', 'hub', 'extender', 'splitter', 'dongle',
    'screen protector', 'tempered glass', 'film', 'foil',
    'replacement', 'spare', 'repair', 'filter', 'bag', 'brush', 'attachment',
    'earpad', 'eartip', 'ear tip', 'cushion', 'pad',
    'stylus', 'remote control', 'controller',
    # NOTE: 'headset' intentionally omitted — over-ear headphones are often marketed as headsets
    # (e.g. "Sony WH-1000XM5 Wireless Headset") and would be incorrectly filtered.
    'watch band', 'sport band', 'fitness band', 'wristband', 'band', 'strap',
    'dėklas', 'maišelis', 'rankinė', 'stovas', 'laikiklis', 'dirželis',
    'kroviklis', 'kabelis', 'plėvelė', 'stikliukas', 'apsauga',
    'etui', 'obudowa', 'pokrowiec', 'ładowarka', 'kabel', 'szkło', 'folia',
    'uchwyt', 'podstawka', 'naklejka', 'ochraniacz', 'filtr', 'pasek',
    'hülle', 'tasche', 'schutzhülle', 'ladegerät', 'halterung', 'schutzglas',
    'ersatz', 'zubehör', 'armband',
    # LT plural accessory forms
    'maišeliai', 'filtrai', 'filtras', 'priedai', 'priedas', 'laikiklis',
    # Multi-word accessory phrases
    'cleaning kit', 'cleaning brush', 'carry bag', 'carry case', 'screen film',
    'wall mount', 'power bank', 'spare part',
    'battery pack', 'replacement battery',
    # Festool-specific storage system (Systainer = proprietary carry case)
    'systainer',
    # German tool battery pack / power supply accessories
    'akkupack', 'netzteil', 'akku-pack',
    # German compound accessories with "Ersatz-" prefix (whole-word "ersatz" doesn't match inside these)
    'ersatzfilter', 'ersatzteil', 'ersatzakku', 'ersatzohrpolster',
    # Coffee machine accessories
    'milchaufschäumer', 'milchaufschaumer', 'entkalkungstabletten', 'reinigungstabletten',
    # Heat pump / HVAC filter accessories
    'luftfilter',
    # Headphone / audio accessories (German)
    'ohrpolster', 'ohrkissen', 'kopfpolster',
    # Carry bag / case (German) — not caught by "tasche" since it's a suffix
    'tragetasche', 'tragegurt', 'schutztasche',
    # Polish accessory words
    'worek pyłowy', 'akcesoria',
    # Printer consumables — always accessories for printer queries
    'toner',
    # German wall mount (more specific than "halterung")
    'wandhalterung',
    # German spare parts plural
    'ersatzteile',
    # LT plural accessory forms
    'dėklai', 'krovikliai', 'kabeliai',
    # Robot vacuum / floor cleaning accessories (German)
    'ersatzbürste', 'seitenbürste', 'hauptbürste', 'wischpad', 'mopppad', 'waschbarer',
    # Cartridge / consumable (printer, filter, water)
    'cartridge', 'refill',
    # Ink (printer consumable — whole-word only, so no false match in "link" etc.)
    'ink cartridge', 'druckerpatrone',
    # German vacuum bags (whole-word; staubsaugerbeutel won't match inside longer compound words)
    'staubsaugerbeutel', 'ersatzbeutel',
    # German toner cartridge
    'tonerkassette',
})
_VARIANT_WORDS = frozenset({
    'pro', 'max', 'ultra', 'plus', 'lite', 'mini', 'fe', 'edge',
    'note', 'fold', 'flip', 'air', 'neo', 'active', 'sport',
    'slim', 'boost', 'titan',
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
    # Position-sensitive check for "headset": over-ear headphones are often sold as "headsets".
    # Filter only when "headset" appears BEFORE any query word (accessory phrasing like
    # "Bluetooth Headset for iPhone 17"), not when it's a suffix ("Sony WH-1000XM5 Headset").
    if 'headset' not in q and re.search(r'(?<![a-z])headset(?![a-z])', t):
        q_words_pos = re.findall(r'[a-z0-9]{2,}', q)
        headset_pos = t.find('headset')
        first_q_pos_in_t = next(
            (t.find(w) for w in q_words_pos if t.find(w) >= 0),
            len(t)
        )
        if headset_pos < first_q_pos_in_t:
            return False  # "Headset ... for [product]" pattern → accessory
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
        # Normalize model: strip hyphens for compact-model comparison (wh-1000xm5 → wh1000xm5)
        t_nh = t.replace("-", "").replace(" ", "")
        def _model_in_title(m):
            m_nh = m.replace("-", "")
            # Strict word-boundary check first
            if re.search(r'(?<![a-z0-9])' + re.escape(m) + r'(?![a-z0-9])', t):
                return True
            # Compact model (e.g. WH1000XM5 contains 1000xm5 token)
            if m_nh and m_nh in t_nh:
                return True
            return False
        if not all(_model_in_title(m) for m in model_tokens):
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
_click_counts: dict = {}   # shop → number of buy-button clicks
_cache_hits: int = 0
_cache_misses: int = 0
_server_start: float = time.time()

_CATEGORY_ICON_MAP = [
    (["iphone", "samsung galaxy", "xiaomi", "oneplus", "pixel", "telefon", "smartphone",
      "galaxy s", "galaxy a", "redmi", "poco", "motorola", "honor", "realme", "oppo", "vivo", "nothing phone"], "📱"),
    (["macbook", "laptop", "notebook", "thinkpad", "dell xps", "asus", "surface pro",
      "chromebook", "nesiojamas kompiuteris"], "💻"),
    (["ipad", "galaxy tab", "tablet"], "📱"),
    (["oled", "qled", " tv ", " tv", "tv ", "television", "televizorius", "fernseher",
      "telewizor", "ekranas", "screen", "55\"", "65\"", "43\""], "📺"),
    (["headphone", "earphone", "earbuds", "ausines", "ausinukai", "airpods", "wh-1000", "bose qc",
      "jabra", "beats", "marshall", "kopfhörer", "słuchawki", "audio-technica"], "🎧"),
    (["playstation", "ps5", "ps4", "xbox", "nintendo", "gamepad", "rtx 4", "rtx 3",
      "geforce", "gaming", "spielkonsole", "konsola", "konsole",
      "gigabyte", "msi", "zotac", "sapphire"], "🎮"),
    (["camera", "nikon", "canon", "sony zv", "sony alpha", "fotoaparatas", "mirrorless", "dslr",
      "gopro", "dji", "aparat foto", "aparat cyfr", "fujifilm", "olympus"], "📷"),
    (["roomba", "roborock", "irobot", "robot siurblys", "robotinis", "saugroboter",
      "dreame", "ecovacs", "eufy"], "🤖"),
    # Heat pump must come before generic "siurblys"→🧹 so "silumos siurblys" matches here first
    (["wärmepumpe", "warmepumpe", "pompa ciepla", "silumos siurblys", "silumos pompa", "heat pump", "daikin"], "🌬️"),
    # Steam cleaner / steam mop — before generic vacuum entry
    (["dampfreiniger", "myjka parowa", "garu valytuvas", "dampfsauger", "odkurzacz parowy",
      "steam cleaner", "steam mop"], "🫧"),
    (["dulkiu siurblys", "siurblys", "vacuum", "dyson v", "miele",
      "staubsauger", "odkurzacz"], "🧹"),
    (["skalbykle", "washing machine", "waschmaschine", "pralka", "indaplove",
      "dishwasher", "spülmaschine", "zmywarka", "bosch wan", "samsung ww",
      "asko", "bauknecht", "constructa"], "🫧"),
    (["virdulys", "kettle", "kavos", "nespresso", "wasserkocher", "kaffeemaschine",
      "czajnik", "ekspres"], "☕"),
    (["keptuve", "blender", "mikser", "multicooker", "air fryer", "gruzdintuve",
      "robot kuchenny", "kuchenny", "thermomix", "küchenmaschine", "maisto procesorius",
      "gasherd", "kuchenka gazowa", "duju virykle", "virykle", "induktion",
      "indukcinis", "indukcine", "kaitlente", "kochfeld",
      "moulinex", "krups", "cuisinart", "neff", "severin", "bomann"], "🍳"),
    (["lego", "zaislai", "pampers", "chicco", "fisher-price", "baby"], "🧸"),
    (["monitor", "monitorius", "gaming monitor", "display", "bildschirm", "ekran komputerowy"], "🖥️"),
    (["ssd", "nvme", "hdd", "ram ddr", "corsair", "kingston fury",
      "procesorius", "cpu", "ryzen", "core i", "festplatte", "dysk ssd"], "🖥️"),
    (["spausdintuvas", "printer", "scanner", "hp laserjet", "epson", "drucker", "drukarka"], "🖨️"),
    (["air purifier", "luftreiniger", "oczyszczacz powietrza", "oro valytuvas",
      "levoit", "blueair", "coway", "winix"], "💨"),
    (["luftbefeuchter", "oro drekintuvas", "nawilżacz powietrza", "humidifier"], "💧"),
    (["svarstykles", "körperwaage", "korperwaage", "body scale", "body fat scale",
      "personenwaage", "waga lazienkowa"], "⚖️"),
    (["beurer", "omron", "medisana", "withings", "blood pressure", "kraujospy dis",
      "tensiometro", "cisnienomierz"], "🩺"),
    (["philips shav", "braun series", "gillette", "oral-b", "skustuvas", "epilator",
      "toothbrush", "zahnbürste", "sepetelis", "šepetėlis", "szczoteczka"], "🪒"),
    (["laikrodis", "smartwatch", "apple watch", "garmin", "fitbit", "samsung watch", "fossil", "polar", "suunto",
      "zegarek"], "⌚"),
    (["paspirtukas", "e-roller", "elektroroller", "hulajnoga elektryczna"], "🛴"),
    (["dviratis", "elektrinis dviratis", "e-bike", "ebike", "scooter", "fahrrad", "rower"], "🚲"),
    (["saldytuvas", "saldiklis", "saldymo", "kühlschrank", "gefrierschrank",
      "lodówka", "zamrażarka", "lodowka", "zamrazarka"], "❄️"),
    (["kondicionierius", "oro kondicionierius", "klimaanlage", "klimatyzator"], "🌬️"),
    (["makita", "dewalt", "bosch gsr", "graztas", "pjuklas", "power tool", "drill", "grąžtas",
      "šlifuoklis", "slifuoklis", "suktukas", "kampinis", "winkelschleifer", "schleifer",
      "schrauber", "bohrmaschine", "szlifierka", "wiertarka", "wkrętarka", "perforatorius",
      "karcher", "kärcher", "hochdruckreiniger", "myjka cisnieniowa", "plovykla", "stihl", "husqvarna"], "🔨"),
    (["begimu takelis", "begimo takelis", "laufband", "treadmill", "treniruoklis", "bieżnia"], "🏃"),
    (["projektorius", "projector", "projektor", "beamer"], "📽️"),
    (["sulciaspaude", "sulciu", "juicer", "entsafter", "wyciskarka"], "🥤"),
    (["garsiakalbis", "garsine", "kolonele", "soundbar", "lautsprecher", "głośnik", "speaker",
      "tragbarer lautsprecher", "głośnik przenośny", "sonos", "harman kardon",
      "yamaha", "denon", "marantz", "pioneer", "onkyo"], "🔊"),
    (["pelė", "pele", "maus", "mouse", "mysz"], "🖱️"),
    (["laidynas", "lygintuvas", "bügeleisen", "bugeleisen", "żelazko", "dampfbügeleisen", "dampfbugeleisen"], "👕"),
    (["ziuronai", "fernglas", "lornetka", "binocular"], "🔭"),
    (["mikrofonas", "microphone", "mikrofon", "condenser mic", "podcast"], "🎙️"),
    (["marsrutizatorius", "router", "mesh wifi", "access point", "switch", "tinklo",
      "tp-link", "ubiquiti", "netgear", "zyxel", "fritzbox", "fritz!box"], "🌐"),
    (["klaviatura", "klaviatūra", "keyboard", "klawiatura", "tastatur", "mechanine"], "⌨️"),
    (["zadintuvas", "zadintuva", "wecker", "budzik", "alarm clock"], "⏰"),
    (["lempa", "lampe", "lampa", "lempute", "lemputes", "led juosta", "led strip", "led lamp", "smart lamp",
      "sviestuvas", "sviestuvai", "prozektorius"], "💡"),
    (["boileris", "bojler", "warmwasserbereiter", "podgrzewacz wody",
      "vandens sildytuvas", "water heater", "katilas", "gaskessel", "kociol",
      "vaillant", "viessmann", "baxi", "ariston"], "🚿"),
    (["nokia"], "📱"),
]


def get_category_icon(query: str, product_type: str = "MAIN") -> str:
    q = _norm_lt(query.lower())
    for keywords, icon in _CATEGORY_ICON_MAP:
        if any(kw in q for kw in keywords):
            return icon
    return "🛍️" if product_type == "ACCESSORY" else "🛒"


_NOISE_WORDS = re.compile(
    r'\b(buy|kur pirkti|kaip nusipirkti|kur rasti|where to buy|cheap|pigiau|best price|geriausia kaina|'
    r'billig|günstig|online|price|kaina|kainos|preis|cena|review|atsiliepimas|apžvalga|bewertung|opinia|'
    r'pigiausiai|pigiausias|pigiausia|kur pigiausia|cheapest|best deal|billigste|najtaniej|order|bestellen|zamów|'
    r'compare|palyginti|vergleichen|porównaj|'
    r'discount|sale|angebote|oferta|rabat|akcija|nuolaida|nuolaidos|'
    r'pirkti|internetu|kur nusipirkti|išpardavimas|'
    r'promocja|wyprzedaż|recenzja|gdzie kupić|preisvergleich|'
    r'lietuva|lietuvoje|vokietija|vokietijoje|lenkija|lenkijoje|anglijoje|'
    r'deutschland|polska|in deutschland|in poland)\b',
    re.IGNORECASE
)


def normalize_query(query: str) -> str:
    """Normalize a search query so minor variations hit the same cache entry."""
    q = query.strip()
    q = re.sub(r'\s+', ' ', q)
    q = q.rstrip('.,;:!?')
    # Strip shopping-intent noise words that don't help scraper results
    q = _NOISE_WORDS.sub('', q)
    q = re.sub(r'\s+', ' ', q).strip()
    return q or query.strip()  # never return empty


def resolve_query(query: str) -> str:
    """If query is a barcode (digits only, 8-14 chars, spaces allowed), look up the product name."""
    candidate = re.sub(r'\s+', '', query)
    if re.match(r'^\d{8,14}$', candidate):
        name = lookup_barcode_free(candidate)
        if name:
            print(f"[Barcode] {candidate} -> {name}")
            return name
    return query


def suggest_simpler_query(query: str) -> str:
    words = query.strip().split()
    if len(words) <= 2:
        return ""
    # Keep 3 tokens for long queries (more specific suggestion)
    return " ".join(words[:3]) if len(words) >= 5 else " ".join(words[:2])


def _sb_upsert_search(query: str, count: int):
    """Persist search count to Supabase `searches` table (fire-and-forget).
    Table DDL: CREATE TABLE searches (query text PRIMARY KEY, count int DEFAULT 1,
               last_seen timestamptz DEFAULT now());
    """
    sb = get_supabase()
    if not sb:
        return
    try:
        # Use max(existing, in-memory) so counts only ever increase
        sb.table("searches").upsert(
            {"query": query, "count": count, "last_seen": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())},
        ).execute()
    except Exception:
        pass


def _sb_load_search_counts():
    """Load persisted search counts from Supabase into in-memory dict on startup."""
    rows = _sb_get_popular_searches(200)
    for row in rows:
        q = row.get("query", "")
        c = int(row.get("count", 0))
        if q and c > 0:
            _search_counts[q] = max(_search_counts.get(q, 0), c)


def _sb_get_popular_searches(limit: int = 10) -> list:
    """Fetch most searched queries from Supabase."""
    sb = get_supabase()
    if not sb:
        return []
    try:
        resp = (
            sb.table("searches")
            .select("query, count")
            .order("count", desc=True)
            .limit(limit)
            .execute()
        )
        return resp.data or []
    except Exception:
        return []


def track_search(query: str):
    key = re.sub(r'\s+', ' ', query.lower().strip())
    if key and len(key) >= 2:
        _search_counts[key] = _search_counts.get(key, 0) + 1
        count = _search_counts[key]
        threading.Thread(target=_sb_upsert_search, args=(key, count), daemon=True).start()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
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
_barcode_cache: dict = {}  # barcode → product_name (permanent, barcodes don't change)

def lookup_barcode_free(barcode: str) -> str:
    """Looks up product name from EAN/UPC barcode using free APIs concurrently."""
    barcode = barcode.strip()
    if not re.match(r'^\d{8,14}$', barcode):
        return ""
    if barcode in _barcode_cache:
        return _barcode_cache[barcode]

    def _off():
        try:
            resp = _http.get(
                f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json",
                timeout=4,
                headers={"User-Agent": "GoodyApp/1.0 (price comparison)"},
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == 1:
                    p = data.get("product", {})
                    name = (p.get("product_name_en") or p.get("product_name") or p.get("generic_name") or "").strip()
                    if name:
                        brand = p.get("brands", "").split(",")[0].strip()
                        return f"{brand} {name}".strip() if brand and brand.lower() not in name.lower() else name
        except Exception as e:
            print(f"[OpenFoodFacts] {e}")
        return ""

    def _upc():
        try:
            resp = _http.get(
                f"https://api.upcitemdb.com/prod/trial/lookup?upc={barcode}",
                timeout=4,
                headers={"User-Agent": "GoodyApp/1.0"},
            )
            if resp.status_code == 200:
                items = resp.json().get("items", [])
                if items:
                    return items[0].get("title", "").strip()
        except Exception as e:
            print(f"[UPCItemDB] {e}")
        return ""

    ex = ThreadPoolExecutor(max_workers=2)
    futs = {ex.submit(_off): "off", ex.submit(_upc): "upc"}
    try:
        for f in as_completed(futs, timeout=5):
            try:
                result = f.result(timeout=0.1)
                if result:
                    _barcode_cache[barcode] = result
                    return result
            except Exception:
                pass
    except Exception:
        pass
    finally:
        ex.shutdown(wait=False)
    _barcode_cache[barcode] = ""  # cache misses too to avoid hammering free APIs
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
    """Popular searches (searched 5+ times) get 2-hour TTL; others get 30 min."""
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
    """Return the real client IP. Render appends the real IP as the RIGHTMOST entry in
    X-Forwarded-For, so we use [-1] — the leftmost is client-controlled and spoofable."""
    xff = request.headers.get("X-Forwarded-For", "")
    if xff:
        return xff.split(",")[-1].strip()
    return request.remote_addr or "unknown"


_rate_minute_store: dict = {}  # ip → {minute: str, count: int}
MINUTE_LIMIT = int(os.getenv("MINUTE_LIMIT", "20"))  # max 20 req/min per IP


def _check_debug_auth() -> bool:
    """Return True if DEBUG_API_KEY is set and request carries it."""
    if not DEBUG_API_KEY:
        return False
    return request.headers.get("X-Debug-Key") == DEBUG_API_KEY or \
           request.args.get("key") == DEBUG_API_KEY


def rate_limit(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        ip = get_client_ip()
        today = time.strftime("%Y-%m-%d")
        minute = time.strftime("%Y-%m-%dT%H:%M")

        # Purge yesterday's entries ~1% of requests to keep memory bounded
        if random.random() < 0.01:
            stale = [k for k, v in list(rate_store.items()) if v.get("date") != today]
            for k in stale:
                rate_store.pop(k, None)
            stale_m = [k for k, v in list(_rate_minute_store.items()) if v.get("minute") != minute]
            for k in stale_m:
                _rate_minute_store.pop(k, None)

        # Per-minute limit (burst protection)
        if ip not in _rate_minute_store or _rate_minute_store[ip]["minute"] != minute:
            _rate_minute_store[ip] = {"minute": minute, "count": 0}
        _rate_minute_store[ip]["count"] += 1
        if _rate_minute_store[ip]["count"] > MINUTE_LIMIT:
            return jsonify({
                "error": "rate_limit",
                "message": f"Per daug užklausų — palaukite minutę ({MINUTE_LIMIT}/min limitas).",
                "remaining": 0,
            }), 429

        # Per-day limit
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


_TV_WORDS   = ["tv ", " tv", "televizorius", "television", "oled", "qled", "naled", "mini led", "smarttv",
               "fernseher", "telewizor"]
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
_ROBOT_VAC_W = ["roomba", "roborock", "irobot", "saugroboter", "robot siurblys", "robotinis siurblys",
                "robot odkurzający", "robot sprzątający", "dreame", "ecovacs", "eufy"]
_CONSOLE_W  = ["playstation 5", "ps5", "xbox series x", "xbox series s", "nintendo switch"]
_VACUUM_W   = ["dulkių siurblys", "dulkiu siurblys", "siurblys", "staubsauger", "odkurzacz", "vacuum cleaner", "dyson v"]
_WATCH_W    = ["apple watch", "samsung watch", "galaxy watch", "garmin", "smartwatch"]
_SPEAKER_W  = ["sonos", "harman kardon"]  # premium speakers: cheapest model >€150
_PRESSURE_W = ["hochdruckreiniger", "myjka cisnieniowa", "pressure washer", "karcher", "kärcher",
               "plovykla", "aukstojo sleglio"]  # cheapest pressure washers ~€30
_MOWER_W    = ["rasenmäher", "rasenmaher", "kosiarka", "žoliapjovė", "zoliapjove",
               "vejapjovė", "vejapjove"]  # cheapest electric mowers ~€80
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

    # Robot vacuum: > €50 (cheapest is ~€70 new)
    if any(w in q for w in _ROBOT_VAC_W) and price < 50:
        return 0.0

    # Gaming console (PS5/Xbox/Switch): > €100
    if any(w in q for w in _CONSOLE_W) and price < 100:
        return 0.0

    # Vacuum cleaner: cheapest budget vac is ~€15 — prevents centai misidentification (549 ct → €5.49)
    if any(w in q for w in _VACUUM_W) and price < 15:
        return 0.0

    # Smartwatch / fitness tracker: > €20 (cheapest Garmin/Galaxy Watch is ~€50+ new)
    if any(w in q for w in _WATCH_W) and price < 20:
        return 0.0

    # Premium speakers (Sonos/Harman Kardon): cheapest model >€150 new
    if any(w in q for w in _SPEAKER_W) and price < 50:
        return 0.0

    # Pressure washers (Kärcher K2 etc.): cheapest ~€30 — prevents centai (600 ct → €6)
    if any(w in q for w in _PRESSURE_W) and price < 20:
        return 0.0

    # Lawn mowers: even cheapest electric mower ~€80 — prevents centai (3000 ct → €30)
    if any(w in q for w in _MOWER_W) and price < 30:
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
def _extract_balanced(text: str, start: int, max_len: int = 600_000) -> str:
    """Return the balanced JSON value (array or object) starting at `start`.
    Correctly skips brackets inside quoted strings."""
    if start >= len(text):
        return ""
    opener = text[start]
    if opener not in ('[', '{'):
        return ""
    closer = ']' if opener == '[' else '}'
    depth = 0
    in_str = False
    escaped = False
    end = min(start + max_len, len(text))
    for i in range(start, end):
        c = text[i]
        if escaped:
            escaped = False
            continue
        if c == '\\' and in_str:
            escaped = True
            continue
        if c == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if c == opener:
            depth += 1
        elif c == closer:
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    return ""


def _extract_json_value(text: str, key: str) -> str:
    """Extract the full JSON array/object for `key` from text, handling nested brackets."""
    pattern = f'"{key}"\\s*:\\s*'
    m = re.search(pattern, text)
    if not m:
        return ""
    return _extract_balanced(text, m.end())


def _walk_for_products(node, query, shop, flag, base_url, src_key, out, depth=0):
    """Recursively search JSON tree for product-like objects."""
    if depth > 12 or len(out) >= 8:
        return
    if isinstance(node, dict):
        name = (node.get("name") or node.get("title") or node.get("productName")
                or node.get("fullName") or node.get("Product_name")
                or node.get("product_name") or node.get("displayName")
                or node.get("short_name") or node.get("label") or "")
        price_val = None
        for pf in ("price", "finalPrice", "priceWithVat", "currentPrice",
                   "salePrice", "regularPrice", "Price", "priceValue",
                   "discountedPrice", "listPrice", "basePrice", "priceIncVat"):
            if pf in node:
                price_val = node[pf]; break
        if price_val is None and isinstance(node.get("prices"), dict):
            price_val = (node["prices"].get("final") or node["prices"].get("regular")
                         or node["prices"].get("current") or node["prices"].get("priceWithVat"))
        if price_val is None and isinstance(node.get("price"), dict):
            price_val = node["price"].get("amount") or node["price"].get("value")
        # priceFormatted: human-readable price string like "39,99 €" — parse it
        if price_val is None and isinstance(node.get("priceFormatted"), str):
            price_val = parse_price(node["priceFormatted"]) or None

        if name and price_val is not None:
            try:
                p = float(str(price_val).replace(",", "."))
                vp = validate_price(p, query)
                if vp:
                    slug = (node.get("url") or node.get("slug") or
                            node.get("urlKey") or node.get("url_key") or
                            node.get("link") or node.get("href") or
                            node.get("productUrl") or node.get("product_url") or
                            node.get("canonical") or node.get("pageUrl") or
                            node.get("path") or "")
                    link = slug if slug.startswith("http") else f"{base_url.rstrip('/')}/{slug.lstrip('/')}"
                    # Extract product image URL if available
                    img = (node.get("imageUrl") or node.get("image_url") or
                           node.get("thumbnailUrl") or node.get("thumbnail_url") or
                           node.get("thumbnail") or node.get("mainImage") or
                           node.get("picture") or "")
                    if not img and isinstance(node.get("image"), str):
                        img = node["image"]
                    if not img and isinstance(node.get("images"), list) and node["images"]:
                        first = node["images"][0]
                        img = first if isinstance(first, str) else (first.get("url") or first.get("src") or "")
                    img = img if isinstance(img, str) and img.startswith("http") else ""
                    # Rating extraction
                    rating_val = (node.get("rating") or node.get("averageRating") or
                                  node.get("ratingAverage") or node.get("starRating") or
                                  node.get("reviewScore") or 0)
                    try:
                        rating_val = float(str(rating_val).replace(",", "."))
                        if not (0 < rating_val <= 5):
                            rating_val = 0
                    except (ValueError, TypeError):
                        rating_val = 0
                    review_count = 0
                    rc = (node.get("reviewCount") or node.get("review_count") or
                          node.get("ratingsCount") or node.get("numberOfReviews") or 0)
                    try:
                        review_count = int(rc)
                    except (ValueError, TypeError):
                        review_count = 0
                    # Original price for discount detection
                    orig_val = None
                    for opf in ("originalPrice", "oldPrice", "regularPrice", "listPrice",
                                "compareAtPrice", "strikePrice", "rrp", "msrp"):
                        if opf in node and opf != pf:
                            orig_val = node[opf]; break
                    orig_price = 0
                    if orig_val is not None:
                        try:
                            op = float(str(orig_val).replace(",", "."))
                            if op > vp:
                                orig_price = op
                        except (ValueError, TypeError):
                            pass
                    name_str = str(name)[:100]
                    if not is_relevant_result(query, name_str):
                        pass  # skip irrelevant SPA items early so they don't fill the 8-slot cap
                    else:
                        r = _make_result(shop, flag, link, vp, name_str, src_key, img)
                        if rating_val > 0:
                            r["rating"] = rating_val
                        if review_count > 0:
                            r["review_count"] = review_count
                        if orig_price > 0:
                            r["original_price"] = orig_price
                        out.append(r)
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

    # 1. Next.js __NEXT_DATA__
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

    # 1b. Nuxt 3 __NUXT_DATA__ (JSON array payload — try to extract dict items)
    nd3 = soup.find("script", {"id": "__NUXT_DATA__"})
    if nd3:
        try:
            raw3 = json.loads(nd3.string or "[]")
            # Nuxt 3 stores state as a flat array; walk each dict-like element
            node3 = raw3 if isinstance(raw3, dict) else {"items": raw3}
            _walk_for_products(node3, query, shop, flag, base_url, src_key, out)
            if out:
                print(f"[{shop}] {len(out)} via __NUXT_DATA__")
                return out
        except Exception:
            pass

    # 2. window.* state patterns in inline scripts
    for scr in soup.find_all("script", src=False):
        txt = scr.string or ""
        if len(txt) < 50:
            continue
        # 2a. Whole-object state assignments (window.__NUXT__, window.__INITIAL_STATE__, etc.)
        _state_pats = [
            r'window\.__(?:INITIAL|PRELOADED|NUXT|APP|REACT_QUERY|REDUX)_?STATE__\s*=\s*\{',
            r'window\.__NUXT__\s*=\s*\{',
            r'window\.(?:state|store|appState|pageData|__data)\s*=\s*\{',
        ]
        for pat in _state_pats:
            m = re.search(pat, txt)
            if not m:
                continue
            # String-aware balanced extraction (handles nested structures + strings with brackets)
            brace_pos = m.end() - 1  # position of the opening {
            raw = _extract_balanced(txt, brace_pos)
            if not raw or len(raw) > 500_000:
                continue
            try:
                data = json.loads(raw)
                _walk_for_products(data, query, shop, flag, base_url, src_key, out)
                if out:
                    print(f"[{shop}] {len(out)} via window state pattern")
                    return out
            except Exception:
                continue
        # 2b. Named JSON array keys — use bracket counter for correct nesting
        for key in ("products", "items", "results", "hits", "productList",
                    "searchResults", "catalogItems", "goods", "offers",
                    "data", "list", "listing", "catalog", "collection",
                    "searchData", "productSearch", "productItems", "entities"):
            raw = _extract_json_value(txt, key)
            if not raw or len(raw) > 500_000:
                continue
            try:
                data = json.loads(raw)
                node = {"items": data} if isinstance(data, list) else data
                _walk_for_products(node, query, shop, flag, base_url, src_key, out)
                if out:
                    print(f"[{shop}] {len(out)} via JSON key '{key}'")
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
                        p = float(str(price_val).replace(",", "."))
                        vp = validate_price(p, query)
                        if vp:
                            slug = node.get("url") or node.get("slug") or node.get("urlKey") or ""
                            link = slug if slug.startswith("http") else f"https://varle.lt/{slug.lstrip('/')}"
                            img = (node.get("imageUrl") or node.get("image_url") or
                                   node.get("thumbnailUrl") or node.get("thumbnail") or
                                   node.get("mainImage") or "")
                            if not img and isinstance(node.get("image"), str):
                                img = node["image"]
                            img = img if isinstance(img, str) and img.startswith("http") else ""
                            name_str = str(name_val)[:100]
                            if not is_relevant_result(query, name_str):
                                pass  # skip accessories early so they don't fill the 8-slot cap
                            else:
                                r = _make_result("Varle.lt", "🇱🇹", link, vp, name_str, "varle", img)
                                rv = node.get("rating") or node.get("averageRating") or 0
                                try:
                                    rv = float(str(rv).replace(",", "."))
                                    if 0 < rv <= 5:
                                        r["rating"] = rv
                                except (ValueError, TypeError):
                                    pass
                                rc = node.get("reviewCount") or node.get("review_count") or 0
                                try:
                                    r["review_count"] = int(rc)
                                except (ValueError, TypeError):
                                    pass
                                results.append(r)
                    except (ValueError, TypeError):
                        pass
                for v in node.values():
                    walk(v, depth + 1)
            elif isinstance(node, list):
                for item in node[:40]:
                    walk(item, depth + 1)

        walk(data)
        print(f"[Varle __NEXT_DATA__] {len(results)} products")
    except Exception as e:
        print(f"[Varle NEXT_DATA err] {e}")
    return results


def _scrape_varle_from_html(html: str, query: str) -> list:
    """Extract Varle results from HTML using all available strategies."""
    results = _varle_from_next_data(html, query)
    if results:
        return results
    results = _extract_spa_products(html, query, "Varle.lt", "🇱🇹", "https://varle.lt", "varle")
    if results:
        return results
    soup = BeautifulSoup(html, "html.parser")
    items = (soup.select(".GRID_ITEM") or
             soup.select("[class*='product-card']") or
             soup.select("[class*='product-item']") or
             soup.select("[data-product-id]"))
    print(f"[Varle DOM] {len(items)} items")
    for item in items[:8]:
        try:
            price_el = (item.select_one(".price-tag") or item.select_one(".price-value") or
                        item.select_one("[class*='price']"))
            if not price_el:
                continue
            price = validate_price(parse_price(price_el.get_text()), query)
            if not price:
                continue
            title_anchor = (item.select_one(".product-title a") or
                            item.select_one("h2 a") or item.select_one("h3 a") or
                            item.select_one("a[href*='/prekes/']") or item.select_one("a[href]"))
            name = title_anchor.get_text(strip=True)[:100] if title_anchor else query
            if not is_relevant_result(query, name):
                continue
            href = title_anchor["href"] if title_anchor and title_anchor.get("href") else ""
            link = href if href.startswith("http") else f"https://varle.lt{href}"
            img_el = item.select_one("img[src]") or item.select_one("img[data-src]")
            img_url = ""
            if img_el:
                img_url = img_el.get("src") or img_el.get("data-src") or ""
                if not img_url.startswith("http"):
                    img_url = ""
            results.append(_make_result("Varle.lt", "🇱🇹", link, price, name, "varle", img_url))
        except Exception as e:
            print(f"[Varle item] {e}")
    return results


def scrape_varle(query: str) -> list:
    url = f"https://varle.lt/search/?q={requests.utils.quote(query)}"
    # Try direct first (free, 2s). If it returns products, skip ScraperAPI entirely.
    resp = None
    try:
        resp = _http.get(url, headers=get_headers("lt"), timeout=2, allow_redirects=True)
        if resp.status_code != 200:
            resp = None
    except Exception:
        resp = None
    if resp:
        results = _scrape_varle_from_html(resp.text, query)
        if results:
            return results
    # Direct failed or returned no products — ScraperAPI with JS rendering (handles CSR shops)
    resp = fetch_url(url, "lt", render_js=True, scraper_timeout=6)
    if resp and resp.status_code == 200:
        return _scrape_varle_from_html(resp.text, query)
    print(f"[Varle] failed {resp.status_code if resp else 'no response'}")
    return []


# ── PIGU.LT ──
def _scrape_pigu_from_html(html: str, query: str) -> list:
    results = _extract_spa_products(html, query, "Pigu.lt", "🇱🇹", "https://pigu.lt", "pigu")
    if results:
        return results
    soup = BeautifulSoup(html, "html.parser")
    cards = (soup.select(".search-result-item") or
             soup.select(".product-block") or
             soup.select("[class*='product-card']") or
             soup.select("[class*='product-item']") or
             soup.select("[class*='search-item']") or
             soup.select("[data-product-id]"))
    for card in cards[:8]:
        try:
            p_el = card.select_one("[class*='price']") or card.select_one("[itemprop='price']")
            price = validate_price(parse_price(p_el.get_text() if p_el else ""), query)
            if not price:
                continue
            name_el = (card.select_one("h2") or card.select_one("h3") or
                       card.select_one("[class*='title']") or card.select_one("a"))
            name = name_el.get_text(strip=True)[:100] if name_el else query
            if not is_relevant_result(query, name):
                continue
            a_el = card.select_one("a[href]")
            href = a_el["href"] if a_el else ""
            link = href if href.startswith("http") else f"https://pigu.lt{href}"
            img_el = card.select_one("img[src]") or card.select_one("img[data-src]")
            img_url = ""
            if img_el:
                img_url = img_el.get("src") or img_el.get("data-src") or ""
                if not img_url.startswith("http"):
                    img_url = ""
            results.append(_make_result("Pigu.lt", "🇱🇹", link, price, name, "pigu", img_url))
        except Exception:
            pass
    return results


def scrape_pigu(query: str) -> list:
    url = f"https://pigu.lt/lt/search?searchPhrase={requests.utils.quote(query)}"
    resp = None
    try:
        resp = _http.get(url, headers=get_headers("lt"), timeout=2, allow_redirects=True)
        if resp.status_code != 200:
            resp = None
    except Exception:
        resp = None
    if resp:
        results = _scrape_pigu_from_html(resp.text, query)
        if results:
            print(f"[Pigu] {len(results)} results")
            return results
    resp = fetch_url(url, "lt", render_js=True, scraper_timeout=6)
    if resp and resp.status_code == 200:
        results = _scrape_pigu_from_html(resp.text, query)
        print(f"[Pigu] {len(results)} results")
        return results
    print(f"[Pigu] failed {resp.status_code if resp else 'no resp'}")
    return []


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
def _scrape_topo_from_html(html: str, query: str) -> list:
    results = _extract_spa_products(html, query, "Topo centras", "🇱🇹",
                                    "https://www.topocentras.lt", "topo")
    if results:
        return results
    soup = BeautifulSoup(html, "html.parser")
    cards = (soup.select(".product-card") or
             soup.select("[class*='product-item']") or
             soup.select("[class*='product-card']") or
             soup.select("[class*='search-result']") or
             soup.select("[data-product-id]"))
    for card in cards[:8]:
        try:
            p_el = card.select_one("[class*='price']") or card.select_one("[itemprop='price']")
            price = validate_price(parse_price(p_el.get_text() if p_el else ""), query)
            if not price:
                continue
            name_el = (card.select_one("h2") or card.select_one("h3") or
                       card.select_one("[class*='name']") or card.select_one("[class*='title']"))
            name = name_el.get_text(strip=True)[:100] if name_el else query
            if not is_relevant_result(query, name):
                continue
            a_el = card.select_one("a[href]")
            href = a_el["href"] if a_el else ""
            link = href if href.startswith("http") else f"https://www.topocentras.lt{href}"
            img_el = card.select_one("img[src]") or card.select_one("img[data-src]")
            img_url = ""
            if img_el:
                img_url = img_el.get("src") or img_el.get("data-src") or ""
                if not img_url.startswith("http"):
                    img_url = ""
            results.append(_make_result("Topo centras", "🇱🇹", link, price, name, "topo", img_url))
        except Exception:
            pass
    return results


def scrape_topo(query: str) -> list:
    url = f"https://www.topocentras.lt/search?q={requests.utils.quote(query)}"
    resp = None
    try:
        resp = _http.get(url, headers=get_headers("lt"), timeout=2, allow_redirects=True)
        if resp.status_code != 200:
            resp = None
    except Exception:
        resp = None
    if resp:
        results = _scrape_topo_from_html(resp.text, query)
        if results:
            print(f"[Topo] {len(results)} results")
            return results
    resp = fetch_url(url, "lt", render_js=True, scraper_timeout=6)
    if resp and resp.status_code == 200:
        results = _scrape_topo_from_html(resp.text, query)
        print(f"[Topo] {len(results)} results")
        return results
    print(f"[Topo] failed {resp.status_code if resp else 'no resp'}")
    return []


# ── ELESEN.LT ──
def _scrape_elesen_from_html(html: str, query: str) -> list:
    """Extract Elesen results: SPA JSON first, then DOM."""
    spa = _extract_spa_products(html, query, "Elesen.lt", "🇱🇹", "https://www.elesen.lt", "elesen")
    if spa:
        return spa
    soup = BeautifulSoup(html, "html.parser")
    items = (
        soup.select("article.product-card") or
        soup.select(".product-card.vertical") or
        soup.select(".product-card") or
        soup.select("[class*='product-item']") or
        soup.select("[class*='catalog-item']") or
        soup.select(".item-box") or
        soup.select("[data-product-id]")
    )
    print(f"[Elesen] {len(items)} items")
    results = []
    for item in items[:8]:
        try:
            price_el = item.select_one(".price") or item.select_one("[class*='price']")
            if not price_el:
                continue
            price_text = price_el.get_text()
            raw_price = parse_price(price_text)
            if not raw_price:
                continue
            # Elesen sometimes returns prices in centai (e.g. "49900" = €499).
            # Only apply centai conversion when text has NO decimal separator — "1499,00"
            # already carries the decimal and must be treated as euros, not centai.
            _pt_stripped = re.sub(r'[^\d,.]', '', price_text.strip())
            _has_decimal = bool(re.search(r'[,\.]\d{2}$', _pt_stripped))
            if raw_price >= 100 and raw_price == int(raw_price) and not _has_decimal:
                centai = round(raw_price / 100, 2)
                p_eur = validate_price(raw_price, query)
                p_cnt = validate_price(centai, query)
                if p_cnt and not p_eur:
                    raw_price = centai
                elif p_cnt and p_eur and raw_price < 50000 and centai >= 5:
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
            if not is_relevant_result(query, name):
                continue
            link_el = item.select_one("a[href]")
            href = link_el["href"] if link_el else ""
            link = href if href.startswith("http") else f"https://www.elesen.lt{href}"
            img_el = item.select_one("img[src]") or item.select_one("img[data-src]")
            img_url = ""
            if img_el:
                img_url = img_el.get("src") or img_el.get("data-src") or ""
                if not img_url.startswith("http"):
                    img_url = ""
            results.append(_make_result("Elesen.lt", "🇱🇹", link, price, name, "elesen", img_url))
        except Exception as e:
            print(f"[Elesen item] {e}")
    return results


def scrape_elesen(query: str) -> list:
    url = f"https://www.elesen.lt/paieska?q={requests.utils.quote(query)}"
    resp = None
    try:
        resp = _http.get(url, headers=get_headers("lt"), timeout=2, allow_redirects=True)
        if resp.status_code != 200:
            resp = None
    except Exception:
        resp = None
    if resp:
        results = _scrape_elesen_from_html(resp.text, query)
        if results:
            print(f"[Elesen] {len(results)} results")
            return results
    resp = fetch_url(url, "lt", render_js=True, scraper_timeout=6)
    if resp and resp.status_code == 200:
        results = _scrape_elesen_from_html(resp.text, query)
        print(f"[Elesen] {len(results)} results")
        return results
    print(f"[Elesen] failed {resp.status_code if resp else 'no resp'}")
    return []


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

        for item in items[:8]:
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
                if not is_relevant_result(query, name):
                    continue  # skip accessories before expensive price parsing

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

                # Fallback: span.a-color-base with currency symbol (used in some Amazon DE layouts)
                if not raw:
                    cur_sym = "zł" if domain == "pl" else "€"
                    for el in item.find_all("span", class_="a-color-base"):
                        txt = el.get_text(strip=True)
                        if cur_sym in txt or "EUR" in txt:
                            raw = parse_price(txt)
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
                img_el = item.select_one("img.s-image") or item.select_one("img[class*='s-image']")
                image_url = img_el["src"] if img_el and img_el.get("src") else ""

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
                    "product_title": name[:80],
                    "image_url": image_url,
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


def _make_result(shop, flag, link, price, name, source, image_url=""):
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
        "product_title": name,
        "image_url": image_url,
    }


# ── TRANSLATION ──
_translate_cache: dict = {}

_LT_NORM_TABLE = str.maketrans("ąčęėįšųūžĄČĘĖĮŠŲŪŽ", "aceeisuuzACEEISUUZ")


def _norm_lt(s: str) -> str:
    """Strip Lithuanian diacritics for accent-insensitive matching."""
    return s.translate(_LT_NORM_TABLE)


# Lithuanian category words that trigger translation for Amazon DE/PL search
_LT_CATEGORY_WORDS = [
    "ausines", "ausinės", "ausinis", "siurblys", "siurblio", "dulkių",
    "skalbyklė", "skalbyklės", "skustuvas", "skustuvo", "telefonas",
    "televizorius", "televizoriaus", "kompiuteris", "planšetė", "kamera",
    "virdulys", "keptuvė", "puodas", "šaldytuvas", "mikrobangų",
    "kavos", "žaislas", "žaislo", "žaislai", "laidynas", "džiovintuvas",
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
    # New product categories
    "dviratis", "paspirtukas", "maišytuvas",
    # Missing trigger words for existing dict entries
    "šaldymo", "valytuvas",
    # Watches, wearables, earbuds
    "laikrodis", "laikrodukas", "ausinukai", "ausinuko",
    # Kitchen / food
    "sulčiaspaudė", "kepyklė", "maisto",
    # Hair / personal care
    "tiesintuvas",
    # Air quality
    "drėkintuvas", "termometras",
    # Gaming, fitness, multimedia
    "žaidimų", "bėgimo", "grotuvas", "įkroviklis", "projektorius",
    # Air fryer (new dict entries from v5.93)
    "gruzdintuvė", "gruzdintuve",
    # Hand mixer / beater
    "plakiklis",
    # Sound system / home cinema
    "garso", "namų", "kino",
    # Water filter
    "vandens",
    # Robot vacuum (standalone "robotinis")
    "robotinis",
    # Juicer (sulčių spaustuvas has dict entry but "spaustuvas" was not a trigger)
    "spaustuvas",
    # Fitness band (sporto apyrankė has dict entry but "apyrankė" was not a trigger)
    "apyrankė", "apyranke",
    # Binoculars
    "žiūronai", "ziuronai",
    # Hair curler
    "garbanojimo",
    # Power tools
    "grąžtas", "pjūklas", "perforatorius",
    "šlifuoklis", "suktukas", "kampinis",
    # Speaker variants (garsinė/kolonėlė not covered by garsiakalbis/garso)
    "garsinė", "garsine", "kolonėlė", "kolonele",
    # Storage / external drives (išorinė/atmintinė/diskas)
    "atmintinė", "atmintine", "diskas", "kietasis", "išorinė", "isorine",
    # Keyboard adjective (mechaninė not covered by klaviatūra alone)
    "mechaninė", "mechanine",
    # Iron variant (lygintuvas = laidynas synonym) + steam prefix
    "lygintuvas", "garų",
    # Electric adjective (elektrinis grąžtas etc. already have multi-word entries;
    # this standalone catches "Marka elektrinis X" where X has no dict entry)
    "elektrinis", "elektrine",
    # Smart adjective (išmanusis laikrodis already handled; standalone catches others)
    "ismanius", "ismanusis",
    # Smart adjective feminine form
    "išmanioji", "ismanioji",
    # Microphone
    "mikrofonas",
    # Router / network
    "maršrutizatorius", "marsrutizatorius",
    # Alarm clock
    "žadintuvas", "zadintuvas",
    # Lamp / lighting
    "lempa",
    # Keyboard (trigger for icon; klaviatūra already translates it)
    "klaviatura",
    # Video / action camera (dict has entries but triggers were missing)
    "vaizdo", "veiksmo",
    # Electric toothbrush / personal care (Oral-B šepetėlis etc.)
    "šepetėlis", "sepetelis",
    # Genitive forms in dict but missing from trigger (so _is_lt_query detects them)
    "svarstyklių",  # genitive of svarstyklės (scale)
    "čiužinio",     # genitive of čiužinys (mattress)
    "kietojo",      # genitive of kietasis diskas (HDD)
    "indų",         # indų plovyklė → dishwasher (indaplovė only covers nominative)
    # Water heater / boiler (common LT purchase)
    "boileris", "šildytuvas",
    # Pressure washer
    "plovykla", "slėginė",
    # Lawn mower variant (vejapjovė = alternative to žoliapjovė, not always used)
    "vejapjovė", "vejapjove",
    # Air compressor (kompresorius not covered by other entries)
    "kompresorius", "kompresoriaus",
    # Snow blower (common LT winter purchase)
    "sniego",
    # Heat pump (expensive, commonly searched)
    "šilumos", "silumos",
    # Gas appliances (dujų viryklė = gas stove, dujų katilas = gas boiler)
    "dujų", "duju",
    # Induction adjective (indukcinis kaitvietas = induction hob)
    "indukcinis", "indukcine",
    # Stand mixer / food processor
    "virtuvinis", "kombainas",
    # Cordless / battery-powered adjective
    "akumuliatorinis", "akumuliatoriniu",
    # Coffee grinder (kavos malūnėlis has dict entry but "malūnėlis" was not a trigger)
    "malūnėlis", "malunėlis",
    # Auto coffee machine (automatinis triggers full phrase match before kavos alone)
    "automatinis",
    # Screen size unit — "55 colių televizorius" → "55 Zoll Fernseher"
    "colių", "coliai", "colio",
]
# Normalized (no diacritics) version so accent-free queries also trigger translation
_LT_CATEGORY_WORDS_NORM = [_norm_lt(w) for w in _LT_CATEGORY_WORDS]


def _is_lt_query(q: str) -> bool:
    """Return True if q contains any Lithuanian product category word (with or without diacritics)."""
    q_norm = _norm_lt(q.lower())
    return any(w in q_norm for w in _LT_CATEGORY_WORDS_NORM)

# Static word-for-word replacement — avoids Claude API for common LT product searches.
# Words are sorted longest-first so "dulkių siurblys" matches before "siurblys".
_LT_DE: list[tuple[str, str]] = sorted([
    ("dulkių siurblys", "Staubsauger"), ("dulkių siurblio", "Staubsauger"),
    ("skalbimo mašina", "Waschmaschine"), ("skalbyklė", "Waschmaschine"),
    ("skalbyklės", "Waschmaschine"), ("skalbimo", "Wasch"),
    ("džiovyklė", "Wäschetrockner"), ("indaplovė", "Spülmaschine"),
    ("šaldytuvas", "Kühlschrank"), ("šaldiklis", "Gefrierschrank"),
    ("orkaitė", "Backofen"), ("mikrobangų", "Mikrowellen"),
    ("automatinis kavos aparatas", "Kaffeevollautomat"), ("automatinis kavos", "Kaffeevollautomat"),
    ("kavos malūnėlis", "Kaffeemühle"), ("kavos malunėlis", "Kaffeemühle"),
    ("pusiau automatinis kavos aparatas", "Kaffeemaschine"),
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
    # Screen size units: "55 colių televizorius" → "55 Zoll Fernseher"
    ("colių", "Zoll"), ("coliai", "Zoll"), ("colio", "Zoll"),
    ("planšetė", "Tablet"), ("kamera", "Kamera"),
    ("fotoaparatas", "Kamera"), ("spausdintuvas", "Drucker"),
    ("monitorius", "Monitor"), ("klaviatūra", "Tastatur"),
    ("pelė", "Maus"), ("garsiakalbis", "Lautsprecher"),
    ("žaislas", "Spielzeug"), ("žaislo", "Spielzeug"), ("žaislai", "Spielzeug"),
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
    ("elektrinis dviratis", "E-Bike"), ("elektrinis paspirtukas", "E-Roller"),
    ("dviratis", "Fahrrad"), ("paspirtukas", "E-Roller"),
    ("rankinis maišytuvas", "Handmixer"), ("maišytuvas", "Mixer"),
    ("šaldymo dėžė", "Kühlbox"), ("oro valytuvas", "Luftreiniger"),
    # Watches & wearables
    ("išmanusis laikrodis", "Smartwatch"), ("sporto laikrodis", "Sportuhr"),
    ("laikrodis", "Uhr"), ("sporto apyrankė", "Fitness Tracker"),
    # Earbuds (different from headphones)
    ("ausinukai", "In-Ear Kopfhörer"), ("ausinuko", "In-Ear Kopfhörer"),
    # Juicer
    ("sulčių spaustuvas", "Entsafter"), ("sulčiaspaudė", "Entsafter"),
    # Hair tools
    ("plaukų tiesintuvas", "Haarglätter"), ("tiesintuvas", "Haarglätter"),
    # Food / kitchen
    ("maisto procesorius", "Küchenmaschine"),
    ("kepyklė", "Brotbackautomat"),
    # Air quality
    ("oro drėkintuvas", "Luftbefeuchter"), ("drėkintuvas", "Luftbefeuchter"),
    ("termometras", "Thermometer"),
    # Gaming
    ("žaidimų konsolė", "Spielkonsole"), ("žaidimų pultai", "Controller"),
    ("žaidimų", "Gaming"),
    # Fitness
    ("bėgimo takelis", "Laufband"),
    # Multimedia
    ("grotuvas", "Player"), ("mp3 grotuvas", "MP3-Player"),
    # Accessories
    ("įkroviklis", "Ladegerät"), ("projektorius", "Projektor"),
    # Robot vacuum (must come before plain "siurblys")
    ("robotinis dulkių siurblys", "Saugroboter"), ("robotinis siurblys", "Saugroboter"),
    ("robotinis", "Roboter"),
    # Audio
    ("garso sistema", "Soundbar"), ("garso", "Audio"),
    ("namų kinas", "Heimkino"), ("kino sistema", "Heimkino"),
    ("soundbar", "Soundbar"),
    # Cameras
    ("vaizdo kamera", "Videokamera"), ("veiksmo kamera", "Action-Kamera"),
    # Kitchen
    ("rankinis plakiklis", "Handmixer"), ("plakiklis", "Handmixer"),
    ("vandens filtras", "Wasserfilter"),
    ("oro gruzdintuvė", "Heißluftfritteuse"), ("gruzdintuvė", "Fritteuse"),
    # Binoculars
    ("žiūronai", "Fernglas"),
    # Hair curler
    ("plaukų garbanojimo žnyplės", "Lockenstab"), ("garbanojimo žnyplės", "Lockenstab"),
    ("garbanojimo", "Locken"),
    # Power tools
    ("elektrinis grąžtas", "Bohrmaschine"), ("grąžtas", "Bohrmaschine"),
    ("pjūklas", "Säge"), ("perforatorius", "Bohrhammer"),
    ("kampinis šlifuoklis", "Winkelschleifer"), ("šlifuoklis", "Schleifer"),
    ("elektrinis suktukas", "Akkuschrauber"), ("suktukas", "Schrauber"),
    # Speaker variants
    ("garsinė sistema", "Soundbar"), ("garsinė kolonėlė", "Lautsprecher"),
    ("garsinė", "Audio"), ("kolonėlė", "Lautsprecher"), ("kolonele", "Lautsprecher"),
    # Storage & drives — long phrase first so it beats "nešiojamas"→"Laptop"
    ("nešiojamas kietasis diskas", "Externe Festplatte"),
    ("nesiojamas kietasis diskas", "Externe Festplatte"),
    ("išorinis kietasis diskas", "Externe Festplatte"),
    ("kietasis diskas", "Festplatte"), ("kietojo disko", "Festplatte"),
    ("išorinė atmintinė", "USB-Stick"), ("usb atmintinė", "USB-Stick"),
    ("atmintinė", "USB-Stick"), ("atmintine", "USB-Stick"),
    ("išorinė", "Externe"), ("isorine", "Externe"),
    ("diskas", "Festplatte"),
    # Keyboard adjective
    ("mechaninė klaviatūra", "Mechanische Tastatur"),
    ("mechanine klaviatura", "Mechanische Tastatur"),
    ("mechaninė", "mechanisch"), ("mechanine", "mechanisch"),
    # "nešiojamas X" where X is NOT a laptop — must all be longer than "nešiojamas"→Laptop
    # so they are matched first in the sorted dict and prevent the Laptop substitution
    ("nešiojamas garsiakalbis", "Tragbarer Lautsprecher"),
    ("nesiojamas garsiakalbis", "Tragbarer Lautsprecher"),
    ("nešiojamas kondicionierius", "Portable Klimaanlage"),
    ("nesiojamas kondicionierius", "Portable Klimaanlage"),
    ("nešiojamas ventiliatorius", "Tragbarer Ventilator"),
    ("nesiojamas ventiliatorius", "Tragbarer Ventilator"),
    ("nešiojamas siurblys", "Akku-Staubsauger"),
    ("nesiojamas siurblys", "Akku-Staubsauger"),
    ("nešiojamas pjūklas", "Akkusäge"), ("nesiojamas pjuklas", "Akkusäge"),
    ("nešiojamas grąžtas", "Akkubohrmaschine"), ("nesiojamas graztas", "Akkubohrmaschine"),
    # Iron (lygintuvas is a common LT alternative to laidynas)
    ("garų lygintuvas", "Dampfbügeleisen"), ("garų laidynas", "Dampfbügeleisen"),
    ("lygintuvas", "Bügeleisen"),
    ("garų valytuvas", "Dampfreiniger"), ("garu valytuvas", "Dampfreiniger"),
    ("garų siurblys", "Dampfsauger"), ("garu siurblys", "Dampfsauger"),
    # Water heater / boiler
    ("vandens šildytuvas", "Warmwasserbereiter"), ("vandens sildytuvas", "Warmwasserbereiter"),
    ("boileris", "Boiler"),
    # Pressure washer
    ("aukštojo slėgio plovykla", "Hochdruckreiniger"), ("slėginė plovykla", "Hochdruckreiniger"),
    ("slegine plovykla", "Hochdruckreiniger"), ("plovykla", "Hochdruckreiniger"),
    # Lawn mower (vejapjovė = variant spelling of žoliapjovė, not yet in dict)
    ("vejapjovė", "Rasenmäher"), ("vejapjove", "Rasenmäher"),
    # Air compressor
    ("kompresorius", "Kompressor"), ("kompresoriaus", "Kompressor"),
    # Snow blower (common in LT winters)
    ("sniego valytuvas", "Schneefräse"), ("sniego frezas", "Schneefräse"),
    ("sniego freza", "Schneefräse"),
    # Heat pump (šilumos siurblys must come before standalone siurblys→Staubsauger)
    ("šilumos siurblys", "Wärmepumpe"), ("silumos siurblys", "Wärmepumpe"),
    ("šilumos pompa", "Wärmepumpe"), ("silumos pompa", "Wärmepumpe"),
    # Gas-type products (dujų viryklė = gas stove, dujų katilas = gas boiler)
    ("dujų viryklė", "Gasherd"), ("duju virykle", "Gasherd"),
    ("dujų katilas", "Gaskessel"), ("duju katilas", "Gaskessel"),
    ("dujų", "Gas"), ("duju", "Gas"),
    # Standalone genitive fallbacks (only fire when longer multi-word phrases don't match)
    ("vandens", "Wasser"),   # water (vandens filtras→Wasserfilter already handled above)
    ("vaizdo", "Video"),     # video (vaizdo kamera→Videokamera already handled above)
    ("veiksmo", "Action"),   # action (veiksmo kamera→Action-Kamera already handled above)
    ("sniego", "Schnee"),    # snow (sniego valytuvas→Schneefräse already handled above)
    ("šilumos", "Wärme"),    # heat (šilumos siurblys→Wärmepumpe already handled above)
    ("silumos", "Wärme"),
    # Standalone fallbacks for trigger words missing direct translations
    # (these fire only when the more-specific multi-word phrases above don't match)
    ("bėgimo", "Lauf"),
    ("garų", "Dampf"),
    ("kondicionierius", "Klimaanlage"), ("kondicionieriaus", "Klimaanlage"),
    ("valytuvas", "Reiniger"),
    ("kraujo", "Blutdruck"),
    ("robotas", "Roboter"),
    ("maisto", "Küchenmaschine"),
    ("spaustuvas", "Entsafter"),
    ("apyrankė", "Fitness Tracker"), ("apyranke", "Fitness Tracker"),
    ("kampinis", "Winkelschleifer"),
    ("kietasis", "Festplatte"),
    # Induction adjective (indukcinis kaitvietas = induction hob)
    ("indukcinis", "Induktions"), ("indukcine", "Induktions"),
    # Electric/smart adjective standalones (multi-word phrases above match first)
    ("elektrinis", "elektrisch"), ("elektrine", "elektrisch"),
    ("ismanusis", "Smart"), ("ismanius", "Smart"),
    ("išmanioji", "Smart"), ("ismanioji", "Smart"),
    # Diminutive watch form (laikrodis → Uhr already exists; laikrodukas = small watch)
    ("laikrodukas", "Uhr"),
    # Standalone "kino" (home cinema context; "kino sistema"→"Heimkino" matches first when paired)
    ("kino", "Heimkino"),
    # Microphone
    ("mikrofonas", "Mikrofon"),
    # Router
    ("maršrutizatorius", "Router"), ("marsrutizatorius", "Router"),
    # Alarm clock
    ("žadintuvas", "Wecker"), ("zadintuvas", "Wecker"),
    # Lamp / lighting
    ("lempa", "Lampe"),
    # Electric toothbrush (šepetėlis alone — "dantų šepetėlis" handles full phrase above)
    ("šepetėlis", "elektrische Zahnbürste"), ("sepetelis", "elektrische Zahnbürste"),
    # Stand mixer / food processor variant (virtuvinis kombainas = common LT term)
    ("virtuvinis kombainas", "Küchenmaschine"), ("virtuvinis kombaintas", "Küchenmaschine"),
    ("virtuvinis", "Küchen"),
    # Cordless / battery-powered adjective (akumuliatorinis grąžtas = cordless drill)
    ("akumuliatorinis", "Akku"), ("akumuliatoriniu", "Akku"),
], key=lambda t: -len(t[0]))

_LT_PL: list[tuple[str, str]] = sorted([
    ("dulkių siurblys", "odkurzacz"), ("dulkių siurblio", "odkurzacz"),
    ("skalbimo mašina", "pralka"), ("skalbyklė", "pralka"),
    ("skalbyklės", "pralka"), ("skalbimo", "pranie"),
    ("džiovyklė", "suszarka do ubrań"), ("indaplovė", "zmywarka"),
    ("šaldytuvas", "lodówka"), ("šaldiklis", "zamrażarka"),
    ("orkaitė", "piekarnik"), ("mikrobangų", "mikrofalówka"),
    ("automatinis kavos aparatas", "ekspres automatyczny"), ("automatinis kavos", "ekspres automatyczny"),
    ("kavos malūnėlis", "młynek do kawy"), ("kavos malunėlis", "młynek do kawy"),
    ("pusiau automatinis kavos aparatas", "ekspres do kawy"),
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
    # Screen size units: "55 colių televizorius" → "55 cali telewizor"
    ("colių", "cali"), ("coliai", "cali"), ("colio", "cali"),
    ("planšetė", "tablet"), ("kamera", "kamera"),
    ("fotoaparatas", "aparat fotograficzny"), ("spausdintuvas", "drukarka"),
    ("monitorius", "monitor"), ("klaviatūra", "klawiatura"),
    ("pelė", "mysz"), ("garsiakalbis", "głośnik"),
    ("žaislas", "zabawka"), ("žaislo", "zabawka"), ("žaislai", "zabawki"),
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
    ("elektrinis dviratis", "rower elektryczny"), ("elektrinis paspirtukas", "hulajnoga elektryczna"),
    ("dviratis", "rower"), ("paspirtukas", "hulajnoga elektryczna"),
    ("rankinis maišytuvas", "mikser ręczny"), ("maišytuvas", "mikser"),
    ("šaldymo dėžė", "lodówka turystyczna"), ("oro valytuvas", "oczyszczacz powietrza"),
    # Watches & wearables
    ("išmanusis laikrodis", "smartwatch"), ("sporto laikrodis", "zegarek sportowy"),
    ("laikrodis", "zegarek"), ("sporto apyrankė", "opaska fitness"),
    # Earbuds
    ("ausinukai", "słuchawki douszne"), ("ausinuko", "słuchawki douszne"),
    # Juicer
    ("sulčių spaustuvas", "wyciskarka do soków"), ("sulčiaspaudė", "wyciskarka"),
    # Hair tools
    ("plaukų tiesintuvas", "prostownica do włosów"), ("tiesintuvas", "prostownica"),
    # Food / kitchen
    ("maisto procesorius", "robot kuchenny"),
    ("kepyklė", "wypiekacz do chleba"),
    # Air quality
    ("oro drėkintuvas", "nawilżacz powietrza"), ("drėkintuvas", "nawilżacz"),
    ("termometras", "termometr"),
    # Gaming
    ("žaidimų konsolė", "konsola do gier"), ("žaidimų pultai", "kontroler"),
    ("žaidimų", "gaming"),
    # Fitness
    ("bėgimo takelis", "bieżnia elektryczna"),
    # Multimedia
    ("grotuvas", "odtwarzacz"), ("mp3 grotuvas", "odtwarzacz mp3"),
    # Accessories
    ("įkroviklis", "ładowarka"), ("projektorius", "projektor"),
    # Robot vacuum
    ("robotinis dulkių siurblys", "robot odkurzający"), ("robotinis siurblys", "robot odkurzający"),
    ("robotinis", "robotyczny"),
    # Audio
    ("garso sistema", "soundbar"), ("garso", "audio"),
    ("namų kinas", "kino domowe"), ("kino sistema", "kino domowe"),
    # Cameras
    ("vaizdo kamera", "kamera wideo"), ("veiksmo kamera", "kamera sportowa"),
    # Kitchen
    ("rankinis plakiklis", "mikser ręczny"), ("plakiklis", "mikser ręczny"),
    ("vandens filtras", "filtr wody"),
    ("oro gruzdintuvė", "frytkownica beztłuszczowa"), ("gruzdintuvė", "frytkownica"),
    # Binoculars
    ("žiūronai", "lornetka"),
    # Hair curler
    ("plaukų garbanojimo žnyplės", "lokówka"), ("garbanojimo žnyplės", "lokówka"),
    ("garbanojimo", "lokówka"),
    # Power tools
    ("elektrinis grąžtas", "wiertarka"), ("grąžtas", "wiertarka"),
    ("pjūklas", "piła"), ("perforatorius", "młotowiertarka"),
    ("kampinis šlifuoklis", "szlifierka kątowa"), ("šlifuoklis", "szlifierka"),
    ("elektrinis suktukas", "wkrętarka akumulatorowa"), ("suktukas", "wkrętarka"),
    # Speaker variants
    ("garsinė sistema", "soundbar"), ("garsinė kolonėlė", "głośnik"),
    ("garsinė", "audio"), ("kolonėlė", "głośnik"), ("kolonele", "głośnik"),
    # Storage & drives
    ("nešiojamas kietasis diskas", "zewnętrzny dysk twardy"),
    ("nesiojamas kietasis diskas", "zewnętrzny dysk twardy"),
    ("išorinis kietasis diskas", "zewnętrzny dysk twardy"),
    ("kietasis diskas", "dysk twardy"), ("kietojo disko", "dysk twardy"),
    ("išorinė atmintinė", "pendrive"), ("usb atmintinė", "pendrive"),
    ("atmintinė", "pendrive"), ("atmintine", "pendrive"),
    ("išorinė", "zewnętrzna"), ("isorine", "zewnętrzna"),
    ("diskas", "dysk"),
    # Keyboard adjective
    ("mechaninė klaviatūra", "mechaniczna klawiatura"),
    ("mechanine klaviatura", "mechaniczna klawiatura"),
    ("mechaninė", "mechaniczna"), ("mechanine", "mechaniczna"),
    # "nešiojamas X" where X is NOT a laptop — must all be longer than "nešiojamas"→laptop
    ("nešiojamas garsiakalbis", "głośnik przenośny"),
    ("nesiojamas garsiakalbis", "głośnik przenośny"),
    ("nešiojamas kondicionierius", "klimatyzator przenośny"),
    ("nesiojamas kondicionierius", "klimatyzator przenośny"),
    ("nešiojamas ventiliatorius", "wentylator przenośny"),
    ("nesiojamas ventiliatorius", "wentylator przenośny"),
    ("nešiojamas siurblys", "odkurzacz akumulatorowy"),
    ("nesiojamas siurblys", "odkurzacz akumulatorowy"),
    ("nešiojamas pjūklas", "piła akumulatorowa"), ("nesiojamas pjuklas", "piła akumulatorowa"),
    ("nešiojamas grąžtas", "wiertarka akumulatorowa"), ("nesiojamas graztas", "wiertarka akumulatorowa"),
    # Iron (lygintuvas is a common LT alternative to laidynas)
    ("garų lygintuvas", "żelazko parowe"), ("garų laidynas", "żelazko parowe"),
    ("lygintuvas", "żelazko"),
    ("garų valytuvas", "myjka parowa"), ("garu valytuvas", "myjka parowa"),
    ("garų siurblys", "odkurzacz parowy"), ("garu siurblys", "odkurzacz parowy"),
    # Water heater / boiler
    ("vandens šildytuvas", "podgrzewacz wody"), ("vandens sildytuvas", "podgrzewacz wody"),
    ("boileris", "bojler"),
    # Pressure washer
    ("aukštojo slėgio plovykla", "myjka ciśnieniowa"), ("slėginė plovykla", "myjka ciśnieniowa"),
    ("slegine plovykla", "myjka ciśnieniowa"), ("plovykla", "myjka ciśnieniowa"),
    # Lawn mower (vejapjovė = variant spelling)
    ("vejapjovė", "kosiarka"), ("vejapjove", "kosiarka"),
    # Air compressor
    ("kompresorius", "kompresor"), ("kompresoriaus", "kompresor"),
    # Snow blower
    ("sniego valytuvas", "odśnieżarka"), ("sniego frezas", "odśnieżarka"),
    ("sniego freza", "odśnieżarka"),
    # Heat pump (šilumos siurblys must come before standalone siurblys→odkurzacz)
    ("šilumos siurblys", "pompa ciepła"), ("silumos siurblys", "pompa ciepła"),
    ("šilumos pompa", "pompa ciepła"), ("silumos pompa", "pompa ciepła"),
    # Gas-type products
    ("dujų viryklė", "kuchenka gazowa"), ("duju virykle", "kuchenka gazowa"),
    ("dujų katilas", "kocioł gazowy"), ("duju katilas", "kocioł gazowy"),
    ("dujų", "gazowy"), ("duju", "gazowy"),
    # Standalone genitive fallbacks
    ("vandens", "woda"),      # water
    ("vaizdo", "wideo"),      # video
    ("veiksmo", "sportowy"),  # action
    ("sniego", "śnieg"),      # snow
    ("šilumos", "cieplna"), ("silumos", "cieplna"),  # heat/thermal
    # Standalone fallbacks for trigger words missing direct translations
    ("bėgimo", "bieganie"),
    ("garų", "parowy"),
    ("kondicionierius", "klimatyzator"), ("kondicionieriaus", "klimatyzator"),
    ("valytuvas", "oczyszczacz"),
    ("kraujo", "ciśnienie krwi"),
    ("robotas", "robot"),
    ("maisto", "robot kuchenny"),
    ("spaustuvas", "wyciskarka"),
    ("apyrankė", "opaska fitness"), ("apyranke", "opaska fitness"),
    ("kampinis", "szlifierka kątowa"),
    ("kietasis", "dysk twardy"),
    # Induction adjective
    ("indukcinis", "indukcyjny"), ("indukcine", "indukcyjna"),
    # Electric/smart adjective standalones
    ("elektrinis", "elektryczny"), ("elektrine", "elektryczna"),
    ("ismanusis", "smart"), ("ismanius", "smart"),
    ("išmanioji", "smart"), ("ismanioji", "smart"),
    # Diminutive watch form
    ("laikrodukas", "zegarek"),
    # Microphone
    ("mikrofonas", "mikrofon"),
    # Router
    ("maršrutizatorius", "router"), ("marsrutizatorius", "router"),
    # Alarm clock
    ("žadintuvas", "budzik"), ("zadintuvas", "budzik"),
    # Lamp / lighting
    ("lempa", "lampa"),
    # Note: standalone "kino" intentionally omitted for PL — "kino sistema"/"namų kinas" handle
    # compound cases; "kino" alone is a valid PL word that Amazon.PL understands directly.
    # Adding ("kino","kino domowe") here would cause cascade: "kino domowe"→"kino domowe domowe".
    # Electric toothbrush
    ("šepetėlis", "elektryczna szczoteczka do zębów"), ("sepetelis", "elektryczna szczoteczka"),
    # Stand mixer / food processor variant
    ("virtuvinis kombainas", "robot kuchenny"), ("virtuvinis kombaintas", "robot kuchenny"),
    ("virtuvinis", "kuchenny"),
    # Cordless / battery-powered adjective
    ("akumuliatorinis", "akumulatorowy"), ("akumuliatoriniu", "akumulatorowy"),
], key=lambda t: -len(t[0]))


def _static_translate(query: str, target_lang: str) -> str:
    """Replace LT category words with target-language equivalents. Free and instant.
    Normalizes LT diacritics first (ą→a, č→c, etc.) so typed-without-accents queries work.
    Uses whole-word matching to prevent shorter rules re-matching inside already-translated text
    (e.g. 'kino' must not match inside 'Heimkino' after 'kino sistema'→'Heimkino')."""
    mapping = _LT_DE if target_lang == "de" else _LT_PL
    result = _norm_lt(query)
    q_low = result.lower()
    for lt_word, target_word in mapping:
        lt_norm = _norm_lt(lt_word)
        pat = r'(?<![a-z0-9])' + re.escape(lt_norm) + r'(?![a-z0-9])'
        if not re.search(pat, q_low):
            continue
        result = re.sub(pat, target_word, result, flags=re.IGNORECASE)
        q_low = result.lower()
    return result


def claude_translate(query: str, target_lang: str = "en") -> str:
    cache_key = f"{query.lower()}:{target_lang}"
    if cache_key in _translate_cache:
        return _translate_cache[cache_key]

    # Evict oldest 20% entries when cache exceeds 1000 to prevent unbounded growth
    if len(_translate_cache) > 1000:
        keys = list(_translate_cache.keys())
        for k in keys[:200]:
            del _translate_cache[k]

    # Fast path: no Lithuanian words → brand/model works in any language
    if not _is_lt_query(query):
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
    # Detect query language for localised rule-based output
    is_lt = _is_lt_query(query) or any(ord(c) > 127 for c in query[:20])
    q_low = query.lower()
    is_de = any(c in q_low for c in ("ä", "ö", "ü", "ß")) or any(w in q_low for w in ("waschmaschine", "kühlschrank", "fernseher", "drucker"))
    is_pl = any(c in q_low for c in ("ę", "ó", "ń")) or any(w in q_low for w in ("pralka", "odkurzacz", "lodówka", "golarka", "ekspres"))
    lang = "lt" if is_lt else ("de" if is_de else ("pl" if is_pl else "en"))

    _L = {
        "lt": {"no_price": "Kainų nerasta.", "try_specific": "Pabandykite tikslesnį pavadinimą.", "refine": "Patikslinkite paiešką.", "one_seller": "Rastas tik 1 pardavėjas — palyginti negalime.", "cheap_pct": "Pigiausia kaina yra {pct:.0f}% žemiau brangiausios.", "near_avg": "Geriausia kaina artima rinkos vidurkiui.", "normal": "Kaina atrodo normali.", "rec": "Geriausia rasta kaina €{pmin:.2f}. Palyginkite pristatymą ir pardavėją prieš pirkdami.", "summary": "Goody rado {n} kainų. Pigiausia: €{pmin:.2f}, vidurkis: €{pavg:.2f}.", "at_hist_low": "Kaina šiuo metu istoriniame minimume — geras metas pirkti.", "above_hist_avg": "Kaina viršija 30 dienų vidurkį — galbūt verta palaukti."},
        "de": {"no_price": "Keine Preise gefunden.", "try_specific": "Bitte genaueren Produktnamen eingeben.", "refine": "Suche verfeinern.", "one_seller": "Nur 1 Händler gefunden — kein Preisvergleich möglich.", "cheap_pct": "Das günstigste Angebot liegt {pct:.0f}% unter dem teuersten.", "near_avg": "Der beste Preis liegt nahe am Marktdurchschnitt.", "normal": "Der Preis sieht angemessen aus.", "rec": "Bester gefundener Preis €{pmin:.2f}. Versandkosten und Händler vergleichen.", "summary": "Goody fand {n} Preise. Günstigster: €{pmin:.2f}, Durchschnitt: €{pavg:.2f}.", "at_hist_low": "Preis aktuell auf historischem Tief — guter Kaufzeitpunkt.", "above_hist_avg": "Preis über dem 30-Tage-Durchschnitt — abwarten könnte sich lohnen."},
        "pl": {"no_price": "Nie znaleziono cen.", "try_specific": "Wpisz dokładniejszą nazwę produktu.", "refine": "Doprecyzuj wyszukiwanie.", "one_seller": "Znaleziono tylko 1 sprzedawcę — porównanie niemożliwe.", "cheap_pct": "Najtańsza oferta jest {pct:.0f}% poniżej najdroższej.", "near_avg": "Najlepsza cena bliska średniej rynkowej.", "normal": "Cena wygląda normalnie.", "rec": "Najlepsza znaleziona cena €{pmin:.2f}. Porównaj dostawę i sprzedawcę.", "summary": "Goody znalazło {n} cen. Najtańsza: €{pmin:.2f}, średnia: €{pavg:.2f}.", "at_hist_low": "Cena aktualnie na historycznym minimum — dobry moment na zakup.", "above_hist_avg": "Cena powyżej 30-dniowej średniej — warto poczekać."},
        "en": {"no_price": "No prices found.", "try_specific": "Try a more specific product name.", "refine": "Refine your search.", "one_seller": "Only one seller found — price comparison unavailable.", "cheap_pct": "The cheapest offer is {pct:.0f}% below the highest found price.", "near_avg": "The best price is close to the current market average.", "normal": "The current price looks reasonable.", "rec": "Best found price is €{pmin:.2f}. Compare delivery and seller reliability before buying.", "summary": "Goody found {n} price(s). Lowest: €{pmin:.2f}, average: €{pavg:.2f}.", "at_hist_low": "Price is at historical low — good time to buy.", "above_hist_avg": "Price is above the 30-day average — consider waiting."},
    }
    L = _L.get(lang, _L["en"])

    if not results:
        return {
            "verdict": "WAIT",
            "verdict_label": "Not found",
            "verdict_reason": L["no_price"],
            "ai_summary": L["try_specific"],
            "alternative": "",
            "buy_recommendation": L["refine"],
            "price_forecast": ""
        }

    prices = [r.get("price", 0) for r in results if r.get("price", 0) > 0]

    if not prices:
        return empty_ai()

    price_min = min(prices)
    price_max = max(prices)
    price_avg = round(sum(prices) / len(prices), 2)
    spread_pct = ((price_max - price_min) / price_max * 100) if price_max else 0

    hist = price_history or {}
    hist_low = hist.get("lowest", 0)
    hist_avg = hist.get("avg", 0)
    hist_count = hist.get("count", 0)

    if len(prices) == 1:
        verdict = "OK"
        label = "Normal"
        reason = L["one_seller"]
    elif hist_low and hist_count >= 2 and price_min <= hist_low * 1.05:
        verdict = "BUY"
        label = "Buy now"
        reason = L["at_hist_low"]
    elif hist_avg and hist_count >= 2 and price_min > hist_avg * 1.10:
        verdict = "WAIT"
        label = "Wait"
        reason = L["above_hist_avg"]
    elif spread_pct >= 20:
        verdict = "BUY"
        label = "Buy now"
        reason = L["cheap_pct"].format(pct=spread_pct)
    elif price_min > price_avg * 0.97:
        verdict = "WAIT"
        label = "Wait"
        reason = L["near_avg"]
    else:
        verdict = "OK"
        label = "Normal"
        reason = L["normal"]

    return {
        "verdict": verdict,
        "verdict_label": label,
        "verdict_reason": reason,
        "ai_summary": L["summary"].format(n=len(prices), pmin=price_min, pavg=price_avg),
        "alternative": "",
        "buy_recommendation": L["rec"].format(pmin=price_min),
        "price_forecast": "",
    }


def build_ai_prompt(query: str, results: list, price_history: dict = None) -> str:
    prices = [r.get("price", 0) for r in results if r.get("price", 0) > 0]
    p_min = min(prices) if prices else 0
    p_max = max(prices) if prices else 0
    spread_pct = round((p_max - p_min) / p_max * 100) if p_max else 0

    shops_summary = "; ".join(
        f"{r.get('shop','')} €{r.get('price',0):.2f}"
        + (f" ★{r.get('rating')}" if r.get("rating") else "")
        for r in sorted(results, key=lambda x: x.get("price", 999999))[:5]
        if r.get("price", 0) > 0
    )

    hist = price_history or {}
    hist_line = ""
    if hist.get("lowest") and hist.get("count", 0) >= 2:
        at_low = p_min <= hist["lowest"] * 1.03
        hist_note = " (AT HISTORICAL LOW!)" if at_low else f", currently {round((p_min/hist['lowest']-1)*100)}% above low"
        hist_line = f" 30d history: low €{hist['lowest']}, high €{hist.get('highest','?')}{hist_note}."

    return f"""Goody price comparison coach. Analyze and return JSON only.
Product: {query}
Shops: {shops_summary}
Price range: €{p_min:.2f}–€{p_max:.2f} ({len(prices)} shops, {spread_pct}% spread).{hist_line}

Rules: use only provided data. Be concise. Respond in the query language (LT/DE/PL/EN).

Return ONLY valid JSON:
{{"verdict":"BUY|WAIT|OK","verdict_label":"1-3 words","verdict_reason":"one sentence","ai_summary":"1-2 sentences","alternative":"cheaper alternative product name if clearly overpriced else empty string","buy_recommendation":"1-2 sentences","price_forecast":"one sentence or empty string"}}"""


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
    # Filter relevance BEFORE dedup: keeps cheapest relevant result per shop, not cheapest overall
    results = [r for r in results if r.get("price", 0) > 0]
    filtered = [r for r in results if is_relevant_result(query, r.get("product_title", ""))]
    if filtered:
        results = filtered
    results = deduplicate_by_shop(results)

    if not results:
        suggestion = suggest_simpler_query(query)
        q_low = query.lower()
        _is_lt = _is_lt_query(query) or any(ord(c) > 127 for c in query[:20])
        _is_de = any(c in q_low for c in ("ä", "ö", "ü", "ß")) or any(w in q_low for w in ("waschmaschine", "kühlschrank", "fernseher"))
        _is_pl = any(c in q_low for c in ("ę", "ó", "ń")) or any(w in q_low for w in ("pralka", "odkurzacz", "lodówka"))
        _lang = "lt" if _is_lt else ("de" if _is_de else ("pl" if _is_pl else "en"))
        _NR = {
            "lt": ("Nerasta", "Produktas nerastas nė vienoje parduotuvėje.", "Pabandykite tikslesnį pavadinimą arba trumpesnę užklausą.", f'Pabandykite: "{suggestion}"' if suggestion else "Pabandykite kitą paieškos terminą."),
            "de": ("Nicht gefunden", "Produkt in keinem Shop gefunden.", "Bitte genaueren Namen oder kürzeren Suchbegriff eingeben.", f'Versuchen Sie: "{suggestion}"' if suggestion else "Versuchen Sie einen anderen Suchbegriff."),
            "pl": ("Nie znaleziono", "Produkt nie został znaleziony w żadnym sklepie.", "Spróbuj bardziej szczegółowej nazwy lub krótszego zapytania.", f'Spróbuj: "{suggestion}"' if suggestion else "Spróbuj innego wyszukiwania."),
            "en": ("Not found", "Product not found in any shop.", "Try a more specific name or shorter query.", f'Try: "{suggestion}"' if suggestion else "Try a different search term."),
        }
        _label, _reason, _summary, _rec = _NR[_lang]
        return {
            "product_name": query,
            "ai_verdict": "WAIT",
            "verdict_label": _label,
            "verdict_reason": _reason,
            "ai_summary": _summary,
            "buy_recommendation": _rec,
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
    q_low2 = query.lower()
    _is_lt2 = _is_lt_query(query) or any(ord(c) > 127 for c in query[:20])
    _is_de2 = any(c in q_low2 for c in ("ä", "ö", "ü", "ß")) or any(w in q_low2 for w in ("waschmaschine", "kühlschrank", "fernseher"))
    _is_pl2 = any(c in q_low2 for c in ("ę", "ó", "ń")) or any(w in q_low2 for w in ("pralka", "odkurzacz", "lodówka"))
    _lang2 = "lt" if _is_lt2 else ("de" if _is_de2 else ("pl" if _is_pl2 else "en"))
    _best_price_fallback = {
        "lt": f"Geriausia rasta kaina €{price_min:.2f}. Palyginkite pristatymą ir pardavėją.",
        "de": f"Bester gefundener Preis €{price_min:.2f}. Versandkosten und Händler vergleichen.",
        "pl": f"Najlepsza znaleziona cena €{price_min:.2f}. Porównaj dostawę i sprzedawcę.",
        "en": f"Best price found: €{price_min:.2f}. Compare delivery and seller before buying.",
    }[_lang2]
    savings_pct = ((price_max - price_min) / price_max * 100) if price_max > 0 else 0
    base_score = min(100, int(savings_pct * 1.5 + 50))

    # Adjust with price history: reward below-avg/below-low current prices, penalise above-avg
    hist = price_history or {}
    hist_avg = hist.get("avg", 0)
    hist_low = hist.get("lowest", 0)
    hist_bonus = 0
    if hist_avg and hist.get("count", 0) >= 2 and price_min > 0:
        ratio = price_min / hist_avg
        if ratio < 0.90:
            hist_bonus = min(15, int((1 - ratio) * 100))
        elif ratio > 1.10:
            hist_bonus = -8
    # Extra bonus for historical low (independent of avg bonus)
    if hist_low and price_min > 0 and price_min <= hist_low * 1.02:
        hist_bonus += 10

    deal_score = max(10, min(100, base_score + hist_bonus))

    return {
        "product_name": query,
        "ai_verdict": ai.get("verdict", "OK"),
        "verdict_label": ai.get("verdict_label", "Normal"),
        "verdict_reason": ai.get("verdict_reason", ""),
        "ai_summary": ai.get("ai_summary", ""),
        "buy_recommendation": ai.get("buy_recommendation", _best_price_fallback),
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
    query = resolve_query(query)

    cache_key = hashlib.md5(f"v64:{query.lower()}".encode()).hexdigest()
    etag = f'"{cache_key}"'
    cached = get_cache(cache_key)

    if cached:
        if request.headers.get("If-None-Match") == etag:
            return "", 304
        age_s = int(time.time() - cache.get(cache_key, {}).get("ts", time.time()))
        cached = dict(cached)
        cached["_cached"] = True
        cached["_cache_age_s"] = age_s
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

    # LT shops start immediately (they use the original query, no translation needed).
    # Translation runs in parallel; Amazon shops are added after it finishes.
    # This saves 1–3s on rare LT queries that miss the static dict and need Claude API.
    executor = ThreadPoolExecutor(max_workers=8)
    try:
        lt_futures = {
            executor.submit(scrape_varle,  query): "Varle",
            executor.submit(scrape_elesen, query): "Elesen",
            executor.submit(scrape_pigu,   query): "Pigu",
            executor.submit(scrape_topo,   query): "Topo",
        }

        is_lt_query = _is_lt_query(query)
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
    # Filter relevance first so AI gets cheapest relevant result per shop, not cheapest overall
    _relevant_for_ai = [r for r in all_results if r.get("price", 0) > 0
                        and is_relevant_result(query, r.get("product_title", ""))] or all_results
    deduped_for_ai = deduplicate_by_shop(_relevant_for_ai)
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
    threading.Thread(target=save_prices_to_supabase, args=(query, result.get("results", all_results)), daemon=True).start()

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
    query = resolve_query(query)

    # Capture rate info before entering the generator (request context won't be in the thread)
    ip = get_client_ip()
    used = rate_store.get(ip, {}).get("count", 1)
    rate_info = {"used": used, "limit": DAILY_FREE_LIMIT, "remaining": max(0, DAILY_FREE_LIMIT - used)}

    cache_key = hashlib.md5(f"v64:{query.lower()}".encode()).hexdigest()

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
            cached["_cache_age_s"] = int(time.time() - cache.get(cache_key, {}).get("ts", time.time()))
            cached["_rate"] = rate_info
            yield _sse("complete", cached)
            return

        print(f"\n=== STREAM: '{_original}' -> '{_query}' ===")
        t_start = time.time()

        all_results = []
        shops_done = 0
        SHOPS_TOTAL = 6  # Active shops: Varle, Elesen, Pigu, Topo, Amazon.DE, Amazon.PL

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
            stream_executor = ThreadPoolExecutor(max_workers=8)
            try:
                _is_lt = _is_lt_query(_query)
                q_de = _query
                q_pl = _query

                lt_shop_futures = {
                    stream_executor.submit(scrape_varle,  _query): "Varle",
                    stream_executor.submit(scrape_elesen, _query): "Elesen",
                    stream_executor.submit(scrape_pigu,   _query): "Pigu",
                    stream_executor.submit(scrape_topo,   _query): "Topo",
                }

                if _is_lt:
                    # For LT queries: start translation in background so LT shop partials
                    # flow to the client immediately instead of waiting up to 4s.
                    _trans_pool = ThreadPoolExecutor(max_workers=2)
                    try:
                        _f_de = _trans_pool.submit(claude_translate, _query, "de")
                        _f_pl = _trans_pool.submit(claude_translate, _query, "pl")

                        # Yield LT partials while translation runs concurrently
                        try:
                            for f in as_completed(lt_shop_futures, timeout=8):
                                name = lt_shop_futures[f]
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
                            print(f"[stream LT timeout] {e}")

                        # Now collect translations (most likely done by now)
                        try:
                            q_de = _f_de.result(timeout=3) or _query
                            q_pl = _f_pl.result(timeout=3) or _query
                        except Exception:
                            pass
                        print(f"  [Stream translate] DE:'{q_de}' PL:'{q_pl}'")
                    finally:
                        _trans_pool.shutdown(wait=False)

                    # Submit Amazon shops with translated queries and collect results
                    amazon_futures = {
                        stream_executor.submit(scrape_amazon, q_de, "de"): "Amazon.DE",
                        stream_executor.submit(scrape_amazon, q_pl, "pl"): "Amazon.PL",
                    }
                    try:
                        for f in as_completed(amazon_futures, timeout=10):
                            name = amazon_futures[f]
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
                        print(f"[stream Amazon timeout] {e}")

                else:
                    # EN/DE/PL query: all 6 shops at once, no translation needed
                    all_shop_futures = {
                        **lt_shop_futures,
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
                _ph_exec.shutdown(wait=False)  # runs even on GeneratorExit (client disconnect)

        except Exception as e:
            print(f"[stream executor] {e}")

        print(f"=== STREAM TOTAL: {len(all_results)} before dedup ===")

        # Collect price history (was running in background since t=0)
        price_history = {}
        try:
            price_history = ph_fut.result(timeout=1)
        except Exception:
            pass

        # ── AI + final result ──
        try:
            _rel_ai = [r for r in all_results if r.get("price", 0) > 0
                       and is_relevant_result(_query, r.get("product_title", ""))] or all_results
            deduped_for_ai = deduplicate_by_shop(_rel_ai)
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
            # Save only relevant/deduped results to keep price history clean
            threading.Thread(target=save_prices_to_supabase, args=(_query, result.get("results", all_results)), daemon=True).start()

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

    all_prices = [float(r.get("price", 0)) for r in rows if r.get("price", 0) > 0]
    return jsonify({
        "product_name": q,
        "labels": sorted_days,
        "datasets": datasets,
        "raw": rows[-100:],
        "price_30d_min": round(min(all_prices), 2) if all_prices else None,
        "price_30d_max": round(max(all_prices), 2) if all_prices else None,
    })


@app.route("/api/watchlist-check", methods=["POST"])
def watchlist_check():
    """Check Supabase price history for watchlist items — no ScraperAPI credits used."""
    data = request.get_json(silent=True) or {}
    items = data.get("items", [])
    if not items or not isinstance(items, list):
        return jsonify({"alerts": []}), 200
    if not (SUPABASE_URL and SUPABASE_KEY):
        return jsonify({"alerts": []}), 200

    # Only check within last 7 days (recent enough to be useful)
    cutoff = time.time() - 7 * 86400
    alerts = []
    for item in items[:20]:  # cap at 20 to avoid abuse
        name = (item.get("name") or "").strip()[:200]
        target = item.get("target")
        if not name:
            continue
        try:
            rows = fetch_price_history_from_supabase(name)
            recent = [r for r in rows if r.get("checked_at", "") and
                      time.mktime(time.strptime(r["checked_at"][:19], "%Y-%m-%dT%H:%M:%S")) > cutoff]
            if not recent:
                continue
            prices = [float(r.get("price", 0)) for r in recent if float(r.get("price", 0)) > 0]
            if not prices:
                continue
            cur_min = min(prices)
            best_row = min(recent, key=lambda r: float(r.get("price", 0) or 999999))
            alert = {"name": name, "current_price": round(cur_min, 2), "shop": best_row.get("shop", "")}
            if target and float(target) > 0:
                if cur_min <= float(target):
                    alert["hit_target"] = True
                    alerts.append(alert)
            else:
                # No target: notify if price dropped vs stored item.price
                original = item.get("price")
                if original and float(original) > 0 and cur_min < float(original) - 1:
                    alert["drop"] = round(float(original) - cur_min, 2)
                    alerts.append(alert)
        except Exception as e:
            print(f"[watchlist-check] {name}: {e}")
    return jsonify({"alerts": alerts}), 200


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
                            "text": """Analyze this image. Find the product, any visible price, and any barcode.

Respond ONLY with JSON (no markdown):
{"product_name":"BRAND MODEL in English","price_visible":0,"barcode":"","confidence":"high/medium/low"}

Rules:
- product_name: brand + model + key specs in English (e.g. "Apple iPhone 16 Pro 256GB", "Sony WH-1000XM5", "Samsung 65\" QLED TV")
- price_visible: numeric price in EUR if a price tag is visible, else 0
- barcode: EAN/UPC/QR digits if a barcode is clearly visible, else empty string
- confidence: high=exact model known, medium=brand+category known, low=category only"""
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

        cache_key = hashlib.md5(f"scan_v64:{product_name.lower()}".encode()).hexdigest()
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
        scan_executor = ThreadPoolExecutor(max_workers=8)
        try:
            futures = {
                scan_executor.submit(scrape_varle,   product_name):    "Varle",
                scan_executor.submit(scrape_elesen,  product_name):    "Elesen",
                scan_executor.submit(scrape_pigu,    product_name):    "Pigu",
                scan_executor.submit(scrape_topo,    product_name):    "Topo",
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
            _scan_ph_exec.shutdown(wait=False)

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

        _scan_rel = [r for r in all_results if r.get("price", 0) > 0
                     and is_relevant_result(product_name, r.get("product_title", ""))] or all_results
        deduped_for_scan_ai = deduplicate_by_shop(_scan_rel)
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
        threading.Thread(target=save_prices_to_supabase, args=(product_name, result.get("results", all_results)), daemon=True).start()

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
    # in-memory is pre-seeded from Supabase on startup
    sorted_q = sorted(_search_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
    public = [(q, c) for q, c in sorted_q if c >= 2][:limit]
    return jsonify({
        "searches": [{"query": q, "count": c} for q, c in public],
        "total_unique": len(_search_counts)
    })


@app.route("/api/track", methods=["POST"])
def track_click():
    data = request.get_json(silent=True) or {}
    shop = (data.get("shop") or "")[:50].strip()
    query = (data.get("q") or "")[:100].strip()
    if shop:
        _click_counts[shop] = _click_counts.get(shop, 0) + 1
    return "", 204


@app.route("/api/click-stats", methods=["GET"])
def click_stats():
    if not _check_debug_auth():
        return jsonify({"error": "unauthorized"}), 401
    sorted_c = sorted(_click_counts.items(), key=lambda x: x[1], reverse=True)
    return jsonify({"clicks": [{"shop": s, "count": c} for s, c in sorted_c]})


@app.route("/api/cache-stats", methods=["GET"])
def cache_stats():
    if not _check_debug_auth():
        return jsonify({"error": "unauthorized"}), 401
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
        q = v.get("data", {}).get("product_name", "?")
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
        "pigu": f"https://pigu.lt/lt/search?searchPhrase={requests.utils.quote(query)}",
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
        "version": "6.87",
        "uptime_s": uptime_s,
        "shops": ["Varle.lt", "Elesen.lt", "Pigu.lt", "Topo centras", "Amazon.DE", "Amazon.PL"],
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
threading.Thread(target=_sb_load_search_counts, daemon=True).start()


@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "internal_error", "message": "Serverio klaida. Bandykite dar kartą."}), 500


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "not_found"}), 404


if __name__ == "__main__":
    import time as _t
    _server_start = _t.time()

    port = int(os.getenv("PORT", 5000))

    print("\n🟢 Goody API v6.87")
    print(f"📊 Supabase: {'✅ configured' if SUPABASE_URL else '⚠️ not set'}")
    print("📦 Active shops: Varle + Elesen + Pigu + Topo + Amazon.DE + Amazon.PL")
    print(f"🔑 ScraperAPI: {'✅ configured' if SCRAPER_API_KEY else '⚠️ not set'}")
    print(f"🔑 Zyte: {'✅ configured' if ZYTE_API_KEY else '⚠️ not set'}")
    print(f"🤖 Anthropic: {'✅ configured' if ANTHROPIC_API_KEY else '❌ missing'}")
    print(f"🤖 OpenAI: {'✅ configured' if OPENAI_API_KEY else '❌ missing'}")
    print(f"🧠 AI provider: {AI_PROVIDER}")
    print(f"🧠 OpenAI model: {AI_MODEL_OPENAI}")

    app.run(host="0.0.0.0", port=port, debug=False)
