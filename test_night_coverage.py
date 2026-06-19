"""
Night-tests: expanded coverage for all committed fixes.
Covers: unit filter, accessory filter, buylink, product-type signals,
        query normalization, model code matching.

Run: python test_night_coverage.py
"""
import re
import sys
import os
import io

os.environ.setdefault("SUPABASE_URL", "")
os.environ.setdefault("SUPABASE_KEY", "")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from server import is_relevant_result, _UNIT_TOKEN_RE, normalize_query, _short_amazon_query

# ── Test harness ───────────────────────────────────────────────────────────────

_results = []

def check(name, got, expected, note=""):
    ok = got == expected
    _results.append((ok, name, got, expected))
    tag = "OK" if ok else "FAIL"
    print(f"  [{tag}] {name}")
    if not ok:
        print(f"       got={got!r}  expected={expected!r}")
        if note:
            print(f"       note: {note}")

# ─────────────────────────────────────────────────────────────────────────────
# 1. UNIT TOKEN FILTER (_UNIT_TOKEN_RE)
#    Fix: food/cosmetics queries with weight/volume units (100g, 400ml) should
#    NOT require the exact unit to appear in the product title.
# ─────────────────────────────────────────────────────────────────────────────

print("\n=== 1. Unit token filter (_UNIT_TOKEN_RE) ===")

# Regex must match unit-only tokens
for tok, expected in [
    ("100g",   True),
    ("400ml",  True),
    ("250ml",  True),
    ("800g",   True),
    ("1kg",    True),
    ("2l",     True),
    ("500mg",  True),
    ("30oz",   True),
    ("33cl",   True),
    ("1dl",    True),
    ("50mm",   True),
    ("30cm",   True),
    ("200w",   True),
    ("12v",    True),
    ("60hz",   True),
    ("1500rpm",True),
    ("10pcs",  True),
    ("3st",    True),
    ("6stk",   True),
    ("6er",    True),
    # NOT unit-only — model codes
    ("wh1000xm5",  False),
    ("rb34c600esa", False),
    ("76430",      False),
    ("s24",        False),
    ("128gb",      False),  # digital storage is kept (not unit)
    ("16pro",      False),
]:
    check(f"_UNIT_TOKEN_RE matches '{tok}'", bool(_UNIT_TOKEN_RE.match(tok)), expected)

# is_relevant_result: food query with unit does NOT require unit in title
print("\n  -- is_relevant_result: food/cosmetics units --")

# Milka 100g → "Milka Vollmilch" (no "100g" in title) should match
check("food: Milka 100g matches title without weight",
      is_relevant_result("Milka 100g", "Milka Vollmilch Schokolade"),
      True)

check("food: Nutella 400g matches title without weight",
      is_relevant_result("Nutella 400g", "Nutella Schokoladenaufstrich"),
      True)

check("cosmetics: Dove Shampoo 400ml matches title without volume",
      is_relevant_result("Dove Shampoo 400ml", "Dove Nourishing Shampoo"),
      True)

check("cosmetics: Nivea Creme 250ml matches title without volume",
      is_relevant_result("Nivea Creme 250ml", "Nivea Creme Weiche Haut Pflege"),
      True)

check("baby: Aptamil 800g matches title without weight",
      is_relevant_result("Aptamil Profutura 1 800g", "Aptamil Profutura 1 Säuglingsnahrung"),
      True)

# Unit in query — pcs is a unit token, should not block match
check("baby: Pampers Newborn matches without pack count in title",
      is_relevant_result("Pampers Premium Care Newborn 52pcs", "Pampers Premium Care Newborn"),
      True)

# ─────────────────────────────────────────────────────────────────────────────
# 2. MODEL CODE MATCHING
#    Fix: hyphen normalization so WH-1000XM5 matches "WH1000XM5" in title
# ─────────────────────────────────────────────────────────────────────────────

print("\n=== 2. Model code matching (hyphen normalization) ===")

check("Sony WH-1000XM5 matches compact title",
      is_relevant_result("Sony WH-1000XM5", "Sony WH1000XM5 Kopfhörer"),
      True)

check("Sony WH-1000XM5 exact match",
      is_relevant_result("Sony WH-1000XM5", "Sony WH-1000XM5 Wireless"),
      True)

check("Bosch WAX32EH0 matches exact",
      is_relevant_result("Bosch WAX32EH0", "Bosch WAX32EH0 Waschmaschine"),
      True)

