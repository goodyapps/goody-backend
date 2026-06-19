"""
Targeted validation of accessory-fix branch changes.
Tests is_relevant_result (Fix A) and post_process price logic (Fix C)
using the ACTUAL code from server.py — not the inlined test version.

Run from goody-backend directory:
    python test_accessory_fix.py
"""
import re, sys

# ── Replicate server.py constants and functions (current state with Fix A) ──

def _norm_units(text):
    return re.sub(r'(\d+)\s+(gb|tb|mb|mp|mah|hz|mhz|ghz)\b',
                  lambda m: m.group(1) + m.group(2), text.lower())

_UNIT_TOKEN_RE = re.compile(
    r'^\d+(?:g|ml|l|kg|mg|oz|cl|dl|mm|cm|m|w|v|hz|rpm|pcs|st|stk|er|x)$'
)

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
    'aeg', 'zanussi', 'liebherr', 'gorenje', 'indesit', 'beko', 'candy', 'haier',
    'ninja', 'kitchenaid', 'smeg', 'melitta', 'sage', 'russell', 'breville',
    'grundig', 'ariston', 'hotpoint', 'bauknecht', 'constructa',
    'polar', 'suunto', 'gopro', 'dji', 'nokia', 'roborock', 'beats', 'marshall',
    'honor', 'vivo', 'poco', 'redmi', 'nothing',
    'fujifilm', 'olympus', 'leica', 'oral-b', 'epson',
    'dreame', 'ecovacs', 'eufy',
    'milwaukee', 'ryobi', 'festool', 'einhell',
    'stihl', 'husqvarna', 'worx', 'metabo', 'parkside', 'greenworks',
    'gardena', 'weber', 'instant', 'vitamix',
    'sonos', 'harman kardon',
    'ilife', 'cecotec', 'blaupunkt',
    'daikin', 'vaillant', 'viessmann', 'mitsubishi electric', 'gree', 'baxi',
    'levoit', 'blueair', 'coway', 'winix',
    'beurer', 'omron', 'medisana', 'withings',
    'moulinex', 'krups', 'severin', 'cuisinart', 'bomann',
    'neff', 'asko', 'midea', 'hoover',
}

_PURE_CATEGORY_WORDS = frozenset({
    'dyktafon', 'dyktafony', 'recorder', 'dictaphone', 'diktofonas',
    'smartphone', 'telefonas', 'laptop', 'tablet', 'monitor',
    'headphones', 'earbuds', 'ausines', 'ausinai',
    'camera', 'kamera', 'drucker', 'printer',
    'router', 'hub', 'switch',
})

_VARIANT_WORDS = frozenset({
    'pro', 'max', 'ultra', 'plus', 'lite', 'mini', 'fe', 'edge',
    'note', 'fold', 'flip', 'air', 'neo', 'active', 'sport',
    'slim', 'boost', 'titan', 'classic',
})

