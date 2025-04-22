from dotatypes import *
import os
import json 

class Preset:
    def __init__(self, name: str, heroes: list[Hero] | None = None, items: list | None = None):
        self.name = name
        self.filename = self.name.replace(" ", "_")

        self.heroes = heroes
        self.items = items

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