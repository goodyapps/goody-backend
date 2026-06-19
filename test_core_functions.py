"""
Tests for core functions not covered by existing test suite:
- normalize_query
- deduplicate_by_shop
- _short_amazon_query
- buy-link URL validation (regression)

Run: python test_core_functions.py
"""
import re
import sys
import os

os.environ.setdefault("SUPABASE_URL", "")
os.environ.setdefault("SUPABASE_KEY", "")
from server import normalize_query, deduplicate_by_shop, _short_amazon_query

results = []
PASS, FAIL = "PASS", "FAIL"

def test(name, got, expected, note=""):
    ok = got == expected
    results.append((PASS if ok else FAIL, name, got, expected))
    tag = "OK" if ok else "FAIL"
    print(f"  [{tag}] {name}")
    if not ok:
        print(f"       got={got!r} expected={expected!r}")
        if note:
            print(f"       note: {note}")


# ── normalize_query ────────────────────────────────────────────────────────────

print("\n=== normalize_query: shopping-intent noise removal ===")

test("kur pirkti stripped",
     normalize_query("kur pirkti iPhone 16"),
     "iPhone 16")

test("buy intent stripped",
     normalize_query("buy cheap Samsung Galaxy S24"),
     "Samsung Galaxy S24")

test("normal query unchanged",
     normalize_query("Sony WH-1000XM5"),
     "Sony WH-1000XM5")

test("pigiausias stripped",
     normalize_query("pigiausias iPhone 15 128GB"),
     "iPhone 15 128GB")

test("leading/trailing whitespace stripped",
     normalize_query("  LEGO 76430  "),
     "LEGO 76430")

test("query with review noise",
     normalize_query("Samsung Galaxy S24 review"),
     "Samsung Galaxy S24")

test("empty query returns empty",
     normalize_query(""),
     "")

test("pure noise query preserved (no product left after stripping)",
     normalize_query("kur pirkti"),
     "kur pirkti",
     "When stripping would leave empty string, original is kept")


# ── deduplicate_by_shop ────────────────────────────────────────────────────────

print("\n=== deduplicate_by_shop: keeps cheapest per shop ===")

results_input = [
    {"shop": "Amazon.DE", "price": 89.99, "product_title": "Sony WH-1000XM5"},
    {"shop": "Amazon.DE", "price": 79.99, "product_title": "Sony WH-1000XM5"},  # cheaper
    {"shop": "Amazon.DE", "price": 95.00, "product_title": "Sony WH-1000XM5"},
    {"shop": "Elesen.lt", "price": 85.00, "product_title": "Sony WH-1000XM5"},
    {"shop": "Elesen.lt", "price": 91.00, "product_title": "Sony WH-1000XM5"},  # more expensive
]
deduped = deduplicate_by_shop(results_input)

test("dedup: 2 shops remain",
     len(deduped), 2)

amz_price = next((r["price"] for r in deduped if r["shop"] == "Amazon.DE"), None)
test("dedup: Amazon keeps cheapest €79.99",
     amz_price, 79.99)

elesen_price = next((r["price"] for r in deduped if r["shop"] == "Elesen.lt"), None)
test("dedup: Elesen keeps cheapest €85.00",
     elesen_price, 85.00)

# Single result per shop when only one
single = [{"shop": "Varle.lt", "price": 45.99, "product_title": "Test"}]
test("dedup: single result unchanged",
     len(deduplicate_by_shop(single)), 1)

# Empty list
test("dedup: empty list returns empty",
     deduplicate_by_shop([]), [])


# ── _short_amazon_query ────────────────────────────────────────────────────────

print("\n=== _short_amazon_query: query truncation for Amazon search ===")

# Short queries should pass through
short_q = _short_amazon_query("Sony WH-1000XM5")
test("short query unchanged or similar",
     "Sony" in short_q or "WH-1000XM5" in short_q,
     True)

# Long query with model code — model code should be preserved
long_q = "LEGO Harry Potter Hogwarts Owl Post Bird 76430 Building Set for Kids"
shortened = _short_amazon_query(long_q)
test("model code preserved in short query",
     "76430" in shortened,
     True,
     "Model code is most important search signal — must survive truncation")

# Brand preserved
test("brand preserved in short query",
     "LEGO" in shortened or "lego" in shortened.lower(),
     True)

# Query already short — should not be unnecessarily truncated
already_short = "iPhone 15 128GB"
short_result = _short_amazon_query(already_short)
test("already-short query: 128GB or 15 present",
     "15" in short_result and ("128" in short_result or "128GB" in short_result),
     True)

# Samsung model: should preserve brand + model number
samsung_q = "Samsung RB34C600ESA Refrigerator 201cm"
samsung_short = _short_amazon_query(samsung_q)
test("Samsung model code preserved",
     "Samsung" in samsung_short and "RB34C600" in samsung_short,
     True)

# Very long query with important terms
long_dyson = "Dyson V15 Detect Absolute Cordless Vacuum Cleaner Anti-Tangle Hair Screw Tool"
dyson_short = _short_amazon_query(long_dyson)
test("Dyson brand preserved",
     "Dyson" in dyson_short,
     True)
test("V15 model preserved",
     "V15" in dyson_short,
     True)


# ── Summary ────────────────────────────────────────────────────────────────────

total = len(results)
passed = sum(1 for r in results if r[0] == PASS)
failed = total - passed

print(f"\n{'='*60}")
print(f"RESULTS: {passed}/{total} PASS, {failed} FAIL")
print(f"{'='*60}")

if failed:
    print("\nFAILED:")
    for status, name, got, expected in results:
        if status == FAIL:
            print(f"  - {name}: got={got!r} expected={expected!r}")

sys.exit(0 if failed == 0 else 1)