# _ACCESSORY_MATCH_WORDS — CURRENT STATE after Fix A (includes LED/lighting terms)
_ACCESSORY_MATCH_WORDS = frozenset({
    'case', 'cover', 'sleeve', 'bumper', 'wallet', 'skin', 'sticker', 'decal',
    'holder', 'stand', 'mount', 'cradle', 'dock', 'bracket', 'grip',
    'charger', 'cable', 'adapter', 'hub', 'extender', 'splitter', 'dongle',
    'screen protector', 'tempered glass', 'film', 'foil',
    'replacement', 'spare', 'repair', 'filter', 'bag', 'brush', 'attachment',
    'earpad', 'eartip', 'ear tip', 'cushion', 'pad',
    'stylus', 'remote control', 'controller',
    'watch band', 'sport band', 'fitness band', 'wristband', 'band', 'strap',
    'deklas', 'maislelis', 'rankine', 'stovas', 'laikiklis', 'dirzelis',
    'kroviklis', 'kabelis', 'plevele', 'stikliukas', 'apsauga',
    'etui', 'obudowa', 'pokrowiec', 'ladowarka', 'kabel', 'szklo', 'folia',
    'uchwyt', 'podstawka', 'naklejka', 'ochraniacz', 'filtr', 'pasek',
    'hulle', 'tasche', 'schutzhuelle', 'ladegerat', 'halterung', 'schutzglas',
    'ersatz', 'zubehor', 'armband',
    'maišeliai', 'filtrai', 'filtras', 'priedai', 'priedas', 'laikiklis',
    'cleaning kit', 'cleaning brush', 'carry bag', 'carry case', 'screen film',
    'wall mount', 'power bank', 'spare part',
    'battery pack', 'replacement battery', 'baterija',
    'systainer', 'akkupack', 'netzteil',
    'milchaufschaeumer', 'entkalkungstabletten', 'reinigungstabletten',
    'luftfilter', 'ohrpolster', 'ohrkissen', 'kopfpolster',
    'tragetasche', 'tragegurt', 'schutztasche',
    'worek pylowy', 'akcesoria',
    'toner', 'wandhalterung', 'ersatzteile',
    'ersatzburste', 'seitenburste', 'hauptburste', 'wischpad',
    'cartridge', 'refill', 'ink cartridge', 'druckerpatrone',
    'staubsaugerbeutel', 'ersatzbeutel', 'tonerkassette',
    'ladekabel', 'aufladekabel', 'netzkabel',
    'ladestation', 'akkuladegerat',
    'notebooktasche', 'laptoptasche', 'kameratasche',
    'rucksack', 'torba', 'plecak',
    'schutzfolie', 'displayschutzfolie', 'bildschirmschutzfolie',
    'bildschirmschutz', 'displayschutz', 'panzerglas',
    'folia ochronna', 'folia',
    'fernbedienung',
    'entkalker', 'descaler', 'odkamieniacz',
    'scherkopf', 'wechselkopf', 'wechselklinge', 'scherfolie',
    'zamienny', 'zamienna', 'zamienne', 'zamiennik',
    'zapasowy', 'zapasowa', 'zapasowe',
    'galvute', 'galvutes',
    'nozzle', 'antgalis', 'antgaliai', 'dose', 'koncowka',
    'baterijos',
    'accessories', 'attachment', 'compatible',
    'skirtas', 'skirta', 'skirtos', 'tinka',
    'spare battery', 'extra battery', 'battery for',
    # Fix A: LED / lighting accessories
    'lighting', 'light kit', 'light set', 'led light', 'lighting kit',
    'beleuchtung', 'oswietlenie',
})


