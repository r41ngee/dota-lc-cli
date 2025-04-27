"""Модуль для работы с пресетами локализации.

Позволяет сохранять и загружать наборы изменений локализации
для героев и предметов.
"""

import json
import logging
import os
from pathlib import Path
from typing import List, Optional

from dotatypes import Hero

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

    def save(self) -> None:
        """Сохраняет пресет в файл."""
        PRESETS_DIR.mkdir(parents=True, exist_ok=True)
        file_path = PRESETS_DIR / self.filename

        try:
            with file_path.open("w", encoding="utf-8") as f:
                json.dump(
                    {
                        "heroes": [hero.to_dict() for hero in self.heroes],
                        "items": self.items,
                    },
                    f,
                    indent=4,
                    ensure_ascii=False,
                )
        except OSError as e:
            logging.error(f"Ошибка сохранения пресета {self.filename}: {e}")

    @staticmethod
    def load(filename: str) -> "Preset":
        """Загружает пресет из файла.

        Args:
            filename: Имя файла пресета

        Returns:
            Загруженный пресет
        """
        file_path = PRESETS_DIR / filename
        try:
            with file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                return Preset(
                    name=filename.replace(".json", ""),
                    heroes=[Hero(hero_data) for hero_data in data["heroes"]],
                    items=data["items"],
                )
        except (OSError, json.JSONDecodeError) as e:
            logging.error(f"Ошибка загрузки пресета {filename}: {e}")
            return Preset(filename.replace(".json", ""))

    @staticmethod
    def load_names() -> List[str]:
        """Получает список всех доступных пресетов.

        Returns:
            Список имен файлов пресетов
        """
        PRESETS_DIR.mkdir(parents=True, exist_ok=True)
        return [f.name for f in PRESETS_DIR.glob("*.json")]
