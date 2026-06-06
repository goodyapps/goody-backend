"""
Goody Backend v7.55 — scan-image: extract exact product_code (LEGO #/EAN/SKU/model) + brand/pieces/age; query uses brand+code (no translation); validate code in result titles, mark "Galimai netikslus atitikimas"; AI accepts language param (lt/en/ru/pl/de) and is enforced in prompt; ru added to rule_based_ai_analyze:
- v7.54 — exact model fix: model-query fallback removed (31385 no longer shows 31128); MacBook floor €500; iPhone floor €400; Lego floor €8; verdict_label LT/DE/PL; AI prompt enforces language:
- v7.53 — trigger gaps fixed: valdymo/peiliu/pienu/piestuko/svarstis now detectable as LT queries:
- v7.45 — _LT_DE/PL +knyga/striuke/megztinis/pirstines/suknele/vafline/supuokles/baldai/konstruktorius/pavesine/masinyke:
- v7.44 — _LT_DE/PL +vitaminas/magnio/kreatinas/batai/kedai/sportbaciai/lele/peilis/zirkles/pjaustytuvas/padangos/tepalas/matavimo juosta:
- v7.43 — _static_translate→None fix; _LT_DE/PL +gitara/pianinas/bügnai/smuikas/batutas/slidės/pačiūžos/meškerė/žvejybos/plaukimo/pienukė/lova/spinta/kilimas/vaizdo registratorius:
- v7.42 — _LT_DE/PL +mažas/titanas/akumuliatoriumi/absoliutus/slėgio/aukšto slėgio:
- v7.41 — _LT_DE/PL +atsuktuvas/automobilio/lagaminas/kalėdinė/šunų/kačių/domkratas/elektroninė/durų/baltymų/kolagenas:
- v7.40 — _LT_DE/PL +portativinis/didelis/kompaktiškas/gamintuvas/termosas/makaronų/picos/popierius/benzininis/monitoriaus/grandiklis/dėžutė/ledų/jogurto/sūrio:
- v7.39 — _LT_DE/PL +kėdė/ofiso/motoroleris/dozatorius/detektorius/kortelė/laistyklė/sodo/juostinis/kontaktinis/vėjo/oro/išpurškiklis/stovintis:
- v7.38 — _LT_DE/PL +matuoklis/akiniai/kaukė/slidinėjimo/filtras/kavinukas/kepimo/saulės/operatyvinė/nerūdijantis/maitinimo blokas/kraujospūdžio:
- v7.37 — _LT_DE/PL +šviestuvas/kilimėlis/smulkintuvas/pupelių/greitasis/valdiklis/rašalinis/lazerinis/gliukometras; stalo/grindų lempa fix:
- v7.36 — _LT_DE/PL +colors/automobilinis/radiatorius/navigatorius/skeneris/duoninė/gamybos/soliariumo/bevielis:
- v7.35 — _LT_DE/PL +lygintuvė/lyginimo/multimetras/objektyvas/trikojis/grafikos/procesorius/burnos/žolės/apsaugos/interneto/tinklo/elektros:
- v7.34 — _LT_DE/PL +gręžtuvas/palapinė/miegmaišis/tonometras/inhalatorius/suvirintuvas/mėsmalė/purkštuvas/signalizacija/elipsinis:
- v7.33 — _NOISE_WORDS +jaki/welcher/testsieger; _LT_DE/PL +depiliatorius/garo/plyteliu:
- v7.32 — _LT_DE/PL +motopjuklas/grindų/pramoninis/muzikos/statybinis; plovykla fix:
- v7.31 — _LT_DE/PL +žarna/laistymo/pompa/šalmas/šašlykų; 🚲 helmet/bike pump:
- v7.30 — _LT_DE/PL +šepetys/valiklis/ausų/generatorius/buitinis; 🔋 generator:
- v7.29 — _LT_DE/PL +veidrodis/antklodė/langų/kūno/daugiafunkcinis; 🫧 window cleaner:
- v7.28 — _LT_DE/PL +garintuvas/stalo kompiuteris/veido; _KNOWN_BRANDS +ugreen/baseus:
- v7.27 — _LT_CATEGORY_WORDS/DE/PL +gartraukis/kirptuvas; +stotelė/pistoletas standalone:
- v7.26 — _VARIANT_WORDS +classic; _LT_DE/PL +fitness; _NOISE_WORDS +free shipping/nemokamas:
- v7.25 — _KNOWN_BRANDS/icon +jackery/ecoflow/bluetti🔋; _LT_DE/PL: +galios stotelė/stebėjimo:
- v7.24 — _LT_DE/PL: standalone +kištukas→Steckdose; +jungiklis→Schalter; +skambutis→Türklingel:
- v7.23 — _LT_CATEGORY_WORDS: +kūdikio/lovelė/pistoletas; _LT_DE/PL: +glue/paint gun; +lovelė/kūdikio:
- v7.22 — _ACCESSORY: +scherkopf/zamienny/zapasowy; _NOISE_WORDS: +najtanszy/bestpreis/opinie:
- v7.21 — _LT_DE/PL: +masažo pistoletas→Massagepistole; +masažo→Massage; icon +massage gun🩺:
- v7.20 — _CATEGORY_ICON_MAP: +panasonic/toshiba📺; +hitachi🫧; +avm🌐; +mitsubishi electric🌬️:
- v7.19 — validate_price: _ROBOT_VAC_W +ilife/cecotec; +_GARDENTOOL_W €5; +_DEHUMID_W €15; +_MASSAGE_W €50:
- v7.18 — _LT_DE/PL: +trimeris/masažo kėdė/drėgmės surinktuvas; icon +rasentrimmer🔨 +massagesessel🩺:
- v7.17 — _LT_DE/PL: +ryžių viryklė/maisto džiovintuvas/arbatinukas/galios bankas; _LT_CATEGORY_WORDS:
- v7.16 — _NOISE_WORDS: +ranking/empfehlung/ratgeber/najlepszy/polecany; _KNOWN_BRANDS: +keychron:
- v7.15 — _LT_DE/PL: +vežimėlis/vaikiška kėdutė/kūdikio monitorius; _KNOWN_BRANDS: +bugaboo/cybex/britax/graco:
- v7.14 — _KNOWN_BRANDS: +nest/tado/shelly/sonoff/ring/arlo/tapo/meross; _LT_DE/PL: +termoregliatorius/išmanusis kištukas:
- v7.13 — _NOISE_WORDS: +im test/testbericht/erfahrungen; _LT_DE/PL: +stebėjimo kamera/durų skambutis:
- v7.12 — validate_price: +e-bike €150 floor; +air purifier €25 floor:
- v7.11 — _LT_DE/PL: +krūmapjovė/lapų pūstuvas/žibintas/nebulizatorius; icon +heckenschere/laubbläser🔨 +taschenlampe💡:
- v7.10 — _CATEGORY_ICON_MAP: +sharp/blaupunkt📺; +aeg🫧; +rowenta👕; +instant🍳; +vitamix🥤; +gree🌬️; +seagate/wd/sandisk🖥️:
- v7.09 — validate_price: +air fryer €20 floor; _CATEGORY_ICON_MAP: +frytkownica/heißluftfritteuse🍳:
- v7.08 — _LT_DE/PL: +oras vanduo→Luft-Wasser/powietrze-woda; +oras oras→Luft-Luft:
- v7.07 — _LT_DE/PL: +robotinė vejapjovė→Mähroboter; _LT_CATEGORY_WORDS: +robotinė:
- v7.06 — _NOISE_WORDS: +kaufen/wo kaufen/kupić (DE/PL buy-intent cache hits):
- v7.05 — _CATEGORY_ICON_MAP: lenovo/acer/dell→💻; hisense/tcl→📺; worx/parkside/greenworks→🔨:
- v7.04 — _CATEGORY_ICON_MAP: ilife/cecotec→🤖; krups→☕; validate_price: +monitor€25:
- v7.03 — _KNOWN_BRANDS: +kärcher/gardena; _CATEGORY_ICON_MAP: +gardena/milwaukee/ryobi/festool/einhell/metabo🔨; remove xiaomi air:
- v7.02 — _LT_DE/PL: +akumuliatorius→Akku/akumulator; _LT_CATEGORY_WORDS: +akumuliatorius/akumuliatoriaus:
- v7.01 — _ACCESSORY: +fernbedienung/entkalker/descaler; _CATEGORY_ICON_MAP: +grill/grilis/bbq/weber🍳:
- v7.00 — validate_price: +printer€20/power tool€10; _LT_DE/PL: +planšetinis/nešiojamasis; lg icon bug fix:
- v6.99 — fix: remove lg from TV icon entry (LG washing machine showed 📺); _LT_DE/PL: +planšetinis/nešiojamasis; validate_price: +shaver€10:
- v6.98 — _CATEGORY_ICON_MAP: dyson🧹/intel+amd🖥️/nvidia🎮/bose+sennheiser🎧/jbl🔊/braun🪒/tefal🍳/delonghi☕/lg📺/huawei📱/siemens+zanussi🫧:
- v6.97 — _NOISE_WORDS: +in lithuania/in germany/in poland/in uk/in europe/delivery to; test_matching: +drone/chromecast tests:
- v6.96 — _CATEGORY_ICON_MAP: +chromecast/fire tv/apple tv/nvidia shield📺; _KNOWN_BRANDS: +alienware; _ACCESSORY: +panzerglas/displayschutzglas:
- v6.95 — _ACCESSORY: +schutzfolie/displayschutzfolie/bildschirmschutz/displayschutz/folia; icon: +philips hue💡:
- v6.94 — _LT_DE/PL: +dronas→Drohne/dron; _ACCESSORY: +torba/plecak(PL)/krepšys/kuprinė(LT); icon: +drone📷/kindle📱:
- v6.93 — _ACCESSORY_MATCH_WORDS: +notebooktasche/laptoptasche/kameratasche/rucksack/ladestation/akkuladegerät (DE compound accessory fix):
- v6.92 — _KNOWN_BRANDS: +steelseries/hyperx/rode/klipsch; icons: steelseries/hyperx🎮 rode🎙️ klipsch🔊; _LT_DE/PL: +rekuperatorius/garų stotis:
- v6.91 — _ACCESSORY: +netzadapter; validate_price: +projector€50/treadmill€50; _NOISE_WORDS: +atsiliepimai/apžvalgos; icon: russell hobbs→russell:
- v6.90 — _CATEGORY_ICON_MAP: +kenwood/kitchenaid/ninja/smeg🍳; +sage/russell/breville/melitta☕; +whirlpool/hotpoint/grundig🫧; +leica📷; +shure🎙️; +logitech🖱️; +razer/corsair🎮:
- v6.89 — _KNOWN_BRANDS: +midea/hoover; _CATEGORY_ICON_MAP: liebherr❄️/indesit+candy+beko+gorenje+haier🫧/hoover🧹/midea🌬️:
- v6.88 — _ACCESSORY_MATCH_WORDS: +ladekabel/aufladekabel/netzkabel (DE cable compounds); _LT_DE/PL: +dantų iryklė→Munddusche/irygator:
- v6.87 — _CATEGORY_ICON_MAP: +neff🍳/asko🫧/bauknecht🫧/severin🍳/bomann🍳; _ROBOT_VAC_W: +dreame/ecovacs/eufy; _NOISE_WORDS: +pigiausia/best deal/kur pigiausia:
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
    # Power tools / garden
    'milwaukee', 'ryobi', 'festool', 'einhell',
    'stihl', 'husqvarna', 'worx', 'metabo', 'parkside', 'greenworks',
    'kärcher',  # umlaut spelling of karcher (also 'karcher' without umlaut above)
    'gardena',  # garden tools brand, popular in LT
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
    'levoit', 'blueair', 'coway', 'winix',
    # Health / medical devices
    'beurer', 'omron', 'medisana', 'withings',
    # Kitchen appliances (popular in LT)
    'moulinex', 'krups', 'severin', 'cuisinart', 'bomann',
    # Home appliances (premium/built-in)
    'neff', 'asko',  # smeg already in set above
    # Vacuum + laundry (EU market brands)
    'midea', 'hoover',
    # Gaming peripherals / laptops
    'steelseries', 'hyperx', 'alienware',
    # Professional audio
    'rode', 'klipsch',
    # Audio / home cinema
    'yamaha', 'denon', 'pioneer', 'onkyo', 'marantz', 'audio-technica',
    # Networking / smart home
    'ubiquiti', 'zyxel', 'netgear', 'tp-link', 'fritzbox', 'avm',
    # GPU / PC component brands
    'gigabyte', 'msi', 'zotac', 'sapphire',
    # Smart home / IoT brands (popular in EU/LT)
    'nest', 'tado', 'shelly', 'sonoff', 'ring', 'arlo', 'tapo', 'meross', 'aqara',
    # Baby / child safety brands
    'bugaboo', 'cybex', 'britax', 'graco', 'uppababy',
    # Mechanical keyboards (popular in EU gamer/enthusiast market)
    'keychron', 'ducky', 'glorious',
    # Portable power stations (growing EU market — solar camping, blackout prep)
    'jackery', 'ecoflow', 'bluetti', 'goal zero', 'anker solix',
    # Charging accessories brands (popular in EU market)
    'ugreen', 'baseus',
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
    'battery pack', 'replacement battery', 'baterija',
    # Festool-specific storage system (Systainer = proprietary carry case)
    'systainer',
    # German tool battery pack / power supply accessories
    'akkupack', 'netzteil', 'akku-pack', 'akku',
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
    # German charging/power cables (compound words — "kabel" whole-word would miss these)
    'ladekabel', 'aufladekabel', 'netzkabel', 'verbindungskabel', 'anschlusskabel',
    # German power adapter (compound — "adapter" whole-word would miss it)
    'netzadapter',
    # German charging station / wireless charger
    'ladestation', 'akkuladegerät', 'akkuladegerat',
    # German bag compounds — "tasche" whole-word misses these compound suffixes
    'notebooktasche', 'laptoptasche', 'kameratasche', 'fototasche', 'tabletasche',
    # Backpack (laptop/camera context; passes if query also contains rucksack)
    'rucksack',
    # Polish bag/backpack accessories
    'torba', 'plecak',
    # Lithuanian bag/backpack accessories
    'krepšys', 'krepsys', 'kuprinė', 'kuprine',
    # German screen protector compound words ("folie"/"glas" whole-word misses these)
    'schutzfolie', 'displayschutzfolie', 'bildschirmschutzfolie',
    'bildschirmschutz', 'displayschutz',
    'panzerglas', 'displayschutzglas', 'bildschirmschutzglas',
    # Polish protective film (whole-word "folia" would miss "ochronna folia" but catches alone)
    'folia ochronna', 'folia',
    # German remote control (Fernbedienung = accessory for TV/audio/etc. — not a standalone product search)
    'fernbedienung',
    # Descaler / limescale remover — always a consumable accessory for coffee machines / boilers
    'entkalker', 'descaler', 'odkamieniacz',
    # German shaver head / changeable head compounds — always accessories
    'scherkopf', 'wechselkopf', 'wechselklinge', 'scherfolie',
    # Polish replacement / spare adjectives (zamienny głowica = replacement shaver head)
    'zamienny', 'zamienna', 'zamienne', 'zamiennik',
    'zapasowy', 'zapasowa', 'zapasowe',
    # Lithuanian replacement head / nozzle (skutimosi galvutė, dušo galvutė — always accessory)
    'galvutė', 'galvute', 'galvutės', 'galvutes',
    # Vacuum nozzles/tips (EN/DE/PL/LT) — common Dyson accessory trap
    'nozzle', 'antgalis', 'antgaliai', 'düse', 'końcówka', 'šepetys', 'szczotka',
    # LT battery (standalone replacement battery accessory)
    'baterija', 'baterijos', 'baterijų',
    # EN accessory/attachment/compatible — indicates accessory product
    'accessories', 'attachment', 'compatible',
    # LT "designed for / fits" — skirtas Dyson = replacement part for Dyson
    'skirtas', 'skirta', 'skirtos', 'tinka',
    # Specific battery accessory phrases
    'spare battery', 'extra battery', 'battery for',
    # German razor blades consumable (Rasierklingen for a razor, not a standalone blade search)
    # Note: NOT added — "Rasierklingen" can itself be a main product (pack of razor blades)
})
_VARIANT_WORDS = frozenset({
    'pro', 'max', 'ultra', 'plus', 'lite', 'mini', 'fe', 'edge',
    'note', 'fold', 'flip', 'air', 'neo', 'active', 'sport',
    'slim', 'boost', 'titan', 'classic',
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

    # Check for "for [brand]" / "compatible with" / "skirta [brand]" patterns
    # These indicate accessories FOR a product, not the product itself
    compat_patterns = [
        r'\bfor\s+[a-z]+',  # "for Dyson", "for iPhone"
        r'\bcompatible\s+with\b',  # "compatible with"
        r'\bskirta\s+[a-z]+',  # "skirta Dyson" (LT)
        r'\btinka\s+[a-z]+',  # "tinka Dyson" (LT)
        r'\bgeeignet\s+für\b',  # "geeignet für" (DE)
        r'\bpassend\s+für\b',  # "passend für" (DE)
        r'\bdla\s+[a-z]+',  # "dla [brand]" (PL)
    ]
    for pattern in compat_patterns:
        if re.search(pattern, t) and not re.search(pattern, q):
            return False  # Title says "for X" but query didn't - this is an accessory

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
            # Check "for <brand>" / "compatible with <brand>" — marks this as an ACCESSORY for the brand
            for _br in brands_in_q:
                _br_esc = re.escape(_br)
                if re.search(
                    r'\b(?:for|compatible\s+with|designed\s+for|suitable\s+for|fits|skirtas?\s|tinka\s|für|pour|voor)\s+' + _br_esc,
                    t
                ):
                    return False
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
    # Scooter / moped — before 📱 to prevent xiaomi matching phone icon
    (["motoroleris", "motorolerio", "e-scooter", "elektrinis motoroleris",
      "skuter", "roller", "moped"], "🛵"),
    (["iphone", "samsung galaxy", "xiaomi", "oneplus", "pixel", "telefon", "smartphone",
      "galaxy s", "galaxy a", "redmi", "poco", "motorola", "honor", "realme", "oppo", "vivo", "nothing phone",
      "huawei"], "📱"),
    (["macbook", "laptop", "notebook", "thinkpad", "dell xps", "asus", "surface pro",
      "chromebook", "nesiojamas kompiuteris", "lenovo", "acer", "dell"], "💻"),
    (["ipad", "galaxy tab", "tablet", "kindle", "kobo", "e-reader", "e-book reader"], "📱"),
    (["oled", "qled", " tv ", " tv", "tv ", "television", "televizorius", "fernseher",
      "telewizor", "ekranas", "screen", "55\"", "65\"", "43\"",
      "chromecast", "fire tv", "fire stick", "firestick", "apple tv",
      "nvidia shield", "android tv box", "android tv stick",
      "hisense", "tcl", "sharp", "blaupunkt", "panasonic", "toshiba"], "📺"),
    (["headphone", "earphone", "earbuds", "ausines", "ausinukai", "airpods", "wh-1000", "bose qc",
      "jabra", "beats", "marshall", "kopfhörer", "słuchawki", "audio-technica",
      "bose", "sennheiser"], "🎧"),
    (["playstation", "ps5", "ps4", "xbox", "nintendo", "gamepad", "rtx 4", "rtx 3",
      "geforce", "gaming", "spielkonsole", "konsola", "konsole",
      "gigabyte", "msi", "zotac", "sapphire", "razer", "corsair",
      "steelseries", "hyperx", "alienware", "nvidia"], "🎮"),
    (["camera", "nikon", "canon", "sony zv", "sony alpha", "fotoaparatas", "mirrorless", "dslr",
      "gopro", "dji", "aparat foto", "aparat cyfr", "fujifilm", "olympus", "leica",
      "dronas", "drohne", "dron",
      "ring doorbell", "arlo", "überwachungskamera", "kamera do monitoringu",
      "stebejimo kamera", "security camera"], "📷"),
    (["roomba", "roborock", "irobot", "robot siurblys", "robotinis", "saugroboter",
      "dreame", "ecovacs", "eufy", "ilife", "cecotec"], "🤖"),
    # Heat pump must come before generic "siurblys"→🧹 so "silumos siurblys" matches here first
    (["wärmepumpe", "warmepumpe", "pompa ciepla", "silumos siurblys", "silumos pompa", "heat pump", "daikin"], "🌬️"),
    # Steam cleaner / steam mop — before generic vacuum entry
    (["dampfreiniger", "myjka parowa", "garu valytuvas", "dampfsauger", "odkurzacz parowy",
      "steam cleaner", "steam mop", "garintuvas", "garintuvo",
      "dampfbesen", "dampfburste", "parownica", "parownik",
      "fensterreiniger", "langu valytuvas", "myjka do okien", "window cleaner"], "🫧"),
    (["dulkiu siurblys", "siurblys", "vacuum", "dyson v", "miele",
      "staubsauger", "odkurzacz", "hoover", "dyson"], "🧹"),
    (["skalbykle", "washing machine", "waschmaschine", "pralka", "indaplove",
      "dishwasher", "spülmaschine", "zmywarka", "bosch wan", "samsung ww",
      "asko", "bauknecht", "constructa", "indesit", "candy", "beko", "gorenje", "haier",
      "whirlpool", "hotpoint", "grundig", "siemens", "zanussi", "electrolux", "aeg", "hitachi"], "🫧"),
    (["virdulys", "kettle", "kavos", "nespresso", "wasserkocher", "kaffeemaschine",
      "czajnik", "ekspres", "sage", "russell", "breville", "melitta", "delonghi", "krups"], "☕"),
    (["keptuve", "blender", "mikser", "multicooker", "air fryer", "gruzdintuve",
      "heißluftfritteuse", "heissluftfritteuse", "frytkownica",
      "robot kuchenny", "kuchenny", "thermomix", "küchenmaschine", "maisto procesorius",
      "instant pot", "instant vortex",
      "gasherd", "kuchenka gazowa", "duju virykle", "virykle", "induktion",
      "indukcinis", "indukcine", "kaitlente", "kochfeld",
      "grill", "grilis", "bbq", "barbecue", "weber",
      "gaubtas", "gartraukis", "dunstabzugshaube", "okap kuchenny",
      "moulinex", "krups", "cuisinart", "neff", "severin", "bomann",
      "kenwood", "kitchenaid", "ninja", "smeg", "tefal", "instant"], "🍳"),
    (["lego", "zaislai", "pampers", "chicco", "fisher-price", "baby",
      "kinderwagen", "wózek dziecięcy", "wozek dzieciecy", "vežimėlis", "vezimelis",
      "kindersitz", "fotelik samochodowy", "kėdutė", "kedute",
      "babyphone", "niania elektroniczna", "kūdikio", "kudikio",
      "babybett", "lopšelis", "lopselis",
      "bugaboo", "cybex", "britax", "graco", "uppababy"], "🧸"),
    (["monitor", "monitorius", "gaming monitor", "display", "bildschirm", "ekran komputerowy"], "🖥️"),
    (["ssd", "nvme", "hdd", "ram ddr", "corsair", "kingston fury",
      "procesorius", "cpu", "ryzen", "core i", "festplatte", "dysk ssd",
      "intel", "amd", "seagate", "sandisk", "wd my", "wd elements", "wd blue", "wd black", "wd red"], "🖥️"),
    (["spausdintuvas", "printer", "scanner", "hp laserjet", "epson", "drucker", "drukarka"], "🖨️"),
    (["air purifier", "luftreiniger", "oczyszczacz powietrza", "oro valytuvas",
      "levoit", "blueair", "coway", "winix"], "💨"),
    (["luftbefeuchter", "oro drekintuvas", "nawilżacz powietrza", "humidifier",
      "luftentfeuchter", "pochłaniacz wilgoci", "drėgmės surinktuvas", "dregmes surinktuvas",
      "dehumidifier"], "💧"),
    (["svarstykles", "körperwaage", "korperwaage", "body scale", "body fat scale",
      "personenwaage", "waga lazienkowa"], "⚖️"),
    (["beurer", "omron", "medisana", "withings", "blood pressure", "kraujospy dis",
      "tensiometro", "cisnienomierz", "blutdruckmessgerats", "tonometras", "tonometro",
      "pulsometras", "pulsometro", "pulsmesser", "pulsometr",
      "inhalatorius", "inhaliatoriaus", "inhalationsgerats", "nebulizatorius", "nebulizator", "inhalator", "inhaler",
      "gliukometras", "gliukometro", "blutzuckermessgerats", "glukometr",
      "burnos dusas", "munddusche", "irygator",
      "massagesessel", "massage chair", "fotel masujacy", "masazo kede",
      "massage gun", "massagepistole", "pistolet do masazu"], "🩺"),
    (["philips shav", "braun series", "gillette", "oral-b", "skustuvas", "epilator",
      "toothbrush", "zahnbürste", "sepetelis", "šepetėlis", "szczoteczka", "braun",
      "kirptuvas", "haarschneider", "haarschneidemaschine", "maszynka do strzyzenia",
      "veidrodis", "kosmetikspiegel", "kosmetinis", "spiegel", "lustro"], "🪒"),
    (["laikrodis", "smartwatch", "apple watch", "garmin", "fitbit", "samsung watch", "fossil", "polar", "suunto",
      "zegarek"], "⌚"),
    (["paspirtukas", "e-roller", "elektroroller", "hulajnoga elektryczna"], "🛴"),
    (["dviratis", "elektrinis dviratis", "e-bike", "ebike", "scooter", "fahrrad", "rower",
      "salmas", "šalmas", "fahrradhelm", "kask rowerowy", "kask",
      "fahrradpumpe", "pompka rowerowa", "dviraciu pompa"], "🚲"),
    (["saldytuvas", "saldiklis", "saldymo", "kühlschrank", "gefrierschrank",
      "lodówka", "zamrażarka", "lodowka", "zamrazarka", "liebherr"], "❄️"),
    (["kondicionierius", "oro kondicionierius", "klimaanlage", "klimatyzator", "midea", "gree",
      "mitsubishi electric", "mitsubishi heavy"], "🌬️"),
    (["makita", "dewalt", "bosch gsr", "graztas", "pjuklas", "power tool", "drill", "grąžtas",
      "šlifuoklis", "slifuoklis", "suktukas", "kampinis", "winkelschleifer", "schleifer",
      "schrauber", "bohrmaschine", "szlifierka", "wiertarka", "wkrętarka", "perforatorius",
      "greztuvas", "gréztuvas", "atsuktuvas", "suvirintuvas", "schweissgeräts", "spawarka",
      "mesmalė", "mesmalę", "fleischwolf", "maszynka do miesa",
      "bandsäge", "bandsage", "pilarka tasmowa",
      "karcher", "kärcher", "hochdruckreiniger", "myjka cisnieniowa", "plovykla",
      "stihl", "husqvarna", "gardena", "milwaukee", "ryobi", "festool", "einhell", "metabo",
      "worx", "parkside", "greenworks",
      "heckenschere", "laubbläser", "laubblaser", "nożyce do żywopłotu", "dmuchawa do liści",
      "rasentrimmer", "podkaszarka", "trimeris",
      "krūmapjovė", "krumapjove", "lapų pūstuvas", "lapu pustuvas"], "🔨"),
    (["begimu takelis", "begimo takelis", "laufband", "treadmill", "treniruoklis", "bieżnia",
      "hanteliai", "hantel", "hanteln", "kettlebell", "svarsciai", "svarsčiai",
      "ciężary", "gewicht", "hantle", "fitnessgerät", "sprzęt fitness"], "🏃"),
    (["projektorius", "projector", "projektor", "beamer"], "📽️"),
    (["sulciaspaude", "sulciu", "juicer", "entsafter", "wyciskarka", "vitamix"], "🥤"),
    (["garsiakalbis", "garsine", "kolonele", "soundbar", "lautsprecher", "głośnik", "speaker",
      "tragbarer lautsprecher", "głośnik przenośny", "sonos", "harman kardon",
      "yamaha", "denon", "marantz", "pioneer", "onkyo", "klipsch", "jbl"], "🔊"),
    (["pelė", "pele", "maus", "mouse", "mysz", "logitech"], "🖱️"),
    (["laidynas", "lygintuvas", "bügeleisen", "bugeleisen", "żelazko", "dampfbügeleisen", "dampfbugeleisen", "rowenta"], "👕"),
    (["ziuronai", "fernglas", "lornetka", "binocular"], "🔭"),
    (["mikrofonas", "microphone", "mikrofon", "condenser mic", "podcast", "shure", "rode"], "🎙️"),
    (["marsrutizatorius", "router", "mesh wifi", "access point", "switch", "tinklo",
      "tp-link", "ubiquiti", "netgear", "zyxel", "fritzbox", "fritz!box", "avm"], "🌐"),
    (["klaviatura", "klaviatūra", "keyboard", "klawiatura", "tastatur", "mechanine",
      "keychron", "ducky", "glorious"], "⌨️"),
    (["zadintuvas", "zadintuva", "wecker", "budzik", "alarm clock"], "⏰"),
    (["lempa", "lampe", "lampa", "lempute", "lemputes", "led juosta", "led strip", "led lamp", "smart lamp",
      "sviestuvas", "sviestuvai", "prozektorius", "philips hue", "hue", "smart bulb",
      "smart light", "zigbee", "nanoleaf",
      "taschenlampe", "latarka", "žibintas", "zibintas", "flashlight", "torch",
      "thermostat", "termoregliatorius", "termoreguliatorius", "smart thermostat",
      "smart steckdose", "smart plug", "smarte steckdose",
      "nest", "tado", "shelly", "sonoff", "meross", "aqara", "tapo"], "💡"),
    (["boileris", "bojler", "warmwasserbereiter", "podgrzewacz wody",
      "vandens sildytuvas", "water heater", "katilas", "gaskessel", "kociol",
      "vaillant", "viessmann", "baxi", "ariston"], "🚿"),
    (["power station", "powerstation", "portable power", "solar generator",
      "jackery", "ecoflow", "bluetti", "goal zero", "anker solix",
      "galios stotelė", "galios stotele",
      "generatorius", "generator", "agregat pradotwor", "inverter generator"], "🔋"),
    (["nokia"], "📱"),
    # Outdoor / camping / travel
    (["palapine", "palapinė", "zelt", "namiot", "tent",
      "miegmaisis", "miegmaišis", "schlafsack", "spiwor", "sleeping bag",
      "lagaminas", "lagamino", "koffer", "walizka", "suitcase"], "⛺"),
    # Office furniture / ergonomics
    (["ofiso kede", "ofiso kėdė", "burotuhl", "burostuhl", "krzeslo biurowe",
      "stovintis stalas", "stehschreibtisch", "biurko stojace",
      "ergonomine", "ergonomiškas"], "🪑"),
    # Alarm / detector / security
    (["signalizacija", "signalizacijos", "alarmanlage", "alarm",
      "dumu detektorius", "rauchmelder", "czujnik dymu",
      "co-melder", "czujnik co", "monoksido detektorius",
      "detektorius", "detektor"], "🚨"),
    # Christmas / seasonal
    (["kaledine", "kalėdinė", "eglute", "eglutė", "weihnachtsbaum", "choinka",
      "christmas"], "🎄"),
    # Music instruments (v7.43)
    (["gitara", "gitaros", "gitarre", "gitara yamaha", "fender", "acoustic guitar",
      "electric guitar", "classical guitar"], "🎸"),
    (["pianinas", "pianino", "klavier", "piano", "elektrinis pianinas", "e-piano",
      "sintezatorius", "synthesizer", "syntezator", "keyboard instrument",
      "yamaha p-", "roland fp", "casio px", "korg b"], "🎹"),
    (["bugnas", "bugnu", "schlagzeug", "perkusja", "drums", "drum kit", "e-drums",
      "smuikas", "skrzypce", "geige", "violine", "violin",
      "fleita", "flet", "flöte", "flute"], "🥁"),
    # Sports / outdoor (v7.43)
    (["batutas", "batuto", "trampolin", "trampolina", "trampoline"], "🤸"),
    (["slidu", "ski ", "skibrille", "skihelm", "narty "], "⛷️"),
    (["paciuzos", "paciuzu", "schlittschuhe", "łyżwy", "ice skates", "patines"], "⛸️"),
    (["meskere", "meskeriu", "angelrute", "wedka", "wędka", "fishing rod",
      "zvejybos", "zvejyba", "angeln", "wedkarstwo", "wedkarski", "fishing"], "🎣"),
    # Furniture / textiles (v7.43)
    (["lova", "lovos", "bett", "lodko", "łóżko", "bed frame", "lozko",
      "spinta", "spintos", "kleiderschrank", "szafa", "wardrobe",
      "kilimas", "kilimo", "teppich", "dywan", "carpet", "rug"], "🛋️"),
    # Dashcam (v7.43)
    (["vaizdo registratorius", "registratorius", "dashcam", "dash cam",
      "wideorejestrator", "blackvue", "viofo", "nextbase", "70mai"], "📹"),
    # Books (v7.45)
    (["knyga", "knygos", "knygu", "buch ", "bucher", "bücher", "książka", "ksiazka",
      "programavimo knyga", "knygu rinkinys"], "📚"),
    # Clothing (v7.45)
    (["striuke", "striuku", "jacke", "kurtka",
      "megztinis", "megztinio", "pullover", "sweter",
      "suknele", "sukneles", "kleid", "sukienka",
      "kostiumas", "kostiumo", "kostüm", "kostium",
      "pirstines", "pirstiniu", "handschuhe", "rękawiczki", "rekawiczki",
      "vafline", "vafliu", "waffeleisen", "gofrownica"], "👕"),
    # Swing / outdoor play (v7.45)
    (["supuokles", "supuokliu", "schaukel", "huśtawka", "hustawka",
      "pavesine", "pavesines", "pavillon", "pawilon"], "🏡"),
    # Furniture (v7.45)
    (["baldai", "baldu", "möbel", "mebel", "meble",
      "lauko baldai", "vaiku baldai", "biuro baldai",
      "gartenmöbel", "kindermöbel", "meble ogrodowe", "ikea"], "🛋️"),
    # Construction toy / toy car (v7.45)
    (["konstruktorius", "konstruktoriaus", "bausatz", "zestaw konstrukcyjny",
      "masinyke", "masiniu", "spielzeugauto", "samochodzik", "matchbox", "hot wheels"], "🧸"),
    # Milk frother (v7.43)
    (["pienuke", "pienuku", "pienu putuke", "milchaufschäumer", "milchaufschaeumer",
      "spieniacz do mleka", "milk frother", "aeroccino"], "☕"),
    # Shoes / footwear (v7.44)
    (["batai", "batu", "kedai", "sportbaciai", "sportiniai batai",
      "schuhe", "sneaker", "buty", "trampki", "adidas", "nike", "puma", "new balance",
      "skechers", "converse", "vans", "reebok", "asics", "salomon"], "👟"),
    # Vitamins / supplements (v7.44)
    (["vitaminas", "vitaminu", "vitaminai", "vitamin", "witamina",
      "kreatinas", "kreatin", "kreatyna",
      "magnio", "magnis", "magnesium", "magnez",
      "omega 3", "omega-3", "kolagenas", "kollagen", "kolagen",
      "baltymu", "protein", "bialko", "suplement"], "💊"),
    # Kitchen knife / scissors (v7.44)
    (["peilis", "peilio", "peiliai", "messer", "nóż", "noz",
      "zirkles", "zirkliu", "schere", "nozyczki", "nożyczki",
      "fiskars", "victorinox", "wusthof", "zwilling", "henckels"], "🍴"),
    # Car tyres (v7.44)
    (["padangos", "padanga", "reifen", "opony", "opona",
      "winterreifen", "sommerreifen", "opony zimowe", "opony letnie",
      "michelin", "continental", "bridgestone", "pirelli", "goodyear", "nokian"], "🚗"),
    # Lubricant / engine oil (v7.44)
    (["tepalas", "tepalo", "motorol", "motoröl", "olej silnikowy",
      "schmiermittel", "castrol", "mobil 1", "shell helix", "liqui moly"], "🔧"),
    # Doll (v7.44)
    (["lele", "leles", "puppe", "lalka", "barbie", "baby born"], "🪆"),
    # Food slicer (v7.44)
    (["pjaustytuvas", "pjaustytuvo", "aufschnittmaschine", "krajalnica",
      "food slicer", "meat slicer"], "🍕"),
    # Perfume / candle / photo frame / shampoo (v7.46)
    (["kvepalai", "kvepalu", "parfumas", "parfumo", "parfüm", "parfum",
      "eau de toilette", "edt", "edp", "cologne", "fragrance"], "🌸"),
    (["zvake", "zvakiu", "aromatine zvake", "duftkerze", "świeca", "swieca",
      "kerze", "candle"], "🕯️"),
    (["ramelis", "ramelio", "foto ramelis", "bilderrahmen", "ramka", "photo frame",
      "picture frame", "fotorahmen"], "🖼️"),
    (["sampunas", "sampuno", "shampoo", "szampon", "haarshampoo"], "🧴"),
    # Sports — tennis / badminton (v7.46)
    (["teniso rakete", "stalo teniso rakete", "badmintono rakete",
      "tenisschläger", "tischtennisschläger", "badmintonschläger",
      "rakieta tenisowa", "rakietka do tenisa", "rakieta badmintonowa",
      "tennisschläger", "racket", "tenisas", "teniso", "badmintonas"], "🎾"),
    # Football (v7.46)
    (["futbolo kamuolys", "futbolas", "futbolo", "fußball", "fussball",
      "piłka nożna", "pilka nozna", "football", "soccer ball"], "⚽"),
    # Basketball (v7.46)
    (["krepsinio kamuolys", "krepsis", "krepsinio", "basketball", "basketballkorb",
      "piłka do koszykówki", "kosz do koszykówki"], "🏀"),
    # Snowboard / skateboard (v7.46)
    (["snieglente", "snieglenciu", "snowboard", "deska snowboardowa"], "🏂"),
    (["riedlente", "riedlenciu", "skateboard", "deskorolka"], "🛹"),
    # Pillow / bedding (v7.46)
    (["pagalve", "pagalviu", "ortopedine pagalve", "kissen", "poduszka",
      "kopfkissen", "schlafkissen"], "🛏️"),
    (["patalyne", "patalynes", "bettwäsche", "bettwaesche", "pościel", "posciel",
      "bettbezug", "duvet cover"], "🛏️"),
    # Thermos mug (v7.46)
    (["termopuodelis", "termopuodelio", "termosinis puodelis", "termo puodelis",
      "thermobecher", "kubek termiczny", "travel mug", "thermos mug",
      "hydro flask", "stanley cup", "contigo", "yeti"], "☕"),
    # Sofa / armchair / shelf / dresser (v7.47)
    (["sofa", "sofos", "schlafsofa", "ecksofa", "sofa rozkładana", "sofa narożna"], "🛋️"),
    (["fotelis", "fotelio", "sessel", "fotel", "recliner", "armchair"], "🪑"),
    (["lentyna", "lentynu", "regal", "regal ", "półka", "polka", "bookshelf", "shelf"], "📦"),
    (["komoda", "komodu", "kommode", "dresser", "chest of drawers"], "🪞"),
    # Clothing (v7.47)
    (["kepure", "kepures", "kepurė", "mutze", "mütze", "czapka", "hat ", "beanie", "cap "], "🧢"),
    (["salikas", "saliko", "šalikas", "schal", "szalik", "scarf"], "🧣"),
    (["kelnes", "kelniu", "kelnės", "hose", "spodnie", "trousers", "pants"], "👖"),
    (["marskiniai", "marskiniu", "marškiniai", "hemd", "koszula", "shirt"], "👔"),
    (["dzinsai", "dzinsu", "džinsai", "jeans", "jeansy"], "👖"),
    (["maudymosi kostiumelis", "maudymosi", "badeanzug", "badehose", "stron kapielowy", "swimsuit", "bikini"], "🩱"),
    # Boxing (v7.47)
    (["boksas", "bokso", "boxen", "boxsack", "boxhandschuhe", "boks", "bokserski", "boxing"], "🥊"),
    # Roller skates / sled (v7.47)
    (["riedutis", "rieduciu", "inlineskates", "rolki", "wrotki", "roller skates"], "⛸️"),
    (["roges", "rogiu", "rogės", "schlitten", "sanki", "sled", "sledge"], "🛷"),
    # Water bottle (v7.47)
    (["gertuve", "gertuviu", "gertuvė", "trinkflasche", "bidon", "water bottle", "sports bottle",
      "hydro flask", "nalgene", "camelbak"], "🍶"),
    # Diapers (v7.47)
    (["sauskelnes", "sauskelnems", "sauskelnės", "windeln", "pieluchy", "pampers", "huggies",
      "baby wipes", "diaper"], "👶"),
    # Yoga (v7.47)
    (["jogos kilimelis", "jogos", "yogamatte", "yoga mat", "mata do jogi", "yoga block",
      "yoga", "pilates mat"], "🧘"),
    # Bags / accessories (v7.48)
    (["kuprine", "kuprines", "kuprinė", "rucksack", "plecak", "backpack",
      "kinderrucksack", "schulrucksack"], "🎒"),
    (["rankine", "rankines", "rankinė", "handtasche", "torebka", "handbag", "purse",
      "schultertasche", "umhängetasche"], "👜"),
    (["portfelis", "portfelio", "aktentasche", "aktówka", "briefcase"], "💼"),
    (["piniginė", "pinigines", "geldbörse", "portfel", "wallet", "geldbeutel"], "👛"),
    (["dirzas", "dirzo", "gürtel", "pasek", "belt", "ledergürtel"], "🧶"),
    # Jewelry (v7.48)
    (["papuošalai", "papuosalu", "schmuck", "biżuteria", "jewelry", "jewellery",
      "karoliai", "karoliu", "halskette", "naszyjnik", "necklace",
      "auskarai", "auskariu", "ohrringe", "kolczyki", "earrings",
      "ziedas", "ziedo", "pierścionek", "ring jewelry"], "💍"),
    # Kitchen / home (v7.48)
    (["puodelis", "puodelio", "tasse", "kubek", "mug ", "cup "], "☕"),
    (["dubuo", "dubens", "schüssel", "miska", "bowl", "suppenschüssel"], "🥣"),
    (["vazonas", "vazono", "blumentopf", "doniczka", "flower pot", "planter"], "🪴"),
    # Tarpaulin / tent cover (v7.48)
    (["tentas", "tento", "plane ", "plandeka", "tarpaulin", "autoplane",
      "campingplane"], "⛺"),
    # Sewing machine (v7.48)
    (["siuvimo mašina", "siuvimo", "nähmaschine", "maszyna do szycia",
      "sewing machine", "singer", "brother cs"], "🧵"),
    # Toy adjective (v7.48)
    (["zaislinis automobilis", "zaislinis", "spielzeugauto", "samochodzik zabawka",
      "spielzeug", "zabawkowy"], "🧸"),
    # Beauty / skincare (v7.49)
    (["kremas", "kremo", "veido kremas", "kuno kremas", "ranku kremas",
      "feuchtigkeitscreme", "gesichtscreme", "körpercreme", "creme",
      "krem nawilżający", "krem do twarzy", "krem do ciała",
      "losjonas", "losjono", "lotion", "balsam",
      "dezodorantas", "dezodoranto", "deodorant", "dezodorant",
      "cerave", "la roche", "nivea", "neutrogena", "vichy"], "🧴"),
    # Bathtub / bathroom (v7.49)
    (["vonia", "vonios", "badewanne", "wanna", "duschkabine", "kabina prysznicowa",
      "bathtub", "whirlpool", "jacuzzi"], "🛁"),
    # Towel (v7.49)
    (["rankslostis", "ranklosciu", "handtuch", "ręcznik", "recznik", "towel"], "🛁"),
    # Pet supplies singular (v7.49)
    (["katinas", "katino", "kater", "kot "], "🐱"),
    (["augintinis", "augintinio", "haustier", "zwierzak", "pet supply", "zooplus"], "🐾"),
    # Hunting (v7.49)
    (["medziokle", "medziokles", "jagd", "myślistwo", "hunting", "hunt"], "🏹"),
    # Knee pads / protection (v7.49)
    (["sliauztukai", "sliauztukas", "knieschoner", "nakolanniki", "knee pad",
      "knieschützer", "elbow pad"], "🦺"),
    # Car radio (v7.50)
    (["automagnetola", "automagnetolos", "automobilio radijas", "autoradio", "radio samochodowe",
      "pioneer avh", "kenwood ddx", "alpine ine", "sony xav"], "📻"),
    # Steering wheel / car wheels (v7.50)
    (["vairas", "vairo", "lenkrad", "kierownica", "steering wheel"], "🚗"),
    (["ratai", "ratu", "felgen", "felgi", "autoräder", "alloy wheel"], "🚗"),
    # Home improvement (v7.50)
    (["dazai", "dazo", "sienu dazai", "farbe", "farba", "paint ", "wandfarbe",
      "lauko dazai", "lacquer", "primer"], "🖌️"),
    (["tapetai", "tapetu", "tapete", "tapeta", "wallpaper"], "🏠"),
    (["laminatas", "laminato", "parketas", "parketo", "laminat", "parkett",
      "panele podłogowe", "parkiet", "laminate flooring", "vinyl flooring"], "🏠"),
    # More music instruments (v7.50)
    (["akordeonas", "akordeono", "akkordeon", "akordeon", "accordion"], "🪗"),
    (["trimitas", "trimito", "trompete", "trąbka", "trumpet",
      "saksofonas", "saksofono", "saxophon", "saksofon", "saxophone",
      "klarnetas", "klarinette", "klarnet", "clarinet"], "🎺"),
    # Stationery (v7.50)
    (["pieštukas", "piestukas", "bleistift", "ołówek", "pencil",
      "flomasteris", "flomasteri", "filzstift", "flamaster", "marker pen",
      "tušinukas", "kugelschreiber", "długopis", "ballpoint"], "✏️"),
    # Garden fountain (v7.50)
    (["fontanas", "fontano", "brunnen", "fontanna", "fountain", "gartenbrunnen"], "⛲"),
    # Window treatments (v7.51)
    (["uzdanga", "uzdangu", "uzuolaida", "uzuolaidų", "vorhang", "zasłona", "zaslona",
      "curtain", "gordijn", "gardine", "fenstergardine"], "🪟"),
    (["rolete", "roletu", "rollo", "roleta", "roller blind", "blackout blind",
      "zaluzija", "zaluziju", "jalousie", "żaluzja", "venetian blind"], "🪟"),
    # Bedding addition (v7.51)
    (["paklode", "paklodziu", "bettlaken", "spannbettlaken", "prześcieradło", "przescieradlo",
      "fitted sheet", "bedsheet"], "🛏️"),
    (["apklotas", "apklotu", "decke", "koc ", "throw blanket", "fleece blanket",
      "wolldecke", "strickdecke"], "🛏️"),
    # Water sports (v7.51)
    (["baseinas", "baseino", "schwimmbecken", "basen", "pool ", "planschbecken",
      "aufblasbarer pool", "swimming pool", "intex pool"], "🏊"),
    (["baidarele", "baidareles", "kanoja", "kanojos", "kajak", "kanu", "canoe",
      "kayak", "kanu "], "🛶"),
    (["irklai", "irklu", "paddel", "wiosło", "wiosla", "paddle", "oar"], "🛶"),
    # Cables / electrical (v7.51)
    (["kabelis", "kabelio", "laidas", "laido", "kabel ", "kabel usb",
      "tinklines", "tinkliniu", "steckdosenleiste", "listwa zasilająca",
      "power strip", "extension cord", "hdmi", "displayport", "usb-c cable"], "🔌"),
    # Arts / crafts (v7.51)
    (["plastilinas", "plastilino", "knete", "plastelina", "plasticine", "modeling clay",
      "fimo", "sculpey", "air dry clay"], "🎨"),
    # Flooring / tiles (v7.51)
    (["grindys", "grindylentu", "boden", "podłoga", "dielen", "deski podłogowe",
      "vinyl floor", "floor panel"], "🏠"),
    (["plytelis", "plyteliu", "fliese", "fliesen", "płytka ceramiczna", "ceramic tile",
      "plytelių klijai", "floor tile"], "🏠"),
    # Hammock (v7.52)
    (["hamakas", "hamaku", "hängematte", "hamak", "hammock"], "🪢"),
    # Earbud singular (v7.52)
    (["ausinukas", "ausinuko", "ohrhörer", "słuchawki douszne", "in-ear"], "🎧"),
    # Fitness equipment (v7.52)
    (["menteliklis", "klimmzugstange", "drążek do podciągania", "pull-up bar"], "🏋️"),
    (["stanga", "stangos", "langhantel", "sztanga", "barbell"], "🏋️"),
    (["suoliukas", "preso suoliukas", "hantelbank", "ławka treningowa", "weight bench"], "🏋️"),
    # SUP board (v7.52)
    (["irklente", "irklentes", "sup-board", "deska sup", "paddleboard", "sup board"], "🏄"),
    # Camping gear (v7.52)
    (["stovyklavimo kede", "stovyklavimo stalas", "stovyklavimo virykle",
      "campingstuhl", "campingtisch", "campingkocher", "krzesło campingowe",
      "camping chair", "camping table", "camping stove"], "⛺"),
    # Amino acids supplement (v7.52)
    (["aminorugsciai", "aminoru", "aminosäuren", "aminokwasy", "amino acids", "bcaa", "eaa"], "💊"),
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
    r'atsiliepimai|apžvalgos|apzvalgos|'
    r'compare|palyginti|vergleichen|porównaj|'
    r'discount|sale|angebote|oferta|rabat|akcija|nuolaida|nuolaidos|'
    r'pirkti|internetu|kur nusipirkti|išpardavimas|'
    r'promocja|wyprzedaż|recenzja|gdzie kupić|preisvergleich|'
    r'wo kaufen|kaufen|kupić|'
    r'im test|testbericht|erfahrungen|erfahrungsbericht|empfehlung|ratgeber|'
    r'ranking|najlepszy|najlepsza|polecany|polecana|najtanszy|najtansza|opinie|'
    r'bestpreis|gunstigste|gunstigsten|'
    r'lietuva|lietuvoje|vokietija|vokietijoje|lenkija|lenkijoje|anglijoje|'
    r'deutschland|polska|in deutschland|in poland|'
    r'in lithuania|in germany|in uk|in europe|delivery to|shipped to|'
    r'nemokamas pristatymas|nemokamas|free delivery|free shipping|'
    r'versandkostenfrei|kostenloser versand|gratis versand|'
    r'bezplatna dostawa|darmowa dostawa|'
    r'jaki|jaka|jakie|'
    r'welcher|welche|welches|welchem|welchen|'
    r'testsieger|'
    r'lithuania|germany|poland)\b',
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
                "robot odkurzający", "robot sprzątający", "dreame", "ecovacs", "eufy", "ilife", "cecotec"]
_GARDENTOOL_W = ["heckenschere", "laubbläser", "laubblaaser", "rasentrimmer", "nożyce do żywopłotu",
                  "dmuchawa do liści", "dmuchawa", "podkaszarka", "krūmapjovė", "krumapjove",
                  "lapų pūstuvas", "lapu pustuvas", "trimeris"]  # garden tools ≥ €5
_DEHUMID_W   = ["luftentfeuchter", "entfeuchter", "pochłaniacz wilgoci", "odwilżacz",
                "drėgmės surinktuvas", "dregmes surinktuvas", "dehumidifier"]  # dehumidifiers ≥ €15
_MASSAGE_W   = ["massagesessel", "massage chair", "fotel masujący", "fotel masujacy",
                "masažo kėdė", "masazo kede"]  # massage chairs ≥ €50
_CONSOLE_W  = ["playstation 5", "ps5", "xbox series x", "xbox series s", "nintendo switch"]
_VACUUM_W   = ["dulkių siurblys", "dulkiu siurblys", "siurblys", "staubsauger", "odkurzacz", "vacuum cleaner", "dyson v"]
_WATCH_W    = ["apple watch", "samsung watch", "galaxy watch", "garmin", "smartwatch"]
_SPEAKER_W  = ["sonos", "harman kardon"]  # premium speakers: cheapest model >€150
_PRESSURE_W = ["hochdruckreiniger", "myjka cisnieniowa", "pressure washer", "karcher", "kärcher",
               "plovykla", "aukstojo sleglio"]  # cheapest pressure washers ~€30
_MOWER_W    = ["rasenmäher", "rasenmaher", "kosiarka", "žoliapjovė", "zoliapjove",
               "vejapjovė", "vejapjove"]  # cheapest electric mowers ~€80
_PROJECTOR_W = ["projektorius", "projector", "projektor", "beamer"]  # cheapest ~€50
_TREADMILL_W = ["laufband", "treadmill", "bieżnia", "bėgimo takelis", "begimo takelis"]  # cheapest ~€100
_SHAVER_W   = ["skustuvas", "rasierer", "golarka", "elektrinis skustuvas", "epilatorius", "epilator"]  # cheapest ~€10
_PRINTER_W  = ["spausdintuvas", "printer", "drucker", "drukarka"]  # cheapest inkjet ~€30
_POWERTOOL_W = ["bohrmaschine", "wiertarka", "akkuschrauber", "wkrętarka", "bohrhammer",
                "elektrinis grąžtas", "kampinis šlifuoklis", "winkelschleifer", "szlifierka katowa",
                "greztuvas", "gręžtuvas", "atsuktuvas", "suvirintuvas", "schweissgerats"]  # floor €10
_MONITOR_W  = ["monitorius", "gaming monitor", "computer monitor", "pc monitor",
               "bildschirm", "ekran komputerowy", "ekran do komputera"]  # PC monitors ≥ €25
_AIRFRYER_W = ["gruzdintuvė", "gruzdintuve", "air fryer", "heißluftfritteuse", "heissluftfritteuse",
               "frytkownica beztłuszczowa", "frytkownica"]  # air fryers ≥ €20
_EBIKE_W    = ["elektrinis dviratis", "e-bike", "ebike", "e fahrrad", "e-fahrrad",
               "pedelec", "rower elektryczny"]  # e-bikes ≥ €150
_AIRPUR_W   = ["air purifier", "luftreiniger", "oczyszczacz powietrza", "oro valytuvas",
               "levoit", "blueair", "coway", "winix"]  # air purifiers ≥ €25
_LEGO_W     = ["lego"]  # Lego sets: cheapest official set ~€8
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

    # MacBook: cheapest refurb ~€500; filters counterfeit/accessory listings
    if any(w in q for w in _MACBOOK_W) and price < 500:
        return 0.0

    # iPhone: cheapest supported model refurb ~€400
    if any(w in q for w in _IPHONE_W) and price < 400:
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

    # Projector: cheapest pico projector ~€50 — prevents centai misidentification
    if any(w in q for w in _PROJECTOR_W) and price < 20:
        return 0.0

    # Treadmill: even cheapest folding treadmill ~€100
    if any(w in q for w in _TREADMILL_W) and price < 40:
        return 0.0

    # Electric shaver / epilator: cheapest entry-level ~€10
    if any(w in q for w in _SHAVER_W) and price < 10:
        return 0.0

    # Printer: cheapest inkjet ~€30 — prevents centai misidentification
    if any(w in q for w in _PRINTER_W) and price < 20:
        return 0.0

    # Power tool (drill/saw/grinder): cheapest entry Parkside ~€10
    if any(w in q for w in _POWERTOOL_W) and price < 10:
        return 0.0

    # PC monitor: cheapest 24" starts at ~€70 new, ~€30 used
    if any(w in q for w in _MONITOR_W) and price < 25:
        return 0.0

    # Air fryer: cheapest entry models start at ~€20
    if any(w in q for w in _AIRFRYER_W) and price < 20:
        return 0.0

    # E-bike: cheapest entry pedal-assist starts at ~€300; floor at €150 to catch centai
    if any(w in q for w in _EBIKE_W) and price < 150:
        return 0.0

    # Air purifier: cheapest desktop HEPA starts at ~€30
    if any(w in q for w in _AIRPUR_W) and price < 25:
        return 0.0

    # Garden tools (hedge trimmer / leaf blower / grass trimmer): cheapest corded ~€15
    if any(w in q for w in _GARDENTOOL_W) and price < 5:
        return 0.0

    # Dehumidifier: cheapest desktop unit ~€30
    if any(w in q for w in _DEHUMID_W) and price < 15:
        return 0.0

    # Massage chair: cheapest entry model ~€100
    if any(w in q for w in _MASSAGE_W) and price < 50:
        return 0.0

    # Lego: cheapest official set ~€8 — filters centai artefacts (800ct → €8 is real, but 80ct → €0.80 is not)
    if any(w in q for w in _LEGO_W) and price < 8:
        return 0.0

    # Electric scooter: cheapest entry models ~€100 — centai prevention
    if any(w in q for w in ["motoroleris", "e-scooter", "elektrinis motoroleris", "elektrinis paspirtukas"]) and price < 50:
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
    # Elesen serves products in static HTML — no JS rendering needed.
    # Use generous timeout because Render servers (US) → elesen.lt (LT) latency ~300-600ms.
    resp = None
    try:
        resp = _http.get(url, headers=get_headers("lt"), timeout=6, allow_redirects=True)
        if resp.status_code != 200:
            resp = None
    except Exception:
        resp = None
    if resp:
        results = _scrape_elesen_from_html(resp.text, query)
        if results:
            print(f"[Elesen] {len(results)} results (direct)")
            return results
    # Fallback: ScraperAPI without JS render (static HTML has products, render_js wastes 5 credits)
    resp = fetch_url(url, "lt", render_js=False, scraper_timeout=8)
    if resp and resp.status_code == 200:
        results = _scrape_elesen_from_html(resp.text, query)
        if results:
            print(f"[Elesen] {len(results)} results (scraper)")
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
    # Fitness weights / equipment
    "hanteliai", "hantelius", "hantelis", "svarsčiai", "svarsciai", "treniruoklis", "treniruoklio",
    # Air fryer (new dict entries from v5.93)
    "gruzdintuvė", "gruzdintuve",
    # Hand mixer / beater
    "plakiklis",
    # Sound system / home cinema
    "garso", "namų", "kino",
    # Water filter
    "vandens",
    # Robot vacuum (standalone "robotinis") and robotic mower (robotinė, feminine form)
    "robotinis", "robotinė", "robotine",
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
    # Oral irrigator / water flosser
    "iryklė", "irykle",
    # Heat recovery ventilation (common LT home appliance)
    "rekuperatorius", "rekuperatoriaus",
    # Steam station (pro iron with detached boiler)
    "stotis",
    # Drone
    "dronas",
    # E-reader
    "e-knygu",
    # Tablet (formal form)
    "planšetinis",
    # Laptop (alternative grammatical form)
    "nešiojamasis",
    # Battery (power tool / standalone battery pack nominative form — genitive "akumuliatoriaus" also common)
    "akumuliatorius", "akumuliatoriaus",
    # Garden tools (common outdoor power tool searches)
    "krūmapjovė", "krumapjove", "lapų pūstuvas", "lapu pustuvas",
    # Flashlight
    "žibintas", "zibintas",
    # Nebulizer / inhaler (health device)
    "nebulizatorius", "nebulizatoriaus",
    # Security camera / video doorbell
    "stebėjimo", "stebejimo", "skambutis",
    # Smart home
    "termoregliatorius", "termoreguliatorius", "kištukas", "kistukas", "jungiklis",
    # Baby / child products
    "vežimėlis", "vezimelis", "kėdutė", "kedute", "lopšelis", "lopselis",
    # Additional kitchen appliances
    "ryžių", "dziov", "džiovintuvas", "dziovintuvas", "arbatinukas", "ryzowar",
    # Power station / power bank
    "galios", "pakrovėjas", "pakrovejas", "stotelė", "stotele",
    # Garden / outdoor tools
    "trimeris",
    # Massage / health
    "masažo",
    # Dehumidifier
    "drėgmės", "dregmes", "surinktuvas",
    # Baby products (kūdikio lovelė = baby crib; kūdikio monitorius triggers via monitorius,
    # but "kūdikio vonelė" etc. need explicit trigger)
    "kūdikio", "kudikio", "lovelė", "lovele",
    # Pistol-type tools (masažo pistoletas, klijų pistoletas, dažų pistoletas)
    "pistoletas", "pistoleto",
    # Range hood (gartraukis = modern LT term; gaubtas is also used)
    "gartraukis", "gartraukio",
    # Hair clipper / beard trimmer
    "kirptuvas", "kirptuvo",
    # Steamer / vaporizer (veido garintuvas = face steamer; drabužių garintuvas = clothes steamer)
    "garintuvas", "garintuvo",
    # Face (veido = face genitive — veido masažuoklis, veido garintuvas, etc.)
    "veido",
    # Desktop computer (stalo kompiuteris)
    "stalo",
    # Mirror (veidrodis = vanity/bathroom mirror; kosmetinis veidrodis = cosmetic mirror)
    "veidrodis", "veidrodžio",
    # Electric blanket (antklodė = blanket; elektrinis antklodė = electric blanket)
    "antklodė", "antklode",
    # Window (langų = window genitive — langų valytuvas = window cleaner)
    "langų", "langu",
    # Body (kūno = body genitive — kūno masažuoklis = body massager)
    "kūno", "kuno",
    # Multifunctional (daugiafunkcinis = multifunctional — common adjective for multicookers)
    "daugiafunkcinis", "daugiafunkcine",
    # Nose (nosies = nose genitive — nosies kirptuvas = nose trimmer)
    "nosies",
    # Brush (šepetys = brush; plaukų šepetys = hair brush)
    "šepetys", "sepetys",
    # Cleaner/cleaning product (valiklis = cleaning product; langų valiklis = window cleaner)
    "valiklis", "valiklio",
    # Ear (ausų = ear genitive — ausų valytuvas = ear cleaner)
    "ausų", "ausu",
    # Generator (electric generator; inverterio generatorius = inverter generator)
    "generatorius", "generatoriaus",
    # Household / domestic adjective
    "buitinis", "buitine",
    # Garden hose / watering (laistymo žarna = garden hose; laistymo sistema = irrigation system)
    "žarna", "zarna", "laistymo",
    # Pump (pompa — bicycle pump, water pump; heat pump covered by šilumos)
    "pompa", "pompos",
    # Bicycle genitive form (dviračių pompa = bike pump; dviratis already in list)
    "dviračių", "dviraciu",
    # Helmet (dviračių šalmas = cycling helmet; motociklo šalmas = motorcycle helmet)
    "šalmas", "salmas",
    # BBQ / skewer context (šašlykų grilis = BBQ grill)
    "šašlykų", "saslyku",
    # Chainsaw (motopjūklas; pjūklas→Säge but motopjūklas is a compound)
    "motopjuklas", "motopjūklas",
    # Floor / ground genitive (grindų šepetys = floor brush; grindų plovykla = floor cleaner)
    "grindų", "grindu",
    # Industrial adjective
    "pramoninis", "pramonine",
    # Music center / stereo system
    "muzikos", "centras",
    # Construction adjective
    "statybinis", "statybine",
    # Shaver head / shower head (always an accessory when used as a query noun)
    "galvutė", "galvute",
    # IPL / light depilator (šviesos depiliatorius = IPL hair removal device)
    "depiliatorius", "depiliatoriaus", "šviesos",
    # Steam (garo = steam genitive, alternative to garų; garo laidynas = steam iron)
    "garo",
    # Tiles (plytelių valytuvas = tile cleaner)
    "plyteliu", "plyteles",
    # Drill
    "gręžtuvas", "grežtuvas", "gręžtuko", "greztuko",
    # Tent
    "palapinė", "palapine", "palapinės", "palapines",
    # Sleeping bag
    "miegmaišis", "miegmaisio",
    # Blood pressure monitor
    "tonometras", "tonometro",
    # Pulse monitor / fitness tracker
    "pulsometras", "pulsometro",
    # Inhaler / nebulizer
    "inhalatorius", "inhaliatoriaus",
    # Welder
    "suvirintuvas", "suvirintuvo",
    # Meat grinder
    "mėsmalė", "mėsmalės", "mesmalė", "mesmale",
    # Sprayer (garden / plant)
    "purkštuvas", "purkštuvo",
    # Alarm system
    "signalizacija", "signalizacijos",
    # High chair (maitinimo kėdutė = feeding high chair)
    "maitinimo",
    # Elliptical trainer prefix (elipsinis treniruoklis)
    "elipsinis", "elipsine",
    # Iron (feminine form)
    "lygintuvė", "lygintuve",
    # Ironing (lyginimo lenta = ironing board)
    "lyginimo",
    # Multimeter
    "multimetras", "multimetro",
    # Camera lens
    "objektyvas", "objektyvo",
    # Tripod
    "trikojis", "trikojo",
    # Graphics card
    "grafikos",
    # CPU
    "procesorius", "procesoriaus",
    # Oral irrigator (burnos dušas = water flosser)
    "burnos",
    # Lawn (žolės pjovimo mašina = lawn mower alternative phrasing)
    "žolės", "zoles",
    # Security genitive (apsaugos kamera = security camera)
    "apsaugos",
    # Internet genitive (interneto maršrutizatorius)
    "interneto",
    # Network genitive (tinklo jungiklis = network switch)
    "tinklo",
    # Electric genitive (elektros pjūklas = electric saw)
    "elektros",
    # Colors (product queries often include color in LT)
    "juodas", "juoda", "juodos",
    "baltas", "balta", "baltos",
    "pilkas", "pilka", "pilkos",
    "sidabrinis", "sidabrine",
    "auksinis", "auksinė", "auksinė",
    "melyna", "mėlyna", "melynas", "mėlynas",
    "zalias", "žalias", "zalia", "žalia",
    "raudonas", "raudona",
    "violetinis", "violetine",
    "rozinis", "rožinis", "rozine", "rožinė",
    # Automotive adjective
    "automobilinis", "automobiline",
    # Radiator / heater
    "radiatorius", "radiatoriaus",
    # GPS navigator
    "navigatorius", "navigatoriaus",
    # Scanner
    "skeneris", "skenerio",
    # Bread maker
    "duoninė", "duonine",
    # Production/making genitive (maisto gamybos mašina = food processor)
    "gamybos",
    # Solarium
    "soliariumo",
    # Wireless adjective
    "bevielis", "bevieles",
    # Light fixture (lubų šviestuvas = ceiling light, sieninis šviestuvas = wall light)
    "šviestuvas", "sviestuvas", "šviestuve", "sviestuve",
    # Floor/yoga mat
    "kilimėlis", "kilimelis",
    # Blender/grinder (trintuvas = food processor type)
    "trintuvas", "trintuvo",
    # Food chopper
    "smulkintuvas", "smulkintuvo",
    # Coffee beans genitive
    "pupelių", "pupeliu",
    # Fast adjective (greitasis įkroviklis = fast charger)
    "greitasis", "greitoji",
    # Controller / remote (žaidimų valdiklis = game controller)
    "valdiklis", "valdiklio",
    # Inkjet adjective
    "rašalinis", "rasalinis",
    # Laser adjective
    "lazerinis", "lazerine",
    # Glucose meter
    "gliukometras", "gliukometro",
    # Massage mat
    "masažinis", "masazinis",
    # Measurement device (matuoklis = meter/gauge)
    "matuoklis", "matuoklio",
    # Goggles / glasses
    "akiniai", "akiniu",
    # Face mask / medical mask
    "kaukė", "kauke",
    # Skiing genitive
    "slidinėjimo", "slidinejimo",
    # Filter
    "filtras", "filtro",
    # Moka pot / coffee pot
    "kavinukas", "kavinuko",
    # Baking (kepimo skarda = baking tray)
    "kepimo",
    # Solar
    "saulės", "saules",
    # RAM (operatyvinė atmintis)
    "operatyvinė", "operatyvine",
    # Stainless steel (nerūdijantis)
    "nerūdijantis", "nerudijantis",
    # Smart (short adjective form without -is)
    "ismanus",
    # PC case / computer case
    "kompiuterio",
    # Blood pressure genitive
    "kraujospūdžio", "kraujospudzio",
    # Chair (kėdė = chair; ofiso kėdė = office chair)
    "kėdė", "kedes", "kede",
    # Scooter / moped
    "motoroleris", "motorolerio",
    # Dispenser
    "dozatorius", "dozatoriaus",
    # Detector (dūmų detektorius = smoke detector)
    "detektorius", "detektoriaus",
    # Memory card (atminties kortelė)
    "kortelė", "korteles",
    # Watering can
    "laistyklė", "laistyklės",
    # Garden (sodo = garden genitive)
    "sodo",
    # Band adjective (juostinis pjūklas = band saw)
    "juostinis", "juostine",
    # Contact adjective (kontaktinis grilis = contact grill)
    "kontaktinis", "kontaktine",
    # Wind genitive
    "vėjo", "vejo",
    # Air (oro siurblys = air pump)
    "oro",
    # Diffuser / air freshener
    "išpurškiklis", "ispurskiklis",
    # Standing desk
    "stovintis", "stovinti",
    # Office genitive
    "ofiso",
    # Portable adjective
    "portativinis", "portativine",
    # Big/large adjective
    "didelis", "didele",
    # Compact adjective
    "kompaktiškas", "kompaktiska", "kompaktiskas",
    # Maker/producer (ledų gamintuvas = ice maker, jogurto = yogurt maker)
    "gamintuvas", "gamintuvo",
    # Thermos / flask
    "termosas", "termoso",
    # Pasta machine
    "makaronų", "makaronu",
    # Paper
    "popierius", "popieriaus",
    # Petrol/gasoline adjective
    "benzininis", "benzinine",
    # Baby monitor (monitoriaus = genitive of monitor)
    "monitoriaus",
    # Video projector
    "videoprojektorius", "videoprojekcija",
    # Multi-channel
    "daugiakanalis", "daugiakanalio",
    # Ice scraper
    "grandiklis", "grandiklio",
    # Mechanical adjective
    "mechaniška", "mechaniskas", "mechaniškas",
    # Interactive screen
    "interaktyvus", "interaktyvi",
    # Lunch box / food container
    "dėžutė", "dezute",
    # Pizza stone
    "picos",
    # Freezer / ice genitive
    "ledų", "ledu",
    # Yogurt / dairy genitive
    "jogurto",
    # Cheese genitive
    "sūrio", "surio",
    # Screwdriver / drill (atsuktuvas = screwdriver)
    "atsuktuvas", "atsuktuvo",
    # Car genitive (automobilio = car genitive)
    "automobilio",
    # Suitcase
    "lagaminas", "lagamino",
    # Small/little adjective
    "mažas", "maza",
    # Titanium (premium phone material)
    "titanas", "titanio",
    # Battery (akumuliatorius) all cases used in LT tool searches
    "akumuliatoriumi", "akumuliatoriaus",
    # Absolute adjective (Dyson Absolute series)
    "absoliutus", "absoliutine",
    # High pressure (aukšto slėgio = high pressure genitive)
    "slėgio", "slegio",
    # Protein / supplement
    "baltymų", "baltymu",
    # Christmas tree
    "kalėdinė", "kaledine", "eglutė", "eglutes",
    # Pet supplies
    "šunų", "sunu", "kačių", "kaciu",
    # Hydraulic jack
    "domkratas", "domkrato",
    # E-book reader
    "elektroninė", "elektronine",
    # Door lock
    "durų", "duru",
    # Protein supplement
    "kolagenas", "kolageno",
    # v7.43 — Music instruments
    "gitara", "gitaros",
    "pianinas", "pianino",
    "sintezatorius", "sintezatoriaus",
    "bugnas", "bugnu",
    "smuikas", "smiko",
    "fleita", "fleitos",
    # Sports / outdoor
    "batutas", "batuto",
    "slidu",
    "paciuzos", "paciuzu",
    "meskere", "meskeriu",
    "zvejybos", "zvejyba",
    "plaukimo",
    # Milk frother
    "pienuke", "pienuku",
    # Furniture / home textiles
    "lova", "lovos",
    "spinta", "spintos",
    "kilimas", "kilimo",
    # Dashcam
    "registratorius", "registratoriaus",
    # v7.45 — Books
    "knyga", "knygos", "knygu",
    # Clothing
    "striuke", "striuku",
    "megztinis", "megztinio",
    "pirstines", "pirstiniu",
    "suknele", "sukneles",
    "kostiumas", "kostiumo",
    # Waffle maker
    "vafline", "vafliu",
    # Outdoor swing / garden
    "supuokles", "supuokliu",
    "pavesine", "pavesines",
    # Furniture
    "baldai", "baldu",
    # Toy construction set
    "konstruktorius", "konstruktoriaus",
    # Toy car
    "masinyke", "masiniu",
    # v7.46 — Perfume / fragrance
    "kvepalai", "kvepalu",
    "parfumas", "parfumo",
    "sampunas", "sampuno",
    # Sports (tennis, badminton, football, basketball, snow/skate)
    "tenisas", "teniso",
    "badmintonas", "badmintono",
    "futbolas", "futbolo",
    "krepsis", "krepsinio",
    "snieglente", "snieglenciu",
    "riedlente", "riedlenciu",
    # Home textiles / bedroom
    "pagalve", "pagalviu",
    "patalyne", "patalynes",
    # Candle
    "zvake", "zvakiu",
    # Photo frame
    "ramelis", "ramelio",
    # Thermos mug / travel cup
    "termopuodelis", "termopuodelio",
    # v7.44 — Vitamins / supplements
    "vitaminas", "vitaminu", "vitaminai",
    "magnio", "magnis",
    "kreatinas", "kreatino",
    # Shoes / footwear
    "batai", "batu",
    "kedai", "kedai",
    "sportbaciai", "sportbacio",
    # Doll
    "lele", "leles",
    # Kitchen knife / scissors
    "peilis", "peilio", "peiliai",
    "zirkles", "zirkliu",
    # Food slicer
    "pjaustytuvas", "pjaustytuvo",
    # Car tyres
    "padangos", "padanga",
    # Engine oil / lubricant
    "tepalas", "tepalo",
    # Tape measure
    "matavimo",
    # v7.47 — Furniture
    "sofa", "sofos",
    "fotelis", "fotelio",
    "lentyna", "lentynu",
    "komoda", "komodu",
    # v7.47 — Clothing
    "kepurė", "kepures",
    "šalikas", "saliko",
    "kelnės", "kelniu",
    "marškiniai", "marskiniu",
    "džinsai", "dzinsu",
    "maudymosi",
    "kostiumelis", "kostiumelio",
    # v7.47 — Sports
    "boksas", "bokso",
    "riedutis", "rieduciu",
    "rogės", "rogiu",
    # v7.47 — Daily products
    "gertuvė", "gertuviu",
    "sauskelnės", "sauskelnems",
    "jogos",
    # v7.48 — Bags / accessories / jewelry
    "kuprinė", "kuprines",
    "rankinė", "rankines",
    "piniginė", "pinigines",
    "dirzas", "dirzo",
    "papuošalai", "papuosalu",
    "karoliai", "karoliu",
    "auskarai", "auskariu",
    "ziedas", "ziedo",
    # v7.48 — Kitchen / home
    "puodelis", "puodelio",
    "dubuo", "dubens",
    "vazonas", "vazono",
    # v7.48 — Miscellaneous
    "tentas", "tento",
    "siuvimo",
    "zaislinis", "zaislinio",
    "portfelis", "portfelio",
    # v7.49 — Beauty / bathroom
    "kremas", "kremo",
    "dezodorantas", "dezodoranto",
    "losjonas", "losjono",
    "vonia", "vonios",
    "rankslostis", "ranklosciu",
    # v7.49 — Pet supplies (singular forms; plural "šunų"/"kačių" already covered)
    "katinas", "katino",
    "augintinis", "augintinio",
    # v7.49 — Hunting / protection sports
    "medziokle", "medziokles",
    "sliauztukai", "sliauztukas",
    # v7.52 — Electrical / triggers
    "tinklinė", "tinklinis",
    # v7.53 — Trigger gaps (dict entries not reachable without these)
    "valdymo",    # nuotolinio valdymo pultas = remote control
    "peiliu",     # peiliu blokas = knife block (peiliai was trigger, not peiliu gen.pl.)
    "pienu",      # pienu putuke = milk frother (compound trigger)
    "piestuko",   # pencil genitive
    "svarstis",   # single weight disc (nominative)
    "svarsti",    # weight (short/genitive form used in queries)
    # v7.52 — Hammock
    "hamakas", "hamaku",
    # v7.52 — Earbud singular
    "ausinukas", "ausinuko",
    # v7.52 — Fitness
    "menteliklis", "menteliklio",
    "štanga", "stangos",
    "suoliukas", "suoliuko",
    # v7.52 — SUP board
    "irklentė", "irklentes",
    # v7.52 — Camping
    "stovyklavimo",
    # v7.52 — Amino acids
    "aminorugsciai", "aminoru",
    # v7.51 — Window treatments
    "uzdanga", "uzdangu",
    "uzuolaida", "uzuolaidų",
    "rolete", "roletu",
    "zaluzija", "zaluziju",
    # v7.51 — Bedding addition
    "paklode", "paklodziu",
    "apklotas", "apklotu",
    # v7.51 — Water sports
    "baseinas", "baseino",
    "baidarele", "baidareles",
    "kanoja", "kanojos",
    "irklai", "irklu",
    # v7.51 — Cables / electrical
    "kabelis", "kabelio",
    "laidas", "laido",
    "tinklines", "tinkliniu",
    # v7.51 — Arts / crafts
    "plastilinas", "plastilino",
    # v7.51 — Flooring / construction
    "grindys", "grindylentu",
    "plytelis", "plyteliu",
    # v7.50 — Automotive accessories
    "automagnetola", "automagnetolos",
    "vairas", "vairo",
    "ratai", "ratu",
    # v7.50 — Home improvement / flooring
    "dazai", "dazo",
    "tapetai", "tapetu",
    "laminatas", "laminato",
    "parketas", "parketo",
    # v7.50 — Music instruments
    "akordeonas", "akordeono",
    "trimitas", "trimito",
    "saksofonas", "saksofono",
    # v7.50 — Office / school
    "pieštukas", "piestukas",
    "flomasteris", "flomasteri",
    # v7.50 — Garden
    "fontanas", "fontano",
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
    ("treniruoklis", "Trainingsgerät"), ("treniruoklio", "Trainingsgerät"),
    ("hanteliai", "Hanteln"), ("hantelius", "Hanteln"), ("hantelis", "Hantel"),
    ("svarsčiai", "Gewichte"), ("svarsciai", "Gewichte"), ("svarsti", "Gewicht"),
    ("kettlebell", "Kettlebell"),
    # Multimedia
    ("grotuvas", "Player"), ("mp3 grotuvas", "MP3-Player"),
    # Accessories
    ("įkroviklis", "Ladegerät"), ("projektorius", "Projektor"),
    # Robot vacuum (must come before plain "siurblys")
    ("robotinis dulkių siurblys", "Saugroboter"), ("robotinis siurblys", "Saugroboter"),
    ("robotinė vejapjovė", "Mähroboter"), ("robotine vejapjove", "Mähroboter"),
    ("robotinis", "Roboter"), ("robotinė", "Roboter"), ("robotine", "Roboter"),
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
    # Pressure washer (must come before generic grindų plovykla below)
    ("aukštojo slėgio plovykla", "Hochdruckreiniger"), ("slėginė plovykla", "Hochdruckreiniger"),
    ("slegine plovykla", "Hochdruckreiniger"),
    # Floor cleaner / wet floor mop (longer than "plovykla" so matches first)
    ("grindų plovykla", "Bodenreiniger"), ("grindu plovykla", "Bodenreiniger"),
    ("plovykla", "Hochdruckreiniger"),
    # Lawn mower (vejapjovė = variant spelling of žoliapjovė, not yet in dict)
    ("vejapjovė", "Rasenmäher"), ("vejapjove", "Rasenmäher"),
    # Hedge trimmer
    ("krūmapjovė", "Heckenschere"), ("krumapjove", "Heckenschere"),
    # Grass trimmer / strimmer
    ("žolės trimeris", "Rasentrimmer"), ("zoles trimeris", "Rasentrimmer"),
    ("trimeris", "Rasentrimmer"),
    # Leaf blower
    ("lapų pūstuvas", "Laubbläser"), ("lapu pustuvas", "Laubbläser"),
    # Flashlight / torch
    ("žibintas", "Taschenlampe"), ("zibintas", "Taschenlampe"),
    # Nebulizer / inhaler
    ("nebulizatorius", "Inhalator"), ("nebulizatoriaus", "Inhalator"),
    # Massage chair / massage gun
    ("masažo kėdė", "Massagesessel"), ("masazo kede", "Massagesessel"),
    ("masažo kede", "Massagesessel"),
    ("masažo pistoletas", "Massagepistole"), ("masazo pistoletas", "Massagepistole"),
    ("masažo", "Massage"),
    # Pistol-type tools
    ("klijų pistoletas", "Heißklebepistole"), ("kliju pistoletas", "Heißklebepistole"),
    ("dažų pistoletas", "Lackierpistole"), ("dazu pistoletas", "Lackierpistole"),
    # Baby crib standalone "lovelė" (kūdikio lovelė already in dict above; this catches bare "lovelė")
    ("lovelė", "Babybett"), ("lovele", "Babybett"),
    # Baby genitive standalone fallback (catches "kūdikio vonelė" etc.)
    ("kūdikio", "Baby"), ("kudikio", "Baby"),
    # Dehumidifier
    ("drėgmės surinktuvas", "Luftentfeuchter"), ("dregmes surinktuvas", "Luftentfeuchter"),
    ("surinktuvas drėgmei", "Luftentfeuchter"), ("surinktuvas dregmei", "Luftentfeuchter"),
    # Air compressor
    ("kompresorius", "Kompressor"), ("kompresoriaus", "Kompressor"),
    # Snow blower (common in LT winters)
    ("sniego valytuvas", "Schneefräse"), ("sniego frezas", "Schneefräse"),
    ("sniego freza", "Schneefräse"),
    # Heat pump (šilumos siurblys must come before standalone siurblys→Staubsauger)
    ("šilumos siurblys", "Wärmepumpe"), ("silumos siurblys", "Wärmepumpe"),
    ("šilumos pompa", "Wärmepumpe"), ("silumos pompa", "Wärmepumpe"),
    # Heat pump system type (oras vanduo = air-to-water; oras oras = air-to-air)
    ("oras vanduo", "Luft-Wasser"), ("oras oras", "Luft-Luft"),
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
    # Oral irrigator / water flosser
    ("dantų iryklė", "Munddusche"), ("dantų irykle", "Munddusche"),
    ("iryklė", "Munddusche"), ("irykle", "Munddusche"),
    # Additional kitchen appliances
    ("ryžių viryklė", "Reiskocher"), ("ryziu virykle", "Reiskocher"),
    ("maisto džiovintuvas", "Dörrgerät"), ("maisto dziovintuvas", "Dörrgerät"),
    ("džiovintuvas maistui", "Dörrgerät"), ("dziovintuvas maistui", "Dörrgerät"),
    ("arbatinukas", "Teekanne"),
    # Power station / power bank
    ("galios stotelė", "Powerstation"), ("galios stotele", "Powerstation"),
    ("galios bankas", "Powerbank"), ("galios banka", "Powerbank"),
    ("galios", "Power"),
    ("belaidis pakrovėjas", "Kabelloses Ladegerät"), ("belaidis pakrovejas", "Kabelloses Ladegerät"),
    ("pakrovėjas", "Ladegerät"), ("pakrovejas", "Ladegerät"),
    # Steam station (professional iron with separate boiler)
    ("garų stotis", "Dampfstation"), ("garu stotis", "Dampfstation"),
    # Heat recovery ventilation (rekuperatorius)
    ("rekuperatorius", "Lüftungsanlage"), ("rekuperatoriaus", "Lüftungsanlage"),
    # Surveillance camera / video doorbell
    ("stebėjimo kamera", "Überwachungskamera"), ("stebejimo kamera", "Überwachungskamera"),
    ("vaizdo durų skambutis", "Video-Türklingel"), ("vaizdo duru skambutis", "Video-Türklingel"),
    ("durų skambutis", "Türklingel"), ("duru skambutis", "Türklingel"),
    # Smart home devices
    ("išmanusis termoregliatorius", "Smart Thermostat"), ("ismanysis termoregliatorius", "Smart Thermostat"),
    ("termoregliatorius", "Thermostat"), ("termoreguliatorius", "Thermostat"),
    ("išmanusis kištukas", "Smarte Steckdose"), ("ismanysis kistukas", "Smarte Steckdose"),
    ("kištukas", "Steckdose"), ("kistukas", "Steckdose"),
    ("išmanusis jungiklis", "Smart Schalter"), ("ismanysis jungiklis", "Smart Schalter"),
    ("jungiklis", "Schalter"),
    # Doorbell standalone (durų skambutis already in dict; this catches bare "skambutis")
    ("skambutis", "Türklingel"),
    # Surveillance standalone (stebėjimo kamera already in dict; catches bare "stebėjimo")
    ("stebėjimo", "Überwachung"), ("stebejimo", "Überwachung"),
    # Baby / child products
    ("kūdikio monitorius", "Babyphone"), ("kudikio monitorius", "Babyphone"),
    ("automobilinė vaikiška kėdutė", "Kindersitz"), ("automobiline vaiskia kedute", "Kindersitz"),
    ("vaikiška kėdutė", "Kindersitz"), ("vaiska kedute", "Kindersitz"),
    ("kėdutė", "Kindersitz"), ("kedute", "Kindersitz"),
    ("vaikiškas vežimėlis", "Kinderwagen"), ("vaikiskas vezimelis", "Kinderwagen"),
    ("vežimėlis", "Kinderwagen"), ("vezimelis", "Kinderwagen"),
    ("kūdikio lovelė", "Babybett"), ("kudikio lovele", "Babybett"),
    ("lopšelis", "Babybett"), ("lopselis", "Babybett"),
    # Drone (common purchase; DJI = most popular brand)
    ("dronas su kamera", "Drohne mit Kamera"), ("dronas", "Drohne"),
    # E-reader
    ("e-knygu skaitvtuvas", "E-Reader"), ("e-knygu", "E-Reader"),
    # Tablet computer (formal LT form)
    ("planšetinis kompiuteris", "Tablet"), ("planšetinis", "Tablet"),
    # Laptop (alternative grammatical form nešiojamasis vs nešiojamas)
    ("nešiojamasis kompiuteris", "Laptop"), ("nešiojamasis", "Laptop"),
    # Battery / accumulator (power tool batteries sold as standalone products)
    ("akumuliatorius", "Akku"), ("akumuliatoriaus", "Akku"),
    # Range hood (gartraukis = modern LT; gaubtas already in dict above)
    ("gartraukis", "Dunstabzugshaube"), ("gartraukio", "Dunstabzugshaube"),
    # Hair clipper / beard trimmer
    ("plaukų kirptuvas", "Haarschneidemaschine"), ("plaukų kirptuvo", "Haarschneidemaschine"),
    ("barzdos kirptuvas", "Bartschneider"), ("barzdos kirptuvo", "Bartschneider"),
    ("kirptuvas", "Haarschneider"), ("kirptuvo", "Haarschneider"),
    # Charging station standalone (galios stotelė→Powerstation is longer and matches first)
    ("stotelė", "Ladestation"), ("stotele", "Ladestation"),
    # Generic pistol/gun-type tool (multi-word phrases above match first when prefix present)
    ("pistoletas", "Pistole"), ("pistoleto", "Pistole"),
    # Desktop computer (stalo kompiuteris → Desktop Computer; standalone "stalo" = table/desktop)
    ("stalo kompiuteris", "Desktop Computer"), ("stalo kompiuterio", "Desktop Computer"),
    ("stalo", "Desktop"),
    # Clothes steamer / face steamer / food steamer
    ("drabužių garintuvas", "Dampfbürste für Kleidung"), ("drabuziu garintuvas", "Dampfbürste für Kleidung"),
    ("veido garintuvas", "Gesichtsdampfgerät"), ("veido garintuvo", "Gesichtsdampfgerät"),
    ("garų šluota", "Dampfbesen"), ("garu slota", "Dampfbesen"),
    ("garintuvas", "Dampfgarer"), ("garintuvo", "Dampfgarer"),
    # Face (genitive — veido masažuoklis, veido garintuvas, etc.)
    ("veido", "Gesicht"),
    # Vanity / bathroom mirror
    ("kosmetinis veidrodis", "Kosmetikspiegel"), ("kosmetinis veidrodžio", "Kosmetikspiegel"),
    ("veidrodis", "Spiegel"), ("veidrodžio", "Spiegel"),
    # Electric blanket
    ("elektrinis antklodė", "Heizdecke"), ("elektrinis antklode", "Heizdecke"),
    ("antklodė", "Decke"), ("antklode", "Decke"),
    # Window cleaner (langų valytuvas)
    ("langų valytuvas", "Fensterreiniger"), ("langu valytuvas", "Fensterreiniger"),
    ("langų", "Fenster"), ("langu", "Fenster"),
    # Body (kūno masažuoklis, kūno losjenas, etc.)
    ("kūno masažuoklis", "Körpermassagegerät"), ("kuno masazuoklis", "Körpermassagegerät"),
    ("kūno", "Körper"), ("kuno", "Körper"),
    # Multifunctional adjective
    ("daugiafunkcinis puodas", "Multikocher"), ("daugiafunkcinis", "Multifunktions"),
    ("daugiafunkcine", "Multifunktions"),
    # Nose trimmer
    ("nosies kirptuvas", "Nasenhaartrimmer"), ("nosies kirptuvo", "Nasenhaartrimmer"),
    ("nosies", "Nasen"),
    # Brush (plaukų šepetys = hair brush; šepetys alone = brush)
    ("plaukų šepetys", "Haarbürste"), ("plauku sepetys", "Haarbürste"),
    ("šepetys", "Bürste"), ("sepetys", "Bürste"),
    # Cleaning product (langų valiklis = window cleaner; valiklis alone = cleaning agent)
    ("langų valiklis", "Fensterreiniger"), ("langu valiklis", "Fensterreiniger"),
    ("valiklis", "Reiniger"), ("valiklio", "Reiniger"),
    # Ear cleaner
    ("ausų valytuvas", "Ohrreiniger"), ("ausu valytuvas", "Ohrreiniger"),
    ("ausų", "Ohr"), ("ausu", "Ohr"),
    # Generator
    ("inverterinis generatorius", "Inverter Generator"), ("inverterinis generatoriaus", "Inverter Generator"),
    ("generatorius", "Generator"), ("generatoriaus", "Generator"),
    # Household / domestic adjective
    ("buitinis prietaisas", "Haushaltsgerät"), ("buitine prietaise", "Haushaltsgerät"),
    ("buitinis", "Haushalt"), ("buitine", "Haushalt"),
    # Garden hose / watering / irrigation
    ("laistymo žarna", "Gartenschlauch"), ("laistymo zarna", "Gartenschlauch"),
    ("laistymo sistema", "Bewässerungssystem"), ("laistymo sistema", "Bewässerungssystem"),
    ("žarna", "Schlauch"), ("zarna", "Schlauch"),
    ("laistymo", "Bewässerungs"),
    # Pump (longer phrases match first — heat pump already handled by šilumos pompa)
    ("dviračių pompa", "Fahrradpumpe"), ("dviraciu pompa", "Fahrradpumpe"),
    ("vandens pompa", "Wasserpumpe"), ("vandens pompos", "Wasserpumpe"),
    ("pompa", "Pumpe"), ("pompos", "Pumpe"),
    # Bicycle genitive
    ("dviračių šalmas", "Fahrradhelm"), ("dviraciu salmas", "Fahrradhelm"),
    ("dviračių", "Fahrrad"), ("dviraciu", "Fahrrad"),
    # Helmet
    ("motociklo šalmas", "Motorradhelm"), ("motociklo salmas", "Motorradhelm"),
    ("šalmas", "Helm"), ("salmas", "Helm"),
    # BBQ / kebab context (šašlykų grilis = BBQ grill; use "BBQ" to avoid doubling with grilis→Grill)
    ("šašlykų", "BBQ"), ("saslyku", "BBQ"),
    # Chainsaw (motopjūklas = chainsaw; "pjūklas"→Säge exists but doesn't match compound)
    ("motopjūklas", "Motorsäge"), ("motopjuklas", "Motorsäge"),
    # Floor / ground (grindų = floor genitive; longer grindų plovykla handled above)
    ("grindų", "Boden"), ("grindu", "Boden"),
    # Industrial adjective
    ("pramoninis", "Industrie"), ("pramonine", "Industrie"),
    # Music center / stereo system
    ("muzikos centras", "Musikanlage"), ("muzikos", "Musik"),
    ("centras", "Zentrum"),
    # Construction adjective + construction dryer (must come before džiovintuvas→Haartrockner)
    ("statybinis džiovintuvas", "Bautrockner"), ("statybine dziovintuvas", "Bautrockner"),
    ("statybinis", "Bau"), ("statybine", "Bau"),
    # IPL / light hair removal device
    ("šviesos depiliatorius", "IPL-Gerät"), ("sviesos depiliatorius", "IPL-Gerät"),
    ("depiliatorius", "Haarentfernungsgerät"), ("depiliatoriaus", "Haarentfernungsgerät"),
    ("šviesos", "Licht"), ("sviesos", "Licht"),
    # Steam (garo = genitive of garas; garų already in dict; garo laidynas = steam iron)
    ("garo laidynas", "Dampfbügeleisen"), ("garo lygintuvas", "Dampfbügeleisen"),
    ("garo", "Dampf"),
    # Tiles (plytelių valytuvas = tile cleaner)
    ("plyteliu valytuvas", "Fliesenreiniger"), ("plyteles valytuvas", "Fliesenreiniger"),
    ("plyteliu", "Fliesen"), ("plyteles", "Fliesen"),
    # Drill
    ("gręžtuvas", "Bohrmaschine"), ("grežtuvas", "Bohrmaschine"),
    ("gręžtuko", "Bohrmaschine"), ("greztuko", "Bohrmaschine"),
    # Tent
    ("palapinė", "Zelt"), ("palapine", "Zelt"),
    ("palapinės", "Zelt"), ("palapines", "Zelt"),
    # Sleeping bag
    ("miegmaišis", "Schlafsack"), ("miegmaisio", "Schlafsack"),
    # Blood pressure monitor
    ("tonometras", "Blutdruckmessgerät"), ("tonometro", "Blutdruckmessgerät"),
    # Pulse / heart rate monitor
    ("pulsometras", "Pulsmesser"), ("pulsometro", "Pulsmesser"),
    # Inhaler / nebulizer
    ("inhalatorius", "Inhalationsgerät"), ("inhaliatoriaus", "Inhalationsgerät"),
    # Welder
    ("suvirintuvas", "Schweißgerät"), ("suvirintuvo", "Schweißgerät"),
    # Meat grinder
    ("mėsmalė", "Fleischwolf"), ("mėsmalės", "Fleischwolf"),
    ("mesmalė", "Fleischwolf"), ("mesmale", "Fleischwolf"),
    # Garden/plant sprayer
    ("augalų purkštuvas", "Gartenspritze"), ("purkštuvas", "Sprühgerät"),
    ("purkštuvo", "Sprühgerät"),
    # Alarm system
    ("signalizacija", "Alarmanlage"), ("signalizacijos", "Alarmanlage"),
    # High chair (feeding chair)
    ("maitinimo kėdutė", "Hochstuhl"), ("maitinimo kedute", "Hochstuhl"),
    ("maitinimo", "Fütterprogramm"),
    # Elliptical trainer
    ("elipsinis treniruoklis", "Ellipsentrainer"), ("elipsinis treniruoklio", "Ellipsentrainer"),
    ("elipsinis", "Elliptisch"), ("elipsine", "Elliptisch"),
    # Iron (feminine form / alternative ending)
    ("lygintuvė", "Bügeleisen"), ("lygintuve", "Bügeleisen"),
    # Ironing board
    ("lyginimo lenta", "Bügelbrett"), ("lyginimo", "Bügel"),
    # Multimeter
    ("multimetras", "Multimeter"), ("multimetro", "Multimeter"),
    # Camera lens
    ("fotoaparato objektyvas", "Kameraobjektiv"), ("objektyvas", "Objektiv"),
    ("objektyvo", "Objektiv"),
    # Tripod
    ("trikojis", "Stativ"), ("trikojo", "Stativ"),
    # Graphics card
    ("grafikos plokštė", "Grafikkarte"), ("grafikos kortele", "Grafikkarte"),
    ("grafikos", "Grafik"),
    # CPU
    ("procesorius", "Prozessor"), ("procesoriaus", "Prozessor"),
    # Oral irrigator / water flosser
    ("burnos dušas", "Munddusche"), ("burnos", "Mund"),
    # Lawn / grass (žolės pjovimo mašina = lawn mower)
    ("žolės pjovimo mašina", "Rasenmäher"), ("zoles pjovimo masina", "Rasenmäher"),
    ("žolės", "Rasen"), ("zoles", "Rasen"),
    # Security camera
    ("apsaugos kamera", "Sicherheitskamera"), ("apsaugos", "Sicherheits"),
    # Internet router
    ("interneto maršrutizatorius", "Internet-Router"), ("interneto marsrutizatorius", "Internet-Router"),
    ("interneto", "Internet"),
    # Network switch
    ("tinklo jungiklis", "Netzwerk-Switch"), ("tinklo", "Netzwerk"),
    # Electric genitive (elektros pjūklas = electric saw)
    ("elektros pjūklas", "Elektrosäge"), ("elektros pjuklas", "Elektrosäge"),
    ("elektros", "Elektro"),
    # Colors
    ("juodas", "Schwarz"), ("juoda", "Schwarz"), ("juodos", "Schwarz"),
    ("baltas", "Weiß"), ("balta", "Weiß"), ("baltos", "Weiß"),
    ("pilkas", "Grau"), ("pilka", "Grau"), ("pilkos", "Grau"),
    ("sidabrinis", "Silber"), ("sidabrine", "Silber"),
    ("auksinis", "Gold"), ("auksinė", "Gold"), ("auksinė", "Gold"),
    ("mėlynas", "Blau"), ("melyna", "Blau"), ("mėlyna", "Blau"), ("melynas", "Blau"),
    ("žalias", "Grün"), ("zalias", "Grün"), ("žalia", "Grün"), ("zalia", "Grün"),
    ("raudonas", "Rot"), ("raudona", "Rot"),
    ("violetinis", "Violett"), ("violetine", "Violett"),
    ("rožinis", "Rosa"), ("rozinis", "Rosa"), ("rožinė", "Rosa"), ("rozine", "Rosa"),
    # Automotive adjective
    ("automobilinis siurblys", "Auto-Staubsauger"), ("automobilinis", "Auto"),
    ("automobiline", "Auto"),
    # Radiator / panel heater
    ("elektrinis radiatorius", "Elektroheizkörper"), ("radiatorius", "Heizkörper"),
    ("radiatoriaus", "Heizkörper"),
    # GPS navigator
    ("navigatorius", "Navigationsgerät"), ("navigatoriaus", "Navigationsgerät"),
    # Scanner
    ("skeneris", "Scanner"), ("skenerio", "Scanner"),
    # Bread maker
    ("duoninė", "Brotbackautomat"), ("duonine", "Brotbackautomat"),
    # Food production/making genitive
    ("maisto gamybos mašina", "Küchenmaschine"), ("gamybos masina", "Küchenmaschine"),
    ("gamybos", "Zubereitung"),
    # Solarium / tanning lamp
    ("soliariumo lempa", "Solarium-Lampe"), ("soliariumo", "Solarium"),
    # Wireless adjective
    ("bevielis", "kabellos"), ("bevieles", "kabellos"),
    # Light fixtures (multi-word BEFORE standalone "stalo"/"grindų" to override those)
    ("lubų šviestuvas", "Deckenleuchte"), ("lubu sviestuvas", "Deckenleuchte"),
    ("sieninis šviestuvas", "Wandleuchte"), ("sieninis sviestuvas", "Wandleuchte"),
    ("stalo lempa", "Tischlampe"), ("stalo sviestuvas", "Tischleuchte"),
    ("grindų lempa", "Stehlampe"), ("grindu lempa", "Stehlampe"),
    ("šviestuvas", "Leuchte"), ("sviestuvas", "Leuchte"),
    # Floor/yoga mat
    ("masažinis kilimėlis", "Massagematte"), ("masazinis kilimelis", "Massagematte"),
    ("jogos kilimėlis", "Yogamatte"), ("jogos kilimelis", "Yogamatte"),
    ("kilimėlis", "Matte"), ("kilimelis", "Matte"),
    # Food chopper / blender type
    ("maisto smulkintuvas", "Zerkleinerer"), ("trintuvas", "Zerkleinerer"),
    ("smulkintuvas", "Zerkleinerer"), ("trintuvo", "Zerkleinerer"), ("smulkintuvo", "Zerkleinerer"),
    # Coffee beans
    ("kavos pupelių", "Kaffeebohnen"), ("kavos pupeliu", "Kaffeebohnen"),
    ("pupelių", "Bohnen"), ("pupeliu", "Bohnen"),
    # Fast charger
    ("greitasis įkroviklis", "Schnellladegerät"), ("greitasis ikroviklis", "Schnellladegerät"),
    ("greitoji įkrova", "Schnellladung"),
    ("greitasis", "Schnell"), ("greitoji", "Schnell"),
    # Game controller
    ("žaidimų valdiklis", "Gamecontroller"), ("zaidimu valdiklis", "Gamecontroller"),
    ("nuotolinio valdymo pultas", "Fernbedienung"),
    ("valdiklis", "Controller"), ("valdiklio", "Controller"),
    # Inkjet printer
    ("rašalinis spausdintuvas", "Tintenstrahldrucker"), ("rasalinis spausdintuvas", "Tintenstrahldrucker"),
    ("rašalinis", "Tintenstrahl"), ("rasalinis", "Tintenstrahl"),
    # Laser printer
    ("lazerinis spausdintuvas", "Laserdrucker"), ("lazerine spausdintuvas", "Laserdrucker"),
    ("lazerinis", "Laser"), ("lazerine", "Laser"),
    # Glucose meter
    ("gliukometras", "Blutzuckermessgerät"), ("gliukometro", "Blutzuckermessgerät"),
    # Massage mat
    ("masažinis", "Massage"), ("masazinis", "Massage"),
    # Blood pressure monitor (full phrase first)
    ("kraujospūdžio matuoklis", "Blutdruckmessgerät"), ("kraujospudzio matuoklis", "Blutdruckmessgerät"),
    ("kraujo spaudimo matuoklis", "Blutdruckmessgerät"), ("kraujo spaudimo", "Blutdruck"),
    ("kraujospūdžio", "Blutdruck"), ("kraujospudzio", "Blutdruck"),
    # Measurement device
    ("matuoklis", "Messgerät"), ("matuoklio", "Messgerät"),
    # Goggles / glasses / sunglasses
    ("slidinėjimo akiniai", "Skibrille"), ("slidinejimo akiniai", "Skibrille"),
    ("dviračių akiniai", "Fahrradbrille"), ("dviraciu akiniai", "Fahrradbrille"),
    ("saulės akiniai", "Sonnenbrille"), ("saules akiniai", "Sonnenbrille"),
    ("akiniai", "Brille"), ("akiniu", "Brille"),
    # Skiing
    ("slidinėjimo šalmas", "Skihelm"), ("slidinejimo salmas", "Skihelm"),
    ("slidinėjimo", "Ski"), ("slidinejimo", "Ski"),
    # Face mask
    ("veido kaukė", "Gesichtsmaske"), ("veido kauke", "Gesichtsmaske"),
    ("akių kaukė", "Augenmaske"), ("akiu kauke", "Augenmaske"),
    ("kaukė", "Maske"), ("kauke", "Maske"),
    # Filter
    ("kavos filtras", "Kaffeefilter"), ("kavos filtro", "Kaffeefilter"),
    ("filtras", "Filter"), ("filtro", "Filter"),
    # Coffee pot / moka pot
    ("kavinukas", "Mokakanne"), ("kavinuko", "Mokakanne"),
    # Baking tray (kepimo skarda)
    ("kepimo skarda", "Backblech"), ("kepimo skardos", "Backblech"),
    ("kepimo forma", "Backform"), ("kepimo", "Back"),
    # Solar
    ("saulės kolektorius", "Solarkollektor"), ("saules kolektorius", "Solarkollektor"),
    ("saulės baterija", "Solarbatterie"), ("saules baterija", "Solarbatterie"),
    ("saulės baterijų", "Solarbatterie"), ("saules bateriju", "Solarbatterie"),
    ("saulės energija", "Solarenergie"), ("saulės", "Solar"), ("saules", "Solar"),
    # RAM
    ("operatyvinė atmintis", "Arbeitsspeicher"), ("operatyvine atmintis", "Arbeitsspeicher"),
    ("operatyvinė", "RAM"), ("operatyvine", "RAM"),
    # Stainless steel
    ("nerūdijantis plienas", "Edelstahl"), ("nerudijantis plienas", "Edelstahl"),
    ("nerūdijantis puodas", "Edelstahlkochtopf"), ("nerudijantis puodas", "Edelstahlkochtopf"),
    ("nerūdijantis", "Edelstahl"), ("nerudijantis", "Edelstahl"),
    # Smart (short form without -is/-ius)
    ("ismanus", "Smart"),
    # Power supply unit
    ("maitinimo blokas", "Netzteil"), ("maitinimo bloko", "Netzteil"),
    # PC case
    ("kompiuterio dėklas", "PC-Gehäuse"), ("kompiuterio deklas", "PC-Gehäuse"),
    ("kompiuterio", "Computer"),
    # Chair types
    ("žaidimų kėdė", "Gaming-Stuhl"), ("zaidimu kede", "Gaming-Stuhl"),
    ("ofiso kėdė", "Bürostuhl"), ("ofiso kede", "Bürostuhl"),
    ("kėdė", "Stuhl"), ("kedes", "Stuhl"), ("kede", "Stuhl"),
    # Office genitive
    ("ofiso", "Büro"),
    # Scooter / e-scooter
    ("elektrinis motoroleris", "E-Scooter"), ("elektrinis motorolerio", "E-Scooter"),
    ("motoroleris", "Roller"), ("motorolerio", "Roller"),
    # Dispenser / dosator
    ("vandens dozatorius", "Wasserspender"), ("dozatorius", "Dosierer"),
    ("dozatoriaus", "Dosierer"),
    # Smoke / CO detector
    ("dūmų detektorius", "Rauchmelder"), ("dumu detektorius", "Rauchmelder"),
    ("anglies monoksido detektorius", "CO-Melder"),
    ("detektorius", "Detektor"), ("detektoriaus", "Detektor"),
    # Memory card
    ("atminties kortelė", "Speicherkarte"), ("atminties korteles", "Speicherkarte"),
    ("kortelė", "Karte"), ("korteles", "Karte"),
    # Watering can
    ("laistyklė", "Gießkanne"), ("laistyklės", "Gießkanne"),
    # Garden genitive (sodo žarna = garden hose — but žarna is already handled)
    ("sodo žarna", "Gartenschlauch"), ("sodo zarna", "Gartenschlauch"),
    ("sodo", "Garten"),
    # Band saw
    ("juostinis pjūklas", "Bandsäge"), ("juostinis pjuklas", "Bandsäge"),
    ("juostinis", "Band"), ("juostine", "Band"),
    # Contact grill
    ("kontaktinis grilis", "Kontaktgrill"), ("kontaktinis grilio", "Kontaktgrill"),
    ("kontaktinis", "Kontakt"), ("kontaktine", "Kontakt"),
    # Wind generator
    ("vėjo generatorius", "Windgenerator"), ("vejo generatorius", "Windgenerator"),
    ("vėjo turbina", "Windturbine"), ("vejo", "Wind"), ("vėjo", "Wind"),
    # Air pump vs vacuum cleaner (oro siurblys = air pump, not vacuum)
    ("oro siurblys", "Luftpumpe"), ("oro siurblio", "Luftpumpe"),
    ("oro išpurškiklis", "Lufterfrischer"), ("oro ispurskiklis", "Lufterfrischer"),
    ("oro", "Luft"),
    # Air diffuser / aroma diffuser
    ("išpurškiklis", "Diffusor"), ("ispurskiklis", "Diffusor"),
    # Standing desk
    ("stovintis stalas", "Stehschreibtisch"), ("stovinti stala", "Stehschreibtisch"),
    ("stovintis", "Steh"), ("stovinti", "Steh"),
    # Portable adjective
    ("portativinis garsiakalbis", "Portabler Lautsprecher"), ("portativinis garsiakalb", "Portabler Lautsprecher"),
    ("portativinis", "Portabel"), ("portativine", "Portabel"),
    # Large adjective (didelis šaldytuvas = large fridge)
    ("didelis", "Groß"), ("didele", "Groß"),
    # Compact adjective
    ("kompaktiškas", "Kompakt"), ("kompaktiska", "Kompakt"), ("kompaktiskas", "Kompakt"),
    # Maker / machine for food
    ("ledų gamintuvas", "Eismaschine"), ("ledu gamintuvas", "Eismaschine"),
    ("jogurto gamintuvas", "Joghurtbereiter"), ("jogurto gamintuve", "Joghurtbereiter"),
    ("sūrio gamintuvas", "Käsebereiter"), ("surio gamintuvas", "Käsebereiter"),
    ("gamintuvas", "Maschine"), ("gamintuvo", "Maschine"),
    # Thermos
    ("termosas", "Thermosflasche"), ("termoso", "Thermosflasche"),
    # Pasta machine
    ("makaronų mašina", "Nudelmaschine"), ("makaronu masina", "Nudelmaschine"),
    ("makaronų", "Nudel"), ("makaronu", "Nudel"),
    # Pizza stone
    ("picos akmuo", "Pizzastein"), ("picos akmenuo", "Pizzastein"),
    ("picos", "Pizza"),
    # Paper
    ("kepimo popierius", "Backpapier"), ("kepimo popieriaus", "Backpapier"),
    ("popierius", "Papier"), ("popieriaus", "Papier"),
    # Petrol / gasoline powered
    ("benzininis generatorius", "Benzingenerator"), ("benzininis", "Benzin"), ("benzinine", "Benzin"),
    # Baby monitor (kūdikio monitoriaus)
    ("kūdikio monitoriaus", "Babyphone"), ("kudikio monitoriaus", "Babyphone"),
    ("monitoriaus", "Monitor"),
    # Video projector
    ("videoprojektorius", "Videoprojektor"), ("videoprojekcija", "Videoprojektion"),
    # Multi-channel
    ("daugiakanalis", "Mehrkanal"), ("daugiakanalio", "Mehrkanal"),
    # Ice scraper / car scraper
    ("ledo grandiklis", "Eisschaber"), ("ledo grandiklio", "Eisschaber"),
    ("grandiklis", "Schaber"), ("grandiklio", "Schaber"),
    # Mechanical (mechaniška šluota = carpet sweeper)
    ("mechaniška šluota", "Teppichkehrer"), ("mechaniska slota", "Teppichkehrer"),
    ("mechaniška", "Mechanisch"), ("mechaniskas", "Mechanisch"), ("mechaniškas", "Mechanisch"),
    # Interactive screen / display
    ("interaktyvus ekranas", "Interaktives Display"), ("interaktyvi", "Interaktiv"),
    ("interaktyvus", "Interaktiv"),
    # Food container / lunch box
    ("dėžutė maistui", "Lunchbox"), ("dezute maistui", "Lunchbox"),
    ("dėžutė", "Behälter"), ("dezute", "Behälter"),
    # Ice cream (ledų)
    ("ledų", "Eis"), ("ledu", "Eis"),
    # Yogurt genitive
    ("jogurto", "Joghurt"),
    # Cheese genitive
    ("sūrio", "Käse"), ("surio", "Käse"),
    # Small adjective
    ("mažas", "Klein"), ("maza", "Klein"),
    # Titanium (premium material)
    ("titanas", "Titan"), ("titanio", "Titan"),
    # Battery instrumental (su akumuliatoriumi = with battery)
    ("akumuliatoriumi", "Akku"), ("akumuliatoriaus", "Akku"),
    # Absolute adjective (Dyson Absolute)
    ("absoliutus", "Absolute"), ("absoliutine", "Absolute"),
    # High pressure (aukšto slėgio plovykla)
    ("aukšto slėgio", "Hochdruck"), ("auksto slegio", "Hochdruck"),
    ("slėgio", "Druck"), ("slegio", "Druck"),
    # Screwdriver
    ("akumuliatorinis atsuktuvas", "Akkuschrauber"), ("akumuliatorinis atsuktuve", "Akkuschrauber"),
    ("elektrinis atsuktuvas", "Elektrischer Schrauber"), ("elektrinis atsuktuve", "Elektrischer Schrauber"),
    ("atsuktuvas", "Schrauber"), ("atsuktuvo", "Schrauber"),
    # Car genitive (automobilio) — compound first
    ("automobilio kompresorius", "Auto-Kompressor"), ("automobilio kompresoriaus", "Auto-Kompressor"),
    ("automobilio siurblys", "Auto-Staubsauger"), ("automobilio siurblio", "Auto-Staubsauger"),
    ("automobilio", "Auto"),
    # Suitcase
    ("lagaminas", "Koffer"), ("lagamino", "Koffer"),
    # Christmas tree / decorations
    ("kalėdinė eglutė", "Weihnachtsbaum"), ("kaledine eglute", "Weihnachtsbaum"),
    ("eglutė", "Weihnachtsbaum"), ("eglutes", "Weihnachtsbaum"),
    ("kalėdinė", "Weihnachts"), ("kaledine", "Weihnachts"),
    # Pet supplies
    ("šunų guolis", "Hundebett"), ("sunu guolis", "Hundebett"),
    ("kačių draskyklė", "Kratzbaum"), ("kaciu draskykle", "Kratzbaum"),
    ("šunų", "Hunde"), ("sunu", "Hunde"),
    ("kačių", "Katzen"), ("kaciu", "Katzen"),
    # Hydraulic jack
    ("hidraulinis domkratas", "Hydraulikwagenheber"), ("domkratas", "Wagenheber"),
    ("domkrato", "Wagenheber"),
    # E-book reader
    ("elektroninė knyga", "E-Book"), ("elektronine knyga", "E-Book"),
    ("elektroninė", "Elektronisch"), ("elektronine", "Elektronisch"),
    # Door lock
    ("durų užraktas", "Türschloss"), ("duru uzraktas", "Türschloss"),
    ("durų spyna", "Türschloss"), ("duru spyna", "Türschloss"),
    ("durų", "Tür"), ("duru", "Tür"),
    # Protein / collagen supplement
    ("baltymų produktas", "Proteinprodukt"), ("baltymu produktas", "Proteinprodukt"),
    ("baltymų", "Protein"), ("baltymu", "Protein"),
    ("kolagenas", "Kollagen"), ("kolageno", "Kollagen"),
    # v7.46 — stalo tenisas fix (sort puts this before standalone "stalo"→Desktop)
    ("stalo tenisas", "Tischtennis"), ("stalo teniso", "Tischtennis"),
    ("stalo teniso rakete", "Tischtennisschläger"), ("stalo teniso kamuolys", "Tischtennisball"),
    # Perfume / fragrance
    ("aromatine zvake", "Duftkerze"), ("aromatines zvakes", "Duftkerze"),
    ("zvake", "Kerze"), ("zvakiu", "Kerzen"),
    ("foto ramelis", "Bilderrahmen"), ("foto ramelio", "Bilderrahmen"),
    ("ramelis", "Rahmen"), ("ramelio", "Rahmen"),
    ("kvepalai", "Parfüm"), ("kvepalu", "Parfüm"),
    ("parfumas", "Parfüm"), ("parfumo", "Parfüm"),
    ("sampunas", "Shampoo"), ("sampuno", "Shampoo"),
    # Tennis / racket sports
    ("teniso rakete", "Tennisschläger"), ("teniso kamuolys", "Tennisball"),
    ("teniso striuke", "Tennisshirt"), ("teniso bateliai", "Tennisschuhe"),
    ("tenisas", "Tennis"), ("teniso", "Tennis"),
    ("badmintono rakete", "Badmintonschläger"), ("badmintono kamuolys", "Federball"),
    ("badmintonas", "Badminton"), ("badmintono", "Badminton"),
    # Football / basketball
    ("futbolo kamuolys", "Fußball"), ("futbolo vartai", "Fußballtor"),
    ("futbolo bateliai", "Fußballschuhe"), ("futbolas", "Fußball"), ("futbolo", "Fußball"),
    ("krepsinio kamuolys", "Basketball"), ("krepsinio vartai", "Basketballkorb"),
    ("krepsis", "Basketball"), ("krepsinio", "Basketball"),
    # Snow / skate sports
    ("snieglenciu rinkinys", "Snowboard-Set"), ("snieglente", "Snowboard"), ("snieglenciu", "Snowboards"),
    ("riedlentes riedmenys", "Skateboard-Trucks"),
    ("riedlente", "Skateboard"), ("riedlenciu", "Skateboards"),
    # Home textiles / bedroom
    ("ortopedine pagalve", "orthopädisches Kissen"), ("kuno pagalve", "Körperkissen"),
    ("miego pagalve", "Schlafkissen"),
    ("pagalve", "Kissen"), ("pagalviu", "Kissen"),
    ("patalynes komplektas", "Bettwäsche-Set"), ("patalyne", "Bettwäsche"), ("patalynes", "Bettwäsche"),
    # Thermos mug
    ("termosinis puodelis", "Thermobecher"), ("termo puodelis", "Thermobecher"),
    ("termopuodelis", "Thermobecher"), ("termopuodelio", "Thermobecher"),
    # v7.45 — Books
    ("programavimo knyga", "Programmierbuch"), ("vaikiskas knyga", "Kinderbuch"),
    ("knygu rinkinys", "Bücherset"), ("knygu rinkinio", "Bücherset"),
    ("knyga", "Buch"), ("knygos", "Buch"), ("knygu", "Bücher"),
    # Clothing (compound before standalone)
    ("vaiku striuke", "Kinderjacke"), ("ziemos striuke", "Winterjacke"),
    ("vasaros striuke", "Sommerjacke"), ("lietaus striuke", "Regenjacke"),
    ("striuke", "Jacke"), ("striuku", "Jacken"),
    ("megztinis", "Pullover"), ("megztinio", "Pullover"),
    ("vaiku suknele", "Kinderkleid"), ("suknele", "Kleid"), ("sukneles", "Kleid"),
    ("sportinis kostiumas", "Sportanzug"), ("kostiumas", "Kostüm"), ("kostiumo", "Kostüm"),
    ("vaiku pirstines", "Kinderhandschuhe"), ("ziemos pirstines", "Winterhandschuhe"),
    ("bokso pirstines", "Boxhandschuhe"),
    ("pirstines", "Handschuhe"), ("pirstiniu", "Handschuhe"),
    # Waffle maker
    ("vafline", "Waffeleisen"), ("vafliu", "Waffel"),
    # Outdoor / garden
    ("sodo pavesine", "Gartenpavillon"), ("pavesine", "Pavillon"), ("pavesines", "Pavillon"),
    ("vaiku supuokles", "Kinderschaukel"), ("sodo supuokles", "Gartenschaukel"),
    ("supuokles", "Schaukel"), ("supuokliu", "Schaukel"),
    # Furniture
    ("lauko baldai", "Gartenmöbel"), ("vaiku baldai", "Kindermöbel"),
    ("biuro baldai", "Büromöbel"), ("miegamojo baldai", "Schlafzimmermöbel"),
    ("baldai", "Möbel"), ("baldu", "Möbel"),
    # Toy construction set / toy car
    ("zaidiminis konstruktorius", "Konstruktionsspielzeug"),
    ("konstruktorius", "Bausatz"), ("konstruktoriaus", "Bausatz"),
    ("zaisline masinyke", "Spielzeugauto"), ("masinyke", "Spielzeugauto"), ("masiniu", "Spielzeugauto"),
    # v7.44 — Vitamins / supplements (compound phrases before standalone)
    ("vitaminu kompleksas", "Vitaminkomplex"), ("vitaminu komplekse", "Vitaminkomplex"),
    ("vitaminu papildas", "Vitaminpräparat"), ("vitaminu papildo", "Vitaminpräparat"),
    ("vitaminas", "Vitamin"), ("vitaminu", "Vitamin"), ("vitaminai", "Vitamin"),
    ("magnio gele", "Magnesiumgel"), ("magnio tabletes", "Magnesiumtabletten"),
    ("magnio", "Magnesium"), ("magnis", "Magnesium"),
    ("kreatinas", "Kreatin"), ("kreatino", "Kreatin"),
    # Shoes / footwear
    ("sportiniai batai", "Sportschuhe"), ("sportbaciai", "Sportschuhe"), ("sportbacio", "Sportschuhe"),
    ("vaiku batai", "Kinderschuhe"), ("vaiku batu", "Kinderschuhe"),
    ("kedai", "Sneaker"),
    ("batai", "Schuhe"), ("batu", "Schuhe"),
    # Doll / toy doll (lėlė — before "lele" disambiguation)
    ("lele Barbie", "Barbie Puppe"), ("leles Barbie", "Barbie Puppe"),
    ("lele", "Puppe"), ("leles", "Puppe"),
    # Kitchen knife
    ("peiliu blokas", "Messerblock"), ("peilio bloko", "Messerblock"),
    ("virtuvinis peilis", "Küchenmesser"), ("keptuves peilis", "Pfannenwender"),
    ("peilis", "Messer"), ("peilio", "Messer"), ("peiliai", "Messer"),
    # Scissors (garden scissors handled by sodo→Garten prefix already)
    ("sodo zirkles", "Gartenschere"), ("sodo zirkliu", "Gartenschere"),
    ("zirkles", "Schere"), ("zirkliu", "Schere"),
    # Food slicer
    ("pjaustytuvas", "Aufschnittmaschine"), ("pjaustytuvo", "Aufschnittmaschine"),
    # Car tyres (padangos compound first — automobilio padangos already covered via automobilio→Auto)
    ("automobilio padangos", "Autoreifen"), ("automobilio padanga", "Autoreifen"),
    ("ziemos padangos", "Winterreifen"), ("vasaros padangos", "Sommerreifen"),
    ("padangos", "Reifen"), ("padanga", "Reifen"),
    # Lubricant / engine oil
    ("variklio tepalas", "Motoröl"), ("variklio tepalo", "Motoröl"),
    ("tepalas", "Schmiermittel"), ("tepalo", "Schmiermittel"),
    # Tape measure (matavimo juosta first — "matavimo" standalone kept generic)
    ("matavimo juosta", "Maßband"), ("matavimo juostos", "Maßband"),
    ("matavimo", "Mess"),
    # v7.43 — Music instruments (compound first, then standalone)
    ("elektrinis pianinas", "E-Piano"), ("elektrine pianinas", "E-Piano"),
    ("elektrinis sintezatorius", "Elektrischer Synthesizer"),
    ("gitara", "Gitarre"), ("gitaros", "Gitarre"),
    ("pianinas", "Klavier"), ("pianino", "Klavier"),
    ("sintezatorius", "Synthesizer"), ("sintezatoriaus", "Synthesizer"),
    ("bugnas", "Schlagzeug"), ("bugnu", "Schlagzeug"),
    ("smuikas", "Geige"), ("smiko", "Geige"),
    ("fleita", "Flöte"), ("fleitos", "Flöte"),
    # Sports / outdoor
    ("vaizdo registratorius", "Dashcam"), ("vaizdo registratoriaus", "Dashcam"),
    ("registratorius", "Dashcam"), ("registratoriaus", "Dashcam"),
    ("batutas", "Trampolin"), ("batuto", "Trampolin"),
    ("slidu", "Ski"),
    ("paciuzos", "Schlittschuhe"), ("paciuzu", "Schlittschuhe"),
    ("meskere", "Angelrute"), ("meskeriu", "Angelrute"),
    ("zvejybos", "Angel"), ("zvejyba", "Angel"),
    ("plaukimo akiniai", "Schwimmbrille"), ("plaukimo kostiumelis", "Badeanzug"),
    ("plaukimo", "Schwimm"),
    # Milk frother
    ("pienu putuke", "Milchaufschäumer"), ("pienu putuku", "Milchaufschäumer"),
    ("pienuke", "Milchaufschäumer"), ("pienuku", "Milchaufschäumer"),
    # Furniture / home textiles (compound before standalone)
    ("dvigule lova", "Doppelbett"), ("viengule lova", "Einzelbett"),
    ("lovos ramas", "Bettrahmen"), ("lovos rama", "Bettrahmen"),
    ("lova", "Bett"), ("lovos", "Bett"),
    ("drabuzine spinta", "Kleiderschrank"), ("spinta", "Schrank"), ("spintos", "Schrank"),
    ("kilimas", "Teppich"), ("kilimo", "Teppich"),
    # v7.52 — Word-order fix for sofa kampine + misc
    ("sofa kampine", "Ecksofa"), ("sofa miegama", "Schlafsofa"),
    ("kampine", "Eck"),
    ("hamakas", "Hängematte"), ("hamaku", "Hängematte"),
    ("ausinukas", "Ohrhörer"), ("ausinuko", "Ohrhörer"),
    ("menteliklis", "Klimmzugstange"), ("menteliklio", "Klimmzugstange"),
    ("stanga", "Langhantel"), ("stangos", "Langhantel"),
    ("preso suoliukas", "Schrägbank"), ("suoliukas", "Hantelbank"), ("suoliuko", "Hantelbank"),
    ("irklente", "SUP-Board"), ("irklentes", "SUP-Boards"),
    ("stovyklavimo kede", "Campingstuhl"), ("stovyklavimo stalas", "Campingtisch"),
    ("stovyklavimo virykle", "Campingkocher"), ("stovyklavimo miegmaišis", "Campingschlafsack"),
    ("stovyklavimo", "Camping"),
    ("aminorugsciai", "Aminosäuren"), ("aminoru", "Aminosäuren"),
    # v7.51 — Window treatments
    ("langų uždanga", "Fenstergardine"), ("interjero uzdanga", "Innengardine"),
    ("uzdanga", "Vorhang"), ("uzdangu", "Vorhänge"),
    ("uzuolaida", "Vorhang"), ("uzuolaidų", "Vorhänge"),
    ("tamsinamoji rolete", "Verdunkelungsrollo"), ("rolete", "Rollo"), ("roletu", "Rollos"),
    ("zaluzija", "Jalousie"), ("zaluziju", "Jalousien"),
    # v7.51 — Bedding addition
    ("flanelinė paklodė", "Flanellbettlaken"), ("paklode", "Bettlaken"), ("paklodziu", "Bettlaken"),
    ("megztas apklotas", "Strickdecke"), ("apklotas", "Decke"), ("apklotu", "Decken"),
    # v7.51 — Water sports
    ("vaiku baseinas", "Kinderplanschbecken"), ("interjero baseinas", "Innenschwimmbad"),
    ("aufblasbarer baseinas", "aufblasbarer Pool"),
    ("baseinas", "Schwimmbecken"), ("baseino", "Pool"),
    ("baidarele", "Kajak"), ("baidareles", "Kajaks"),
    ("kanoja", "Kanu"), ("kanojos", "Kanu"),
    ("irklai", "Paddel"), ("irklu", "Paddel"),
    # v7.51 — Cables / electrical
    ("kabelis", "Kabel"), ("kabelio", "Kabel"),
    ("laidas", "Kabel"), ("laido", "Kabel"),
    ("tinklines", "Steckdosenleiste"), ("tinkliniu", "Steckdosenleisten"),
    # v7.51 — Arts / crafts
    ("plastilinas", "Knete"), ("plastilino", "Knete"),
    # v7.51 — Flooring / construction
    ("grindys", "Boden"), ("grindylentu", "Dielen"),
    ("plytelis", "Fliese"), ("plyteliu", "Fliesen"),
    # v7.50 — Automotive accessories
    ("automobilio radijas", "Autoradio"), ("automagnetola", "Autoradio"), ("automagnetolos", "Autoradio"),
    ("automobilio vairas", "Lenkrad"), ("sportinis vairas", "Sportlenkrad"),
    ("vairas", "Lenkrad"), ("vairo", "Lenkrad"),
    ("automobilio ratai", "Autoräder"), ("ratu rinkinys", "Rädersatz"),
    ("ratai", "Felgen"), ("ratu", "Felgen"),
    # v7.50 — Home improvement / flooring
    ("sienu dazai", "Wandfarbe"), ("lauko dazai", "Außenfarbe"), ("medzio dazai", "Holzfarbe"),
    ("dazai", "Farbe"), ("dazo", "Farbe"),
    ("tapetai", "Tapete"), ("tapetu", "Tapeten"),
    ("laminatas", "Laminat"), ("laminato", "Laminat"),
    ("parketas", "Parkett"), ("parketo", "Parkett"),
    # v7.50 — Music instruments
    ("akordeonas", "Akkordeon"), ("akordeono", "Akkordeon"),
    ("trimitas", "Trompete"), ("trimito", "Trompete"),
    ("saksofonas", "Saxophon"), ("saksofono", "Saxophon"),
    # v7.50 — Office / school
    ("pieštukas", "Bleistift"), ("piestukas", "Bleistift"), ("piestuko", "Bleistift"),
    ("flomasteris", "Filzstift"), ("flomasteri", "Filzstift"),
    # v7.50 — Garden
    ("sodo fontanas", "Gartenbrunnen"), ("fontanas", "Brunnen"), ("fontano", "Brunnen"),
    # v7.49 — Beauty / bathroom / pet / hunting / protection
    ("veidrodis su apšvietimu", "Beleuchteter Spiegel"), ("kosmetinis veidrodis", "Kosmetikspiegel"),
    ("drėkinamasis kremas", "Feuchtigkeitscreme"), ("veido kremas", "Gesichtscreme"),
    ("kuno kremas", "Körpercreme"), ("rankų kremas", "Handcreme"),
    ("kremas", "Creme"), ("kremo", "Creme"),
    ("dezodorantas", "Deodorant"), ("dezodoranto", "Deodorant"),
    ("losjonas", "Lotion"), ("losjono", "Lotion"),
    ("vonios kabina", "Duschkabine"), ("vonios kubas", "Whirlpool"),
    ("vonia", "Badewanne"), ("vonios", "Bad"),
    ("vonios rankslostis", "Badetuch"), ("vaiku rankslostis", "Kinderhandtuch"),
    ("rankslostis", "Handtuch"), ("ranklosciu", "Handtücher"),
    ("sunu maistas", "Hundefutter"), ("sunu lova", "Hundebett"), ("sunu pavadeli", "Hundeleine"),
    ("kaciu maistas", "Katzenfutter"), ("kaciu kraikes dezute", "Katzentoilette"),
    ("katinas", "Kater"), ("katino", "Katers"),
    ("augintinis", "Haustier"), ("augintinio", "Haustier"),
    ("medziokles slidai", "Jagdski"), ("medziokles kuprine", "Jagdrucksack"),
    ("medziokle", "Jagd"), ("medziokles", "Jagd"),
    ("sliauztukai", "Knieschoner"), ("sliauztukas", "Knieschoner"),
    # v7.48 — Bags / accessories / jewelry
    ("kuprine su ratukais", "Trolley-Rucksack"), ("vaiku kuprine", "Kinderrucksack"),
    ("kuprine", "Rucksack"), ("kuprines", "Rucksack"),
    ("odine rankine", "Lederhandtasche"), ("rankine", "Handtasche"), ("rankines", "Handtaschen"),
    ("odinis dirzas", "Ledergürtel"), ("sportinis dirzas", "Sportgürtel"),
    ("dirzas", "Gürtel"), ("dirzo", "Gürtel"),
    ("piniginė", "Geldbörse"), ("pinigines", "Geldbörse"),
    ("papuošalai", "Schmuck"), ("papuosalu", "Schmuck"),
    ("ausų karoliai", "Ohrringe"), ("karoliai", "Halskette"), ("karoliu", "Halskette"),
    ("auskarai", "Ohrringe"), ("auskariu", "Ohrringe"),
    ("portfelis", "Aktentasche"), ("portfelio", "Aktentasche"),
    ("ziedas", "Ring"), ("ziedo", "Ring"),
    # v7.48 — Kitchen / home
    ("kavos puodelis", "Kaffeetasse"), ("puodelis", "Tasse"), ("puodelio", "Tasse"),
    ("sriubos dubuo", "Suppenschüssel"), ("dubuo", "Schüssel"), ("dubens", "Schüssel"),
    ("vazonas", "Blumentopf"), ("vazono", "Blumentopf"),
    # v7.48 — Miscellaneous
    ("automobilio tentas", "Autoplane"), ("lauko tentas", "Campingplane"),
    ("tentas", "Plane"), ("tento", "Plane"),
    ("siuvimo mašina", "Nähmaschine"), ("siuvimo", "Näh"),
    ("zaislinis automobilis", "Spielzeugauto"), ("zaislinis", "Spielzeug"),
    # v7.47 — Furniture
    ("kampine sofa", "Ecksofa"), ("miegama sofa", "Schlafsofa"),
    ("sofa", "Sofa"), ("sofos", "Sofas"),
    ("fotelis", "Sessel"), ("fotelio", "Sessel"),
    ("knygu lentyna", "Bücherregal"), ("sodo lentyna", "Gartenregal"),
    ("lentyna", "Regal"), ("lentynu", "Regale"),
    ("komoda", "Kommode"), ("komodu", "Kommoden"),
    # v7.47 — Clothing
    ("ziemos kepure", "Wintermütze"), ("vaiku kepure", "Kindermütze"),
    ("kepure", "Mütze"), ("kepures", "Mützen"),
    ("salikas", "Schal"), ("saliko", "Schal"),
    ("sportines kelnes", "Sporthose"), ("ziemos kelnes", "Winterhose"),
    ("kelnes", "Hose"), ("kelniu", "Hosen"),
    ("marskiniai", "Hemd"), ("marskiniu", "Hemden"),
    ("dzinsai", "Jeans"), ("dzinsu", "Jeans"),
    ("maudymosi kostiumelis", "Badeanzug"), ("maudymosi kelnaites", "Badehose"),
    ("maudymosi", "Bade"),
    ("kostiumelis", "Kostümchen"),
    # v7.47 — Boxing / roller skates / sled
    ("bokso maišas", "Boxsack"), ("bokso pirstines", "Boxhandschuhe"),
    ("boksas", "Boxen"), ("bokso", "Box"),
    ("riedutis", "Inlineskates"), ("rieduciu", "Inlineskates"),
    ("roges", "Schlitten"), ("rogiu", "Schlitten"),
    # v7.47 — Water bottle / diapers / yoga
    ("sporto gertuve", "Sporttrinkflasche"), ("vaiku gertuve", "Kinderflasche"),
    ("gertuve", "Trinkflasche"), ("gertuviu", "Trinkflaschen"),
    ("sauskelnes", "Windeln"), ("sauskelnems", "Windeln"),
    ("jogos kilimelis", "Yogamatte"), ("jogos blokelis", "Yogablock"),
    ("jogos", "Yoga"),
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
    ("treniruoklis", "sprzęt fitness"), ("treniruoklio", "sprzęt fitness"),
    ("hanteliai", "hantle"), ("hantelius", "hantle"), ("hantelis", "hantel"),
    ("svarsčiai", "ciężary"), ("svarsciai", "ciężary"), ("svarsti", "ciężarek"),
    ("kettlebell", "kettlebell"),
    # Multimedia
    ("grotuvas", "odtwarzacz"), ("mp3 grotuvas", "odtwarzacz mp3"),
    # Accessories
    ("įkroviklis", "ładowarka"), ("projektorius", "projektor"),
    # Robot vacuum
    ("robotinis dulkių siurblys", "robot odkurzający"), ("robotinis siurblys", "robot odkurzający"),
    ("robotinė vejapjovė", "robot koszący"), ("robotine vejapjove", "robot koszący"),
    ("robotinis", "robotyczny"), ("robotinė", "robotyczny"), ("robotine", "robotyczny"),
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
    # Pressure washer (must come before generic grindų plovykla below)
    ("aukštojo slėgio plovykla", "myjka ciśnieniowa"), ("slėginė plovykla", "myjka ciśnieniowa"),
    ("slegine plovykla", "myjka ciśnieniowa"),
    # Floor cleaner / wet floor mop
    ("grindų plovykla", "mop elektryczny"), ("grindu plovykla", "mop elektryczny"),
    ("plovykla", "myjka ciśnieniowa"),
    # Lawn mower (vejapjovė = variant spelling)
    ("vejapjovė", "kosiarka"), ("vejapjove", "kosiarka"),
    # Hedge trimmer
    ("krūmapjovė", "nożyce do żywopłotu"), ("krumapjove", "nożyce do żywopłotu"),
    # Grass trimmer / strimmer
    ("žolės trimeris", "podkaszarka do trawy"), ("zoles trimeris", "podkaszarka do trawy"),
    ("trimeris", "podkaszarka"),
    # Leaf blower
    ("lapų pūstuvas", "dmuchawa do liści"), ("lapu pustuvas", "dmuchawa do liści"),
    # Flashlight / torch
    ("žibintas", "latarka"), ("zibintas", "latarka"),
    # Nebulizer / inhaler
    ("nebulizatorius", "nebulizator"), ("nebulizatoriaus", "nebulizator"),
    # Massage chair / massage gun
    ("masažo kėdė", "fotel masujący"), ("masazo kede", "fotel masujący"),
    ("masažo kede", "fotel masujący"),
    ("masažo pistoletas", "pistolet do masażu"), ("masazo pistoletas", "pistolet do masażu"),
    ("masažo", "masaż"),
    # Pistol-type tools
    ("klijų pistoletas", "pistolet do kleju"), ("kliju pistoletas", "pistolet do kleju"),
    ("dažų pistoletas", "pistolet lakierniczy"), ("dazu pistoletas", "pistolet lakierniczy"),
    # Baby crib standalone "lovelė" (kūdikio lovelė already in dict above; this catches bare "lovelė")
    ("lovelė", "łóżeczko niemowlęce"), ("lovele", "łóżeczko"),
    # Baby genitive standalone fallback
    ("kūdikio", "dla niemowląt"), ("kudikio", "dla niemowląt"),
    # Dehumidifier
    ("drėgmės surinktuvas", "pochłaniacz wilgoci"), ("dregmes surinktuvas", "pochłaniacz wilgoci"),
    # Air compressor
    ("kompresorius", "kompresor"), ("kompresoriaus", "kompresor"),
    # Snow blower
    ("sniego valytuvas", "odśnieżarka"), ("sniego frezas", "odśnieżarka"),
    ("sniego freza", "odśnieżarka"),
    # Heat pump (šilumos siurblys must come before standalone siurblys→odkurzacz)
    ("šilumos siurblys", "pompa ciepła"), ("silumos siurblys", "pompa ciepła"),
    ("šilumos pompa", "pompa ciepła"), ("silumos pompa", "pompa ciepła"),
    # Heat pump system type
    ("oras vanduo", "powietrze-woda"), ("oras oras", "powietrze-powietrze"),
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
    # Oral irrigator / water flosser
    ("dantų iryklė", "irygator dentystyczny"), ("dantų irykle", "irygator dentystyczny"),
    ("iryklė", "irygator"), ("irykle", "irygator"),
    # Additional kitchen appliances
    ("ryžių viryklė", "ryżowar"), ("ryziu virykle", "ryżowar"),
    ("maisto džiovintuvas", "suszarka do żywności"), ("maisto dziovintuvas", "suszarka do żywności"),
    ("džiovintuvas maistui", "suszarka do żywności"), ("dziovintuvas maistui", "suszarka do żywności"),
    ("arbatinukas", "czajnik do herbaty"),
    # Power station / power bank
    ("galios stotelė", "stacja zasilania"), ("galios stotele", "stacja zasilania"),
    ("galios bankas", "powerbank"), ("galios banka", "powerbank"),
    ("galios", "zasilanie"),
    ("belaidis pakrovėjas", "ładowarka bezprzewodowa"), ("belaidis pakrovejas", "ładowarka bezprzewodowa"),
    ("pakrovėjas", "ładowarka"), ("pakrovejas", "ładowarka"),
    # Steam station (professional iron)
    ("garų stotis", "stacja pary"), ("garu stotis", "stacja pary"),
    # Heat recovery ventilation
    ("rekuperatorius", "rekuperator"), ("rekuperatoriaus", "rekuperator"),
    # Surveillance camera / video doorbell
    ("stebėjimo kamera", "kamera do monitoringu"), ("stebejimo kamera", "kamera do monitoringu"),
    ("vaizdo durų skambutis", "wideo dzwonek do drzwi"), ("vaizdo duru skambutis", "wideo dzwonek do drzwi"),
    ("durų skambutis", "dzwonek do drzwi"), ("duru skambutis", "dzwonek do drzwi"),
    # Smart home devices
    ("išmanusis termoregliatorius", "inteligentny termostat"), ("ismanysis termoregliatorius", "inteligentny termostat"),
    ("termoregliatorius", "termostat"), ("termoreguliatorius", "termostat"),
    ("išmanusis kištukas", "inteligentne gniazdko"), ("ismanysis kistukas", "inteligentne gniazdko"),
    ("kištukas", "gniazdko"), ("kistukas", "gniazdko"),
    ("išmanusis jungiklis", "smart włącznik"), ("ismanysis jungiklis", "smart włącznik"),
    ("jungiklis", "włącznik"),
    # Doorbell standalone
    ("skambutis", "dzwonek do drzwi"),
    # Surveillance standalone
    ("stebėjimo", "monitoringu"), ("stebejimo", "monitoringu"),
    # Baby / child products
    ("kūdikio monitorius", "niania elektroniczna"), ("kudikio monitorius", "niania elektroniczna"),
    ("automobilinė vaikiška kėdutė", "fotelik samochodowy"), ("vaikiška kėdutė", "fotelik samochodowy"),
    ("vaiska kedute", "fotelik samochodowy"), ("kėdutė", "fotelik"), ("kedute", "fotelik"),
    ("vaikiškas vežimėlis", "wózek dziecięcy"), ("vaikiskas vezimelis", "wózek dziecięcy"),
    ("vežimėlis", "wózek dziecięcy"), ("vezimelis", "wózek dziecięcy"),
    ("kūdikio lovelė", "łóżeczko niemowlęce"), ("kudikio lovele", "łóżeczko niemowlęce"),
    ("lopšelis", "łóżeczko niemowlęce"), ("lopselis", "łóżeczko niemowlęce"),
    # Drone
    ("dronas su kamera", "dron z kamerą"), ("dronas", "dron"),
    # E-reader
    ("e-knygu skaitvtuvas", "czytnik e-booków"), ("e-knygu", "e-book"),
    # Tablet computer (formal LT form)
    ("planšetinis kompiuteris", "tablet"), ("planšetinis", "tablet"),
    # Laptop (alternative grammatical form)
    ("nešiojamasis kompiuteris", "laptop"), ("nešiojamasis", "laptop"),
    # Battery / accumulator
    ("akumuliatorius", "akumulator"), ("akumuliatoriaus", "akumulator"),
    # Range hood (gartraukis = modern LT; gaubtas already in dict above)
    ("gartraukis", "okap kuchenny"), ("gartraukio", "okap kuchenny"),
    # Hair clipper / beard trimmer
    ("plaukų kirptuvas", "maszynka do strzyżenia"), ("plaukų kirptuvo", "maszynka do strzyżenia"),
    ("barzdos kirptuvas", "trymer do brody"), ("barzdos kirptuvo", "trymer do brody"),
    ("kirptuvas", "maszynka"), ("kirptuvo", "maszynka"),
    # Charging station standalone (galios stotelė→stacja zasilania is longer and matches first)
    ("stotelė", "stacja ładowania"), ("stotele", "stacja ładowania"),
    # Generic pistol/gun-type tool
    ("pistoletas", "pistolet"), ("pistoleto", "pistolet"),
    # Desktop computer
    ("stalo kompiuteris", "komputer stacjonarny"), ("stalo kompiuterio", "komputer stacjonarny"),
    ("stalo", "stacjonarny"),
    # Clothes steamer / face steamer / food steamer
    ("drabužių garintuvas", "parownica do ubrań"), ("drabuziu garintuvas", "parownica do ubrań"),
    ("veido garintuvas", "parownik do twarzy"), ("veido garintuvo", "parownik do twarzy"),
    ("garų šluota", "mop parowy"), ("garu slota", "mop parowy"),
    ("garintuvas", "parownik"), ("garintuvo", "parownik"),
    # Face (genitive)
    ("veido", "twarzy"),
    # Vanity / bathroom mirror
    ("kosmetinis veidrodis", "lusterko kosmetyczne"), ("kosmetinis veidrodžio", "lusterko kosmetyczne"),
    ("veidrodis", "lustro"), ("veidrodžio", "lustro"),
    # Electric blanket
    ("elektrinis antklodė", "koc elektryczny"), ("elektrinis antklode", "koc elektryczny"),
    ("antklodė", "koc"), ("antklode", "koc"),
    # Window cleaner
    ("langų valytuvas", "myjka do okien"), ("langu valytuvas", "myjka do okien"),
    ("langų", "okna"), ("langu", "okna"),
    # Body
    ("kūno masažuoklis", "masażer do ciała"), ("kuno masazuoklis", "masażer do ciała"),
    ("kūno", "do ciała"), ("kuno", "do ciała"),
    # Multifunctional
    ("daugiafunkcinis puodas", "multicooker"), ("daugiafunkcinis", "wielofunkcyjny"),
    ("daugiafunkcine", "wielofunkcyjna"),
    # Nose trimmer
    ("nosies kirptuvas", "trymer do nosa"), ("nosies kirptuvo", "trymer do nosa"),
    ("nosies", "do nosa"),
    # Brush
    ("plaukų šepetys", "szczotka do włosów"), ("plauku sepetys", "szczotka do włosów"),
    ("šepetys", "szczotka"), ("sepetys", "szczotka"),
    # Cleaning product
    ("langų valiklis", "płyn do mycia okien"), ("langu valiklis", "płyn do mycia okien"),
    ("valiklis", "środek czyszczący"), ("valiklio", "środek czyszczący"),
    # Ear cleaner
    ("ausų valytuvas", "oczyszczacz do uszu"), ("ausu valytuvas", "oczyszczacz do uszu"),
    ("ausų", "do uszu"), ("ausu", "do uszu"),
    # Generator
    ("inverterinis generatorius", "agregat prądotwórczy inwertorowy"),
    ("generatorius", "agregat prądotwórczy"), ("generatoriaus", "agregat prądotwórczy"),
    # Household / domestic adjective
    ("buitinis prietaisas", "sprzęt AGD"), ("buitinis", "AGD"), ("buitine", "AGD"),
    # Garden hose / watering / irrigation
    ("laistymo žarna", "wąż ogrodowy"), ("laistymo zarna", "wąż ogrodowy"),
    ("laistymo sistema", "system nawadniania"),
    ("žarna", "wąż"), ("zarna", "wąż"),
    ("laistymo", "nawadnianie"),
    # Pump
    ("dviračių pompa", "pompka rowerowa"), ("dviraciu pompa", "pompka rowerowa"),
    ("vandens pompa", "pompa wody"), ("vandens pompos", "pompa wody"),
    ("pompa", "pompa"), ("pompos", "pompa"),
    # Bicycle genitive
    ("dviračių šalmas", "kask rowerowy"), ("dviraciu salmas", "kask rowerowy"),
    ("dviračių", "rowerowy"), ("dviraciu", "rowerowy"),
    # Helmet
    ("motociklo šalmas", "kask motocyklowy"), ("motociklo salmas", "kask motocyklowy"),
    ("šalmas", "kask"), ("salmas", "kask"),
    # BBQ
    ("šašlykų", "BBQ"), ("saslyku", "BBQ"),
    # Chainsaw
    ("motopjūklas", "piła łańcuchowa"), ("motopjuklas", "piła łańcuchowa"),
    # Floor / ground
    ("grindų", "podłogi"), ("grindu", "podłogi"),
    # Industrial adjective
    ("pramoninis", "przemysłowy"), ("pramonine", "przemysłowa"),
    # Music center / stereo system
    ("muzikos centras", "zestaw muzyczny"), ("muzikos", "muzyka"),
    ("centras", "centrum"),
    # Construction dryer (must come before džiovintuvas→suszarka)
    ("statybinis džiovintuvas", "osuszacz budowlany"), ("statybine dziovintuvas", "osuszacz budowlany"),
    ("statybinis", "budowlany"), ("statybine", "budowlana"),
    # IPL / light hair removal device
    ("šviesos depiliatorius", "urządzenie IPL"), ("sviesos depiliatorius", "urządzenie IPL"),
    ("depiliatorius", "urządzenie do depilacji"), ("depiliatoriaus", "urządzenie do depilacji"),
    ("šviesos", "świetlny"), ("sviesos", "świetlny"),
    # Steam (garo genitive form)
    ("garo laidynas", "żelazko parowe"), ("garo lygintuvas", "żelazko parowe"),
    ("garo", "parowy"),
    # Tiles
    ("plyteliu valytuvas", "myjka do płytek"), ("plyteles valytuvas", "myjka do płytek"),
    ("plyteliu", "do płytek"), ("plyteles", "do płytek"),
    # Drill
    ("gręžtuvas", "wiertarka"), ("grežtuvas", "wiertarka"),
    ("gręžtuko", "wiertarka"), ("greztuko", "wiertarka"),
    # Tent
    ("palapinė", "namiot"), ("palapine", "namiot"),
    ("palapinės", "namiot"), ("palapines", "namiot"),
    # Sleeping bag
    ("miegmaišis", "śpiwór"), ("miegmaisio", "śpiwór"),
    # Blood pressure monitor
    ("tonometras", "ciśnieniomierz"), ("tonometro", "ciśnieniomierz"),
    # Pulse / heart rate monitor
    ("pulsometras", "pulsometr"), ("pulsometro", "pulsometr"),
    # Inhaler / nebulizer
    ("inhalatorius", "nebulizator"), ("inhaliatoriaus", "nebulizator"),
    # Welder
    ("suvirintuvas", "spawarka"), ("suvirintuvo", "spawarka"),
    # Meat grinder
    ("mėsmalė", "maszynka do mięsa"), ("mėsmalės", "maszynka do mięsa"),
    ("mesmalė", "maszynka do mięsa"), ("mesmale", "maszynka do mięsa"),
    # Garden/plant sprayer
    ("augalų purkštuvas", "opryskiwacz"), ("purkštuvas", "opryskiwacz"),
    ("purkštuvo", "opryskiwacz"),
    # Alarm system
    ("signalizacija", "alarm"), ("signalizacijos", "alarm"),
    # High chair (feeding chair)
    ("maitinimo kėdutė", "krzesełko do karmienia"), ("maitinimo kedute", "krzesełko do karmienia"),
    ("maitinimo", "karmienie"),
    # Elliptical trainer
    ("elipsinis treniruoklis", "orbitrek"), ("elipsinis treniruoklio", "orbitrek"),
    ("elipsinis", "eliptyczny"), ("elipsine", "eliptyczny"),
    # Iron (feminine form)
    ("lygintuvė", "żelazko"), ("lygintuve", "żelazko"),
    # Ironing board
    ("lyginimo lenta", "deska do prasowania"), ("lyginimo", "do prasowania"),
    # Multimeter
    ("multimetras", "multimetr"), ("multimetro", "multimetr"),
    # Camera lens
    ("fotoaparato objektyvas", "obiektyw do aparatu"), ("objektyvas", "obiektyw"),
    ("objektyvo", "obiektyw"),
    # Tripod
    ("trikojis", "statyw"), ("trikojo", "statyw"),
    # Graphics card
    ("grafikos plokštė", "karta graficzna"), ("grafikos kortele", "karta graficzna"),
    ("grafikos", "graficzny"),
    # CPU
    ("procesorius", "procesor"), ("procesoriaus", "procesor"),
    # Oral irrigator
    ("burnos dušas", "irygator"), ("burnos", "jamy ustnej"),
    # Lawn mower (alternative phrasing)
    ("žolės pjovimo mašina", "kosiarka"), ("zoles pjovimo masina", "kosiarka"),
    ("žolės", "trawnik"), ("zoles", "trawnik"),
    # Security camera
    ("apsaugos kamera", "kamera bezpieczeństwa"), ("apsaugos", "bezpieczeństwa"),
    # Internet router
    ("interneto maršrutizatorius", "router internetowy"), ("interneto marsrutizatorius", "router internetowy"),
    ("interneto", "internetowy"),
    # Network switch
    ("tinklo jungiklis", "switch sieciowy"), ("tinklo", "sieciowy"),
    # Electric saw
    ("elektros pjūklas", "piła elektryczna"), ("elektros pjuklas", "piła elektryczna"),
    ("elektros", "elektryczny"),
    # Colors
    ("juodas", "czarny"), ("juoda", "czarny"), ("juodos", "czarny"),
    ("baltas", "biały"), ("balta", "biały"), ("baltos", "biały"),
    ("pilkas", "szary"), ("pilka", "szary"), ("pilkos", "szary"),
    ("sidabrinis", "srebrny"), ("sidabrine", "srebrny"),
    ("auksinis", "złoty"), ("auksinė", "złoty"), ("auksinė", "złoty"),
    ("mėlynas", "niebieski"), ("melyna", "niebieski"), ("mėlyna", "niebieski"), ("melynas", "niebieski"),
    ("žalias", "zielony"), ("zalias", "zielony"), ("žalia", "zielony"), ("zalia", "zielony"),
    ("raudonas", "czerwony"), ("raudona", "czerwony"),
    ("violetinis", "fioletowy"), ("violetine", "fioletowy"),
    ("rožinis", "różowy"), ("rozinis", "różowy"), ("rožinė", "różowy"), ("rozine", "różowy"),
    # Automotive adjective
    ("automobilinis siurblys", "odkurzacz samochodowy"), ("automobilinis", "samochodowy"),
    ("automobiline", "samochodowy"),
    # Radiator / panel heater
    ("elektrinis radiatorius", "grzejnik elektryczny"), ("radiatorius", "grzejnik"),
    ("radiatoriaus", "grzejnik"),
    # GPS navigator
    ("navigatorius", "nawigacja GPS"), ("navigatoriaus", "nawigacja GPS"),
    # Scanner
    ("skeneris", "skaner"), ("skenerio", "skaner"),
    # Bread maker
    ("duoninė", "maszyna do chleba"), ("duonine", "maszyna do chleba"),
    # Food production/making genitive
    ("maisto gamybos mašina", "robot kuchenny"), ("gamybos masina", "robot kuchenny"),
    ("gamybos", "przygotowania"),
    # Solarium / tanning lamp
    ("soliariumo lempa", "lampa solaryjna"), ("soliariumo", "solarium"),
    # Wireless adjective
    ("bevielis", "bezprzewodowy"), ("bevieles", "bezprzewodowy"),
    # Light fixtures
    ("lubų šviestuvas", "lampa sufitowa"), ("lubu sviestuvas", "lampa sufitowa"),
    ("sieninis šviestuvas", "lampa ścienna"), ("sieninis sviestuvas", "lampa ścienna"),
    ("stalo lempa", "lampka biurkowa"), ("stalo sviestuvas", "lampka biurkowa"),
    ("grindų lempa", "lampa podłogowa"), ("grindu lempa", "lampa podłogowa"),
    ("šviestuvas", "lampa"), ("sviestuvas", "lampa"),
    # Floor/massage mat
    ("masažinis kilimėlis", "mata do masażu"), ("masazinis kilimelis", "mata do masażu"),
    ("jogos kilimėlis", "mata do jogi"), ("jogos kilimelis", "mata do jogi"),
    ("kilimėlis", "mata"), ("kilimelis", "mata"),
    # Food chopper
    ("maisto smulkintuvas", "rozdrabniacz"), ("trintuvas", "rozdrabniacz"),
    ("smulkintuvas", "rozdrabniacz"), ("trintuvo", "rozdrabniacz"), ("smulkintuvo", "rozdrabniacz"),
    # Coffee beans
    ("kavos pupelių", "kawa ziarnista"), ("kavos pupeliu", "kawa ziarnista"),
    ("pupelių", "ziarnista"), ("pupeliu", "ziarnista"),
    # Fast charger
    ("greitasis įkroviklis", "szybka ładowarka"), ("greitasis ikroviklis", "szybka ładowarka"),
    ("greitoji įkrova", "szybkie ładowanie"),
    ("greitasis", "szybki"), ("greitoji", "szybki"),
    # Game controller
    ("žaidimų valdiklis", "kontroler do gier"), ("zaidimu valdiklis", "kontroler do gier"),
    ("nuotolinio valdymo pultas", "pilot"),
    ("valdiklis", "kontroler"), ("valdiklio", "kontroler"),
    # Inkjet printer
    ("rašalinis spausdintuvas", "drukarka atramentowa"), ("rasalinis spausdintuvas", "drukarka atramentowa"),
    ("rašalinis", "atramentowy"), ("rasalinis", "atramentowy"),
    # Laser printer
    ("lazerinis spausdintuvas", "drukarka laserowa"), ("lazerine spausdintuvas", "drukarka laserowa"),
    ("lazerinis", "laserowy"), ("lazerine", "laserowy"),
    # Glucose meter
    ("gliukometras", "glukometr"), ("gliukometro", "glukometr"),
    # Massage mat
    ("masažinis", "do masażu"), ("masazinis", "do masażu"),
    # Blood pressure monitor
    ("kraujospūdžio matuoklis", "ciśnieniomierz"), ("kraujospudzio matuoklis", "ciśnieniomierz"),
    ("kraujo spaudimo matuoklis", "ciśnieniomierz"), ("kraujo spaudimo", "ciśnienie krwi"),
    ("kraujospūdžio", "ciśnienie krwi"), ("kraujospudzio", "ciśnienie krwi"),
    # Measurement device
    ("matuoklis", "miernik"), ("matuoklio", "miernik"),
    # Goggles / glasses
    ("slidinėjimo akiniai", "gogle narciarskie"), ("slidinejimo akiniai", "gogle narciarskie"),
    ("dviračių akiniai", "okulary rowerowe"), ("dviraciu akiniai", "okulary rowerowe"),
    ("saulės akiniai", "okulary przeciwsłoneczne"), ("saules akiniai", "okulary przeciwsłoneczne"),
    ("akiniai", "okulary"), ("akiniu", "okulary"),
    # Skiing
    ("slidinėjimo šalmas", "kask narciarski"), ("slidinejimo salmas", "kask narciarski"),
    ("slidinėjimo", "narciarski"), ("slidinejimo", "narciarski"),
    # Face mask
    ("veido kaukė", "maska do twarzy"), ("veido kauke", "maska do twarzy"),
    ("akių kaukė", "maska na oczy"), ("akiu kauke", "maska na oczy"),
    ("kaukė", "maska"), ("kauke", "maska"),
    # Filter
    ("kavos filtras", "filtr do kawy"), ("kavos filtro", "filtr do kawy"),
    ("filtras", "filtr"), ("filtro", "filtr"),
    # Coffee pot / moka pot
    ("kavinukas", "kawiarka"), ("kavinuko", "kawiarka"),
    # Baking tray
    ("kepimo skarda", "blacha do pieczenia"), ("kepimo skardos", "blacha do pieczenia"),
    ("kepimo forma", "forma do pieczenia"), ("kepimo", "do pieczenia"),
    # Solar
    ("saulės kolektorius", "kolektor słoneczny"), ("saules kolektorius", "kolektor słoneczny"),
    ("saulės baterija", "bateria słoneczna"), ("saules baterija", "bateria słoneczna"),
    ("saulės baterijų", "bateria słoneczna"), ("saules bateriju", "bateria słoneczna"),
    ("saulės energija", "energia słoneczna"), ("saulės", "słoneczny"), ("saules", "słoneczny"),
    # RAM
    ("operatyvinė atmintis", "pamięć RAM"), ("operatyvine atmintis", "pamięć RAM"),
    ("operatyvinė", "RAM"), ("operatyvine", "RAM"),
    # Stainless steel
    ("nerūdijantis plienas", "stal nierdzewna"), ("nerudijantis plienas", "stal nierdzewna"),
    ("nerūdijantis puodas", "garnek ze stali nierdzewnej"), ("nerudijantis puodas", "garnek ze stali nierdzewnej"),
    ("nerūdijantis", "nierdzewny"), ("nerudijantis", "nierdzewny"),
    # Smart (short form)
    ("ismanus", "inteligentny"),
    # Power supply unit
    ("maitinimo blokas", "zasilacz"), ("maitinimo bloko", "zasilacz"),
    # PC case
    ("kompiuterio dėklas", "obudowa PC"), ("kompiuterio deklas", "obudowa PC"),
    ("kompiuterio", "komputerowy"),
    # Chair types
    ("žaidimų kėdė", "fotel gamingowy"), ("zaidimu kede", "fotel gamingowy"),
    ("ofiso kėdė", "krzesło biurowe"), ("ofiso kede", "krzesło biurowe"),
    ("kėdė", "krzesło"), ("kedes", "krzesło"), ("kede", "krzesło"),
    # Office genitive
    ("ofiso", "biurowy"),
    # Scooter
    ("elektrinis motoroleris", "hulajnoga elektryczna"), ("elektrinis motorolerio", "hulajnoga elektryczna"),
    ("motoroleris", "skuter"), ("motorolerio", "skuter"),
    # Dispenser
    ("vandens dozatorius", "dystrybutor wody"), ("dozatorius", "dozownik"),
    ("dozatoriaus", "dozownik"),
    # Smoke / CO detector
    ("dūmų detektorius", "czujnik dymu"), ("dumu detektorius", "czujnik dymu"),
    ("anglies monoksido detektorius", "czujnik CO"),
    ("detektorius", "detektor"), ("detektoriaus", "detektor"),
    # Memory card
    ("atminties kortelė", "karta pamięci"), ("atminties korteles", "karta pamięci"),
    ("kortelė", "karta"), ("korteles", "karta"),
    # Watering can
    ("laistyklė", "konewka"), ("laistyklės", "konewka"),
    # Garden genitive
    ("sodo žarna", "wąż ogrodowy"), ("sodo zarna", "wąż ogrodowy"),
    ("sodo", "ogrodowy"),
    # Band saw
    ("juostinis pjūklas", "pilarka taśmowa"), ("juostinis pjuklas", "pilarka taśmowa"),
    ("juostinis", "taśmowy"), ("juostine", "taśmowy"),
    # Contact grill
    ("kontaktinis grilis", "grill kontaktowy"), ("kontaktinis grilio", "grill kontaktowy"),
    ("kontaktinis", "kontaktowy"), ("kontaktine", "kontaktowy"),
    # Wind generator
    ("vėjo generatorius", "generator wiatrowy"), ("vejo generatorius", "generator wiatrowy"),
    ("vėjo turbina", "turbina wiatrowa"), ("vejo", "wiatrowy"), ("vėjo", "wiatrowy"),
    # Air pump (oro siurblys)
    ("oro siurblys", "pompka do powietrza"), ("oro siurblio", "pompka do powietrza"),
    ("oro išpurškiklis", "odświeżacz powietrza"), ("oro ispurskiklis", "odświeżacz powietrza"),
    ("oro", "powietrze"),
    # Diffuser
    ("išpurškiklis", "dyfuzor"), ("ispurskiklis", "dyfuzor"),
    # Standing desk
    ("stovintis stalas", "biurko stojące"), ("stovinti stala", "biurko stojące"),
    ("stovintis", "stojący"), ("stovinti", "stojący"),
    # Portable adjective
    ("portativinis garsiakalbis", "przenośny głośnik"), ("portativinis", "przenośny"), ("portativine", "przenośny"),
    # Large adjective
    ("didelis", "duży"), ("didele", "duży"),
    # Compact adjective
    ("kompaktiškas", "kompaktowy"), ("kompaktiska", "kompaktowy"), ("kompaktiskas", "kompaktowy"),
    # Maker / machine for food
    ("ledų gamintuvas", "maszyna do lodów"), ("ledu gamintuvas", "maszyna do lodów"),
    ("jogurto gamintuvas", "jogurtownica"), ("jogurto gamintuve", "jogurtownica"),
    ("sūrio gamintuvas", "maszyna do sera"), ("surio gamintuvas", "maszyna do sera"),
    ("gamintuvas", "maszyna"), ("gamintuvo", "maszyna"),
    # Thermos
    ("termosas", "termos"), ("termoso", "termos"),
    # Pasta machine
    ("makaronų mašina", "maszynka do makaronu"), ("makaronu masina", "maszynka do makaronu"),
    # Pizza stone
    ("picos akmuo", "kamień do pizzy"), ("picos akmenuo", "kamień do pizzy"),
    ("picos", "pizza"),
    # Paper
    ("kepimo popierius", "papier do pieczenia"), ("kepimo popieriaus", "papier do pieczenia"),
    ("popierius", "papier"), ("popieriaus", "papier"),
    # Petrol powered
    ("benzininis generatorius", "generator benzynowy"), ("benzininis", "benzynowy"), ("benzinine", "benzynowy"),
    # Baby monitor
    ("kūdikio monitoriaus", "niania elektroniczna"), ("kudikio monitoriaus", "niania elektroniczna"),
    ("monitoriaus", "monitor"),
    # Video projector
    ("videoprojektorius", "projektor wideo"), ("videoprojekcija", "projekcja wideo"),
    # Multi-channel
    ("daugiakanalis", "wielokanałowy"), ("daugiakanalio", "wielokanałowy"),
    # Ice scraper
    ("ledo grandiklis", "skrobaczka do lodu"), ("ledo grandiklio", "skrobaczka do lodu"),
    ("grandiklis", "skrobaczka"), ("grandiklio", "skrobaczka"),
    # Mechanical (carpet sweeper)
    ("mechaniška šluota", "zamiatacz dywanów"), ("mechaniska slota", "zamiatacz dywanów"),
    ("mechaniška", "mechaniczny"), ("mechaniskas", "mechaniczny"), ("mechaniškas", "mechaniczny"),
    # Interactive screen
    ("interaktyvus ekranas", "interaktywny ekran"), ("interaktyvi", "interaktywny"),
    ("interaktyvus", "interaktywny"),
    # Lunch box
    ("dėžutė maistui", "lunchbox"), ("dezute maistui", "lunchbox"),
    ("dėžutė", "pojemnik"), ("dezute", "pojemnik"),
    # Ice cream
    ("ledų", "lodowy"), ("ledu", "lodowy"),
    # Yogurt genitive
    ("jogurto", "jogurtowy"),
    # Cheese genitive
    ("sūrio", "serowy"), ("surio", "serowy"),
    # Small adjective
    ("mažas", "mały"), ("maza", "mały"),
    # Titanium
    ("titanas", "tytan"), ("titanio", "tytan"),
    # Battery instrumental
    ("akumuliatoriumi", "akumulator"), ("akumuliatoriaus", "akumulator"),
    # Absolute adjective
    ("absoliutus", "Absolute"), ("absoliutine", "Absolute"),
    # High pressure
    ("aukšto slėgio", "wysokociśnieniowy"), ("auksto slegio", "wysokociśnieniowy"),
    ("slėgio", "ciśnienie"), ("slegio", "ciśnienie"),
    # Screwdriver
    ("akumuliatorinis atsuktuvas", "wkrętarka akumulatorowa"), ("akumuliatorinis atsuktuve", "wkrętarka akumulatorowa"),
    ("elektrinis atsuktuvas", "wkrętarka elektryczna"), ("elektrinis atsuktuve", "wkrętarka elektryczna"),
    ("atsuktuvas", "wkrętarka"), ("atsuktuvo", "wkrętarka"),
    # Car genitive
    ("automobilio kompresorius", "kompresor samochodowy"), ("automobilio kompresoriaus", "kompresor samochodowy"),
    ("automobilio siurblys", "odkurzacz samochodowy"), ("automobilio siurblio", "odkurzacz samochodowy"),
    ("automobilio", "samochodowy"),
    # Suitcase
    ("lagaminas", "walizka"), ("lagamino", "walizka"),
    # Christmas tree
    ("kalėdinė eglutė", "choinka"), ("kaledine eglute", "choinka"),
    ("eglutė", "choinka"), ("eglutes", "choinka"),
    ("kalėdinė", "świąteczny"), ("kaledine", "świąteczny"),
    # Pet supplies
    ("šunų guolis", "legowisko dla psa"), ("sunu guolis", "legowisko dla psa"),
    ("kačių draskyklė", "drapak dla kota"), ("kaciu draskykle", "drapak dla kota"),
    ("šunų", "dla psów"), ("sunu", "dla psów"),
    ("kačių", "dla kotów"), ("kaciu", "dla kotów"),
    # Hydraulic jack
    ("hidraulinis domkratas", "podnośnik hydrauliczny"), ("domkratas", "podnośnik"),
    ("domkrato", "podnośnik"),
    # E-book reader
    ("elektroninė knyga", "e-book"), ("elektronine knyga", "e-book"),
    ("elektroninė", "elektroniczny"), ("elektronine", "elektroniczny"),
    # Door lock
    ("durų užraktas", "zamek do drzwi"), ("duru uzraktas", "zamek do drzwi"),
    ("durų spyna", "zamek do drzwi"), ("duru spyna", "zamek do drzwi"),
    ("durų", "drzwiowy"), ("duru", "drzwiowy"),
    # Protein / collagen supplement
    ("baltymų produktas", "produkt białkowy"), ("baltymu produktas", "produkt białkowy"),
    ("baltymų", "białko"), ("baltymu", "białko"),
    ("kolagenas", "kolagen"), ("kolageno", "kolagen"),
    # v7.45 — Books
    ("programavimo knyga", "książka programistyczna"), ("vaikiskas knyga", "książka dla dzieci"),
    ("knygu rinkinys", "zestaw książek"), ("knygu rinkinio", "zestaw książek"),
    ("knyga", "książka"), ("knygos", "książka"), ("knygu", "ksiązek"),
    # Clothing
    ("vaiku striuke", "kurtka dziecięca"), ("ziemos striuke", "kurtka zimowa"),
    ("vasaros striuke", "kurtka letnia"), ("lietaus striuke", "kurtka przeciwdeszczowa"),
    ("striuke", "kurtka"), ("striuku", "kurtki"),
    ("megztinis", "sweter"), ("megztinio", "sweter"),
    ("vaiku suknele", "sukienka dziecięca"), ("suknele", "sukienka"), ("sukneles", "sukienki"),
    ("sportinis kostiumas", "dres sportowy"), ("kostiumas", "kostium"), ("kostiumo", "kostiumu"),
    ("vaiku pirstines", "rękawiczki dziecięce"), ("ziemos pirstines", "rękawiczki zimowe"),
    ("bokso pirstines", "rękawice bokserskie"),
    ("pirstines", "rękawiczki"), ("pirstiniu", "rękawiczek"),
    # Waffle maker
    ("vafline", "gofrownica"), ("vafliu", "gofrów"),
    # Outdoor / garden
    ("sodo pavesine", "pawilon ogrodowy"), ("pavesine", "pawilon"), ("pavesines", "pawilon"),
    ("vaiku supuokles", "huśtawka dla dzieci"), ("sodo supuokles", "huśtawka ogrodowa"),
    ("supuokles", "huśtawka"), ("supuokliu", "huśtawek"),
    # Furniture
    ("lauko baldai", "meble ogrodowe"), ("vaiku baldai", "meble dziecięce"),
    ("biuro baldai", "meble biurowe"), ("miegamojo baldai", "meble do sypialni"),
    ("baldai", "meble"), ("baldu", "mebli"),
    # Toy construction set / toy car
    ("zaidiminis konstruktorius", "klocki konstrukcyjne"),
    ("konstruktorius", "zestaw konstrukcyjny"), ("konstruktoriaus", "zestawu konstrukcyjnego"),
    ("zaisline masinyke", "samochodzik zabawka"), ("masinyke", "samochodzik"), ("masiniu", "samochodzik"),
    # v7.44 — Vitamins / supplements
    ("vitaminu kompleksas", "kompleks witamin"), ("vitaminu komplekse", "kompleks witamin"),
    ("vitaminu papildas", "suplement witaminowy"), ("vitaminu papildo", "suplement witaminowy"),
    ("vitaminas", "witamina"), ("vitaminu", "witamina"), ("vitaminai", "witaminy"),
    ("magnio gele", "żel magnezowy"), ("magnio tabletes", "tabletki magnezowe"),
    ("magnio", "magnez"), ("magnis", "magnez"),
    ("kreatinas", "kreatyna"), ("kreatino", "kreatyny"),
    # Shoes / footwear
    ("sportiniai batai", "buty sportowe"), ("sportbaciai", "buty sportowe"), ("sportbacio", "buty sportowe"),
    ("vaiku batai", "buty dziecięce"), ("vaiku batu", "buty dziecięce"),
    ("kedai", "trampki"),
    ("batai", "buty"), ("batu", "buty"),
    # Doll
    ("lele Barbie", "lalka Barbie"), ("leles Barbie", "lalka Barbie"),
    ("lele", "lalka"), ("leles", "lalka"),
    # Kitchen knife
    ("peiliu blokas", "blok do noży"), ("peilio bloko", "blok do noży"),
    ("virtuvinis peilis", "nóż kuchenny"), ("keptuves peilis", "łopatka do patelni"),
    ("peilis", "nóż"), ("peilio", "noża"), ("peiliai", "noże"),
    # Scissors
    ("sodo zirkles", "nożyce ogrodowe"), ("sodo zirkliu", "nożyce ogrodowe"),
    ("zirkles", "nożyczki"), ("zirkliu", "nożyczek"),
    # Food slicer
    ("pjaustytuvas", "krajalnica"), ("pjaustytuvo", "krajalnica"),
    # Car tyres
    ("automobilio padangos", "opony samochodowe"), ("automobilio padanga", "opona samochodowa"),
    ("ziemos padangos", "opony zimowe"), ("vasaros padangos", "opony letnie"),
    ("padangos", "opony"), ("padanga", "opona"),
    # Lubricant / engine oil
    ("variklio tepalas", "olej silnikowy"), ("variklio tepalo", "olej silnikowy"),
    ("tepalas", "olej"), ("tepalo", "olej"),
    # Tape measure
    ("matavimo juosta", "miara taśmowa"), ("matavimo juostos", "miara taśmowa"),
    ("matavimo", "pomiarowy"),
    # v7.43 — Music instruments (same-PL words included to prevent Claude fallback)
    ("elektrinis pianinas", "pianino elektryczne"), ("elektrine pianinas", "pianino elektryczne"),
    ("elektrinis sintezatorius", "syntezator elektryczny"),
    ("gitara", "gitara"), ("gitaros", "gitara"),
    ("pianinas", "pianino"), ("pianino", "pianino"),
    ("sintezatorius", "syntezator"), ("sintezatoriaus", "syntezator"),
    ("bugnas", "perkusja"), ("bugnu", "perkusja"),
    ("smuikas", "skrzypce"), ("smiko", "skrzypce"),
    ("fleita", "flet"), ("fleitos", "flet"),
    # Sports / outdoor
    ("vaizdo registratorius", "wideorejestrator"), ("vaizdo registratoriaus", "wideorejestrator"),
    ("registratorius", "wideorejestrator"), ("registratoriaus", "wideorejestrator"),
    ("batutas", "trampolina"), ("batuto", "trampolina"),
    ("slidu", "narty"),
    ("paciuzos", "łyżwy"), ("paciuzu", "łyżwy"),
    ("meskere", "wędka"), ("meskeriu", "wędka"),
    ("zvejybos", "wędkarstwo"), ("zvejyba", "wędkarstwo"),
    ("plaukimo akiniai", "okulary pływackie"), ("plaukimo kostiumelis", "strój kąpielowy"),
    ("plaukimo", "pływacki"),
    # Milk frother
    ("pienu putuke", "spieniacz do mleka"), ("pienu putuku", "spieniacz do mleka"),
    ("pienuke", "spieniacz do mleka"), ("pienuku", "spieniacz do mleka"),
    # Furniture / home textiles
    ("dvigule lova", "łóżko dwuosobowe"), ("viengule lova", "łóżko jednoosobowe"),
    ("lovos ramas", "rama łóżka"), ("lovos rama", "rama łóżka"),
    ("lova", "łóżko"), ("lovos", "łóżko"),
    ("drabuzine spinta", "szafa ubraniowa"), ("spinta", "szafa"), ("spintos", "szafa"),
    ("kilimas", "dywan"), ("kilimo", "dywan"),
    # v7.46 — Perfume / fragrance / candle
    ("aromatine zvake", "świeca zapachowa"), ("aromatines zvakes", "świeca zapachowa"),
    ("zvake", "świeca"), ("zvakiu", "świece"),
    ("foto ramelis", "ramka na zdjęcia"), ("foto ramelio", "ramka na zdjęcia"),
    ("ramelis", "ramka"), ("ramelio", "ramka"),
    ("kvepalai", "perfumy"), ("kvepalu", "perfumy"),
    ("parfumas", "perfumy"), ("parfumo", "perfumy"),
    ("sampunas", "szampon"), ("sampuno", "szampon"),
    # Tennis / racket sports
    ("stalo tenisas", "tenis stołowy"), ("stalo teniso", "tenis stołowy"),
    ("stalo teniso rakete", "rakietka do tenisa stołowego"),
    ("teniso rakete", "rakieta tenisowa"), ("teniso kamuolys", "piłka tenisowa"),
    ("teniso striuke", "koszulka tenisowa"), ("teniso bateliai", "buty tenisowe"),
    ("tenisas", "tenis"), ("teniso", "tenisowy"),
    ("badmintono rakete", "rakieta badmintonowa"), ("badmintono kamuolys", "lotka"),
    ("badmintonas", "badminton"), ("badmintono", "badmintonowy"),
    # Football / basketball
    ("futbolo kamuolys", "piłka nożna"), ("futbolo vartai", "bramka piłkarska"),
    ("futbolo bateliai", "buty piłkarskie"), ("futbolas", "piłka nożna"), ("futbolo", "piłkarski"),
    ("krepsinio kamuolys", "piłka do koszykówki"), ("krepsinio krepselis", "kosz do koszykówki"),
    ("krepsis", "koszykówka"), ("krepsinio", "koszykarski"),
    # Snow / skate sports
    ("snieglenciu rinkinys", "zestaw snowboardowy"),
    ("snieglente", "deska snowboardowa"), ("snieglenciu", "snowboard"),
    ("riedlentes riedmenys", "trucks do deskorolki"),
    ("riedlente", "deskorolka"), ("riedlenciu", "deskorolki"),
    # Home textiles / bedroom
    ("ortopedine pagalve", "poduszka ortopedyczna"), ("kuno pagalve", "poduszka ciążowa"),
    ("miego pagalve", "poduszka do spania"),
    ("pagalve", "poduszka"), ("pagalviu", "poduszek"),
    ("patalynes komplektas", "komplet pościeli"), ("patalyne", "pościel"), ("patalynes", "pościel"),
    # Thermos mug
    ("termosinis puodelis", "kubek termiczny"), ("termo puodelis", "kubek termiczny"),
    ("termopuodelis", "kubek termiczny"), ("termopuodelio", "kubek termiczny"),
    # v7.52 — Word-order fix for sofa kampine + misc
    ("sofa kampine", "sofa narożna"), ("sofa miegama", "sofa rozkładana"),
    ("kampine", "narożna"),
    ("hamakas", "hamak"), ("hamaku", "hamaka"),
    ("ausinukas", "słuchawki douszne"), ("ausinuko", "słuchawki douszne"),
    ("menteliklis", "drążek do podciągania"), ("menteliklio", "drążka do podciągania"),
    ("stanga", "sztanga"), ("stangos", "sztanga"),
    ("preso suoliukas", "ławka do wyciskania"), ("suoliukas", "ławka treningowa"), ("suoliuko", "ławki treningowej"),
    ("irklente", "deska SUP"), ("irklentes", "deski SUP"),
    ("stovyklavimo kede", "krzesło campingowe"), ("stovyklavimo stalas", "stół campingowy"),
    ("stovyklavimo virykle", "kuchenka campingowa"), ("stovyklavimo miegmaišis", "śpiwór campingowy"),
    ("stovyklavimo", "campingowy"),
    ("aminorugsciai", "aminokwasy"), ("aminoru", "aminokwasów"),
    # v7.51 — Window treatments
    ("langu uzdanga", "firanka okienna"), ("interjero uzdanga", "zasłona wewnętrzna"),
    ("uzdanga", "zasłona"), ("uzdangu", "zasłony"),
    ("uzuolaida", "zasłona"), ("uzuolaidų", "zasłony"),
    ("tamsinamoji rolete", "roletka zaciemniająca"), ("rolete", "roleta"), ("roletu", "rolety"),
    ("zaluzija", "żaluzja"), ("zaluziju", "żaluzje"),
    # v7.51 — Bedding addition
    ("flanelinė paklodė", "flanelowe prześcieradło"), ("paklode", "prześcieradło"), ("paklodziu", "prześcieradła"),
    ("megztas apklotas", "koc dziergany"), ("apklotas", "koc"), ("apklotu", "koce"),
    # v7.51 — Water sports
    ("vaiku baseinas", "basen dziecięcy"), ("baseinas", "basen"), ("baseino", "basenu"),
    ("baidarele", "kajak"), ("baidareles", "kajaki"),
    ("kanoja", "kajak"), ("kanojos", "kajaki"),
    ("irklai", "wiosło"), ("irklu", "wiosła"),
    # v7.51 — Cables / electrical
    ("kabelis", "kabel"), ("kabelio", "kabla"),
    ("laidas", "kabel"), ("laido", "kabla"),
    ("tinklines", "listwa zasilająca"), ("tinkliniu", "listwy zasilające"),
    # v7.51 — Arts / crafts
    ("plastilinas", "plastelina"), ("plastilino", "plasteliny"),
    # v7.51 — Flooring / construction
    ("grindys", "podłoga"), ("grindylentu", "deski podłogowe"),
    ("plytelis", "płytka ceramiczna"), ("plyteliu", "płytki ceramiczne"),
    # v7.50 — Automotive accessories
    ("automobilio radijas", "radio samochodowe"), ("automagnetola", "radio samochodowe"), ("automagnetolos", "radio samochodowe"),
    ("automobilio vairas", "kierownica"), ("sportinis vairas", "kierownica sportowa"),
    ("vairas", "kierownica"), ("vairo", "kierownicy"),
    ("automobilio ratai", "felgi samochodowe"), ("ratu rinkinys", "zestaw felg"),
    ("ratai", "felgi"), ("ratu", "felgi"),
    # v7.50 — Home improvement / flooring
    ("sienu dazai", "farba do ścian"), ("lauko dazai", "farba zewnętrzna"), ("medzio dazai", "farba do drewna"),
    ("dazai", "farba"), ("dazo", "farby"),
    ("tapetai", "tapeta"), ("tapetu", "tapety"),
    ("laminatas", "panele podłogowe"), ("laminato", "panele podłogowe"),
    ("parketas", "parkiet"), ("parketo", "parkietu"),
    # v7.50 — Music instruments
    ("akordeonas", "akordeon"), ("akordeono", "akordeon"),
    ("trimitas", "trąbka"), ("trimito", "trąbki"),
    ("saksofonas", "saksofon"), ("saksofono", "saksofonu"),
    # v7.50 — Office / school
    ("pieštukas", "ołówek"), ("piestukas", "ołówek"), ("piestuko", "ołówka"),
    ("flomasteris", "flamaster"), ("flomasteri", "flamastry"),
    # v7.50 — Garden
    ("sodo fontanas", "fontanna ogrodowa"), ("fontanas", "fontanna"), ("fontano", "fontanny"),
    # v7.49 — Beauty / bathroom / pet / hunting / protection
    ("drekinamasis kremas", "krem nawilżający"), ("veido kremas", "krem do twarzy"),
    ("kuno kremas", "krem do ciała"), ("ranku kremas", "krem do rąk"),
    ("kremas", "krem"), ("kremo", "kremu"),
    ("dezodorantas", "dezodorant"), ("dezodoranto", "dezodoranta"),
    ("losjonas", "balsam"), ("losjono", "balsamu"),
    ("vonios kabina", "kabina prysznicowa"), ("vonios kubas", "wanna z hydromasażem"),
    ("vonia", "wanna"), ("vonios", "łazienkowy"),
    ("vonios rankslostis", "ręcznik kąpielowy"), ("vaiku rankslostis", "ręcznik dziecięcy"),
    ("rankslostis", "ręcznik"), ("ranklosciu", "ręczniki"),
    ("sunu maistas", "karma dla psa"), ("sunu lova", "legowisko dla psa"), ("sunu pavadeli", "smycz"),
    ("kaciu maistas", "karma dla kota"), ("kaciu kraikes dezute", "kuweta"),
    ("katinas", "kot"), ("katino", "kota"),
    ("augintinis", "zwierzak"), ("augintinio", "zwierzaka"),
    ("medziokles kuprine", "plecak myśliwski"),
    ("medziokle", "myślistwo"), ("medziokles", "myśliwski"),
    ("sliauztukai", "nakolanniki"), ("sliauztukas", "nakolannik"),
    # v7.48 — Bags / accessories / jewelry
    ("kuprine su ratukais", "plecak na kółkach"), ("vaiku kuprine", "plecak dziecięcy"),
    ("kuprine", "plecak"), ("kuprines", "plecak"),
    ("odine rankine", "torebka skórzana"), ("rankine", "torebka"), ("rankines", "torebki"),
    ("odinis dirzas", "pasek skórzany"), ("sportinis dirzas", "pasek sportowy"),
    ("dirzas", "pasek"), ("dirzo", "paska"),
    ("piniginė", "portfel"), ("pinigines", "portfele"),
    ("papuošalai", "biżuteria"), ("papuosalu", "biżuteria"),
    ("ausų karoliai", "kolczyki"), ("karoliai", "naszyjnik"), ("karoliu", "naszyjniki"),
    ("auskarai", "kolczyki"), ("auskariu", "kolczyki"),
    ("portfelis", "aktówka"), ("portfelio", "aktówki"),
    ("ziedas", "pierścionek"), ("ziedo", "pierścionka"),
    # v7.48 — Kitchen / home
    ("kavos puodelis", "filiżanka do kawy"), ("puodelis", "kubek"), ("puodelio", "kubka"),
    ("sriubos dubuo", "miska do zupy"), ("dubuo", "miska"), ("dubens", "miski"),
    ("vazonas", "doniczka"), ("vazono", "doniczki"),
    # v7.48 — Miscellaneous
    ("automobilio tentas", "plandeka na samochód"), ("lauko tentas", "plandeka campingowa"),
    ("tentas", "plandeka"), ("tento", "plandeka"),
    ("siuvimo mašina", "maszyna do szycia"), ("siuvimo", "do szycia"),
    ("zaislinis automobilis", "samochodzik zabawka"), ("zaislinis", "zabawkowy"),
    # v7.47 — Furniture
    ("kampine sofa", "sofa narożna"), ("miegama sofa", "sofa rozkładana"),
    ("sofa", "sofa"), ("sofos", "sofa"),
    ("fotelis", "fotel"), ("fotelio", "fotela"),
    ("knygu lentyna", "regał na książki"), ("sodo lentyna", "regał ogrodowy"),
    ("lentyna", "półka"), ("lentynu", "półki"),
    ("komoda", "komoda"), ("komodu", "komoda"),
    # v7.47 — Clothing
    ("ziemos kepure", "czapka zimowa"), ("vaiku kepure", "czapka dziecięca"),
    ("kepure", "czapka"), ("kepures", "czapki"),
    ("salikas", "szalik"), ("saliko", "szalik"),
    ("sportines kelnes", "spodnie sportowe"), ("ziemos kelnes", "spodnie zimowe"),
    ("kelnes", "spodnie"), ("kelniu", "spodnie"),
    ("marskiniai", "koszula"), ("marskiniu", "koszule"),
    ("dzinsai", "jeansy"), ("dzinsu", "jeansy"),
    ("maudymosi kostiumelis", "strój kąpielowy"), ("maudymosi kelnaites", "kąpielówki"),
    ("maudymosi", "kąpielowy"),
    ("kostiumelis", "kostiumek"),
    # v7.47 — Boxing / roller skates / sled
    ("bokso maišas", "worek treningowy"), ("bokso pirstines", "rękawice bokserskie"),
    ("boksas", "boks"), ("bokso", "bokserski"),
    ("riedutis", "rolki"), ("rieduciu", "rolki"),
    ("roges", "sanki"), ("rogiu", "sanki"),
    # v7.47 — Water bottle / diapers / yoga
    ("sporto gertuve", "bidon sportowy"), ("vaiku gertuve", "bidon dla dzieci"),
    ("gertuve", "bidon"), ("gertuviu", "bidon"),
    ("sauskelnes", "pieluchy"), ("sauskelnems", "pieluchy"),
    ("jogos kilimelis", "mata do jogi"), ("jogos blokelis", "blok do jogi"),
    ("jogos", "joga"),
], key=lambda t: -len(t[0]))


def _static_translate(query: str, target_lang: str) -> str | None:
    """Replace LT category words with target-language equivalents. Free and instant.
    Returns None if no mapping matched (caller should fall through to Claude).
    Returns the translated string (possibly same as normalized input for same-language words)
    when at least one mapping matched — this avoids unnecessary Claude calls for words like
    'gitara' that are valid Polish as-is.
    Normalizes LT diacritics first (ą→a, č→c, etc.) so typed-without-accents queries work.
    Uses whole-word matching to prevent shorter rules re-matching inside already-translated text
    (e.g. 'kino' must not match inside 'Heimkino' after 'kino sistema'→'Heimkino')."""
    mapping = _LT_DE if target_lang == "de" else _LT_PL
    result = _norm_lt(query)
    q_low = result.lower()
    matched = False
    for lt_word, target_word in mapping:
        lt_norm = _norm_lt(lt_word)
        pat = r'(?<!\w)' + re.escape(lt_norm) + r'(?!\w)'
        if not re.search(pat, q_low):
            continue
        matched = True
        result = re.sub(pat, target_word, result, flags=re.IGNORECASE)
        q_low = result.lower()
    return result if matched else None


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
    if static_result is not None:
        # Static matched at least one word — use result (even if identical, e.g. gitara→gitara in PL)
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


def rule_based_ai_analyze(query: str, results: list, price_history: dict = None, language: str = "") -> dict:
    # Explicit language param from frontend takes priority over auto-detect
    lang = (language or "").strip().lower()
    if lang not in ("lt", "en", "ru", "pl", "de"):
        is_lt = _is_lt_query(query) or any(ord(c) > 127 for c in query[:20])
        q_low = query.lower()
        is_de = any(c in q_low for c in ("ä", "ö", "ü", "ß")) or any(w in q_low for w in ("waschmaschine", "kühlschrank", "fernseher", "drucker"))
        is_pl = any(c in q_low for c in ("ę", "ó", "ń")) or any(w in q_low for w in ("pralka", "odkurzacz", "lodówka", "golarka", "ekspres"))
        lang = "lt" if is_lt else ("de" if is_de else ("pl" if is_pl else "en"))

    _L = {
        "lt": {"no_price": "Kainų nerasta.", "try_specific": "Pabandykite tikslesnį pavadinimą.", "refine": "Patikslinkite paiešką.", "one_seller": "Rastas tik 1 pardavėjas — palyginti negalime.", "cheap_pct": "Pigiausia kaina yra {pct:.0f}% žemiau brangiausios.", "near_avg": "Geriausia kaina artima rinkos vidurkiui.", "normal": "Kaina atrodo normali.", "rec": "Geriausia rasta kaina €{pmin:.2f}. Palyginkite pristatymą ir pardavėją prieš pirkdami.", "summary": "Goody rado {n} kainų. Pigiausia: €{pmin:.2f}, vidurkis: €{pavg:.2f}.", "at_hist_low": "Kaina šiuo metu istoriniame minimume — geras metas pirkti.", "above_hist_avg": "Kaina viršija 30 dienų vidurkį — galbūt verta palaukti."},
        "de": {"no_price": "Keine Preise gefunden.", "try_specific": "Bitte genaueren Produktnamen eingeben.", "refine": "Suche verfeinern.", "one_seller": "Nur 1 Händler gefunden — kein Preisvergleich möglich.", "cheap_pct": "Das günstigste Angebot liegt {pct:.0f}% unter dem teuersten.", "near_avg": "Der beste Preis liegt nahe am Marktdurchschnitt.", "normal": "Der Preis sieht angemessen aus.", "rec": "Bester gefundener Preis €{pmin:.2f}. Versandkosten und Händler vergleichen.", "summary": "Goody fand {n} Preise. Günstigster: €{pmin:.2f}, Durchschnitt: €{pavg:.2f}.", "at_hist_low": "Preis aktuell auf historischem Tief — guter Kaufzeitpunkt.", "above_hist_avg": "Preis über dem 30-Tage-Durchschnitt — abwarten könnte sich lohnen."},
        "pl": {"no_price": "Nie znaleziono cen.", "try_specific": "Wpisz dokładniejszą nazwę produktu.", "refine": "Doprecyzuj wyszukiwanie.", "one_seller": "Znaleziono tylko 1 sprzedawcę — porównanie niemożliwe.", "cheap_pct": "Najtańsza oferta jest {pct:.0f}% poniżej najdroższej.", "near_avg": "Najlepsza cena bliska średniej rynkowej.", "normal": "Cena wygląda normalnie.", "rec": "Najlepsza znaleziona cena €{pmin:.2f}. Porównaj dostawę i sprzedawcę.", "summary": "Goody znalazło {n} cen. Najtańsza: €{pmin:.2f}, średnia: €{pavg:.2f}.", "at_hist_low": "Cena aktualnie na historycznym minimum — dobry moment na zakup.", "above_hist_avg": "Cena powyżej 30-dniowej średniej — warto poczekać."},
        "ru": {"no_price": "Цены не найдены.", "try_specific": "Попробуйте более точное название.", "refine": "Уточните поиск.", "one_seller": "Найден только 1 продавец — сравнение невозможно.", "cheap_pct": "Самое дешёвое предложение на {pct:.0f}% ниже самого дорогого.", "near_avg": "Лучшая цена близка к рыночной средней.", "normal": "Цена выглядит нормальной.", "rec": "Лучшая найденная цена €{pmin:.2f}. Сравните доставку и продавца.", "summary": "Goody нашёл {n} цен. Самая дешёвая: €{pmin:.2f}, средняя: €{pavg:.2f}.", "at_hist_low": "Цена сейчас на историческом минимуме — хорошее время для покупки.", "above_hist_avg": "Цена выше 30-дневного среднего — возможно стоит подождать."},
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

    _vl = {
        "lt": {"BUY": "Pirkti dabar", "WAIT": "Palaukite", "OK": "Normali"},
        "de": {"BUY": "Jetzt kaufen", "WAIT": "Abwarten", "OK": "Normal"},
        "pl": {"BUY": "Kup teraz", "WAIT": "Poczekaj", "OK": "Normalna"},
        "ru": {"BUY": "Покупать", "WAIT": "Подождать", "OK": "Нормально"},
        "en": {"BUY": "Buy now", "WAIT": "Wait", "OK": "Normal"},
    }.get(lang, {"BUY": "Buy now", "WAIT": "Wait", "OK": "Normal"})

    if len(prices) == 1:
        verdict = "OK"
        label = _vl["OK"]
        reason = L["one_seller"]
    elif hist_low and hist_count >= 2 and price_min <= hist_low * 1.05:
        verdict = "BUY"
        label = _vl["BUY"]
        reason = L["at_hist_low"]
    elif hist_avg and hist_count >= 2 and price_min > hist_avg * 1.10:
        verdict = "WAIT"
        label = _vl["WAIT"]
        reason = L["above_hist_avg"]
    elif spread_pct >= 20:
        verdict = "BUY"
        label = _vl["BUY"]
        reason = L["cheap_pct"].format(pct=spread_pct)
    elif price_min > price_avg * 0.97:
        verdict = "WAIT"
        label = _vl["WAIT"]
        reason = L["near_avg"]
    else:
        verdict = "OK"
        label = _vl["OK"]
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


_LANG_NAME_MAP = {
    "lt": "Lithuanian", "en": "English", "ru": "Russian",
    "pl": "Polish", "de": "German",
}


def build_ai_prompt(query: str, results: list, price_history: dict = None, language: str = "") -> str:
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

    _lang_code = (language or "").strip().lower()
    if _lang_code in _LANG_NAME_MAP:
        _ai_lang = _LANG_NAME_MAP[_lang_code]
    else:
        _ai_lang = "Lithuanian"

    return f"""CRITICAL: Respond ONLY in {_ai_lang}. The entire response must be in {_ai_lang}, no exceptions.

