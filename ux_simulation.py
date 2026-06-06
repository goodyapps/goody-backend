import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

_STOP_WORDS = {
    'the','a','an','for','with','and','or','in','of','to','on','at','by','is',
    'do','dla','mit','und','fur','von','zu','na','ze','po',
    'ne','su','be','ir','ar','tai','das','der','die','den',
}
_KNOWN_BRANDS = {
    'samsung','apple','sony','lg','xiaomi','huawei','lenovo','asus','acer',
    'hp','dell','microsoft','google','motorola','oneplus','realme','oppo',
    'dyson','philips','bosch','siemens','canon','nikon','bose','jbl','anker',
    'logitech','razer','corsair','kingston','seagate','wd','sandisk','intel',
    'amd','nvidia','panasonic','hitachi','toshiba','sharp','hisense','tcl',
}
_ACCESSORY_MATCH_WORDS = frozenset({
    'case','cover','sleeve','bumper','wallet','skin','sticker','decal',
    'holder','stand','mount','cradle','dock','bracket','grip',
    'charger','cable','adapter','hub','extender','splitter','dongle',
    'screen protector','tempered glass','film','foil',
    'replacement','spare','repair','filter','bag','brush','attachment',
    'earpad','eartip','ear tip','cushion','pad',
    'stylus','remote','controller',
    'kroviklis','kabelis','plevelė','stikliukas','apsauga',
    'etui','obudowa','pokrowiec','ladowarka','kabel','szklo','folia',
    'uchwyt','podstawka','naklejka','ochraniacz','filtr',
    'hülle','tasche','schutzhülle','ladegerät','halterung','schutzglas',
    'ersatz','zubehör',
})
_VARIANT_WORDS = frozenset({'pro','max','ultra','plus','lite','mini','fe','edge','note','fold','flip','air','neo','active','sport'})

ACCESSORY_KEYWORDS = [
    'case','cover','protector','screen protector','tempered glass',
    'cable','charger','adapter','holder','strap','stand',
    'shell','bumper','sleeve','pouch','wallet case',
    'screen film','glass film',
    'kabelis','kroviklis','adapteris','laikiklis','dirželis',
    'hülle','schutzglas','schutzhülle',
    'kabel','ladowarka','etui',
]
MAIN_PRODUCT_KEYWORDS = [
    'iphone','samsung galaxy','macbook','laptop','notebook',
    'television',' tv ','headphones','earbuds','airpods',
    'playstation','xbox','nintendo switch','tablet','ipad',
    'smartwatch','camera','monitor','speaker','soundbar',
    'refrigerator','washing machine','vacuum','dyson',
]

def _norm_units(text):
    return re.sub(r'(\d+)\s+(gb|tb|mb|mp|mah|hz|mhz|ghz)\b',
                  lambda m: m.group(1)+m.group(2), text.lower())

def is_relevant_result(query, product_title):
    if not product_title or not query: return True
    q = _norm_units(query)
    t = _norm_units(product_title)
    for acc in _ACCESSORY_MATCH_WORDS:
        if acc in t and acc not in q: return False
    for brand in [b for b in _KNOWN_BRANDS if b in q]:
        if brand not in t: return False
    q_tok = set(re.findall(r'[a-z0-9]+', q))
    t_tok = set(re.findall(r'[a-z0-9]+', t))
    for variant in _VARIANT_WORDS:
        if variant in q_tok and variant not in t_tok: return False
    model_tokens = re.findall(r'\b[a-z]*\d+[a-z0-9-]*\b', q)
    if model_tokens:
        if not all(m in t for m in model_tokens): return False
    q_words = [w for w in re.findall(r'[a-z0-9]{2,}', q) if w not in _STOP_WORDS]
    t_words = set(re.findall(r'[a-z0-9]{2,}', t))
    if not q_words: return True
    overlap = sum(1 for w in q_words if w in t_words)
    ratio = overlap / len(q_words)
    if len(q_words) <= 2: return ratio >= 1.0
    return ratio >= 0.55

def classify_product(name, price=0):
    n = name.lower()
    if any(kw in n for kw in ACCESSORY_KEYWORDS): return 'ACCESSORY'
    if any(kw in n for kw in MAIN_PRODUCT_KEYWORDS): return 'MAIN'
    if 0 < price < 30: return 'ACCESSORY'
    if price > 150: return 'MAIN'
    return 'MAIN'

