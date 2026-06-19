# UX_EXPLORATION.md
**Data:** 2026-06-20 | **Šaka:** security-night  
**Metodas:** Frontend kodo analizė (index.html ~6400 eilučių) — vartotojo kelio rekonstrukcija

---

## VARTOTOJO KELIAS: NUFOTOGRAFUOK → RASK KAINĄ

```
[Pradžia] Hero mygtukas 📷
    ↓ openCam()
[Kamera] 3 režimai: Price tag / Barcode / Upload
    ↓ takePhoto()
[Identifikacija] API: /api/identify-product (30s timeout)
    ↓ _showConfirmResult() arba _showConfirmError()
[Patvirtinimas] Vartotojas mato pavadinimą + gali redaguoti
    ↓ confirmSearch()
[Paieška] API: /api/search-stream (90s timeout) — partial results stream
    ↓ renderResults()
[Rezultatai] Verdict bar + shop cards + kainų istorija
    ↓ "Buy now" → išeina į parduotuvę
[Grįžimas] Back banner jei grįžta per browser tab
```

---

## TRINTYS VARTOTOJO KELYJE

### T1 — Laukimo laikas: iki 2 minučių

**Problema:** Blogiausias atvejis: identify (~30s) + search (~90s) = 2 minutės be jokių rezultatų.

**Kodas:**
```javascript
const _sc=new AbortController();
const _st=setTimeout(()=>_sc.abort(),30000);  // identify: 30s timeout
const _tid=setTimeout(()=>_ctrl.abort(),90000); // search: 90s timeout
```

**Kas vartotojas mato:**
1. "Atpažįstu produktą..." + suktukas → iki 30s
2. Patvirtinimo ekranas (jei sekasi) → vartotojas paspaudžia "Ieškoti"
3. "Ieškome geriausių kainų..." + 3 rotacinės žinutės → iki 90s

**Geras žingsnis:** Daliniai rezultatai atkeliauja per SSE — pirmos kainos pasirodo jau po ~7-9s nuo paieškos pradžios. Tai labai pagerina suvokiamą greitį.

**Problema:** Tarp nuotraukos ir PIRMOS kainos realus laikas gali būti 30s (identify) + 7-9s (pirma parduotuvė) = **~40 sekundžių**. Tai per ilga mobiliesiems vartotojams.

---

### T2 — "Produktas neatpažintas" — aklavietė neaiški

**Ekranas po nesėkmingo identify:**
```javascript
_showConfirmError(partialData)
// Rodo: "Įvesk pavadinimą arba fotografuok iš arčiau"
// + input laukas + "Ieškoti" mygtukas + "Fotografuoti iš naujo"
```

**Gerai:** Yra du veiksmai — rankinė paieška arba pakartoti nuotrauką.

**Problema:** Vartotojas nežino, KAS nepavyko. Trūksta:
- "Ar daiktas neturėjo etiketės?"
- "Ar nuotrauka buvo per tamsi?"
- Nėra vizualinio pavyzdžio kaip nufotografuoti teisingai

Jei input laukas tuščias → "Ieškoti" mygtukas neveikia (`if(!q)return;`) — vartotojas gali nesuprati kodėl mygtukas nereaguoja.

---

### T3 — Kamera: nėra kokybės tikrinimo

**Problema:** Vartotojas gali nufotografuoti neaiškų, per tamso arba per tolimą vaizdą. Sistema jį siūlo identify, AI sako "žemas tikslumas", tada vartotojas gauna įspėjimą (`warn.style.display="block"`) — bet tik PO to, kai buvo iššauktas API.

**Trūksta:**
- Realaus laiko kokybės indikatoriaus kameroje (pvz., "Per toli" ar "Geresnis apšvietimas")
- ZXing barcode scanner naudojamas barkodams — veikia realiu laiku. Toks pat patyrimas galėtų veikti price tag režimui.

---

### T4 — "Nieko nerasta" — gerai suprojektuotas

**Vertinimas: GERAS.** `_nr` objektas turi:
- Redaguojamą paieškos lauką (vartotojas gali pataisyti)
- "Fotografuoti dar kartą" mygtuką
- 2 patarimų eilutes (sutrumpink, pabandyk be regiono kodo)
- Amazon.de atsarginę nuorodą (su affiliate tagu)
- Populiarių paieškų chips

**Viena problema:** Tik 1 iš 2 patarimų matomas pirmiau lauko — vartotojas gali jų nepastebėti prieš bandydamas dar kartą.

---

### T5 — Rate limit: "Grįžk rytoj" be alternatyvos

**Kodas:**
```javascript
const msg="Viršytas dienos paieškų limitas. Limitas atsinaujins rytoj."
// Mygtukas: "Grįžti į pradžią"
```

