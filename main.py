import json
import logging
from tkinter.filedialog import askdirectory

import art
import vpk
from tabulate import tabulate

import dlctypes
import keyparser2
from misc import *

with open("json/config.json", "r") as f:
    config = json.load(f)

config_logger_level_dict = {
    "info": logging.INFO,
    "error": logging.ERROR,
    "debug": logging.DEBUG,
    "warning": logging.WARNING,
    "warn": logging.WARN
}

logging.basicConfig(
    level=config_logger_level_dict[config["logger_lvl"]],  # МЕНЯТЬ на info
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Формат сообщения
    filename='.log',  # Имя файла для записи логов
    filemode='w'  # Режим записи в файл ('a' - добавление, 'w' - перезапись)
)

del config_logger_level_dict


def main():
    try:
        # READER
        with open("json/user_hero.json") as file:
            herolist = json.load(file)
        herolist = [dlctypes.Hero(i) for i in herolist]

        with open("json/default_hero.json") as file:
            def_herolist = json.load(file)
        def_herolist = [dlctypes.Hero(i) for i in def_herolist]

        # WELCOME
        clear_console()

        art.tprint("DOTA 2")
        art.tprint("LOCALIZATION")
        art.tprint("CHANGER")
        print("\n\n")
        art.tprint("by")
        art.tprint("r41ngee")

        print("\n")

        print("0. Выход")
        print("1. Изменить героя")
        print("2. Сброс настроек\n")

        match input("Ваш выбор: "):
            case "0": 
                logging.info("Exit called")
                return
            case "1":
                clear_console()
                tab = []
                for i in def_herolist:
                    tab.append([def_herolist.index(i), i.name])

                print(tabulate(tab, tablefmt="grid", headers=["ЧИСЛО", "ГЕРОЙ"]))

                hero = herolist[int(input("\nВаш герой: "))] 

                art.tprint(hero.name)
                print("1. Изменить имя")
                print("2. Изменить способности")
                print("3. Изменить аспекты")

                match input("\nДействие: "):
                    case "1":
                        hero.name = "#|m|#" + input("Ваше имя: ")
                        keylog(hero.key, hero.name)
                    case "2":
                        skills = []
                        for i in hero.skills:
                            skills.append([hero.skills.index(i), i.name])

                        print(tabulate(skills, tablefmt="grid", headers=["ЧИСЛО", "СПОСОБНОСТЬ"]))

                        skill = hero.skills[int(input("Ваша способность: "))]
                        skill.name = input("Введите название: ")
                        keylog(skill.key, skill.name)

                    case "3":
                        facets = []
                        for i in hero.facets:
                            facets.append([hero.facets.index(i), i.name])

                        print(tabulate(facets, headers=["ЧИСЛО", "АСПЕКТ"], tablefmt="grid"))

                        facet = hero.facets[int(input("Ваш аспект: "))]
                        facet.name = input("Выберите имя аспекта: ")
                        keylog(facet.key, facet.name)
            case "2":
                clear_console()
                herolist = def_herolist
                print("Сброс данных завершен.")
            case _:
                logging.error("Неверный ввод")
    except Exception as e:
        logging.error(e)
        endlog(1)
    finally:
        with open("json/user_hero.json", "w") as file:
            json.dump([i.desc for i in herolist], file, indent=4)

        allkeys = {}
        for i in herolist:
            allkeys.update(i.ToKeyPair())

        with open("abilities_russian.txt", "r+", encoding="utf-8") as file:
            lines = file.readlines()

            abilities = keyparser2.parse(lines)
            
            abilities.update(allkeys)

            file.seek(0)
            file.truncate()

            file.write(keyparser2.unparse(abilities))

if __name__=="__main__":
    main()
    input("Нажмите ENTER чтобы выйти")
    endlog(0)
