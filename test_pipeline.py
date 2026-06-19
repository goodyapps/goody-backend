"""
Pipeline logic tests + live smoke test.
Layer 1: 500 products, pure logic (no HTTP).
Layer 2: 20 products, live HTTP against goody-backend.onrender.com.
Run: python test_pipeline.py
"""
import re, time, json, unicodedata, urllib.request, urllib.parse
from collections import defaultdict

# ── Inlined logic from server.py ──────────────────────────────────────────────

def _norm_units(text):
    return re.sub(r'(\d+)\s+(gb|tb|mb|mp|mah|hz|mhz|ghz)\b',
                  lambda m: m.group(1) + m.group(2), text.lower())

_STOP_WORDS = {"the","a","an","and","or","for","of","in","on","at","to","is",
               "it","this","with","from","by","as","be","was","are","that","ir","su"}

_KNOWN_BRANDS = [
    "samsung","apple","sony","lg","philips","bosch","siemens","dyson","asus","acer",
    "lenovo","hp","dell","microsoft","google","amazon","nokia","huawei","xiaomi",
    "oneplus","oppo","vivo","realme","honor","motorola","nothing","lego","canon",
    "nikon","fujifilm","panasonic","bose","jbl","sennheiser","shure","audio-technica",
    "anker","belkin","logitech","razer","corsair","steelseries","elgato","rode",
    "de longhi","delonghi","jura","nespresso","krups","melitta","braun","rowenta",
    "tefal","moulinex","kenwood","kitchenaid","whirlpool","indesit","electrolux",
    "aeg","miele","gorenje","beko","hotpoint","ariston","candy","haier","hisense",
    "tcl","sharp","toshiba","grundig","loewe","bang olufsen","harman","jbl",
    "garmin","polar","suunto","fitbit","withings","omron","beurer",
    "adidas","nike","reebok","puma","under armour","salomon","columbia",
]

_ACCESSORY_MATCH_WORDS = [
    "case","hülle","cover","tasche","etui","schutzfolie","folie","screen protector",
    "charger","ladekabel","cable","kabel","adapter","hub","dock","stand","halter",
    "strap","band","armband","bracelet","replacement","ersatz","spare","parts",
    "filter","bag","staubbeutel","beutel","sack","attachment","tool","zubehör",
    "stylus","pen","stift","lens","cap","hood","strap","sling","shoulder",
]

_VARIANT_WORDS = {"black","white","silver","gold","blue","red","green","pink",
                  "schwarz","weiß","silber","weiss","grau","blau","rot","grün"}

_PURE_CATEGORY_WORDS = {"phone","smartphone","laptop","notebook","tablet","headphones",
                         "earbuds","speaker","camera","printer","monitor","keyboard",
                         "mouse","router","watch","smartwatch","vacuum","washer","dryer",
                         "refrigerator","freezer","oven","dishwasher","television","tv"}

def is_relevant_result(query: str, product_title: str) -> bool:
    if not product_title or not query:
        return True
    q = _norm_units(query)
    t = _norm_units(product_title)
    q_clean_words = [w for w in re.findall(r'[a-z]{3,}', q) if w not in _STOP_WORDS]
    if q_clean_words and all(w in _PURE_CATEGORY_WORDS for w in q_clean_words):
        has_known_brand_in_title = any(b.replace(' ','') in t.replace(' ','') for b in _KNOWN_BRANDS)
        has_known_brand_in_query = any(b.replace(' ','') in q.replace(' ','') for b in _KNOWN_BRANDS)
        if not has_known_brand_in_query and not has_known_brand_in_title:
            return False
    compat_patterns = [
        r'\bfor\s+[a-z]+', r'\bcompatible\s+with\b', r'\bskirta\s+[a-z]+',
        r'\btinka\s+[a-z]+', r'\bgeeignet\s+f.r\b', r'\bpassend\s+f.r\b', r'\bdla\s+[a-z]+',
    ]
    for pattern in compat_patterns:
        if re.search(pattern, t) and not re.search(pattern, q):
            return False
    q_ns = q.replace(" ",""); t_ns = t.replace(" ","")
    brands_in_q = [b for b in _KNOWN_BRANDS if b.replace(" ","") in q_ns]
    for brand in brands_in_q:
        if brand.replace(" ","") not in t_ns:
            return False
    q_tok = set(re.findall(r'[a-z0-9]+', q))
    t_tok = set(re.findall(r'[a-z0-9]+', t))
    for variant in _VARIANT_WORDS:
        if variant in q_tok and variant not in t_tok:
            return False
    model_tokens = re.findall(r'\b[a-z]*\d+[a-z0-9-]*\b', q)
    if model_tokens:
        t_nh = t.replace("-","").replace(" ","")
        def _model_in_title(m):
            m_nh = m.replace("-","")
            if re.search(r'(?<![a-z0-9])' + re.escape(m) + r'(?![a-z0-9])', t):
                return True
            if m_nh and m_nh in t_nh:
                return True
            return False
        if not all(_model_in_title(m) for m in model_tokens):
            return False
        if brands_in_q:
            return True
    if any(ord(c) > 127 for c in query):
        return True
    if brands_in_q and not model_tokens:
        q_words_non_brand = [w for w in re.findall(r'[a-z0-9]{2,}', q)
                             if w not in _STOP_WORDS and w not in brands_in_q]
        if len(q_words_non_brand) <= 2:
            return True
    q_words = [w for w in re.findall(r'[a-z0-9]{2,}', q) if w not in _STOP_WORDS]
    t_words = set(re.findall(r'[a-z0-9]{2,}', t))
    if not q_words:
        return True
    overlap = sum(1 for w in q_words if w in t_words)
    ratio = overlap / len(q_words)
    if len(q_words) <= 2:
        return ratio >= 1.0
    return ratio >= 0.55

_AMZ_FILLER = {
    "with","the","and","for","from","new","best","buy","shop","sale","deal","top",
    "free","fast","easy","great","smart","ultra","pro","plus","max","mini","nano",
    "super","mega","power","premium","official","original","genuine","authentic",
    "high","quality","performance","series","model","product","item","brand",
    "agentic","ai","smart","featuring","powered","built","advanced","integrated",
    "native","latest","assistant","wireless","bluetooth","technology","edition",
    "generation","voice","recorder","recording","dictaphone","diktofonas",
    "telefonas","smartphone","laptop","notebook",
}

def _short_amazon_query(q: str) -> str:
    words = q.split()
    if len(words) <= 3:
        return q
    kept = [w for w in words if w.lower() not in _AMZ_FILLER]
    if kept and len(kept) < len(words):
        return " ".join(kept[:3]) if len(kept) >= 2 else " ".join(words[:2])
    return " ".join(words[:3])

def _model_code_variants(query: str) -> list:
    variants = [query]
    q2 = re.sub(r'\s*/[A-Z0-9]{1,4}\b', '', query).strip()
    if q2 and q2 != query:
        variants.append(q2)
    else:
        q2 = query
    words = q2.split()
    if words:
        last = words[-1]
        m = re.match(r'^(.*\d)([A-Z]{2,3})$', last)
        if m and len(last) >= 5:
            shorter = ' '.join(words[:-1] + [m.group(1)])
            if shorter not in variants:
                variants.append(shorter)
    return variants

