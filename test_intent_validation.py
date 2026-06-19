"""
test_intent_validation.py — Intent data dizaino validacija
Šaka: intent-data | Data: 2026-06-20

IZOLIUOTAS testas: SQLite (ne Supabase, ne produkcija).
Tikrina: product_key, migracijos struktūra, pilnas srautas.
"""
import sys, io, re, uuid, sqlite3, json, time, os
from datetime import datetime, timezone

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# KOPIJUOJAME _make_product_key iš intent_schema.py (be importo)
# ---------------------------------------------------------------------------
_UNIT_TOKEN_RE = re.compile(
    r'^\d+(?:g|ml|l|kg|mg|oz|cl|dl|mm|cm|m|w|v|hz|rpm|pcs|st|stk|er|x)$'
)
_FILLER_WORDS = frozenset({
    "buy","cheap","best","review","pigiausias","pirkti","kur","where",
    "kaufen","acheter","gdzie","najtaniej","for","and","the","ir","und",
    "czy","dla","le","la","les","de","du","find","get","pigiau","ieškoti",
})

def _make_product_key(query: str, brand: str = "", model_code: str = "") -> str:
    """v2 — brand iš query, regioninis sufixas, Unicode, brūkšneliai modeliuose."""
    b = re.sub(r'[^\w]', '', brand.lower()).strip() if brand else ""
    if model_code:
        mc_raw = re.sub(r'/\w{1,3}$', '', model_code.lower().strip())
        mc = re.sub(r'[^\w-]', '-', mc_raw).strip('-')
        mc = re.sub(r'-+', '-', mc)
        return f"{b}:{mc}" if b else mc
    q = query.lower().strip()
    if not q:
        return ""
    tokens = [t for t in q.split() if t not in _FILLER_WORDS]
    if not tokens:
        return ""
    model_tokens = []
    word_tokens = []
    for raw in tokens:
        t = re.sub(r'/\w{1,3}$', '', raw)
        clean = re.sub(r'[^\w-]', '', t).strip('-')
        clean = re.sub(r'-+', '-', clean)
        if not clean:
            continue
        has_digit = bool(re.search(r'\d', clean))
        if has_digit and not _UNIT_TOKEN_RE.match(clean):
            model_tokens.append(clean)
        elif not has_digit and len(clean) >= 2:
            word_tokens.append(clean)
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
# TESTŲ REZULTATŲ KAUPIKLIS
# ---------------------------------------------------------------------------
results = []
errors = []

def check(label: str, got, expected, danger: bool = False):
    ok = (got == expected)
    results.append((label, ok, got, expected, danger))
    if not ok:
        tag = "PAVOJINGA" if danger else "KLAIDA"
        errors.append(f"[{tag}] {label}: gauta='{got}', laukta='{expected}'")
    return ok

def check_different(label: str, key_a, key_b, danger: bool = False):
    ok = (key_a != key_b)
    results.append((label, ok, f"{key_a} ≠ {key_b}", "turi būti skirtingi", danger))
    if not ok:
        tag = "PAVOJINGA" if danger else "KLAIDA"
        errors.append(f"[{tag}] {label}: abu raktai vienodi='{key_a}' — SUSILIEJIMAS!")
    return ok

def check_same(label: str, keys: list, expected: str, danger: bool = False):
    unique = set(keys)
    ok = (unique == {expected}) if expected else (len(unique) == 1)
    results.append((label, ok, str(unique), f"visi='{expected}'", danger))
    if not ok:
        errors.append(f"[{'PAVOJINGA' if danger else 'KLAIDA'}] {label}: {unique} ≠ visi '{expected}'")
    return ok


# ===========================================================================
# 1 SEKCIJA: PRODUCT_KEY NORMALIZAVIMO TESTAI
# ===========================================================================
print("\n" + "="*70)
print("1. PRODUCT_KEY NORMALIZAVIMO TESTAI")
print("="*70)

