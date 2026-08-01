"""
Mass recognition test runner.

Usage:
  python tests/mass_recognition/runner.py [--mode=mock] [--sample=N] [--seed=42]
  python tests/mass_recognition/runner.py --mode=mock --sample=50
  python tests/mass_recognition/runner.py --mode=mock          # full 500

Modes:
  mock   — recognition+matching against fixture data, NO live API calls (default)
  vision — live vision calls, mock store responses
  full   — live vision + live scrapers

Output files (tests/mass_recognition/results/):
  summary.json   — accuracy per category/difficulty/input_type
  failures.csv   — every failed case with expected vs actual + failure_type
  report.md      — markdown summary grouping top recurring failure patterns
"""
import argparse
import csv
import json
import os
import random
import sys
import time
from collections import defaultdict
from pathlib import Path

# Allow importing from goody-backend root
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

_HERE = Path(__file__).parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from config import (
    CACHE_DIR, CATEGORY_THRESHOLDS, FIXTURE_PATH, MAX_CONCURRENT,
    MAX_SCRAPER_CALLS, MAX_VISION_CALLS, THRESHOLD_OVERALL,
)

try:
    from server import is_relevant_result
except Exception as _e:
    print(f"[ERROR] Could not import is_relevant_result from server.py: {_e}", file=sys.stderr)
    sys.exit(2)

RESULTS_DIR = Path(__file__).parent / "results"

# ── per-product scoring ───────────────────────────────────────────────────────

def score_product(product: dict, mode: str = "mock") -> dict:
    """
    Run is_relevant_result() against all listings for one product.
    Returns a dict with pass/fail counts and failure details.
    """
    query = product["input_value"]
    category = product.get("expected_category", "unknown")
    difficulty = product.get("difficulty", "easy")
    input_type = product.get("input_type", "text")

    correct_listings   = product.get("correct_listings", [])
    incorrect_listings = product.get("incorrect_listings", [])
    must_not_match     = product.get("must_not_match", [])

    failures = []
    t0 = time.perf_counter()

    # ── correct_listings: must match ──────────────────────────────────────────
    correct_pass = correct_fail = 0
    for title in correct_listings:
        result = is_relevant_result(query, title)
        if result:
            correct_pass += 1
        else:
            correct_fail += 1
            failures.append({
                "product_id":   product["id"],
                "query":        query,
                "title":        title,
                "failure_type": "false_negative",
                "category":     category,
                "difficulty":   difficulty,
                "input_type":   input_type,
            })

    # ── incorrect_listings: must NOT match ────────────────────────────────────
    incorrect_pass = incorrect_fail = 0
    for title in incorrect_listings:
        result = is_relevant_result(query, title)
        if not result:
            incorrect_pass += 1
        else:
            incorrect_fail += 1
            failures.append({
                "product_id":   product["id"],
                "query":        query,
                "title":        title,
                "failure_type": "false_positive",
                "category":     category,
                "difficulty":   difficulty,
                "input_type":   input_type,
            })

    # ── must_not_match: critical — absolutely must not match ──────────────────
    critical_pass = critical_fail = 0
    for title in must_not_match:
        result = is_relevant_result(query, title)
        if not result:
            critical_pass += 1
        else:
            critical_fail += 1
            failures.append({
                "product_id":   product["id"],
                "query":        query,
                "title":        title,
                "failure_type": "critical_false_positive",
                "category":     category,
                "difficulty":   difficulty,
                "input_type":   input_type,
            })

    latency_ms = (time.perf_counter() - t0) * 1000

    total = correct_pass + correct_fail + incorrect_pass + incorrect_fail + critical_pass + critical_fail
    passed = correct_pass + incorrect_pass + critical_pass

    return {
        "id":            product["id"],
        "query":         query,
        "category":      category,
        "difficulty":    difficulty,
        "input_type":    input_type,
        "total":         total,
        "passed":        passed,
        "failed":        total - passed,
        "accuracy":      passed / total if total > 0 else 1.0,
        "correct_pass":  correct_pass,
        "correct_fail":  correct_fail,
        "incorrect_pass":incorrect_pass,
        "incorrect_fail":incorrect_fail,
        "critical_pass": critical_pass,
        "critical_fail": critical_fail,
        "latency_ms":    round(latency_ms, 2),
        "failures":      failures,
    }


# ── aggregate stats ───────────────────────────────────────────────────────────

