import sys, io, os, base64

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf-8-sig'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

os.environ.setdefault('SUPABASE_URL', '')
os.environ.setdefault('SUPABASE_KEY', '')
import server
from server import is_relevant_result, get_category_icon, parse_price, classify_product_cheap, suggest_simpler_query

app = server.app
app.config['TESTING'] = True
c = app.test_client()

fails = 0
total = 0

def chk(label, got, exp):
    global fails, total
    total += 1
    ok = got == exp
    if not ok:
        fails += 1
    tag = 'OK  ' if ok else 'FAIL'
    mark = '' if ok else f'  <- got {got!r}, exp {exp!r}'
    print(f'  [{tag}] {label}{mark}')

def chk_bool(label, cond):
    global fails, total
    total += 1
    if not cond:
        fails += 1
    tag = 'OK  ' if cond else 'FAIL'
    print(f'  [{tag}] {label}')

def rel(q, t):
    return is_relevant_result(q, t)

# ── 1. PHONES ─────────────────────────────────────────────────
print()
print('=== 1. TELEFONAI ===')
chk('iPhone 15 Pro matches',              rel('iPhone 15 Pro', 'Apple iPhone 15 Pro 128GB Black'), True)
chk('iPhone 15 Pro 256GB blocks 128GB',  rel('iPhone 15 Pro 256GB', 'Apple iPhone 15 Pro 128GB'), False)
chk('iPhone 15 Pro blocks iPhone 15',    rel('iPhone 15 Pro', 'Apple iPhone 15 128GB'), False)
chk('iPhone 15 blocks leather case',     rel('iPhone 15', 'iPhone 15 leather case'), False)
chk('Pixel 9 Pro matches',               rel('Google Pixel 9 Pro', 'Google Pixel 9 Pro 128GB Obsidian'), True)
chk('Pixel 9 Pro blocks Pixel 8 Pro',   rel('Google Pixel 9 Pro', 'Google Pixel 8 Pro 256GB'), False)
chk('OnePlus 12 256GB matches',          rel('OnePlus 12 256GB', 'OnePlus 12 256GB Silky Black'), True)
chk('OnePlus 12 blocks 65W charger',    rel('OnePlus 12', 'OnePlus 12 65W charger'), False)
chk('Xiaomi 14 Pro matches',             rel('Xiaomi 14 Pro', 'Xiaomi 14 Pro 512GB Black'), True)
chk('Xiaomi 14 blocks bumper case',     rel('Xiaomi 14', 'Xiaomi 14 case bumper'), False)

# ── 2. LAPTOPS ────────────────────────────────────────────────
print()
print('=== 2. LAPTOPAI ===')
chk('Dell XPS 15 matches',               rel('Dell XPS 15', 'Dell XPS 15 9530 Intel i7 16GB 512GB'), True)
chk('Dell XPS 15 blocks sleeve',         rel('Dell XPS 15', 'Dell XPS 15 neoprene sleeve'), False)
chk('Lenovo ThinkPad X1 matches',        rel('Lenovo ThinkPad X1 Carbon', 'Lenovo ThinkPad X1 Carbon Gen 12 i7'), True)
chk('Lenovo ThinkPad blocks dock',       rel('Lenovo ThinkPad', 'Lenovo ThinkPad USB-C dock'), False)
chk('ASUS ROG Zephyrus G14 matches',     rel('ASUS ROG Zephyrus G14', 'ASUS ROG Zephyrus G14 Ryzen 9 RTX 4060'), True)
chk('MacBook Air M2 matches',            rel('MacBook Air M2', 'Apple MacBook Air 13 M2 8GB 256GB Midnight'), True)
chk('MacBook Air M2 blocks M1',         rel('MacBook Air M2', 'Apple MacBook Air 13 M1 8GB 256GB'), False)
chk('MacBook Air M2 blocks USB hub',    rel('MacBook Air M2', 'USB-C Hub for MacBook Air M2 7-in-1'), False)

# ── 3. AUDIO ─────────────────────────────────────────────────
print()
print('=== 3. AUDIO ===')
chk('AirPods Pro 2 matches',             rel('AirPods Pro 2', 'Apple AirPods Pro 2nd Generation MagSafe'), True)
chk('AirPods Pro 2 blocks silicone case', rel('AirPods Pro 2', 'AirPods Pro 2 silicone case'), False)
chk('Bose QC45 matches',                 rel('Bose QuietComfort 45', 'Bose QuietComfort 45 Wireless Headphones Black'), True)
chk('Bose QC45 blocks replacement pads', rel('Bose QuietComfort 45', 'Bose QuietComfort 45 replacement earpads'), False)
chk('JBL Charge 5 matches',              rel('JBL Charge 5', 'JBL Charge 5 Portable Bluetooth Speaker Blue'), True)
chk('JBL Charge 5 blocks cable',        rel('JBL Charge 5', 'JBL Charge 5 USB-C charging cable'), False)
chk('Jabra Elite 85t matches',           rel('Jabra Elite 85t', 'Jabra Elite 85t True Wireless Earbuds Titanium'), True)
chk('Sony WH-1000XM4 blocks XM5 query', rel('Sony WH-1000XM5', 'Sony WH-1000XM4'), False)

