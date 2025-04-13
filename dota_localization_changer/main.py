# -----------
# - r41ngee -
# -----------

import logging
from time import sleep

import art
# -----------
from config import *
from dlctypes import *
from misc import *

logging.basicConfig(
    level=cfg["logger_lvl"],
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='.log',
    filemode='w'
)

def main():
    try:
        KVFILE = open("data/abilities_russian.txt", "r")
    except OSError as e:
        logging.error(e)
        endlog(2)
        return
    
    try:
        DATAFILE = open("data/tags.json", "r")
    except OSError as e:
        logging.error(e)
        endlog(4)
        return
    
    HEROLIST = [Hero(i) for i in json.load(DATAFILE)]
    
    art.tprint("DOTA 2")
    art.tprint("LOCALIZATION")
    art.tprint("CHANGER")
    art.tprint("@r41ngee")

    sleep(5)
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
                    ...
            case "2":
                print("Ну сказано же что неактивно")
                continue
            case "3":
                for i in HEROLIST:
                    i.username = i.name

                continue
            case _:
                print(f"Неверный ввод: {action}")


if __name__=="__main__":
    main()
    input("Нажмите ENTER чтобы выйти")
    endlog(0)
