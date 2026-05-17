import sys, io, os

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf-8-sig'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Import the real function from server so tests always reflect production logic
os.environ.setdefault('SUPABASE_URL', '')
os.environ.setdefault('SUPABASE_KEY', '')
from server import is_relevant_result


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
        mark = '' if ok else '  <- MISMATCH'
        print(f"  [{tag}] {show} (exp {exp}): {title}{mark}")
    return fails


total_fails = 0

# ── iPhone 17 Pro 256GB ───────────────────────────────────────
total_fails += run("telefonas", "iPhone 17 Pro 256GB", [
    ("Apple iPhone 17 Pro 256GB Black Titanium",        True),
    ("Apple iPhone 17 Pro 256GB Natural Titanium",      True),
    ("iPhone 17 Pro 256 GB Smartphone",                 True),
    ("Apple iPhone 17 Pro 256GB – Black",          True),

    ("Apple iPhone 17 Pro 512GB",                       False),
    ("Apple iPhone 17 Pro 128GB Black",                 False),

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

    ("Samsung Galaxy S24 Ultra 256GB",                  False),
    ("Samsung Galaxy S24 Plus 512GB",                   False),
    ("Case Samsung Galaxy S24 Ultra",                   False),
    ("Etui Samsung S24 Ultra 512GB",                    False),
    ("Samsung Galaxy S24 Ultra Charger 45W",            False),
    ("Tempered glass Samsung S24 Ultra",                False),
])

# ── Sony WH-1000XM5 ───────────────────────────────────────────
total_fails += run("ausines", "Sony WH-1000XM5", [
    ("Sony WH-1000XM5 Wireless Noise Cancelling Headphones Black", True),
    ("Sony WH-1000XM5 Silver",                          True),

    ("Sony WH-1000XM4",                                 False),
    ("Case for Sony WH-1000XM5",                        False),
    ("Sony WH-1000XM5 Cable USB-C",                     False),
    ("Earpad Replacement Sony WH-1000XM5",              False),
])

# ── MacBook Pro 14 M4 ─────────────────────────────────────────
total_fails += run("laptop", "MacBook Pro 14 M4", [
    ("Apple MacBook Pro 14 M4 16GB 512GB Silver",       True),
    ("Apple MacBook Pro 14-inch M4 Space Black",        True),

    ("MacBook Pro 13 M4",                               False),
    ("MacBook Pro 14 M3",                               False),
    ("Case MacBook Pro 14 M4",                          False),
    ("Sleeve for MacBook Pro 14",                       False),
    ("USB-C Hub MacBook Pro 14 M4",                     False),
])

# ── Dyson V15 Detect ──────────────────────────────────────────
total_fails += run("siurblys", "Dyson V15 Detect", [
    ("Dyson V15 Detect Absolute Vacuum Cleaner",        True),
    ("Dyson V15 Detect Extra",                          True),

    ("Dyson V12 Detect",                                False),
    ("Dyson V15 Detect Replacement Filter",             False),
    ("Dyson V15 Detect Charger",                        False),
])

# ── Trumpi užklausos ──────────────────────────────────────────
total_fails += run("trumpas", "iPhone 17", [
    ("Apple iPhone 17 128GB Black",                     True),
    ("Apple iPhone 17 Pro 256GB",                       True),

    ("Case iPhone 17",                                  False),
    ("iPhone 17 Tempered Glass",                        False),
])

# ── Lietuviškos užklausos (non-ASCII) ────────────────────────
total_fails += run("LT ausines", "Sony ausinės", [
    ("Sony WH-1000XM5 belaidės ausinės juodos",         True),
    ("Sony WH-1000XM5 Kabellose Kopfhörer Schwarz",    True),   # DE → SHOW
    ("Sony WH-1000XM5 Bezprzewodowe Słuchawki",        True),   # PL → SHOW
    ("Sony WH-1000XM5 Cable USB-C replacement",        False),
    ("Earpad Replacement Sony ausinėms",                False),
])

total_fails += run("LT skustuvas", "Philips skustuvas", [
    ("Philips Series 3000 Wet Dry Shaver S3233",        True),
    ("Philips S7783 Electric Shaver Series 7000",       True),
    ("Philips Elektrorasierer Series 3000 S3233",       True),   # DE → SHOW
    ("Philips Ersatz-Scherblatt für Rasierer",          False),  # DE accessory
])

total_fails += run("LT skalbykle", "Bosch skalbyklė", [
    ("Bosch WAN28000PL Washing Machine 7kg",            True),
    ("Bosch Serie 4 Waschmaschine 8kg WAN28282PL",     True),   # DE → SHOW
    ("Bosch WGB256A40PL 10kg i-DOS skalbyklė",         True),
    ("Bosch Filtras skalbyklei",                        False),
])

total_fails += run("LT priedai", "Philips dulkių siurblys", [
    ("Philips XC2011 Series 2000 dulkių siurblys",      True),
    ("Philips PowerGo FC8243 siurblys",                 True),
    ("Philips maišeliai dulkių siurbliui FC8021",       False),  # bags → HIDE
    ("Philips siurblių filtrai HR6999",                 False),  # filters → HIDE
])

print(f"\n{'='*60}")
if total_fails == 0:
    print("  Visi testai praejo!")
else:
    print(f"  {total_fails} testai nepraejo!")
print(f"{'='*60}\n")
