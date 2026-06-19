"""
Testai: _PRODUCT_TYPE_SIGNALS — produkto tipo nesuderinamumo filtras is_relevant_result viduje.
Tikrina ar netinkami produkto tipai (žaidimai, knygos) filtruojami kai query jų neieško.
"""
import sys
sys.path.insert(0, ".")
from server import is_relevant_result

results = []

def ok(label, got, expected):
    status = "OK" if got == expected else "FAIL"
    results.append((status, label, got, expected))

# ── VAIZDO ŽAIDIMAI — turi būti FILTRUOJAMI ──────────────────────────────

# Pagrindinis bug: LEGO rinkinys vs Nintendo Switch žaidimas
ok("LEGO 76430 vs Nintendo Switch žaidimas",
   is_relevant_result("LEGO 76430 Hogwarts", "LEGO Harry Potter Nintendo Switch"),
   False)

ok("LEGO 76430 vs Playstation 5 žaidimas",
   is_relevant_result("LEGO 76430 Hogwarts", "LEGO Harry Potter Playstation 5"),
   False)

ok("LEGO 76430 vs PS4 žaidimas",
   is_relevant_result("LEGO 76430", "LEGO Marvel For PS4  Collection"),
   False)

ok("LEGO 76430 vs Xbox One žaidimas",
   is_relevant_result("LEGO 76430", "LEGO Worlds Xbox One"),
   False)

ok("iPhone 15 vs iPhone 15 žaidimas Nintendo Switch",
   is_relevant_result("iPhone 15", "iPhone 15 Case Nintendo Switch Game"),
   False)

ok("Sony WH-1000XM5 vs Steam Key žaidimas",
   is_relevant_result("Sony WH-1000XM5", "Sony headset game Steam Key"),
   False)

ok("Samsung Galaxy vs Xbox Series X žaidimas",
   is_relevant_result("Samsung Galaxy S24", "Samsung Xbox Series X game"),
   False)

# ── VAIZDO ŽAIDIMAI — turi PRAEITI (query ieško žaidimo) ─────────────────

ok("Nintendo Switch konsolė — query turi 'nintendo'",
   is_relevant_result("Nintendo Switch", "Nintendo Switch Mario Kart 8"),
   True)

ok("Playstation 5 FIFA — query turi 'playstation'",
   is_relevant_result("FIFA Playstation 5", "FIFA 2024 Playstation 5"),
   True)

ok("Xbox game — query turi 'game'",
   is_relevant_result("Xbox game FIFA 2024", "FIFA 2024 Xbox One"),
   True)

ok("žaidimas Nintendo — LT query",
   is_relevant_result("LEGO žaidimas Nintendo Switch", "LEGO Harry Potter Nintendo Switch"),
   True)

ok("Nintendo Switch konsolė pati — query turi 'switch'",
   is_relevant_result("Nintendo Switch OLED", "Nintendo Switch OLED Console"),
   True)

ok("PC game — query turi 'steam'",
   is_relevant_result("Steam key FIFA", "FIFA 2024 PC Game Steam Key"),
   True)

# ── KNYGOS — turi būti FILTRUOJAMOS ──────────────────────────────────────

ok("LEGO 76430 vs LEGO knyga (LT)",
   is_relevant_result("LEGO 76430 Hogwarts", "LEGO Harry Potter knyga"),
   False)

ok("iPhone 15 vs iPhone knyga",
   is_relevant_result("iPhone 15", "iPhone 15 vadovas knyga"),
   False)

ok("Samsung TV vs Samsung knyga (LT)",
   is_relevant_result("Samsung QE55", "Samsung QE55 instrukcija knyga."),
   False)

ok("LEGO 76430 vs książka (PL)",
   is_relevant_result("LEGO 76430", "LEGO Harry Potter książka,"),
   False)

# ── KNYGOS — turi PRAEITI (query ieško knygos) ────────────────────────────

ok("Knyga query — leidžia knygas",
   is_relevant_result("LEGO knyga", "LEGO Harry Potter knyga"),
   True)

ok("Book query — leidžia knygas",
   is_relevant_result("Harry Potter book", "Harry Potter book illustrated"),
   True)

# ── NORMALŪS PRODUKTAI — neturi būti paveikti ────────────────────────────

ok("Sony WH-1000XM5 ausinės — normalus",
   is_relevant_result("Sony WH-1000XM5", "Sony WH-1000XM5 Wireless Headphones"),
   True)

ok("Samsung Galaxy S24 — normalus",
   is_relevant_result("Samsung Galaxy S24", "Samsung Galaxy S24 5G 256GB"),
   True)

ok("iPhone 15 Pro — normalus",
   is_relevant_result("iPhone 15 Pro", "Apple iPhone 15 Pro 256GB"),
   True)

ok("MacBook Pro — 'book' tekste, bet ne knyga",
   is_relevant_result("MacBook Pro 16", "Apple MacBook Pro 16 M3"),
   True)

ok("Notebook laptop — 'book' tekste, bet ne knyga",
   is_relevant_result("Dell Notebook", "Dell Notebook 15 Intel i7"),
   True)

ok("Dyson V15 — normalus",
   is_relevant_result("Dyson V15", "Dyson V15 Detect Absolute"),
   True)

ok("LEGO rinkinys be žaidimų žymių — normalus",
   is_relevant_result("LEGO 76430 Hogwarts", "LEGO 76430 Hogwarts Castle Building Set"),
   True)

ok("Bosch WAX32 — normalus",
   is_relevant_result("Bosch WAX32EH0", "Bosch WAX32EH0 Washing Machine"),
   True)

# ── REGRESINIAI — ankstesnių fix'ų patikra ───────────────────────────────

ok("Accessory fix: LED kit for LEGO — vis dar filtruojamas",
   is_relevant_result("LEGO 76430", "LED Lighting Kit for LEGO 76430"),
   False)

ok("Sponsored fix: accessory with 'compatible' — vis dar filtruojamas",
   is_relevant_result("Dyson V15", "Replacement Filter compatible with Dyson V15"),
   False)

ok("Brand mismatch — vis dar filtruojamas",
   is_relevant_result("Sony WH-1000XM5", "Samsung Galaxy Buds WH1000XM5 style"),
   False)

# ── REZULTATAI ────────────────────────────────────────────────────────────

print("=" * 60)
passed = sum(1 for s, *_ in results if s == "OK")
failed = sum(1 for s, *_ in results if s == "FAIL")
for status, label, got, expected in results:
    if status == "FAIL":
        print(f"  [FAIL] {label}")
        print(f"         got={got}, expected={expected}")
    else:
        print(f"  [OK] {label}")
print("=" * 60)
print(f"RESULTS: {passed}/{len(results)} PASS, {failed} FAIL")
print("=" * 60)
sys.exit(0 if failed == 0 else 1)