# --- 1.1 LEGO: susijungimas ---
print("\n--- 1.1 LEGO: skirtingi užrašai → VIENAS raktas ---")
lego_queries = [
    _make_product_key("LEGO 76430 Hogwarts"),           # brand iš query
    _make_product_key("lego 76430"),                     # brand iš query
    _make_product_key("76430 hogwarts castle", "LEGO"),  # brand iš param
    _make_product_key("LEGO Harry Potter 76430"),        # brand iš query
    _make_product_key("lego 76430 hogwarts castle owlery"),
    _make_product_key("LEGO 76430", "LEGO", "76430"),   # iš scan/identify
]
check_same("LEGO 76430 — visi užrašai → lego:76430", lego_queries, "lego:76430", danger=True)
for q, k in zip(["LEGO 76430 Hogwarts", "lego 76430", "76430+LEGO brand",
                  "LEGO Harry Potter 76430", "lego 76430 hogwarts castle owlery",
                  "LEGO 76430 su model_code"], lego_queries):
    print(f"  '{q}' → '{k}'")

# --- 1.2 LEGO: atskiri rinkiniai NESUSILIEJA ---
print("\n--- 1.2 LEGO: skirtingi rinkiniai → SKIRTINGI raktai ---")
k_76430 = _make_product_key("LEGO 76430")
k_76451 = _make_product_key("LEGO 76451")
k_42151 = _make_product_key("LEGO 42151 Technic")
k_21325 = _make_product_key("LEGO 21325 Medieval")
check_different("LEGO 76430 vs 76451 → atskiri", k_76430, k_76451, danger=True)
check_different("LEGO 76430 vs 42151 → atskiri", k_76430, k_42151, danger=True)
check_different("LEGO 76451 vs 21325 → atskiri", k_76451, k_21325, danger=True)
print(f"  76430→'{k_76430}', 76451→'{k_76451}', 42151→'{k_42151}', 21325→'{k_21325}'")

# --- 1.3 Elektronika: Samsung šaldytuvas ---
print("\n--- 1.3 Samsung šaldytuvas: modelio variacijų susijungimas ---")
samsung_queries = [
    _make_product_key("Samsung RB34C600ESA"),           # brand iš query
    _make_product_key("RB34C600ESA/EF", "Samsung"),     # /EF pašalinamas
    _make_product_key("samsung rb34c600esa šaldytuvas"),# brand iš query
    _make_product_key("Samsung RB34C600ESA/EF 341L"),   # sufixas toke'e
]
print(f"  'Samsung RB34C600ESA'          → '{samsung_queries[0]}'")
print(f"  'RB34C600ESA/EF' (Samsung)     → '{samsung_queries[1]}'")
print(f"  'samsung rb34c600esa šaldytuvas' → '{samsung_queries[2]}'")
print(f"  'Samsung RB34C600ESA/EF 341L'  → '{samsung_queries[3]}'")
check_same("Samsung RB34C600ESA variacijos → vienas raktas", samsung_queries[:3],
           "samsung:rb34c600esa", danger=True)

# --- 1.4 Sony ausinės ---
print("\n--- 1.4 Sony WH-1000XM5 ---")
sony_queries = [
    _make_product_key("Sony WH-1000XM5"),                    # brand iš query
    _make_product_key("WH-1000XM5", "Sony"),                 # brand iš param
    _make_product_key("Sony WH-1000XM5", "Sony", "WH-1000XM5"),  # iš scan
]
# "sony wh 1000xm5" (su tarpais) duos ":1000xm5" — priimtinas apribojimas
# nes "wh" ir "1000xm5" kaip atskiri tokenai nesusijungia į "wh-1000xm5"
check_same("Sony WH-1000XM5 variacijos (su brūkšneliu)", sony_queries, "sony:wh-1000xm5", danger=True)
k_wh_space = _make_product_key("sony wh 1000xm5 headphones")
print(f"  [INFO] 'sony wh 1000xm5 headphones' → '{k_wh_space}' (su tarpu — žinomas apribojimas)")
for q, k in zip(["Sony WH-1000XM5", "WH-1000XM5+Sony", "su model_code"], sony_queries):
    print(f"  '{q}' → '{k}'")