# ── 4. TV / MONITOR ───────────────────────────────────────────
print()
print('=== 4. TV / MONITORIAI ===')
chk('LG OLED C3 55 matches',             rel('LG OLED C3 55', 'LG OLED55C31LA 55 inch 4K Smart TV'), True)
chk('LG OLED C3 55 blocks wall mount',  rel('LG OLED C3 55', 'TV wall mount 55 inch LG'), False)
chk('Samsung QLED 65 matches',           rel('Samsung QLED 65', 'Samsung QE65Q80B QLED 65 inch 4K UHD'), True)
chk('Dell UltraSharp 27 matches',        rel('Dell UltraSharp 27', 'Dell UltraSharp U2722D 27 inch 4K Monitor'), True)
chk('Monitor blocks arm stand',          rel('Dell UltraSharp 27', 'Monitor arm stand Dell 27 inch'), False)
chk('Hisense 55 matches',                rel('Hisense 55 TV', 'Hisense 55A7NQ 55 inch QLED 4K'), True)

# ── 5. BUITINĖ TECHNIKA ───────────────────────────────────────
print()
print('=== 5. BUITINĖ TECHNIKA ===')
chk('Bosch virdulys matches EN',         rel('Bosch virdulys', 'Bosch TWK3A011 Compact Kettle 1.7L'), True)
chk('Tefal keptuve matches EN pan',      rel('Tefal keptuve', 'Tefal Ingenio Essential Frying Pan 28cm'), True)
chk('Tefal keptuve blocks lid',          rel('Tefal keptuve', 'Tefal pan lid 28cm replacement'), False)
chk('Philips lygintuvas matches',        rel('Philips lygintuvas', 'Philips DST5040 Steam Iron 2400W'), True)
chk('Karcher K5 matches',                rel('Karcher K5', 'Karcher K5 Premium Pressure Washer 145 bar'), True)
chk('DeLonghi kavos matches',            rel('DeLonghi kavos aparatas', 'De Longhi Magnifica Start ECAM220'), True)
chk('Rowenta lygintuvas matches',        rel('Rowenta lygintuvas', 'Rowenta DW9240 Focus Excel Iron 2800W'), True)
chk('Electrolux siurblys matches',       rel('Electrolux dulkių siurblys', 'Electrolux EP71AB12UG PureQ9 Vacuum'), True)

# ── 6. GAMING ────────────────────────────────────────────────
print()
print('=== 6. GAMING ===')
chk('PS5 Disc Edition matches',          rel('PlayStation 5', 'Sony PlayStation 5 Disc Edition Console'), True)
chk('PS5 blocks DualSense controller',  rel('PlayStation 5', 'PS5 DualSense controller'), False)
chk('Xbox Series X matches',             rel('Xbox Series X', 'Microsoft Xbox Series X 1TB Console'), True)
chk('Xbox blocks headset',               rel('Xbox Series X', 'Xbox Series X wireless headset'), False)
chk('Nintendo Switch OLED matches',      rel('Nintendo Switch OLED', 'Nintendo Switch OLED Model White'), True)
chk('Nintendo Switch blocks carry case', rel('Nintendo Switch', 'Nintendo Switch carry case blue'), False)
chk('RTX 4080 matches',                  rel('RTX 4080', 'ASUS ROG Strix GeForce RTX 4080 16GB OC'), True)
chk('RTX 4080 blocks cleaning kit',     rel('RTX 4080', 'RTX 4080 cleaning kit GPU thermal paste'), False)
chk('RTX 4070 blocks cleaning kit',     rel('RTX 4070', 'RTX 4070 cleaning kit'), False)