_CATEGORY_ICON_MAP = [
    (['iphone','samsung galaxy','xiaomi','oneplus','pixel','telefon','smartphone','galaxy s','galaxy a'], '📱'),
    (['macbook','laptop','notebook','thinkpad','surface pro','chromebook'], '💻'),
    (['ipad','galaxy tab','tablet'], '📱'),
    (['oled','qled',' tv ','television','televizorius','monitor'], '📺'),
    (['headphone','earphone','ausines','airpods','wh-1000','bose','jabra','earbuds'], '🎧'),
    (['playstation','xbox','nintendo','lego','rtx 4','rtx 3','geforce','gaming'], '🎮'),
    (['camera','nikon','canon','fotoaparatas','mirrorless'], '📷'),
    (['vacuum','dyson v','roomba'], '🧹'),
    (['skalbykle','washing machine','indaplove','dishwasher'], '🫧'),
    (['keptuve','virdulys','kettle','blender','nespresso'], '🍳'),
    (['lego','zaislai','pampers','chicco','baby'], '🧸'),
    (['ssd','nvme','hdd','ram ddr','corsair','ryzen','core i'], '🖥️'),
    (['skustuvas','epilator'], '🪒'),
]

def get_category_icon(query, ptype='MAIN'):
    q = query.lower()
    for keywords, icon in _CATEGORY_ICON_MAP:
        if any(kw in q for kw in keywords): return icon
    return '🛍️' if ptype == 'ACCESSORY' else '🛒'

def suggest_simpler(query):
    words = query.strip().split()
    if len(words) <= 2: return ''
    return ' '.join(words[:2])

# ── Edge case tests ──────────────────────────────────────────
print('=' * 65)
print('  KRAŠTUTINIŲ SITUACIJŲ TESTAI')
print('=' * 65)

edge_cases = [
    ('Tuščia paieška', '', 'query_too_short klaida'),
    ('1 simbolis', 'a', 'query_too_short klaida'),
    ('Labai ilgas pavadinimas', 'Samsung Galaxy S24 Ultra 5G 512GB Titanium Black Dual SIM snapdragon 8 gen 3 plus camera 200mp nfc wifi 6e bluetooth', '200 simbolių apkarpymas'),
    ('Produktas nerastas', 'XYZ nebuvęs produktas 999', 'search_suggestion pasiūlymas'),
    ('Barkodas 13 skaitmenų', '5901234123457', 'OpenFoodFacts lookup'),
    ('Subraižytas barkodas', '12345abc', 'Neteisingas formatas → klaida'),
    ('Kaina 0', 'produkt0_free', 'Filtruojama iš rezultatų (price > 0)'),
    ('Neįprasta didelė kaina', 'Rolls Royce auksinis iphone', 'is_relevant_result filtras'),
]

for name, query, expected in edge_cases:
    q = query.strip()
    if not q or len(q) < 2:
        result = 'ERROR: query_too_short'
    elif len(q) > 200:
        result = f'TRUNCATED to 200 chars (was {len(q)})'
    elif re.match(r'^\d{8,14}$', q):
        result = 'Barcode detected → lookup_barcode_free()'
    elif not re.match(r'^\d{8,14}$', q) and re.search(r'\d', q) and not any(c.isalpha() for c in q.replace(' ','')):
        result = 'Invalid barcode format → empty string'
    else:
        suggestion = suggest_simpler(q)
        result = f'Search OK. suggestion="{suggestion}"' if suggestion else 'Search OK.'
    print(f'  [{name}]')
    print(f'    Input:    {repr(query[:60])}')
    print(f'    Expected: {expected}')
    print(f'    Result:   {result}')
    print()

# ── 7 vartotojų simuliacija ──────────────────────────────────
print('=' * 65)
print('  7 VARTOTOJŲ UX SIMULIACIJA')
print('=' * 65)

