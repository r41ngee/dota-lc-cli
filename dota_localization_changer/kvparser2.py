# -----------
# - r41ngee -
# -----------

import logging
import re

from tqdm import tqdm


def parse(lines: list | tuple) -> dict:
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
        match = re.match(r'(".*?")\s*(".*?")(?:\s*//\s*(.*))?', line)

        if match:
            key, value, _ = match.groups()
            key, value = key.strip('"'), value.strip('"')
            if "<" not in value:
                data[key] = value
                parsed += 1
        else:
            logging.warning(f"Parse error: line {lindex + 1} was not parsed")

    logging.info(f"Parser ended with {len(data)} pairs")
    return data


def unparse(data: dict, lang: str = "russian") -> str:
    result = """"lang"
{ 
	"Language" "russian" 
	"Tokens" 
	{"""  # ДОРАБОТАТЬ языки(на будущее)

    logging.info(f"Unparser starts with {len(data.items())} pairs")

    i = 5

    print("\n")

    for key, value in tqdm(
        data.items(), desc="Запаковка файла локализации", colour="green"
    ):
        result += f'\n\t\t"{key}" "{value}"'
        logging.debug(f"Key {key} written with value {value} in line {i}")
        i += 1

    result += """
	}
}"""

    return result
