"""Парсер KV-файлов для Dota 2 Localization Changer.

Модуль для парсинга и генерации KV-файлов локализации Dota 2.
"""

import re
from typing import Dict, List, Tuple

# Предварительно компилируем регулярные выражения
KV_PATTERN = re.compile(r'("(?:[^"\\]|\\.)*")\s*("(?:[^"\\]|\\.)*")(?:\s*//\s*(.*))?')
HEADER_LINES = 5
FOOTER_LINES = 3


def parse(lines: List[str] | Tuple[str, ...]) -> Dict[str, str]:
    """Парсит файл локализации Dota 2 из формата KV в словарь Python.

    Args:
        lines: Список строк файла локализации

    Returns:
        Словарь, где ключи - это идентификаторы строк локализации,
        а значения - соответствующие тексты
    """
    data: Dict[str, str] = {}
    total_lines = len(lines)

    # Фильтруем и обрабатываем только нужные строки
    valid_lines = (
        (i, line.strip())
        for i, line in enumerate(lines)
        if HEADER_LINES <= i < total_lines - FOOTER_LINES
        and line.strip()
        and not line.strip().startswith("//")
    )

    for lindex, line in valid_lines:
        if match := KV_PATTERN.match(line):
            key, value, _ = match.groups()
            # Убираем внешние кавычки и экранируем внутренние
            data[key[1:-1].replace('\\"', '"')] = value[1:-1].replace('\\"', '"')

    return data


def unparse(data: Dict[str, str], lang: str = "russian") -> str:
    """Преобразует словарь Python обратно в формат KV файла локализации Dota 2.

    Args:
        data: Словарь с данными локализации
        lang: Язык локализации (по умолчанию "russian")

    Returns:
        Строка в формате KV файла локализации Dota 2
    """
    # Используем список для более эффективной конкатенации
    lines = ['"lang"', "{", f'\t"Language" "{lang}"', '\t"Tokens"', "\t{"]

    # Экранируем и добавляем все строки одним махом
    for key, value in data.items():
        escaped_key = key.replace('"', '\\"')
        escaped_value = value.replace('"', '\\"')
        lines.append(f'\t\t"{escaped_key}" "{escaped_value}"')

    lines.extend(["\t}", "}"])
    return "\n".join(lines)
