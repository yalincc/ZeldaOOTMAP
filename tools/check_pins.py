import re
from collections import Counter

with open(r"E:\WorkSpace\ZeldaOOTMAP\app\data\pins_data.js", "r", encoding="utf-8") as f:
    text = f.read()

areas = re.findall(r'"area":\s*"([^"]+)"', text)
counts = Counter(areas)
print("Total pins:", len(areas))
for area, count in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"  {area}: {count}")