Goody price comparison coach. Analyze and return JSON only.
Product: {query}
Shops: {shops_summary}
Price range: €{p_min:.2f}–€{p_max:.2f} ({len(prices)} shops, {spread_pct}% spread).{hist_line}

Rules: use only provided data. Be concise. ALL text fields MUST be written in {_ai_lang} ONLY. Do NOT mix languages. Do NOT use English if the target language is not English.

Return ONLY valid JSON:
{{"verdict":"BUY|WAIT|OK","verdict_label":"1-3 words in {_ai_lang}","verdict_reason":"one sentence in {_ai_lang}","ai_summary":"1-2 sentences in {_ai_lang}","alternative":"cheaper alternative product name if clearly overpriced else empty string","buy_recommendation":"1-2 sentences in {_ai_lang}","price_forecast":"one sentence in {_ai_lang} or empty string"}}"""


def openai_analyze(query: str, results: list, price_history: dict = None, language: str = "") -> dict:
    if not OPENAI_API_KEY or OpenAI is None or not results:
        return rule_based_ai_analyze(query, results, price_history, language)

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        prompt = build_ai_prompt(query, results, price_history, language)

        _lang_code_oa = (language or "").strip().lower()
        _sys_lang_oa = _LANG_NAME_MAP.get(_lang_code_oa, "Lithuanian")
        resp = client.chat.completions.create(
            model=AI_MODEL_OPENAI,
            messages=[
                {
                    "role": "system",
                    "content": f"You are Goody's AI deal analyst. CRITICAL: Respond ONLY in {_sys_lang_oa}. Return strict JSON only."
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
        return rule_based_ai_analyze(query, results, price_history, language)


def claude_analyze(query: str, results: list, price_history: dict = None, language: str = "") -> dict:
    if not ANTHROPIC_API_KEY or not results:
        return rule_based_ai_analyze(query, results, price_history, language)

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        prompt = build_ai_prompt(query, results, price_history, language)

        _lang_code_cl = (language or "").strip().lower()
        _sys_lang_cl = _LANG_NAME_MAP.get(_lang_code_cl, "Lithuanian")
        resp = client.messages.create(
            model=AI_MODEL_CLAUDE,
            max_tokens=AI_MAX_TOKENS,
            system=f"You are Goody's AI deal analyst. CRITICAL: Respond ONLY in {_sys_lang_cl}. Return strict JSON only.",
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
        return rule_based_ai_analyze(query, results, price_history, language)


def analyze_deal_with_ai(query: str, results: list, price_history: dict = None, language: str = "") -> dict:
    # Rule-based (free) when too few shops; paid AI when 2+ shops with meaningful spread
    if not results:
        return rule_based_ai_analyze(query, results, price_history, language)

    prices = [r.get("price", 0) for r in results if r.get("price", 0) > 0]
    if len(prices) < 2:   # need at least 2 shops to compare
        return rule_based_ai_analyze(query, results, price_history, language)

    price_max = max(prices)
    spread_pct = ((price_max - min(prices)) / price_max * 100) if price_max else 0
    if spread_pct < 5:    # prices are within 5% — not interesting enough for AI
        return rule_based_ai_analyze(query, results, price_history, language)

    if AI_PROVIDER == "openai":
        return openai_analyze(query, results, price_history, language)

    if AI_PROVIDER == "claude":
        return claude_analyze(query, results, price_history, language)

    return rule_based_ai_analyze(query, results, price_history, language)


def validate_results_with_ai(query: str, results: list, language: str = "lt") -> list:
    """AI validates results, filtering accessories/parts. Runs when price spread >= 3x."""
    if not results or len(results) <= 1 or not ANTHROPIC_API_KEY:
        return results
    prices = [r.get("price", 0) for r in results if r.get("price", 0) > 0]
    if len(prices) < 2 or max(prices) / min(prices) < 3:
        return results  # No suspicious spread — skip AI call (save tokens)
    try:
        items = "\n".join(
            f"{i+1}. {r.get('product_title','')[:90]} — €{r.get('price',0):.2f} ({r.get('shop','')})"
            for i, r in enumerate(results[:8])
        )
        prompt = (
            f'User searched for: "{query}"\n\nSearch results:\n{items}\n\n'
            "CRITICAL TASK: Identify which results are the ACTUAL searched product vs accessories/parts/filters.\n"
            "KEY RULE: If a result is DRAMATICALLY cheaper than most others (e.g. €20 when others are €500-800), "
            "it is almost certainly an accessory, filter, brush, battery, or replacement part — mark match:false.\n"
            "Filter out: accessories, filters, nozzles, brushes, batteries, replacement parts, "
            "items 'for [brand]', 'compatible with', cleaning kits, bags, chargers.\n"
            "Keep: items that are the COMPLETE product the user searched for.\n"
            "When in doubt about a suspiciously cheap item — mark match:false.\n"
            'Return JSON only: [{"index":1,"match":true},{"index":2,"match":false},...]'
        )
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        resp = client.messages.create(
            model=AI_MODEL_CLAUDE,
            max_tokens=300,
            system="You are a product classifier. When price is dramatically lower than other results, assume accessory. Return strict JSON array only.",
            messages=[{"role": "user", "content": prompt}]
        )
        text = "".join(b.text for b in resp.content if hasattr(b, "text")).strip()
        text = text.replace("```json", "").replace("```", "").strip()
        jm = re.search(r'\[.*\]', text, re.DOTALL)
        if not jm:
            return results
        validation = json.loads(jm.group(0))
        _warn = {
            "lt": "Galimai detalė ar priedas, ne pats produktas — patikrink prieš pirkdamas",
            "en": "Possibly accessory/part, not main product — verify before buying",
            "ru": "Возможно аксессуар или деталь, а не основной продукт",
            "pl": "Możliwe akcesorium lub część, nie główny produkt — sprawdź",
            "de": "Möglicherweise Zubehör oder Teil, nicht das Hauptprodukt",
        }.get(language, "Possibly accessory/part — verify before buying")
        validated = []
        for v in validation:
            idx = int(v.get("index", 0)) - 1
            if 0 <= idx < len(results):
                if v.get("match", True):
                    validated.append(results[idx])
                else:
                    results[idx]["ai_filtered"] = True
                    results[idx].setdefault("match_warning", _warn)
        print(f"[validate_results_with_ai] '{query}': {len(validated)}/{len(results[:8])} matched")
        # Only return validated if we kept at least 1 result; otherwise fall back
        return validated if validated else results
    except Exception as e:
        print(f"[validate_results_with_ai] {e}")
        return results


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


def post_process(results: list, query: str, ai_data: dict = None, price_history: dict = None,
                 language: str = "lt") -> dict:
    # Filter relevance BEFORE dedup: keeps cheapest relevant result per shop, not cheapest overall
    results = [r for r in results if r.get("price", 0) > 0]
    filtered = [r for r in results if is_relevant_result(query, r.get("product_title", ""))]
    if filtered:
        results = filtered
    elif re.findall(r'\b[a-z]*\d+[a-z0-9-]*\b', query.lower()):
        results = []  # model-specific query: no exact match → show nothing rather than wrong product
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

    # ── Step 1: Price sanity check — flag outlier-cheap results (likely accessories) ──
    all_prices = [r["price"] for r in results]
    # Median: for 2 items [20, 800] → median = 800 (index 1). €20 < 30% of €800 = €240 → flagged.
    _price_median = sorted(all_prices)[len(all_prices) // 2] if all_prices else 0
    _outlier_warn = {
        "lt": "Galimai detalė ar priedas, ne pats produktas — patikrink prieš pirkdamas",
        "en": "Possibly accessory/part, not the main product — verify before buying",
        "ru": "Возможно аксессуар или деталь, а не основной продукт — проверьте",
        "pl": "Możliwe akcesorium lub część, nie główny produkt — sprawdź przed zakupem",
        "de": "Möglicherweise Zubehör oder Teil, nicht das Hauptprodukt — bitte prüfen",
    }.get(language, "Possibly accessory/part — verify before buying")
    if len(all_prices) >= 2 and _price_median > 0:  # >= 2 catches the 2-item [€20, €800] case
        for r in results:
            if r["price"] < _price_median * 0.30:
                r["is_suspicious"] = True
                r.setdefault("match_warning", _outlier_warn)

    # ── Step 2: Compute reliable price_min/max from non-flagged results ──
    reliable = [r for r in results if not r.get("is_suspicious") and not r.get("ai_filtered")]
    if not reliable:
        reliable = results  # fallback: all results if everything flagged

    prices = [r["price"] for r in reliable]
    price_min = min(prices)
    price_max = max(prices)  # only reliable prices for honest savings calculation
    price_avg = round(sum(prices) / len(prices), 2)

    # Mark cheapest from reliable set
    reliable[0]["is_cheapest"] = True

    rated = [r for r in reliable if r.get("rating", 0) > 0]
    if rated:
        max(rated, key=lambda r: r.get("rating", 0))["is_top_rated"] = True

    reliable[
        max(range(len(reliable)), key=lambda i: reliable[i].get("deal_score", 0))
    ]["is_best_value"] = True

    ai = ai_data or {}
    q_low2 = query.lower()
    _is_lt2 = _is_lt_query(query) or any(ord(c) > 127 for c in query[:20])
    _is_de2 = any(c in q_low2 for c in ("ä", "ö", "ü", "ß")) or any(w in q_low2 for w in ("waschmaschine", "kühlschrank", "fernseher"))
    _is_pl2 = any(c in q_low2 for c in ("ę", "ó", "ń")) or any(w in q_low2 for w in ("pralka", "odkurzacz", "lodówka"))
    _lang2 = "lt" if _is_lt2 else ("de" if _is_de2 else ("pl" if _is_pl2 else "en"))

    # Honest messaging when only 1 reliable result
    _reliable_count = len(reliable)
    _one_result_note = {
        "lt": f"Radome tik {_reliable_count} patikimą pasiūlymą.",
        "en": f"Found only {_reliable_count} verified offer(s).",
        "ru": f"Найдено только {_reliable_count} проверенное предложение.",
        "pl": f"Znaleziono tylko {_reliable_count} zweryfikowaną ofertę.",
        "de": f"Nur {_reliable_count} geprüftes Angebot gefunden.",
    }.get(language, f"Only {_reliable_count} verified offer(s) found.")

    _best_price_fallback = {
        "lt": f"Geriausia rasta kaina €{price_min:.2f}. Palyginkite pristatymą ir pardavėją.",
        "de": f"Bester gefundener Preis €{price_min:.2f}. Versandkosten und Händler vergleichen.",
        "pl": f"Najlepsza znaleziona cena €{price_min:.2f}. Porównaj dostawę i sprzedawcę.",
        "en": f"Best price found: €{price_min:.2f}. Compare delivery and seller before buying.",
    }[_lang2]
    if _reliable_count == 1:
        _best_price_fallback = _one_result_note + " " + _best_price_fallback

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
        "reliable_count": _reliable_count,
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
    language = (data.get("language") or "").strip().lower()
    if language not in ("lt", "en", "ru", "pl", "de"):
        language = "lt"

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

    cache_key = hashlib.md5(f"v64:{query.lower()}:{language}".encode()).hexdigest()
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

    # AI validation: filter out accessories/parts before deal analysis
    validated_results = validate_results_with_ai(query, deduped_for_ai, language)
    _t_after_validation = time.time()

    ai_data = analyze_deal_with_ai(query, validated_results, price_history, language)
    _t_after_ai = time.time()
    result = post_process(validated_results, query, ai_data, price_history, language=language)
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
    language = (data.get("language") or "").strip().lower()
    if language not in ("lt", "en", "ru", "pl", "de"):
        language = "lt"
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

    cache_key = hashlib.md5(f"v64:{query.lower()}:{language}".encode()).hexdigest()

    # Freeze query strings for generator closure
    _query = query
    _original = original_query
    _lang = language

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
            p = post_process(list(all_results), _query, None, {}, language=_lang)
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
            _validated_stream = validate_results_with_ai(_query, deduped_for_ai, _lang)
            ai_data = analyze_deal_with_ai(_query, _validated_stream, price_history, _lang)
            result = post_process(_validated_stream, _query, ai_data, price_history, language=_lang)

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


@app.route("/api/identify-product", methods=["POST"])
@rate_limit
def identify_product():
    """Vision-only: identify product from image, no price search."""
    data = request.get_json()
    if not data or "image" not in data:
        return jsonify({"error": "No image"}), 400

    image_b64 = data.get("image", "")
    if len(image_b64) >= 14_000_000:
        return jsonify({"error": "image_too_large"}), 413

    language = (data.get("language") or "").strip().lower()
    if language not in ("lt", "en", "ru", "pl", "de"):
        language = "lt"

    if not ANTHROPIC_API_KEY:
        return jsonify({"error": "scan_unavailable"}), 503

    import base64 as _b64
    def _det_mt(b64):
        try:
            h = _b64.b64decode(b64[:32] + "==")[:8]
            if h[:4] == b'\x89PNG': return "image/png"
            if h[:3] in (b'GIF',): return "image/gif"
            if h[:4] == b'RIFF' or b'WEBP' in h: return "image/webp"
        except Exception: pass
        return "image/jpeg"

    media_type = _det_mt(image_b64)

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model=AI_MODEL_CLAUDE,
            max_tokens=400,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": image_b64}},
                    {"type": "text", "text": """Extract exact product identification from packaging. NEVER guess or invent.

