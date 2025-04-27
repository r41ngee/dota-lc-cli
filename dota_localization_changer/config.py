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


def change_dota_directory() -> bool:
    """Смена пути установки Dota 2

    Returns:
        bool: True если путь был успешно изменен, False в противном случае
    """
    global DOTA_DIR, VPK_PATH
    new_dir = askdirectory()
    if not new_dir:
        return False

    DOTA_DIR = new_dir
    VPK_PATH = DOTA_DIR + "/game/dota_russian/pak01_dir.vpk"

    cfg["dota_directory"] = DOTA_DIR
    with open("data/config.json", "w") as f:
        json.dump(cfg, f, indent=4)

    return True


# Сохранение обновленной конфигурации
with open("data/config.json", "w") as f:
    json.dump(cfg, f, indent=4)

print(VPK_PATH)
