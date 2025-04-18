from dotatypes import *
import os
import json 

class Preset:
    def __init__(self, name: str, heroes: list[Hero] | None = None, items: list | None = None):
        self.filename = name + ".json"

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

    def load(filename: str) -> None:
        with open(f"presets/{filename}", "r") as f:
            dct = json.load(f)
            return Preset(
                name=filename.replace(".json", ""),
                heroes=dct["heroes"],
                items=dct["items"],
            )