def aggregate(results: list) -> dict:
    by_category  = defaultdict(lambda: {"total": 0, "passed": 0, "critical_fail": 0, "products": 0})
    by_difficulty= defaultdict(lambda: {"total": 0, "passed": 0, "products": 0})
    by_input_type= defaultdict(lambda: {"total": 0, "passed": 0, "products": 0})

    for r in results:
        cat  = r["category"]
        diff = r["difficulty"]
        inp  = r["input_type"]

        by_category[cat]["total"]        += r["total"]
        by_category[cat]["passed"]       += r["passed"]
        by_category[cat]["critical_fail"]+= r["critical_fail"]
        by_category[cat]["products"]     += 1

        by_difficulty[diff]["total"]     += r["total"]
        by_difficulty[diff]["passed"]    += r["passed"]
        by_difficulty[diff]["products"]  += 1

        by_input_type[inp]["total"]      += r["total"]
        by_input_type[inp]["passed"]     += r["passed"]
        by_input_type[inp]["products"]   += 1

    def pct(d):
        return {k: {**v, "accuracy_pct": round(v["passed"] / v["total"] * 100, 2) if v["total"] else 0}
                for k, v in d.items()}

    total_assertions = sum(r["total"] for r in results)
    total_passed     = sum(r["passed"] for r in results)

    return {
        "products_tested": len(results),
        "total_assertions": total_assertions,
        "total_passed": total_passed,
        "overall_accuracy_pct": round(total_passed / total_assertions * 100, 2) if total_assertions else 0,
        "by_category":   pct(by_category),
        "by_difficulty": pct(by_difficulty),
        "by_input_type": pct(by_input_type),
    }


# ── threshold check ───────────────────────────────────────────────────────────

def check_thresholds(summary: dict) -> list:
    """Returns list of (category, actual_pct, threshold_pct, PASS/FAIL) tuples."""
    checks = []
    by_cat = summary["by_category"]
    for cat, threshold in CATEGORY_THRESHOLDS.items():
        if cat not in by_cat:
            continue
        actual = by_cat[cat]["accuracy_pct"] / 100
        status = "PASS" if actual >= threshold else "FAIL"
        checks.append((cat, round(actual * 100, 2), round(threshold * 100, 2), status))

    overall_actual = summary["overall_accuracy_pct"] / 100
    overall_threshold = THRESHOLD_OVERALL
    checks.append(("OVERALL", round(overall_actual * 100, 2),
                   round(overall_threshold * 100, 2),
                   "PASS" if overall_actual >= overall_threshold else "FAIL"))
    return checks


# ── failure pattern extraction ────────────────────────────────────────────────

def extract_patterns(all_failures: list) -> list:
    """Group failures by type+category and return sorted by frequency."""
    patterns = defaultdict(lambda: {"count": 0, "examples": []})
    for f in all_failures:
        key = f"{f['failure_type']}::{f['category']}"
        patterns[key]["count"] += 1
        if len(patterns[key]["examples"]) < 5:
            patterns[key]["examples"].append(f)

    return sorted(
        [{"pattern": k, **v} for k, v in patterns.items()],
        key=lambda x: -x["count"]
    )


# ── report writing ────────────────────────────────────────────────────────────

