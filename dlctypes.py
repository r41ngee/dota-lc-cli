# -----------
# - r41ngee -
# -----------

class Skill:
    def __init__(self, desc):
        self.name = desc["name"]
        self.key = desc["key"]
        self.linked = desc["link"]

        self.desc = desc

    def ToKeyPair(self) -> dict[str, str]:
        result = {}
        result.update({self.key: self.name})
        for i in self.linked:
            result.update({i: self.name})

        return result

class Facet:
    def __init__(self, desc):
        self.name = desc["name"]
        self.key = desc["key"]

        self.desc = desc

    def ToKeyPair(self):
        result = {self.key: self.name}

        return result

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