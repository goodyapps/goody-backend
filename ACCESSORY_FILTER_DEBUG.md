# ACCESSORY_FILTER_DEBUG.md
**Data:** 2026-06-19  
**Simptomas:** "LEGO 76430 Hogwarts" paieška grąžino LED apšvietimo priedą (€27.98)  
vietoj tikro LEGO rinkinio (€78.98) → rodoma klaidinga "Sutaupoma €51.00 / 65% pigiau"

---

## 1. Kodėl accessory filtras praleido šį priedą?

### Klaidos kelias (step-by-step)

**Tikėtinas Amazon h2 title:** `"LEGO 76430 LED Lighting Kit Hogwarts Owl Post"`  
(arba panašus — brand+model iš pradžių be "for"/"compatible with" frazės)

```
query = "LEGO Harry 76430"   # po _short_amazon_query
title = "lego 76430 led lighting kit hogwarts owl post"   # po _norm_units (lowercase)
```

**Žingsnis 1 — `compat_patterns` (eilutės 602–613):**
```python
r'\bfor\s+[a-z]+'    # "for lego" — NERASTAS (nėra "for" žodžio prieš "lego")
r'\bcompatible\s+with\b'  # NERASTAS
# visos kitos šablonai — NERASTA
```
→ **Praleista**. Jei title būtų `"LED Kit compatible with Lego 76430"` — būtų sugautas.  
Jei title būtų `"LED Kit for Lego 76430"` — būtų sugautas.  
Bet kai "LEGO" yra pavadinimo **pradžioje be preposition** — nė vienas šablonas nesutampa.

**Žingsnis 2 — `_ACCESSORY_MATCH_WORDS` (eilutės 615–623):**
```python
# Tikrinama: ar acc yra t, bet ne q?
# "led"      → nėra frozenset'e ← SPRAGOS
# "lighting" → nėra frozenset'e ← SPRAGA
# "light kit"→ nėra frozenset'e ← SPRAGA
# "light set"→ nėra frozenset'e ← SPRAGA
```
→ **Praleista**. Žodžiai "led", "lighting", "light kit" nėra `_ACCESSORY_MATCH_WORDS` sąraše.

**Žingsnis 3 — Brand + model patikrinimas (eilutės 639–674):**
```python
brands_in_q = ["lego"]          # "lego" yra _KNOWN_BRANDS (eilutė 308)
"lego" in t_ns?  → TAIP         # "lego 76430 led lighting..." turi "lego"
model_tokens = ["76430"]        # 76430 nefiltruojamas (ne vienetas)
_model_in_title("76430")? → TAIP  # "76430" yra title
```

Toliau (eilutė 664–674):
```python
# Tikrinama: ar title turi "for lego|compatible with lego|..."?
if re.search(r'\b(?:for|compatible\s+with|designed\s+for|...)\s+lego', t):
    return False
# "lego 76430 led lighting kit" — "lego" NĖRA po "for/compatible" → NESUGAUTAS
return True   # ← KLAIDINGAI PRALEISTAS
```

→ **Funkcija grąžina True** — priedas rodomas kaip tinkamas rezultatas.

### Struktūrinė klaidos priežastis

Tikrinimas eilutėje 664–672 ieško **"for/compatible with BRAND"** šablono — t.y. ar brandas einą PO prediakto žodžio. Bet jis **nepastebi** kai brand+model yra pavadinimo pradžioje:

| Pavadinimas | Pagaunama? | Kodėl |
|---|---|---|
| `"LED Kit for LEGO 76430"` | ✓ Taip | `\bfor\s+lego` atitinka `compat_patterns` |
| `"LED Kit compatible with LEGO 76430"` | ✓ Taip | `\bcompatible\s+with\b` atitinka `compat_patterns` |
| `"LEGO 76430 LED Lighting Kit"` | ✗ **Ne** | "lego" pavadinimo pradžioje, nėra preposition → niekas nesugauna |
| `"BrickBling LEGO 76430 LED Lights"` | ✗ **Ne** | Ta pati problema |

---

## 2. Kaip veikia model code atitikimas

```python
# is_relevant_result("LEGO Harry 76430", title):

# 1. Normalizacija
q = _norm_units("lego harry 76430")  # → "lego harry 76430"
t = _norm_units(title)               # → lowercase, "128 gb" → "128gb"

# 2. Model tokenai iš query
model_tokens = re.findall(r'\b[a-z]*\d+[a-z0-9-]*\b', q)
# → ["76430"]
# Filtruojami unit tokenai: "100g", "400ml" → pašalinama
# "76430" neturi unit sufikso → lieka

# 3. Ar kiekvienas model tokenas yra title?
def _model_in_title(m):           # m = "76430"
    if re.search(r'(?<![a-z0-9])76430(?![a-z0-9])', t):  # exact word
        return True
    if "76430" in t_nh:           # compact (be brūkšnelių)
        return True
    return False
# → True (76430 yra LED akcesuary pavadinime)

# 4. Jei brands_in_q ir visi model tokenai rasti → grąžina True ANKSČIAU
# nei tikrina papildomus accessory signalus
```

