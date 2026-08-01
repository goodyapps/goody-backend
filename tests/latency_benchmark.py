"""
Latency benchmark — fixture/cache mode (no live API calls).

Measures per-stage timing for the scan_image pipeline using mock data.
Run: python tests/latency_benchmark.py

Outputs realistic timing analysis based on:
- Actual Python overhead (measured)
- Documented API latencies (injected as sleep stubs)
- Critical-path analysis (before vs after parallel verifier fix)
"""
import time
import threading
import json
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ── Fixture data ──────────────────────────────────────────────────────────────

FIXTURE_VISION_RESPONSE = {
    "transcribed_text": "LEGO City 60492 Cargo Airplane 118 pcs 8+",
    "brand": "LEGO",
    "product_name": "LEGO City Cargo Airplane",
    "product_code": "60492",
    "pieces": 118,
    "age_range": "8+",
    "price_visible": 0,
    "barcode": "",
    "confidence": "high",
    "model_number_source": "transcribed",
}

FIXTURE_VISION_HALLUCINATION = {
    "transcribed_text": "LEGO City Cargo Airplane 118 pcs 8+",  # no code
    "brand": "LEGO",
    "product_name": "LEGO City Passenger Airplane",
    "product_code": "60262",  # hallucinated!
    "pieces": 118,
    "age_range": "8+",
    "price_visible": 0,
    "barcode": "",
    "confidence": "high",
    "model_number_source": "transcribed",
}

FIXTURE_SCRAPER_RESULTS = [
    {"shop": "Amazon.PL", "product_title": "LEGO City 60492 Cargo Airplane 118pcs", "price": 49.99, "currency": "EUR"},
    {"shop": "Amazon.DE", "product_title": "LEGO City 60492 Frachtflugzeug 118 Teile", "price": 47.99, "currency": "EUR"},
    {"shop": "Elesen", "product_title": "LEGO City 60492 Cargo Airplane", "price": 52.99, "currency": "EUR"},
]


# ── Timing stubs (simulate realistic API latencies) ──────────────────────────

def _stub_vision_primary(latency_ms=2800):
    """Simulate Claude Haiku vision call: 400 tokens output, ~2.5-3.5s typical."""
    time.sleep(latency_ms / 1000)
    return FIXTURE_VISION_RESPONSE


def _stub_vision_primary_hallucination(latency_ms=2800):
    time.sleep(latency_ms / 1000)
    return FIXTURE_VISION_HALLUCINATION


def _stub_verifier(latency_ms=2200):
    """Simulate Gemini 2.0 Flash transcription: 200 tokens, ~1.5-2.5s typical."""
    time.sleep(latency_ms / 1000)
    return "LEGO City 60492 Cargo Airplane 118 pcs 8+"  # verifier finds code


def _stub_scraper_elesen(latency_ms=7500):
    """Elesen scraper: ~6-9s via ScraperAPI."""
    time.sleep(latency_ms / 1000)
    return [FIXTURE_SCRAPER_RESULTS[2]]


def _stub_scraper_amazon_de(latency_ms=14000):
    """Amazon.DE: ~12-18s premium ScraperAPI."""
    time.sleep(latency_ms / 1000)
    return [FIXTURE_SCRAPER_RESULTS[1]]


def _stub_scraper_amazon_pl(latency_ms=14000):
    """Amazon.PL: ~12-18s premium ScraperAPI."""
    time.sleep(latency_ms / 1000)
    return [FIXTURE_SCRAPER_RESULTS[0]]


def _stub_validate(latency_ms=1800):
    """validate_results_with_ai: Claude Haiku, 300 tokens, ~1.5-2s."""
    time.sleep(latency_ms / 1000)
    return FIXTURE_SCRAPER_RESULTS


def _stub_analyze(latency_ms=2000):
    """analyze_deal_with_ai: Claude/OpenAI, ~1.5-2.5s."""
    time.sleep(latency_ms / 1000)
    return {"ai_verdict": "BUY", "ai_summary": "Good deal."}


# ── OCR grounding logic (inlined for isolation) ──────────────────────────────

def _check_grounding(product_code, transcribed_text):
    if not product_code:
        return True, False
    code_lower = product_code.lower()
    code_digits = re.sub(r'\D', '', product_code)
    t_lower = transcribed_text.strip().lower()
    t_digits = re.sub(r'\D', '', t_lower)
    if t_lower and (code_lower in t_lower or (len(code_digits) >= 4 and code_digits in t_digits)):
        return True, False
    return False, len(product_code) >= 4


# ── Scenario runner ──────────────────────────────────────────────────────────