Respond ONLY with JSON (no markdown):
{"brand":"","product_name":"","product_code":null,"pieces":null,"age_range":"","confidence":"high|medium|low"}

- brand: manufacturer visible on packaging. Empty if unsure.
- product_name: full name in English (e.g. "LEGO Creator 3in1 Exotic Parrot").
- product_code: EXACT set/model/SKU number printed. null if not clearly visible.
- pieces: integer if visible, else null.
- age_range: as printed (e.g. "8+"), empty if not visible.
- confidence: "high"=code clearly read, "medium"=brand+name confident, "low"=ambiguous."""}
                ]
            }]
        )

        raw = "".join(b.text for b in response.content if hasattr(b, "text")).strip()
        text = raw.replace("```json", "").replace("```", "").strip()
        jm = re.search(r'\{.*\}', text, re.DOTALL)
        if jm: text = jm.group(0)
        try:
            vision = json.loads(text)
        except Exception:
            nm = re.search(r'"product_name"\s*:\s*"([^"]+)"', raw)
            vision = {"brand": "", "product_name": nm.group(1) if nm else "", "product_code": None, "pieces": None, "age_range": "", "confidence": "low"}

        brand = (vision.get("brand") or "").strip()
        product_name = (vision.get("product_name") or "").strip()
        raw_code = vision.get("product_code")
        product_code = str(raw_code).strip() if raw_code not in (None, "", "null", "None") else ""
        pieces = vision.get("pieces")
        try: pieces = int(pieces) if pieces not in (None, "", "null") else None
        except Exception: pieces = None
        age_range = (vision.get("age_range") or "").strip()
        confidence = (vision.get("confidence") or "medium").strip().lower()

        if product_code and re.match(r'^\d{8,14}$', product_code):
            bc_name = lookup_barcode_free(product_code)
            if bc_name: product_name = bc_name; confidence = "high"

        if not product_name and not product_code:
            return jsonify({"error": "product_not_recognized", "confidence": "low"}), 422

        if product_code and brand:
            search_query = f"{brand} {product_code}"
        elif product_code:
            search_query = f"{product_name} {product_code}".strip() if product_name else product_code
        else:
            parts = [product_name] if product_name else []
            if pieces: parts.append(f"{pieces} pieces")
            search_query = " ".join(parts).strip()

        _dp = []
        if brand: _dp.append(brand)
        if product_code:
            _cl = {"lt": "kodas", "en": "code", "ru": "код", "pl": "kod", "de": "Code"}.get(language, "code")
            _dp.append(f"{_cl} {product_code}")
        if pieces:
            _pl = {"lt": "dalys", "en": "pieces", "ru": "деталей", "pl": "części", "de": "Teile"}.get(language, "pieces")
            _dp.append(f"{pieces} {_pl}")
        if age_range:
            _al = {"lt": "amžius", "en": "age", "ru": "возраст", "pl": "wiek", "de": "Alter"}.get(language, "age")
            _dp.append(f"{_al} {age_range}")
        details = ", ".join(_dp) if _dp else ""

        return jsonify({
            "product_name": product_name,
            "product_code": product_code or None,
            "brand": brand or None,
            "details": details,
            "confidence": confidence,
            "search_query": search_query,
        })

    except Exception as e:
        print(f"[identify_product] {e}")
        return jsonify({"error": "identify_failed"}), 500


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

    language = (data.get("language") or "").strip().lower()
    if language not in ("lt", "en", "ru", "pl", "de"):
        language = "lt"

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
            max_tokens=500,
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
                            "text": """You are extracting an EXACT product identification from packaging. Accuracy matters more than completeness — NEVER guess.