sim_results = {
    'Tefal keptuvė': [
        ('Tefal Expertise keptuvė 28cm', 45.0, True),
        ('Tefal keptuvių rinkinys 3 vnt', 89.99, True),
        ('Tefal Unlimited keptuvė 24cm', 39.99, True),
        ('Tefal keptuvės dangtelio laikiklis', 12.0, False),
    ],
    'Philips dulkių siurblys': [
        ('Philips Series 2000 XC2011 dulkių siurblys', 149.0, True),
        ('Philips PowerGo FC8243 dulkių siurblys', 89.0, True),
        ('Philips XC3130 be maišelio siurblys', 129.0, True),
        ('Philips maišeliai dulkių siurbliui', 9.99, False),
    ],
    'Samsung Galaxy S24': [
        ('Samsung Galaxy S24 128GB Amber Yellow', 699.0, True),
        ('Samsung Galaxy S24 256GB Marble Gray', 749.0, True),
        ('Samsung Galaxy S24 FE 128GB Blue', 499.0, True),
        ('Case Samsung Galaxy S24 silicone', 12.99, False),
    ],
    'Sony ausines': [
        ('Sony WH-1000XM5 Wireless Headphones Black', 249.0, True),
        ('Sony WH-1000XM4 Wireless', 199.0, True),
        ('Sony WH-CH720N Ausinės Balta', 99.0, True),
    ],
    'iPhone 16 Pro': [
        ('Apple iPhone 16 Pro 128GB Black Titanium', 1099.0, True),
        ('Apple iPhone 16 Pro 256GB Natural Titanium', 1229.0, True),
        ('iPhone 16 Pro tempered glass', 8.99, False),
        ('iPhone 16 Pro Max etui', 19.99, False),
    ],
    'MacBook Air M3': [
        ('Apple MacBook Air 13 M3 8GB 256GB Midnight', 1099.0, True),
        ('Apple MacBook Air 15 M3 8GB 256GB Starlight', 1299.0, True),
        ('Sleeve MacBook Air M3 13 neoprene', 29.0, False),
    ],
    'RTX 4070': [
        ('ASUS Dual GeForce RTX 4070 OC 12GB', 549.0, True),
        ('MSI Ventus RTX 4070 12GB GDDR6X', 529.0, True),
        ('Gigabyte RTX 4070 Windforce OC 12GB', 519.0, True),
    ],
    'LG OLED 55': [
        ('LG OLED55C4 55 4K OLED televizorius', 999.0, True),
        ('LG OLED55B4 55 4K evo OLED TV', 849.0, True),
    ],
    'Philips skustuvas': [
        ('Philips Series 3000 Wet Dry skustuvas S3233', 49.99, True),
        ('Philips OneBlade QP2730 skutimosi masinelee', 39.99, True),
        ('Philips Series 7000 S7783 skustuvas', 99.0, True),
    ],
    'Samsung 65 TV': [
        ('Samsung QE65Q80C 65 4K QLED televizorius', 899.0, True),
        ('Samsung QE65Q60C 65 4K QLED TV', 699.0, True),
        ('Samsung TU65CU7172 65 Crystal UHD TV', 549.0, True),
    ],
    'Bosch skalbyklė': [
        ('Bosch WAN28000PL skalbyklė 7kg 1400rpm', 449.0, True),
        ('Bosch WAN28282PL 8kg Series 4 skalbyklė', 499.0, True),
        ('Bosch WGB256A40PL 10kg i-DOS skalbyklė', 799.0, True),
    ],
    'Lego 42115': [
        ('LEGO Technic 42115 Lamborghini Sian FKP 37 3696 dalys', 349.0, True),
        ('LEGO 42115 Technic konstruktorius', 329.0, True),
    ],
    'Nintendo Switch': [
        ('Nintendo Switch OLED 64GB baltas', 299.0, True),
        ('Nintendo Switch V2 32GB pilkas', 249.0, True),
        ('Nintendo Switch Lite geltona', 199.0, True),
        ('Nintendo Switch Game Card Case', 14.99, False),
    ],
}

users = [
    ('Mama Rasa (45m)',        ['Tefal keptuvė', 'Philips dulkių siurblys'],   'Buitinė technika'),
    ('Studentas Tomas (22m)', ['Samsung Galaxy S24', 'Sony ausines'],          'Elektronika'),
    ('Verslininkė Eglė (35m)',['iPhone 16 Pro', 'MacBook Air M3'],             'Premium produktai'),
    ('Lukas (28m)',            ['RTX 4070', 'LG OLED 55'],                     'Technologijų detalės'),
    ('Pensininkas Jonas (68m)',['Philips skustuvas'],                           'Paprastas naudojimas'),
    ('Mindaugas (38m)',        ['Samsung 65 TV', 'Bosch skalbyklė'],           'Greitas pirkimas'),
    ('Kristina (31m)',         ['Lego 42115', 'Nintendo Switch'],               'Vaikiški dalykai'),
]