**Kritinė problema:** Kai brand+model patvirtinti (eilutė 674 `return True`), funkcija **nebekvietė** jokių papildomų tikrinimų — viskas praleista.

---

## 3. Kokie title signalai rodo priedą — ir ko trūksta

### Dabar veikianti aptikimas:

| Šablonas | Pavyzdys | Metodas |
|---|---|---|
| "for [brand]" | "LED Kit for Dyson V15" | `compat_patterns` `\bfor\s+[a-z]+` |
| "compatible with" | "Case compatible with iPhone" | `compat_patterns` `\bcompatible\s+with\b` |
| "designed for" | "Strap designed for Galaxy Watch" | eilutė 669 |
| "compatible" (vienas žodis) | "Adapter compatible iPhone" | `_ACCESSORY_MATCH_WORDS` eilutė 547 |
| "accessories" | "Accessories for PS5" | `_ACCESSORY_MATCH_WORDS` |
| "replacement" | "Replacement filter" | `_ACCESSORY_MATCH_WORDS` |

### Ko šiuo metu TRŪKSTA `_ACCESSORY_MATCH_WORDS`:

| Žodis | Pavyzdys, kur atsiranda | Rizika jei pridėti |
|---|---|---|
| `"lighting"` | "LEGO 76430 Lighting Kit" | Žema — jei query neturi "lighting", tai priedas |
| `"light kit"` | "Hogwarts Light Kit LocoLee" | Žema — "light kit" retai pagrindinis produktas |
| `"light set"` | "LED Light Set for LEGO" | Žema — analogiškai |
| `"led light"` | "LocoLee LED Light 76430" | Vidutinė — "LED" galima painioti su LED TV |
| `"only lights"` | "Only Lights, Not a Lego Model" | Žema — labai specifiškas tekstas |

**Pavojingi žodžiai (ne pridėti):**
- `"light"` — per platus: "Google Pixel 8a Light" (spalva), "LG light series"
- `"led"` — per platus: "LG LED TV", "Philips LED bulb" gali būti pagrindinis produktas

---

## 4. Kainos anomalijų aptikimas

**Dabar:** Nėra jokio kainų palyginimo filtro `post_process` funkcijoje.

```python
def post_process(results, query, language):
    # filtruoja pagal relevance, deduplikuoja, kviečia AI verdict
    # BET: niekada nelygina kainos su kitais rezultatais
    # nėra "65% cheaper than median → suspicious" logikos
```

**Šiuo atveju:**
- Pigu.lt: €78.98 (tikras LEGO rinkinys)
- Amazon.DE: €27.98 (LED priedas) — **65% pigiau**

Tokia kainų skirtumas turėtų kelti įspėjimą. Jei produkto kaina yra >50% žemiau medianinės kitos rezultatų kainos, tai galimas arba:
1. Akivaizdus sandoris (labai reta)
2. Klaidingai sugretintas produktas (dažniau)

---

## 5. Siūloma filtravimo strategija

### Strategija A — Pridėti LED/apšvietimo žodžius į `_ACCESSORY_MATCH_WORDS` *(MAŽA RIZIKA)*

```python
# Pridėti į _ACCESSORY_MATCH_WORDS:
'lighting kit', 'light kit', 'light set', 'led light', 'light compatible',
'only lights', 'not a lego model', 'usb light', 'light for lego',
```

**Rizika:** Mažos. `_ACCESSORY_MATCH_WORDS` tikrina: ar žodis yra title, bet NE query? Jei vartotojas ieškotų "LEGO light kit" (ieško apšvietimo), šie žodžiai būtų ir query → filtras neaktyvuotų.

**Problema:** Užklausos be "light kit" bet apie LED produktus (pvz., Philips Hue LED Kit) gali būti klaidingai filtruotos. Reikia patikrinti arba naudoti LEGO-specific versiją.

---

### Strategija B — Tikrinti "BRAND+MODEL pavadinime bet tai nėra tas pats produktas" *(VIDUTINĖ RIZIKA)*

```python
# Po model_tokens aptikimo (eilutė 674), PRIEŠ return True:
# Papildomas patikrinimas: ar title pradžioje yra kitoks brandas (ne query brand)?
if brands_in_q:
    title_words = t.split()
    title_brand = title_words[0] if title_words else ""
    query_brands = {b.replace(" ", "") for b in brands_in_q}
    if title_brand not in query_brands:
        # Pirmas žodis nėra query brand — gali būti kito gamintojo priedas
        # Tikrinti papildomai: ar yra accessory signalų?
        _light_words = {"lighting", "light kit", "light set", "led light"}
        if any(lw in t for lw in _light_words):
            return False
```

**Rizika:** Vidutinė. Gali sugadinti teisingus rezultatus, kur title pradeda distributor/seller vardas.

---

