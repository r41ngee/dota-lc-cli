import json

def parse_localization_string(localization_string):
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

with open("abilities_russian.txt", encoding="utf-8") as file:
    with open("abilities_russian.json", "w", encoding="utf-8") as jfile:
        json.dump(parse_localization_string(file.read()), jfile)