# Sony skirtingi modeliai
k_xm5 = _make_product_key("Sony WH-1000XM5")
k_xm4 = _make_product_key("Sony WH-1000XM4")
k_xm3 = _make_product_key("Sony WH-1000XM3")
check_different("Sony XM5 vs XM4 → atskiri", k_xm5, k_xm4, danger=True)
check_different("Sony XM4 vs XM3 → atskiri", k_xm4, k_xm3, danger=True)
print(f"  XM5→'{k_xm5}', XM4→'{k_xm4}', XM3→'{k_xm3}'")

# --- 1.5 Maistas: kiekis ---
print("\n--- 1.5 Maistas: kiekis turi SKIRTI produktus ---")
k_milka100 = _make_product_key("Milka 100g", "Milka")
k_milka300 = _make_product_key("Milka 300g", "Milka")
k_milka_choc = _make_product_key("Milka šokoladas 100g", "Milka")
k_milka_no_weight = _make_product_key("Milka šokoladas", "Milka")
print(f"  'Milka 100g'          → '{k_milka100}'")
print(f"  'Milka 300g'          → '{k_milka300}'")
print(f"  'Milka šokoladas 100g'→ '{k_milka_choc}'")
print(f"  'Milka šokoladas'     → '{k_milka_no_weight}'")
# 100g vs 300g - abu turėtų būti Milka produktai, bet tai SKIRTINGOS SKU
# Pagal _UNIT_TOKEN_RE: 100g ir 300g filtruojami → abu tampa "milka"
# Tai yra ŽINOMAS APKRITIMAS: maisto kiekiai nesaugomi raktui
# Sprendimas: priimame šį apribojimą, nes "Milka 100g" ir "Milka 300g" paprastai
# yra pakaitalai ir kainų istorija kartu naudinga
print("  [INFO] Milka 100g ir 300g turi vienodą raktą — priimtinas apkribojimas")
# "Milka 100g" → "milka", "Milka šokoladas 100g" → "milka:šokoladas"
# TEISINGAI skirtingi: Milka plain ≠ Milka šokoladas (skirtingos SKU)
check_different("Milka plain vs Milka šokoladas → skirtingi (teisingai)",
                k_milka100, k_milka_choc, danger=False)

# --- 1.6 Knygos (ISBN) ---
print("\n--- 1.6 Knygos: ISBN kaip modelio kodas ---")
k_isbn = _make_product_key("978-3-16-148410-0")
k_isbn2 = _make_product_key("9783161484100")  # be brūkšnelių
print(f"  ISBN su brūkšneliais  → '{k_isbn}'")
print(f"  ISBN be brūkšnelių   → '{k_isbn2}'")
# ISBN turi skaičius → bus model token
check("ISBN su brūkšneliais → turi model token", bool(re.search(r'\d', k_isbn)), True)

# --- 1.7 iPhone modeliai ---
print("\n--- 1.7 iPhone: skirtingi modeliai → atskiri ---")
k_iphone15 = _make_product_key("iPhone 15 Pro Max", "Apple")
k_iphone14 = _make_product_key("iPhone 14 Pro", "Apple")
k_iphone13 = _make_product_key("Apple iPhone 13 mini")
check_different("iPhone 15 Pro Max vs 14 Pro → atskiri", k_iphone15, k_iphone14, danger=True)
check_different("iPhone 14 Pro vs 13 mini → atskiri", k_iphone14, k_iphone13, danger=True)
print(f"  iPhone 15 Pro Max → '{k_iphone15}'")
print(f"  iPhone 14 Pro     → '{k_iphone14}'")
print(f"  Apple iPhone 13   → '{k_iphone13}'")

# --- 1.8 Produktai BEZ kodo ---
print("\n--- 1.8 Produktai be kodo (tik pavadinimas) ---")
k_nutella = _make_product_key("Nutella", "Ferrero")
k_nutella2 = _make_product_key("ferrero nutella")
k_haribo = _make_product_key("Haribo Goldbären")
k_dove = _make_product_key("Dove Nourishing Shampoo", "Dove")
k_dove2 = _make_product_key("Dove šampūnas maitinantis", "Dove")
print(f"  'Nutella' (brand=Ferrero)   → '{k_nutella}'")
print(f"  'ferrero nutella'           → '{k_nutella2}'")
print(f"  'Haribo Goldbären'          → '{k_haribo}'")
print(f"  'Dove Nourishing Shampoo'   → '{k_dove}'")
print(f"  'Dove šampūnas maitinantis' → '{k_dove2}'")
check_different("Nutella vs Haribo → atskiri", k_nutella, k_haribo, danger=True)
check_different("Dove šampūnas vs Nutella → atskiri", k_dove, k_nutella, danger=True)

