# -----------
# - r41ngee -
# -----------

import logging
import re

from tqdm import tqdm


def parse(lines: list | tuple) -> dict:
    """Парсит файл локализации Dota 2 из формата KV в словарь Python.

    Args:
        lines (list | tuple): Список строк файла локализации

    Returns:
        dict: Словарь, где ключи - это идентификаторы строк локализации,
              а значения - соответствующие тексты

    Note:
        Пропускает первые 5 и последние 3 строки файла, а также пустые строки
        и строки, начинающиеся с '//'.
    """
    data = {}
    len_lines = len(lines)
    logging.debug(f"Started parsing with {len_lines} lines")

    # Предварительно компилируем регулярное выражение
    pattern = re.compile(r'("(?:[^"\\]|\\.)*")\s*("(?:[^"\\]|\\.)*")(?:\s*//\s*(.*))?')

    # Предварительно фильтруем строки, которые нужно обработать
    valid_lines = [
        (i, line.strip())
        for i, line in enumerate(lines)
        if 5 <= i < len_lines - 3 and line.strip() and not line.strip().startswith("//")
    ]

    for lindex, line in valid_lines:
        match = pattern.match(line)
        if match:
            key, value, _ = match.groups()
            # Убираем внешние кавычки и экранируем внутренние
            data[key[1:-1].replace('\\"', '"')] = value[1:-1].replace('\\"', '"')
        else:
            logging.warning(f"Parse error: line {lindex + 1} was not parsed")

    logging.info(f"Parser ended with {len(data)} pairs")
    return data


def unparse(data: dict, lang: str = "russian") -> str:
    """Преобразует словарь Python обратно в формат KV файла локализации Dota 2.

    Args:
        data (dict): Словарь с данными локализации
        lang (str, optional): Язык локализации. По умолчанию "russian"

    Returns:
        str: Строка в формате KV файла локализации Dota 2

    Note:
        В настоящее время поддерживается только русский язык.
        В будущем планируется добавить поддержку других языков.
    """
    logging.info(f"Unparser starts with {len(data.items())} pairs")

    # Используем список для более эффективной конкатенации
    lines = ['"lang"', "{", '\t"Language" "russian"', '\t"Tokens"', "\t{"]

    # Предварительно экранируем все ключи и значения
    escaped_items = []
    for key, value in data.items():
        escaped_key = key.replace('"', '\\"')
        escaped_value = value.replace('"', '\\"')
        escaped_items.append((escaped_key, escaped_value))

    # Добавляем все строки одним махом
    lines.extend(f'\t\t"{key}" "{value}"' for key, value in escaped_items)

    lines.extend(["\t}", "}"])

    return "\n".join(lines)