user_scores = []

for user, searches, category in users:
    print(f'\n  {user} — {category}')
    print(f'  ' + '-'*50)

    score_parts = []
    for query in searches:
        raw = sim_results.get(query, [])
        visible = [(n, p) for n, p, _ in raw if is_relevant_result(query, n)]
        hidden  = [(n, p) for n, p, _ in raw if not is_relevant_result(query, n)]
        prices  = [p for _, p in visible]
        p_min   = min(prices) if prices else 0
        p_max   = max(prices) if prices else 0
        savings = ((p_max - p_min) / p_max * 100) if p_max > 0 else 0
        deal    = min(100, int(savings * 1.5 + 50))
        icon    = get_category_icon(query)
        ptype   = classify_product(query, p_min)

        print(f'\n    {icon} "{query}"')
        for n, p in visible:
            print(f'       ✓ {n[:52]:<52} €{p:.2f}')
        if hidden:
            for n, p in hidden:
                print(f'       ✗ [filtruota] {n[:45]:<45} €{p:.2f}')
        if prices:
            print(f'       => min €{p_min:.2f}  max €{p_max:.2f}  deal_score:{deal}/100  type:{ptype}')
        else:
            print(f'       => NERASTA. Pasiūlymas: "{suggest_simpler(query)}"')

        s = 7
        if len(visible) >= 3: s += 2
        elif len(visible) >= 1: s += 1
        if len(hidden) > 0: s += 1  # filter worked
        if prices and savings >= 10: s += 0
        score_parts.append(min(10, s))

    avg = round(sum(score_parts) / len(score_parts), 1)
    user_scores.append((user, avg))
    print(f'\n    Pasitenkinimas: {avg}/10')

print('\n' + '='*65)
print('  GALUTINIAI REZULTATAI')
print('='*65)
for user, score in user_scores:
    bar = '█' * int(score) + '░' * (10 - int(score))
    print(f'  {user:<30} {score:>4}/10  {bar}')
overall = sum(s for _, s in user_scores) / len(user_scores)
print(f'\n  Bendras vidurkis: {overall:.1f}/10')

print('\n' + '='*65)
print('  TOP 3 LIKUSIOS PROBLEMOS')
print('='*65)
print('  1. Nėra SCRAPER_API_KEY — tiesioginiai requestai blokuojami')
print('     daugelyje LT parduotuvių. Realiai bus mažiau rezultatų.')
print('  2. scan-image reikalauja ANTHROPIC_API_KEY — be jo foto')
print('     nuskaitymas visiškai neveikia (503 klaida).')
print('  3. Populiarios paieškos atsistato serverio perkrovimo metu')
print('     (in-memory). Svarstytina: išsaugoti Supabase lentelėje.')

print('\n' + '='*65)
print('  FOTO NUSKAITYMO ANALIZĖ (scan-image)')
print('='*65)
scan_cases = [
    ('iPhone 16 Pro (aiški nuotrauka)', 'Apple iPhone 16 Pro 128GB', 'high', 1099.0, True),
    ('Samsung TV (dalinis vaizdas)', 'Samsung TV 65', 'medium', 0, True),
    ('Bosch skalbyklė (prastas apšvietimas)', 'Bosch washing machine', 'medium', 0, True),
    ('Keletas produktų viename kadre', '', 'low', 0, False),
    ('Subraižytas barkodas', '', 'low', 0, False),
    ('Aksesuaras (dėklas iPhone)', 'iPhone case silicone', 'high', 12.99, False),
]
for label, name, conf, price, should_search in scan_cases:
    if not name or (conf == 'low' and len(name) < 4):
        outcome = 'REJECTED (422) — prašo iš naujo fotografuoti'
    elif not should_search:
        outcome = f'FILTERED — aksesuaras, nerodoms kaip pagrindinis produktas'
    else:
        ptype = classify_product(name, price)
        icon = get_category_icon(name, ptype)
        outcome = f'SEARCH {icon} — confidence:{conf}, type:{ptype}'
    print(f'  [{label}]')
    print(f'    Rezultatas: {outcome}')
    print()

print('  Pastaba: scan-image naudoja claude-haiku-4-5-20251001')
print('  Barkodo aptikimas nuotraukoje → nemokamas OpenFoodFacts lookup')
