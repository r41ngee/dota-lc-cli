# -----------
# - r41ngee -
# -----------

# BOX IMPORTS
import json
import logging
from tkinter.filedialog import askdirectory

# REMOTE IMPORTS
import art
import dlctypes
import kvparser2

# LOCAL IMPORTS
from misc import *
from rich.console import Console
from tabulate import tabulate

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
    level=config_logger_level_dict[config["logger_lvl"]],
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='.log',
    filemode='w'
)

console = Console()

del config_logger_level_dict


def main():
    try:
        # READER
        with open("json/default_hero.json") as file:
            herolist = json.load(file)
        herolist = [dlctypes.Hero(i) for i in herolist]

        while True:  # Главный цикл меню
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

            choice = input("Ваш выбор: ")
            
            if choice == "0": 
                logging.info("Exit called")
                break
            
            elif choice == "1":
                while True:  # Цикл меню изменения героя
                    clear_console()
                    tab = []
                    # Добавляем пункт "Назад" с номером 0
                    tab.append([0, "Назад"])
                    # Герои нумеруются с 1
                    for i, hero in enumerate(herolist, start=1):
                        tab.append([i, hero.name])

                    print(tabulate(tab, tablefmt="grid", headers=["ЧИСЛО", "ГЕРОЙ"]))

                    hero_choice = input("\nВаш выбор: ")
                    
                    if hero_choice == "0":
                        break  # Возврат в главное меню
                    
                    try:
                        hero_index = int(hero_choice) - 1  # Преобразуем в индекс (1-based -> 0-based)
                        if 0 <= hero_index < len(herolist):
                            hero = herolist[hero_index]

                            while True:  # Цикл меню действий с героем
                                clear_console()
                                art.tprint(hero.name)
                                print("0. Назад")
                                print("1. Изменить имя")
                                print("2. Изменить способности")
                                print("3. Изменить аспекты\n")

                                action = input("Действие: ")
                                
                                if action == "0":
                                    break  # Возврат к выбору героя
                                    
                                elif action == "1":
                                    hero.name = "#|m|#" + input("Ваше имя: ")
                                    keylog(hero.key, hero.name)
                                    input("\nИзменения сохранены. Нажмите ENTER чтобы продолжить")
                                    
                                elif action == "2":
                                    while True:  # Цикл изменения способностей
                                        clear_console()
                                        skills = []
                                        skills.append([0, "Назад"])
                                        for i, skill in enumerate(hero.skills, start=1):
                                            skills.append([i, skill.name])

                                        print(tabulate(skills, tablefmt="grid", headers=["ЧИСЛО", "СПОСОБНОСТЬ"]))

                                        skill_choice = input("Ваш выбор: ")
                                        if skill_choice == "0":
                                            break
                                            
                                        try:
                                            skill_index = int(skill_choice) - 1
                                            if 0 <= skill_index < len(hero.skills):
                                                skill = hero.skills[skill_index]
                                                skill.name = input("Введите название: ")
                                                keylog(skill.key, skill.name)
                                                input("\nИзменения сохранены. Нажмите ENTER чтобы продолжить")
                                            else:
                                                input("\nНеверный номер. Нажмите ENTER чтобы продолжить")
                                        except ValueError:
                                            input("\nНеверный ввод. Нажмите ENTER чтобы продолжить")
                                            
                                elif action == "3":
                                    while True:  # Цикл изменения аспектов
                                        clear_console()
                                        facets = []
                                        facets.append([0, "Назад"])
                                        for i, facet in enumerate(hero.facets, start=1):
                                            facets.append([i, facet.name])

                                        print(tabulate(facets, headers=["ЧИСЛО", "АСПЕКТ"], tablefmt="grid"))
                                        facet_choice = input("Ваш выбор: ")
                                        if facet_choice == "0":
                                            break
                                            
                                        try:
                                            facet_index = int(facet_choice) - 1
                                            if 0 <= facet_index < len(hero.facets):
                                                facet = hero.facets[facet_index]
                                                facet.name = input("Выберите имя аспекта: ")
                                                keylog(facet.key, facet.name)
                                                input("\nИзменения сохранены. Нажмите ENTER чтобы продолжить")
                                            else:
                                                input("\nНеверный номер. Нажмите ENTER чтобы продолжить")
                                        except ValueError:
                                            input("\nНеверный ввод. Нажмите ENTER чтобы продолжить")
                                else:
                                    input("\nНеверный выбор. Нажмите ENTER чтобы продолжить")
                        else:
                            input("\nНеверный номер героя. Нажмите ENTER чтобы продолжить")
                    except ValueError:
                        input("\nНеверный ввод. Нажмите ENTER чтобы продолжить")
            
            elif choice == "2":
                clear_console()
                herolist = herolist
                print("Сброс данных завершен.")
                input("\nНажмите ENTER чтобы продолжить")
                
            else:
                logging.error("Неверный ввод")
                input("\nНеверный выбор. Нажмите ENTER чтобы продолжить")
                
    except Exception as e:
        logging.error(e)
        endlog(1)
        raise Exception()
    finally:
        allkeys = {}
        for i in herolist:
            allkeys.update(i.ToKeyPair())

        with open("abilities_russian.txt", "r+", encoding="utf-8") as file:
            lines = file.readlines()

            abilities = kvparser2.parse(lines)
            abilities.update(allkeys)

            file.seek(0)
            file.truncate()

            file.write(kvparser2.unparse(abilities))

if __name__=="__main__":
    main()
    input("Нажмите ENTER чтобы выйти")
    endlog(0)
