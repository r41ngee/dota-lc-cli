"""Модуль конфигурации для Dota 2 Localization Changer.

Содержит настройки для работы программы, включая:
- Уровень логирования
- Путь к директории Dota 2
- Путь к VPK файлу
"""

import json
import logging
from tkinter.filedialog import askdirectory

# Загрузка конфигурации из файла
try:
    with open("data/config.json", "r") as f:
        cfg: dict[str, str] = json.load(f)
except OSError as e:
    logging.error(e)
    raise e

# Уровень логирования
LOGGER_LEVEL = cfg["logger_lvl"]

# Путь к директории Dota 2
DOTA_DIR = cfg["dota_directory"]
if DOTA_DIR is None:
    print("Выберите корневую директорию доты (dota 2 beta)")
    DOTA_DIR = askdirectory()
    cfg["dota_directory"] = DOTA_DIR

# Путь к VPK файлу с русской локализацией
VPK_PATH = DOTA_DIR + "/game/dota_russian/pak01_dir.vpk"

# Сохранение обновленной конфигурации
with open("data/config.json", "w") as f:
    json.dump(cfg, f, indent=4)
