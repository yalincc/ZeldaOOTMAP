import subprocess
import os
import shutil

# To capture with calibration mode active, we can quickly write a tiny shot that clicks or calls toggleCalibrationMode
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
local_out = r"E:\WorkSpace\ZeldaOOTMAP\preview_cal_active.png"
dest = r"C:\Users\Administrator\.gemini\antigravity\brain\9678aa79-6e05-40bd-9ad1-54a2d53260eb\preview_cal_active.png"

# We can launch edge with headless and a script that triggers key E
cmd = [
    edge_path,
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--allow-file-access-from-files",
    f"--screenshot={local_out}",
    "--window-size=1920,1080",
    "--virtual-time-budget=3000",
    "file:///E:/WorkSpace/ZeldaOOTMAP/app/index.html?cal=1"
]
subprocess.run(cmd, capture_output=True)
if os.path.exists(local_out):
    shutil.copy2(local_out, dest)
    print("SUCCESS:", os.path.getsize(dest))
