"""
Mass recognition test — tests is_relevant_result() against 200+ fixture cases.
Uses no live API calls. All cases are from tests/fixtures/recognition_dataset.json.

Run from goody-backend root:
    python tests/recognition_mass_test.py

Or via pytest:
    pytest tests/recognition_mass_test.py -v

Results logged to RECOGNITION_TEST_RESULTS.md
"""
import sys, json, time
from pathlib import Path

# Allow importing from parent (goody-backend root)
sys.path.insert(0, str(Path(__file__).parent.parent))
from server import is_relevant_result

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "recognition_dataset.json"
RESULTS_MD = Path(__file__).parent.parent / "RECOGNITION_TEST_RESULTS.md"

def run_tests(cases: list) -> dict:
    total = 0
    passed = 0
    must_not_failures = []
    should_match_failures = []
    should_not_match_failures = []

    for case in cases:
        query = case["query"]
        case_id = case["id"]

        for title in case.get("must_not_match", []):
            total += 1
            result = is_relevant_result(query, title)
            if result:
                must_not_failures.append({
                    "id": case_id, "query": query,
                    "title": title, "type": "MUST_NOT_MATCH_FAILED"
                })
            else:
                passed += 1

        for title in case.get("should_match", []):
            total += 1
            result = is_relevant_result(query, title)
            if result:
                passed += 1
            else:
                should_match_failures.append({
                    "id": case_id, "query": query,
                    "title": title, "type": "SHOULD_MATCH_FAILED"
                })

        for title in case.get("should_not_match", []):
            total += 1
            result = is_relevant_result(query, title)
            if not result:
                passed += 1
            else:
                should_not_match_failures.append({
                    "id": case_id, "query": query,
                    "title": title, "type": "SHOULD_NOT_MATCH_FAILED"
                })

    return {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": passed / total * 100 if total > 0 else 0,
        "must_not_failures": must_not_failures,
        "should_match_failures": should_match_failures,
        "should_not_match_failures": should_not_match_failures,
    }


def write_results_md(results: dict, cases: list, elapsed: float):
    lines = [
        "# RECOGNITION_TEST_RESULTS.md",
        "",
        f"**Run date:** {time.strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"**Cases:** {len(cases)}  ",
        f"**Assertions:** {results['total']}  ",
        f"**Passed:** {results['passed']}  ",
        f"**Failed:** {results['failed']}  ",
        f"**Pass rate:** {results['pass_rate']:.1f}%  ",
        f"**Elapsed:** {elapsed:.2f}s  ",
        "",
        "---",
        "",
    ]

    if results["must_not_failures"]:
        lines.append("## ❌ CRITICAL: must_not_match failures (should NEVER match)")
        lines.append("")
        for f in results["must_not_failures"]:
            lines.append(f"- **[{f['id']}]** query=`{f['query']}` matched `{f['title']}`")
        lines.append("")

    if results["should_match_failures"]:
        lines.append("## ⚠️ should_match failures (false negatives)")
        lines.append("")
        for f in results["should_match_failures"]:
            lines.append(f"- **[{f['id']}]** query=`{f['query']}` did NOT match `{f['title']}`")
        lines.append("")

    if results["should_not_match_failures"]:
        lines.append("## ⚠️ should_not_match failures (false positives)")
        lines.append("")
        for f in results["should_not_match_failures"]:
            lines.append(f"- **[{f['id']}]** query=`{f['query']}` wrongly matched `{f['title']}`")
        lines.append("")

    if not results["must_not_failures"] and not results["should_match_failures"] and not results["should_not_match_failures"]:
        lines.append("## ✅ All tests passed")
        lines.append("")

    # Category breakdown
    categories = {}
    for c in cases:
        cat = c.get("category", "unknown")
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += 1

    lines.append("## Category breakdown")
    lines.append("")
    for cat, count in sorted(categories.items()):
        lines.append(f"- `{cat}`: {count} cases")
    lines.append("")

    RESULTS_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nResults written to {RESULTS_MD}")


def main():
    cases = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    print(f"Loaded {len(cases)} test cases from {FIXTURE_PATH}")

    t0 = time.time()
    results = run_tests(cases)
    elapsed = time.time() - t0

    print(f"\n{'='*60}")
    print(f"RESULTS: {results['passed']}/{results['total']} passed ({results['pass_rate']:.1f}%)")
    print(f"{'='*60}")

    if results["must_not_failures"]:
        print(f"\n❌ CRITICAL — {len(results['must_not_failures'])} must_not_match failures:")
        for f in results["must_not_failures"]:
            print(f"  [{f['id']}] query={f['query']!r} matched {f['title']!r}")

    if results["should_match_failures"]:
        print(f"\n⚠️  {len(results['should_match_failures'])} should_match failures (false negatives):")
        for f in results["should_match_failures"]:
            print(f"  [{f['id']}] query={f['query']!r} did NOT match {f['title']!r}")

    if results["should_not_match_failures"]:
        print(f"\n⚠️  {len(results['should_not_match_failures'])} should_not_match failures (false positives):")
        for f in results["should_not_match_failures"]:
            print(f"  [{f['id']}] query={f['query']!r} wrongly matched {f['title']!r}")

    write_results_md(results, cases, elapsed)
    print(f"\nElapsed: {elapsed:.2f}s")

    # Exit 1 if any must_not_match failures or pass rate below 95%
    if results["must_not_failures"]:
        print("\n💥 FAILED: must_not_match violations (100% required)")
        sys.exit(1)
    if results["pass_rate"] < 95.0:
        print(f"\n💥 FAILED: pass rate {results['pass_rate']:.1f}% < 95%")
        sys.exit(1)
    print("\n✅ PASSED")


# pytest-compatible test function
def test_recognition_mass():
    cases = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    results = run_tests(cases)

    assert not results["must_not_failures"], (
        f"must_not_match violations: {results['must_not_failures']}"
    )
    assert results["pass_rate"] >= 95.0, (
        f"Pass rate {results['pass_rate']:.1f}% < 95% required. "
        f"should_match failures: {len(results['should_match_failures'])}, "
        f"should_not_match failures: {len(results['should_not_match_failures'])}"
    )


if __name__ == "__main__":
    main()
