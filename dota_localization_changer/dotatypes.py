"""Типы данных для Dota 2 Localization Changer.

Содержит классы для работы с локализуемыми сущностями Dota 2.
"""

from typing import Dict, List, Literal, Optional


class LocalizableEntity:
    """Базовый класс для локализуемых сущностей."""

    def __init__(self, desc: Dict) -> None:
        """Инициализирует локализуемую сущность.

        Args:
            desc: Словарь с описанием сущности
        """
        self.name: str = desc["name"]
        self.key: str = desc["key"]
        self.username: Optional[str] = desc.get("username")

    def to_key_pair(self) -> Dict[str, str]:
        """Преобразует сущность в пару ключ-значение для KV-файла.

        Returns:
            Словарь с одним элементом: ключ локализации и её значение
        """
        return {self.key: self.username if self.username is not None else self.name}

    def to_dict(self) -> Dict:
        """Преобразует сущность в словарь.

        Returns:
            Словарь с описанием сущности
        """
        result = {"name": self.name, "key": self.key}
        if self.username is not None:
            result["username"] = self.username
        return result


class Skill(LocalizableEntity):
    """Класс для навыков героев."""

    def __init__(self, desc: Dict) -> None:
        """Инициализирует навык.

        Args:
            desc: Словарь с описанием навыка
        """
        super().__init__(desc)


class Facet(LocalizableEntity):
    """Класс для аспектов героев."""

    def __init__(self, desc: Dict) -> None:
        """Инициализирует аспект.

        Args:
            desc: Словарь с описанием аспекта
        """
        super().__init__(desc)


class Hero(LocalizableEntity):
    """Класс для героев."""

    def __init__(self, desc: Dict) -> None:
        """Инициализирует героя.

        Args:
            desc: Словарь с описанием героя
        """
        super().__init__(desc)
        self.gender: Literal["m", "f"] = desc.get("gender", "m")
        self.skills: List[Skill] = [Skill(skill) for skill in desc["skills"]]
        self.facets: List[Facet] = [Facet(facet) for facet in desc["facets"]]

    def to_dict(self) -> Dict:
        """Преобразует героя в словарь.

        Returns:
            Словарь с описанием героя
        """
        result = {
            "name": self.name,
            "key": self.key,
            "skills": [skill.to_dict() for skill in self.skills],
            "facets": [facet.to_dict() for facet in self.facets],
        }
        if self.username is not None:
            result["username"] = self.username
        if self.gender == "f":
            result["gender"] = "f"
        return result

    def to_key_pair(self) -> Dict[str, str]:
        """Преобразует героя в пары ключ-значение для KV-файла.

        Returns:
            Словарь с парами ключ-значение для всех локализуемых элементов героя
        """
        result = {}
        if self.username is not None:
            result[self.key] = f"#|{self.gender}|#{self.username}"
        else:
            result[self.key] = f"#|{self.gender}|#{self.name}"

        for skill in self.skills:
            result.update(skill.to_key_pair())
        for facet in self.facets:
            result.update(facet.to_key_pair())

        return result


class Item(LocalizableEntity):
    """Класс для предметов."""

    def __init__(self, desc: Dict) -> None:
        """Инициализирует предмет.

        Args:
            desc: Словарь с описанием предмета
        """
        super().__init__(desc)
