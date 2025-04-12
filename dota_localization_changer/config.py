import json
from tkinter.filedialog import askdirectory
with open("data/config.json", "r") as f:
    cfg: dict[str, str] = json.load(f)

DOTA_DIR = cfg["dota_directory"]
if DOTA_DIR in ("", None):
    DOTA_DIR = askdirectory(initialdir="C:\\Program Files (x86)\\Steam\\steamapps\\common\\dota 2 beta")
    cfg["dota_directory"] = DOTA_DIR

with open("data/config.json", "w") as f:
    json.dump(cfg, f, indent=4)