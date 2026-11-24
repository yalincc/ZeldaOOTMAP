import re
import json

with open(r"E:\WorkSpace\ZeldaOOTMAP\tools\gg_rendered.html", "r", encoding="utf-8") as f:
    html = f.read()

print("HTML length:", len(html))

# Look for script tags
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
print("Scripts found:", len(scripts))
for i, s in enumerate(scripts):
    s_strip = s.strip()
    if len(s_strip) > 0:
        print(f"Script #{i} length={len(s_strip)}")
        if any(k in s_strip.lower() for k in ["marker", "location", "point", "coord", "map"]):
            print(f"  First 300 chars of script #{i}:")
            print(s_strip[:300])

# Look for data- attributes or JSON in div
matches = re.findall(r'data-[\w\-]+="[^"]*"', html)
print("data- attributes count:", len(matches))
for m in matches[:10]:
    if len(m) < 200:
        print(" ", m)

# Search for any leaflet / mapbox / custom map config
if "map" in html.lower():
    lines = [line.strip() for line in html.split("\n") if "map" in line.lower()]
    print("Lines mentioning 'map':", len(lines))
    for l in lines[:10]:
        print("  map line:", l[:150])