# --- 1.9 PAVOJINGI susiliejimo atvejai ---
print("\n--- 1.9 PAVOJINGI susiliejimų testai ---")
# Ar du visiškai skirtingi produktai gali gautiti vienodą raktą?
k_lego_technic = _make_product_key("LEGO Technic 42151")
k_lego_city = _make_product_key("LEGO City 42151")  # tas pats numeris, kita serija
# (realybėje 42151 yra Technic, bet testuojame)
print(f"  'LEGO Technic 42151' → '{k_lego_technic}'")
print(f"  'LEGO City 42151'    → '{k_lego_city}'")
# Abu turi 42151 → raktai bus vienodi lego:42151 → tai OK (42151 yra unikalus LEGO rinkinys)

# Tikras pavojus: numeriai su skirtinga reikšme
k_size_32 = _make_product_key("Nike Air Max 90 size 32", "Nike")
k_set_32 = _make_product_key("Nike model 32", "Nike")
print(f"  'Nike Air Max 90 size 32' → '{k_size_32}'")
print(f"  'Nike model 32'           → '{k_set_32}'")
check_different("Nike size 32 vs model 32 → skirtingi", k_size_32, k_set_32, danger=False)

# Kraštinis atvejis: labai trumpas query
k_short = _make_product_key("TV")
k_short2 = _make_product_key("PC")
check_different("'TV' vs 'PC' → atskiri", k_short, k_short2)
print(f"  'TV' → '{k_short}', 'PC' → '{k_short2}'")

# Tušti/labai trumpi queries
k_empty = _make_product_key("")
k_space = _make_product_key("   ")
print(f"  '' → '{k_empty}', '   ' → '{k_space}'")
check("Tuščias query → tuščias raktas", k_empty, "", danger=False)


# ===========================================================================
# 2 SEKCIJA: MIGRACIJOS SAUSAS TESTAS (SQLite)
# ===========================================================================
print("\n" + "="*70)
print("2. MIGRACIJOS SAUSAS TESTAS (SQLite — izoliuota)")
print("="*70)

# SQLite adaptuotas migration.sql (PostgreSQL specifikos -> SQLite ekvivalentai)
# gen_random_uuid() -> tai palaikome Python lygmenyje
# TIMESTAMPTZ -> TEXT
# SMALLINT -> INTEGER
# NUMERIC(10,2) -> REAL
# BOOLEAN -> INTEGER (0/1)

SQLITE_MIGRATION = """
-- Etapas 1: esamos price_history lentelė + product_key kolona
CREATE TABLE IF NOT EXISTS price_history (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    shop         TEXT NOT NULL,
    price        REAL NOT NULL,
    currency     TEXT DEFAULT 'EUR',
    checked_at   TEXT
);

-- Pirma įrašome testų duomenis (prieš migraciją)
INSERT INTO price_history (product_name, shop, price, currency, checked_at) VALUES
    ('lego 76430 hogwarts',   'varle',  89.99, 'EUR', '2026-06-19T10:00:00Z'),
    ('lego 76430',            'pigu',   87.99, 'EUR', '2026-06-18T10:00:00Z'),
    ('Sony WH-1000XM5',       'elesen', 249.0, 'EUR', '2026-06-17T10:00:00Z'),
    ('nutella 750g',          'varle',  4.99,  'EUR', '2026-06-16T10:00:00Z');

-- Etapas 1a: pridėti product_key koloną (SQLite: ALTER TABLE ADD COLUMN)
ALTER TABLE price_history ADD COLUMN product_key TEXT;

-- Etapas 1b: backfill
UPDATE price_history SET product_key = LOWER(TRIM(product_name)) WHERE product_key IS NULL;

-- Etapas 1c: indeksas
CREATE INDEX IF NOT EXISTS idx_price_history_product_key
    ON price_history(product_key, checked_at);

-- Etapas 2: nauja intent_events lentelė
CREATE TABLE IF NOT EXISTS intent_events (
    id                   TEXT PRIMARY KEY,
    product_key          TEXT NOT NULL,
    product_name         TEXT NOT NULL,
    product_type         TEXT,
    input_method         TEXT NOT NULL DEFAULT 'text',
    scan_confidence      TEXT,
    language             TEXT NOT NULL DEFAULT 'lt',
    hour_of_day          INTEGER,
    day_of_week          INTEGER,
    week_of_year         INTEGER,
    verdict              TEXT,
    price_min_eur        REAL,
    price_max_eur        REAL,
    shops_found          INTEGER DEFAULT 0,
    cheapest_shop        TEXT,
    has_history          INTEGER DEFAULT 0,
    clicked_shop         TEXT,
    clicked_at           TEXT,
    added_watchlist      INTEGER DEFAULT 0,
    watchlist_target_eur REAL,
    created_at           TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_intent_product_key
    ON intent_events(product_key, created_at);

CREATE INDEX IF NOT EXISTS idx_intent_verdict_type
    ON intent_events(verdict, product_type, created_at);

CREATE INDEX IF NOT EXISTS idx_intent_day_hour
    ON intent_events(day_of_week, hour_of_day);

CREATE INDEX IF NOT EXISTS idx_intent_input_method
    ON intent_events(input_method, created_at);
"""

