"""
DIAGNOSTINIS SKRIPTAS: Elesen.lt wrong-product root cause
Ieško tikslios priežasties (A/B/C iš ELESEN_MATCH_DEBUG.md):
  A = Elesen kataloge "76430" priskirtas žaidimui
  B = Fix A1 (empty-URL skip) numetė tikrą rinkinį
  C = is_relevant_result atmeta viską → or all_results fallback
"""

import sys
import io
import re
import json
import requests
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# --- Importuojam iš server.py tikslias funkcijas ---
sys.path.insert(0, ".")
from server import (
    normalize_query,
    is_relevant_result,
    _extract_spa_products,
    _scrape_elesen_from_html,
    _walk_for_products,
    fetch_url,
    get_headers,
    _http,
    validate_price,
    parse_price,
    _make_result,
)

QUERY = "LEGO 76430 Hogwarts"
BASE_URL = "https://www.elesen.lt"
URL = f"{BASE_URL}/paieska?q={requests.utils.quote(QUERY)}"

print("=" * 70)
print(f"ELESEN LIVE DIAGNOSTIC: '{QUERY}'")
print(f"URL: {URL}")
print("=" * 70)

# ── 1. Fetch HTML (tiksliai kaip scrape_elesen) ──────────────────────────
print("\n[1] Fetching Elesen HTML...")
resp = None
try:
    resp = _http.get(URL, headers=get_headers("lt"), timeout=2, allow_redirects=True)
    if resp.status_code != 200:
        print(f"    Direct: {resp.status_code} - pereisim prie ScraperAPI")
        resp = None
    else:
        print(f"    Direct: 200 OK ({len(resp.text)} chars)")
except Exception as e:
    print(f"    Direct failed: {e}")

if not resp:
    print("    Bandau ScraperAPI render_js=True...")
    resp = fetch_url(URL, "lt", render_js=True, scraper_timeout=15)
    if resp and resp.status_code == 200:
        print(f"    ScraperAPI: 200 OK ({len(resp.text)} chars)")
    else:
        print(f"    ScraperAPI: FAILED {resp.status_code if resp else 'no resp'}")
        sys.exit(1)

html = resp.text

# ── 2. SPA kelias: žaliaviniai duomenys ─────────────────────────────────
print("\n[2] SPA JSON analizė (prieš is_relevant_result filtrą)...")

class RawCapture:
    """_walk_for_products wrapper — fiksuoja VISKĄ prieš filtrus."""
    def __init__(self):
        self.all_nodes = []

    def walk_raw(self, node, depth=0):
        if depth > 15 or len(self.all_nodes) >= 30:
            return
        if isinstance(node, dict):
            name = (node.get("name") or node.get("title") or node.get("productName")
                    or node.get("fullName") or node.get("Product_name")
                    or node.get("product_name") or node.get("displayName")
                    or node.get("short_name") or node.get("label")
                    or node.get("productTitle") or node.get("itemName")
                    or node.get("item_name") or node.get("heading")
                    or node.get("headline") or "")
            price_val = None
            for pf in ("price", "finalPrice", "priceWithVat", "currentPrice",
                       "salePrice", "regularPrice", "Price", "priceValue",
                       "discountedPrice", "listPrice", "basePrice", "priceIncVat",
                       "sellingPrice", "selling_price", "specialPrice", "special_price",
                       "promotionalPrice", "effectivePrice"):
                if pf in node:
                    price_val = node[pf]; break
            if price_val is None and isinstance(node.get("prices"), dict):
                price_val = (node["prices"].get("final") or node["prices"].get("regular")
                             or node["prices"].get("current") or node["prices"].get("priceWithVat"))
            if price_val is None and isinstance(node.get("price"), dict):
                price_val = node["price"].get("amount") or node["price"].get("value")
            if price_val is None and isinstance(node.get("priceFormatted"), str):
                price_val = parse_price(node["priceFormatted"]) or None

            if name and price_val is not None:
                try:
                    p = float(str(price_val).replace(",", "."))
                    if p > 0:
                        slug = (node.get("url") or node.get("slug") or
                                node.get("urlKey") or node.get("url_key") or
                                node.get("link") or node.get("href") or
                                node.get("productUrl") or node.get("product_url") or
                                node.get("canonical") or node.get("pageUrl") or
                                node.get("detailUrl") or node.get("productLink") or
                                node.get("itemUrl") or node.get("path") or "")
                        link = slug if slug.startswith("http") else f"{BASE_URL.rstrip('/')}/{slug.lstrip('/')}" if slug else ""
                        # Extra ID/barcode fields
                        barcode = (node.get("ean") or node.get("barcode") or node.get("gtin")
                                   or node.get("sku") or node.get("id") or node.get("productId") or "")
                        self.all_nodes.append({
                            "name": str(name)[:120],
                            "price": p,
                            "slug": slug or "(TUŠČIAS)",
                            "link": link or "(NĖRA URL)",
                            "barcode": str(barcode) if barcode else "",
                        })
                except (ValueError, TypeError):
                    pass
            for v in node.values():
                self.walk_raw(v, depth + 1)
        elif isinstance(node, list):
            for item in node[:40]:
                self.walk_raw(item, depth + 1)

