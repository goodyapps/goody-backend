# Recognition Debug — Screen-Photo "Not Recognized" Case
**Date:** 2026-06-19  
**Symptom:** Photo of laptop screen showing "Šaldytuvas Samsung RB34C600ESA kaina nuo 389,00 €" → "Product not recognized"

---

## 1. Which endpoint actually ran?

The "Price photo" scan button triggers this chain:

```
[Camera shutter] snapOrSearch()
  → captureFrame()          (index.html:2762)
  → runIdentify()           (index.html:2855)
  → POST /api/identify-product
  → if data.error || !data.product_name  → _showConfirmError()  ← "Not recognized" panel
```

**`/api/scan-image` was NOT called in this flow.** `runScan()` (which calls `/api/scan-image`) is a different function used in a different context. The "Price photo" shutter always goes through `/api/identify-product`.

---

## 2. The exact vision prompt sent to Claude Haiku AND Gemini 2.0 Flash

Both models receive the **same prompt** simultaneously:

```
You are a product identification assistant for a price comparison app.
The image may be: a physical product label, product packaging, a photo of a shop shelf, OR a screenshot/photo of a webpage or price comparison site.
In ALL cases extract the product name and brand from any visible text.

Respond ONLY with valid JSON (no markdown, no explanation):
{"brand":"","product_name":"","model":"","key_specs":"","search_query":"","confidence":"high|medium|low","scanned_price":null}

- brand: manufacturer name (e.g. "Mobvoi", "Lenovo", "Apple", "LEGO", "Nutella")
- product_name: full product name in English — read it from ANY text visible in the image
  (label, webpage title, heading, product card)
- model: ONLY include model identifiers that are EXPLICITLY printed/shown as text in the image.
  Do NOT guess, infer, or invent model names. If model name is not clearly visible, leave blank.
- key_specs: key differentiating specs if visible (e.g. "16GB 512GB", "750g", null)
- search_query: 2-4 word Amazon search query. Brand + confirmed model ONLY. If model is uncertain
  or not clearly visible, use just brand + product category. NO storage sizes unless they ARE
  the model name.
- confidence: "high"=text clearly readable, "medium"=partially visible, "low"=mostly inferred
- scanned_price: numeric price in EUR if a price tag/label is visible, else null
IMPORTANT: Even if this is a screenshot of a webpage, still extract the product name from the
visible text. Do not refuse. NEVER invent product names or model suffixes not visible in the image.
```

**Assessment:** The prompt explicitly covers "screenshot/photo of a webpage." The intent is correct. The problem is not the prompt's coverage of use cases — it is the **physical image quality** delivered to the AI.

---

## 3. Exact "not recognized" condition in the code

**Backend** (`/api/identify-product`, line 6757):
```python
if not product_name and not model_code:
    return jsonify({"error": "product_not_recognized", "confidence": "low"}), 422
```
Triggers when **both** `product_name` AND `model` are empty strings after both models have run.

**Frontend** (`runIdentify()`, line 2867):
```javascript
if (data.error || !data.product_name) {
    _showConfirmError();
}
```
Also triggers if product_name is empty even without HTTP error.

**What specifically happened:**
1. Both Gemini 2.0 Flash and Claude Haiku returned `product_name: ""`
2. OCR fallback ran (Gemini re-reads raw text from the same blurry image)
3. OCR also failed to produce `product_name`
4. Backend returned 422 `{"error":"product_not_recognized"}`
5. Frontend showed the "Not recognized" panel

---

## 4. OCR fallback — does it exist?

Yes. The OCR fallback (`_call_gemini_ocr()`) is the **third stage** in `/api/identify-product`:

```python
# Stage 1: Gemini 2.0 Flash (parallel)
# Stage 2: Claude Haiku (parallel)
# Winner selected by _score()

# Stage 3: OCR fallback — only fires if winner has no product_name
if not vision.get("product_name"):
    ocr_text = _call_gemini_ocr()   # Gemini reads raw visible text
    if ocr_text:
        # Stage 4: Claude Haiku parses OCR text → structured JSON
        parse_resp = claude.messages.create(...)
```

The OCR prompt:
```
Read ALL brand names, product names, and model numbers visible in this image.
Output only the text you can read — no explanations, no JSON, just the raw text lines.
```

