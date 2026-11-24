import urllib.request
import re
import json

url = "https://www.gamerguides.com/the-legend-of-zelda-ocarina-of-time/maps/hyrule"
req = urllib.request.Request(url, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
    print(f"Fetched HTML length: {len(html)}")
    
    # Save a snippet
    with open(r"E:\WorkSpace\ZeldaOOTMAP\tools\gg_page.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Saved tools/gg_page.html")

    # Search for embedded json or props
    matches = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
    print(f"Inline scripts count: {len(matches)}")
    for i, s in enumerate(matches):
        if "markers" in s or "pins" in s or "locations" in s or "layers" in s or "map" in s:
            print(f"  Script #{i} length={len(s)} contains keywords!")
            if len(s) < 5000:
                print(s[:500])

except Exception as e:
    print("Error:", e)
