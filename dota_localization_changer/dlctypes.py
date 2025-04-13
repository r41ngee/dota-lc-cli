# -----------
# - r41ngee -
# -----------

class Skill:
    def __init__(self, desc):
        self.name = desc["name"]
        self.key = desc["key"]
        self.username = desc["username"]

        self.desc = desc

    def ToKeyPair(self) -> dict[str, str]:
        return {self.key: self.name}

class Facet:
    def __init__(self, desc):
        self.name = desc["name"]
        self.key = desc["key"]
        self.username = desc["username"]

        self.desc = desc

    def ToKeyPair(self):
        return {self.key: self.name}

class Hero:
    def __init__(self, desc: dict):
        self.name: str = desc["name"]
        self.key: str = desc["key"]
        self.skills: list[Skill] = [Skill(i) for i in desc["skills"]]
        self.facets: list[Facet] = [Facet(i) for i in desc["facet"]]

        self.desc = desc

    def ToKeyPair(self):
        result = {self.key: self.name}
        for i in self.skills:
            result.update(i.ToKeyPair())
        for i in self.facets:
            result.update(i.ToKeyPair())

        return result