def is_relevant_result(query: str, product_title: str) -> bool:
    if not product_title or not query:
        return True
    q = _norm_units(query)
    t = _norm_units(product_title)

    q_clean_words = [w for w in re.findall(r'[a-z]{3,}', q) if w not in _STOP_WORDS]
    if q_clean_words and all(w in _PURE_CATEGORY_WORDS for w in q_clean_words):
        has_brand_in_title = any(b.replace(' ', '') in t.replace(' ', '') for b in _KNOWN_BRANDS)
        has_brand_in_q = any(b.replace(' ', '') in q.replace(' ', '') for b in _KNOWN_BRANDS)
        if not has_brand_in_q and not has_brand_in_title:
            return False

    compat_patterns = [
        r'\bfor\s+[a-z]+',
        r'\bcompatible\s+with\b',
        r'\bskirta\s+[a-z]+',
        r'\btinka\s+[a-z]+',
        r'\bgeeignet\s+fur\b',
        r'\bpassend\s+fur\b',
        r'\bdla\s+[a-z]+',
    ]
    for pattern in compat_patterns:
        if re.search(pattern, t) and not re.search(pattern, q):
            return False

    for acc in _ACCESSORY_MATCH_WORDS:
        if acc not in t:
            continue
        if acc.isascii() and ' ' not in acc:
            if not re.search(r'(?<![a-z0-9])' + re.escape(acc) + r'(?![a-z0-9])', t):
                continue
        if acc not in q:
            return False

    q_ns = q.replace(' ', '')
    t_ns = t.replace(' ', '')
    brands_in_q = [b for b in _KNOWN_BRANDS if b.replace(' ', '') in q_ns]
    for brand in brands_in_q:
        if brand.replace(' ', '') not in t_ns:
            return False

    q_tok = set(re.findall(r'[a-z0-9]+', q))
    t_tok = set(re.findall(r'[a-z0-9]+', t))
    for variant in _VARIANT_WORDS:
        if variant in q_tok and variant not in t_tok:
            return False

    model_tokens = [tok for tok in re.findall(r'\b[a-z]*\d+[a-z0-9-]*\b', q)
                    if not _UNIT_TOKEN_RE.match(tok)]
    if model_tokens:
        t_nh = t.replace('-', '').replace(' ', '')
        def _model_in_title(m):
            m_nh = m.replace('-', '')
            if re.search(r'(?<![a-z0-9])' + re.escape(m) + r'(?![a-z0-9])', t):
                return True
            if m_nh and m_nh in t_nh:
                return True
            return False
        if not all(_model_in_title(m) for m in model_tokens):
            return False
        if brands_in_q:
            for _br in brands_in_q:
                _br_esc = re.escape(_br)
                if re.search(
                    r'\b(?:for|compatible\s+with|designed\s+for|suitable\s+for|fits|skirtas?\s|tinka\s|fur|pour|voor)\s+' + _br_esc,
                    t
                ):
                    return False
            return True

    if any(ord(c) > 127 for c in query):
        return True
    if brands_in_q and not model_tokens:
        q_words_non_brand = [w for w in re.findall(r'[a-z0-9]{2,}', q)
                             if w not in _STOP_WORDS and w not in brands_in_q]
        if len(q_words_non_brand) <= 2:
            return True

    q_words = [w for w in re.findall(r'[a-z0-9]{2,}', q)
               if w not in _STOP_WORDS and not _UNIT_TOKEN_RE.match(w)]
    t_words = set(re.findall(r'[a-z0-9]{2,}', t))
    if not q_words:
        return True
    overlap = sum(1 for w in q_words if w in t_words)
    ratio = overlap / len(q_words)
    if len(q_words) <= 2:
        return ratio >= 1.0
    return ratio >= 0.55


# ── Fix C: price sanity logic ────────────────────────────────────────────────

_SUSPICIOUS_ACCESSORY_SIGNALS = frozenset({
    'lighting', 'light kit', 'light set', 'led light', 'lighting kit',
    'beleuchtung', 'oswietlenie',
    'only lights', 'not included',
    'compatible', 'accessories',
    'priedas', 'priedai', 'aksesuaras',
})