# ── 7. LIETUVIŠKA PAIEŠKA ─────────────────────────────────────
print()
print('=== 7. LIETUVIŠKA PAIEŠKA ===')
chk('Samsung skalbyklė matches DE',      rel('Samsung skalbyklė', 'Samsung WW90T504AAW Waschmaschine 9kg'), True)
chk('Samsung skalbyklė matches EN',      rel('Samsung skalbyklė', 'Samsung WW11BB534CAW Washing Machine 11kg'), True)
chk('LG televizorius 55 matches',        rel('LG televizorius 55', 'LG 55UR78003LK 55 inch 4K UHD TV'), True)
chk('Dyson dulkių siurblys matches',     rel('Dyson dulkių siurblys', 'Dyson V11 Absolute Vacuum Cleaner'), True)
chk('Dyson dulkių siurblys blocks filter', rel('Dyson dulkių siurblys', 'Dyson filter replacement kit'), False)
chk('Philips skustuvas matches PL',      rel('Philips skustuvas', 'Philips S9000 Prestige Golarka SP9883'), True)
chk('Sony ausinės matches PL',           rel('Sony ausinės', 'Sony WH-1000XM5 Bezprzewodowe Słuchawki'), True)
chk('Sony ausinės blocks cable',         rel('Sony ausinės', 'Sony WH-1000XM5 Cable USB-C replacement'), False)
chk('Apple Watch matches',               rel('Apple Watch', 'Apple Watch Series 9 45mm GPS Aluminium'), True)
chk('Apple Watch blocks sport band',     rel('Apple Watch', 'Apple Watch sport band 45mm midnight'), False)
chk('Bosch skalbyklė matches PL',        rel('Bosch skalbyklė', 'Bosch Serie 4 Waschmaschine 8kg WAN28282PL'), True)
chk('Bosch skalbyklė blocks filter',     rel('Bosch skalbyklė', 'Bosch Filtras skalbyklei'), False)

# ── 8. KAINOS PARSAVIMAS ──────────────────────────────────────
print()
print('=== 8. KAINŲ PARSAVIMAS ===')
chk('EUR comma decimal',    parse_price('249,99 €'), 249.99)
chk('EUR dot decimal',      parse_price('249.99 EUR'), 249.99)
chk('PLN zł symbol',        parse_price('1 359,00 zł'), 1359.0)
chk('PLN zl text',          parse_price('3 359,00 zl'), 3359.0)
chk('PLN text symbol',      parse_price('1299,00 PLN'), 1299.0)
chk('no currency symbol',   parse_price('89,90'), 89.9)
chk('whole number',         parse_price('450'), 450.0)
chk('empty string',         parse_price(''), 0.0)
chk('garbage text',         parse_price('N/A'), 0.0)
chk('nbsp separator',       parse_price('1\xa0299,00\xa0€'), 1299.0)
chk('Eur suffix no space',  parse_price('599Eur'), 599.0)
chk('dot thousands comma',  parse_price('1.299,99'), 1299.99)
chk('comma thousands dot',  parse_price('1,299.99'), 1299.99)

# ── 9. CATEGORY ICONS ────────────────────────────────────────
print()
print('=== 9. KATEGORIJŲ IKONOS ===')
chk('iPhone -> phone',         get_category_icon('iPhone 16 Pro'), '📱')
chk('Samsung Galaxy -> phone', get_category_icon('Samsung Galaxy S24'), '📱')
chk('MacBook -> laptop',       get_category_icon('MacBook Pro 14'), '💻')
chk('laptop generic',          get_category_icon('laptop 15 inch'), '💻')
chk('TV keyword',              get_category_icon('Samsung 65 TV'), '📺')
chk('headphone keyword',       get_category_icon('Sony WH-1000XM5 headphone'), '🎧')
chk('ausines keyword',         get_category_icon('Sony ausines belaidės'), '🎧')
chk('PS5 -> gaming',           get_category_icon('PlayStation 5'), '🎮')
chk('RTX -> gaming',           get_category_icon('RTX 4070 Super'), '🎮')
chk('camera -> camera',        get_category_icon('Canon EOS R50 mirrorless'), '📷')
chk('Dyson vacuum -> vacuum',  get_category_icon('Dyson V15 vacuum'), '🧹')
chk('washing machine',         get_category_icon('Bosch washing machine'), '🫧')
chk('air fryer -> kitchen',    get_category_icon('Tefal air fryer'), '🍳')
chk('Philips skustuvas',       get_category_icon('Philips skustuvas'), '🪒')
chk('SSD -> pc parts',         get_category_icon('Samsung SSD 1TB nvme'), '🖥️')
chk('unknown -> shopping',     get_category_icon('Unknown XYZ gadget'), '🛒')

# ── 10. ENDPOINT VALIDATION ───────────────────────────────────
print()
print('=== 10. ENDPOINT VALIDACIJA ===')

r = c.get('/api/health')
d = r.get_json() or {}
chk_bool('health 200', r.status_code == 200)
chk_bool('health status=ok', d.get('status') == 'ok')
chk_bool('health version 5.13', '5.13' in d.get('version', ''))
chk_bool('health 8 shops', len(d.get('shops', [])) == 8)
chk_bool('health no ai_model_openai', 'ai_model_openai' not in d)
chk_bool('health no ai_model_claude', 'ai_model_claude' not in d)
chk_bool('health has ai_configured bool', isinstance(d.get('ai_configured'), bool))

