import os
import glob
import re

cache_dir = r"C:\Users\Administrator\AppData\Local\Microsoft\Edge\User Data\Default\Cache\Cache_Data"
files = glob.glob(os.path.join(cache_dir, "f_*"))
print("Cache files count:", len(files))

found = []
for f in files:
    try:
        if os.path.getsize(f) > 5000: # marker json usually > 50KB
            with open(f, "rb") as fp:
                data = fp.read()
                if b"markers" in data.lower() and (b"hyrule" in data.lower() or b"ocarina" in data.lower() or b"skulltula" in data.lower()):
                    found.append((f, len(data)))
                    print(f"Match found: {f} ({len(data)} bytes)")
    except Exception as e:
        pass

print("Total matches:", len(found))
