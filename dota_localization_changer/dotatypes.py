# -----------
# - r41ngee -
# -----------
from typing import Literal


class LocalizableEntity:
    def __init__(self, desc: dict):
        self.name: str = desc["name"]
        self.key: str = desc["key"]
        self.username: str = desc.get("username")

    def to_key_pair(self) -> dict[str, str]:
        return {self.key: self.username if self.username is not None else self.name}

    def to_dict(self) -> dict:
        result = {"name": self.name, "key": self.key}
        if self.username is not None:
            result["username"] = self.username
        return result


class Skill(LocalizableEntity):
    def __init__(self, desc: dict):
        super().__init__(desc)


class Facet(LocalizableEntity):
    def __init__(self, desc: dict):
        super().__init__(desc)


class Hero(LocalizableEntity):
    def __init__(self, desc: dict):
        super().__init__(desc)
        self.gender: Literal["m", "f"] = desc.get("gender", "m")
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


class Item(LocalizableEntity):
    def __init__(self, desc: dict):
        super().__init__(desc)
