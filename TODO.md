# TODO.md

## ⚠️ SVARBU: PO night-hardening DEPLOY — Render env vars

**BŪTINA nustatyti Render dashboard → Environment:**

- `DEBUG_API_KEY` — kad `/api/debug-html` veiktų su raktu. **Be šio env var endpoint grąžins 401 visiems, įskaitant tave.** Nustatyti stiprų atsitiktinį raktą (pvz. `openssl rand -hex 32`).
- `ALLOWED_ORIGINS` — frontend domenas CORS apsaugai (pvz. `https://goody-app.onrender.com`). Be šio CORS leidžia bet kurią svetainę (`"*"` numatytoji).

**Dabartinė situacija po merge:**
- `/api/debug-html` — uždarytas (401 visiems) ← GERAI saugumui, bet reikia rakto naudojimui
- CORS — vis dar `"*"` ← iki kol nustatysi `ALLOWED_ORIGINS`

---

## Monitoringas

- Periodiškai tikrinti sponsored detekciją — priklauso nuo Amazon CSS klasių (`.s-sponsored-label-info-icon`, `.puis-sponsored-label-text`), gali tyliai sulūžti jei Amazon pakeis HTML. Tikrinti Render logus: ar matosi `skip sponsored+competing-model` kai ieškoma LEGO set'ų Amazon.PL/DE.

## Žinomos problemos

- `is_relevant_result`: kai vartotojas ieško "LEGO 76430 lighting" (nori LED rinkinio), pavadinimas "LED Lighting Kit for LEGO 76430" atmestamas dėl `compat_patterns` ("for lego" title'e). Pre-existing, nekeičiama.
- Layer 2 live testai: Samsung RB34C600ESA, Bosch WAX32EH0, Nike, Adidas, Philips Airfryer → 0 rezultatų. Specifiniai modeliai kurių negrąžina aktyvios parduotuvės.