def write_summary(summary: dict, out_dir: Path):
    (out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def write_failures_csv(all_failures: list, out_dir: Path):
    csv_path = out_dir / "failures.csv"
    if not all_failures:
        csv_path.write_text("No failures.\n", encoding="utf-8")
        return
    fields = ["product_id", "query", "title", "failure_type", "category", "difficulty", "input_type"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_failures)


def write_report(summary: dict, checks: list, patterns: list, elapsed: float,
                 sample_n: int, mode: str, out_dir: Path):
    lines = [
        "# Mass Recognition Test Report",
        "",
        f"**Mode:** `{mode}`  ",
        f"**Products tested:** {summary['products_tested']} (sample={sample_n})  ",
        f"**Elapsed:** {elapsed:.2f}s  ",
        f"**Total assertions:** {summary['total_assertions']}  ",
        f"**Overall accuracy:** {summary['overall_accuracy_pct']}%  ",
        "",
        "---",
        "",
        "## Threshold Check",
        "",
        "| Category | Actual % | Threshold % | Status |",
        "|---|---|---|---|",
    ]
    for cat, actual, threshold, status in checks:
        icon = "✅" if status == "PASS" else "❌"
        lines.append(f"| {cat} | {actual}% | {threshold}% | {icon} {status} |")

    lines += [
        "",
        "## Accuracy by Category",
        "",
        "| Category | Products | Assertions | Passed | Accuracy |",
        "|---|---|---|---|---|",
    ]
    for cat, v in sorted(summary["by_category"].items()):
        lines.append(
            f"| {cat} | {v['products']} | {v['total']} | {v['passed']} | {v['accuracy_pct']}% |"
        )

    lines += [
        "",
        "## Accuracy by Difficulty",
        "",
        "| Difficulty | Products | Assertions | Passed | Accuracy |",
        "|---|---|---|---|---|",
    ]
    for diff, v in sorted(summary["by_difficulty"].items()):
        lines.append(
            f"| {diff} | {v['products']} | {v['total']} | {v['passed']} | {v['accuracy_pct']}% |"
        )

    lines += [
        "",
        "## Accuracy by Input Type",
        "",
        "| Input Type | Products | Assertions | Passed | Accuracy |",
        "|---|---|---|---|---|",
    ]
    for inp, v in sorted(summary["by_input_type"].items()):
        lines.append(
            f"| {inp} | {v['products']} | {v['total']} | {v['passed']} | {v['accuracy_pct']}% |"
        )

    lines += ["", "## Top Failure Patterns", ""]
    for i, p in enumerate(patterns[:15], 1):
        ft, cat = p["pattern"].split("::")
        lines.append(f"### {i}. `{ft}` in category `{cat}` — {p['count']} failures")
        lines.append("")
        for ex in p["examples"][:3]:
            lines.append(f"- query=`{ex['query']}` → title=`{ex['title']}`")
        lines.append("")

    (out_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Mass recognition test runner")
    parser.add_argument("--mode",   default="mock",
                        choices=["mock", "vision", "full"])
    parser.add_argument("--sample", type=int, default=0,
                        help="Run a seeded random subset (0 = all)")
    parser.add_argument("--seed",   type=int, default=42)
    parser.add_argument("--max-vision-calls",  type=int, default=MAX_VISION_CALLS)
    parser.add_argument("--max-scraper-calls", type=int, default=MAX_SCRAPER_CALLS)
    args = parser.parse_args()

    # Load fixture
    products = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    print(f"Loaded {len(products)} products from fixture.")

    # Sample if requested
    if args.sample and args.sample < len(products):
        rng = random.Random(args.seed)
        products = rng.sample(products, args.sample)
        print(f"Sampled {len(products)} products (seed={args.seed}).")

    if args.mode in ("vision", "full"):
        print(f"[WARN] mode='{args.mode}' not fully implemented in this build — "
              f"live recognition uses mock query fallback. "
              f"Vision/scraper budget caps: {args.max_vision_calls}/{args.max_scraper_calls}")

    # Run
    t0 = time.perf_counter()
    all_results = []
    all_failures = []
    vision_calls = 0
    scraper_calls = 0

    for i, product in enumerate(products, 1):
        if args.mode in ("vision", "full") and product.get("input_type") == "photo":
            if vision_calls >= args.max_vision_calls:
                print(f"[BUDGET] Vision call cap reached ({args.max_vision_calls}). Skipping photo inputs.")
                continue
            vision_calls += 1
        if args.mode == "full":
            if scraper_calls >= args.max_scraper_calls:
                print(f"[BUDGET] Scraper call cap reached ({args.max_scraper_calls}).")
                break
            scraper_calls += 1

        result = score_product(product, mode=args.mode)
        all_results.append(result)
        all_failures.extend(result["failures"])

        if i % 50 == 0 or i == len(products):
            elapsed_so_far = time.perf_counter() - t0
            print(f"  [{i}/{len(products)}] elapsed={elapsed_so_far:.1f}s  failures so far={len(all_failures)}")

    elapsed = time.perf_counter() - t0

    # Aggregate
    summary = aggregate(all_results)
    summary["mode"] = args.mode
    summary["sample"] = args.sample or len(products)
    summary["seed"] = args.seed
    summary["elapsed_s"] = round(elapsed, 2)

    checks = check_thresholds(summary)
    patterns = extract_patterns(all_failures)

    # Write output
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    write_summary(summary, RESULTS_DIR)
    write_failures_csv(all_failures, RESULTS_DIR)
    write_report(summary, checks, patterns, elapsed, args.sample or len(products),
                 args.mode, RESULTS_DIR)

    # Print summary
    print(f"\n{'='*60}")
    print(f"Overall: {summary['overall_accuracy_pct']}%  "
          f"({summary['total_passed']}/{summary['total_assertions']} assertions)")
    print(f"{'='*60}")
    print("\nThreshold checks:")
    any_fail = False
    for cat, actual, threshold, status in checks:
        icon = "OK" if status == "PASS" else "FAIL"
        print(f"  [{icon}] {cat:20s}: {actual:5.1f}% (threshold {threshold:.0f}%)")
        if status == "FAIL":
            any_fail = True

    print(f"\nResults written to {RESULTS_DIR}/")
    print(f"Elapsed: {elapsed:.2f}s")

    if any_fail:
        print("\n[FAILED] One or more category thresholds not met")
        sys.exit(1)
    print("\n[PASSED] All thresholds met")


# ── pytest hook ───────────────────────────────────────────────────────────────

def test_mass_recognition_mock():
    """Pytest-compatible test — runs in mock mode, full 500 products."""
    import importlib.util
    products = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    all_results  = [score_product(p) for p in products]
    all_failures = [f for r in all_results for f in r["failures"]]
    summary = aggregate(all_results)
    checks  = check_thresholds(summary)

    # Write results for inspection even in CI
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    write_summary(summary, RESULTS_DIR)
    write_failures_csv(all_failures, RESULTS_DIR)
    patterns = extract_patterns(all_failures)
    write_report(summary, checks, patterns, 0.0, len(products), "mock", RESULTS_DIR)

    fails = [f"{cat}: {actual}% < {threshold}%" for cat, actual, threshold, s in checks if s == "FAIL"]
    assert not fails, f"Threshold failures: {fails}\nSee tests/mass_recognition/results/report.md"


if __name__ == "__main__":
    main()
