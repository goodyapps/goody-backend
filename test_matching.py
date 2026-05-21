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

total_fails += run("Compact model (WH-1000XM5 vs WH1000XM5B)", "Sony WH-1000XM5", [
    ("Sony WH-1000XM5 Wireless Headphones",         True),   # exact model
    ("Sony WH1000XM5B Black ausinės",               True),   # compact (no hyphen)
    ("Sony WH-1000XM5N Noise Cancelling",           True),   # suffix N
    ("Sony WH-1000XM4 Wireless Headphones",         False),  # different model (XM4 not XM5)
    ("Sony MDR-ZX310 headphones",                   False),  # different model entirely
])

# ── Headset ambiguity (product vs accessory) ─────────────
total_fails += run("headset ambiguity", "Sony WH-1000XM5", [
    ("Sony WH-1000XM5 Wireless Headset Black",      True),   # product (headset = headphones)
    ("Sony WH-1000XM5 Noise Cancelling Headset",    True),   # product descriptor
    ("Bluetooth Headset Adapter for Sony WH-1000XM5", False), # accessory adapter
])

total_fails += run("headset for phone", "iPhone 17", [
    ("Bluetooth Headset for iPhone 17",             False),  # headset = accessory for phone
])

# ── Watch band accessory filter ──────────────────────────────
total_fails += run("watch band filter", "Apple Watch Series 11", [
    ("Apple Watch Series 11 Midnight 45mm GPS",     True),
    ("Apple Watch Series 11 GPS 41mm Starlight",    True),
    ("Apple Watch Series 11 Leather Band 45mm",     False),  # band = accessory
    ("Apple Watch Sport Band 45mm Series 11",       False),  # sport band = accessory
])

# ── Strap / Armband / Pasek accessory filter ─────────────────
total_fails += run("strap filter", "Samsung Galaxy Watch6", [
    ("Samsung Galaxy Watch6 Classic 47mm Black",       True),
    ("Samsung Galaxy Watch6 44mm Gold GPS",            True),
    ("Samsung Galaxy Watch6 Leather Strap 20mm",       False),  # strap = accessory
    ("Samsung Galaxy Watch6 Armband Silikon",          False),  # DE armband = accessory
    ("Pasek Samsung Galaxy Watch6 Sport",              False),  # PL pasek = accessory
    ("Samsung Galaxy Watch6 Dirželis Odinis",          False),  # LT dirželis = accessory
])

# ── Newly-added brands (_KNOWN_BRANDS v6.50) ──────────────────
total_fails += run("new brands", "Xiaomi 14 Pro", [
    ("Xiaomi 14 Pro 512GB Black",                      True),
    ("Xiaomi 14 Pro 256GB White",                      True),
    ("Case for Xiaomi 14 Pro",                         False),  # case = accessory
    ("Xiaomi 14 Pro Tempered Glass Screen Protector",  False),  # screen protector
])

total_fails += run("dreame brand", "Dreame L20 Ultra", [
    ("Dreame L20 Ultra Robot Vacuum",                  True),
    ("Dreame L20 Ultra Complete",                      True),
    ("Replacement Brush for Dreame L20 Ultra",         False),  # replacement = accessory
])

total_fails += run("festool brand", "Festool TSC 55", [
    ("Festool TSC 55 KEB-Plus Cordless Saw",           True),
    ("Festool TSC 55 Li Tracksaw",                     True),
    ("Systainer for Festool TSC 55",                   False),  # carry case
])

# ── Sonos brand filtering ─────────────────────────────────────
total_fails += run("sonos brand", "Sonos Arc", [
    ("Sonos Arc Soundbar 5.0.2 Premium Smart Speaker",  True),
    ("Sonos Arc Ultra Premium Soundbar",                True),
    ("Bose Soundbar 600",                               False),  # different brand
    ("Wall Mount for Sonos Arc",                        False),  # accessory
])

# ── Stihl brand filtering ─────────────────────────────────────
total_fails += run("stihl brand", "Stihl MS 180", [
    ("Stihl MS 180 C-BE Chainsaw 35cm",                True),
    ("Stihl MS 180 14\" Bar Petrol Chainsaw",          True),
    ("Husqvarna 135 Chainsaw",                         False),  # different brand
    ("Replacement Chain for Stihl MS 180",             False),  # replacement = accessory
])

# ── Husqvarna brand filtering ─────────────────────────────────
total_fails += run("husqvarna brand", "Husqvarna Automower 315", [
    ("Husqvarna Automower 315 Robotic Lawn Mower",     True),
    ("Husqvarna Automower 315X",                       True),   # suffix variant (like WH-1000XM5N)
    ("Worx Landroid M700 Plus",                        False),  # different brand
])

# ── New accessory words (v6.85-v6.86) ────────────────────────
total_fails += run("toner accessory", "HP LaserJet M110w", [
    ("HP LaserJet M110w Laser Printer",                True),
    ("HP 78A Toner Cartridge Black",                   False),
    ("HP Tonerkassette 78A Schwarz",                   False),  # DE toner cartridge
])

total_fails += run("cartridge accessory", "Epson EcoTank ET-2850", [
    ("Epson EcoTank ET-2850 Inkjet Printer",           True),
    ("Epson 502XL Ink Cartridge Pack",                 False),
    ("Epson Druckerpatrone T502 Schwarz",              False),  # DE ink cartridge
])

total_fails += run("vacuum bag accessory", "Dyson V15 Detect", [
    ("Dyson V15 Detect Absolute Vacuum Cleaner",       True),
    ("Dyson Staubsaugerbeutel Ersatzpaket",            False),  # DE vacuum bags
    ("Dyson Ersatzbeutel für V15",                     False),  # DE spare bags
])

total_fails += run("robot brush accessory", "Dreame L20 Ultra", [
    ("Dreame L20 Ultra Robot Vacuum",                  True),
    ("Ersatzbürste für Dreame L20 Ultra",              False),  # DE replacement brush
    ("Seitenbürste Dreame L20",                        False),  # DE side brush
])

print(f"\n{'='*60}")
if total_fails == 0:
    print("  Visi testai praejo!")
else:
    print(f"  {total_fails} testai nepraejo!")
print(f"{'='*60}\n")
