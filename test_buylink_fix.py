"""
Targeted validation of buylink-fix branch changes.
Tests URL validation (Fix A) and Amazon sponsored/ASIN logic (Fix B).
Run from goody-backend directory:
    python test_buylink_fix.py
"""
import re
import sys
from bs4 import BeautifulSoup

# ── Replicated logic from server.py (buylink-fix state) ─────────────────────

def _norm_units(text):
    return re.sub(r'(\d+)\s+(gb|tb|mb|mp|mah|hz|mhz|ghz)\b',
                  lambda m: m.group(1) + m.group(2), text.lower())

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
    'grundig', 'ariston', 'hotpoint', 'polar', 'suunto', 'gopro', 'dji', 'nokia',
    'roborock', 'beats', 'marshall', 'honor', 'vivo', 'poco', 'redmi', 'nothing',
    'fujifilm', 'olympus', 'leica', 'oral-b', 'epson', 'dreame', 'ecovacs', 'eufy',
}

_UNIT_TOKEN_RE = re.compile(
    r'^\d+(?:g|ml|l|kg|mg|oz|cl|dl|mm|cm|m|w|v|hz|rpm|pcs|st|stk|er|x)$'
)

_ACCESSORY_MATCH_WORDS = frozenset([
    "case", "hülle", "cover", "tasche", "etui", "schutzfolie", "folie", "screen protector",
    "charger", "ladekabel", "cable", "kabel", "adapter", "hub", "dock", "stand", "halter",
    "strap", "band", "armband", "bracelet", "replacement", "ersatz", "spare", "parts",
    "filter", "bag", "staubbeutel", "beutel", "sack", "attachment", "tool", "zubehör",
    "stylus", "pen", "stift", "lens", "cap", "hood", "strap", "sling", "shoulder",
    # LED / lighting accessories
    "lighting", "light kit", "light set", "led light", "lighting kit",
    "beleuchtung", "oswietlenie",
])

def is_relevant_result(query: str, product_title: str) -> bool:
    if not product_title or not query:
        return True
    q = _norm_units(query)
    t = _norm_units(product_title)
    compat_patterns = [
        (r'\bfor\b', r'\bfor\b'),
        (r'\bfür\b', r'\bfür\b'),
        (r'\bdo\b', r'\bdo\b'),
        (r'\bcompatible\b', r'\bcompatible\b'),
        (r'\bpassend\b', r'\bpassend\b'),
        (r'\bkompatibel\b', r'\bkompatibel\b'),
    ]
    for q_pat, t_pat in compat_patterns:
        if re.search(t_pat, t) and not re.search(q_pat, q):
            return False
    for acc in _ACCESSORY_MATCH_WORDS:
        if acc in t and acc not in q:
            return False
    q_words = q.split()
    brands_in_q = [b for b in _KNOWN_BRANDS if b in q]
    model_tokens = []
    for w in q_words:
        if re.match(r'^\d{4,}$', w):
            model_tokens.append(w)
        elif re.match(r'^[a-z]{1,4}\d+', w) and len(w) >= 4:
            model_tokens.append(w)
        elif _UNIT_TOKEN_RE.match(w):
            pass
    if brands_in_q and model_tokens:
        if not any(tok in t for tok in model_tokens):
            return False
        if not any(b in t for b in brands_in_q):
            return False
    elif brands_in_q and not model_tokens:
        if not any(b in t for b in brands_in_q):
            return False
    elif model_tokens and not brands_in_q:
        if not any(tok in t for tok in model_tokens):
            return False
    return True


# ── Fix A: Empty URL logic ───────────────────────────────────────────────────

def check_empty_url_walk(slug: str, base_url: str) -> bool:
    """Simulates _walk_for_products URL validation. Returns True if URL is valid (not skipped)."""
    if slug.startswith("http"):
        link = slug
    else:
        link = f"{base_url.rstrip('/')}/{slug.lstrip('/')}"
    return not (not slug or link.rstrip("/") == base_url.rstrip("/"))


def check_elesen_href(href: str) -> bool:
    """Simulates _scrape_elesen_from_html href validation. Returns True if valid."""
    link = href if href.startswith("http") else f"https://www.elesen.lt{href}"
    return not (not href or href in ("/", "#") or link.rstrip("/") == "https://www.elesen.lt")


# ── Fix B: Sponsored + competing model code logic ───────────────────────────

