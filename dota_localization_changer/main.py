# -----------
# - r41ngee -
# -----------

# -BOX IMPORTS-
import logging
import subprocess
from time import sleep

# -REMOTE IMPORTS-
import art
import kvparser2
import tabulate

# -LOCAL IMPORTS-
from config import *
from dotatypes import *
from misc import *
from presets import *


# -LOGGER SETTINGS-
logging.basicConfig(
    level=LOGGER_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='.log',
    filemode='w'
)


def main() -> int:
    try:
        herotagsfile = open("data/hero_tags.json", "r+", encoding='utf-8')
        herolist = [Hero(i) for i in json.load(herotagsfile)]
    except OSError as e:
        logging.error(e)
        return 2
    
    try:
        itemstagsfile = open("data/items_tags.json", "r+", encoding="utf-8")
        itemslist = [Item(i) for i in json.load(itemstagsfile)]
    except OSError:
        return 5
    
    
    art.tprint("DOTA 2")
    art.tprint("LOCALIZATION")
    art.tprint("CHANGER")
    art.tprint("@r41ngee")

    sleep(3)

    while True:
        cls()

        print("Действия:")
        print("0. ВЫХОД")
        print("1. Изменить героя")
        print("2. Загрузить пресет")
        print("3. Сохранить пресет")
        print("4. Сбросить настройки\n")

        action = input("Действие: ")

        match action:
            case "0":
                break
            case "1":
                while True:
                    cls()
                    table = [["0", "Выход", None]]
                    for i in herolist:
                        table.append([(herolist.index(i)+ 1), i.name, i.username])

                    print(tabulate.tabulate(table, headers=["ID", "Имя", "Кастомное имя"], missingval="N/A"))
                    try:
                        hero_input = int(input("Герой: "))
                    except ValueError:
                        logging.warning("Incorrect input in hero choice(non-integer)")
                        continue

                    if hero_input == 0:
                        break
                    
                    try:
                        current_hero = herolist[hero_input - 1]
                        logging.info(f"{current_hero.name} chosen")
                    except IndexError:
                        logging.warning("Incorrect input in hero choice(missindexed)")
                        continue

                    while True:
                        cls()

                        art.tprint(current_hero.name)

                        print("Действия:")
                        print("0. Выход")
                        print("1. Изменить имя")
                        print("2. Изменить названия способностей")
                        print("3. Изменить названия аспектов\n")

                        subact = input("Действие: ")

                        cls()

                        match subact:
                            case "0":
                                break
                            case "1":
                                select_name = input("Новое имя героя (пустая строка для сброса): ")
                                if select_name.strip() == "":
                                    current_hero.username = None
                                else:
                                    current_hero.username = select_name
                                logging.info(f"Name of hero {current_hero.name} is {current_hero.username} now")
                            case "2":
                                skilltable = [["0", "Выход", None]]
                                for i in current_hero.skills:
                                    skilltable.append([current_hero.skills.index(i) + 1, i.name, i.username])

                                print(tabulate.tabulate(skilltable, headers=["ID", "Имя", "Кастомное имя"], missingval="N/A"))
                                skill_choice = int(input("Ввод: "))

                                if skill_choice == 0:
                                    break

                                current_skill = current_hero.skills[skill_choice - 1]

                                select_skill = input("Новое название способности (пустая строка для сброса): ")
                                if select_skill.strip() == "":
                                    current_skill.username = None
                                else:
                                    current_skill.username = select_skill
                                logging.info(f"Name of skill {current_skill.name} is {current_skill.username} now")
                            case "3":
                                facettable = [["0", "Выход", None]]
                                for i in current_hero.facets:
                                    facettable.append([current_hero.facets.index(i) + 1, i.name, i.username])

                                print(tabulate.tabulate(facettable, headers=["ID", "Имя", "Кастомное имя"], missingval="N/A"))
                                facet_choice = int(input("Ввод: "))
                                
                                if facet_choice == 0:
                                    break

                                current_facet = current_hero.facets[facet_choice - 1]
                                select_facet = input("Новое название аспекта (пустая строка для сброса): ")
                                if select_facet.strip() == "":
                                    current_facet.username = None
                                else:
                                    current_facet.username = select_facet
                                logging.info(f"Name of facet {current_facet.name} is {current_facet.username} now")

            case "2":
                preset_filenames: list = Preset.load_names()
                table = [["0", "Выход"]]
                table += [[preset_filenames.index(name) + 1, name] for name in preset_filenames]
                print(tabulate.tabulate(table, missingval="N/A", headers=["Индекс", "Пресет"]))
                
                selected_preset_input = int(input("Выбранный пресет: "))
                if selected_preset_input == 0:
                    break

                selected_preset: Preset = Preset.load(preset_filenames[selected_preset_input - 1])

                herolist = selected_preset.heroes
                itemslist = selected_preset.items
            
            case "3":
                preset_name = input("Введите имя пресета(английские буквы, цифры и нижние подчеркивания): ")

                preset = Preset(preset_name, heroes=[i.toDict() for i in herolist])
                preset.save()

            case "4":
                for i in herolist:
                    i.username = None
                    for j in i.skills:
                        j.username = None
                    for j in i.facets:
                        j.username = None

                for i in itemslist:
                    i.username = None

                continue
            case _:
                print(f"Неверный ввод: {action}")
    
    cls()

    try:
        abil_file = open("data/abilities_russian.txt", "r", encoding='utf-8')
    except OSError as e:
        logging.error(e)
        return 2
    kv: dict = kvparser2.parse(abil_file.readlines())
    abil_file.close()

    for i in herolist:
        kv.update(i.ToKeyPair())

    for i in itemslist:
        kv.update(i.ToKeyPair())

    herotagsfile.seek(0)
    json.dump([i.toDict() for i in herolist], herotagsfile, indent=4, ensure_ascii=False)
    herotagsfile.truncate()
    herotagsfile.close()

    itemstagsfile.seek(0)
    json.dump([i.toDict() for i in itemslist], itemstagsfile, indent=4, ensure_ascii=False)
    itemstagsfile.truncate()
    itemstagsfile.close()

    with open("data/abilities_russian.txt", "w", encoding="utf-8") as f:
        f.write(kvparser2.unparse(kv))

    try:
        subprocess.run(
            [
                "bin/vpkeditcli.exe",
                "--remove-file",
                "resource/localization/abilities_russian.txt",
                VPK_PATH
            ],
            check=True,
        )
    except Exception:
        logging.warning("r/l/abilities does not exist")
        cls()

    try:
        subprocess.run([
            "bin/vpkeditcli.exe",
            "--add-file",
            "./data/abilities_russian.txt",
            "resource/localization/abilities_russian.txt",
            VPK_PATH
        ])
    except Exception:
        logging.error("")


if __name__=="__main__":
    result = 0
    try:
        result = main()
    except Exception as e:
        logging.error(e)
    if result is None:
        result = 0
    input("Нажмите ENTER чтобы выйти ")
    endlog(result)