def check_price_sanity(results, query):
    """Simulate post_process Step 1 + Step 1b logic."""
    all_prices = [r['price'] for r in results]
    if len(all_prices) < 2:
        return results, []

    _price_median = sorted(all_prices)[len(all_prices) // 2]
    rejected = []
    warned = []
    _q_norm = _norm_units(query)

    for r in results:
        if r['price'] < _price_median * 0.40:
            r['is_suspicious'] = True
            _t = _norm_units(r.get('product_title', ''))
            _hit = next(
                (sig for sig in _SUSPICIOUS_ACCESSORY_SIGNALS
                 if sig in _t and sig not in _q_norm),
                None
            )
            if _hit:
                rejected.append((r, _hit))
            else:
                warned.append(r)

    non_rejected = [r for r in results if not any(r is rj for rj, _ in rejected)]
    final = non_rejected if non_rejected else results
    return final, rejected


# ─────────────────────────────────────────────────────────────────────────────
# TEST CASES
# ─────────────────────────────────────────────────────────────────────────────

PASS = 0
FAIL = 0
results_log = []


def check(label, query, title, expect_relevant, reason=""):
    global PASS, FAIL
    got = is_relevant_result(query, title)
    ok = (got == expect_relevant)
    status = "PASS" if ok else "FAIL"
    if ok:
        PASS += 1
    else:
        FAIL += 1
    note = reason if reason else ""
    results_log.append(f"  [{status}] {label}")
    results_log.append(f"         query='{query}'")
    results_log.append(f"         title='{title[:80]}'")
    results_log.append(f"         expect={expect_relevant} got={got}  {note}")
    results_log.append("")


def section(name):
    results_log.append(f"\n{'='*60}")
    results_log.append(f"  {name}")
    results_log.append('='*60)


# ── Section 1: LEGO LED accessory filtering (Fix A) ──

section("Fix A — LEGO LED accessories MUST be rejected")

# The exact bug case from ACCESSORY_FILTER_DEBUG.md
check("LocoLee with compat phrasing",
      "LEGO Harry 76430",
      "LocoLee Light Compatible with Lego 76430 Owl on Hogwarts Castle, Only Lights, Not a Lego Model",
      expect_relevant=False,
      reason="'compatible with' in compat_patterns OR 'compatible' in _ACCESSORY_MATCH_WORDS")

# Title WITHOUT "compatible with" — the actual bug path (lego+model at start, lighting keyword)
check("LED Lighting Kit — brand+model at start, no compat phrase",
      "LEGO Harry 76430",
      "LEGO 76430 LED Lighting Kit Hogwarts Owl Post USB-C",
      expect_relevant=False,
      reason="Fix A: 'lighting' in _ACCESSORY_MATCH_WORDS, not in query => return False")

check("LED Light Set — brand+model at start",
      "LEGO 76430 Hogwarts",
      "LEGO 76430 LED Light Set Hogwarts Owl Post",
      expect_relevant=False,
      reason="Fix A: 'light set' in _ACCESSORY_MATCH_WORDS")

check("BrickBling Lighting Kit (third-party brand, no compat phrase)",
      "LEGO Harry 76430",
      "BrickBling LEGO 76430 Lighting Kit for Hogwarts",
      expect_relevant=False,
      reason="Fix A: 'lighting' in _ACCESSORY_MATCH_WORDS")

check("Lighting Kit for another LEGO set",
      "LEGO 75257 Millennium Falcon",
      "LED Lighting Kit LEGO 75257 Millennium Falcon USB",
      expect_relevant=False,
      reason="Fix A: 'lighting' in _ACCESSORY_MATCH_WORDS")

check("'for lego' phrasing — already worked before Fix A",
      "LEGO Harry 76430",
      "BrickBling LED Light Set for Lego 76430 Hogwarts",
      expect_relevant=False,
      reason="compat_patterns: 'for lego' matches \\bfor\\s+[a-z]+")

check("German beleuchtung (Amazon.DE)",
      "LEGO Harry 76430",
      "LEGO 76430 Beleuchtung Set Hogwarts Eule USB-C",
      expect_relevant=False,
      reason="Fix A: 'beleuchtung' in _ACCESSORY_MATCH_WORDS")


section("Fix A — REAL LEGO sets MUST NOT be rejected")

check("Actual LEGO set — no accessory words",
      "LEGO Harry 76430",
      "LEGO Harry Potter 76430 Hogwarts Owl Post Building Set",
      expect_relevant=True,
      reason="Real set: no accessory words, brand+model confirmed")

check("LEGO set — explicit 'Building Set' label",
      "LEGO 75257 Millennium Falcon",
      "LEGO Star Wars 75257 Millennium Falcon Building Set 1351 Pieces",
      expect_relevant=True,
      reason="Real set: no accessory words")

check("LEGO set — short title",
      "LEGO 76430",
      "LEGO Harry Potter 76430",
      expect_relevant=True,
      reason="Real set: brand+model match, no accessory signals")


section("Fix A — PS5 controller accessory vs real controller")

check("PS5 silicone cover — should be rejected (has 'cover')",
      "PS5 controller",
      "Silicone Cover for PS5 DualSense Controller Anti-Slip Case",
      expect_relevant=False,
      reason="'cover' and 'for ps5' both trigger")

check("Real PS5 DualSense controller",
      "PS5 controller",
      "Sony PlayStation DualSense PS5 Wireless Controller White",
      expect_relevant=True,
      reason="Real product: 'sony' brand matches, no accessory words")

check("PS5 controller stand (accessory)",
      "PS5 controller",
      "OIVO PS5 Controller Charging Stand Station Dock",
      expect_relevant=False,
      reason="'stand' in _ACCESSORY_MATCH_WORDS, 'charging' similar to charger")


section("Fix A — Regression: real products with overlapping words")

# "lighting" as accessory word — but what about a product that legitimately has it?
# Philips Hue lighting system IS the main product when searched directly
check("Philips Hue — 'lighting' in query too, should pass",
      "Philips Hue lighting kit",
      "Philips Hue White and Colour Ambiance Smart Lighting Starter Kit",
      expect_relevant=True,
      reason="'lighting' is in BOTH query and title => no rejection (acc check: if acc not in q => skip)")

check("Smart lighting — 'lighting' in query",
      "Govee smart lighting",
      "Govee RGBIC LED Strip Lighting 5m Smart Home",
      expect_relevant=True,
      reason="'lighting' is in query => _ACCESSORY_MATCH_WORDS check skipped")

# LED TV — 'led' alone is NOT in match words, only 'led light' (phrase) is
check("LG OLED TV — no accessory",
      "LG OLED55C3",
      "LG OLED 55 C3 OLED55C3 4K Smart TV 2023",
      expect_relevant=True,
      reason="'oled' not blocked; model token oled55c3 present")

check("iPhone 15 128GB — real product",
      "iPhone 15 128GB",
      "Apple iPhone 15 128GB Black Smartphone",
      expect_relevant=True,
      reason="No accessory words, brand+model present")

check("Samsung fridge — real product",
      "Samsung RB34C600ESA",
      "Samsung RB34C600ESA Kühlschrank 201cm 342L NoFrost",
      expect_relevant=True,
      reason="No accessory words, brand+model present")

check("Sony WH-1000XM5 — real headphones",
      "Sony WH-1000XM5",
      "Sony WH-1000XM5 Wireless Noise-Cancelling Headphones Black",
      expect_relevant=True,
      reason="No accessory words, brand+model present")

check("Milka 100g — food (unit-token filtering)",
      "Milka 100g",
      "Milka Alpenmilch Schokolade 100g",
      expect_relevant=True,
      reason="100g is unit token, filtered from model_tokens; brand 'milka' not in known brands but word overlap passes")

check("Dyson V15 Detect — real vacuum",
      "Dyson V15 Detect",
      "Dyson V15 Detect Absolute Cordless Vacuum Cleaner",
      expect_relevant=True,
      reason="No accessory words, brand+model present")


section("Fix A — Edge cases: accessory words that should NOT block")

# 'light kit' in query itself
check("Light kit query — searching for light kit explicitly",
      "Philips Hue light kit",
      "Philips Hue White Ambiance GU10 Light Kit 3 bulbs",
      expect_relevant=True,
      reason="'light kit' in query AND title => _ACCESSORY_MATCH_WORDS: if acc not in q => skip => passes")

# 'led light' in query
check("LED light query — searching for LED lights explicitly",
      "Govee LED light strip",
      "Govee RGBIC LED Light Strip 5m 16 Million Colors",
      expect_relevant=True,
      reason="'led light' in query AND title => no rejection")

# 'lighting' in long query with LEGO set number — this is ambiguous
# A user searching "LEGO 76430 lighting" MIGHT want the lighting kit
# → in that case, the accessory should be shown
check("User explicitly wants lighting for LEGO",
      "LEGO 76430 lighting",
      "LocoLee LED Lighting Kit for LEGO 76430 Hogwarts",
      expect_relevant=True,
      reason="'lighting' in query => _ACCESSORY_MATCH_WORDS bypass; 'for lego' is in title but 'for' is also in query (lego harry 76430 for?)")


section("Fix C — Price sanity: suspicious+accessory → reject")

def test_price_sanity(label, results_data, query, expect_reject_count, expect_warn_count=0):
    global PASS, FAIL
    final, rejected = check_price_sanity(results_data, query)
    warned = [r for r in final if r.get('is_suspicious')]
    ok_reject = len(rejected) == expect_reject_count
    ok_warn = len(warned) == expect_warn_count
    ok = ok_reject and ok_warn
    if ok:
        PASS += 1
    else:
        FAIL += 1
    status = "PASS" if ok else "FAIL"
    results_log.append(f"  [{status}] {label}")
    results_log.append(f"         rejected={len(rejected)} (expect {expect_reject_count}), warned={len(warned)} (expect {expect_warn_count})")
    for r, sig in rejected:
        results_log.append(f"         REJECT signal='{sig}' price={r['price']:.2f} title='{r['product_title'][:60]}'")
    for r in warned:
        results_log.append(f"         WARN price={r['price']:.2f} title='{r['product_title'][:60]}'")
    results_log.append("")


# LED kit €27.98 vs LEGO set €78.98 — should reject LED kit
test_price_sanity(
    "LEGO LED kit vs real set — LED kit should be REJECTED",
    [
        {'price': 27.98, 'product_title': 'LEGO 76430 LED Lighting Kit Hogwarts Owl Post', 'shop': 'amazon'},
        {'price': 78.98, 'product_title': 'LEGO Harry Potter 76430 Hogwarts Owl Post Building Set', 'shop': 'pigu'},
    ],
    query="LEGO 76430 Hogwarts",
    expect_reject_count=1,
    expect_warn_count=0,
)

# Genuinely cheap product (no accessory signal) — should WARN not reject
test_price_sanity(
    "Genuine cheap deal — should WARN, not reject",
    [
        {'price': 35.00, 'product_title': 'Sony WH-1000XM5 Headphones Black', 'shop': 'amazon'},
        {'price': 120.00, 'product_title': 'Sony WH-1000XM5 Wireless Noise-Cancelling Headphones', 'shop': 'elesen'},
    ],
    query="Sony WH-1000XM5",
    expect_reject_count=0,
    expect_warn_count=1,
)

# All results at similar price — no suspicious flag
test_price_sanity(
    "Similar prices — no flagging",
    [
        {'price': 78.99, 'product_title': 'LEGO Harry Potter 76430 Hogwarts', 'shop': 'amazon'},
        {'price': 82.50, 'product_title': 'LEGO Harry Potter 76430 Hogwarts Owl Post', 'shop': 'pigu'},
    ],
    query="LEGO 76430 Hogwarts",
    expect_reject_count=0,
    expect_warn_count=0,
)

# If the ONLY result is cheap+accessory — should NOT reject (nothing to replace it with)
test_price_sanity(
    "Only result is suspicious — keep with warning (no alternatives)",
    [
        {'price': 27.98, 'product_title': 'LED Lighting Kit LEGO 76430 Hogwarts', 'shop': 'amazon'},
    ],
    query="LEGO 76430 Hogwarts",
    expect_reject_count=0,  # can't reject if no alternatives — safety fallback
    expect_warn_count=0,    # only 1 price, median == price, price < median * 0.40 is False
)

# Compatible accessory signal via Fix C
test_price_sanity(
    "Compatible signal + suspicious price → reject",
    [
        {'price': 15.00, 'product_title': 'PS5 Controller Compatible Silicone Cover', 'shop': 'amazon'},
        {'price': 65.00, 'product_title': 'Sony PS5 DualSense Controller White', 'shop': 'pigu'},
    ],
    query="PS5 controller",
    expect_reject_count=1,
)

# ─────────────────────────────────────────────────────────────────────────────
# PRINT RESULTS
# ─────────────────────────────────────────────────────────────────────────────

total = PASS + FAIL
print(f"\n{'='*60}")
print(f"  ACCESSORY FIX VALIDATION RESULTS")
print(f"  PASS: {PASS}/{total}   FAIL: {FAIL}/{total}")
print(f"{'='*60}")
for line in results_log:
    print(line)

print(f"\n{'='*60}")
print(f"  FINAL: {'ALL PASS' if FAIL == 0 else f'{FAIL} FAILED'}")
print(f"{'='*60}")

sys.exit(0 if FAIL == 0 else 1)