**This fallback is correct in design** — but it sends the **same blurry image** to Gemini. If Gemini couldn't read the small screen text in stage 1, it likely can't read it in stage 3 either.

---

## 5. Does the prompt handle screens? Yes, but with a gap

**What the prompt says:**
> "The image may be... a screenshot/photo of a webpage or price comparison site."

**What the AI actually receives in this case:**
- A photo of a laptop sitting on a desk
- The laptop screen takes up ~30% of the image area
- The browser with the product page takes up part of that screen
- The text "Šaldytuvas Samsung RB34C600ESA kaina nuo 389,00 €" is rendered in a small font within the browser window

**The gap:** The prompt says "screenshot/photo of a webpage" — but this image is a **photo of a physical scene that CONTAINS a screen**. The AI sees: room environment → laptop → screen → browser → product text.

This is different from:
- A direct screenshot (AI gets full-resolution webpage)
- A close-up photo of the screen text

**The AI's challenge:** To read the product name, it must mentally "zoom into" the screen within the scene, then "zoom into" the browser, then "zoom into" the product title text — which, at the captured resolution, may be only 20-30 pixels tall.

**The prompt has no instruction** for this "screen within a scene" case. It says "read text from ANY text visible" but doesn't say "if you see a screen or monitor in the image, focus on the content of that screen and read it."

---

## Hypothesis: Why it failed

**Primary cause:** The captured JPEG frame at 1280×720 (or similar) resolution, taken from ~1-2 meters away from the laptop, renders the product title text at roughly 15-25 pixels height. At this resolution, AI vision models (which process images at 512×512 or 768×768 patches) cannot reliably distinguish individual characters in small text.

**Secondary cause:** The prompt does not instruct the AI to specifically focus on screen content when a monitor/laptop is visible in the scene. The AI sees the whole room scene and may not zoom in on the screen.

**Why OCR also failed:** `_call_gemini_ocr()` sends the same low-resolution image. "Read ALL brand names and product names visible" — if the text is below the minimum readable resolution, neither structured nor OCR extraction works.

**Confirmation:** If the user had taken a close-up photo of just the screen showing the same product name, `/api/identify-product` would almost certainly succeed (the prompt explicitly handles webpage screenshots).

---

## Proposed fix: Improve prompt for "screen in scene" case

**Option A — Prompt addition (quick, no code change in backend):**

Add this instruction to `_VISION_PROMPT`:

```
SCREEN/MONITOR CASE: If the image shows a laptop, desktop monitor, phone, or TV screen as part of a physical scene, focus on the CONTENT of the screen. Read any product names, model numbers, or prices displayed on the screen, even if the text appears small. Ignore the physical environment (desk, hands, room) and focus on what is shown ON the screen.
```

This directly addresses the "photo of a screen" case without changing the general structure.

**Option B — Frontend improvement (better UX for the failure case):**

When "Not recognized" is returned, instead of just showing tips, show an **editable text field** pre-populated with whatever the AI partially returned (even just "Samsung" or "šaldytuvas"), with a "Search for this →" button. Currently the error panel has no input — the user must go back to home and type manually.

This is especially important because the user clearly SAW the product name ("Samsung RB34C600ESA") — they just need a way to type it quickly.

**Option C — Partial result rescue:**

If `product_name` is empty but `brand` is non-empty (AI recognized "Samsung" but not the model), do NOT return 422. Instead, return the partial result and show it in the confirm panel with a yellow warning: "Brand recognized — model unclear. Edit the query below."

Currently: `if not product_name and not model_code → 422`.  
Proposed: `if not product_name and not model_code and not brand → 422` (brand alone is enough to offer a search).

---

## Summary

| Question | Answer |
|---|---|
| Which endpoint ran? | `/api/identify-product` (not `/api/scan-image`) |
| Does prompt handle screens? | Yes — explicitly mentions screenshots/webpages |
| Missing from prompt | No instruction to "zoom into" screen within physical scene |
| "Not recognized" condition | Both `product_name` AND `model` empty after 3 stages |
| OCR fallback? | Exists, but uses same blurry image — also failed |
| Root cause | Text too small in image (screen photographed from distance) + no "focus on screen content" instruction |
| Quick fix | Add screen/monitor sentence to `_VISION_PROMPT` |
| UX fix | Editable text field in "Not recognized" panel so user can type what they see |
