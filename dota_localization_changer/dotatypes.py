# -----------
# - r41ngee -
# -----------
from typing import Literal


class Skill:
    def __init__(self, desc):
        self.name = desc["name"]
        self.key = desc["key"]
        try:
            self.username = desc["username"]
        except KeyError:
            self.username = None

        self.desc = desc

    def ToKeyPair(self) -> dict[str, str]:
        if self.username is not None:
            return {self.key: self.username}
        else:
            return {self.key: self.name}
    
    def toDict(self):
        return {
            "name": self.name,
            "key": self.key,
            "username": self.username,
        }

class Facet:
    def __init__(self, desc):
        self.name = desc["name"]
        self.key = desc["key"]
        self.username = desc["username"]

        self.desc = desc

    def ToKeyPair(self):
        if self.username is not None:
            return {self.key: self.username}
        else:
            return {self.key: self.name}
    
    def toDict(self):
        return {
            "name": self.name,
            "key": self.key,
            "username": self.username,
        }

class Hero:
    def __init__(self, desc: dict):
        self.name: str = desc["name"]
        self.key: str = desc["key"]
        self.username: str = desc["username"]
        self.gender: str | Literal["m", "f"] = desc["gender"]
        self.skills: list[Skill] = [Skill(i) for i in desc["skills"]]
        self.facets: list[Facet] = [Facet(i) for i in desc["facets"]]

        self.desc = desc

    def toDict(self) -> dict:
        return {
            "name": self.name,
            "key": self.key,
            "username": self.username,
            "gender": self.gender,
            "skills": [i.toDict() for i in self.skills],
            "facets": [i.toDict() for i in self.facets],
        }

    def ToKeyPair(self):
        if self.username is not None:
            result = {self.key: f"#|{self.gender}|#{self.username}"}
        else:
            result = {self.key: f"#|{self.gender}|#{self.name}"}
        for i in self.skills:
            result.update(i.ToKeyPair())
        for i in self.facets:
            result.update(i.ToKeyPair())

        return result