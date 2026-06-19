import sys, io, requests, re
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from server import _http, get_headers

url = "https://www.elesen.lt/paieska?q=LEGO%2076430%20Hogwarts"
resp = _http.get(url, headers=get_headers("lt"), timeout=5, allow_redirects=True)
html = resp.text

# Visi 76430 pasirod.
positions = [m.start() for m in re.finditer("76430", html)]
print(f"76430 pasirodymai: {len(positions)}")
for pos in positions:
    ctx = html[max(0,pos-150):pos+300]
    print(f"--- pos {pos} ---")
    print(ctx)
    print()

# Ar yra JSON produktu duomenys?
print("=== JSON in <script> tagus ===")
scripts = re.findall(r"<script[^>]*>(.*?)</script>", html, re.DOTALL)
print(f"<script> tagų skaičius: {len(scripts)}")
for i, s in enumerate(scripts):
    if len(s) > 100 and any(kw in s for kw in ["product", "price", "name", "lego", "76430"]):
        print(f"  Script #{i} ({len(s)} chars) — turi product/price/name/lego/76430:")
        print(f"  {s[:500]}")
        print()

# AJAX
ajax = re.findall(r'fetch\(["\'](/[^"\']+)["\']', html)
print("AJAX fetch() URL:", ajax[:10])

# Frameworkai
for fw in ["__vue", "nuxt", "next", "react", "angular", "window.config"]:
    if fw in html.lower():
        print(f"Framework: {fw}")
