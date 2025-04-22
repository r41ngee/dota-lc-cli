from dotatypes import *
import os
import json 

class Preset:
    def __init__(self, name: str, heroes: list[Hero] | None = None, items: list | None = None):
        self.filename = name + ".json"

        self.heroes = heroes
        self.items = items
        if self.items is None:
            self.items = []
        if self.heroes is None:
            self.heroes = []

    def save(self):
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
        with open(f"presets/{filename}", "r") as f:
            dct = json.load(f)
            return Preset(
                name=filename.replace(".json", ""),
                heroes=[Hero(h) for h in dct["heroes"]],  # Преобразуем словари в Hero
                items=dct["items"],
            )
        
    def load_names() -> list[str]:
        files = [f for f in os.listdir("presets/") if f.endswith(".json")]

        return files