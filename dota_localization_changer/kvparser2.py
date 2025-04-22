# -----------
# - r41ngee -
# -----------

import logging
import re

from tqdm import tqdm

def parse(lines: list|tuple) -> dict:
    data = {}
    len_lines = len(lines)
    logging.debug(f"Started parsing with {len_lines} lines")
    parsed = 0

    for lindex in tqdm(range(len_lines), desc="Распаковка файла локализации", colour="red"):
        if lindex < 5 or lindex>len_lines-3:
                logging.debug(f"Skipped parsing line {lindex+1} (shell lines)")
                continue
        line = lines[lindex].strip()
        if line.startswith("//"):
            logging.debug(f"Skipped parsing line {lindex+1} (full comment)")
            continue
        if not line:
            logging.debug(f"Skipped parsing line {lindex+1} (empty line)")
            continue

        match_c = re.match(r'(".*?")\s*(".*?")\s*//\s*(.*)', line)
        match_wc = re.match(r'(".*?")\s*(".*?")', line)

        if match_c:
            logging.debug(f"Line {lindex+1} matched with comment")
            key, value, _ = match_c.groups()
            key, value = key.strip('"'), value.strip('"')
            if "<" in value:
                logging.debug(f"Line {key}:{value} skipped(html)")
            else:
                logging.debug(f"Readed key {key}: value {value}")

                data[key] = value
            parsed += 1
        elif match_wc:
            logging.debug(f"Line {lindex+1} matched without comment")
            key, value = match_wc.groups()
            key, value = key.strip('"'), value.strip('"')

            if "<" in value:
                logging.debug(f"Line {key}:{value} skipped(html)")
            else:
                logging.debug(f"Readed key {key}: value {value}")

                data[key] = value
            parsed += 1
        else:
            logging.warning(f"Parse error: line {lindex+1} was not parsed")
            
            
    logging.info(f"Parser ended with {len(data)} pairs")
    return data

def unparse(data: dict, lang: str = "russian") -> str:
    result = '''"lang"
{ 
	"Language" "russian" 
	"Tokens" 
	{''' # ДОРАБОТАТЬ языки(на будущее)

    logging.info(f"Unparser starts with {len(data.items())} pairs")

    i = 5

    print("\n")

    for key, value in tqdm(data.items(), desc="Запаковка файла локализации", colour="green"):
        result += f'\n\t\t"{key}" "{value}"'
        logging.debug(f"Key {key} written with value {value} in line {i}")
        i+=1

    result += """
	}
}"""

    return result