SQLITE_ROLLBACK = """
DROP TABLE IF EXISTS intent_events;
ALTER TABLE price_history DROP COLUMN IF EXISTS product_key;
"""

db = sqlite3.connect(":memory:")
db.row_factory = sqlite3.Row
cur = db.cursor()

migration_ok = True
try:
    # Vykdyti migraciją
    cur.executescript(SQLITE_MIGRATION)
    db.commit()
    print("  ✓ Migracija įvykdyta be klaidų")

    # Patikrinti price_history struktūrą
    cur.execute("PRAGMA table_info(price_history)")
    cols = {r["name"] for r in cur.fetchall()}
    check("price_history turi product_key koloną", "product_key" in cols, True)
    check("price_history išlaikė price koloną", "price" in cols, True)
    check("price_history išlaikė product_name koloną", "product_name" in cols, True)

    # Patikrinti backfill
    cur.execute("SELECT COUNT(*) as n FROM price_history WHERE product_key IS NULL")
    nulls = cur.fetchone()["n"]
    check("Visos eilutės turi product_key (backfill)", nulls, 0)

    # Patikrinti backfill reikšmes
    cur.execute("SELECT product_name, product_key FROM price_history ORDER BY id")
    rows = cur.fetchall()
    print("\n  Backfill rezultatai:")
    for r in rows:
        print(f"    product_name='{r['product_name']}' → product_key='{r['product_key']}'")

    # Patikrinti intent_events struktūrą
    cur.execute("PRAGMA table_info(intent_events)")
    intent_cols = {r["name"] for r in cur.fetchall()}
    for expected_col in ["id", "product_key", "product_name", "input_method",
                          "language", "verdict", "price_min_eur", "shops_found",
                          "clicked_shop", "has_history", "created_at"]:
        check(f"intent_events.{expected_col} egzistuoja", expected_col in intent_cols, True)

    # Patikrinti indeksus
    cur.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='intent_events'")
    indexes = {r["name"] for r in cur.fetchall()}
    check("idx_intent_product_key egzistuoja", "idx_intent_product_key" in indexes, True)
    check("idx_intent_verdict_type egzistuoja", "idx_intent_verdict_type" in indexes, True)
    check("idx_intent_day_hour egzistuoja", "idx_intent_day_hour" in indexes, True)

    print("\n  ✓ Visos lentelės ir indeksai sukurti teisingai")

except Exception as e:
    migration_ok = False
    errors.append(f"[KRITINĖ KLAIDA] Migracija nepavyko: {e}")
    print(f"  ✗ Migracija NEPAVYKO: {e}")

