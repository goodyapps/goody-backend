"""
intent_schema.py — Ketinimo duomenų serverio kodo eskizas
Šaka: intent-data | Data: 2026-06-20

STATUSAS: PERŽIŪRAI — nėra integruotas į server.py
Šis failas rodo kaip atrodys kodo pakeitimai kai bus patvirtinti.
Nekeičia gyvo kodo. Nereikia leisti.
"""
import re
import uuid
import time
import threading
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# 1. PRODUKTO RAKTO NORMALIZAVIMAS
# ---------------------------------------------------------------------------

# _UNIT_TOKEN_RE — kopijuojamas iš server.py (kad šis failas veiktų atskirai)
_UNIT_TOKEN_RE = re.compile(
    r'^\d+(?:g|ml|l|kg|mg|oz|cl|dl|mm|cm|m|w|v|hz|rpm|pcs|st|stk|er|x)$'
)
_FILLER_WORDS = frozenset({
    "buy", "cheap", "best", "review", "pigiausias", "pirkti", "kur",
    "where", "kaufen", "acheter", "gdzie", "najtaniej", "for", "and", "the",
    "ir", "und", "czy", "dla", "le", "la", "les", "de", "du", "find", "get",
    "pigiau", "ieškoti",
})


def _make_product_key(query: str, brand: str = "", model_code: str = "") -> str:
    """
    Normalizuotas produkto raktas duomenų sujungimui per paieškas.
    Formatas: "brand:model" arba "brand:name" arba ":model"

    Pavyzdžiai:
      "LEGO 76430 Hogwarts"              → "lego:76430"   (brand iš query)
      "Sony WH-1000XM5"                 → "sony:wh-1000xm5"
      "samsung rb34c600esa"             → "samsung:rb34c600esa"
      "RB34C600ESA/EF", brand="Samsung" → "samsung:rb34c600esa" (/EF pašalintas)
      "Nutella 750g"                    → "nutella"  (750g = unit)
      "Milka šokoladas 100g"            → "milka:šokoladas"
      "76430"                           → ":76430"
    """
    b = re.sub(r'[^\w]', '', brand.lower()).strip() if brand else ""

    if model_code:
        # Pašalinti regioninius sufixus (/EF, /EK, /EN, /BH...)
        mc_raw = re.sub(r'/\w{1,3}$', '', model_code.lower().strip())
        mc = re.sub(r'[^\w-]', '-', mc_raw).strip('-')
        mc = re.sub(r'-+', '-', mc)
        return f"{b}:{mc}" if b else mc

    q = query.lower().strip()
    if not q:
        return ""

    raw_tokens = q.split()
    tokens = [t for t in raw_tokens if t not in _FILLER_WORDS]
    if not tokens:
        return ""

    model_tokens = []
    word_tokens = []

    for raw in tokens:
        # Pašalinti regioninius sufixus (rb34c600esa/ef → rb34c600esa)
        t = re.sub(r'/\w{1,3}$', '', raw)
        # Valymas: raides (Unicode), skaičiai, brūkšneliai
        clean = re.sub(r'[^\w-]', '', t).strip('-')
        clean = re.sub(r'-+', '-', clean)
        if not clean:
            continue
        has_digit = bool(re.search(r'\d', clean))
        if has_digit and not _UNIT_TOKEN_RE.match(clean):
            model_tokens.append(clean)
        elif not has_digit and len(clean) >= 2:
            word_tokens.append(clean)

    # Brand: iš parametro arba pirmasis žodžio tokenas
    effective_brand = b or (word_tokens[0] if word_tokens else "")

    if effective_brand and model_tokens:
        return f"{effective_brand}:{model_tokens[0]}"
    elif model_tokens:
        return f":{model_tokens[0]}"
    elif effective_brand:
        rest = [t for t in word_tokens if t != effective_brand][:2]
        return effective_brand + (":" + '-'.join(rest) if rest else "")
    else:
        return '-'.join(word_tokens[:3])