### Strategija C — Kainų anomalijų aptikimas `post_process` *(MAŽESNĖ RIZIKA)*

```python
def post_process(results, query, language):
    ...
    # NAUJAS: outlier kainų filtras
    if len(results) >= 2:
        prices = [r["price"] for r in results if r.get("price")]
        if prices:
            median_price = sorted(prices)[len(prices) // 2]
            filtered = []
            for r in results:
                p = r.get("price", 0)
                if p > 0 and p < median_price * 0.35:  # >65% pigiau nei medianas
                    print(f"[post_process] price anomaly: {p} vs median {median_price}, dropping")
                    continue  # Nerodom staigiai pigesno rezultato
                filtered.append(r)
            results = filtered if filtered else results  # Negrąžinam tuščio
```

**Rizika:** Galimi false positives kai tikrai yra didelis skirtumas (pvz., naudotas vs naujas). Bet 65% skirtumas yra labai ryškus — tai tinkamas threshold.

---

## Rizikos įvertinimas

| Strategija | Aptikimo tikimybė | False positive rizika | Įgyvendinimo sudėtingumas |
|---|---|---|---|
| A — LED žodžiai į frozenset | Aukšta šiam atvejui | Žema | Žema |
| B — Pirmo žodžio patikrinimas | Vidutinė | Vidutinė | Vidutinė |
| C — Kainų anomalijų filtras | Aukšta bet ne visuomet | Žema | Žema |

**Rekomenduojama kombinacija:** A + C

- A fiksuoja šio tipo priedus (LED kit su brand+model SEO stuffing)
- C fiksuoja bet kokią kainų anomaliją, kuri praslysta pro kitus filtrus

---

## Tikslus kodo kelias, vedęs į klaidą

```
1. Vartotojas ieško: "LEGO 76430 Hogvartso" (arba "LEGO Harry Potter 76430")
2. _short_amazon_query → "LEGO Harry 76430"
3. Amazon.DE grąžina sponsored priedą: h2.aria-label = 
   "LEGO 76430 LED Lighting Kit Hogwarts Owl Post" (arba panaši formuluotė)
4. is_relevant_result("LEGO Harry 76430", "lego 76430 led lighting kit..."):
   → compat_patterns: nėra "for lego" / "compatible with" → PRALEISTA
   → _ACCESSORY_MATCH_WORDS: "lighting" nėra frozenset'e → PRALEISTA
   → brand check: "lego" title'e → PASS
   → model check: "76430" title'e → PASS
   → brands_in_q check: nėra "for lego" prieš brand → return True ← KLAIDA
5. Priedas patenka į rezultatus
6. post_process: nėra kainų anomalijų tikrinimo → lieka
7. UI rodo: Amazon.DE €27.98 vs Pigu.lt €78.98 → "Sutaupoma €51.00 / 65% pigiau"
```

---

## Kodėl ŠIUO ATVEJU filtras turėjo veikti, bet nepaveikė

Jei tikrasis title buvo `"LocoLee Light Compatible with Lego 76430..."` — `compat_patterns` `\bcompatible\s+with\b` **TURĖJO** jį sugauti. Tačiau Amazon search results puslapio `<h2>` `aria-label` **dažnai skiriasi** nuo product page pavadinimo. Sponsored ads gali naudoti **marketing title** h2'e — trumpesnę versiją be "compatible with" frazės.

**Galimi h2 variantai, kurie praslystų pro filtrą:**
- `"LocoLee LED Light LEGO 76430 Hogwarts USB-C"` — nėra "for/compatible with"
- `"76430 Hogwarts Castle LED Lights Rechargeable"` — nėra brand visai, bet "76430" in title; "lego" nėra → brands_in_q check grąžina False (brands_in_q = ["lego"] bet "lego" nėra t_ns) → funkcija grąžintų False eilutėje 642. Šis variantas NEBŪTŲ praleistas.

**Tiksliausia hipotezė:** h2 title turėjo "lego" ir "76430" bet be "for"/"compatible with":
```
"LEGO 76430 LED Lighting Set Hogwarts LocoLee"  ← praslystų
"BrickBling LEGO 76430 Lights Hogwarts"          ← praslystų
```

---

## Santrauka

| Klausimas | Atsakymas |
|---|---|
| Kodėl compat_patterns neveikė? | H2 title neturėjo "for [brand]" / "compatible with" frazės — sponsored titles dažnai būna kitokios formos |
| Kaip veikia model atitikimas? | Visi query model tokenai (76430) turi būti title'e → true → early return True |
| Kokie trūkstami signalai? | "led light", "lighting", "light kit", "light set", "only lights" nėra `_ACCESSORY_MATCH_WORDS` |
| Kainų anomalija? | Nėra `post_process` kainų tikrinimo |
| Geriausias fix? | Pridėti LED/apšvietimo žodžius į `_ACCESSORY_MATCH_WORDS` + kainų anomalijų filtras `post_process` |
| Rizika? | Žema — abu fix'ai yra konservatyvūs ir targeted |
