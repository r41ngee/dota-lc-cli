from dotatypes import *
import os
import json 

class Preset:
    def __init__(self, name: str, heroes: list[Hero] | None = None, items: list | None = None):
        self.name = name
        self.filename = self.name.replace(" ", "_")

        self.heroes = heroes
        self.items = items