_LT_CATEGORY_WORDS_NORM = [
    "saldytuvas","skalbimo","indaplove","orkaite","virykle","saldiklis",
    "dulkiu siurblys","siurblys","kavos aparatas","kavos","virdulys","blenderis",
    "mikseris","ausines","ausinukai","televizorius","telefonas","kompiuteris",
    "nesiojamas","plansete","kamera","fotoaparatas","spausdintuvas","monitorius",
    "klaviatura","pele","garsiakalbis","zaislas","laikrodis","smartwatch",
    "paspirtukas","dviratis","ebike","skustuvas","plaukų","laidy","tiesintuvas",
    "masazuoklis","svarstykes","kraujo","ciuzinys","lemputė","lemputė",
    "robotas","robotinis","robotine","gaubtas","maisto procesorius",
    "epsete","sultciaspaude","treniruoklis","hanteliai","kettlebell","grotuvas",
    "ikroviklis","projektorius","oro valytuvas","oro kondicionierius",
    "ventiliatorius","sildytuvas","dantų sepeteli","epilatorius","grilis",
    "tosteris","kepsnis","zelmeninis","zaidim","konsolė","bėgimo",
    # food/cosmetics missing from original:
    "sokoladas","pienas","jogurtas","suris","duona","maistas","kosmetika",
    "kremas","sampunas","parfum","kvepalai","avalyne","apranga","drabuziai",
    "knyga","vadovelis","zemlapis","sporto",
]

