import os
import glob

for browser, bpath in [
    ("Chrome", r"C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default\Cache\Cache_Data"),
    ("Edge", r"C:\Users\Administrator\AppData\Local\Microsoft\Edge\User Data\Default\Cache\Cache_Data")
]:
    if not os.path.exists(bpath):
        continue
    files = glob.glob(os.path.join(bpath, "f_*"))
    print(f"[{browser}] Cache files count: {len(files)}")
    for f in files:
        try:
            with open(f, "rb") as fp:
                data = fp.read()
                if b"gamerguides" in data.lower() or b"skulltula" in data.lower():
                    print(f"[{browser}] Match in {f} ({len(data)} bytes)")
                    # extract sample
                    sample = data[:300]
                    print(f"  sample: {sample}")
        except:
            pass
