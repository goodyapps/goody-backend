# TEST_RESULTS.md
**Date:** 2026-06-19

## Layer 1 — Logic Tests (500 products, no HTTP)

| Category | Total | Rel✓ | Rel✗ | Acc✓ | Acc✗ | UnitBug | PostProc∅ | ShortQ | LTdet |
|---|---|---|---|---|---|---|---|---|---|
| appliances | 20 | 20 | 0 | 20 | 0 | 0 | 0 | 0 | 0 |
| electronics | 20 | 19 | 1 | 20 | 0 | 0 | 0 | 10 | 0 |
| lego | 20 | 20 | 0 | 18 | 2 | 0 | 0 | 6 | 0 |
| food | 20 | 20 | 0 | 18 | 2 | 0 | 0 | 6 | 0 |
| cosmetics | 20 | 17 | 3 | 20 | 0 | 3 | 0 | 15 | 0 |
| clothing | 20 | 20 | 0 | 20 | 0 | 0 | 0 | 12 | 0 |
| books | 20 | 20 | 0 | 19 | 1 | 0 | 0 | 14 | 0 |
| household | 20 | 20 | 0 | 20 | 0 | 0 | 0 | 13 | 0 |
| sports | 20 | 18 | 2 | 19 | 1 | 0 | 1 | 4 | 0 |
| baby | 20 | 19 | 1 | 20 | 0 | 1 | 0 | 11 | 0 |
| **TOTAL** | **200** | **193** | **7** | **194** | **6** | **4** | **1** | **91** | **0** |

### Failed relevance checks (Rel✗) — good title rejected:

- `Anker 65W USB-C Charger` -> good title NOT matched: `Anker 65W USB-C GaN Ladegerät`
- `Dove Shampoo 400ml` -> good title NOT matched: `Dove Intensive Repair Shampoo 400ml`
- `Schwarzkopf Gliss 400ml` -> good title NOT matched: `Schwarzkopf Gliss Ultimate Repair Shampoo 400ml`
- `Garnier Micellar Water 400ml` -> good title NOT matched: `Garnier Skin Naturals Micellar Cleansing Water 400ml`
- `TRX Pro Suspension Trainer` -> good title NOT matched: `TRX PRO4 Suspension Trainer Kit`
- `Osprey Kestrel 48` -> good title NOT matched: `Osprey Kestrel 48 Herren Rucksack`
- `Nuk First Choice Plus Flasche 300ml` -> good title NOT matched: `NUK First Choice+ Babyflasche 300ml Silikonschnuller`

### Accessory filter failures (Acc✗) — bad title NOT filtered:

- `Hot Wheels Monster Trucks` -> accessory title NOT rejected: `Ramp set for Hot Wheels`
- `Barbie Fashionista` -> accessory title NOT rejected: `Clothes for Barbie Fashionista`
- `Haribo Goldbären 200g` -> accessory title NOT rejected: `Display box Haribo`
- `Jacobs Krönung 500g` -> accessory title NOT rejected: `Coffee grinder accessory`
- `Harry Potter Philosopher's Stone` -> accessory title NOT rejected: `Harry Potter bookmark`
- `Head Gravity MP` -> accessory title NOT rejected: `String set for Head Gravity MP`

### Unit-token false negatives (food/cosmetics units in query):

- `Dove Shampoo 400ml` (cat=cosmetics) — unit in query, title rejected
- `Schwarzkopf Gliss 400ml` (cat=cosmetics) — unit in query, title rejected
- `Garnier Micellar Water 400ml` (cat=cosmetics) — unit in query, title rejected
- `Nuk First Choice Plus Flasche 300ml` (cat=baby) — unit in query, title rejected

### _short_amazon_query truncations:

