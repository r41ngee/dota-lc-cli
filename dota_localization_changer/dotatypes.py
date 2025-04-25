# -----------
# - r41ngee -
# -----------
from typing import Literal

class BaseEntity:
    def __init__(self, desc: dict):
        self.name: str = desc["name"]
        self.key: str = desc["key"]
        try:
            self.username: str = desc["username"]
        except KeyError:
            self.username = None

    def to_key_pair(self) -> dict[str, str]:
        if self.username is not None:
            return {self.key: self.username}
        else:
            return {self.key: self.name}
    
    def to_dict(self) -> dict:
        result = {
            "name": self.name,
            "key": self.key,
        }

        if self.username is not None:
            result["username"] = self.username

        return result

class Skill(BaseEntity):
    def __init__(self, desc: dict):
        super().__init__(desc)

class Facet(BaseEntity):
    def __init__(self, desc: dict):
        super().__init__(desc)

class Hero(BaseEntity):
    def __init__(self, desc: dict):
        super().__init__(desc)
        try:
            self.gender: Literal["m", "f"] = desc["gender"]
        except KeyError:
            self.gender = "m"

        self.skills: list[Skill] = [Skill(i) for i in desc["skills"]]
        self.facets: list[Facet] = [Facet(i) for i in desc["facets"]]

    def to_dict(self) -> dict:
        result = {
            "name": self.name,
            "key": self.key,
            "skills": [i.to_dict() for i in self.skills],
            "facets": [i.to_dict() for i in self.facets],
        }

        if self.username is not None:
            result["username"] = self.username

        if self.gender == "f":
            result["gender"] = "f"

        return result

    def to_key_pair(self):
        if self.username is not None:
            result = {self.key: f"#|{self.gender}|#{self.username}"}
        else:
            result = {self.key: f"#|{self.gender}|#{self.name}"}
        for i in self.skills:
            result.update(i.to_key_pair())
        for i in self.facets:
            result.update(i.to_key_pair())

        return result
    
class Item:
    def __init__(self, desc:dict[str, str]):
        self.name = desc["name"]
        self.key = desc["key"]
        try:
            self.username = desc["username"]
        except KeyError:
            self.username = None

    def ToKeyPair(self):
        if self.username:
            result = {self.key: self.username}
        else:
            result = {self.key: self.name}

        return result
    
    def toDict(self):
        result = {
            "name": self.name,
            "key": self.key,
        }
        if self.username:
            result["username"] = self.username
        
        return result