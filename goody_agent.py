"""
Goody Autonomous Agent
Runs nightly, finds bugs, fixes them with Claude API, pushes to GitHub.

Usage:
  python goody_agent.py            # run once now
  python goody_agent.py --schedule # run every night at 02:00
"""

import sys, io, os, re, json, time, subprocess, argparse, smtplib, traceback
from datetime import datetime
from email.mime.text import MIMEText

# ── UTF-8 stdout ──
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

os.environ.setdefault("SUPABASE_URL", "")
os.environ.setdefault("SUPABASE_KEY", "")

from dotenv import load_dotenv
load_dotenv()

import anthropic
import requests as _req

# ── CONFIG ──
ANTHROPIC_API_KEY  = os.getenv("ANTHROPIC_API_KEY", "")
EMAIL_FROM         = os.getenv("AGENT_EMAIL_FROM", "")
EMAIL_TO           = os.getenv("AGENT_EMAIL_TO", "giedrius.simonavicius@gmail.com")
EMAIL_PASS         = os.getenv("AGENT_EMAIL_PASS", "")
BACKEND_URL        = os.getenv("RENDER_EXTERNAL_URL", "https://goody-backend.onrender.com")
AGENT_MODEL        = "claude-opus-4-7"          # most capable for autonomous fixes
AGENT_MAX_TOKENS   = 4096
LOG_FILE           = "agent_log.txt"
ERR_FILE           = "agent_errors.txt"
REPORT_FILE        = "agent_report.txt"

TESTS = [
    ("price_validation", ["python", "test_price_validation.py"]),
    ("matching",         ["python", "test_matching.py"]),
]

SERVER_FILE = "server.py"

# ─────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────