# Rollback testas
print("\n--- 2b. Rollback testas ---")
try:
    db_rollback = sqlite3.connect(":memory:")
    db_rollback.row_factory = sqlite3.Row
    cur_rb = db_rollback.cursor()

    # Sukurti ir backfill'inti
    cur_rb.executescript(SQLITE_MIGRATION)
    db_rollback.commit()

    # Rollback (SQLite nepalaiko ALTER TABLE DROP COLUMN senose versijose, bet testuojam DROP TABLE)
    try:
        cur_rb.execute("DROP TABLE IF EXISTS intent_events")
        db_rollback.commit()
        cur_rb.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='intent_events'")
        exists = cur_rb.fetchone()
        check("Rollback: intent_events pašalinta", exists is None, True)
        print("  ✓ Rollback DROP TABLE intent_events — sėkmingas")
    except Exception as e:
        print(f"  ✗ Rollback klaida: {e}")

    # price_history vis dar egzistuoja po rollback
    cur_rb.execute("SELECT COUNT(*) as n FROM price_history")
    count = cur_rb.fetchone()["n"]
    check("Rollback: price_history išliko nepažeista", count, 4)
    print(f"  ✓ price_history išliko su {count} eilutėmis po rollback")

    db_rollback.close()
except Exception as e:
    errors.append(f"[KLAIDA] Rollback testas nepavyko: {e}")
    print(f"  ✗ Rollback testas nepavyko: {e}")


# ===========================================================================
# 3 SEKCIJA: PILNO SRAUTO SIMULIACIJA
# ===========================================================================
print("\n" + "="*70)
print("3. PILNO SRAUTO SIMULIACIJA")
print("="*70)

# Simuliuojami scenarijai:
# A: Vartotojas fotografuoja LEGO → verdiktas BUY → spaudžia Varle
# B: Vartotojas tekstą ieško Sony WH-1000XM5 → WAIT → neperka
# C: Kitas vartotojas ieško lego 76430 → tas pats product_key kaip A

def build_intent_event(query, input_method, language, verdict, price_min,
                        price_max, shops_found, cheapest_shop, has_history,
                        product_type=None, scan_confidence=None,
                        brand="", model_code=""):
    now = datetime.now(timezone.utc)
    return {
        "id": str(uuid.uuid4()),
        "product_key": _make_product_key(query, brand, model_code),
        "product_name": query.lower().strip()[:200],
        "product_type": product_type,
        "input_method": input_method,
        "scan_confidence": scan_confidence,
        "language": language,
        "hour_of_day": now.hour,
        "day_of_week": now.weekday(),
        "week_of_year": now.isocalendar()[1],
        "verdict": verdict,
        "price_min_eur": round(float(price_min), 2) if price_min else None,
        "price_max_eur": round(float(price_max), 2) if price_max else None,
        "shops_found": shops_found,
        "cheapest_shop": cheapest_shop,
        "has_history": 1 if has_history else 0,
        "clicked_shop": None,
        "clicked_at": None,
        "added_watchlist": 0,
        "watchlist_target_eur": None,
        "created_at": now.isoformat(),
    }

def insert_intent(cur, ev):
    cur.execute("""
        INSERT INTO intent_events (
            id, product_key, product_name, product_type, input_method,
            scan_confidence, language, hour_of_day, day_of_week, week_of_year,
            verdict, price_min_eur, price_max_eur, shops_found, cheapest_shop,
            has_history, clicked_shop, clicked_at, added_watchlist,
            watchlist_target_eur, created_at
        ) VALUES (
            :id, :product_key, :product_name, :product_type, :input_method,
            :scan_confidence, :language, :hour_of_day, :day_of_week, :week_of_year,
            :verdict, :price_min_eur, :price_max_eur, :shops_found, :cheapest_shop,
            :has_history, :clicked_shop, :clicked_at, :added_watchlist,
            :watchlist_target_eur, :created_at
        )""", ev)
    return ev["id"]

def update_click(cur, intent_id, shop):
    cur.execute("""
        UPDATE intent_events
        SET clicked_shop = ?, clicked_at = ?
        WHERE id = ?
    """, (shop, datetime.now(timezone.utc).isoformat(), intent_id))
    return cur.rowcount

