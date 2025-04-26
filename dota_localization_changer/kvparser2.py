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
    parsed = 0

    for lindex in tqdm(
        range(len_lines), desc="Распаковка файла локализации", colour="red"
    ):
        if (
            lindex < 5
            or lindex > len_lines - 3
            or not lines[lindex].strip()
            or lines[lindex].strip().startswith("//")
        ):
            continue

        line = lines[lindex].strip()
        # Используем более точное регулярное выражение для парсинга
        match = re.match(
            r'("(?:[^"\\]|\\.)*")\s*("(?:[^"\\]|\\.)*")(?:\s*//\s*(.*))?', line
        )

        if match:
            key, value, _ = match.groups()
            # Убираем внешние кавычки и экранируем внутренние
            key = key[1:-1].replace('\\"', '"')
            value = value[1:-1].replace('\\"', '"')
            data[key] = value
            parsed += 1
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
    result = """"lang"
{ 
	"Language" "russian" 
	"Tokens" 
	{"""

    logging.info(f"Unparser starts with {len(data.items())} pairs")

    i = 5

    print("\n")

    for key, value in tqdm(
        data.items(), desc="Запаковка файла локализации", colour="green"
    ):
        # Экранируем кавычки в ключах и значениях
        escaped_key = key.replace('"', '\\"')
        escaped_value = value.replace('"', '\\"')
        result += f'\n\t\t"{escaped_key}" "{escaped_value}"'
        logging.debug(f"Key {key} written with value {value} in line {i}")
        i += 1

    result += """
	}
}"""

    return result