Respond ONLY with JSON (no markdown):
{"brand":"","product_name":"","product_code":null,"pieces":null,"age_range":"","price_visible":0,"barcode":"","confidence":"high|medium|low"}

STRICT rules:
- brand: manufacturer logo / brand name visible on box (e.g. "LEGO", "Apple", "Samsung"). Empty string if unsure.
- product_name: full descriptive title in English (e.g. "LEGO Creator 3in1 Exotic Parrot", "Apple iPhone 16 Pro 256GB").
- product_code: the EXACT product number printed on the box — LEGO set number (e.g. "31385"), model number, SKU, part number. Read the digits character by character. Set to null if you cannot see it clearly. DO NOT guess. DO NOT invent. DO NOT pick a similar code from memory.
- pieces: integer number of pieces / parts if printed (e.g. 542 for LEGO). null if not visible.
- age_range: age range as printed (e.g. "8+", "6-12"). Empty string if not visible.
- price_visible: numeric price in EUR if a price tag is visible, else 0.
- barcode: EAN/UPC digits if a barcode is clearly visible, else empty string.
- confidence: "high" only when product_code is clearly read from the box. "medium" when brand + name confident but no code visible. "low" when ambiguous or category only.

If you are not 100% sure of a digit in product_code, set product_code to null and confidence to "low". A wrong code is worse than no code."""
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
        json_m = re.search(r'\{.*\}', text, re.DOTALL)

        if json_m:
            text = json_m.group(0)

        try:
            vision = json.loads(text)
        except Exception:
            name_m = re.search(r'"product_name"\s*:\s*"([^"]+)"', raw_text)
            vision = {
                "brand": "",
                "product_name": name_m.group(1) if name_m else "",
                "product_code": None,
                "pieces": None,
                "age_range": "",
                "price_visible": 0,
                "barcode": "",
                "confidence": "low"
            }

        brand = (vision.get("brand") or "").strip()
        product_name = (vision.get("product_name") or "").strip()
        raw_code = vision.get("product_code")
        product_code = str(raw_code).strip() if raw_code not in (None, "", "null", "None") else ""
        pieces = vision.get("pieces")
        try:
            pieces = int(pieces) if pieces not in (None, "", "null") else None
        except Exception:
            pieces = None
        age_range = (vision.get("age_range") or "").strip()
        price_visible = vision.get("price_visible", 0)
        confidence = (vision.get("confidence") or "medium").strip().lower()
        barcode_from_image = (vision.get("barcode") or "").strip()

        # If AI found a barcode in the image, try free barcode lookup for a better name
        if barcode_from_image and re.match(r'^\d{8,14}$', barcode_from_image):
            bc_name = lookup_barcode_free(barcode_from_image)
            if bc_name:
                product_name = bc_name
                if not product_code:
                    product_code = barcode_from_image
                confidence = "high"

        if isinstance(price_visible, (int, float)) and price_visible <= 1:
            price_visible = 0

        if not product_name and not product_code:
            return jsonify({
                "error": "product_not_recognized",
                "message": "Produktas neatpažintas. Pabandykite nufotografuoti arčiau, su geresniu apšvietimu arba įveskite pavadinimą rankiniu būdu.",
                "confidence": confidence
            }), 422

        # ── Build search query: prefer exact product code, fall back to name + pieces ──
        if product_code and brand:
            search_query = f"{brand} {product_code}"
        elif product_code:
            search_query = f"{product_name} {product_code}".strip() if product_name else product_code
        else:
            parts = [product_name] if product_name else []
            if pieces:
                parts.append(f"{pieces} pieces")
            search_query = " ".join(parts).strip()

        display_name = product_name or search_query

        cache_key = hashlib.md5(f"scan_v66:{search_query.lower()}:{product_code}:{language}".encode()).hexdigest()
        cached = get_cache(cache_key)

        if cached:
            cached["_cached"] = True
            cached["scanned_product"] = display_name
            cached["scanned_product_code"] = product_code
            cached["store_price"] = price_visible
            return jsonify(cached)

        query_de = search_query
        query_pl = search_query
        # If we have a product code, do NOT translate it (LEGO 31385 stays LEGO 31385 in every market)
        if not product_code:
            try:
                with ThreadPoolExecutor(max_workers=2) as _pre:
                    _f_de = _pre.submit(claude_translate, search_query, "de")
                    _f_pl = _pre.submit(claude_translate, search_query, "pl")
                    query_de = _f_de.result(timeout=4) or search_query
                    query_pl = _f_pl.result(timeout=4) or search_query
            except Exception:
                pass

        # Price history fetches in parallel with shops (starts immediately)
        _scan_ph_exec = ThreadPoolExecutor(max_workers=1)
        scan_ph_fut = _scan_ph_exec.submit(get_price_history, search_query)

        all_results = []
        scan_executor = ThreadPoolExecutor(max_workers=8)
        try:
            futures = {
                scan_executor.submit(scrape_varle,   search_query):    "Varle",
                scan_executor.submit(scrape_elesen,  search_query):    "Elesen",
                scan_executor.submit(scrape_pigu,    search_query):    "Pigu",
                scan_executor.submit(scrape_topo,    search_query):    "Topo",
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

        # ── VALIDATION: when we have a product code, verify it appears in each result title ──
        _code_warn_map = {
            "lt": "Galimai netikslus atitikimas",
            "en": "Possibly inaccurate match",
            "ru": "Возможно неточное совпадение",
            "pl": "Możliwe niedokładne dopasowanie",
            "de": "Möglicherweise ungenaue Übereinstimmung",
        }
        _warn_lang = language if language in _code_warn_map else "lt"
        warn_label = _code_warn_map[_warn_lang]

        if product_code:
            code_lower = product_code.lower()
            code_digits = re.sub(r'\D', '', product_code)
            for r in all_results:
                title = (r.get("product_title") or "").lower()
                title_digits = re.sub(r'\D', '', title)
                matched = code_lower in title or (len(code_digits) >= 4 and code_digits in title_digits)
                r["code_match"] = bool(matched)
                if not matched:
                    r["match_warning"] = warn_label

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
                "product_title": display_name,
                "code_match": True
            })

        # Collect price history (was running in parallel since shop start)
        price_history = {}
        try:
            price_history = scan_ph_fut.result(timeout=1)
        except Exception:
            pass

        _scan_rel = [r for r in all_results if r.get("price", 0) > 0
                     and is_relevant_result(display_name, r.get("product_title", ""))] or all_results
        # When we have a code, prefer matching results for AI analysis
        if product_code:
            _code_matched = [r for r in _scan_rel if r.get("code_match")]
            if _code_matched:
                _scan_rel = _code_matched
        deduped_for_scan_ai = deduplicate_by_shop(_scan_rel)
        _validated_scan = validate_results_with_ai(display_name, deduped_for_scan_ai, language)
        ai_data = analyze_deal_with_ai(display_name, _validated_scan, price_history, language)
        result = post_process(_validated_scan, display_name, ai_data, price_history, language=language)

        result["scanned_product"] = display_name
        result["scanned_product_code"] = product_code
        result["scanned_brand"] = brand
        result["scanned_pieces"] = pieces
        result["scanned_age_range"] = age_range
        result["scan_confidence"] = confidence
        # Global match warning if code present but no result matched it
        if product_code and not any(r.get("code_match") for r in all_results):
            result["match_warning"] = warn_label
            result["match_warning_detail"] = {
                "lt": f"Nepavyko rasti produkto su tiksliu kodu {product_code}. Rezultatai gali būti netikslūs.",
                "en": f"Could not find a product with exact code {product_code}. Results may be inaccurate.",
                "ru": f"Не удалось найти продукт с точным кодом {product_code}. Результаты могут быть неточными.",
                "pl": f"Nie znaleziono produktu z dokładnym kodem {product_code}. Wyniki mogą być niedokładne.",
                "de": f"Produkt mit exaktem Code {product_code} nicht gefunden. Ergebnisse können ungenau sein.",
            }[_warn_lang]
        result["store_price"] = (
            price_visible
            if isinstance(price_visible, (int, float)) and price_visible > 1
            else 0
        )
        price_for_scan_classify = price_visible if isinstance(price_visible, (int, float)) and price_visible > 1 else result.get("price_min", 0)
        scan_product_type = classify_product_cheap(display_name, price_for_scan_classify)
        result["product_type"] = scan_product_type
        result["category_icon"] = get_category_icon(display_name, scan_product_type)
        result["search_time_ms"] = int((time.time() - t0) * 1000)

        set_cache(cache_key, result)

        track_search(display_name)
        threading.Thread(target=save_prices_to_supabase, args=(display_name, result.get("results", all_results)), daemon=True).start()

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
        "version": "7.55",
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

    print("\n🟢 Goody API v7.55")
    print(f"📊 Supabase: {'✅ configured' if SUPABASE_URL else '⚠️ not set'}")
    print("📦 Active shops: Varle + Elesen + Pigu + Topo + Amazon.DE + Amazon.PL")
    print(f"🔑 ScraperAPI: {'✅ configured' if SCRAPER_API_KEY else '⚠️ not set'}")
    print(f"🔑 Zyte: {'✅ configured' if ZYTE_API_KEY else '⚠️ not set'}")
    print(f"🤖 Anthropic: {'✅ configured' if ANTHROPIC_API_KEY else '❌ missing'}")
    print(f"🤖 OpenAI: {'✅ configured' if OPENAI_API_KEY else '❌ missing'}")
    print(f"🧠 AI provider: {AI_PROVIDER}")
    print(f"🧠 OpenAI model: {AI_MODEL_OPENAI}")

    app.run(host="0.0.0.0", port=port, debug=False)