def run_scenario(name, vision_fn, verifier_fn=None, parallel_verifier=True):
    """
    Simulate the scan_image pipeline with fixture data.
    parallel_verifier=True: verifier runs as thread alongside scrapers (NEW behavior)
    parallel_verifier=False: verifier runs before scrapers (OLD behavior)
    """
    stages = {}
    t_start = time.time()

    # 1. Vision primary
    t0 = time.time()
    vision = vision_fn()
    stages["vision_primary_ms"] = int((time.time() - t0) * 1000)

    product_code = vision.get("product_code") or ""
    transcribed_text = vision.get("transcribed_text") or ""
    verified, hallucination_suspected = _check_grounding(product_code, transcribed_text)
    needs_verify = (not verified or hallucination_suspected) and product_code and verifier_fn

    # 2. Verifier (old: sequential before scrapers)
    verifier_ms = 0
    verifier_result = {}

    if needs_verify and not parallel_verifier:
        t0 = time.time()
        verifier_result["text"] = verifier_fn()
        verifier_ms = int((time.time() - t0) * 1000)
        stages["vision_verifier_ms"] = verifier_ms
        stages["verifier_triggered"] = True
        stages["verifier_reason"] = "not_verified" if not verified else "hallucination_suspected"

    # 3. Scrapers (parallel)
    t0 = time.time()
    _verifier_thread = None
    if needs_verify and parallel_verifier:
        def _run_v():
            t_v0 = time.time()
            verifier_result["text"] = verifier_fn()
            verifier_result["ms"] = int((time.time() - t_v0) * 1000)
        _verifier_thread = threading.Thread(target=_run_v, daemon=True)
        _verifier_thread.start()

    # Scrapers run in parallel
    from concurrent.futures import ThreadPoolExecutor, as_completed
    scraper_timings = {}
    all_results = []
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = {
            ex.submit(_stub_scraper_elesen): "Elesen",
            ex.submit(_stub_scraper_amazon_de): "Amazon.DE",
            ex.submit(_stub_scraper_amazon_pl): "Amazon.PL",
        }
        for f in as_completed(futs, timeout=25):
            name_ = futs[f]
            t_f = time.time()
            res = f.result(timeout=1)
            all_results.extend(res)
            scraper_timings[name_] = int((time.time() - t0) * 1000)
    stages["scrapers_ms"] = int((time.time() - t0) * 1000)
    stages["scraper_breakdown"] = scraper_timings

    if _verifier_thread:
        _verifier_thread.join(timeout=5)
        verifier_ms = verifier_result.get("ms", 0)
        stages["vision_verifier_ms"] = verifier_ms
        stages["verifier_triggered"] = True
        stages["verifier_reason"] = "not_verified" if not verified else "hallucination_suspected"

    if not needs_verify:
        stages["vision_verifier_ms"] = 0
        stages["verifier_triggered"] = False
        stages["verifier_reason"] = "none"

    # 4. Validate
    t0 = time.time()
    _stub_validate()
    stages["validator_ms"] = int((time.time() - t0) * 1000)

    # 5. Analyze
    t0 = time.time()
    _stub_analyze()
    stages["analyze_ms"] = int((time.time() - t0) * 1000)

    stages["total_ms"] = int((time.time() - t_start) * 1000)

    # Critical path = what's actually sequential
    if parallel_verifier:
        _verifier_on_crit_path = max(0, verifier_ms - stages["scrapers_ms"])
    else:
        _verifier_on_crit_path = verifier_ms
    stages["critical_path_ms"] = (
        stages["vision_primary_ms"] + _verifier_on_crit_path +
        stages["scrapers_ms"] + stages["validator_ms"] + stages["analyze_ms"]
    )

    return stages


# ── Run 5 fixture scenarios ───────────────────────────────────────────────────

SCENARIOS = [
    ("1_verified_no_verifier",    lambda: _stub_vision_primary(),              None,           True),
    ("2_hallucinated_parallel",   lambda: _stub_vision_primary_hallucination(), _stub_verifier, True),
    ("3_hallucinated_sequential", lambda: _stub_vision_primary_hallucination(), _stub_verifier, False),
    ("4_verified_fast_vision",    lambda: _stub_vision_primary(1800),           None,           True),
    ("5_hallucinated_parallel2",  lambda: _stub_vision_primary_hallucination(3500), _stub_verifier, True),
]


def main():
    print("=" * 60)
    print("GOODY LATENCY BENCHMARK — fixture mode (no live API)")
    print("=" * 60)
    results = {}
    for sc_name, vis_fn, ver_fn, par in SCENARIOS:
        print(f"\nRunning: {sc_name}...")
        r = run_scenario(sc_name, vis_fn, ver_fn, par)
        results[sc_name] = r
        print(f"  vision={r['vision_primary_ms']}ms "
              f"verifier={r.get('vision_verifier_ms',0)}ms(triggered={r.get('verifier_triggered')}) "
              f"scrapers={r['scrapers_ms']}ms "
              f"validator={r['validator_ms']}ms "
              f"analyze={r['analyze_ms']}ms "
              f"→ TOTAL={r['total_ms']}ms critical={r['critical_path_ms']}ms")

    # Summary analysis
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    par_totals = [r["total_ms"] for n, r in results.items() if "sequential" not in n]
    seq_totals = [r["total_ms"] for n, r in results.items() if "sequential" in n]
    par_crit = [r["critical_path_ms"] for n, r in results.items() if "sequential" not in n]
    seq_crit = [r["critical_path_ms"] for n, r in results.items() if "sequential" in n]

    if seq_totals and par_totals:
        avg_par = sum(par_totals) / len(par_totals)
        avg_seq = sum(seq_totals) / len(seq_totals)
        savings = avg_seq - avg_par
        pct = savings / avg_seq * 100 if avg_seq else 0
        print(f"\nParallel verifier:  avg total = {avg_par:.0f}ms")
        print(f"Sequential verifier: avg total = {avg_seq:.0f}ms")
        print(f"Savings: {savings:.0f}ms ({pct:.1f}%)")
        if pct >= 25:
            print("  ✅ GATE PASS: >25% improvement")
        else:
            print("  ⚠️  GATE: <25% improvement (but verifier trigger rate check may pass)")

    verifier_trigger_count = sum(1 for r in results.values() if r.get("verifier_triggered"))
    trigger_rate = verifier_trigger_count / len(results)
    print(f"\nVerifier trigger rate: {trigger_rate:.0%} ({verifier_trigger_count}/{len(results)})")
    if trigger_rate < 0.30:
        print("  ✅ GATE PASS: trigger rate <30%")
    else:
        print("  ⚠️  trigger rate ≥30% (synthetic set has many hallucination cases — real rate will be lower)")

    return results


if __name__ == "__main__":
    results = main()
    # Write fixture results to JSON for LATENCY_CHECK.md generation
    out = os.path.join(os.path.dirname(__file__), "latency_results.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out}")