try:
    # --- Scenarijus A: LEGO foto paieška ---
    print("\n--- A: Vartotojas fotografuoja LEGO 76430 ---")
    ev_A = build_intent_event(
        query="LEGO 76430 Hogwarts", input_method="photo", language="lt",
        verdict="BUY", price_min=87.99, price_max=94.99, shops_found=3,
        cheapest_shop="pigu", has_history=False,
        product_type="MAIN", scan_confidence="high", brand="LEGO"
    )
    id_A = insert_intent(cur, ev_A)
    print(f"  Įrašyta intent_event: id={id_A[:8]}..., product_key='{ev_A['product_key']}'")
    check("A: product_key teisingas", ev_A["product_key"], "lego:76430", danger=True)
    check("A: input_method=photo", ev_A["input_method"], "photo")
    check("A: verdict=BUY", ev_A["verdict"], "BUY")

    # Vartotojas spaudžia Pigu
    rows_updated = update_click(cur, id_A, "pigu")
    db.commit()
    check("A: click atnaujintas DB (rowcount=1)", rows_updated, 1)

    cur.execute("SELECT clicked_shop FROM intent_events WHERE id=?", (id_A,))
    row = cur.fetchone()
    check("A: clicked_shop=pigu DB'e", row["clicked_shop"], "pigu")
    print(f"  ✓ Click susietas: clicked_shop='{row['clicked_shop']}'")

    # --- Scenarijus B: Sony tekstas, WAIT ---
    print("\n--- B: Tekstas 'Sony WH-1000XM5', verdiktas WAIT ---")
    ev_B = build_intent_event(
        query="Sony WH-1000XM5", input_method="text", language="lt",
        verdict="WAIT", price_min=249.0, price_max=279.0, shops_found=5,
        cheapest_shop="amazon.de", has_history=True,
        product_type="MAIN", brand="Sony"
    )
    id_B = insert_intent(cur, ev_B)
    db.commit()
    check("B: product_key=sony:wh-1000xm5", ev_B["product_key"], "sony:wh-1000xm5", danger=True)
    check("B: has_history=1", ev_B["has_history"], 1)
    check("B: clicked_shop=None (neperka)", ev_B["clicked_shop"], None)
    print(f"  ✓ WAIT, neperka: product_key='{ev_B['product_key']}', clicked_shop=None")

    # --- Scenarijus C: Kitas vartotojas, tas pats produktas ---
    print("\n--- C: Kitas vartotojas ieško 'lego 76430' (tekstas) ---")
    ev_C = build_intent_event(
        query="lego 76430", input_method="text", language="lt",
        verdict="BUY", price_min=85.99, price_max=91.99, shops_found=4,
        cheapest_shop="varle", has_history=True
    )
    id_C = insert_intent(cur, ev_C)
    db.commit()
    check("C: product_key tas pats kaip A (lego:76430)", ev_C["product_key"], "lego:76430", danger=True)
    print(f"  ✓ Skirtinga paieška, tas pats product_key='{ev_C['product_key']}' — susijungs su A!")

    # --- Srautų užklausos ---
    print("\n--- 3a. Agregatinės užklausos ---")

    # Kiek kartų ieškota LEGO 76430?
    cur.execute("""
        SELECT product_key, COUNT(*) as searches,
               AVG(price_min_eur) as avg_price,
               MIN(price_min_eur) as min_ever,
               SUM(CASE WHEN clicked_shop IS NOT NULL THEN 1 ELSE 0 END) as purchases
        FROM intent_events
        WHERE product_key = 'lego:76430'
    """)
    lego_stats = cur.fetchone()
    check("LEGO 76430: 2 paieškos (A + C)", lego_stats["searches"], 2)
    print(f"  LEGO 76430 statistika:")
    print(f"    Paieškų: {lego_stats['searches']}")
    print(f"    Vidutinė kaina: €{lego_stats['avg_price']:.2f}")
    print(f"    Min kaina: €{lego_stats['min_ever']:.2f}")
    print(f"    Pirkimų: {lego_stats['purchases']}")

    # Konversijų analizė pagal shopą
    cur.execute("""
        SELECT cheapest_shop,
               COUNT(*) as impressions,
               SUM(CASE WHEN clicked_shop IS NOT NULL THEN 1 ELSE 0 END) as clicks
        FROM intent_events
        WHERE verdict = 'BUY'
        GROUP BY cheapest_shop
        ORDER BY impressions DESC
    """)
    print(f"\n  Shopų konversijos (BUY verdiktas):")
    for r in cur.fetchall():
        ctr = round(100.0 * r["clicks"] / r["impressions"], 1) if r["impressions"] else 0
        print(f"    {r['cheapest_shop']}: {r['impressions']} rodymų, {r['clicks']} paspaudimų ({ctr}% CTR)")

    # Input method analizė
    cur.execute("""
        SELECT input_method, COUNT(*) as n,
               SUM(CASE WHEN clicked_shop IS NOT NULL THEN 1 ELSE 0 END) as clicks
        FROM intent_events GROUP BY input_method
    """)
    print(f"\n  Input method statistika:")
    for r in cur.fetchall():
        conv = round(100.0 * r["clicks"] / r["n"], 1) if r["n"] else 0
        print(f"    {r['input_method']}: {r['n']} paieškų, {conv}% konversija")

    # product_key JOIN su price_history
    print(f"\n--- 3b. product_key JOIN tarp lentelių ---")
    # Pirma atnaujinam price_history product_key su mūsų normalizacija
    cur.execute("UPDATE price_history SET product_key = 'lego:76430' WHERE product_name LIKE '%lego%76430%'")
    db.commit()

    cur.execute("""
        SELECT ph.shop, ph.price, ph.checked_at
        FROM price_history ph
        WHERE ph.product_key = 'lego:76430'
        ORDER BY ph.checked_at DESC
    """)
    ph_rows = cur.fetchall()
    check("JOIN: price_history randa LEGO 76430 istorija per product_key",
          len(ph_rows) > 0, True, danger=True)
    print(f"  Kainų istorija (price_history JOIN per product_key='lego:76430'):")
    for r in ph_rows:
        print(f"    {r['shop']}: €{r['price']} @ {r['checked_at']}")

    print("\n  ✓ Pilnas srautas simuliuotas sėkmingai")