- `Samsung Galaxy S24 Ultra` -> `Samsung Galaxy S24`
- `Apple iPhone 15 Pro` -> `Apple iPhone 15`
- `Apple MacBook Air M3` -> `Apple MacBook Air`
- `Asus ROG Zephyrus G14 GA402` -> `Asus ROG Zephyrus`
- `Logitech MX Master 3S` -> `Logitech MX Master`
- `DJI Mini 4 Pro` -> `DJI Mini 4`
- `Lenovo ThinkPad X1 Carbon Gen 11` -> `Lenovo ThinkPad X1`
- `Canon EOS R6 Mark II` -> `Canon EOS R6`
- `Anker 65W USB-C Charger` -> `Anker 65W USB-C`
- `Google Pixel 8 Pro` -> `Google Pixel 8`
- `LEGO Harry Potter 76430` -> `LEGO Harry 76430`
- `LEGO Star Wars 75367` -> `LEGO Star 75367`
- `LEGO Speed Champions 76919` -> `LEGO Speed 76919`
- `LEGO Creator Expert 10281` -> `LEGO Creator 10281`
- `Hot Wheels Monster Trucks` -> `Hot Wheels Monster`
- `Nerf Elite 2.0 Commander` -> `Nerf Elite 2.0`
- `Lindt Excellence 70% 100g` -> `Lindt Excellence 70%`
- `Alpro Soya Drink 1L` -> `Alpro Soya Drink`
- `Dr. Oetker Backhefe 7g` -> `Dr. Oetker Backhefe`
- `Ritter Sport Marzipan 100g` -> `Ritter Sport Marzipan`
- `Kellogg's Corn Flakes 750g` -> `Kellogg's Corn Flakes`
- `Maggi Suppe 3er Pack` -> `Maggi Suppe 3er`
- `L'Oreal Elvive Shampoo 400ml` -> `L'Oreal Elvive Shampoo`
- `Head & Shoulders 500ml` -> `Head & Shoulders`
- `Gillette Fusion5 Klingen 8` -> `Gillette Fusion5 Klingen`
- `Oral-B Pro 3 3500` -> `Oral-B Pro 3500`
- `Rexona 48h Deo 150ml` -> `Rexona 48h Deo`
- `Garnier Micellar Water 400ml` -> `Garnier Micellar Water`
- `Neutrogena Hydro Boost 50ml` -> `Neutrogena Hydro Boost`
- `CeraVe Moisturizing Cream 454g` -> `CeraVe Moisturizing Cream`
- `The Ordinary Niacinamide 30ml` -> `Ordinary Niacinamide 30ml`
- `Eucerin UreaRepair PLUS 5% 400ml` -> `Eucerin UreaRepair PLUS`
- `Avène Thermal Spring Water 300ml` -> `Avène Thermal Spring`
- `La Roche-Posay Anthelios SPF50 50ml` -> `La Roche-Posay Anthelios`
- `Bioderma Sensibio H2O 250ml` -> `Bioderma Sensibio H2O`
- `Vichy Liftactiv Supreme 50ml` -> `Vichy Liftactiv Supreme`
- `Kiehl's Ultra Facial Cream 50ml` -> `Kiehl's Ultra Facial`
- `Nike Air Max 270` -> `Nike Air Max`
- `Levi's 501 Original Jeans` -> `Levi's 501 Original`
- `Puma Softride Pro 24` -> `Puma Softride Pro`
- `Adidas Tiro 23 Hose` -> `Adidas Tiro 23`
- `The North Face Resolve 2` -> `North Face Resolve`
- `H&M Regular Fit Shirt XL` -> `H&M Regular Fit`
- `Zara Slim Fit Trousers 32` -> `Zara Slim Fit`
- `Mango Slim Jeans W30` -> `Mango Slim Jeans`
- `Tommy Hilfiger Polo XL` -> `Tommy Hilfiger Polo`
- `Hugo Boss Suit 48` -> `Hugo Boss Suit`
- `Calvin Klein Boxer Briefs M` -> `Calvin Klein Boxer`
- `Gant Shield Hoodie L` -> `Gant Shield Hoodie`
- `Atomic Habits James Clear` -> `Atomic Habits James`
- `Harry Potter Philosopher's Stone` -> `Harry Potter Philosopher's`
- `Clean Code Robert Martin` -> `Clean Code Robert`
- `The 7 Habits Covey` -> `7 Habits Covey`
- `Thinking Fast and Slow` -> `Thinking Fast Slow`
- `Sapiens Yuval Noah Harari` -> `Sapiens Yuval Noah`
- `The Great Gatsby Fitzgerald` -> `Great Gatsby Fitzgerald`
- `Rich Dad Poor Dad Kiyosaki` -> `Rich Dad Poor`
- `The Lean Startup Ries` -> `Lean Startup Ries`
- `Deep Work Cal Newport` -> `Deep Work Cal`
- `Zero to One Peter Thiel` -> `Zero to One`
- `Man's Search for Meaning Frankl` -> `Man's Search Meaning`
- `The Power of Now Tolle` -> `Power Now Tolle`
- `Surely You're Joking Feynman` -> `Surely You're Joking`
- `Philips Hue White E27 3er Pack` -> `Philips Hue White`
- `Tefal Ingenio Pfanne 28cm` -> `Tefal Ingenio Pfanne`
- `Zwilling Pro Messer 20cm` -> `Zwilling Pro Messer`
- `Braun Series 9 Pro 9477cc` -> `Braun Series 9`
- `Philips Airfryer XXL HD9860` -> `Philips Airfryer XXL`
- `Vileda 1-2 Spray Mop` -> `Vileda 1-2 Spray`
- `Leifheit Pegasus 200 Solid` -> `Leifheit Pegasus 200`
- `Emsa Clip & Close 3er Set` -> `Emsa Clip &`
- `Melitta Caffeo Solo E950` -> `Melitta Caffeo Solo`
- `Klarstein Maipo Fondue 1200W` -> `Klarstein Maipo Fondue`
- `Rowenta Steam Force DW9280` -> `Rowenta Steam Force`
- `Elgato Key Light 45W` -> `Elgato Key Light`
- `Sage Barista Express SES875` -> `Sage Barista Express`
- `Suunto 9 Peak Pro` -> `Suunto 9 Peak`
- `TRX Pro Suspension Trainer` -> `TRX Pro Suspension`
- `Wilson Pro Staff 97` -> `Wilson Pro Staff`
- `Callaway Rogue ST Max` -> `Callaway Rogue ST`
- `Pampers Premium Care Newborn 2-5kg` -> `Pampers Premium Care`
- `Aptamil Profutura 1 800g` -> `Aptamil Profutura 1`
- `Babybjörn Baby Carrier One` -> `Babybjörn Baby Carrier`
- `Nuk First Choice Plus Flasche 300ml` -> `Nuk First Choice`
- `Graco Pack'n Play On The Go` -> `Graco Pack'n Play`
- `Philips Avent Natural 3.0 260ml` -> `Philips Avent Natural`
- `Beurer BC 58 Babyphone` -> `Beurer BC 58`
- `Britax Römer Dualfix iSense` -> `Britax Römer Dualfix`
- `Maxi-Cosi Pearl 360 Pro` -> `Maxi-Cosi Pearl 360`
- `Silver Cross Wave 2` -> `Silver Cross Wave`
- `Munchkin Latch Flasche 240ml` -> `Munchkin Latch Flasche`

