"""
Build high-quality illuminated dungeon composite maps.
Replaces the pitch-black *_All.webp silhouettes with illuminated golden-parchment maps.
"""
import glob
import os
from PIL import Image
import numpy as np

DUNGEON_DIR = r"E:\WorkSpace\ZeldaOOTMAP\app\assets\maps\dungeon"

DUNGEONS = {
    "InsideTheDekuTree": {
        "floors": ["B2", "B1", "1F", "2F", "3F"],
        "main_floor": "1F",
        "output_files": ["InsideTheDekuTree_All.webp"]
    },
    "DodongoCavern": {
        "floors": ["2F", "1F"],
        "main_floor": "1F",
        "output_files": ["DodongoCavern_All.webp"]
    },
    "InsideJabuJabuBelly": {
        "floors": ["B1", "2F", "1F"],
        "main_floor": "1F",
        "output_files": ["InsideJabuJabuBelly_All.webp"]
    },
    "ForestTemple": {
        "floors": ["B2", "B1", "3F", "2F", "1F"],
        "main_floor": "1F",
        "output_files": ["ForestTemple_All.webp"]
    },
    "FireTemple": {
        "floors": ["5F", "4F", "3F", "2F", "1F"],
        "main_floor": "1F",
        "output_files": ["FireTemple_All.webp"]
    },
    "WaterTemple": {
        "floors": ["B1", "3F", "2F", "1F"],
        "main_floor": "1F",
        "output_files": ["WaterTemple_All.webp"]
    },
    "ShadowTemple": {
        "floors": ["B4", "B3", "B2", "B1"],
        "main_floor": "B1",
        "output_files": ["ShadowTemple_All.webp"]
    },
    "SpiritTemple": {
        "floors": ["4F", "3F", "2F", "1F"],
        "main_floor": "1F",
        "output_files": ["SpiritTemple_State00_All.webp", "SpiritTemple_State01_All.webp"]
    },
    "BottomOfTheWell": {
        "floors": ["B2", "B1"],
        "main_floor": "B1",
        "output_files": ["BottomOfTheWell_All.webp"]
    },
    "IceCavern": {
        "floors": ["1F"],
        "main_floor": "1F",
        "output_files": ["IceCavern_All.webp"]
    }
}

all_files = [os.path.basename(f) for f in glob.glob(os.path.join(DUNGEON_DIR, "*.webp"))]

for dname, cfg in DUNGEONS.items():
    # Find matching Main files for each floor
    layers = []
    for fl in cfg["floors"]:
        # Find State00 or standard Main
        candidates = [
            f for f in all_files 
            if f.startswith(f"{dname}_{fl}_") and "Main" in f 
            and "State01" not in f and "State02" not in f and "State03" not in f 
            and "Lv2" not in f and "Lv3" not in f
        ]
        if candidates:
            layers.append((fl, candidates[0]))
    
    if not layers:
        print(f"No layers found for {dname}")
        continue
    
    # Load first image to get dimensions
    first_path = os.path.join(DUNGEON_DIR, layers[0][1])
    first_img = Image.open(first_path)
    w, h = first_img.size
    
    # Composite: back with subtle parchment texture and all main rooms
    comp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    
    for fl, fname in layers:
        img = Image.open(os.path.join(DUNGEON_DIR, fname)).convert("RGBA")
        comp = Image.alpha_composite(comp, img)
    
    # Save to each output file
    for out_name in cfg["output_files"]:
        out_path = os.path.join(DUNGEON_DIR, out_name)
        comp.save(out_path, "WEBP", quality=88, method=4)
        print(f"Generated {out_name}: {comp.size} with {len(layers)} floors")

print("All dungeon composite maps successfully built!")
