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
from dlctypes import *
from misc import *


logging.basicConfig(
    level=cfg["logger_lvl"],
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='.log',
    filemode='a'
)

VPK_PATH = cfg["dota_directory"] + "/game/dota_russian/pak01_dir.vpk"
INNER_VPK_PATH = "resource/localization/abilities_russian.txt"

def main() -> int:
    try:
        tagsfile = open("data/tags.json", "r+", encoding='utf-8')
        herolist = [Hero(i) for i in json.load(tagsfile)]
    except OSError as e:
        logging.error(e)
        return 2
    
    
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
        print("2. Изменить предметы(неактивно)")
        print("3. Сбросить настройки\n")

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
                                current_hero.username = input("Имя: ")
                                logging.info(f"Name of hero {current_hero.name} is {current_hero.username} now")
                            case "2":
                                print("Не работает")
                                sleep(2)
                                break
                                skilltable = [["0", "Выход", None]]
                                for i in current_hero.skills:
                                    skilltable.append([current_hero.skills.index(i) + 1, i.name, i.username])

                                print(tabulate.tabulate(skilltable, headers=["ID", "Имя", "Кастомное имя"], missingval="N/A"))
                                skill_choice = int(input("Ввод: "))
                                current_skill = current_hero.skills[skill_choice - 1]
                                current_skill.username = input("Новое название способности: ")
                                logging.info(f"Name of skill {current_skill.name} is {current_skill.username} now")
                            case "3":
                                print("Не работает")
                                sleep(2)
                                break
                                facettable = [["0", "Выход", None]]
                                for i in current_hero.facets:
                                    facettable.append([current_hero.facets.index(i) + 1, i.name, i.username])

                                print(tabulate.tabulate(facettable, headers=["ID", "Имя", "Кастомное имя"], missingval="N/A"))
                                facet_choice = int(input("Ввод: "))
                                current_facet = current_hero.facets[facet_choice - 1]
                                current_facet.username = input("Новое название аспекта: ")
                                logging.info(f"Name of facet {current_facet.name} is {current_facet.username} now")
                                
            case "2":
                print("Ну сказано же что неактивно")
                continue
            case "3":
                for i in herolist:
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

    tagsfile.seek(0)
    json.dump([i.toDict() for i in herolist], tagsfile, indent=4, ensure_ascii=False)
    tagsfile.truncate()
    tagsfile.close()

    with open("data/abilities_russian.txt", "w", encoding="utf-8") as f:
        f.write(kvparser2.unparse(kv))
        f.close()

    subprocess.run([
        "bin/vpkeditcli.exe",
        "--remove-file",
        "resource/localization/abilities_russian.txt",
        VPK_PATH
    ])

    subprocess.run([
        "bin/vpkeditcli.exe",
        "--add-file",
        "./data/abilities_russian.txt",
        "resource/localization/abilities_russian.txt",
        VPK_PATH
    ])


if __name__=="__main__":
    result = main()
    if result is None:
        result = 0
    input("Нажмите ENTER чтобы выйти ")
    endlog(result)