---

## Layer 2 — Live Smoke Test (20 products)

| Query | Category | Results | Time(s) | Status |
|---|---|---|---|---|
| Samsung RB34C600ESA | appliances | 1 | 0.6 | ok |
| Bosch WAX32EH0 | appliances | 0 | 10.7 | zero |
| Sony WH-1000XM5 | electronics | 3 | 8.4 | ok |
| Apple iPhone 15 Pro 128GB | electronics | 2 | 9.7 | ok |
| LEGO Technic 42170 | lego | 2 | 8.3 | ok |
| LEGO Harry Potter 76430 | lego | 0 | 7.2 | zero |
| Milka 100g | food | 2 | 10.4 | ok |
| Nutella 400g | food | 2 | 9.2 | ok |
| Dove Shampoo 400ml | cosmetics | 1 | 10.9 | ok |
| Nivea Creme 250ml | cosmetics | 2 | 11.2 | ok |
| Nike Air Max 270 42 | clothing | 0 | 8.6 | zero |
| Adidas Ultraboost 22 | clothing | 0 | 9.7 | zero |
| Atomic Habits James Clear | books | 1 | 14.2 | ok |
| Clean Code Robert Martin | books | 1 | 5.7 | ok |
| Dyson V15 Detect | household | 2 | 9.4 | ok |
| Philips Airfryer XXL HD9860 | household | 0 | 6.9 | zero |
| Garmin Forerunner 265 | sports | 2 | 8.1 | ok |
| Polar Vantage V3 | sports | 2 | 11.3 | ok |
| Pampers Premium Care Newborn | baby | 1 | 7.4 | ok |
| Aptamil Profutura 1 800g | baby | 0 | 4.8 | zero |

**OK:** 14/20  **Zero results:** 6/20  **Errors:** 0/20

### Zero-result queries:

- `Bosch WAX32EH0` (appliances)
- `LEGO Harry Potter 76430` (lego)
- `Nike Air Max 270 42` (clothing)
- `Adidas Ultraboost 22` (clothing)
- `Philips Airfryer XXL HD9860` (household)
- `Aptamil Profutura 1 800g` (baby)
