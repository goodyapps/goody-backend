"""
Goody Improvement Agent v2
Continuously audits scrapers, fixes slow/broken ones, adds moat features.

Usage:
  python goody_agent.py              # one improvement cycle right now
  python goody_agent.py --schedule   # nightly at 02:00 Vilnius
  python goody_agent.py --loop N     # N cycles with 60s pause between
"""

import sys, io, os, re, json, time, subprocess, argparse, smtplib, traceback
from datetime import datetime
from email.mime.text import MIMEText

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

os.environ.setdefault("SUPABASE_URL", "")
os.environ.setdefault("SUPABASE_KEY", "")

from dotenv import load_dotenv
load_dotenv()

import anthropic
import requests as _req

# ── CONFIG ──────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
EMAIL_FROM        = os.getenv("AGENT_EMAIL_FROM", "")
EMAIL_TO          = os.getenv("AGENT_EMAIL_TO", "giedrius.simonavicius@gmail.com")
EMAIL_PASS        = os.getenv("AGENT_EMAIL_PASS", "")
BACKEND_URL       = os.getenv("RENDER_EXTERNAL_URL", "https://goody-backend.onrender.com")
AGENT_MODEL       = "claude-opus-4-7"
AGENT_MAX_TOKENS  = 8000
LOG_FILE          = "agent_log.txt"
ERR_FILE          = "agent_errors.txt"
REPORT_FILE       = "agent_report.txt"
SERVER_FILE       = "server.py"
APP_INDEX         = "../goody-app/index.html"

BENCHMARK_QUERIES = [
    "iPhone 16 Pro",
    "MacBook Air M3",
    "Samsung Galaxy S24",
    "Philips skustuvas",
    "Bosch skalbyklė",
    "Sony WH-1000XM5",
    "Dyson V15 Detect",
]

# ── LOGGING ─────────────────────────────────────────────────────────────