soup = BeautifulSoup(html, "html.parser")
capture = RawCapture()

# Bandome visus SPA JSON šaltinius
spa_found = False
nd = soup.find("script", {"id": "__NEXT_DATA__"})
if nd:
    try:
        capture.walk_raw(json.loads(nd.string or "{}"))
        if capture.all_nodes:
            print(f"    SPA šaltinis: __NEXT_DATA__ ({len(capture.all_nodes)} žaliaviniai)")
            spa_found = True
    except Exception as e:
        print(f"    __NEXT_DATA__ parse error: {e}")

if not spa_found:
    nd3 = soup.find("script", {"id": "__NUXT_DATA__"})
    if nd3:
        try:
            raw3 = json.loads(nd3.string or "[]")
            node3 = raw3 if isinstance(raw3, dict) else {"items": raw3}
            capture.walk_raw(node3)
            if capture.all_nodes:
                print(f"    SPA šaltinis: __NUXT_DATA__ ({len(capture.all_nodes)} žaliaviniai)")
                spa_found = True
        except Exception as e:
            print(f"    __NUXT_DATA__ parse error: {e}")

if not spa_found:
    print("    SPA JSON nerastas — bus naudojamas DOM kelias")

# ── 3. Spausdinti VISUS žaliavinius SPA rezultatus ──────────────────────
print(f"\n[3] VISI žaliaviniai SPA produktai (iki filtrų) — {len(capture.all_nodes)} vnt:")
print("-" * 70)
for i, n in enumerate(capture.all_nodes, 1):
    has_76430_name = "76430" in n["name"]
    has_76430_link = "76430" in n["link"]
    empty_url = n["slug"] == "(TUŠČIAS)" or not n["slug"]
    is_game = any(kw in n["name"].lower() for kw in ["nintendo", "switch", "ps4", "ps5", "xbox", "žaidimas", "game"])
    is_set  = any(kw in n["name"].lower() for kw in ["76430", "hogwarts", "pilis", "castle"])

    flags = []
    if has_76430_name: flags.append("⚠️  TURI '76430' PAVADINIME")
    if empty_url: flags.append("🔴 TUŠČIAS URL → Fix A1 numestų")
    if is_game: flags.append("🎮 ŽAIDIMAS")
    if is_set:  flags.append("🧱 RINKINYS?")

    print(f"  #{i}: {n['name']}")
    print(f"       Kaina: €{n['price']:.2f}")
    print(f"       Slug:  {n['slug'][:80]}")
    print(f"       URL:   {n['link'][:80]}")
    if n['barcode']:
        print(f"       ID/EAN:{n['barcode']}")
    if flags:
        print(f"       >>>    {' | '.join(flags)}")
    print()

# ── 4. DOM kelias: žaliaviniai duomenys ─────────────────────────────────
print("[4] DOM kelias (HTML product-card elementai)...")
dom_items = (
    soup.select("article.product-card") or
    soup.select(".product-card.vertical") or
    soup.select(".product-card") or
    soup.select("[class*='product-item']") or
    soup.select("[class*='catalog-item']") or
    soup.select(".item-box") or
    soup.select("[data-product-id]")
)
print(f"    Rasta {len(dom_items)} DOM kortelių")

dom_raw = []
for item in dom_items[:10]:
    price_el = item.select_one(".price") or item.select_one("[class*='price']")
    price_text = price_el.get_text() if price_el else ""
    raw_price = parse_price(price_text) if price_text else None
    name_el = (item.select_one(".product-card__title") or item.select_one(".product_name")
               or item.select_one("[class*='name']") or item.select_one("h2") or item.select_one("h3"))
    name = name_el.get_text(strip=True)[:100] if name_el else "(NĖRA PAVADINIMO → fallback į query)"
    link_el = item.select_one("a[href]")
    href = link_el["href"] if link_el else ""
    link = href if href.startswith("http") else f"{BASE_URL}{href}" if href else ""
    dom_raw.append({"name": name, "price": raw_price, "href": href, "link": link})

print("-" * 70)
for i, d in enumerate(dom_raw, 1):
    has_76430 = "76430" in d["name"]
    empty_url = not d["href"] or d["href"] in ("/", "#")
    is_game = any(kw in d["name"].lower() for kw in ["nintendo", "switch", "ps4", "ps5", "xbox", "žaidimas"])
    flags = []
    if has_76430: flags.append("⚠️  TURI '76430'")
    if empty_url: flags.append("🔴 TUŠČIAS URL")
    if is_game:   flags.append("🎮 ŽAIDIMAS")
    print(f"  DOM #{i}: {d['name']}")
    print(f"           Kaina: {d['price']}")
    print(f"           href:  {d['href'][:80] if d['href'] else '(TUŠČIAS)'}")
    if flags:
        print(f"           >>>   {' | '.join(flags)}")
    print()

