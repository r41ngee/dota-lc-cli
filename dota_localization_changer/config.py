"""Модуль конфигурации для Dota 2 Localization Changer.

Содержит настройки для работы программы, включая:
- Уровень логирования
- Путь к директории Dota 2
- Путь к VPK файлу
"""

import json
import os
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from typing import Final

# Константы
CONFIG_FILE: Final[str] = "config.json"
DEFAULT_LOGGER_LEVEL: Final[str] = "INFO"


def load_config() -> dict[str, str]:
    """Загружает конфигурацию из файла."""
    global VPK_PATH
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            VPK_PATH = config.get("vpk_path", "")
            return config
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка загрузки конфигурации: {e}")
        return {"logger_lvl": DEFAULT_LOGGER_LEVEL, "dota_directory": None}


def save_config(config: dict[str, str]) -> None:
    """Сохраняет конфигурацию в файл."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка сохранения конфигурации: {e}")


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
    global VPK_PATH
    new_path = askdirectory(title="Выберите папку с Dota 2")
    if not new_path:
        return False

    VPK_PATH = os.path.join(new_path, "game", "dota", "pak01_dir.vpk")
    cfg["dota_directory"] = new_path
    save_config(cfg)
    return True
