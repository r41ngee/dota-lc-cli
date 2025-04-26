"""Модуль для работы с пресетами локализации.

Позволяет сохранять и загружать наборы изменений локализации
для героев и предметов.
"""

import json
import os

from dotatypes import Hero


class Preset:
    """Класс для работы с пресетами локализации.

    Attributes:
        filename (str): Имя файла пресета
        heroes (list[Hero]): Список героев в пресете
        items (list): Список предметов в пресете
    """

    def __init__(
        self, name: str, heroes: list[Hero] | None = None, items: list | None = None
    ):
        """Инициализирует пресет.

        Args:
            name (str): Имя пресета
            heroes (list[Hero] | None, optional): Список героев. По умолчанию None
            items (list | None, optional): Список предметов. По умолчанию None
        """
        self.filename = name + ".json"
        self.heroes = heroes or []
        self.items = items or []

    def save(self):
        """Сохраняет пресет в файл.

        Создает директорию presets, если она не существует,
        и сохраняет пресет в формате JSON.
        """
        os.makedirs("presets", exist_ok=True)

        with open(f"presets/{self.filename}", "w") as f:
            json.dump(
                {
                    "heroes": self.heroes,
                    "items": self.items,
                },
                f,
                indent=4,
                ensure_ascii=False,
            )

    def load(filename: str):
        """Загружает пресет из файла.

        Args:
            filename (str): Имя файла пресета

        Returns:
            Preset: Загруженный пресет
        """
        with open(f"presets/{filename}", "r") as f:
            dct = json.load(f)
            return Preset(
                name=filename.replace(".json", ""),
                heroes=[Hero(h) for h in dct["heroes"]],  # Преобразуем словари в Hero
                items=dct["items"],
            )

    def load_names() -> list[str]:
        """Получает список всех доступных пресетов.

        Returns:
            list[str]: Список имен файлов пресетов
        """
        files = [f for f in os.listdir("presets/") if f.endswith(".json")]

        return files