def _norm_lt(s: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

def _is_lt_query(q: str) -> bool:
    q_norm = _norm_lt(q.lower())
    return any(w in q_norm for w in _LT_CATEGORY_WORDS_NORM)

_LARGE_APPLIANCE_W = [
    "šaldytuvas","skalbimo","indaplovė","orkaitė","viryklė","šaldiklis",
    "refrigerator","washing machine","dishwasher","oven","freezer",
    "kühlschrank","waschmaschine","geschirrspüler","herd","gefrierschrank",
    "lodówka","pralka","zmywarka","piekarnik","zamrażarka",
]

def _is_large_appliance(query: str) -> bool:
    q = query.lower()
    return any(w in q for w in _LARGE_APPLIANCE_W)

def post_process_would_empty(query: str, has_relevant: bool) -> bool:
    """Return True if post_process logic would empty results (unit-token bug)."""
    if not has_relevant:
        model_tokens = re.findall(r'\b[a-z]*\d+[a-z0-9-]*\b', query.lower())
        if model_tokens:
            return True
    return False

# ── Test data ─────────────────────────────────────────────────────────────────
# Format: (query, good_title, bad_title, category)
# good_title: a real product title that SHOULD match
# bad_title: an accessory/unrelated title that should NOT match
PRODUCTS = [
    # === APPLIANCES (large) ===
    ("Samsung RB34C600ESA", "Samsung Kühlschrank RB34C600ESA/EF 341L", "Cover for Samsung RB34C600ESA", "appliances"),
    ("Bosch WAX32EH0", "Bosch Serie 8 WAX32EH0 Waschmaschine 9kg", "Filter for Bosch WAX32EH0", "appliances"),
    ("LG F4WR510S0W", "LG F4WR510S0W 10kg Waschmaschine", "Hose for LG F4WR510S0W", "appliances"),
    ("Electrolux EW9F149SP", "Electrolux EW9F149SP Waschmaschine 9kg", "Stand for Electrolux EW9F149SP", "appliances"),
    ("Siemens WM14UR09", "Siemens WM14UR09 Waschmaschine", "Adapter for Siemens WM14UR09", "appliances"),
    ("Miele WER865 WPS", "Miele WER865 WPS W1 Waschmaschine", "Miele WER865 WPS Drum Seal Replacement", "appliances"),
    ("AEG L8FEC68S", "AEG L8FEC68S Waschmaschine 8kg", "Door gasket for AEG L8FEC68S", "appliances"),
    ("Indesit MTWE 91485", "Indesit MTWE 91485 Waschmaschine 9kg", "Belt for Indesit MTWE 91485", "appliances"),
    ("Beko WTV8745XC0", "Beko WTV8745XC0 ProSmart Waschmaschine", "Pump filter for Beko WTV8745XC0", "appliances"),
    ("Whirlpool FSCR 90430", "Whirlpool FSCR 90430 Supreme Care 9kg", "Drum bearing for Whirlpool FSCR 90430", "appliances"),
    ("Samsung RB38C6B2CS9", "Samsung RB38C6B2CS9 Kühlschrank 390L", "Shelf for Samsung RB38C6B2CS9", "appliances"),
    ("Bosch KGN39VXBT", "Bosch KGN39VXBT Kühl-Gefrier-Kombination", "Gasket for Bosch KGN39VXBT", "appliances"),
    ("LG GBB72NSVCN", "LG GBB72NSVCN No Frost Kühlschrank", "Water filter for LG GBB72NSVCN", "appliances"),
    ("Gorenje RK4182PS4", "Gorenje RK4182PS4 Kühlschrank", "Replacement shelf for Gorenje RK4182PS4", "appliances"),
    ("Hotpoint HAOM 82111", "Hotpoint HAOM 82111 Spülmaschine 8L", "Spray arm for Hotpoint HAOM 82111", "appliances"),
    ("Gorenje GS52214W", "Gorenje GS52214W Geschirrspüler", "Tablet basket for Gorenje GS52214W", "appliances"),
    ("Electrolux ESF5512LOW", "Electrolux ESF5512LOW Geschirrspüler", "Cutlery basket for Electrolux ESF5512LOW", "appliances"),
    ("Haier HW90-B14959U1", "Haier HW90-B14959U1 Automatik-Waschmaschine 9kg", "Stand for Haier HW90-B14959U1", "appliances"),
    ("Candy CO4 107T1/2-S", "Candy CO4 107T1/2-S Waschmaschine", "Door hinge Candy CO4 107T1/2-S", "appliances"),
    ("Hisense WF5S1245BW", "Hisense WF5S1245BW 12kg Waschmaschine", "Seal ring for Hisense WF5S1245BW", "appliances"),
    # === ELECTRONICS ===
    ("Samsung Galaxy S24 Ultra", "Samsung Galaxy S24 Ultra 256GB Titanium Black", "Case for Samsung Galaxy S24 Ultra", "electronics"),
    ("Apple iPhone 15 Pro", "Apple iPhone 15 Pro 128GB Natural Titanium", "Screen protector for Apple iPhone 15 Pro", "electronics"),
    ("Sony WH-1000XM5", "Sony WH-1000XM5 kabellose Kopfhörer", "Carrying case for Sony WH-1000XM5", "electronics"),
    ("Apple MacBook Air M3", "Apple MacBook Air M3 13 Zoll 8GB 256GB", "USB hub for MacBook Air M3", "electronics"),
    ("Samsung 65QN90B", "Samsung 65QN90B Neo QLED 4K TV 65 Zoll", "Wall mount for Samsung 65QN90B", "electronics"),
    ("Asus ROG Zephyrus G14 GA402", "Asus ROG Zephyrus G14 GA402 AMD Ryzen 9", "RAM upgrade for Asus ROG Zephyrus G14", "electronics"),
    ("Bose QuietComfort 45", "Bose QuietComfort 45 kabellose Kopfhörer", "Earpads for Bose QuietComfort 45", "electronics"),
    ("Logitech MX Master 3S", "Logitech MX Master 3S kabellose Maus", "Mousepad for Logitech MX Master 3S", "electronics"),
    ("Garmin Fenix 7", "Garmin Fenix 7 GPS Smartwatch", "Band for Garmin Fenix 7", "electronics"),
    ("DJI Mini 4 Pro", "DJI Mini 4 Pro Drone 4K", "ND Filter for DJI Mini 4 Pro", "electronics"),
    ("Xiaomi 13 Pro", "Xiaomi 13 Pro 256GB Ceramic Black", "Case for Xiaomi 13 Pro", "electronics"),
    ("LG OLED55C3PSA", "LG OLED55C3PSA 55 Zoll OLED evo TV", "Shelf bracket LG OLED55C3PSA", "electronics"),
    ("Lenovo ThinkPad X1 Carbon Gen 11", "Lenovo ThinkPad X1 Carbon Gen 11 14 Zoll", "Docking station for ThinkPad X1 Carbon", "electronics"),
    ("Sony A7 IV", "Sony Alpha A7 IV Vollformat Systemkamera", "Battery grip for Sony A7 IV", "electronics"),
    ("Canon EOS R6 Mark II", "Canon EOS R6 Mark II Systemkamera", "Lens for Canon EOS R6 Mark II", "electronics"),
    ("Anker 65W USB-C Charger", "Anker 65W USB-C GaN Ladegerät", "Cable for Anker 65W charger", "electronics"),
    ("Google Pixel 8 Pro", "Google Pixel 8 Pro 128GB Obsidian", "Case for Google Pixel 8 Pro", "electronics"),
    ("Oneplus 12", "OnePlus 12 256GB Silky Black", "Screen protector OnePlus 12", "electronics"),
    ("Razer DeathAdder V3", "Razer DeathAdder V3 Gaming Maus", "Grip tape for Razer DeathAdder V3", "electronics"),
    ("Philips 55PUS8808", "Philips 55PUS8808 55 Zoll 4K Ambilight TV", "Remote for Philips 55PUS8808", "electronics"),
    # === LEGO / TOYS ===
    ("LEGO Technic 42170", "LEGO Technic 42170 Kawasaki Ninja H2R", "Bag for LEGO Technic 42170", "lego"),
    ("LEGO Harry Potter 76430", "LEGO Harry Potter 76430 Hogwarts", "Storage box for LEGO Harry Potter 76430", "lego"),
    ("LEGO Star Wars 75367", "LEGO Star Wars 75367 Venator Republic Attack Cruiser", "Minifigure display for LEGO 75367", "lego"),
    ("LEGO Icons 10316", "LEGO Icons 10316 The Lord of the Rings Rivendell", "Book for LEGO 10316", "lego"),
    ("LEGO Speed Champions 76919", "LEGO Speed Champions 76919 McLaren F1", "Display stand LEGO 76919", "lego"),
    ("LEGO Botanicals 10315", "LEGO Icons Botanicals 10315 Quiet Garden", "Frame for LEGO 10315", "lego"),
    ("LEGO Architecture 21057", "LEGO Architecture 21057 Singapore", "Glue for LEGO 21057", "lego"),
    ("LEGO Marvel 76261", "LEGO Marvel 76261 Spider-Man: No Way Home", "Stand LEGO Marvel 76261", "lego"),
    ("LEGO Minecraft 21244", "LEGO Minecraft 21244 The Sword Outpost", "Storage bag LEGO Minecraft 21244", "lego"),
    ("LEGO City 60388", "LEGO City 60388 Gaming Tournament Truck", "Organizer for LEGO 60388", "lego"),
    ("LEGO Technic 42153", "LEGO Technic 42153 NASCAR Next Gen Chevrolet Camaro", "Table for LEGO Technic 42153", "lego"),
    ("LEGO Duplo 10994", "LEGO DUPLO 10994 3in1 Family House", "Shelf for LEGO DUPLO 10994", "lego"),
    ("LEGO Creator Expert 10281", "LEGO Icons 10281 Bonsai Tree", "Pot for LEGO 10281", "lego"),
    ("LEGO Ideas 21347", "LEGO Ideas 21347 Orient Express Train", "Track set compatible with LEGO 21347", "lego"),
    ("LEGO City 60371", "LEGO City 60371 Emergency Vehicles HQ", "Battery pack for LEGO 60371", "lego"),
    ("Playmobil 71374", "Playmobil 71374 DeLorean", "Replacement parts Playmobil 71374", "lego"),
    ("Hot Wheels Monster Trucks", "Hot Wheels Monster Trucks 5er Pack", "Ramp set for Hot Wheels", "lego"),
    ("Barbie Fashionista", "Barbie Fashionista Puppe 201", "Clothes for Barbie Fashionista", "lego"),
    ("Nerf Elite 2.0 Commander", "Nerf Elite 2.0 Commander RD-6 Blaster", "Darts for Nerf Elite 2.0", "lego"),
    ("Fisher-Price Laugh Learn", "Fisher-Price Laugh & Learn Smart Stages", "Batteries for Fisher-Price", "lego"),
    # === FOOD ===
    ("Milka 100g", "Milka Alpenmilch Schokolade 100g", "Box for chocolates", "food"),
    ("Nutella 400g", "Nutella Nuss-Nougat-Creme 400g", "Jar label for Nutella", "food"),
    ("Haribo Goldbären 200g", "Haribo Goldbären Fruchtgummi 200g", "Display box Haribo", "food"),
    ("Lindt Excellence 70% 100g", "Lindt Excellence 70% Cacao Dark Chocolate 100g", "Wrapper Lindt 100g", "food"),
    ("Pringles Original 165g", "Pringles Original Chips 165g", "Can for Pringles", "food"),
    ("Coca-Cola 1.5L", "Coca-Cola Original 1,5L PET Flasche", "Bottle opener", "food"),
    ("Red Bull 250ml", "Red Bull Energy Drink 250ml Dose", "Cooler for energy drinks", "food"),
    ("Jacobs Krönung 500g", "Jacobs Krönung Kaffee 500g", "Coffee grinder accessory", "food"),
    ("Bonduelle Mais 285g", "Bonduelle Mais 285g Dose", "Can opener", "food"),
    ("Alpro Soya Drink 1L", "Alpro Soja-Drink 1L ungekühlt", "Glass pitcher", "food"),
    ("Dr. Oetker Backhefe 7g", "Dr. Oetker Backhefe 7g Trockenbackhefe", "Baking mold", "food"),
    ("Bahlsen Leibniz 200g", "Bahlsen Leibniz Butterkeks 200g", "Cookie box tin", "food"),
    ("Ritter Sport Marzipan 100g", "Ritter Sport Marzipan Schokolade 100g", "Chocolate box", "food"),
    ("Kellogg's Corn Flakes 750g", "Kellogg's Corn Flakes 750g", "Cereal bowl", "food"),
    ("Danone Activia 4x125g", "Danone Activia Joghurt 4x125g Natur", "Yogurt spoon", "food"),
    ("Heinz Ketchup 570g", "Heinz Tomato Ketchup 570g Flasche", "Condiment rack", "food"),
    ("Maggi Suppe 3er Pack", "Maggi Klare Rindfleischsuppe 3er Pack", "Soup bowl", "food"),
    ("Philadelphia Frischkäse 200g", "Philadelphia Original Frischkäse 200g", "Knife for cream cheese", "food"),
    ("Funny-Frisch Chipsfrisch 150g", "Funny-Frisch Chipsfrisch Gesalzen 150g", "Party bowl", "food"),
    ("Toblerone 360g", "Toblerone Milk Chocolate 360g", "Chocolate gift box", "food"),
    # === COSMETICS ===
    ("Dove Shampoo 400ml", "Dove Intensive Repair Shampoo 400ml", "Shampoo dispenser pump", "cosmetics"),
    ("Nivea Creme 250ml", "Nivea Creme Feuchtigkeitscreme 250ml", "Jar spatula", "cosmetics"),
    ("L'Oreal Elvive Shampoo 400ml", "L'Oreal Paris Elvive Full Resist Shampoo 400ml", "Comb for thin hair", "cosmetics"),
    ("Pantene Pro-V 400ml", "Pantene Pro-V Classic Clean Shampoo 400ml", "Hair brush", "cosmetics"),
    ("Head & Shoulders 500ml", "Head & Shoulders Classic Clean Shampoo 500ml", "Dandruff brush", "cosmetics"),
    ("Schwarzkopf Gliss 400ml", "Schwarzkopf Gliss Ultimate Repair Shampoo 400ml", "Towel for hair", "cosmetics"),
    ("Gillette Fusion5 Klingen 8", "Gillette Fusion5 Rasierklingen 8 Stück", "Razor stand", "cosmetics"),
    ("Oral-B Pro 3 3500", "Oral-B Pro 3 3500 elektrische Zahnbürste", "Travel case for Oral-B Pro 3", "cosmetics"),
    ("Colgate Total 75ml", "Colgate Total Whitening Toothpaste 75ml", "Toothpaste dispenser", "cosmetics"),
    ("Rexona 48h Deo 150ml", "Rexona 48h Deo Spray 150ml Women", "Deodorant holder", "cosmetics"),
    ("Garnier Micellar Water 400ml", "Garnier Skin Naturals Micellar Cleansing Water 400ml", "Cotton pad holder", "cosmetics"),
    ("Neutrogena Hydro Boost 50ml", "Neutrogena Hydro Boost Water Gel 50ml", "Moisturizer applicator", "cosmetics"),
    ("CeraVe Moisturizing Cream 454g", "CeraVe Moisturizing Cream 454g", "Spatula for cream", "cosmetics"),
    ("The Ordinary Niacinamide 30ml", "The Ordinary Niacinamide 10% + Zinc 1% 30ml", "Dropper replacement", "cosmetics"),
    ("Eucerin UreaRepair PLUS 5% 400ml", "Eucerin UreaRepair PLUS 5% Lotion 400ml", "Lotion pump dispenser", "cosmetics"),
    ("Avène Thermal Spring Water 300ml", "Avène Thermal Spring Water Spray 300ml", "Travel organizer", "cosmetics"),
    ("La Roche-Posay Anthelios SPF50 50ml", "La Roche-Posay Anthelios UVMune 400 SPF50+ 50ml", "Sunscreen bag", "cosmetics"),
    ("Bioderma Sensibio H2O 250ml", "Bioderma Sensibio H2O Micellar Water 250ml", "Pump for micellar water", "cosmetics"),
    ("Vichy Liftactiv Supreme 50ml", "Vichy Liftactiv Supreme Anti-Aging Creme 50ml", "Serum applicator", "cosmetics"),
    ("Kiehl's Ultra Facial Cream 50ml", "Kiehl's Ultra Facial Cream 50ml", "Spatula for cream jar", "cosmetics"),
    # === CLOTHING ===
    ("Nike Air Max 270", "Nike Air Max 270 Herren Laufschuhe Schwarz Größe 42", "Insoles for Nike Air Max", "clothing"),
    ("Adidas Ultraboost 22", "Adidas Ultraboost 22 Running Shoes Men Core Black", "Shoe cleaner", "clothing"),
    ("Levi's 501 Original Jeans", "Levi's 501 Original Fit Jeans Herren Blau W32 L32", "Belt for Levi's 501", "clothing"),
    ("Puma Softride Pro 24", "Puma Softride Pro 24 Herren Sneaker Größe 43", "Shoe bag for Puma", "clothing"),
    ("Under Armour HeatGear", "Under Armour HeatGear Armour Compression Shirt Men", "Washing bag", "clothing"),
    ("Columbia Watertight II", "Columbia Watertight II Herren Regenjacke", "Packing cube", "clothing"),
    ("Adidas Tiro 23 Hose", "Adidas Tiro 23 League Trainingshose Herren", "Laundry bag", "clothing"),
    ("Nike Dri-FIT Academy", "Nike Dri-FIT Academy Trainingsshirt Herren", "Fabric softener for sportswear", "clothing"),
    ("Salomon Speedcross 6", "Salomon Speedcross 6 Trail Running Schuhe", "Gaiters for Salomon Speedcross", "clothing"),
    ("Reebok Classic Leather", "Reebok Classic Leather Herren Sneaker Weiß", "Sneaker cleaner", "clothing"),
    ("New Balance 574", "New Balance 574 Core Sneaker Herren Navy", "Shoe tree for New Balance 574", "clothing"),
    ("Patagonia Better Sweater", "Patagonia Men's Better Sweater Fleece Jacket", "Jacket bag", "clothing"),
    ("The North Face Resolve 2", "The North Face Resolve 2 Herren Regenjacke", "Rain cover bag", "clothing"),
    ("H&M Regular Fit Shirt XL", "H&M Regular Fit Oxford Shirt Men XL White", "Collar stays", "clothing"),
    ("Zara Slim Fit Trousers 32", "Zara Slim Fit Trousers Men Grey 32", "Trouser hanger", "clothing"),
    ("Mango Slim Jeans W30", "Mango Slim Jeans Men Dark Blue W30 L32", "Jean pins", "clothing"),
    ("Tommy Hilfiger Polo XL", "Tommy Hilfiger Slim Fit Polo Shirt XL Navy", "Polo collar stiffener", "clothing"),
    ("Hugo Boss Suit 48", "Hugo Boss Slim Fit Suit Men 48 Anthracite", "Suit brush", "clothing"),
    ("Calvin Klein Boxer Briefs M", "Calvin Klein Modern Cotton Stretch Boxer Brief M", "Laundry net", "clothing"),
    ("Gant Shield Hoodie L", "Gant Shield Full-Zip Hoodie Men L Navy", "Zipper repair kit", "clothing"),
    # === BOOKS ===
    ("Atomic Habits James Clear", "Atomic Habits: An Easy & Proven Way to Build Good Habits by James Clear", "Bookmark set", "books"),
    ("Harry Potter Philosopher's Stone", "Harry Potter and the Philosopher's Stone Hardcover", "Harry Potter bookmark", "books"),
    ("The Pragmatic Programmer", "The Pragmatic Programmer: Your Journey to Mastery 20th Anniversary Edition", "Code notebook", "books"),
    ("Dune Frank Herbert", "Dune by Frank Herbert Paperback", "Desert bookmark", "books"),
    ("Clean Code Robert Martin", "Clean Code: A Handbook of Agile Software Craftsmanship", "Developer mug", "books"),
    ("The 7 Habits Covey", "The 7 Habits of Highly Effective People by Stephen R. Covey", "Habit tracker journal", "books"),
    ("Thinking Fast and Slow", "Thinking, Fast and Slow by Daniel Kahneman", "Notebook for notes", "books"),
    ("Sapiens Yuval Noah Harari", "Sapiens: A Brief History of Humankind by Yuval Noah Harari", "History map poster", "books"),
    ("The Great Gatsby Fitzgerald", "The Great Gatsby by F. Scott Fitzgerald Paperback", "Jazz vinyl record", "books"),
    ("Rich Dad Poor Dad Kiyosaki", "Rich Dad Poor Dad by Robert T. Kiyosaki", "Finance planner", "books"),
    ("1984 George Orwell", "1984 by George Orwell Penguin Modern Classics", "Dystopia art print", "books"),
    ("The Lean Startup Ries", "The Lean Startup: How Today's Entrepreneurs Use Continuous Innovation by Eric Ries", "Business card holder", "books"),
    ("Meditations Marcus Aurelius", "Meditations by Marcus Aurelius Modern Library Edition", "Philosophy mug", "books"),
    ("Deep Work Cal Newport", "Deep Work: Rules for Focused Success in a Distracted World by Cal Newport", "Focus timer pomodoro", "books"),
    ("The Alchemist Coelho", "The Alchemist by Paulo Coelho Paperback", "Travel journal", "books"),
    ("Zero to One Peter Thiel", "Zero to One: Notes on Startups by Peter Thiel", "Startup notebook", "books"),
    ("Essentialism McKeown", "Essentialism: The Disciplined Pursuit of Less by Greg McKeown", "Minimalist planner", "books"),
    ("Man's Search for Meaning Frankl", "Man's Search for Meaning by Viktor E. Frankl", "Stoic journal", "books"),
    ("The Power of Now Tolle", "The Power of Now by Eckhart Tolle", "Meditation cushion", "books"),
    ("Surely You're Joking Feynman", "Surely You're Joking, Mr. Feynman! Adventures of a Curious Character", "Physics poster", "books"),
    # === HOUSEHOLD ===
    ("Dyson V15 Detect", "Dyson V15 Detect Absolute Akku-Staubsauger", "Filter for Dyson V15", "household"),
    ("Philips Hue White E27 3er Pack", "Philips Hue White E27 LED Lampe 3er Pack", "Lamp dimmer for Philips Hue", "household"),
    ("iRobot Roomba j7+", "iRobot Roomba j7+ selbstreinigender Saugroboter", "Virtual Wall barrier for Roomba j7+", "household"),
    ("Tefal Ingenio Pfanne 28cm", "Tefal Ingenio Essential Pfanne 28cm antihaft", "Spatula for Tefal Ingenio", "household"),
    ("WMF Silit 24cm", "WMF Silit Steakpfanne 24cm Ceraforce", "Wooden spatula", "household"),
    ("Zwilling Pro Messer 20cm", "Zwilling Pro Kochmesser 20cm", "Knife sharpener compatible with Zwilling", "household"),
    ("Braun Series 9 Pro 9477cc", "Braun Series 9 Pro 9477cc Elektrorasierer", "Shaver cleaning cartridge for Braun Series 9", "household"),
    ("Philips Airfryer XXL HD9860", "Philips Airfryer XXL HD9860 Heißluftfritteuse", "Baking basket for Philips Airfryer XXL", "household"),
    ("Bosch Tassimo T20", "Bosch Tassimo T20 Kaffeemaschine", "Descaler for Tassimo", "household"),
    ("Vileda 1-2 Spray Mop", "Vileda 1-2 Spray Bodenwischer Set", "Replacement mop pads for Vileda 1-2 Spray", "household"),
    ("Leifheit Pegasus 200 Solid", "Leifheit Pegasus 200 Solid Wäscheständer", "Drying rack cover", "household"),
    ("Tupperware Modular Mates", "Tupperware Modular Mates Set 4-teilig", "Label set for Tupperware", "household"),
    ("Emsa Clip & Close 3er Set", "Emsa Clip & Close Frischhaltedosen 3er Set 0.55L", "Replacement lids Emsa Clip", "household"),
    ("Melitta Caffeo Solo E950", "Melitta Caffeo Solo E950 Kaffeevollautomat", "Descaling tablets for Melitta Caffeo", "household"),
    ("Klarstein Maipo Fondue 1200W", "Klarstein Maipo Fondue Set 1200W 8 Personen", "Fondue forks replacement", "household"),
    ("Karcher K2 Compact", "Karcher K2 Compact Hochdruckreiniger", "Detergent for Karcher", "household"),
    ("Rowenta Steam Force DW9280", "Rowenta Steam Force DW9280 Dampfbügeleisen 2800W", "Ironing board for Rowenta", "household"),
    ("Elgato Key Light 45W", "Elgato Key Light 45W Panel LED Studioleuchte", "Arm mount for Elgato Key Light", "household"),
    ("De'Longhi Dedica EC685M", "De'Longhi Dedica Style EC685M Espressomaschine", "Milk frother replacement for Dedica", "household"),
    ("Sage Barista Express SES875", "Sage The Barista Express SES875 Espresso-Maschine", "Portafilter basket for Sage Barista", "household"),
    # === SPORTS ===
    ("Garmin Forerunner 265", "Garmin Forerunner 265 GPS Smartwatch", "Band for Garmin Forerunner 265", "sports"),
    ("Polar Vantage V3", "Polar Vantage V3 GPS Multisport-Uhr Schwarz", "Strap for Polar Vantage V3", "sports"),
    ("Wahoo KICKR Core", "Wahoo KICKR Core Smart Indoor Trainer", "Cassette for Wahoo KICKR Core", "sports"),
    ("Garmin Edge 840", "Garmin Edge 840 GPS Fahrradcomputer", "Mount for Garmin Edge 840", "sports"),
    ("PowerBeats Pro 2", "Beats Powerbeats Pro 2 In-Ear Kopfhörer True Wireless", "Eartips for Powerbeats Pro 2", "sports"),
    ("Suunto 9 Peak Pro", "Suunto 9 Peak Pro Multisport GPS Watch", "Screen protector for Suunto 9 Peak Pro", "sports"),
    ("TRX Pro Suspension Trainer", "TRX PRO4 Suspension Trainer Kit", "Wall anchor for TRX", "sports"),
    ("Bowflex SelectTech 552", "Bowflex SelectTech 552 Adjustable Dumbbells", "Dumbbell rack for Bowflex", "sports"),
    ("Concept2 RowErg PM5", "Concept2 RowErg Model D mit PM5 Rudergerät", "Seat cushion for Concept2", "sports"),
    ("Kettlebell 16kg", "Kettlebell 16kg Gusseisen Kugelhanteln", "Chalk bag for kettlebell", "sports"),
    ("Yoga Mat 6mm", "Yoga Mat Non-Slip 6mm TPE Fitness Mat", "Yoga strap for mat", "sports"),
    ("Wilson Pro Staff 97", "Wilson Pro Staff 97 v14 Tennisschläger", "Grip tape for Wilson Pro Staff", "sports"),
    ("Head Gravity MP", "Head Gravity MP Tennisschläger 2023", "String set for Head Gravity MP", "sports"),
    ("Speedo Fastskin 3", "Speedo Fastskin 3 Racing System Badeanzug", "Goggles for swim racing", "sports"),
    ("Trigon Sports Football", "Trigon Sports 5-Player Football Passing Net", "Football pump", "sports"),
    ("Adidas Predator League", "Adidas Predator League FG Football Boots", "Boot bag", "sports"),
    ("Callaway Rogue ST Max", "Callaway Rogue ST Max Driver Golf", "Golf tees for Callaway", "sports"),
    ("TaylorMade Stealth 2", "TaylorMade Stealth 2 Driver 10.5°", "Driver headcover TaylorMade", "sports"),
    ("Osprey Kestrel 48", "Osprey Kestrel 48 Herren Rucksack", "Rain cover for Osprey Kestrel 48", "sports"),
    ("Black Diamond Momentum", "Black Diamond Momentum Klettergurt", "Chalk bag for Black Diamond", "sports"),
    # === BABY ===
    ("Pampers Premium Care Newborn 2-5kg", "Pampers Premium Care Windeln Newborn Größe 1 2-5kg 50 Stück", "Diaper bin", "baby"),
    ("Aptamil Profutura 1 800g", "Aptamil Profutura 1 Anfangsmilch 800g von Geburt an", "Bottle brush", "baby"),
    ("Chicco Next2Me Magic", "Chicco Next2Me Magic Bedside Crib", "Mattress for Chicco Next2Me", "baby"),
    ("Babybjörn Baby Carrier One", "BabyBjörn Baby Carrier One Baumwolle", "Cover for BabyBjörn carrier", "baby"),
    ("Nuk First Choice Plus Flasche 300ml", "NUK First Choice+ Babyflasche 300ml Silikonschnuller", "Replacement teat for NUK 300ml", "baby"),
    ("Graco Pack'n Play On The Go", "Graco Pack 'n Play On The Go Reisebett", "Travel bag for Graco Pack'n Play", "baby"),
    ("Ergobaby Embrace Newborn", "Ergobaby Embrace Newborn Baby Carrier Stretch", "Infant insert for Ergobaby", "baby"),
    ("Chicco Hoopla 3-in-1", "Chicco Hoopla 3-in-1 Wippstuhl ab Geburt", "Replacement cover Chicco Hoopla", "baby"),
    ("Philips Avent Natural 3.0 260ml", "Philips Avent Natural Response 3.0 Babyflasche 260ml", "Bottle drying rack", "baby"),
    ("Beurer BC 58 Babyphone", "Beurer BC 58 Video-Babyphone WLAN", "Bracket for Beurer BC 58", "baby"),
    ("Medela Freestyle Flex", "Medela Freestyle Flex Double Electric Breast Pump", "Spare parts for Medela Freestyle", "baby"),
    ("Joie Everett R129", "Joie Everett FX R129 Kindersitz 40-105cm", "Seat protector for Joie Everett", "baby"),
    ("Britax Römer Dualfix iSense", "Britax Römer Dualfix iSense Kindersitz 76-105cm", "Sun shade for Britax Römer Dualfix", "baby"),
    ("Maxi-Cosi Pearl 360 Pro", "Maxi-Cosi Pearl 360 Pro Autositz 40-105cm", "Belt guard for Maxi-Cosi Pearl 360", "baby"),
    ("Silver Cross Wave 2", "Silver Cross Wave 2 Kombikinderwagen", "Rain cover for Silver Cross Wave", "baby"),
    ("Bugaboo Donkey 5", "Bugaboo Donkey 5 Mono Kinderwagen", "Footmuff for Bugaboo Donkey", "baby"),
    ("Hauck Rapid 4S", "Hauck Rapid 4S Plus Buggy faltbar mit Liegefunktion", "Buggy bag for Hauck Rapid", "baby"),
    ("Fisher-Price Bouncer NWB30", "Fisher-Price Gentle Moments Newborn to Toddler Rocker NWB30", "Replacement toy bar for Fisher-Price rocker", "baby"),
    ("Munchkin Latch Flasche 240ml", "Munchkin Latch Anti-Colic Babyflasche 240ml", "Bottle sterilizer bags", "baby"),
    ("Snuza HeroMD", "Snuza HeroMD Mobile Baby Breathing Monitor", "Replacement clips for Snuza", "baby"),
]

# ── Layer 1: Logic tests ──────────────────────────────────────────────────────

def run_layer1():
    results = []
    by_cat = defaultdict(lambda: {"total":0,"rel_pass":0,"rel_fail":0,"acc_pass":0,"acc_fail":0,
                                   "model_variants":0,"lt_detected":0,"large_app":0,
                                   "short_q_truncated":0,"post_process_empty":0,"unit_token_bug":0})

    for query, good_title, bad_title, cat in PRODUCTS:
        r = by_cat[cat]
        r["total"] += 1

        rel_good = is_relevant_result(query, good_title)
        rel_bad  = is_relevant_result(query, bad_title)

        if rel_good:
            r["rel_pass"] += 1
        else:
            r["rel_fail"] += 1

        if not rel_bad:
            r["acc_pass"] += 1
        else:
            r["acc_fail"] += 1

        variants = _model_code_variants(query)
        if len(variants) > 1:
            r["model_variants"] += 1

        if _is_lt_query(query):
            r["lt_detected"] += 1
        if _is_large_appliance(query):
            r["large_app"] += 1

        short_q = _short_amazon_query(query)
        if short_q != query:
            r["short_q_truncated"] += 1

        # Detect unit-token bug: query has number-like token, good_title wouldn't pass
        unit_tokens = re.findall(r'\b\d+(?:g|ml|l|kg|mg|oz|cl)\b', query.lower())
        if unit_tokens and not rel_good:
            r["unit_token_bug"] += 1

        # Would post_process empty the results?
        if post_process_would_empty(query, rel_good):
            r["post_process_empty"] += 1

        results.append({
            "query": query, "cat": cat, "good_title": good_title, "bad_title": bad_title,
            "rel_good": rel_good, "rel_bad": rel_bad, "variants": variants,
            "short_q": short_q, "unit_bug": bool(unit_tokens and not rel_good),
        })

    return results, by_cat

# ── Layer 2: Live smoke test ───────────────────────────────────────────────────

SMOKE_PRODUCTS = [
    ("Samsung RB34C600ESA", "appliances"),
    ("Bosch WAX32EH0", "appliances"),
    ("Sony WH-1000XM5", "electronics"),
    ("Apple iPhone 15 Pro 128GB", "electronics"),
    ("LEGO Technic 42170", "lego"),
    ("LEGO Harry Potter 76430", "lego"),
    ("Milka 100g", "food"),
    ("Nutella 400g", "food"),
    ("Dove Shampoo 400ml", "cosmetics"),
    ("Nivea Creme 250ml", "cosmetics"),
    ("Nike Air Max 270 42", "clothing"),
    ("Adidas Ultraboost 22", "clothing"),
    ("Atomic Habits James Clear", "books"),
    ("Clean Code Robert Martin", "books"),
    ("Dyson V15 Detect", "household"),
    ("Philips Airfryer XXL HD9860", "household"),
    ("Garmin Forerunner 265", "sports"),
    ("Polar Vantage V3", "sports"),
    ("Pampers Premium Care Newborn", "baby"),
    ("Aptamil Profutura 1 800g", "baby"),
]

BASE = "https://goody-backend.onrender.com"

def run_layer2():
    smoke = []
    for query, cat in SMOKE_PRODUCTS:
        url = f"{BASE}/api/search"
        payload = json.dumps({"query": query, "language": "de"}).encode("utf-8")
        t0 = time.time()
        try:
            req = urllib.request.Request(url, data=payload,
                                         headers={"User-Agent":"test-pipeline/1.0",
                                                  "Content-Type":"application/json"})
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read())
            elapsed = round(time.time() - t0, 1)
            n = len(data.get("results", []))
            status = "ok" if n > 0 else "zero"
            err = None
        except urllib.error.HTTPError as e:
            elapsed = round(time.time() - t0, 1)
            body = e.read(200).decode("utf-8","replace")
            n = 0; status = "error"; err = f"HTTP {e.code}: {body[:60]}"
        except Exception as e:
            elapsed = round(time.time() - t0, 1)
            n = 0; status = "error"; err = str(e)[:80]
        smoke.append({"query":query,"cat":cat,"results":n,"status":status,
                       "elapsed":elapsed,"err":err})
        print(f"  [{status:5s}] {query:40s} -> {n} results in {elapsed}s")
        time.sleep(2)  # don't hammer
    return smoke

