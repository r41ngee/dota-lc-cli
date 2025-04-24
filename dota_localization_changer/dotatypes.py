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

    def ToKeyPair(self) -> dict[str, str]:
        if self.username is not None:
            return {self.key: self.username}
        else:
            return {self.key: self.name}
    
    def toDict(self):
        result = {
            "name": self.name,
            "key": self.key,
        }

        if self.username is not None:
            result["username"] = self.username

        return result

class Facet:
    def __init__(self, desc):
        self.name = desc["name"]
        self.key = desc["key"]
        try:
            self.username = desc["username"]
        except KeyError:
            self.username = None

    def ToKeyPair(self):
        if self.username is not None:
            return {self.key: self.username}
        else:
            return {self.key: self.name}
    
    def toDict(self):
        result = {
            "name": self.name,
            "key": self.key,
        }

        if self.username is not None: 
            result["username"] = self.username

        return result

class Hero:
    def __init__(self, desc: dict):
        self.name: str = desc["name"]
        self.key: str = desc["key"]
        try:
            self.username: str = desc["username"]
        except KeyError:
            self.username= None
        try:
            self.gender: str | Literal["m", "f"] = desc["gender"]
        except KeyError:
            self.gender = "m"
        self.skills: list[Skill] = [Skill(i) for i in desc["skills"]]
        self.facets: list[Facet] = [Facet(i) for i in desc["facets"]]

    def toDict(self) -> dict:
        result = {
            "name": self.name,
            "key": self.key,
            "gender": self.gender,
            "skills": [i.toDict() for i in self.skills],
            "facets": [i.toDict() for i in self.facets],
        }

        if self.username is not None:
            result["username"] = self.username

        if self.gender == "f":
            result["gender"] = "f"

        return result

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