r = c.get('/api/popular-searches')
d = r.get_json() or {}
chk_bool('popular-searches 200', r.status_code == 200)
chk_bool('popular-searches has searches list', isinstance(d.get('searches'), list))
chk_bool('popular-searches limit=3 ok', c.get('/api/popular-searches?limit=3').status_code == 200)

r = c.get('/api/rate-limit')
d = r.get_json() or {}
chk_bool('rate-limit 200', r.status_code == 200)
chk_bool('rate-limit has remaining', 'remaining' in d)
chk_bool('rate-limit has used', 'used' in d)
chk_bool('rate-limit has limit', 'limit' in d)

chk_bool('price-history no q -> 400', c.get('/api/price-history').status_code == 400)
chk_bool('price-history q -> 200', c.get('/api/price-history?q=test').status_code == 200)
chk_bool('price-history long q ok', c.get('/api/price-history?q=' + 'A'*300).status_code == 200)

chk_bool('search empty -> 400', c.post('/api/search', json={'query': ''}).status_code == 400)
chk_bool('search 1char -> 400', c.post('/api/search', json={'query': 'a'}).status_code == 400)
chk_bool('search no json -> 400', c.post('/api/search', data='', content_type='application/json').status_code == 400)
chk_bool('search XSS no crash', c.post('/api/search', json={'query': '<script>alert(1)</script>'}).status_code in (200, 400))
chk_bool('search SQLi no crash', c.post('/api/search', json={'query': "' OR 1=1 --"}).status_code in (200, 400))
chk_bool('search special chars', c.post('/api/search', json={'query': '!@#$%^&*()'}).status_code in (200, 400))

d = (c.post('/api/classify', json={'product_name': 'iPhone 16 Pro'}).get_json() or {})
chk_bool('classify iPhone -> MAIN', d.get('product_type') == 'MAIN')
d = (c.post('/api/classify', json={'product_name': 'iPhone silicone case'}).get_json() or {})
chk_bool('classify case -> ACCESSORY', d.get('product_type') == 'ACCESSORY')
chk_bool('classify no body -> 400/415', c.post('/api/classify').status_code in (400, 415))
chk_bool('classify empty name -> 400', c.post('/api/classify', json={'product_name': ''}).status_code == 400)
chk_bool('classify charger -> ACCESSORY', (c.post('/api/classify', json={'product_name': 'USB-C charger 65W'}).get_json() or {}).get('product_type') == 'ACCESSORY')

chk_bool('barcode no body -> 400/415', c.post('/api/barcode').status_code in (400, 415))
chk_bool('barcode empty -> 400', c.post('/api/barcode', json={'barcode': ''}).status_code == 400)
chk_bool('barcode 3 chars -> 404', c.post('/api/barcode', json={'barcode': '123'}).status_code == 404)
chk_bool('barcode letters -> 404', c.post('/api/barcode', json={'barcode': 'ABCDEFGH'}).status_code == 404)

chk_bool('scan-image no body -> 400', c.post('/api/scan-image', json={}).status_code == 400)
big = base64.b64encode(b'x' * 10_600_000).decode()
chk_bool('scan-image 10.6MB -> 413', c.post('/api/scan-image', json={'image': big}).status_code == 413)
small = base64.b64encode(b'\xff\xd8\xff' + b'x' * 100).decode()
chk_bool('scan-image small no key -> 503', c.post('/api/scan-image', json={'image': small}).status_code == 503)

r = c.get('/api/debug-html?shop=varle&q=test')
chk_bool('debug-html auth disabled -> not 401', r.status_code != 401)

# ── 11. SUGGEST SIMPLER QUERY ────────────────────────────────
print()
print('=== 11. SUGGEST SIMPLER QUERY ===')
chk('4 words -> first 2',       suggest_simpler_query('Apple iPhone 16 Pro Max'), 'Apple iPhone')
chk('2 words -> empty',         suggest_simpler_query('iPhone 16'), '')
chk('1 word -> empty',          suggest_simpler_query('Samsung'), '')
chk('empty string -> empty',    suggest_simpler_query(''), '')
chk('3 words -> first 2',       suggest_simpler_query('Sony WH-1000XM5 Silver'), 'Sony WH-1000XM5')

# ── SUMMARY ───────────────────────────────────────────────────
print()
print('=' * 60)
print(f'  Rezultatai: {total - fails}/{total} testų praejo')
if fails == 0:
    print('  VISI TESTAI PRAEJO!')
else:
    print(f'  {fails} TESTAI NEPRAEJO!')
print('=' * 60)