check("Samsung RB34C600ESA matches exact",
      is_relevant_result("Samsung RB34C600ESA", "Samsung RB34C600ESA Kühlschrank"),
      True)

check("LEGO 76430 matches — set number in title",
      is_relevant_result("LEGO 76430", "LEGO Harry Potter 76430 Hogwarts"),
      True)

check("LEGO 76430 rejected — set number NOT in title",
      is_relevant_result("LEGO 76430", "LEGO Harry Potter Hogwarts Castle"),
      False)

check("iPhone 15 Pro 128GB — model tokens matched",
      is_relevant_result("Apple iPhone 15 Pro 128GB", "Apple iPhone 15 Pro 128GB Space Black"),
      True)

check("iPhone 15 Pro rejected — wrong model number in title",
      is_relevant_result("Apple iPhone 15 Pro 128GB", "Apple iPhone 14 Pro 128GB"),
      False)

# ─────────────────────────────────────────────────────────────────────────────
# 3. ACCESSORY FILTER
#    Fix: titles with "for [brand]", compat patterns, accessory words rejected.
# ─────────────────────────────────────────────────────────────────────────────

print("\n=== 3. Accessory filter ===")

# "for X" in title but not query → rejected
check("case 'for iPhone' rejected when not in query",
      is_relevant_result("Apple iPhone 15", "Phone case for iPhone 15 Clear Cover"),
      False)

check("'compatible with' rejected",
      is_relevant_result("Sony WH-1000XM5", "Headphone cable compatible with WH-1000XM5"),
      False)

check("accessory word 'charger' rejected",
      is_relevant_result("Apple iPhone 15", "USB-C Charger for iPhone 15"),
      False)

check("accessory word 'cable' rejected",
      is_relevant_result("Apple iPhone 15", "Lightning Cable for iPhone 15"),
      False)

check("accessory word 'screen protector' rejected",
      is_relevant_result("Samsung Galaxy S24", "Screen protector for Samsung S24"),
      False)

# Real product — no accessory signals → accepted
check("Sony WH-1000XM5 real product accepted",
      is_relevant_result("Sony WH-1000XM5", "Sony WH-1000XM5 Over-Ear Wireless"),
      True)

# Query itself includes accessory word AND title has no "for X" pattern
check("case query + case in title (no for-X pattern) = user wants case",
      is_relevant_result("iPhone 15 case", "iPhone 15 Protective Case Premium"),
      True)

# ─────────────────────────────────────────────────────────────────────────────
# 4. PRODUCT-TYPE SIGNALS (gaming platform filter)
#    Fix from type-filter branch: reject gaming platform titles when query
#    isn't about games. Logic tested inline (not yet merged to this branch).
# ─────────────────────────────────────────────────────────────────────────────

print("\n=== 4. Product-type signals (inline logic test) ===")

_PRODUCT_TYPE_SIGNALS = [
    (
        {"nintendo switch", "for nintendo switch", "nintendo ds", "nintendo 3ds",
         "playstation 4", "playstation 5", "for ps4 ", "for ps5 ",
         "xbox one", "xbox series x", "xbox series s", "pc game", "steam key"},
        {"nintendo", "switch", "playstation", "ps4", "ps5", "xbox",
         "game", "žaidimas", "spiel", "gra", "steam"},
    ),
    (
        {" knyga", "knyga,", "knyga.", "knyga:", " książka", "książka,"},
        {"knyga", "book", "buch", "livre", "książka"},
    ),
]

def type_filter_check(query: str, title: str) -> bool:
    q = query.lower()
    t = title.lower()
    for type_title_sigs, type_query_sigs in _PRODUCT_TYPE_SIGNALS:
        if any(sig in t for sig in type_title_sigs):
            if not any(sig in q for sig in type_query_sigs):
                return False
    return True

# LEGO set query → Nintendo Switch game title → REJECT
check("LEGO 76430 vs Nintendo Switch game → rejected",
      type_filter_check("LEGO 76430 Hogwarts", "LEGO Harry Potter 76430 Nintendo Switch"),
      False)

check("LEGO 76430 vs PS4 game → rejected",
      type_filter_check("LEGO 76430 Hogwarts", "LEGO Harry Potter PS4 Playstation 4"),
      False)

check("LEGO 76430 vs Xbox One game → rejected",
      type_filter_check("LEGO 76430 Hogwarts", "LEGO Harry Potter Xbox One"),
      False)

