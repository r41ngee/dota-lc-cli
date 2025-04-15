# -----------
# - r41ngee -
# -----------
from typing import Literal


class Skill:
    def __init__(self, desc):
        self.name = desc["name"]
        self.key = desc["key"]
        self.username = desc["username"]

        self.desc = desc

    def ToKeyPair(self) -> dict[str, str]:
        return {self.key: self.username}
    
    def toDict(self):
        if self.username is None:
            username = self.name
        else:
            username = self.username
        return {
            "name": self.name,
            "key": self.key,
            "username": username,
        }

class Facet:
    def __init__(self, desc):
        self.name = desc["name"]
        self.key = desc["key"]
        self.username = desc["username"]

        self.desc = desc

    def ToKeyPair(self):
        return {self.key: self.username}
    
    def toDict(self):
        if self.username is None:
            username = self.name
        else:
            username = self.username
        return {
            "name": self.name,
            "key": self.key,
            "username": username,
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
        if self.username is None:
            username = self.name
        else:
            username = self.username
        return {
            "name": self.name,
            "key": self.key,
            "username": username,
            "gender": self.gender,
            "skills": [i.toDict() for i in self.skills],
            "facets": [i.toDict() for i in self.facets],
        }

    def ToKeyPair(self):
        result = {self.key: f"#|{self.gender}|#{self.username}"}
        for i in self.skills:
            result.update(i.ToKeyPair())
        for i in self.facets:
            result.update(i.ToKeyPair())

        return result