"""Модуль для работы с пресетами локализации.

Позволяет сохранять и загружать наборы изменений локализации
для героев и предметов.
"""

import json
import os
from pathlib import Path
from tkinter import messagebox
from typing import List, Optional

from dotatypes import Hero, Item

PRESETS_DIR = Path("presets")


class Preset:
    """Класс для работы с пресетами локализации.

    Attributes:
        filename: Имя файла пресета
        heroes: Список героев в пресете
        items: Список предметов в пресете
    """

    def __init__(
        self,
        name: str,
        heroes: Optional[List[Hero]] = None,
        items: Optional[List[dict]] = None,
    ) -> None:
        """Инициализирует пресет.

        Args:
            name: Имя пресета
            heroes: Список героев
            items: Список предметов
        """
        self.filename = f"{name}.json"
        self.heroes = heroes or []
        self.items = items or []

    def to_dict(self):
        return {
            "heroes": [hero.to_dict() for hero in self.heroes],
            "items": [item.to_dict() for item in self.items],
        }

    def save(self) -> None:
        """Сохраняет пресет в файл."""
        try:
            os.makedirs("presets", exist_ok=True)
            with open(
                os.path.join("presets", f"{self.filename}"), "w", encoding="utf-8"
            ) as f:
                json.dump(self.to_dict(), f, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror(
                "Ошибка", f"Ошибка сохранения пресета {self.filename}: {e}"
            )

    @staticmethod
    def load(filename: str) -> "Preset":
        """Загружает пресет из файла.

        Args:
            filename: Имя файла пресета

        Returns:
            Загруженный пресет
        """
        try:
            with open(
                os.path.join("presets", f"{filename}"), "r", encoding="utf-8"
            ) as f:
                data = json.load(f)
                return Preset(
                    filename.replace(".json", ""),
                    [Hero(i) for i in data["heroes"]],
                    [Item(i) for i in data["items"]],
                )
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки пресета {filename}: {e}")
            return Preset(filename.replace(".json", ""))

    @staticmethod
    def load_names() -> List[str]:
        """Получает список всех доступных пресетов.

        Returns:
            Список имен файлов пресетов
        """
        PRESETS_DIR.mkdir(parents=True, exist_ok=True)
        return [f.name for f in PRESETS_DIR.glob("*.json")]
