import json
import logging
from tkinter.filedialog import askdirectory

try:
    with open("data/config.json", "r") as f:
        cfg: dict[str, str] = json.load(f)
except OSError as e:
    logging.error(e)
    raise e

LOGGER_LEVEL = cfg["logger_lvl"]

DOTA_DIR = cfg["dota_directory"]
if DOTA_DIR is None:
    print("Выберите корневую директорию доты (dota 2 beta)")
    DOTA_DIR = askdirectory()
    cfg["dota_directory"] = DOTA_DIR

VPK_PATH = DOTA_DIR + "/game/dota_russian/pak01_dir.vpk"

with open("data/config.json", "w") as f:
    json.dump(cfg, f, indent=4)