# ── 5. is_relevant_result filtras ────────────────────────────────────────
print("[5] is_relevant_result filtro rezultatai (SPA žaliaviniai):")
print("-" * 70)
passed = []
blocked = []
for n in capture.all_nodes:
    result = is_relevant_result(QUERY, n["name"])
    if result:
        passed.append(n)
        print(f"  ✅ PRAEINA: {n['name'][:70]}")
    else:
        blocked.append(n)
        print(f"  ❌ BLOKUOJA: {n['name'][:70]}")

print(f"\n    Praeina: {len(passed)}, Blokuojama: {len(blocked)}")
if len(passed) == 0 and len(capture.all_nodes) > 0:
    print("  ⚠️  VISI filtruoti → 'or all_results' fallback → PRIEŽASTIS C")

# ── 6. Oficialus scrape_elesen rezultatas ────────────────────────────────
print("\n[6] Oficialus scrape_elesen() rezultatas (kaip Goody jį mato):")
print("-" * 70)
from server import scrape_elesen
official = scrape_elesen(QUERY)
print(f"    Grąžinta {len(official)} rezultatų")
for i, r in enumerate(official, 1):
    title = r.get("product_title", "?")
    price = r.get("price", "?")
    url   = r.get("url", "?")
    has_76430_title = "76430" in title
    has_76430_url   = "76430" in url
    is_game = any(kw in title.lower() for kw in ["nintendo", "switch", "žaidimas", "game", "harry potter"])
    flags = []
    if has_76430_title: flags.append("'76430' pavadinime")
    if has_76430_url:   flags.append("'76430' URL")
    if is_game:         flags.append("🎮 ŽAIDIMAS")
    if not has_76430_title and not has_76430_url:
        flags.append("❌ '76430' NĖRA nei pavadinime, nei URL")
    print(f"  #{i}: {title}")
    print(f"       Kaina: €{price}")
    print(f"       URL:   {url}")
    if flags:
        print(f"       >>>   {' | '.join(flags)}")
    print()

# ── 7. VERDIKTAS ─────────────────────────────────────────────────────────
print("=" * 70)
print("VERDIKTAS:")
print("=" * 70)

# Renkame faktus
fact_76430_in_any_name = any("76430" in n["name"] for n in capture.all_nodes)
fact_true_set_empty_url = any(
    ("76430" in n["name"] or "hogwarts" in n["name"].lower() or "castle" in n["name"].lower())
    and (n["slug"] == "(TUŠČIAS)" or not n["slug"])
    for n in capture.all_nodes
)
fact_all_filtered = len(passed) == 0 and len(capture.all_nodes) > 0
fact_game_in_official = any(
    any(kw in r.get("product_title", "").lower() for kw in ["nintendo", "switch", "harry potter", "žaidimas"])
    for r in official
)
fact_76430_missing_official = all(
    "76430" not in r.get("product_title", "") and "76430" not in r.get("url", "")
    for r in official
)

if fact_76430_in_any_name and not fact_all_filtered:
    print("PRIEŽASTIS A — Elesen katalogo duomenų klaida:")
    print("  Žaidimo pavadinime YRA '76430' → is_relevant_result leidžia žaidimą.")
    print("  SPRENDIMAS: Post-scraping tipo patikra — atmesti jei URL neturi '76430'")
    print("              arba pavadinime yra 'nintendo/switch/ps4/ps5/xbox'.")
elif fact_true_set_empty_url:
    print("PRIEŽASTIS B — Fix A1 numetė tikrą rinkinį:")
    print("  Tikras LEGO 76430 rinkinys turėjo tuščią URL → praleistas.")
    print("  Liko tik žaidimas → Goody rodo žaidimą.")
    print("  SPRENDIMAS: Rodyti rezultatą be URL mygtuko, o ne visai atmesti.")
elif fact_all_filtered:
    print("PRIEŽASTIS C — is_relevant_result filtruoja viską:")
    print("  Visi SPA/DOM produktai filtruojami → 'or all_results' fallback.")
    print("  SPRENDIMAS: Patikrinti kodėl filtras per griežtas šiam query.")
else:
    print("NEAIŠKU — reikia papildomos analizės.")
    print(f"  SPA žaliaviniai: {len(capture.all_nodes)}")
    print(f"  Praeina filtrą:  {len(passed)}")
    print(f"  Oficialus scrape: {len(official)}")
    print(f"  '76430' SPA pavadinime: {fact_76430_in_any_name}")
    print(f"  Tikras rinkinys tuščiu URL: {fact_true_set_empty_url}")
    print(f"  Visi filtruoti: {fact_all_filtered}")
    print(f"  Žaidimas oficialiam rezultate: {fact_game_in_official}")
    print(f"  '76430' nėra oficialiam: {fact_76430_missing_official}")

print("=" * 70)
