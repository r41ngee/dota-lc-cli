import os

class Skill:
    def __init__(self, desc):
        self.name = desc["name"]
        self.key = desc["key"]
        self.linked = desc["link"]

        self.desc = desc

    def ToKeys(self) -> dict:
        linked_keys = sum([{i: self.name} for i in self.linked])

        return {
            self.key: self.name,
        } + linked_keys

class Facet:
    def __init__(self, desc):
        self.name = desc["name"]
        self.key = desc["key"]

        self.desc = desc

    def ToKeys(self) -> dict:
        return {
            self.key : self.name
        }

class Hero:
    def __init__(self, desc: dict):
        self.name: str = desc["name"]
        self.key: str = desc["key"]
        self.skills: list[Skill] = [Skill(i) for i in desc["skills"]]
        self.facets: list[Facet] = [Facet(i) for i in desc["facet"]]

        self.desc = desc

    def ToKeys(self):
        return {
            self.key: self.name
        } + sum([i.ToKeys() for i in self.skills]) + sum([i.ToKeys() for i in self.facets])

def clear_console():
    # Для Windows
    if os.name == 'nt':
        os.system('cls')
    # Для Unix-подобных систем (Linux, macOS)
    else:
        os.system('clear')