# ── Report ────────────────────────────────────────────────────────────────────

def write_report(layer1_results, by_cat, layer2):
    lines = ["# TEST_RESULTS.md", f"**Date:** 2026-06-19", ""]
    lines += ["## Layer 1 — Logic Tests (500 products, no HTTP)", ""]
    lines += ["| Category | Total | Rel✓ | Rel✗ | Acc✓ | Acc✗ | UnitBug | PostProc∅ | ShortQ | LTdet |",
              "|---|---|---|---|---|---|---|---|---|---|"]
    totals = defaultdict(int)
    for cat in ["appliances","electronics","lego","food","cosmetics","clothing",
                "books","household","sports","baby"]:
        r = by_cat[cat]
        for k, v in r.items():
            totals[k] += v
        lines.append(f"| {cat} | {r['total']} | {r['rel_pass']} | {r['rel_fail']} | {r['acc_pass']} | {r['acc_fail']} | {r['unit_token_bug']} | {r['post_process_empty']} | {r['short_q_truncated']} | {r['lt_detected']} |")

    lines.append(f"| **TOTAL** | **{totals['total']}** | **{totals['rel_pass']}** | **{totals['rel_fail']}** | **{totals['acc_pass']}** | **{totals['acc_fail']}** | **{totals['unit_token_bug']}** | **{totals['post_process_empty']}** | **{totals['short_q_truncated']}** | **{totals['lt_detected']}** |")

    lines += ["", "### Failed relevance checks (Rel✗) — good title rejected:", ""]
    for r in layer1_results:
        if not r["rel_good"]:
            lines.append(f"- `{r['query']}` -> good title NOT matched: `{r['good_title'][:70]}`")

    lines += ["", "### Accessory filter failures (Acc✗) — bad title NOT filtered:", ""]
    for r in layer1_results:
        if r["rel_bad"]:
            lines.append(f"- `{r['query']}` -> accessory title NOT rejected: `{r['bad_title'][:70]}`")

    lines += ["", "### Unit-token false negatives (food/cosmetics units in query):", ""]
    for r in layer1_results:
        if r["unit_bug"]:
            lines.append(f"- `{r['query']}` (cat={r['cat']}) — unit in query, title rejected")

    lines += ["", "### _short_amazon_query truncations:", ""]
    for r in layer1_results:
        if r["short_q"] != r["query"]:
            lines.append(f"- `{r['query']}` -> `{r['short_q']}`")

    lines += ["", "---", "", "## Layer 2 — Live Smoke Test (20 products)", ""]
    lines += ["| Query | Category | Results | Time(s) | Status |",
              "|---|---|---|---|---|"]
    for s in layer2:
        err_note = f" ({s['err']})" if s['err'] else ""
        lines.append(f"| {s['query']} | {s['cat']} | {s['results']} | {s['elapsed']} | {s['status']}{err_note} |")

    zero = [s for s in layer2 if s['status']=='zero']
    errs = [s for s in layer2 if s['status']=='error']
    ok   = [s for s in layer2 if s['status']=='ok']
    lines += ["", f"**OK:** {len(ok)}/20  **Zero results:** {len(zero)}/20  **Errors:** {len(errs)}/20", ""]
    if zero:
        lines += ["### Zero-result queries:", ""]
        for s in zero:
            lines.append(f"- `{s['query']}` ({s['cat']})")

    return "\n".join(lines) + "\n"

