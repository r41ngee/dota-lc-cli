# -----------
# - r41ngee -
# -----------

# -BOX IMPORTS-
import logging
import subprocess
from time import sleep

# -REMOTE IMPORTS
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

def main():
    try:
        KVFILE = open("data/abilities_russian.txt", "r", encoding='utf-8')
    except OSError as e:
        logging.error(e)
        endlog(2)
        return
    
    try:
        DATAFILE = open("data/tags.json", "r", encoding='utf-8')
    except OSError as e:
        logging.error(e)
        endlog(4)
        return
    
    HEROLIST = [Hero(i) for i in json.load(DATAFILE)]
    
    art.tprint("DOTA 2")
    art.tprint("LOCALIZATION")
    art.tprint("CHANGER")
    art.tprint("@r41ngee")

    sleep(3)
    cls()

    while True:
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
                    for i in HEROLIST:
                        table.append([(HEROLIST.index(i)+ 1), i.name, i.username])

                    print(tabulate.tabulate(table, headers=["ID", "Имя", "Кастомное имя"], missingval="N/A"))
                    try:
                        hero_input = int(input("Герой: "))
                    except ValueError:
                        logging.warning("Incorrect input in hero choice(non-integer)")
                        continue

                    if hero_input == 0:
                        break
                    
                    try:
                        current_hero = HEROLIST[hero_input - 1]
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
                                skilltable = [["0", "Выход", None]]
                                for i in current_hero.skills:
                                    skilltable.append([current_hero.skills.index(i) + 1, i.name, i.username])

                                print(tabulate.tabulate(skilltable, headers=["ID", "Имя", "Кастомное имя"], missingval="N/A"))
                                skill_choice = int(input("Ввод: "))
                                current_skill = current_hero.skills[skill_choice - 1]
                                current_skill.username = input("Новое название способности: ")
                                logging.info(f"Name of skill {current_skill.name} is {current_skill.username} now")
                            case "3":
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
                for i in HEROLIST:
                    i.username = i.name

                continue
            case _:
                print(f"Неверный ввод: {action}")
    
    cls()

    kv: dict = kvparser2.parse(KVFILE.readlines())
    for i in HEROLIST:
        kv.update(i.ToKeyPair())

    KVFILE.close()

    with open("data/abilities_russian.txt", "w", encoding="utf-8") as f:
        f.write(kvparser2.unparse(kv))

    ...


if __name__=="__main__":
    main()
    input("Нажмите ENTER чтобы выйти")
    endlog(0)
