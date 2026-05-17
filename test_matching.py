import re, sys, io

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf-8-sig'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

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
_ACCESSORY_WORDS = frozenset({
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
    'ersatz', 'zubehör', 'filter',
})

_VARIANT_WORDS = frozenset({
    'pro', 'max', 'ultra', 'plus', 'lite', 'mini', 'fe', 'edge',
    'note', 'fold', 'flip', 'air', 'neo', 'active', 'sport',
})

def _normalize_units(text):
    return re.sub(
        r'(\d+)\s+(gb|tb|mb|mp|mah|hz|mhz|ghz)\b',
        lambda m: m.group(1) + m.group(2),
        text.lower()
    )

def is_relevant_result(original_query, product_title):
    if not product_title or not original_query:
        return False
    q = _normalize_units(original_query)
    t = _normalize_units(product_title)
    for acc in _ACCESSORY_WORDS:
        if acc in t and acc not in q:
            return False
    brands_in_query = [b for b in _KNOWN_BRANDS if b in q]
    for brand in brands_in_query:
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

def run(label, query, tests):
    print(f"\n{'='*60}")
    print(f"  Query: {query!r}  [{label}]")
    print(f"{'='*60}")
    fails = 0
    for title, expected in tests:
        result = is_relevant_result(query, title)
        ok = result == expected
        if not ok:
            fails += 1
        tag = 'OK  ' if ok else 'FAIL'
        show = 'SHOW' if result else 'HIDE'
        exp  = 'SHOW' if expected else 'HIDE'
        mark = '' if ok else '  ← MISMATCH'
        print(f"  [{tag}] {show} (exp {exp}): {title}{mark}")
    return fails

total_fails = 0

# ── iPhone 17 Pro 256GB ────────────────────────────────────────
total_fails += run("telefonas", "iPhone 17 Pro 256GB", [
    # Teisingi produktai → SHOW
    ("Apple iPhone 17 Pro 256GB Black Titanium",        True),
    ("Apple iPhone 17 Pro 256GB Natural Titanium",      True),
    ("iPhone 17 Pro 256 GB Smartphone",                 True),   # tarpas tarp "256 GB"
    ("Apple iPhone 17 Pro 256GB – Black",               True),

    # Neteisingas saugojimas → HIDE
    ("Apple iPhone 17 Pro 512GB",                       False),
    ("Apple iPhone 17 Pro 128GB Black",                 False),

    # Aksesuarai → HIDE
    ("Case for iPhone 17 Pro 256GB - silicone",         False),
    ("Etui na iPhone 17 Pro silikonowe",                False),
    ("iPhone 17 Pro tempered glass screen protector",   False),
    ("Silicone Cover iPhone 17 Pro",                    False),
    ("Apple iPhone 17 Pro 256GB Charging Cable",        False),
    ("Schutzhülle für iPhone 17 Pro 256GB",             False),
    ("iPhone 17 Pro Screen Protector Film",             False),
    ("Dėklas iPhone 17 Pro 256GB skaidrus",             False),
    ("Kroviklis iPhone 17 Pro 20W",                     False),
    ("Szkło hartowane iPhone 17 Pro 256GB",             False),
])

# ── Samsung Galaxy S24 Ultra 512GB ────────────────────────────
total_fails += run("telefonas", "Samsung Galaxy S24 Ultra 512GB", [
    ("Samsung Galaxy S24 Ultra 512GB Titanium Black",   True),
    ("Samsung Galaxy S24 Ultra 512 GB Gray",            True),

    ("Samsung Galaxy S24 Ultra 256GB",                  False),  # blogas storage
    ("Samsung Galaxy S24 Plus 512GB",                   False),  # kitas modelis
    ("Case Samsung Galaxy S24 Ultra",                   False),
    ("Etui Samsung S24 Ultra 512GB",                    False),
    ("Samsung Galaxy S24 Ultra Charger 45W",            False),
    ("Tempered glass Samsung S24 Ultra",                False),
])

# ── Sony WH-1000XM5 ───────────────────────────────────────────
total_fails += run("ausinės", "Sony WH-1000XM5", [
    ("Sony WH-1000XM5 Wireless Noise Cancelling Headphones Black",  True),
    ("Sony WH-1000XM5 Silver",                          True),

    ("Sony WH-1000XM4",                                 False),  # kitas modelis
    ("Case for Sony WH-1000XM5",                        False),
    ("Sony WH-1000XM5 Cable USB-C",                     False),
    ("Earpad Replacement Sony WH-1000XM5",              False),
])

# ── MacBook Pro 14 M4 ─────────────────────────────────────────
total_fails += run("laptop", "MacBook Pro 14 M4", [
    ("Apple MacBook Pro 14 M4 16GB 512GB Silver",       True),
    ("Apple MacBook Pro 14-inch M4 Space Black",        True),

    ("MacBook Pro 13 M4",                               False),  # kitas dydis
    ("MacBook Pro 14 M3",                               False),  # kitas chip
    ("Case MacBook Pro 14 M4",                          False),
    ("Sleeve for MacBook Pro 14",                       False),
    ("USB-C Hub MacBook Pro 14 M4",                     False),
])

# ── Dyson V15 Detect ──────────────────────────────────────────
total_fails += run("siurblys", "Dyson V15 Detect", [
    ("Dyson V15 Detect Absolute Vacuum Cleaner",        True),
    ("Dyson V15 Detect Extra",                          True),

    ("Dyson V12 Detect",                                False),  # kitas modelis
    ("Dyson V15 Detect Replacement Filter",             False),
    ("Dyson V15 Detect Charger",                        False),
])

# ── trumpi užklausos ──────────────────────────────────────────
total_fails += run("trumpas", "iPhone 17", [
    ("Apple iPhone 17 128GB Black",                     True),
    ("Apple iPhone 17 Pro 256GB",                       True),   # Pro taip pat tinka "iPhone 17"

    ("Case iPhone 17",                                  False),
    ("iPhone 17 Tempered Glass",                        False),
])

print(f"\n{'='*60}")
if total_fails == 0:
    print("  ✅  Visi testai praėjo!")
else:
    print(f"  ❌  {total_fails} testai nepraėjo!")
print(f"{'='*60}\n")
