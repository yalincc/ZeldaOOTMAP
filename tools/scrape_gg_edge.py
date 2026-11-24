import subprocess
import os

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
url = "https://www.gamerguides.com/the-legend-of-zelda-ocarina-of-time/maps/hyrule"
out_html = r"E:\WorkSpace\ZeldaOOTMAP\tools\gg_rendered.html"

cmd = [
    edge_path,
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--dump-dom",
    url
]

res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
print("Return code:", res.returncode)
print("Output length:", len(res.stdout))
if len(res.stdout) > 1000:
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(res.stdout)
    print("Saved rendered DOM to tools/gg_rendered.html")
else:
    print("Stderr:", res.stderr[:500])