def check_sponsored_competing_model(is_sponsored: bool, query: str, name: str) -> bool:
    """Returns True if result should be SKIPPED (sponsored + competing model)."""
    if not is_sponsored:
        return False
    q_codes = set(re.findall(r'\b\d{4,6}\b', query))
    if not q_codes:
        return False
    t_codes = set(re.findall(r'\b\d{4,6}\b', name))
    competing = t_codes - q_codes
    return bool(competing and any(len(c) == len(next(iter(q_codes))) for c in competing))


def check_asin_mismatch(item_asin: str, url_asin: str):
    """Returns corrected asin. Mirrors server.py ASIN consistency logic."""
    if item_asin and url_asin and item_asin != url_asin:
        return item_asin  # correct mismatched ASIN
    elif item_asin and not url_asin:
        return item_asin  # reconstruct from item_asin when link extraction failed
    return url_asin  # unchanged


# ── Test runner ───────────────────────────────────────────────────────────────

results = []
PASS = "PASS"
FAIL = "FAIL"

def test(name, got, expected, desc=""):
    ok = got == expected
    status = PASS if ok else FAIL
    results.append((status, name, got, expected, desc))
    tag = "OK" if ok else "FAIL"
    print(f"  [{tag}] {name}")
    if not ok:
        print(f"         got={got!r} expected={expected!r}")
    if desc and not ok:
        print(f"         note: {desc}")


print("\n=== Fix A: Empty URL rejection (_walk_for_products) ===")

test("empty slug -> skip",
     check_empty_url_walk("", "https://www.elesen.lt"), False,
     "slug='' produces homepage URL -> must be skipped")

test("None-equivalent slug -> skip",
     check_empty_url_walk("", "https://www.1a.lt"), False)

test("relative slug -> keep",
     check_empty_url_walk("/lt/products/lego-76430-hogwarts", "https://www.elesen.lt"), True,
     "relative slug with product path -> valid")

test("absolute slug -> keep",
     check_empty_url_walk("https://www.elesen.lt/lt/products/lego-76430", "https://www.elesen.lt"), True)

test("1a.lt relative slug -> keep",
     check_empty_url_walk("/tovaras/lego-76430", "https://www.1a.lt"), True)

test("1a.lt homepage slug -> skip",
     check_empty_url_walk("", "https://www.1a.lt"), False)

test("slug is just '/' -> skip",
     check_empty_url_walk("/", "https://www.elesen.lt"), False,
     "slug='/' resolves to homepage -> skip")


print("\n=== Fix A: Empty URL rejection (_scrape_elesen_from_html DOM path) ===")

test("empty href -> skip",
     check_elesen_href(""), False)

test("href='/' -> skip",
     check_elesen_href("/"), False)

test("href='#' -> skip",
     check_elesen_href("#"), False)

test("relative href with path -> keep",
     check_elesen_href("/lt/products/lego-76430-hogwarts-peles-narvas"), True)

test("absolute href -> keep",
     check_elesen_href("https://www.elesen.lt/lt/products/lego-76430"), True)

test("relative href -> constructs full URL -> keep",
     check_elesen_href("/lt/prekes/samsung-galaxy-s24"), True)


print("\n=== Fix B1/B2: Sponsored + competing model code ===")

# THE BUG: query=76430, sponsored item shows 76451 in title
test("sponsored + competing 5-digit code (76430 vs 76451) -> SKIP",
     check_sponsored_competing_model(
         True,
         "LEGO 76430 Hogwarts",
         "LEGO Harry Potter 76430 Hogwarts 76451 Privet Drive Building Set"
     ), True,
     "Sponsored 76451 ad shown for 76430 query -> reject")

# Same-digit-length competing code — other digit lengths should NOT trigger
test("sponsored + competing 4-digit code (different length to 5-digit query) -> KEEP",
     check_sponsored_competing_model(
         True,
         "LEGO 76430 Hogwarts",
         "LEGO Harry Potter 76430 Hogwarts Owl Post 432 pieces"
     ), False,
     "432 is 3 digits, not same length as 76430 (5 digits) -> keep")

# Not sponsored -> never skip
test("NOT sponsored + competing code -> KEEP",
     check_sponsored_competing_model(
         False,
         "LEGO 76430 Hogwarts",
         "LEGO Harry Potter 76430 Hogwarts 76451 Privet Drive"
     ), False,
     "Organic result with two set numbers -> keep (not sponsored)")

# Correct sponsored: only query code in title, no competing
test("sponsored + ONLY query code in title -> KEEP",
     check_sponsored_competing_model(
         True,
         "LEGO 76430 Hogwarts",
         "LEGO Harry Potter 76430 Hogwarts Owl Post Building Set"
     ), False,
     "Sponsored but title has only 76430 (correct product) -> keep")