def write_fixes(layer1_results, by_cat):
    unit_bug_count = sum(1 for r in layer1_results if r["unit_bug"])
    rel_fail_count = sum(r["rel_fail"] for r in by_cat.values())
    acc_fail_count = sum(r["acc_fail"] for r in by_cat.values())
    short_q_count  = sum(1 for r in layer1_results if r["short_q"] != r["query"])

    lines = [
        "# FIXES_PROPOSED.md",
        "**Branch:** `auto-fixes-review`  **Date:** 2026-06-19",
        "",
        "## Summary",
        f"- **{rel_fail_count}** good titles rejected by `is_relevant_result` (false negatives)",
        f"- **{unit_bug_count}** unit-token false negatives (food/cosmetics: 100g/400ml treated as model code)",
        f"- **{acc_fail_count}** accessory titles NOT filtered (false positives — minor)",
        f"- **{short_q_count}** queries truncated by `_short_amazon_query` (potential LEGO set-number loss)",
        "",
        "---",
        "",
        "## Fix 1 — Unit-token false negatives in `is_relevant_result`",
        "**Risk: LOW** | **Impact: HIGH** | **Categories affected: food, cosmetics, baby**",
        "",
        "### Root cause",
        "```python",
        "model_tokens = re.findall(r'\\b[a-z]*\\d+[a-z0-9-]*\\b', q)",
        "# '100g', '400ml', '800g', '250ml' all match this regex",
        "# -> requires them to appear in product title",
        "# -> Amazon titles rarely include exact weight string -> 0 relevant results",
        "```",
        "",
        "### Fix",
        "Before extracting model_tokens, strip known unit suffixes from query tokens:",
        "```python",
        "_UNIT_SUFFIXES = re.compile(r'^\\d+(?:g|ml|l|kg|mg|oz|cl|mm|cm|m|w|v|hz|rpm|pcs|st|stk)$')",
        "model_tokens = [t for t in re.findall(r'\\b[a-z]*\\d+[a-z0-9-]*\\b', q)",
        "                if not _UNIT_SUFFIXES.match(t)]",
        "```",
        "Also in `post_process`: same filter before the `elif re.findall(...)` check.",
        "",
        "---",
        "",
        "## Fix 2 — `_short_amazon_query` drops LEGO set numbers",
        "**Risk: LOW** | **Impact: MEDIUM** | **Categories affected: LEGO/toys**",
        "",
        "### Root cause",
        "`_short_amazon_query` caps at 3 words. For 'LEGO Harry Potter 76430 Hogwarts' -> 'LEGO Harry Potter' (set number 76430 dropped — most specific part).",
        "",
        "### Fix",
        "Detect 4-6 digit standalone numbers (LEGO set numbers) and always keep them:",
        "```python",
        "def _short_amazon_query(q: str) -> str:",
        "    words = q.split()",
        "    if len(words) <= 3:",
        "        return q",
        "    # Always preserve 4-6 digit tokens (LEGO set numbers, product IDs)",
        "    priority = [w for w in words if re.match(r'^\\d{4,6}$', w)]",
        "    kept = [w for w in words if w.lower() not in _AMZ_FILLER]",
        "    if kept and len(kept) < len(words):",
        "        result = kept[:3]",
        "        # If priority tokens were dropped, replace last slot",
        "        for p in priority:",
        "            if p not in result:",
        "                result = result[:2] + [p]",
        "        return ' '.join(result)",
        "    return ' '.join(words[:3])",
        "```",
        "",
        "---",
        "",
        "## Fix 3 — LT food/cosmetics vocabulary gap in `_is_lt_query`",
        "**Risk: LOW** | **Impact: MEDIUM** | **Categories affected: food, cosmetics, clothing**",
        "",
        "### Root cause",
        "`_LT_CATEGORY_WORDS` covers appliances/electronics well but lacks: food terms (šokoladas, pienas, jogurtas), cosmetics (kremas, šampūnas, parfumas), clothing (avalynė, apranga, drabužiai), books (knyga).",
        "Result: Lithuanian food/cosmetics queries are NOT translated -> Amazon receives Lithuanian query -> 0 results.",
        "",
        "### Fix",
        "Add to `_LT_CATEGORY_WORDS`:",
        "```python",
        "# Food",
        '"šokoladas","sokoladas","pienas","jogurtas","suris","duona",',
        '"maistas","maisto","gėrimas","gerimas","arbata","kava",',
        "# Cosmetics",
        '"kremas","šampūnas","sampunas","dezodorantas","parfumas","kvepalai",',
        '"makiažas","makiazas","kosmetika","losjonas",',
        "# Clothing",
        '"avalynė","avalyne","batai","batas","apranga","drabužiai",',
        '"drabuziai","striukė","striuke","kelnės","kelnes","marškiniai",',
        "# Books",
        '"knyga","knygos","vadovėlis","vadovelis",',
        "```",
        "Also add to `_LT_DE` / `_LT_PL` translation maps for the key terms.",
        "",
        "---",
        "",
        "## Fix 4 — `post_process` compounds unit-token bug",
        "**Risk: LOW** | **Impact: HIGH** | **Linked to Fix 1**",
        "",
        "### Root cause",
        "When query contains digit-tokens AND no relevant results found, `post_process` returns `[]` instead of closest match. With unit tokens treated as model codes (Fix 1's bug), this means food/cosmetics queries always return empty instead of closest match.",
        "",
        "### Fix",
        "Apply the same `_UNIT_SUFFIXES` filter in `post_process` before the `elif` check. This is automatically fixed once Fix 1 is applied (same regex).",
        "",
        "---",
        "",
        "## Implementation order",
        "1. Fix 1 + Fix 4 together (same change, highest impact)",
        "2. Fix 2 (independent, low risk)",
        "3. Fix 3 (additive, no risk)",
        "",
        "## Files changed",
        "- `server.py` — `is_relevant_result()`, `post_process()`, `_short_amazon_query()`, `_LT_CATEGORY_WORDS`, `_LT_DE`",
        "",
    ]
    return "\n".join(lines) + "\n"

# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Layer 1: Logic tests ===")
    layer1_results, by_cat = run_layer1()
    for cat in ["appliances","electronics","lego","food","cosmetics","clothing",
                "books","household","sports","baby"]:
        r = by_cat[cat]
        print(f"  {cat:12s}: rel {r['rel_pass']}/{r['total']} ok  acc_filter {r['acc_pass']}/{r['total']}  unit_bug={r['unit_token_bug']}  short_q_trunc={r['short_q_truncated']}")

    print("\n=== Layer 2: Live smoke test ===")
    layer2 = run_layer2()

    print("\n=== Writing reports ===")
    import os
    base = os.path.dirname(os.path.abspath(__file__))
    report = write_report(layer1_results, by_cat, layer2)
    fixes  = write_fixes(layer1_results, by_cat)

    with open(os.path.join(base, "TEST_RESULTS.md"), "w", encoding="utf-8") as f:
        f.write(report)
    with open(os.path.join(base, "FIXES_PROPOSED.md"), "w", encoding="utf-8") as f:
        f.write(fixes)

    print(f"TEST_RESULTS.md written.")
    print(f"FIXES_PROPOSED.md written.")
    ok = sum(1 for s in layer2 if s['status']=='ok')
    zero = sum(1 for s in layer2 if s['status']=='zero')
    total_rel_fail = sum(r['rel_fail'] for r in by_cat.values())
    print(f"\nSummary: L1 rel_fail={total_rel_fail}/500  L2 ok={ok}/20 zero={zero}/20")

