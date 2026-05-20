import sys, io, os

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf-8-sig'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

os.environ.setdefault('SUPABASE_URL', '')
os.environ.setdefault('SUPABASE_KEY', '')
from server import validate_price, parse_price

fails = 0

def chk(label, price, query, expected_pass: bool):
    global fails
    result = validate_price(price, query)
    ok = bool(result) == expected_pass
    if not ok:
        fails += 1
    tag = "OK  " if ok else "FAIL"
    verdict = f"PASS ({result:.2f}€)" if result else "REJECT"
    exp = "PASS" if expected_pass else "REJECT"
    mark = "" if ok else "  ← MISMATCH"
    print(f"  [{tag}] {verdict} (exp {exp}): {query!r} @ {price}€{mark}")

print("\n" + "="*60)
print("  validate_price — sanity checks")
print("="*60)

# ── Global limits ──
chk("ceiling",      60_000, "anything",          False)  # > 50k → reject
chk("zero",         0,      "anything",           False)
chk("negative",    -5,      "anything",           False)
chk("sub-50cent",   0.3,    "anything",           False)

# ── TVs with sizes ──
chk("tv55 ok",      549,    "Samsung TV 55",      True)
chk("tv65 ok",      799,    "LG OLED 65 tv",      True)
chk("tv55 cheap",   49,     "Samsung tv 55",      False)  # TV 55" for €49 → nonsense
chk("tv65 cheap",   9.99,   "Sony tv 65",         False)
chk("tv no size ok",120,    "tv samsung",         True)
chk("tv no size low",2,     "televizorius",       False)

# ── MacBook ──
chk("macbook ok",   1349,   "MacBook Air M3",     True)
chk("macbook ok2",  699,    "MacBook refurb",     True)
chk("macbook cheap",49,     "MacBook Air M3",     False)
chk("macbook cheap2",1,     "MacBook Pro 14",     False)

# ── iPhone ──
chk("iphone ok",    1049,   "iPhone 16 Pro",      True)
chk("iphone ok2",   219,    "iPhone SE",          True)
chk("iphone cheap", 9.99,   "iPhone 16 Pro",      False)
chk("iphone cheap2",0.5,    "iPhone case",        False)

# ── Samsung Galaxy (no iPhone rule — passes) ──
chk("samsung ok",   749,    "Samsung Galaxy S24", True)
chk("samsung low",  1.50,   "Samsung Galaxy S24", False)  # Samsung Galaxy floor = €50

# ── AirPods / headphones (no strict floor) ──
chk("airpods ok",   219,    "AirPods Pro",        True)
chk("airpods cheap",5,      "AirPods Pro",        True)   # no AirPods floor rule

# ── Washing machines ──
chk("washing ok",   449,    "Bosch skalbyklė",    True)
chk("washing cheap",49,     "Bosch skalbyklė",    False)
chk("washing ok2",  599,    "Bosch washing machine",True)
chk("washing cheap2",10,    "washing machine",    False)

# ── Fridges ──
chk("fridge ok",    399,    "Samsung šaldytuvas", True)
chk("fridge cheap", 30,     "Samsung šaldytuvas", False)

# ── Laptop (non-MacBook) — floor €80 ──
chk("laptop ok",    299,    "Asus VivoBook laptop",  True)
chk("laptop ok2",   89,     "Chromebook Lenovo",     True)   # €89 > €80 floor
chk("laptop cheap", 49,     "laptop Dell",           False)  # €49 < €80
chk("laptop cheap2", 1,     "notebook Lenovo",       False)
chk("thinkpad ok",  699,    "ThinkPad X1 Carbon",    True)
chk("thinkpad cheap",30,    "ThinkPad E14",          False)

# ── Air conditioner — floor €150 ──
chk("aircon ok",    599,    "oro kondicionierius Samsung", True)
chk("aircon ok2",   199,    "air conditioner Daikin",      True)   # €199 > €150
chk("aircon cheap", 99,     "air conditioner LG",          False)  # €99 < €150
chk("aircon cheap2",49,     "klimaanlage Bosch",           False)
chk("aircon cheap3",149,    "klimatyzator Samsung",        False)  # €149 < €150
chk("aircon lt ok", 399,    "kondicionierius Samsung",     True)   # standalone LT word
chk("aircon lt bad",99,     "kondicionierius Samsung",     False)  # standalone LT word, too cheap

# ── Dishwasher (in _WASHING_W via indaplovė/dishwasher) ──
chk("dishwasher ok",  449,  "indaplovė Bosch",     True)
chk("dishwasher ok2", 299,  "dishwasher Samsung",  True)
chk("dishwasher cheap",49,  "dishwasher Whirlpool",False)
chk("dishwasher cheap2",9,  "indaplovė Electrolux",False)

# ── Freezer (in _FRIDGE_W via šaldiklis/gefrierschrank) ──
chk("freezer ok",   299,    "šaldiklis Samsung",    True)
chk("freezer ok2",  199,    "zamrażarka Bosch",     True)
chk("freezer cheap", 49,    "gefrierschrank Bosch", False)
chk("freezer cheap2",30,    "šaldiklis Electrolux", False)

# ── Normal accessories — should pass ──
chk("shaver ok",    35,     "Philips skustuvas",  True)
chk("shaver ok2",   79,     "Philips shaver",     True)
chk("cable ok",     9.99,   "USB-C cable 2m",     True)
chk("lamp ok",      12,     "Philips lemputė",    True)

# ── parse_price integration ──
print("\n" + "="*60)
print("  parse_price + validate_price — real text samples")
print("="*60)

def chk_text(label, text, query, expected_pass: bool, approx: float = 0):
    global fails
    price = validate_price(parse_price(text), query)
    ok = bool(price) == expected_pass
    if ok and approx and price:
        ok = abs(price - approx) < approx * 0.1  # within 10%
        if not ok:
            fails += 1
    if not (bool(price) == expected_pass):
        fails += 1
        ok = False
    tag = "OK  " if ok else "FAIL"
    verdict = f"PASS ({price:.2f}€)" if price else "REJECT"
    exp = f"PASS ~{approx}€" if (expected_pass and approx) else ("PASS" if expected_pass else "REJECT")
    mark = "" if ok else "  ← MISMATCH"
    print(f"  [{tag}] {verdict} (exp {exp}): {text!r} for {query!r}{mark}")

chk_text("macbook eur",  "1 349,00 €",    "MacBook Air M3",   True,  1349)
chk_text("iphone eur",   "1 049,00€",     "iPhone 16 Pro",    True,  1049)
chk_text("samsung eur",  "749.99 EUR",    "Samsung S24",      True,  749.99)
chk_text("airpods eur",  "219,00 €",      "AirPods Pro",      True,  219)
chk_text("shaver eur",   "49,90 €",       "Philips skustuvas",True,  49.90)
chk_text("tv garbage",   "1.99",          "Samsung TV 55",    False)
chk_text("above50k",     "99999 €",       "anything",         False)
chk_text("pln macbook",  "5 799 zł",      "MacBook Air M3",   True)  # PLN — passes parse_price

print(f"\n{'='*60}")
if fails == 0:
    print("  Visi testai praejo!")
else:
    print(f"  {fails} testai nepraejo!")
print(f"{'='*60}\n")