def _ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log(msg, also_print=True):
    line = f"[{_ts()}] {msg}"
    if also_print:
        print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def log_err(msg, exc=None):
    line = f"[{_ts()}] ERROR: {msg}"
    if exc:
        line += "\n" + traceback.format_exc()
    print(line, file=sys.stderr)
    with open(ERR_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


# ─────────────────────────────────────────────
# TEST RUNNER
# ─────────────────────────────────────────────

def run_tests():
    """Returns dict: {name: {"passed": bool, "output": str}}"""
    results = {}
    for name, cmd in TESTS:
        log(f"Running {name} tests...")
        try:
            r = subprocess.run(
                cmd, capture_output=True, text=True, encoding="utf-8",
                errors="replace", timeout=60
            )
            output = r.stdout + r.stderr
            passed = r.returncode == 0 and "praejo" in output and "nepraejo" not in output
            results[name] = {"passed": passed, "output": output.strip()}
            log(f"  {name}: {'PASS' if passed else 'FAIL'}")
        except Exception as e:
            results[name] = {"passed": False, "output": str(e)}
            log_err(f"{name} test run failed", e)
    return results


# ─────────────────────────────────────────────
# LIVE HEALTH CHECK
# ─────────────────────────────────────────────

def check_live_health():
    issues = []
    try:
        r = _req.get(f"{BACKEND_URL}/api/health", timeout=10)
        if not r.ok:
            issues.append(f"Health endpoint returned {r.status_code}")
        else:
            d = r.json()
            log(f"  Live version: {d.get('version', '?')}")
    except Exception as e:
        issues.append(f"Health check failed: {e}")
    try:
        r = _req.post(
            f"{BACKEND_URL}/api/search",
            json={"query": "Philips skustuvas"},
            timeout=40,
        )
        if r.ok:
            d = r.json()
            n = len(d.get("results", []))
            log(f"  Live search 'Philips skustuvas': {n} results")
            if n == 0:
                issues.append("Live search returned 0 results for 'Philips skustuvas'")
        else:
            issues.append(f"Live search failed: {r.status_code}")
    except Exception as e:
        issues.append(f"Live search error: {e}")
    return issues


# ─────────────────────────────────────────────
# CLAUDE API — FIX CODE
# ─────────────────────────────────────────────

def read_server():
    with open(SERVER_FILE, encoding="utf-8") as f:
        return f.read()

def ask_claude_to_fix(test_name, test_output, live_issues, server_code):
    """Send failing test + server code to Claude, get back fixed code."""
    if not ANTHROPIC_API_KEY:
        log_err("ANTHROPIC_API_KEY not set — cannot call Claude")
        return None

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    live_section = ""
    if live_issues:
        live_section = f"\n\nLive health issues:\n" + "\n".join(f"- {i}" for i in live_issues)

    prompt = f"""You are an expert Python backend engineer fixing the Goody price-comparison app.

## Failing test: {test_name}
```
{test_output[-3000:]}
```
{live_section}

## Current server.py (relevant parts — full file is {len(server_code)} chars)
```python
{server_code[:12000]}
```

## Task
1. Identify what is failing and why.
2. Write the minimal fix — edit only what is necessary.
3. Return ONLY a JSON object in this exact format, no other text:

{{
  "analysis": "1-2 sentences explaining the root cause",
  "changes": [
    {{
      "old": "exact string to replace (must be unique in the file)",
      "new": "replacement string"
    }}
  ],
  "commit_message": "fix: short description (under 72 chars)"
}}

If there is nothing to fix, return {{"analysis": "No fix needed", "changes": [], "commit_message": ""}}.
"""

    log(f"  Asking Claude ({AGENT_MODEL}) for fix...")
    try:
        msg = client.messages.create(
            model=AGENT_MODEL,
            max_tokens=AGENT_MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )
        text = msg.content[0].text.strip()
        # Strip markdown code fences if present
        text = re.sub(r"^```(?:json)?\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
        return json.loads(text)
    except Exception as e:
        log_err("Claude API call failed", e)
        return None


# ─────────────────────────────────────────────
# APPLY FIXES
# ─────────────────────────────────────────────

def apply_fix(fix_data):
    """Apply the changes returned by Claude. Returns True if anything changed."""
    if not fix_data or not fix_data.get("changes"):
        return False

    code = read_server()
    applied = 0

    for ch in fix_data["changes"]:
        old = ch.get("old", "")
        new = ch.get("new", "")
        if not old:
            continue
        count = code.count(old)
        if count == 0:
            log(f"  WARNING: 'old' string not found in file — skipping change")
            continue
        if count > 1:
            log(f"  WARNING: 'old' string appears {count} times — skipping (ambiguous)")
            continue
        code = code.replace(old, new, 1)
        applied += 1
        log(f"  Applied change: {old[:60].strip()!r} -> {new[:60].strip()!r}")

    if applied:
        with open(SERVER_FILE, "w", encoding="utf-8") as f:
            f.write(code)
        log(f"  Wrote {applied} change(s) to {SERVER_FILE}")

    return applied > 0


# ─────────────────────────────────────────────
# GIT
# ─────────────────────────────────────────────

def git_commit_push(message):
    try:
        subprocess.run(["git", "add", SERVER_FILE], check=True, capture_output=True)
        diff = subprocess.run(["git", "diff", "--cached", "--stat"], capture_output=True, text=True)
        if not diff.stdout.strip():
            log("  Nothing staged — skipping commit")
            return False
        subprocess.run(["git", "commit", "-m", message], check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], check=True, capture_output=True)
        log(f"  Committed and pushed: {message}")
        return True
    except subprocess.CalledProcessError as e:
        log_err("git commit/push failed", e)
        return False


# ─────────────────────────────────────────────
# EMAIL REPORT
# ─────────────────────────────────────────────

def send_email_report(subject, body):
    if not EMAIL_FROM or not EMAIL_PASS or not EMAIL_TO:
        log("  Email not configured — writing report to file only")
        return
    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"]    = EMAIL_FROM
        msg["To"]      = EMAIL_TO
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as smtp:
            smtp.login(EMAIL_FROM, EMAIL_PASS)
            smtp.send_message(msg)
        log("  Email report sent")
    except Exception as e:
        log_err("Email send failed", e)


# ─────────────────────────────────────────────
# MAIN CYCLE
# ─────────────────────────────────────────────

def run_agent_cycle():
    start = time.time()
    log("=" * 60)
    log("GOODY AGENT — starting cycle")
    log("=" * 60)

    # 1. Run tests
    log("STEP 1: Running tests")
    test_results = run_tests()
    all_passed = all(v["passed"] for v in test_results.values())

    # 2. Live health
    log("STEP 2: Live health check")
    live_issues = check_live_health()

    fixes_applied = []
    committed = False
    claude_cost_note = ""

    # 3. If anything broken — ask Claude to fix
    if not all_passed or live_issues:
        log("STEP 3: Issues found — asking Claude for fix")
        server_code = read_server()

        for name, res in test_results.items():
            if res["passed"]:
                continue
            log(f"  Fixing: {name}")
            fix = ask_claude_to_fix(name, res["output"], live_issues, server_code)
            if not fix:
                continue
            log(f"  Analysis: {fix.get('analysis', '')}")
            if apply_fix(fix):
                fixes_applied.append(fix.get("commit_message", f"fix: {name}"))
                # Re-read after change for next iteration
                server_code = read_server()

        # Re-run tests after fixes
        if fixes_applied:
            log("STEP 3b: Re-running tests after fixes")
            test_results = run_tests()
            all_passed = all(v["passed"] for v in test_results.values())

            # Commit + push
            msg = fixes_applied[0] if len(fixes_applied) == 1 else f"fix: autonomous fixes ({len(fixes_applied)} issues)"
            msg += f" [agent {datetime.now().strftime('%Y-%m-%d')}]"
            committed = git_commit_push(msg)
            claude_cost_note = f"~${len(fixes_applied) * 0.03:.2f} (est. Claude API)"
    else:
        log("STEP 3: All tests pass, no fixes needed")

    # 4. Write report
    duration = round(time.time() - start, 1)
    test_lines = "\n".join(
        f"  {'OK' if v['passed'] else 'FAIL'}  {k}" for k, v in test_results.items()
    )
    fix_lines = "\n".join(f"  - {f}" for f in fixes_applied) or "  (none)"
    live_lines = "\n".join(f"  - {i}" for i in live_issues) or "  (all good)"

    report = f"""Goody Agent Report — {datetime.now().strftime('%Y-%m-%d %H:%M')}
{'=' * 50}

TEST RESULTS:
{test_lines}

LIVE HEALTH ISSUES:
{live_lines}

FIXES APPLIED:
{fix_lines}

COMMITTED TO GITHUB: {'Yes' if committed else 'No'}
CLAUDE API COST: {claude_cost_note or 'N/A (no fixes needed)'}
DURATION: {duration}s
"""

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)
    log("Report written to " + REPORT_FILE)
    print(report)

    # 5. Email
    status = "OK" if all_passed and not live_issues else "ISSUES"
    send_email_report(
        f"[Goody Agent] {status} — {datetime.now().strftime('%Y-%m-%d')}",
        report,
    )

    log("Agent cycle complete")
    return all_passed


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Goody autonomous agent")
    parser.add_argument("--schedule", action="store_true",
                        help="Run on schedule (nightly at 02:00)")
    parser.add_argument("--hour", type=int, default=2,
                        help="Hour (24h) to run scheduled job (default: 2)")
    args = parser.parse_args()

    if args.schedule:
        try:
            from apscheduler.schedulers.blocking import BlockingScheduler
        except ImportError:
            print("Install APScheduler: pip install apscheduler")
            sys.exit(1)

        sched = BlockingScheduler(timezone="Europe/Vilnius")
        sched.add_job(run_agent_cycle, "cron", hour=args.hour, minute=0)
        log(f"Scheduler started — will run daily at {args.hour:02d}:00 Vilnius time")
        log("Press Ctrl+C to stop")
        try:
            sched.start()
        except (KeyboardInterrupt, SystemExit):
            log("Scheduler stopped")
    else:
        success = run_agent_cycle()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
