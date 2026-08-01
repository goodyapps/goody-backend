# Mass Recognition Test Report

**Mode:** `mock`  
**Products tested:** 501 (sample=501)  
**Elapsed:** 9.22s  
**Total assertions:** 2498  
**Overall accuracy:** 96.16%  

---

## Threshold Check

| Category | Actual % | Threshold % | Status |
|---|---|---|---|
| lego | 100.0% | 98.0% | ✅ PASS |
| electronics | 96.05% | 95.0% | ✅ PASS |
| generic | 91.27% | 90.0% | ✅ PASS |
| hard_case | 91.87% | 85.0% | ✅ PASS |
| loyalty_pricing | 95.71% | 90.0% | ✅ PASS |
| OVERALL | 96.16% | 93.0% | ✅ PASS |

## Accuracy by Category

| Category | Products | Assertions | Passed | Accuracy |
|---|---|---|---|---|
| electronics | 201 | 886 | 851 | 96.05% |
| generic | 100 | 401 | 366 | 91.27% |
| hard_case | 51 | 209 | 192 | 91.87% |
| lego | 99 | 792 | 792 | 100.0% |
| loyalty_pricing | 50 | 210 | 201 | 95.71% |

## Accuracy by Difficulty

| Difficulty | Products | Assertions | Passed | Accuracy |
|---|---|---|---|---|
| easy | 396 | 1965 | 1898 | 96.59% |
| hard | 33 | 164 | 158 | 96.34% |
| medium | 72 | 369 | 346 | 93.77% |

## Accuracy by Input Type

| Input Type | Products | Assertions | Passed | Accuracy |
|---|---|---|---|---|
| barcode | 1 | 4 | 2 | 50.0% |
| photo | 2 | 8 | 7 | 87.5% |
| text | 498 | 2486 | 2393 | 96.26% |

## Top Failure Patterns

### 1. `false_negative` in category `electronics` — 25 failures

- query=`Apple iPhone SE 2022` → title=`iPhone SE (2022) 128GB`
- query=`Apple iPhone SE 2022` → title=`Apple iPhone SE 3rd Generation 128GB`
- query=`LG OLED55C3` → title=`LG 55C3 OLED evo 4K`

### 2. `false_positive` in category `generic` — 18 failures

- query=`Le Creuset casserole` → title=`Le Creuset cleaning spray`
- query=`Finish dishwasher tablets` → title=`Finish dishwasher cleaner`
- query=`Head and Shoulders shampoo` → title=`Shampoo pump head`

### 3. `false_negative` in category `generic` — 17 failures

- query=`Eucerin Q10 anti-wrinkle cream` → title=`Eucerin Anti-Age Nachtcreme 50ml`
- query=`Nescafé Gold instant coffee 200g` → title=`Nescafé Gold Löslicher Kaffee 200g Glas`
- query=`Nescafé Gold instant coffee 200g` → title=`Nescafé Gold Original 200g`

### 4. `false_negative` in category `hard_case` — 11 failures

- query=`Samsung Galaxy S24 Ultra case` → title=`OtterBox Commuter Series Samsung Galaxy S24 Ultra`
- query=`PS5 game Spider-Man 2` → title=`Spider-Man 2 PS5`
- query=`7622210701220` → title=`Milka Oreo Schokolade 100g`

### 5. `false_positive` in category `electronics` — 9 failures

- query=`Sony A7 IV` → title=`Akku Sony Alpha A7 IV`
- query=`Fujifilm X-T5` → title=`Battery grip Fujifilm X-T5`
- query=`GoPro HERO12 Black` → title=`GoPro battery HERO12`

### 6. `false_positive` in category `hard_case` — 6 failures

- query=`Bosch skalbimo mašina 9kg` → title=`Bosch Zulaufschlauch`
- query=`iPhone 11` → title=`Apple iPhone 11 Pro 64GB`
- query=`iPhone 11` → title=`Apple iPhone 11 Pro Max 256GB`

### 7. `false_positive` in category `loyalty_pricing` — 5 failures

- query=`Milka chocolate 200g` → title=`Milka chocolate tin collector`
- query=`Lay's chips 175g` → title=`Lay's chips bowl ceramic`
- query=`Milka Alpine Milk chocolate 100g` → title=`Milka chocolate tin collector`

### 8. `false_negative` in category `loyalty_pricing` — 4 failures

- query=`Danone Activia yogurt 4x125g` → title=`Activia Natural 4x125g loyalty offer`
- query=`Danone Activia yogurt 4x125g` → title=`Activia Greek Style 4x125g`
- query=`Lay's chips 175g` → title=`Lays Sour Cream & Onion 175g`

### 9. `critical_false_positive` in category `electronics` — 1 failures

- query=`DJI Mini 4 Pro` → title=`Propeller DJI Mini 4 Pro`