check("LEGO 76430 vs PC game → rejected",
      type_filter_check("LEGO 76430 Hogwarts", "LEGO Harry Potter PC Game Steam Key"),
      False)

# Legit game query → Nintendo Switch title → ALLOW
check("Nintendo Switch game query → Switch title → allowed",
      type_filter_check("Nintendo Switch žaidimas FIFA", "FIFA 2024 Nintendo Switch"),
      True)

check("PS5 game query → Playstation 5 title → allowed",
      type_filter_check("FIFA Playstation 5", "FIFA 2024 Playstation 5"),
      True)

# LEGO set with no gaming signals → real LEGO title → ALLOW
check("LEGO 76430 vs correct LEGO set title → allowed",
      type_filter_check("LEGO 76430 Hogwarts", "LEGO Harry Potter Hogwarts 76430 Building Set"),
      True)

# MacBook/Notebook — should NOT be blocked by book filter
check("MacBook Pro → not blocked by book filter",
      type_filter_check("MacBook Pro 14", "Apple MacBook Pro 14 M3"),
      True)

# LT book query vs real book → allow
check("LT book query vs knyga title → allowed",
      type_filter_check("Atomines paradai knyga", "Atomines paradai knyga James Clear"),
      True)

# LT book query vs product title → reject
check("non-book query vs knyga title → rejected",
      type_filter_check("Apple iPhone 15", "Apple iPhone knyga vadovas"),
      False)

# ─────────────────────────────────────────────────────────────────────────────
# 5. QUERY NORMALIZATION
#    Fix: shopping-intent noise words stripped from query.
# ─────────────────────────────────────────────────────────────────────────────

print("\n=== 5. Query normalization ===")

check("'kur pirkti' stripped",
      normalize_query("kur pirkti iPhone 16"),
      "iPhone 16")

check("'buy cheap' stripped",
      normalize_query("buy cheap Samsung Galaxy S24"),
      "Samsung Galaxy S24")

check("'pigiausias' stripped",
      normalize_query("pigiausias iPhone 15 128GB"),
      "iPhone 15 128GB")

check("'review' stripped",
      normalize_query("Samsung Galaxy S24 review"),
      "Samsung Galaxy S24")

check("normal query unchanged",
      normalize_query("Sony WH-1000XM5"),
      "Sony WH-1000XM5")

check("leading/trailing whitespace stripped",
      normalize_query("  LEGO 76430  "),
      "LEGO 76430")

check("trailing punctuation stripped",
      normalize_query("iPhone 15."),
      "iPhone 15")

check("empty query returns empty",
      normalize_query(""),
      "")

check("noise-only query preserved (never return empty after stripping)",
      len(normalize_query("kur pirkti")) > 0,
      True)

# ─────────────────────────────────────────────────────────────────────────────
# 6. SHORT AMAZON QUERY — model code preservation
# ─────────────────────────────────────────────────────────────────────────────

print("\n=== 6. _short_amazon_query: model code preservation ===")

# LEGO set number must survive shortening
lego_q = "LEGO Harry Potter Hogwarts Owl Post Bird 76430 Building Set for Kids"
lego_short = _short_amazon_query(lego_q)
check("LEGO 76430 set number preserved after shortening",
      "76430" in lego_short,
      True)

check("LEGO brand preserved after shortening",
      "LEGO" in lego_short or "lego" in lego_short.lower(),
      True)

# Samsung model code
samsung_q = "Samsung RB34C600ESA Refrigerator 201cm Silver"
samsung_short = _short_amazon_query(samsung_q)
check("Samsung model code preserved after shortening",
      "RB34C600" in samsung_short or "RB34C600ESA" in samsung_short,
      True)

# Short query should not be truncated further
short_q = "Sony WH-1000XM5"
check("short query not over-truncated",
      "WH-1000XM5" in _short_amazon_query(short_q) or "WH1000XM5" in _short_amazon_query(short_q),
      True)

# ─────────────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────────────

total = len(_results)
passed = sum(1 for ok, *_ in _results if ok)
failed = total - passed

print(f"\n{'='*60}")
print(f"RESULTS: {passed}/{total} PASS  {failed} FAIL")
print(f"{'='*60}")

if failed:
    print("\nFAILED:")
    for ok, name, got, expected in _results:
        if not ok:
            print(f"  - {name}")
            print(f"    got={got!r}  expected={expected!r}")

sys.exit(0 if failed == 0 else 1)