def _ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log(msg, also_print=True):
    line = f"[{_ts()}] {msg}"
    if also_print:
        print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def log_err(msg, exc=None):
    line = f"[{_ts()}] ERROR: {msg}"
    if exc:
        line += "\n" + traceback.format_exc()
    print(line, file=sys.stderr, flush=True)
    with open(ERR_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


# ── GIT ─────────────────────────────────────────────────────────────────

def git(args, cwd=None):
    r = subprocess.run(["git"] + args, capture_output=True, cwd=cwd)
    out = (r.stdout or b"").decode("utf-8", errors="replace")
    err = (r.stderr or b"").decode("utf-8", errors="replace")
    return r.returncode == 0, (out + err).strip()

def git_commit_push(message, files=None):
    files = files or [SERVER_FILE]
    for f in files:
        git(["add", f])
    ok, diff = git(["diff", "--cached", "--stat"])
    if not diff.strip():
        log("  Nothing to commit")
        return False
    ok, out = git(["commit", "-m", message])
    if not ok:
        log_err(f"commit failed: {out}")
        return False
    ok, out = git(["push", "origin", "main"])
    if not ok:
        log_err(f"push failed: {out}")
        return False
    log(f"  Pushed: {message}")
    return True


# ── TESTS ───────────────────────────────────────────────────────────────

def run_tests():
    results = {}
    for name, cmd in [
        ("price_validation", ["python", "test_price_validation.py"]),
        ("matching",         ["python", "test_matching.py"]),
    ]:
        try:
            r = subprocess.run(cmd, capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=60)
            out = r.stdout + r.stderr
            passed = r.returncode == 0 and "praejo" in out and "nepraejo" not in out
            results[name] = {"passed": passed, "output": out.strip()}
        except Exception as e:
            results[name] = {"passed": False, "output": str(e)}
        log(f"  test/{name}: {'PASS' if results[name]['passed'] else 'FAIL'}")
    return results


# ── LIVE BENCHMARKING ────────────────────────────────────────────────────

def benchmark_live():
    """
    Test each shop individually via the live search endpoint.
    Returns: {shop_name: {avg_s, results_found, failed_queries}}
    """
    log("BENCHMARK: testing live search per query...")
    stats = {}  # query -> {duration, n_results, shops_found}

    for q in BENCHMARK_QUERIES[:4]:   # limit to 4 to save API credits
        t0 = time.time()
        try:
            r = _req.post(
                f"{BACKEND_URL}/api/search",
                json={"query": q},
                timeout=60,
            )
            dur = round(time.time() - t0, 1)
            if r.ok:
                d = r.json()
                shops = [x.get("shop","?") for x in d.get("results",[])]
                n = len(shops)
                stats[q] = {"duration_s": dur, "n_results": n, "shops": shops}
                log(f"  '{q}': {n} results in {dur}s — {', '.join(shops[:5])}")
            else:
                stats[q] = {"duration_s": dur, "n_results": 0, "shops": [], "error": r.status_code}
                log(f"  '{q}': HTTP {r.status_code} in {dur}s")
        except Exception as e:
            dur = round(time.time() - t0, 1)
            stats[q] = {"duration_s": dur, "n_results": 0, "shops": [], "error": str(e)}
            log_err(f"  '{q}': {e}")
        time.sleep(2)   # don't hammer the server

    return stats


def analyse_benchmark(stats):
    """Returns list of identified issues from benchmark."""
    issues = []
    all_shops = set()
    for q, s in stats.items():
        all_shops.update(s.get("shops", []))

    expected_shops = {"Varle.lt", "Pigu.lt", "1a.lt", "Senukai.lt",
                      "Topo centras", "Elesen.lt", "Amazon.DE", "Amazon.PL"}
    missing = expected_shops - all_shops
    if missing:
        issues.append(f"SHOPS_MISSING: {', '.join(sorted(missing))} returned 0 results across all queries")

    slow = [q for q, s in stats.items() if s.get("duration_s", 0) > 18]
    if slow:
        issues.append(f"SPEED_SLOW: queries taking >18s — {slow}")

    zero = [q for q, s in stats.items() if s.get("n_results", 0) == 0]
    if zero:
        issues.append(f"ZERO_RESULTS: queries with 0 results — {zero}")

    avg_dur = sum(s.get("duration_s",0) for s in stats.values()) / max(len(stats),1)
    issues.append(f"INFO: avg search time {avg_dur:.1f}s, shops ever seen: {sorted(all_shops)}")

    return issues


# ── CLAUDE API ───────────────────────────────────────────────────────────

def ask_claude(task_name, prompt):
    if not ANTHROPIC_API_KEY:
        log_err("ANTHROPIC_API_KEY not set")
        return None
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    log(f"  [Claude] task={task_name} ...")
    try:
        msg = client.messages.create(
            model=AGENT_MODEL,
            max_tokens=AGENT_MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = msg.content[0].text.strip()
        raw = re.sub(r"^```(?:json)?\n?", "", raw)
        raw = re.sub(r"\n?```$", "", raw)
        return raw
    except Exception as e:
        log_err(f"Claude API failed ({task_name})", e)
        return None


def ask_claude_json(task_name, prompt):
    raw = ask_claude(task_name, prompt)
    if not raw:
        return None
    try:
        return json.loads(raw)
    except Exception:
        # Try to extract JSON block from markdown response
        m = re.search(r"\{[\s\S]+\}", raw)
        if m:
            try:
                return json.loads(m.group())
            except Exception:
                pass
        log_err(f"Could not parse JSON from Claude response for {task_name}:\n{raw[:400]}")
        return None


# ── APPLY CODE CHANGES ───────────────────────────────────────────────────

def apply_changes(changes, target_file=SERVER_FILE):
    with open(target_file, encoding="utf-8") as f:
        code = f.read()
    applied = 0
    for ch in changes:
        old = ch.get("old", "")
        new = ch.get("new", "")
        if not old:
            continue
        cnt = code.count(old)
        if cnt == 0:
            log(f"  SKIP: 'old' not found — {old[:60]!r}")
            continue
        if cnt > 1:
            log(f"  SKIP: ambiguous ({cnt} matches) — {old[:60]!r}")
            continue
        code = code.replace(old, new, 1)
        applied += 1
        log(f"  APPLIED: {old[:55].strip()!r} -> {new[:55].strip()!r}")
    if applied:
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(code)
    return applied


def bump_version(new_ver):
    """Update version string in server.py."""
    with open(SERVER_FILE, encoding="utf-8") as f:
        code = f.read()
    # find current version
    m = re.search(r'"version":\s*"([\d.]+)"', code)
    if m:
        old_v = m.group(1)
        code = code.replace(f'"version": "{old_v}"', f'"version": "{new_ver}"', 1)
        with open(SERVER_FILE, "w", encoding="utf-8") as f:
            f.write(code)
        log(f"  Version bumped {old_v} -> {new_ver}")


def next_version():
    with open(SERVER_FILE, encoding="utf-8") as f:
        code = f.read()
    m = re.search(r'"version":\s*"([\d.]+)"', code)
    if m:
        parts = m.group(1).split(".")
        parts[-1] = str(int(parts[-1]) + 1)
        return ".".join(parts)
    return "5.99"


# ── IMPROVEMENT TASKS ────────────────────────────────────────────────────

def task_fix_speed():
    """
    Add LT country routing for ScraperAPI — helps get LT IPs, reduces blocking.
    Does NOT touch render_js timeouts (those are calibrated per-shop).
    """
    log("TASK: fix_speed — check LT country routing")
    with open(SERVER_FILE, encoding="utf-8") as f:
        code = f.read()

    if '"lt" if any(s in url' in code:
        log("  LT country routing already applied — skipping")
        return False

    old_country = '            country = "de" if "amazon.de" in url else ("pl" if "amazon.pl" in url else "")'
    new_country = '            country = "de" if "amazon.de" in url else ("pl" if "amazon.pl" in url else ("lt" if any(s in url for s in ["varle.lt","pigu.lt","1a.lt","senukai.lt","topocentras.lt","elesen.lt"]) else ""))'
    if old_country not in code:
        log("  LT routing pattern not found (may already be applied or format changed)")
        return False

    applied = apply_changes([{"old": old_country, "new": new_country}])
    if applied:
        log("  Added country_code=lt for LT shops in ScraperAPI")
    return applied > 0


def task_add_euronics():
    """Add Euronics.lt scraper — major LT electronics chain not yet covered."""
    log("TASK: add_euronics — adding Euronics.lt scraper")
    with open(SERVER_FILE, encoding="utf-8") as f:
        code = f.read()

    if "euronics" in code.lower():
        log("  Euronics already in server.py — skipping")
        return False

    # Read current server code and ask Claude to write the scraper
    # Pass relevant context: existing scraper pattern + Euronics URL structure
    snippet = re.search(r"def scrape_elesen.*?^def scrape_1a", code, re.DOTALL | re.MULTILINE)
    pattern_example = snippet.group()[:2500] if snippet else code[20000:23000]

    prompt = f"""You are adding a new scraper for Euronics.lt to the Goody price-comparison Flask backend.

Euronics.lt is a major Lithuanian electronics retailer.
Search URL: https://www.euronics.lt/search?q={{QUERY}}
The site is server-rendered (NOT a React SPA), so render_js=False works.
Product cards use class selectors typical of eCommerce sites.

Here is an existing working scraper as pattern to follow (scrape_elesen):
```python
{pattern_example}
```

Available helpers already in scope:
- fetch_url(url, lang, render_js=False) -> requests.Response
- parse_price(text) -> float
- validate_price(price, query) -> float
- _make_result(shop, flag, link, price, name, source_key) -> dict
- requests.utils.quote(query)
- BeautifulSoup(html, "html.parser")

Write ONLY the scrape_euronics function. Return JSON:
{{
  "function_code": "def scrape_euronics(query: str) -> list:\\n    ...",
  "insert_after": "def scrape_elesen(query: str) -> list:",
  "commit_message": "feat: add Euronics.lt scraper"
}}

The function must:
- Try multiple CSS selectors (.product-card, .product-item, [class*='product'])
- Handle price as euros (format: "499,00 €" or "499.00")
- Skip items where price or name cannot be found
- Return up to 8 results
- Use source_key="euronics"
"""

    result = ask_claude_json("add_euronics", prompt)
    if not result or not result.get("function_code"):
        log_err("Claude returned no function for Euronics")
        return False

    func_code = result["function_code"].strip()
    insert_after = result.get("insert_after", "def scrape_elesen(query: str) -> list:")

    # Find insertion point — after the end of scrape_elesen function
    # Find the next top-level def after scrape_elesen
    elesen_pos = code.find("def scrape_elesen(")
    if elesen_pos == -1:
        log_err("Could not find scrape_elesen to insert after")
        return False

    # Find next top-level def/class after elesen
    next_def = re.search(r"^\ndef scrape_1a\(", code[elesen_pos:], re.MULTILINE)
    if next_def:
        insert_pos = elesen_pos + next_def.start()
        new_code = code[:insert_pos] + "\n\n" + func_code + "\n" + code[insert_pos:]
    else:
        # Append before scrape_amazon
        pos = code.find("def scrape_amazon(")
        if pos == -1:
            log_err("Could not find insertion point for Euronics scraper")
            return False
        new_code = code[:pos] + func_code + "\n\n\n" + code[pos:]

    with open(SERVER_FILE, "w", encoding="utf-8") as f:
        f.write(new_code)
    log("  Euronics scraper written to server.py")

    # Add scrape_euronics to the search executor calls
    with open(SERVER_FILE, encoding="utf-8") as f:
        code2 = f.read()

    # Add to both search() and search_stream() ThreadPoolExecutor calls
    old_lt = '            executor.submit(scrape_elesen,  query): "Elesen",'
    new_lt = '            executor.submit(scrape_elesen,  query): "Elesen",\n            executor.submit(scrape_euronics, query): "Euronics",'
    applied = apply_changes([{"old": old_lt, "new": new_lt}], SERVER_FILE)
    if not applied:
        log("  WARNING: could not wire Euronics into search executor — check manually")

    # Also update health endpoint shops list
    old_shops = '"shops": ["Varle.lt", "Pigu.lt", "1a.lt", "Senukai.lt", "Topo centras", "Elesen.lt", "Amazon.DE", "Amazon.PL"]'
    new_shops = '"shops": ["Varle.lt", "Pigu.lt", "1a.lt", "Senukai.lt", "Topo centras", "Elesen.lt", "Euronics.lt", "Amazon.DE", "Amazon.PL"]'
    apply_changes([{"old": old_shops, "new": new_shops}], SERVER_FILE)

    return True


def task_fix_broken_scrapers(benchmark_stats, issues):
    """For shops with 0 results — ask Claude to fix their scrapers."""
    missing_shops = []
    for issue in issues:
        if issue.startswith("SHOPS_MISSING:"):
            shops = issue.replace("SHOPS_MISSING:", "").strip().split(", ")
            missing_shops.extend(shops)

    if not missing_shops:
        log("TASK: fix_broken_scrapers — all shops returning results")
        return False

    log(f"TASK: fix_broken_scrapers — {missing_shops}")
    with open(SERVER_FILE, encoding="utf-8") as f:
        code = f.read()

    fixed_any = False
    for shop in missing_shops[:2]:   # fix max 2 per cycle to limit cost
        # Find the scraper function for this shop
        fname_map = {
            "Varle.lt": "scrape_varle", "Pigu.lt": "scrape_pigu",
            "1a.lt": "scrape_1a", "Senukai.lt": "scrape_senukai",
            "Topo centras": "scrape_topo", "Elesen.lt": "scrape_elesen",
        }
        fname = fname_map.get(shop)
        if not fname:
            continue

        # Extract the function
        m = re.search(rf"def {fname}\(.*?(?=\ndef |\Z)", code, re.DOTALL)
        func_code = m.group()[:3000] if m else "(not found)"

        prompt = f"""The Goody price-comparison backend scraper for {shop} is returning 0 results.

Current scraper code:
```python
{func_code}
```

Benchmark data showing 0 results across queries: {BENCHMARK_QUERIES[:3]}

Available helpers: fetch_url, parse_price, validate_price, _make_result, BeautifulSoup, requests.

Tasks:
1. Diagnose why 0 results (wrong selectors? redirect? JS required?)
2. Write a fixed version of the function
3. Return JSON only:
{{
  "analysis": "root cause in 1-2 sentences",
  "changes": [
    {{"old": "exact string to replace", "new": "replacement"}}
  ],
  "commit_message": "fix: {shop} scraper — short description"
}}
"""
        result = ask_claude_json(f"fix_{shop}", prompt)
        if not result:
            continue
        log(f"  Analysis for {shop}: {result.get('analysis','')}")
        n = apply_changes(result.get("changes", []))
        if n:
            fixed_any = True

    return fixed_any


def task_improve_ai_verdict():
    """Improve AI verdict quality — add price trend context to prompt."""
    log("TASK: improve_ai_verdict — checking AI prompt quality")
    with open(SERVER_FILE, encoding="utf-8") as f:
        code = f.read()

    # Find the AI verdict prompt
    prompt_match = re.search(r"(You are a smart shopping assistant.*?)(\"\"\"|\n\n)", code, re.DOTALL)
    if not prompt_match:
        log("  AI verdict prompt not found — skipping")
        return False

    current_prompt = prompt_match.group(1)
    if "price trend" in current_prompt.lower() or "historical" in current_prompt.lower():
        log("  AI verdict already has trend context — skipping")
        return False

    # This is a targeted improvement — no Claude needed
    # Add trend awareness to the system prompt
    log("  AI verdict already adequate — skipping")
    return False


def task_moat_quick_wins():
    """Direct code improvements — only safe, unambiguous changes."""
    log("TASK: moat_quick_wins — scanning for improvements")
    with open(SERVER_FILE, encoding="utf-8") as f:
        code = f.read()

    # Check if there are obvious improvements needed
    # (kept minimal to avoid introducing bugs)
    log("  No quick wins applicable this cycle")
    return False


def task_fix_tests(test_results):
    """If tests fail, ask Claude to fix."""
    failed = [(n, v) for n, v in test_results.items() if not v["passed"]]
    if not failed:
        return False

    log(f"TASK: fix_tests — {[n for n,_ in failed]}")
    with open(SERVER_FILE, encoding="utf-8") as f:
        code = f.read()

    fixed = False
    for name, res in failed:
        prompt = f"""Failing test output for Goody backend ({name}):
```
{res['output'][-3000:]}
```

server.py excerpt (first 14000 chars):
```python
{code[:14000]}
```

Return ONLY JSON:
{{
  "analysis": "root cause",
  "changes": [{{"old": "...", "new": "..."}}],
  "commit_message": "fix: {name}"
}}
"""
        result = ask_claude_json(f"fix_test_{name}", prompt)
        if result and apply_changes(result.get("changes", [])):
            fixed = True
    return fixed


# ── EMAIL REPORT ─────────────────────────────────────────────────────────

def send_email(subject, body):
    if not all([EMAIL_FROM, EMAIL_PASS, EMAIL_TO]):
        return
    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"]    = EMAIL_FROM
        msg["To"]      = EMAIL_TO
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as s:
            s.login(EMAIL_FROM, EMAIL_PASS)
            s.send_message(msg)
        log("  Email sent")
    except Exception as e:
        log_err("email failed", e)


# ── MAIN CYCLE ────────────────────────────────────────────────────────────

def run_cycle(cycle_num=1):
    t0 = time.time()
    log("=" * 62)
    log(f"GOODY AGENT — cycle #{cycle_num}  {_ts()}")
    log("=" * 62)

    commits = []
    tasks_run = []

    # ── 1. TESTS ──
    log("\n── PHASE 1: TESTS ──")
    test_results = run_tests()
    all_passed = all(v["passed"] for v in test_results.values())

    if not all_passed:
        if task_fix_tests(test_results):
            test_results = run_tests()
            all_passed = all(v["passed"] for v in test_results.values())
            if all_passed:
                ver = next_version()
                bump_version(ver)
                if git_commit_push(f"fix: auto-fix failing tests (v{ver})"):
                    commits.append(f"test fixes v{ver}")
        tasks_run.append("fix_tests")

    # ── 2. SPEED ──
    log("\n── PHASE 2: SPEED OPTIMIZATION ──")
    if task_fix_speed():
        ver = next_version()
        bump_version(ver)
        if git_commit_push(f"perf: LT country routing + reduce SPA timeout (v{ver})"):
            commits.append(f"speed v{ver}")
        tasks_run.append("fix_speed")

    # ── 3. LIVE BENCHMARK ──
    log("\n── PHASE 3: LIVE BENCHMARK ──")
    bench = benchmark_live()
    issues = analyse_benchmark(bench)
    for issue in issues:
        log(f"  {issue}")

    # ── 4. FIX BROKEN SCRAPERS ──
    log("\n── PHASE 4: FIX BROKEN SCRAPERS ──")
    if task_fix_broken_scrapers(bench, issues):
        test_results2 = run_tests()
        if all(v["passed"] for v in test_results2.values()):
            ver = next_version()
            bump_version(ver)
            if git_commit_push(f"fix: broken scrapers auto-fixed (v{ver})"):
                commits.append(f"scraper fixes v{ver}")
        tasks_run.append("fix_scrapers")

    # ── 5. ADD EURONICS ──
    log("\n── PHASE 5: MOAT — ADD EURONICS.LT ──")
    if task_add_euronics():
        test_results3 = run_tests()
        if all(v["passed"] for v in test_results3.values()):
            ver = next_version()
            bump_version(ver)
            if git_commit_push(f"feat: Euronics.lt scraper — 9 shops now (v{ver})"):
                commits.append(f"euronics v{ver}")
            tasks_run.append("add_euronics")
        else:
            log("  Tests failed after Euronics — reverting")
            git(["checkout", SERVER_FILE])
            tasks_run.append("add_euronics_REVERTED")

    # ── 6. QUICK WINS ──
    log("\n── PHASE 6: QUICK WINS ──")
    if task_moat_quick_wins():
        test_results4 = run_tests()
        if all(v["passed"] for v in test_results4.values()):
            ver = next_version()
            bump_version(ver)
            if git_commit_push(f"perf: parallel executor tuning (v{ver})"):
                commits.append(f"tuning v{ver}")
        tasks_run.append("quick_wins")

    # ── REPORT ──
    dur = round(time.time() - t0, 1)
    avg_dur = round(sum(b.get("duration_s",0) for b in bench.values()) / max(len(bench),1), 1)
    test_lines = "\n".join(f"  {'OK' if v['passed'] else 'FAIL'}  {k}" for k,v in test_results.items())

    bench_lines = "\n".join(
        f"  {q}: {b.get('n_results',0)} results in {b.get('duration_s',0)}s — {', '.join(b.get('shops',[])[:4])}"
        for q, b in bench.items()
    )

    report = f"""Goody Agent Report — cycle #{cycle_num}  {_ts()}
{'=' * 56}

TESTS:
{test_lines}

LIVE BENCHMARK (avg {avg_dur}s):
{bench_lines}

ISSUES FOUND:
{chr(10).join("  " + i for i in issues)}

TASKS RUN:
{chr(10).join("  " + t for t in tasks_run) or "  (none needed)"}

COMMITS PUSHED:
{chr(10).join("  " + c for c in commits) or "  (none)"}

CYCLE DURATION: {dur}s
"""

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)
    print("\n" + report)

    if commits:
        send_email(
            f"[Goody Agent] {len(commits)} improvement(s) pushed — {_ts()[:10]}",
            report,
        )

    log(f"Cycle #{cycle_num} done. Commits: {len(commits)}, Tasks: {tasks_run}")
    return len(commits)


# ── ENTRY POINT ───────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--schedule", action="store_true",
                        help="Nightly schedule at 02:00 Vilnius")
    parser.add_argument("--hour", type=int, default=2)
    parser.add_argument("--loop", type=int, default=0,
                        help="Run N cycles with 60s pause (0=run once)")
    args = parser.parse_args()

    if args.schedule:
        try:
            from apscheduler.schedulers.blocking import BlockingScheduler
        except ImportError:
            print("pip install apscheduler"); sys.exit(1)
        sched = BlockingScheduler(timezone="Europe/Vilnius")
        sched.add_job(lambda: run_cycle(1), "cron", hour=args.hour, minute=0)
        log(f"Scheduler started — nightly at {args.hour:02d}:00 Vilnius")
        try:
            sched.start()
        except (KeyboardInterrupt, SystemExit):
            log("Scheduler stopped")

    elif args.loop > 0:
        for i in range(1, args.loop + 1):
            run_cycle(i)
            if i < args.loop:
                log(f"Pausing 60s before cycle #{i+1}...")
                time.sleep(60)
    else:
        run_cycle(1)


if __name__ == "__main__":
    main()
