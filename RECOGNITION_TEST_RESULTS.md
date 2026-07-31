# RECOGNITION_TEST_RESULTS.md

**Run date:** 2026-07-31 20:32:40  
**Cases:** 145  
**Assertions:** 997  
**Passed:** 952  
**Failed:** 45  
**Pass rate:** 95.5%  
**Elapsed:** 0.22s  

---

## ⚠️ should_match failures (false negatives)

- **[anker_65w_charger]** query=`Anker 65W USB-C Charger` did NOT match `Anker Nano Pro 65W 3-Port-Ladegerät`
- **[milka_chocolate_100g]** query=`Milka chocolate 100g` did NOT match `Milka Alpenmilch Schokolade 100g`
- **[milka_chocolate_100g]** query=`Milka chocolate 100g` did NOT match `Milka Oreo Schokolade 100g`
- **[garnier_skin_naturals]** query=`Garnier Skin Naturals` did NOT match `Garnier SkinActive Mizellen Reinigungswasser`
- **[barcode_7622210701220]** query=`7622210701220` did NOT match `Milka Oreo Schokolade 100g`
- **[barcode_7622210701220]** query=`7622210701220` did NOT match `Milka Oreo Chocolate 100g`
- **[barcode_5900951287541]** query=`5900951287541` did NOT match `Lay's Classic Chips 200g`
- **[barcode_5900951287541]** query=`5900951287541` did NOT match `Lays Kartoffelchips 150g`
- **[lt_adata_nesiojamas]** query=`Apple MacBook nešiojamas kompiuteris` did NOT match `Apple MacBook Pro 14 M3 laptop`
- **[ambiguous_apple_watch]** query=`Apple Watch Ultra` did NOT match `Apple Watch Ultra 2 Titanium Case with Trail Loop`
- **[ambiguous_mini_projector]** query=`mini projector` did NOT match `Mini Beamer Full HD 1080p 200ANSI tragbar`
- **[ambiguous_mini_projector]** query=`mini projector` did NOT match `XGIMI Halo+ 1080p Projektor tragbar Mini`
- **[known_bug_cross_lang_charger]** query=`Anker Ladegerät 65W` did NOT match `Anker Nano Pro 65W Charger`
- **[electronics_lg_oled_55c3]** query=`LG OLED55C3PSA` did NOT match `LG OLED C3 55" 4K TV`
- **[ambiguous_hot_wheels_ramp]** query=`Hot Wheels Ramp Set` did NOT match `Ramp Set for Hot Wheels Track Builder`
- **[electronics_ps5]** query=`PlayStation 5 Console` did NOT match `Sony PlayStation 5 Disc Edition`
- **[electronics_ps5]** query=`PlayStation 5 Console` did NOT match `PlayStation 5 Slim Digital Edition`
- **[electronics_nest_hub]** query=`Google Nest Hub 2nd Gen` did NOT match `Google Nest Hub (2. Generation) 7-Zoll-Anzeige`
- **[fmcg_pampers_size3]** query=`Pampers Active Baby Size 3` did NOT match `Pampers Baby-Dry Größe 3 Monatsbox`
- **[barcode_4008400323978]** query=`4008400323978` did NOT match `Kinder Schokolade 100g`
- **[barcode_4008400323978]** query=`4008400323978` did NOT match `Ferrero Kinder Schokolade Riegel`
- **[lt_velosipedas]** query=`elektrinis dviratis Bosch motor` did NOT match `Cube Reaction Hybrid Pro 500 e-bike Bosch Performance CX`
- **[electronics_apple_pencil]** query=`Apple Pencil 2nd generation` did NOT match `Apple Pencil (2. Generation) für iPad Pro`
- **[electronics_apple_pencil]** query=`Apple Pencil 2nd generation` did NOT match `Apple Pencil 2. Gen USB-C`
- **[ambiguous_ipad_vs_case]** query=`iPad Air 5th generation` did NOT match `Apple iPad Air (5. Generation) 64GB Wi-Fi`
- **[ambiguous_ipad_vs_case]** query=`iPad Air 5th generation` did NOT match `Apple iPad Air 5 M1 256GB Wi-Fi`
- **[electronics_benq_monitor]** query=`BenQ EW2880U 28 inch 4K monitor` did NOT match `BenQ EW2880U Eye-care IPS Display`
- **[lt_sienas_kamera]** query=`apsaugos kamera lauke 4K Dahua` did NOT match `Dahua IPC-HFW2849S-S-IL 4K Smart Dual Light Fixed-focal Bullet Network Camera`
- **[electronics_jabra_evolve2]** query=`Jabra Evolve2 85` did NOT match `Jabra Evolve2 85 MS Stereo mit USB-A Dongle`
- **[fmcg_fairy_dishwasher]** query=`Fairy Platinum Dishwasher Tablets 72 pcs` did NOT match `Fairy Platinum Plus Geschirrspülmaschinentabs 72er`
- **[fmcg_whiskas_cat_food]** query=`Whiskas Adult Cat Food 1+ 400g` did NOT match `Whiskas 1+ Adult Katzenfutter Nass 400g Rind in Gelee`
- **[fmcg_whiskas_cat_food]** query=`Whiskas Adult Cat Food 1+ 400g` did NOT match `Whiskas Adult Katzennahrung 400g Truthahn`
- **[lt_espresso_kavos_aparatas]** query=`espresso kavos aparatas DeLonghi Magnifica` did NOT match `De'Longhi Magnifica Evo ECAM290.21.B pilnai automatinis kavos aparatas`
- **[fmcg_dreft_pods]** query=`Dreft Baby Laundry Pods 25 pcs` did NOT match `Dreft Platinum Plus Baby Capsules 25WL`

## ⚠️ should_not_match failures (false positives)

- **[lego_harry_potter_76430]** query=`LEGO Harry Potter 76430` wrongly matched `Book about LEGO 76430`
- **[sony_a7_iv]** query=`Sony A7 IV` wrongly matched `Akku Sony Alpha A7 IV`
- **[ambiguous_pro_variant]** query=`TRX PRO4` wrongly matched `Tür-Anker für TRX PRO4`
- **[ambiguous_hot_wheels_ramp]** query=`Hot Wheels Ramp Set` wrongly matched `Hot Wheels einzelne Autos 5er Pack`
- **[lt_siuvimo_masina]** query=`siuvimo mašina Singer` wrongly matched `Siūlų rinkinys Singer siuvimo mašinai`
- **[lt_kavos_aparatas]** query=`kavos aparatas DeLonghi espresso` wrongly matched `Filtro paketas DeLonghi kavos aparatui`
- **[electronics_gopro_hero12]** query=`GoPro Hero 12 Black` wrongly matched `Akku GoPro Hero 12 Black`
- **[electronics_steam_deck]** query=`Steam Deck OLED 512GB` wrongly matched `microSD 512GB für Steam Deck`
- **[electronics_nikon_z6iii]** query=`Nikon Z6 III` wrongly matched `EN-EL15c Akku Nikon Z6 III`
- **[fmcg_nescafe_gold]** query=`Nescafé Gold 200g` wrongly matched `Kaffeedispenser für Büro`
- **[fmcg_persil_flussig]** query=`Persil Flüssigwaschmittel 40 Waschgänge` wrongly matched `Persil Universal 3in1 Discs 40ST`

## Category breakdown

- `ambiguous`: 12 cases
- `appliances`: 16 cases
- `barcode`: 4 cases
- `books`: 2 cases
- `electronics`: 54 cases
- `fmcg`: 14 cases
- `known_bugs`: 8 cases
- `lego`: 14 cases
- `lt_language`: 21 cases