# ---------------------------------------------------------------------------
# 2. INTENT EVENTO KONSTRUKTORIUS
# ---------------------------------------------------------------------------

def _build_intent_event(
    query: str,
    input_method: str,  # 'text' | 'photo' | 'barcode' | 'voice'
    language: str,
    result_data: dict,
    search_id: str = None,
    scan_confidence: str = None,
    brand: str = "",
    model_code: str = "",
) -> dict:
    """
    Sukuria intent_events lentelei tinkantį Python dict.
    Nekeičia result_data.
    """
    now = datetime.now(timezone.utc)

    # Ištraukti rezultatų statistiką
    results_list = result_data.get("results") or []
    verdict = result_data.get("ai_verdict") or result_data.get("verdict")
    price_min = result_data.get("price_min") or 0
    price_max = result_data.get("price_max") or 0
    cheapest = results_list[0].get("shop") if results_list else None

    return {
        "id": search_id or str(uuid.uuid4()),

        "product_key": _make_product_key(query, brand, model_code),
        "product_name": query.lower().strip()[:200],
        "product_type": result_data.get("product_type"),

        "input_method": input_method or "text",
        "scan_confidence": scan_confidence,  # None jei text/voice
        "language": language or "lt",

        "hour_of_day": now.hour,
        "day_of_week": now.weekday(),   # 0=Mon, 6=Sun
        "week_of_year": now.isocalendar()[1],

        "verdict": verdict,
        "price_min_eur": round(float(price_min), 2) if price_min else None,
        "price_max_eur": round(float(price_max), 2) if price_max else None,
        "shops_found": len(results_list),
        "cheapest_shop": cheapest,
        "has_history": bool(result_data.get("price_history")),

        # Veiksmo signalas: užpildomas vėliau per /api/track
        "clicked_shop": None,
        "clicked_at": None,
        "added_watchlist": False,
        "watchlist_target_eur": None,
    }


# ---------------------------------------------------------------------------
# 3. SUPABASE ĮRAŠYMAS (fire-and-forget)
# ---------------------------------------------------------------------------

def _sb_log_intent(event: dict, sb_client=None):
    """
    Asinchroniškai išsaugo intent evento įrašą į Supabase.
    Klaidos tyliai prarandamos (loguojamos) — neturi sutrikdyti paieškos.
    """
    if not sb_client:
        return
    try:
        sb_client.table("intent_events").insert(event).execute()
    except Exception as e:
        print(f"[intent_log] WARNING: failed to log intent event: {e}")


def log_intent_async(event: dict, sb_client):
    """Paleisti atskirame thread'e po paieškos — neblokuoja response."""
    t = threading.Thread(
        target=_sb_log_intent,
        args=(event, sb_client),
        daemon=True
    )
    t.start()


# ---------------------------------------------------------------------------
# 4. CLICK SIEJIMAS SU INTENT EVENTU
# ---------------------------------------------------------------------------

def _sb_update_intent_click(intent_id: str, clicked_shop: str, sb_client=None):
    """
    Kai vartotojas spaudžia "Buy Now" (/api/track), susieti su intent eventu.
    Reikia, kad frontend siųstų intent_id kartu su /api/track.
    """
    if not sb_client or not intent_id:
        return
    try:
        sb_client.table("intent_events").update({
            "clicked_shop": clicked_shop,
            "clicked_at": datetime.now(timezone.utc).isoformat(),
        }).eq("id", intent_id).execute()
    except Exception as e:
        print(f"[intent_click] WARNING: failed to update click: {e}")


# ---------------------------------------------------------------------------
# 5. KĄ KEISTI server.py
# ---------------------------------------------------------------------------

