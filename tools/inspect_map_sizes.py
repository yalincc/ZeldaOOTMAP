import glob
import os
from PIL import Image

field_maps = glob.glob(r"E:\WorkSpace\ZeldaOOTMAP\app\assets\maps\field\*_Child_00.webp")
field_maps += glob.glob(r"E:\WorkSpace\ZeldaOOTMAP\app\assets\maps\field\*_Adult_00.webp")
print(f"Total field maps: {len(field_maps)}")

for f in sorted(field_maps):
    im = Image.open(f)
    print(f"  {os.path.basename(f):35s}: size = {im.size}")
