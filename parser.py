import json
import os
# import pathlib

def parse_lstr(localization_string):
    """
    Парсит строку локализации в словарь Python.

    Args:
        localization_string: Строка локализации в формате, как в примере.

    Returns:
        Словарь Python, представляющий структуру локализации.
    """
    result = {}
    current_section = result
    lines = localization_string.strip().splitlines()

    for line in lines:
        line = line.strip()

        # Пропускаем пустые строки и комментарии
        if not line or line.startswith("//"):
            continue

        if line.startswith('"lang"'):
            result['lang'] = {}
            current_section = result['lang']
        elif line.startswith('"Language"'):
            parts = line.split('"')
            if len(parts) >= 4:
                current_section['Language'] = parts[3]
        elif line.startswith('"Tokens"'):
            current_section['Tokens'] = {}
            current_section = current_section['Tokens']
        else:
            parts = line.split('"')
            if len(parts) >= 4:
                key = parts[1]
                value = parts[3]
                current_section[key] = value

    return result

def generate_lstr(localization_dict):
    """
    Генерирует строку локализации из словаря Python.

    Args:
        localization_dict: Словарь Python, представляющий структуру локализации.

    Returns:
        Строка локализации в исходном формате.
    """
    output_string = ""

    if 'lang' in localization_dict:
        output_string += '"lang"\n{\n'
        lang_section = localization_dict['lang']

        if 'Language' in lang_section:
            output_string += f'\t"Language"\t\t"{lang_section["Language"]}"\n'

        if 'Tokens' in lang_section:
            output_string += '\t"Tokens"\n\t{\n'
            tokens_section = lang_section['Tokens']
            for token_key, token_value in tokens_section.items():
                output_string += f'\t\t"{token_key}"\t\t"{token_value}"\n'
            output_string += '\t}\n'

        output_string += '}\n'

    return output_string

with open("abilities_russian.txt", encoding="utf-8") as file:
    with open("abilities_russian.json", "w", encoding="utf-8") as jfile:
        content = file.read()
        json.dump(parse_lstr(content), jfile, ensure_ascii=False, indent=4) 