import json
import logging
from tkinter.filedialog import askdirectory

from misc import *

try:
    with open("data/config.json", "r") as f:
        cfg: dict[str, str] = json.load(f)
except OSError as e:
    logging.error(e)
    endlog(3)
    raise e
LOGGER_LEVEL = cfg["logger_lvl"]
DOTA_DIR = cfg["dota_directory"]
if DOTA_DIR in ("", None):
    print("Выберите корневую директорию доты (dota 2 beta)")
    DOTA_DIR = askdirectory(initialdir="C:\\Program Files (x86)\\Steam\\steamapps\\common\\dota 2 beta")
    cfg["dota_directory"] = DOTA_DIR

with open("data/config.json", "w") as f:
    json.dump(cfg, f, indent=4)