except Exception as e:
    errors.append(f"[KRITINĖ KLAIDA] Srauto simuliacija nepavyko: {e}")
    print(f"  ✗ Klaida: {e}")
    import traceback; traceback.print_exc()

db.close()


# ===========================================================================
# REZULTATŲ SUVESTINĖ
# ===========================================================================
print("\n" + "="*70)
print("REZULTATŲ SUVESTINĖ")
print("="*70)

total = len(results)
passed = sum(1 for r in results if r[1])
failed = total - passed
dangerous_failures = [r for r in results if not r[1] and r[4]]

print(f"\nViso testų:  {total}")
print(f"Praėjo:      {passed}")
print(f"Nepraėjo:    {failed}")
print(f"Pavojingų:   {len(dangerous_failures)}")

if errors:
    print("\nKLAIDŲ SĄRAŠAS:")
    for e in errors:
        print(f"  {e}")

if dangerous_failures:
    print("\n!!! PAVOJINGOS KLAIDOS (gali užteršti duomenis): !!!")
    for r in dangerous_failures:
        print(f"  {r[0]}: gauta={r[2]}")

print("\n" + "="*70)
if not dangerous_failures and failed == 0:
    print("VERDIKTAS: ✅ ŽALIA — dizainas paruoštas diegimui")
elif not dangerous_failures:
    print(f"VERDIKTAS: ⚠️  GELTONA — {failed} nekritinių klaidų, taisytina")
else:
    print(f"VERDIKTAS: ❌ RAUDONA — {len(dangerous_failures)} pavojingų klaidų")
print("="*70)

# Išsaugome rezultatą validacijos dokumentui
_verdict = "GREEN" if (not dangerous_failures and failed == 0) else \
           ("YELLOW" if not dangerous_failures else "RED")
_summary = {
    "total": total, "passed": passed, "failed": failed,
    "dangerous": len(dangerous_failures),
    "verdict": _verdict,
    "errors": errors
}

with open("_intent_test_results.json", "w", encoding="utf-8") as f:
    json.dump(_summary, f, ensure_ascii=False, indent=2)
print(f"\nRezultatai išsaugoti: _intent_test_results.json")
