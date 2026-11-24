import subprocess
import os
import shutil

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
out_dir = r"C:\Users\Administrator\.gemini\antigravity\brain\9678aa79-6e05-40bd-9ad1-54a2d53260eb"

def take_shot(url, name):
    local_out = os.path.join(r"E:\WorkSpace\ZeldaOOTMAP", name)
    cmd = [
        edge_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        f"--screenshot={local_out}",
        "--window-size=1920,1080",
        "--virtual-time-budget=3000",
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(local_out):
        dest = os.path.join(out_dir, name)
        shutil.copy2(local_out, dest)
        print(f"Captured {name}: {os.path.getsize(dest)} bytes")
    else:
        print(f"Failed to capture {name}")

take_shot("http://localhost:8123/index.html?node=KokiriForest", "preview_kokiri_calibrated.png")
take_shot("http://localhost:8123/index.html?node=KakarikoVillage", "preview_kakariko_calibrated.png")
take_shot("http://localhost:8123/index.html?node=LakeHylia", "preview_lakehylia_calibrated.png")
take_shot("http://localhost:8123/index.html", "preview_hyrule_overview_v2.png")