**Problema:** Naujas vartotojas pasiekia 200 paieškų/dieną limitą → gauna pranešimą. Mygtukas grąžina į pradžią — bet ten nieko naujo nėra. **Nėra aiškaus kito žingsnio.**

**Galimas pagerinimas:** Pasiūlyti išsaugoti watchlist arba instaliuoti PWA prieš einant.

---

### T6 — Grįžimas iš parduotuvės: pusiau veikianti funkcija

**Kodas:**
```javascript
document.addEventListener('visibilitychange',()=>{
  if(document.visibilityState!=='visible')return;
  const age=Date.now()-click.ts;
  if(age<800||age>30*60*1000)return; // too soon or stale
  showBackBanner(click.shop,click.q);
});
```

**Gerai:** Kai vartotojas grįžta iš parduotuvės per 30 minučių, matomas "Back to Goody" banner.

**Problema:** `visibilitychange` ne visada šaukiamas mobiliuosiuose (iOS Safari, PWA mode). Vartotojai, kurie atidaro nuorodą naujame tabe, negrįžta į Goody tab — banner nematomas.

**Trūksta:** "Ar radai geresnę kainą?" grįžimo apklausa arba "Ar nupirkai?" patvirtinimas.

---

### T7 — Balso paieška: tik Chrome

```javascript
const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
if(!SR){
  toast("Voice search not supported — use Chrome");
  return;
}
```

**Problema:** iOS Safari, Firefox, Samsung Internet — negalima naudoti balso paieškos. Šie naršyklė sudaro ~30% mobiliojo srauto. Toast klaida atsiranda TIK paspaudus mygtuką — vartotojas nemato perspėjimo iš anksto.

---

### T8 — Rusų kalba: neišbaigta

**Problema:** `LANGS` objektas turi: `en`, `lt`, `de`, `pl` — bet **ne `ru`**.

Rusų kalba matoma:
- Kai kuriose inline eilutėse: `{"lt":"...","ru":"Определяю продукт...","pl":"..."}[curLang]`
- Balso paieškos klaidų pranešimuose
- Camera error toasts
- identify-product server pusėje (palaiko `ru`)

**Bet LANGS objekte:** `curLang` gali būti `"ru"` tik jei vartotojas jį nustatė rankiniu būdu — o naršyklė auto-detect atpažįsta tik `["lt","de","pl","en"]`:
```javascript
return ["lt","de","pl","en"].includes(l)?l:"lt";
```

**Poveikis:** Rusiškai kalbantis vartotojas gauna pusiau LT / pusiau anglišką UX. `LANGS["ru"]` neegzistuoja → `LANGS.en` fallback. Dalis žinučių yra rusų, dalis anglų.

---

### T9 — Kainų istorija: dažnai "nauja"

**Kodas:**
```javascript
currentContainer.innerHTML=`...📊 ${noDataMsg}`;
// noDataMsg: "Kainų istorija kaupiama — pabandykite vėliau"
```

**Problema:** Kainų istorija matoma tik kai ta pati paieška buvo atlikta anksčiau. Daugumai produktų istorija bus "nauja" arba tuščia, ypač naujiems vartotojams.

**Poveikis:** Viena iš labiausiai pažadamų funkcijų (kainų trendai) dažnai nerodoma.

---

## ONBOARDING KOKYBĖ

**Gerai:**
- 3 žingsniai, 4 kalbos (LT/DE/PL/EN), skip galimybė
- Aiškios ikonos ir tekstai
- Rodyklės indikatorius progresui

**Trūksta:**
- Nėra realios demo nuotraukos ar video
- "Fotografuok kainą" — bet ne rodo KAIP (apšvietimas, atstumas, kampas)
- Onboarding neprašo kalbos pasirinkimo eksplicitiškai — auto-detect

---

## APIBENDRINIMAS: UX BALAI

| Sritis | Balas | Pastaba |
|---|---|---|
| Nuskaitymo patirtis | 7/10 | Gerai, bet per ilgas laukimas kai identify lėtas |
| "Nieko nerasta" | 8/10 | Geras — redagavimas + alternatyvos |
| Daugiakalbystė | 6/10 | RU neišbaigtas, tik LT/DE/PL/EN pilni |
| Loading state | 8/10 | Streaming rodomas progresyviai |
| Klaidos būsenos | 7/10 | Aiškios, bet rate limit "grįžk rytoj" šiurkštu |
| Grįžimo patirtis | 5/10 | Back banner nepastoviai veikia mobile |
| Kainų istorija | 5/10 | Dažnai tuščia naujiems vartotojams |
| Onboarding | 6/10 | Geras tekstas, trūksta vaizdinių pavyzdžių |
