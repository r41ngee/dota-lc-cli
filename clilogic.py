import os

class Skill:
    def __init__(self, desc):
        self.name = desc["name"]
        self.key = desc["key"]
        self.linked = desc["link"]

        self.desc = desc

class Facet:
    def __init__(self, desc):
        self.name = desc["name"]
        self.key = desc["key"]

        self.desc = desc

class Hero:
    def __init__(self, desc: dict):
        self.name: str = desc["name"]
        self.key: str = desc["key"]
        self.skills: list[Skill] = [Skill(i) for i in desc["skills"]]
        self.facets: list[Facet] = [Facet(i) for i in desc["facet"]]

        self.desc = desc

def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')