# Query without numeric code -> sponsored detection skips (no codes to compare)
test("sponsored + query has no model code -> KEEP",
     check_sponsored_competing_model(
         True,
         "iPhone 15 Pro Max",
         "Apple iPhone 15 Pro Max 256GB Natural Titanium"
     ), False,
     "No numeric code in query -> competing code check not applied")

# iPhone 128GB — query has no pure numeric code (128 is part of "128GB"), should be fine
test("sponsored + iPhone 128GB query (no bare 5-digit code) -> KEEP",
     check_sponsored_competing_model(
         True,
         "iPhone 15 128GB",
         "Apple iPhone 15 128GB Black Smartphone"
     ), False,
     "128 is 3 digits and part of 128GB — not matched as 4-6 digit bare code")

# Samsung model number in query: RB34C600ESA — contains digits but they're mixed with letters
# This is handled by model_tokens (alphanumeric) not by the pure digit re.findall
test("sponsored + Samsung alphanumeric model -> KEEP (no pure digit code in query)",
     check_sponsored_competing_model(
         True,
         "Samsung RB34C600ESA",
         "Samsung RB34C600ESA/EF Refrigerator"
     ), False,
     "RB34C600ESA has no standalone 4-6 digit token -> competing code check skipped")

# 4-digit LEGO set: 9999 vs different 4-digit 8888
test("sponsored + competing 4-digit code -> SKIP",
     check_sponsored_competing_model(
         True,
         "LEGO Technic 9999",
         "LEGO Technic 9999 Motor Set and 8888 Bonus Building Set"
     ), True,
     "Both 9999 and 8888 are 4-digit codes, competing -> skip")


print("\n=== Fix B3: ASIN consistency correction ===")

test("item_asin == url_asin -> no correction",
     check_asin_mismatch("B0ABCDE1234", "B0ABCDE1234"), "B0ABCDE1234")

test("item_asin != url_asin -> corrects to item_asin",
     check_asin_mismatch("B0ABCDE1234", "B0ZZZZZZ999"), "B0ABCDE1234",
     "item data-asin is authoritative for the result container")

test("item_asin empty -> keep url_asin",
     check_asin_mismatch("", "B0ABCDE1234"), "B0ABCDE1234",
     "no item_asin -> nothing to correct")

test("url_asin empty -> keep empty (handled by skip-no-URL check)",
     check_asin_mismatch("B0ABCDE1234", ""), "B0ABCDE1234",
     "url_asin empty -> item_asin missing means skip triggered upstream")


print("\n=== Regression: accessory fix (Fix A from accessory-fix branch) ===")

test("LED kit rejected (accessory-fix regression check)",
     is_relevant_result("LEGO Harry Potter 76430", "LEGO 76430 LED Lighting Kit Hogwarts Owl Post"),
     False, "LED Lighting Kit must still be rejected")

test("LED light set rejected",
     is_relevant_result("LEGO 76430 Hogwarts", "LocoLee LED Light Set for LEGO 76430 Hogwarts"),
     False)

test("Real LEGO 76430 passes",
     is_relevant_result("LEGO 76430 Hogwarts", "LEGO Harry Potter 76430 Hogwarts Owl Post Building Set"),
     True)

test("iPhone 15 128GB passes",
     is_relevant_result("iPhone 15 128GB", "Apple iPhone 15 128GB Black Smartphone"),
     True)

test("Samsung RB34C600ESA passes",
     is_relevant_result("Samsung RB34C600ESA", "Samsung RB34C600ESA/EF Refrigerator 201cm Silver"),
     True)

test("Sony WH-1000XM5 passes",
     is_relevant_result("Sony WH-1000XM5", "Sony WH-1000XM5 Wireless Noise-Cancelling Headphones"),
     True)

test("PS5 controller passes",
     is_relevant_result("PS5 controller", "Sony PlayStation DualSense PS5 Wireless Controller White"),
     True)

test("Dyson V15 passes",
     is_relevant_result("Dyson V15 Detect", "Dyson V15 Detect Absolute Cordless Vacuum Cleaner"),
     True)


# ── Summary ───────────────────────────────────────────────────────────────────

total = len(results)
passed = sum(1 for r in results if r[0] == PASS)
failed = total - passed

print(f"\n{'='*60}")
print(f"RESULTS: {passed}/{total} PASS, {failed} FAIL")
print(f"{'='*60}")

if failed:
    print("\nFAILED TESTS:")
    for status, name, got, expected, desc in results:
        if status == FAIL:
            print(f"  - {name}")
            print(f"    got={got!r} expected={expected!r}")
            if desc:
                print(f"    note: {desc}")

sys.exit(0 if failed == 0 else 1)