"""
PAKEITIMŲ VIETOS server.py:

A. Importai (failo viršuje):
   import uuid
   from datetime import datetime, timezone
   # (intent_schema.py funkcijos bus integruotos tiesiai į server.py,
   #  ne kaip modulis — kad nebūtų naujų failų)

B. search() funkcija (~line 6277, po post_process()):

   # Loguoti intent eventą (fire-and-forget)
   _search_id = str(uuid.uuid4())
   _intent_ev = _build_intent_event(
       query=query,
       input_method=data.get("input_method", "text"),
       language=language,
       result_data=result,
       search_id=_search_id,
   )
   log_intent_async(_intent_ev, get_supabase())
   result["search_id"] = _search_id  # grąžinti frontend'ui siejimui su track

C. search_stream() funkcija (~line 6517, po result = post_process()):

   _stream_id = str(uuid.uuid4())
   _intent_ev = _build_intent_event(
       query=_query,
       input_method=data.get("input_method", "text"),
       language=_lang,
       result_data=result,
       search_id=_stream_id,
   )
   log_intent_async(_intent_ev, get_supabase())
   # Siųsti search_id per SSE kaip papildomą eventą prieš 'complete'
   yield f"data: {json.dumps({'type':'search_id','id':_stream_id})}\\n\\n"

D. track_click() funkcija (line 7317):

   intent_id = (data.get("intent_id") or "")[:36].strip()
   if intent_id and shop:
       threading.Thread(
           target=_sb_update_intent_click,
           args=(intent_id, shop, get_supabase()),
           daemon=True
       ).start()

E. Frontend doSearch() — siųsti intent_id atgal su track():

   // Kai gaunamas search_id iš SSE 'search_id' evento:
   let _intentId = null;
   sse.addEventListener('message', e => {
     const d = JSON.parse(e.data);
     if (d.type === 'search_id') { _intentId = d.id; return; }
     // ... rest of handling
   });

   // track() funkcija:
   function track(shop, q) {
     fetch('/api/track', {
       method: 'POST',
       body: JSON.stringify({ shop, q, intent_id: _intentId })
     });
   }
"""


# ---------------------------------------------------------------------------
# 6. PRODUKTO RAKTO TESTAI
# ---------------------------------------------------------------------------

def _test_product_key():
    """Patikrina _make_product_key() elgesį."""
    cases = [
        # (query, brand, model_code, expected_key)
        # Brand iš query (ne parametro)
        ("LEGO 76430 Hogwarts",    "",      "",          "lego:76430"),
        ("Sony WH-1000XM5",        "",      "",          "sony:wh-1000xm5"),
        ("samsung rb34c600esa",    "",      "",          "samsung:rb34c600esa"),
        # Brand iš parametro
        ("LEGO 76430 Hogwarts",    "LEGO",  "",          "lego:76430"),
        ("lego 76430",             "LEGO",  "76430",     "lego:76430"),
        ("Sony WH-1000XM5",        "Sony",  "WH-1000XM5","sony:wh-1000xm5"),
        # Regioninis sufixas
        ("RB34C600ESA/EF",         "Samsung","",         "samsung:rb34c600esa"),
        # Tik model code (be brand)
        ("WH-1000XM5",             "",      "WH-1000XM5","wh-1000xm5"),
        ("76430",                  "",      "",           ":76430"),
        # Maistas / be kodo
        ("Nutella 750g",           "Nutella","",         "nutella"),
        ("buy cheap iPhone 15",    "Apple", "",          "apple:15"),
        ("Philips Airfryer XL",    "Philips","",         "philips:airfryer-xl"),
    ]

    print("=== _make_product_key() testai ===")
    passed = 0
    for query, brand, model_code, expected in cases:
        result = _make_product_key(query, brand, model_code)
        status = "✓" if result == expected else "✗"
        if result != expected:
            print(f"  {status} '{query}' (brand='{brand}', mc='{model_code}')")
            print(f"       Laukta: '{expected}'")
            print(f"       Gauta:  '{result}'")
        else:
            print(f"  {status} '{query}' → '{result}'")
            passed += 1

    print(f"\n{passed}/{len(cases)} testų PASS")
    return passed == len(cases)


if __name__ == "__main__":
    _test_product_key()
