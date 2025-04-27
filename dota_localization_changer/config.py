"""Модуль конфигурации для Dota 2 Localization Changer.

Содержит настройки для работы программы, включая:
- Уровень логирования
- Путь к директории Dota 2
- Путь к VPK файлу
"""

import json
import logging
from pathlib import Path
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from typing import Final

# Константы
CONFIG_PATH: Final[Path] = Path("data/config.json")
DEFAULT_LOGGER_LEVEL: Final[str] = "INFO"


def load_config() -> dict[str, str]:
    """Загружает конфигурацию из файла."""
    try:
        with CONFIG_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        logging.error(f"Ошибка загрузки конфигурации: {e}")
        return {"logger_lvl": DEFAULT_LOGGER_LEVEL, "dota_directory": None}


def save_config(config: dict[str, str]) -> None:
    """Сохраняет конфигурацию в файл."""
    try:
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with CONFIG_PATH.open("w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    except OSError as e:
        logging.error(f"Ошибка сохранения конфигурации: {e}")


# Загрузка конфигурации
cfg = load_config()

# Уровень логирования
LOGGER_LEVEL: Final[str] = cfg.get("logger_lvl", DEFAULT_LOGGER_LEVEL)

# Путь к директории Dota 2
DOTA_DIR: str = cfg.get("dota_directory")
if not DOTA_DIR:
    messagebox.showinfo(
        "Выбор директории Dota 2",
        "Пожалуйста, выберите корневую директорию Dota 2 (dota 2 beta).\n\n"
        "Обычно она находится в:\n"
        "C:\\Program Files (x86)\\Steam\\steamapps\\common\\dota 2 beta",
    )
    DOTA_DIR = askdirectory()
    if DOTA_DIR:
        cfg["dota_directory"] = DOTA_DIR
        save_config(cfg)

# Путь к VPK файлу с русской локализацией
VPK_PATH: Final[str] = (
    f"{DOTA_DIR}/game/dota_russian/pak01_dir.vpk" if DOTA_DIR else None
)


def change_dota_directory() -> bool:
    """Смена пути установки Dota 2.

    Returns:
        bool: True если путь был успешно изменен, False в противном случае
    """
    global DOTA_DIR, VPK_PATH
    new_dir = askdirectory()
    if not new_dir:
        return False

    DOTA_DIR = new_dir
    VPK_PATH = f"{DOTA_DIR}/game/dota_russian/pak01_dir.vpk"
    cfg["dota_directory"] = DOTA_DIR
    save_config(cfg)
    return True
